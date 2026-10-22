# 고행자 (flagellant) 변경 항목

바닐라 수치: `heroes/flagellant/flagellant.vanilla.txt`

---

### FLA-000 방향 결정: 2018-06 하향 이후 상태를 출발점으로
- 상태: 결정
- 분류: 방향 메모 (수치 변경 없음)
- 목표: G-04
- 의도: 고행자는 출시 후 너무 강해 공식 패치(2018-06-19)에서 회복·생존 계열이 하향됐다. 이 하향은 원 개발사의 조정으로 존중하고, 출시 수치로 되돌리지 않는다.
- 근거:
  - `analysis/dlc_history.md`: 방혈 전투당 3회·체력 40% 이하, 구제 전투당 2회·체력 40% 이하, 인내 스트레스 회복 12→16 에서 10→14로 하향
  - 원칙 P-06
- 이후 검토 범위: 하향 후에도 남은 원칙 이탈 — 매혹 시 1열인데 피해 성장 20%(R-GROW-01), 속도 6/6/8/8/9(R-GROW-03), 죽음의 일격 저항 73, 처벌 가격표 대비 +45
- 대비: 방패 파괴자는 같은 패치에서 순 상향이라 출시 수치로 복원(SB-000)

### FLA-001 저항: 기절·이동 50 → 40, 출혈 65 → 60 (적용)

- 목표: P-22, R-RES-01
- 경위: 제작자가 먼저 기절·이동 50 → 30, 출혈 65 → 60으로 조정했다. 그때 메모는 "+20 되어있음 → 근거 없음 → 정상화", "출혈 +35를 +30으로 → 나병환자 기절 +30과 맞춤"으로, **기준선을 30으로 가정**했다. 실제 기준선은 기절·이동 40이다(`analysis/resistances.md` 1절).
- 기절·이동 → **40 (기준값)**:
  - 가점: 대장간 "흉터와 상처들로부터 기쁨을 얻으며… 스스로 찢음으로써 **더욱 견고해집니다**" — 게임에서 가장 강한 고통 내성.
  - 감점: 대장간 문구에는 옷 이야기가 없지만, 외형이 거의 벌거벗은 차림이다(P-19).
  - 가점과 감점이 상쇄되어 기준값. 바닐라 50은 감점을 무시했고, RB 30(−10)은 **순감소를 뒷받침할 문장이 없다.**
  - 제작자의 원래 의도("근거 없음 → 정상화")를 올바른 기준선으로 실행한 값이기도 하다.
- 출혈 → **60 유지**, 근거만 정정:
  - 원래 근거 "나병환자 기절 +30과 맞춤"은 틀렸다. 나병환자 기절은 기준 40 대비 **+20**이다.
  - 올바른 근거: **대표 저항의 상한은 +30**이다. 괴인 중독 60, 역병 의사 중독 60, 신비학자 약화 60이 모두 +30이고, 바닐라 고행자 출혈 +35가 유일한 초과였다. 고행자 출혈은 설정상 가장 강한 문장을 가진 대표 저항이므로 상한 +30에 맞춘다.
- 결과: 저항 총합 220 → 240.

### FLA-002~004 (제안, 미적용) — 재검토: 모델 버그 위에서 나온 상향안

2026-09-27 분기 대화에서 제안했으나 **저장소에 적용된 적 없다.**
- FLA-002 재기: 회복 지속 3 고정, 자기 출혈 지속 3 → 2
- FLA-003 소진: 주는 회복 −25%만 제거 (받는 회복 −25%, 속도 −3 유지)
- FLA-004 인내: 자기 스트레스 −2

**전제가 틀렸다.** 제안 당시 표는 구제를 평타의 **4%**로 봤는데, 이는 `heal_percent 0.43`(= 43%)을 0.43%로 읽은 모델 버그였다. 고치면 구제는 **266%**, 고행자는 영웅 순위 **1위**다(체력 40% 이하 유지율 0.6 가정, `analysis/hero_power_v2.md` 9절). 상향 세 건은 모두 보류한다.

**FLA-003의 형평성 (제작자 지적 2026-09-28)**

소진은 방혈과 구제 **양쪽 모두**가 건다. 첫 사용에는 적용되지 않고(`.queue true`), 이후 회복에 적용된다. 자기 회복은 "주는 회복"이자 "받는 회복"이라 두 감소를 모두 받는다.

| 두 번째 사용부터 | 현재 소진 (가산 가정) | FLA-003 | 변화 |
|---|---|---|---|
| 방혈 자기 회복 (38 x 50% = 19) | 9.5 | **14.3** | **+50%** |
| 구제 자기 회복 (19) | 9.5 | 14.3 | +50% |
| 구제 아군 회복 (43 x 43% = 18.5) | 13.9 | 18.5 | +33% |
| 재기 아군 지속 회복 (12) | 9.0 | 12.0 | +33% |

- FLA-003은 방혈을 하향하지 않는다. **오히려 방혈 자기 회복을 가장 크게(+50%) 올린다.**
- 두 기술의 자기 회복 부분은 똑같이 취급된다. 구제가 더 얻는 건 아군 회복 부분이 따로 있기 때문이다.
- 문제는 형평이 아니라 **방향**이다. 방혈은 쓸 수 있는 순간 게임 최고 기술이다. 거기에 +50%를 얹는 안은 버린다.
- 아군 회복만 풀고 방혈은 그대로 두려면 "주는 회복 0 / 받는 회복 −50%"로 바꿔야 한다(가산이면 자기 회복 x0.5 유지). 이 경우 다른 힐러에게 받는 회복도 반으로 줄어 생존이 크게 깎인다. 고행자 전체 수준이 V-06으로 확정된 뒤 결정한다.

### 기술 판정 (2026-09-28, v2 모델, 5레벨, 평타 5.63 HP)

| 기술 | 가치 | 판정 | 이유 |
|---|---|---|---|
| **방혈** | 23.3 HP (414%) | **조건부 사기** | 출혈 9x3 = 게임 최대, 피해 보정 0%, 자기 회복 최대 체력 50%. 쓸 수 있으면 게임 전체 최고 기술. 제동은 공식 패치의 체력 40% 조건·전투당 3회뿐이라 **판정이 V-06에 달려 있다**(유지율 0.3이면 11.7) |
| **처벌** | 16.7 HP (297%) | **사기 아님 (동류 상단)** | 아래 동류 비교 참고 |
| 구제 | 15.0 HP (266%) | 정상~강 | 아군 43% + 자기 50%. 체력 40% 조건·전투당 2회·소진이 제동 |
| 슬픔의 비 | 8.9 HP (157%) | 정상 | 1·2열에서 **3·4열 광역 출혈**. 광역 지속 0.40을 받는다. 후열 스트레스 발생원 우선(R-STRAT-01)의 가치는 모델에 없어 과소평가 가능 |
| 인내 | 3.4 HP (61%) | 약함 | 스트레스 14(x0.43) − 자기 스트레스 6. 속도 강화는 모델에 없음 |
| 재기 | −3.0 HP | **단독으론 손해** | 아군 12 회복 < 자기 출혈 15. 대신 **체력 40% 조건을 여는 "혹사 엔진"**이다. 그 가치는 방혈·구제의 유지율(0.6)에 들어가 있고 재기 자신에게는 잡히지 않는다 |
| 고통 | 0 (모델 밖) | 미평가 | 아군 출혈·중독 흡수, 자기 표식(공격 유도), 받는 스트레스 −40%, 죽음의 일격 저항 +10. 전부 모델이 계산하지 않는 항목 |

**처벌은 왜 "사기"로 분류됐었나 — 그리고 왜 아닌가**

"처벌 가격표 대비 +45(과대 2위)"는 R-TRADE-01 **가격표(층 A)**의 값이다. 기능이 비슷한 기술들의 피해 보정을 회귀한 예측값은 −45 정도인데, 처벌은 0%라서 +45가 나왔다.

1·2열을 치는 단일 출혈 기술끼리 비교하면(RB, 5레벨):

| 영웅 | 기술 | 사용→대상 | 피해 보정 | 무기 평균 | 출혈 | 직접 HP | 출혈 HP | 합계 |
|---|---|---|---|---|---|---|---|---|
| 고행자 | 방혈 | 12→12 | 0% | **8.0** | 9x3 | 6.4 | 13.3 | 23.3 |
| 야만인 | 출혈 | 1→1 | 0% | 14.5 | 5x3 | 11.7 | 7.6 | 20.1 |
| **고행자** | **처벌** | **12→12** | **0%** | **8.0** | **6x3** | **6.9** | **9.5** | **16.7** |
| 광대 | 저며내기 | 32→23 | −33% | 10.0 | 5x3 | 5.9 | 8.3 | 15.8 |
| 노상강도 | 정맥 절개 | 321→12 | −40% | 12.5 | 4x3 | 6.7 | 6.7 | 13.8 |
| 역병 의사 | 절개 | 321→12 | 0% | 10.0 | 4x3 | 7.6 | 5.7 | 13.5 |

1. **+45의 대부분은 약한 무기 탓이다.** 피해 보정은 무기에 곱하는 비율이다. 고행자 무기(평균 8)는 동류 최저라, 0%로 쳐도 직접 피해가 **6.9 HP로 −40%인 정맥 절개(6.7)와 같다.** 가격표는 무기 크기를 보지 않는다(R-TRADE-01 "무기가 강한 영웅은 피해 보정이 낮게 매겨졌다"의 거울상).
2. **진짜 차이는 출혈이다.** 턴당 6은 동류(4~5)보다 1~2 높아 출혈분이 약 +3 HP다. 합계는 절개·정맥 절개보다 약 3 HP(+24%) 높고, 야만인 출혈(20.1)보다 낮다. **동류 범위 안의 상단**이다.
3. **대가가 있다.** 사용 1·2열 → 대상 1·2열로 동류 중 두 번째로 좁고(2018 패치로 3열 대상 삭제), 출혈 면역 몬스터(영웅 등급 36.5%)에게는 직접 피해 6.9만 남는다.

→ 처벌은 조정 대상이 아니다. 고행자에서 수치가 튀는 곳은 **방혈**이다.

### FLA-005 재기: 아군 턴당 회복 = 자해 출혈 턴당, 지속 3 고정 (적용)

- 목표: G-02, G-05 [제작자 지시 2026-09-28: "자기 출혈은 유지, 타 캐릭 힐량은 높여, 저레벨·고레벨 효율 일관되게"]
- 변경: `Flag Healdot` 턴당 2/2/3/3/4 → **3/3/4/4/5**, 지속 2/3/2/3/3 → **3 고정**. 자해 출혈(`Flag Self Wound`)은 그대로.
- **"일관된 효율"의 기준**: 게임의 고정량 회복은 영웅 체력과 같은 속도로 오른다(`heal.md`, 1→5레벨 x1.7~2.2). 그래서 기준을 **대상 최대 체력 대비 회복 비율**로 잡았다. 레벨별 영웅 체력 중앙값은 23/28/33/38/43이다.

| 레벨 | 현재 아군 회복 | 체력 대비 | **변경 후** | **체력 대비** | 자해 기대 | 파티 순 체력 (현재 → 변경 후) |
|---|---|---|---|---|---|---|
| 1 | 2x2 = 4 | 17% | 3x3 = 9 | **39%** | 5.4 | −1.4 → **+3.6** |
| 2 | 2x3 = 6 | 21% | 3x3 = 9 | **32%** | 6.3 | −0.3 → **+2.7** |
| 3 | 3x2 = 6 | 18% | 4x3 = 12 | **36%** | 9.6 | −3.6 → **+2.4** |
| 4 | 3x3 = 9 | 24% | 4x3 = 12 | **32%** | 10.8 | −1.8 → **+1.2** |
| 5 | 4x3 = 12 | 28% | 5x3 = 15 | **35%** | 15.0 | −3.0 → **0.0** |

- 체력 대비 회복이 17~28%(3레벨이 2레벨보다 낮은 역전 포함)에서 **32~39%로 고르게** 된다. 파티 순 체력은 전 레벨 0 이상이다.
- **설정 (P-22)**: 턴당 회복량이 자해 출혈 턴당과 같다. "스스로를 혹사함으로써 얻는 힘" — **흘린 피만큼 돌려준다**는 교환이 수치로 보인다.
- 5레벨 순 체력이 0인 이유: 자해 출혈 확률이 120 → 160으로 올라 적용률이 60% → 100%가 되기 때문이다(영웅 저항은 레벨로 오르지 않음, R-RES-02). 자해 출혈은 제작자 지시로 유지했다. 5레벨 재기는 **고행자 체력을 아군에게 옮기는 기술**이고, 그 출혈이 체력 40% 조건을 열어 방혈·구제로 이어진다.
- 기각한 대안: 턴당 2/3/4/5/6. 5레벨 18(체력 대비 42%)은 조건 없는 구제(43%)급이고 체력 대비 비율도 26% → 42%로 다시 벌어진다.

### FLA-006 인내: 자기 스트레스 10/9/8/7/6 → 4 고정 (적용)

- 목표: G-05 [제작자 지시 2026-09-28: "스트레스 힐러로서 저렙부터 일관되게 좋게"]
- **"일관된 효율"의 기준**: 몬스터 스트레스 피해는 던전 레벨이 올라도 **그대로**다(`heal.md`, 견습 → 영웅 x1.00). 스트레스 회복은 1레벨부터 쓸 만해야 한다. 기준은 스트레스 전문 힐러인 광대 격려의 선율(8~12, 대가 없음)과의 거리다.

| 레벨 | 회복 | 자기 스트레스 (현재 → 변경 후) | 순회복 (현재 → 변경 후) | 광대 대비 |
|---|---|---|---|---|
| 1 | 10 | 10 → 4 | 0 → **6** | −8 → **−2** |
| 2 | 11 | 9 → 4 | 2 → **7** | −7 → **−2** |
| 3 | 12 | 8 → 4 | 4 → **8** | −6 → **−2** |
| 4 | 13 | 7 → 4 | 6 → **9** | −5 → **−2** |
| 5 | 14 | 6 → 4 | 8 → **10** | −4 → **−2** |

- 1레벨 순회복 0(쓸 이유가 없음)이 6이 되고, **광대보다 항상 2 낮게** 고정된다. 광대는 전문 힐러로 남고(P-14), 인내는 "1~4열 어디서나, 자기를 대가로" 쓰는 스트레스 힐러가 된다.
- **FLA-000과의 관계**: 공식 하향 항목인 **회복량 10~14는 건드리지 않았다.** 2018 패치의 자기 스트레스 변경(+10 → +6)은 고레벨 비용 **완화**였고, FLA-006은 그 방향을 전 레벨로 넓힌 것이다. 단 1레벨 4는 출시(+5)·패치 후(+10)보다 낮은 새 값이다.
- 참고: 출시 버전은 회복 12~16, 자기 +5~+9로 **순회복 7 고정**이었다. 원 개발사도 처음엔 "레벨과 무관한 일정한 순회복"으로 설계했다.

### 모델 참고

v2 모델에서 두 기술은 고행자 상위 3기술(방혈·처벌·구제)에 들지 않아 **영웅 총점은 변하지 않는다**(1위, 67). 재기 5레벨 0.0 HP, 인내 4.3 HP. 재기가 체력 40% 조건을 여는 가치는 방혈·구제의 유지율(V-06)에 들어가 있다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### FLA-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 기존 설정·저항 예산 근거에 맞춰 기절/이동40, 출혈60을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `resistances/`
  - 원본: `resistances: .stun 50% .poison 30% .bleed 65% .disease 40% .move 50% .debuff 30% .death_blow 73% .trap 0%`
  - 현재: `resistances: .stun 40% .poison 30% .bleed 60% .disease 40% .move 40% .debuff 30% .death_blow 73% .trap 0%`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 1행; Git 원문 {"commit": "afdddd4fe5ecb3c998a50ef8f79df79d027a69f4", "summary": "FLA-001 고행자 기절·이동 40 + SB-010 방패 파괴자 근거 정정"}
- 기존 주석 원문:
```text
// FLA-001 저항: 기절·이동 50 -> 40(기준값), 출혈 65 -> 60. 기절·이동 기준선은 40이다(R-RES-01; 30 가정으로 30까지 내렸던 것을 정정). 대장간 "스스로 찢음으로써 더욱 견고해집니다"(고통 내성 +)와 거의 벌거벗은 외형(경장 -, P-19)이 상쇄되어 기준값. 30(-10)은 순감소를 뒷받침할 문장이 없다. 출혈 60(+30)은 대표 저항 상한 +30(괴인 중독, 역병 의사 중독, 신비학자 약화)에 맞춤 - 바닐라 +35가 유일한 초과였다
```

### FLA-007 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자 메모의 속도 정상화66889→66778을 기록한다. 구체적인 성장 선택 이유는 기존 메모에 추가 설명이 없어 확인되지 않았다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/flagellant_weapon_2`
  - 원본: `weapon: .name "flagellant_weapon_2" .atk 0% .dmg 4 8 .crit 4% .spd 8 .upgradeRequirementCode 1`
  - 현재: `weapon: .name "flagellant_weapon_2" .atk 0% .dmg 4 8 .crit 4% .spd 7 .upgradeRequirementCode 1`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 10행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/flagellant_weapon_3`
  - 원본: `weapon: .name "flagellant_weapon_3" .atk 0% .dmg 5 10 .crit 5% .spd 8 .upgradeRequirementCode 2`
  - 현재: `weapon: .name "flagellant_weapon_3" .atk 0% .dmg 5 10 .crit 5% .spd 7 .upgradeRequirementCode 2`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `weapon/flagellant_weapon_4`
  - 원본: `weapon: .name "flagellant_weapon_4" .atk 0% .dmg 5 11 .crit 6% .spd 9 .upgradeRequirementCode 3`
  - 현재: `weapon: .name "flagellant_weapon_4" .atk 0% .dmg 5 11 .crit 6% .spd 8 .upgradeRequirementCode 3`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 12행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
//속도 정상화 66889 -> 66778
```

### FLA-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 아군 지속 회복과 자기 출혈 비용을 레벨별로 맞추고 지속3턴을 유지한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/reclaim`
  - 원본: `combat_skill: .id "reclaim" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Healdot 1" "Flag Self Wound 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "reclaim" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "RB FLA Flag Healdot 1" "Flag Self Wound 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "reclaim" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Healdot 2" "Flag Self Wound 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "reclaim" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "RB FLA Flag Healdot 2" "Flag Self Wound 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "reclaim" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Healdot 3" "Flag Self Wound 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "reclaim" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "RB FLA Flag Healdot 3" "Flag Self Wound 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "reclaim" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Healdot 4" "Flag Self Wound 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "reclaim" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "RB FLA Flag Healdot 4" "Flag Self Wound 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "reclaim" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Healdot 5" "Flag Self Wound 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "reclaim" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "RB FLA Flag Healdot 5" "Flag Self Wound 5" .is_stall_invalidating false`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 48행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Healdot 1`
- 원본: `effect: .name "Flag Healdot 1" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 2 .duration 2	.on_hit true .on_miss true`
- 현재: `effect: .name "Flag Healdot 1" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 112행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-005 재기 1레벨: 턴당 회복 = 자해 출혈 턴당(3), 지속 3 고정. 아군 최대 체력 대비 32~39%로 전 레벨 일정(현재 17~28% 들쭉날쭉), 파티 순 체력 전 레벨 0 이상
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Healdot 2`
- 원본: `effect: .name "Flag Healdot 2" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 2 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "Flag Healdot 2" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 117행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-005 재기 2레벨: 턴당 회복 = 자해 출혈 턴당(3), 지속 3 고정. 아군 최대 체력 대비 32~39%로 전 레벨 일정(현재 17~28% 들쭉날쭉), 파티 순 체력 전 레벨 0 이상
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Healdot 3`
- 원본: `effect: .name "Flag Healdot 3" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 2	.on_hit true .on_miss true`
- 현재: `effect: .name "Flag Healdot 3" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 122행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-005 재기 3레벨: 턴당 회복 = 자해 출혈 턴당(4), 지속 3 고정. 아군 최대 체력 대비 32~39%로 전 레벨 일정(현재 17~28% 들쭉날쭉), 파티 순 체력 전 레벨 0 이상
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Healdot 4`
- 원본: `effect: .name "Flag Healdot 4" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "Flag Healdot 4" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 127행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-005 재기 4레벨: 턴당 회복 = 자해 출혈 턴당(4), 지속 3 고정. 아군 최대 체력 대비 32~39%로 전 레벨 일정(현재 17~28% 들쭉날쭉), 파티 순 체력 전 레벨 0 이상
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Healdot 5`
- 원본: `effect: .name "Flag Healdot 5" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "Flag Healdot 5" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 5 .duration 3	.on_hit true .on_miss true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 132행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-005 재기 5레벨: 턴당 회복 = 자해 출혈 턴당(5), 지속 3 고정. 아군 최대 체력 대비 32~39%로 전 레벨 일정(현재 17~28% 들쭉날쭉), 파티 순 체력 전 레벨 0 이상
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Healdot 1`
- 원본 (Flag Healdot 1): `effect: .name "Flag Healdot 1" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 2 .duration 2	.on_hit true .on_miss true`
- 현재: `effect: .name "RB FLA Flag Healdot 1" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// edited vanilla effect (from dlc/580100_crimson_court/features/flagellant/effects/flagellant.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Healdot 2`
- 원본 (Flag Healdot 2): `effect: .name "Flag Healdot 2" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 2 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "RB FLA Flag Healdot 2" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Healdot 3`
- 원본 (Flag Healdot 3): `effect: .name "Flag Healdot 3" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 2	.on_hit true .on_miss true`
- 현재: `effect: .name "RB FLA Flag Healdot 3" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Healdot 4`
- 원본 (Flag Healdot 4): `effect: .name "Flag Healdot 4" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 3 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "RB FLA Flag Healdot 4" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Healdot 5`
- 원본 (Flag Healdot 5): `effect: .name "Flag Healdot 5" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 4 .duration 3	.on_hit true .on_miss true`
- 현재: `effect: .name "RB FLA Flag Healdot 5" .target "target" .curio_result_type "positive" .chance 100% .dotHpHeal 5 .duration 3	.on_hit true .on_miss true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}

### FLA-006 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 자기 스트레스 부담을 고정4로 줄여 광대 외 스트레스 회복 역할을 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/endure`
  - 원본: `combat_skill: .id "endure" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 1" "Flag Self Stress 1" "Flag Endure Speed Buff 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "endure" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 1" "RB FLA Flag Self Stress 1" "Flag Endure Speed Buff 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "endure" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 2" "Flag Self Stress 2" "Flag Endure Speed Buff 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "endure" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 2" "RB FLA Flag Self Stress 2" "Flag Endure Speed Buff 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "endure" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 3" "Flag Self Stress 3" "Flag Endure Speed Buff 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "endure" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 3" "RB FLA Flag Self Stress 3" "Flag Endure Speed Buff 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "endure" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 4" "Flag Self Stress 4" "Flag Endure Speed Buff 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "endure" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 4" "RB FLA Flag Self Stress 4" "Flag Endure Speed Buff 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "endure" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 5" "Flag Self Stress 5" "Flag Endure Speed Buff 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "endure" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .self_target_valid false .launch 1234 .target @1234 .is_crit_valid True  .effect "Flag Steal Stress 5" "RB FLA Flag Self Stress 5" "Flag Endure Speed Buff 5" .is_stall_invalidating false`
- 출처: `heroes/flagellant/flagellant.info.darkest`, 주석 추가 전 65행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Self Stress 1`
- 원본: `effect: .name "Flag Self Stress 1" .target "performer" .curio_result_type "negative" .chance 100% .stress 10	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "Flag Self Stress 1" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 159행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-006 인내 1레벨: 자기 스트레스 10 -> 4 고정. 순회복 0 -> 6, 광대 격려의 선율보다 항상 2 낮게. 회복량 10~14(공식 하향값)는 유지
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Self Stress 2`
- 원본: `effect: .name "Flag Self Stress 2" .target "performer" .curio_result_type "negative" .chance 100% .stress 9	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "Flag Self Stress 2" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 166행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-006 인내 2레벨: 자기 스트레스 9 -> 4 고정. 순회복 2 -> 7, 광대 격려의 선율보다 항상 2 낮게. 회복량 10~14(공식 하향값)는 유지
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Self Stress 3`
- 원본: `effect: .name "Flag Self Stress 3" .target "performer" .curio_result_type "negative" .chance 100% .stress 8	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "Flag Self Stress 3" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 173행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-006 인내 3레벨: 자기 스트레스 8 -> 4 고정. 순회복 4 -> 8, 광대 격려의 선율보다 항상 2 낮게. 회복량 10~14(공식 하향값)는 유지
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Self Stress 4`
- 원본: `effect: .name "Flag Self Stress 4" .target "performer" .curio_result_type "negative" .chance 100% .stress 7	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "Flag Self Stress 4" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 180행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-006 인내 4레벨: 자기 스트레스 7 -> 4 고정. 순회복 6 -> 9, 광대 격려의 선율보다 항상 2 낮게. 회복량 10~14(공식 하향값)는 유지
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Flag Self Stress 5`
- 원본: `effect: .name "Flag Self Stress 5" .target "performer" .curio_result_type "negative" .chance 100% .stress 6	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "Flag Self Stress 5" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `heroes/flagellant/flagellant.effects_edit.txt`, 주석 추가 전 187행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// FLA-006 인내 5레벨: 자기 스트레스 6 -> 4 고정. 순회복 8 -> 10, 광대 격려의 선율보다 항상 2 낮게. 회복량 10~14(공식 하향값)는 유지
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Self Stress 1`
- 원본 (Flag Self Stress 1): `effect: .name "Flag Self Stress 1" .target "performer" .curio_result_type "negative" .chance 100% .stress 10	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "RB FLA Flag Self Stress 1" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 기존 주석 원문:
```text
// edited vanilla effect (from dlc/580100_crimson_court/features/flagellant/effects/flagellant.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Self Stress 2`
- 원본 (Flag Self Stress 2): `effect: .name "Flag Self Stress 2" .target "performer" .curio_result_type "negative" .chance 100% .stress 9	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "RB FLA Flag Self Stress 2" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Self Stress 3`
- 원본 (Flag Self Stress 3): `effect: .name "Flag Self Stress 3" .target "performer" .curio_result_type "negative" .chance 100% .stress 8	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "RB FLA Flag Self Stress 3" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 19행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Self Stress 4`
- 원본 (Flag Self Stress 4): `effect: .name "Flag Self Stress 4" .target "performer" .curio_result_type "negative" .chance 100% .stress 7	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "RB FLA Flag Self Stress 4" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 21행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB FLA Flag Self Stress 5`
- 원본 (Flag Self Stress 5): `effect: .name "Flag Self Stress 5" .target "performer" .curio_result_type "negative" .chance 100% .stress 6	.on_hit true .on_miss false	.queue true`
- 현재: `effect: .name "RB FLA Flag Self Stress 5" .target "performer" .curio_result_type "negative" .chance 100% .stress 4	.on_hit true .on_miss false	.queue true`
- 출처: `effects/rebalance_flagellant.effects.darkest`, 주석 추가 전 23행; Git 원문 {"commit": "e45819b3d49885514d861ecb697f87b8e5707742", "summary": "FLA-005 재기 회복 일관화 + FLA-006 인내 자기 스트레스 4 고정"}

### FLA-008 인내: 자기 스트레스 4 고정 → 4/5/6/7/8 (2026-10-17)
- 상태: 적용 (제작자 결정, 커스텀·창작마당 공통)
- 근거: FLA-006(4 고정)은 2018 공식 하향(바닐라 10/9/8/7/6, 1렙 순회복 0)을 출시 이상으로 되돌려 P-06과 충돌했다(창작마당 감사 X). 회복 10~14는 그대로 두고 자기 스트레스를 레벨마다 올려 순회복을 매 레벨 6으로 고정 — 저레벨부터 쓸 만한 스트레스 힐러(G-05)는 유지하면서 5렙 순회복은 바닐라 8보다 낮다.


### FLA-009 인내: 자기 속도 강화 제거, 순수 스트레스 회복 (2026-10-21)
- 상태: 적용 (제작자 결정 "고행자 스트레스 회복에 속도 증가 없애고 순수 스트레스 회복 기술로")
- 변경: 효과 목록에서 `Flag Endure Speed Buff 1~5`(자기 속도 +1/1/2/2/3) 제거. 아군 스트레스 회복 10~14와 자기 스트레스 4~8(FLA-008)은 그대로.


### FLA-010 재기: 회복 2/2/3/3/4 x 3턴, 자해 출혈 3/4/5/6/7 x 2턴 (FLA-005 철회) (2026-10-21)
- 상태: 적용 (제작자 결정 "B가 맞고", 자해 출혈은 처음 "5/5/6/6/7 2턴" -> "34567로 하자, 레벨 오를 때마다 뭔가는 변해야")
- 근거: FLA-005의 1렙 3x3=9는 게임 최대 단일 아군 회복(성녀 신성한 은총 5)이었고, 자해 출혈을 대가로 계산했으나 고행자에게 출혈은 체력 40%를 만들어 구제·방혈을 여는 이득이다. 지속 3턴은 유지하고 회복량은 바닐라로(5렙 12 = 바닐라). 자해 출혈은 2턴에 몰아 40%에 빨리 도달하고(총 6/8/10/12/14), 매 레벨 1씩 올라 업그레이드마다 무언가가 바뀐다. 확률(120~160%)은 유지: 출혈 저항 장신구를 끼면 재기를 순수 회복기로 쓰는 운용을 남긴다 [제작자].
- 모델 메모: 강함 모델은 지속 회복 틱을 전부 센다(전투 종료로 사라지는 틱 할인 없음) — 지속 피해(0.90/0.40)와 같은 할인 필요.

### FLA-011 인내: 아군 스트레스 회복 10~14 -> 12~16 (2026-10-21)
- 상태: 적용 (제작자 결정 "인내 회복 상향")
- 근거: FLA-009로 속도 버프를 뺀 보상. 자기 스트레스 4~8을 빼면 순회복 매 레벨 8. 광대 격려의 선율(8~12, 자기 비용 없음)과 1렙 순회복이 같다. 고행자는 장신구로 운용이 갈린다(받는 스트레스 감소 장신구 + 인내 = 스트레스 힐러) [제작자].


### FLA-012 고통: 아군 약화 해제 추가 (2026-10-21)
- 상태: 적용 (제작자 결정 "고통이 약화도 가져오자")
- 변경: 1~5렙 효과 목록에 바닐라 `Cure Debuffs`(대상 약화 해제) 추가. 출혈·중독 가져오기·자기 표식·투지는 그대로.
- 근거: P-19 이름(고통 = 아군의 고통을 대신 짊어진다). 엔진은 출혈·중독만 "가져오기"(steal_buff_stat_type)를 지원해, 다른 약화는 해제로 구현. 후열 아군 정화가 비어 있던 자리(후열 빈 역할 조사 10-21)도 채운다.
- 미결: 속도 버프 추가 여부와 수치(제작자: "속도 넣는 건 맞는 것 같은데 1,2는 너무 적다, 계속 생각").

### FLA-013 고통: 자기 속도 +3/3/4/4/5 (3턴) (2026-10-21)
- 상태: 적용 (제작자 결정 "속도 33445가 더 낫지 않니? 아예 선턴 잡게")
- 근거: 고통으로 아군의 출혈·중독을 가져오면 체력이 40%로 내려간다. 다음 라운드에 먼저 움직여 구제·방혈을 적보다 먼저 쓰게 한다. 지속 피해는 속도와 상관없이 라운드당 한 번 들어가 손해가 없다. 행동 순서는 속도 + 1~8 무작위라 선턴을 보장하지는 못하고 확률을 크게 올린다.
