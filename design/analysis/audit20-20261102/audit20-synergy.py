import importlib.util,sys,copy,json,math,statistics as st
from pathlib import Path
def load(name,file):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
G=load('gear20','audit20-gear.py');A=G.A;S=A.S;D=S.damage_support;DLC=A.DLC;O=A.O
A.fullpool();S.evaluate('vanilla');S.evaluate('rb');P=A.params();E=S.load_effects('rb');B=S.ec.load_buffs(S.G,str(A.R))
def skill(h,sid,level=4):return next((l,d) for l,d in S.load_hero(h,'rb',level)['skills'] if S.first(d,'id')==sid)
def value(h,sid,extra=None,monster=None):
 l,d=skill(h,sid);p=dict(P,**(extra or {}));old=S.MONS;n=S.N_MON
 if monster:S.MONS=[monster];S.N_MON=1
 C=S.Ctx(S.load_hero(h,'rb'),E,B,p);v,parts=S.skill_value(C,l,d)
 S.MONS=old;S.N_MON=n;return dict(hp=v,parts=parts)
out={'assumptions':{'skill_weapon_level':5,'target_dodge':20,'debuff_resistance':60,'stun_resistance':90,'stress_missing':True,'gear':G.BUILDS,'party_optimization':False}}
# Exact per-target application, separating first stun and +50 recovery resistance.
out['stuns']=[]
for h,sid,ids in [('plague_doctor','blinding_gas',['blasphemous_vial','witchs_vial']),('abomination','manacles',['com_abom_broken_key','padlock_2']),('occultist','hands_from_abyss',['demons_cauldron','cc_set_occ_vial_of_sand']),('crusader','stunning_blow',['paralyzers_crest','focus_ring']),('houndmaster','blackjack',['cudgel_weight','focus_ring']),('duelist','the_boot',['duelist_steel_tip_boots','focus_ring']),('vestal','dazzling_light',['sacred_scroll','cc_set_vest_salacious_diary'])]:
 for gear in [[],ids]:
  l,d=skill(h,sid);H,l,e,meta=G.equip(h,l,'rb',gear,2);d=S.kv(l);stuns=[S.kv(e[n]) for n in S.ec.effect_names_in(l) if n in e and 'stun' in S.kv(e[n])];assert stuns
  acc=S.num(S.first(d,'atk'));crit=(H['wcrit']+S.num(S.first(d,'crit')))/100 if S.first(d,'is_crit_valid','true').lower()=='true' else 0;chance=S.num(S.first(stuns[0],'chance'))
  rates={str(res):S.hit_probability(acc,20)*((1-crit)*max(0,min(1,(chance-res)/100))+crit*max(0,min(1,(chance+20-res)/100))) for res in [60,90,140]}
  out['stuns'].append(dict(hero=h,skill=A.name(h,sid),ids=gear,accuracy=acc,crit=crit,chance=chance,success=rates,target=S.first(d,'target'),meta=meta))
# Same physical follow-up pool, no simultaneous free debuff stacks. One opener costs one ally action.
physical=[]
for h,sid in [('leper','chop'),('crusader','smite'),('highwayman','wicked_slice')]:
 H=S.load_hero(h,'rb');l,d=skill(h,sid);physical.append((H['dmg'],S.num(S.first(d,'atk')),(H['wcrit']+S.num(S.first(d,'crit')))/100,S.num(S.first(d,'dmg'))))
out['armor']=[]
for prot in [0,.25,.5]:
 monster=dict(name='controlled',dodge=20,prot=prot,hp=60,stun=90,debuff=60,bleed=60,poison=60,move=60,spd=7,type='human',size=1)
 for h,sid in [('occultist','weakening_curse'),('vestal','gods_illumination'),('musketeer','call_the_shot'),('leper','intimidate'),('shieldbreaker','break_guard'),('man_at_arms','retribution'),('antiquarian','flashpowder')]:
  l,d=skill(h,sid);H=S.load_hero(h,'rb');effs=[E[n] for n in S.ec.effect_names_in(l) if n in E]
  for count in [1,2,3]:
   p=dict(P,SUPPORT_PROFILES=physical,TGT_ATTACKS=count,SUPPORT_HORIZON=1,DEBUFF_TIMING=False,SUPPORT_MARKED=0,CRIT_SIDE=False,SUPPORT_TARGET_HP=60)
   C=S.Ctx(H,E,B,p);gain,side=D.support_value(S,C,l,d,effs,[monster])
   out['armor'].append(dict(hero=h,skill=A.name(h,sid),prot=prot,followups=count,followup_extra_hp=gain,gear=False))
# Legal marks: rank3 Occultist mark then rank2 BH/rank4 Arbalest or Musketeer/rank1 Houndmaster.
out['mark']=[]
for h,sid,rank in [('bounty_hunter','collect_bounty',2),('arbalest','sniper_shot',4),('musketeer','aimed_shot',4),('houndmaster','hounds_rush',1)]:
 H=S.load_hero(h,'rb');l,d=skill(h,sid);acc=S.num(S.first(d,'atk'));crit=(H['wcrit']+S.num(S.first(d,'crit')))/100
 bonus=0
 for n in S.ec.effect_names_in(l):
  k=S.kv(E.get(n,''))
  if S.first(k,'target')=='performer' and S.first(k,'keyStatus')=='tagged':
   low=S.num(S.first(k,'damage_low_multiply'));high=S.num(S.first(k,'damage_high_multiply',str(low)));assert low==high,(h,low,high);bonus+=low/100
 ap=sum(B.get(b.strip('"'),{}).get('amount',0) for n in S.ec.effect_names_in(l) for k in [S.kv(E.get(n,''))] if S.first(k,'skill_instant')=='true' for b in k.get('buff_ids',[]) if B.get(b.strip('"'),{}).get('stat_type')=='ignore_protection')
 for prot in [0,.5]:
  a=S.hit_probability(acc,20)*S.damage_mean(H['dmg'],S.num(S.first(d,'dmg')),crit,max(0,prot-ap),0)
  b=S.hit_probability(acc,20)*S.damage_mean(H['dmg'],S.num(S.first(d,'dmg')),crit,max(0,prot-ap),bonus)
  out['mark'].append(dict(hero=h,rank=rank,skill=A.name(h,sid),prot=prot,plain=a,marked=b,extra=b-a,marked_bonus=bonus))
out['dlc']=[]
for h,sids in [('runaway',['firefly','controlled_burn','hearthlight','searing_strike','backdraft']),('duelist',['coup_de_grace','feint','fleche'])]:
 for sid in sids:
  for prot in [0,.5]:
   for hp in ([6,12,30] if h=='duelist' else [25,100]):
    for cond in ([False,True] if h=='duelist' else [0,6,12]):
     q=dict(target_hp=hp,rear_hp=hp,rear_exists=True,remaining_enemies=2,rounds=3,rank=2 if sid in ('searing_strike','backdraft','feint','fleche') else 4)
     if h=='runaway':q.update(burn=cond,rear_burn=cond,target_rank=2)
     else:q.update(target_stunned=cond,target_rank=2,stance='stance_aggressive')
     m=dict(S.MONS[0],name='controlled',dodge=20,prot=prot,hp=hp,debuff=60,stun=90,bleed=60,poison=60,move=60,spd=7)
     val=value(h,sid,dict(RANK_MODEL=False,FRONT_REACH=None,DLC_STATE=q),m)
     out['dlc'].append(dict(hero=h,skill=A.name(h,sid),id=sid,prot=prot,target_hp=hp,condition=cond,state=q,**val))
out['burn_math']=[]
for stacks in [0,3,6,9,12,20]:
 plain=DLC.burn_trace(stacks,3)[0];plus=DLC.burn_trace(stacks+3,3)[0];slow=DLC.burn_trace(stacks,3,slow=.5,slow_events=1)[0]
 out['burn_math'].append(dict(stacks=stacks,baseline=plain,illumination_additional=plus-plain,hearthlight_success_additional=slow-plain))
# Repeated adjacency and automatic burn-on-death are not added without actual corpse/position data.
out['equipment_callbacks']={t['id']:{k:v for k,v in t.items() if k.endswith('_additional_effects')} for t in G.T.values() if t.get('hero_class_requirements') and any(k.endswith('_additional_effects') for k in t)}
(O/'synergy.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('synergy done',flush=True)
