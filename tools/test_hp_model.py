"""R-HP-027 independent integer-riposte cases; no game files are modified."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import strength as S

class HPModelTests(unittest.TestCase):
    def context(self, engine=True, crit=0, dmg=-60, stack='mult'):
        return SimpleNamespace(H={'dmg':(11,20),'wcrit':0,'riposte':S.kv(f'.atk 95% .dmg {dmg}% .crit {crit}%')},
                               avg=15.5,max=20,P=dict(S.PARAM,ENGINE_DAMAGE=engine,DMG_STACK=stack))
    def value(self, prot=0, **kwargs):
        with patch.object(S,'MONS',[{'dodge':0,'prot':prot}]):
            return S.Ctx.riposte(self.context(**kwargs),{})
    def test_integer_normal(self):
        self.assertAlmostEqual(self.value(),7) # ceil endpoints=5..9, mean7
    def test_integer_protection(self):
        self.assertAlmostEqual(self.value(.5),3.2) # outcomes2,3,3,4,4
    def test_critical_branch(self):
        self.assertAlmostEqual(self.value(.5,crit=100),6)
    def test_critical_mixture(self):
        self.assertAlmostEqual(self.value(.5,crit=50),4.6)
    def test_critical_cap(self):
        self.assertEqual(self.value(crit=200),self.value(crit=100))
    def test_legacy_continuous_explicit(self):
        self.assertAlmostEqual(self.value(engine=False),6.2)
    def test_miss_and_always_hit_region(self):
        with patch.object(S,'MONS',[{'dodge':45,'prot':0}]):
            self.assertAlmostEqual(S.Ctx.riposte(self.context(),{}),7*.55)
    def test_zero_damage(self):
        self.assertEqual(self.value(dmg=-100),0)
    def test_weapon_difference(self):
        self.assertAlmostEqual(S.damage_mean((13,26),-50,0),10)
        self.assertAlmostEqual(S.damage_mean((7,13),-50,0),5.5)
    def test_additive_and_multiplicative(self):
        with patch.object(S,'MONS',[{'dodge':0,'prot':0}]):
            # Fixed weapon removes variance; -50% skill and +50% buff.
            c=self.context(dmg=-50); c.H['dmg']=(20,20); c.avg=c.max=20
            self.assertEqual(S.Ctx.riposte(c,S.kv('.damage_low_multiply 50%')),15)
            c.P['DMG_STACK']='add'
            self.assertEqual(S.Ctx.riposte(c,S.kv('.damage_low_multiply 50%')),20)

    def test_mode_effect_names_keep_spaces_and_do_not_fall_back_to_vanilla(self):
        H=S.load_hero('abomination','rb')
        captured=[]
        def capture(C,line,d):
            captured.append(S.ec.effect_names_in(line))
            self.assertNotIn('.per_battle_limit',line)
            return 0.,{}
        sk={S.first(d,'id'):(0.,{},'1234') for _,d in H['skills']}
        with patch.object(S,'skill_value',side_effect=capture):
            S.mode_plans(None,H,sk,dict(S.PARAM,STRESS_HP=1.))
        self.assertEqual(len(captured),2)
        self.assertIn('RB ABO beast_stress_party',captured[0])
        self.assertIn('RB ABO Transform Self Stress',captured[0])
        self.assertIn('RB ABO Transform Heal 5',captured[0])
        self.assertNotIn('beast_stress_party',captured[0])
        self.assertIn('RB ABO human_stress_heal_party_1',captured[1])
        self.assertNotIn('human_stress_heal_party_1',captured[1])

if __name__=='__main__': unittest.main()
