"""WS-PUSH-001: poll the remote main ref, not commits, chat text, or the live test checkout."""
from pathlib import Path, PurePosixPath
import re
import tarfile

from common import REMOTE, run

SHA = re.compile(r'^[0-9a-f]{40}$')


class GitSource:
    def __init__(self, state_dir):
        self.root = Path(state_dir).resolve()
        self.repo = self.root / 'cache.git'

    def git(self, *args, timeout=180):
        return run(['git', '-c', 'core.hooksPath=' + str(self.root / 'disabled-hooks'), '--git-dir=' + str(self.repo), *args], timeout=timeout)

    def remote_sha(self):
        out = run(['git', 'ls-remote', '--refs', REMOTE, 'refs/heads/main'], timeout=60)
        rows = [r.split() for r in out.splitlines() if r.strip()]
        if len(rows) != 1 or rows[0][1] != 'refs/heads/main' or not SHA.fullmatch(rows[0][0]):
            raise RuntimeError('Could not identify the single remote main commit')
        return rows[0][0]

    def fetch(self):
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.repo.exists():
            run(['git', 'init', '--bare', self.repo])
            self.git('remote', 'add', 'origin', REMOTE)
        if self.git('remote', 'get-url', 'origin').strip() != REMOTE:
            raise RuntimeError('Unexpected origin in private build cache')
        self.git('fetch', '--no-tags', 'origin', '+refs/heads/main:refs/heads/observed-main', timeout=300)
        return self.git('rev-parse', 'refs/heads/observed-main').strip()

    def ensure_forward(self, previous, current):
        for value in (previous, current):
            if not SHA.fullmatch(value):
                raise ValueError('Invalid source SHA')
        try:
            self.git('merge-base', '--is-ancestor', previous, current)
        except RuntimeError as e:
            raise RuntimeError('Remote history was rewritten. Reconcile the release baseline before publishing.') from e

    def changed_files(self, previous, current):
        return self.git('diff', '--name-only', previous, current).splitlines()

    def diff(self, previous, current):
        return self.git('diff', '--no-ext-diff', '--unified=5', previous, current, '--',
                        'heroes', 'effects', 'shared', 'trinkets', 'localization',
                        'design/changes', 'design/workshop/why.json', 'design/workshop/intents',
                        'design/workshop/changes.json', 'design/workshop/workshop.effects.darkest',
                        'design/workshop/workshop.buffs.json', 'design/workshop/hero_cards.json',
                        'design/workshop/description_*.txt', 'design/workshop/i18n/*.txt',
                        'design/workshop/project.template.xml', 'design/workshop/cards/preview.png')

    def snapshot(self, sha, job):
        if not SHA.fullmatch(sha):
            raise ValueError('Invalid source SHA')
        job = Path(job).resolve()
        source = job / 'source'
        marker = job / 'source-sha.txt'
        if source.exists():
            if marker.exists() and marker.read_text().strip() == sha:
                return source
            raise RuntimeError('Partial or mismatched source snapshot; preserve it for inspection')
        job.mkdir(parents=True, exist_ok=True)
        archive = job / 'source.tar'
        self.git('archive', '--format=tar', '--output=' + str(archive), sha, timeout=300)
        source.mkdir()
        with tarfile.open(archive) as tar:
            for entry in tar:
                rel = PurePosixPath(entry.name)
                if rel.is_absolute() or '..' in rel.parts or '\\' in entry.name or ':' in entry.name:
                    raise ValueError('Unsafe archive path')
                if entry.isdir():
                    continue
                if not entry.isfile():
                    raise ValueError('Links/special files are not allowed in build snapshots')
                if entry.name.startswith('design/workshop/cards_history/'):
                    continue  # Historical media remain in Git; only this release's images are staged.
                path = source.joinpath(*rel.parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(entry) as src, path.open('wb') as dst:
                    import shutil
                    shutil.copyfileobj(src, dst)
        marker.write_text(sha + '\n')
        archive.unlink()  # The private Git object store and extracted SHA snapshot already preserve the source.
        return source
