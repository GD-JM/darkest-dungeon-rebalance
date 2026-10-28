import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import LANGUAGES, read_json, sha256, write_json
from release import load_intents, validate_editor, is_game_file, next_version, merge_editorial, apply_description_patches, inherit_published_editorial, editor_diff, hero_gameplay_changed
from sync import publish, publish_batch, verify_public, PublicRateLimited, once, metadata_with_marker, verify_phase, relevant, owned_card_previews
from steam import SteamError, SubmissionUnknown


class FakeSteam:
    current = None
    calls = []
    lose_response = False
    localized = {}

    def __init__(self, *_): pass
    def __enter__(self): return self
    def __exit__(self, *_): pass
    def query(self, language='english'):
        result = copy.deepcopy(self.current)
        result.update(self.localized.get(language, {}))
        return result
    def update(self, **kwargs):
        kwargs['before_submit']()
        self.calls.append(kwargs)
        self.current['metadata'] = kwargs['metadata']
        if 'description' in kwargs:
            self.localized[kwargs['language']] = {'description':kwargs['description'], 'title':kwargs['title']}
        if 'replace_previews' in kwargs:
            old, paths = kwargs['replace_previews']
            self.current['previews'] = [p for p in self.current['previews'] if p['filename'] not in old]
            self.current['previews'] += [dict(filename=Path(p).name, type=0) for p in paths]
        if self.lose_response:
            raise SubmissionUnknown('response lost after server accepted update')
        return self.query(kwargs.get('language','english'))


class SyncTests(unittest.TestCase):
    def setUp(self):
        # Use the granted project area for deterministic Windows sandbox tests.
        root = Path(__file__).resolve().parents[1] / 'test-tmp'
        root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.root = Path(self.temp.name)
        public_patch = patch('sync.verify_public', return_value=True)
        self.public_checker = public_patch.start()
        self.addCleanup(public_patch.stop)
    def tearDown(self): self.temp.cleanup()

    def image_release(self):
        (self.root / 'images').mkdir()
        image = self.root / 'images/01_bounty_hunter_p1.png'
        image.write_bytes(b'image fixture')
        release = dict(source_sha='a'*40, digest='digest', descriptions=[],
                       images=[dict(hero='bounty_hunter', path=image.name, sha256=sha256(image))])
        FakeSteam.current = dict(owned=True, metadata='', title='existing', description='existing',
            previews=[dict(filename='01_bounty_hunter.png', type=0), dict(filename='user-video', type=1)])
        FakeSteam.calls = []
        FakeSteam.lose_response = False
        FakeSteam.localized = {}
        return release

    def test_image_refresh_preserves_unrelated_preview_and_has_no_change_note(self):
        release = self.image_release()
        with patch('sync.Steam', FakeSteam):
            publish({'game_root':'game'}, self.root, release, True)
            publish({'game_root':'game'}, self.root, release, True)
        self.assertEqual(len(FakeSteam.calls), 1)
        self.assertNotIn('note', FakeSteam.calls[0])
        self.assertNotIn('content', FakeSteam.calls[0])
        self.assertIn('user-video', [p['filename'] for p in FakeSteam.current['previews']])

    def test_metadata_reconcile_updates_all_languages_without_payload_or_note(self):
        release = self.image_release()
        release['descriptions'] = [dict(language=x,title='Title '+x,body='Body '+x) for x in LANGUAGES]
        with patch('sync.Steam',FakeSteam):
            publish({'game_root':'game'},self.root,release,metadata_only=True)
        self.assertEqual(len(FakeSteam.calls),10)
        self.assertEqual(set(FakeSteam.localized),set(LANGUAGES))
        self.assertTrue(all('content' not in c and 'note' not in c for c in FakeSteam.calls))

    def test_lost_response_reconciles_without_duplicate_submit(self):
        release = self.image_release()
        FakeSteam.lose_response = True
        with patch('sync.Steam', FakeSteam):
            with self.assertRaises(SubmissionUnknown):
                publish({'game_root':'game'}, self.root, release, True)
            self.assertEqual(read_json(self.root/'publish-state.json')['status'], 'unknown')
            FakeSteam.lose_response = False
            publish({'game_root':'game'}, self.root, release, True)
        self.assertEqual(len(FakeSteam.calls), 1)
        self.assertEqual(read_json(self.root/'publish-state.json')['status'], 'complete')

    def test_unknown_result_without_matching_checkpoint_stays_blocked(self):
        release = self.image_release()
        write_json(self.root/'publish-state.json', dict(digest='digest', completed=[], phase='assets', status='submitting'))
        with patch('sync.Steam', FakeSteam), self.assertRaises(SubmissionUnknown):
            publish({'game_root':'game'}, self.root, release, True)
        self.assertEqual(FakeSteam.calls, [])

    def test_changed_image_is_rejected_before_steam_connection(self):
        release = self.image_release()
        (self.root/'images'/release['images'][0]['path']).write_bytes(b'changed')
        with patch('sync.Steam') as native, self.assertRaises(ValueError):
            publish({'game_root':'game'}, self.root, release, True)
        native.assert_not_called()

    def test_old_long_card_must_disappear_and_new_pages_keep_order(self):
        release = self.image_release()
        details = dict(previews=[dict(filename='01_bounty_hunter_p1.png'), dict(filename='01_bounty_hunter.png')])
        with self.assertRaises(ValueError): verify_phase(details, release, 'assets')

    def test_metadata_preserves_existing_other_keys(self):
        result = json.loads(metadata_with_marker('{"other":42}', {'digest':'a'}))
        self.assertEqual(result['other'], 42)
        self.assertEqual(result['workshop_sync']['digest'], 'a')

    def test_fresh_intent_required_for_new_runtime_changes(self):
        runtime = 'heroes/jester/jester.info.darkest'
        with self.assertRaisesRegex(ValueError, 'lack fresh'):
            load_intents(self.root, [runtime])
        rel = 'design/workshop/intents/test.json'
        record = dict(id='JES-X', decision='adopted', original_quote='사용자 원문', rationale_ko='이유',
                      source=dict(product='codex', reference='actual-session / actual-message'), files=[runtime])
        write_json(self.root/rel, record)
        self.assertEqual(load_intents(self.root, [runtime, rel])[0]['original_quote'], '사용자 원문')
        record['decision'] = 'proposed'
        write_json(self.root/rel, record)
        with self.assertRaises(ValueError): load_intents(self.root, [runtime, rel])

    def test_editor_cannot_invent_evidence_or_omit_language(self):
        result = dict(blocked_reason='', source_ids=['real'], note_en='change', note_zh='变化', card_updates=[], reasons=[],
            descriptions=[dict(language=lang, title='Title', body='Body') for lang in LANGUAGES])
        intents = [dict(id='real')]
        self.assertEqual(validate_editor(result, {}, intents), {})
        result['source_ids']=['invented']
        with self.assertRaises(ValueError): validate_editor(result, {}, intents)
        result['source_ids']=['real']; result['descriptions'].pop()
        with self.assertRaises(ValueError): validate_editor(result, {}, intents)

    def test_utf8_byte_budget_not_character_budget(self):
        result = dict(blocked_reason='', source_ids=[], note_en='change', note_zh='变化', card_updates=[], reasons=[],
            descriptions=[dict(language=lang, title='Title', body='한'*3000) for lang in LANGUAGES])
        with self.assertRaisesRegex(ValueError, 'byte budget'): validate_editor(result, {}, [])

    def test_description_patch_preserves_unrelated_text_exactly(self):
        source = {'english':dict(language='english',title='Title',body='Crusader: 5\nJester: 8\nCredits stay intact')}
        result = apply_description_patches(source,[dict(language='english',old_text='Crusader: 5',new_text='Crusader: 6')])
        self.assertEqual(result[0]['body'], 'Crusader: 6\nJester: 8\nCredits stay intact')
        self.assertEqual(source['english']['body'], 'Crusader: 5\nJester: 8\nCredits stay intact')
        with self.assertRaises(ValueError):
            apply_description_patches(source,[dict(language='english',old_text='not found',new_text='bad')])

    def test_first_release_retry_restores_original_patch_input(self):
        class ImmutableGit:
            def git(self, command, reference):
                return '{}' if reference.endswith('.json') else 'Original text\n'
        source = self.root/'source'
        for _ in range(2):
            inherit_published_editorial(source, ImmutableGit(), 'a'*40, 'b'*40, {'version':'2.5.1'}, self.root)
            text = (source/'design/workshop/description_en.txt').read_text(encoding='utf-8')
            result = apply_description_patches({'english':dict(language='english',title='Title',body=text)},
                       [dict(language='english',old_text='Original text',new_text='Patched text')])
            (source/'design/workshop/description_en.txt').write_text(result[0]['body'],encoding='utf-8')

    def test_push_editing_committed_published_text_is_not_a_conflict(self):
        # WS-INTENT-003: published text was committed back (commit c), then edited again in the push.
        texts = {'a': 'Old intro\nOld list\n', 'c': 'New intro\nNew list\n', 'b': 'New intro\nNew list\nAdded section\n'}
        prior = self.root/'prior'
        (prior/'source/design/workshop').mkdir(parents=True)
        (prior/'source/design/workshop/description_en.txt').write_text(texts['c'], encoding='utf-8')
        write_json(prior/'release.json', {'source_sha':'a'*40})
        class HistoryGit:
            def git(self, command, *args):
                if command == 'rev-list':
                    return ('b'*40) + '\n' + ('c'*40) + '\n' if args[2].endswith('.txt') else ''
                commit, rel = args[0].split(':', 1)
                return '{}' if rel.endswith('.json') else texts[commit[0]]
        source = self.root/'source'
        inherit_published_editorial(source, HistoryGit(), 'a'*40, 'b'*40, {'version':'2.5.7','job':str(prior)}, self.root)
        self.assertEqual((source/'design/workshop/description_en.txt').read_text(encoding='utf-8'), texts['b'])

    def test_editor_diff_omits_only_duplicated_or_non_runtime_hunks(self):
        # WS-EDITOR-005
        def part(path, body='+x\n'):
            return f'diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n{body}'
        kept = [part('heroes/jester/jester.info.darkest'), part('design/workshop/why.json'), part('effects/rebalance_jester.effects.darkest')]
        omitted = [part('design/changes/jester.md'), part('design/workshop/intents/a.json'), part('heroes/jester/jester.effects_edit.txt'),
                   part('design/workshop/description_en.txt'), part('design/workshop/i18n/description_french.txt')]
        self.assertEqual(editor_diff(''.join(kept + omitted)), ''.join(kept))

    def test_hero_data_only_for_gameplay_changes(self):
        # WS-EDITOR-005: borrowed riposte line, comments and animation do not pull the full hero files.
        def part(path, *lines):
            return f'diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n' + ''.join(l + '\n' for l in lines)
        riposte = (part('heroes/leper/leper.info.darkest', '+riposte_skill: .id "riposte1"', '+// SYS-105 note', '-// old note')
                   + part('heroes/leper/leper.art.darkest', '+combat_skill: .id "riposte1"'))
        self.assertFalse(hero_gameplay_changed(riposte, 'leper'))
        real = riposte + part('effects/rebalance_leper.effects.darkest', '+effect: .name "RB LEP X"')
        self.assertTrue(hero_gameplay_changed(real, 'leper'))
        self.assertFalse(hero_gameplay_changed(real, 'jester'))

    def test_dropped_hero_cards_leave_the_gallery(self):
        # WS-GALLERY-002
        previews = [dict(filename=n) for n in ('05_crusader.png', '06_duelist.png', '17_runaway.png', '13_man_at_arms_p2.png', 'trailer.png', 'fan_art.png')]
        release = {'images': [dict(hero='crusader'), dict(hero='man_at_arms')]}
        self.assertEqual(owned_card_previews(previews, release), {'05_crusader.png', '06_duelist.png', '17_runaway.png', '13_man_at_arms_p2.png'})

    def test_editing_sheet_is_not_runtime_payload(self):
        self.assertFalse(is_game_file('heroes/jester/jester.effects_edit.txt'))
        self.assertFalse(is_game_file('heroes/jester/jester.vanilla.txt'))
        self.assertTrue(is_game_file('effects/rebalance_jester.effects.darkest'))
        self.assertFalse(relevant('design/workshop/description_built_en.txt'))
        self.assertFalse(relevant('localization/3821353035_english.loc2'))
        self.assertTrue(relevant('design/workshop/cards/preview.png'))

    def test_workshop_overrides_cannot_bypass_intent_gate(self):
        for path in ['design/workshop/changes.json', 'design/workshop/workshop.effects.darkest', 'design/workshop/workshop.buffs.json']:
            self.assertTrue(is_game_file(path))
            with self.assertRaisesRegex(ValueError, 'lack fresh'):
                load_intents(self.root, [path])

    def test_next_push_keeps_prior_generated_changes_to_other_heroes(self):
        base = {'crusader': {'skills':[{'key':'crusader|a','new':['5']}]},
                'jester': {'skills':[{'key':'jester|b','new':['8']}]}}
        generated = copy.deepcopy(base); generated['crusader']['skills'][0]['new']=['6']
        pushed = copy.deepcopy(base); pushed['jester']['skills'][0]['new']=['9']
        merged = merge_editorial(base, generated, pushed)
        self.assertEqual(merged['crusader']['skills'][0]['new'], ['6'])
        self.assertEqual(merged['jester']['skills'][0]['new'], ['9'])

    def test_three_way_merge_keeps_changes_to_other_skills_of_same_hero(self):
        base = {'skills':[{'key':'a','new':['1']},{'key':'b','new':['2']}]}
        generated = {'skills':[{'key':'a','new':['3']},{'key':'b','new':['2']}]}
        pushed = {'skills':[{'key':'a','new':['1']},{'key':'b','new':['4']}]}
        self.assertEqual(merge_editorial(base, generated, pushed),
                         {'skills':[{'key':'a','new':['3']},{'key':'b','new':['4']}]})

    def test_unchanged_remote_skips_prepare_and_publish(self):
        write_json(self.root/'state.json', dict(last_seen_sha='a'*40,last_published_sha='a'*40))
        with patch('sync.GitSource') as source, patch('sync.prepare') as prep, patch('sync.publish') as pub:
            source.return_value.remote_sha.return_value='a'*40
            self.assertEqual(once({'state_dir':str(self.root)}), 'idle')
        prep.assert_not_called(); pub.assert_not_called()

    def test_push_event_rejects_remote_drift_before_idle_or_fetch(self):
        write_json(self.root/'state.json',dict(last_seen_sha='c'*40,last_published_sha='c'*40))
        with patch('sync.GitSource') as source, patch('sync.publish') as pub:
            source.return_value.remote_sha.return_value='c'*40
            with self.assertRaisesRegex(RuntimeError,'changed after'):
                once({'state_dir':str(self.root)},True,expected_sha='b'*40)
            source.return_value.fetch.assert_not_called()
        pub.assert_not_called()

    def test_push_event_rejects_remote_drift_during_fetch(self):
        write_json(self.root/'state.json',dict(last_seen_sha='a'*40,last_published_sha='a'*40))
        with patch('sync.GitSource') as source, patch('sync.prepare') as prep, patch('sync.publish') as pub:
            source.return_value.remote_sha.return_value='b'*40
            source.return_value.fetch.return_value='c'*40
            with self.assertRaisesRegex(RuntimeError,'changed during'):
                once({'state_dir':str(self.root)},True,expected_sha='b'*40)
        prep.assert_not_called(); pub.assert_not_called()

    def test_dry_run_prepares_without_publishing_or_advancing_baseline(self):
        write_json(self.root/'state.json', dict(last_seen_sha='a'*40,last_published_sha='a'*40))
        with patch('sync.GitSource') as source, patch('sync.prepare',return_value={'digest':'x'}), patch('sync.publish') as pub:
            source.return_value.remote_sha.return_value='b'*40
            source.return_value.fetch.return_value='b'*40
            source.return_value.changed_files.return_value=['heroes/jester/jester.info.darkest']
            self.assertTrue(once({'state_dir':str(self.root)}).startswith('prepared'))
        pub.assert_not_called()
        self.assertEqual(read_json(self.root/'state.json')['last_published_sha'],'a'*40)

    def test_removed_pending_commit_cannot_be_published_after_force_push(self):
        state = dict(last_seen_sha='a'*40,last_published_sha='a'*40,pending_sha='b'*40)
        write_json(self.root/'state.json',state)
        with patch('sync.GitSource') as source, patch('sync.prepare') as prep, patch('sync.publish') as pub:
            git = source.return_value
            git.remote_sha.return_value = git.fetch.return_value = 'c'*40
            git.ensure_forward.side_effect = [None, ValueError('pending commit removed from main')]
            with self.assertRaisesRegex(ValueError, 'removed from main'):
                once({'state_dir':str(self.root)},True)
            self.assertEqual(git.ensure_forward.call_args.args, ('b'*40,'c'*40))
        prep.assert_not_called(); pub.assert_not_called()
        self.assertEqual(read_json(self.root/'state.json'),state)

    def test_stale_registry_cannot_reactivate_retired_modules(self):
        import types
        write_json(self.root/'state.json',dict(last_seen_sha='a'*40,last_published_sha='a'*40))
        job=self.root/'jobs'/('b'*40)
        write_json(job/'source/design/workshop/modules.json',{'base':{'item_id':3826129567}})
        fake=types.ModuleType('modules')
        def forbidden(*args): raise AssertionError('retired module builder called')
        fake.prepare_modules=forbidden
        with patch.dict(sys.modules,{'modules':fake}), patch('sync.GitSource') as source, patch('sync.prepare',return_value={'digest':'aio','version':'2.5.4'}), patch('sync.publish') as pub:
            source.return_value.remote_sha.return_value=source.return_value.fetch.return_value='b'*40
            source.return_value.changed_files.return_value=['design/workshop/modules.json']
            self.assertTrue(once({'state_dir':str(self.root)},True).startswith('published '))
        pub.assert_called_once()
        self.assertEqual(pub.call_args.args[1],job)

    def test_retired_batch_and_direct_publication_fail_before_remote_writes(self):
        with patch('sync.publish') as pub:
            with self.assertRaisesRegex(ValueError,'retired'):
                publish_batch({'state_dir':str(self.root)},self.root,{}, {'base':{'item_id':3826129567}})
        pub.assert_not_called()
        with self.assertRaisesRegex(ValueError,'retired'):
            publish({},self.root,{'item_id':3826129567})

    def test_validation_failure_still_aborts_other_items(self):
        with patch('sync.publish', side_effect=ValueError('ownership mismatch')) as pub:
            with self.assertRaisesRegex(ValueError, 'ownership mismatch'):
                publish_batch({'state_dir':str(self.root)}, self.root, {}, {})
        self.assertEqual(pub.call_count, 1)

    def test_uploaded_hidden_item_cannot_complete_release(self):
        self.public_checker.return_value = False
        with patch('sync.publish'):
            with self.assertRaisesRegex(SteamError, 'public page remains hidden'):
                publish_batch({'state_dir':str(self.root)}, self.root, {}, {})
        item=read_json(self.root/'batch-state.json')['items']['all_dlc']
        self.assertEqual(item['status'], 'awaiting_public_review')
        self.assertTrue(item['upload_complete'])

    def test_public_check_distinguishes_subscription_from_hidden_or_unknown(self):
        with patch('sync.urlopen') as request:
            response=request.return_value.__enter__.return_value
            response.geturl.return_value='https://steamcommunity.com/sharedfiles/filedetails/?id=123&l=english'
            response.read.return_value=b'<a id="SubscribeItemBtn">Subscribe</a>'
            self.assertTrue(verify_public(123))
            response.read.return_value=b'The item is either marked as hidden or you do not have permission to view it.'
            self.assertFalse(verify_public(123))
            response.read.return_value=b'Service unavailable'
            with self.assertRaisesRegex(SteamError, 'unconfirmed'):
                verify_public(123)

    def test_public_rate_limit_is_not_retried_or_reported_as_success(self):
        from urllib.error import HTTPError
        with patch('sync.urlopen', side_effect=HTTPError('https://steamcommunity.com/',429,'Too Many Requests',{},None)) as request:
            with self.assertRaisesRegex(SteamError, '429'):
                verify_public(123)
            request.assert_called_once()

    def test_gallery_requires_every_expected_image_not_just_subscribe_or_thumbnails(self):
        urls = ['https://images.steamusercontent.com/ugc/1/A/', 'https://images.steamusercontent.com/ugc/2/B/']
        with patch('sync.urlopen') as request:
            response = request.return_value.__enter__.return_value
            response.geturl.return_value = 'https://steamcommunity.com/sharedfiles/filedetails/?id=123&l=english'
            body = '<a id="SubscribeItemBtn">Subscribe</a><img id="previewImage10" src="https://images.steamusercontent.com/ugc/1/A/?imw=637"><img id="previewImageMain" src="https://images.steamusercontent.com/ugc/2/B/">'
            response.read.return_value = body.encode()
            with self.assertRaisesRegex(SteamError, 'missing 1/2'):
                verify_public(123, urls)
            response.read.return_value = (body + '<img id="previewImage11" src="https://images.steamusercontent.com/ugc/2/B/?imw=637">').encode()
            self.assertTrue(verify_public(123, urls))
            response.read.return_value = ('<a id="SubscribeItemBtn">Subscribe</a>'
                '<div id="thumb_screenshot_10"><img src="https://images.steamusercontent.com/ugc/1/A/?imw=116"></div>'
                '<div id="thumb_screenshot_11"><img src="https://images.steamusercontent.com/ugc/2/B/?imw=116"></div>').encode()
            self.assertTrue(verify_public(123, urls))

    def test_public_rate_limit_defers_later_checks_and_persists_across_batches(self):
        self.public_checker.side_effect=PublicRateLimited(900)
        with patch('sync.publish') as pub:
            for _ in range(2):
                with self.assertRaises(SteamError):
                    publish_batch({'state_dir':str(self.root)}, self.root, {}, {})
        self.assertEqual(pub.call_count, 2)
        self.public_checker.assert_called_once()
        self.assertTrue(read_json(self.root/'public-check-cooldown.json')['until_epoch'] > 0)
        self.assertTrue(read_json(self.root/'batch-state.json')['items']['all_dlc']['upload_complete'])


if __name__ == '__main__': unittest.main()
