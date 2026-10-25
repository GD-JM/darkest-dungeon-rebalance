"""Independent arithmetic cases + installed-data assertions for R-AUDIT-25."""
import unittest
from types import SimpleNamespace
import strength as S
import damage_support as D

class DamageSupportTests(unittest.TestCase):
    def setUp(self):
        self.P=dict(S.PARAM, SUPPORT_PROFILES=(((20.,20.),100.,0.,0.),),
                    TGT_ATTACKS=1.,DEBUFF_W1=1.,DEATH_RATE=0.,SUPPORT_HORIZON=1,
                    CRIT_SIDE=False, SUPPORT_MARKED=0.)
        self.H=dict(dmg=(1,1),wcrit=0)
        self.C=SimpleNamespace(P=self.P,H=self.H,buffs={})
        self.d=S.kv('.level 4 .atk 100% .dmg -100% .crit 0% .is_crit_valid False')
        self.m=dict(dodge=0,prot=.5,debuff=0,hp=50)
        self.armor='.target target .chance 100% .duration 2 .combat_stat_buff 1 .protection_rating_add -20% .on_hit true .on_miss false'
    def value(self,effects=None):
        return D.support_value(S,self.C,'',self.d,[self.armor] if effects is None else effects,[self.m])[0]
    def test_manual_armor_damage(self):
        self.assertAlmostEqual(self.value(),4.) # raw20: 50% ->30%, 10 ->14
    def test_immune(self):
        self.m['debuff']=200
        self.assertEqual(self.value(),0.)
    def test_zero_armor(self):
        self.m['prot']=0
        self.assertEqual(self.value(),0.)
    def test_zero_followups(self):
        self.P['TGT_ATTACKS']=0
        self.assertEqual(self.value(),0.)
    def test_armor_floor(self):
        self.m['prot']=.1
        self.assertAlmostEqual(self.value(),2.)
    def test_duration_not_flattened(self):
        self.P.update(SUPPORT_HORIZON=3,DEBUFF_W1=.5,DEATH_RATE=.5)
        self.assertAlmostEqual(self.value(),4.) # .5+.5 windows
        self.assertAlmostEqual(self.value([self.armor.replace('duration 2','duration 3')]),5.)
    def test_combined_interaction(self):
        self.m['dodge']=50 # opening h=.55, followup .55 -> .75
        dodge='.target target .chance 100% .duration 2 .combat_stat_buff 1 .defense_rating_add -20%'
        joint=self.value([self.armor,dodge])
        single=self.value()+self.value([dodge])
        self.assertAlmostEqual(joint-single,.55*.2*4.)
    def test_shared_effect_roll(self):
        self.m.update(dodge=50,debuff=50)
        joint=self.value([self.armor+' .defense_rating_add -20%'])
        separate=self.value([self.armor,'.target target .chance 100% .duration 2 .combat_stat_buff 1 .defense_rating_add -20%'])
        self.assertGreater(joint,separate)
    def test_opening_kill_removes_support(self):
        self.H.update(dmg=(100,100))
        self.d=S.kv('.level 4 .atk 100% .dmg 0% .crit 0%')
        self.assertEqual(self.value(),0.)
    def test_crit_kill_correlated_with_proc(self):
        self.H.update(dmg=(10,10),wcrit=50)
        self.m.update(prot=.5,hp=7,debuff=50) # normal5 alive, critical7 dead
        self.d=S.kv('.level 4 .atk 100% .dmg 0% .crit 0%')
        self.assertAlmostEqual(self.value(),1.) # 4*.5 noncrit*.5 apply
    def test_mark_condition(self):
        self.C.buffs={'test':dict(stat_type='crit_received_chance',amount=.1,rule_type='is_actor_status',rule_data={'string':'tagged'})}
        k=S.kv('.buff_ids "test"')
        self.assertEqual(D.modifiers(S,k,self.C.buffs,False),{})
        self.assertEqual(D.modifiers(S,k,self.C.buffs,True),{'crit_received':.1})
    def test_finite_overkill(self):
        self.assertAlmostEqual(D.finite_sequence(S,(20,20),100,0,0,5,0,0,3),5.)
    def test_finite_misses(self):
        self.assertAlmostEqual(D.finite_sequence(S,(20,20),50,0,0,5,0,0,2),5*(1-.45**2))
    def test_ehp_diagnostic(self):
        self.assertEqual(D.ehp(30,.5),60.)
        self.assertEqual(D.ehp(30,0),30.)
        self.assertEqual(self.value(),4.) # EHP never double-counted
    def test_engine_regression(self):
        self.assertEqual(S.damage_distribution((11,20),-60),(tuple(range(5,10)),12))
        self.assertEqual(S.damage_distribution((1,1),0,.01),((0,),1))
    def test_levels(self):
        for h in S.KO:
            for level in range(5):
                H=S.load_hero(h,'vanilla',level)
                self.assertTrue(H['skills'])
                self.assertTrue(all(int(S.first(d,'level'))==level for _,d in H['skills']))
                self.assertGreater(H['dmg'][1],0)
    def test_population(self):
        self.assertTrue(all(m['hp']>0 for m in S.MONS))
    def test_no_effect_no_support(self):
        self.assertEqual(self.value([]),0.)
    def test_same_enemy_resistance_covariance(self):
        pool=[dict(self.m,prot=.5,debuff=200),dict(self.m,prot=0,debuff=0)]
        self.assertEqual(D.support_value(S,self.C,'',self.d,[self.armor],pool)[0],0.)
    def test_stun_survival_regression(self):
        self.assertEqual(S.stun_joint_probability(1,.2,(5,6),9,1.4,.7,5),0.)
        self.assertAlmostEqual(S.stun_joint_probability(.9,.25,(3,4,5),10,1.3,.7,6),.9*.75*.6)
        self.assertAlmostEqual(S.stun_joint_probability(1,0,(3,4,5),9,1,0,4),1/3)
        self.assertEqual(S.stun_joint_probability(1,.1,(1,),2,1.5,0,20,0),0.)
    def test_integration_no_double_count(self):
        H=dict(self.H,id='test',skills=[],crit_effects=[],modes={},spd=0,hp=40)
        P=dict(self.P,RANK_MODEL=False,FRONT_REACH=False,STRESS_HP=1.)
        row='combat_skill: .id "test" .level 4 .atk 100% .dmg -100% .crit 0% .launch 1234 .target 1234 .is_crit_valid False .effect "armor"'
        C=S.Ctx(H,{'armor':self.armor},{},P)
        total,parts=S.skill_value(C,row,S.kv(row))
        expected,_=D.support_value(S,C,row,S.kv(row),[self.armor])
        self.assertAlmostEqual(total,expected)
        self.assertNotIn('약화',parts)
    def test_stealth_reach_monotone(self):
        a=D.destealth_coverage(S,(1,2,3))
        b=D.destealth_coverage(S,(1,2,3,4))
        self.assertLess(a['fraction'],b['fraction'])
        self.assertEqual(b['fraction'],1.)
    def test_timing_switch(self):
        self.P.update(SUPPORT_HORIZON=2,DEBUFF_W1=.5,DEATH_RATE=.9,DEBUFF_TIMING=False)
        self.assertAlmostEqual(self.value(),8.)
    def test_format_and_received_switches(self):
        self.C.buffs={'test':dict(stat_type='damage_received_percent',amount=.1,rule_type='always')}
        e='.target target .chance 100% .duration 2 .buff_ids "test"'
        self.assertGreater(self.value([e]),0.)
        self.P['DMG_RECEIVED']=False
        self.assertEqual(self.value([e]),0.)
        self.P.update(DMG_RECEIVED=True,DEBUFF_FORMATS=False)
        self.assertEqual(self.value([e]),0.)
if __name__=='__main__':unittest.main()
