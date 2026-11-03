from pathlib import Path
import re,sys,json
G=Path('C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon')
R=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(G/'mods/Rebalance/tools'));import strength as S
hero=(R/'heroes/occultist/occultist.info.darkest').read_text(encoding='utf-8')
skills={S.first(d,'id'):d for l in hero.splitlines() if l.startswith('combat_skill:') and '.level 4 ' in l for d in [S.kv(l)]}
rows=[]
for name in ['skeleton_courtier','skeleton_defender','swine_skiver','fishman_shaman']:
 m=name+'_C';raw=(G/f'monsters/{name}/{m}/{m}.info.darkest').read_text();d=S.kv(next(l for l in raw.splitlines() if l.startswith('stats:')))
 num=lambda k:S.num(S.first(d,k))
 for gear,acc,crit,move,debuff,stun in [('none',0,0,0,0,0),('ring+cauldron',10,8,0,40,30),('vial+cauldron',0,3,20,60,50)]:
  x=dict(monster=m,gear=gear,first=S.p_before(8,num('spd')));rows.append(x)
  for sid,v in skills.items():
   if sid=='wyrd_reconstruction':continue
   hit=S.hit_probability(S.num(S.first(v,'atk'))+acc,num('def'));c=(10+crit+S.num(S.first(v,'crit')))/100
   bonus=({'bloodlet':.35,'abyssal_artillery':.25}.get(sid,0) if name=='fishman_shaman' else 0)
   x[sid]=round(hit*S.damage_mean((7,13),S.num(S.first(v,'dmg')),c,num('prot'),bonus),3)
   def p(base,res):
    q=lambda b:max(0,min(1,(b-res)/100))
    return hit*((1-c)*q(base)+c*q(base+20))
   if sid=='hands_from_abyss':x['stun']=p(150+stun,num('stun_resist'))
   if sid=='daemons_pull':x['pull']=p(140+move,num('move_resist'));x['first_pull']=x['first']*x['pull']
   if sid in ('weakening_curse','disruptive_curse'):x[sid+'_proc']=p(140+debuff,num('debuff_resist'));x['mark_hit']=hit
  if name=='skeleton_defender':
   x['shred_2x14']=x['weakening_curse']+x['weakening_curse_proc']*28*.35
   x['stun_4.26']=x['hands_from_abyss']+x['stun']*4.26
  print(name,gear,*[round(x[k],2) for k in ['bloodlet','abyssal_artillery','daemons_pull','pull','first_pull','weakening_curse','weakening_curse_proc','disruptive_curse','mark_hit','stun']],round(x.get('shred_2x14',0),2),round(x.get('stun_4.26',0),2))
Path(__file__).with_name('results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
