from pathlib import Path
import json,math,re,hashlib,subprocess,statistics as st
O=Path(__file__).parent/'all-heroes-20261102';R=Path(__file__).resolve().parents[3]
load=lambda n:json.loads((O/n).read_text('utf-8'))
b=load('base.json');g=load('gear.json');sy=load('synergy.json');extra=load('extra.json');sens=load('sensitivity.json');inv=load('inventory.json');K=inv['names']
for f in (R/'localization').glob('*.string_table.xml'):
 text=f.read_text('utf-8');m=re.search(r'<language id="koreana">(.*?)</language>',text,re.S)
 if m:K.update(dict(re.findall(r'<entry id="([^"]*)"><!\[CDATA\[(.*?)\]\]></entry>',m[1],re.S)))
def name(h,s):return K.get('combat_skill_name_'+h+'_'+s,s)
def hn(h):return inv['heroes'][h]['name']
def finite(x):
 if isinstance(x,float):assert math.isfinite(x)
 elif isinstance(x,dict):
  for v in x.values():finite(v)
 elif isinstance(x,list):
  for v in x:finite(v)
for d in [b,g,sy,extra,sens]:finite(d)
assert len(b['base']['rb'])==20
assert sum(len(x['skills']) for x in b['base']['rb'].values())==140
assert all(x['changed_skills'] for x in b['coverage'].values())
assert len(b['monsters'])==62
assert not any(m['type']=='corpse' for m in b['monsters'])
for mode in ['vanilla','rb']:
 for h,v in b['base'][mode].items():
  for sid,(total,parts,rank) in v['skills'].items():assert abs(total-sum(parts.values()))<1e-8,(mode,h,sid)
gear_delta=[]
for h,d in g.items():
 for key,v in d['rb'].items():
  sid=key.split('|')[0];dif=v['before']['hp']-b['base']['rb'][h]['skills'][sid][0]
  if abs(dif)>1e-7:gear_delta.append([h,sid,dif])
assert not gear_delta,gear_delta
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();assert head==b['commit']
runtime=[p for p in subprocess.check_output(['git','diff','--name-only'],cwd=R).decode().splitlines() if p.startswith(('heroes/','effects/','shared/'))];assert not runtime,runtime
notes={
'abomination':'인간 제어가 강함. 야수 비용은 자기 스트레스의 여유와 억제의 자물쇠를 별도로 봐야 함.',
'antiquarian':'전투 성능은 가장 크게 증가. 회복 장신구·반격 보호 조합과 경제 이득이 있어 추가 일괄 상향 금물.',
'arbalest':'후열 표식 공격·확정 결집 신호탄이 강점. 방어 높은 적에게 총사와 역할이 갈림.',
'bounty_hunter':'표식·기절·출혈 보너스가 겹치는 편성에서 고점이 큼. 사용열 전체와 대상열은 구분해야 함.',
'crusader':'낮은 속도 대신 회복·스트레스 회복·제어를 함께 제공. 전투 치유는 회복 장신구로 역할 확보.',
'duelist':'일반 행동은 하향됐지만 반격/표식/처치 추가 행동 고점은 남음. 발동 장신구까지 보며 관찰.',
'flagellant':'핵심 출혈·위기 회복 구조를 거의 보존. 두 기술 변경만 있다고 미완료로 보지 않음.',
'grave_robber':'돌진·그림자 은신과 높은 속도로 강한 개시. 이동/준비 행동을 계산하지 않은 평균은 과대평가 가능.',
'hellion':'전열에서 적4열 공격을 유지하는 장점. 출혈 저항·탈진으로 상황 차이가 큼.',
'highwayman':'칼질/정맥 절개 공존이 유지. 정맥 절개는 출혈 장신구에서 우위, 칼질은 즉시 피해/3열.',
'houndmaster':'전열·후열 유연성, 보호, 스트레스 회복 유지. 약한 직접 피해만 보고 상향하지 않음.',
'jester':'선율·출혈이 강점. 선율은3열 전용이며 장기전 발라드 누적은 계속 관찰.',
'leper':'명중 구제는 작게 작동. 대열/후열 개입 약점 유지. 평온 점수로 공격 성능을 대신 평가하면 안 됨.',
'man_at_arms':'고양·응징으로 큰 상향. 반격 집중과 파티 스트레스 회복이 겹칠 때 우선 관찰.',
'musketeer':'낮은 무장비 평균·체력/속도 감소. 관통탄은 장갑 상대 강점; 엄호 연막의 선택 이유 재검토 우선.',
'occultist':'전열 제어와 후열 운용 간 격차가 큼. 약화 저주는 물리 조합에서는 충분하므로 일괄 상향 불필요.',
'plague_doctor':'후열 동시 기절의 가치가 장신구에서 크게 상승. 하위 평균을 근거로 상향하면 위험.',
'runaway':'일반전 평균 하향 확인. 후열 불티의 장신구 효율과 다회 행동 적의 지면 발동은 여전히 고점.',
'shieldbreaker':'행동가치는 높지만 기본 피해·속도는 이미 하향. 휘감기/꿰뚫기를 먼저 확인하고 전역 하향은 보류.',
'vestal':'광휘가 약화+화상 공급을 겸해 경쟁력 확보. 물리 조합에서 심판을 밀어내는지 관찰.'}
rows=sorted(b['base']['rb'],key=lambda h:-b['base']['rb'][h]['act'])
out=[];add=out.append
add('20영웅 동일 조건 검토 — 2026-11-02\n')
add(f'기준 커밋 `{head}` / test / 푸시 없음. RUN-011·VES-022만 기존 승인대로 커밋했다. 다른 신규 밸런스안은 적용하지 않았다.\n')
add('**결론**\n')
add('20영웅 모두 원본 대비 변경이 있다. 현 상태에서 전 영웅을 다시 올리거나 내릴 근거는 없다. 강한 쪽은 방패 파괴자의 휘감기, 결투가의 반격 조합, 도망자의 후열 화상 및 다회 행동 적을 먼저 본다. 약한 쪽은 총사의 엄호 연막과 신비학자4열의 행동 선택이 우선이다. 광휘는 추가 상향보다 심판과의 공존을 관찰한다.\n')
add('**무엇을 비교했는가**\n')
add('설치본 PvE 원본 백업과 현재 커밋의20영웅·140개 기술을 비교했다. 기술/무기/방어구5단계, 같은62종 영웅 등급 일반 전투원 분포, 무장비·기벽/야영/영지 강화 없음이 기본이다. 능력치와 효과 변경 유무는1~5레벨 전부 대조했다. 장신구는 PvE 직업 전용167개 정의를 수집하고 각 영웅당 실제2칸 조합1개를 동일 조건으로 평가했다. 이것은 모든 장신구 조합의 최적화가 아니다. 발동 장신구16개의 이벤트/효과 원문도 별도로 추적했다.\n')
add('수치는 **HP 환산 행동가치**이다. 직접 피해 외에 후속 피해, 회복, 스트레스, 제어, 방어 효과를 포함하므로 실제 적 체력이 그만큼 줄었다는 뜻이 아니다. 종합 행동 지표는 상위3기술 평균+무료 행동/모드 보정이다. 기술4칸과 파티 이동을 모두 최적화한 전투 승률이 아니다. 체력·속도는 아래 별도 열로 남겼다. 무기 피해 차이는 정수 피해 산식에 직접 반영한다.\n')
add('기본 회수 가능한 스트레스1점=1.6616HP, 광역 유효 대상=칸수×0.8, 단일/광역 지속 피해 유효율0.9/0.4, 약화 후 타격1.5회/라운드, 평균 전투2.55행동을 사용하는 기존 가정이다. 치료 대상의 부족 HP와 스트레스가 충분하다고 놓는다. 이 가정은 실제 원정 로그로 적합된 확률이 아니다.\n')
add('**이번 비교 실행에서 통일한 항목 — 공통 모델 파일 자체는 추가 수정하지 않음**\n')
add('- 기존 표본에 들어 있던 일반 시체2종(corpse_C/corpse_large_C)을 제외했다. 회피가 양수여서 기존 필터를 통과했지만 전투원이 아니다. 방앗간지기 연결 오브젝트2종도 일반전에서 제외했다.\n- 광휘·섬광 가루에만 남아 있던 라운드 말 화상 지연 보정을 끄고, 도망자와 같은 행동 시작 해석으로 계산했다.\n- 단기/장기 민감도에서 도망자의 화상 평가 기간도2/4회로 바꿨다. 기존 DLC 기본 상태의3회 고정 때문에 전투 길이가 달라도 점수가 그대로인 오류를 피했다.\n- 실제 핵심 코드 전체를 고쳤다는 뜻은 아니다. `audit20-model.py`의 실행 보정이며 원래 기본 결과도 `base.json.default`에 보관했다.\n')
avg0=st.mean(x['act'] for x in b['base']['vanilla'].values());avg1=st.mean(x['act'] for x in b['base']['rb'].values())
add(f'**20영웅 표**\n\n동일 지표의 평균 {avg0:.2f}→{avg1:.2f}({100*(avg1/avg0-1):+.1f}%). 이는 총 난이도 중립의 증명이 아니다.\n')
add('| 영웅 | 바닐라 | 현재 | 변화 | 현재HP/속도 | 변경 기술 | 판단 |\n|---|---:|---:|---:|---:|---:|---|')
for h in rows:
 v=b['base']['vanilla'][h]['act'];r=b['base']['rb'][h]['act'];H=inv['heroes'][h]['rb']
 add(f'| {hn(h)} | {v:.2f} | {r:.2f} | {100*(r/v-1):+.1f}% | {H["hp"]:g}/{H["spd"]:g} | {len(b["coverage"][h]["changed_skills"])}/7 | {notes[h]} |')
add('\n**장신구를 포함한20영웅 대조**\n')
add('횃불100, 착용자HP80%, 기본은 비표식·비화상·비출혈·비은신, 첫 턴 전용 보너스는 미적용. 조건이 충족되지 않는 장신구 효과는 공짜로 주지 않았다. 아래는 해당 사용열에서 가장 높은 기술1개의 변화이며 영웅 전체 점수가 아니다. 행동가치에 없는 받은 회복/스트레스·HP·회피·속도 비용은 반드시 별도로 읽는다. 장신구 전용 발동, 세트 전체 최적화, 모든 외부 확률을 포함한 완전한 장비 점수로 부르지 않는다.\n')
add('| 영웅·사용열 | 장신구2개 | 대표 기술 | 무장비→착용 | 주의할 비용/조건 |\n|---|---|---|---:|---|')
for h in rows:
 d=g[h];usable=[(key,v) for key,v in d['rb'].items() if str(d['rank']) in v['launch'] and not v['free']];key,v=max(usable,key=lambda z:z[1]['after']['hp']);meta=v['after']['gear'];H=inv['heroes'][h]['rb'];cost=[]
 for label,new,old in [('HP',meta['hp'],H['hp']),('회피',meta['dodge'],H['def']),('속도',meta['speed'],H['spd'])]:
  if new!=old:cost.append(f'{label}{new-old:+g}')
 if meta['received_stress']:cost.append(f'받는 스트레스{meta["received_stress"]:+.0%}')
 if meta['received_heal']:cost.append(f'받는 회복{meta["received_heal"]:+.0%}')
 if meta['callbacks']:cost.append('발동 효과 별도')
 if meta['inactive_or_unknown']:cost.append('조건 미충족/미가격 효과 별도')
 add(f'| {hn(h)} {d["rank"]}열 | {" + ".join(d["names"])} | {name(h,key.split("|")[0])} | {v["before"]["hp"]:.2f}→{v["after"]["hp"]:.2f} | {", ".join(cost) or "상세 저항·기타 수치는 gear.json"} |')
add('\n괴인은 표의 인간/야수 기술을 한 턴에 동시에 사용할 수 없다. 부러진 열쇠+전환의 자물쇠는 인간 제어 장비이며 이 표의 높은 야수 기술값을 추천 장비 결론으로 취급하지 않는다. 억제의 자물쇠는 변신 기술 스트레스−40%, 야수 유지 스트레스−40%를 별도 처리해야 한다. 현재 자기 변신 스트레스12, 동료5, 유지6, 복귀 동료회복3이다. 반올림/변동 전에는 동료가5×0.6−3=0이 되고, 유지2회 자기 비용은(12+6×2)×0.6=14.4다. 인간 참회로 확보한 스트레스 여유를 화력으로 바꾸는 의도를 보존한다.\n')
add('**조합에서 달라지는 지점**\n')
add('1. 광휘+물리 공격: 적 회피20·방어25%·약화저항60%,60HP인 한 적에게 광휘 이후 물리 공격2회(토막치기/강타/사악한 칼질의 동일 비중 프로필)가 들어가면 약화만으로 후속+9.27HP. 방어50%에서는+8.46HP. 약화 저주는 각각+6.73/+9.41HP다. 실제로 모든 공격이 도착하기 전에 죽는다면 줄어든다. 시전 자체의 행동 비용·직접 피해·화상은 이 증가분에 포함하지 않았다. 광휘가 모든 상황에서 약화 저주보다 좋다는 뜻도 아니다.\n')
add('2. 광휘+도망자: 광휘5레벨 화상3은 화상이 없는 적에게3회 내4HP, 기존 화상3/6/9에서는 순증6/5/6HP다(모두 실제 틱까지 생존, 명중 이후 조건). 같은 턴의 화상끼리 합쳐진 뒤 정수로 감소하므로 단순 합계보다 증가할 수 있다. 화톳불 성공1회의 추가 화상 피해는 기존6/9/12에서2/3/4HP. 4명 모두 불탄다고 항상 가정하지 않으며 약화 성공·명중·남은HP를 적용해야 한다.\n')
add('3. 역병 의사/괴인/신비학자 제어: 아래는 기술5·회피20·기절저항90인 살아 있는 적의 다음 행동이 남았을 때다. 역병 의사의 실명 기체는 두 적이 유효하면0.85×2=1.70개의 적 행동을 막는다. 이미 기절한 적에게+50저항이 붙으면 각0.35로 낮아진다. 스턴이 있는 적을 치는 최후의 일격/끝장내기는 기절이 끝나기 전에 공격 순서가 돌아와야 한다.\n')
add('| 기술 | 장신구 | 첫 기절 성공률 | 회복저항+50 후 |\n|---|---|---:|---:|')
for x in sy['stuns']:
 if x['ids']:add(f'| {x["skill"]} | {" + ".join(inv["trinkets"][i]["name"] for i in x["ids"])} | {x["success"]["90"]:.2%} | {x["success"]["140"]:.2%} |')
add('\n4. 표식: 신비학자3열이 표식을 걸고 현상금 사냥꾼2열 또는 석궁사수/총사4열이 따라가는 합법적 구성이다. 같은 한 적에 대해 회피20·방어0에서 현상금 수거+12.85HP, 저격+12.60HP, 관통탄+5.16HP가 직접 피해 증가분이다. 표식 행동이 공짜는 아니며 두 번 이상의 유효 후속타가 도착하는지가 핵심이다. 방어50%에서 저격의 표식 직접 기대는12.41HP, 관통탄은17.66HP다. 총사의 평균이 낮아도 장갑 대응 역할은 살아 있다.\n')
add('5. 반격 집중: 동료 방패 같은 기술로 반격 영웅이 더 많은 공격을 받게 하면 반격 횟수에 비례해 이득이 커진다. 공격을2번 받는 경우를 기본1번과 비교하면 추가1회분만 더해야 한다. 보호 피해 예방과 같은 공격의 회피/방어를 중복으로 더하지 않는다. 표식은 AI 유도를 보장하지 않으며 광역/무시 기술도 있다.\n')
for x in extra['riposte']:add(f'- {hn(x["hero"])} {x["skill"]}: 현재 일반 몬스터 분포에서 반격 시도1회 직접 기대{x["one_attempt_damage"]:.2f}HP. 치명 스트레스/회복 발동은 별도.\n')
add('6. 결투가: 공격 자세·기절한 적·남은HP6·회피20·다른 적이 남는 조건에서 최후의 일격은 직접6HP+다음 행동7.17HP, 여기에 회수 가능한 치명 스트레스/직업 효과9.97HP를 더해23.14HP 환산이다. 현재HP12면 확정 처치가 아니므로 추가 행동0이다. 따라서 일반 표의8.02를 그대로 사장된 기술로 보면 안 된다. 망령의 재치는 반격 치명 시 최대HP10%, 반격 처치 시25% 회복이므로 촉발 빈도와 과회복을 별도로 추정해야 한다.\n')
add('7. 도망자의 남은 장기전 위험: 기술5 통제된 화상(최초5·지면5·2라운드)을 적중시키고 그 열에 충분한HP의 적이 유지되면3라운드 내 화상은 적1행동/라운드에서25HP,2행동/라운드에서47HP다. 최초 명중·이동 없음·화상 지연 없음이라는 조건부 원시 총량이며 실제 보스 처치 피해를 관측한 값은 아니다. 지옥불 석탄의 강제 이동·들불 양쪽 확산과 결합하면 추가 진입/확산 경로가 생긴다. 보스전 하향은 불티 전역 하향보다 이 발동 빈도부터 검증할 근거가 있다.\n')
add('**실제 조정 우선순위 — 아직 적용하지 않은 판단**\n')
add('- 우선 관찰: 방패 파괴자 휘감기(23.83), 도망자 후열 불티(장비18.00→22.74)·다회 행동 적의 지면, 결투가 반격 집중 및 발동 장신구, 중보병의 고양+응징. 방패 파괴자는 무기5 피해9–18→8–16·속도9→7이 이미 적용돼 있어 높은 행동점수만으로 전체 하향하지 않는다.\n- 추가 상향 중단: 광휘. 현재13.20 대 심판10.62이며, 성녀 회복 장비를 끼면 광휘12.71 대 심판7.67이다. 화상/약화가 직접 피해 감소 장신구의 영향을 적게 받기 때문이다. 물리·화상 편성에서 광휘 선택은 자연스럽지만, 심판이 빠른 즉시 처치 역할로 남는지 확인해야 한다.\n- 약한 후보: 총사 엄호 연막4.09와 신비학자4열. 신비학자 상위3기술 평균은1·2열14.04,4열11.41이다. 다만 약화 저주는 장갑 물리 조합에서 충분한 이득이 있으므로 방어 감소를 또 높이는 결론으로 연결하지 않는다. 총사도 관통탄 장갑 대응은 유지하고 엄호 연막의 회피·은신 중첩 효용과 실제 사용 빈도를 먼저 확인한다.\n- 모델 보완 우선: 나병환자 인내0.55, 역병 의사 강화 작용제2.42. 전투 종료까지 지속/회수 제한을 일률 할인하고, 저항·강화 대상의 실제 공격 수를 충분히 반영하지 못하므로 이 숫자를 근거로 즉시 상향하지 않는다.\n- 노상강도는 무장비 정맥 절개16.21·사악한 칼질15.40 안팎에서 출혈 포함 장기 이득과 즉시 피해/3열 접근으로 구분된다. 장갑·출혈 면역·다음 틱 전에 죽이는 상황을 나눠야 하며 한 지표로 어느 하나를 삭제할 근거는 없다.\n')
add('**변경하지 않은 영웅 / 덜 변경한 영웅**\n')
add('완전히 미조정인 영웅은0명이다. 비교 기준은 원본에 없는 기술 ID 개수가 아니라 같은 기술의 명중·피해·열·참조 효과 및 강화 정의까지 포함한 실제 차이다.\n')
for h in sorted(rows,key=lambda h:len(b['coverage'][h]['changed_skills'])):
 c=b['coverage'][h];add(f'- {hn(h)}: {len(c["changed_skills"])}/7 변경. 원본 유지: {", ".join(name(h,s) for s in c["unchanged_skills"]) or "없음"}.\n')
add('\n역병 의사2/7, 고행자2/7, 도굴꾼3/7, 광대3/7은 변경이 적지만 검토 누락이라는 뜻이 아니다. 바닐라 정체성을 의도적으로 보존한 기술도 포함한다.\n')
add('**신뢰 범위와 다음 모델 작업**\n')
add('장신구 부정 효과·조건부 발동은 원문과 계산 적용 여부를 gear.json/extra.json에 분리했다. 전체 직업 장신구167개의 모든 발동을 전투 시뮬레이션으로 자동 가격화한 상태는 아니다. 특히 가연성 액체의 적 치명−6%/받는 치명+6%·자기 화상2·12회 제한, 지옥불 석탄의 자동 이동·확산, 아카데미 반지의 빗나감 회피−10 및 우호 기술 명중+10, 망령의 재치의 반격 치명/처치 회복은 단순 공격력/명중 합산표에 들어가지 않는다. 따라서 장비 표는 그 조건부 추가효과를 누락한 채 절대 우열을 선언하는 자료가 아니다.\n')
add('추가로 괴인의 준비된 자기 스트레스 자원, 도굴꾼의 돌진-그림자 은신 왕복, 평온/참회 과회복, 회복기의 출혈 부작용·중독 제거, 인내의 저항, 스톨링의 전투 전체 비용은 현재 평균 지표에 남는 한계다. 스트레스 가치0 시나리오는 비용도0으로 되므로 괴인·고행자의 점수가 오를 수 있다. 낮은 점수=약함, 높은 점수=너프라는 판정기를 만들지 않는다.\n')
add('재현 파일: audit20-model.py, audit20-gear.py, audit20-synergy.py, audit20-extra.py. 원자료: inventory.json, base.json, sensitivity.json, gear.json, synergy.json, extra.json. 모든 스크립트는 게임 데이터 읽기 및 outputs 결과 저장만 수행한다.\n')
(O/'review.md').write_text('\n'.join(out),encoding='utf-8')
detail=['140기술 세부 HP 환산값 — 기술5, 무장비, 동일62전투원\n','주 보고서 review.md의 가정과 제한을 함께 읽어야 한다. 각 효과 숫자는 실제 피해가 아닌 환산 기여다.\n']
for h in rows:
 detail+=['\n**'+hn(h)+'**\n','| 기술 | 바닐라 | 현재 | 사용→대상 | 현재 기여 |','|---|---:|---:|---|---|']
 for sid,v in b['base']['rb'][h]['skills'].items():
  orig=b['base']['vanilla'][h]['skills'].get(sid);fields=next(d for l,d in inv['heroes'][h]['rb']['skills'] if d['id'][0].strip('"')==sid);target=(fields.get('target') or [''])[0]
  detail.append(f'| {name(h,sid)} | {orig[0]:.2f} | {v[0]:.2f} | {v[2]}→{target} | '+', '.join(f'{k} {x:+.2f}' for k,x in v[1].items())+' |')
detail+=['\n**민감도**\n','| 영웅 | 기본 | 짧은 전투 | 긴 전투 | 스트레스 가격0 | 사거리 프리미엄 제외 | 방어50%·사거리 제외 |','|---|---:|---:|---:|---:|---:|---:|']
for h in rows:detail.append('| '+hn(h)+' | '+f'{b["base"]["rb"][h]["act"]:.2f}'+' | '+' | '.join(f'{sens[k][h]["act"]:.2f}' for k in ['short','long','no_stress_value','no_rank_premium','armor50'])+' |')
(O/'skill-details.md').write_text('\n'.join(detail),encoding='utf-8')
validation=dict(commit=head,heroes=20,unique_skills=140,monster_population=62,class_trinkets=sum(bool(t.get('hero_class_requirements')) for t in inv['trinkets'].values()),gear_builds=20,finite=True,component_sums=True,gear_baselines_identical=True,uncommitted_runtime_changes=runtime,push=False,game_runtime_test=False,model_file_changes=False)
validation['source_hashes']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for parent,pattern in [('heroes','*.info.darkest'),('effects','*.effects.darkest'),('shared','*.json'),('tools','*.py')] for p in (R/parent).rglob(pattern)}
(O/'audit-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print('Report ready; finite sums, 20/140 coverage, gear baseline equality and committed runtime verified')
