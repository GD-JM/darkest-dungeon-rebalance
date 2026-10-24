import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from modules import fields,refs,closure,manifest,descriptions,APPROVED
from common import LANGUAGES


class ModulesTests(unittest.TestCase):
    def test_quoted_bare_modes_and_reaction_lists(self):
        text='mode: .id defensive .battle_start_effect_ids "Start A" StartB\ncombat_skill: .effects "Main" .stance_defensive_effects Defense .stance_aggressive_effects Attack\ndeaths_door: .enter_effects Enter .buffs Debuff .recovery_buffs "Recover A" .recovery_heart_attack_buffs Heart'
        effects,buffs=refs(text)
        self.assertEqual(effects,{'Start A','StartB','Main','Defense','Attack','Enter'})
        self.assertEqual(buffs,{'Debuff','Recover A','Heart'})

    def test_unavailable_other_dlc_reference_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unavailable effect'):
            closure(['crit: .effects OtherDLC'],{}, {},{}, {})

    def test_transitive_native_riposte_and_clear_buff_references(self):
        effects={'Start':'effect: .name Start .riposte_effect Nested', 'Nested':'effect: .name Nested .buff_ids NativeBuff'}
        buffs={'NativeBuff':{'clear_buffs_on_rule_active':['Missing']}}
        with self.assertRaisesRegex(ValueError,'Unavailable buff'):
            closure(['crit: .effects Start'],{},{},effects,buffs)
        custom={'Missing':{'id':'Missing'}}
        self.assertEqual(closure(['crit: .effects Start'],{},custom,effects,buffs),(set(),{'Missing'}))

    def test_effect_cycle_is_bounded_and_collects_custom_nodes(self):
        custom={'A':'effect: .name A .effects B','B':'effect: .name B .effects A'}
        self.assertEqual(closure(['crit: .effects A'],custom,{},{},{}),({'A','B'},set()))

    def test_unsupported_reachable_actor_dot_stops_release(self):
        with self.assertRaisesRegex(ValueError,'Actor DOT'):
            closure(['crit: .effects A'],{'A':'effect: .name A .actor_dot egg'},{},{},{})

    def test_comments_do_not_add_dependencies(self):
        self.assertEqual(refs('// .effects Bogus\ncrit: .effects Real // .effects Bogus'),({'Real'},set()))

    def test_every_description_has_correct_dependencies_and_budget(self):
        registry={k:{'item_id':v} for k,v in APPROVED.items()}
        for key in registry:
            rows=descriptions(key,registry)
            self.assertEqual({r['language'] for r in rows},set(LANGUAGES))
            for row in rows:
                self.assertIn(str(APPROVED['base']),row['body'])
                self.assertIn('3821353035',row['body'])
                self.assertLess(len(row['body'].replace('\n','\r\n').encode()),8000)
                self.assertLess(len(row['title'].encode()),129)

    def test_manifest_self_size_and_content_hash(self):
        root=Path(__file__).resolve().parents[1]/'test-tmp'
        root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            p=Path(tmp); (p/'hello.txt').write_text('hello',encoding='utf-8')
            hashes=manifest(p)
            self.assertEqual(set(hashes),{'hello.txt','modfiles.txt'})
            self.assertEqual((p/'modfiles.txt').stat().st_size,int((p/'modfiles.txt').read_text().splitlines()[-1].rsplit(' ',1)[1]))


if __name__=='__main__': unittest.main()
