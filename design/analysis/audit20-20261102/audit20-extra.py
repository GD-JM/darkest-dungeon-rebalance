import runpy,json,copy,re,statistics as st
from pathlib import Path
g=runpy.run_path(str(Path(__file__).with_name('audit20-synergy.py')));S=g['S'];G=g['G'];A=g['A'];P=g['P'];E=g['E'];B=g['B'];O=g['O']
extra={'riposte':[],'callbacks':{},'selected_effects':{},'healing':[]}
for h,sid in [('highwayman','take_aim'),('man_at_arms','retribution'),('duelist','anticipation')]:
 H=S.load_hero(h,'rb');C=S.Ctx(H,E,B,P);l,d=g['skill'](h,sid)
 # A single sustained riposte's damage. Buff-trigger side effects and team redirection are separate.
 es=[S.kv(E[n]) for n in S.ec.effect_names_in(l) if n in E and 'riposte' in S.kv(E[n])]
 assert es,(h,sid)
 for e in es:
  v=C.riposte(e);extra['riposte'].append(dict(hero=h,skill=A.name(h,sid),one_attempt_damage=v,attempts_1=v,attempts_2=2*v,extra_attempt_hp=v,effect=e))
for id,t in G.T.items():
 if not t.get('hero_class_requirements'):continue
 callbacks={k:v for k,v in t.items() if k.endswith('_additional_effects')}
 if not callbacks:continue
 found={};queue=[n for ns in callbacks.values() for n in ns]
 while queue:
  n=queue.pop()
  if n in found:continue
  e=E.get(n);found[n]=dict(row=e,buffs=[])
  if not e:continue
  k=S.kv(e);found[n]['buffs']=[B.get(b.strip('"'),{'missing':b}) for b in k.get('buff_ids',[])]
  queue.extend(S.ec.effect_names_in(e))
 extra['callbacks'][id]=dict(name=t['name'],fields=callbacks,effects=found,trigger_limit=t.get('trigger_limit'))
for n in ['Leper Protect 5','Leper Resist Buff 1','GR Fade Attack 5','GR Dodge 5','RB MUS Cover Dodge 5','Stealth2','RB PD Cure Poison','RB MUS Prey Armor 5']:
 k=S.kv(E.get(n,''));extra['selected_effects'][n]=dict(row=E.get(n),buffs=[B.get(b.strip('"')) for b in k.get('buff_ids',[])])
for h,sid in [('crusader','battle_heal'),('vestal','divine_grace'),('musketeer','patch_up'),('arbalest','battlefield_bandage'),('antiquarian','fortifying_vapours'),('occultist','wyrd_reconstruction'),('plague_doctor','battlefield_medicine')]:
 l,d=g['skill'](h,sid);rank,ids=G.BUILDS[h];v=G.calc(h,l,'rb',ids,rank,P)
 extra['healing'].append(dict(hero=h,skill=A.name(h,sid),range=d.get('heal'),gear=ids,result=v))
(O/'extra.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf-8')
print('Extra complete')
