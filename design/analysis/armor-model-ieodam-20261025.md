# R-AUDIT-26 공식·의도·이어담 연결 기록

모델 코드 `450f95e5ebbb9cc1bb59cefd8574a5168b6fe018` · 게임 입력 `1f5d3b83d5f0aa177df39ca73c247d0577dff5ad`
이어담 주제 `topic:darkest-dungeon:residual-balance` · 버전 **11** · 업데이트 `b379fc13-2fb4-4db8-97bc-e7b3d7482b7e`

사용자 요청: 그럼 방금 개선한 모델이랑 항목별 산정 공식, 변경 의도까지 이어담에 정리하고 커밋 후 푸쉬까지 해보자

14개 공식의 단위·표현식·기본 입력·변경 이유·한계를 이어담에 반영하고 get_formula로 전부 다시 읽어 동일함을 확인했다. 이번 기록 요청과 이전 모델 개선 요청은 사용자 원문, 계산 결과 보고는 assistant 원문으로 구분했다. 게임 수치를 새로 바꾸거나 분석 권고를 사용자 채택으로 바꾸지 않았다.

## 출처

- `64ce712f2d20e58bfb58195435f6009ec0879dcd5b3a4b87dce49c29fa7183b4` · user · 2026-10-25T06:31:35.044Z · message `msg_01a171c1-e584-7291-a84a-a8ea6d2d27aa`
- `7f6883932fbc90d904bae48aaac61316dd8d64f73f4d9e3f550f3335c3237abc` · user · 2026-10-25T05:25:25.633Z · message `msg_01a17185-5400-7910-9e3d-b71a8d52688d`
- `054824cd40abdd08aa501cb2ab754290a2a4c00e93d444bc94b493b12b9b1189` · assistant · 2026-10-25T06:12:03.733Z · message `msg_09497bc333ddedd0016add9d751628819191581cf0e1bcd797`

## 변경 의도와 범위

- 실제 무기는 분자에, 공통 표준 평타는 분모에 두어 영웅의 기본 피해 차이를 유지한다.
- 광역마다 후속 공격을 복제하지 않고 파티 행동 예산을 나눈다.
- 같은 타깃에 들어가는 여러 약화의 증폭을 공동 계산하고 기여를 중복 배분하지 않는다.
- 조건부 반격·장신구·호위·치명 회복은 발동하지 않는 상황과 분리한다.
- 회피0 정상 적을 포함하고 원본 등급별 배치·저항·피해·명중을 사용한다.
- 준비 행동은 남은HP 상한과 실제 후속 공격 수로 따로 비교한다.
- 모형의 구현·산술 통과·엔진 기본 분기 확인·실전 밸런스 타당성을 구별한다.

## 항목별 산정식

### R-AUDIT-26 — 방어도 지원 통합 비교 모델

직접 피해·후속 피해·예방 피해·부가 효과를 같은 눈금으로 비교하되 조건과 중복을 숨기지 않는다.

```text
V_HP = V_direct + V_joint_followup + V_prevention + V_speed + V_critical_side + V_conditional_utility; score_pp=100*V_HP/B-100, B=8.14872802734375. 각 구성요소 contribution_pp=100*V_i/B.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 일반 초기 편성 대상 균등 선택/장신구 시나리오/방어0·20·40·60/후속공격 예산 민감도/유한HP 비교를 분리한다.

**한계·가드레일:** global strength.py 전체 순위가 자동 교체된 것은 아니다. 현재 방어감소8기술+바닐라 비교군2기술. 모든 영웅 모든 효과의 완전 전투 시뮬레이터가 아니다.

### R-AUDIT-26-UNIT — 공통 평타 단위와 EHP 분리

자기 무기로 각각 나누면 사라지는 영웅 기본 공격력 차이를 보존한다.

```text
V_percent=100*V_HP/8.14872802734375; delta_from_basic_pp=V_percent-100; component_pp=100*component_HP/8.14872802734375. EHP=HP/(1-PROT)는 별도 진단.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 고정 5단계 표준 평타 B를 사용. 영웅 무기·치명은 분자에서 계산. 모든 레벨 결과도 같은 B이며 서로 다른 레벨을 동일 위력이라고 해석하지 않는다.

**한계·가드레일:** EHP 감소와 실제 추가 피해를 중복 합산하지 않는다. score_pp는 OLS 회귀 잔차가 아니다. 0.076HP/%p 같은 과거 다른 기준과 혼합하지 않는다.

### R-AUDIT-26-HIT-DAMAGE — 명중·치명·정수 직접 피해

실제 무기와 반올림 및 치명 불가 플래그를 반영한다.

```text
h=.05+clamp((ACC-DODGE)/100,0,.95); c=clamp((weaponCrit+skillCrit+activeGearCrit)/100,0,1), crit_invalid이면0. multiplier=skillMultiplier*(1+buffBonus). normal raw는 ceil(min*multiplier)..ceil(max*multiplier) 균등; crit raw=max*multiplier*1.5. HP(raw)=max(0,roundf(raw-(PROT>0&&raw>0 ? max(1,roundf(PROT*raw)):0))). D=h*((1-c)*mean(min(currentHP,HP(normal)))+c*min(currentHP,HP(crit))). float32 연산 순서는 strength.damage_distribution 참조.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 기본 엔진 분기의 기존 REA 확인 커널을 재사용. skill·weapon level을 일치시킨다.

**한계·가드레일:** 빗나감 이력 보정·강제명중·특수 기벽 등은 범위 밖. 조건부 피해 연산 전체가 엔진 검증됐다는 뜻은 아니다.

### R-AUDIT-26-JOINT — 동일 대상 후속 공격과 약화 성공

명중·치명·처치·저항을 독립 평균으로 섞지 않는다.

```text
opening branch b=(miss,normal-hit,critical-hit); P_b=(1-h,h*(1-c)*S_normal,h*c*S_crit). q_gb=clamp(chance_g+critBonus_gb-resist,0,1), on_hit/on_miss 조건 적용. 상태 조합 P_g=product(q_gb 또는1-q_gb). V_support=sum_{m,b,g,t}w_m*P_b*P_g*N_t*alive_t*(D_m(mods_g,t)-D_m(noMods)). PROT_after=max(0,PROT-sum(armorDebuffs)); 회피·받는치명·받는피해도 같은 D에서 평가.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 공격 후 생존 S는 실제 HP·정수 피해로 계산. 서로 다른 효과 roll은 같은 명중/치명 조건 아래 독립이라고 가정. 표식 유지율 기본0.3.

**한계·가드레일:** 미래 사망은 생존 가정이며 전체 전투 시뮬레이션이 아니다. damage_received_percent의 엔진 연산 순서는 미확인. 후속 치명 부수효과는 직접 피해와 별도.

### R-AUDIT-26-BUDGET — 단일·광역 공통 후속 공격 예산

광역 대상마다 후속 공격1.5회를 줘 파티 행동 수가 늘어나는 오류를 막는다.

```text
B_party=3 attacks/round; 단일 N=B_party*focusShare=1.5 (focusShare=.5); 광역 총 N=B_party=3을 실제 대상 가중치 w/sum(w)로 분배. alive[0]=.5; alive[t]=(1-.393)^t. 실제 지속에서 최대3개 시간창만 합산. 2턴 단일 effective attacks=1.6605, 3턴=2.2131735.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 3회는 라운드당 예산이며 전체 전투 총3회가 아니다. 파티예산0/1/2/3/4 민감도 제공.

**한계·가드레일:** 예산/집중률/생존율은 시나리오 가정이다. 광역 방어감소 이득을 적 수만큼 다시 곱하지 않는다.

### R-AUDIT-26-SHAPLEY — 방어 감소와 다른 공격 지원의 상호작용 배분

회피와 방어를 함께 낮춰 얻는 증폭분을 양쪽에 전부 더하지 않는다.

```text
A=방어감소만 적용한 추가 직접피해; O=기타 공격지원만; J=둘을 함께 적용. phi_armor=(A+J-O)/2; phi_other=(O+J-A)/2; phi_armor+phi_other=J.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 동일 대상·명중·무기·생존/지속·후속 공격 예산을 유지한 2그룹 Shapley 배분. 후속 치명 부수효과는 별도.

**한계·가드레일:** 배분 규칙이지 게임 엔진 규칙이 아니다. J에 A/O를 다시 더하지 않는다.

### R-AUDIT-26-PREVENT — 공격력·명중·치명 약화의 예방 HP

적 기술의 실제 위협을 사용하고 DOT를 직접 피해 감소로 잘못 줄이지 않는다.

```text
T(m,mods)=sum_native_AI_weights(targetCount*(h*D + expectedDOT + expectedLostAllyAction + stressHP*(stress+criticalStress))). V_prevent=sum_{m,b,g,t}w_m*P_b*P_g*alive_t*(T(m,0)-T(m,mods)). DOT=amount*min(duration,realizedTicks)*effectSuccess*activation; stun=effectSuccess*activation*allyActionHP*actionAvailable.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 원본 basic AI skill weights와 실제 사용열. 레벨5 allyDodge25, DOT저항.6, stun저항.8, realizedDOTticks2, allyActionHP8.148728, stressHP1.6615733437616491. 페인트 표식 피해자 비율.556(단일), 자기표식2턴 후0.

**한계·가드레일:** 질병·섞기·적 치유·소환 전체 가치 미포함. 저항/피격/표식 타깃 선택은 공통 노출 가정이다. on-hit/on-miss 및 조건부 효과의 구현 범위는 코드와 ignored_enemy_effect_keys 참고.

### R-AUDIT-26-SPEED — 속도 약화의 행동 예방

공격력/명중을 이미 낮춘 적 행동을 사용해 예방 가치를 중복하지 않는다.

```text
V_speed=sum w_m*P_b*P_g*alive_t*.393*(p_before(allySpeed,enemySpeed-SPDdown)-p_before(allySpeed,enemySpeed))*T(m,otherDebuffs). p_before는 strength.py의 기존 주사위 순서 모형.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 기본 allySpeed7. 선공 후 처치율.393은 기존 모델 가정. 포효의 큰 기여도가 이 항목에서 나옴.

**한계·가드레일:** 선공=무조건 행동 삭제가 아니다. 처치율0이면 이 항목0. 관측 플레이 로그로 교정되지 않은 가정을 엔진 사실로 기록하지 않는다.

### R-AUDIT-26-CRITICAL — 치명 부수효과와 후속 회복

치명 직접 피해와 스트레스 회복·직업 치명 강화를 분리한다.

```text
V_crit_side=P(landedCrit)*(5.25*stressHP+classCritBuffHP+healProcHP). healProcHP=healBuffRate*maxOwnSingleTargetHealMean*(1+.12)*healFollowupRate(.5)*critBuffDuration(2). 후속 공격의 치명 증가 부수효과는 damage_support.followup의 동일 hit/crit 차이로 별도 계산.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 회복 가능한 스트레스와 실제 미래 회복 필요. 직업별 무기·기술 치명과 class crit effects를 읽음.

**한계·가드레일:** 치명 불가 기술에 무기/장신구 치명 이득을 더하지 않는다. 스트레스0/후속 회복0이면 관련 회복 이득0. 상시 보장 회복으로 주장하지 않는다.

### R-AUDIT-26-RIPOSTE — 페인트의 실제 반격 횟수별 한계 이득

반격을 하지 않아도 반격 강화 점수가 생기는 문제를 피한다.

```text
V_riposte=n_actual_ripostes*E[h_r*(D_r(withFeintBuff)-D_r(withoutFeintBuff))]. n=0/1/2 별도. 아카데미 반지 riposte-only crit는 반격 c_r에만 더한다. 자기 표식 위험·조건부 적 명중 약화는 별도 계정.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 기본표는 추가반격0회. 1/2회 시나리오는 전투 시작 반격 피해−50% 디버프가 없는 시점의 기준.

**한계·가드레일:** 페인트가 반격을 켜지는 않지만 결투가 직업은 전투 시작2턴 반격 보유. 반격 횟수와 피격은 보장되지 않는다. 기존 반격 피해 전부를 이번 강화의 이득으로 넣지 않는다.

### R-AUDIT-26-REACH — 대상열·사용열·회피0 적과 대열 이동

1열 한정 기술과 전열/후열 접근성을 같은 적 평균으로만 비교하지 않는다.

```text
기본4던전 initial mash weights에서 legalTargets=occupiedRanks∩targetRanks; 단일은 편성 weight/legalTargetCount, 광역은 각 합법 유닛당 weight. size2는 유닛1개. HP>0·실제 skill행이 있는 비보스 전투원 포함, DODGE=0도 허용. PullValue=기존 move_value(전체대열 전/후 위협)*P(hit AND moveSuccess).
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 기술별 실제 대상열의 적 집합, 선택은 균등. 사용열은 실행 가능 조건으로 명시하고 임의 위치 감점은 만들지 않음.

**한계·가드레일:** 이동은 기존 최선 타깃 선택 모형, 직접 피해는 균등 선택이라 완전한 공동 정책이 아님. 전진/후퇴는 항상 손실로 처리하지 않는다. 미관측 전투/최적 플레이 빈도라고 주장하지 않는다.

### R-AUDIT-26-GEAR — 장신구의 활성 조건과 착용 대가

약화 성공률만 올리고 회피·스트레스 대가를 누락한 순위화를 피한다.

```text
ACC'=ACC+activeACC; crit'=crit+activeCrit; weaponMin/Max'=weaponMin/Max*(1+activeDamageMod); chance'=chance+activeDebuffChance (pull/push는 moveChance). V_skill_with_gear를 동일 시나리오로 재계산. exposureCost_per_action=E[T_to_wearer(gearDodge,gearStressMult)-T_to_wearer(baseDodge,0)].
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 461개 관련 직업/공용 항목 조사, 직업별 대표 약화 장신구1개 및 집중의 반지 조합 비교. 활성 rule과 불충족 조건을 따로 기록.

**한계·가드레일:** 모든 장신구2개 조합의 최적화나 전체 순이익 순위가 아니다. CC세트2개 미착용이면 세트이득0. 이번 공격이 새로 만드는 표식으로 이번 명중 보너스를 소급하지 않는다. 최대HP/미덕/저항 등 상황 대가는 문서와 원자료에 남김.

### R-AUDIT-26-UTILITY — 표식·은신·시체·호위·횃불의 범위

빈도가 없는 상황 효과를 항상 발동한다고 꾸미지 않는다.

```text
표식·은신 해제·시체·자기 속도/표식 위험은 strength.py의 공개된 기존 HP prior를 재사용. 현재 호위가 없으면 guard utility0. 호위자PROT.75→의도한타깃.4의 후속 평타 이득=E[h*(D(.4)-D(.75))], 방어 감소 자체 이득과 분리. Clear Guarded Target는 on_hit/on_miss 모두 true라 기존호위해제에는 opening h를 곱하지 않음. 새 호위 차단은 명중 조건. 횃불은 제외.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 기존 priors MARK_PARTY2HP, CORPSE.5HP, DESTEALTH1.14HP 및 대상열 커버리지. 실제 상태가 없으면 관련 이득0이어야 하는 시나리오 해석.

**한계·가드레일:** 조건별 완전 전투 시뮬레이션이 아니다. guard 예시는 초과피해/호위자 처치 전이가 없는 조건부 값이며 발생빈도를 임의로 총점에 더하지 않는다.

### R-AUDIT-26-FINITE — HP 상한을 둔 준비 행동 손익분기

적이 이미 죽었는데 추가 공격 이득이 계속 쌓이는 과대평가를 줄인다.

```text
F(H,n,P)=sum_outcomes q*[min(H,d)+F(max(0,H-d),n-1,P)], F(H,0,P)=0. setup경로는 miss/normal/crit 및 armor success 분기, baseline경로는 같은 시전자 무기·ACC105·기술치명0·피해100% 평타. deltaHP=E[setup+F]-E[basic+F]; deltaPP=100*deltaHP/B.
```

**단위:** HP-equivalent; fixed-standard percentage-points; chance in probabilities, ACC/DODGE in points; rounds and attacks explicit

**입력·가정:** 적HP60,DODGE20,약화저항60%; 후속은 현재 성전사/나병/현상금의 표준 평타 동등 가중, n0..4 모두 만료 전. 105개 시나리오.

**한계·가드레일:** 직접피해+방어 감소만 분리한 기회비용. 실제 특정 평타의 사용열/치명/고유효과까지 같은 대안이라고 주장하지 않는다. 다른 기술효과·재적용·추가 적 행동은 별도.

## 재현과 의미 정리 범위

`python tools/armor_audit.py --output <새 결과 폴더>`

전체 Python 계산은 저장소 도구로 재현한다. 이어담의 실행 허용 목록에는 이 전체 모형 adapter가 없으므로, 공식 검색/버전 보존과 MCP 계산 실행을 혼동하지 않는다. 이번 작업에서 이어담 프로그램을 수정하거나 허용 목록을 우회하지 않았다.

이전 검증: 11개 핵심 검증, 252개 평가, 8,775개 유한 수, 별도 실행 수치 동일. 이번에는 모델 코드 해시와 이어담 14개 공식의 readback을 확인했다. 수학식·기본 입력·결과·원문 event ID·코드 SHA256은 [JSON 기록](armor-model-formulas-20261025.json)에 함께 보관했다.

기존 R-VALUE-04 및 전체 영웅 순위 경로를 자동 교체하지 않았다. 잔차라는 표현도 회귀 설계가격과 HP 시나리오의 공통 평타 차이를 구분한다. 전체 과거 대화의 의미 정리 완료를 주장하지 않는다.

푸시 대상은 현재 test다. 현재 기록 외에 test에 이미 커밋돼 있던 승인된 변경도 그 브랜치 이력으로 함께 올라간다. main 병합과 창작마당 게시 요청으로 확대하지 않는다.
