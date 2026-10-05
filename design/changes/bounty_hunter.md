# 현상금 사냥꾼 (bounty_hunter) 변경 항목

바닐라 수치: `heroes/bounty_hunter/bounty_hunter.vanilla.txt`

---

### BH-000 방향성: 출혈 딜러 + 후반부 강화, "강약약강" 아키타입
- 상태: 방향 (세부 항목은 BH-001~)
- 분류: 방향 설정
- 목표: G-01(영웅 다양성), G-02(기술 다양성)
- 사용자 메모 (원문):
  > 방향성 : 출혈 딜러로 변경 , 반격 딜러(노상, 결투가), 방관 딜러에 비해 후반부에 너무 구림 -> 후반부 강화 (1. 스턴 킬러 깡딜 증가, 2. ?)
- 사용자 의견 (대화 원문, 2026-09-15):
  > 스턴 당한 적한테 딜링을 넣는 거 자체가 사실 굉장한 기대값을 포기하는거거든 현상금사냥꾼은 다른 반격딜러 혹은 실브 같이 방어구 관통이 없기 때문에 후반 갈수록 사장되는 딜러거든 그래서 버프 필요성이 있다고 봐 나는.

  > 현상금은 방어관통은 없는 대신에 -> 방어 떡칠한테는 약함. 다만 방어가 없는 다른 애들을 확실하게 정리가능한 화끈한 화력 즉 강약약강의 아키타입으로 만들면 좋을 것 같아

  > 현상금 사냥꾼을 버프 하려고 결투가(최후의 일격 같은 사기 스킬)나 노상강도(영거리 사격 같은 사기스킬)에 맞춰서 버프를 해버리면 난이도 자체가 쉬워지는 참사가 일어날 것 같아서
- 데이터 확인 (`analysis/dealers.md`, `analysis/hero_power.md`):
  - **가격:** 현상금 사냥꾼 공격 기술은 정가(+5.7, +6.0)다. 노상강도는 가격 초과 기술이 5개(+19 ~ +51)다.
  - **방어도:**
    - 몬스터 방어도는 던전 등급에 따라 오르지 않는다. 후반에 오르는 것은 체력(×1.85)과 회피(+21)다.
    - 방어도를 가진 몬스터는 등급과 무관하게 40%다. 방어 무시가 없다는 약점 자체는 성립한다.
  - **보정: 방어도 대응 수단이 전혀 없는 것은 아니다.** 죽음의 표식이 대상 방어도를 −10→−20% 깎는다(3턴). "준비하면 장갑도 뚫는다"가 이미 원본 설계에 들어 있다.
  - **강약약강은 방어도 계산 방식에서 저절로 생긴다.** 방어도는 피해를 비율로 줄인다. 따라서 배율이 높은 딜러일수록 방어도 높은 적에게 잃는 절대 피해가 크고, 방어 무시 딜러와의 격차도 커진다.
  - **구현 제약:** "대상 방어도 조건"은 엔진에 없다(`keyStatus`: 표식·중독·출혈·기절·화상, `monsterType`: 인간·짐승·불경·이형). 아키타입은 방어 무시 없이 기본 배율을 높이는 방식으로 만든다.
- **기준선 (사용자 결정):** 버프 목표는 가격표 초과 기술(노상강도 영거리 사격 +51, 결투가 최후의 일격 등)이 아니다. 조건부 딜러 상위권(방패 파괴자 휘감기 20.8, 조련사 19.5, 석궁사수 19.4)에 맞춘다.

### BH-001 끝장내기: 출혈 대상 추가 피해 (신규 효과)
- 상태: 적용 (게임 테스트 전)
- 분류: 신규규칙 (원본 대칭 복원)
- 목표: G-01, G-02
- 의도: 끝장내기가 기절 대상뿐 아니라 출혈 대상에게도 추가 피해를 준다. 현상금 사냥꾼 자신의 출혈 기술(마름쇠)과 파티의 출혈 영웅과 연계하는 딜러로 만든다.
- 근거:
  - **원본 대칭:** 도굴꾼에게는 중독 대상 추가 피해(Poison Killer 1~5: +20/23/26/29/33%)가 있다. 출혈에 대응하는 효과는 기술에 없다.
  - **미사용 원본 흔적:** 원본 효과 파일에 `BleedKiller`(+50%)가 정의돼 있지만 어떤 기술도 쓰지 않는다.
  - **핏빛 궁정 선례:** 세트 "저들은. 대가를. 치를 것이다."
    - 범죄 거물의 어금니들: 출혈 대상 피해 +20%
    - 세트 효과: 출혈 대상 치명타 +5
  - **시너지 풀:** 출혈을 거는 영웅은 8명이다. 중독을 거는 영웅은 5명이다.
  - **제약:** 영웅 등급 몬스터의 출혈 면역은 25%다.
- 변경:
  - `effects/rebalance_bounty_hunter.effects.darkest`에 신규 효과 `RB BH Bleed Killer 1~5`를 추가했다(+20/23/26/29/33%).
  - 끝장내기 1~5레벨 `.effect`에 `"RB BH Bleed Killer N"`을 추가했다. 기존 "Stun Killer N"은 유지한다.
  - 기절 + 출혈 동시 충족 시 두 배율이 합산되는지는 게임 테스트로 확인한다.
- 따르는 원칙:
  - R-TRADE-01: 조건부 보너스는 거의 무료
  - R-EFF-05: 조건부 피해는 레벨마다 성장
- 어기는 원칙: 없음
- 영향: BH-002와 합치면 끝장내기 조건이 2개가 된다.
- 수치 편집: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt` 맨 아래 "모드 신규 효과" 구역
- 검증: (플레이 후 기록)

### BH-002 끝장내기: 기절 대상 추가 피해 강화 (제안)
- 상태: 검토 (수치 미정, 사용자가 effects_edit에서 결정)
- 분류: 원칙복원
- 목표: G-01
- 의도: 기절 대상 추가 피해를 조건 달성 난이도와 기회비용에 맞게 올린다.
- 사용자 근거: BH-000 인용 (기절한 적을 때리는 것은 기대값을 포기하는 선택)
- 데이터 근거:
  - **조건 난이도와 보너스가 거꾸로다.**
    - 현상금 수거는 표식 대상에 +90%다. 표식은 저항이 없고, 명중 120 기준 약 95%로 걸린다.
    - 끝장내기는 기절 대상에 +25→60%다. 기절은 영웅 등급 기준 약 44~56% 판정에 성공해야 걸린다(`analysis/stun.md`).
  - **5레벨 영웅 던전 기대 피해** (명중 105 → 82.5%, 무기 평균 12):

    | 조건 | 기대 피해 |
    |---|---|
    | 끝장내기 기본 | 9.9 |
    | 기절 +60% (원본) | 15.8 |
    | 기절 +90% | 18.8 |

- 제안 수치
  - **A안 (권장):** 50/60/70/80/90%. 5레벨을 같은 영웅의 표식 조건 +90%에 맞춘다. 18.8은 BH-000 기준선(조건부 딜러 상위권) 안이다.
  - **B안 (기각):** 피해 %는 유지하고 기절 대상 치명타를 추가한다(결투가 방식).
    - 기각 사유, 사용자 원문:
      > 기절 대상 치명타는 결투가가 사기라서 받은거 같고 그게 똑같이 있으면 안되지..
    - 데이터: 결투가 최후의 일격의 가치는 피해(5레벨 기절 대상 약 5.8)가 아니다. 확정 치명타, 방어 무시, 처치 시 추가 행동에 있다. 이는 가격표 모델 밖의 가치다. 같은 장치를 주면 영웅 정체성이 겹친다(G-01 위반).
- 편집 방법: `bounty_hunter.effects_edit.txt`의 "끝장내기" 구역에서 `Stun Killer N` 줄의 `.damage_low_multiply` / `.damage_high_multiply`를 고친다. 적용 시 자동으로 `RB BH Stun Killer N`이 된다.
- 영향: BH-001과 합산 시 끝장내기 조건 2개. 가격표(R-TRADE-01) 재계산 필요.

### BH-003 현상금 수거: 표식 대상 추가 피해를 레벨마다 성장 (제안)
- 상태: 검토
- 분류: 원칙복원 (R-EFF-05 예외 해소)
- 목표: G-01
- 의도: "후반에 사장된다"를 원인에서 고친다. 현상금 사냥꾼만 표식 보너스가 레벨과 무관하게 고정이다.
- 근거 (R-EFF-05):

  | 영웅 | 표식 조건 추가 피해 (1→5레벨) |
  |---|---|
  | 조련사 | +60→100 |
  | 석궁사수·총사 | +50→100 (치명타 +9→13) |
  | 방패 파괴자 | +40→60 |
  | 노상강도 | +25→50 |
  | 도굴꾼 | +25→40 |
  | **현상금 사냥꾼** | **+90→90 (고정)** |

  - 조건부 피해 효과 20종 중 고정은 현상금 사냥꾼 표식과 결투가 기절 치명타 2개뿐이다.
  - 현상금 사냥꾼은 1레벨 표식 보너스가 가장 크다. 5레벨에서는 조련사·석궁사수(+100)보다 작다. 초반형 설계가 후반 약세의 원인 중 하나다.
- 제안 수치
  - A안 (권장): 90/95/100/105/110%
    - 1레벨 정체성(+90)을 유지하고 5레벨만 +20% 올린다.
    - 5레벨 표식 대상 기대 피해 18.8 → 20.8. 인간 킬러는 제외한 값이다.
    - 20.8은 방패 파괴자 휘감기와 같은 수준으로, BH-000 기준선의 상단이다.
  - 조련사식 +10/레벨(90→130)은 기준선을 넘으므로 제외한다.
- 구현: 원본은 5레벨 모두 같은 효과 "BH Dmg Marked"를 쓴다. 레벨별 신규 효과 `RB BH Dmg Marked 1~5`가 필요하다(BH-001과 같은 방식).
- 영향: 인간 킬러(+35)와 합산되는지는 게임 테스트로 확인해야 한다. 합산되면 5레벨 인간 표식 대상은 +145%다.

### BH-004 무기 피해 성장 15% → 20%, 매혹 시 열 1 → 2 (제안)
- 상태: 검토
- 분류: 원칙복원 (규칙 안에서 조정)
- 목표: G-01
- 의도: 전열 탱커 성장률(15%)을 받으면서 탱커 체력은 없는 구조를 바로잡는다.
- 근거:
  - **R-GROW-01:** 무기 피해 성장 15%는 "헤비 태그 + 매혹 시 열 1"일 때만 적용된다. 해당 영웅은 나병환자·성전사·야만인·중보병·현상금 사냥꾼이다.
  - 같은 그룹의 1레벨 체력은 나병환자 35, 성전사 33, 중보병 31, 야만인 26이다. **현상금 사냥꾼은 25**다.
  - 현상금 사냥꾼 5레벨 피해 성장 ×1.60은 20명 중 두 번째로 낮다. 가장 낮은 영웅은 중보병 ×1.57이다.
  - 기본 능력치 자체는 적정하다. R-BASE-01 회귀(체력 = 22.3 − 1.42×속도 + 1.29×평균 피해)로 계산한 예측 대비 +0.2다.
  - **역할 가중 최적 열이 2열**이다(`analysis/hero_ranks.md` 2절). 매혹 시 열 2가 데이터와 맞는다.
  - 선례: 방패 파괴자는 같은 기본 피해 5-10, 헤비, 매혹 시 열 2, 성장 20%다.
- 변경안:
  - `controlled: .target_rank 1` → `2`
  - 무기 5-10 / 6-12 / 7-13 / 7-15 / 8-16 → 5-10 / 6-12 / 7-14 / 8-16 / **9-18**
  - 5레벨 평균 피해 12.0 → 13.5 (+12.5%)
- 따르는 원칙: R-GROW-01. 두 값을 함께 바꾸므로 규칙 예외가 생기지 않는다.
- 영향: 기술 기대 피해 전부 +12.5%. BH-002·003과 합치면 과할 수 있으므로 셋 중 조합을 고른다.

### BH-003 / BH-004 추가 검토 (2026-09-15)
- 사용자 의견 (원문):
  > 방향성은 표식 데미지를 최대한 다 늘려서 전부 활용 가능하게 만드는 거야 내 생각에 조련사를 40~60 정도로 고정시켜놓고 현상금 사냥꾼은 90 ~ 110 까지 늘려도 되지 않을까 싶은데 왜냐하면 어차피 1,2열만 타격이잖아 다른애들은 다 전열 타격인데 현상금은 1,2열만 타격이라 가장 쌔야하지 않을까?

  > 현상금 사냥꾼을 20% 20% 로 최소 최대 늘려도 사기 아니야? 확실해? 장신구까지 한번 고려해볼래?
- **BH-003 판단: 90→110 동의.**
  - 표식 보상 기술 중 대상이 1·2열뿐인 기술은 현상금 수거 하나다. 나머지는 2·3·4열 또는 1~4열을 친다. 사거리가 가장 좁으므로 보상이 가장 커도 된다.
  - 5레벨 20.8은 석궁사수 저격(19.4)을 약간 넘는 1위이며 기준선(19~21) 상단이다.
  - 좁은 사거리의 해법(이리 오너라: 3·4열을 당겨 2턴 표식)이 이미 자기 기술에 있어 조합이 완결된다.
- **조련사 40→60 판단: 제안 보류.** `houndmaster.md` HM-001 참고.
- **BH-004 판단: 단독 적용은 적정, 표식 파티 + 전용 장신구 2개에서는 과할 수 있음.** 상세: `analysis/hero_power.md` 7절.
  - 스스로 표식: 턴당 17.4. 노상강도 순환 18.3보다 낮다.
  - 파티 표식: 매 턴 26.2, 비교 대상 중 1타 최고.
  - 순위 모델: 15위 → 12위 (BH-002·003을 모두 넣으면 10위)
- 권장 순서: BH-004 → 플레이 테스트 → BH-003 여부 결정. 셋을 한 번에 넣지 않는다.

### BH-005 마름쇠: 피해 보정 −95% → −70% (제안)
- 상태: 제안 (BH-006 권장 패키지 포함)
- 분류: 원칙복원 (가격표 R-TRADE-01)
- 목표: G-02, G-03
- 변경안: 1~5레벨 `.dmg -95%` → `.dmg -70%`. 효과(출혈, 속도 −8, 받는 피해 +20%)는 유지한다.
- 근거:
  - 가격표 −25 과소 → 0(정가).
  - 5레벨 직접 피해 0.5 → 약 3. 모델 가치 12.0 → 14.3.
  - 사용 2·3·4열 → 대상 3·4열이다. 3열에 서도 할 일이 생긴다(G-03, 3열 점수 11/13).
- 사냥 순환: 마름쇠(뒷줄 출혈 + 받는 피해 +20%) → 이리 오너라(1·2열로 당기기 + 2턴 표식) → 끝장내기(출혈·기절 킬러) 또는 현상금 수거(표식 보상).
- 강약약강 유지: 방어 무시는 추가하지 않는다.

### BH-006 상향 패키지 비교와 권장안 (2026-09-15)
- 사용자 요청 (원문):
  > 현상금 사냥꾼 합리적 상향안
- **판단 기준**
  1. 순위: 약함(15위)에서 중위권 상단으로. 노상강도 하향(HWY-001~003) 후 순위(약 5위)보다 아래
  2. 모델 가정을 바꿔도 같은 구간(`analysis/hero_power.md` 9절)
  3. 혼자 싸울 때 조건부 1타가 기준선 상단(약 22)을 넘지 않음
  4. 장신구 최상 조합(범죄 거물의 어금니들 + 부상의 투구)에서도 극단적 폭발을 피함
  5. 최소 변경(P-09), 새 원칙 예외를 만들지 않음

**비교** (5레벨, 1타는 치명타·방어도 제외. 순위는 노상강도 하향 반영 여부와 무관하게 같았다)

| 안 | 구성 | 순위 기본 / 보수적 | 가정별 범위 | 1타 표식 / 기절 / 기절+출혈 | 장신구 최대 1타 |
|---|---|---|---|---|---|
| P0 | 원본 | 15 / 14 | 14~15 | 18.8 / 15.8 / 15.8 | 23.3 |
| P1 | 001 (현재 모드) | 13 / 13 | 12~14 | 18.8 / 15.8 / 19.1 | 25.5 |
| P2 | 001+004 | 11 / 7 | 7~11 | 21.2 / 17.8 / 21.5 | 28.7 |
| P5 | 001+002+003 | 12 / 9 | 9~13 | 20.8 / 18.8 / 22.1 | 28.5 |
| P6 | 001+004+002 | 9 / 5 | 5~10 | 21.2 / 21.2 / 24.8 | **32.1** |
| P7 | 001+004+003 | 9 / 5 | 5~10 | **23.4** / 17.8 / 21.5 | 28.7 |
| P8 | 001+003+005 | 11 / 7 | 7~11 | 20.8 / 15.8 / 19.1 | 25.5 |
| **P9** | **001+002+003+005** | **9 / 5** | **5~10** | **20.8 / 18.8 / 22.1** | **28.5** |
| P10 | 001+004+003+005 | 7 / 5 | 5~8 | 23.4 / 17.8 / 21.5 | 28.7 |
| P11 | 001~005 전부 | 6 / 5 | 4~6 | 23.4 / 21.2 / 24.8 | 32.1 |

비교 기준: 석궁사수 저격 표식 19.4(장신구 23.8), 노상강도 영거리 사격 17.3 → 하향 후 15.0.

- **권장: P9 = BH-001(적용됨) + BH-002(기절 50→90) + BH-003(표식 90→110) + BH-005(마름쇠 −70)**
  - 순위 15위 → 9위(가정별 5~10위). 기본 가중치에서 노상강도 하향 후 순위보다 아래다.
  - 혼자 싸울 때 조건부 1타가 모두 22 이하다. 조건 없는 1타는 9.9 그대로라, 조건을 맞춰야 화력이 나오는 강약약강 설계와 맞는다.
  - BH-004를 넣은 P6·P7과 순위는 같고, 장신구 최대 폭발은 32.1 → 28.5로 낮다.
  - 사용자 의견 반영: 기절 킬러 강화(BH-000), 표식 110(BH-003 추가 검토에서 동의).
- **이전 권장(004+002)을 바꾼 이유:** 기절+출혈 이중 조건에 장신구 두 개가 겹치면 32.1까지 올라가 기준선을 크게 넘는다. BH-005라는 더 싼 선택지가 생겼다.
- **BH-004는 예비안으로 보류한다.** 테스트에서 조건 없는 화력이 부족하면 BH-002 대신 넣는다(P10: 7위/5위, 장신구 최대 28.7). 넣을 때는 매혹 시 열 2를 함께 바꿔 R-GROW-01 예외를 만들지 않는다.
- **게임 테스트 항목**
  1. 기절 킬러 + 출혈 킬러 동시 충족 시 배율이 더해지는가
  2. 어금니들의 기절·출혈 대상 버프가 동시에 적용되는가
  3. 표식 110 + 인간 킬러 35가 더해지는가(더해지면 +145%)
- **구현**
  - BH-002: `bounty_hunter.effects_edit.txt`의 `Stun Killer 1~5` 수치 수정 → 적용 도구가 `RB BH Stun Killer N` 생성
  - BH-003: 편집 사본 "모드 신규 효과" 구역에 `RB BH Dmg Marked 1~5` 추가 + 현상금 수거 1~5레벨 참조 교체
  - BH-005: `bounty_hunter.info.darkest` 마름쇠 5줄의 `.dmg`
  - 모든 변경 줄 밑에 `// BH-00N` 주석

### BH-007 어퍼컷: 1열 전용 처형 기절기로 재정의
- 상태: 적용 (게임 테스트 전)
- 분류: 의도적 조정
- 목표: G-02(기술 다양성), G-03(열 다양성), G-01
- 수정 주체: Claude (사용자 요청 2026-09-27)
- 문제 정의 [사용자]
  > 섬광탄이 더 좋아서 어퍼컷을 사용할 일이 없다. 바운티헌터를 쓴다면 어퍼컷을 안 써버리는 게 문제다. 상향 근거가 없더라도 상향하거나 섬광탄을 너프해야만 한다. 각 기술의 사용 근거를 마련해야 한다.
- 변경 (1~5레벨)
  - 대상 `1·2` → **`1열만`**
  - 피해 보정 `-67%` → **`-45%`**
  - 치명타 보정 `0/1/2/3/4` → **`9/10/11/12/13`** (실제 치명타 13% → 21%)
  - 사용 열 `2·1` 유지, 기절 140 유지, 밀치기 2 유지
- 근거
  1. **가격표상 어퍼컷은 정가였다**(잔차 +13, 정가선 14.9). 상향 근거는 영웅 층(BH 최약체권)과 구조적 문제에서 나온다.
  2. **밀치기 과금 반환**: 가격표는 밀치기를 칸당 −9%p로 매기지만 실측은 2칸 −5.4%p다(전열 몬스터 53종을 2칸 밀면 화력 −0.92 HP, 성공률 64%). 어퍼컷은 밀치기 2에 −18을 냈으나 실제 값어치는 5.4로, **12.6%p 과금** 상태였다.
  3. **대상 1열 특화는 실효 손실이 0에 가깝다.** 1열을 치면 밀치기 2로 3열에 가서 끝장내기(대상 1·2·3)·마름쇠(대상 3·4) 사거리 안이지만, 2열을 치면 4열로 가서 끝장내기가 닿지 않는다. **2열 타격은 자기 기술끼리 충돌하는 옵션이었다.** 밀치기가 실패해도(약 25%) 적이 1열에 남아 끝장내기가 닿으므로 연계는 어느 쪽이든 성립한다.
  4. **기절 기술 12개 중 대상이 1개 열인 것은 없다**(최소 2개). 공격 기술에는 대상 1열 특화가 4개 있다(영거리 사격 피해 +50%, 출혈 +20%, 강철의 추모곡 0%, 축출 −40%). 기절에 없던 아키타입을 신설한다.
  5. **치명타를 고른 이유** [사용자]: 어퍼컷은 맨손 기술이라 피해를 크게 올리면 "BH 무기가 약해 보이는" 결과가 된다(P-19). 치명타는 턱 급소 타격이라는 아트에 맞고, R-CMB-08대로 기절 확률(+20%p)·밀치기 확률(+20%p)도 함께 올린다. 또 **BH의 직업 치명타 버프가 "표식 대상 피해 +33%, 2턴"** 이라, 치명타 발동률 상승이 다음 턴 현상금 수거(표식 +90%)로 이어진다.
  6. **사용 열을 3·2·1로 넓히지 않은 이유** [사용자]: 맨손 어퍼컷이 3열에서 1열에 닿는 것은 비현실적이다. 같은 일을 하는 결투가 부츠·중보병 성채의 일격은 **자기 전진 1칸**이 붙어 정당화되고, 현상금 수거는 무기(갈고리) 사거리가 있다. 사용 2·1을 유지하면 2열→1열 인접 타격이라 문제가 없다.
- 수치 근거 (합 +24%p)

  | 항목 | %p |
  |---|---|
  | 피해 −67% → −45% | +22 |
  | 치명타 보정 +9 | 약 +7 (R-CMB-08 개정 계수, 피해 −45% 기준 1점 ≈ 0.8%p) |
  | 대상 열 1개 축소 | −5 |

- 영향 (5레벨, 무기 8-16, 영웅 등급 몬스터 회피 25 기준. 치명타 피해는 최대값 ×1.5)

  | | 변경 전 | 변경 후 |
  |---|---|---|
  | 기대 피해 | 3.77 | **6.79** |
  | 무기 기술(현상금 수거·끝장내기 10.5) 대비 | 34% | **65%** |
  | 실제 치명타 | 12% | **21%** |
  | 기절 기대 성공 | 57.4% | 59.2% |
  | 밀치기 기대 성공 | 77.4% | 79.2% |
  | 끝장내기 연계 | 절반 (2열 치면 4열로 이탈) | **100%** |
  | 전열 기절기 기대 피해 순위 | 4위/4 | **2위** (성전사 기절의 일격 6.5 바로 위) |

- 치명타 21%는 게임 상위권이되 1위(신비학자 제물 암습·심연에서의 손아귀 23%)는 아니다. P-14를 건드리지 않는다.
- BH-008(섬광탄 사용 열 4·3·2 → 4·3, 제작자 적용)과 짝이다. 두 기술의 사용 열과 대상 열이 완전히 분리된다.

  | | 어퍼컷 | 섬광탄 |
  |---|---|---|
  | 사용 열 | 1·2 | 3·4 |
  | 대상 | 1열만 | 2·3·4 |
  | 기대 피해 | 6.79 | 0 |
  | 치명타 | 21% | 불가 |
  | 기절 | 140 (59.2%) | 150 (65%) |

- 검증: 밀치기 성공 시 실제로 3열로 가는지(크기 2 이상 몬스터), 끝장내기 연계가 의도대로 매 라운드 성립하는지, 치명타 21%의 체감

### BH-008 섬광탄: 사용 열 4·3·2 → 4·3
- 상태: 적용 (제작자 직접 수정)
- 분류: 의도적 조정
- 목표: G-03(열 다양성), G-02
- 제작자 메모 (원문)
  > 사용열 432 -> 43 이유 2열에서 어퍼컷이랑 겹침. 다양한 열에서 영웅이 사용될 수 있게
  > 1.2열 쓰면 어퍼컷 , 3,4열 쓰면 섬광탄으로 구분 되게 설정
  > 기존에는 2열에 모든 기술들이 몰려있었음. 2>3>1>4열로 다양하게 사용될 수 있게 조정
- 근거 (검증)
  - 변경 전 BH가 각 열에서 쓸 수 있는 기술 수: 1열 5개 / **2열 7개(전부)** / 3열 6개 / 4열 4개 → 2열이 유일하게 전 기술을 쓸 수 있어 **2열 붙박이**였다.
  - 변경 후: 1열 5개 / **2열 6개** / **3열 6개** / 4열 4개 → 2·3열이 동률이 되고 역할이 갈린다. 2열은 전열 처형(어퍼컷·현상금 수거·끝장내기), 3열은 후열 제어(섬광탄·마름쇠·표식·이리 오너라).
  - 아트: 섬광탄을 2열에서 던지는 것보다 3·4열 후방에서 던지는 편이 자연스럽다(P-19).
- 대가: 사용 열 1개 감소 = 약 −5%p. BH-007의 상향과 합쳐 영웅 총량은 순증이며, BH가 가격표 "약함" 등급이므로 의도한 방향이다(P-11 ③ 영웅 간 비교).

### BH-009 이리 오너라: 당기기 2칸 → 3칸, 피해 −80% → −70%
- 상태: 적용 (게임 테스트 전)
- 분류: 의도적 조정
- 목표: G-02(기술 다양성), G-01
- 수정 주체: Claude (사용자 요청 2026-09-27)
- 문제: BH 7기술 중 잔차 최하위(−32)였다. 피해 −80%에 당기기 2칸 + 소표식뿐이다.
- 기각한 대안: 소표식 → 정식 표식. **죽음의 표식을 쓸 이유가 사라진다**는 제작자 지적으로 철회했다(G-02 위반).
- 변경: `Pull 2A~E` → `Pull 3A~E` (바닐라 효과, 확률 100/110/120/130/140로 동일), 피해 보정 −80% → −70%
- 근거
  1. **당기기 3칸은 게임에 없다.** 영웅 이동 기술 12개 중 당기기는 4개이고 전부 1~2칸이다(이리 오너라 2, 신비학자 악마의 아귀팔 2, 방패 파괴자 구멍내기 2, 도망자 판 뒤엎기 1). 3칸은 밀치기 쪽 나병환자 축출 하나뿐이다. **빈 아키타입을 채운다.**
  2. **결과가 확정된다.** 이리 오너라의 대상은 3·4열이므로, 3칸이면 4열 → 1열, 3열 → 1열(상한). **무엇을 끌어오든 1열에 선다.**
  3. **BH 근접기 전체와 맞물린다.** 현상금 수거(대상 1·2), 끝장내기(1·2·3), **어퍼컷(BH-007로 1열 전용)** 이 모두 1열을 덮는다. 후열 적을 1열로 끌어오면 BH의 모든 처형 기술이 닿는다. 정체성이 "사냥감을 자기 사거리로 끌어와 처형한다"로 정리된다(BH-000 강약약강).
  4. 피해 −70%는 같은 후열 견제기인 마름쇠(BH-005)와 같은 값이라 영웅 내부 기준이 통일된다.
- 값: 당기기 1칸당 9%p 기준 +9, 피해 +10 → 잔차 **−32 → −13**
- 검증: 3열 적을 잘못 끌어 대열이 과하게 흔들리는 상황이 실제로 불편한지. 당기기 성공률(이동 저항 중앙 65 기준 약 75%)

### BH-010 이리 오너라: 소표식 삭제, 명중 +5, 피해 −70% → −60% (적용)

- 목표: G-02(죽음의 표식 사용 이유), MARK-01(표식 쏠림 완화) [제작자 결정 2026-09-28]
- 문제 [제작자]: BH-009로 당기기가 3칸이 되자, 이리 오너라 한 번으로 "1열로 끌어오기 + 표식"이 끝나 **죽음의 표식을 쓸 이유가 없어졌다.**
- 변경 (1~5레벨): `BH Minor Mark` 삭제, 명중 90~110 → **95~115**, 피해 −70% → **−60%**
- 근거
  1. **설정 (P-22)**: 길드 "공격 목표에 **미리 표식을 새겨**… 또한 **갈고리와 섬광탄과 강력한 어퍼컷**을 활용해 적 일행의 **열과 오를 완전히 헤집어**". 갈고리는 진형 교란 도구로 묶여 있고, 표식은 따로 "미리" 새기는 행동이다.
  2. **죽음의 표식의 자리**: 표식 3턴 + 자기 속도 +5(2턴)는 "표식 → 당기기 → 처형" 3턴 연계에 맞는 구성이다. 기존 2턴 연계(당기기+표식 → 처형)가 3턴이 되어, 강함 순위에서 상향 과다로 표시된 BH의 처형 속도도 늦어진다(`analysis/hero_power_v2.md` 4절).
  3. **피해 −60%**: 이리 오너라에 남는 효과는 당기기 하나다. 출혈·약화 2개를 단 마름쇠(−70%)보다 효과가 적으므로 피해를 덜 깎는다(R-TRADE-01: 약화 1개 −19%p, 당기기 −9%p). BH-009의 "마름쇠와 같은 −70%" 기준은 두 기술의 효과 구성이 같을 때의 것이라 대체한다.
  4. **명중 +5**: 기술의 본업인 당기기 성공률이 54.6%였다(명중 × (140 − 이동 저항, 중앙 65)). 57.9%로 오른다. 후열을 전열로 끌어오면 스트레스 기술을 못 쓰게 되는 가치(제작자, R-STRAT-01)는 v2 모델에 아직 없어 수치보다 실제 가치가 크다.
- 수치 (v2 모델 5레벨): 6.53 → **6.18 HP**. 표식 가치(1.6)를 피해(+0.9)와 명중(+0.3)으로 대부분 보전한 재구성이다.
- 검증: 죽음의 표식 3턴이 연계 세 번째 턴까지 남는지(지속 차감 시점).


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### BH-003 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 사용자의 90→100 표식 피해 결정과 전열 표식 처형 역할을 기록한다. 레벨별 성장 제안과 현재 고정100은 구분한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/collect_bounty`
  - 원본: `combat_skill: .id "collect_bounty" .level 0 .type "melee" .atk 85% .dmg 0% .crit 7% .launch 321 .target 12 .is_crit_valid True  .effect "BH Dmg Marked" "Man Killer 1" .generation_guaranteed true`
  - 현재: `combat_skill: .id "collect_bounty" .level 0 .type "melee" .atk 85% .dmg 0% .crit 7% .launch 321 .target 12 .is_crit_valid True  .effect "RB BH Dmg Marked" "Man Killer 1" .generation_guaranteed true`
  - 원본: `combat_skill: .id "collect_bounty" .level 1 .type "melee" .atk 90% .dmg 0% .crit 8% .launch 321 .target 12 .is_crit_valid True  .effect "BH Dmg Marked" "Man Killer 2"`
  - 현재: `combat_skill: .id "collect_bounty" .level 1 .type "melee" .atk 90% .dmg 0% .crit 8% .launch 321 .target 12 .is_crit_valid True  .effect "RB BH Dmg Marked" "Man Killer 2"`
  - 원본: `combat_skill: .id "collect_bounty" .level 2 .type "melee" .atk 95% .dmg 0% .crit 9% .launch 321 .target 12 .is_crit_valid True  .effect "BH Dmg Marked" "Man Killer 3"`
  - 현재: `combat_skill: .id "collect_bounty" .level 2 .type "melee" .atk 95% .dmg 0% .crit 9% .launch 321 .target 12 .is_crit_valid True  .effect "RB BH Dmg Marked" "Man Killer 3"`
  - 원본: `combat_skill: .id "collect_bounty" .level 3 .type "melee" .atk 100% .dmg 0% .crit 10% .launch 321 .target 12 .is_crit_valid True  .effect "BH Dmg Marked" "Man Killer 4"`
  - 현재: `combat_skill: .id "collect_bounty" .level 3 .type "melee" .atk 100% .dmg 0% .crit 10% .launch 321 .target 12 .is_crit_valid True  .effect "RB BH Dmg Marked" "Man Killer 4"`
  - 원본: `combat_skill: .id "collect_bounty" .level 4 .type "melee" .atk 105% .dmg 0% .crit 11% .launch 321 .target 12 .is_crit_valid True  .effect "BH Dmg Marked" "Man Killer 5"`
  - 현재: `combat_skill: .id "collect_bounty" .level 4 .type "melee" .atk 105% .dmg 0% .crit 11% .launch 321 .target 12 .is_crit_valid True  .effect "RB BH Dmg Marked" "Man Killer 5"`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 30행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
//사용열, 타겟열 변경 123 -> 12, 12 -> 123
```
- 기존 주석 원문:
```text
//사유 끝장내기와의 차별점 있어야 함. 끝장내기가 범용적으로 더 좋음 지금은, 그래서 2개 채용할 이유가 굳이 사라짐.
```
- 기존 주석 원문:
```text
//기존엔 끝장내기와 이 기술 동시에 채용했음 이유는 12열은 현상금 사냥, 3열은 끝장내기
```
- 기존 주석 원문:
```text
// 여기서 끝장내기 1,2열 공격이 출혈딜러가 생겨서 범용성이 너무 높아짐. 이게 현상금 사냥보다 더 좋아지면 현상금 사냥 쓸 이유가 없어짐 그래서 조정
```
- 기존 주석 원문:
```text
//근데 어퍼컷과의 시너지를 생각해서 다시 롤백
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `BH Dmg Marked`
- 원본: `effect: .name "BH Dmg Marked"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 90%	.damage_high_multiply 90%	.on_hit true .on_miss false`
- 현재: `effect: .name "BH Dmg Marked"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 100%	.damage_high_multiply 100%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 19행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
// BH-003 표식 대상 피해 90%% -> 100%% (90은 수치가 애매). damage_high도 100으로 맞춤
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Dmg Marked`
- 원본 (BH Dmg Marked): `effect: .name "BH Dmg Marked"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 90%	.damage_high_multiply 90%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Dmg Marked"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "tagged"	.combat_stat_buff 1 .damage_low_multiply 100%	.damage_high_multiply 100%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 5행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```

### BH-009 BH-010 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 당기기와 표식을 분리하여 죽음의 표식 사용 이유를 보존하고 당기기 접근성과 명중을 보완한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/come_hither`
  - 원본: `combat_skill: .id "come_hither" .level 0 .type "ranged" .atk 90% .dmg -80% .crit 0% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 2A" "BH Minor Mark"`
  - 현재: `combat_skill: .id "come_hither" .level 0 .type "ranged" .atk 95% .dmg -60% .crit 0% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 3A"`
  - 원본: `combat_skill: .id "come_hither" .level 1 .type "ranged" .atk 95% .dmg -80% .crit 1% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 2B" "BH Minor Mark"`
  - 현재: `combat_skill: .id "come_hither" .level 1 .type "ranged" .atk 100% .dmg -60% .crit 1% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 3B"`
  - 원본: `combat_skill: .id "come_hither" .level 2 .type "ranged" .atk 100% .dmg -80% .crit 2% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 2C" "BH Minor Mark"`
  - 현재: `combat_skill: .id "come_hither" .level 2 .type "ranged" .atk 105% .dmg -60% .crit 2% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 3C"`
  - 원본: `combat_skill: .id "come_hither" .level 3 .type "ranged" .atk 105% .dmg -80% .crit 3% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 2D" "BH Minor Mark"`
  - 현재: `combat_skill: .id "come_hither" .level 3 .type "ranged" .atk 110% .dmg -60% .crit 3% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 3D"`
  - 원본: `combat_skill: .id "come_hither" .level 4 .type "ranged" .atk 110% .dmg -80% .crit 4% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 2E" "BH Minor Mark"`
  - 현재: `combat_skill: .id "come_hither" .level 4 .type "ranged" .atk 115% .dmg -60% .crit 4% .launch 4321 .target 34 .is_crit_valid True  .effect "Pull 3E"`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 48행; Git 원문 {"commit": "c0b60f8882374879b91b4cae2602f3f8b0f41958", "summary": "BH-010 이리 오너라: 소표식 삭제, 명중 +5, 피해 -70% -> -60%"}
- 기존 주석 원문:
```text
// BH-010 come_hither: 소표식(BH Minor Mark) 삭제, 명중 +5 (1렙 90 -> 95), 피해 -70% -> -60%. 길드 "미리 표식을 새겨" / "갈고리와 섬광탄과 어퍼컷으로 열과 오를 헤집어" - 표식과 갈고리는 다른 전술. 표식은 죽음의 표식(3턴)이 맡아 표식 -> 당기기 -> 처형 3턴 연계
```
- 기존 주석 원문:
```text
// BH-009 come_hither: Pull 2 -> Pull 3 (게임 최초 당기기 3칸), dmg -80% -> -70%
```

### BH-007 BH-011 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 현상금 사냥꾼 1열 운용의 특장점으로 강한 기절과 전열 접근을 주고 피해로 대가를 낸다. 높은 치명과 표식 후속 연계를 보존한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/uppercut`
  - 원본: `combat_skill: .id "uppercut" .level 0 .type "melee" .atk 90% .dmg -67% .crit 0% .launch 21 .target 12 .is_crit_valid True  .effect "Push 2A" "Stun 1"`
  - 현재: `combat_skill: .id "uppercut" .level 0 .type "melee" .atk 90% .dmg -67% .crit 9% .launch 1 .target 12 .is_crit_valid True  .effect "Push 2A" "Hero Strong Stun 1"`
  - 원본: `combat_skill: .id "uppercut" .level 1 .type "melee" .atk 95% .dmg -67% .crit 1% .launch 21 .target 12 .is_crit_valid True  .effect "Push 2B" "Stun 2"`
  - 현재: `combat_skill: .id "uppercut" .level 1 .type "melee" .atk 95% .dmg -67% .crit 10% .launch 1 .target 12 .is_crit_valid True  .effect "Push 2B" "Hero Strong Stun 2"`
  - 원본: `combat_skill: .id "uppercut" .level 2 .type "melee" .atk 100% .dmg -67% .crit 2% .launch 21 .target 12 .is_crit_valid True  .effect "Push 2C" "Stun 3"`
  - 현재: `combat_skill: .id "uppercut" .level 2 .type "melee" .atk 100% .dmg -67% .crit 11% .launch 1 .target 12 .is_crit_valid True  .effect "Push 2C" "Hero Strong Stun 3"`
  - 원본: `combat_skill: .id "uppercut" .level 3 .type "melee" .atk 105% .dmg -67% .crit 3% .launch 21 .target 12 .is_crit_valid True  .effect "Push 2D" "Stun 4"`
  - 현재: `combat_skill: .id "uppercut" .level 3 .type "melee" .atk 105% .dmg -67% .crit 12% .launch 1 .target 12 .is_crit_valid True  .effect "Push 2D" "Hero Strong Stun 4"`
  - 원본: `combat_skill: .id "uppercut" .level 4 .type "melee" .atk 110% .dmg -67% .crit 4% .launch 21 .target 12 .is_crit_valid True  .effect "Push 2E" "Stun 5"`
  - 현재: `combat_skill: .id "uppercut" .level 4 .type "melee" .atk 110% .dmg -67% .crit 13% .launch 1 .target 12 .is_crit_valid True  .effect "Push 2E" "Hero Strong Stun 5"`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 56행; Git 원문 {"commit": "0000000000000000000000000000000000000000", "summary": "Version of heroes/bounty_hunter/bounty_hunter.info.darkest from heroes/bounty_hunter/bounty_hunter.info.darkest"}
- 기존 주석 원문:
```text
// BH-007 uppercut: target 12 -> 1, dmg -67% -> -45%, crit +0~4 -> +9~13 (launch 21 kept)
```
- 기존 주석 원문:
```text
// 히어로 스트롱 스턴 섬광탄 걸 빼와서 얘한테 줌. 대신에 데미지를 바닐라로 줄임
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//타겟열 사용열도 바꿈 이유는 1열 설수있는 영웅이 많이 없음 이 게임에, 그래서 1열 섰을 때 특장점 메리트를 줌. 현상금 1열은 표식조합 쓰면 강제됨. 거기에 특장점을 더 줘서 1열 파티 조합 가능성을 더 높임 사용열 12 -> 1 타겟열 1-> 12 이게 좋은게 또 현상금 치명타 효과가 표식 대상 데미지 증가임 -> 어퍼컷의 높은 치명타 보정으로 1턴에 치명타 내서 표식 증가 데미지 갖추고 남이 표식 찍어준거를 끝낸다는 윈플랜도 가능해짐. "
```

### BH-008 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 2열 어퍼컷과 사용열을 분리하고 높은 명중·후열 도달·자리바꿈의 대가로 일반 기절을 사용한다. 사용자 가치 판단이며 바닐라 보편 규칙의 확정은 아니다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/flashbang`
  - 원본: `combat_skill: .id "flashbang" .level 0 .type "ranged" .atk 95% .dmg -100% .crit 0% .launch 432 .target 234 .is_crit_valid False  .effect "Hero Strong Stun 1" "Disorient 1" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flashbang" .level 0 .type "ranged" .atk 95% .dmg -100% .crit 0% .launch 43 .target 234 .is_crit_valid False  .effect "Stun 1" "Disorient 1" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flashbang" .level 1 .type "ranged" .atk 100% .dmg -100% .crit 0% .launch 432 .target 234 .is_crit_valid False  .effect "Hero Strong Stun 2" "Disorient 2" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flashbang" .level 1 .type "ranged" .atk 100% .dmg -100% .crit 0% .launch 43 .target 234 .is_crit_valid False  .effect "Stun 2" "Disorient 2" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flashbang" .level 2 .type "ranged" .atk 105% .dmg -100% .crit 0% .launch 432 .target 234 .is_crit_valid False  .effect "Hero Strong Stun 3" "Disorient 3" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flashbang" .level 2 .type "ranged" .atk 105% .dmg -100% .crit 0% .launch 43 .target 234 .is_crit_valid False  .effect "Stun 3" "Disorient 3" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flashbang" .level 3 .type "ranged" .atk 110% .dmg -100% .crit 0% .launch 432 .target 234 .is_crit_valid False  .effect "Hero Strong Stun 4" "Disorient 4" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flashbang" .level 3 .type "ranged" .atk 110% .dmg -100% .crit 0% .launch 43 .target 234 .is_crit_valid False  .effect "Stun 4" "Disorient 4" .is_stall_invalidating false`
  - 원본: `combat_skill: .id "flashbang" .level 4 .type "ranged" .atk 115% .dmg -100% .crit 0% .launch 432 .target 234 .is_crit_valid False  .effect "Hero Strong Stun 5" "Disorient 5" .is_stall_invalidating false`
  - 현재: `combat_skill: .id "flashbang" .level 4 .type "ranged" .atk 115% .dmg -100% .crit 0% .launch 43 .target 234 .is_crit_valid False  .effect "Stun 5" "Disorient 5" .is_stall_invalidating false`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 68행; Git 원문 {"commit": "0000000000000000000000000000000000000000", "summary": "Version of heroes/bounty_hunter/bounty_hunter.info.darkest from heroes/bounty_hunter/bounty_hunter.info.darkest"}
- 기존 주석 원문:
```text
//사용열 432 -> 43 이유 2열에서 어퍼컷이랑 겹침. 다양한 열에서 영웅이 사용될 수 있게
```
- 기존 주석 원문 (JSON 문자열, 끝 공백 포함):
```json
"//대신에 스트롱 스턴을 그냥 스턴으로 바꿈 근거는 명중이 95임 명중 90을 표준이라 두면, 명중 +5, 데미지 없는 것 + 3,4열 타격가능 + 자리바꿈 3개가 추가되면 데미지 없는 걸 상쇄함. 물론 치명타 안뜨는 것도 포함되서 상쇄되는것 "
```

### BH-001 BH-002 BH-012 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 출혈·기절 준비 후 처형을 강화하고 어퍼컷 이후 3열 후속 공격이 가능하도록 한다. 기절 피해의 최소/최대가 비대칭임을 그대로 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/finish_him`
  - 원본: `combat_skill: .id "finish_him" .level 0 .type "melee" .atk 85% .dmg 0% .crit 5% .launch 321 .target 123 .is_crit_valid True  .effect "Stun Killer 1"`
  - 현재: `combat_skill: .id "finish_him" .level 0 .type "melee" .atk 85% .dmg 0% .crit 5% .launch 21 .target 123 .is_crit_valid True  .effect "RB BH Stun Killer 1" "RB BH Bleed Killer 1"`
  - 원본: `combat_skill: .id "finish_him" .level 1 .type "melee" .atk 90% .dmg 0% .crit 6% .launch 321 .target 123 .is_crit_valid True  .effect "Stun Killer 2"`
  - 현재: `combat_skill: .id "finish_him" .level 1 .type "melee" .atk 90% .dmg 0% .crit 6% .launch 21 .target 123 .is_crit_valid True  .effect "RB BH Stun Killer 2" "RB BH Bleed Killer 2"`
  - 원본: `combat_skill: .id "finish_him" .level 2 .type "melee" .atk 95% .dmg 0% .crit 7% .launch 321 .target 123 .is_crit_valid True  .effect "Stun Killer 3"`
  - 현재: `combat_skill: .id "finish_him" .level 2 .type "melee" .atk 95% .dmg 0% .crit 7% .launch 21 .target 123 .is_crit_valid True  .effect "RB BH Stun Killer 3" "RB BH Bleed Killer 3"`
  - 원본: `combat_skill: .id "finish_him" .level 3 .type "melee" .atk 100% .dmg 0% .crit 8% .launch 321 .target 123 .is_crit_valid True  .effect "Stun Killer 4"`
  - 현재: `combat_skill: .id "finish_him" .level 3 .type "melee" .atk 100% .dmg 0% .crit 8% .launch 21 .target 123 .is_crit_valid True  .effect "RB BH Stun Killer 4" "RB BH Bleed Killer 4"`
  - 원본: `combat_skill: .id "finish_him" .level 4 .type "melee" .atk 105% .dmg 0% .crit 9% .launch 321 .target 123 .is_crit_valid True  .effect "Stun Killer 5"`
  - 현재: `combat_skill: .id "finish_him" .level 4 .type "melee" .atk 105% .dmg 0% .crit 9% .launch 21 .target 123 .is_crit_valid True  .effect "RB BH Stun Killer 5" "RB BH Bleed Killer 5"`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 77행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
// BH-001 finish_him: + RB BH Bleed Killer 1-5 (dmg vs bleeding target, mirrors GR Poison Killer)
```
- 기존 주석 원문:
```text
// 사용열 변경 123 -> 12 사유는 어퍼컷 때문에 3열 때릴 수 있어야함 연계되려면
```

### BH-005 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 후열 출혈·약화 기술의 직접 피해를 보완해 출혈 딜러 선택지를 만든다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/hook_and_slice`
  - 원본: `combat_skill: .id "hook_and_slice" .level 0 .type "ranged" .atk 90% .dmg -95% .crit 5% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 1" "Caltrops SPD Debuff 1" "Caltrops Prey Debuff 1"`
  - 현재: `combat_skill: .id "hook_and_slice" .level 0 .type "ranged" .atk 90% .dmg -70% .crit 5% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 1" "Caltrops SPD Debuff 1" "Caltrops Prey Debuff 1"`
  - 원본: `combat_skill: .id "hook_and_slice" .level 1 .type "ranged" .atk 95% .dmg -95% .crit 6% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 2" "Caltrops SPD Debuff 2" "Caltrops Prey Debuff 2"`
  - 현재: `combat_skill: .id "hook_and_slice" .level 1 .type "ranged" .atk 95% .dmg -70% .crit 6% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 2" "Caltrops SPD Debuff 2" "Caltrops Prey Debuff 2"`
  - 원본: `combat_skill: .id "hook_and_slice" .level 2 .type "ranged" .atk 100% .dmg -95% .crit 7% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 3" "Caltrops SPD Debuff 3" "Caltrops Prey Debuff 3"`
  - 현재: `combat_skill: .id "hook_and_slice" .level 2 .type "ranged" .atk 100% .dmg -70% .crit 7% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 3" "Caltrops SPD Debuff 3" "Caltrops Prey Debuff 3"`
  - 원본: `combat_skill: .id "hook_and_slice" .level 3 .type "ranged" .atk 105% .dmg -95% .crit 8% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 4" "Caltrops SPD Debuff 4" "Caltrops Prey Debuff 4"`
  - 현재: `combat_skill: .id "hook_and_slice" .level 3 .type "ranged" .atk 105% .dmg -70% .crit 8% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 4" "Caltrops SPD Debuff 4" "Caltrops Prey Debuff 4"`
  - 원본: `combat_skill: .id "hook_and_slice" .level 4 .type "ranged" .atk 110% .dmg -95% .crit 9% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 5" "Caltrops SPD Debuff 5" "Caltrops Prey Debuff 5"`
  - 현재: `combat_skill: .id "hook_and_slice" .level 4 .type "ranged" .atk 110% .dmg -70% .crit 9% .launch 234 .target 34 .is_crit_valid True  .effect "Bleed 5" "Caltrops SPD Debuff 5" "Caltrops Prey Debuff 5"`
- 출처: `heroes/bounty_hunter/bounty_hunter.info.darkest`, 주석 추가 전 88행; Git 원문 {"commit": "85ed78358dc522e062c53336633b0ea0120f71c3", "summary": "R-RANK-01 이동기 원칙 + 야만인 자가 회복 적용 + BH-005 마름쇠"}
- 기존 주석 원문:
```text
// BH-005 hook_and_slice(마름쇠): dmg -80% -> -70% (vanilla -95%)
```

### BH-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 출혈·기절 준비 후 처형을 강화하고 어퍼컷 이후 3열 후속 공격이 가능하도록 한다. 기절 피해의 최소/최대가 비대칭임을 그대로 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Stun Killer 1`
- 원본: `effect: .name "Stun Killer 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 25% .damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "Stun Killer 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 25% .damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 151행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Stun Killer 2`
- 원본: `effect: .name "Stun Killer 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 33% .damage_high_multiply 33%	.on_hit true .on_miss false`
- 현재: `effect: .name "Stun Killer 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 33% .damage_high_multiply 70%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 153행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Stun Killer 3`
- 원본: `effect: .name "Stun Killer 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 40% .damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "Stun Killer 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 40% .damage_high_multiply 80%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 155행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Stun Killer 4`
- 원본: `effect: .name "Stun Killer 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 50% .damage_high_multiply 50%	.on_hit true .on_miss false`
- 현재: `effect: .name "Stun Killer 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 50% .damage_high_multiply 90%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 157행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `Stun Killer 5`
- 원본: `effect: .name "Stun Killer 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 60% .damage_high_multiply 60%	.on_hit true .on_miss false`
- 현재: `effect: .name "Stun Killer 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 60% .damage_high_multiply 100%	.on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 159행; Git 원문 {"commit": "3e0b7650d63bb2c9bf5c6fe2fece69519ef897da", "summary": "BH-007 어퍼컷 1열 전용 처형 기절기 + BH-008 섬광탄 사용 열 기록"}
- 기존 주석 원문:
```text
// 60-100으로 변경
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Stun Killer 1`
- 원본 (Stun Killer 1): `effect: .name "Stun Killer 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 25% .damage_high_multiply 25%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Stun Killer 1"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 25% .damage_high_multiply 60%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 7행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
// edited vanilla effect (from effects/base.effects.darkest)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Stun Killer 2`
- 원본 (Stun Killer 2): `effect: .name "Stun Killer 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 33% .damage_high_multiply 33%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Stun Killer 2"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 33% .damage_high_multiply 70%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 9행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Stun Killer 3`
- 원본 (Stun Killer 3): `effect: .name "Stun Killer 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 40% .damage_high_multiply 40%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Stun Killer 3"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 40% .damage_high_multiply 80%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 11행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Stun Killer 4`
- 원본 (Stun Killer 4): `effect: .name "Stun Killer 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 50% .damage_high_multiply 50%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Stun Killer 4"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 50% .damage_high_multiply 90%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 13행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Stun Killer 5`
- 원본 (Stun Killer 5): `effect: .name "Stun Killer 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 60% .damage_high_multiply 60%	.on_hit true .on_miss false`
- 현재: `effect: .name "RB BH Stun Killer 5"	.target "performer" .chance 100%	.curio_result_type "positive" .keyStatus "stunned"	.combat_stat_buff 1	.damage_low_multiply 60% .damage_high_multiply 100%	.on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 15행; Git 원문 {"commit": "c1826646598f71f92681c3901362602332285460", "summary": "BH-003 표식 피해 100%% 적용 + damage_high 90 누락 수정"}
- 기존 주석 원문:
```text
// mod-only new effects
```

### BH-001 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 출혈·기절 준비 후 처형을 강화하고 어퍼컷 이후 3열 후속 공격이 가능하도록 한다. 기절 피해의 최소/최대가 비대칭임을 그대로 기록한다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB BH Bleed Killer 1`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 20% .damage_high_multiply 20% .on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 225행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 기존 주석 원문:
```text
// BH-001 finish_him: +20% dmg vs bleeding (level 1, mirrors GR Poison Killer 1)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB BH Bleed Killer 2`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 23% .damage_high_multiply 23% .on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 227행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 기존 주석 원문:
```text
// BH-001 finish_him: +23% dmg vs bleeding (level 2, mirrors GR Poison Killer 2)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB BH Bleed Killer 3`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 26% .damage_high_multiply 26% .on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 229행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 기존 주석 원문:
```text
// BH-001 finish_him: +26% dmg vs bleeding (level 3, mirrors GR Poison Killer 3)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB BH Bleed Killer 4`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 29% .damage_high_multiply 29% .on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 231행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 기존 주석 원문:
```text
// BH-001 finish_him: +29% dmg vs bleeding (level 4, mirrors GR Poison Killer 4)
```
- 상태: 편집 사본(게임이 직접 읽지 않음)
- 효과: `RB BH Bleed Killer 5`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 33% .damage_high_multiply 33% .on_hit true .on_miss false`
- 출처: `heroes/bounty_hunter/bounty_hunter.effects_edit.txt`, 주석 추가 전 233행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 기존 주석 원문:
```text
// BH-001 finish_him: +33% dmg vs bleeding (level 5, mirrors GR Poison Killer 5)
```
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Bleed Killer 1`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 1" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 20% .damage_high_multiply 20% .on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 18행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Bleed Killer 2`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 2" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 23% .damage_high_multiply 23% .on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 20행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Bleed Killer 3`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 3" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 26% .damage_high_multiply 26% .on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 22행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Bleed Killer 4`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 4" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 29% .damage_high_multiply 29% .on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 24행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
- 상태: 게임용 파생 효과의 현재 정의
- 효과: `RB BH Bleed Killer 5`
- 원본: `None`
- 현재: `effect: .name "RB BH Bleed Killer 5" .target "performer" .chance 100% .curio_result_type "positive" .keyStatus "bleeding" .combat_stat_buff 1 .damage_low_multiply 33% .damage_high_multiply 33% .on_hit true .on_miss false`
- 출처: `effects/rebalance_bounty_hunter.effects.darkest`, 주석 추가 전 26행; Git 원문 {"commit": "c7df494cb407eebf6deb6bbc0e22f0a43c7a3c3b", "summary": "BH-001 끝장내기 출혈 대상 추가 피해(신규 효과), BH-002 기절 조건 강화 제안, 최적 열·딜러 비교"}
