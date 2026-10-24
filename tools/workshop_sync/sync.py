"""WS-SYNC-001: local main-push worker; one release at a time, durable progress, no browser."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import sys
import time
import uuid

from common import read_json, sha256, write_json, WorkerLock
from git_source import GitSource
from release import prepare, is_release_input, validate_payload
from steam import Steam, SubmissionUnknown, ITEM_ID

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def relevant(path):
    return is_release_input(path)


def metadata_with_marker(current, marker):
    try:
        obj = json.loads(current) if current else {}
        if not isinstance(obj, dict):
            obj = {'previous_metadata': obj}
    except ValueError:
        obj = {'previous_metadata': current}
    obj['workshop_sync'] = marker
    encoded = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
    if len(encoded.encode()) >= 5000:
        raise ValueError('Existing Steam metadata leaves no room for a release checkpoint')
    return encoded


def marker_of(details):
    try:
        value = json.loads(details['metadata'])
        return value.get('workshop_sync', {}) if isinstance(value, dict) else {}
    except ValueError:
        return {}


def normalized(text):
    return text.replace('\r\n', '\n').strip()


def verify_phase(details, release, phase):
    if phase == 'assets':
        names = [Path(p['path']).name for p in release['images']]
        heroes = {p['hero'] for p in release['images']}
        found = [p['filename'] for p in details['previews'] if any(
            re.fullmatch(r'\d{2}_' + re.escape(h) + r'(?:_p[12])?\.png', p['filename']) for h in heroes)]
        if found != names:
            raise ValueError('Uploaded preview list does not match the prepared release')
        desc = next(d for d in release.get('descriptions', []) if d['language'] == 'english') if release.get('descriptions') else None
    else:
        desc = next(d for d in release['descriptions'] if d['language'] == phase)
    if desc and (normalized(details['description']) != normalized(desc['body']) or details['title'] != desc['title']):
        raise ValueError('Steam description read-back mismatch: ' + phase)


def publish(config, job, release, images_only=False, metadata_only=False):
    journal_path = job / 'publish-state.json'
    journal = read_json(journal_path, {'digest': release['digest'], 'completed': [], 'phase': None, 'status': 'ready'})
    if journal['digest'] != release['digest']:
        raise ValueError('Prepared release changed after a publish attempt')
    image_dir = Path(release.get('image_dir', job / 'images')).resolve()
    if not image_dir.is_relative_to(job.resolve()):
        raise ValueError('Image directory must belong to this release job')
    for image in release['images']:
        path = image_dir / image['path']
        if path.resolve().parent != image_dir or sha256(path) != image['sha256']:
            raise ValueError('Prepared image changed before publication')
    if not images_only and not metadata_only and validate_payload(Path(release['payload'])) != release['payload_hashes']:
        raise ValueError('Prepared payload changed before publication')
    with Steam(config['game_root'], release['item_id']) if 'item_id' in release else Steam(config['game_root']) as steam:
        initial = steam.query()
        write_json(job / 'steam-before.json', initial)
        if not initial['owned']:
            raise ValueError('Active Steam account does not own the configured Workshop item')
        # The specific source-known hero filenames are ours; unrelated images/videos survive.
        heroes = {p['hero'] for p in release['images']}
        old_names = {p['filename'] for p in initial['previews'] if any(
            re.fullmatch(r'\d{2}_' + re.escape(h) + r'(?:_p[12])?\.png', p['filename']) for h in heroes)}
        phases = ['assets'] + ([] if images_only else [d['language'] for d in release['descriptions'] if d['language'] != 'english'])
        for phase in phases:
            if phase in journal['completed']:
                continue
            lang = 'english' if phase == 'assets' else phase
            current = steam.query(lang)
            marker = marker_of(current)
            if journal['status'] in ('submitting', 'unknown'):
                # WS-SYNC-002: reconcile server-side checkpoint before ever repeating a change note.
                if journal['phase'] != phase or marker.get('digest') != release['digest'] or phase not in marker.get('completed', []):
                    raise SubmissionUnknown('Previous submit may have succeeded. Remote checkpoint is inconclusive; no duplicate submission was sent.')
                verify_phase(current, release, phase)
                journal['completed'].append(phase)
                journal.update(status='ready', phase=None, updated=now())
                write_json(journal_path, journal)
                continue
            completed = journal['completed'] + [phase]
            marker = {'digest': release['digest'], 'source_sha': release['source_sha'], 'completed': completed, 'at': now()}
            kwargs = {'language': lang, 'metadata': metadata_with_marker(current['metadata'], marker)}
            if phase == 'assets':
                kwargs['replace_previews'] = (old_names, [image_dir / p['path'] for p in release['images']])
                if not images_only and not metadata_only:
                    kwargs.update(content=release['payload'], thumbnail=Path(release['payload']) / 'preview_icon.png', note=release['note'])
                    if 'item_id' in release and release['item_id'] != ITEM_ID:
                        kwargs['visibility'] = 0
            if not images_only:
                desc = next(d for d in release['descriptions'] if d['language'] == lang)
                kwargs.update(description=desc['body'], title=desc['title'])

            def before_submit():
                journal.update(phase=phase, status='submitting', updated=now())
                write_json(journal_path, journal)

            try:
                result = steam.update(**kwargs, before_submit=before_submit)
                verify_phase(result, release, phase)
                if marker_of(result).get('digest') != release['digest']:
                    raise SubmissionUnknown('Release checkpoint was not visible after submission')
            except Exception:
                if journal['status'] == 'submitting':
                    journal['status'] = 'unknown'
                    write_json(journal_path, journal)
                raise
            journal['completed'].append(phase)
            journal.update(phase=None, status='ready', updated=now())
            write_json(journal_path, journal)
        journal.update(status='complete', updated=now())
        write_json(journal_path, journal)
        write_json(job / 'steam-after.json', steam.query())
    return journal


def once(config, publish_enabled=False, expected_sha=None):
    root = Path(config['state_dir']).resolve()
    git = GitSource(root)
    state_path = root / 'state.json'
    state = read_json(state_path)
    remote = git.remote_sha()
    if expected_sha is not None and remote != expected_sha:
        raise RuntimeError('Remote main changed after the push event; retry the intended release explicitly')
    if not state:
        raise RuntimeError('Initialize the existing main baseline before starting the watcher')
    if remote == state.get('last_seen_sha') and not state.get('pending_sha'):
        return 'idle'
    sha = git.fetch()
    if expected_sha is not None and sha != expected_sha:
        raise RuntimeError('Remote main changed during fetch; no publication was started')
    previous = state['last_published_sha']
    git.ensure_forward(previous, sha)
    if state.get('pending_sha') and state['pending_sha'] != sha:
        # WS-SYNC-003: never publish a queued commit removed from remote main.
        # A newer descendant can follow it; rewritten history requires reconciliation.
        git.ensure_forward(state['pending_sha'], sha)
        sha = state['pending_sha']
    changed = git.changed_files(previous, sha)
    if not any(relevant(p) for p in changed):
        state.update(last_seen_sha=sha, checked_at=now())
        write_json(state_path, state)
        return 'no player-facing change'
    job = root / 'jobs' / sha
    job.mkdir(parents=True, exist_ok=True)
    release = read_json(job / 'release.json')
    if release is None:
        release = prepare(config, git, previous, sha, job, state.get('last_release'))
    # WS-MODULAR-001: validate all packages before writing any Workshop item.
    registry = read_json(job / 'source/design/workshop/modules.json')
    module_releases = {}
    if registry:
        from modules import prepare_modules
        module_releases = prepare_modules(config, job, release, registry)
    if not publish_enabled:
        return 'prepared ' + str(job / 'release.json')
    if (root / 'stop.request').exists():
        return 'prepared; stop requested before publication'
    state.update(pending_sha=sha, checked_at=now())
    write_json(state_path, state)
    for key, module_release in module_releases.items():
        if key != 'base':
            # Steam's required-item link is idempotent; persist its confirmed callback.
            dependency_path = job / 'modules' / key / 'dependency.json'
            if not dependency_path.exists():
                with Steam(config['game_root'], module_release['item_id']) as steam:
                    dependency = steam.add_dependency(module_releases['base']['item_id'])
                write_json(dependency_path, dependency)
        publish(config, job / 'modules' / key, module_release)
    publish(config, job, release)
    state.update(last_published_sha=sha, last_seen_sha=sha, pending_sha=None,
                 last_release={'version': release['version'], 'digest': release['digest'], 'job': str(job)},
                 published_at=now(), last_error=None)
    write_json(state_path, state)
    return 'published ' + release['version'] + ' @ ' + sha


def bootstrap(config):
    root = Path(config['state_dir']).resolve()
    if (root / 'state.json').exists():
        raise RuntimeError('Baseline already exists; do not overwrite release history')
    git = GitSource(root)
    sha = git.fetch()
    source = git.snapshot(sha, root / 'jobs' / ('baseline-' + sha[:12]))
    notes = sorted((source / 'design/workshop/changenotes').glob('*.txt'))
    match = re.search(r'Update (\d+\.\d+(?:\.\d+)?)', notes[-1].read_text(encoding='utf-8')) if notes else None
    if not match:
        raise ValueError('Cannot establish the existing published version')
    # Existing main is the user-established published branch. Do not replay old changes.
    write_json(root / 'state.json', {'last_published_sha': sha, 'last_seen_sha': sha,
               'pending_sha': None, 'last_release': {'version': match.group(1)},
               'baseline_kind': 'existing-main-no-historical-replay', 'created_at': now()})
    return sha


def image_refresh(config, publish_enabled=False, reconcile=False):
    from cards import render_cards
    from release import descriptions
    root = Path(config['state_dir']).resolve()
    git = GitSource(root)
    sha = git.fetch()
    state = read_json(root / 'state.json', {})
    if sha != state.get('last_published_sha'):
        raise ValueError('Publish pending main changes before refreshing the live gallery')
    job = root / 'jobs' / (('reconcile-' if reconcile else 'images-') + sha + '-' + sha256(ROOT / 'cards.py')[:12])
    job.mkdir(parents=True, exist_ok=True)
    source = git.snapshot(sha, job)
    release = read_json(job / 'release.json')
    if release is None:
        # WS-CARD-003: Git stores original editorial input; use the successfully
        # published generated cards so image-only repairs cannot revert new stats.
        from release import inherit_published_editorial
        inherit_published_editorial(source, git, sha, sha, state.get('last_release'), job)
        image_dir = job / ('images-' + uuid.uuid4().hex[:12])
        images = render_cards(read_json(source / 'design/workshop/hero_cards.json'), Path(config['game_root']), image_dir, max_height=config.get('max_image_height', 1500))
        release = {'source_sha': sha, 'images': images, 'image_dir': str(image_dir),
                   'descriptions': list(descriptions(source).values()) if reconcile else []}
        release['digest'] = hashlib.sha256(json.dumps(release, sort_keys=True).encode()).hexdigest()
        write_json(job / 'release.json', release)
    if publish_enabled:
        publish(config, job, release, images_only=not reconcile, metadata_only=reconcile)
    return str(job / 'release.json')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', default=str(ROOT / 'config.json'))
    p.add_argument('command', choices=['inspect', 'baseline', 'once', 'images', 'reconcile', 'status', 'stop'])
    p.add_argument('--publish', action='store_true', help='Enable actual writes to the fixed Workshop item')
    args = p.parse_args(argv)
    config = read_json(args.config)
    if not config:
        p.error('Config file is missing')
    root = Path(config['state_dir']).resolve()
    root.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=root / 'worker.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8')
    if args.command == 'stop':
        (root / (args.command + '.request')).write_text(now())
        return
    if args.command == 'status':
        print(json.dumps(read_json(root / 'state.json', {}), ensure_ascii=False, indent=2))
        return
    if args.command == 'inspect':
        with Steam(config['game_root']) as steam:
            result = steam.query()
        write_json(root / 'steam-inspection.json', result)
        print(json.dumps({k: result[k] for k in ('item_id', 'owned', 'title', 'updated')}, ensure_ascii=False))
        return
    with WorkerLock(root / 'worker.lock'):
        if args.command == 'baseline':
            print(bootstrap(config))
        elif args.command in ('images', 'reconcile'):
            print(image_refresh(config, args.publish, reconcile=args.command == 'reconcile'))
        elif args.command == 'once':
            print(once(config, args.publish))


if __name__ == '__main__':
    main()
