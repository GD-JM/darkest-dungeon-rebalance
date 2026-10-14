# 2·3열을 동시에 치는 광역 기술 전수 조사 (RB)

- 생성: 2026-10-15, 데이터 커밋 `f603495 R-VALUE-20 revised: front-rank reach +8% to rank 3, +15% to rank 4`, `python tools/reach34_survey.py aoe23`로 다시 만든다.
- 조건: 2·3열을 동시에 치는 광역 기술, 적 대상 기술 전부(손으로 고른 목록 없음). 명중·치명 보정은 1렙, 지속 피해는 "턴당×턴" 1~5렙, 모델(5렙) 표준 평타 7.7 HP 기준 %p.

## 피해 있는 공격 9개

| 영웅 | 기술 | 형태 | 사용 → 대상 | 명중 | 피해 | 치명 | 출혈 | 중독 | 화상 | 제한·모드·관통 | 모델(5렙) | 구성 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 노상강도 | 포도탄 발사 | 원거리 | 2·3 → ~123 | 90% | -60% | -9% | - | - | - | - | +75 | 직접+91 약화+73 치명타+10 |
| 야만인 | 돌파 | 근접 | 4·3·2 → ~123 | 85% | -60% | -1% | - | - | - | - | +36 | 직접+107 치명타+29 |
| 총사 | 산탄 | 원거리 | 4·3·2 → ~123 | 80% | +0% | -10% | - | - | - | - | +86 | 직접+182 치명타+5 |
| 방패 파괴자 | 꿰뚫기 | 원거리 | 1 → ~1234 | 85% | -60% | -6% | - | 1×3/1×3/1×3/1×3/2×3 | - | - | +127 | 직접+122 중독+53 치명타+23 전열→후열+30 |
| 조련사 | 사냥개 습격 | 원거리 | 4·3·2 → ~1234 | 90% | -70% | -5% | 1×3/1×3/2×3/2×3/3×3 | - | - | - | +86 | 직접+80 출혈+87 치명타+20 |
| 광대 | 수확의 낫질 | 근접 | 3·2 → ~23 | 90% | -50% | 0% | 2×3/2×3/3×3/3×3/4×3 | - | - | - | +58 | 직접+70 출혈+55 강화+16 치명타+17 |
| 괴인 | 아수의 담즙 | 원거리 | 3·2 → ~23 | 90% | -75% | 2% | - | 2×3/3×3/3×3/4×3/5×3 | - | human | +54 | 직접+54 중독+74 치명타+26 |
| 도굴꾼 | 번뜩이는 비도 | 원거리 | 4·3·2 → ~23 | 90% | -33% | -5% | - | - | - | - | +48 | 직접+96 약화+37 치명타+15 |
| 총사 | 연막탄 | 원거리 | 4·3 → ~23 | 90% | -100% | 0% | - | - | - | - | +24 | 직접+0 약화+29 기절+94 |

## 피해 없는 기술 5개

| 영웅 | 기술 | 형태 | 사용 → 대상 | 명중 | 피해 | 치명 | 출혈 | 중독 | 화상 | 제한·모드·관통 | 모델(5렙) | 구성 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 광대 | 독주 | 원거리 | 1·2·3·4 → ~1234 | 125% | -100% | 0% | - | - | - | 전투당 2회 | +142 | 시체+6 강화+225 약화+108 공격 유도+26 표식 위험-3 |
| 도망자 | hearthlight | 원거리 | 4·3·2·1 → ~1234 | 100% | -100% | 0% | - | - | - | ignore_stealth | +80 | 은신 해제+15 강화+166 |
| 석궁사수 | 결집 신호탄 | 원거리 | 4·3·2·1 → ~1234 | 95% | -100% | 0% | - | - | - | ignore_stealth | +97 | 은신 해제+15 스트레스+182 |
| 야만인 | 야만스러운 함성! | 근접 | 2·1 → ~1234 | 95% | -100% | 0% | - | - | - | - | +81 | 시체+6 강화+105 약화+45 전열→후열+24 |
| 중보병 | 포효 | 원거리 | 1·2·3·4 → ~1234 | 90% | -100% | 0% | - | - | - | - | +118 | 약화+211 시체+6 |

## 효과 원문 (1렙)

- 광대 수확의 낫질: target[dotBleed 2 100% 3t]; performer[buffs build_to_finale_dmgL,build_to_finale_dmgH 100% 8t]
- 광대 독주: performer[tag 100% 3t]; target_group[kill_enemy_types corpse 100%]; performer[defense 30% 100% 4t]; performer[buffs RB_JES_build_to_finale2_dmgL,RB_JES_build_to_finale2_dmgH,RB_JES_build_to_finale2_crit 100% 8t]; target[buffs SPD-1 100% 3t]; performer_group_other[ 100%]
- 괴인 아수의 담즙: target[dotPoison 2 100% 3t]; target[buffs Vomit,BlightResist,Debuff,1 100%]
- 노상강도 포도탄 발사: target[crit_received_chance 4% 100% 3t]
- 도굴꾼 번뜩이는 비도: target[buffs bleed_debuff_1 100% 3t]
- 도망자 hearthlight: target[unstealth 100%]; performer[torch_increase 6 100%]; performer_group[attack 5% 100% 3t]; performer_group[buffs rw_hearthlight_crit_vs_burning_1 100% 3t]
- 방패 파괴자 꿰뚫기: target[dotPoison 100% 3t]
- 석궁사수 결집 신호탄: global[torch_increase 3 100%]; target[unstealth 100%]; performer_group_other[healstress 2 100%]
- 야만인 야만스러운 함성!: target_group[kill_enemy_types corpse 100%]; performer[attack 5% damage_low× 20% damage_high× 20% 100%]; target[damage_low× -10% damage_high× -10% 100% 3t]
- 야만인 돌파: -
- 조련사 사냥개 습격: target[dotBleed 110% 3t]
- 중보병 포효: target[defense -5% speed -5 100% 3t]; target_group[kill_enemy_types corpse 100%]; target[buffs MAA_Bellow_CritReceived_1 100%]
- 총사 산탄: performer[buffs musk_buckshot_tooltip 100% 1t]; performer[buffs musk_armour_piercing_1 100% 1t]
- 총사 연막탄: target[speed -2 100%]; target[stun 85%]; target[buffs musk_smoke_stealth 500% 1t]; performer[buffs musk_smokescreen_tooltip 100% 1t]
