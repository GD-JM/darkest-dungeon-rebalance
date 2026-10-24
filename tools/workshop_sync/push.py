"""WS-PUSH-002: explicit local push event; main publication runs under one lock."""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
import uuid

import common
from common import WorkerLock, read_json, run, write_json
from sync import once

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def push(config, repo, branch):
    """Return an exit code, preserving Git success independently of deployment."""
    root = Path(config['state_dir']).resolve()
    receipt_path = root / 'events' / (uuid.uuid4().hex + '.json')
    receipt = dict(timestamp=now(), sha=None, branch=branch,
                   git_push_success=False, deployment_result=None, error=None,
                   status='validating')

    def save():
        receipt['updated_at'] = now()
        write_json(receipt_path, receipt)

    def health(ok):
        write_json(root / 'health.json', dict(
            ok=ok, at=now(), source='push', branch=branch, sha=receipt['sha'],
            git_push_success=receipt['git_push_success'],
            result=receipt['deployment_result'], error=receipt['error'],
            event=str(receipt_path)))

    acquired = False
    with ExitStack() as locks:
        try:
            locks.enter_context(WorkerLock(root / 'worker.lock'))
            acquired = True
            save()  # Refuse to push if the private event log cannot be written.
            if branch not in ('main', 'test'):
                raise ValueError('Only main or test may be pushed')
            repo = Path(repo).resolve(strict=True)
            if not repo.is_dir():
                raise ValueError('Repository must be a local directory')

            def git(*args):
                return run(['git', '-C', str(repo), '-c', 'core.hooksPath=' + str(root / 'disabled-hooks'),
                            '-c', 'remote.origin.mirror=false', *args], timeout=300)

            # Check every effective fetch/push URL, including pushurl and URL rewrites.
            for args in [('remote', 'get-url', '--all', 'origin'),
                         ('remote', 'get-url', '--push', '--all', 'origin')]:
                if git(*args).splitlines() != [common.REMOTE]:
                    raise ValueError('origin must have exactly the fixed repository URL')
            sha = git('rev-parse', '--verify', 'refs/heads/' + branch + '^{commit}').strip()
            if not re.fullmatch(r'[0-9a-f]{40}', sha):
                raise ValueError('Invalid local branch commit SHA')
            receipt.update(sha=sha, status='pushing')
            save()
            # Explicit immutable source/ref, no force, deletion, tags, or configured mirror.
            git('push', '--porcelain', '--no-follow-tags', 'origin', sha + ':refs/heads/' + branch)
            receipt.update(git_push_success=True, status='pushed')
            save()  # A publication crash must not erase the successful Git event.
            if branch == 'test':
                receipt.update(deployment_result='skipped: test branch', status='complete')
            else:
                rows = [line.split() for line in git('ls-remote', '--refs', 'origin', 'refs/heads/main').splitlines() if line.strip()]
                if rows != [[sha, 'refs/heads/main']]:
                    raise RuntimeError('Remote main no longer equals the captured push SHA; deployment refused')
                # Only this explicit, successful, verified main push clears a legacy stop.
                (root / 'stop.request').unlink(missing_ok=True)
                receipt['status'] = 'deploying'
                save()
                receipt['deployment_results'] = []
                for _ in range(2):
                    result = once(config, True, expected_sha=sha)
                    receipt['deployment_result'] = result
                    receipt['deployment_results'].append(result)
                    save()
                    if not isinstance(result, str) or not (result in ('idle', 'no player-facing change') or result.startswith('published ')):
                        raise RuntimeError('Deployment did not complete: ' + str(result))
                    state = read_json(root / 'state.json', {})
                    if isinstance(state, dict) and state.get('last_seen_sha') == sha and not state.get('pending_sha'):
                        break
                else:
                    raise RuntimeError('Deployment did not reach the requested SHA with no pending release after two attempts')
                receipt['status'] = 'complete'
            save()
            health(True)
            print('Git push succeeded (' + branch + ' @ ' + sha + '). Deployment: ' + receipt['deployment_result'])
            return 0
        except Exception as exc:
            receipt.update(status='failed', error=str(exc))
            try:
                save()
            except Exception as log_error:
                print('Could not persist event receipt: ' + str(log_error), file=sys.stderr)
            if acquired:
                try:
                    health(False)
                except Exception as health_error:
                    print('Could not persist health outcome: ' + str(health_error), file=sys.stderr)
            if receipt['git_push_success']:
                print('Git push succeeded; deployment/event processing failed: ' + str(exc) +
                      '. Rerun the same push command to retry, including when up-to-date.', file=sys.stderr)
            else:
                print('Git push did not succeed; deployment was not started: ' + str(exc), file=sys.stderr)
            return 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--repo', required=True, help='Local repository directory')
    parser.add_argument('--branch', required=True, choices=('main', 'test'))
    parser.add_argument('--config', default=str(ROOT / 'config.json'))
    args = parser.parse_args(argv)
    config = read_json(args.config)
    if not isinstance(config, dict) or not config.get('state_dir'):
        parser.error('Config must specify the private runtime state_dir')
    return push(config, args.repo, args.branch)


if __name__ == '__main__':
    sys.exit(main())
