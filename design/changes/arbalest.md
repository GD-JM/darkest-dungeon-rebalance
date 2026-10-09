# 석궁사수 (arbalest) 변경 항목

바닐라 수치: `heroes/arbalest/arbalest.vanilla.txt`

---

### ARB-001 야전 붕대질: 스택 힐 → 출혈 치료, 회복량 상향
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
  - 회복 1~5레벨: 2-3 / 3-3 / 3-4 / 4-4 / 4-5 → **3-3 / 3-4 / 4-5 / 5-6 / 6-7** (5레벨 평균 4.5 → 6.5)
  - 효과: `Arb Stacking Heal N`(받는 회복 +38%) 제거 → 신규 `RB ARB Cure Bleed`(대상 출혈 치료)
  - 계산: 8.5 − 1(출혈만 치료) = 7.5 → 상한 7.0 아래로 6.5
- 의도: 석궁사수를 "출혈 던전 전용 회복 담당"으로 만든다. 스택 힐은 성전사 전투 치유로 이전할 예정(제안 상태).
- 영향
  - 총사는 모드 대상이 아니므로(창작마당 모드와 충돌) 응급처치는 그대로다. 같은 기술이 두 영웅에서 달라진다.
  - 스택 힐이 사라져 회복 증폭 조합(붕대 → 성녀)이 약해진다.
- 검증 (P-15)
  1. `.cure_bleed 1`이 전투 기술 효과에서 동작하는지. 원본에서는 붕대 아이템만 쓰던 키다. **실패 시 `Cure`(출혈·중독 동시)로 되돌리고 회복 6-7 → 6-6으로 내린다.**
  2. 아군 대상 기술에서 `.target "target"`이 회복 대상에게 적용되는지.

### ARB-002 회복 표기 정정: `.heal N` → `.heal N N` (적용, 회복량 변화 없음)

- 문제: ARB-001에서 회복량을 "3/4/5/6/7로 직관적으로" 바꾸며 `.heal 3`처럼 숫자를 하나만 썼다. 바닐라 기술 줄의 회복 표기 **45개는 전부 `.heal 최소 최대` 두 숫자**다. 한 숫자는 게임이 어떻게 읽는지 보장되지 않는다(강함 모델은 회복 0으로 읽었다).
- 조치: 같은 값을 두 번 쓴다. `.heal 3 3` ~ `.heal 7 7`. 뜻(랜덤 없는 고정 회복)은 그대로다.
- 같은 문제가 성녀 신성한 은총(`.heal 5`~`9`)에도 있어 함께 고쳤다(`vestal.info.darkest`).
- 검증 (P-15): 게임에서 붕대질 1렙이 정확히 3을 회복하는지.

### 검토 기록 (2026-09-28): 저격 대상 2·3·4 유지, 결집 신호탄 상향안

- **저격이 1열을 못 치는 이유**: 바닐라에서 후열에서 쏘는 원거리 단일기 5개(저격·조준 사격·단검 투척·권총 사격·표적 지정)가 **전부 1열을 뺀다.** 길드 "두드러지는 대상을 저격", 역할 분담(1열은 근접), 메인 전략(후열 스트레스 발생원부터, R-STRAT-01), 최강 단일 사격의 대가. **유지** (제작자 동의).
- **결집 신호탄 상향안 → ARB-003으로 적용 (2026-09-28)**: 스트레스 회복 1/2/2/3/3 · 확률 60/60/67/60/67 → **3/3/4/4/5 · 74% 고정**. 파티 기대 회복 5렙 6.0 → 11.1(광대 격려의 선율 한 번 분량), 1렙 1.8 → 6.7. 조련사 위험 경보(RB 17.8)의 약 62% — 결집 신호탄은 아군 기절·표식 해제·횃불·은신 해제를 함께 하므로 더 작게. 근거: 길드 "그녀는 **결집소**이자 포탑이며 어둠 속의 횃불"(P-22), 광역 스트레스 회복 법칙 H6(확률형 60~74%).

### ARB-003 결집 신호탄: 스트레스 회복 3/3/4/4/5, 확률 74% 고정 (적용)

- 목표: G-05 (석궁사수를 스트레스 힐러로도 쓰게) [제작자 지시 2026-09-28]
- 변경: `FlareHealStress` 회복 1/2/2/3/3 → **3/3/4/4/5**, 확률 60/60/67/60/67 → **74% 고정** (자신 외 아군 3명). 총사 스키트 사격은 바닐라 그대로(`RB ARB` 사본).
- 근거: 위 검토 기록. 설정 "결집소이자… 어둠 속의 횃불"(P-22), 광역 스트레스 회복 법칙 H6, 위험 경보(RB)의 약 62%(다른 기능 4개를 함께 하므로).
- 결과: 파티 기대 회복 1렙 1.8 → 6.7, 5렙 6.0 → 11.1. v2 모델 1.8 → 3.3 HP.
- 모델 수정: 대상 `performer_group_other`(자신 외 아군 전원)를 1명으로 세던 것을 3명으로 고쳤다. 영웅 순위 변화 없음.

### 컨셉 확정: 석궁사수는 3·4열 붙박이 (제작자 2026-09-28)

> 석궁은 3·4열 붙박이가 컨셉이다. 1·2열에서 완벽히 바보가 되어야 한다.

- 그래서 **야전 붕대질 사용 열 4·3 → 4·3·2 안은 철회**한다. 1·2열에서 쓸 수 있는 기술은 무차별 사격(무작위 대상, 명중 75)과 결집 신호탄 둘뿐인 지금 구성이 컨셉 그대로다.
- R-RANK-01과 연결: 붙박이 영웅은 **주 열에서 더 강해야** 한다. 석궁사수 조정은 3·4열 성능 안에서만 한다.

### ARB-004 사냥돌 발사 5레벨: 밀치기 확률 105 → 115 (적용)

- 목표: G-02 (결함 수정)
- 변경: 5레벨 효과 `Bolo Push 1D`(105) → **`Bolo Push 1E`(115)**. 새 효과 없음.
- 근거
  1. **바닐라에 `Bolo Push 1E`(115)가 정의돼 있는데 어떤 기술도 쓰지 않는다.** 석궁사수·총사 모두 4·5레벨이 같은 1D를 쓴다. 원 개발사가 만들고 연결을 빠뜨린 것으로 본다.
  2. **이동 기술 12개 중 레벨이 오를수록 약해지는 유일한 기술**이었다(`analysis/displacement.md` M1·M5). 몬스터 이동 저항이 레벨마다 +20 오르는데 확률 성장이 5레벨에서 멈춰, 성공률이 43% → 40% → 28%로 떨어졌다. 다른 이동기는 50~69%로 유지된다.
  3. 1레벨 75에서 시작하는 것(광역 2명의 대가, 가격표상 정가)은 그대로 두고 **멈춘 마지막 단계만 되살린다.** 가장 작은 수정이다(P-12).
- 결과: 5레벨 밀치기 성공률(대상 1명당) 30.5% → **37.8%**. 총사 산탄은 바닐라 그대로(MUS-000).
- R-DATA-01: 같은 계열(Bolo Push)의 다른 단계를 가리키는 재사용이라 허용된다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### ARB-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 기존 MARK-01 재배분에 맞춰 표식 파티의 서브 딜러 선택을 넓힌다. 마지막 레벨 상한은 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/sniper_shot`
  - 원본: `combat_skill: .id "sniper_shot" .level 0 .type "ranged" .atk 95% .dmg 0% .crit 5% .launch 43 .target 234 .is_crit_valid True  .effect "Sniper Damage 1" .generation_guaranteed true`
  - 현재: `combat_skill: .id "sniper_shot" .level 0 .type "ranged" .atk 95% .dmg 0% .crit 5% .launch 43 .target 234 .is_crit_valid True  .effect "RB ARB Sniper Damage 1" .generation_guaranteed true`
  - 원본: `combat_skill: .id "sniper_shot" .level 1 .type "ranged" .atk 100% .dmg 0% .crit 6% .launch 43 .target 234 .is_crit_valid True  .effect "Sniper Damage 2"`
  - 현재: `combat_skill: .id "sniper_shot" .level 1 .type "ranged" .atk 100% .dmg 0% .crit 6% .launch 43 .target 234 .is_crit_valid True  .effect "RB ARB Sniper Damage 2"`
  - 원본: `combat_skill: .id "sniper_shot" .level 2 .type "ranged" .atk 105% .dmg 0% .crit 7% .launch 43 .target 234 .is_crit_valid True  .effect "Sniper Damage 3"`
  - 현재: `combat_skill: .id "sniper_shot" .level 2 .type "ranged" .atk 105% .dmg 0% .crit 7% .launch 43 .target 234 .is_crit_valid True  .effect "RB ARB Sniper Damage 3"`
  - 원본: `combat_skill: .id "sniper_shot" .level 3 .type "ranged" .atk 110% .dmg 0% .crit 8% .launch 43 .target 234 .is_crit_valid True  .effect "Sniper Damage 4"`
  - 현재: `combat_skill: .id "sniper_shot" .level 3 .type "ranged" .atk 110% .dmg 0% .crit 8% .launch 43 .target 234 .is_crit_valid True  .effect "RB ARB Sniper Damage 4"`
- 출처: `heroes/arbalest/arbalest.info.darkest`, 주석 추가 전 22행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Sniper Damage 1`
- 원본: `effect: .name "Sniper Damage 1".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 50%  .damage_high_multiply 50% .crit_chance_add 9%	 .on_hit true .on_miss false`
- 현재: `effect: .name "Sniper Damage 1".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60% .crit_chance_add 9%	 .on_hit true .on_miss false`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 19행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Sniper Damage 2`
- 원본: `effect: .name "Sniper Damage 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60% .crit_chance_add 10%	 .on_hit true .on_miss false`
- 현재: `effect: .name "Sniper Damage 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 70%  .damage_high_multiply 70% .crit_chance_add 10%	 .on_hit true .on_miss false`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 22행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Sniper Damage 3`
- 원본: `effect: .name "Sniper Damage 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 70%  .damage_high_multiply 70% .crit_chance_add 11%	 .on_hit true .on_miss false`
- 현재: `effect: .name "Sniper Damage 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 80%  .damage_high_multiply 80% .crit_chance_add 11%	 .on_hit true .on_miss false`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 25행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Sniper Damage 4`
- 원본: `effect: .name "Sniper Damage 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 80%  .damage_high_multiply 80% .crit_chance_add 12%	 .on_hit true .on_miss false`
- 현재: `effect: .name "Sniper Damage 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 90%  .damage_high_multiply 90% .crit_chance_add 12%	 .on_hit true .on_miss false`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 28행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB Sniper Damage 1`
- 원본 (Sniper Damage 1): `effect: .name "Sniper Damage 1".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 50%  .damage_high_multiply 50% .crit_chance_add 9%	 .on_hit true .on_miss false`
- 현재: `effect: .name "RB ARB Sniper Damage 1".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60% .crit_chance_add 9%	 .on_hit true .on_miss false`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB Sniper Damage 2`
- 원본 (Sniper Damage 2): `effect: .name "Sniper Damage 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60% .crit_chance_add 10%	 .on_hit true .on_miss false`
- 현재: `effect: .name "RB ARB Sniper Damage 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 70%  .damage_high_multiply 70% .crit_chance_add 10%	 .on_hit true .on_miss false`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB Sniper Damage 3`
- 원본 (Sniper Damage 3): `effect: .name "Sniper Damage 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 70%  .damage_high_multiply 70% .crit_chance_add 11%	 .on_hit true .on_miss false`
- 현재: `effect: .name "RB ARB Sniper Damage 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 80%  .damage_high_multiply 80% .crit_chance_add 11%	 .on_hit true .on_miss false`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB Sniper Damage 4`
- 원본 (Sniper Damage 4): `effect: .name "Sniper Damage 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 80%  .damage_high_multiply 80% .crit_chance_add 12%	 .on_hit true .on_miss false`
- 현재: `effect: .name "RB ARB Sniper Damage 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged" .duration 3 .combat_stat_buff 1 .damage_low_multiply 90%  .damage_high_multiply 90% .crit_chance_add 12%	 .on_hit true .on_miss false`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}

### ARB-004 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 5레벨 밀치기 연결 누락을 보완해 마지막 업그레이드의 성공률 성장을 복구한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/bola`
  - 원본: `combat_skill: .id "bola" .level 4 .type "ranged" .atk 115% .dmg -50% .crit 6% .launch 43 .target ~12 .is_crit_valid True  .effect "Bolo Push 1D"`
  - 현재: `combat_skill: .id "bola" .level 4 .type "ranged" .atk 115% .dmg -50% .crit 6% .launch 43 .target ~12 .is_crit_valid True  .effect "Bolo Push 1E"`
- 출처: `heroes/arbalest/arbalest.info.darkest`, 주석 추가 전 44행; Git 원문 {"commit": "5a0b78fbe8644317732f33431d3f433231f39626", "summary": "ARB-004 사냥돌 발사 5렙 Bolo Push 1E + 시체 제거 가치 R-VALUE-05 + 모델 파서 수정"}
- 기존 주석 원문:
```text
// ARB-004 bola 5레벨: Bolo Push 1D(105) -> 1E(115). 바닐라에 1E가 정의돼 있는데 어떤 기술도 쓰지 않는다(연결 누락). 4·5레벨이 같은 105를 써서 성장이 멈췄고, 이동 저항이 레벨당 +20 오르는 동안 성공률이 43 -> 40 -> 28%로 떨어지는 유일한 이동 기술이었다(M1·M5). 5레벨 성공률 30.5 -> 37.8%
```

### ARB-001 ARB-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 예측 가능한 동료 회복과 출혈 치료로 다른 회복 기술과 역할을 나눈다. 단일값 회복은 최소/최대 같은 값 표기를 유지한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/battlefield_bandage`
  - 원본: `combat_skill: .id "battlefield_bandage" .level 0 .heal 2 3 .launch 43 .target @1234  .effect "Arb Stacking Heal 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_bandage" .level 0 .heal 3 3 .launch 43 .target @1234  .effect "RB ARB Cure Bleed" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_bandage" .level 1 .heal 3 3 .launch 43 .target @1234  .effect "Arb Stacking Heal 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_bandage" .level 1 .heal 4 4 .launch 43 .target @1234  .effect "RB ARB Cure Bleed" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_bandage" .level 2 .heal 3 4 .launch 43 .target @1234  .effect "Arb Stacking Heal 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_bandage" .level 2 .heal 5 5 .launch 43 .target @1234  .effect "RB ARB Cure Bleed" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_bandage" .level 3 .heal 4 4 .launch 43 .target @1234  .effect "Arb Stacking Heal 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_bandage" .level 3 .heal 6 6 .launch 43 .target @1234  .effect "RB ARB Cure Bleed" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "battlefield_bandage" .level 4 .heal 4 5 .launch 43 .target @1234  .effect "Arb Stacking Heal 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "battlefield_bandage" .level 4 .heal 7 7 .launch 43 .target @1234  .effect "RB ARB Cure Bleed" .is_stall_invalidating false`
- 출처: `heroes/arbalest/arbalest.info.darkest`, 주석 추가 전 62행; Git 원문 {"commit": "8f52fcfe821547d58c60e6547066b8d66da8553d", "summary": "총사 모드 제외(MUS-000) + 회복 표기 정정(ARB-002: 석궁사수 붕대질, 성녀 신성한 은총)"}
- 기존 주석 원문:
```text
// 표기: .heal N -> .heal N N. 바닐라 기술 줄 회복 45개는 전부 "최소 최대" 두 숫자다. 한 숫자는 게임 해석이 보장되지 않아 같은 값을 두 번 쓴다(회복량 변화 없음)
```
- 기존 주석 원문:
```text
// ARB-001 battlefield_bandage: heal 2-3/4-5 -> 3-3/6-7, Arb Stacking Heal -> RB ARB Cure Bleed
```
- 기존 주석 원문:
```text
// 34567로 바꿈 직관적으로
```

### ARB-003 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 저레벨 불안정성을 줄이고 광대 외 파티 스트레스 회복 선택지를 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/flare`
  - 원본: `combat_skill: .id "flare" .level 0 .type "ranged" .atk 95% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 1" "Destealth" "FlareHealStress 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flare" .level 0 .type "ranged" .atk 95% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 1" "Destealth" "RB ARB FlareHealStress 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flare" .level 1 .type "ranged" .atk 100% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 2" "Destealth" "FlareHealStress 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flare" .level 1 .type "ranged" .atk 100% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 2" "Destealth" "RB ARB FlareHealStress 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flare" .level 2 .type "ranged" .atk 105% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 3" "Destealth" "FlareHealStress 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flare" .level 2 .type "ranged" .atk 105% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 3" "Destealth" "RB ARB FlareHealStress 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flare" .level 3 .type "ranged" .atk 110% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 4" "Destealth" "FlareHealStress 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flare" .level 3 .type "ranged" .atk 110% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 4" "Destealth" "RB ARB FlareHealStress 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flare" .level 4 .type "ranged" .atk 115% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 5" "Destealth" "FlareHealStress 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flare" .level 4 .type "ranged" .atk 115% .dmg -100% .crit 0% .launch 4321 .target ~1234 .is_crit_valid False .ignore_stealth true  .effect "FlareClear 1" "FlareLight 5" "Destealth" "RB ARB FlareHealStress 5" .is_stall_invalidating false`
- 출처: `heroes/arbalest/arbalest.info.darkest`, 주석 추가 전 72행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `FlareHealStress 1`
- 원본: `effect: .name "FlareHealStress 1" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 1 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "FlareHealStress 1" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 143행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// ARB-003 결집 신호탄 1레벨 스트레스 회복 1 (60%) -> 3 (74% 고정). 길드 "결집소이자 포탑이며 어둠 속의 횃불". 광역 스트레스 회복 법칙 H6(확률형). 파티 기대 1렙 1.8 -> 6.7, 5렙 6.0 -> 11.1, 위험 경보의 약 62%
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `FlareHealStress 2`
- 원본: `effect: .name "FlareHealStress 2" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 2 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "FlareHealStress 2" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 150행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// ARB-003 결집 신호탄 2레벨 스트레스 회복 2 (60%) -> 3 (74% 고정). 길드 "결집소이자 포탑이며 어둠 속의 횃불". 광역 스트레스 회복 법칙 H6(확률형). 파티 기대 1렙 1.8 -> 6.7, 5렙 6.0 -> 11.1, 위험 경보의 약 62%
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `FlareHealStress 3`
- 원본: `effect: .name "FlareHealStress 3" .target "performer_group_other" .curio_result_type "positive" .chance 67% .healstress 2 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "FlareHealStress 3" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 4 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 157행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// ARB-003 결집 신호탄 3레벨 스트레스 회복 2 (67%) -> 4 (74% 고정). 길드 "결집소이자 포탑이며 어둠 속의 횃불". 광역 스트레스 회복 법칙 H6(확률형). 파티 기대 1렙 1.8 -> 6.7, 5렙 6.0 -> 11.1, 위험 경보의 약 62%
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `FlareHealStress 4`
- 원본: `effect: .name "FlareHealStress 4" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "FlareHealStress 4" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 4 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 164행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// ARB-003 결집 신호탄 4레벨 스트레스 회복 3 (60%) -> 4 (74% 고정). 길드 "결집소이자 포탑이며 어둠 속의 횃불". 광역 스트레스 회복 법칙 H6(확률형). 파티 기대 1렙 1.8 -> 6.7, 5렙 6.0 -> 11.1, 위험 경보의 약 62%
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `FlareHealStress 5`
- 원본: `effect: .name "FlareHealStress 5" .target "performer_group_other" .curio_result_type "positive" .chance 67% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "FlareHealStress 5" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 5 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 171행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// ARB-003 결집 신호탄 5레벨 스트레스 회복 3 (67%) -> 5 (74% 고정). 길드 "결집소이자 포탑이며 어둠 속의 횃불". 광역 스트레스 회복 법칙 H6(확률형). 파티 기대 1렙 1.8 -> 6.7, 5렙 6.0 -> 11.1, 위험 경보의 약 62%
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB FlareHealStress 1`
- 원본 (FlareHealStress 1): `effect: .name "FlareHealStress 1" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 1 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB ARB FlareHealStress 1" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB FlareHealStress 2`
- 원본 (FlareHealStress 2): `effect: .name "FlareHealStress 2" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 2 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB ARB FlareHealStress 2" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB FlareHealStress 3`
- 원본 (FlareHealStress 3): `effect: .name "FlareHealStress 3" .target "performer_group_other" .curio_result_type "positive" .chance 67% .healstress 2 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB ARB FlareHealStress 3" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 4 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB FlareHealStress 4`
- 원본 (FlareHealStress 4): `effect: .name "FlareHealStress 4" .target "performer_group_other" .curio_result_type "positive" .chance 60% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB ARB FlareHealStress 4" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 4 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 19행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB FlareHealStress 5`
- 원본 (FlareHealStress 5): `effect: .name "FlareHealStress 5" .target "performer_group_other" .curio_result_type "positive" .chance 67% .healstress 3 .on_hit true .on_miss true .queue true .apply_once true`
- 현재: `effect: .name "RB ARB FlareHealStress 5" .target "performer_group_other" .curio_result_type "positive" .chance 74% .healstress 5 .on_hit true .on_miss true .queue true .apply_once true`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 21행; Git 원문 {"commit": "5b9b587c16f06c41a44d4119c10ff9c0a0a6d20d", "summary": "ARB-003 결집 신호탄 스트레스 회복 3/3/4/4/5, 74% 고정 + 모델 그룹 대상 수정"}
- 기존 주석 원문:
```text
// mod-only new effects
```

### ARB-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 예측 가능한 동료 회복과 출혈 치료로 다른 회복 기술과 역할을 나눈다. 단일값 회복은 최소/최대 같은 값 표기를 유지한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB ARB Cure Bleed`
- 원본: `None`
- 현재: `effect: .name "RB ARB Cure Bleed" .target "target" .curio_result_type "positive" .chance 100% .cure_bleed 1 .on_hit true .on_miss false`
- 출처: `heroes/arbalest/arbalest.effects_edit.txt`, 주석 추가 전 191행; Git 원문 {"commit": "0e828416b7347a0972bd347c000141963cc8b189", "summary": "ARB-001 야전 붕대질 출혈 치료, PD-001 야전 의술 중독 치료 (회복량 상향)"}
- 기존 주석 원문:
```text
// ARB-001 battlefield_bandage: cure bleed on the healed ally (replaces Arb Stacking Heal)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB ARB Cure Bleed`
- 원본: `None`
- 현재: `effect: .name "RB ARB Cure Bleed" .target "target" .curio_result_type "positive" .chance 100% .cure_bleed 1 .on_hit true .on_miss false`
- 출처: `effects/rebalance_arbalest.effects.darkest`, 주석 추가 전 24행; Git 원문 {"commit": "0e828416b7347a0972bd347c000141963cc8b189", "summary": "ARB-001 야전 붕대질 출혈 치료, PD-001 야전 의술 중독 치료 (회복량 상향)"}


### ARB-006 결집 신호탄: 스트레스 회복 확률 100% 고정 (적용 2026-10-06)
- 상태: 사용자 명시 승인으로 적용. ARB-003의 회복량은 유지하고 74% 확률 결정을 대체한다.
- 사용자 원문: “석궁 100으로 해보자 그리고 나머지 수정할 부분 있는지 전체 다 검토하면서 알려줘”
- 목표/의도: G-00 조합 다양성. 광대 없이 팀 스트레스를 관리할 때 결집 신호탄의 회복 실패를 제거하여 석궁사수의 지원 신뢰도를 높인다. 기존 효과의 확률만 바꾸며 새로운 발동 규칙을 추가하지 않는다.
- 변경 (기술1~5): 스트레스 회복 적용 확률74%→100%; 다른 동료 각각의 회복3/3/4/4/5 유지. 자신은 회복 대상이 아니다. 기술 명중·기절/표식 해제·은신 해제·횃불 효과와 전용 장신구를 보존한다.
- 수지: 동료3명이 충분한 스트레스를 잃은 상태의 합산 회복은 기술1 기대6.66→9, 기술5 기대11.10→15. 과회복·죽거나 없는 대상·장신구와 반올림을 제외한 값이다. 한 명에게 큰 회복을 집중하는 선율과 역할이 다르다.
- 원칙/이력: H6의 확률형 광역 회복 관찰에 대한 사용자 승인 예외. ARB-003의 옛 한국어 메모를 원문 보존한다. 발라드의 기존 선턴/치명/간접 스트레스 공급 하향과 대체 지원 공급을 P-11 취지에서 함께 검토하지만, 이번 확률 증가만으로 전체 전력 총량 보존을 입증하지 않는다. 다른 영웅 후보는 이번 승인에 포함되지 않는다.
- 검증: 편집 사본과 도구 생성 효과의5행만 확률 변경; 재적용 일관성; 요청 외 수치/참조/사용자 작업 보존;20영웅 의도 주석과 배포 파일 목록 크기 검사. 실제 게임 회복/툴팁/그룹 적용 확인은 미실시.

### ARB-007 볼라: 피해 −50% → −40% (2026-10-09)
- 상태: 적용 (제작자 결정)
- 문제: 석궁사수 핵심 4개(저격 +152.3, 조명탄 +143.3, 무작위 사격 +52.5, 야전 붕대 회복 역할)에 밀려 볼라(+19.8)·제압 사격(−23.7)을 고를 이유가 없었다 [제작자].
- 변경: 1~5레벨 피해 −50% → **−40%**. 적 1·2열 광역·밀치기 1·명중 그대로
- 영향: +19.8 → **+33.0%p**(강함 모델 5렙). 비교안: −30% +46.2, 밀치기 2 +62.5.


### ARB-008 제압 사격: 피해 −80% → −60% (2026-10-09)
- 상태: 적용 (제작자 결정, 2·3·4열 광역안과 비교 후)
- 비교(강함 모델 5렙 %p, 약화 장신구 +30% 가정): 현재 −23.7 / 장신구 −14.9 · 2·3·4열 +4.3 / +16.2(장신구 상승폭 +11.9로 최대) · **3·4열 −60% +10.5 / +19.3**
- 근거: 기본·장신구 착용 모두 −60% 안이 높고, 후열 스트레스 딜러 2명에게 피해와 명중·치명타 감소를 집중해 메인 전략(R-STRAT-01)과 맞는다. 독주·함성의 광역 명중 감소와도 "후열만 골라 깎는다"로 구분된다.
- 변경: 1~5레벨 피해 −80% → **−60%**. 대상 3·4열·제압(명중 −15~−20, 치명타 −15~−19, 2턴) 그대로
