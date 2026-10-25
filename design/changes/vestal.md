# 성녀 (vestal) 변경 항목

바닐라 수치: `heroes/vestal/vestal.vanilla.txt`

---

## 제작자 설계 의도 (파일 머리 메모, 원문 요약, 기록 2026-10-01)

- 성녀의 정체성은 **안정성·예측 가능성**. 단점은 열 붙박이라 대열 섞임에 약함.
- 바닐라 문제: 3·4열 안정성이 너무 좋다. 가장 큰 원인은 3열 기절과 심판의 자기 회복. **쓰는 기술 4개가 고정**(심판·눈부신 광채·회복 2개), 100이면 100 이 4개만 쓴다.
- 방향: 회복 2개는 정답 성능 유지. 심판·기절은 하향, 다른 기술은 상향해서 **상황마다 다른 기술이 정답**이 되게 한다. 1·2열 성녀(탱커 성녀)를 가능하게 한다.

아래 VES-001~007은 이 메모 아래 제작자가 이미 고친 값이다. 기록이 없어 이번에 번호를 붙였다. 가치는 자기 평타 기준 환산 %p (R-VALUE-02, 모델 R-VALUE-04/08).

| ID | 기술 | 변경 | 제작자 근거 | 가치 바닐라 → RB |
|---|---|---|---|---|
| VES-001 | 철퇴 후려치기 | 심판의 자기 회복(3/3/4/4/5) 이전, 치명타 0~4 → 5~9 | 1·2열 성녀가 때에 따라 가능하게. 이것만으로 1열 탱커 성녀가 가능 | +2 → **+79** |
| VES-002 | 심판 | 자기 회복 제거, 명중 85~105 → 90~110, 치명타 5~9 → 0~4 | 자힐을 철퇴로, 명중은 원거리 표준 90 | +72 → **+2** |
| VES-003 | 눈부신 광채 | 사용 열 432 → 43, 피해 −75 → −100 | 3·4열과 1·2열 분리. 심판보다 좋아서 피해 제거 | +24 → **−19** |
| VES-004 | 신성한 은총 | 회복 4-5 … 8-9 → 5 … 9 고정, 사용 열 43 → 4321 | 예측 가능성, 소폭 상향, 1열 성녀 | +16 → +23 |
| VES-005 | 신성한 위무 | 사용 열 432 → 43, 회복 1-3/2-3/3-3/3-4/4-5 → 2-3/3-3/3-4/4-4/4-5 | 가장 사기 기술이라 3·4열 전용. 1레벨이 은총보다 약하고 4→5 상승이 비정상이라 등차로 | +73 → +73 (5레벨 동일) |
| VES-006 | 신의 광휘 | 사용 열 321 → 4321 | 1열에서 쓸 게 없음 | +3 → +3 |
| VES-007 | 신의 손길 | 명중 85~105 → 90~110 | 1·2열 성녀 상향, 원거리 표준 90 | +64 → +68 |

표기 수정 (2026-10-01, 값 변화 없음):
- 철퇴 후려치기 `.effect "Unholy Killer N"  .effect "Vestal HealSelf N"` → 한 목록. 한 줄에 `.effect` 두 번은 바닐라·설치된 창작마당 모드 14개 어디에도 없다. 게임이 한쪽만 읽을 위험. 모델도 앞 목록만 읽어서 철퇴 회복을 0으로 셌다(이전 표 17위 → 실제 15위).
- 심판 `.atk 90 .crit 0` → `90% 0%`. % 없는 명중·치명타 역시 선례가 없다. 90을 9000%, 4를 400%(항상 치명타)로 읽을 위험.

## 분석 (2026-10-01)

**순위**: RB 15위 47점 (바닐라 18위 40점). 상승은 거의 전부 철퇴(+77%p).

**의도 대비 판정**

1. **1·2열 성녀 → 달성.** 철퇴 +79, 신의 손길 +68은 RB 성녀의 1·3위 기술이다. 개발사도 전열 성녀를 상정했다: 속죄의 목걸이(근접 공격만 피해 +15%, 치명타 +8%), 불경한 두루마리(특정 열 방어 +10, 회복 +33%), 바닐라 신의 손길 사용 열 12. P-20(장신구 제약)과 맞는다.
2. **"기술 4개 고정" 해소 → 미달.** 열별로 쓸 수 있는 기술을 보면:
   - 3·4열: 위무 +73, 은총 +23, 광휘 +3, 심판 +2, 광채 −19 → 쓸 만한 건 **회복 2개뿐**. 공격 셋이 모두 0 근처라 "상황마다 다른 정답"이 아니라 "아무거나"다.
   - 1·2열: 철퇴, 손길, 은총, 광휘 → 4개. **정정 (제작자, 2026-10-02)**: 바닐라 1열 성녀는 3개(철퇴·손길·광휘)뿐이었다. 4개는 '고정'이 아니라 **선택지를 늘린 결과**다.
   - 결과: 미달은 3·4열 쪽만이다. 후열 공격 셋이 0 근처라 바닐라보다 단조로워졌다 → VES-008·009로 보완.
3. **눈부신 광채는 이중 하향.** 사용 열(432 → 43)과 피해(−75 → −100)를 둘 다 깎아 키트 최하위(−19)다. 사용 열 분리만으로 "1·2열에서 기절" 문제는 이미 사라진다. 모델은 바닐라 광채(+24)가 심판(+72)보다 약하다고 보는데, 이는 기절 가치가 적 1행동이라는 가정 때문이다(R-STRAT-01의 행동 우위 연장 프리미엄은 민감도 기절 x1.3으로만 본다: 그때 +48). 제작자 경험("기절이 너무 좋다")과 차이가 나는 지점.

**대안 계산** (순위는 모두 15위 그대로 — 행동 가치는 상위 3기술 평균이고, 상위 3개는 철퇴·위무·손길이라 4번째 이하는 순위를 못 움직인다)

| 안 | 변경 | 결과 |
|---|---|---|
| 현재 | — | 광채 −19, 심판 +2 |
| A | 광채 피해 −100 → −75 (사용 열 43 유지) | 광채 **+24** (기절 x1.3이면 +48) |
| B | 심판 피해 −25 → 0 (회복 없음 유지) | 심판 **+33** |
| A+B | 둘 다 | 후열 선택지: 위무 +73 / 심판 +33 / 광채 +24 / 은총 +23 |

**권장: A+B.** 후열 성녀에게 "회복 / 4열까지 닿는 공격(심판) / 1~3열 기절(광채)" 세 갈래 선택지를 남긴다. 어느 것도 위무를 넘지 않아 바닐라의 "심판 자힐 정답" 구조로 돌아가지 않는다. 철퇴의 자기 회복은 그대로 두니 1·2열 성녀의 정체성도 유지된다. 이 키트에서 후열 성녀는 자기 회복이 없다. 그게 붙박이 후열에 대한 대가다.

**확인 사항**
- P-19: 자기 회복이 심판(빛)에서 철퇴로 옮겨갔다. 이름·연출이 회복을 약속하지 않는 기술이다. 바닐라 연출은 심판에 회복 이펙트가 붙어 있을 가능성이 있다(게임에서 확인). 문제가 되면 철퇴 쪽 이름은 못 바꾸니 기록만 남긴다.
- 신속의 성배(기절 확률 −25%)는 광채 가치가 낮을수록 대가가 작아진다. A안이면 바닐라와 같은 대가.

## 제작자 판단: 바닐라 기절·심판이 사기였던 이유 (2026-10-02)

> 기절은 사기가 맞다. 3열에 닿으니까. 심판도 사기다. 4열에 닿는데 회복까지 있어서 진짜 사기였다. 심판·기절·회복 2개가 무조건 고정이었다. 성녀는 이걸 흔들려고 여러 개 시도해 본 것이다. [제작자]

- 데이터 뒷받침: 바닐라 영웅의 적 기절 기술 12개 중 **4열에서 쓸 수 있으면서 3열 이상에 닿는 것은 4개**뿐이다(현상금 사냥꾼 섬광탄, 역병 의사 실명 가스·혼란의 일격, 성녀 눈부신 광채). 그중 회복 담당은 성녀 하나. 후열 우선 전략(R-STRAT-01, R-VALUE-07: 3·4열 위협도 x1.16)에서 **후열에 서서 후열을 막는 기절은 희소 자원**이다.
- 모델과의 차이: 모델은 바닐라 광채(+24)가 심판(+72)보다 약하다고 본다. 기절 가치 = 성공률 x 적 1행동 x 열 배수라서 희소성(다른 영웅이 대신 못 하는 것)은 값에 없다. 제작자 경험이 이 차이를 가리킨다. 모델 보정 후보로 남긴다(기절 x1.3 민감도에서 광채 +48).
- 심판의 바닐라 +72는 모델 안에서도 키트 1위였다(직접 +94, 회복 +68). 4열 도달 공격에 자기 회복이 붙은 구조가 문제였다는 판단과 일치한다.

## VES-008 눈부신 광채 피해 −100 → −75 롤백 (적용 2026-10-02)

- 사용 열 43(VES-003)은 유지, 피해만 바닐라로. 사용 열 분리만으로 1·2열 기절은 이미 사라진다. 피해까지 없애면 키트 최하위(−19%p)라 후열 선택지에서 빠졌다.
- 가치 −19 → **+24%p** (바닐라와 같은 수치, 사용 열만 좁음).

## VES-009 심판 피해 −25 → 0 (적용 2026-10-02)

- 자기 회복이 철퇴로 옮겨간(VES-001) 뒤 심판은 +2%p로 사실상 죽은 기술이었다. **회복 없는 4열 도달 공격**으로 남긴다.
- 가치 +2 → **+33%p**. 바닐라 +72(회복 포함)의 절반 아래라 '심판 자힐 정답' 구조로 돌아가지 않는다.

## 적용 후 성녀 키트 (RB 15위 47점)

| 열 | 기술 (자기 평타 기준 %p) |
|---|---|
| 3·4열 | 위무 +73 / **심판 +33** / **광채 +24** / 은총 +23 / 광휘 +3 |
| 1·2열 | 철퇴 +79 / 손길 +68 / 은총 +23 / 광휘 +3 |

후열에서 회복·4열 공격·1~3열 기절 중 상황에 따라 고르는 구조. 어느 것도 위무를 넘지 않는다. 순위는 상위 3기술 평균이라 그대로다(4번째 이하 개선은 순위가 아닌 선택지 다양성에 기여).

## 재판정 (2026-10-02, VES-008·009 + R-VALUE-09 은신 해제 반영)

| 열 | 기술 | 자기 평타 기준 | 언제 정답인가 |
|---|---|---|---|
| 3·4열 | 신성한 위무 | +73%p | 파티 체력이 고루 깎였을 때 |
| | 심판 | +33%p | 4열을 쳐야 할 때 (광채가 못 닿음) |
| | 눈부신 광채 | +24%p (기절 x1.3이면 +48) | 1~3열 위협을 한 턴 막을 때 |
| | 신성한 은총 | +23%p | 한 명만 급할 때 |
| | 신의 광휘 | +16%p, **은신 적이 있으면 약 +55** | 전투 36.9%에 나오는 챔피언 은신 적을 풀 때 |
| 1·2열 | 철퇴 후려치기 | +79%p | 전열 성녀의 주력, 자기 회복 |
| | 신의 손길 | +68%p | 자기 강화 후 연타 |
| | 신성한 은총 / 신의 광휘 | +23 / +16%p | 위와 같음 |

**판정: 의도 달성.**
1. **기술 4개 고정이 깨졌다.** 후열 5개가 각각 다른 상황의 정답이다. 바닐라의 심판(+72, 4열 + 자힐)처럼 모든 상황을 이기는 기술이 없다. 최고인 위무도 회복이 필요할 때만 쓴다.
2. **기절은 여전히 강하지만 독점은 아니다.** 제작자 판단(3열 도달 기절은 희소 자원 → 사기)을 반영해 기절 x1.3으로 보면 광채 +48 > 심판 +33. 그래도 4열을 못 치니 심판의 자리가 남는다.
3. **은신 해제가 광휘의 자리를 만든다.** 전투 셋 중 하나꼴로 챔피언 은신 적이 나오고, 그중 58%가 3·4열이다. 광휘는 4321 어디서나 쓸 수 있어(VES-006) 전열·후열 성녀 모두의 상황기가 된다.
4. **철퇴는 과하지 않다.** 표준 평타 기준 +71%p로, 1·2열 공격 기술 중 17위권이다. 전열 전문 영웅의 주력기(방패 파괴자 +192, 고행자 +176, 야만인 +130, 현상금 사냥꾼 +126, 중보병 +120)보다 낮다. 성녀는 탱커가 아니라 "전열에서도 버티는 회복 담당"이다.
5. **순위 15위 47점**(바닐라 18위 40). 같은 회복 담당인 신비학자(14위 47점)와 같은 수준이다. 추가 상향은 필요 없다.

**남은 확인 (게임)**
- 1열 성녀 생존: 체력 44, 회피 20, 방어 0. 철퇴 자기 회복 5/회로 버티는지.
- P-19: 바닐라 심판 연출에 회복 이펙트가 붙어 있는지.
- 표기 수정 2건이 게임에서 의도대로 읽히는지(철퇴 회복이 뜨는지, 심판 치명타가 0~4%인지).


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### VES-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 심판의 자기 회복과 치명을 철퇴로 옮겨 전열 성녀의 운용 가능성을 만든다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/mace_bash`
  - 원본: `combat_skill: .id "mace_bash" .level 0 .type "melee" .atk 85% .dmg 0% .crit 0% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 1"`
  - 현재: `combat_skill: .id "mace_bash" .level 0 .type "melee" .atk 85% .dmg 0% .crit 5% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 1" "Vestal HealSelf 1"`
  - 원본: `combat_skill: .id "mace_bash" .level 1 .type "melee" .atk 90% .dmg 0% .crit 1% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 2"`
  - 현재: `combat_skill: .id "mace_bash" .level 1 .type "melee" .atk 90% .dmg 0% .crit 6% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 2" "Vestal HealSelf 1"`
  - 원본: `combat_skill: .id "mace_bash" .level 2 .type "melee" .atk 95% .dmg 0% .crit 2% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 3"`
  - 현재: `combat_skill: .id "mace_bash" .level 2 .type "melee" .atk 95% .dmg 0% .crit 7% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 3" "Vestal HealSelf 2"`
  - 원본: `combat_skill: .id "mace_bash" .level 3 .type "melee" .atk 100% .dmg 0% .crit 3% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 4"`
  - 현재: `combat_skill: .id "mace_bash" .level 3 .type "melee" .atk 100% .dmg 0% .crit 8% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 4" "Vestal HealSelf 2"`
  - 원본: `combat_skill: .id "mace_bash" .level 4 .type "melee" .atk 105% .dmg 0% .crit 4% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 5"`
  - 현재: `combat_skill: .id "mace_bash" .level 4 .type "melee" .atk 105% .dmg 0% .crit 9% .launch 21 .target 12 .is_crit_valid True  .effect "Unholy Killer 5" "Vestal HealSelf 3"`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 30행; Git 원문 {"commit": "8149600a5b1ae1e4e2b97dd25aa84ac4fb4dcab6", "summary": "VES-001~007 성녀 제작자 변경 기록 + 표기 수정 2건, 분석"}
- 기존 주석 원문:
```text
// 1,2열 성녀가 때에 따라 가능하도록, 3,4열 붙박이 스킬인 심판의 자힐을 메이스로 가져옴
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"// 이 변화만으로 1열의 탱커 성녀가 진짜 가능할거라 생각함. "
```
- 기존 주석 원문:
```text
// 치명타 확률 심판이랑 바꿈
```
- 기존 주석 원문:
```text
// 표기: .effect 를 한 줄에 두 번 쓰던 것을 한 목록으로 합침(바닐라·창작마당 모드 어디에도 없는 형식, 한쪽이 무시될 수 있음). 효과 변화 없음
```

### VES-002 VES-009 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 자기 회복을 철퇴로 옮긴 뒤에도 후열 도달 공격으로 선택할 수 있게 명중과 직접 피해를 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/judgement`
  - 원본: `combat_skill: .id "judgement" .level 0 .type "ranged" .atk 85% .dmg -25% .crit 5% .launch 43 .target 1234 .is_crit_valid True  .effect "Vestal HealSelf 1"`
  - 현재: `combat_skill: .id "judgement" .level 0 .type "ranged" .atk 90% .dmg 0% .crit 0% .launch 43 .target 1234 .is_crit_valid True `
  - 원본: `combat_skill: .id "judgement" .level 1 .type "ranged" .atk 90% .dmg -25% .crit 6% .launch 43 .target 1234 .is_crit_valid True  .effect "Vestal HealSelf 1"`
  - 현재: `combat_skill: .id "judgement" .level 1 .type "ranged" .atk 95% .dmg 0% .crit 1% .launch 43 .target 1234 .is_crit_valid True`
  - 원본: `combat_skill: .id "judgement" .level 2 .type "ranged" .atk 95% .dmg -25% .crit 7% .launch 43 .target 1234 .is_crit_valid True  .effect "Vestal HealSelf 2"`
  - 현재: `combat_skill: .id "judgement" .level 2 .type "ranged" .atk 100% .dmg 0% .crit 2% .launch 43 .target 1234 .is_crit_valid True`
  - 원본: `combat_skill: .id "judgement" .level 3 .type "ranged" .atk 100% .dmg -25% .crit 8% .launch 43 .target 1234 .is_crit_valid True  .effect "Vestal HealSelf 2"`
  - 현재: `combat_skill: .id "judgement" .level 3 .type "ranged" .atk 105% .dmg 0% .crit 3% .launch 43 .target 1234 .is_crit_valid True`
  - 원본: `combat_skill: .id "judgement" .level 4 .type "ranged" .atk 105% .dmg -25% .crit 9% .launch 43 .target 1234 .is_crit_valid True  .effect "Vestal HealSelf 3"`
  - 현재: `combat_skill: .id "judgement" .level 4 .type "ranged" .atk 110% .dmg 0% .crit 4% .launch 43 .target 1234 .is_crit_valid True`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 40행; Git 원문 {"commit": "d15763d3d66b968e0a11270f80e21b3658a36fad", "summary": "VES-008 눈부신 광채 피해 -75 롤백, VES-009 심판 피해 0"}
- 기존 주석 원문:
```text
// 자힐을 메이스로 넘김
```
- 기존 주석 원문:
```text
// 명중을 RANGE 표준인 90으로 바꾸고 대신에 치명타 확율을 메이스랑 바꿈
```
- 기존 주석 원문:
```text
// 표기: .atk 90 -> 90%, .crit 0 -> 0%. % 없는 명중·치명타는 바닐라에 없다. 90을 9000%, 4를 400%로 읽을 위험. 값 변화 없음
```
- 기존 주석 원문:
```text
// VES-009 피해 -25 -> 0. 자기 회복이 철퇴로 갔으니(VES-001) 회복 없는 4열 도달 공격으로 남긴다. 가치 +2 -> +33%p, 위무(+73)는 못 넘음
```

### VES-003 VES-008 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 후열 기절과 전열 운용을 나누되 직접 피해까지 없애 과도하게 약해지지 않도록 바닐라 피해를 복귀시킨다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/dazzling_light`
  - 원본: `combat_skill: .id "dazzling_light" .level 0 .type "ranged" .atk 90% .dmg -75% .crit 5% .launch 432 .target 123 .is_crit_valid True  .effect "Vestal Stun 1" "Dazzling Light 1"`
  - 현재: `combat_skill: .id "dazzling_light" .level 0 .type "ranged" .atk 90% .dmg -75% .crit 5% .launch 43 .target 123 .is_crit_valid True  .effect "Vestal Stun 1" "Dazzling Light 1"`
  - 원본: `combat_skill: .id "dazzling_light" .level 1 .type "ranged" .atk 95% .dmg -75% .crit 6% .launch 432 .target 123 .is_crit_valid True  .effect "Vestal Stun 2" "Dazzling Light 1"`
  - 현재: `combat_skill: .id "dazzling_light" .level 1 .type "ranged" .atk 95% .dmg -75% .crit 6% .launch 43 .target 123 .is_crit_valid True  .effect "Vestal Stun 2" "Dazzling Light 1"`
  - 원본: `combat_skill: .id "dazzling_light" .level 2 .type "ranged" .atk 100% .dmg -75% .crit 7% .launch 432 .target 123 .is_crit_valid True  .effect "Vestal Stun 3" "Dazzling Light 1"`
  - 현재: `combat_skill: .id "dazzling_light" .level 2 .type "ranged" .atk 100% .dmg -75% .crit 7% .launch 43 .target 123 .is_crit_valid True  .effect "Vestal Stun 3" "Dazzling Light 1"`
  - 원본: `combat_skill: .id "dazzling_light" .level 3 .type "ranged" .atk 105% .dmg -75% .crit 8% .launch 432 .target 123 .is_crit_valid True  .effect "Vestal Stun 4" "Dazzling Light 1"`
  - 현재: `combat_skill: .id "dazzling_light" .level 3 .type "ranged" .atk 105% .dmg -75% .crit 8% .launch 43 .target 123 .is_crit_valid True  .effect "Vestal Stun 4" "Dazzling Light 1"`
  - 원본: `combat_skill: .id "dazzling_light" .level 4 .type "ranged" .atk 110% .dmg -75% .crit 9% .launch 432 .target 123 .is_crit_valid True  .effect "Vestal Stun 5" "Dazzling Light 1"`
  - 현재: `combat_skill: .id "dazzling_light" .level 4 .type "ranged" .atk 110% .dmg -75% .crit 9% .launch 43 .target 123 .is_crit_valid True  .effect "Vestal Stun 5" "Dazzling Light 1"`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 51행; Git 원문 {"commit": "d15763d3d66b968e0a11270f80e21b3658a36fad", "summary": "VES-008 눈부신 광채 피해 -75 롤백, VES-009 심판 피해 0"}
- 기존 주석 원문:
```text
//3,4열과 1,2열 분리 위해 432 -> 43으로 변경
```
- 기존 주석 원문:
```text
// VES-008 피해 -100 -> -75 롤백(바닐라). 사용 열 43 분리(VES-003)만으로 하향은 충분, 피해까지 없애면 키트 최하위(-19%p)라 후열 선택지에서 빠짐. 가치 -19 -> +24%p
```

### VES-004 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 회복의 예측 가능성을 성녀 정체성으로 두고 전열에서도 단일 회복을 쓰게 한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/divine_grace`
  - 원본: `combat_skill: .id "divine_grace" .level 0 .heal 4 5 .launch 43 .target @4321  .generation_guaranteed true .is_stall_invalidating false`
  - 현재: `combat_skill: .id "divine_grace" .level 0 .heal 5 5 .launch 4321 .target @4321  .generation_guaranteed true .is_stall_invalidating false`
  - 원본: `combat_skill: .id "divine_grace" .level 1 .heal 5 6 .launch 43 .target @4321  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "divine_grace" .level 1 .heal 6 6 .launch 4321 .target @4321  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "divine_grace" .level 2 .heal 6 7 .launch 43 .target @4321  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "divine_grace" .level 2 .heal 7 7 .launch 4321 .target @4321  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "divine_grace" .level 3 .heal 7 8 .launch 43 .target @4321  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "divine_grace" .level 3 .heal 8 8 .launch 4321 .target @4321  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "divine_grace" .level 4 .heal 8 9 .launch 43 .target @4321  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "divine_grace" .level 4 .heal 9 9 .launch 4321 .target @4321  .is_stall_invalidating false`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 62행; Git 원문 {"commit": "8f52fcfe821547d58c60e6547066b8d66da8553d", "summary": "총사 모드 제외(MUS-000) + 회복 표기 정정(ARB-002: 석궁사수 붕대질, 성녀 신성한 은총)"}
- 기존 주석 원문:
```text
// 표기: .heal N -> .heal N N. 바닐라 기술 줄 회복 45개는 전부 "최소 최대" 두 숫자다. 한 숫자는 게임 해석이 보장되지 않아 같은 값을 두 번 쓴다(회복량 변화 없음)
```
- 기존 주석 원문:
```text
//성녀의 정체성을 안정성 즉 예측 가능성에 둠.
```
- 기존 주석 원문:
```text
//그렇기에 힐의 랜덤성을 없애고 소폭 상향함
```
- 기존 주석 원문:
```text
//1열 성녀의 가능성 때문에 사용열을 전라인으로 변경 43 -> 4321
```

### VES-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 강한 광역 회복을 후열에 제한하고 초반 회복 성장의 불균형을 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/gods_comfort`
  - 원본: `combat_skill: .id "gods_comfort" .level 0 .heal 1 3 .launch 432 .target @~1234  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "gods_comfort" .level 0 .heal 2 3 .launch 43 .target @~1234  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "gods_comfort" .level 1 .heal 2 3 .launch 432 .target @~1234  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "gods_comfort" .level 1 .heal 3 3 .launch 43 .target @~1234  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "gods_comfort" .level 2 .heal 3 3 .launch 432 .target @~1234  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "gods_comfort" .level 2 .heal 3 4 .launch 43 .target @~1234  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "gods_comfort" .level 3 .heal 3 4 .launch 432 .target @~1234  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "gods_comfort" .level 3 .heal 4 4 .launch 43 .target @~1234  .is_stall_invalidating false`
  - 원본: `combat_skill: .id "gods_comfort" .level 4 .heal 4 5 .launch 432 .target @~1234  .is_stall_invalidating false`
  - 현재: `combat_skill: .id "gods_comfort" .level 4 .heal 4 5 .launch 43 .target @~1234  .is_stall_invalidating false`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 74행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//가장 사기기술인 이 기술은 대신에 3,4열에서만 사용하게 변경 432 -> 43
```
- 기존 주석 원문:
```text
//힐량 소폭 상승 이유는 1렙에 1힐이 떠버리면 디바인 그레이스보다 힐량이 구림. 근데 마지막 4->5렙 갈 때 비정상으로 높은 수치로 레벨 상승
```
- 기존 주석 원문:
```text
//그래서 1렙에 몰아줌 힐성능을 대신에 등차적으로 성장하게 바꿈
```

### VES-006 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 성녀에게도 은신 대응/견제 선택지를 제공한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/gods_illumination`
  - 원본: `combat_skill: .id "gods_illumination" .level 0 .type "ranged" .atk 90% .dmg -75% .crit 0% .launch 321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 1" "Vestal Light 1" "Destealth"`
  - 현재: `combat_skill: .id "gods_illumination" .level 0 .type "ranged" .atk 90% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 1" "Vestal Light 1" "Destealth"`
  - 원본: `combat_skill: .id "gods_illumination" .level 1 .type "ranged" .atk 95% .dmg -75% .crit 0% .launch 321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 2" "Vestal Light 2" "Destealth"`
  - 현재: `combat_skill: .id "gods_illumination" .level 1 .type "ranged" .atk 95% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 2" "Vestal Light 2" "Destealth"`
  - 원본: `combat_skill: .id "gods_illumination" .level 2 .type "ranged" .atk 100% .dmg -75% .crit 0% .launch 321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 3" "Vestal Light 3" "Destealth"`
  - 현재: `combat_skill: .id "gods_illumination" .level 2 .type "ranged" .atk 100% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 3" "Vestal Light 3" "Destealth"`
  - 원본: `combat_skill: .id "gods_illumination" .level 3 .type "ranged" .atk 105% .dmg -75% .crit 0% .launch 321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 4" "Vestal Light 4" "Destealth"`
  - 현재: `combat_skill: .id "gods_illumination" .level 3 .type "ranged" .atk 105% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 4" "Vestal Light 4" "Destealth"`
  - 원본: `combat_skill: .id "gods_illumination" .level 4 .type "ranged" .atk 110% .dmg -75% .crit 0% .launch 321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 5" "Vestal Light 5" "Destealth"`
  - 현재: `combat_skill: .id "gods_illumination" .level 4 .type "ranged" .atk 110% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid False .ignore_stealth true  .effect "Dodge Curse 5" "Vestal Light 5" "Destealth"`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 84행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//1열에 쓸게 없어서 이거 넣어야함
```
- 기존 주석 원문:
```text
//사용열 321 -> 4321
```

### VES-007 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 성녀 공격/지원 선택을 보완하려는 명중90 결정을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/gods_hand`
  - 원본: `combat_skill: .id "gods_hand" .level 0 .type "ranged" .atk 85% .dmg -50% .crit 1% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 1" "Unholy Killer 1"`
  - 현재: `combat_skill: .id "gods_hand" .level 0 .type "ranged" .atk 90% .dmg -50% .crit 1% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 1" "Unholy Killer 1"`
  - 원본: `combat_skill: .id "gods_hand" .level 1 .type "ranged" .atk 90% .dmg -50% .crit 2% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 2" "Unholy Killer 2"`
  - 현재: `combat_skill: .id "gods_hand" .level 1 .type "ranged" .atk 95% .dmg -50% .crit 2% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 2" "Unholy Killer 2"`
  - 원본: `combat_skill: .id "gods_hand" .level 2 .type "ranged" .atk 95% .dmg -50% .crit 3% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 3" "Unholy Killer 3"`
  - 현재: `combat_skill: .id "gods_hand" .level 2 .type "ranged" .atk 100% .dmg -50% .crit 3% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 3" "Unholy Killer 3"`
  - 원본: `combat_skill: .id "gods_hand" .level 3 .type "ranged" .atk 100% .dmg -50% .crit 4% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 4" "Unholy Killer 4"`
  - 현재: `combat_skill: .id "gods_hand" .level 3 .type "ranged" .atk 105% .dmg -50% .crit 4% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 4" "Unholy Killer 4"`
  - 원본: `combat_skill: .id "gods_hand" .level 4 .type "ranged" .atk 105% .dmg -50% .crit 5% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 5" "Unholy Killer 5"`
  - 현재: `combat_skill: .id "gods_hand" .level 4 .type "ranged" .atk 110% .dmg -50% .crit 5% .launch 12 .target 123 .is_crit_valid True  .effect "Vestal Inspiration 5" "Unholy Killer 5"`
- 출처: `heroes/vestal/vestal.info.darkest`, 주석 추가 전 94행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//1,2열 성녀 버프 위해 명중 레인지 표준 90으로 조정 85 -> 90
```


### VES-010 신의 광휘: 1렙 명중 90 → 95 (2026-10-08)
- 상태: 적용 (제작자 결정)
- 제작자 근거 (요지): 선택지 다양성. 성녀의 다른 공격 기술이 모두 명중 90이라, 확실히 맞히는 기술 하나를 두어 마무리(딸피 처리)에도 쓰게 한다.
- 보강 근거: 피해 −75%이고 본업이 회피 감소(−20~−30)·은신 해제인 효과 기술이다. 효과 본업 기술은 명중 우선(R-SKILL-09: 피해 없는 약화 95).
- 영향: 강함 모델 5렙 가치 +13.2 → **+20.1%p (+6.9)**. 여전히 성녀 기술 중 최하위라 과하지 않다. 성녀 16위(46점) 그대로.

### VES-011 광휘: 회피 −20~−30 → 받는 피해 +10/11/12/13/15% (2026-10-11)
- 상태: 적용 (제작자 동의)
- 문제: 회피 −30이 석궁사수 저격수의 표식과 같았다. 성녀에게 약화 관련 장신구가 없어 고정 제약(P-20)도 없다.
- 변경: 신규 효과 `RB VES Illumination Exposed 1~5`(받는 피해 +10/11/12/13/15%, 3턴, 확률 100~140% 그대로). +10·+12·+15는 마름쇠 강화(caltrops_dmg_received_1~3) 재사용, +11·+13은 `shared/buffs/rebalance_vestal.buffs.json` 신규. 횃불·은신 해제 유지.
- 근거: "성스러운 빛이 악을 드러낸다"(P-19). 받는 피해 증가는 마름쇠(3·4열 대상)뿐이었고, 광휘는 4321열에서 1234열을 노려 역할이 다르다. 은신 해제는 빛 기술인 광휘가 가장 어울리는 주인.

### VES-012 광휘: 받는 피해 +10~15% → +20/21/22/23/25% (2026-10-11)
- 상태: 적용 (제작자 "광휘 버프, 너무 약한 듯")
- 근거(R-VALUE-19 기준, 라운드당 HP): 예전 회피 −30 = 2.9(적 회피 분포 + 95% 자동 명중 상한: 적중률 77% → 98%). 받는 피해 +15% = 1.6, +25% = 2.7(93%). 5렙 −22%p → **+1%p**(같은 눈금에서 예전 회피 −30판은 약 +5%p).
- 변경: +20은 마름쇠 강화(caltrops_dmg_received_5) 재사용, +21/22/23/25는 `rebalance_vestal.buffs.json` 신규(VES-011의 +11·+13은 삭제). 3턴·확률 그대로.
- 참고: 마름쇠(3·4열 대상, 출혈·속도 감소 포함)는 +10~20%. 광휘가 수치는 더 높지만 피해·출혈이 거의 없는 순수 약화 기술.

### VES-013 광휘: 화상 1/1/2/2/3 추가 (2026-10-17)
- 상태: 적용 (제작자 결정)
- 변경: 화상 1/1/2/2/3(저항 무시, 확률 100~140%) 추가 — 같은 수치인 `RB ANT Flash Burn 1~5`(ANT-001) 재사용(R-DATA-01). 받는 피해 +20~25%·횃불·은신 해제 그대로.
- 근거: "성스러운 빛이 악을 태운다" — 받는 피해 증가(드러난 악이 더 아프다)와 이어진다. 도망자 화톳불(화상 대상 치명 +10~14%)·불길 역류 연계를 연다. 아트는 빛이라 섬광 가루만큼 직접적이지는 않다.
- 영향(모델(5렙)): −4 → 약 +44(burn_synergy.md 계산). 성녀 41점 그대로(광휘는 주력 행동 밖).

### VES-007 보충 근거: 신의 손길 명중 85 → 90 (2026-10-17)
- [제작자] 원거리 강화 기술인데 명중 85는 원칙에 맞지 않는다 — 맞혀야 아군 강화가 걸리는 효과 위주 기술은 명중을 우선한다(R-TRADE-02 메모 "효과 본업 기술은 명중 우선").

### VES-014 광휘: 창작마당판(VES-W01)으로 통합 (2026-10-21)
- 명중 바닐라 90~110, 받는 피해 증가(VES-011·012) 대신 회피 감소 복귀 −15/−18/−20/−22/−25%(바닐라 −20~−30보다 5 낮춤: 석궁 저격수의 표식과 구분, 추가한 화상의 대가). 4321열 사용(VES-006)·화상 1/1/2/2/3(VES-013) 유지.
- 효과: 바닐라 Dodge Curse 편집 → RB VES Dodge Curse 1~5 (도구 생성). 받는 피해 효과(RB VES Illumination Exposed) 삭제.

### VES-015 눈부신 광채: 2열 사용 복귀, 대상 1·2열 (2026-10-23, test)
- 사용 3·4 → 2·3·4열(바닐라 복귀, VES-003 되돌림), 대상 1·2·3 → 1·2열.
- 제작자: "성녀는 2열 스턴 가능해야 한다. 3열까지 닿는 게 사기 — 3열 닿는 순간 심판·스턴·힐 2개 4개 스킬이 정답이 되어 다른 스킬 안 쓴다. 상황에 맞춰 다양하게 쓰게."
- 근거: 장신구 가치 감사(trinket_viability_C.md) — 핏빛 궁정 세트(기절 +35%p)를 끼는 1·2열 성녀에게 기절 기술이 없어 세트가 약해졌다(VES-003 원인).


### VES-016 광휘: 명중 95로 지원 공격 안정성 확보 (2026-10-25)
- 상태: 적용. 기술 1~5 명중 90/95/100/105/110 → 95/100/105/110/115.
- 의도: 심판(명중 90, 피해 0%)과 달리 정확한 빈사 적 마무리 및 회피 감소·화상·은신 해제 전달을 선택 이유로 삼는다.
- 유지: 피해 -75%, 치명 불가, 전열 사용/대상, 회피 감소 -15~-25, 화상 1/1/2/2/3, 효과 적용 확률. 횃불은 가치 계산에서 제외.
- 이력: VES-014의 명중만 대체. 이전 피해 -60% 후보는 미채택. 효과 위주 기술의 명중 95는 비교 사례이지 모든 원거리 기술의 보편 규칙은 아니다.

### VES-017 신의 손길: 명중 95로 마무리와 후속 철퇴 연계 (2026-10-25)
- 상태: 적용. 기술 1~5 명중 90/95/100/105/110 → 95/100/105/110/115.
- 의도: 적을 마무리하면서 자기 명중/피해를 준비하는 전열 성녀 선택지. 철퇴의 즉시 피해·자가 회복 역할은 유지한다. 반드시 손길 선행이 정답이라고 단정하지 않는다.
- 유지: 피해 -50%, 치명 보정, 사용 1·2열/대상 1·2·3열, 명중 +6~10/피해 +25~35%, 불경 특효.
- 사실 정정: Vestal Inspiration은 on_hit true/on_miss true이므로 빗나가도 강화가 발동하도록 설정돼 있다. 기존 why.json의 적중해야 강화 발동이라는 설명은 수정한다.
- 이력: VES-007의 명중을 대체. 피해 -35% 후보는 미채택.
- 사용자 원문 (두 항목 공통): 신의손길과 광휘 둘 다 명중을 95로 맞추면 활용성이 있지 않을까? 예를 들어 딸피 처리 같은데는 버프를 사용하는거지 그리고 철퇴는 명중이 낮으니 무조건 빛의 손길 이후에 쓰고 이런식으로 둘다 버프나 너프 효과가 있는 원거리 기술이란 점에서 명중 95가 일반 원칙에 어긋나지도 않고 너 생각은 어때?
- 배포 승인 원문: 그리고 선택형 패키지 창작마당에 쓸데 없는거 전부 없애주고 이거는 내꺼 창작모드 메인인건데 들어가보니 이거 왜 이미지가 없니 5개밖에 없어 지금 우리가 하는 성녀 작업까지 마무리 하고 푸쉬한 다음에 다 올리자
- 검증: 정적 수치/주석/배포 입력 확인. 게임 내 실제 순서·체감은 미검증.


### VES-018 신의 손길 명중90, 광휘95 유지 (2026-10-25)

- 사용자 원문: "그럼 광휘 95 유지하고 손길만 90으로 바꾸자 그거에 맞춰서 전부 성능 조절해봐"
- 승인 맥락: 직전 제안은 손길90/95/100/105/110, 광휘95 유지, 피해·자기 강화·열 등 나머지 수치 유지였다. 다른 성녀 기술 전반의 추가 재설계로 확장하지 않는다.
- 변경: 손길 전 레벨 명중만95/100/105/110/115→90/95/100/105/110. VES-017의 손길 명중만 대체한다. VES-016 광휘95/100/105/110/115는 유지한다.
- 의도: 광휘는 적중 기반 회피 약화·화상 지원의 신뢰도, 손길은 빗나가도 설정상 발동하는 자기 강화로 다음 공격을 준비하는 특징을 구분한다.
- 보존: 손길 피해-50%, 기술1레벨 치명+1%, 사용1·2열/대상1·2·3열, 자기 명중+6/7/8/9/10 및 피해+25/27/30/33/35%. 철퇴85/피해0%와 다른 기술도 변경 없음.
- 주의: 손길 선행이 항상 최선이라는 의미는 아니다. 즉시 처치·회복 기회비용을 고려한다. 실전 균형 및 총량 보존을 수학적으로 증명한 변경은 아니다.
- 기록: 카드 원본과 why를 동기화했다. 기존 VES-017 원문·기록은 역사로 보존한다. 게임 실행 시험/창작마당 배포는 이번 작업에 포함하지 않는다.


### VES-019 신의 손길 피해 −40%: 준비 공격의 첫 타격 보완 (2026-10-25)

- 사용자 원문: "그럼 손길 피해 -40으로 가자 광휘는 그대로 두고 의도 주석 남겨서 커밋까지 해 푸시는 아직 하지 말고"
- 변경: 기술1~5레벨 피해 보정 −50%→−40%. 실제 게임 수치는 손길의 피해5개 행만 변경한다.
- 의도: 손길의 준비 행동 비용과 첫 타격 손해를 줄여 빈사 적 마무리 후 강화된 후속 공격으로 이어지는 선택을 지원한다. 명중95→90은 유지하면서 첫 피해를 보충하는 조정이다.
- 강화 자체를 더 높이지 않으므로 자기 강화 중첩을 추가로 강화하는 안과 구분된다. 철퇴의 즉시 피해·자가 회복 역할은 유지한다.
- 유지: 명중90/95/100/105/110, 치명1/2/3/4/5%, 사용1·2열/대상1·2·3열, 기존 자기 강화와 불경 추가 피해. 광휘 전 항목 및 다른 성녀 기술 유지.
- 이력: VES-018의 명중90은 유지하며, 그때의 피해−50% 유지 결정만 이번 승인으로 대체한다. 이전 한국어 주석·원문은 보존한다.
- 단순 피해 합산 예시는 명중·치명·방어·정수화·자가 회복·행동 비용을 포함한 전체 잔차가 아니다. 이번 조정의 실전 균형이나 총량 보존을 증명한 계산으로 취급하지 않는다.
- 범위: 의도·카드 원본 동기화 및 커밋. 사용자 지시로 푸시·창작마당 게시 보류, 게임 실행 시험 미실시.

### VES-020 광휘: 물리 파티를 위한 방어도 감소 (2026-10-25, test)
- 상태: 사용자 승인, test 적용. main/push/공개 배포는 이번 범위가 아니다.
- 변경: 방어도 감소 15/17/20/22/25%p, 3턴, 약화 기본 확률 100/110/120/130/140%.
- 의도: 화상 1/1/2/2/3을 제거하고 방어도 감소로 교체한다. 직접 화상 피해 대신 아군 물리 공격을 지원하며 회피 감소·은신 해제·횃불을 유지한다.
- 교환: 화상 1/1/2/2/3 제거. 방어도는 0 아래로 낮추는 효과로 설계하지 않는다. 숫자·지속·범위에 따른 실전 총량 보존은 플레이 검증 대상.
- 유지: 기존 test의 명중·피해·치명·사용열·대상열과 나머지 효과. 성녀 main의 최신 명중95/손길-40을 test에 가져오는 변경은 포함하지 않는다.
- 중간 레벨: 1·5레벨 및 지속은 직전 제안에 대한 승인; 중간 수열은 구현상 완만한 정수 성장으로 정했다.
- 사용자 원문: 방어도 감소는 넣어야 해 너 말처럼 광휘와 섬광가루에 방어도 감소 넣는 거 추천해 화상 없애고 그리고 포효에 회피 감소 없애고 방어 감소 넣자 근거는 이미 지휘에 명중 증가가 있어
- 직전 제안 연결: 광휘 15→25%p, 3턴. 화상을 방어도 감소로 교체.
- 이력: VES-013의 화상 추가을 이번 범위에서 대체. 원문 주석·과거 기록·공유 원본 효과는 보존.
- 검증: 기술 5행과 효과/편집 사본 참조 일치, 다른 수치 보존, 주석·배포 목록 검사. 게임 내 시험은 미실시.


### VES-021 main 통합: 광휘 이중 약화와 명중 유지 (2026-10-25)
- 사용자 원문: "화상 없애고 광휘 명중 95 손길 명중 90으로 올려", "광휘 회피 감소랑 방어감소 둘다"
- 광휘: 기술1레벨 명중95, 피해-75%, 회피 감소15~25 및 방어도 감소15~25%p(3턴)를 함께 유지하고 화상을 제거한다. 명중은 main VES-016을 보존하며 test의 오래된90으로 되돌리지 않는다.
- 손길: 기술1레벨 명중90, 피해-40%, 기존 자기 강화를 유지한다. 성전사 CRU-010과 main 배포 안전장치도 보존한다.
- VES-020의 test 한정 상태는 이번 전체 main 승격 승인으로 대체한다. 수치 모델의 기존 test 명중90 결과는 당시 분석이며 새95의 결과로 둔갑시키지 않는다.
