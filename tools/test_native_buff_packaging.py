"""Regression: package native-ID overrides reached through vanilla effects.
Runs only dependency collection, never writes a game or a published payload.
"""
from pathlib import Path
import json,sys,re,glob,textwrap,os
R=Path(__file__).resolve().parent.parent
G=Path(sys.argv[1])
sys.path.insert(0,str(R/'tools')); import effect_common as ec
cust_eff={}
for p in (R/'effects').glob('*.darkest'):
 for l in p.read_text(encoding='utf8').splitlines():
  m=re.match(r'effect: .name "([^"]+)"',l)
  if m:cust_eff[m[1]]=l
for filename in ['tools/build_workshop.py','tools/refined/build_refined.py']:
 src=(R/filename).read_text(encoding='utf8');a=src.index('    need = []');b=src.index('    if effects:',a)
 block=textwrap.dedent(src[a:b])
 for heroes in [['duelist'],['vestal']]:
  env={'heroes':heroes,'built':heroes,'OUT':str(R),'out':str(R),'src':str(R),'M':str(R),'W':str(R/'design/workshop'),'G':str(G),'GAME':str(G),'pkg':{'key':'test'},'os':os,'glob':glob,'json':json,'re':re,'ec':ec,'cust_eff':cust_eff,'van_eff':ec.load_vanilla_effects(str(G)),'rd':lambda p:Path(p).read_text(encoding='utf8')}
  exec(block,env)
  vals={x['id']:x for x in env['need_b']}
  assert len(vals)==len(env['need_b'])
  ids=[f'DUELIST_TOUCHE_DODGE_{i}' for i in range(1,6)]
  if heroes==['duelist']:
   assert [vals[x]['amount'] for x in ids]==[.3,.32,.35,.37,.4]
  else:assert not set(ids)&vals.keys(), 'DLC override leaked into a base-only package'
  print(filename,heroes,'PASS',len(vals),'buffs')
