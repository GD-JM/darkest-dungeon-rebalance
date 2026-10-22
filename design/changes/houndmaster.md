# 조련사 (houndmaster) 변경 항목

바닐라 수치: `heroes/houndmaster/houndmaster.vanilla.txt`

---

### HM-001 사냥개 돌진: 표식 대상 추가 피해 하향 (제안)
- 상태: 보류
- 분류: 의도적 조정 (표식 보상 서열)
- 목표: G-01
- 사용자 제안: 60→100을 40~60으로 낮춰 현상금 사냥꾼(90→110)보다 확실히 아래에 둔다. 원문은 `bounty_hunter.md` "BH-003 / BH-004 추가 검토" 참고.
- 데이터:

  | 안 | 5레벨 표식 대상 기대 피해 |
  |---|---|
  | 원본 +100 | 16.5 |
  | 사용자안 +60 | 13.2 (방패 파괴자 휘감기 13.4 수준) |
  | 대안 +80 | 14.8 |

  - 조련사는 순위 모델 2위(아군 효과 적용 확률 누락을 고친 뒤. 수정 전 1위), 가격표 초과 합 +52다.
  - 모델 가정을 보수적으로 바꾸면 7위까지 내려간다(`analysis/hero_power.md` 9절). 가정과 무관한 최상위는 노상강도다.
  - 그러나 상위권의 원천은 사냥개 돌진(가치 15.6)이 아니라 **사냥개 습격**(광역 출혈, 가격표 +28.7, 가치 22.3)과 **위험 경보**(스트레스 회복, 적용 확률 74%, 가치 12.4)다.
  - 사냥개 돌진은 대상이 1~4열로 가장 넓다. 사거리 서열로 보면 표식 보상이 가장 낮아야 한다는 논리는 성립한다.
- 보류 이유:
  0. 조련사는 사기가 아니라 가정에 따라 2~7위인 상위권이다. 5레벨 체력 37로 생존은 중간 이하다.
  1. 방향이 "표식 보상을 늘려 전부 활용"인데 이 안은 하향이다.
  2. 조련사가 강한 원인(사냥개 습격)을 건드리지 않는다.
- 다음: 조련사 하향이 필요하면 사냥개 습격을 먼저 검토한다. 사냥개 돌진을 조정하면 고정이 아니라 성장을 유지(R-EFF-05)하고 60→80안을 우선한다.

---

## 2026-09-27 조련사 전면 조정 (HM-010 ~ HM-015)

### 설계 목표: "육각형 · 모든 열에서 제 몫, 대신 느리다"

공식 설정(P-22)에서 도출한 정체성이다.

| 계층 | 문장 | 함의 |
|---|---|---|
| 대장간 | "곤봉은 적을 효과적으로 기절시키지만, **진짜 치명타는 사냥개가 먹입니다**" | 조련사 **본인**은 딜러가 아니다. 화력은 사냥개(돌진·습격)에만 |
| 대장간 | "공격을 받아내기보다는 **아예 회피**하는 쪽을 선호" | 전열형이 아니다. 방어도 0, 회피 의존 |
| 길드 | "사냥개와 함께 **측면에서 지원**하며" | 주 역할은 지원 |
| 길드 | "약자를 보호하고 **고통을 받은 자들을 부축**하며" | 보호·회복은 자리를 가리지 않는다 |

**장점** = 1·2·3·4열 어디서나 제 몫을 한다.
**단점** = **어느 열에서도 적을 빨리 지우지 못한다.** 돌진은 조건부, 습격은 광역 DoT라 구조적으로 처치 불가, 둔기 강타는 화력 0, 나머지 넷은 피해가 없다. 4v3 전환(R-STRAT-01)은 남이 한다.

**열 구조**: 둔기 강타(사용 2·1) + 사냥개 습격(사용 4·3·2)이 **2열에서만 함께** 잡힌다.
1열에 서면 습격을 못 쓰고, 3열에 서면 둔기 강타를 못 쓴다. → **1·3·4열 모두 활용 가능하되 2열이 메인**.

### 광역 지속 피해 재평가 (R-STRAT-01 적용)

기존 평가는 단일·광역 지속 피해에 같은 행동 경제 배율(0.90)을 썼다. **이것이 오류였다.**

전투 길이가 상한이다. 적 4명 ÷ 라운드당 처치 1.57명 = **전투 2.55라운드**.
라운드당 적 사망률 1.57/4 = 39.3% → 생존율 0.608.

| 틱 | 유효율 |
|---|---|
| 1틱 | 0.608 |
| 2틱 | 0.369 |
| 3틱 | 0.224 |
| 합 | **1.20 / 3 = 40%** |

단일 지속 피해가 다른 이유: 단일 출혈은 **직접 피해와 같은 대상**에 들어가고, 그 대상은 파티가 집중 사격 중인 적이다. 남은 틱이 날아가도 **그 처치에 기여한 뒤** 날아간다. 광역 출혈은 처치 순서와 무관한 전원에게 얕게 깔려 회수 전에 전투가 끝난다.

| 유형 | 유효율 | 근거 |
|---|---|---|
| 단일 직접 | 1.00 | 기준 |
| 단일 지속 | 0.90 | 즉시성 손실, 처치 기여로 회수 |
| 광역 직접 | 0.85 | 템포 손실만. 적이 전멸해야 전투가 끝나므로 **총량은 회수** |
| **광역 지속** | **0.40** | **회수 전에 전투 종료** |

실제 평균 적 수는 4가 아니라 **3.2명**이다(2~3명 전투·보스전 포함).

이 수정으로 사냥개 습격은 **15.8 HP(2위) → 13.2 HP(4위)** 로 내려간다. 기술 슬롯이 4개이므로 4~5위는 잘린다. "아무도 쓰지 않는다"는 실제 체감과 일치한다. **사기 판정을 철회한다.**

### 평가 단위: 평타 배수

HP와 %p를 섞어 쓰던 것을 통일한다. **평타(그 영웅의 피해 보정 0% 단일 공격) = 100%**.
조련사 평타 = 10.87 HP. 영웅 간 비교가 되면서 %p의 직관도 유지된다.

---

### HM-010 사냥개 돌진 출혈: 지속 3턴 → 1턴, 턴당 1/1/1/2/2 → 1/1/2/2/3
- 상태: 적용
- 분류: 의도적 조정 (하향)
- 목표: G-01
- 수치: `RB HM Hound Bleed 1~5`. 5레벨 총량 **6 → 3**. 치명타 시 지속 1→2턴(R-CMB-08).
- 근거: 돌진은 야수 특효 + 표식 보상 + 출혈의 3겹이다. 피해 보정을 낮추면 사용감이 무너지므로(P-12) 가장 덜 체감되는 출혈 총량을 절반으로 줄인다.
- 예외 기록: R-EFF-02의 "출혈 지속 3턴" 경향에서 벗어난다. 도망자 화상에 이미 2턴 선례가 있다.

### HM-011 사냥개 돌진: 사용 4·3·2 → 4·3·2·1, 대상 1·2·3·4 → 2·3·4
- 상태: 적용
- 분류: 의도적 조정 (구조 변경)
- 목표: G-04
- 근거:
  - 사용 열 확대 — "모든 열에서 제 몫" 정체성. 1열에서도 쓸 수 있되, 대상이 2·3·4이므로 1열이 **메인이 되지는 않는다**.
  - 대상 1열 제거 — 길드 "**후열에 접근해** 괴롭히고". 1열 타격의 설정 근거가 없다.
- **피해 보정 0% 유지**: 출혈 −2.9 HP(HM-010)와 대상 1열 제거가 사용 열 확대와 상쇄된다. 재계산 결과 14.4 HP(132%)로 이미 −17%다. 추가 하향은 과하다.
  - (이전 제안이던 −25% 하향은 출혈 너프 효과를 과소평가한 것이라 철회)

### HM-012 사냥개 습격: 사용 4·3·2·1 → 4·3·2, 피해 −75% → −70%
- 상태: 적용
- 분류: 의도적 조정 (상향 + 구조 변경)
- 목표: G-04
- 근거:
  - 사용 1열 제거 — 대장간 "공격을 받아내기보다는 아예 회피". 전열형이 아니다. 그리고 **둔기 강타(사용 2·1)와 함께 잡히는 열이 2열뿐**이 되어 메인 열이 확정된다.
  - 피해 상향 — 위 재평가에서 13.2 HP(121%, 4위)로 슬롯 경쟁에서 잘린다. −70%면 **14.4 HP(132%)** 로 3위권에 들어가 선택지가 된다. 사용 열 축소의 대가이기도 하다.

  | | −75% | −70% |
  |---|---|---|
  | 직접 | 5.8 | 7.0 |
  | 출혈 (명목 21.6) | 6.9 | 6.9 |
  | 합 | 13.2 (121%) | **14.4 (132%)** |

### HM-013 둔기 강타: 1레벨 명중 95 → 90, 피해 −65% → −80%, 기절 강한(110) → 기본(100) (→ HM-022 −65% → HM-024 −50%)
- 상태: 적용 → 피해는 HM-022(−65%)·HM-024(−50%)로 바뀜. 현재 데이터: 1렙 명중 90, 피해 −50%, 바닐라 `Stun 1~5`(일반 기절), 대상 1·2·3.
- 분류: 의도적 조정 (하향)
- 목표: G-01
- 수치: 명중 90/95/100/105/110, 피해 −80%, `RB HM Hero Strong Stun 1~5` 확률 100/110/120/130/140. **대상 1·2·3 유지.**
- 근거 (설정): 대장간 "곤봉은 적을 효과적으로 기절시키지만, **진짜 치명타는 사냥개가 먹입니다**".
  → 곤봉은 기절 담당이고 화력이 아니다. **3열 도달("후려치며 혼란을 일으킨다")과 기절은 남기고 화력만 제거한다.**
- 근거 (수치): 근접 기절기 중 혼자 명중 95 + 강한 기절(110) + 3열 도달의 3중 우위였다. 명중·기절 등급은 표준으로 되돌리고, 3열 도달의 대가를 피해로 치르게 한다.
  - 피해 −80%는 근접 기절기 중 야만인 함성(−100%) 다음으로 낮다. 3열 도달 + 기절의 값이다.
  - 결과: 8.0 HP(74%) → **5.0 HP(46%)**
- 구현: `Hero Strong Stun 1~5`(110~150)를 내린 결과가 바닐라 **`Stun 1~5`**(100~140)와 글자 하나까지 같다. **사본을 만들지 않고 `Stun 1~5`를 그대로 가리킨다**(R-DATA-01). 섬광탄·야만스러운 함성!은 `Hero Strong Stun`을 그대로 쓰므로 영향 없다.
- 철회 기록: "곤봉 모션이 아파 보이니 피해를 올리자"(P-19 아트-기능 일치)는 위 대장간 문장과 정면으로 충돌한다. **P-22가 P-19의 상위 원칙이므로 철회한다.**

### HM-014 위험 경보: 회복 2/3/4/5/6 → 4/4/5/5/6, 확률 66~74 → 74 고정
- 상태: 적용
- 분류: 의도적 조정 (상향, 저레벨 한정)
- 목표: G-02
- 데이터:

  | 렙 | 현재 기대 회복 | 변경 후 | 배율 |
  |---|---|---|---|
  | 1 | 2×66% = 1.32 | 4×74% = **2.96** | **2.24배** |
  | 2 | 3×68% = 2.04 | 4×74% = 2.96 | 1.45배 |
  | 3 | 4×70% = 2.80 | 5×74% = 3.70 | 1.32배 |
  | 4 | 5×72% = 3.60 | 5×74% = 3.70 | 1.03배 |
  | **5** | 6×74% = **4.44** | 6×74% = **4.44** | **1.00배** |

- 근거:
  - 아군 **전체** 스트레스 회복은 이 기술뿐인데, 유일하게 확률이 100%가 아니다(고행자 인내 10→14, 광대 격려의 선율 8→12, 성전사 격려의 함성 5→8 — 전부 단일 대상이지만 전부 100%).
  - 문제는 저레벨 불안정성이다. **5레벨 값을 그대로 두고 1~3레벨만 끌어올려 P-12를 완전히 지킨다.**
  - 74% 고정은 "완전 보장은 아니다"라는 원래 설계 정체성을 유지한다.
  - 대안이던 "확률 100%"는 5레벨을 4.44 → 6.00(+35%)으로 올려 숙련 파티의 체감을 바꾸므로 기각.
- 설정 근거: 야영 "충성스러운 개와 정서적 교감을 나눈다면, 감정은 누그러지고 **마음도 안정될 것입니다**". 확률적이면 안정이 아니다.
- **사용 열은 4·3 유지** [사용자 판정 2026-09-27]. 2열까지 열어주면 **2열 붙박이가 심해진다.** "2열 아니면 3열" 중에서 고르게 만드는 편이 낫다 — 조련사가 한 자리에 굳지 않게 하는 것이 육각형 정체성에 맞는다.
  - 이것이 열 설계의 일반 원칙이다: **좋은 기술을 한 열에 몰아주면 그 열 붙박이가 되고, 유연성이라는 장점이 사라진다.**

### HM-015 상처 핥기: 사용 4·3·2 → 4·3·2·1
- 상태: 적용
- 분류: 의도적 조정 (상향)
- 목표: G-04
- 근거:
  - **가장 많이 맞는 1열에서 자가 회복을 못 쓰는 구조**가 이상하다.
  - 조련사의 1열 사용 가능 기술은 4개로 **전체 평균 4.7 미만**이었다. 변경 후 5개.
  - 설정: 길드 "약자를 보호하고 **고통을 받은 자들을 부축**하며" — 자리를 가리지 않는다.
- 참고 (1열 소외 구조): 열별 영웅당 평균 사용 가능 기술 수는 1열 4.7 / 2열 5.4 / 3열 5.5 / **4열 4.2**다. 1열보다 **4열이 더 부족**하다. "1열 활용 영웅이 적다"는 판단은 절반만 맞고, 실제로는 **양 끝 열이 소외**되는 구조다.

### HM-016 사냥개 돌진: 피해 0% → −25% (적용)

- 목표: G-04
- 근거:
  - 돌진은 **표식(+60%) · 야수 특효(+35%) · 출혈**을 한 기술에 겹쳐 쥐고 있어 조건 충족 시 실전가 **226%**로 조련사 1위였다.
  - 사용 열이 4·3·2 → 4·3·2·1로 넓어져(HM-011) **가용성이 올라간 만큼 위력으로 대가를 지불**한다(R-TRADE-02).
  - 조정 후: 조건 없을 때 **92%(평타 수준)**, 표식+야수 충족 시 **188%**. 조건부 아키타입의 낙차가 선명해진다.
- 검증 전: 피해 보정 가산/곱산 여부(V-01)에 따라 조건 충족 시 값이 13% 달라진다. 곱산으로 판명되면 −25%로는 부족하다.

### 광역 지속 피해 재평가 — 결론 정정

이전에 사냥개 습격을 "사기"로 판정했던 것을 **철회한다.** 제작자 지적("이거 쓰는 사람 거의 한 명도 없어")이 맞다.

원인은 모델이 지속 피해에 **행동 경제 배율 0.90을 일률 적용**한 것이다. 광역 DoT에는 세 보정이 모두 필요하다(R-VALUE-03):

| 보정 | 습격 5레벨 |
|---|---|
| 보정 없음 | 170% |
| ① 출혈 실측 적용률(60.4%) | 158% |
| ② 광역 DoT 행동 경제 0.40 | 158% |
| ③ 광역 유효 대상 2.8/4 | **112%** |
| **1레벨** | **52%** |

결정적 근거는 **출혈 면역**이다. 영웅 등급 몬스터 74종 중 **27종(36.5%)이 저항 100 이상**으로 사실상 면역이고(해골 전군·익사자 전군·에크토플라즘·가고일), 5레벨에서도 **20%에겐 적용률 0%**다. 납골당과 만에서 기술 슬롯 하나가 통째로 죽는다.

1레벨 실전가가 평타의 **52%**이므로, 기술을 고르는 시점에 아무도 선택하지 않는다. 그래서 하향이 아니라 **상향(−75% → −70%)이 맞다**.

### 변경 후 조련사 기술 서열 (5레벨, 평타 = 8.61 HP = 100%)

평타 = 무기 5단계 평균 10, 명중 105, 치명타 8%의 피해 보정 0% 단일 공격.

| 기술 | 평타 배수 | 변경 전 | 비고 |
|---|---|---|---|
| 사냥개 돌진 (표식+야수) | **188%** | 226% | 조건 충족 시 |
| 사냥개 습격 | **120%** | 112% | 광역 3보정 적용값 |
| 목표물 지정 | 62% | 62% | 아군 표식 딜러를 살리는 기술 |
| 사냥개 돌진 (조건 없음) | **92%** | 131% | 조건 미충족 시 |
| 상처 핥기 | 93% | 93% | |
| 위험 경보 | 83% | 83% | 5레벨 불변, 1레벨만 5.28 → 11.84 |
| 경비견 | 69% | 69% | |
| 둔기 강타 | **55%** | 80% | 기절 담당으로 역할 축소 |

**설계 결과**: 돌진이 조건에 따라 92~188%로 갈리고, 습격이 120%로 실사용권에 진입하며, 둔기 강타가 55%로 순수 제어기가 된다. 열 구성은 아래와 같다.

| 열 | 쓸 수 있는 기술 | 공격 기술 수 |
|---|---|---|
| 1열 | 돌진 · 목표물 지정 · 경비견 · 상처 핥기 · 둔기 강타 | 2 |
| **2열** | 돌진 · **습격** · 목표물 지정 · 경비견 · 상처 핥기 · **둔기 강타** | **3** |
| 3열 | 돌진 · 습격 · 목표물 지정 · 경비견 · 상처 핥기 · 위험 경보 | 2 |
| 4열 | 돌진 · 습격 · 목표물 지정 · 경비견 · 상처 핥기 · 위험 경보 | 2 |

**2열만 습격과 둔기 강타를 모두 쓸 수 있다.** 1열에서는 습격이, 3·4열에서는 둔기 강타가 빠진다. 모든 열에서 제 몫을 하되 **2열이 메인**인 구조가 수치로 성립한다.

### HM-017 저항: 중독 40 → 30, 출혈 40 → 30 (적용)

- 목표: G-04, P-22
- 근거: `analysis/resistances.md` 4절.
  - 저항 기준선은 기절·이동 40 / 중독·출혈·질병·약화 30 / 함정 10이다. 조련사 편차는 함정 +30 · 중독 +10 · 출혈 +10.
  - 함정 +30은 야영 "늑대개를 정찰에 내보내거나 밤에 경비로 세울 수 있습니다"로 정당화된다. **유지.**
  - 중독·출혈 +10은 대응 문장이 없다. 오히려 같은 문장 구조의 노상강도("두껍게 덧댄 외투… 칼도 잘 박히지 않지만, 받아내기보다는 회피")가 출혈 30인데 "낡은 제복"의 조련사가 40인 건 모순이다.
- 결과: 저항 총합 260(1위) → 240(야만인·나병환자·역병 의사와 공동 2위).
- 대안 철회: 출혈 20. 20은 "방어구를 걸치지 않는" 영웅 급이라 "낡은 제복"보다 과하다.

### 남은 문제: 단점이 없다

조련사는 **저항 총합 1위**다.

| 영웅 | 기절 | 중독 | 출혈 | 질병 | 이동 | 약화 | 함정 | 합 |
|---|---|---|---|---|---|---|---|---|
| **조련사** | 40 | 40 | 40 | 30 | 40 | 30 | 40 | **260** |
| 야만인 | 40 | 40 | 40 | 30 | 40 | 30 | 20 | 240 |
| 나병환자 | 60 | 40 | **10** | 20 | 60 | 40 | 10 | 240 |
| 역병 의사 | **20** | 60 | **20** | 50 | **20** | 50 | 20 | 240 |

**조련사만 최저값이 30이다.** 다른 영웅은 전부 10~20짜리 구멍이 있다. 그리고 **야만인의 완전 상위호환**(함정 40 vs 20, 나머지 전부 동일)이다.

"육각형 · 표준"이 정체성이라면 **어딘가는 평균 이하여야 한다.** 저항이 구멍 없이 전부 평균 이상인 현재 상태가 "단점이 안 보인다"의 데이터적 실체다. → HM-017로 설정 근거 없는 편차(중독·출혈 +10)를 제거했다.


### 참고: v2 모델 재계산 (2026-09-27)

위 서열표들은 이번 세션의 임시 계산이다. 규칙을 정리한 v2 모델(`analysis/hero_power_v2.md`)로 다시 계산하면 RB 조련사 기술 서열은 다음과 같다(평타 7.12 HP).

| 기술 | HP | 평타 배수 |
|---|---|---|
| 사냥개 습격 | 13.2 | 185% |
| 사냥개 돌진 | 10.8 | 151% |
| 상처 핥기 | 8.0 | 112% |
| 목표물 지정 | 7.2 | 101% |
| 경비견 | 5.4 | 75% |
| 위험 경보 | 5.4 | 75% |
| 둔기 강타 | 4.1 | 58% |

- 영웅 순위: 바닐라 10위 → RB 12위(기본 가중치), 균등 가중치 4위.
- **미해결**: 모델은 습격을 여전히 1위로 본다. 제작자 경험(바닐라 습격 미사용)과 어긋난다. 원인 후보는 출혈 면역 몬스터의 던전 편중(v2 7절).


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### HM-017 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 기존 설정 비교에 따라 설명되지 않은 중독/출혈 저항 우위를 줄인다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `resistances/`
  - 원본: `resistances: .stun 40% .poison 40% .bleed 40% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 40%`
  - 현재: `resistances: .stun 40% .poison 30% .bleed 30% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 40%`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 1행; Git 원문 {"commit": "58a206d640f107da347acc230f675d5ffea1ed40", "summary": "조련사 HM-017 저항 정상화 + 저항 설계 축 분석(R-RES-01)"}
- 기존 주석 원문:
```text
// HM-017 저항: 중독 40 -> 30, 출혈 40 -> 30 (기준값 복귀). 설정 근거 없는 편차 제거. 노상강도는 "두껍게 덧댄 외투... 칼도 잘 박히지 않지만, 받아내기보다는 회피 선호"로 출혈 30인데, 같은 문장 구조의 조련사("낡은 제복... 받아내기보다는 아예 회피 선호")가 40인 건 모순. 함정 40(+30)은 야영 "늑대개를 정찰에 내보내거나 경비로 세울 수 있습니다"로 정당화되어 유지. 저항 총합 260(1위) -> 240. analysis/resistances.md
```

### HM-010 HM-011 HM-016 HM-018 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 표식·야수 조건부 역할을 남기되 직접 피해/출혈/도달 범위를 재배분한다. 실제 표식 피해60 고정과 옛40~60 메모를 구분한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/hounds_rush`
  - 원본: `combat_skill: .id "hounds_rush" .level 0 .type "ranged" .atk 85% .dmg 0% .crit 5% .launch 432 .target 1234 .is_crit_valid True  .effect "Beast Killer 1" "HM Dmg Marked 1" "Hound Bleed 1" .generation_guaranteed true`
  - 현재: `combat_skill: .id "hounds_rush" .level 0 .type "ranged" .atk 85% .dmg -25% .crit 5% .launch 4321 .target 234 .is_crit_valid True  .effect "Beast Killer 1" "HM Dmg Marked 1" "RB HM Hound Bleed 1" .generation_guaranteed true`
  - 원본: `combat_skill: .id "hounds_rush" .level 1 .type "ranged" .atk 90% .dmg 0% .crit 6% .launch 432 .target 1234 .is_crit_valid True  .effect "Beast Killer 2" "HM Dmg Marked 2" "Hound Bleed 2"`
  - 현재: `combat_skill: .id "hounds_rush" .level 1 .type "ranged" .atk 90% .dmg -25% .crit 6% .launch 4321 .target 234 .is_crit_valid True  .effect "Beast Killer 2" "HM Dmg Marked 1" "RB HM Hound Bleed 2"`
  - 원본: `combat_skill: .id "hounds_rush" .level 2 .type "ranged" .atk 95% .dmg 0% .crit 7% .launch 432 .target 1234 .is_crit_valid True  .effect "Beast Killer 3" "HM Dmg Marked 3" "Hound Bleed 3"`
  - 현재: `combat_skill: .id "hounds_rush" .level 2 .type "ranged" .atk 95% .dmg -25% .crit 7% .launch 4321 .target 234 .is_crit_valid True  .effect "Beast Killer 3" "HM Dmg Marked 1" "RB HM Hound Bleed 3"`
  - 원본: `combat_skill: .id "hounds_rush" .level 3 .type "ranged" .atk 100% .dmg 0% .crit 8% .launch 432 .target 1234 .is_crit_valid True  .effect "Beast Killer 4" "HM Dmg Marked 4" "Hound Bleed 4"`
  - 현재: `combat_skill: .id "hounds_rush" .level 3 .type "ranged" .atk 100% .dmg -25% .crit 8% .launch 4321 .target 234 .is_crit_valid True  .effect "Beast Killer 4" "HM Dmg Marked 1" "RB HM Hound Bleed 4"`
  - 원본: `combat_skill: .id "hounds_rush" .level 4 .type "ranged" .atk 105% .dmg 0% .crit 9% .launch 432 .target 1234 .is_crit_valid True  .effect "Beast Killer 5" "HM Dmg Marked 5" "Hound Bleed 5"`
  - 현재: `combat_skill: .id "hounds_rush" .level 4 .type "ranged" .atk 105% .dmg -25% .crit 9% .launch 4321 .target 234 .is_crit_valid True  .effect "Beast Killer 5" "HM Dmg Marked 1" "RB HM Hound Bleed 5"`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 22행; Git 원문 {"commit": "d5762d209d46704fa8d1f4aea12babd6af9f57c2", "summary": "조련사 HM-016 + 광역 지속 피해 재평가(R-VALUE-03) + 검증 목록 신설"}
- 기존 주석 원문:
```text
// HM-016 hounds_rush: 피해 0% -> -25%. 표식(+60%)+야수(+35%) 중첩 시 실전가 226%(조련사 1위). 조정 후 조건 없을 때 92%(평타 수준), 조건 충족 시 188%로 조건부 아키타입을 선명하게
```
- 기존 주석 원문:
```text
// HM-011 사냥개 돌진: 사용 432 -> 4321(1열 추가), 대상 1234 -> 234(1열 제거). 설정 "후열에 접근해" / 1열에서도 쓰되 1열이 메인이 되지 않게. 출혈 너프(HM-010)와 상쇄되어 피해 보정 0% 유지
```
- 기존 주석 원문:
```text
// MARK-01 hounds_rush: 표식 피해 60~100 -> 40~60 (RB HM Dmg Marked). 야수 특효+출혈과 중복, 조련사 강함 2위
```

### HM-012 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 1열 사용을 내주는 대신 광역 출혈 선택지를 보완한다. 최신 명중90은 사용자 출혈 기술 기준 메모에 근거한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/hounds_harry`
  - 원본: `combat_skill: .id "hounds_harry" .level 0 .type "ranged" .atk 85% .dmg -75% .crit -5% .launch 4321 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 1"`
  - 현재: `combat_skill: .id "hounds_harry" .level 0 .type "ranged" .atk 90% .dmg -70% .crit -5% .launch 432 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 1"`
  - 원본: `combat_skill: .id "hounds_harry" .level 1 .type "ranged" .atk 90% .dmg -75% .crit -4% .launch 4321 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 2"`
  - 현재: `combat_skill: .id "hounds_harry" .level 1 .type "ranged" .atk 95% .dmg -70% .crit -4% .launch 432 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 2"`
  - 원본: `combat_skill: .id "hounds_harry" .level 2 .type "ranged" .atk 95% .dmg -75% .crit -3% .launch 4321 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 3"`
  - 현재: `combat_skill: .id "hounds_harry" .level 2 .type "ranged" .atk 100% .dmg -70% .crit -3% .launch 432 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 3"`
  - 원본: `combat_skill: .id "hounds_harry" .level 3 .type "ranged" .atk 100% .dmg -75% .crit -2% .launch 4321 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 4"`
  - 현재: `combat_skill: .id "hounds_harry" .level 3 .type "ranged" .atk 105% .dmg -70% .crit -2% .launch 432 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 4"`
  - 원본: `combat_skill: .id "hounds_harry" .level 4 .type "ranged" .atk 105% .dmg -75% .crit -1% .launch 4321 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 5"`
  - 현재: `combat_skill: .id "hounds_harry" .level 4 .type "ranged" .atk 110% .dmg -70% .crit -1% .launch 432 .target ~1234 .is_crit_valid True  .effect "Harry Bleed 5"`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 32행; Git 원문 {"commit": "82e021e47a720a7e9565b5355463b605210dc2bd", "summary": "강함 순위 모델 v2 (R-VALUE-04): tools/strength.py 신설, 바닐라·RB 동시 계산"}
- 기존 주석 원문:
```text
// HM-012 사냥개 습격: 사용 4321 -> 432(1열 제거, 2열 메인 구조), 피해 -75% -> -70%. 광역 지속 피해는 전투 2.55라운드 안에 40%만 회수되어 R-STRAT-01에 역행 -> 실사용률 최하위. 사용 열 축소의 대가로 화력 보상
```
- 기존 주석 원문:
```text
// 명중 85 ->90 , 사유 : 출혈 기술 표준치가 90임
```

### HM-014 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 최고 레벨은 유지하고 저레벨 위험 경보의 스트레스 회복 불안정성을 줄인다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/howl`
  - 원본: `combat_skill: .id "howl" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "Hound Howl 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "howl" .level 0 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "RB HM Hound Howl 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "howl" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "Hound Howl 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "howl" .level 1 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "RB HM Hound Howl 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "howl" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "Hound Howl 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "howl" .level 2 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "RB HM Hound Howl 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "howl" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "Hound Howl 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "howl" .level 3 .type "ranged" .atk 0% .dmg 0% .crit 0% .launch 43 .target @~1234 .is_crit_valid True  .effect "RB HM Hound Howl 4" .is_stall_invalidating false`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 47행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Howl 1`
- 원본: `effect: .name "Hound Howl 1" .target "target" .curio_result_type "positive" .chance 66% .healstress 2	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hound Howl 1" .target "target" .curio_result_type "positive" .chance 74% .healstress 4	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 89행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-014 위험 경보: 회복 2 -> 4, 확률 66 -> 74. 5렙(6@74%)은 그대로 두고 저레벨 불안정성만 해소 (P-12)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Howl 2`
- 원본: `effect: .name "Hound Howl 2" .target "target" .curio_result_type "positive" .chance 68% .healstress 3	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hound Howl 2" .target "target" .curio_result_type "positive" .chance 74% .healstress 4	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 92행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-014 회복 3 -> 4, 확률 68 -> 74
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Howl 3`
- 원본: `effect: .name "Hound Howl 3" .target "target" .curio_result_type "positive" .chance 70% .healstress 4	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hound Howl 3" .target "target" .curio_result_type "positive" .chance 74% .healstress 5	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 95행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-014 회복 4 -> 5, 확률 70 -> 74
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Howl 4`
- 원본: `effect: .name "Hound Howl 4" .target "target" .curio_result_type "positive" .chance 72% .healstress 5	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hound Howl 4" .target "target" .curio_result_type "positive" .chance 74% .healstress 5	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 98행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-014 회복 5 -> 5(유지), 확률 72 -> 74
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Howl 1`
- 원본 (Hound Howl 1): `effect: .name "Hound Howl 1" .target "target" .curio_result_type "positive" .chance 66% .healstress 2	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "RB HM Hound Howl 1" .target "target" .curio_result_type "positive" .chance 74% .healstress 4	.on_hit true .on_miss false .queue true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 25행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Howl 2`
- 원본 (Hound Howl 2): `effect: .name "Hound Howl 2" .target "target" .curio_result_type "positive" .chance 68% .healstress 3	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "RB HM Hound Howl 2" .target "target" .curio_result_type "positive" .chance 74% .healstress 4	.on_hit true .on_miss false .queue true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 27행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Howl 3`
- 원본 (Hound Howl 3): `effect: .name "Hound Howl 3" .target "target" .curio_result_type "positive" .chance 70% .healstress 4	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "RB HM Hound Howl 3" .target "target" .curio_result_type "positive" .chance 74% .healstress 5	.on_hit true .on_miss false .queue true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 29행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Howl 4`
- 원본 (Hound Howl 4): `effect: .name "Hound Howl 4" .target "target" .curio_result_type "positive" .chance 72% .healstress 5	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "RB HM Hound Howl 4" .target "target" .curio_result_type "positive" .chance 74% .healstress 5	.on_hit true .on_miss false .queue true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 31행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}

### HM-015 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 주로 맞는 1열에서도 자기 회복을 사용할 수 있게 한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/lick_wounds`
  - 원본: `combat_skill: .id "lick_wounds" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 432 .target  .is_crit_valid True  .effect "Lick Wounds 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "lick_wounds" .level 0 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Lick Wounds 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "lick_wounds" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 432 .target  .is_crit_valid True  .effect "Lick Wounds 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "lick_wounds" .level 1 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Lick Wounds 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "lick_wounds" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 432 .target  .is_crit_valid True  .effect "Lick Wounds 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "lick_wounds" .level 2 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Lick Wounds 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "lick_wounds" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 432 .target  .is_crit_valid True  .effect "Lick Wounds 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "lick_wounds" .level 3 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Lick Wounds 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "lick_wounds" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 432 .target  .is_crit_valid True  .effect "Lick Wounds 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "lick_wounds" .level 4 .type "melee" .atk 0% .dmg 0% .crit 0% .launch 4321 .target  .is_crit_valid True  .effect "Lick Wounds 5" .is_stall_invalidating false`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 65행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-015 상처 핥기: 사용 432 -> 4321. 가장 많이 맞는 1열에서 자가 회복을 못 쓰는 구조 해소. 조련사 1열 사용 가능 기술 4개 -> 평균(4.7) 수준
```

### HM-013 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 3열 도달을 보존하고 명중/피해/기절 등급으로 대가를 낸다. 이중 우위 제거라는 옛 판단은 설계 의도이며 바닐라 보편 규칙은 아니다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/blackjack`
  - 원본: `combat_skill: .id "blackjack" .level 0 .type "melee" .atk 95% .dmg -65% .crit 5% .launch 21 .target 123 .is_crit_valid True  .effect "Hero Strong Stun 1"`
  - 현재: `combat_skill: .id "blackjack" .level 0 .type "melee" .atk 90% .dmg -80% .crit 5% .launch 21 .target 123 .is_crit_valid True  .effect "Stun 1"`
  - 원본: `combat_skill: .id "blackjack" .level 1 .type "melee" .atk 100% .dmg -65% .crit 6% .launch 21 .target 123 .is_crit_valid True  .effect "Hero Strong Stun 2"`
  - 현재: `combat_skill: .id "blackjack" .level 1 .type "melee" .atk 95% .dmg -80% .crit 6% .launch 21 .target 123 .is_crit_valid True  .effect "Stun 2"`
  - 원본: `combat_skill: .id "blackjack" .level 2 .type "melee" .atk 105% .dmg -65% .crit 7% .launch 21 .target 123 .is_crit_valid True  .effect "Hero Strong Stun 3"`
  - 현재: `combat_skill: .id "blackjack" .level 2 .type "melee" .atk 100% .dmg -80% .crit 7% .launch 21 .target 123 .is_crit_valid True  .effect "Stun 3"`
  - 원본: `combat_skill: .id "blackjack" .level 3 .type "melee" .atk 110% .dmg -65% .crit 8% .launch 21 .target 123 .is_crit_valid True  .effect "Hero Strong Stun 4"`
  - 현재: `combat_skill: .id "blackjack" .level 3 .type "melee" .atk 105% .dmg -80% .crit 8% .launch 21 .target 123 .is_crit_valid True  .effect "Stun 4"`
  - 원본: `combat_skill: .id "blackjack" .level 4 .type "melee" .atk 115% .dmg -65% .crit 9% .launch 21 .target 123 .is_crit_valid True  .effect "Hero Strong Stun 5"`
  - 현재: `combat_skill: .id "blackjack" .level 4 .type "melee" .atk 110% .dmg -80% .crit 9% .launch 21 .target 123 .is_crit_valid True  .effect "Stun 5"`
- 출처: `heroes/houndmaster/houndmaster.info.darkest`, 주석 추가 전 73행; Git 원문 {"commit": "6381c531a2e253486cc7222d22bd079047d3f198", "summary": "R-DATA-01 중복 효과 금지 + 도구가 기존 효과를 자동 재사용"}
- 기존 주석 원문:
```text
// HM-013 둔기 강타: 1렙 명중 95 -> 90(표준), 피해 -65% -> -80%. 대상 1/2/3 유지. 설정 "곤봉은 효과적으로 기절시키지만 진짜 치명타는 사냥개가 먹입니다" -> 3열 도달과 기절은 남기고 화력만 제거
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hero Strong Stun 1`
- 원본: `effect: .name "Hero Strong Stun 1" .target "target" .curio_result_type "negative" .chance 110% .stun 1	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hero Strong Stun 1" .target "target" .curio_result_type "negative" .chance 100% .stun 1	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 143행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-013 둔기 강타 기절: 강한 기절(110) -> 기본 기절(100) 등급으로 정상화. 조련사만 3열까지 닿는데 등급까지 상위인 중복 우위 제거
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hero Strong Stun 2`
- 원본: `effect: .name "Hero Strong Stun 2" .target "target" .curio_result_type "negative" .chance 120% .stun 1	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hero Strong Stun 2" .target "target" .curio_result_type "negative" .chance 110% .stun 1	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 147행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-013 120 -> 110
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hero Strong Stun 3`
- 원본: `effect: .name "Hero Strong Stun 3" .target "target" .curio_result_type "negative" .chance 130% .stun 1	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hero Strong Stun 3" .target "target" .curio_result_type "negative" .chance 120% .stun 1	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 151행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-013 130 -> 120
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hero Strong Stun 4`
- 원본: `effect: .name "Hero Strong Stun 4" .target "target" .curio_result_type "negative" .chance 140% .stun 1	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hero Strong Stun 4" .target "target" .curio_result_type "negative" .chance 130% .stun 1	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 155행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-013 140 -> 130
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hero Strong Stun 5`
- 원본: `effect: .name "Hero Strong Stun 5" .target "target" .curio_result_type "negative" .chance 150% .stun 1	.on_hit true .on_miss false .queue true`
- 현재: `effect: .name "Hero Strong Stun 5" .target "target" .curio_result_type "negative" .chance 140% .stun 1	.on_hit true .on_miss false .queue true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 159행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-013 150 -> 140
```

### HM-010 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 표식·야수 조건부 역할을 남기되 직접 피해/출혈/도달 범위를 재배분한다. 실제 표식 피해60 고정과 옛40~60 메모를 구분한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Bleed 1`
- 원본: `effect: .name "Hound Bleed 1" .target "target" .curio_result_type "negative" .chance 100%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "Hound Bleed 1" .target "target" .curio_result_type "negative" .chance 100%  .dotBleed 1 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 23행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-010 사냥개 돌진 출혈: 지속 3턴 -> 1턴. 턴당 1/1/1/2/2 -> 1/1/2/2/3 (5렙 총량 6 -> 3). 치명타 시 1->2턴
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Bleed 2`
- 원본: `effect: .name "Hound Bleed 2" .target "target" .curio_result_type "negative" .chance 110%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "Hound Bleed 2" .target "target" .curio_result_type "negative" .chance 110%  .dotBleed 1 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 30행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-010 지속 3 -> 1
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Bleed 3`
- 원본: `effect: .name "Hound Bleed 3" .target "target" .curio_result_type "negative" .chance 120%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "Hound Bleed 3" .target "target" .curio_result_type "negative" .chance 120%  .dotBleed 2 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 37행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-010 지속 3 -> 1, 턴당 1 -> 2
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Bleed 4`
- 원본: `effect: .name "Hound Bleed 4" .target "target" .curio_result_type "negative" .chance 130%  .dotBleed 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "Hound Bleed 4" .target "target" .curio_result_type "negative" .chance 130%  .dotBleed 2 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 44행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Hound Bleed 5`
- 원본: `effect: .name "Hound Bleed 5" .target "target" .curio_result_type "negative" .chance 140%  .dotBleed 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "Hound Bleed 5" .target "target" .curio_result_type "negative" .chance 140%  .dotBleed 3 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 52행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// HM-010 지속 3 -> 1, 턴당 2 -> 3
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Bleed 1`
- 원본 (Hound Bleed 1): `effect: .name "Hound Bleed 1" .target "target" .curio_result_type "negative" .chance 100%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB HM Hound Bleed 1" .target "target" .curio_result_type "negative" .chance 100%  .dotBleed 1 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Bleed 2`
- 원본 (Hound Bleed 2): `effect: .name "Hound Bleed 2" .target "target" .curio_result_type "negative" .chance 110%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB HM Hound Bleed 2" .target "target" .curio_result_type "negative" .chance 110%  .dotBleed 1 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 17행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Bleed 3`
- 원본 (Hound Bleed 3): `effect: .name "Hound Bleed 3" .target "target" .curio_result_type "negative" .chance 120%  .dotBleed 1 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB HM Hound Bleed 3" .target "target" .curio_result_type "negative" .chance 120%  .dotBleed 2 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 19행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Bleed 4`
- 원본 (Hound Bleed 4): `effect: .name "Hound Bleed 4" .target "target" .curio_result_type "negative" .chance 130%  .dotBleed 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB HM Hound Bleed 4" .target "target" .curio_result_type "negative" .chance 130%  .dotBleed 2 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 21행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB HM Hound Bleed 5`
- 원본 (Hound Bleed 5): `effect: .name "Hound Bleed 5" .target "target" .curio_result_type "negative" .chance 140%  .dotBleed 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true`
- 현재: `effect: .name "RB HM Hound Bleed 5" .target "target" .curio_result_type "negative" .chance 140%  .dotBleed 3 .duration 1	.on_hit true .on_miss false .can_apply_on_death true`
- 출처: `effects/rebalance_houndmaster.effects.darkest`, 주석 추가 전 23행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}

### HM-018 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 표식/야수/출혈/간식의 조건부 중첩을 줄이고 서브 표식 딜러로 재배분한 실제 표식60 고정을 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HM Dmg Marked 2`
- 원본: `effect: .name "HM Dmg Marked 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 70%  .damage_high_multiply 70%	.on_hit true .on_miss false`
- 현재: `effect: .name "HM Dmg Marked 2".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 28행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HM Dmg Marked 3`
- 원본: `effect: .name "HM Dmg Marked 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 80%  .damage_high_multiply 80%  .on_hit true .on_miss false`
- 현재: `effect: .name "HM Dmg Marked 3".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60%  .on_hit true .on_miss false`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 35행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HM Dmg Marked 4`
- 원본: `effect: .name "HM Dmg Marked 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 90%  .damage_high_multiply 90%  .on_hit true .on_miss false`
- 현재: `effect: .name "HM Dmg Marked 4".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60%  .on_hit true .on_miss false`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 42행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `HM Dmg Marked 5`
- 원본: `effect: .name "HM Dmg Marked 5".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 100%  .damage_high_multiply 100% .on_hit true .on_miss false`
- 현재: `effect: .name "HM Dmg Marked 5".target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"  .combat_stat_buff 1 .damage_low_multiply 60%  .damage_high_multiply 60% .on_hit true .on_miss false`
- 출처: `heroes/houndmaster/houndmaster.effects_edit.txt`, 주석 추가 전 49행; Git 원문 {"commit": "00fb87c575ff90e81960a1bfd767461b04c04c64", "summary": "조련사 전면 조정 (HM-010~015) + R-STRAT-02 광역 지속 피해 재평가"}
- 기존 주석 원문:
```text
// MARK-01 HM Dmg Marked: 표식 피해 60~100 -> 60 고정(전 레벨). 야수 특효+출혈+개 간식과 중복, 조련사 강함 2위
```


### HM-019 사냥개 돌진: 모든 열 사용·모든 적 열 대상, 낮은 기본 피해와 표식 +60 고정 유지 (2026-10-06)
- 상태: 적용 (사용자 명시 승인)
- 분류: 의도적 예외 / HM-011 대상 제한을 대체
- 목표: G-00 조합 다양성; P-11 상향·하향의 맞물림과 총량·체감 난이도 보존.
- 변경 (기술 1~5레벨): 사용 4321 유지, 대상 234 → 1234. 단일 대상 선택이며 광역 공격이 아니다. 기본 피해 −25% 유지, 표식 대상 추가 피해 +60% 전 레벨 고정 유지.
- 현재 적용 전 확인: 사용 열과 표식 +60은 이미 실행 파일에 반영되어 있었다. 이번 수치 변경은 대상에 1열을 추가한 5행뿐이며 새로운 표식 하향을 적용한 것은 아니다.
- 의도: 어느 대열에서도 원하는 적을 공격할 수 있는 범용성과 보호·스트레스 회복·자가 회복 지원을 직업의 강점으로 둔다. 평상시 직접 피해는 낮게 유지하고, 표식·야수 특효·제한된 개 간식으로 조건부 화력을 보완한다.
- 이력: HM-010 출혈 단축, HM-016 기본 피해 −25%, HM-018 표식 +60 고정은 유지한다. HM-011의 적 1열 제외는 이번 승인으로 대체한다. 이전 한국어 메모는 역사 기록으로 원문 보존한다.
- 총량 판단: 바닐라 대비 기존 기본 피해·출혈·표식 하향과 이번 범용성 확대를 함께 검토한다. 바로 직전 실행값 대비 이번 변경 자체는 대상 확장의 상향이다. 일대일 수치 상쇄나 원정 난이도 보존이 입증된 것은 아니다.
- 개 간식: 설치 원본 dog_treats는 3턴 동안 명중 +15, 피해 하한·상한 +50%. 소모성 화력 보완이며 지속 화력의 자동 보증으로 계산하지 않는다.
- 고정 장신구 확인: 가시 목걸이 피해 +20%/출혈 확률 +30%, 보호 목걸이 피해 −15%, 원거리 명중 +15의 CC 장신구와 개 간식 보유 시 출혈 확률 +50%의 수정 장신구 경로를 유지한다. 관련 효과나 장신구는 변경하지 않는다.
- 기술 1레벨 명중 85, 기술 치명타 보정 +5% 유지. 야수 특효·출혈량/확률·무기·기절·지원 기술은 변경하지 않는다.
- 검증: 준비 사본과 설치 파일에서 5개 기술 행/모든 열 단일 선택/표식 효과 +60/요청 외 수치 보존/효과 참조/20영웅 의도 주석/파일 목록 크기를 검사한다. 게임에서 실제 대상 선택·이펙트·툴팁 시험은 미실시.
- 사용자 원문:

> 사냥개 조련사 사냥개 돌진 전열 사용 전열 타겟으로 바꾸자 그럼 범용성의 끝판왕 기술로 바꾸고 대신에 표식 대상 공격력을 전 레벨 60으로 고정 딜이 약해야만해 사냥개조련사는 범용성과 서포트 능력이 고트인 대신에 그리고 어차피 개간식 통해서 데미지 폭증 시킬 수도 있으니 큰 너프는 아닐거야


### HM-020 휘파람: 방어 감소 → 받는 치명타 +15/16/17/18/20% (2026-10-11)
- 상태: 적용 (제작자 결정, 수치 제작자 안)
- 문제: 방어 −20~−30%는 방어 0인 적(56%)에게 효과 0이었고(V-17), 현상금 사냥꾼 죽음의 표식과 겹쳤다.
- 변경: `Hound Debuff 1~5` → 신규 `RB HM Whistle Vuln 1~5`(받는 치명타 +15/16/17/18/20%, 3턴, 확률 130~170%). 표식은 유지.
- 근거: 사냥개가 약점을 물고 늘어진다(P-19). 받는 치명타 증가는 포도탄·포효에 있는 기존 메커니즘이라 새 설명이 필요 없다.
- 영향(5렙 %p): −42.6 → **−41.6**(같은 세기, 방어 0인 적에게도 들어감). 모델은 치명타를 피해로만 세어 치명 부가 효과(직업 치명 효과·스트레스 회복·효과 확률·지속 피해 연장)를 빼므로 실제는 더 크다.

### HM-021 휘파람: 받는 치명타 → 적 명중 −25/26/27/28/30 (2026-10-11)
- 상태: 적용 (제작자 결정 "명중 감소로", 수치 제안 승인)
- 문제: HM-020의 받는 치명타 +15~20%가 총사 스키트 사격(표식 + 받는 치명타 +12%)과 겹쳤다.
- 변경: 신규 효과 `RB HM Whistle Distract 1~5`(명중 −25/26/27/28/30, 3턴, 확률 130~170% 그대로). 표식 유지.
- 근거: 표식 기술 중 유일한 방어형(경비견·상처 핥기의 보호형 조련사와 일치, P-19). 표식 3종이 −30으로 짝 — 석궁사수 회피, 현상금 사냥꾼 방어, 조련사 명중. 매 레벨 성장.
- 영향(5렙, R-VALUE-17): +28 → **+35%p**(약화 +104, 표식 +30). 조련사 10위 그대로.

### HM-022 둔기 강타: 피해 −80% → −65% (2026-10-14)
- 상태: 적용 (제작자 결정 "−65에 명중 90, 바닐라에서 명중 5랑 강한 스턴만 깎기")
- 변경: 피해 −80% → −65%(바닐라 값). 1렙 명중 90·일반 기절(1렙 100%)은 HM-013 그대로.
- 근거: HM-013은 명중·피해·기절 등급 세 가지를 모두 깎아 대상 1·2·3열 기절 4종 중 최하위(모델(5렙) +34%p)가 됐다. 3열 도달의 대가는 명중 −5와 강한 기절 제거로 충분.
- 영향: 모델(5렙) +34 → **+53%p** (바닐라 +75%p). 비교표 `design/analysis/stun_target123.md`.

### HM-023 사냥개 돌진: 1렙 명중 85 → 90, 출혈 지속 1 → 2턴 (2026-10-14)
- 상태: 적용 (제작자 결정 "피해 −25로 대폭 감소시켰으니 출혈 11223, 2턴, 명중 90")
- 변경: 출혈 턴당 1/1/2/2/3(그대로)의 지속 1 → 2턴(RB HM Hound Bleed 1~5). 1렙 명중 85 → 90. 피해 −25%·표식 특효·야수 특효 그대로.

### HM-024 둔기 강타: 피해 −65% → −50% (2026-10-15)
- 상태: 적용 (제작자 결정 2026-10-15)
- 1렙 명중 90·일반 기절 그대로.

### HM-025 경비견: 자기 회피 +10~20 → +20/22/25/27/30 (2026-10-15)
- 상태: 적용 (제작자 동의)
- 근거: 길드 문구 "약자를 보호". 보호 중인 영웅은 공격을 약 1.59배 받는데 모델은 회피 버프에 이를 반영하지 않아 실제 가치가 더 크다. 모델(5렙) +1 → +38(5렙 회피 +30). 조련사 총점 53 그대로(경비견은 주력 행동 밖).
- 방향: 조련사 패치는 딜을 낮추고 유틸을 올린다(intent.md P-24).

### HM-026 울부짖기: 1~4렙 확률 74% 고정 → 70/71/72/73% (2026-10-17)
- 상태: 적용 (제작자 결정 "70 71 72 73 74 하면 되는 거 아님?")
- 근거: HM-014는 1~4렙 확률을 74%로 고정해 1→2렙·3→4렙 성장이 없었다(회복도 4/4/5/5). 확률이 매 레벨 +1%p 오르게 해 성장 체감을 살린다. 창작마당판에도 같은 값.

### HM-024 보충 근거: 둔기 강타 피해 −50% (2026-10-17)
- [제작자] 명중(95 → 90)과 강한 기절을 없애 꽤 많이 하향했으므로 피해를 올렸다. R-STUN-02(3열 기절은 피해 낮게)의 예외 — 다른 두 축으로 이미 대가를 치름.

### HM-018·MARK-01 보충 근거: 사냥개 돌진 표식 +60% 고정 (2026-10-17, 창작마당 감사 답변)
- [제작자] 조련사 방향(P-24)이 딜 하향·유틸 상향이다. 표식 특효 성장(+60→100%, R-EFF-05)을 없앤 것은 딜 하향 방향의 의도적 이탈.
### HM-027 기록: 사냥개 습격 명중 85 → 90, 피해 −75% → −70%·사용 열 4321 → 432 (2026-10-17, 창작마당 감사 답변)
- [제작자] 사냥개 습격은 딜을 줄이고 명중을 올렸다(P-24, 광역 출혈의 적용 안정성). 기존에 변경 ID 없이 들어가 있던 값.
- 정정 (2026-10-17): 피해 −75% → −70%는 피해 **상향**이다(딜을 줄인 것이 아님). 바뀐 것은 명중 +5·피해 +5%p 상향과 사용 열 1열 제거(HM-012)이고, 데이터와 why.json("피해를 조금 올리고")이 이와 같다.

### HM-028 목표물 지정 명중 감소 확률 정상화 130~170% → 100~140% (2026-10-21, test)
- 제작자: 근거 없는 조련사 특혜 정상화. 바닐라 휘파람 효과의 130~170%를 이어받았던 것. 수치(명중 −25~−30%, 3턴)는 그대로.

### HM-029 사냥개 돌진: 출혈 특화 (2026-10-23, test)
- 제작자: "딜을 더 깎고 출혈 쪽이 더 부각되게. 장신구가 그렇게 프레임을 깔아놨다." 계기: 창작마당 Rlver 댓글("피해를 낮추면서 출혈을 강화해 다른 장신구·기술이 발휘되게").
- 변경: 피해 −25% → −50%, 출혈 1/1/2/2/3 × 2턴 → 3/3/4/4/5 × 3턴(확률 100~140% 그대로).
- 비교(모델(5렙), 표준 평타 기준): 지금 +93 / −40%·2~4 +115 / **−50%·3~5 +120** / −40%·3~5 +138%p(과함). 출혈을 거는 영웅 기술 13개 전수 비교: 1렙 출혈 3은 광대 사지 절단(2·3열, −33%)·야만인 출혈 공격(1열, 0%)과 같고, 돌진은 1~4열 어디서나라 피해를 더 낮춤.
- 근거: lore_audit_B.md — 출혈 장신구 3종·핏빛 궁정 세트(출혈 대상 피해 +25%)·직업 치명(출혈 확률 +20)이 출혈을 전제하는데 출혈원이 약했다(HM-023 주석 "1→2턴"은 바닐라 3턴 대비 하향이었음).

### HM-030 사냥개 습격: 출혈 특화 (2026-10-23, test)
- 피해 −70% → −80%, 출혈 1/1/2/2/3 → 2/2/3/3/4 × 3턴(확률 110~150% 유지, `RB HM Harry Bleed 1~5`).
- 모델(5렙, 표준): 지금 +85 / −85% +74 / **−80% +87** / −90% +61%p. 가치는 그대로, 직접 6.1 : 출혈 6.7 → 4.1 : 8.9.
- 근거: analysis/bleed_distribution.md — 후열에서 1~4열 어디든 출혈을 거는 영웅은 조련사뿐(겹침 없음). 조련사 = 원거리 출혈 부여자, 끝장내기·야만인 치명·면도날 힐트가 받아먹는 구조.
