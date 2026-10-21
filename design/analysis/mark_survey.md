# 표식 전수 조사 (2026-10-21, 커스텀=창작마당 통합판)

수치는 1렙 / 5렙. 데이터: `tools/mark_survey.py`.

## 1. 영웅 기술

| 영웅 | 기술 | 종류 | 사용 | 대상 | 명중(1렙) | 피해 | 1렙 | 5렙 | 같은 기술의 다른 효과(1렙) |
|---|---|---|---|---|---|---|---|---|---|
| 석궁사수 | 저격수의 표식 | 걸기 | 43 | 234 | 100% | -100% | 표식 3턴 | 표식 3턴 | target: .curio_result_type "negative" .chance 100% .duration 2 .combat_stat_buff |
| 신비학자 | 취약화 주술 | 걸기 | 1234 | 1234 | 95% | -100% | 표식 3턴 | 표식 3턴 | target: .chance 100% .duration 3 .curio_result_type "negative" .buff_ids "STUNRE |
| 유물수집상 | 동료 방패 | 걸기 | 4321 | @1234 | 0% | 0% | 표식 3턴 | 표식 3턴 | target: .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_; performer: .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss t; target: .chance 100% .clearguarding 1 .clearguarded 1 .on_hit true .on_miss true; target: .swap_source_and_target true .chance 100% .guard 1 .on_hit true .on_miss |
| 조련사 | 목표물 지정 | 걸기 | 4321 | 1234 | 100% | -100% | 표식 3턴 | 표식 3턴 | target: .curio_result_type "negative" .chance 130% .duration 3 .combat_stat_buff |
| 총사 | 사냥감 지정 | 걸기 | 43 | 1234 | 100% | -100% | 표식 3턴 | 표식 3턴 | performer: .curio_result_type "positive" .chance 100% .duration 3 .buff_ids RB_M; performer: .curio_result_type "positive" .chance 100% .duration 3 .combat_stat_b |
| 현상금 사냥꾼 | 죽음의 표식 | 걸기 | 4321 | 1234 | 100% | -100% | 표식 3턴 | 표식 3턴 | target: .curio_result_type "negative" .chance 130% .combat_stat_buff 1  .protect |
| 결투가 | 눈속임 | 자기 표식 | 321 | 12 | 95% | -50% | 표식 2턴 | 표식 2턴 | performer: .chance 100% .duration 4 .buff_ids "DUELIST_FEINT_RIPOSTEDMGLBUFF1" " |
| 결투가 | 날쌘 돌진 | 자기 표식 | 432 | 123 | 90% | 25% | 표식 2턴 | 표식 2턴 |  |
| 고행자 | 고통 | 자기 표식 | 1234 | @1234 | 0% | 0% | 표식 2턴 | 표식 2턴 | target: .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_; target: .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_; performer: .curio_result_type "positive" .chance 100% .duration 4 .buff_ids flag; target: .chance 100% .clear_debuff 1 .on_hit true .on_miss false; performer: .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .speed |
| 광대 | 독주 | 자기 표식 | 1234 | ~1234 | 125% | -100% | 표식 3턴 | 표식 3턴 | target_group: .chance 100% .kill_enemy_types corpse .on_hit true .on_miss false ; performer: .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defen; performer: .curio_result_type "positive" .chance 100% .buff_ids "RB_JES_build_to; target: .curio_result_type "negative" .chance 100% .duration 3 .buff_ids "SPD-1" |
| 나병환자 | 인내 | 자기 표식 | 123 |  | 0% | 0% | 표식 1턴 | 표식 1턴 | performer: .curio_result_type "positive" .chance 100% .duration 1 .buff_duration; performer: .chance 100% .duration 1 .buff_duration_type combat_end .buff_ids lep |
| 성전사 | 신앙의 방패 | 자기 표식 | 4321 |  | 0% | 0% | 표식 1턴 | 표식 1턴 | performer: .curio_result_type "positive" .chance 100% .duration 1 .buff_duration; global: .chance 100% .curio_result_type "positive" .torch_increase 24	.on_hit tr |
| 중보병 | 응징 | 자기 표식 | 123 | 12 | 85% | -20% | 표식 2턴 | 표식 2턴 | performer: .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit |
| 노상강도 | 권총 사격 | 특효 | 432 | 234 | 90% | -15% | 피해 40% | 피해 60% |  |
| 도굴꾼 | 단검 투척 | 특효 | 432 | 234 | 90% | -10% | 피해 40% | 피해 80% | performer: .chance 100%	.curio_result_type "positive" .keyStatus "poisoned"	.com |
| 방패 파괴자 | 휘감기 | 특효 | 32 | 23 | 90% | -25% | 피해 50% | 피해 90% | target: .curio_result_type "negative" .chance 100%  .dotPoison 3 .duration 3	.on |
| 석궁사수 | 저격 | 특효 | 43 | 234 | 95% | 0% | 피해 60%, 치명 9% | 피해 100%, 치명 13% |  |
| 조련사 | 사냥개 돌진 | 특효 | 4321 | 1234 | 90% | -25% | 피해 60% | 피해 60% | performer: .chance 100% .curio_result_type "positive" .monsterType "beast" .comb; target: .curio_result_type "negative" .chance 100%  .dotBleed 1 .duration 2	.on_ |
| 총사 | 관통탄 | 특효 | 43 | 1234 | 90% | 0% | 피해 25%, 치명 9% | 피해 40%, 치명 13% | performer: .chance 100% .skill_instant true .duration 1 .buff_ids RB_MUS_AP_1 .o |
| 현상금 사냥꾼 | 현상금 수거 | 특효 | 321 | 12 | 85% | 0% | 피해 100% | 피해 100% | performer: .chance 100% .curio_result_type "positive" .monsterType "man" .combat |
| 결투가 | 눈속임 | 특효(강화) | 321 | 12 | 95% | -50% | combat_stat_add attack_rating -10% (3턴) | combat_stat_add attack_rating -10% (3턴) | performer: .chance 100% .duration 4 .buff_ids "DUELIST_FEINT_RIPOSTEDMGLBUFF1" " |
| 중보병 | 포효 | 특효(강화) | 1234 | ~1234 | 90% | -100% | crit_received_chance  +5% (?턴) | crit_received_chance  +5% (?턴) | target: .curio_result_type "negative" .chance 100% .duration 3  .combat_stat_buf; target_group: .chance 100% .kill_enemy_types corpse .on_hit true .on_miss false  |
| 고행자 | 고통 | 표식 해제 | 1234 | @1234 | 0% | 0% | 표식 해제 | 표식 해제 | target: .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_; target: .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_; performer: .curio_result_type "positive" .chance 100% .duration 4 .buff_ids flag; target: .chance 100% .clear_debuff 1 .on_hit true .on_miss false; performer: .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .speed |
| 광대 | 독주 | 표식 해제 | 1234 | ~1234 | 125% | -100% | 표식 해제 | 표식 해제 | target_group: .chance 100% .kill_enemy_types corpse .on_hit true .on_miss false ; performer: .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defen; performer: .curio_result_type "positive" .chance 100% .buff_ids "RB_JES_build_to; target: .curio_result_type "negative" .chance 100% .duration 3 .buff_ids "SPD-1" |

## 2. 직업 치명타 버프 (표식 관련)

- 석궁사수: combat_stat_multiply damage_low +33% (표식 대상, 2턴)
- 석궁사수: combat_stat_multiply damage_high +33% (표식 대상, 2턴)
- 현상금 사냥꾼: combat_stat_multiply damage_low +33% (표식 대상, 2턴)
- 현상금 사냥꾼: combat_stat_multiply damage_high +33% (표식 대상, 2턴)
- 총사: combat_stat_multiply damage_low +33% (표식 대상, 2턴)
- 총사: combat_stat_multiply damage_high +33% (표식 대상, 2턴)

## 3. 장신구 (표식 조건)

| 장신구 | 영웅 | 등급 | 표식 관련 효과 | 다른 효과 |
|---|---|---|---|---|
| 불프의 옷 장식 | 공용 | trophy | combat_stat_multiply damage_low +20% [actorStatus]; combat_stat_multiply damage_high +20% [actorStatus]; combat_stat_add attack_rating +10% [actorStatus] | combat_stat_add crit_chance +5% |
| Aru | 공용 | kickstarter | stress_dmg_received_percent  +10% [actorStatus] | resistance trap +5%; combat_stat_add defense_rating +3%; resistance disease +5% |
| Negus visage | 공용 | kickstarter | combat_stat_add attack_rating +6% [actorStatus] | combat_stat_add attack_rating +6%; combat_stat_add attack_rating +6%; hp_heal_percent  -13%; resolve_check_percent  -8%; food_consumption_percent  +50% |
| The News | 공용 | kickstarter | combat_stat_add attack_rating +6% [actorStatus] | hp_heal_received_percent  +17%; resistance death_blow +6%; combat_stat_add speed_rating -400%; combat_stat_add protection_rating -6%; resolve_check_percent  -8% |
| Shigless Requium | 공용 | kickstarter | resistance bleed -10% [actorStatus] | combat_stat_add attack_rating +6%; combat_stat_add crit_chance +5%; combat_stat_add defense_rating +8%; resistance disease -10%; resistance move -10% |
| Shroud of Living Failures | 공용 | kickstarter | combat_stat_add speed_rating +400% [actorStatus] | combat_stat_multiply damage_low +10%; combat_stat_multiply damage_high +10%; combat_stat_add crit_chance +4%; combat_stat_add defense_rating -6%; stress_dmg_received_percent  +10% |
| Bloodstained Bounty List | 공용 | kickstarter | combat_stat_add crit_chance +5% [actorStatus]; combat_stat_multiply damage_low +13% [actorStatus]; combat_stat_multiply damage_high +13% [actorStatus]; combat_stat_add attack_rating -5% [actorStatus] |  |
| Pamplemousse | 공용 | kickstarter | combat_stat_multiply damage_low +15% [actorStatus]; combat_stat_multiply damage_high +15% [actorStatus] | combat_stat_add defense_rating +9%; combat_stat_add attack_rating -5%; stress_dmg_received_percent  +10% |
| The Mantle of the Owl | 공용 | kickstarter | combat_stat_add attack_rating +6% [actorStatus] | combat_stat_add crit_chance +5%; stress_dmg_received_percent  +10% |
| The Tattered King | 공용 | kickstarter | combat_stat_add crit_chance +6% [actorStatus] | monsters_surprise_chance  +8%; resistance death_blow -6%; stress_dmg_received_percent  +10% |
| Headhunter's Herbs | 공용 | kickstarter | combat_stat_add attack_rating +6% [actorStatus]; combat_stat_multiply damage_low +13% [actorStatus]; combat_stat_multiply damage_high +13% [actorStatus]; combat_stat_add crit_chance +5% [actorStatus] | combat_stat_multiply max_hp -10%; hp_heal_received_percent  -13%; resistance stun -10% |
| 금박 망토 | 결투가 | uncommon | crit_received_chance  -6% [is_actor_status]; combat_stat_add defense_rating +10% [is_actor_status] | crit_received_chance  -6% |
| 잠잘 때 듣는 이야기 | 석궁사수 | crimson_court | combat_stat_add attack_rating +15% [actorStatus]; combat_stat_add crit_chance +8% [actorStatus] | debuff_chance  +35%; move_chance  +35% |
| 범죄 거물의 어금니들 | 현상금 사냥꾼 | crimson_court | combat_stat_multiply damage_low +20% [actorStatus]; combat_stat_multiply damage_high +20% [actorStatus] | combat_stat_multiply damage_low +20%; combat_stat_multiply damage_high +20%; combat_stat_multiply damage_low +20%; combat_stat_multiply damage_high +20%; combat_stat_add defense_rating -10% |
| 은 화승총 탄환 | 총사 | crimson_court | combat_stat_add attack_rating +15% [actorStatus]; combat_stat_add crit_chance +8% [actorStatus] | debuff_chance  +35%; move_chance  +35% |
| 송곳니 창끝 | 방패 파괴자 | shieldbreaker | combat_stat_multiply damage_low +35% [actorStatus]; combat_stat_multiply damage_high +35% [actorStatus] | combat_stat_multiply damage_low -10%; combat_stat_multiply damage_high -10% |

## 4. 몬스터 (영웅 등급 _C)

- 특효 11개: carrion_eater_C/munch, carrion_eater_big_C/tentacle_devour, cultist_brawler_C/brawler_claw, fanatic_C/holy_stake, fungal_bloat_C/fierce_swipe, skeleton_arbalist_C/crossbow_shot, spider_spitter_C/spider_bite, spider_spitter_C/spider_spit, spider_webber_C/spider_bite, swine_prince_C/obliterate_marked_one, swine_prince_C/obliterate_marked_two
- 걸기 18개: carrion_eater_big_C/weaken_prey, castellan_C/enraging_slight, collector_C/life_steal, courtesan_C/damsel_in_distress, courtesan_C/expose_the_vein, courtesan_C/rebuff_slap, crone_C/curse_vulnerability, cultist_witch_C/cultist_incantation, esquire_C/needling_execration, fanatic_C/brand_tainted, foreman_C/no_tresspassers, fungal_artillery_C/artillery_tag, spider_webber_C/spider_web, steward_C/enraging_slight, swine_drummer_C/drum_debuff, swine_piglet_C/wilbur_mark_1, swine_piglet_C/wilbur_mark_2, virago_hateful_C/ruinous_hex
- 표식 해제 2개: swine_prince_C/obliterate_marked_one, swine_prince_C/obliterate_marked_two
- 자기 표식 1개: steward_C/gibbering_entourage

## 6. 바닐라 대비 (5렙 표식 대상 피해 / 표식 걸기에 붙은 효과)

| 영웅 | 기술 | 바닐라 | 지금 |
|---|---|---|---|
| 현상금 사냥꾼 | 죽음의 표식 | 방어 −10~−20%(3턴) + 자기 속도 +3~5 | 방어 −20~−30%(130~170%) — 바닐라 조련사 휘파람 효과(Hound Debuff)를 옮김(BH-013) |
| 현상금 사냥꾼 | 이리 오너라 | 당기기 2 + **표식** | 당기기 3, 표식 없음 |
| 조련사 | 목표물 지정 | 방어 −20~−30% | 명중 −25~−30% (P-24 딜↓ 유틸↑) |
| 석궁사수 | 저격수의 표식 | 회피 −20~−30%(2턴) | 같음 |
| 신비학자 | 취약화 주술 | 회피 감소 등 | 기절·중독·출혈·약화 저항 −15~−20% |
| 총사 | 사냥감 지정 | 회피 −20~−30%(석궁 복제) | 자기 속도 +3~5, 대형 상대 치명 +4~8% |
| 현상금 사냥꾼 | 현상금 수거 | +90% | +100% |
| 석궁사수 | 저격 | +50~100%, 치명 +9% | +60~100%, 치명 +9~13% |
| 조련사 | 사냥개 돌진 | +60~100% | +60% |
| 방패 파괴자 | 휘감기 | +40~60% | +50~90% |
| 도굴꾼 | 단검 투척 | +25~40% | +40~80% |
| 노상강도 | 권총 사격 | +25~50% | +40~60% |
| 총사 | 관통탄 | +50~100%(조준사격) | +25~40%, 치명 +9~13% |
