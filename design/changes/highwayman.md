# 노상강도 (highwayman) 변경 항목

바닐라 수치: `heroes/highwayman/highwayman.vanilla.txt`

---

### HWY-000 방향: 가정과 무관한 최상위 → "강함" 구간으로
- 상태: 방향
- 목표: G-01, G-02
- 사용자 요청 (원문):
  > 노상강도 적정 조정안 얘기해봐
- 근거 (`analysis/hero_power.md` 8~10절):
  - 가격표 초과 합 +172. 20명 중 1위이고, 2위 도굴꾼은 +81이다.
  - 순위 모델에서 가정을 어떻게 바꿔도 1~3위를 유지하는 유일한 영웅이다.
  - 영거리 사격 +51은 결투가의 진격 순환으로 자리 이탈 비용이 상쇄된다.
  - 정맥 절개 +43은 역병 의사 절개에 약화 2개를 더한 형태다.
  - 포도탄 발사는 과대 판정을 철회했다(명중·치명타로 값을 치름).
- 목표 위치: 순위 5위 전후, 보수적 가정에서 4위. 현상금 사냥꾼 버프 기준선(조건부 19~21)을 넘는 순환 피해를 주지 않는다.
- 원칙: P-09 최소 변경. 기술 ID·정체성(전·후열 전환, 반격, 출혈 연계) 유지.

### HWY-001 영거리 사격: 피해 보정 +50% → +30% (제안)
- 상태: 제안 (권장)
- 분류: 원칙복원 (가격표 R-TRADE-01)
- 변경안: 1~5레벨 `.dmg 50%` → `.dmg 30%`
- 근거:
  - 1열 전용 단일 기술 중 +50은 유일하다(야만인 출혈 +20에 자기 약화, 나머지 0).
  - 가격표 +51 → +31. 1열 전용 단일 기술 중 최고 피해는 여전히 유지된다.
- 결과: 5레벨 기대 피해 17.3 → 15.0, 진격과의 2턴 순환 13.0 → 11.9. 순위 3위 → 5위.
- 기각한 대안: 명중 −10(원거리 명중 법칙 기대치 약 90보다 더 깎음), 결투가의 진격 사용 열 축소(정체성 훼손).

### HWY-002 정맥 절개: 속도 약화 제거 (제안)
- 상태: 제안 (권장)
- 분류: 원칙복원 (가격표)
- 변경안: 1~5레벨 `.effect`에서 `"HW Open Vein SPD Debuff N"` 제거. 출혈과 출혈 저항 약화는 유지한다.
- 근거:
  - 약화 2개로 가격표 +43이다. 약화 1개를 빼면 +24가 된다.
  - 명중 95는 근접 명중·피해 교환 법칙(피해 −15 ≈ 명중 +6)상 적정하므로 명중은 건드리지 않는다.
- 결과: 모델 가치 15.6 → 15.3 (작음). 가격 정상화가 주목적이다.

### HWY-003 추적탄: 피해 보정 −80% → −60% (제안)
- 상태: 제안
- 분류: 기술 다양성 보상 (G-02)
- 변경안: 1~5레벨 `.dmg -80%` → `.dmg -60%`
- 근거:
  - 가치 1.9로 노상강도 기술 중 최하위다. 가격표 −28 과소이며, 조정 후 −8이 된다.
  - 전투당 1회 제한이 있어 순위 영향이 없다. HWY-001과 묶어 하향 체감을 줄인다.

### 패키지 권장: HWY-001 + HWY-002 + HWY-003
- 순위 3위 → 5위, 보수적 가정 1위 → 4위.
- 보류: 사악한 칼질 +23(상위 기술이 아니어서 실제 강함 기여 작음), 결투가의 진격 +19(순환의 절반, HWY-001 테스트 후 재검토).

### HWY-001 P-12 재검토 (2026-09-16)
- 계기: P-12(사용감 보존)를 원칙으로 추가하면서 영거리 사격 조정안을 다시 봤다.
- 사용자 의견 (원문):
  > 기존 사용감 자체를 크게 해치지 않는 게 목적이라고 아예 스킬 자체를 변경시키면 이질감이 들잖아 사용자 입장에서 그래서 유저 체감을 고려한다는 게 메인이지
- 선택지 (제작자 결정 대기)

  | 안 | 내용 | 5레벨 순환 피해 | 체감 |
  |---|---|---|---|
  | A | 피해 +50 유지, 전투당 2회 제한 | 필살기 1~2회 17.3, 순환 불가 | 한 방 감각 유지, 반복만 차단 |
  | B | 피해 +50 유지, 자기 후퇴 1칸 → 2칸 | 순환 2턴 → 3턴 | 위치 관리 부담으로 전환 |
  | C (기존 HWY-001) | 피해 +50 → +30 | 15.0, 2턴 평균 11.9 | 수치는 완만, 필살기 느낌 감소 |
  | D | 결투가의 진격 전진 1칸 → 0칸 | 순환 차단 | 정체성 훼손, 기각 |
- 판단 보류. P-12는 "빈도 제한"이 아니라 "이질감 최소화"가 기준이므로, A·B·C 중 무엇이 덜 이질적인지는 제작자가 정한다.

### HWY-004 / HWY-005 추적탄 ↔ 결투가의 진격: 반격과 자기 강화를 맞바꿈
- 상태: 적용 (사용자 요청 2026-09-27)
- 분류: 의도적 조정 / 구조 변경
- 목표: G-02(기술 다양성), G-03(열 다양성)
- 사용자 의도 (원문)
  > 원거리 빌드도 사용가능하게 변경, 근거리만 올리면 되는 기존 설계를 너프로 재조정
  > 앞으로 전진하면서 결투가가 되는거지 그러면서 버프 받는거지. 테이크에임은 에임조준하면서 반격가능성을 갖추는 거고
  > 나는 전진공격하는 데 왜 반격이 켜져야해? 에임조준하면서 상대를 관찰하고 간파할 때 반격이 켜지는 게 맞지
  > 테이크에임의 버프가 전투당 1번이어서 되게 버프량이 과해
- 변경
  - **HWY-004 추적탄**: `Tracking Buff 1~5` → **`Hwy Riposte 1~5`**, **전투당 1회 제한 제거**, 피해 −80% → **−60%**. Destealth 유지
  - **HWY-005 결투가의 진격**: `Hwy Riposte 1~5` → **`RB HWY Tracking Buff 1~5`**(축소판), **1레벨 명중 90 유지**, 피해 −20% → **−40%**
  - **Tracking Buff 축소**: 명중 6~10 → **3~5**, 치명타 4~8 → **3~5**, 피해 12~20% → **6~10%**
- 근거
  1. **반격이 근접 기술에만 있어 원거리 빌드가 성립하지 않았다.** 결투가의 진격은 자기 전진 1칸이 붙어 있어, 3열 원거리 빌드에서 반격을 켜면 2열로 밀려나 빌드가 깨진다. 추적탄은 **사용 4·3·2·1 전 열, 자기 이동 없음**이라 자리를 지킨 채 반격을 켤 수 있다.
  2. **아트 정합성(P-19)**: 조준하며 상대를 관찰·간파 → 받아치기(반격), 앞으로 전진하며 자세를 잡음 → 자기 강화. 모션의 인과가 교환 후에 더 맞는다.
  3. **전투당 1회 제한 해제의 대가로 버프를 축소했다.** 제한 제거 = +15%p 이득, 버프 스탯 합 48%p → 25%p로 −23%p. 비교: 야만인 아드레날린 분출은 명중 +10·피해 +30%·디버프 해제를 **제한 없이** 준다(스탯 50%p). 노상강도는 강함 3위라 그보다 낮게 잡았다.
  4. 추적탄 피해 −60%는 "막타를 치면서 반격을 켠다"는 용법을 위한 값이다. 기대 피해 **2.44 → 4.87**(2배).
     - 반격 획득(+47) − 자버프 상실(−22) + 전투당 1회 제거(+15) + 피해 +20 = **+60**. 잔차 +0.6 → **+60.6**.
     - 노상강도 총량이 다른 조정으로 −17 순감 상태였으므로, 이 +5가 중립에 가깝게 만든다.
- 총량 (P-11)

  | 기술 | 변경 전 | 변경 후 |
  |---|---|---|
  | 추적탄 | +0.6 | +55.6 |
  | 결투가의 진격 | +77.8 | +22.3 |
  | **합** | **78.4** | **77.9** |

  거의 완전 중립이다. 편차만 77 → 33으로 줄었다.
- 검증: 원거리 빌드(3열 상주 + 추적탄 반격 + 권총 사격 + 포도탄)가 실제로 성립하는지. 반격이 원거리 기술에서 켜져도 근접 반격처럼 작동하는지(**검증 전**)

### HWY-006 정맥 절개: 치명타 대폭 상향 + 피해 하향
- 상태: 적용 (사용자 요청 2026-09-27) → 피해는 HWY-019 −25% → HWY-020 −30%(현재 데이터). 치명 1렙 +8, 명중 1렙 95 유지.
- 분류: 의도적 조정
- 목표: G-02
- 변경: **1레벨 치명타 보정 +0 → +8**(실제 치명타 13% → 21%), 피해 −15% → **−40%**. 1레벨 명중 95와 약화 2개는 유지
- **대응 기술: 도굴꾼 맹독 다트** [사용자 지정]

  | | 맹독 다트 | 정맥 절개 (변경 후) |
  |---|---|---|
  | 종류 | 원거리 | 근접 |
  | 1렙 명중 | 95 | 95 |
  | 피해 보정 | −60% | **−40%** |
  | 1렙 치명타 보정 | +7.5 (실제 13.5%) | **+8 (실제 13%)** |
  | 대상 열 | **1·2·3·4** | **1·2** |
  | 지속 피해 총량 | 중독 12 | 출혈 12 |
  | 약화 | 1개 | **2개** |
  | 자버프 | 명중 +10 | — |

- 근거
  1. **지속 피해 총량이 12로 완전히 같고 명중도 같다.** 짝으로 설계된 기술이다.
  2. 맹독 다트가 더 받는 것을 환산하면 원거리 +18, 대상 열 2개 +10, 자버프 +10, 치명타 +4 = **+42**. 정맥 절개가 더 받는 것은 약화 1개 **+19**. 순 **+23**이므로 정맥 절개의 피해 보정이 23%p 높아야 대등하다(−60 + 23 = −37%).
  3. **−40%로 한 이유 [사용자]**: 도굴꾼은 전 열을 때리는데 노상강도는 1·2열만 때린다. 대등(−37%)보다 조금 더 유리해야 한다.
  4. **명중 95 유지**: 지속 피해 기술 23개의 1레벨 명중 분포는 85가 8개, 90이 4개, **95가 10개(최빈)**다. 명중 95는 원칙에 맞다. R-TRADE-02의 "효과는 명중을 사고 피해를 크게 낸다"에 해당한다. 명중 95인 지속 피해 기술 10개의 피해 보정 중앙값은 **−71%**이고, 변경 전 −15%는 아래에서 두 번째였다.
  5. **치명타 +8의 근거**: 지속 피해 기술 중 최상위는 광대 저며내기 +8, 맹독 다트 +7.5다. +8은 그 선을 지키며 맹독 다트와 나란히 선다. 모션(정맥을 긋는 정밀한 칼질)에도 맞다(P-21 예외).
  6. **약화 2개 유지**: P-20. 약화 확률을 올리는 장신구가 있어 뺄 수 없다.
  7. **치명타 상향은 출혈 상향이기도 하다**(R-CMB-08). 치명타 시 출혈 지속 3턴 → 5턴이므로 총량 12 → 20. 치명타 21%면 5회 중 1회다. 출혈 기대 총량 12.7 → **13.4**.
- 영향: 직접 기대 피해 10.35 → 6.50, 출혈 포함 합 23.1 → 19.9. 잔차 +79.4 → **+51.6**

### HWY-007 포도탄 발사: 명중 상향 + 피해 하향 (견제기로 통일)
- 상태: 적용 (사용자 요청 2026-09-27) → 피해는 HWY-020에서 −60%(현재 데이터). 명중 1렙 90 유지.
- 분류: 의도적 조정
- 변경: **1레벨 명중 90(표준)**, 피해 −75% → **−70%**. 치명타 보정 −9는 **유지**
  - 주: 제작자가 앞서 1레벨 명중 75 → 95, 피해 −50% → −75%로 바꿔둔 상태에서 조정했다.
- 근거
  1. **치명타 −9는 설계된 값이다 [사용자]**(P-21). 포도탄의 목적은 자기가 딜하는 것이 아니라 **취약(대상이 받는 치명타 +8%)을 걸어 반격과 다른 기술의 치명타를 여는 것**이다. 두 번 쏘면 세 번째에 치명타가 터지도록 의도된 구조다. 따라서 치명타는 건드리지 않고 명중·피해로만 조정했다.
  2. **−70%인 이유**: 같은 구조의 견제기인 석궁사수 제압 사격·총사 연막탄은 **2대상에 −80%**다. 포도탄은 **3대상**이라 대상당 화력이 더 낮을 이유가 없다.
  3. 1레벨 명중 85는 광역 공격의 평균 수준이다(변경 전 75는 나병환자 가르기·토막치기와 함께 전체 최하위였다).
- 영향: 적중률 70% → 80%, 3대상 기대 피해 13.6 → 9.3. 잔차 +26.5 → +27.5 (거의 중립 교환)

### 노상강도 총량 점검 (HWY-004~007 적용 후)

| 기술 | 변경 전 | 변경 후 |
|---|---|---|
| 추적탄 | +0.6 | +55.6 |
| 결투가의 진격 | +77.8 | +52.3 |
| 정맥 절개 | +79.4 | +51.6 |
| 포도탄 발사 | +26.5 | +27.5 |
| 영거리 사격 | +99.6 | +99.6 |
| 사악한 칼질 | +37.6 | +37.6 |
| 권총 사격 | +82.4 | +82.4 |
| **합계** | **+403.9** | **+406.6** |

총량은 +2.7로 거의 중립이고, **편차가 99 → 72로 줄었다.** 네 기술이 서로를 상쇄한다 — 추적탄이 얻은 것을 결투가의 진격과 정맥 절개가 나눠 낸다.

### 장신구 제약 확인 — 원거리 명중 +15, 그리고 "낮은 명중은 장신구 전제"라는 해석의 기각 (2026-09-27)

노상강도 전용 **`poisoning_buckle`**(독 바른 버클)에 `TRINKET_rangedonly_ACC_B3` = **원거리 기술 명중 +15**가 붙어 있다. 같은 값의 `ancestors_pistol`(조상의 권총)도 있다.

**한때 세웠던 가설**: 1레벨 명중의 설계 천장이 95(공격 기술 104개 중 95 이하가 97개, 95가 최빈 37개)이므로, 장신구 +15를 천장 안에서 다 쓰려면 기술의 1레벨 명중이 80이어야 한다. 원거리 기술의 낮은 명중은 장신구를 전제한 설계다.

**이 가설은 기각한다.** 근거는 몬스터 회피 분포다.

영웅 등급 일반 몬스터 85종: 회피 **중앙 25% / 평균 26% / 상위 25%는 31.25% / 상위 10%는 36.25% / 최대 62.5%(까마귀)**.

| 1레벨 명중 | 5레벨 + 장신구 | 명중률 95% 상한에 닿는 적 | **명중이 낭비되지 않는 적** |
|---|---|---|---|
| 75 | 110 | 5% | **95%** |
| 80 | 115 | 7% | **93%** |
| 85 | 120 | 51% | **49%** |
| 90 | 125 | 74% | 26% |
| 95 | 130 | 88% | 12% |

- **1레벨 명중 85여도 절반(51%)에서만 상한에 닿는다.** "85면 딱 맞다"는 계산은 **중앙값 몬스터 하나만 놓고 본 것**이었다(Claude 오류, 제작자 지적으로 정정).
- **장신구 없이는(5레벨 = 1레벨 + 20) 1레벨 명중 95여도 상한에 닿는 적이 7%뿐이다.** 명중은 거의 항상 값어치를 한다.

| 1레벨 명중 | 5레벨 명중 | 상한 도달 | 평균 적중률 |
|---|---|---|---|
| 75 | 95 | 5% | 69.0% |
| 85 | 105 | 5% | 78.5% |
| 90 | 110 | 5% | 83.3% |
| 95 | 115 | 7% | 88.1% |

**후열 몬스터 회피가 특별히 높은가**: 중앙값 차이는 작다(전열 선호 21.25% / 최강 공격이 3·4열에서만 나오는 종 25.75%). 다만 **회피 30% 이상인 22종(전체의 26%)** 중 상당수가 실전에서 후열에 선다 — 마녀·광인 41.25%, 거미 계열 36.25%, 까마귀 62.5%. 이런 적에게는 명중이 아무리 높아도 낭비가 없다(까마귀 상대: 명중 120 − 62.5 = 적중률 57.5%).

**결론 — 원거리 명중을 일괄로 낮추지 않는다.**

1. `poisoning_buckle`은 노상강도 장신구 6개 중 하나이고, 나머지는 명중을 주지 않는다. `dodgy_sheath`는 오히려 원거리 명중 **−10**이다. 특정 장신구 하나를 전제로 기본 수치를 낮추면 **그 장신구를 안 낀 대다수 상황이 나빠진다.**
2. 원 개발사가 명중 75~80으로 둔 것은 장신구 전제가 아니라 **"이 기술은 잘 안 맞는다"는 설계**로 읽는 게 맞다. 포도탄이 산탄이고 견제기라서 치명타도 −9인 것과 같은 맥락이다.
3. **P-20의 올바른 적용 방향은 반대다.** "장신구가 명중을 올려주니 기본을 낮추자"가 아니라, **"기본을 낮추면 그 장신구가 필수가 되어 선택지가 줄어든다"**이다. 장신구는 선택을 넓혀야지 강제하면 안 된다.

**따라서 포도탄 1레벨 명중 90 / 권총 사격 90 / 영거리 사격 90을 그대로 유지한다.** 권총 사격은 표식 피해를 포함해 손대지 않는다 [제작자 결정].


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### HWY-008 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 전열 근접 선택지를 남기면서 사용자의 최신 표준 명중90/피해0 결정을 기록한다. 예전 피해+15 주석은 역사 기록이다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/wicked_slice`
  - 원본: `combat_skill: .id "wicked_slice" .level 0 .type "melee" .atk 85% .dmg 15% .crit 5% .launch 321 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_slice" .level 0 .type "melee" .atk 90% .dmg 15% .crit 5% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_slice" .level 1 .type "melee" .atk 90% .dmg 15% .crit 6% .launch 321 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_slice" .level 1 .type "melee" .atk 95% .dmg 15% .crit 6% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_slice" .level 2 .type "melee" .atk 95% .dmg 15% .crit 7% .launch 321 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_slice" .level 2 .type "melee" .atk 100% .dmg 15% .crit 7% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_slice" .level 3 .type "melee" .atk 100% .dmg 15% .crit 8% .launch 321 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_slice" .level 3 .type "melee" .atk 105% .dmg 15% .crit 8% .launch 21 .target 12 .is_crit_valid True `
  - 원본: `combat_skill: .id "wicked_slice" .level 4 .type "melee" .atk 105% .dmg 15% .crit 9% .launch 321 .target 12 .is_crit_valid True `
  - 현재: `combat_skill: .id "wicked_slice" .level 4 .type "melee" .atk 110% .dmg 15% .crit 9% .launch 21 .target 12 .is_crit_valid True `
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 30행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// HWY-008 wicked_slice: 사용 321 -> 21(근접 사거리), 명중 1렙 85 -> 90, dmg 0% -> +15%(바닐라 원복)
```
- 기존 주석 원문:
```text
//표준으로 바꿈 데미지 보정 15 -> 0
```

### HWY-009 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자 원거리 명중90 결정과 MARK-01의 서브 표식 피해 재배분을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/pistol_shot`
  - 원본: `combat_skill: .id "pistol_shot" .level 0 .type "ranged" .atk 85% .dmg -15% .crit 7.5% .launch 432 .target 234 .is_crit_valid True  .effect "HW Pistol Dmg Marked 1" .generation_guaranteed true`
  - 현재: `combat_skill: .id "pistol_shot" .level 0 .type "ranged" .atk 90% .dmg -15% .crit 7.5% .launch 432 .target 234 .is_crit_valid True  .effect "RB HWY HW Pistol Dmg Marked 1" .generation_guaranteed true`
  - 원본: `combat_skill: .id "pistol_shot" .level 1 .type "ranged" .atk 90% .dmg -15% .crit 8.5% .launch 432 .target 234 .is_crit_valid True  .effect "HW Pistol Dmg Marked 2"`
  - 현재: `combat_skill: .id "pistol_shot" .level 1 .type "ranged" .atk 95% .dmg -15% .crit 8.5% .launch 432 .target 234 .is_crit_valid True  .effect "RB HWY HW Pistol Dmg Marked 2"`
  - 원본: `combat_skill: .id "pistol_shot" .level 2 .type "ranged" .atk 95% .dmg -15% .crit 9.5% .launch 432 .target 234 .is_crit_valid True  .effect "HW Pistol Dmg Marked 3"`
  - 현재: `combat_skill: .id "pistol_shot" .level 2 .type "ranged" .atk 100% .dmg -15% .crit 9.5% .launch 432 .target 234 .is_crit_valid True  .effect "RB HWY HW Pistol Dmg Marked 3"`
  - 원본: `combat_skill: .id "pistol_shot" .level 3 .type "ranged" .atk 100% .dmg -15% .crit 10.5% .launch 432 .target 234 .is_crit_valid True  .effect "HW Pistol Dmg Marked 4"`
  - 현재: `combat_skill: .id "pistol_shot" .level 3 .type "ranged" .atk 105% .dmg -15% .crit 10.5% .launch 432 .target 234 .is_crit_valid True  .effect "RB HWY HW Pistol Dmg Marked 4"`
  - 원본: `combat_skill: .id "pistol_shot" .level 4 .type "ranged" .atk 105% .dmg -15% .crit 11.5% .launch 432 .target 234 .is_crit_valid True  .effect "HW Pistol Dmg Marked 5"`
  - 현재: `combat_skill: .id "pistol_shot" .level 4 .type "ranged" .atk 110% .dmg -15% .crit 11.5% .launch 432 .target 234 .is_crit_valid True  .effect "RB HWY HW Pistol Dmg Marked 5"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 39행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
//명중 원거리 표준 90으로 변경 85 -> 90
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HW Pistol Dmg Marked 1`
- 원본: `effect: .name "HW Pistol Dmg Marked 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 25%	.damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "HW Pistol Dmg Marked 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 24행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HW Pistol Dmg Marked 2`
- 원본: `effect: .name "HW Pistol Dmg Marked 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 30%	.damage_high_multiply 30%	.on_hit true .on_miss false`
- 현재: `effect: .name "HW Pistol Dmg Marked 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 45%	.damage_high_multiply 45%	.on_hit true .on_miss false`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 26행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HW Pistol Dmg Marked 3`
- 원본: `effect: .name "HW Pistol Dmg Marked 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 35%	.damage_high_multiply 35%	.on_hit true .on_miss false`
- 현재: `effect: .name "HW Pistol Dmg Marked 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 28행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HW Pistol Dmg Marked 4`
- 원본: `effect: .name "HW Pistol Dmg Marked 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "HW Pistol Dmg Marked 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 55%	.damage_high_multiply 55%	.on_hit true .on_miss false`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 30행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HW Pistol Dmg Marked 5`
- 원본: `effect: .name "HW Pistol Dmg Marked 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 현재: `effect: .name "HW Pistol Dmg Marked 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 32행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// MARK-01 HW Pistol Dmg Marked: 표식 피해 25~50 -> 40~60 (서브 표식 딜러)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY HW Pistol Dmg Marked 1`
- 원본 (HW Pistol Dmg Marked 1): `effect: .name "HW Pistol Dmg Marked 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 25%	.damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB HWY HW Pistol Dmg Marked 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY HW Pistol Dmg Marked 2`
- 원본 (HW Pistol Dmg Marked 2): `effect: .name "HW Pistol Dmg Marked 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 30%	.damage_high_multiply 30%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB HWY HW Pistol Dmg Marked 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 45%	.damage_high_multiply 45%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY HW Pistol Dmg Marked 3`
- 원본 (HW Pistol Dmg Marked 3): `effect: .name "HW Pistol Dmg Marked 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 35%	.damage_high_multiply 35%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB HWY HW Pistol Dmg Marked 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY HW Pistol Dmg Marked 4`
- 원본 (HW Pistol Dmg Marked 4): `effect: .name "HW Pistol Dmg Marked 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 40%	.damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB HWY HW Pistol Dmg Marked 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 55%	.damage_high_multiply 55%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY HW Pistol Dmg Marked 5`
- 원본 (HW Pistol Dmg Marked 5): `effect: .name "HW Pistol Dmg Marked 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 50%	.damage_high_multiply 50%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB HWY HW Pistol Dmg Marked 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 60%	.damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "30e207f78a8342186f06ebafd638d53ded3d8a34", "summary": "MARK-01 표식 피해 재배분: 서브 표식 딜러 상향 + 조련사 하향"}

### HWY-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 필살기 사용감을 남기되 후퇴2칸으로 손쉬운 반복 순환과 특정 고정 조합을 줄인다. 현재 명중90/피해40/밀치기2를 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/point_blank_shot`
  - 원본: `combat_skill: .id "point_blank_shot" .level 0 .type "ranged" .atk 95% .dmg 50% .crit 5% .move 1 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 1A"`
  - 현재: `combat_skill: .id "point_blank_shot" .level 0 .type "ranged" .atk 90% .dmg 40% .crit 5% .move 2 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 2A"`
  - 원본: `combat_skill: .id "point_blank_shot" .level 1 .type "ranged" .atk 100% .dmg 50% .crit 6% .move 1 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 1B"`
  - 현재: `combat_skill: .id "point_blank_shot" .level 1 .type "ranged" .atk 95% .dmg 40% .crit 6% .move 2 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 2B"`
  - 원본: `combat_skill: .id "point_blank_shot" .level 2 .type "ranged" .atk 105% .dmg 50% .crit 7% .move 1 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 1C"`
  - 현재: `combat_skill: .id "point_blank_shot" .level 2 .type "ranged" .atk 100% .dmg 40% .crit 7% .move 2 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 2C"`
  - 원본: `combat_skill: .id "point_blank_shot" .level 3 .type "ranged" .atk 110% .dmg 50% .crit 8% .move 1 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 1D"`
  - 현재: `combat_skill: .id "point_blank_shot" .level 3 .type "ranged" .atk 105% .dmg 40% .crit 8% .move 2 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 2D"`
  - 원본: `combat_skill: .id "point_blank_shot" .level 4 .type "ranged" .atk 115% .dmg 50% .crit 9% .move 1 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 1E"`
  - 현재: `combat_skill: .id "point_blank_shot" .level 4 .type "ranged" .atk 110% .dmg 40% .crit 9% .move 2 0 .launch 1 .target 1 .is_crit_valid True  .effect "Push 2E"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 46행; Git 원문 {"commit": "caa6e47fdf918af3de85869ee82165271fc85979", "summary": "P-20 장신구 고정 제약 + P-21 치명타는 조정 수단 아님"}
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//명중 95, 아무런 패널티 없는 스킬데미지 50, 높은 크리 확률 명백한 사기스킬임 사실 떡너프가 맞으나, 순수 성능 너프를 때리면 유저 체감이 불쾌해짐. "
```
- 기존 주석 원문:
```text
//그래서 연속해서 사용하기 어렵게 변경하고 대신에, 사용 체감 늘리는 부분도 만듦
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//도굴꾼 돌진과 역으로 대칭 도굴꾼으로 앞으로 2칸 전진, 노상은 뒤로 2칸 후퇴. 대신에 상대 밀쳐내기도 2칸으로 버프.    "
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//일단 명중 5 너프, 데미지 10 너프 적용해놓음. 명중 95 -> 90, 딜 50 -> 40   "
```
- 기존 주석 원문:
```text
//방파자 살모사 입맞춤, 스피어랑 너무 찰떡이었음 그래서 사기 빌드가 성녀 광대 노상 실브 이렇게 고정 됐었음 이를 타파하기 위해
```
- 기존 주석 원문:
```text
//영거리 뒤로 2칸 물러나게 바꿈
```

### HWY-007 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 받는 치명 약화의 견제 역할을 보존하고 명중을 높이는 대가로 직접 피해를 낮춘다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/grape_shot_blast`
  - 원본: `combat_skill: .id "grape_shot_blast" .level 0 .type "ranged" .atk 75% .dmg -50% .crit -9% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 1"`
  - 현재: `combat_skill: .id "grape_shot_blast" .level 0 .type "ranged" .atk 90% .dmg -70% .crit -9% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 1"`
  - 원본: `combat_skill: .id "grape_shot_blast" .level 1 .type "ranged" .atk 80% .dmg -50% .crit -8% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 2"`
  - 현재: `combat_skill: .id "grape_shot_blast" .level 1 .type "ranged" .atk 95% .dmg -70% .crit -8% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 2"`
  - 원본: `combat_skill: .id "grape_shot_blast" .level 2 .type "ranged" .atk 85% .dmg -50% .crit -7% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 3"`
  - 현재: `combat_skill: .id "grape_shot_blast" .level 2 .type "ranged" .atk 100% .dmg -70% .crit -7% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 3"`
  - 원본: `combat_skill: .id "grape_shot_blast" .level 3 .type "ranged" .atk 90% .dmg -50% .crit -6% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 4"`
  - 현재: `combat_skill: .id "grape_shot_blast" .level 3 .type "ranged" .atk 105% .dmg -70% .crit -6% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 4"`
  - 원본: `combat_skill: .id "grape_shot_blast" .level 4 .type "ranged" .atk 95% .dmg -50% .crit -5% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 5"`
  - 현재: `combat_skill: .id "grape_shot_blast" .level 4 .type "ranged" .atk 110% .dmg -70% .crit -5% .launch 23 .target ~123 .is_crit_valid True  .effect "Grapeshot Vulnerability 5"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 59행; Git 원문 {"commit": "7c4149ab216433ca9f31d5902c210f525ba467a2", "summary": "HWY 수치 확정: 포도탄 1렙 명중 90, 진격 1렙 90/-40%, 정맥 절개 -40%"}
- 기존 주석 원문:
```text
// HWY-007 grape_shot_blast: 명중 1렙 75 -> 90, dmg -75% -> -70% (치명타 -5 유지 = 설계된 값, P-21)
```
- 기존 주석 원문:
```text
//돌파와 직접 비교 기술 치명타 낮은것과 약화거는 것을 동률이라 보고
```
- 기존 주석 원문:
```text
//명중을 높이는 대신 데미지를 깎겠다. 데미지 깎는 이유 -> 포도탄 반복하면서 치명타 확률만 높이는 편법 배제?
```
- 기존 주석 원문:
```text
//명중 높이는 이유 -> 부가효과가 있으면 명중이 올라간다
```
- 기존 주석 원문:
```text
//데미지 50 -> 70
```

### HWY-004 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 자리 이동 없이 원거리 빌드에서 반격을 켤 수 있도록 자기 강화와 반격의 기술 배치를 바꾼다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/take_aim`
  - 원본: `combat_skill: .id "take_aim" .level 0 .type "ranged" .atk 95% .dmg -80% .crit 0% .per_battle_limit 1 .launch 4321 .target 234 .is_crit_valid True .ignore_stealth true  .effect "Tracking Buff 1" "Destealth"`
  - 현재: `combat_skill: .id "take_aim" .level 0 .type "ranged" .atk 95% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid True .ignore_stealth true  .effect "Hwy Riposte 1" "Destealth"`
  - 원본: `combat_skill: .id "take_aim" .level 1 .type "ranged" .atk 100% .dmg -80% .crit 0% .per_battle_limit 1 .launch 4321 .target 234 .is_crit_valid True .ignore_stealth true  .effect "Tracking Buff 2" "Destealth"`
  - 현재: `combat_skill: .id "take_aim" .level 1 .type "ranged" .atk 100% .dmg -75% .crit 0% .launch 4321 .target 1234 .is_crit_valid True .ignore_stealth true  .effect "Hwy Riposte 2" "Destealth"`
  - 원본: `combat_skill: .id "take_aim" .level 2 .type "ranged" .atk 105% .dmg -80% .crit 0.5% .per_battle_limit 1 .launch 4321 .target 234 .is_crit_valid True .ignore_stealth true  .effect "Tracking Buff 3" "Destealth"`
  - 현재: `combat_skill: .id "take_aim" .level 2 .type "ranged" .atk 105% .dmg -75% .crit 0.5% .launch 4321 .target 1234 .is_crit_valid True .ignore_stealth true  .effect "Hwy Riposte 3" "Destealth"`
  - 원본: `combat_skill: .id "take_aim" .level 3 .type "ranged" .atk 110% .dmg -80% .crit 0.5% .per_battle_limit 1 .launch 4321 .target 234 .is_crit_valid True .ignore_stealth true  .effect "Tracking Buff 4" "Destealth"`
  - 현재: `combat_skill: .id "take_aim" .level 3 .type "ranged" .atk 110% .dmg -75% .crit 0.5% .launch 4321 .target 1234 .is_crit_valid True .ignore_stealth true  .effect "Hwy Riposte 4" "Destealth"`
  - 원본: `combat_skill: .id "take_aim" .level 4 .type "ranged" .atk 115% .dmg -80% .crit 1% .per_battle_limit 1 .launch 4321 .target 234 .is_crit_valid True .ignore_stealth true  .effect "Tracking Buff 5" "Destealth"`
  - 현재: `combat_skill: .id "take_aim" .level 4 .type "ranged" .atk 115% .dmg -75% .crit 1% .launch 4321 .target 1234 .is_crit_valid True .ignore_stealth true  .effect "Hwy Riposte 5" "Destealth"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 73행; Git 원문 {"commit": "0000000000000000000000000000000000000000", "summary": "Version of heroes/highwayman/highwayman.info.darkest from heroes/highwayman/highwayman.info.darkest"}
- 기존 주석 원문:
```text
// HWY-004 take_aim: Hwy Riposte, 전투당 1회 제거, dmg -80% -> -75% ->중보병꺼랑 데미지 바꿈 대상 234 -> 1234
```

### HWY-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 반격을 추적탄으로 옮기고 전진 공격은 축소 자기 강화를 맡긴다. 현재 수치와 역사 속 후보를 구분한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/duelist_advance`
  - 원본: `combat_skill: .id "duelist_advance" .level 0 .type "melee" .atk 90% .dmg -20% .crit 5% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "Hwy Riposte 1"`
  - 현재: `combat_skill: .id "duelist_advance" .level 0 .type "melee" .atk 95% .dmg -20% .crit 5% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "RB HWY Tracking Buff 1"`
  - 원본: `combat_skill: .id "duelist_advance" .level 1 .type "melee" .atk 95% .dmg -20% .crit 6% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "Hwy Riposte 2"`
  - 현재: `combat_skill: .id "duelist_advance" .level 1 .type "melee" .atk 100% .dmg -20% .crit 6% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "RB HWY Tracking Buff 2"`
  - 원본: `combat_skill: .id "duelist_advance" .level 2 .type "melee" .atk 100% .dmg -20% .crit 7% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "Hwy Riposte 3"`
  - 현재: `combat_skill: .id "duelist_advance" .level 2 .type "melee" .atk 105% .dmg -20% .crit 7% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "RB HWY Tracking Buff 3"`
  - 원본: `combat_skill: .id "duelist_advance" .level 3 .type "melee" .atk 105% .dmg -20% .crit 8% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "Hwy Riposte 4"`
  - 현재: `combat_skill: .id "duelist_advance" .level 3 .type "melee" .atk 110% .dmg -20% .crit 8% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "RB HWY Tracking Buff 4"`
  - 원본: `combat_skill: .id "duelist_advance" .level 4 .type "melee" .atk 110% .dmg -20% .crit 9% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "Hwy Riposte 5"`
  - 현재: `combat_skill: .id "duelist_advance" .level 4 .type "melee" .atk 115% .dmg -20% .crit 9% .move 0 1 .launch 432 .target 123 .is_crit_valid True  .effect "RB HWY Tracking Buff 5"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 81행; Git 원문 {"commit": "119535adb664630cf45efd9a1d07240d791e8a47", "summary": "R-CMB-09 명중 상한과 장신구: '낮은 명중 = 장신구 전제' 가설 기각"}
- 기존 주석 원문:
```text
// HWY-005 duelist_advance: 명중 1렙 90 -> 95, dmg -20% 유지 (반격 상실 -47 / 축소 버프 +11.5 보상)
```
- 기존 주석 원문:
```text
// HWY-005 duelist_advance: Hwy Riposte -> Tracking Buff(축소), dmg -20% -> -40%
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Tracking Buff 1`
- 원본: `effect: .name "Tracking Buff 1" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6%  .crit_chance_add 4% .damage_low_multiply 12% .damage_high_multiply 12%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "Tracking Buff 1" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 3%  .crit_chance_add 3% .damage_low_multiply 6% .damage_high_multiply 6%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 72행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Tracking Buff 2`
- 원본: `effect: .name "Tracking Buff 2" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7%  .crit_chance_add 5% .damage_low_multiply 14% .damage_high_multiply 14%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "Tracking Buff 2" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 3%  .crit_chance_add 3% .damage_low_multiply 7% .damage_high_multiply 7%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 77행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Tracking Buff 3`
- 원본: `effect: .name "Tracking Buff 3" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8%  .crit_chance_add 6% .damage_low_multiply 16% .damage_high_multiply 16%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "Tracking Buff 3" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 4%  .crit_chance_add 4% .damage_low_multiply 8% .damage_high_multiply 8%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 79행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Tracking Buff 4`
- 원본: `effect: .name "Tracking Buff 4" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 9%  .crit_chance_add 7% .damage_low_multiply 18% .damage_high_multiply 18%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "Tracking Buff 4" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 4%  .crit_chance_add 4% .damage_low_multiply 9% .damage_high_multiply 9%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 81행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Tracking Buff 5`
- 원본: `effect: .name "Tracking Buff 5" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 8% .damage_low_multiply 20% .damage_high_multiply 20%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "Tracking Buff 5" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 5% .damage_low_multiply 10% .damage_high_multiply 10%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `heroes/highwayman/highwayman.effects_edit.txt`, 주석 추가 전 83행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 기존 주석 원문:
```text
// HWY-004 Tracking Buff 축소: 명중 6~10 -> 3~5, 치명타 4~8 -> 3~5, 피해 12~20%% -> 6~10%% (전투당 1회 제한 해제 대가)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY Tracking Buff 1`
- 원본 (Tracking Buff 1): `effect: .name "Tracking Buff 1" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 6%  .crit_chance_add 4% .damage_low_multiply 12% .damage_high_multiply 12%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "RB HWY Tracking Buff 1" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 3%  .crit_chance_add 3% .damage_low_multiply 6% .damage_high_multiply 6%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY Tracking Buff 2`
- 원본 (Tracking Buff 2): `effect: .name "Tracking Buff 2" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 7%  .crit_chance_add 5% .damage_low_multiply 14% .damage_high_multiply 14%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "RB HWY Tracking Buff 2" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 3%  .crit_chance_add 3% .damage_low_multiply 7% .damage_high_multiply 7%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY Tracking Buff 3`
- 원본 (Tracking Buff 3): `effect: .name "Tracking Buff 3" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 8%  .crit_chance_add 6% .damage_low_multiply 16% .damage_high_multiply 16%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "RB HWY Tracking Buff 3" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 4%  .crit_chance_add 4% .damage_low_multiply 8% .damage_high_multiply 8%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 19행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY Tracking Buff 4`
- 원본 (Tracking Buff 4): `effect: .name "Tracking Buff 4" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 9%  .crit_chance_add 7% .damage_low_multiply 18% .damage_high_multiply 18%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "RB HWY Tracking Buff 4" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 4%  .crit_chance_add 4% .damage_low_multiply 9% .damage_high_multiply 9%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 21행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HWY Tracking Buff 5`
- 원본 (Tracking Buff 5): `effect: .name "Tracking Buff 5" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 10% .crit_chance_add 8% .damage_low_multiply 20% .damage_high_multiply 20%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 현재: `effect: .name "RB HWY Tracking Buff 5" .target "performer" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 5% .crit_chance_add 5% .damage_low_multiply 10% .damage_high_multiply 10%  .on_hit true .on_miss true .duration 1 .buff_duration_type combat_end`
- 출처: `effects/rebalance_highwayman.effects.darkest`, 주석 추가 전 23행; Git 원문 {"commit": "2b526f34c1c82ec33b43856ed2a0898b99475688", "summary": "HWY-004/005 추적탄 반격 <-> 결투가의 진격 자기 강화 교환"}

### HWY-006 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 출혈·두 약화와 기존 치명을 보존하며 사용자의 최신 명중90/피해−25 교환을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/opened_vein`
  - 원본: `combat_skill: .id "opened_vein" .level 0 .type "melee" .atk 95% .dmg -15% .crit 0% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 1" "HW Open Vein Bleed Debuff 1" "HW Open Vein SPD Debuff 1"`
  - 현재: `combat_skill: .id "opened_vein" .level 0 .type "melee" .atk 95% .dmg -40% .crit 8% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 1" "HW Open Vein Bleed Debuff 1" "HW Open Vein SPD Debuff 1"`
  - 원본: `combat_skill: .id "opened_vein" .level 1 .type "melee" .atk 100% .dmg -15% .crit 1% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 2" "HW Open Vein Bleed Debuff 2" "HW Open Vein SPD Debuff 2"`
  - 현재: `combat_skill: .id "opened_vein" .level 1 .type "melee" .atk 100% .dmg -40% .crit 9% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 2" "HW Open Vein Bleed Debuff 2" "HW Open Vein SPD Debuff 2"`
  - 원본: `combat_skill: .id "opened_vein" .level 2 .type "melee" .atk 105% .dmg -15% .crit 2% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 3" "HW Open Vein Bleed Debuff 3" "HW Open Vein SPD Debuff 3"`
  - 현재: `combat_skill: .id "opened_vein" .level 2 .type "melee" .atk 105% .dmg -40% .crit 10% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 3" "HW Open Vein Bleed Debuff 3" "HW Open Vein SPD Debuff 3"`
  - 원본: `combat_skill: .id "opened_vein" .level 3 .type "melee" .atk 110% .dmg -15% .crit 3% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 4" "HW Open Vein Bleed Debuff 4" "HW Open Vein SPD Debuff 4"`
  - 현재: `combat_skill: .id "opened_vein" .level 3 .type "melee" .atk 110% .dmg -40% .crit 11% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 4" "HW Open Vein Bleed Debuff 4" "HW Open Vein SPD Debuff 4"`
  - 원본: `combat_skill: .id "opened_vein" .level 4 .type "melee" .atk 115% .dmg -15% .crit 4% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 5" "HW Open Vein Bleed Debuff 5" "HW Open Vein SPD Debuff 5"`
  - 현재: `combat_skill: .id "opened_vein" .level 4 .type "melee" .atk 115% .dmg -40% .crit 12% .launch 321 .target 12 .is_crit_valid True  .effect "Bleed 5" "HW Open Vein Bleed Debuff 5" "HW Open Vein SPD Debuff 5"`
- 출처: `heroes/highwayman/highwayman.info.darkest`, 주석 추가 전 90행; Git 원문 {"commit": "0ea50274ef8fede611b3351997bcea18f0668c84", "summary": "HWY-005~007 + 명중 표기 1레벨 기준 규칙"}
- 기존 주석 원문:
```text
// HWY-006 opened_vein: 치명타 보정 1렙 +0 -> +8, dmg -15% -> -40% (명중 1렙 95, 약화 2개 유지)
```
- 기존 주석 원문:
```text
//명중 95 -> 90 , 출혈 기술은 5 올리는 게 국룰, 약화 까지 달려서 10 올라간 거 같은 데 그러면 데미지를 까야함.
```
- 기존 주석 원문:
```text
//데미지 15 -> 25 로 바꿈 대신 명중 5만 깎음. 명중 안 깎으면 데미지 35까지 내려야할듯?
```

### HWY-010 결투가의 진격 자기 강화: 전투 종료까지 → 3턴 (2026-10-06)
- 상태: 사용자 승인 적용. 원문: "3번 지속 3턴 가자".
- 목표: G-00, G-02. 원칙: P-11, P-12, P-13, P-21.
- 변경: Tracking Buff 1~5 및 RB HWY Tracking Buff 1~5의 duration1/combat_end를 일반 duration3으로 변경. 명중3/3/4/4/5, 치명타3/3/4/4/5, 피해6/7/8/9/10%는 그대로.
- 의도: 공격과 전진을 하면서 얻는 준비 강화를 유지하되, 반복 사용으로 전투 끝까지 성능이 누적될 수 있는 경로를 제한한다. 진격의 사용 횟수나 이동을 제한하지 않는다.
- 현재 기술 명중1=95/기술 치명타1=5/피해−20. 이 작업은 기존 사용자 info 변경을 커밋하거나 수정하지 않는다.
- 총량 교환 문맥: 응징 최초 공격−20과 추적탄 최초 공격−75는 다른 역할에 화력을 배분한 현재 조정이다. 실제 반격 타격의 피해 배율은 이 최초 공격 수치와 별도다.
- 검증: 편집 사본/게임 효과5단계 일치, 재적용 안정성 및 다른 필드 보존. 실제 게임의 턴 감소 시점·동일 효과 중첩은 확인 전이며, 중첩 금지를 새로 구현했다고 주장하지 않는다.


### 명중 점검 (2026-10-07, 수치 변경 없음)
- 요청 (원문): "노상강도 명중이 너무 비정상적으로 높은 기술들이 많아서 검증한번해야할듯"
- 방법: ① 바닐라 1레벨 공격 기술 102개로 명중 회귀를 다시 맞춤(효과·사거리·대상 수·무기 평균·피해 보정, R2 0.31, 잔차 SD 6.9) ② 강함 모델(`tools/strength.py`, 5레벨)로 기술별 "명중 −5" 반사실 → 명중 5의 값 %p.
- 영웅 단위: 1레벨 공격 기술 평균 명중 바닐라 88.6 → **RB 92.1**, 평균 잔차 **+0.3 → +3.8**(20명 중 광대 다음 2위). 다만 원값 평균 92.1은 결투가·고행자 93.3, 역병 의사 93.0, 석궁사수 92.5와 같은 무리라 **절댓값이 튀는 게 아니라 "무기 피해 높은 영웅치고 높다"**는 뜻이다.

| 기술 | 1렙 명중 바닐라→RB | 피해 바닐라→RB | 가치 바닐라→RB (%p) | 명중 5의 값 | 판정 |
|---|---|---|---|---|---|
| 사악한 칼질 | 85→**90** | +15→+15 | +39.9→+48.6 | +8.7 | **대가 없음**. 주석 "표준으로 바꿈 데미지 보정 15 -> 0"이 데이터에 반영되지 않음 |
| 권총 사격 | 85→**90** | −15→−15 | +69.6→+84.2 | +10.7 | **대가 없음 + 표식 피해 25~50→40~60(MARK-01)** 이중 상향 |
| 결투가의 진격 | 90→**95** | −20→−20 | +157.2→+100.5 | +8.7 | 반격 상실 보상. 가치는 순감 |
| 포도탄 발사 | 75→**90** | −50→−70 | +2.3→−21.3 | +4.6 | 명중을 피해로 치렀고 순감. 비정상 아님 |
| 영거리 사격 | 95→90 | +50→+40 | +95.9→+91.0 | +11.2 | 하향 |
| 정맥 절개 | 95→95 | −15→−40 | +80.5→+70.9 | +9.6 | 바닐라 명중 |
| 추적탄 | 95→95 | −80→−75 | −52.4→+74.7 | +3.6 | 바닐라 명중(효과 기술) |

- 결론
  1. 대가 없이 명중만 오른 기술은 **사악한 칼질·권총 사격** 2개다. 결투가의 진격 +5는 반격 상실 보상이고 포도탄 +15는 피해로 치렀다.
  2. **총량 경고(P-11)**: 강함 모델 v2에서 노상강도는 바닐라 8위(58점) → **RB 15위(50점)**다. 목표(5위 전후)보다 이미 아래라, 두 기술 명중을 내리면(−8.7, −10.7%p) 더 내려간다. 명중을 내리려면 다른 곳 보상이 짝으로 필요하다.
  3. **주석·데이터 불일치 3건**(제작자 확인 필요)
     - 사악한 칼질: 주석은 피해 15 → 0, 데이터는 +15. 0을 적용하면 −16.8%p
     - 정맥 절개: 주석 "명중 95 -> 90 … 데미지 15 -> 25"는 HWY-006(95/−40)으로 대체된 옛 메모
     - 결투가의 진격: 주석 "dmg -20% -> -40%"(HWY-005 초안)와 "dmg -20% 유지"가 함께 있다. 데이터는 −20


### HWY-011 사악한 칼질: 피해 +15% → 0% (2026-10-07)
- 상태: 적용 (제작자 결정 "칼질 피해 0으로 적용하고")
- 근거: 명중 점검(위)에서 1렙 명중 85 → 90이 대가 없이 올라 있었고, info 주석 "표준으로 바꿈 데미지 보정 15 -> 0"이 데이터에 반영되지 않은 상태였다. 명중 +5를 피해로 치르게 해 R-TRADE-02 기준(명중 +5 ≈ 10%p) 안으로 넣는다.
- 영향: 강함 모델 5렙 가치 +48.6 → **+31.7%p (−16.8)**. 바닐라(+39.9)보다 낮은데, 사용 열 321 → 21 축소(HWY-008)는 바닐라에 없던 제약이 아니라 근접 사거리 정리라서 그대로 둔다.

### HWY-012 권총 사격: 1렙 명중 90 → 85 (2026-10-07)
- 상태: 적용 (제작자 결정 "권총은 명중 깎자")
- 근거: 명중 +5와 MARK-01 표식 추가 피해 25~50% → 40~60%가 한 기술에 겹친 이중 상향이었다. 바닐라 명중으로 돌리고 표식 피해 상향은 유지한다. R-TRADE-02 "기본 명중은 근접·원거리 모두 85"와 맞는다.
- 영향: +84.2 → **+73.4%p (−10.7)**. 바닐라 +69.6보다 +3.8 높은 것은 표식 피해 상향분이다.
- 총량: HWY-011+012 합 −27.5%p. 영웅 점수 50 → 49, 순위 15위 그대로(14위 총사 52, 16위 성녀 46).


### HWY-013 결투가의 진격: 명중 90 / 피해 −40% / 대상 1·2열 / 바닐라 버프 3턴 (2026-10-08) (→ HWY-016·018: 피해 −20%, 버프 레벨당 +1)
- 상태: 적용 (제작자 결정)
- 제작자 원문
  > 진격 버프 원래버전 그대로 유지하고 -40에 3열 안닿게 하고 명중 90 하면 딱 맞지않니?
- 변경
  - 1렙 명중 95 → **90**, 피해 −20% → **−40%**, 대상 `123` → **`12`**
  - `RB HWY Tracking Buff 1~5`: HWY-004 축소판(명중 3~5, 치명타 3~5, 피해 6~10%) → **바닐라 수치(명중 6~10, 치명타 4~8, 피해 12~20%)**, 지속은 HWY-010의 3턴 유지
- 근거
  1. 버프를 줄였던 이유는 반복 사용 시 전투 끝까지 누적되는 문제였고, HWY-010의 3턴 지속이 이미 그것을 막는다. 축소할 이유가 사라졌다.
  2. 근접으로 3열에 닿는 것은 희소한 가치다(R-STRAT-01, 후열 도달 희소성). 모델에서 3열 도달 하나가 약 29%p이고, 모델은 이 값을 과소평가한다.
  3. 명중 90: 적에게 거는 효과가 없는 피해 + 자기 강화 기술이라 효과 기술(95)이 아니라 피해 기술 기준을 따른다.
- 영향: 강함 모델 5렙 가치 +100.5 → **+73.7%p (−26.8)**. 바닐라 진격(반격 포함)은 +157.2
- 확인 필요: 같은 기술 버프가 3턴 안에 중첩되는지(4→3→2열로 최대 2회 연속 사용). 중첩되면 5렙 피해 +40%·명중 +20까지 쌓인다.

### HWY-014 사악한 칼질: 피해 0% → +15% 복귀 (HWY-011 철회, 2026-10-08) (→ HWY-019: 명중 85, 피해 0%)
- 상태: 적용 (제작자 결정 "사악한 칼질은 명중 90 피해 15로 하자")
- 결과: 명중 90 / 피해 +15 / 사용 21. 가치 +31.7 → +48.6%p(바닐라 85/+15/321은 +39.9)
- 제작자 판단: 노상강도 공격 기술 명중을 90으로 맞추는 정렬(효과 본업인 정맥 절개·추적탄은 95). 사용 열 321 → 21 축소가 명중 +5의 대가 역할을 한다.

### 노상강도 총량 (HWY-011~014 적용 후, 2026-10-08)

| 기술 | 1렙 명중 | 가치 %p |
|---|---|---|
| 사악한 칼질 | 90 | +48.6 |
| 권총 사격 | **85** | +73.4 |
| 영거리 사격 | 90 | +91.0 |
| 포도탄 발사 | 90 | −21.3 |
| 추적탄 | 95 | +74.7 |
| 결투가의 진격 | 90 | +73.7 |
| 정맥 절개 | 95 | +70.9 |

- 이번 점검 전 대비 −37.5%p(권총 −10.7, 진격 −26.8). 영웅 점수 50 → **46**. 15위로 성녀(46)와 동점이다. 14위 총사는 52.


### HWY-015 권총 사격: 1렙 명중 85 → 90 복귀 (HWY-012 철회, 2026-10-08)
- 상태: 적용 (제작자 결정 "권총 명중 90으로 되돌리자")
- 근거: 공격 기술 명중 90 정렬(칼질·권총·영거리·포도탄·진격 90, 효과 본업인 정맥 절개·추적탄 95). HWY-013 이후 영웅 점수가 46까지 내려가 총량 보전도 겸한다. 표식 피해 상향(MARK-01)과 겹치는 점은 감수한다.
- 영향: +73.4 → +84.2%p (+10.7). 영웅 점수 46 → 47, 15위.

### 결투가의 진격 버프 크기 검토 (2026-10-08, 수치 변경 없음)
- 제작자 질문: "진격 버프 좀 과한것 같은데"
- 강함 모델(5렙, 강화 지속 상한 2턴, 중첩 미반영)

| 안 | 5렙 버프 (명중/치명타/피해) | 진격 가치 %p |
|---|---|---|
| 바닐라 ×1.0 (현재) | 10 / 8 / 20% | +73.7 |
| ×0.75 | 8 / 6 / 15% | +53.3 |
| ×0.5 (HWY-004 축소판 수준) | 5 / 4 / 10% | +30.3 |

- 동류 비교(RB): 성녀 빛의 손길(피해 −50%, 1·2·3열, 자기 명중 +10·피해 +35% 3턴) **+61.3**, 야만인 함성(피해 없음, 명중 +10·피해 +30%) +12.3. 진격의 강화 몫은 빛의 손길과 거의 같고, 차이는 노상강도 무기 피해에서 나오는 직접 피해다.
- 노상강도 키트 안: 칼질 +48.6 / 정맥 절개 +70.9 / **진격 +73.7** / 추적탄 +74.7 / 권총 +84.2 / 영거리 +91.0. 진격은 중간이다.
- 판정: 수치상 과하지 않다. 위험은 모델이 세지 않는 **같은 버프 중첩**이다(4→3→2열로 최대 2회 연속 → 5렙 명중 +20·치명타 +16·피해 +40%). 게임에서 중첩이 확인되면 ×0.75로 낮춘다.


### HWY-016 결투가의 진격 버프: 바닐라 ×0.75 (2026-10-08) (→ HWY-018: 명중 4~8, 치명타 2~6, 피해 10~14%)
- 상태: 적용 (제작자: "당연 쌓이고 중복됨 . 0.5 0.75 뭐가 나은지 판단해서 적용")
- 전제 확인 [제작자, 게임]: 같은 Tracking Buff가 3턴 안에 **중첩된다.** 진격은 사용 4·3·2열 + 자기 전진 1이라 연속 사용은 4→3→2열 **최대 2중첩**이다.
- 변경: `RB HWY Tracking Buff 1~5` 명중 6~10 → **5/5/6/7/8**, 치명타 4~8 → **3/4/5/5/6**, 피해 12~20% → **9/11/12/14/15%**. 지속 3턴 유지
- 판단: ×0.75

| | ×0.5 | **×0.75** |
|---|---|---|
| 1회 5렙 버프 | 5 / 4 / 10% | **8 / 6 / 15%** |
| 2중첩 상한 | 10 / 8 / 20% (= 바닐라 1회분) | **15 / 12 / 30% (바닐라 1.5배)** |
| 진격 가치 (모델 5렙) | +30.3 | **+53.3** |
| 키트 안 위치 | 포도탄 다음 최하위 | 사악한 칼질(+48.6)과 비슷 |

  1. 모델은 사용 1회마다 버프를 따로 세므로 이미 가산 중첩을 가정한 값이다. 중첩 확인으로 바뀌는 것은 평균 가치가 아니라 **2중첩 순간 최대치**다.
  2. ×0.75의 2중첩 최대치(피해 +30%·명중 +15)는 야만인 함성 1회분(명중 +10·피해 +30%)과 같은 급이다. 함성은 제자리에서 3회 이상 쌓을 수 있다.
  3. ×0.5는 진격을 자리 이동 말고는 쓸 이유가 없는 기술(+30.3)로 만들고, 노상강도 총량(15위)을 −43.4%p 더 깎는다. ×0.75는 −20.4%p.
  4. 2중첩 직후 노상강도는 2열에 있어 영거리 사격(1열)·권총 사격(3·4열)을 쓸 수 없다. 2열에서 쓸 수 있는 기술은 사악한 칼질·정맥 절개·포도탄(−70%)·추적탄(−75%)이고, 뒤의 둘은 피해가 낮아 순간 화력이 폭주하지 않는다.

### HWY-017 영거리 사격: 명중·피해 바닐라 복귀 (2026-10-09)
- 상태: 적용 (제작자 직접 편집, Claude가 주석·기록 정리)
- 변경: 1렙 명중 90 → **95**, 피해 +40% → **+50%**(HWY-001의 수치 너프 철회). 사용 후 뒤로 2칸 후퇴·밀치기 2칸(HWY-001 구조 변경)은 유지
- 제작자가 지운 기존 주석: "일단 명중 5 너프, 데미지 10 너프 적용해놓음. 명중 95 -> 90, 딜 50 -> 40"
- 철회 사유: 원문 없음(기록하지 않음). HWY-001 원래 의도는 "순수 성능 너프는 체감이 불쾌하니 연속 사용을 어렵게 만드는 구조로 조절"이었고, 후퇴 구조가 남아 그 의도와는 일치한다.
- 영향: 강함 모델 5렙 가치 +91.0 → **+113.8%p**. 노상강도 점수 47 → 50(다른 변경 포함 현재값).

### HWY-018 결투가의 진격: 피해 −40% → −20%, 버프 규칙값 정리 (2026-10-09)
- 상태: 적용 (제작자 결정)
- 피해: −40%는 3열 도달 제거(HWY-013)의 대가로 버프를 바닐라로 돌리며 건 값인데, 이후 중첩 확인으로 버프를 ×0.75로 줄여(HWY-016) 대가가 이중이 됐다. −20%(바닐라 피해)로 복귀. 강함 모델 +53.3 → **+75.7%p**(추적탄 +74.7과 같은 급).
- 버프: ×0.75 반올림값(명중 5/5/6/7/8, 치명타 3/4/5/5/6, 피해 9/11/12/14/15%)이 들쭉날쭉해 **레벨당 +1 규칙값**으로 정리 [제작자 "딱 맞아 떨어지게"]: 명중 **4/5/6/7/8**, 치명타 **2/3/4/5/6**, 피해 **10/11/12/13/14%**, 3턴. 2중첩 최대치(5렙) 명중 +16·치명타 +12·피해 +28%.

### HWY-019 노상강도 재정렬: 칼질 3열 도달, 정맥 절개·추적탄 피해 상향 (2026-10-10)
- 상태: 적용 (제작자 결정 "노상강도 너무 구려진 듯")
- 변경
  - 사악한 칼질: 1렙 명중 90 → **85**, 피해 +15% → **0%**, 대상 1·2 → **1·2·3열**
  - 정맥 절개: 피해 −40% → **−25%** (바닐라 −15%)
  - 추적탄: 피해 −75% → **−60%** (결투가 결정타와 같게)
  - 결투가의 진격: 그대로(1·2열, −20%, 레벨당 +1 버프)
- 근거 [제작자 안]: 진격에 3열을 다시 주면 버프·이동까지 가진 진격이 칼질을 대체한다. 3열 도달은 버프·이동 없는 칼질에 주고, 칼질은 근접 단일 표준(명중 85·피해 0, R-SKILL-09)으로 맞춘다. 진격은 사용 열 4·3·2라 1열에서 못 쓰므로 1열 근접은 칼질 몫이다.
- 영향(강함 모델 5렙 %p): 칼질 +48.6 → **+67.5**, 정맥 절개 +70.9 → **+89.2**, 추적탄 +74.7 → **+98.3**. 포도탄을 빼면 여섯 기술이 +67~+114에 고르게 놓인다. 노상강도 16위 → **14위(52점)**.

### HWY-020 정맥 절개 −30%, 포도탄 −60% (2026-10-10)
- 상태: 적용 (제작자 결정, Claude 권장안)
- 배경: 강함 모델이 buff_ids·buff_type 형식의 적 약화를 세지 못하던 것을 고쳤다(R-VALUE-12). 정맥 절개는 +89.2 → +115.4(키트 1위), 포도탄은 −21.3 → −0.9(취약 반영 후에도 최하위).
- 변경: 정맥 절개 피해 −25% → **−30%**(+109.3), 포도탄 피해 −70% → **−60%**(+22.0). 두 기술 모두 명중은 유지.
- 기각한 안: 정맥 절개 명중 95 → 90(+103.3), 포도탄 명중 85/−60%(+14.8) — 효과 본업 기술은 명중 우선(출혈·약화·취약 적중이 떨어져 체감 손해가 수치보다 크다).

### HWY-009 보충 근거: 권총 사격 명중 85 → 90 (2026-10-17)
- [제작자] 원거리 기술은 거의 명중 90인데 노상강도만 없었다. 근접 빌드에 비해 원거리 빌드가 너무 약해서 상향이 필요했다.
- 데이터: 바닐라 원거리 단일 피해 기술 34개의 1렙 명중 중앙값 90. 85는 노상강도 권총·조련사 돌진·도망자 반딧불·방패 파괴자 표적 지정뿐. R-TRADE-02(기본 명중 85)의 예외로 기록.

### HWY-021 영거리 사격 치명 5~9% → 8~12% (2026-10-21)
- 제작자 결정: 도굴꾼 돌진(치명 8~12%)만큼 준다. 결국 2칸 멀어지는 게 빡세기 때문에 한 방의 보상을 키운다.
- 근거: 영거리 사격은 쏘고 뒤로 2칸·적 밀치기 2칸(HWY-001)이라 연속 사용이 어렵다. 같은 "앞으로 나가 한 방" 계열인 돌진과 치명을 맞춘다.

### HWY-022 정맥 절개 바닐라 복귀 (2026-10-21)
- 피해 −15%, 치명 0~4%(바닐라). HWY-006·019·020(치명 +8, 피해 −40 → −25 → −30) 철회.
- 근거: 앞열 출혈 기술 비교(1렙) — 역병 의사 절개 명중 90·피해 0%·치명 5%·효과 1개 대비, 정맥 절개 바닐라는 명중 95(+5) 대신 피해 −15%·치명 0%로 출혈 저항 −20%·속도 −1을 더 받는다. "공짜 상향 없음"에 맞는 바닐라 교환이라 바꿀 근거가 약했다 [제작자 "바닐라로 test에 넣어줘"].

### HWY-023 결투가의 진격 강화 수치 정리 (2026-10-21)
- 명중 +4~8 → **+5/6/7/8/10**, 치명 +2~6 → **+1/2/3/4/5**, 피해 +10~14 → **+10/11/12/13/15%** (3턴). 제작자: "깔끔하게". 명중 +1~2, 치명 −1로 가치는 거의 같거나 조금 위(명중 5 = 피해 10%p). 기술 피해 −20%는 유지(치고 전진 + 3턴 강화).

### HWY-024 칼질 ↔ 정맥절개 치명타 교환 (2026-10-25, test)
- 상태: 사용자 승인, test 적용. 커밋만 요청했으며 push/공개 배포는 하지 않는다.
- 변경: 기술 1~5레벨 사악한 칼질 치명 5/6/7/8/9% → 0/1/2/3/4%; 정맥절개 0/1/2/3/4% → 5/6/7/8/9%.
- 의도: 칼질은 3열 도달 일반 평타, 정맥절개는 출혈이 통하는 전열 장갑 적 대응. 사거리 이점은 칼질에 두고 치명 연계는 정맥절개로 옮긴다.
- 유지: 두 기술의 명중·피해·사용열·대상열, 정맥절개의 출혈·출혈 저항 감소·속도 감소. 고정 장신구와 다른 기술 유지.
- 근거/제약: 출혈 확률 +40%·근접 치명 +7% 장신구와 연계된다. 치명 자체는 방어 관통이 아니고 출혈 면역을 해결하지 않는다. 같은 5%p 교환도 출혈·치명 부수효과 때문에 총가치 보존의 수학적 증명은 아니다.
- 이력: HWY-022의 정맥절개 치명 바닐라 복귀만 대체한다. 기존 한국어 주석과 기록은 보존.
- 사용자 승인 원문: 일단 노상강도 치명타는 서로 바꾸자 칼질 0 정맥절개 5로 의도 주석 남기고 test에 적용해서 커밋까지 해
- 방향 원문: 노상강도 개편하고 싶어 개편안은 다음과 같아 정맥절개로 방어도 캐릭 상대 사악한 칼질은 3열까지 닿는 일반 평타 근데 지금은 사악한 칼질이 3열 닿고 치명타율도 정맥절개보다 높아서, 정맥 절개가 쓸 이유가 없어졌어. 나는 정맥절개가 치명타 더ㅏ 높았으면 하거든 정맥 절개이고, 방어도 상대 취약점을 정맥절개 치명타 도트딜로 이겨나갔으면 해서 그래서 사악한 칼질을 3열까지로 어마어마하게 버프했으니 치명타를 정맥절개에 넘기려고 해 어느정도가 적당할까?
- 검증: 10개 기술 행의 치명 외 필드 보존, 주석 검사, 배포 목록 크기 확인. 게임 내 시험은 미실시.


### HWY-025 사용자 확정 수정 (2026-10-26, local)
- 상태: 로컬 적용, 공개 미배포.
- 사용자 원문: "정맥절개 피해 -20 왜 반영안됐니? 치명타는 높아졌는데?"
- 의도·변경: 기존 -20은 검토안으로만 남아 실제 파일은 -15였다. 이번 명시 요청으로 -20을 적용한다. HWY-024의 치명 5~9% 및 출혈·약화는 유지하여 직접 피해와 장갑 대응 출혈의 교환을 만든다.
- 출처: local-knowledge event d93df284982f63a61845429af6e52d067d9e59987c639e09ebab8853bff4b19b
- 검증: 원본/무관 데이터 보존 및 주석 검사. 게임 화면 재확인은 별도이며 런타임 확인으로 주장하지 않는다.

### HWY-026 반격 기술 피해 0 → −15%, 자기 반격 보정 −29/−21/−12/−6/0% (2026-10-28, test)
- 자기 반격 결과는 그대로(−40/−33/−25/−20/−15, 0.85 x (1+보정)). 보정은 반격 상태 안에 그대로라 중첩 없음.
- 의도: 유물 날 지켜줘(보정 0)로 덮어써질 때 저렙 숨은 강화를 +40%p → +25%p로 줄이고 5렙은 0(P-25). 제작자 "저렙 때 약하고 나중에 강해진다 … 위배되는 모델이잖아".
