"""SYS-104 effect reuse must not drop secondary buffs or decimal values."""
import unittest
from effect_common import effect_sig, reuse_candidate, vanilla_index

class EffectSignatureTests(unittest.TestCase):
    def test_secondary_buff_changes_are_not_identical(self):
        a='effect: .name "a" .buff_ids "BLEED" "BLIGHT" .duration 3'
        b='effect: .name "b" .buff_ids "BLEED" "BLIGHT" "STUN" "DEBUFF" .duration 3'
        self.assertNotEqual(effect_sig(a),effect_sig(b))
    def test_decimal_and_vector_tails_are_significant(self):
        for a,b in [('.amount 0.15','.amount 0.19'),('.move 0 1','.move 0 2')]:
            self.assertNotEqual(effect_sig('effect: .name "a" '+a),effect_sig('effect: .name "b" '+b))
    def test_name_whitespace_and_field_order_are_irrelevant(self):
        self.assertEqual(effect_sig('effect: .name "a" .amount 0.15 .buff_ids "X" "Y"'),effect_sig('effect: .buff_ids  "X"   "Y" .name "b" .amount 0.15'))
    def test_reuse_rejects_lost_buff_and_allows_exact_family(self):
        base='effect: .name "Resists 1" .buff_ids "BLEED" "BLIGHT" .duration 3'
        eff={'Resists 1':(base,'fixture')}; idx=vanilla_index(eff)
        expanded='effect: .name "Hero Resists 1" .buff_ids "BLEED" "BLIGHT" "STUN" .duration 3'
        self.assertIsNone(reuse_candidate('Hero Resists 1',expanded,eff,idx))
        self.assertEqual(reuse_candidate('Hero Resists 1',base.replace('"Resists 1"','"Hero Resists 1"'),eff,idx),'Resists 1')

if __name__=='__main__':unittest.main()
