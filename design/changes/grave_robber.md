# 도굴꾼 (grave_robber) 변경 항목

바닐라 수치: `heroes/grave_robber/grave_robber.vanilla.txt`

---

### GR-001 맹독 다트: 중독 지속 4턴 → 3턴
- 상태: 적용 (게임 테스트 전)
- 분류: 원칙복원 (R-EFF-02 예외 해소)
- 목표: G-02
- 수정 주체: 제작자
- 제작자 메모 (원문)
  > 대신에 유일한 4턴 중독을 3턴으로 정상화
- 근거
  - 영웅 지속 피해는 전부 3턴이고, 4턴은 맹독 다트 하나뿐이었다(`analysis/hero_power.md`, 2026-09-15 조사).
  - 몬스터까지 봐도 4턴 이상은 백작부인·거대 뱀·광기의 색채 보스 정도다.
- 변경: `GR Blight 1~5`의 `.duration 4` → `3` → 적용 시 `RB GR Blight 1~5`로 분리. 바닐라 효과 파일은 건드리지 않았다.
- 영향 (5레벨)
  - 중독 총량 16 → 12, 기대 피해 12.8 → 10.6
  - 중독 상태 유지가 4턴 → 3턴이라, 돌진·단검 투척의 중독 대상 +33% 연계가 3회 → **2회**
  - 가격표: −4.9 → 약 −12.5 (지속 피해가 줄어 예측이 올라감). GR-002와 합치면 아래 참고
- 검증: (플레이 후 기록)

### GR-002 명중 버프를 단검 투척에서 맹독 다트로 이동
- 상태: 적용 (게임 테스트 전)
- 분류: 의도적 조정
- 목표: G-02 (정답 스킬 조합 해체)
- 수정 주체: 제작자
- 제작자 메모 (원문)
  > 명중 버프를 맹독다트로 옮김. 그래도 괜찮은게 피해 보정이 적고(쉴브 휘감기 -25) 크리률이 높아서 괜찮. 거기에 포이즌 킬러까지 있어서 충분히 상쇄. 이 자체로 충분히 좋은 기술임 명중버프까지 있던 게 op였음. 다양성 높이려는 스킬셋 방향성에 맞음

  > 노상 정맥절개와 대칭 정맥절개가 약화 2개 있음, 맹독다트는 약화 1개랑 자버프 1개

  > 노상 정맥절개처럼 고유모션이라 활용성이 높으면 좋음
- 변경: `GR Acc Buff 1~5`(자기 명중 +5→+10) 참조를 단검 투척에서 빼고 맹독 다트에 붙였다. 효과 자체는 수정하지 않았다.
- 가격표 변화 (자기 강화 1개 = 피해 −19%p)

  | 기술 | 변경 전 | 변경 후 |
  |---|---|---|
  | 단검 투척 | **+27.3** (원거리 단일 중 최상위 과대) | 약 **+8.3** |
  | 맹독 다트 | −4.9 | 자기 강화 +19 → +14.1, GR-001의 중독 감소 −7.6 → 약 **+6.5** |

- 판정: 두 기술이 +8 전후로 모이고, 도굴꾼 전체 과대 합은 거의 그대로다(P-11 충족). 과대 1위였던 단검 투척이 정리되고, 준비기였던 맹독 다트가 쓸 이유를 얻는다(G-02).
- 남은 관찰 포인트: 맹독 다트가 "중독 + 약화 + 자기 명중"을 한 번에 가지므로, 실전에서 단검 투척을 완전히 대체하는지 확인이 필요하다.

### GR-003 극약처방: 전투당 1회 제한 삭제, 자기 회복 추가, 자기 버프 축소 (적용)

- 현재 데이터 정정 (2026-10-17): 자기 회복은 GR-006에서 1/2/3/4/5로 바뀌었다. 아래 3/3/4/4/5와 그 이유는 GR-003 당시 기록.

- 목표: G-05(모든 영웅 자기 회복), G-02 [제작자 지시 2026-09-28]
- 근거
  - 바닐라 극약처방은 v2 모델 **0.1 HP**(평타 2%)다. 전투당 1회에 버프만 있어 사실상 고르지 않는 기술이었다.
  - **P-19**: 이름이 "극약**처방**"이다. 처방은 치료를 약속한다. 치료(`.cure`)는 원래 있었고, 회복이 빠져 있었다.
- 변경 (5레벨 기준, 괄호는 1→5레벨)

| 항목 | 바닐라 | 변경 후 |
|---|---|---|
| 사용 제한 | 전투당 1회 | **없음** |
| 자기 회복 | 없음 | **3/3/4/4/5** (신규 `RB GR Toxin Heal`) → GR-006에서 **1/2/3/4/5** (현재 데이터) |
| 치료 (출혈·중독) | 있음 | 그대로 |
| 회피 | +9~+13, **전투 끝까지** | **+5/5/6/6/7, 3턴** |
| 속도 | +2~+4, **전투 끝까지** | **+1/1/2/2/2, 3턴** |

- **회복량을 1/2/3/4/5가 아니라 3/3/4/4/5로 넣은 이유**: FLA-005와 같은 기준(회복은 영웅 체력과 같은 속도로 성장, `heal.md`). 도굴꾼 체력 20/24/28/32/36 대비 1/2/3/4/5는 **5% → 14%**로 1레벨이 무의미하고, 3/3/4/4/5는 **15/13/14/13/14%로 일정**하다. 다른 반복 자기 회복과 비교하면 괴인 사면(3→5)과 같은 대역이고, 야만인 아드레날린(3→7, 치료 포함)·조련사 상처 핥기(4→8, 회복만)보다 낮다. 치료와 버프가 같이 붙어 있어서다.
- **버프를 3턴으로 바꾼 이유**: 제한을 없애면 전투 끝까지 가는 버프를 매 턴 다시 걸 수 있다. 같은 효과가 재사용 시 중첩되는지는 미검증(V-07)이라, 중첩돼도 겹치는 수가 3턴 안으로 묶이게 했다.
- 결과: v2 모델 0.1 → **5.4 HP(평타 70%)**. 공격기(12.6~15.9)를 밀어내지 않는 상황기다. 속도 강화는 모델이 계산하지 않는다.
- 참고: `RB GR Toxin Heal 1`은 `HealSelf 1`(성녀 등)과 수치가 같다. R-DATA-01은 다른 영웅 효과로 갈아타기를 금지하므로 사본을 유지한다.

### GR-004 그림자 은신: 뒤로 2칸 → 3칸 (철회, 바닐라 2칸 유지)

- 제작자 메모: "3열 빠지는 거로 바꿈. 2열이 아니라 이유는 런지 사용성 늘리려고"
- **검토 결과: 돌진 사용성은 바뀌지 않는다.** 그림자 은신은 1·2열에서만 쓰고, 뒤로 2칸이면 1열 → 3열, 2열 → 4열이다. 돌진(사용 3·4열)은 **2칸일 때도 은신 직후 항상 쓸 수 있다.**
- **실제로 바뀌는 것: 루프가 둘에서 하나로 줄어든다.** 은신 → 돌진(앞으로 2칸)을 반복하면:

| | 1열에서 시작 | 2열에서 시작 |
|---|---|---|
| **2칸 (바닐라)** | 1 ↔ 3 루프, 대열 완전 복원 | 2 ↔ 4 루프, 대열 완전 복원 |
| **3칸 (변경)** | 첫 회에 **1열 아군과 자리가 영구히 바뀌고** 2 ↔ 4 루프로 합류 | 2 ↔ 4 루프 (변화 없음) |

  - 바닐라의 "뒤로 2 + 앞으로 2 = 0"은 **대열을 망가뜨리지 않는 설계된 닫힌 루프**다.
  - 3칸은 **1 ↔ 3 루프를 없앤다.** 도굴꾼을 1열 돌격수로 쓰는 조합이 사라지고, 모든 도굴꾼이 2 ↔ 4로 수렴한다.
- 장점: 체력 36·방어도 0인 도굴꾼이 가장 많이 맞는 1열을 비운다.
- 단점: 선택지가 줄어든다(G-00·G-03 역행). 1열에서 쓰면 첫 회에 대열이 한 칸씩 밀린다.
- 판단: 목적이 "돌진 사용성"이면 **2칸으로 되돌리는 것을 권한다.** 목적이 "도굴꾼을 1열에서 빼기"라면 의도된 선택이고, 위 단점을 감수하는 것이다. 결정은 제작자(P-18).
- **결정 (2026-09-28, 제작자)**: 철회. 2칸으로 원복했다. 바닐라의 닫힌 루프 두 개(1↔3, 2↔4)를 유지한다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### GR-002 GR-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 명중 준비를 맹독 다트로 옮기고 MARK-01의 서브 표식 딜러 재배분을 단검에 반영한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/thrown_dagger`
  - 원본: `combat_skill: .id "thrown_dagger" .level 0 .type "ranged" .atk 90% .dmg -10% .crit 8% .launch 432 .target 234 .is_crit_valid True  .effect "GR Acc Buff 1" "GR Dagger Dmg Marked 1" "Poison Killer 1"`
  - 현재: `combat_skill: .id "thrown_dagger" .level 0 .type "ranged" .atk 90% .dmg -10% .crit 8% .launch 432 .target 234 .is_crit_valid True  .effect "RB GR Dagger Dmg Marked 1" "Poison Killer 1"`
  - 원본: `combat_skill: .id "thrown_dagger" .level 1 .type "ranged" .atk 95% .dmg -10% .crit 9% .launch 432 .target 234 .is_crit_valid True  .effect "GR Acc Buff 2" "GR Dagger Dmg Marked 2" "Poison Killer 2"`
  - 현재: `combat_skill: .id "thrown_dagger" .level 1 .type "ranged" .atk 95% .dmg -10% .crit 9% .launch 432 .target 234 .is_crit_valid True  .effect "RB GR Dagger Dmg Marked 2" "Poison Killer 2"`
  - 원본: `combat_skill: .id "thrown_dagger" .level 2 .type "ranged" .atk 100% .dmg -10% .crit 10% .launch 432 .target 234 .is_crit_valid True  .effect "GR Acc Buff 3" "GR Dagger Dmg Marked 3" "Poison Killer 3"`
  - 현재: `combat_skill: .id "thrown_dagger" .level 2 .type "ranged" .atk 100% .dmg -10% .crit 10% .launch 432 .target 234 .is_crit_valid True  .effect "RB GR Dagger Dmg Marked 3" "Poison Killer 3"`
  - 원본: `combat_skill: .id "thrown_dagger" .level 3 .type "ranged" .atk 105% .dmg -10% .crit 11% .launch 432 .target 234 .is_crit_valid True  .effect "GR Acc Buff 4" "GR Dagger Dmg Marked 4" "Poison Killer 4"`
  - 현재: `combat_skill: .id "thrown_dagger" .level 3 .type "ranged" .atk 105% .dmg -10% .crit 11% .launch 432 .target 234 .is_crit_valid True  .effect  "RB GR Dagger Dmg Marked 4" "Poison Killer 4"`
  - 원본: `combat_skill: .id "thrown_dagger" .level 4 .type "ranged" .atk 110% .dmg -10% .crit 12% .launch 432 .target 234 .is_crit_valid True  .effect "GR Acc Buff 5" "GR Dagger Dmg Marked 5" "Poison Killer 5"`
  - 현재: `combat_skill: .id "thrown_dagger" .level 4 .type "ranged" .atk 110% .dmg -10% .crit 12% .launch 432 .target 234 .is_crit_valid True  .effect  "RB GR Dagger Dmg Marked 5" "Poison Killer 5"`
- 출처: `heroes/grave_robber/grave_robber.info.darkest`, 주석 추가 전 52행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// GR-002 thrown_dagger: GR Acc Buff moved to poison_dart
```

### GR-001 GR-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 지속 피해 총량을 줄이고 명중 준비 효과를 이전해 기술별 역할을 나눈다. 동일 바닐라 중독 효과 재사용을 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/poison_dart`
  - 원본: `combat_skill: .id "poison_dart" .level 0 .type "ranged" .atk 95% .dmg -60% .crit 7.5% .launch 432 .target 1234 .is_crit_valid True  .effect "GR Blight 1" "GR Blight Debuff 1"`
  - 현재: `combat_skill: .id "poison_dart" .level 0 .type "ranged" .atk 95% .dmg -60% .crit 7.5% .launch 432 .target 1234 .is_crit_valid True  .effect "Blight 1" "GR Blight Debuff 1" "GR Acc Buff 1" `
  - 원본: `combat_skill: .id "poison_dart" .level 1 .type "ranged" .atk 100% .dmg -60% .crit 8.5% .launch 432 .target 1234 .is_crit_valid True  .effect "GR Blight 2" "GR Blight Debuff 2"`
  - 현재: `combat_skill: .id "poison_dart" .level 1 .type "ranged" .atk 100% .dmg -60% .crit 8.5% .launch 432 .target 1234 .is_crit_valid True  .effect "RB GR Blight 2" "GR Blight Debuff 2" "GR Acc Buff 2" `
  - 원본: `combat_skill: .id "poison_dart" .level 2 .type "ranged" .atk 105% .dmg -60% .crit 9.5% .launch 432 .target 1234 .is_crit_valid True  .effect "GR Blight 3" "GR Blight Debuff 3"`
  - 현재: `combat_skill: .id "poison_dart" .level 2 .type "ranged" .atk 105% .dmg -60% .crit 9.5% .launch 432 .target 1234 .is_crit_valid True  .effect "Blight 3" "GR Blight Debuff 3" "GR Acc Buff 3" `
  - 원본: `combat_skill: .id "poison_dart" .level 3 .type "ranged" .atk 110% .dmg -60% .crit 10.5% .launch 432 .target 1234 .is_crit_valid True  .effect "GR Blight 4" "GR Blight Debuff 4"`
  - 현재: `combat_skill: .id "poison_dart" .level 3 .type "ranged" .atk 110% .dmg -60% .crit 10.5% .launch 432 .target 1234 .is_crit_valid True  .effect "Blight 4" "GR Blight Debuff 4" "GR Acc Buff 4"`
  - 원본: `combat_skill: .id "poison_dart" .level 4 .type "ranged" .atk 115% .dmg -60% .crit 11.5% .launch 432 .target 1234 .is_crit_valid True  .effect "GR Blight 5" "GR Blight Debuff 5"`
  - 현재: `combat_skill: .id "poison_dart" .level 4 .type "ranged" .atk 115% .dmg -60% .crit 11.5% .launch 432 .target 1234 .is_crit_valid True  .effect "Blight 5" "GR Blight Debuff 5" "GR Acc Buff 5"`
- 출처: `heroes/grave_robber/grave_robber.info.darkest`, 주석 추가 전 59행; Git 원문 {"commit": "6381c531a2e253486cc7222d22bd079047d3f198", "summary": "R-DATA-01 중복 효과 금지 + 도구가 기존 효과를 자동 재사용"}
- 기존 주석 원문:
```text
// GR-001 poison_dart: blight 4 -> 3 turns (RB GR Blight 1-5), + GR Acc Buff moved here (GR-002)
```

### GR-003 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 반복 자기 유지기를 만들되 회피/속도 버프 크기와 지속을 낮춰 대가를 낸다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/toxin_trickery`
  - 원본: `combat_skill: .id "toxin_trickery" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .per_battle_limit 1 .launch 4321 .target  .is_crit_valid True  .effect "Shadow Blood 1" "GR Self Speed 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "toxin_trickery" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "RB GR Shadow Blood 1" "RB GR Self Speed 1" "RB GR Toxin Heal 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "toxin_trickery" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .per_battle_limit 1 .launch 4321 .target  .is_crit_valid True  .effect "Shadow Blood 2" "GR Self Speed 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "toxin_trickery" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "RB GR Shadow Blood 2" "RB GR Self Speed 2" "RB GR Toxin Heal 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "toxin_trickery" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .per_battle_limit 1 .launch 4321 .target  .is_crit_valid True  .effect "Shadow Blood 3" "GR Self Speed 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "toxin_trickery" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "RB GR Shadow Blood 3" "RB GR Self Speed 3" "RB GR Toxin Heal 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "toxin_trickery" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .per_battle_limit 1 .launch 4321 .target  .is_crit_valid True  .effect "Shadow Blood 4" "GR Self Speed 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "toxin_trickery" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "RB GR Shadow Blood 4" "RB GR Self Speed 4" "RB GR Toxin Heal 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "toxin_trickery" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .per_battle_limit 1 .launch 4321 .target  .is_crit_valid True  .effect "Shadow Blood 5" "GR Self Speed 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "toxin_trickery" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "RB GR Shadow Blood 5" "RB GR Self Speed 5" "RB GR Toxin Heal 5" .is_stall_invalidating false`
- 출처: `heroes/grave_robber/grave_robber.info.darkest`, 주석 추가 전 66행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 toxin_trickery: 전투당 1회 제한 삭제, 자기 회복 3/3/4/4/5 추가, 회피·속도 버프 절반 + 전투 끝까지 -> 3턴. G-05(모든 영웅 자기 회복), P-19(이름 "극약처방" = 처방·치료)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Shadow Blood 1`
- 원본: `effect: .name "Shadow Blood 1" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 9%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "Shadow Blood 1" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 5%	.on_hit true .on_miss true .queue true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 147행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 1레벨 회피: +9%(전투 끝까지) -> +5%(3턴). 전투당 1회 제한 해제로 재사용 시 중첩 가능성(V-07) -> 지속을 턴 단위로 묶고 절반으로. 치료(.cure)는 원래 있음
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Self Speed 1`
- 원본: `effect: .name "GR Self Speed 1" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "GR Self Speed 1" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 1  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 150행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 1레벨 속도: +2(전투 끝까지) -> +1(3턴). 같은 이유
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Shadow Blood 2`
- 원본: `effect: .name "Shadow Blood 2" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 10%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "Shadow Blood 2" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 5%	.on_hit true .on_miss true .queue true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 153행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 2레벨 회피: +10%(전투 끝까지) -> +5%(3턴). 전투당 1회 제한 해제로 재사용 시 중첩 가능성(V-07) -> 지속을 턴 단위로 묶고 절반으로. 치료(.cure)는 원래 있음
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Self Speed 2`
- 원본: `effect: .name "GR Self Speed 2" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "GR Self Speed 2" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 1  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 156행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 2레벨 속도: +2(전투 끝까지) -> +1(3턴). 같은 이유
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Shadow Blood 3`
- 원본: `effect: .name "Shadow Blood 3" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 11%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "Shadow Blood 3" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 6%	.on_hit true .on_miss true .queue true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 159행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 3레벨 회피: +11%(전투 끝까지) -> +6%(3턴). 전투당 1회 제한 해제로 재사용 시 중첩 가능성(V-07) -> 지속을 턴 단위로 묶고 절반으로. 치료(.cure)는 원래 있음
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Self Speed 3`
- 원본: `effect: .name "GR Self Speed 3" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 3  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "GR Self Speed 3" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 162행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 3레벨 속도: +3(전투 끝까지) -> +2(3턴). 같은 이유
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Shadow Blood 4`
- 원본: `effect: .name "Shadow Blood 4" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 12%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "Shadow Blood 4" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 6%	.on_hit true .on_miss true .queue true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 165행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 4레벨 회피: +12%(전투 끝까지) -> +6%(3턴). 전투당 1회 제한 해제로 재사용 시 중첩 가능성(V-07) -> 지속을 턴 단위로 묶고 절반으로. 치료(.cure)는 원래 있음
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Self Speed 4`
- 원본: `effect: .name "GR Self Speed 4" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 3  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "GR Self Speed 4" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 168행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 4레벨 속도: +3(전투 끝까지) -> +2(3턴). 같은 이유
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Shadow Blood 5`
- 원본: `effect: .name "Shadow Blood 5" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 13%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "Shadow Blood 5" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 7%	.on_hit true .on_miss true .queue true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 171행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 5레벨 회피: +13%(전투 끝까지) -> +7%(3턴). 전투당 1회 제한 해제로 재사용 시 중첩 가능성(V-07) -> 지속을 턴 단위로 묶고 절반으로. 치료(.cure)는 원래 있음
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Self Speed 5`
- 원본: `effect: .name "GR Self Speed 5" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 4  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "GR Self Speed 5" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 174행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 5레벨 속도: +4(전투 끝까지) -> +2(3턴). 같은 이유
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB GR Toxin Heal 1`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 3 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 188행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 1레벨 자기 회복 3 (신규). 도굴꾼 체력 20/24/28/32/36 대비 13~15%로 레벨마다 일정. 괴인 사면(3->5)과 같은 대역, 야만인 아드레날린(3->7)·조련사 상처 핥기(4->8)보다 낮음(치료·버프가 같이 있으므로)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB GR Toxin Heal 2`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 3 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 190행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 2레벨 자기 회복 3 (신규). 도굴꾼 체력 20/24/28/32/36 대비 13~15%로 레벨마다 일정. 괴인 사면(3->5)과 같은 대역, 야만인 아드레날린(3->7)·조련사 상처 핥기(4->8)보다 낮음(치료·버프가 같이 있으므로)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB GR Toxin Heal 3`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 4 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 192행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 3레벨 자기 회복 4 (신규). 도굴꾼 체력 20/24/28/32/36 대비 13~15%로 레벨마다 일정. 괴인 사면(3->5)과 같은 대역, 야만인 아드레날린(3->7)·조련사 상처 핥기(4->8)보다 낮음(치료·버프가 같이 있으므로)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB GR Toxin Heal 4`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 4 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 194행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 4레벨 자기 회복 4 (신규). 도굴꾼 체력 20/24/28/32/36 대비 13~15%로 레벨마다 일정. 괴인 사면(3->5)과 같은 대역, 야만인 아드레날린(3->7)·조련사 상처 핥기(4->8)보다 낮음(치료·버프가 같이 있으므로)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB GR Toxin Heal 5`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 5 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 196행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// GR-003 극약처방 5레벨 자기 회복 5 (신규). 도굴꾼 체력 20/24/28/32/36 대비 13~15%로 레벨마다 일정. 괴인 사면(3->5)과 같은 대역, 야만인 아드레날린(3->7)·조련사 상처 핥기(4->8)보다 낮음(치료·버프가 같이 있으므로)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Shadow Blood 1`
- 원본 (Shadow Blood 1): `effect: .name "Shadow Blood 1" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 9%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "RB GR Shadow Blood 1" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 5%	.on_hit true .on_miss true .queue true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 22행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Self Speed 1`
- 원본 (GR Self Speed 1): `effect: .name "GR Self Speed 1" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "RB GR Self Speed 1" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 1  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 24행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Shadow Blood 2`
- 원본 (Shadow Blood 2): `effect: .name "Shadow Blood 2" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 10%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "RB GR Shadow Blood 2" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 5%	.on_hit true .on_miss true .queue true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 26행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Self Speed 2`
- 원본 (GR Self Speed 2): `effect: .name "GR Self Speed 2" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "RB GR Self Speed 2" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 1  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 28행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Shadow Blood 3`
- 원본 (Shadow Blood 3): `effect: .name "Shadow Blood 3" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 11%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "RB GR Shadow Blood 3" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 6%	.on_hit true .on_miss true .queue true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 30행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Self Speed 3`
- 원본 (GR Self Speed 3): `effect: .name "GR Self Speed 3" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 3  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "RB GR Self Speed 3" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 32행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Shadow Blood 4`
- 원본 (Shadow Blood 4): `effect: .name "Shadow Blood 4" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 12%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "RB GR Shadow Blood 4" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 6%	.on_hit true .on_miss true .queue true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 34행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Self Speed 4`
- 원본 (GR Self Speed 4): `effect: .name "GR Self Speed 4" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 3  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "RB GR Self Speed 4" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 36행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Shadow Blood 5`
- 원본 (Shadow Blood 5): `effect: .name "Shadow Blood 5" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .defense_rating_add 13%	.on_hit true .on_miss true .queue true`
- 현재: `effect: .name "RB GR Shadow Blood 5" .target "performer" .curio_result_type "positive" .cure 1 .chance 100% .duration 3 .combat_stat_buff 1 .defense_rating_add 7%	.on_hit true .on_miss true .queue true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 38행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Self Speed 5`
- 원본 (GR Self Speed 5): `effect: .name "GR Self Speed 5" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .speed_rating_add 4  .on_hit true .on_miss false .queue true .apply_once true`
- 현재: `effect: .name "RB GR Self Speed 5" .target "performer" .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_buff 1 .speed_rating_add 2  .on_hit true .on_miss false .queue true .apply_once true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 40행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 기존 주석 원문:
```text
// mod-only new effects
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Toxin Heal 1`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 3 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 43행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Toxin Heal 2`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 3 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 44행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Toxin Heal 3`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 4 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 45행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Toxin Heal 4`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 4 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 46행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Toxin Heal 5`
- 원본: `None`
- 현재: `effect: .name "RB GR Toxin Heal 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 5 .on_hit true .on_miss false .queue true .source_heal_type hero_skill`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 47행; Git 원문 {"commit": "7e3bd8107a6d3446af60b507c8be15972696b6bf", "summary": "GR-003 극약처방 반복 자기 유지기화 + GR-004 그림자 은신 3칸 검토 기록"}

### GR-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 명중 준비를 맹독 다트로 옮기고 MARK-01의 서브 표식 딜러 재배분을 단검에 반영한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Dagger Dmg Marked 1`
- 원본: `effect: .name "GR Dagger Dmg Marked 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 25%	.damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "GR Dagger Dmg Marked 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 90행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Dagger Dmg Marked 2`
- 원본: `effect: .name "GR Dagger Dmg Marked 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 28%	.damage_high_multiply 28%	.on_hit true .on_miss false`
- 현재: `effect: .name "GR Dagger Dmg Marked 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 94행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Dagger Dmg Marked 3`
- 원본: `effect: .name "GR Dagger Dmg Marked 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 32%	.damage_high_multiply 32%	.on_hit true .on_miss false`
- 현재: `effect: .name "GR Dagger Dmg Marked 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 98행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Dagger Dmg Marked 4`
- 원본: `effect: .name "GR Dagger Dmg Marked 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 36%	.damage_high_multiply 36%	.on_hit true .on_miss false`
- 현재: `effect: .name "GR Dagger Dmg Marked 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 70%	.damage_high_multiply 70%	.on_hit true .on_miss false`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 102행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Dagger Dmg Marked 5`
- 원본: `effect: .name "GR Dagger Dmg Marked 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "GR Dagger Dmg Marked 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 80%	.damage_high_multiply 80%	.on_hit true .on_miss false`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 106행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// MARK-01 GR Dagger Dmg Marked: 표식 피해 25~40 -> 40~80 (서브 표식 딜러)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Dagger Dmg Marked 1`
- 원본 (GR Dagger Dmg Marked 1): `effect: .name "GR Dagger Dmg Marked 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 25%	.damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB GR Dagger Dmg Marked 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 10행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Dagger Dmg Marked 2`
- 원본 (GR Dagger Dmg Marked 2): `effect: .name "GR Dagger Dmg Marked 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 28%	.damage_high_multiply 28%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB GR Dagger Dmg Marked 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 12행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Dagger Dmg Marked 3`
- 원본 (GR Dagger Dmg Marked 3): `effect: .name "GR Dagger Dmg Marked 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 32%	.damage_high_multiply 32%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB GR Dagger Dmg Marked 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 14행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Dagger Dmg Marked 4`
- 원본 (GR Dagger Dmg Marked 4): `effect: .name "GR Dagger Dmg Marked 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 36%	.damage_high_multiply 36%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB GR Dagger Dmg Marked 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 70%	.damage_high_multiply 70%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 16행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Dagger Dmg Marked 5`
- 원본 (GR Dagger Dmg Marked 5): `effect: .name "GR Dagger Dmg Marked 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB GR Dagger Dmg Marked 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 80%	.damage_high_multiply 80%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 18행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}

### GR-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 지속 피해 총량을 줄이고 명중 준비 효과를 이전해 기술별 역할을 나눈다. 동일 바닐라 중독 효과 재사용을 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Blight 1`
- 원본: `effect: .name "GR Blight 1" .target "target" .curio_result_type "negative" .chance 100%  .dotPoison 2 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "GR Blight 1" .target "target" .curio_result_type "negative" .chance 100%  .dotPoison 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 113행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Blight 2`
- 원본: `effect: .name "GR Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 3 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "GR Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 118행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Blight 3`
- 원본: `effect: .name "GR Blight 3" .target "target" .curio_result_type "negative" .chance 120%  .dotPoison 3 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "GR Blight 3" .target "target" .curio_result_type "negative" .chance 120%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 123행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Blight 4`
- 원본: `effect: .name "GR Blight 4" .target "target" .curio_result_type "negative" .chance 130%  .dotPoison 3 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "GR Blight 4" .target "target" .curio_result_type "negative" .chance 130%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 128행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `GR Blight 5`
- 원본: `effect: .name "GR Blight 5" .target "target" .curio_result_type "negative" .chance 140%  .dotPoison 4 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "GR Blight 5" .target "target" .curio_result_type "negative" .chance 140%  .dotPoison 4 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/grave_robber/grave_robber.effects_edit.txt`, 주석 추가 전 133행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB GR Blight 2`
- 원본 (GR Blight 2): `effect: .name "GR Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 3 .duration 4	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB GR Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_grave_robber.effects.darkest`, 주석 추가 전 20행; Git 원문 {"commit": "a75753c5ad39f95d0e0d13f12147a4eb0cd079fc", "summary": "GR-001·GR-002 도굴꾼 적용, CRU-001 성전사 전투 치유, RB 접두어 중복 제거"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```


### GR-006 극약 처방: 자기 회복 3/3/4/4/5 → 1/2/3/4/5 (2026-10-09)
- 상태: 적용 (제작자 결정 "극약처방이 아드레날린 분출 상위호환")
- 비교: 극약 처방 = 출혈·중독 치료 + 회피 +5~7·속도 +1~2(3턴) + 회복 3~5. 야만인 아드레날린 분출 = 치료 + 회복 3~7(HEL-004). 저레벨에서 회복이 같고 회피·속도가 덤으로 붙어 상위 호환이었다.
- 변경: `RB GR Toxin Heal 1~5` 회복 → **1/2/3/4/5**. 치료·회피·속도 그대로
- 영향: 5렙은 5로 같아 강함 모델 −0.8%p 그대로(아드레날린 분출 +12.7). 1~4렙에서 회복이 1~2 낮아진다.
- 메모: 3~5렙 사본이 기존 `HealSelf 1~3`과 수치가 같다는 도구 경고가 있으나, 레벨 사본 체계를 유지한다(MAA-007과 같은 판단).

### GR-005 보충 근거: 단검 투척 표식 대상 피해 상향 (2026-10-17, 창작마당 감사 답변)
- [제작자] 표식 파티를 다양하게 하기 위한 상향(intent.md P-26): 여러 영웅의 표식 특효 기술을 올려 표식 조합이 한두 영웅에 묶이지 않게 한다.
