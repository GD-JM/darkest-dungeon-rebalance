# 분석 자료 목록

제작자가 "예전에 본 ○○ 보여줘"라고 하면 Claude는 **새로 만들지 않고** 이 목록에서 찾아 그 파일 내용을 보여 준다.
- 파일 머리의 생성일·데이터 커밋을 함께 알린다. 그 뒤 데이터가 바뀌었으면 "갱신할까요?"만 묻는다.
- 대화에서 표·비교를 새로 만들면 여기에 파일로 저장하고 한 줄을 추가한다(대화에만 남기지 않는다).
- 수치 순위는 `python tools/strength.py`(매번 계산), 변경 기록은 `../changes/<영웅>.md`.

| 파일 | 내용 | 찾는 말 | 날짜 |
|---|---|---|---|
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
| [musketeer-full-review.txt](musketeer-full-review.txt) | 총사 전수 검토 | 총사 | 2026-10-05 |
| [comment-trace-cleanup.md](comment-trace-cleanup.md) | 주석·의도 전수 보완 기록 | 주석 | 2026-10-05 |
