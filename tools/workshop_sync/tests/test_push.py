import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import push
import sync
from common import REMOTE, read_json, write_json

SHA = 'a' * 40


class PushTests(unittest.TestCase):
    def setUp(self):
        area = push.ROOT / 'test-tmp'
        area.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=area)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.runtime = self.root / 'runtime'
        self.runtime.mkdir()
        self.config = {'state_dir': str(self.runtime)}
        self.stop = self.runtime / 'stop.request'
        self.stop.write_text('legacy stop')
        self.commands = []
        self.locked = False
        self.remote = SHA + '\trefs/heads/main\n'
        self.urls = [REMOTE + '\n', REMOTE + '\n']
        self.push_error = None
        owner = self

        class Lock:
            def __init__(self, path):
                owner.assertEqual(path, owner.runtime / 'worker.lock')
            def __enter__(self):
                owner.locked = True
            def __exit__(self, *_):
                owner.locked = False

        self.enter_context = contextlib.ExitStack()
        self.addCleanup(self.enter_context.close)
        self.enter_context.enter_context(patch('push.WorkerLock', Lock))
        self.runner = self.enter_context.enter_context(patch('push.run', side_effect=self.git))
        self.publisher = self.enter_context.enter_context(patch('push.once', side_effect=self.publish))
        self.output = io.StringIO()
        self.enter_context.enter_context(contextlib.redirect_stdout(self.output))
        self.enter_context.enter_context(contextlib.redirect_stderr(self.output))

    def receipts(self):
        return [read_json(p) for p in (self.runtime / 'events').glob('*.json')]

    def git(self, argv, **kwargs):
        self.assertTrue(self.locked)
        self.commands.append(argv)
        if 'get-url' in argv:
            return self.urls[1 if '--push' in argv else 0]
        if 'rev-parse' in argv:
            return SHA + '\n'
        if 'push' in argv:
            if self.push_error:
                raise RuntimeError(self.push_error)
            return '= up to date\n'
        if 'ls-remote' in argv:
            return self.remote
        raise AssertionError(argv)

    def publish(self, config, enabled, *, expected_sha):
        self.assertTrue(self.locked)
        self.assertEqual(config, self.config)
        self.assertIs(enabled, True)
        self.assertEqual(expected_sha, SHA)
        self.assertFalse(self.stop.exists())
        receipt = self.receipts()[-1]
        self.assertTrue(receipt['git_push_success'])
        self.assertEqual(receipt['sha'], SHA)
        write_json(self.runtime / 'state.json', dict(last_seen_sha=SHA, pending_sha=None))
        return 'published 1.0 @ ' + SHA

    def execute(self, branch='main'):
        return push.push(self.config, self.repo, branch)

    def test_main_push_exact_sha_under_lock_and_durable_success(self):
        self.assertEqual(self.execute(), 0)
        cmd = next(c for c in self.commands if 'push' in c)
        self.assertEqual(cmd[-5:], ['push', '--porcelain', '--no-follow-tags', 'origin', SHA + ':refs/heads/main'])
        self.assertIn('remote.origin.mirror=false', cmd)
        self.assertTrue(any(c.startswith('core.hooksPath=') for c in cmd))
        self.publisher.assert_called_once_with(self.config, True, expected_sha=SHA)
        r = self.receipts()[0]
        self.assertEqual((r['branch'], r['sha'], r['status']), ('main', SHA, 'complete'))
        self.assertIsNone(r['error'])
        self.assertTrue(r['timestamp'])
        self.assertFalse(self.locked)

    def test_failed_push_never_deploys_or_clears_stop(self):
        self.push_error = 'rejected non-fast-forward'
        self.assertEqual(self.execute(), 1)
        self.publisher.assert_not_called()
        self.assertTrue(self.stop.exists())
        self.assertFalse(self.receipts()[0]['git_push_success'])
        self.assertFalse(any('ls-remote' in c for c in self.commands))

    def test_test_success_never_deploys_or_checks_main_or_clears_stop(self):
        self.assertEqual(self.execute('test'), 0)
        self.publisher.assert_not_called()
        self.assertTrue(self.stop.exists())
        self.assertFalse(any('ls-remote' in c for c in self.commands))
        self.assertEqual(self.receipts()[0]['deployment_result'], 'skipped: test branch')

    def test_changed_or_ambiguous_remote_ref_refuses_deployment(self):
        for remote in ['b'*40 + '\trefs/heads/main', '', SHA + '\trefs/heads/test', self.remote * 2]:
            with self.subTest(remote=remote):
                self.remote = remote
                self.assertEqual(self.execute(), 1)
                self.assertTrue(self.stop.exists())
        self.publisher.assert_not_called()
        self.assertTrue(all(r['git_push_success'] for r in self.receipts()))

    def test_deployment_failure_keeps_git_success_and_prints_retry(self):
        self.publisher.side_effect = RuntimeError('Steam unavailable')
        self.assertEqual(self.execute(), 1)
        r = self.receipts()[0]
        self.assertTrue(r['git_push_success'])
        self.assertEqual(r['error'], 'Steam unavailable')
        self.assertIn('Git push succeeded; deployment/event processing failed', self.output.getvalue())
        self.assertIn('Rerun the same push command', self.output.getvalue())

    def test_up_to_date_retry_processes_pending_and_keeps_unique_receipts(self):
        def retry(config, enabled, *, expected_sha):
            if self.publisher.call_count == 1:
                raise RuntimeError('temporary')
            write_json(self.runtime / 'state.json', dict(last_seen_sha=SHA, pending_sha=None))
            return 'published 1.0 @ ' + SHA if self.publisher.call_count == 2 else 'idle'
        self.publisher.side_effect = retry
        self.assertEqual(self.execute(), 1)
        self.assertEqual(self.execute(), 0)
        self.assertEqual(self.execute(), 0)
        self.assertEqual(self.publisher.call_count, 3)
        self.assertEqual(len(self.receipts()), 3)
        self.assertEqual(sum(r['status'] == 'complete' for r in self.receipts()), 2)

    def test_stopped_or_only_prepared_result_is_failure(self):
        self.publisher.side_effect = None
        self.publisher.return_value = 'prepared; stop requested before publication'
        self.assertEqual(self.execute(), 1)
        self.assertIn('stop requested', self.receipts()[0]['deployment_result'])

    def test_no_player_facing_change_is_success(self):
        write_json(self.runtime / 'state.json', dict(last_seen_sha=SHA, pending_sha=None))
        self.publisher.side_effect = None
        self.publisher.return_value = 'no player-facing change'
        self.assertEqual(self.execute(), 0)

    def test_wrong_or_multiple_fetch_and_push_urls_rejected(self):
        for index in (0, 1):
            for value in ['https://example.com/repo.git\n', REMOTE + '\nhttps://example.com/other\n']:
                with self.subTest(index=index, value=value):
                    self.urls = [REMOTE+'\n', REMOTE+'\n']
                    self.urls[index] = value
                    self.assertEqual(self.execute(), 1)
        self.assertFalse(any('push' in c for c in self.commands))
        self.publisher.assert_not_called()
        self.assertTrue(self.stop.exists())

    def test_invalid_branch_rejected_before_git(self):
        for branch in ['--force', ':main', '+main', 'main:other', 'refs/heads/main', 'other', 'https://example.com']:
            self.assertEqual(self.execute(branch), 1)
        self.runner.assert_not_called()
        self.publisher.assert_not_called()

    def test_bad_or_missing_local_commit_rejected(self):
        original = self.git
        def bad_sha(argv, **kwargs):
            return 'HEAD' if 'rev-parse' in argv else original(argv, **kwargs)
        self.runner.side_effect = bad_sha
        self.assertEqual(self.execute(), 1)
        self.publisher.assert_not_called()
        self.assertFalse(any('push' in c for c in self.commands))

    def test_missing_local_branch_never_pushes(self):
        original = self.git
        def missing(argv, **kwargs):
            if 'rev-parse' in argv:
                raise RuntimeError('unknown revision')
            return original(argv, **kwargs)
        self.runner.side_effect = missing
        self.assertEqual(self.execute(), 1)
        self.publisher.assert_not_called()
        self.assertFalse(any('push' in c for c in self.commands))

    def test_repo_url_is_not_accepted_as_local_path(self):
        self.assertEqual(push.push(self.config, 'https://example.invalid/repo.git', 'main'), 1)
        self.runner.assert_not_called()
        self.publisher.assert_not_called()

    def test_success_receipt_failure_does_not_publish_or_claim_git_failure(self):
        original = push.write_json
        def fail_success(path, value):
            if value.get('status') == 'pushed':
                raise OSError('receipt unavailable')
            original(path, value)
        with patch('push.write_json', side_effect=fail_success):
            self.assertEqual(self.execute(), 1)
        self.publisher.assert_not_called()
        self.assertTrue(self.stop.exists())
        self.assertTrue(self.receipts()[0]['git_push_success'])
        self.assertIn('Git push succeeded;', self.output.getvalue())

    def test_lock_contention_never_pushes_or_publishes(self):
        health_path = self.runtime / 'health.json'
        write_json(health_path, dict(ok=True, result='concurrent successful process'))
        original_health = health_path.read_bytes()
        temp_health = self.runtime / 'health.json.tmp'
        temp_health.write_bytes(b'concurrent writer in progress')
        with patch('push.WorkerLock') as lock:
            lock.return_value.__enter__.side_effect = RuntimeError('busy')
            self.assertEqual(self.execute(), 1)
            lock.return_value.__exit__.assert_not_called()
        self.runner.assert_not_called()
        self.publisher.assert_not_called()
        self.assertEqual(self.receipts()[0]['error'], 'busy')
        self.assertEqual(health_path.read_bytes(), original_health)
        self.assertEqual(temp_health.read_bytes(), b'concurrent writer in progress')

    def test_health_writes_hold_original_lock_until_success_or_failure_recorded(self):
        original_write = push.write_json
        outcomes = []

        def checked_write(path, value):
            if Path(path) == self.runtime / 'health.json':
                self.assertTrue(self.locked, 'health must be written before releasing the original lock')
                outcomes.append(value['ok'])
            original_write(path, value)

        with patch('push.write_json', side_effect=checked_write):
            self.assertEqual(self.execute(), 0)
            self.assertFalse(self.locked)
            self.push_error = 'push rejected'
            self.assertEqual(self.execute(), 1)
            self.assertFalse(self.locked)
            self.push_error = None
            self.publisher.side_effect = RuntimeError('deployment failed')
            self.assertEqual(self.execute(), 1)
            self.assertFalse(self.locked)
        self.assertEqual(outcomes, [True, False, False])

    def test_health_write_error_still_releases_lock_after_failure_attempt(self):
        original_write = push.write_json
        outcomes = []

        def failed_health(path, value):
            if Path(path) == self.runtime / 'health.json':
                self.assertTrue(self.locked)
                outcomes.append(value['ok'])
                raise OSError('health disk failure')
            original_write(path, value)

        with patch('push.write_json', side_effect=failed_health):
            self.assertEqual(self.execute(), 1)
        self.assertEqual(outcomes, [True, False])
        self.assertFalse(self.locked)
        self.assertTrue(self.receipts()[0]['git_push_success'])

    def test_receipt_write_failure_prevents_push(self):
        with patch('push.write_json', side_effect=OSError('disk full')):
            self.assertEqual(self.execute(), 1)
        self.runner.assert_not_called()
        self.publisher.assert_not_called()

    def test_remote_check_failure_preserves_success_receipt_and_stop(self):
        original = self.git
        def failed_check(argv, **kwargs):
            if 'ls-remote' in argv:
                raise RuntimeError('remote unavailable')
            return original(argv, **kwargs)
        self.runner.side_effect = failed_check
        self.assertEqual(self.execute(), 1)
        self.assertTrue(self.receipts()[0]['git_push_success'])
        self.assertTrue(self.stop.exists())
        self.publisher.assert_not_called()

    def test_cli_requires_explicit_local_repo_branch_and_rejects_extra_controls(self):
        for args in [[], ['--repo', str(self.repo)], ['--repo', str(self.repo), '--branch', 'main', '--force'],
                     ['--repo', str(self.repo), '--branch', 'main', '--delete'],
                     ['--repo', str(self.repo), '--branch', 'main', '--remote', REMOTE]]:
            with self.subTest(args=args), self.assertRaises(SystemExit) as raised:
                push.main(args)
            self.assertEqual(raised.exception.code, 2)
        self.runner.assert_not_called()

    def test_cli_uses_given_config_and_returns_failure_exit_code(self):
        config_path = self.root / 'config.json'
        write_json(config_path, self.config)
        self.push_error = 'denied'
        self.assertEqual(push.main(['--repo', str(self.repo), '--branch', 'main', '--config', str(config_path)]), 1)

    def test_older_pending_is_drained_then_requested_sha_with_real_once(self):
        old, baseline = 'b' * 40, 'c' * 40
        write_json(self.runtime / 'state.json', dict(
            last_seen_sha=baseline, last_published_sha=baseline, pending_sha=old))
        self.publisher.side_effect = sync.once
        with patch('sync.GitSource') as source, patch('sync.prepare') as prepare, patch('sync.publish') as publish:
            git = source.return_value
            git.remote_sha.return_value = git.fetch.return_value = SHA
            git.changed_files.return_value = ['heroes/jester/jester.info.darkest']
            prepare.return_value = dict(version='1.0', digest='fixture')
            publish.side_effect = lambda *args: self.assertTrue(self.locked)
            self.assertEqual(self.execute(), 0)
            self.assertEqual([c.args[3] for c in prepare.call_args_list], [old, SHA])
            self.assertEqual(publish.call_count, 2)
        self.assertEqual(self.publisher.call_count, 2)
        for call in self.publisher.call_args_list:
            self.assertEqual(call.kwargs, {'expected_sha': SHA})
        state = read_json(self.runtime / 'state.json')
        self.assertEqual(state['last_seen_sha'], SHA)
        self.assertIsNone(state['pending_sha'])
        self.assertEqual(len(self.receipts()[0]['deployment_results']), 2)

    def test_remote_drift_inside_once_or_fetch_never_publishes(self):
        self.publisher.side_effect = sync.once
        for during_fetch in (False, True):
            with self.subTest(during_fetch=during_fetch):
                write_json(self.runtime / 'state.json', dict(last_seen_sha='c'*40, last_published_sha='c'*40))
                with patch('sync.GitSource') as source, patch('sync.prepare') as prepare, patch('sync.publish') as publish:
                    source.return_value.remote_sha.return_value = SHA if during_fetch else 'b'*40
                    source.return_value.fetch.return_value = 'b'*40
                    self.assertEqual(self.execute(), 1)
                    prepare.assert_not_called()
                    publish.assert_not_called()
                health = read_json(self.runtime / 'health.json')
                self.assertFalse(health['ok'])
                self.assertTrue(health['git_push_success'])
                self.assertIn('changed', health['error'])

    def test_two_attempt_limit_rejects_stale_missing_or_pending_state(self):
        self.publisher.side_effect = None
        self.publisher.return_value = 'idle'
        for state in [{}, {'last_seen_sha': 'b'*40, 'pending_sha': None},
                      {'last_seen_sha': SHA, 'pending_sha': 'b'*40}]:
            with self.subTest(state=state):
                write_json(self.runtime / 'state.json', state)
                self.publisher.reset_mock()
                self.assertEqual(self.execute(), 1)
                self.assertEqual(self.publisher.call_count, 2)
                self.assertIn('two attempts', read_json(self.runtime / 'health.json')['error'])

    def test_health_replaces_stale_failure_on_main_and_test_success(self):
        for branch in ('main', 'test'):
            write_json(self.runtime / 'health.json', {'ok': False, 'error': 'old polling failure'})
            self.assertEqual(self.execute(branch), 0)
            health = read_json(self.runtime / 'health.json')
            self.assertTrue(health['ok'])
            self.assertIsNone(health['error'])
            self.assertEqual(health['branch'], branch)
            self.assertEqual(health['sha'], SHA)
            self.assertTrue(Path(health['event']).is_file())

    def test_health_replaces_stale_success_on_push_and_deployment_failure(self):
        for failure in ('push', 'deployment'):
            write_json(self.runtime / 'health.json', {'ok': True, 'result': 'old polling success'})
            self.push_error = 'push rejected' if failure == 'push' else None
            self.publisher.side_effect = RuntimeError('deployment rejected')
            self.assertEqual(self.execute(), 1)
            health = read_json(self.runtime / 'health.json')
            self.assertFalse(health['ok'])
            self.assertEqual(health['git_push_success'], failure == 'deployment')
            self.assertIn('rejected', health['error'])


if __name__ == '__main__':
    unittest.main()
