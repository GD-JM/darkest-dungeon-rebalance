# 야만인 (hellion) 변경 항목

바닐라 수치: `heroes/hellion/hellion.vanilla.txt`

---

### HEL-000 방향: 탈진 제거 + 몰아치는 아트에 맞는 성능
- 상태: 방향 (세부 항목은 HEL-001~)
- 목표: G-01, G-02, **P-19**
- 사용자 의도 (원문)
  > 야만인 모든 기술에 탈진이 있잖아 탈진 없애고 기술 자체를 너프 하는 방식으로 하려 하는데
  > 야만인은 누가봐도 몰아치게 생겼잖아 근데 몰아칠 수 없어 탈진 때문에
- 근거: 탈진(`Hellion Exhaust`)은 지속시간이 없어 **전투가 끝날 때까지** 피해 −20%·속도 −3이고 `is_clear_debuff_valid: false`라 해제도 불가다. 함성·돌파·출혈 3개에 붙어 있었다.
- 탈진 제거 전 스펙 잔차 (야만인 기준 명중 105, 정가선 +15)

  | 기술 | 제거 전 | 제거 시 | 판정 |
  |---|---|---|---|
  | 야만스러운 함성! | −47 | −21 | 이미 피해 100% 포기 + 전투당 3회로 값을 다 치른 위에 얹은 삼중 과금 |
  | 돌파 | −11 | +15 | 소폭 반납 필요 |
  | 출혈 | +17 | +43 | 확실한 반납 필요 |

### HEL-001 야만스러운 함성!: 기절 → 자기 강화 + 시체 제거
- 상태: 적용 (제작자 직접 수정)
- 분류: 의도적 조정 / 구조 변경
- 목표: G-02, P-19
- 변경
  - 탈진 제거, **강한 기절 제거**, 전투당 3회 제한 해제
  - `Adrenaline 5`(자기 명중 +10, 피해 +30%, 디버프 해제) + `clear_corpses` 추가
  - 대상 `~12` → `~1234`
  - 아드레날린 분출에서 `Adrenaline`을 빼 함성으로 옮긴 형태다(HEL-004)
- **예외 기록: 대상 `~1234`의 광역은 연출용이며 가격 환산에서 제외한다**
  - 피해 −100%이고 적에게 걸리는 효과가 하나도 없다. `clear_corpses`는 `.target "target_group"`이라 대상 열과 무관하게 시체 전체를 지우고, `Adrenaline 5`는 `.target "performer"`라 자기에게만 걸린다.
  - 따라서 대상을 `~1234`로 하든 `~12`로 하든 **게임상 결과가 동일하다.** 적 4명을 때리는 판정이지만 적에게 일어나는 일은 0이다.
  - 가격표로 환산하면 광역 4대상이 +72%p로 잡혀 잔차 +50이 나오지만 **실효는 0**이다. 이 숫자를 근거로 함성을 너프하면 안 된다.
  - **제작자 판단 [사용자]**: 전체를 향해 포효하는 **공격 이펙트가 뜨는 것이 목적**이다(중보병 포효와 같은 연출). 기능이 아니라 연출의 문제이므로 숫자로 깎지 않는다.
  - 제안했던 대안(적 약화 `RB HEL Yawp Debuff` 명중 −10·속도 −5, `RB HEL Yawp Crit` 받는 치명타 +10% 신설로 광역을 실제 작동시키는 안)은 **기각**했다. 이유: ① 신규 효과 2종은 P-09에서 가장 무거운 변경 ② 야만인에게 줄 만한 약화가 마땅치 않고 중보병 포효·방패 파괴자와 성격이 겹친다.
- 남은 영향: **게임에서 1·2열 동시 기절이 사라졌다.** 전열 광역 기절은 함성이 유일했고, 광역 기절은 역병 의사 실명 기체(3·4열)만 남는다. 제작자가 다른 영웅에서 대체 자리를 찾는 중이다.

### HEL-002 돌파: 탈진 제거 + 피해 −50% → −60%
- 상태: 적용 (제작자 직접 수정)
- 분류: 의도적 조정
- 변경: `Hellion Exhaust Sm` 제거, 피해 보정 −50% → −60%
- 근거: 탈진 제거분(+26%p)의 일부를 피해로 반납했다.
- **판정 정정 (2026-09-27)**: 처음에 자기 전진 1칸(`.move 0 1`)을 부담 −17로 계산해 잔차 −7로 보고 "과지불"이라 했으나, **R-RANK-01에 따라 자기 이동은 부담이 아니다.** 이동을 빼면 잔차 **+10**으로 정상 범위이며 −60% 유지가 맞다.

### HEL-003 출혈: 탈진 제거 + 피해 +20% → 0% + 치명타 상향
- 상태: 적용 (제작자 직접 수정)
- 분류: 의도적 조정
- 목표: G-01, P-19
- 변경: 탈진 제거, 피해 보정 `+20%` → `0%`, 치명타 보정 `6~10` → **`10~14`**(실제 치명타 15~23%)
- 제작자 메모 (원문)
  > 살모사의 입맞춤에 비해 명중 5 낮음, 살모사의 입맞춤은 2열까지 공격 가능 / 치명타 확률로 보정
- 근거
  - **대응 대상은 방패 파괴자 살모사의 입맞춤.** 두 기술은 지속 피해가 완전히 동일하다(5×3턴, 확률 140). 변경 전에는 실제 치명타까지 11~19%로 같았다.
  - 바닐라는 "명중 −5 + 대상 1열"의 대가를 **피해 +20%**로 보상하고 있었다. 이번 변경은 그 보상 수단을 **치명타로 교체**한 것이다.
  - **후반 고방어 대응 [사용자]**: 지속 피해는 방어도를 무시한다(R-EFF-02). 영웅 등급 일반 몬스터 85종 중 38%가 방어도를 보유하고 평균 35%, 40% 이상이 15%다. 치명타 23%면 4~5회에 한 번 **출혈 5×5턴 = 25 HP**가 방어도와 무관하게 박힌다(R-CMB-08).
  - 치명타 23%는 신비학자 제물 암습·심연에서의 손아귀와 **공동 1위**이며 단독 1위는 아니다(P-14).
- 잔차: 변경 전 +17 → 변경 후 **+61** (살모사의 입맞춤 +51 대비 +10). 야만인이 20명 중 11위라 허용 범위로 본다.
  - 주의: 이 값은 R-CMB-08 개정판 치명타 계수(피해 0%인 지속 피해 기술 1.6%p/점)를 쓴 것이다. 옛 계수(0.69)로는 +48이었다.

### HEL-004 아드레날린 분출: 자가 회복 상향
- 상태: 적용 (제작자가 편집 사본 수정 → Claude가 게임 적용 2026-09-27)
- 분류: 의도적 조정
- 목표: **G-05**(회복 편중 해소), G-02
- 제작자 메모 (원문)
  > 야만인 힐수치 조정 12234 에서 34567으로
- 변경: `HellionHealSelf 1~5`의 회복 `1/2/2/3/4` → **`3/4/5/6/7`** → 적용 시 `RB HEL HellionHealSelf 1~5`로 분리. 바닐라 효과 파일은 건드리지 않았다.
- 근거: HEL-001로 `Adrenaline`이 함성으로 옮겨가면서 이 기술에 **치료 + 자가 회복 4**만 남았다. 자가 회복 시세 표준은 8.0(조련사 상처 핥기)이라 4는 절반이었고, 한 턴을 써서 4를 회복하는 기술은 아무도 고르지 않는다(G-02 위반). 7은 표준에 근접한다.
- 주의: 편집 사본만 고쳐진 상태로 **게임에는 반영되지 않고 있었다.** `tools/apply_effect_edits.py` 실행이 필요하다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### HEL-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 출혈·유혈·강철 백조·아드레날린 분출 고정 조합 밖의 변주를 위해 평타 명중을 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/wicked_hack`
  - 원본: `combat_skill: .id "wicked_hack" .level 0 .type "melee" .atk 85% .dmg 0% .crit 4% .launch 21 .target 12 .is_crit_valid True  .generation_guaranteed true`
  - 현재: `combat_skill: .id "wicked_hack" .level 0 .type "melee" .atk 90% .dmg 0% .crit 4% .launch 21 .target 12 .is_crit_valid True  .generation_guaranteed true`
  - 원본: `combat_skill: .id "wicked_hack" .level 1 .type "melee" .atk 90% .dmg 0% .crit 5% .launch 21 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_hack" .level 1 .type "melee" .atk 95% .dmg 0% .crit 5% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_hack" .level 2 .type "melee" .atk 95% .dmg 0% .crit 6% .launch 21 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_hack" .level 2 .type "melee" .atk 100% .dmg 0% .crit 6% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_hack" .level 3 .type "melee" .atk 100% .dmg 0% .crit 7% .launch 21 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_hack" .level 3 .type "melee" .atk 105% .dmg 0% .crit 7% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_hack" .level 4 .type "melee" .atk 105% .dmg 0% .crit 8% .launch 21 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_hack" .level 4 .type "melee" .atk 110% .dmg 0% .crit 8% .launch 21 .target 12 .is_crit_valid True `
- 출처: `heroes/hellion/hellion.info.darkest`, 주석 추가 전 27행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//명중 85 -> 90 근거는 블리드아웃,이프잇블리즈,아이언스완,아드레날린 러쉬 4개가 너무 정답조합임 변주 필요함
```

### HEL-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 몰아치는 연출에 맞춰 탈진/기절 대신 자기 준비와 시체 제거를 맡기고 반복 사용을 허용한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/barbaric_yawp`
  - 원본: `combat_skill: .id "barbaric_yawp" .level 0 .type "melee" .atk 95% .dmg -100% .crit 0% .per_battle_limit 3 .launch 21 .target ~12 .is_crit_valid False  .effect "Hero Strong Stun 1" "Hellion Exhaust" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "barbaric_yawp" .level 0 .type "melee" .atk 95% .dmg -100% .crit 0% .launch 21 .target ~1234 .is_crit_valid False  .effect "clear_corpses" "Adrenaline 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "barbaric_yawp" .level 1 .type "melee" .atk 100% .dmg -100% .crit 0% .per_battle_limit 3 .launch 21 .target ~12 .is_crit_valid False  .effect "Hero Strong Stun 2" "Hellion Exhaust" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "barbaric_yawp" .level 1 .type "melee" .atk 100% .dmg -100% .crit 0% .launch 21 .target ~1234 .is_crit_valid False  .effect "clear_corpses"  "Adrenaline 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "barbaric_yawp" .level 2 .type "melee" .atk 105% .dmg -100% .crit 0% .per_battle_limit 3 .launch 21 .target ~12 .is_crit_valid False  .effect "Hero Strong Stun 3" "Hellion Exhaust" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "barbaric_yawp" .level 2 .type "melee" .atk 105% .dmg -100% .crit 0% .launch 21 .target ~1234 .is_crit_valid False  .effect "clear_corpses" "Adrenaline 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "barbaric_yawp" .level 3 .type "melee" .atk 110% .dmg -100% .crit 0% .per_battle_limit 3 .launch 21 .target ~12 .is_crit_valid False  .effect "Hero Strong Stun 4" "Hellion Exhaust" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "barbaric_yawp" .level 3 .type "melee" .atk 110% .dmg -100% .crit 0% .launch 21 .target ~1234 .is_crit_valid False  .effect "clear_corpses" "Adrenaline 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "barbaric_yawp" .level 4 .type "melee" .atk 115% .dmg -100% .crit 0% .per_battle_limit 3 .launch 21 .target ~12 .is_crit_valid False  .effect "Hero Strong Stun 5" "Hellion Exhaust" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "barbaric_yawp" .level 4 .type "melee" .atk 115% .dmg -100% .crit 0% .launch 21 .target ~1234 .is_crit_valid False  .effect "clear_corpses" "Adrenaline 5" .is_stall_invalidating false`
- 출처: `heroes/hellion/hellion.info.darkest`, 주석 추가 전 42행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//탈진 삭제
```
- 기존 주석 원문:
```text
//스턴 삭제
```
- 기존 주석 원문:
```text
//시체 제거 추가
```
- 기존 주석 원문:
```text
//아드레날린 버프 추가
```

### HEL-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 탈진 제거의 이득 일부를 직접 피해로 반납한다. 자기 전진을 자동 패널티로 가격 매기지 않는다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/breakthru`
  - 원본: `combat_skill: .id "breakthru" .level 0 .type "melee" .atk 85% .dmg -50% .crit -1% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  .effect "Hellion Exhaust Sm"`
  - 현재: `combat_skill: .id "breakthru" .level 0 .type "melee" .atk 85% .dmg -60% .crit -1% .move 0 1 .launch 432 .target ~123 .is_crit_valid True`
  - 원본: `combat_skill: .id "breakthru" .level 1 .type "melee" .atk 90% .dmg -50% .crit 0% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  .effect "Hellion Exhaust Sm"`
  - 현재: `combat_skill: .id "breakthru" .level 1 .type "melee" .atk 90% .dmg -60% .crit 0% .move 0 1 .launch 432 .target ~123 .is_crit_valid True`
  - 원본: `combat_skill: .id "breakthru" .level 2 .type "melee" .atk 95% .dmg -50% .crit 1% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  .effect "Hellion Exhaust Sm"`
  - 현재: `combat_skill: .id "breakthru" .level 2 .type "melee" .atk 95% .dmg -60% .crit 1% .move 0 1 .launch 432 .target ~123 .is_crit_valid True `
  - 원본: `combat_skill: .id "breakthru" .level 3 .type "melee" .atk 100% .dmg -50% .crit 2% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  .effect "Hellion Exhaust Sm"`
  - 현재: `combat_skill: .id "breakthru" .level 3 .type "melee" .atk 100% .dmg -60% .crit 2% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  `
  - 원본: `combat_skill: .id "breakthru" .level 4 .type "melee" .atk 105% .dmg -50% .crit 3% .move 0 1 .launch 432 .target ~123 .is_crit_valid True  .effect "Hellion Exhaust Sm"`
  - 현재: `combat_skill: .id "breakthru" .level 4 .type "melee" .atk 105% .dmg -60% .crit 3% .move 0 1 .launch 432 .target ~123 .is_crit_valid True `
- 출처: `heroes/hellion/hellion.info.darkest`, 주석 추가 전 60행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//피해량 50 -> 60
```
- 기존 주석 원문:
```text
//탈진 삭제
```

### HEL-004 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 공격 강화를 함성으로 옮기고 자기 회복을 높여 회복 기술의 역할을 분리한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/adrenaline_rush`
  - 원본: `combat_skill: .id "adrenaline_rush" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Adrenaline 1" "HellionHealSelf 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "adrenaline_rush" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Cureself" "RB HEL HellionHealSelf 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "adrenaline_rush" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Adrenaline 2" "HellionHealSelf 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "adrenaline_rush" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Cureself" "RB HEL HellionHealSelf 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "adrenaline_rush" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Adrenaline 3" "HellionHealSelf 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "adrenaline_rush" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Cureself" "RB HEL HellionHealSelf 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "adrenaline_rush" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Adrenaline 4" "HellionHealSelf 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "adrenaline_rush" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Cureself" "RB HEL HellionHealSelf 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "adrenaline_rush" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Adrenaline 5" "HellionHealSelf 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "adrenaline_rush" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Cureself" "RB HEL HellionHealSelf 5" .is_stall_invalidating false`
- 출처: `heroes/hellion/hellion.info.darkest`, 주석 추가 전 68행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HellionHealSelf 1`
- 원본: `effect: .name "HellionHealSelf 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 1	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "HellionHealSelf 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 3	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `heroes/hellion/hellion.effects_edit.txt`, 주석 추가 전 84행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HellionHealSelf 2`
- 원본: `effect: .name "HellionHealSelf 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 2	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "HellionHealSelf 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 4	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `heroes/hellion/hellion.effects_edit.txt`, 주석 추가 전 88행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HellionHealSelf 3`
- 원본: `effect: .name "HellionHealSelf 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 2	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "HellionHealSelf 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 5	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `heroes/hellion/hellion.effects_edit.txt`, 주석 추가 전 92행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HellionHealSelf 4`
- 원본: `effect: .name "HellionHealSelf 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 3	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "HellionHealSelf 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 6	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `heroes/hellion/hellion.effects_edit.txt`, 주석 추가 전 96행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HellionHealSelf 5`
- 원본: `effect: .name "HellionHealSelf 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 4	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "HellionHealSelf 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 7	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `heroes/hellion/hellion.effects_edit.txt`, 주석 추가 전 100행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//야만인 힐수치 조정 12234 에서 34567으로
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HEL HellionHealSelf 1`
- 원본 (HellionHealSelf 1): `effect: .name "HellionHealSelf 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 1	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "RB HEL HellionHealSelf 1" .target "performer" .curio_result_type "positive" .chance 100% .heal 3	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `effects/rebalance_hellion.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HEL HellionHealSelf 2`
- 원본 (HellionHealSelf 2): `effect: .name "HellionHealSelf 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 2	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "RB HEL HellionHealSelf 2" .target "performer" .curio_result_type "positive" .chance 100% .heal 4	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `effects/rebalance_hellion.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HEL HellionHealSelf 3`
- 원본 (HellionHealSelf 3): `effect: .name "HellionHealSelf 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 2	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "RB HEL HellionHealSelf 3" .target "performer" .curio_result_type "positive" .chance 100% .heal 5	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `effects/rebalance_hellion.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HEL HellionHealSelf 4`
- 원본 (HellionHealSelf 4): `effect: .name "HellionHealSelf 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 3	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "RB HEL HellionHealSelf 4" .target "performer" .curio_result_type "positive" .chance 100% .heal 6	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `effects/rebalance_hellion.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HEL HellionHealSelf 5`
- 원본 (HellionHealSelf 5): `effect: .name "HellionHealSelf 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 4	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 현재: `effect: .name "RB HEL HellionHealSelf 5" .target "performer" .curio_result_type "positive" .chance 100% .heal 7	.on_hit true .on_miss false .queue false .source_heal_type hero_skill`
- 출처: `effects/rebalance_hellion.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}

### HEL-003 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 탈진 제거 뒤 피해를 반납하고 살모사의 입맞춤과 비교한 사용자의 치명 보상 결정을 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/bleed_out`
  - 원본: `combat_skill: .id "bleed_out" .level 0 .type "melee" .atk 85% .dmg 20% .crit 6% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 1" "Hellion Exhaust"`
  - 현재: `combat_skill: .id "bleed_out" .level 0 .type "melee" .atk 85% .dmg 0% .crit 10% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 1" `
  - 원본: `combat_skill: .id "bleed_out" .level 1 .type "melee" .atk 90% .dmg 20% .crit 7% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 2" "Hellion Exhaust"`
  - 현재: `combat_skill: .id "bleed_out" .level 1 .type "melee" .atk 90% .dmg 0% .crit 11% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 2" `
  - 원본: `combat_skill: .id "bleed_out" .level 2 .type "melee" .atk 95% .dmg 20% .crit 8% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 3" "Hellion Exhaust"`
  - 현재: `combat_skill: .id "bleed_out" .level 2 .type "melee" .atk 95% .dmg 0% .crit 12% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 3" `
  - 원본: `combat_skill: .id "bleed_out" .level 3 .type "melee" .atk 100% .dmg 20% .crit 9% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 4" "Hellion Exhaust"`
  - 현재: `combat_skill: .id "bleed_out" .level 3 .type "melee" .atk 100% .dmg 0% .crit 13% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 4" `
  - 원본: `combat_skill: .id "bleed_out" .level 4 .type "melee" .atk 105% .dmg 20% .crit 10% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 5" "Hellion Exhaust"`
  - 현재: `combat_skill: .id "bleed_out" .level 4 .type "melee" .atk 105% .dmg 0% .crit 14% .launch 1 .target 1 .is_crit_valid True  .effect "Strong Bleed 5" `
- 출처: `heroes/hellion/hellion.info.darkest`, 주석 추가 전 75행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//탈진 없애고 피해량 20 -> 0 "
```
- 기존 주석 원문:
```text
// 살모사의 입맞춤에 비해 명중 5 낮음 , 살모사의 입맞춤은 2열까지 공격 가능
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"// 치명타 확률로 보정 "
```
- 기존 주석 원문:
```text
// 치명타 6 -> 10
```
