import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from release import load_intents

class ReleaseIntentTests(unittest.TestCase):
    def test_tooling_does_not_enter_notes_or_cover_missing_gameplay_intent(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            source=Path(directory)
            rel='design/workshop/intents/fixture.json'
            (source/rel).parent.mkdir(parents=True)
            def record(id, files):
                return {'id':id,'decision':'adopted','original_quote':'Exact approval',
                        'rationale_ko':'Reason','source':{'product':'codex','reference':'test fixture'},'files':files}
            tooling=record('tool',['tools/workshop_sync/release.py'])
            gameplay=record('skill',['heroes/vestal/vestal.info.darkest'])
            changed=[rel,'tools/workshop_sync/release.py','heroes/vestal/vestal.info.darkest']
            (source/rel).write_text(json.dumps([tooling,gameplay]),encoding='utf-8')
            self.assertEqual([r['id'] for r in load_intents(source,changed)],['skill'])
            (source/rel).write_text(json.dumps([tooling]),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'lack fresh user-intent'):
                load_intents(source,changed)
            self.assertEqual(load_intents(source,changed[:-1]),[])
