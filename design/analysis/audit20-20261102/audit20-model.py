from pathlib import Path
import sys,json,copy,functools,statistics as st,subprocess,math,re
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent/'all-heroes-20261102';sys.path.insert(0,str(R/'tools'))
import strength as S
import armor_valuation as V
import dlc_valuation as DLC
from dataclasses import replace
_state=DLC.state
def audit_state(C):
 q=_state(C)
 return q if C.P.get('DLC_STATE') else replace(q,rounds=int(C.P['DEFAULT_DUR']))
DLC.state=audit_state
S.load_effects=functools.lru_cache(None)(S.load_effects)
S.ec.load_buffs=functools.lru_cache(None)(S.ec.load_buffs)
S.load_hero=functools.lru_cache(None)(S.load_hero)
inventory=json.loads((O/'inventory.json').read_text('utf-8'));K=inventory['names']
for f in (R/'localization').glob('*.string_table.xml'):
 text=f.read_text('utf-8');lang=re.search(r'<language id="koreana">(.*?)</language>',text,re.S)
 if lang:K.update(dict(re.findall(r'<entry id="([^"]*)"><!\[CDATA\[(.*?)\]\]></entry>',lang[1],re.S)))
def name(h,s):return '갑옷 쪼개기' if h=='leper' and s=='intimidate' else K.get('combat_skill_name_'+h+'_'+s,s)
def params(**overrides):
 p=dict(S.PARAM,STRESS_HP=S.stress_value(S.PARAM,median_hp=S.PARAM_MED_HP),STRESS_TAKEN=S._STRESS_CACHE,HEAL_FOLLOWUP_AMOUNT=S.followup_heal_amount(),STRESS_HEAL_FOLLOWUP_AMOUNT=S.followup_stress_heal_amount(),MARK_DAMAGE_BONUS=S.marked_damage_bonus(),BURN_TIMING=False)
 p.update(overrides);return p
def fullpool():
 old=S.MONS;S.MONS=[m for m in V.monster_pool('C') if m['name'] not in ('cocoon_C','corpse_crystal_C')];S.N_MON=len(S.MONS);S._STRESS_CACHE=None
 for n in ['monster_attack_accs','monster_crit_skills','marked_damage_bonus','dp_self','dp_enemy','formation_stats','formation_lineups']:
  f=getattr(S,n,None)
  if hasattr(f,'cache_clear'):f.cache_clear()
 return sorted(set(m['name'] for m in S.MONS)-set(m['name'] for m in old))
def rows(mode,P):
 out={};E=S.load_effects(mode);B=S.ec.load_buffs(S.G,str(R) if mode=='rb' else None)
 for h in S.KO:
  H=S.load_hero(h,mode);C=S.Ctx(H,E,B,P);ss=[]
  for l,d in H['skills']:
   v,parts=S.skill_value(C,l,d);sid=S.first(d,'id');ss.append(dict(id=sid,name=name(h,sid),hp=v,parts=parts,launch=S.first(d,'launch'),target=S.first(d,'target'),free=S.first(d,'is_continue_turn')=='true',mode=S.first(d,'valid_modes'),move=d.get('move',[])))
  ranks={}
  for rank in range(1,5):
   usable=[x for x in ss if str(rank) in x['launch'] and not x['free']];top=sorted(usable,key=lambda x:-x['hp'])[:3]
   ranks[str(rank)]={'hp':st.mean(x['hp'] for x in top) if top else None,'skills':[x['name'] for x in top],'count':len(usable)}
  out[h]=dict(skills=ss,ranks=ranks)
 return out
def normalized(d):return {k:v for k,v in d.items() if k not in ('level',)}
def diffcoverage():
 out={}
 for h in S.KO:
  changes=set();stats=set();same=[]
  for level in range(5):
   a=S.load_hero(h,'vanilla',level);b=S.load_hero(h,'rb',level)
   for k in ['dmg','wcrit','def','spd','hp','res','modes','riposte']:
    if a.get(k)!=b.get(k):stats.add(k)
   def signature(H,mode):
    E=S.load_effects(mode);B=S.ec.load_buffs(S.G,str(R) if mode=='rb' else None)
    out={}
    for l,d in H['skills']:
     key=S.first(d,'id')+'|'+S.first(d,'valid_modes');dd=copy.deepcopy(d)
     for k in ['effect','human_effects','beast_effects']:dd.pop(k,None)
     effects=[]
     for n in S.ec.effect_names_in(l):
      e=E.get(n,'');ek=S.kv(e);bs=[]
      for bid in ek.pop('buff_ids',[]):
       bb=copy.deepcopy(B.get(bid.strip('"'),{}));bb.pop('id',None);bs.append(bb)
      effects.append((ek,bs))
     out[key]=(dd,effects)
    return out
   aa=signature(a,'vanilla');bb=signature(b,'rb')
   for key in set(aa)|set(bb):
    if aa.get(key)!=bb.get(key):changes.add(key.split('|')[0])
  allskills={S.first(d,'id') for _,d in S.load_hero(h,'rb')['skills']}
  out[h]=dict(changed_skills=sorted(changes),unchanged_skills=sorted(allskills-changes),stats=sorted(stats))
 return out
if __name__=='__main__':
 print('Default reproduction',flush=True)
 default=S.run();out={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'default':default,'old_pool':S.MONS.copy()}
 out['added_monsters']=fullpool();out['excluded_old_monsters']=sorted(set(m['name'] for m in out['old_pool'])-set(m['name'] for m in S.MONS));print('Full combatants',len(S.MONS),out['added_monsters'],out['excluded_old_monsters'],flush=True)
 # The shared model still contains round-end burn discount for non-DLC sources. Audit disables it consistently.
 base=S.run(dict(S.PARAM,BURN_TIMING=False));P=params();out.update(base=base,parameters=P,monsters=S.MONS,rows={m:rows(m,P) for m in ('vanilla','rb')},coverage=diffcoverage())
 (O/'base.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 for h,r in sorted(base['rb'].items(),key=lambda z:-z[1]['act']):
  top=sorted(r['skills'].items(),key=lambda z:-z[1][0])[:3]
  print(S.KO[h],round(base['vanilla'][h]['act'],2),'->',round(r['act'],2),[(name(h,s),round(v[0],2)) for s,v in top],flush=True)
 scenarios={}
 for n,extra in [('no_stress_value',dict(STRESS_HP=0,CRIT_STRESS=0)),('short',dict(BUFF_DUR_CAP=1,SUPPORT_HORIZON=1,DEFAULT_DUR=2,DEATH_RATE=.6)),('long',dict(BUFF_DUR_CAP=3,SUPPORT_HORIZON=3,DEFAULT_DUR=4,DEATH_RATE=.2)),('no_rank_premium',dict(RANK_MODEL=False,FRONT_REACH=None)),('armor50',dict(RANK_MODEL=False,FRONT_REACH=None))]:
  orig=S.MONS
  if n=='armor50':S.MONS=[dict(m,prot=.5) for m in orig]
  scenarios[n]=S.evaluate('rb',dict(S.PARAM,BURN_TIMING=False,**extra));S.MONS=orig
  print('Scenario',n,'done',flush=True)
 (O/'sensitivity.json').write_text(json.dumps(scenarios,ensure_ascii=False,indent=2),encoding='utf-8')
