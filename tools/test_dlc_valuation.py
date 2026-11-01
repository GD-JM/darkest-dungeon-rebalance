"""R-DLC-029 independent hand-calculated mechanic and integration cases."""
import math
import re
import unittest
from unittest.mock import patch
from dataclasses import replace
import strength as S
import dlc_valuation as D

class Events(unittest.TestCase):
    def test_decay_integer_order(self):
        self.assertEqual(D.decay(5,.25),2)  # Not floor(5*.625)=3.
        self.assertEqual([D.decay(9,x) for x in [0,.5,1,1.5]],[4,6,9,9])
    def test_firefly_one_decay(self):
        total,left,trace=D.burn_trace(9,3,slow=.5,slow_events=1)
        self.assertEqual([x['stacks'] for x in trace],[9,6,3]);self.assertEqual(total,18)
    def test_two_slow_sources_one_event(self):
        self.assertEqual([x['stacks'] for x in D.burn_trace(9,3,slow=1,slow_events=1)[2]],[9,9,4])
    def test_independently_expiring_slow_layers(self):
        t=D.burn_trace(9,3,slow=.5,slow_events=2,slow_layers=((.5,1),))[2]
        self.assertEqual([x['stacks'] for x in t],[9,9,6])
    def test_ground_after_miss(self):
        self.assertEqual(D.burn_trace(0,2,zone=5,zone_rounds=2)[0],12) # 5 + (2+5).
    def test_ground_lifetime(self):
        self.assertEqual(D.burn_trace(5,12,zone=5,zone_rounds=2)[0],28)
        self.assertEqual(D.burn_trace(6,12,zone=4,zone_rounds=3)[0],34)
    def test_multi_action_does_not_consume_round_lifetime(self):
        self.assertEqual(D.burn_trace(5,12,zone=5,zone_rounds=2,actions=2)[0],48)
    def test_entry_reward(self):
        self.assertEqual(D.burn_trace(5,12,zone=5,zone_rounds=2,entries=(1,))[0],37)
    def test_hp_cap(self):
        total,stacks,trace=D.burn_trace(10,3,hp=6)
        self.assertEqual(total,6);self.assertTrue(trace[-1]['dead'])
    def test_wildfire_needs_adjacency_and_no_corpse(self):
        self.assertEqual(D.wildfire_payload(8,True,2),(0,0))
        self.assertEqual(D.wildfire_payload(8,False,2),(4,1))
        self.assertEqual(D.wildfire_payload(8,False,2,True),(4,2))
    def test_consumed_dodge(self):
        self.assertAlmostEqual(D.consume_dodge_factor(.35,2),(1-math.exp(-1.3))/1.3)
        self.assertLess(D.consume_dodge_factor(.35,4),D.consume_dodge_factor(.35,1))
    def test_joint_kill(self):
        self.assertEqual(D.kill_probability((3,4),6,1,.95,6),.95)
        self.assertEqual(D.kill_probability((2,3,4),5,1,.95,6),0)
        self.assertEqual(D.kill_probability((3,4),6,.2,1,5),.2)
    def test_legal_move(self):
        d=S.kv('.id hearthlight .launch 43 .target ~1234 .move 0 2')
        self.assertEqual(D.transition(S,d,D.State(rank=4)).rank,2)
        with self.assertRaises(ValueError):D.transition(S,d,D.State(rank=2))
    def test_stance_limit(self):
        d=S.kv('.id anticipation .launch 4321 .per_turn_limit 1')
        q=D.transition(S,d,D.State())
        self.assertEqual(q.stance,'stance_aggressive')
        with self.assertRaises(ValueError):D.transition(S,d,q)
    def test_cb_wave_reset(self):
        d=S.kv('.id controlled_burn .launch 43 .target 123 .per_battle_limit 2')
        q=D.State(rank=4,cb_uses=2)
        self.assertFalse(D.legal(S,d,q));self.assertTrue(D.legal(S,d,D.next_wave(q)))
    def test_disengage_override(self):
        d=S.kv('.id disengage .launch 21 .target 12 .move 3 0')
        q=D.transition(S,d,D.State(rank=1))
        self.assertEqual(q.rank,4);self.assertTrue(q.any_position)

class Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eff={m:S.load_effects(m) for m in ['vanilla','rb']}
        cls.buffs={m:S.ec.load_buffs(S.G,S.M_ROOT if m=='rb' else None) for m in cls.eff}
    def ctx(self,hero='duelist',mode='rb',lv=4,**state):
        P=dict(S.PARAM,STRESS_HP=1.,STRESS_TAKEN=2.,HEAL_FOLLOWUP_AMOUNT=5.,STRESS_HEAL_FOLLOWUP_AMOUNT=6.,MARK_DAMAGE_BONUS=.075)
        if state:P['DLC_STATE']=state
        h=S.load_hero(hero,mode,lv);return S.Ctx(h,self.eff[mode],self.buffs[mode],P)
    def value(self,C,sid):
        l,d=next((l,d) for l,d in C.H['skills'] if S.first(d,'id')==sid)
        return S.skill_value(C,l,d)
    def test_all_140_skill_states(self):
        for hero in D.SKILLS:
            for mode in ['vanilla','rb']:
                for lv in range(5):
                    C=self.ctx(hero,mode,lv)
                    self.assertEqual({S.first(k,'id') for _,k in C.H['skills']},set(D.SKILLS[hero]))
                    for sid in D.SKILLS[hero]:
                        v,p=self.value(C,sid)
                        self.assertTrue(math.isfinite(v),(hero,mode,lv,sid));self.assertAlmostEqual(v,sum(p.values()))
    def test_coup_extra_action_threshold(self):
        C=self.ctx(target_hp=6,target_stunned=True,stance='stance_aggressive')
        _,p=self.value(C,'coup_de_grace')
        self.assertGreater(p['처치 후 추가 행동'],0)
        C.P['DLC_STATE']['remaining_enemies']=1
        self.assertEqual(self.value(C,'coup_de_grace')[1]['처치 후 추가 행동'],0)
    def test_touche_consumption(self):
        self.assertLess(self.value(self.ctx(mode='vanilla'),'touche')[1]['회피 소모 보정'],0)
        self.assertLess(self.value(self.ctx(),'touche')[1]['회피 소모 보정'],0)
        self.assertAlmostEqual(self.value(self.ctx(),'touche')[0],self.value(self.ctx(mode='vanilla'),'touche')[0])
    def test_exclusive_stance(self):
        C=self.ctx();l,d=next((l,d) for l,d in C.H['skills'] if S.first(d,'id')=='anticipation')
        line,_=D.prepare(S,C,l,d)
        self.assertIn('duelist_aggressive_buff5',line);self.assertNotIn('duelist_defensive_buff5',line)
    def test_backdraft_target_requirement(self):
        self.assertEqual(self.value(self.ctx('runaway',burn=0,rank=2),'backdraft')[0],0)
    def test_backdraft_rear(self):
        c=self.ctx('runaway',burn=8,rank=2)
        a=self.value(c,'backdraft')[0];c.P['DLC_STATE']['rear_exists']=False
        self.assertGreater(a,self.value(c,'backdraft')[0])
    def test_hearthlight_burning_only(self):
        c=self.ctx('runaway',burn=0,rank=4)
        self.assertEqual(self.value(c,'hearthlight')[1]['화상 상태 변화'],0)
        c.P['DLC_STATE']['burn']=8
        self.assertGreater(self.value(c,'hearthlight')[1]['화상 상태 변화'],0)
    def test_hot_overheal(self):
        c=self.ctx('runaway',rank=2,missing_hp=2,future_hot_ticks=2)
        self.assertEqual(self.value(c,'run_and_hide')[1]['회복'],2)
    def test_backdraft_uses_rear_own_stacks(self):
        c=self.ctx('runaway',burn=8,rear_burn=0,rank=2,crit_bonus=-11)
        c.H['dmg']=(10,10);c.H['wcrit']=0;c.P['RANK_MODEL']=False
        m=dict(S.MONS[0],hp=100,dodge=0,prot=0)
        with patch.object(S,'MONS',[m]):
            _,p=self.value(c,'backdraft')
        self.assertEqual(p['직접'],13)
        self.assertEqual(p['뒤 대상 직접'],5)
        self.assertEqual(p['화상 전이 순증감'],0)
    def test_hearthlight_duration_changes_increment(self):
        c=self.ctx('runaway',burn=9,rank=4)
        c.eff=dict(c.eff)
        # Explicit one/two-event fixtures; independent of uncommitted RUN-011.
        name='RB RUN Hearthlight Decay 5'
        c.eff[name]=re.sub(r'\.duration \d+', '.duration 1', c.eff[name])
        c.eff[name]=re.sub(r'\.buff_duration_type \w+', '.buff_duration_type after_turn', c.eff[name])
        if '.buff_duration_type' not in c.eff[name]:c.eff[name]+=' .buff_duration_type after_turn'
        one=self.value(c,'hearthlight')[1]['화상 상태 변화']
        c.eff['RB RUN Hearthlight Decay 5']=c.eff['RB RUN Hearthlight Decay 5'].replace('.duration 1 ','.duration 2 ')
        two=self.value(c,'hearthlight')[1]['화상 상태 변화']
        self.assertGreater(two,one)
    def test_already_marked_gets_no_new_mark_damage(self):
        c=self.ctx(marked=True,stance='stance_aggressive')
        self.assertNotIn('표식 반격 연계',self.value(c,'fleche')[1])
    def test_disengage_access_uses_actual_attacks(self):
        c=self.ctx(followup_target_rank=4)
        self.assertGreater(D.reach_delta(S,c,D.state(c)),0)
        self.assertEqual(D.reach_delta(S,c,replace(D.state(c),followup_target_rank=1)),0)
    def test_disengage_post_move_defense(self):
        c=self.ctx(rank=1,rank4_windows=1)
        b=c.buffs['DUELIST_DISENGAGE_DODGEBUFF5']
        self.assertEqual(D.rule_weight(c,b),.5)
    def test_boot_cannot_stun_a_killed_target(self):
        c=self.ctx(target_hp=1,stance='stance_aggressive')
        m=dict(S.MONS[0],hp=100,prot=0,dodge=0,stun=0)
        with patch.object(S,'MONS',[m]):
            _,p=self.value(c,'the_boot')
        self.assertEqual(p.get('기절',0),0)

if __name__=='__main__':unittest.main()
