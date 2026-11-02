from pathlib import Path
import sys,json,subprocess
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent/'all-heroes-20261102'
sys.path.insert(0,str(R/'tools'))
import strength as S
K={k:v for k,v in S.ec.load_korean(S.G).items() if k.startswith(('combat_skill_name_','str_inventory_title_trinket'))};B=S.ec.load_buffs(S.G,str(R))
entries={};excluded=[]
for root in [Path(S.G)/'trinkets',Path(S.G)/'dlc',R/'trinkets',R/'dlc']:
 for f in sorted(root.rglob('*.entries.trinkets.json')):
  if 'arena' in str(f):continue
  try:data=json.loads(f.read_text('utf-8-sig'))
  except Exception as ex:excluded.append([str(f),str(ex)]);continue
  for t in data.get('entries',[]):
   t=dict(t);t['source']=str(f);t['name']=K.get('str_inventory_title_trinket'+t['id'],K.get('str_inventory_title_trinket_'+t['id'],t['id']));t['details']=[B.get(b,{'id':b,'missing':True}) for b in t.get('buffs',[])];entries[t['id']]=t
out={'trinkets':entries,'excluded':excluded,'names':K,'heroes':{h:{'name':name,'vanilla':S.load_hero(h,'vanilla'),'rb':S.load_hero(h,'rb')} for h,name in S.KO.items()},'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()}
(O/'inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for h in S.KO:
 print(h,[(t['id'],t['name']) for t in entries.values() if h in t.get('hero_class_requirements',[])])
print('rules',sorted({str(b.get('rule_type')) for t in entries.values() for b in t['details']}))
print('stats',sorted({str(b.get('stat_type')) for t in entries.values() for b in t['details']}))
