# Rebalance — Patch notes (full)


## Abomination
- **Transform** [ABO-004] (P-23, P-12) — Self stress relief 4–8 on transforming; beast form stress per turn 6 → 4. The cost to allies stays — this gives a reason to transform at all.
- **Manacles** [ABO-005, ABO-006] (P-23, R-STUN-03) — Accuracy 95 → 90, the baseline for damaging stuns. Damage unchanged; his large weapon already puts it near the top of stun skills.
- **Beast's Bile** [ABO-002, ABO-007] (P-23, G-01) — Accuracy 95 → 90, damage −90% → −75%. Human-form accuracy comes down and base output goes up, closing the gap with beast skills (accuracy 85–90).
- **Slam** [ABO-001, ABO-003] (P-23, G-03) — Usable ranks 1-2-3 → 2-3-4, debuffs removed, accuracy 80 → 90, damage −25% → 0%. The beast had nothing to do from rank 4; now it slams from the back and moves forward.
- **mode** [ABO-004] (P-23, P-12) — Self stress relief 4–8 on transforming; beast form stress per turn 6 → 4. The cost to allies stays — this gives a reason to transform at all.

## Antiquarian
- **Flashpowder** [ANT-001] (P-19, P-25) — 

## Arbalest
- **Sniper Shot** [ARB-005] — Support marked-target specialization; retain the existing top-level ceiling.
- **Sniper Shot** [ARB-012] (P-21, P-19) — 
- **Suppressing Fire** [ARB-008] (R-STRAT-01) — 
- **Bola** [ARB-007, ARB-004] (P-01) — Level 5 push now uses the intended effect (1D 105% → 1E 115%). Bug fix: 1E exists in the base game but was never linked.
- **Battlefield Bandage** [ARB-001, ARB-002] (G-05, G-00, P-18, P-15) — battlefield_bandage: heal 2-3/4-5 -> 3-3/6-7, Arb Stacking Heal -> RB ARB Cure Bleed
- **Rallying Flare** [ARB-009, MAA-008, ARB-006, ARB-003] (G-00, P-11, G-05, P-22) — Rallying Flare stress recovery guaranteed at all levels; keep other-ally amounts 3/3/4/4/5 and utility effects unchanged.
// ARB-003 [trace 2026-10-05] Add an alternative party stress recovery option with stable low-level chance.

## Bounty Hunter
- **Collect Bounty** [BH-003] (R-EFF-05, G-01) — [2026-10-06] Keep current marked-target specialization and restored rank layout; attach the existing change ID without changing skill data.
- **Mark for Death** [BH-013] — 
- **Come Hither** [BH-010, BH-009] (G-02, P-22, R-TRADE-01, R-STRAT-01, G-01) — 
- **Uppercut** [BH-007, BH-014, BH-015] (G-02, G-03, G-01, P-19, R-CMB-08) — uppercut: target 12 -> 1, dmg -67% -> -45%, crit +0~4 -> +9~13 (launch 21 kept)
- **Flashbang** [BH-008] (G-03, G-02, P-19, P-11) — [2026-10-06] Keep rank34 flash control separate from front Uppercut, paying with normal stun; restore the missing trace ID only.
- **Finish Him** [-] — 
- **Caltrops** [BH-005, BH-016] (R-TRADE-01, G-02, G-03, R-RANK-01) — 

## Crusader
- **Zealous Accusation** [CRU-002] (G-02) — Accuracy 85 → 90, so there are fights where it beats Smite (a −40% AoE with low accuracy on top had no reason to be picked).
- **Stunning Blow** [CRU-003, CRU-008, CRU-009] (R-STUN-01, P-19) — Normal stun → strong stun (damage −50% unchanged). The standard front-line stun; the Crusader's signature skill now stuns as reliably as its name says.
- **Bulwark of Faith** [CRU-007] (P-19) — 
- **Battle Heal** [CRU-001] (G-05, G-00, P-11, R-VALUE-11, R-VALUE-12) — Trade immediate healing for followup healing received on the target.
- **Inspiring Cry** [CRU-006] (G-00, P-11) — [2026-10-06] Inspiring Cry stress recovery 5/5/6/7/8 -> 5/6/7/8/9; improve non-Jester concentrated support and preserve healing, torch and targeting.

## Duelist
- **touche** [DUE-005] — 
- **feint** [DUE-007] — 
- **coup_de_grace** [DUE-010] — 
- **the_boot** [DUE-006, DUE-004, DUE-001, DUE-003, DUE-002, DUE-008, DUE-009] (R-STUN-01, R-STRAT-01, G-02, G-03, P-11) — Damage −40% → −60%. A melee skill that stuns and pushes at once, yet it gave up less damage than other stuns. −60% sits inside the damage range of stun skills (−40 to −75%).

## Flagellant
- **resistances** [FLA-001] (G-04, R-RES-01) — Bleed resist 65 → 60. Matches the base game's cap for a hero's signature resist (baseline +30).
- **weapon** [FLA-007] (G-04, R-GROW-03) — Weapon speed 6/6/8/8/9 → 6/6/7/7/8. Brings an exception back to the base game's growth rule.
- **weapon** [FLA-007] (G-04, R-GROW-03) — Weapon speed 6/6/8/8/9 → 6/6/7/7/8. Brings an exception back to the base game's growth rule.
- **weapon** [FLA-007] (G-04, R-GROW-03) — Weapon speed 6/6/8/8/9 → 6/6/7/7/8. Brings an exception back to the base game's growth rule.
- **Reclaim** [FLA-005] (G-02, G-05, P-22, R-RES-02) — Match ally HOT output to the self-bleed cost across skill levels.

## Grave Robber
- **Thrown Dagger** [GR-002, GR-005] (G-02, P-11, R-DATA-01, P-26) — thrown_dagger: GR Acc Buff moved to poison_dart
- **Poison Darts** [GR-001, GR-002] (R-SKILL-05, P-11, G-02, R-DATA-01) — Poison Dart blight 4 turns → 3 (the standard DoT duration); in exchange the self accuracy buff moves from Thrown Dagger to Poison Dart.
- **Toxin Trickery** [GR-003] (G-05, G-02, P-19) — Enable repeatable self upkeep with shorter and smaller defensive buffs.

## Hellion
- **Wicked Hack** [HEL-005] (G-02) — Accuracy 85 → 90, making her basic attack reliable now that exhaustion is gone.
- **Barbaric YAWP!** [HEL-009, HEL-008, HEL-001, HEL-006] (P-19, G-02, R-STRAT-01, P-20) — Stun, exhaustion and the 3-per-battle limit removed → self buff (accuracy +5, damage +20%, once per use) + all enemies deal 10–20% less damage (3 turns) + corpse clear; targets ranks 1-2 → all ranks. The un-cleansable, battle-long exhaustion (−20% damage, −3 speed) contradicted the relentless art.
- **Breakthrough** [HEL-002, HEL-008] (P-19, G-02) — Exhaustion removed, damage −50% → −55%. It was the weakest damaging AoE hitting ranks 2 and 3 (exhaustion cost most of its value).
- **Adrenaline Rush** [HEL-004] (G-05, P-12) — Its self buff moved to YAWP, leaving cure + self heal → self heal 1/2/2/3/4 → 3/4/5/6/7.
- **Bleed Out** [HEL-003] (P-19, P-21) — Exhaustion removed, damage +20% → 0%, crit modifier +6–10 → +10–14. Its rank-1-only target is now paid back with crit instead of damage; crits extend the bleed, which suits late-game armored enemies.

## Highwayman
- **Wicked Slice** [HWY-019, HWY-008, HWY-014, HWY-011] (R-SKILL-09, R-TRADE-02) — Keep a front melee alternative with the latest author-set accuracy and damage budget.
- **Pistol Shot** [HWY-009, HWY-015, HWY-012] (G-02, P-03, R-TRADE-02) — Accuracy 85 → 90. The median level-1 accuracy of the base game's 34 single-target damaging ranged skills is 90; Pistol Shot alone sat at 85, leaving his ranged build behind his melee one (logged as an exception to the 85 baseline of R-TRADE-02).
- **Point Blank Shot** [HWY-017, HWY-001] (R-TRADE-01, P-12, P-20, P-21) — Limit easy repeat cycles through two-rank retreat while preserving the heavy shot feel.
- **Grapeshot Blast** [HWY-020, HWY-007] (R-VALUE-12, P-21) — Trade damage for accurate critical-vulnerability setup instead of repeated AOE damage.
- **Tracking Shot** [HWY-019, HWY-004] (R-SKILL-09, G-02, G-03, P-19, P-11) — Enable stationary ranged riposte play instead of tying riposte to melee advance.
- **Duelist's Advance** [HWY-018, HWY-016, HWY-005, HWY-013] (G-02, G-03, P-19, P-11, R-CMB-09, R-STRAT-01) — Use advance for smaller self setup after transferring riposte to Tracking Shot.
- **Open Vein** [HWY-020, HWY-019, HWY-006] (R-VALUE-12, R-SKILL-09, G-02, P-21, P-20, R-CMB-08) — Retain bleed/debuff identity while recording the latest author-set accuracy/damage trade.

## Houndmaster
- **resistances** [HM-017] (P-22, R-RES-01) — Blight/Bleed resist 40 → 30. In the base game a resist only deviates from baseline when the hero's lore says so; this +10 has no such line (Trap +30 stays, backed by the guard-dog text).
- **Hound's Rush** [HM-019, HM-011, HM-010, HM-016, HM-018, MARK-01, HM-023] (G-00, P-11, G-04, R-VALUE-03, G-01, R-CMB-08, P-12, R-STRAT-02, R-TRADE-02, P-24, R-EFF-05) — [2026-10-06] Target all enemy ranks from all ally ranks; retain damage -25 and flat marked bonus +60 to favor versatility and support over sustained damage. Supersedes HM-011 target234.
- **Hound's Harry** [HM-012] (G-04, R-VALUE-04) — Support the rear AOE bleed option after removing front-rank launch.
- **Target Whistle** [HM-020, HM-021] (P-19, R-VALUE-17) — 
- **Cry Havoc** [HM-014] (G-02, G-05, P-12) — Levels 1–4: stress heal 2/3/4/5 → 4/4/5/5, chance 66/68/70/72% → 70/71/72/73% (level 5 stays 74%, so every level still grows). Fixes only the low-level unreliability of the party-wide stress heal.
- **Guard Dog** [HM-025] (P-24) — 
- **Lick Wounds** [HM-015] (G-04, R-STRAT-02) — Allow self recovery in the front rank where incoming damage is frequent.
- **Blackjack** [HM-013, HM-022, HM-024] (R-STUN-03, P-11, R-STUN-02) — Accuracy 95 → 90, strong stun → normal stun, damage −65% → −50%. It was the only melee stun that both reaches rank 3 and stuns at the strong tier; accuracy and stun tier come down, damage goes up in return.

## Jester
- **Solo** [JES-011, JES-008, JES-009, JES-007, JES-001, JES-005, JES-006] (P-19, R-DATA-01) — Solo dodge 25/27/30/32/35 via dedicated effects; JES-005 all-rank launch and two uses retained. / Solo usable from ranks 1/2/3/4; improve front-rank dodge/mark use and skill selection. Existing effects, forward 3 and two uses per battle retained.
- **Battle Ballad** [JES-012, JES-002] (P-11) — Battle Ballad team speed 1/1/2/2/3 and critical bonus 1/2/3/4/5%; accuracy and Finale-specific preparation retained. / [intent 2026-10-06] High-speed Jester plus party speed can dominate initiative and suppress enemy stress actions; reduce speed to preserve turn-order choices. / [intent 2026-10-06] Critical bonuses also trigger class critical benefits and stress recovery; combined with Inspiring Tune this can over-supply party stress management.
- **Inspiring Tune** [JES-003] (G-03, G-05) — Inspiring Tune usable from ranks 2/3/4; stress healing and stress resistance retained.

## Leper
- **Intimidate** [LEP-001, LEP-002, LEP-003, LEP-004, LEP-005] — 

## Man At Arms
- **weapon** [MAA-001] (G-01, P-03) — Weapon max damage 9/10/12/13/14 → 10/12/13/15/16 (min unchanged). He sat furthest below the HP-to-damage trend across all 20 heroes; 5-10 is the existing preset of comparable heroes (Bounty Hunter, Highwayman).
- **weapon** [MAA-001] (G-01, P-03) — Weapon max damage 9/10/12/13/14 → 10/12/13/15/16 (min unchanged). He sat furthest below the HP-to-damage trend across all 20 heroes; 5-10 is the existing preset of comparable heroes (Bounty Hunter, Highwayman).
- **weapon** [MAA-001] (G-01, P-03) — Weapon max damage 9/10/12/13/14 → 10/12/13/15/16 (min unchanged). He sat furthest below the HP-to-damage trend across all 20 heroes; 5-10 is the existing preset of comparable heroes (Bounty Hunter, Highwayman).
- **weapon** [MAA-001] (G-01, P-03) — Weapon max damage 9/10/12/13/14 → 10/12/13/15/16 (min unchanged). He sat furthest below the HP-to-damage trend across all 20 heroes; 5-10 is the existing preset of comparable heroes (Bounty Hunter, Highwayman).
- **weapon** [MAA-001] (G-01, P-03) — Weapon max damage 9/10/12/13/14 → 10/12/13/15/16 (min unchanged). He sat furthest below the HP-to-damage trend across all 20 heroes; 5-10 is the existing preset of comparable heroes (Bounty Hunter, Highwayman).
- **Rampart** [MAA-006, MAA-014] (G-01, G-02, G-03, P-19) — [current 2026-10-05] Remove Rampart self forward movement at all levels; retain -60% damage, enemy push and stun to control without displacing allies.
- **Bellow** [MAA-002, HEL-001] (P-19, R-VALUE-05, R-VALUE-01, R-TRADE-01, R-TRADE-02, R-VALUE-02, G-02, R-STRAT-01) — Stun, exhaustion and the 3-per-battle limit removed → self buff (accuracy +5, damage +20%, once per use) + all enemies deal 10–20% less damage (3 turns) + corpse clear; targets ranks 1-2 → all ranks. The un-cleansable, battle-long exhaustion (−20% damage, −3 speed) contradicted the relentless art.
- **Retribution** [MAA-004] (P-19, R-VALUE-07, G-02) — Trade rank-3 reach for front riposte damage while preserving the three-turn support loop.
- **Command** [MAA-012, MAA-009, MAA-008] (P-19) — 
- **Bolster** [MAA-011, MAA-010, MAA-007, MAA-005] (P-19, P-22, P-14, G-05) — Add immediate morale recovery to a buff whose benefit otherwise accumulates later.

## Occultist
- **Weakening Curse** [OCC-007] — 
- **Wyrd Reconstruction** [OCC-001] — wyrd level 5: heal 0-22 -> 0-20; reuse level 4 bleed (2 x 3, 80%). Preserve gambling identity and remove the final upgrade cost spike.
- **Vulnerability Hex** [OCC-003, OCC-004, OCC-005, OCC-006, OCC-009] (R-VALUE-15, R-VALUE-16, R-SKILL-05) — 
- **Hands from the Abyss** [OCC-008] — 

## Plague Doctor
- **Incision** [PD-002] — 
- **Battlefield Medicine** [PD-001] (G-05, G-00, P-18, P-15) — Differentiate allied blight treatment from the Arbalest bleed-heal option.

## Runaway
- **ransack** [RUN-001] — 

## Shieldbreaker
- **resistances** [SB-010] (P-22, R-RES-01) — Use the documented light-armour lore comparison for stun and movement resistance.
- **weapon** [SB-011] (G-04, R-GROW-03) — Weapon speed 5/6/8/8/9 → 5/5/6/6/7. Brings an exception back to the base game's growth rule (level-1 value + floor((n−1)/2)).
- **weapon** [SB-011] (G-04, R-GROW-03) — Weapon speed 5/6/8/8/9 → 5/5/6/6/7. Brings an exception back to the base game's growth rule (level-1 value + floor((n−1)/2)).
- **weapon** [SB-011] (G-04, R-GROW-03) — Weapon speed 5/6/8/8/9 → 5/5/6/6/7. Brings an exception back to the base game's growth rule (level-1 value + floor((n−1)/2)).
- **weapon** [SB-011] (G-04, R-GROW-03) — Weapon speed 5/6/8/8/9 → 5/5/6/6/7. Brings an exception back to the base game's growth rule (level-1 value + floor((n−1)/2)).
- **Pierce** [SB-013, SB-002] (G-04, R-VALUE-20, P-09) — Target ranks 1-2-3-4 → 1-2-3, crit modifier +5–9 → +2/3/4/4/4. Melee + armor piercing + reaching every rank was the core Shieldbreaker problem; a melee skill reaching rank 4 is a rare premium, so rank 4 is removed.
- **Impale** [SB-014, SB-018] — Record the author-set accuracy exchange and early-level DOT addition without applying old release proposals.
- **Expose** [SB-015] — Trade accuracy with Pierce to favor the effect-bearing control skill.
- **Captivate** [SB-016] — Support the author-set accuracy exchange and secondary marked-target damage role.
- **Serpent Sway** [SB-017] — 

## Vestal
- **Mace Bash** [VES-001] — Move self healing to the front attack to enable a front support build.
- **Judgement** [VES-002, VES-009, VES-001] — Keep a rear-reaching damage choice after moving self healing to Mace Bash.
- **Dazzling Light** [VES-003, VES-008] — Separate rear stun from front play without removing its vanilla damage.
- **Divine Grace** [VES-004] — Offer predictable healing and allow front-rank support.
- **Divine Comfort** [VES-005] — Keep strong party healing rear-only and smooth early upgrade values.
- **Illumination** [VES-010, VES-006, VES-011, VES-012, VES-013] (R-SKILL-09, P-20, P-19, R-VALUE-19, R-DATA-01) — Provide an all-rank utility option for front Vestal play.
- **Hand of Light** [VES-007] (R-TRADE-02, G-02) — Accuracy 85 → 90. A ranged skill whose job is the ally buff it applies on hit; for effect-first skills accuracy takes priority.
