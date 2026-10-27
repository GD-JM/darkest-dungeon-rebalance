# 분석 자료 목록

제작자가 "예전에 본 ○○ 보여줘"라고 하면 Claude는 **새로 만들지 않고** 이 목록에서 찾아 그 파일 내용을 보여 준다.
- 파일 머리의 생성일·데이터 커밋을 함께 알린다. 그 뒤 데이터가 바뀌었으면 "갱신할까요?"만 묻는다.
- 대화에서 표·비교를 새로 만들면 여기에 파일로 저장하고 한 줄을 추가한다(대화에만 남기지 않는다).
- 수치 순위는 `python tools/strength.py`(매번 계산), 변경 기록은 `../changes/<영웅>.md`.

| 파일 | 내용 | 찾는 말 | 날짜 |
|---|---|---|---|
| [workshop_languages.md](workshop_languages.md) | 다키스트 던전 사용 언어층(스팀 리뷰 언어별) → 창작마당 번역 대상 10개 언어 | 창작마당·번역 | 2026-10-17 |
| [workshop_total_power.md](workshop_total_power.md) | 창작마당판 전체 강함 총량 점검 (바닐라 981 → 976, 편차 14.1 → 12.2) | 창작마당·총량 | 2026-10-17 |
| [audit_2026-10-17/SUMMARY.md](audit_2026-10-17/SUMMARY.md) | 창작마당판 선별 전수 감사: 실제 데이터 차이 전부를 W(검증)/C(주관)/X(원칙 위배)/V로 분류, W 12건, X 목록, 낡은 기록, 패키징 | 창작마당, 감사, 원칙 위배, 검증된 변경 | 2026-10-17 |
| [chat/INDEX.md](chat/INDEX.md) | 지난 대화에서 만든 분석 답변 243개 원문(날짜·질문별). 질문 문구로 찾는다 | 지난번에 본 표, 비교, 예전 분석 | 2026-09-12~10-11 |
| [buff_debuff_map.md](buff_debuff_map.md) | 영웅 5렙 기술의 강화·약화를 대상(적 1명/적 전체/아군/자신)×능력치로 분류. 재생성 `tools/buff_map.py` | 버프 분포, 약화 분포, 겹치는 효과, 표식 | 2026-10-11 |
| [hm_vs_bh.md](hm_vs_bh.md) | 조련사 vs 현상금 사냥꾼: 영웅 능력치·기술 7개씩 전부·역할 겹침 판정 | 조련사 현상금 비교, 경쟁군, 표식 딜러 | 2026-10-14 |
| [hero_lore.md](hero_lore.md) | 영웅 공식 설정(길드·대장간·야영 문구, 직업 치명타 버프, 전용 장신구) | 설정, 스토리, 장신구 | 2026-09-27 |
| [hero_power_v2.md](hero_power_v2.md) | 강함 순위 모델 v2 설명 | 강함 순위, 모델 | 2026-10-05 |
| [hero_power.md](hero_power.md) | 영웅 능력치·조건부 피해·과대 기술 | 능력치, 버프 기준선 | 2026-09-27 |
| [hero_ranks.md](hero_ranks.md) | 영웅 주 열(기술 사용 열 기준) | 열, 위치 | 2026-09-15 |
| [burn_synergy.md](burn_synergy.md) | 도망자 화상 연계: 화상 관련 효과·장신구 전수, 불 아트 기술, 섬광 가루·결집 신호탄에 화상 붙인 모델 값 | 화상, 도망자 시너지, 섬광 가루 | 2026-10-17 |
| [aoe23_survey.md](aoe23_survey.md) | 2·3열을 동시에 치는 광역 기술 전수(피해 있는 9·없는 5) + 꿰뚫기·돌파 수정안 비교. 재생성 `tools/reach34_survey.py aoe23`(후속 비교 절은 손으로 추가) | 2·3열 광역, 23 동시 타격 | 2026-10-15 |
| [reach34_survey.md](reach34_survey.md) | 3·4열을 칠 수 있는 기술 전수(피해 있는 57·없는 14), 마름쇠 vs 슬픔의 비. 재생성 `tools/reach34_survey.py`(집중 비교 절은 손으로 추가) | 3·4열 공격, 후열 공격, 마름쇠, 슬픔의 비 | 2026-10-15 |
| [front_aoe_stun.md](front_aoe_stun.md) | 1·2열 광역 기절 후보: 지금 1·2열 광역 기술 전부, 기절 추가 시 모델 값(볼라·성채의 일격 등) | 앞열 광역 스턴, 2열 광역 기절 | 2026-10-14 |
| [stun_survey.md](stun_survey.md) | 기절 전수 조사: RB·바닐라 기절 기술 전부(1~5렙 확률·효과), 기절 확률 장신구 16개, 몬스터 열별 위협. 재생성 `tools/stun_survey.py` | 기절 전수, 스턴 목록, 스턴 장신구 | 2026-10-14 |
| [stun_redesign.md](stun_redesign.md) | 3열 닿는 기절 가늠: 1·2열 기절 띠, 3열 도달 가격(+46~53), 손아귀·족쇄 후보 | 3열 기절, 스턴 가격, 기절 재설계 | 2026-10-14 |
| [stun_target123.md](stun_target123.md) | 대상 1·2·3열 기절 기술 4개 비교(명중·피해·기절 확률·모델 %p) | 123열 기절, 스턴 비교 | 2026-10-14 |
| [stun.md](stun.md) / [stun-reassessment.md](stun-reassessment.md) | 기절 기술 분석 / 전수 재검토(최신) | 기절 | 2026-10-05 |
| [displacement.md](displacement.md) | 밀치기·당기기 기술 | 밀치기, 당기기, 이동기 | 2026-09-14 |
| [dot.md](dot.md) | 출혈·중독(화상 부록) 기술 | 출혈, 중독, 지속 피해 | 2026-09-14 |
| [aoe.md](aoe.md) | 광역 공격 기술 | 광역 | 2026-09-15 |
| [dealers.md](dealers.md) | 딜러 비교 | 딜러 | 2026-09-15 |
| [heal.md](heal.md) / [heal_skills.md](heal_skills.md) | 회복 분석 / 회복 기술(체력·스트레스) | 회복, 스트레스 회복 | 2026-09-15 |
| [affliction.md](affliction.md) | 고통·미덕의 가치 (R-VALUE-06) | 고통, 붕괴, 스트레스 가치 | 2026-10-03 |
| [resistances.md](resistances.md) | 영웅 저항 설계 축 | 저항 | 2026-09-27 |
| [accuracy.md](accuracy.md), [accuracy_baseline.md](accuracy_baseline.md), [accuracy_budget.md](accuracy_budget.md), [accuracy_laws.md](accuracy_laws.md), [low_accuracy_skills.md](low_accuracy_skills.md) | 명중 분석 묶음 | 명중 | 2026-09-14 |
| [trinkets_rank.md](trinkets_rank.md) | 열 조건 장신구 | 장신구 | 2026-09-14 |
| [dlc_history.md](dlc_history.md) | DLC 영웅 패치 이력 | 패치, DLC | 2026-09-14 |
| [wiki_notes.md](wiki_notes.md) | 위키에서 얻은 엔진 규칙 | 위키 | 2026-10-10 |
| [leper-full-review.txt](leper-full-review.txt) | 나병환자 전수 조사 | 나병환자 | 2026-10-05 |
| [jester-full-review.txt](jester-full-review.txt), [jester-position-buff-options.txt](jester-position-buff-options.txt) | 광대 전수 조사, 위치 버프 선택지 | 광대 | 2026-10-05 |
| [comment-trace-cleanup.md](comment-trace-cleanup.md) | 주석·의도 전수 보완 기록 | 주석 | 2026-10-05 |
| [musketeer_identity.md](musketeer_identity.md), [musketeer_identity_dump.txt](musketeer_identity_dump.txt) | 총사 정체성: 창작마당판 빈 역할 전수 조사 | 총사, 정체성 | 2026-10-21 |
| [mark_survey.md](mark_survey.md) | 표식 전수 조사(영웅·직업 치명타·장신구·몬스터, 바닐라 대비) | 표식 | 2026-10-21 |
| [../backlog.md](../backlog.md) | 보류 아이디어 목록 (BL-01 현상금 이동 저항) | 보류 | 2026-10-21 |
| [lore_audit_A.md](lore_audit_A.md), [lore_audit_B.md](lore_audit_B.md), [lore_audit_C.md](lore_audit_C.md) | 공식 설정·전용 장신구·야영 기술 vs 현재 설계 전수 대조 (총사 제외 19명; A 괴인·유물·석궁·현상금·성전사·결투가 / B 고행자·도굴꾼·야만인·노상·조련사·광대 / C 나병·중보병·신비·역병·도망자·방패·성녀) | 설정, 장신구, 야영 | 2026-10-22 |
| [strength_2026-10-22.md](strength_2026-10-22.md) | 강함 순위 (R-VALUE-23 약화 기회비용 반영 후, 2.0.5 기준) | 순위, 모델 | 2026-10-22 |
| [bleed_distribution.md](bleed_distribution.md) | 출혈 기술 13개 열·형태·수치 분포, 출혈 대상 보너스, 조련사 출혈 특화 판단 | 출혈, 조련사 | 2026-10-23 |
| [trinket_direction_A.md](trinket_direction_A.md), [trinket_direction_B.md](trinket_direction_B.md), [trinket_direction_C.md](trinket_direction_C.md) | 장신구가 제시하는 방향(버프)·가드레일(패널티)로 본 19명(조련사 제외) 기술 대조, 최소 수정 제안 | 장신구, 방향, 가드레일 | 2026-10-23 |
| [trinket_viability_A.md](trinket_viability_A.md), [trinket_viability_B.md](trinket_viability_B.md), [trinket_viability_C.md](trinket_viability_C.md) | 전용 장신구 전수(20명) 바닐라 대비 현재 가치: 살아있음/약해짐/버려짐, 원인 ID·최소 수정안 (가드레일 = 버려지는 장신구 없게) | 장신구, 가드레일 | 2026-10-23 |
| [abomination_transform_stress.md](abomination_transform_stress.md) | 괴인 변신 스트레스 수지(억제의 자물쇠 포함), "깎으려고 변신" 방지 계산, ABO-008 | 괴인, 스트레스, 장신구 | 2026-10-23 |
| [debuff_survey.md](debuff_survey.md) | 약화 전수 조사: 영웅 20명 모든 기술·반격 1~5렙의 적 약화를 범주별(바닐라→현재), 영웅별 약화 확률 장신구, 몬스터·엔진에만 있는 미배분 약화 후보. 재생성 `tools/debuff_survey.py` | 약화 분포, 약화 평준화, 미배분 약화, 약화 다양화 | 2026-10-27 |
| [bleed_vs_blight_count.md](bleed_vs_blight_count.md) | 출혈 vs 중독 영웅 기술 수(바닐라 12/8 → 현재 12/8), 기술별 1~5렙 수치·대상, 몬스터 출혈 28/중독 22 | 출혈 개수, 중독 개수, 출혈 중독 비교 | 2026-10-27 |
| [buff_survey.md](buff_survey.md) | 강화(버프) 전수 조사: 영웅 20명 모든 기술·반격 1~5렙의 자신·아군 강화를 범주별(바닐라→현재)·받는 쪽(자신/아군 1명/아군 전체)·영웅별로. 재생성 `tools/buff_survey.py` | 버프 분포, 강화 분포, 파티 버프, 자기 강화 | 2026-10-27 |
| [antiq_curve_2026-10-27.md](antiq_curve_2026-10-27.md) | 유물수집상 P-25(챔피언에서 장신구로 비등) 레벨 곡선: 1~5렙 x 장신구 조합 점수, 시안 v2/v3. 재계산 `tools/antiq_curve.py` | 유물수집상, 레벨 곡선, 장신구 | 2026-10-27 |
