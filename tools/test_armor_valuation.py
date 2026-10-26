import copy,json,pathlib,sys,unittest,warnings
from unittest.mock import patch
R=pathlib.Path(__file__).parent
import strength as S
import armor_valuation as V

class ArmorModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore',category=ResourceWarning)
        S.evaluate('vanilla')
        cls.P=dict(S.PARAM,STRESS_HP=1.,STRESS_TAKEN=0.,MARK_DAMAGE_BONUS=0.,HEAL_FOLLOWUP_AMOUNT=6.,PARTY_ATTACKS=3.,FOCUS_SHARE=.5,CRIT_RECV_STRESS=0.,ALLY_DODGE=25)
        cls.m=dict(name='fixture',hp=1000,prot=.4,dodge=20,debuff=60,move=60,spd=5,ranks=(1,))
        cls.action=dict(acc=100.,crit=0.,weapon=(10.,10.),effects=(),friendly=False,count=1.,weight=1.)
    def test_fixed_unit_and_additivity(self):
        self.assertEqual(V.contribution(V.STANDARD),100)
        self.assertEqual(V.score(V.STANDARD),0)
        self.assertAlmostEqual(V.contribution(2)+V.contribution(5),V.contribution(7))
    def test_zero_dodge_real_enemy_retained(self):
        m=next(x for x in V.monster_pool('A') if x['name']=='skeleton_defender_A')
        self.assertEqual(m['dodge'],0);self.assertEqual(m['prot'],.25)
    def test_size_two_is_one_target(self):
        big=dict(self.m,size=2,ranks=(1,2));small=dict(self.m,name='other',size=1,ranks=(3,))
        with patch.object(V,'rank_cases',return_value=(((1.,(big,small)),),())):
            cases,meta=V.target_cases((1,2),True)
        self.assertEqual(len(cases),1);self.assertEqual(meta['units'],1.)
    def test_rank_unavailable_not_magic_reach(self):
        with patch.object(V,'rank_cases',return_value=(((1.,(self.m,)),),())):
            cases,meta=V.target_cases((4,),False)
        self.assertEqual(cases,[]);self.assertEqual(meta['availability'],0)
    def test_damage_prevention_and_hit_use_actual_kernel(self):
        with patch.object(V,'enemy_actions',return_value=(self.action,)):
            a=V.enemy_action_hp(self.m,{},self.P)
            b=V.enemy_action_hp(self.m,{'damage_low_multiply':.2,'damage_high_multiply':.2},self.P)
        self.assertAlmostEqual(a-b,2*S.hit_probability(100,25))
    def test_acc_prevents_dot_without_dmg_reduction_preventing_dot(self):
        a=dict(self.action,weapon=(0.,0.),effects=('effect: .target "target" .chance 100% .dotBleed 2 .duration 3',))
        p=dict(self.P,ALLY_BLEED_RESIST=.6,ENEMY_DOT_TICKS=2)
        with patch.object(V,'enemy_actions',return_value=(a,)):
            base=V.enemy_action_hp(self.m,{},p)
            attack=V.enemy_action_hp(self.m,{'damage_low_multiply':.5,'damage_high_multiply':.5},p)
            accuracy=V.enemy_action_hp(self.m,{'attack_rating_add':.1},p)
        self.assertAlmostEqual(base,1.6*S.hit_probability(100,25))
        self.assertEqual(base,attack);self.assertLess(accuracy,base)
    def test_mark_condition_is_conditional(self):
        with patch.object(V,'enemy_actions',return_value=(self.action,)):
            baseline=V.enemy_action_hp(self.m,{},self.P)
            inactive=V.enemy_action_hp(self.m,{'attack_marked_add':.1},dict(self.P,MARKED_VICTIM_SHARE=0))
            active=V.enemy_action_hp(self.m,{'attack_marked_add':.1},dict(self.P,MARKED_VICTIM_SHARE=1))
        self.assertEqual(baseline,inactive);self.assertAlmostEqual(baseline-active,1.)
    def test_joint_support_shapley_and_zero_budget(self):
        H=S.load_hero('vestal','rb');row=next(r for r,k in H['skills'] if S.first(k,'id')=='gods_illumination')
        eff=S.load_effects('rb');buffs=S.ec.load_buffs(S.G,S.M_ROOT)
        with patch.object(V,'target_cases',return_value=([(self.m,1.)],dict(units=1.,availability=1.))):
            v=V.evaluate_skill(H,row,eff,buffs,self.P)
            z=V.evaluate_skill(H,row,eff,buffs,dict(self.P,PARTY_ATTACKS=0))
        self.assertAlmostEqual(sum(v['parts_pp'].values()),v['basic_percent'])
        self.assertNotIn('방어도 감소',z['parts_pp']);self.assertNotIn('기타 공격 지원',z['parts_pp'])
        self.assertGreater(v['parts_pp']['방어도 감소'],0)
        cc=S.Ctx(H,eff,buffs,dict(self.P,TGT_ATTACKS=1.5))
        both,_=V.D.support_value(S,cc,row,S.kv(row),[eff[n] for n in S.ec.effect_names_in(row)],[self.m])
        self.assertAlmostEqual(v['parts_pp']['방어도 감소']+v['parts_pp']['기타 공격 지원'],V.contribution(both))
    def test_real_debuff_probability_uses_effect_not_level_guess(self):
        H=S.load_hero('duelist','rb');row=next(r for r,k in H['skills'] if S.first(k,'id')=='feint' and S.first(k,'valid_modes')=='stance_defensive')
        eff=S.load_effects('rb');buffs=S.ec.load_buffs(S.G,S.M_ROOT)
        with patch.object(V,'target_cases',return_value=([(self.m,1.)],dict(units=1.,availability=1.))),patch.object(V,'enemy_actions',return_value=(self.action,)):
            v=V.evaluate_skill(H,row,eff,buffs,self.P)
        k=S.kv(row);crit=(S.num(S.first(k,'crit'))+H['wcrit'])/100
        expected=S.hit(self.m,S.num(S.first(k,'atk')))*((1-crit)*.9+crit*1.)
        self.assertAlmostEqual(v['prot_probability'],expected)
        self.assertNotIn('반격 강화',v['parts_pp'])
    def test_aoe_does_not_multiply_party_followup_budget(self):
        H=S.load_hero('man_at_arms','rb');row=next(r for r,k in H['skills'] if S.first(k,'id')=='bellow')
        eff=S.load_effects('rb');buffs=S.ec.load_buffs(S.G,S.M_ROOT)
        # R-HP-027: Bellow no longer shreds PROT (MAA-020/022).
        # Use a test-only armor effect: this test checks the shared attack budget,
        # not a historical balance value. Keep current Bellow's speed debuff.
        eff=dict(eff)
        eff['TEST armor budget']='effect: .name "TEST armor budget" .target "target" .chance 140% .duration 3 .combat_stat_buff 1 .protection_rating_add -20% .on_hit true .on_miss false'
        row += ' .effect "TEST armor budget"'
        values=[]
        for count in (1.,4.):
            with patch.object(V,'target_cases',return_value=([(self.m,count)],dict(units=count,availability=1.))),patch.object(V,'enemy_actions',return_value=(self.action,)):
                values.append(V.evaluate_skill(H,row,eff,buffs,self.P))
        self.assertEqual(values[0]['followup_budget'],3.)
        self.assertAlmostEqual(values[0]['parts_pp']['방어도 감소'],values[1]['parts_pp']['방어도 감소'])
        self.assertGreater(values[1]['parts_pp']['속도 약화'],values[0]['parts_pp']['속도 약화'])
    def test_finite_hp_cap_and_no_armor_counterfactual(self):
        try:from armor_scenarios import finite_after_setup
        except ImportError:from extra_scenarios import finite_after_setup
        H=dict(dmg=(10.,10.),wcrit=0.)
        row='combat_skill: .id test .level 4 .atk 105% .dmg 0% .crit 0% .target 1'
        profiles=(((10.,10.),105.,0.,0.),)
        for hp in (1,10,60):
            for n in (0,1,3):
                v=finite_after_setup(H,row,{}, {},.4,hp,n,profiles)
                self.assertAlmostEqual(v['delta_hp'],0.)
                self.assertLessEqual(v['setup_hp'],hp+1e-9)

if __name__=='__main__':unittest.main(verbosity=2)
