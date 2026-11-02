import importlib.util,sys,copy,json,re,statistics as st,math
from pathlib import Path
spec=importlib.util.spec_from_file_location('a20',Path(__file__).with_name('audit20-model.py'));A=importlib.util.module_from_spec(spec);sys.modules['a20']=A;spec.loader.exec_module(A)
S,R,O=A.S,A.R,A.O
T=A.inventory['trinkets'];B=S.ec.load_buffs(S.G,str(R));E=S.load_effects('rb')
BUILDS={
'abomination':(2,['com_abom_broken_key','padlock_2']),
'antiquarian':(4,['antiq_5','cc_set_anti_the_masters_essence']),
'arbalest':(4,['medics_greaves','bulls_eye_bandana']),
'bounty_hunter':(2,['hunters_talon','focus_ring']),
'crusader':(2,['commanders_orders','cc_set_cru_signed_conscription']),
'duelist':(2,['duelist_set_academie_ring','focus_ring']),
'flagellant':(1,['flag_3','focus_ring']),
'grave_robber':(3,['raiders_talisman','cc_set_gr_sharpened_letter_opener']),
'hellion':(1,['heavens_hairpin','bleeding_pendant']),
'highwayman':(2,['sharpening_sheath','cc_set_high_shameful_locket']),
'houndmaster':(3,['cudgel_weight','cc_set_hm_lawmans_badge']),
'jester':(3,['bright_tambourine','critical_dice']),
'leper':(1,['fortunate_armlet','berserk_mask']),
'man_at_arms':(2,['rampart_shield','cc_set_maa_old_unit_banner']),
'musketeer':(4,['medics_boots','cc_set_musk_silver_bullet']),
'occultist':(2,['demons_cauldron','cc_set_occ_vial_of_sand']),
'plague_doctor':(4,['blasphemous_vial','witchs_vial']),
'runaway':(3,['rw_set_carved_toy','focus_ring']),
'shieldbreaker':(1,['sb_5','sb_set_1']),
'vestal':(3,['sacred_scroll','cc_set_vest_salacious_diary'])}
def field(row,key,value):
 pattern=r'\.'+re.escape(key)+r'\s+.*?(?=\s+\.[a-z_]|$)'
 if re.search(pattern,row):return re.sub(pattern,'.'+key+' '+value,row,count=1)
 return row+' .'+key+' '+value
def active(b,h,d,rank,state):
 rule=b.get('rule_type','always');rd=b.get('rule_data',{});f=rd.get('float',0);s=rd.get('string','')
 answers={'always':True,None:True,'meleeonly':S.first(d,'type')=='melee','rangedonly':S.first(d,'type')=='ranged','skill':S.first(d,'id')==s,'in_rank':rank==int(f)+1,'lightabove':100>f,'lightbelow':100<f,'hpabove':.8>f,'hpbelow':.8<f,'is_stealthed':state.get('stealthed',False),'target_is_burning':state.get('burn',0)>0,'any_is_burning':state.get('burn',0)>0,'in_mode':state.get('stance','stance_defensive')==s,'firstroundonly':False,'at_deaths_door':False}
 if rule in ('actorStatus','is_actor_status'):value=state.get(s,False) or (s=='burning' and state.get('burn',0)>0)
 else:value=answers.get(rule,None)
 return None if value is None else (not value if b.get('is_false_rule') else value)
def equip(h,row,mode,ids,rank,state=None):
 state=state or {};H=copy.deepcopy(S.load_hero(h,mode));baseH=copy.deepcopy(H);d=S.kv(row);eff=dict(S.load_effects(mode));buffs=S.ec.load_buffs(S.G,str(R) if mode=='rb' else None);mods={};ignored=[];activeids=[];ripcrit=ripdmg=0;callbacks=[]
 for id in ids:
  t=T[id];assert not t.get('hero_class_requirements') or h in t['hero_class_requirements']
  callbacks.extend({'trinket':id,'event':k,'effects':v} for k,v in t.items() if k.endswith('_additional_effects') and v)
  for b in t['details']:
   rule=b.get('rule_type');key=(b.get('stat_type'),b.get('stat_sub_type',''));amt=b.get('amount',0)
   if rule=='riposte':
    if key==('combat_stat_add','crit_chance'):ripcrit+=100*amt;activeids.append(b['id']);continue
    if key[1] in ('damage_low','damage_high'):ripdmg+=amt/2;activeids.append(b['id']);continue
   ok=active(b,h,d,rank,state)
   if ok is not True:ignored.append(dict(id=b.get('id'),reason='inactive' if ok is False else 'unpriced rule',rule=rule));continue
   mods[key]=mods.get(key,0)+amt;activeids.append(b['id'])
 def m(stat,sub=''):return mods.get((stat,sub),0)
 H['wcrit']+=m('combat_stat_add','crit_chance')*100
 H['def']+=m('combat_stat_add','defense_rating')*100;H['spd']+=m('combat_stat_add','speed_rating');H['hp']*=1+m('combat_stat_multiply','max_hp');H['prot']+=m('combat_stat_add','protection_rating')
 H['dmg']=tuple(x*(1+m('combat_stat_multiply',k)) for x,k in zip(H['dmg'],('damage_low','damage_high')))
 if 'riposte' in H:
  H['riposte']['atk']=[str(S.num(S.first(H['riposte'],'atk'))+m('combat_stat_add','attack_rating')*100)]
  H['riposte']['crit']=[str(S.num(S.first(H['riposte'],'crit'))+ripcrit)]
 for k in H['res']:H['res'][k]+=m('resistance',k)*100
 if 'atk' in d:row=field(row,'atk',str(S.num(S.first(d,'atk'))+m('combat_stat_add','attack_rating')*100)+'%')
 if m('ignore_protection')>=1:row=field(row,'ignore_protection','true')
 if 'heal' in d:row=field(row,'heal',' '.join(str(S.num(x)*(1+m('hp_heal_percent'))) for x in d['heal']))
 for n in S.ec.effect_names_in(row):
  if n not in eff:continue
  e=eff[n];k=S.kv(e);chancebonus=0;who=S.first(k,'target','target')
  for key,stat in [('stun','stun_chance'),('dotBleed','bleed_chance'),('dotPoison','poison_chance'),('push','move_chance'),('pull','move_chance')]:
   if key in k:chancebonus+=m(stat)*100
  debuff=(who in ('target','target_group') and ('combat_stat_buff' in k or any(buffs.get(b.strip('"'),{}).get('amount',0)<0 or buffs.get(b.strip('"'),{}).get('stat_type')=='hp_dot_burn_decay_percent' for b in k.get('buff_ids',[]))))
  if debuff:chancebonus+=m('debuff_chance')*100
  if chancebonus:e=field(e,'chance',str(S.num(S.first(k,'chance','100'))+chancebonus)+'%')
  self_heal_mult=(1+m('hp_heal_percent'))*(1+m('hp_heal_received_percent') if who=='performer' or not S.first(d,'target') else 1)-1
  self_stress_mult=(1+m('stress_heal_percent'))*(1+m('stress_heal_received_percent') if who=='performer' or not S.first(d,'target') else 1)-1
  for key,rate in [('heal',self_heal_mult),('dotHpHeal',self_heal_mult),('healstress',self_stress_mult),('stress',m('stress_dmg_percent')),('dotBurn',m('hp_dot_burn_amount_percent'))]:
   if key in k and rate:e=field(e,key,str(S.num(S.first(k,key))*(1+rate)))
  eff[n]=e
 # Keep scalar costs/defenses separate from action value; they are not free.
 handled={'combat_stat_add','combat_stat_multiply','resistance','stun_chance','debuff_chance','poison_chance','bleed_chance','move_chance','hp_heal_percent','stress_heal_percent','stress_dmg_percent','hp_dot_burn_amount_percent','ignore_protection'}
 unpriced=[dict(stat=k[0],sub=k[1],amount=v) for k,v in mods.items() if k[0] not in handled]
 meta=dict(ids=ids,names=[T[i]['name'] for i in ids],active_buffs=activeids,inactive_or_unknown=ignored,unpriced_stats=unpriced,callbacks=callbacks,hp=H['hp'],dodge=H['def'],speed=H['spd'],prot=H['prot'],res=H['res'],received_stress=m('stress_dmg_received_percent'),received_heal=m('hp_heal_received_percent'),received_stress_heal=m('stress_heal_received_percent'))
 return H,row,eff,meta
def calc(h,row,mode,ids,rank,P,state=None):
 H,l,e,meta=equip(h,row,mode,ids,rank,state);buffs=S.ec.load_buffs(S.G,str(R) if mode=='rb' else None)
 C=S.Ctx(H,e,buffs,P);v,parts=S.skill_value(C,l,S.kv(l));return dict(hp=v,parts=parts,gear=meta,row=l)
if __name__=='__main__':
 print('Gear init',flush=True);A.fullpool();crit_sides={}
 for mode in ['vanilla','rb']:S.evaluate(mode,dict(S.PARAM,BURN_TIMING=False));crit_sides[mode]=S.CRIT_SIDE_HP
 P=A.params();out={}
 for h,(rank,ids) in BUILDS.items():
  out[h]={'rank':rank,'ids':ids,'names':[T[i]['name'] for i in ids]}
  for mode in ['vanilla','rb']:
   S.CRIT_SIDE_HP=crit_sides[mode]
   vals={}
   for l,d in S.load_hero(h,mode)['skills']:
    sid=S.first(d,'id');key=sid+'|'+S.first(d,'valid_modes');before=calc(h,l,mode,[],rank,P);after=calc(h,l,mode,ids,rank,P)
    vals[key]=dict(name=A.name(h,sid),launch=S.first(d,'launch'),target=S.first(d,'target'),free=S.first(d,'is_continue_turn')=='true',before=before,after=after)
   out[h][mode]=vals
  print(h,'done',flush=True)
 (O/'gear.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 # Specific paired conditions are explicit, not assumed permanently active.
 conditions=[]
 for h,sid,ids,rank,qs in [('runaway','firefly',['rw_set_carved_toy','focus_ring'],3,[{},dict(burn=6)]),('duelist','fleche',['duelist_razor_hilt','focus_ring'],3,[{},dict(bleeding=True)]),('abomination','transform',['padlock_5','padlock_4'],2,[{}]),('musketeer','musketeer_mark',['cc_set_musk_silver_bullet','focus_ring'],4,[dict(tagged=True)])]:
  matches=[(l,d) for l,d in S.load_hero(h,'rb')['skills'] if S.first(d,'id')==sid]
  for l,d in matches:
   for q in qs:conditions.append(dict(hero=h,skill=sid,state=q,value=calc(h,l,'rb',ids,rank,P,q)))
 (O/'gear-conditions.json').write_text(json.dumps(conditions,ensure_ascii=False,indent=2),encoding='utf-8')
