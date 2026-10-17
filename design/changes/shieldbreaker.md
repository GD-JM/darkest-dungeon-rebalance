# 방패 파괴자 (shieldbreaker) 변경 항목

바닐라 수치: `heroes/shieldbreaker/shieldbreaker.vanilla.txt`

---

### SB-000 방향 결정: 2018-06-19 패치 이전(출시 2017-10-26) 수치로 복원
- 상태: 부분 적용 — 찌르기(SB-002)만 유지, 나머지는 SB-009에서 롤백
- 분류: 원칙복원 (출시 수치 복원)
- 목표: G-04, G-00
- 의도: 방패 파괴자는 출시 8개월 뒤 전 영웅 밸런스 패치에서 순 상향됐다. 특히 찌르기가 근접으로 전 열을 방어 무시로 공격하게 되면서 정답 조합의 핵심이 됐다. 패치로 바뀐 수치를 출시 값으로 되돌린다.
- 근거:
  - 출시 값 = 원 개발사가 처음 설계한 값 = 공식 패치 노트의 "변경 전" 값 (`analysis/dlc_history.md`)
  - 찌르기 데이터 비교 (SB-002)
  - 원칙 P-07
- 범위: 2018-06-19 패치 노트에 적힌 방패 파괴자 전투 수치 전부 (SB-001~008)
- 범위 밖 (유지):
  - 치명타 발동 효과(방어 +15%, 2라운드): 노트에 이전 값이 없어 복원 불가
  - 2018-08-15 회상 전투 빈도·야영 보상: 전투 수치가 아닌 시스템 보상
  - 속도 5/6/8/8/9: 패치와 무관한 원칙 이탈(R-GROW-03) → 별도 항목으로 검토
- 구현: 바뀐 효과는 바닐라 효과 파일을 덮어쓰지 않고 새 이름으로 추가(`effects/rebalance_shieldbreaker.effects.darkest`, 접두어 `RB SB`). 다른 모드와의 충돌을 줄이기 위함.
- 불확실성: 패치 노트의 "변경 후" 값과 현재 데이터가 1%p 다른 곳이 있다(무기 치명타, 살모사의 입맞춤 치명타). 노트의 "변경 전" 값을 그대로 적용했다.
  - 대안(현재 값에서 패치 차이만 되돌리기): 무기 치명타 6.5/7/7.5/8/8.5, 살모사의 입맞춤 치명타 4/5/5/5/6
- 방향 요약:
  - 하향: 찌르기, 살모사의 입맞춤 치명타·중독, 휘감기 치명타·중독, 노출 치명타, 무기 치명타(3~5레벨)
  - 상향: 구멍내기 속도 감소, 꿰뚫기 치명타, 뱀의 형상 속도, 노출·휘감기 피해 보정, 무기 치명타(1~2레벨)
  - 순방향: 하향
- 영향: 방패 파괴자의 딜·성장 가치(+10%) 하락 예상. 같은 정답 조합 후보인 노상강도·결투가와 비교 검토 필요.
- 검증: (플레이 후 기록)

### SB-001 무기 치명타·회피 출시 값
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 의도·근거: SB-000
- 따르는 원칙: P-07
- 어기는 원칙: R-GROW-03 — 출시 값 자체가 규칙 밖(치명타 +0.5/레벨, 회피 7.5 시작). 출시 복원을 우선.

| 레벨 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 무기 치명타 바닐라 | 6 | 7 | 8 | 9 | 10 |
| 무기 치명타 변경 | 7.5 | 8 | 8.5 | 9 | 9.5 |
| 회피 바닐라 | 8 | 13 | 18 | 23 | 28 |
| 회피 변경 | 7.5 | 12.5 | 17.5 | 22.5 | 27.5 |

### SB-002 찌르기: 대상 1·2열, 피해 보정 −20%, 치명타 2/3/4/4/4 (→ SB-013: 대상 1·2·3열, −10%)
- 상태: 적용 → 대상·피해 보정은 SB-013이 대체 (치명타 2/3/4/4/4는 유지)
- 현재 데이터 정정 (2026-10-17): 찌르기는 대상 1·2·3열, 피해 보정 −10%(바닐라와 같음), 치명타 2/3/4/4/4, 명중 85/90/95/100/105. "1·2열, −20%"는 SB-013(도굴꾼 얼굴 찍기보다 좋아야 해서 123열·−10)으로 바뀌었다. 아래 본문은 당시 기록.
- 분류: 원칙복원
- 목표: G-04, G-00
- 변경: 대상 1234열 → 12열 / 피해 보정 −10% → −20% / 치명타 5/6/7/8/9 → 2/3/4/4/4
- 의도: 근접·전 열·방어 무시가 한 기술에 겹친 상태를 해소한다.
- 근거:
  - 원본 근접 단일 공격 48개 중 4열까지 닿는 기술은 4개뿐: 도망자 판 뒤엎기(−10), 방패 파괴자 찌르기(−10), 광대 대단원(1·2열에서만 사용), 나병환자 위협(−85)
  - 방어 무시 공격 기술은 게임 전체에 3개: 찌르기(근접, 전 열, −10), 결투가 최후의 일격(원거리, −60), 도굴꾼 얼굴 찍기(근접, 1·2열, −15)
  - "근접 + 전 열 + 방어 무시"를 모두 가진 기술은 찌르기뿐인데, 피해 보정은 −10으로 가장 싸다(R-TRADE-01 기준 추가 대상 범위·방어 무시 가격이 반영되지 않음)
  - 출시 값(SB-000)
- 따르는 원칙: P-07, R-TRADE-01
- 어기는 원칙: R-SKILL-02 — 치명타 2/3/4/4/4는 +1/레벨이 아님(출시 값 자체)
- 영향: 방패 파괴자 주력 딜 하락. 후열·방어형 적 대응은 구멍내기·노출·휘감기로 분산.
- 추가 근거 (`analysis/accuracy_budget.md`): 원본 규칙은 대상 열이 넓을수록 명중이 낮다(열당 −1). 전 열 대상 찌르기는 명중 90으로 예측 83.5보다 +6.5 높다. 가격표·명중 모델 모두 "근접 전 열 도달"과 "방어 무시"를 가격에 넣지 못해 수치상 평범해 보일 뿐, 강함은 이 조합에 있다. SB-002 적용 후에도 명중 잔차 +4.5 → 플레이 검증 후 명중 85~90 조정 검토 여지.

### SB-003 구멍내기: 속도 감소 −2/−2/−3/−3/−4
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 속도 감소 −1/−1/−2/−2/−3 → −2/−2/−3/−3/−4 (적용 확률 100~140% 유지)
- 구현: 효과 `Daze Slowdown N` → 새 효과 `RB SB Daze Slowdown N`
- 의도·근거: SB-000 (보조 기술 출시 값 복원, 상향 방향)

### SB-004 살모사의 입맞춤: 치명타 5/6/6/6/7, 중독 2/2/3/3/4
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 치명타 5/6/7/8/9 → 5/6/6/6/7 / 중독 피해 3/3/4/4/5 → 2/2/3/3/4 (지속 3턴·확률 유지)
- 구현: 효과 `SB Adder Blight N` → 새 효과 `RB SB Adder Blight N`
- 불확실성: 이 중독 효과는 휘감기도 같이 쓰는 공유 효과다. 출시 때도 공유였다고 보고 휘감기에도 함께 적용했다(노트에는 살모사의 입맞춤에만 표기) → SB-007
- 어기는 원칙: R-SKILL-02 (출시 값 자체)

### SB-005 꿰뚫기: 치명타 1/2/2/2/3
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 치명타 −6/−5/−4/−3/−2 → 1/2/2/2/3
- 어기는 원칙: R-SKILL-02 (출시 값 자체)

### SB-006 노출: 피해 보정 −20%, 치명타 0/0/1/2/2
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 피해 보정 −40% → −20% / 치명타 2.5/3.5/4.5/5.5/6.5 → 0/0/1/2/2
- 어기는 원칙: R-SKILL-02 (출시 값 자체)

### SB-007 휘감기: 피해 보정 −20%, 치명타 2/3/4/4/4, 중독 2/2/3/3/4
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 피해 보정 −25% → −20% / 치명타 4/5/6/7/8 → 2/3/4/4/4 / 중독 3/3/4/4/5 → 2/2/3/3/4 (SB-004 공유 효과)
- 어기는 원칙: R-SKILL-02 (출시 값 자체)

### SB-008 뱀의 형상: 속도 +3/3/4/4/5, 지연 행동 판정 원복
- 상태: 기각 — SB-009에서 바닐라로 롤백
- 분류: 원칙복원
- 목표: G-04
- 변경: 자기 속도 +1/2/3/3/4 → +3/3/4/4/5 / `.is_stall_invalidating false` 제거(출시 때처럼 전투 지연 행동으로 분류하지 않음)
- 구현: 효과 `SB Serpent Speed N` → 새 효과 `RB SB Serpent Speed N`
- 의도·근거: SB-000

### SB-009 롤백: 찌르기만 출시 값 유지, 나머지는 바닐라로
- 상태: 적용
- 분류: 의도적예외 (SB-000 범위 축소)
- 목표: G-04, G-00
- 의도: 방패 파괴자 문제의 핵심은 찌르기의 "근접 + 전 열 + 방어 무시" 조합 하나다. 나머지까지 출시 값으로 되돌리면 문제와 무관한 기술까지 바뀌어 과도한 하향이 된다. 찌르기만 출시 값으로 둔다.
- 근거:
  - 제작자 판단 (2026-09-14)
  - SB-002에는 데이터 근거(원본 기술 비교)가 있지만, SB-001·SB-003~008에는 "출시 값이었다"는 사실 외에 과한 강세를 보여주는 데이터 근거가 없었다
  - 원칙 P-09
- 변경: SB-001, SB-003~008 기각 → 바닐라 값 복귀, 새 효과 파일 `effects/rebalance_shieldbreaker.effects.darkest` 삭제
- 유지: SB-002 찌르기 (대상 1·2열, 피해 보정 −20%, 치명타 2/3/4/4/4) — 이후 SB-013에서 대상 1·2·3열, 피해 보정 −10%로 바뀜
- 정리: "출시 값"은 근거의 출처일 뿐 문제 정의가 아니다. 문제가 확인된 기술에만 적용한다.
- 검증: (플레이 후 기록)

### SB-010 저항: 기절·이동 50 → 30 (값 유지, 근거 정정)

- 목표: P-22, R-RES-01
- 경위: 제작자가 먼저 50 → 30으로 조정했다. 그때 메모 "+20 되어있음 → 근거 없음 → 정상화"는 기준선을 30으로 가정했다. 실제 기준선은 40이므로 이 조정은 **+10 → −10**이다.
- 값은 **30이 맞다.** 근거는 노상강도 대조:
  - 노상강도: "두껍게 덧댄 외투를 걸치고 있어 **칼도 잘 박히지 않지만**, 무딘 검을 **받아내기보다는 회피**하는 쪽을 더 선호합니다" → 30 (−10)
  - 방패 파괴자: "**약간의** 방어 능력을 발휘합니다. 하지만 걸치고 있는 **의복은 던전보다 무대에 더 어울리는 것**이라, 살아남기 위해서는 **발 빠르게 움직여야** 합니다"
  - 가점은 노상강도보다 약하고("약간의"), 감점은 더 많다(무대 의복 + 회피 생존). **노상강도 이하이므로 30.**
- 결과: 값 변화 없음. 파일 주석을 정정본으로 교체.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### SB-010 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 기존 경장 설정 비교에 따라 기절/이동 저항30을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `resistances/`
  - 원본: `resistances: .stun 50% .poison 20% .bleed 30% .disease 30% .move 50% .debuff 30% .death_blow 67% .trap 20%`
  - 현재: `resistances: .stun 30% .poison 20% .bleed 30% .disease 30% .move 30% .debuff 30% .death_blow 67% .trap 20%`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 1행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// SB-010 저항: 기절·이동 50 -> 30. 기준선 40 대비 +10 -> -10(R-RES-01). 노상강도("두껍게 덧댄 외투... 칼도 잘 박히지 않지만, 받아내기보다는 회피 선호")가 30이다. 방패 파괴자는 가점이 더 약하고("약간의 방어 능력") 감점이 더 많다("의복은 던전보다 무대에 어울리는 것이라, 살아남기 위해서는 발 빠르게 움직여야") -> 노상강도 이하 = 30
```

### SB-011 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자 속도/체력 관계와 무기15% 성장 정상화 메모를 기록한다. 가설의 보편 타당성을 새로 검증한 것은 아니다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/shieldbreaker_weapon_1`
  - 원본: `weapon: .name "shieldbreaker_weapon_1" .atk 0% .dmg 6 12 .crit 7% .spd 6 .upgradeRequirementCode 0`
  - 현재: `weapon: .name "shieldbreaker_weapon_1" .atk 0% .dmg 6 12 .crit 7% .spd 5 .upgradeRequirementCode 0`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/shieldbreaker_weapon_2`
  - 원본: `weapon: .name "shieldbreaker_weapon_2" .atk 0% .dmg 7 14 .crit 8% .spd 8 .upgradeRequirementCode 1`
  - 현재: `weapon: .name "shieldbreaker_weapon_2" .atk 0% .dmg 7 13 .crit 8% .spd 6 .upgradeRequirementCode 1`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 8행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/shieldbreaker_weapon_3`
  - 원본: `weapon: .name "shieldbreaker_weapon_3" .atk 0% .dmg 8 16 .crit 9% .spd 8 .upgradeRequirementCode 2`
  - 현재: `weapon: .name "shieldbreaker_weapon_3" .atk 0% .dmg 7 15 .crit 9% .spd 6 .upgradeRequirementCode 2`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/shieldbreaker_weapon_4`
  - 원본: `weapon: .name "shieldbreaker_weapon_4" .atk 0% .dmg 9 18 .crit 10% .spd 9 .upgradeRequirementCode 3`
  - 현재: `weapon: .name "shieldbreaker_weapon_4" .atk 0% .dmg 8 16 .crit 10% .spd 7 .upgradeRequirementCode 3`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 10행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// 속도 56889 -> 55667 기존 법칙 따름 속도가 높은 대신 hp 가 낮음. 속도와 hp가 서로 상관관계를 가지게 설계되어있는 걸로 확인
```
- 기존 주석 원문:
```text
// 데미지 헤비인데 20% 20% 규칙임 -> 15% 15% 규칙으로 수정
```

### SB-012 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자가 혼자만 예외로 지적한 기본 회피8을7.5로 둔 현재 결정을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `armour/shieldbreaker_armour_0`
  - 원본: `armour: .name "shieldbreaker_armour_0" .def 8% .prot 0 .hp 20 .spd 0`
  - 현재: `armour: .name "shieldbreaker_armour_0" .def 7.5% .prot 0 .hp 20 .spd 0`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `armour/shieldbreaker_armour_1`
  - 원본: `armour: .name "shieldbreaker_armour_1" .def 13% .prot 0 .hp 24 .spd 0 .upgradeRequirementCode 0`
  - 현재: `armour: .name "shieldbreaker_armour_1" .def 12.5% .prot 0 .hp 24 .spd 0 .upgradeRequirementCode 0`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 16행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `armour/shieldbreaker_armour_2`
  - 원본: `armour: .name "shieldbreaker_armour_2" .def 18% .prot 0 .hp 28 .spd 0 .upgradeRequirementCode 1`
  - 현재: `armour: .name "shieldbreaker_armour_2" .def 17.5% .prot 0 .hp 28 .spd 0 .upgradeRequirementCode 1`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `armour/shieldbreaker_armour_3`
  - 원본: `armour: .name "shieldbreaker_armour_3" .def 23% .prot 0 .hp 32 .spd 0 .upgradeRequirementCode 2`
  - 현재: `armour: .name "shieldbreaker_armour_3" .def 22.5% .prot 0 .hp 32 .spd 0 .upgradeRequirementCode 2`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 18행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `armour/shieldbreaker_armour_4`
  - 원본: `armour: .name "shieldbreaker_armour_4" .def 28% .prot 0 .hp 36 .spd 0 .upgradeRequirementCode 3`
  - 현재: `armour: .name "shieldbreaker_armour_4" .def 27.5% .prot 0 .hp 36 .spd 0 .upgradeRequirementCode 3`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 19행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//회피 괴인처럼 7.5로 바꿈 8은 혼자만 예외적인 수치
```

### SB-013 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 영웅 정체성을 보호하려고 전열에서 전열까지 방어 무시 도달을 제한하되 도굴꾼 얼굴찍기 비교로 현재 대상123/피해−10을 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/pierce`
  - 원본: `combat_skill: .id "pierce" .level 0 .type "melee" .atk 90% .dmg -10% .crit 5% .move 0 1 .launch 321 .target 1234 .is_crit_valid True .ignore_protection true  .generation_guaranteed true`
  - 현재: `combat_skill: .id "pierce" .level 0 .type "melee" .atk 85% .dmg -10% .crit 2% .move 0 1 .launch 321 .target 123 .is_crit_valid True .ignore_protection true  .generation_guaranteed true`
  - 원본: `combat_skill: .id "pierce" .level 1 .type "melee" .atk 95% .dmg -10% .crit 6% .move 0 1 .launch 321 .target 1234 .is_crit_valid True .ignore_protection true `
  - 현재: `combat_skill: .id "pierce" .level 1 .type "melee" .atk 90% .dmg -10% .crit 3% .move 0 1 .launch 321 .target 123 .is_crit_valid True .ignore_protection true `
  - 원본: `combat_skill: .id "pierce" .level 2 .type "melee" .atk 100% .dmg -10% .crit 7% .move 0 1 .launch 321 .target 1234 .is_crit_valid True .ignore_protection true `
  - 현재: `combat_skill: .id "pierce" .level 2 .type "melee" .atk 95% .dmg -10% .crit 4% .move 0 1 .launch 321 .target 123 .is_crit_valid True .ignore_protection true `
  - 원본: `combat_skill: .id "pierce" .level 3 .type "melee" .atk 105% .dmg -10% .crit 8% .move 0 1 .launch 321 .target 1234 .is_crit_valid True .ignore_protection true `
  - 현재: `combat_skill: .id "pierce" .level 3 .type "melee" .atk 100% .dmg -10% .crit 4% .move 0 1 .launch 321 .target 123 .is_crit_valid True .ignore_protection true `
  - 원본: `combat_skill: .id "pierce" .level 4 .type "melee" .atk 110% .dmg -10% .crit 9% .move 0 1 .launch 321 .target 1234 .is_crit_valid True .ignore_protection true `
  - 현재: `combat_skill: .id "pierce" .level 4 .type "melee" .atk 105% .dmg -10% .crit 4% .move 0 1 .launch 321 .target 123 .is_crit_valid True .ignore_protection true `
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 27행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//이전 패치 버전으로 롤백, 사유 1,2,열에서 상대 전열 공격은 너무 사기 야만인의 정체성을 훼손
```
- 기존 주석 원문:
```text
// 노출 이란 기술과 명중 변경 -> 효과가 있으면 명중이 높고 없으면 낮다는 닼던 명중 기본 공식에 충실
```
- 기존 주석 원문:
```text
// SB-002 release: target ranks 1-2, dmg -20%, crit 2/3/4/4/4
```
- 기존 주석 원문:
```text
// 도굴꾼 얼굴찍기보다는 좋아야 해서 123열 타격으로 변경, 데미지 -20에서 -10로 변경
```

### SB-014 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 휘감기와 명중을 교환한 사용자의85 결정과 저레벨 중독 비교 메모를 기록한다. 현재 중독이 원본과 같은 부분은 추가 변경으로 주장하지 않는다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/spearing`
  - 원본: `combat_skill: .id "spearing" .level 0 .type "ranged" .atk 90% .dmg -60% .crit -6% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True `
  - 현재: `combat_skill: .id "spearing" .level 0 .type "ranged" .atk 85% .dmg -60% .crit -6% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 1" `
  - 원본: `combat_skill: .id "spearing" .level 1 .type "ranged" .atk 95% .dmg -60% .crit -5% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True `
  - 현재: `combat_skill: .id "spearing" .level 1 .type "ranged" .atk 90% .dmg -60% .crit -5% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 2"`
  - 원본: `combat_skill: .id "spearing" .level 2 .type "ranged" .atk 100% .dmg -60% .crit -4% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 3"`
  - 현재: `combat_skill: .id "spearing" .level 2 .type "ranged" .atk 95% .dmg -60% .crit -4% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 3"`
  - 원본: `combat_skill: .id "spearing" .level 3 .type "ranged" .atk 105% .dmg -60% .crit -3% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 4"`
  - 현재: `combat_skill: .id "spearing" .level 3 .type "ranged" .atk 100% .dmg -60% .crit -3% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 4"`
  - 원본: `combat_skill: .id "spearing" .level 4 .type "ranged" .atk 110% .dmg -60% .crit -2% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 5"`
  - 현재: `combat_skill: .id "spearing" .level 4 .type "ranged" .atk 105% .dmg -60% .crit -2% .move 1 0 .launch 1 .target ~1234 .is_crit_valid True  .effect "SB Spearing Blight 5"`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 53행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// 명중 90 -> 85로 수정 -> 휘감기랑 맞변경
```
- 기존 주석 원문:
```text
// 대신에 1,2렙에 중독 추가 = 조련사 스킬과 대칭
```

### SB-015 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 부가 효과가 있는 제어 기술에 명중을 배분하려는 사용자 의도로 찌르기와의 명중 교환을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/expose`
  - 원본: `combat_skill: .id "expose" .level 0 .type "melee" .atk 85% .dmg -40% .crit 2.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 1" "Destealth" "SB Slow 1"`
  - 현재: `combat_skill: .id "expose" .level 0 .type "melee" .atk 90% .dmg -40% .crit 2.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 1" "Destealth" "SB Slow 1"`
  - 원본: `combat_skill: .id "expose" .level 1 .type "melee" .atk 90% .dmg -40% .crit 3.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 2" "Destealth" "SB Slow 2"`
  - 현재: `combat_skill: .id "expose" .level 1 .type "melee" .atk 95% .dmg -40% .crit 3.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 2" "Destealth" "SB Slow 2"`
  - 원본: `combat_skill: .id "expose" .level 2 .type "melee" .atk 95% .dmg -40% .crit 4.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 3" "Destealth" "SB Slow 3"`
  - 현재: `combat_skill: .id "expose" .level 2 .type "melee" .atk 100% .dmg -40% .crit 4.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 3" "Destealth" "SB Slow 3"`
  - 원본: `combat_skill: .id "expose" .level 3 .type "melee" .atk 100% .dmg -40% .crit 5.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 4" "Destealth" "SB Slow 4"`
  - 현재: `combat_skill: .id "expose" .level 3 .type "melee" .atk 105% .dmg -40% .crit 5.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 4" "Destealth" "SB Slow 4"`
  - 원본: `combat_skill: .id "expose" .level 4 .type "melee" .atk 105% .dmg -40% .crit 6.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 5" "Destealth" "SB Slow 5"`
  - 현재: `combat_skill: .id "expose" .level 4 .type "melee" .atk 110% .dmg -40% .crit 6.5% .move 1 0 .launch 321 .target 123 .is_crit_valid True .ignore_stealth true  .effect "Expose Crit Debuff 5" "Destealth" "SB Slow 5"`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 65행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// 찌르기와 명중 변경 -> 효과가 있으면 명중이 높고 없으면 낮다는 기본 공식에 충실
```

### SB-016 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자의 명중90 결정과 MARK-01의 서브 표식 피해 재배분을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/single_out`
  - 원본: `combat_skill: .id "single_out" .level 0 .type "ranged" .atk 85% .dmg -25% .crit 4% .launch 32 .target 23 .is_crit_valid True  .effect "SB Dmg Marked 1" "SB Adder Blight 1"`
  - 현재: `combat_skill: .id "single_out" .level 0 .type "ranged" .atk 90% .dmg -25% .crit 4% .launch 32 .target 23 .is_crit_valid True  .effect "RB SB Dmg Marked 1" "SB Adder Blight 1"`
  - 원본: `combat_skill: .id "single_out" .level 1 .type "ranged" .atk 90% .dmg -25% .crit 5% .launch 32 .target 23 .is_crit_valid True  .effect "SB Dmg Marked 2" "SB Adder Blight 2"`
  - 현재: `combat_skill: .id "single_out" .level 1 .type "ranged" .atk 95% .dmg -25% .crit 5% .launch 32 .target 23 .is_crit_valid True  .effect "RB SB Dmg Marked 2" "SB Adder Blight 2"`
  - 원본: `combat_skill: .id "single_out" .level 2 .type "ranged" .atk 95% .dmg -25% .crit 6% .launch 32 .target 23 .is_crit_valid True  .effect "SB Dmg Marked 3" "SB Adder Blight 3"`
  - 현재: `combat_skill: .id "single_out" .level 2 .type "ranged" .atk 100% .dmg -25% .crit 6% .launch 32 .target 23 .is_crit_valid True  .effect "RB SB Dmg Marked 3" "SB Adder Blight 3"`
  - 원본: `combat_skill: .id "single_out" .level 3 .type "ranged" .atk 100% .dmg -25% .crit 7% .launch 32 .target 23 .is_crit_valid True  .effect "SB Dmg Marked 4" "SB Adder Blight 4"`
  - 현재: `combat_skill: .id "single_out" .level 3 .type "ranged" .atk 105% .dmg -25% .crit 7% .launch 32 .target 23 .is_crit_valid True  .effect "RB SB Dmg Marked 4" "SB Adder Blight 4"`
  - 원본: `combat_skill: .id "single_out" .level 4 .type "ranged" .atk 105% .dmg -25% .crit 8% .launch 32 .target 23 .is_crit_valid True  .effect "SB Dmg Marked 5" "SB Adder Blight 5"`
  - 현재: `combat_skill: .id "single_out" .level 4 .type "ranged" .atk 110% .dmg -25% .crit 8% .launch 32 .target 23 .is_crit_valid True  .effect "RB SB Dmg Marked 5" "SB Adder Blight 5"`
- 출처: `heroes/shieldbreaker/shieldbreaker.info.darkest`, 주석 추가 전 73행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"// 명중 85 -> 90으로 변경 "
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `SB Dmg Marked 1`
- 원본: `effect: .name "SB Dmg Marked 1"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40% .on_hit true .on_miss false`
- 현재: `effect: .name "SB Dmg Marked 1"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50% .on_hit true .on_miss false`
- 출처: `heroes/shieldbreaker/shieldbreaker.effects_edit.txt`, 주석 추가 전 114행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `SB Dmg Marked 2`
- 원본: `effect: .name "SB Dmg Marked 2"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 45%	.damage_high_multiply 45% .on_hit true .on_miss false`
- 현재: `effect: .name "SB Dmg Marked 2"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60% .on_hit true .on_miss false`
- 출처: `heroes/shieldbreaker/shieldbreaker.effects_edit.txt`, 주석 추가 전 116행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `SB Dmg Marked 3`
- 원본: `effect: .name "SB Dmg Marked 3"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50% .on_hit true .on_miss false`
- 현재: `effect: .name "SB Dmg Marked 3"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 70%	.damage_high_multiply 70% .on_hit true .on_miss false`
- 출처: `heroes/shieldbreaker/shieldbreaker.effects_edit.txt`, 주석 추가 전 118행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `SB Dmg Marked 4`
- 원본: `effect: .name "SB Dmg Marked 4"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 55%	.damage_high_multiply 55% .on_hit true .on_miss false`
- 현재: `effect: .name "SB Dmg Marked 4"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 80%	.damage_high_multiply 80% .on_hit true .on_miss false`
- 출처: `heroes/shieldbreaker/shieldbreaker.effects_edit.txt`, 주석 추가 전 120행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `SB Dmg Marked 5`
- 원본: `effect: .name "SB Dmg Marked 5"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60% .on_hit true .on_miss false`
- 현재: `effect: .name "SB Dmg Marked 5"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 90%	.damage_high_multiply 90% .on_hit true .on_miss false`
- 출처: `heroes/shieldbreaker/shieldbreaker.effects_edit.txt`, 주석 추가 전 122행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// MARK-01 SB Dmg Marked: 표식 피해 40~60 -> 50~90 (열 붙박이 패널티 보상, 피해 -25% 유지)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB SB Dmg Marked 1`
- 원본 (SB Dmg Marked 1): `effect: .name "SB Dmg Marked 1"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40% .on_hit true .on_miss false`
- 현재: `effect: .name "RB SB Dmg Marked 1"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50% .on_hit true .on_miss false`
- 출처: `effects/rebalance_shieldbreaker.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// edited vanilla effect (from dlc/702540_shieldbreaker/effects/shieldbreaker.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB SB Dmg Marked 2`
- 원본 (SB Dmg Marked 2): `effect: .name "SB Dmg Marked 2"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 45%	.damage_high_multiply 45% .on_hit true .on_miss false`
- 현재: `effect: .name "RB SB Dmg Marked 2"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60% .on_hit true .on_miss false`
- 출처: `effects/rebalance_shieldbreaker.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB SB Dmg Marked 3`
- 원본 (SB Dmg Marked 3): `effect: .name "SB Dmg Marked 3"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50% .on_hit true .on_miss false`
- 현재: `effect: .name "RB SB Dmg Marked 3"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 70%	.damage_high_multiply 70% .on_hit true .on_miss false`
- 출처: `effects/rebalance_shieldbreaker.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB SB Dmg Marked 4`
- 원본 (SB Dmg Marked 4): `effect: .name "SB Dmg Marked 4"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 55%	.damage_high_multiply 55% .on_hit true .on_miss false`
- 현재: `effect: .name "RB SB Dmg Marked 4"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 80%	.damage_high_multiply 80% .on_hit true .on_miss false`
- 출처: `effects/rebalance_shieldbreaker.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB SB Dmg Marked 5`
- 원본 (SB Dmg Marked 5): `effect: .name "SB Dmg Marked 5"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60% .on_hit true .on_miss false`
- 현재: `effect: .name "RB SB Dmg Marked 5"	.target "performer" .chance 100% .curio_result_type "positive" .keyStatus "tagged" .combat_stat_buff 1 .damage_low_multiply 90%	.damage_high_multiply 90% .on_hit true .on_miss false`
- 출처: `effects/rebalance_shieldbreaker.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}


### SB-017 뱀의 형상: 사용 열 3·2·1 → 4·3·2 (2026-10-09)
- 상태: 적용 (제작자 결정)
- 제작자 근거: 1열에서는 찌르기·살모사의 입맞춤·꿰뚫기 등 쓸 기술이 이미 있다. 1열에서 쓰면 앞으로 1칸이 무의미해 피해 2회 막기(SB Aegis)·속도만 받는 붙박이 운용이 되고, 이것이 "붙박이면 약하고 움직여야 고점"이라는 방패 파괴자 설정과 어긋난다.
- 변경: 사용 열 `321` → `432`. 효과(피해 2회 막기, 속도 +1~4, 전진 1, 전투당 2회) 그대로
- 의도한 순환: 1열에서 살모사의 입맞춤·꿰뚫기(뒤로 1칸) → 2열에서 뱀의 형상으로 1열 복귀하며 방어 준비.
- 영향: 모델은 사용 열을 세지 않아 −5.6%p 그대로.

### SB-018 꿰뚫기: 명중 90, 피해 −70%, 중독 1/1/2/2/3 × 2턴 (2026-10-16)
- 상태: 적용 (제작자 결정)
- 변경: 1렙 명중 85 → 90(바닐라 값으로, SB-014의 −5 취소), 피해 −60% → −70%, 중독 1~5렙 1/1/1/1/2 × 3턴 → 1/1/2/2/3 × 2턴(신규 사본 RB SB Spearing Blight 1~5, 확률 100~140% 그대로). 바닐라는 1·2렙 중독 없음, 3~5렙 1/1/2 × 3턴.
- 근거: 조련사 사냥개 습격(광역 1·2·3·4, −70%, 출혈 1/1/2/2/3 × 3턴)과 같은 줄에 맞춘다. 같은 지속 피해 수치를 쓰되 꿰뚫기는 2턴 — 방패 파괴자 무기(8-16)가 조련사(7-13)보다 세서 직접 피해 쪽 기술로 갈린다.
- 지속 피해 총량(1~5렙): 2/2/4/4/6 (바닐라 0/0/3/3/6). 비교: `analysis/aoe23_survey.md`.
- 영향(모델(5렙)): 바닐라 +159, 이전 RB +127 → **+102**(직접 +97, 중독 +55, 치명 +24, 전열→후열 +26). 사냥개 습격 +86. 방패 파괴자 51점 13위.

### SB-019 방어구 회피: 7.5 → 바닐라 8 (SB-012 취소) (2026-10-17)
- 상태: 적용 (제작자 결정 "회피는 바닐라 8")
- 근거: SB-012(7.5)는 SB-009에서 기각한 출시 값을 새 근거 없이 다시 넣은 것(창작마당 감사 X).
### SB-011 보충: 무기 피해 성장 15%는 R-GROW-01 예외로 유지 (2026-10-17)
- [제작자] 방패 파괴자는 헤비 계열이라 15%가 맞다. 규칙상(매혹 시 열 2) 20%지만 예외로 기록(rules.md R-GROW-01 예외 목록).
