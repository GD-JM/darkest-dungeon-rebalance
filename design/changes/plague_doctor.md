# 역병 의사 (plague_doctor) 변경 항목

바닐라 수치: `heroes/plague_doctor/plague_doctor.vanilla.txt`

---

### PD-001 야전 의술: 중독 치료 전용으로 변경, 자기 치료 제거, 회복량 상향
- 상태: 적용 (게임 테스트 전)
- 분류: 신규규칙
- 목표: G-05(회복 편중 해소), G-00(조합 다양성)
- 사용자 요청 (원문, 2026-09-26):
  > 석궁 붕대에 출혈 치료 역병 힐에 중독 치료 넣어줘
- 적용 주체: Claude (제작자가 명시적으로 요청 → P-18 예외)
- 회복 교환 시세 (`analysis/heal_skills.md` + 2026-09-16 재산정)
  - 아군 회복 표준 8.5 (성녀 신성한 은총, 유지 결정)
  - 한 종류만 치료 −1, 출혈·중독 동시 치료 −2
  - 받는 회복 +38%(스택 힐) −4
  - 겸업 회복 상한 = 성녀 −1.5 = **7.0**
- 변경
  - 회복 1~5레벨: 1-1 / 1-2 / 2-2 / 2-3 / 3-3 → **3-3 / 4-4 / 5-5 / 6-6 / 6-7** (5레벨 평균 3.0 → 6.5)
  - 효과: `Cure`(대상 출혈·중독) + `Cureself`(자기 출혈·중독) 제거 → 신규 `RB PD Cure Poison`(대상 중독만 치료)
  - 계산: 8.5 − 1(중독만 치료) = 7.5 → 상한 7.0 아래로 6.5
- 의도: 역병 의사를 "중독 던전 전용 회복 담당"으로 만든다. 석궁사수(출혈)와 역할을 나눈다.
- 영향
  - 자기 치료가 사라져 역병 의사 단독 자가 해제는 불가능해진다. 아이템(해독제·붕대)으로 대체된다.
  - 회복량이 3.0 → 6.5로 두 배가 되어 성녀·신비학자 외 선택지가 된다.
- 검증 (P-15)
  1. `.cure_poison 1`이 전투 기술 효과에서 동작하는지. **실패 시 `Cure`로 되돌리고 회복 6-7 → 6-6으로 내린다.**
  2. 자기 치료 제거가 실제 플레이에서 체감상 과한 손실인지.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### PD-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 석궁사수 출혈 치료와 달리 동료 중독 치료를 맡기고 자기 치료를 제거해 회복 담당 선택을 나눈다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/battlefield_medicine`
  - 원본: `combat_skill: .id "battlefield_medicine" .level 0 .heal 1 1 .launch 43 .target @1234  .effect "Cure" "Cureself" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_medicine" .level 0 .heal 3 3 .launch 43 .target @1234  .effect "RB PD Cure Poison" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_medicine" .level 1 .heal 1 2 .launch 43 .target @1234  .effect "Cure" "Cureself" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_medicine" .level 1 .heal 4 4 .launch 43 .target @1234  .effect "RB PD Cure Poison" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_medicine" .level 2 .heal 2 2 .launch 43 .target @1234  .effect "Cure" "Cureself" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_medicine" .level 2 .heal 5 5 .launch 43 .target @1234  .effect "RB PD Cure Poison" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_medicine" .level 3 .heal 2 3 .launch 43 .target @1234  .effect "Cure" "Cureself" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_medicine" .level 3 .heal 6 6 .launch 43 .target @1234  .effect "RB PD Cure Poison" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_medicine" .level 4 .heal 3 3 .launch 43 .target @1234  .effect "Cure" "Cureself" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_medicine" .level 4 .heal 7 7 .launch 43 .target @1234  .effect "RB PD Cure Poison" .is_stall_invalidating false`
- 출처: `heroes/plague_doctor/plague_doctor.info.darkest`, 주석 추가 전 56행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// PD-001 battlefield_medicine: heal 1-1/3-3 -> 3-3/7-7, Cure+Cureself -> RB PD Cure Poison (blight only, ally target)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB PD Cure Poison`
- 원본: `None`
- 현재: `effect: .name "RB PD Cure Poison" .target "target" .curio_result_type "positive" .chance 100% .cure_poison 1 .on_hit true .on_miss false`
- 출처: `heroes/plague_doctor/plague_doctor.effects_edit.txt`, 주석 추가 전 159행; Git 원문 {"commit": "0e828416b7347a0972bd347c000141963cc8b189", "summary": "ARB-001 야전 붕대질 출혈 치료, PD-001 야전 의술 중독 치료 (회복량 상향)"}
- 기존 주석 원문:
```text
// PD-001 battlefield_medicine: cure blight only, on the target ally (replaces Cure + Cureself)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB PD Cure Poison`
- 원본: `None`
- 현재: `effect: .name "RB PD Cure Poison" .target "target" .curio_result_type "positive" .chance 100% .cure_poison 1 .on_hit true .on_miss false`
- 출처: `effects/rebalance_plague_doctor.effects.darkest`, 주석 추가 전 6행; Git 원문 {"commit": "0e828416b7347a0972bd347c000141963cc8b189", "summary": "ARB-001 야전 붕대질 출혈 치료, PD-001 야전 의술 중독 치료 (회복량 상향)"}


### PD-002 절개: 1렙 명중 85 → 90 (2026-10-08)
- 상태: 적용 (제작자 결정)
- 제작자 근거 (요지): 역병 의사의 다른 기술이 좋아 절개를 고를 이유가 약하다. 명중으로 선택지를 보강한다.
- 참고 (같은 날 질문 "출혈 기술인데 왜 피해 감소가 없나"): 피해 보정은 무기 피해에 곱한다. 5렙 무기 평균 역병 의사 10.0 / 야만인 14.5라, 절개(0%) 직접 피해 10.0 ≈ 유혈사태(−35%) 9.4로 같다. 유혈사태가 더 비싼 이유는 3열 도달이다.
- 영향: 가치 +58.4 → **+68.1%p (+9.7)**. 역병 의사 19위(34점) 그대로.


### 역병 의사 전체 분석 (2026-10-09, 수치 변경 없음)
- 결정 [제작자]: **조정 없음.** "실제론 좋아 건드릴 것 없어"
- 강함 모델: 19위(34점, 바닐라도 19위). 행동 19위·생존 18위·속도 4위·열 유연성 20위.
- 모델과 실전의 차이: 적 3·4열 동시 기절(실명 기체)은 이 영웅만 가진다. 제한 없는 4열 단일 기절(혼란 기체 폭발)도 현상금 사냥꾼 섬광탄과 둘뿐이다. 메인 전략(R-STRAT-01)의 핵심 수단인데, 모델은 후열 도달 기절을 과소평가한다(혼란 기체 폭발 +8.7). 3·4열 붙박이의 대가를 후열 기절 독점으로 받는다.
- 명중: 효과 본업 기술 1렙 95로 원칙과 일치. 전용 장신구(기절·중독 확률, 근접 출혈 세트)는 현재 구성을 받친다.
- 강화 작용제(−45.3%p): **보스전 전용 기술** [제작자]. 아군 1명 피해 +20~25%·속도 +3~5가 전투 끝까지 가므로, 긴 보스전에서 가치가 생긴다. 일반 전투 기준(지속 상한 2턴) 모델 값으로 판정하지 않는다. 검토했던 A안(스트레스 회복 추가 +70.7)·B안(아군 전체 +118.6)은 기각.
