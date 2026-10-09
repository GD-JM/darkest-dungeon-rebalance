# 광대 (jester) 변경 항목

바닐라 수치: `heroes/jester/jester.vanilla.txt`

---

### JES-001 독주: 시체 제거 추가 (적용 2026-09-29, 검토 2026-09-28)

- 제작자 의도: "3·4열 하나를 자르고 독주로 시체를 치운 뒤 3열을 바로 대단원으로 자를 수 있다."
- **전제 확인**: 대단원(heroic_end)의 대상은 바닐라부터 **1·2·3·4열 전부**다. 시체가 있어도 3·4열의 산 적을 직접 칠 수 있어, 시체 제거가 이 연계를 새로 열지 않는다.
- 3열 적을 자르고 4열이 살아 있으면, 시체 제거는 4열 적을 3열로 한 칸 당길 뿐이다. 여전히 후열이라 스트레스 기술을 쓴다. 대상이 3열까지인 기술(저며내기·수확의 낫질 2·3열 등)이 닿게 되는 효과는 있으나, 독주를 쓴 광대는 1열로 이동해 그 기술들을 못 쓴다.
- 설정: 독주의 효과 이름이 `Jester Spotlight`(무대 조명)라 "무대를 비운다"는 해석은 가능하다(P-19 약함~보통).
- 판단: 넣어도 해는 없지만(모델 3.3 → 3.8 HP) **독주를 쓸 이유는 만들지 못한다.** 독주의 문제(대단원 준비 외 역할이 없음)는 따로 본다.
- **제작자 반론 (2026-09-29)**: "대단원은 3열까지밖에 안 닿는다. 3열을 죽인 상태면 독주를 쓰는 순간 시체가 치워져 4열이 3열로 끌려온다."
  - 연계 논리: 3열 처치 → 3열 시체, 4열 생존 → 독주(광대 1열 이동 + 시체 제거) → 4열 적이 3열로 → 대단원으로 처치. **대단원이 3열까지라면 성립한다.**
  - 데이터 확인: 설치본 `jester.info.darkest`, 원본 `jester.info원본.darkest`, 이 모드 파일 모두 `heroic_end` 5개 레벨이 `.launch 12 .target 1234`다. 구독 중인 창작마당 모드 14개 중 광대를 건드리는 것은 UI Enhancement의 그림 파일(`jester.art.darkest`)뿐이다.
  - 검증 목록 **V-08**: 게임에서 대단원이 4열을 대상으로 잡는지. 4열이 안 잡히면 이 모드가 모르는 규칙이 있는 것이고, 제작자 연계가 성립하므로 독주 시체 제거를 적용한다.
- **결정 (제작자 2026-09-29)**: "일단" 적용한다. `solo` 1~5레벨에 `clear_corpses` 추가, 나머지 수치는 그대로.
- 수치 (v2, 자기 무기 기준 환산 피해 보정): 독주 −56%p → **−49%p** (시체 +7%p).
- 남은 확인: V-08(대단원 4열 도달). 4열에 닿는다면 이 연계의 근거가 약해지므로 그때 다시 본다.


### 2026-10-05 광대 전수 검사 (분석만)

- 설치 원본·백업·현재 모드 기술35줄씩/능력치/참조 효과·강화 효과/고정 PvE 장신구8개+CC세트/야영7개/구획 theater를 확인했다. 현재 차이는 JES-001 독주 시체 제거5줄뿐이며 신규 수치 수정 없음.
- 상세 보고서: `../analysis/jester-full-review.txt`, 원문·계산: `../analysis/jester-full-review.json`. 재현 스크립트는 이어가기 작업공간 `outputs/jester-audit.py`, `jester-supplement.py`, `jester-report.py`에 보관한다.
- **기존 독주 판단 정정:** 원본부터 자기 표식3턴과 회피+20→30(효과 duration4)이 있다. 고회피 광대에게 공격을 유도하는 방어적 운용과 대단원 약화에 대비하는 용도가 있으므로 '대단원 준비 외 역할이 없음'으로 단정하지 않는다. 시체 제거가 대단원 접근을 새로 열지 않는다는 데이터상 판단과 V-08의 게임 확인 과제는 유지한다.
- 대단원은 적1234 대상/전투당1회/후퇴3칸이다. 사용 뒤 회피−25·속도−3·받는 스트레스+100%, 전투 끝까지·약화 제거 불가. 별도 피해 감소·체력 감소는 현재 참조 효과에 없다. 독주 회피가 대단원 뒤에도 남는 시간과 표식 위험은 게임 확인 필요.
- 대단원 전용 `rule_type skill` 강화의 일반 공격 배정을 제외하고 실제 대단원 경로에 따로 반영했다. 발라드의 자기 명중+10·치명+6%p를 대단원 전용 치명+8%p와 함께 반영하며 선율 경로와 구분한다. 한 번 행동을 제한1/3·2/3으로 할인하던 규칙도 별도 비교에서 제거했다. **live strength.py 수정은 없다.**
- 직업 치명은 주는 스트레스 회복+40%. 유효한 후속 선율1회가 있어야 그 가치를 얻는다. CC세트+33%는 야영 조건이고 전투 선율에 상시 합산하지 않는다. 자기 이동·상위3개 평균·고정 출혈 틱·부족한 초과 회복 표현의 한계를 함께 기록했다.
- 지원·공격 일괄 상향은 권하지 않는다. 단검/출혈/독주·대단원/발라드/선율의 선택과4슬롯 기회비용을 보존한다. 선율5레벨12→11 또는 받는 스트레스 억제20→17.5% 등은 독립 민감도 후보이며 미승인·미적용이다. 회복12→10을5레벨만 바꾸면4레벨11보다 낮아지므로 그 방식은 기각한다. 총량 보존을 기술 점수의 단순 합으로 선언하지 않는다.
- 유한 수치·열 경로·후속 선율·초과 회복·처치 지평을 검사했고 영웅/효과/편집 사본/도구58파일 해시가 일치한다. 이는 계산 검증이며 게임엔진 테스트가 아니다. 기존 사용자 수정과 부츠 DUE-002 등 승인 변경을 보존했다.


### 2026-10-05 追加 검토: 2·4열, 발라드와 단검 (미승인 조정안)

- 사용자 요청:2열 선율 개방의 과도함, 다른 강화기와 비교한 발라드 조정, 단검의 낮은 선택률과4열 운영을 검토한다. 원문은 `../analysis/jester-position-buff-options.txt`에 그대로 보존했다. 전체 원본·현재 정의 및162시나리오는 동명 `.json`.
- 선율 사용34→234는 수치 유지여도 이동·지원 타이밍을 개선하는 상향이다. 발라드/독주는34를 유지해2열은 출혈·스트레스 지원, 후열은 팀 강화·스트레스 지원으로 분리하는 후보.2열에서 쓸 수 있는 기술4→5개 중4개 선택이 생긴다.
- 다른 강화기: 지휘5는 명중+10/치명+8%p 및 보호받음(is_guarded) 피해+25%; 강화 작용제5는 단일 피해+25%/속도+5·전투 끝까지·2회. 고양의 모드 즉시 스트레스−2, 고양의 연막3턴·반복, 복수의 자기 위험, 그림자 은신의 후퇴·다음 공격도 원문으로 대조했다. 발라드를 모든 상황의 최강이라고 단정하지 않는다.
- 우선안: 발라드 명중5/6/7/8/10·치명2/3/4/5/6 유지, 속도2/2/3/3/4→1/1/2/2/2. 강한 안은 치명1/2/2/3/4까지 축소한다. 팀 치명 필드라도 기존 연계를 약하게 하므로 P-21의 연계 보존을 고려해 속도만 낮추는 안을 먼저 제시한다. 전투당 제한·대단원 전용 강화·장신구는 그대로.
- 공통 공격자2명×2라운드에서 발라드 현재+28.32/속도2안+18.83/치명4·속도2안+1.16%p. 표준평타 환산으로, 실효 후속 공격·치명 스트레스·선제 처치 가정이 있다. 지휘 보호받음 상한과 비교하고 실제 보호를 거는 행동 비용을 무료로 주지 않는다. 사용 열 확장과 숫자 변화의 합으로 총량 보존을 선언하지 않는다.
- 단검 우선 후보: 명중1레벨85→90·피해0 유지, 부분 보완+8.28%p.3→2 전진 뒤 선율을 계속 쓸 수 있는 해금과 연결한다. 명중90/피해−10은−4.35%p로 주안 아님,95/−10은+3.40%p의 안정성 대안. 치명·보호 무시·전진1·대단원 준비는 유지하고 적4열 도달은 동시에 추가하지 않는다.
-4열은 이미 지원 사용 위치다. 정착 공격이 필요하면 수확 사용23→234를 별도 후보로 둔다. 저며내기4열보다 집중 처치·높은 명중/치명을 덜 확장한다. 수확 피해−55는 열 확장에 대가를 붙이는 추가 후보이고 자동 포함하지 않는다. 직접 피해−7.04%p이며 출혈은 유지.
- 신규 수치·열·효과·live strength.py 수정 없음.7강화기×5레벨×원본/현재70줄,162시나리오,4열 해금 목록, 단검5안, 성장 역전 없음을 확인했다. 라이브58파일 바이트 보존. 조정안 모두 미승인·미적용.


### 2026-10-05 승인 묶음 적용: JES-002/003/004

- 사용자 지시 원문: "발라드 속도를 11223으로 하자 치명은 12345로 하자 나머지도 반영 내 생각엔 독주를 1234 전열 사용가능으로 바꾸는 것도 괜찮아 보이는데 너의 생각은? 독주는 도대체 활용성이 뭐야? 대단원은 어차피 다른거 해도 알아서 상승하잖아 굳이 독주 넣어야할 필요성 없어 보이는데?"
- 앞선 우선 묶음의 선율2열·단검 명중90을 함께 반영한다. 사용자 지정 발라드 성장값이 앞선 미승인 속도 상한2 및 치명1/2/2/3/4 후보를 대체한다. 독주1234는 의견을 묻는 검토안이며 이번 적용에 포함하지 않는다. 수확4열/피해−55는 별도 미승인 후보로 남는다.

### JES-002 전투의 발라드: 속도·팀 치명 완화 (적용 2026-10-05)

- 상태: 사용자 승인·적용. 목표: 조합 다양성과 강화기 선택의 균형.
- 기술1~5레벨 팀 속도2/2/3/3/4 → **1/1/2/2/3**, 팀 치명2/3/4/5/6 → **1/2/3/4/5%p**. 팀 명중5/6/7/8/10은 유지한다.
- 의도·근거: 명중·속도·치명이 동시에 높은 전체 강화의 총량을 낮추면서 세 능력치와 지원 정체성을 보존한다. 속도5레벨3은 사용자 지정으로 이전 제안 상한2보다 높다. 기존 연계의 영향을 고려하는 P-21에 대해 팀 치명−1%p는 이번 명시적 선택이며, 공격 기술 자체의 치명 보정을 조정하지 않는다.
- 영향: 강화 중 적중 안정성은 유지하되 선행 확률·공격 치명·치명 스트레스 회복 기여가 줄어든다. 대단원 전용 피해+30%/치명+8%p 효과 자체는 유지하며 발라드 팀 치명의 대단원 기여만−1%p다. 고정 장신구·원본 공유 효과는 보존하고 변경5효과를 광대 전용 이름으로 적용한다.

### JES-003 격려의 선율: 2열 사용 허용 (적용 2026-10-05)

- 상태: 사용자 승인·적용. 목표: 2열 출혈·스트레스 지원 조합과4슬롯 선택 확장.
- 전 레벨 사용34 → **234**. 회복량8/9/10/11/12, 받는 스트레스 완화10/12.5/15/17.5/20%, 대상 열과 대단원 준비는 유지한다.
- 의도·근거: 2열 공격 광대가 후퇴 행동 없이 스트레스 지원을 선택할 수 있게 한다. 숫자가 같아도 행동 비용 감소에 따른 상향이며, 발라드 완화와 함께 검토하되 영웅 총량 보존을 기술 점수의 단순 합으로 선언하지 않는다.
- 영향: 단검으로3→2 이동한 뒤 선율 사용 가능. 발라드·독주는34를 유지하고 저며내기·수확은23를 유지해2열 지원/공격과 후열 전체 강화를 구분한다.

### JES-004 단검찌르기: 명중 보완 (적용 2026-10-05)

- 상태: 사용자 승인·적용. 목표: 보호 무시·전진·직접 공격 경로의 선택성.
- 기술1레벨 명중85 → **90**; 전 레벨90/95/100/105/110. 피해0% 및 기술1레벨 치명+5%(성장5/6/7/8/9%), 보호 무시·전진1·대상123·대단원 피해 준비+30%는 유지한다.
- 의도·근거: 출혈 공격과 이동만으로 대체되던 단검의 안정성을 일부 보완한다. 명중+5/피해−10%p를 붙이면 기존 비교보다 약해지는 후보였으므로 이번에는 피해 대가 없이 부분 상향한다. R의 통상 교환에서 의도적으로 이탈하며 사용 열 확장과 별도로 기록한다.
- 앞선 공통 표준 평타 환산 비교에서+8.28%p(5레벨 무장신구·기존 모델 가정), 실제 조합·전투 길이의 총가치를 증명하지 않는다. 관련 고정 장신구8개+CC세트의 스트레스 회복·출혈·명중·치명·전열 회피 축을 보존한다.

### 적용 검증과 후속 확인

- 변경35기술줄/효과 성장/참조/관련 원본과 사용자 미커밋 파일을 대조한다. 광대만 대상으로 효과 편집 도구와 주석 검사를 실행하고 신규 효과가 포함된 모드 목록을 생성한다.
- 독주 사용1234 또는234는 미승인·미적용이다.1열 허용 시 제자리 독주2회→대단원 경로가 열릴 수 있으므로 사용 열과 준비 누적을 함께 검토한다.
- 버프 중첩·기간·표식 공격 유도·대단원 뒤 회피 잔존 및 실제 툴팁은 게임 확인이 남는다. 이번 검증은 설치 데이터와 계산 검증이다.


### 2026-10-05 승인 적용 후 독주 사용 열 비교 (분석만)

- 현행 독주34 유지. 검토안234는2열→1열 진입과 회피·표식 운용을 추가한다.1234는1열 제자리 독주2회→대단원3행동을 추가하므로 단순 열 해금 이상이다. 대단원 피해+150%/치명+16%p 준비 누적 및 회피 중첩은 게임 확인 필요.234를 첫 검토안으로 권한다. 어떤 독주 열 변경도 이번에 승인·적용하지 않았다.
- 독주는 준비 피해+75%/치명+8%p·전진3이며, 공격은+30%와 직접 피해/출혈, 노래는+30%/치명+8%p와 지원이다.4열 독주→대단원은2행동이나 단검2회→대단원은3행동.3열에서는 둘 다2행동으로 즉시 피해까지 비교해야 한다.
- 같은 적123 대상·회피20/방어0/체력30, 무기·기술5레벨/무장신구·곱셈 피해 준비·반올림 제외·기존적중 가정에서 단검→대단원 처치57.10%, 독주→대단원46.43%. 체력40에서는20.74%/25.00%로 뒤집힌다. 피해 합산/명중 대안과72상황×3경로(216개 계산)를 기록했다. 표식·회피·시체·치명 스트레스·아군 지원·적 행동·대단원 후 약화 비용을 제외한 직접 피해 비교이므로 전체 판정이 아니다.
- 발라드 승인값의 동일 후속2명×2라운드 비교는28.32→15.18%p(−13.15%p), 후속 명중105/치명10%/속도7 및 선제처치기여.393·회복가능 스트레스 가정. 독주·선율·단검의 종합 가치와 혼합하지 않는다.
- 상세 및 재현은 이어가기 작업공간 outputs/jester-approved-and-solo-review.txt/.json 및 verify-jester-and-solo.py. 데이터 대조144항목, 관련 원본·사용자 수정·도구58파일 바이트 보존. 주석 검사는 광대 범위로 통과; 무관한 기존 사용자 주석/공백은 정리하지 않았다.


### JES-005 독주: 전 열 사용 허용 (적용 2026-10-05)

- 상태: 사용자 승인·적용. 분류: 의도적 사용 열 확장. 목표: 조합 다양성과 독주의 실용적 선택성.
- 사용자 지시 원문: "그렇게 해보자 다른 기술이 너무 좋아서 (선율,버프 수확 저며내기) 독주도 나름 실용성 있게 만드는 걸 목표로 해보자"
- 승인 맥락: 사용1234 제안 후 탱킹·대단원 강화 상한을 검토했고, 독주의 전 열 해금을 적용하라는 후속 지시로 반영한다. 앞선234 우선 검토 의견과1234 미승인 표시는 해당 시점의 기록이며 이번 승인이 대체한다.
- 변경: 독주 기술1~5레벨 사용34(`.launch 43`) → **1234**. 전진3, 자기 표식3턴, 회피20/22/25/27/30(효과duration4), 대단원 준비 피해+75%/치명+8%p, 전투당2회, 적 전체 대상, 명중1레벨125·기술 치명0 및 JES-001 시체 제거는 유지한다.
- 의도: 선율·발라드·수확·저며내기의 높은 선택 가치 사이에서 독주가 후열의 대단원 진입뿐 아니라 전열의 회피·표식 운용으로 기술 슬롯을 얻도록 한다. 수치 추가 효과 대신 기존 효과의 사용 기회를 확장한다.
- 근거: 5레벨 무장신구 회피35→65, 적명중100에서 피격65→35%로 같은 공격 횟수의 기대 직접 피해46.2% 감소. 표식 때문에 광대 개인 피해가 증가해도 파티 피해가 감소할 수 있으므로 보호와 개인 안전은 구분한다. 적별 대상 열·표식 선호·표식 추가피해를 고려한다. 자세한 계산은 이어가기 outputs/solo-tanking-cap-review.txt/.json.
- 원칙 대조: 전열 사용은 행동·재배치 비용을 줄이는 상향이다. 앞선 발라드 완화와 함께 선택지를 비교하되 전체 총량 보존을 선언하지 않는다. 기술/효과ID·치명 수치·고정 장신구·바닐라 공유 효과를 보존한다. 폭군의 손가락뼈의 전열 회피·속도 축과 함께 검토하지만 조건 적용을 무료 상시 강화로 계산하지 않는다.
- 영향: 2열→1열 독주 진입,1열 제자리 독주,1열에서 두 번 독주→대단원 경로가 데이터상 허용된다. 사용 가능 횟수는2회로 유지된다. 대단원을 이미 사용한 뒤에도 회피·표식 재사용의 목적은 남지만 대단원 준비는 재사용할 대단원이 없어 기여하지 않는다.
- 전열 광대의 기술 선택: 1열은 단검·독주·대단원 중 선택; 2열은 단검·수확·저며내기·독주·대단원·선율 중4개 선택; 3열은 단검·수확·저며내기·독주·발라드·선율; 4열은 단검·독주·발라드·선율. 수확4열은 포함하지 않는다.
- 강화 상한: PvE 정의에서 별도 최대 강화 수치 필드를 찾지 못했지만 엔진 상한 부재를 입증한 것은 아니다. 두 번 독주의+150%/+16%p는 정상 중첩·유지와 상한 비적용을 전제로 한 계산이다. 회피 중첩·기간·준비 적용을 게임에서 확인한다.
- 플레이 검증: 전 열 사용과 전진·밀려나는 동료 위치,1열 연속 사용의2회 제한, 회피의 중첩/갱신, 대단원 준비의 누적/상한, 표식 유도와 특효 피해, 즉시 대단원 뒤 회피−25·받는 스트레스+100%를 확인한다. 독주가 다른 기술 대신 채용되는지·첫 사용 이후 제자리 두 번째 사용이 항상 정답이 되는지를 기록한다.
- 이력: JES-001 시체 제거를 유지하고 JES-005 사용 열 확장을 추가한다. 기존 한국어 제작자 주석은 원문 그대로 보존한다. JES-002/003/004 발라드·선율·단검 변경은 유지한다.


### JES-006 독주: 회피 전 레벨 +5 (적용 2026-10-05)

- 상태: 사용자 승인·적용. 목표: 조합 다양성·전열 독주의 실용적 선택성.
- 사용자 지시 원문: "그렇게 해보자 그리고 나병환자 전수조사 들어가보자"
- 승인 내용: 직전 제시한25/27/30/32/35안을 적용한다. 더 강한30/32/35/37/40안은 미승인·미적용이다.
- 변경: 독주1~5레벨 회피20/22/25/27/30 → **25/27/30/32/35**. 효과duration4, 자기표식3턴, 대단원 준비75%/8%p, 명중1레벨125·치명0, 전진3, 전투당2회, JES-005 사용1234 및 JES-001 시체 제거는 유지한다.
- 의도: 전열 자기표식으로 동료 부담을 가져오는 과정에서 광대 개인의 위험이 과도해지는 것을 완화하고 공격·노래 기술 사이에서 독주 선택 이유를 만든다. 새로운 발동 규칙 대신 기존 회피 효과의 수치를 조정한다.
- 근거:5레벨 무장신구·적명중100·설치적중가정에서 한 번 사용 후 회피65→70, 피격35→30%.4명 모두 공격가능·광대 몫25→55.6%·표식특효 없음이라는 민감도 예시에서 독주 전 대비 개인 기대피해 증가19.75→2.65%. 적별 대상열/표식특효가 다르므로 실전고정결과나생존보장이아니다.
- 원칙 대조: 고정 장신구·효과ID·치명·영웅 능력치를 보존한다. JES-005로 제자리 두 번째 사용이 열렸으므로 두 번 중첩/장신구 결합이 큰 상향이 될 수 있다. 발라드 완화와 함께 검토하되 총량 보존을 선언하지 않는다.
- 영향: 기본 회피와 두 번 사용·폭군의 손가락뼈 등 전열 조건을 따로 검토한다.5레벨 두 번 정상 중첩 가정 회피95→105이며, 대단원 직후에는 회피−25와받는스트레스+100%가 있어 한 번 독주65/70의보호량을그대로연장하지않는다.
- 참조: 이어가기 outputs/solo-dodge-options.txt/.json, solo-tanking-cap-review.txt/.json. 회피 중첩·기간·숨은 명중·대단원 강화 상한은 아직 게임 확인 항목이다.
- 검증: 광대만 대상으로 편집 효과를 적용하고35기술줄과모든편집효과에서회피5줄/참조5줄만승인대로변경됐는지대조한다.주석검사·전용효과정의·참조·모드목록과관련파일바이트보존을확인한다. 기존 사용자 한국어 주석은 원문 그대로 보존한다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### JES-004 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 이동 공격의 명중을 보완해 기술 선택지를 만들고 기존 치명/보호 무시/대단원 준비를 유지한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/dirk_stab`
  - 원본: `combat_skill: .id "dirk_stab" .level 0 .type "melee" .atk 85% .dmg 0% .crit 5% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 현재: `combat_skill: .id "dirk_stab" .level 0 .type "melee" .atk 90% .dmg 0% .crit 5% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 원본: `combat_skill: .id "dirk_stab" .level 1 .type "melee" .atk 90% .dmg 0% .crit 6% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 현재: `combat_skill: .id "dirk_stab" .level 1 .type "melee" .atk 95% .dmg 0% .crit 6% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 원본: `combat_skill: .id "dirk_stab" .level 2 .type "melee" .atk 95% .dmg 0% .crit 7% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 현재: `combat_skill: .id "dirk_stab" .level 2 .type "melee" .atk 100% .dmg 0% .crit 7% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 원본: `combat_skill: .id "dirk_stab" .level 3 .type "melee" .atk 100% .dmg 0% .crit 8% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 현재: `combat_skill: .id "dirk_stab" .level 3 .type "melee" .atk 105% .dmg 0% .crit 8% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 원본: `combat_skill: .id "dirk_stab" .level 4 .type "melee" .atk 105% .dmg 0% .crit 9% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
  - 현재: `combat_skill: .id "dirk_stab" .level 4 .type "melee" .atk 110% .dmg 0% .crit 9% .move 0 1 .launch 4321 .target 123 .is_crit_valid True .ignore_guard true  .effect "Build to Finale"`
- 출처: `heroes/jester/jester.info.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-004 Dirk Stab accuracy +5 at every level; damage, critical modifier, guard bypass, movement and Finale preparation retained.
```

### JES-001 JES-005 JES-006 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 표식/회피 운영을 실용적으로 만들어 강한 지원·출혈 기술과 슬롯 경쟁이 가능하게 한다. 전열 노출 비용을 회피+5로 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/solo`
  - 원본: `combat_skill: .id "solo" .level 0 .type "ranged" .atk 125% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 43 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "Jester Spotlight 1" "Build to Finale 2"`
  - 현재: `combat_skill: .id "solo" .level 0 .type "ranged" .atk 125% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 1234 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "clear_corpses" "RB JES Jester Spotlight 1" "Build to Finale 2"`
  - 원본: `combat_skill: .id "solo" .level 1 .type "ranged" .atk 130% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 43 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "Jester Spotlight 2" "Build to Finale 2"`
  - 현재: `combat_skill: .id "solo" .level 1 .type "ranged" .atk 130% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 1234 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "clear_corpses" "RB JES Jester Spotlight 2" "Build to Finale 2"`
  - 원본: `combat_skill: .id "solo" .level 2 .type "ranged" .atk 135% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 43 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "Jester Spotlight 3" "Build to Finale 2"`
  - 현재: `combat_skill: .id "solo" .level 2 .type "ranged" .atk 135% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 1234 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "clear_corpses" "RB JES Jester Spotlight 3" "Build to Finale 2"`
  - 원본: `combat_skill: .id "solo" .level 3 .type "ranged" .atk 140% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 43 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "Jester Spotlight 4" "Build to Finale 2"`
  - 현재: `combat_skill: .id "solo" .level 3 .type "ranged" .atk 140% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 1234 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "clear_corpses" "RB JES Jester Spotlight 4" "Build to Finale 2"`
  - 원본: `combat_skill: .id "solo" .level 4 .type "ranged" .atk 145% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 43 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "Jester Spotlight 5" "Build to Finale 2"`
  - 현재: `combat_skill: .id "solo" .level 4 .type "ranged" .atk 145% .dmg -100% .crit 0% .move 0 3 .per_battle_limit 2 .launch 1234 .target ~1234 .is_crit_valid False  .effect "Solo Mark Self" "clear_corpses" "RB JES Jester Spotlight 5" "Build to Finale 2"`
- 출처: `heroes/jester/jester.info.darkest`, 주석 추가 전 33행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 기존 주석 원문:
```text
// JES-006 Solo dodge 25/27/30/32/35 via dedicated effects; JES-005 all-rank launch and two uses retained.
```
- 기존 주석 원문:
```text
// JES-005 Solo usable from ranks 1/2/3/4; improve front-rank dodge/mark use and skill selection. Existing effects, forward 3 and two uses per battle retained.
```
- 기존 주석 원문:
```text
// JES-001 solo: 시체 제거 추가. 3열 처치 -> 독주(1열 이동 + 시체 제거)로 4열 적을 3열로 -> 대단원 연계 [제작자]. 효과 이름 Jester Spotlight(무대 조명) = 무대를 비운다(P-19). 대단원 4열 도달 여부는 V-08
```

### JES-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 중요 능력치 셋을 함께 올리는 지원기의 우위를 줄여 다른 버프/조합의 선택을 넓힌다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/battle_ballad`
  - 원본: `combat_skill: .id "battle_ballad" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "Embolden Team 1" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battle_ballad" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "RB JES Embolden Team 1" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battle_ballad" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "Embolden Team 2" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battle_ballad" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "RB JES Embolden Team 2" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battle_ballad" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "Embolden Team 3" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battle_ballad" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "RB JES Embolden Team 3" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battle_ballad" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "Embolden Team 4" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battle_ballad" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "RB JES Embolden Team 4" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battle_ballad" .level 4 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "Embolden Team 5" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battle_ballad" .level 4 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 34 .target @~1234 .is_crit_valid True  .effect "RB JES Embolden Team 5" "Build to Finale Song" .is_stall_invalidating false`
- 출처: `heroes/jester/jester.info.darkest`, 주석 추가 전 47행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Battle Ballad team speed 1/1/2/2/3 and critical bonus 1/2/3/4/5%; accuracy and Finale-specific preparation retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Embolden Team 1`
- 원본: `effect: .name "Embolden Team 1" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 2% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false    .queue false`
- 현재: `effect: .name "Embolden Team 1" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 1% .speed_rating_add 1	.on_hit true .on_miss true .apply_once false    .queue false`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 101행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Team critical bonus -1% point and speed -1; approved level 1 values, accuracy retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Embolden Team 2`
- 원본: `effect: .name "Embolden Team 2" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6% .crit_chance_add 3% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "Embolden Team 2" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6% .crit_chance_add 2% .speed_rating_add 1	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 110행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Team critical bonus -1% point and speed -1; approved level 2 values, accuracy retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Embolden Team 3`
- 원본: `effect: .name "Embolden Team 3" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7% .crit_chance_add 4% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "Embolden Team 3" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7% .crit_chance_add 3% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 113행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Team critical bonus -1% point and speed -1; approved level 3 values, accuracy retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Embolden Team 4`
- 원본: `effect: .name "Embolden Team 4" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8% .crit_chance_add 5% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "Embolden Team 4" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8% .crit_chance_add 4% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 116행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Team critical bonus -1% point and speed -1; approved level 4 values, accuracy retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Embolden Team 5`
- 원본: `effect: .name "Embolden Team 5" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 6% .speed_rating_add 4	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "Embolden Team 5" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 5% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 119행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-002 Team critical bonus -1% point and speed -1; approved level 5 values, accuracy retained.
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Embolden Team 1`
- 원본 (Embolden Team 1): `effect: .name "Embolden Team 1" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 2% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false    .queue false`
- 현재: `effect: .name "RB JES Embolden Team 1" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 1% .speed_rating_add 1	.on_hit true .on_miss true .apply_once false    .queue false`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 20행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Embolden Team 2`
- 원본 (Embolden Team 2): `effect: .name "Embolden Team 2" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6% .crit_chance_add 3% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "RB JES Embolden Team 2" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6% .crit_chance_add 2% .speed_rating_add 1	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 23행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Embolden Team 3`
- 원본 (Embolden Team 3): `effect: .name "Embolden Team 3" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7% .crit_chance_add 4% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "RB JES Embolden Team 3" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7% .crit_chance_add 3% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 26행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Embolden Team 4`
- 원본 (Embolden Team 4): `effect: .name "Embolden Team 4" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8% .crit_chance_add 5% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "RB JES Embolden Team 4" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8% .crit_chance_add 4% .speed_rating_add 2	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 29행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Embolden Team 5`
- 원본 (Embolden Team 5): `effect: .name "Embolden Team 5" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 6% .speed_rating_add 4	.on_hit true .on_miss true .apply_once false	.queue false`
- 현재: `effect: .name "RB JES Embolden Team 5" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 5% .speed_rating_add 3	.on_hit true .on_miss true .apply_once false	.queue false`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 32행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}

### JES-003 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 2열 광대가 공격 기술만 고정 채용하지 않도록 지원 선택지를 연다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/inspiring_tune`
  - 원본: `combat_skill: .id "inspiring_tune" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @1234 .is_crit_valid True  .effect "InspiringTune 1" "Jester Tune Buff 1" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "inspiring_tune" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 234 .target @1234 .is_crit_valid True  .effect "InspiringTune 1" "Jester Tune Buff 1" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "inspiring_tune" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @1234 .is_crit_valid True  .effect "InspiringTune 2" "Jester Tune Buff 2" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "inspiring_tune" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 234 .target @1234 .is_crit_valid True  .effect "InspiringTune 2" "Jester Tune Buff 2" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "inspiring_tune" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @1234 .is_crit_valid True  .effect "InspiringTune 3" "Jester Tune Buff 3" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "inspiring_tune" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 234 .target @1234 .is_crit_valid True  .effect "InspiringTune 3" "Jester Tune Buff 3" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "inspiring_tune" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @1234 .is_crit_valid True  .effect "InspiringTune 4" "Jester Tune Buff 4" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "inspiring_tune" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 234 .target @1234 .is_crit_valid True  .effect "InspiringTune 4" "Jester Tune Buff 4" "Build to Finale Song" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "inspiring_tune" .level 4 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @1234 .is_crit_valid True  .effect "InspiringTune 5" "Jester Tune Buff 5" "Build to Finale Song" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "inspiring_tune" .level 4 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 234 .target @1234 .is_crit_valid True  .effect "InspiringTune 5" "Jester Tune Buff 5" "Build to Finale Song" .is_stall_invalidating false`
- 출처: `heroes/jester/jester.info.darkest`, 주석 추가 전 53행; Git 원문 {"commit": "84a709eea8f59e18bb43c17f3bc0d9083f1269fb", "summary": "JES-002/003/004 apply approved Ballad growth, rank-2 Tune and Dirk accuracy"}
- 기존 주석 원문:
```text
// JES-003 Inspiring Tune usable from ranks 2/3/4; stress healing and stress resistance retained.
```

### JES-006 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 표식/회피 운영을 실용적으로 만들어 강한 지원·출혈 기술과 슬롯 경쟁이 가능하게 한다. 전열 노출 비용을 회피+5로 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Jester Spotlight 1`
- 원본: `effect: .name "Jester Spotlight 1" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 20% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "Jester Spotlight 1" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 25% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 58행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 기존 주석 원문:
```text
// JES-006 Solo dodge +5 at every level to offset front-rank mark exposure; duration and other effects retained.
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Jester Spotlight 2`
- 원본: `effect: .name "Jester Spotlight 2" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 22% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "Jester Spotlight 2" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 27% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 66행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Jester Spotlight 3`
- 원본: `effect: .name "Jester Spotlight 3" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 25% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "Jester Spotlight 3" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 30% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 69행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Jester Spotlight 4`
- 원본: `effect: .name "Jester Spotlight 4" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 27% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "Jester Spotlight 4" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 32% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 72행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Jester Spotlight 5`
- 원본: `effect: .name "Jester Spotlight 5" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 30% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "Jester Spotlight 5" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 35% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/jester/jester.effects_edit.txt`, 주석 추가 전 75행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Jester Spotlight 1`
- 원본 (Jester Spotlight 1): `effect: .name "Jester Spotlight 1" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 20% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB JES Jester Spotlight 1" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 25% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Jester Spotlight 2`
- 원본 (Jester Spotlight 2): `effect: .name "Jester Spotlight 2" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 22% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB JES Jester Spotlight 2" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 27% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 8행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Jester Spotlight 3`
- 원본 (Jester Spotlight 3): `effect: .name "Jester Spotlight 3" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 25% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB JES Jester Spotlight 3" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 30% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Jester Spotlight 4`
- 원본 (Jester Spotlight 4): `effect: .name "Jester Spotlight 4" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 27% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB JES Jester Spotlight 4" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 32% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 14행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB JES Jester Spotlight 5`
- 원본 (Jester Spotlight 5): `effect: .name "Jester Spotlight 5" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 30% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB JES Jester Spotlight 5" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 35% .duration 4	.on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_jester.effects.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "577aabb0717238508f421a9dd119fb5072f75ea0", "summary": "JES-006 raise Solo dodge by five at each level"}


### JES-002 발라드 하향 의도 보강: 선턴 우위·치명타 연계·스트레스 관리 중복 공급 (2026-10-06)
- 상태: 사용자가 기존 하향 이유를 명시하여 기록 보강. 이번 작업의 추가 수치 변경은 없음.
- 속도 하향의 의도: 기본 속도가 높은 광대가 초반에 파티 속도를 올리면 선턴 우위를 확보하기 쉬워지고, 적 행동 이전 처치·기절로 행동과 스트레스 공격을 억제한다. 사용자는 이를 기습에 가까운 선턴 지배로 체감했다. 속도 수치 자체뿐 아니라 원정 스트레스 수요까지 줄이는 선제 행동의 가치를 낮추려는 결정이다.
- 치명타 하향의 의도: 치명타 확률 증가는 직접 피해뿐 아니라 각 영웅의 치명타 발동 효과와 치명타에 따른 스트레스 회복을 함께 늘린다. 따라서 발라드 치명은 피해 수치만으로 평가할 수 없다.
- 선율과의 결합: 선율의 직접 스트레스 회복·받는 스트레스 감소와 발라드의 치명타 회복·선제 행동에 따른 스트레스 피해 예방이 결합한다. 광대 자신의 공격 치명타 발동 효과도 주는 스트레스 회복량 +40%를 제공한다. 사용자는 두 지원 기술만으로 관리 공급이 넘쳐 조합에서 광대 의존이 커지는 문제를 완화하려 했다.
- 유지한 정체성: 팀 명중과 명중/속도/치명 세 축, 선율, 대단원 준비를 보존한 채 발라드의 속도1/1/2/2/3 및 치명1/2/3/4/5%p로 기존 승인을 유지한다. 이번 설명 보강은 선율의 추가 하향이나 다른 회복 기술의 상향 승인이 아니다.
- 전력 재배분: 광대의 직접 회복량을 키우기보다 다른 영웅의 기존 스트레스 회복 기술을 검토하여 지원 공급을 분산한다. 광대 강화의 예방·치명 회복을 축소하는 기존 하향과 대체 회복 공급을 P-11 취지에서 함께 추적한다. 적용 빈도·대상·스트레스 손실·행동비용이 달라 단순 합으로 총량 보존을 선언하지 않는다.
- 엔진 확인 범위: 아래 “무조건 아군이 올 선턴”은 사용자 체감·의도 원문이다. 실제 선턴 확률은 상대 속도·대열 및 행동 순서 규칙에 달리며, 첫 라운드 도중 속도 증가가 남은 순서를 즉시 재정렬하는지는 설치 데이터만으로 검증하지 않았다. 광대가 항상 속도 단독1위라는 수치 판정도 아니다.
- 검증: info/편집 사본/게임용 효과의 모든 수치·참조·데이터 행이 작업 전후 동일함을 확인했다. 기존 한국어 메모는 그대로 보존하고 JES-002 설명 주석만 추가했다. 전체20영웅 주석 검사와 파일 목록 크기를 확인한다.
- 사용자 원문:

> 스트레스 회복기술 최대한 버프하고 싶은데 또 뭐가 있을까 그리고 광대 버프기술 너프한 이유가 속도 가 기존엔 그정도오르면 광대가 최고 속도에 1턴에 걸면 마치 기습효과처럼 무조건 아군이 올 선턴 잡아버리는 그런 사기성이 존재했어 그래서 너프한거고, 치명타는 치명타 버프 효과와 스트레스 회복 효과까지 있어서 생각보다 엄청 사기야 그래서 선율이랑 광대 버프 2개로 스트레스관리가 차고 넘치는 현상 발생해서 조정한거야 덧붙여줘


### JES-007 독주: 적 전체에 제압(명중·치명타 감소) 추가 (2026-10-08)
- 상태: 적용 (제작자 A안 "독주 명중 감소 좋은듯")
- 문제: 명중 125~145의 적 전체 대상 기술인데 적에게 일어나는 일이 시체 제거뿐이라 명중이 통째로 낭비됐다. 가치 −36.7%p로 광대 키트 최하위.
- 변경: 1~5레벨에 기존 효과 `Suppression 1~5`(명중 −15~−20, 치명타 −15~−19, 2턴, 확률 100~140%) 추가. 나머지(자기 표식·회피·시체 제거·대단원 준비·전진 3·전투당 2회) 유지
- 근거
  1. P-19: 무대 조명(Spotlight)에 시선을 뺏긴 관객 → 적이 제대로 노리지 못한다.
  2. **약화 총량 유지 [제작자 제안]**: `Suppression`은 바닐라 총사 연막탄에 있던 약화로, YAMR 총사 편입(MUS-001)으로 영웅 기술에서 빠졌다. 새 효과를 만들지 않고 재사용한다(R-DATA-01).
  3. 비교안 `Antiq Distract`(명중 −15, 2턴)는 −3.4%p로 여전히 쓸 이유가 약했다.
- 영향: 가치 −36.7 → **+7.7%p (+44.4)**. 키트 안(고무하는 노래 +195.5, 저며내기 +156.4, 전투 발라드 +145.8)에서 여전히 아래쪽이라 지배적이지 않다. 광대 1위(71점) 그대로.


### 작업 파일 복구 (2026-10-09)
- `heroes/jester/jester.info.darkest`가 2026-10-09 15:43에 바닐라(+JES-001)로 덮여 JES-002~007이 게임에서 빠져 있었다(원인 미상, 스팀 패치 아님). 제작자 승인으로 커밋 버전으로 복구. 덮인 파일 사본은 세션 임시 폴더에 보관.

### JES-008 독주: 회피 +5 (2026-10-09)
- 상태: 적용 (제작자 결정 "독주가 찌르기보다 구린 게 말이 안 돼")
- 변경: `RB JES Jester Spotlight 1~5` 회피 25/27/30/32/35 → **30/32/35/37/40**, 4턴 유지
- 근거: 결투가 찌르기(피해 0% 평타, 제한 없음)가 회피 +40~50으로 독주보다 높았다. 독주는 전투당 2회·1열로 3칸 전진·자기 표식이라는 대가를 치르는 회피 기술이라 회피 1위여야 한다. 찌르기는 DUE-005로 15~25로 내림.
- 영향: 강함 모델 +7.7 → +12.1%p

### JES-009 독주의 대단원 준비 보너스: 피해 +75% → +100%, 치명타 +8% → +10% (2026-10-09)
- 상태: 적용 (제작자 결정)
- 변경: `Build to Finale 2`의 강화를 리밸런스 전용 버프 `RB_JES_build_to_finale2_dmgL/dmgH/crit`(shared/buffs/rebalance_jester.buffs.json, 대단원 사용 시에만)로 교체 → `RB JES Build to Finale 2`
- 근거: 독주 → 대단원 연계(JES-001 의도)의 보상 강화. 5렙 대단원 한 방 약 26 → 30(+14%, 곱산 가정), 치명타 17% → 19%. 대단원은 전투당 1회라 총량 영향이 작다.
- 메모: 강함 모델은 대단원 연계를 평가하지 못한다(대단원 −56.6). 수치는 직접 계산.


### JES-010 전투 발라드: 치명타 바닐라 복귀 (2026-10-09)
- 상태: 적용 (제작자 결정 "발라드 롤백하고 속도 증가만 11223")
- 변경: 아군 치명타 1~5% → **바닐라 2/3/4/5/6%**. 명중(바닐라)·아군 속도 1/1/2/2/3(JES-002) 유지. JES-002 중 치명타 하향만 철회.

### JES-011 독주: 제압 → 적 속도 감소, 다른 아군 표식 해제 추가 (2026-10-09)
- 상태: 적용 (제작자 결정)
- 변경: JES-007 `Suppression 1~5` 제거 → 기존 효과 `HW Open Vein SPD Debuff 1~5`(적 속도 −1~−3, 3턴, 정맥 절개와 공용) 추가. 신규 효과 `RB JES Solo Clear Ally Mark`(자신 제외 아군 표식 해제) 추가(석궁사수 결집 신호탄에서 분산).
- 근거 [제작자]: 아군 표식은 지우고 자기만 표식 — 무대 조명이 광대 한 명에게 쏠리는 독주 연출과 맞다(P-19). 적 명중 감소는 함성(HEL-008)·제압 사격과 겹쳐 속도 감소로 바꿈.
- 속도 감소 후보 중 가장 약한 기존 효과를 택했다(마름쇠 −8, 위협 −5는 적 전체 대상에는 과함).
