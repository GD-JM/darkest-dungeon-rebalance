from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent/'all-heroes-20261102';sys.path.insert(0,str(R/'tools'))
import effect_common as ec
import dlc_valuation as D
G=R.parent.parent;B=ec.load_buffs(str(G),str(R));inv=json.loads((O/'inventory.json').read_text('utf-8'));sets={};empty=[]
for root in [G/'trinkets',G/'dlc',R/'trinkets',R/'dlc']:
 for f in root.rglob('*.sets.trinkets.json'):
  if 'arena' in str(f):continue
  data=json.loads(f.read_text('utf-8-sig'))
  if not data.get('sets'):empty.append(str(f))
  for s in data.get('sets',[]):sets[s['id']]=dict(source=str(f),raw=s,buffs=[B.get(n,dict(missing=n)) for n in s.get('buffs',[])])
burn={str(actions):D.burn_trace(5,rounds=3,zone=5,zone_rounds=2,actions=actions,hp=100)[0] for actions in [1,2]};assert burn=={'1':25,'2':47},burn
(O/'set-bonuses.json').write_text(json.dumps(dict(sets=sets,empty=empty,controlled_burn_events=burn),ensure_ascii=False,indent=2),encoding='utf-8')
lines=['\n**세트 보너스 정의 추가 확인**\n','직업 전용 장신구 정의와 별도로 세트 보너스도 읽었다. 도망자·결투가의 설치본 sets 파일은 빈 배열이다. 이름에 set이 붙었다는 이유로 존재하지 않는 추가 세트 효과를 가산하면 안 된다. 아래는 실제 정의이며, 대표2칸 조합 표는 이 세트를 완성한 조합을 사용하지 않는다.\n']
for k,v in sets.items():
 lines.append('- '+k+': '+'; '.join(f'{b.get("stat_type")}/{b.get("stat_sub_type", "")} {b.get("amount")} [{b.get("rule_type")}, {b.get("rule_data")}]' for b in v['buffs'])+'\n')
lines.append('\n세트 완성 조건의 낮은HP·특정열·표식/기절·횃불 등은 기본 상태에서 모두 충족한다고 가정하지 않았다. 실제 효율 최적화는 각 조합의 두 슬롯 비용과 조건 유지율을 함께 비교해야 한다.\n')
p=O/'review.md';t=p.read_text('utf-8');marker='\n**세트 보너스 정의 추가 확인**';t=t.split(marker)[0];p.write_text(t+'\n'.join(lines),encoding='utf-8')
print('sets',len(sets),'CB verified',burn)
