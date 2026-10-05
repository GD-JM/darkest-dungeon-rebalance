# 결투가 (duelist) 변경 항목

바닐라 수치: `heroes/duelist/duelist.vanilla.txt`

---

## DUE-000 공식 패치(2026-09-18) 반영 (적용 2026-09-30)

모드 파일이 패치 전 원본(8/25) 기반이라 패치를 되돌리고 있었다(`changes/runaway.md` 1절과 같은 문제). 패치 후 공식 파일로 교체하고 DUE-001만 다시 얹었다. 기준점 `duelist.info원본.darkest`도 패치 후로 교체(패치 전은 `_0825` 보관).

| 항목 | 패치 전 | 패치 후 |
|---|---|---|
| 체력 1~5레벨 | 20/24/28/32/36 | 21/25/29/33/37 |
| 눈속임 치명타 | 3~7 | 8~12 |
| 날쌘 돌진 피해 | +20% | +25% |
| 반격 명중 | 95 | 100 |
| 회수 자기 강화 (4턴) | 명중 +10, 속도 +4~6 | 명중 +10, 속도 **+6~8**, 특정 열(rule_data 3)에서 회피 **+30~40%** 추가 (효과가 `buff_ids` 참조로 바뀜) |

공식 패치는 결투가 상향이다(패치 전 기준 모델 18위 영웅).

## DUE-001 부츠(박차기) 피해 보정 −40 → −60 (제작자 변경, 기록 2026-09-30)

- 전 레벨 `.dmg -40%` → `-60%`. 기절·밀치기·명중은 그대로.
- 제작자 근거(원문 메모): "중보병 성채의 일격과 데미지 보정을 바꿈. 40 → 60 너무 사기임. 거기에 명중 95까지 있어서 바꿔도 사실 3열에서 사용 가능하기도 하고 성기사 거랑 비교하면 더 좋은 수준".
- 해석: 기절 + 밀치기 + 3열 사용 가능 기술의 가격표를 중보병 성채의 일격(−60, MAA-003에서 바닐라 복귀)과 맞춘 것. 
- 이 변경은 패치 전 파일 위에 있었고 기록이 없었다. 패치 반영 때 그대로 옮기고 이번에 번호를 붙였다.


## DUE-002 부츠 피해 보정 −60 → −70 (적용 2026-10-05)

- 상태: 사용자 승인·적용. DUE-001의 후속 수치 조정.
- 목표: 기술 선택의 균형과 조합 다양성. 높은 적중·밀치기 안정성의 피해 대가를 조정하고 기존 기절·밀치기·태세 운용을 보존한다.
- 사용자 지시 원문: "부츠 -70은 적용하자 왜냐면 성채의 일격보다 명중이 높잖아 치명타 낮은대신 맞아? 두개가 확실히 차별화되지 않고 같은 기술이라 불만이긴 해"
- 전 레벨 `.dmg -60%` → `-70%`. 피해 배율 0.4 → 0.3으로 직접 피해는 기존 대비 25% 감소한다. 명중·치명·기절·밀치기·열·전진·태세 제한은 유지한다.

### 근거와 원칙 대조

| 항목 | 부츠 | 성채의 일격(현재 모드) |
|---|---|---|
| 명중, 기술 1레벨 | 95 | 90 |
| 기술 치명 보정, 기술 1레벨 | +1% | +5% |
| 무기·기술 5레벨 합산 치명, 장신구 없음 | 14% | 15% |
| 밀치기 1칸 적용 확률, 기술 1→5레벨·저항 전 | 110→150% | 100→140% |
| 일반 기절 적용 확률, 기술 1→5레벨·저항 전 | 100→140% | 100→140% |
| 피해 보정 | −70% | −60% |
| 사용 열 / 대상 열 / 자기 이동 | 123 / 12 / 전진 1 | 123 / 12 / 전진 1 |
| 사용 조건 | 공격 태세 | 태세 제한 없음 |

- 명중 +5와 피해 −10%p의 기존 교환 원칙에 맞는다. 전체 균형 판단에는 부츠의 높은 밀치기 확률, 낮은 치명, 공격 태세 조건과 서로 다른 무기 수치도 함께 고려한다.
- 고정 장신구의 기절·공격 태세·근접 강화 축을 보존한다. 치명타를 조정 수단으로 쓰지 않고 원본 효과를 재사용한다.
- 바닐라 중앙 잔차 31.25%p를 기준으로 현재 부츠의 잔차 43.09 → 32.77%p, 중앙과 차이 +1.52%p. 공통 표준 평타 기준 피해 보정 환산값이며 전체 실전가치와 구분한다. 조건·계산은 `outputs/stun-normalization-proposals.json` 및 이번 적용 기록 `outputs/duelist-boot-070-model.json`에 있다.
- 사용 조건을 충족한 무장신구 기술·무기 5레벨 비교이며 치명 스트레스 회복·후속 강화·이동 등에 기존 모델 가정을 쓴다. 영웅 총량 보존이나 게임 내 최적 선택을 증명하지 않는다.
- 두 기술의 단일 행동 구조는 여전히 같다. 부츠의 높은 안정성과 낮은 피해를 구분하지만 역할 중복 자체의 해결은 별도 설계 과제다. 영웅 전체 운용에서는 부츠의 공격 태세·전진에 따른 다음 기술 선택과 성채의 대열 회복·동료 보호를 비교할 수 있다. 기절 대상 특효 연계는 양쪽 기술 모두 지원하므로 부츠만의 고유 기능으로 보지 않는다. 후속 공격은 기절 지속·행동 순서·대상 생존이 필요하다.

### 이력과 검증

- 원본 −40 → DUE-001 −60 → DUE-002 −70. 기존 제작자 주석을 아래에 원문 그대로 보존한다.

```text
// DUE-001 박차기 피해 보정 -40 -> -60. 제작자 메모: 중보병 성채의 일격과 데미지 보정을 바꿈. 40-> 60너무 사기임. 거기에 명중 95까지 있어서 바꿔도 사실 3열에서 사용 가능하기도 하고 성기사 거랑 비교하면 더 좋은 수준
```

- 기술 5개 레벨의 피해 필드와 해당 주석만 변경하고 나머지 기술 필드는 바이트 단위로 검증한다. 관련 영웅·효과·편집 사본·도구는 변경 전후 해시로 보존 여부를 확인한다.
- `tools/check_comments.py duelist` 통과, 해당 두 파일의 `git diff --check` 통과. 기술 피해 5개 필드·주석 외 데이터 변경 없음, 나머지 57개 영웅·효과·편집 사본·도구 파일 해시 일치. 게임 내 실전 확인은 별도다.


## 2026-10-05 주석·의도 전수 추적 (수치 변경 없음)
이번 항목은 이전 문서의 후보/기각/예전 수치를 덮어쓰지 않는 현재 스냅샷이다. 사용자 한국어 메모를 원문 그대로 보존했다. 실제 데이터와 편집 사본의 상태를 별도로 기록하며, 새로운 수치 결정이나 전역 효과 적용을 하지 않는다. 최신 사용자 작업은 이 섹션을 우선 참고한다.

### DUE-001 DUE-002 현재 연결·의도 기록
- 목표: 기존 조합/기술 선택 다양성과 해당 항목의 기존 목표를 추적한다.
- 의도: 성채의 일격보다 높은 명중과 밀치기 안정성에 피해로 대가를 내고 기존 기절/태세를 보존한다. 이 수치만으로 두 기술의 역할 차이가 해결된 것은 아니다.
- 근거: 아래 사용자 원문, 기존 항목/커밋 출처와 실제 원본 대조. 추적된 의도는 설계의 보편적 정답을 입증하지 않는다. 값의 세부 이유가 원문에 없는 경우 새로 창작하지 않는다.
- 상태: 게임이 읽는 info의 현재 값. 기존 HEAD와 다른 데이터는 사용자가 이미 편집한 상태이며 이번 작업은 주석만 추가했다.
- 기술/행: `combat_skill/the_boot`
  - 원본: `combat_skill: .id "the_boot" .level 0 .type "melee" .atk 95%  .dmg -40% .crit 1% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 1" "Push 1B" .valid_modes stance_aggressive`
  - 현재: `combat_skill: .id "the_boot" .level 0 .type "melee" .atk 95%  .dmg -70% .crit 1% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 1" "Push 1B" .valid_modes stance_aggressive`
  - 원본: `combat_skill: .id "the_boot" .level 1 .type "melee" .atk 100% .dmg -40% .crit 2% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 2" "Push 1C" .valid_modes stance_aggressive`
  - 현재: `combat_skill: .id "the_boot" .level 1 .type "melee" .atk 100% .dmg -70% .crit 2% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 2" "Push 1C" .valid_modes stance_aggressive`
  - 원본: `combat_skill: .id "the_boot" .level 2 .type "melee" .atk 105% .dmg -40% .crit 3% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 3" "Push 1D" .valid_modes stance_aggressive`
  - 현재: `combat_skill: .id "the_boot" .level 2 .type "melee" .atk 105% .dmg -70% .crit 3% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 3" "Push 1D" .valid_modes stance_aggressive`
  - 원본: `combat_skill: .id "the_boot" .level 3 .type "melee" .atk 110% .dmg -40% .crit 4% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 4" "Push 1E" .valid_modes stance_aggressive`
  - 현재: `combat_skill: .id "the_boot" .level 3 .type "melee" .atk 110% .dmg -70% .crit 4% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 4" "Push 1E" .valid_modes stance_aggressive`
  - 원본: `combat_skill: .id "the_boot" .level 4 .type "melee" .atk 115% .dmg -40% .crit 5% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 5" "Push 1F" .valid_modes stance_aggressive`
  - 현재: `combat_skill: .id "the_boot" .level 4 .type "melee" .atk 115% .dmg -70% .crit 5% .move 0 1 .launch 321 .target 12 .is_crit_valid True  .effect "Stun 5" "Push 1F" .valid_modes stance_aggressive`
- 출처: `heroes/duelist/duelist.info.darkest`, 주석 추가 전 56행; Git 원문 {"commit": "eca6f56492abde68e068e46c48eb9935424586ae", "summary": "DUE-002 부츠 피해 보정 -70% 적용"}
- 기존 주석 원문:
```text
// DUE-002 The Boot damage -60% -> -70% at all levels; accuracy, crit, stun, push and stance retained. Previous change: DUE-001.
```
