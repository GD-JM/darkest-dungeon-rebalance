# 영웅 공식 설정 (게임 데이터 원문)

게임 로컬라이제이션에서 그대로 추출했다. 2차 해석이 아니라 **1차 출처**다.

계층 구분은 제작자 지정(2026-09-27):
1. 선조의 모집 대사 — 첫인상·핵심 이미지 (18/20 확보)
2. **길드** — 전투 역할·전술·강약점 선언. **리워크 시 최우선 준거** (20/20)
3. **대장간** — 무기·방어 방식·신체 특성 (20/20)
4. 야영 트레이너 — 전투 밖 성격·행동 (20/20)
5. Darkest Dungeon Presents (공식 코믹) — **게임 파일에 없음. 외부 1차 출처**
6. 전용 장신구 + 대사 — 과거·욕망·트라우마 단서

요양원·여관 문구는 이 게임에 존재하지 않는다(0/20 확인).

---

## 성전사 (`crusader`)

> **[선조]** 신성한 결의와 강인한 육체로 칼날을 휘두르도다, 그대 광신에 불타는 전사여!

**길드 — 전투 역할**
떡 벌어진 어깨와 수많은 전투로 단련된 성전사는 수백 번의 성전을 최전선에서 이끌어왔습니다. 성전사는 정당한 분노로 적들을 정면으로 맞서거나, 방어 강화 기술과 치료 기술로 가까운 동료들을 지원합니다.

**대장간 — 무기·방어**
성전사는 무거운 판금 갑옷을 입고 장검을 휘두릅니다. 하지만 그의 갑옷은 완벽한 방어와 피해량을 선사한 대가로 기동성을 상당히 앗아간 데다, 후열에서는 검을 제대로 휘두를 수도 없습니다.

**야영 — 전투 밖**
성전사는 모닥불 앞에 서서 정의와 신념으로 설득력 있는 연설을 토해냅니다! 또한 엄청난 스트레스에 직면하더라도, 일행을 이끄는 지도자로서 굳건히 버티며 휴식을 거부합니다. 그 흔들림 없는 믿음은 동료들의 공포를 완화하고, 그 어떤 고난이 있더라도 결국엔 모든 것이 잘 풀릴 것이라고 믿게 합니다.

**직업 치명타 버프** (2턴): 방어도 +15%

**전용 장신구 9개**

- **거룩한 사명** — resolve_check_percent +15% / stress_dmg_received_percent -20% / death_blow +12% / poison -20% / bleed -20%
- **지휘명령서** — stress_heal_received_percent +15% / hp_heal_percent +33% / damage_low -10% / damage_high -10%
- **마비사의 문장** — stun_chance +20% / defense_rating -2%
- **기사의 문장** — max_hp +10%
- **검사의 문장** — damage_low +10% [meleeonly] / damage_high +10% [meleeonly] / hp_heal_percent -50%
- **방어자의 봉인** — protection_rating +5% / crit_chance -3%
- **번쩍이는 어깨 갑옷** — protection_rating +15% / move +35% / stress_dmg_received_percent -15% / speed_rating -2
- **서명이 새겨진 징병서류** — hp_heal_percent +20% / stress_heal_percent +20%
- **비기하학적 칼자루** — max_hp +15% / random_target_attack_chance +5% / stun_chance +25% [has_item_id:holy_water]

---

## 노상강도 (`highwayman`)

> **[선조]** 약삭빠르고, 눈치 빠르며, 고집도 세구나. 악당으로선 만점이로다.

**길드 — 전투 역할**
노상강도는 그야말로 불한당이자 폭력배이고 도둑놈으로, 자신의 단검과 수발총을 끝내주게 잘 사용하여 엄청난 효과를 보여주기도 합니다. 원거리에서든 근거리에서든 상대를 똑같이 뭉개줄 수 있다는 말입니다. 그 기술들도 넓은 범위에 타격을 입히는 포도탄이나 단일 목표에게 출혈을 일으키는 등, 주로 상대에게 다양한 방식으로 피해를 주는 것에 집중되어 있습니다.

**대장간 — 무기·방어**
노상강도는 두껍게 덧댄 외투를 걸치고 있어 칼도 잘 박히지 않지만, 무딘 검을 받아내기보다는 회피하는 쪽을 더 선호합니다. 수발총과 단검이라는 무장은 어떤 상황도 대처할 수 있도록 해줍니다. 그 어떤 위치에서든 제 몫을 해내며, 기습을 당할 일도 없는 거죠.

**야영 — 전투 밖**
노상강도는 화톳불 주변에서도 최악의 상황을 준비하며 온갖 저속한 농담을 던집니다. 도주와 은신으로 점철된 삶을 보낸 덕택에, 노상강도는 삼엄한 경계나 야음을 틈탄 정찰 등의 중요성과 이점을 잘 알고 있습니다.

**직업 치명타 버프** (2턴): 속도 +2

**전용 장신구 9개**

- **총잡이의 버클** — damage_low +20% [rangedonly] / damage_high +20% [rangedonly] / attack_rating +15% [rangedonly] / damage_low -10% [meleeonly] / damage_high -10% [meleeonly] / crit_chance -5% [meleeonly]
- **예리함의 칼집** — crit_chance +7% [meleeonly] / bleed_chance +40% / speed_rating -1
- **회피의 칼집** — defense_rating +8% / speed_rating +1 / attack_rating -10% [rangedonly]
- **섬광의 화약** — damage_low +10% [rangedonly] / damage_high +10% [rangedonly] / stun -20%
- **방랑자의 허리띠** — trap +10% / defense_rating +4% / stress_heal_received_percent -5%
- **튼튼한 버클** — crit_chance +5% / stress_dmg_received_percent +5% / resolve_check_percent -3%
- **수치스러운 목걸이** — attack_rating +10% / crit_chance +5% / stress_dmg_received_percent +15%
- **피투성이 목두건** — speed_rating +2 / defense_rating +10%
- **수정 화약** — damage_low +20% / damage_high +20% / speed_rating +3 / stun -15%

---

## 성녀 (`vestal`)

> **[선조]** 저 신실함과 끝없는 저력을 보라, 실로 전투의 성녀로다!

**길드 — 전투 역할**
자신의 전의를 치유 능력과 성스러운 심판, 그리고 빛의 폭발로 승화하는 전사 수녀입니다. 그 어떤 조합의 일행을 짜든 가장 중추적인 역할을 맡는 성녀는, 이따금 자신의 강력한 철퇴를 들고 최전선에 나서 직접 심판을 내리기도 합니다.

**대장간 — 무기·방어**
성녀는 축성 판금 갑옷을 걸치고 끔찍한 폭력과 자애로운 치유를 동시에 가져다주는 이입니다. 한 손에는 철퇴, 다른 손에는 성서 - 극과 극을 동시에 공부해야 더 효과적이니 말입니다!

**야영 — 전투 밖**
성녀는 기도와 노래, 축복으로 일행에게 평화와 위안을 가져다줍니다. 또한 동료의 전투 능력을 높여주거나, 원정대의 스트레스 관리에 집중하고, 제대로 휴식을 취할 수 있게 야영지를 안전한 곳으로 만들어 줄 수 있습니다.

**직업 치명타 버프** (2턴): 회복량 +25%

**전용 장신구 9개**

- **신성한 두루마리** — stress_dmg_received_percent -10% / hp_heal_percent +33% / stun_chance -10% / damage_low -33% / damage_high -33%
- **불경한 두루마리** — damage_low +15% / damage_high +15% / protection_rating +10% [in_rank:1] / hp_heal_percent +33% [in_rank:1] / stress_dmg_received_percent +15%
- **성스러운 치유의 서** — hp_heal_percent +25% / max_hp -15%
- **신속의 성배** — speed_rating +8 [firstroundonly] / speed_rating +2 [firstroundonly] / stun_chance -25%
- **젊음의 성배** — max_hp +20% / damage_low -10% / damage_high -10%
- **고결한 성배** — resolve_check_percent +10% / max_hp -5%
- **속죄의 목걸이** — damage_low +15% [meleeonly] / damage_high +15% [meleeonly] / crit_chance +8% [meleeonly] / resolve_check_percent -15%
- **외설스러운 일기장** — stress_heal_percent +33% [in_camp] / hp_heal_percent +25%
- **이단의 길** — hp_heal_percent +20% [has_item_id:holy_water] / damage_low +25% [monsterType:husk] / damage_high +25% [monsterType:husk] / damage_low +25% [monsterType:eldritch] / damage_high +25% [monsterType:eldritch] / stress_dmg_received_percent +10%

---

## 역병 의사 (`plague_doctor`)

> **[선조]** 피바다로 물든 전장보다 좋은 실험실이 어디 있겠느냐?

**길드 — 전투 역할**
의사이자 연구자이며 연금술사로 후열에 있기를 선호하는 그녀는, 독 구름과 역병으로 채운 수류탄 같은 지속 피해를 입히는 기술로 적들을 갉아냅니다. 또한, 적들을 실명시키거나 혼란에 빠뜨리고, 아군의 피해량을 증강해주거나 출혈 및 중독 효과를 없애주는 등 조력자로서도 효과적입니다.

**대장간 — 무기·방어**
역병 의사는 가능한 한 근접 전투에서 회피하기 위하여 가벼운 복장만을 입습니다. 주로 먼 거리에서 상대를 실명이나 혼란에 빠뜨릴 수 있는 작은 독주머니를 던집니다.

**야영 — 전투 밖**
역병 의사는 온갖 실험적인 약물들과 위험한 치료법들을 동원하여, 동료들을 치료하고 또 활기를 불어넣어 줍니다. 자신이 최근 개발해낸 미실험 약물의 효능을 증명하고 싶어 안달이 나 있어서, 좋은 결과가 나올 것이란 확신을 품고 약물을 스스로에게도 거리낌 없이 투여하기도 합니다.

**직업 치명타 버프** (2턴): 중독 확률 +20

**전용 장신구 9개**

- **신성모독의 물약** — attack_rating +10% [rangedonly] / stun_chance +20% / poison_chance +20% / stress_dmg_received_percent +25%
- **마녀의 물약** — stun_chance +15%
- **시든 약초** — disease +40%
- **독초** — poison_chance +40% / max_hp -15%
- **저질 향로** — attack_rating +8% / max_hp -5%
- **핏빛 약초** — attack_rating +10% [meleeonly] / bleed_chance +30% / damage_low +20% [meleeonly] / damage_high +20% [meleeonly]
- **실험체 40번 기록서** — max_hp +25% / disease +35%
- **해부용 도구** — bleed_chance +35% / damage_low +25% / damage_high +25%
- **무색 정수** — defense_rating +20% / poison_chance +25% / hp_heal_received_percent +20% [has_item_id:medicinal_herbs]

---

## 현상금 사냥꾼 (`bounty_hunter`)

> **[선조]** 사냥의 쾌감과 짭짤한 돈벌이라.

**길드 — 전투 역할**
현상금 사냥꾼은 일대일 전투에 특화된 사형 집행인이자 군중 제어 전문가입니다. 현상금 사냥꾼에게 있어 책략은 곧 열쇠입니다. 공격 목표에 미리 표식을 새겨 추가적인 피해를 주거나, 기절시킨 적을 최우선으로 공격하는 식으로 말이지요. 또한, 갈고리와 섬광탄과 강력한 어퍼컷을 활용해 적 일행의 열과 오를 완전히 헤집어버릴 수도 있습니다.

**대장간 — 무기·방어**
현상금 사냥꾼은 자신의 한손 도끼와 갈고리를 자유자재로 휘두르며, 희생자들을 낚아채 솜씨 좋게 목숨을 끊어놓습니다. 걸치고 있는 질긴 가죽 미늘 갑옷은 가볍고 좋은 방어력을 가지고 있으며, 기동성을 깎지 않습니다.

**야영 — 전투 밖**
현상금 사냥꾼은 야영지에서도 전투태세를 갖추고 있습니다. 다른 동료들에게 전투의 흐름에 관해 지도하고, 직접 필기해둔 내용을 복습하며 앞으로 닥쳐올 '한탕'에 대비하여 승산을 최대한 높이려 합니다. 또한 정찰을 통해 현재 일행의 앞에 숨어있는 위협들을 분석하고, 이를 추적하여 일행의 기습 확률을 높여줍니다.

**직업 치명타 버프** (2턴): 표식 대상 피해 +33%

**전용 장신구 8개**

- **민첩의 갈퀴** — speed_rating +1 / defense_rating +4%
- **사냥꾼의 갈퀴** — crit_chance +6% / attack_rating +10% / food_consumption_percent +50%
- **야영의 투구** — stress_heal_received_percent +20% [in_camp] / scouting_chance +10%
- **부상의 투구** — damage_low +25% [meleeonly] / damage_high +25% [meleeonly] / move_chance -25% / stun_chance -20%
- **부동의 투구** — move +30% / move_chance +20%
- **범죄 거물의 어금니들** — damage_low +20% [actorStatus:tagged] / damage_high +20% [actorStatus:tagged] / damage_low +20% [actorStatus:stunned] / damage_high +20% [actorStatus:stunned] / damage_low +20% [actorStatus:bleeding] / damage_high +20% [actorStatus:bleeding] / defense_rating -10%
- **복수심 서린 살생부** — move_chance +50% / bleed_chance +35% / attack_rating +15% [rangedonly]
- **영원의 가면** — speed_rating +2 / defense_rating +15% / stress_dmg_received_percent +5%

---

## 야만인 (`hellion`)

> **[선조]** 야만의 분노와 무자비한 흉포함도 강력한 동맹이 될 수 있는 법.

**길드 — 전투 역할**
유혈을 흩뿌리며 전율을 느낀다니, 야만인은 거칠고 어디로 튈지 종잡을 수도 없는 데다 실로 무자비하기까지 한 인물입니다! 야만인의 거대한 글레이브는 전투에서 상당한 사거리를 자랑하며, 그 날카로운 칼날은 적들에게 깊은 상처를 남깁니다. 하지만 특정 전투 기술을 사용할 경우 완전히 탈진하고 말아, 적들에게 다시 달려들기 위해서는 몸에 아드레날린이 돌 때까지 기다려야 할 겁니다.

**대장간 — 무기·방어**
조잡한 가죽과 털은 미약한 방호를 제공하지만 야만인은 전투의 흔적을 자랑스럽게 생각합니다. 그녀에게는 거대한 글레이브로 혼란을 일으키고 상대방의 피로 몸을 적시는 것이 가장 중요합니다.

**야영 — 전투 밖**
야영지에 있을 때면 야만인은 온갖 신성모독을 중얼거리며 자신의 칼을 갈아댑니다. 그 칼날을 떨거지들의 몸에 박아줄 생각만 하면서 말이죠. 고요하게 전투를 준비하다가도 이단자의 광소를 터뜨리는 모습을 보고 있자면, 실로 길들여지지 않은 야수라 하겠습니다.

**직업 치명타 버프** (2턴): 출혈 대상 피해 +33%

**전용 장신구 8개**

- **지옥의 머리핀** — crit_chance +10% [lightbelow:25] / attack_rating +15% [lightbelow:25] / debuff -10% / bleed -10%
- **천국의 머리핀** — stress_dmg_received_percent -25% [lightabove:75] / attack_rating +10% [lightabove:75]
- **양날의 목걸이** — max_hp +15% / stun -20%
- **출혈의 펜던트** — bleed_chance +15%
- **이기심의 목걸이** — stress_dmg_received_percent -15%
- **암사자의 출진 물감** — damage_low +20% [hpbelow:0.75] / damage_high +20% [hpbelow:0.75] / damage_low +20% [hpbelow:0.5] / damage_high +20% [hpbelow:0.5] / damage_low +20% [hpbelow:0.25] / damage_high +20% [hpbelow:0.25] / stress_dmg_received_percent +10%
- **추방자의 낙인** — speed_rating +2 / bleed_chance +35% / death_blow +15% / hp_heal_received_percent -15%
- **목마른 칼날** — attack_rating +15% / bleed -20% / speed_rating +2 / crit_chance +8% [actorStatus:bleeding]

---

## 도굴꾼 (`grave_robber`)

> **[선조]** 저 날카로운 눈빛을 보라. 칼끝처럼 예리하게 보물의 낌새를 알아채겠구나.

**길드 — 전투 역할**
도굴꾼은 전열을 손쉽게 이동 가능한 다재다능하고 날렵한 전투원입니다. 주로 적들을 기습한 뒤 어둠 속으로 숨는 식의 일격이탈형 전투를 선호합니다. 비도와 독침이 빗나가더라도, 그 육중한 곡괭이를 휘두르며 근접전에 임할 수도 있습니다!

**대장간 — 무기·방어**
도굴꾼은 방어력보단 기동성과 민첩함을 선호하기에, 달랑 얇은 외투 한 장만 걸치고 다닙니다. 그 외투 밑에는 면도날처럼 날카로운 투척 단검을 품고 있고, 등에는 곡괭이 한 자루를 둘러메고 있습니다.

**야영 — 전투 밖**
도굴꾼은 가만히 못 있는 성격 탓에, 야영하는 중에도 이리저리 돌아다니면서 항상 장신구와 싸구려 보석을 찾아다닙니다. 영지를 등질 때면 사실 그 촌구석에서 뭘 좀 슬쩍했다며 마지못해 털어놓을 때도 있으며, 이따금 배배꼬였지만 날카로운 뼈가 있는 농담을 던져 동료들을 즐겁게 해주기도 합니다.

**직업 치명타 버프** (2턴): 회피 +10

**전용 장신구 8개**

- **약탈자의 부적** — crit_chance +5% / trap +30% / speed_rating +2 / scouting_chance +15% / max_hp -10%
- **행운의 부적** — defense_rating +12% / attack_rating +10% [rangedonly] / stress_dmg_received_percent +10%
- **중독의 가방** — poison_chance +25% / speed_rating +1 / defense_rating -4%
- **질병의 가방** — damage_low +20% [actorStatus:poisoned] / damage_high +20% [actorStatus:poisoned]
- **신속의 가방** — speed_rating +2
- **압생트** — disease +35% / poison +35% / poison_chance +35% / max_hp -10%
- **날카로운 편지 여는 칼** — damage_low +25% [meleeonly] / damage_high +25% [meleeonly] / attack_rating +10% [meleeonly] / defense_rating +5%
- **최고급 물약** — defense_rating +15% [has_item_id:medicinal_herbs] / speed_rating +3 / poison -20% / hp_dot_poison_duration_percent +50%

---

## 신비학자 (`occultist`)

> **[선조]** 심연과 싸우려는 자는 일단 심연을 알아야만 한다.

**길드 — 전투 역할**
신비학자는 평생을 걸쳐 고대의 금기와 전설들을 연구한 결과, 자신의 마음을 공허의 힘에 완전히 개방할 수 있게 되었습니다. 그의 전공은 적들의 몸을 쇠하게 하는 저주와, 불가능을 넘어 차라리 광기에 더 가까울 보조 기술들이라 하겠습니다. 하지만 공허는 어디까지나 예측할 수 없는 힘이기에, 신비학자가 사용하는 기술들의 효과는 극과 극을 달리며, 그 대가로 빛이나 시전자의 스트레스를 희생하게 됩니다.

**대장간 — 무기·방어**
신비학자가 걸치고 있는 학자의 가운만 보고 있자면, 이런 거친 모험보다는 차라리 도서관의 사서 쪽이 더 어울리지 않나 싶은 느낌이 듭니다. 그의 의식과 찬가는 손가락의 재빠른 움직임이 필요하기에, 그가 반질반질한 두개골을 만지고 있을 땐 방해하지 않는 편이 좋습니다.

**야영 — 전투 밖**
신비학자는 휴식을 취할 때에도 어둠과 공허의 부자연스러운 힘을 불러내어, 자신과 일행의 전투력을 강화하며 시간을 보내곤 합니다. 허나 그 힘의 대가는 어둠과 스트레스로 치러야 합니다.

**직업 치명타 버프** (2턴): 회복량 +25%

**전용 장신구 8개**

- **악마의 가마솥** — stun_chance +30% / debuff_chance +40% / crit_chance +3% / resolve_check_percent -10% / stress_dmg_received_percent +15%
- **희생의 가마솥** — damage_low +20% / damage_high +20% / stress_dmg_received_percent +10%
- **저주받은 향료** — debuff_chance +40% / move_chance +20% / max_hp -10%
- **회피의 향료** — defense_rating +8% / speed_rating -1
- **이물잡이의 향료** — crit_chance +6% [monsterType:eldritch] / damage_low +15% [monsterType:eldritch] / damage_high +15% [monsterType:eldritch]
- **모래가 담긴 약병** — stun_chance +20% / debuff_chance +20% / move_chance +20% / stun +20%
- **피의 계약물** — speed_rating +4 [lightbelow:60] / damage_low +25% [lightbelow:60] / damage_high +25% [lightbelow:60] / bleed_chance -25% / max_hp -10%
- **결정화된 두개골** — protection_rating +40% [attacking_monster_type:husk] / hp_heal_received_percent -20% / protection_rating +30% [attacking_monster_type:eldritch] / max_hp +15%

---

## 중보병 (`man_at_arms`)

> **[선조]** 젊은 혈기는 다 써버렸을지도 모르나, 이 노장의 눈에는 수많은 전장을 거치며 얻은 비밀들이 담겨 있다.

**길드 — 전투 역할**
숱한 전투를 겪어온 노병으로, 지금껏 겪은 투쟁을 통해 냉정한 판단력과 씻을 수 없는 죄책감을 모두 얻었습니다. 중보병은 집요하고 확고한 의지를 가진 지휘관으로써 철퇴, 버클러와 맹렬한 함성으로 적의 전열을 짓뭉갭니다.

**대장간 — 무기·방어**
중보병은 가장 두터운 갑주를 걸치고 철퇴를 휘두르며 뭐든지 으깨버립니다! 그는 순식간에 반응하고 적응하며, 깨지지 않는 방패로 동료들을 보호하며 돌격을 이끄는 데 가장 효과적입니다.

**야영 — 전투 밖**
중보병은 휴식 시간에도 스스로 엄격한 훈련을 하고, 이를 동료들에게도 시행하여 전의를 갈고 닦습니다. 이런 강인한 훈련을 이겨낸 자들은 응당 민첩성과 전투력, 명중률의 향상을 얻을 수 있습니다.

**직업 치명타 버프** (2턴): 받는 스트레스 −33%

**전용 장신구 8개**

- **수호자의 방패** — protection_rating +10% [in_rank:3] / hp_heal_received_percent +50% [in_rank:3] / defense_rating +10% [in_rank:3]
- **성벽 방패** — move_chance +40% / stun_chance +30% / damage_low -15% / damage_high -15%
- **오래된 안대** — max_hp +15% / speed_rating -2
- **비밀스러운 안대** — defense_rating +4% / stun -10% / move -10%
- **정화된 안대** — poison +30% / disease +20% / defense_rating -2%
- **낡은 군기** — stun_chance +15% / debuff_chance +20% / death_blow +15% / stress_dmg_received_percent +10%
- **장난감 병정** — protection_rating +10% / crit_chance +5%
- **거울 방패** — defense_rating +10% / reflected_dmg +30% / stun +20%

---

## 광대 (`jester`)

> **[선조]** 죽는 순간까지도 웃고만 있을 자로구나.

**길드 — 전투 역할**
전투는 힘 있는 발라드와도 같습니다. 잔잔하게 진행되다, 힘차게 종결되지요! 공격할 때, 광대는 피투성이 불협화음을 내며 앞뒤로 도약해, 영광스러운 끝을 맺기 위해 최전선에 섭니다! 아니면, 뒤에 남아서 서늘한 가락과 불안한 악절을 연주해 적들을 공포에 떨게 하고, 아군에게는 힘을 불어넣어 줄 수도 있습니다.

**대장간 — 무기·방어**
광대는 곰팡내 풍기는 옷만 걸친 채, 싸움 그 자체를 조롱합니다. 하지만 바보가 아니라면 광대가 휘두르는 예리한 낫질이나, 그 류트에서 흘러나올 불협화음을 얕보지는 않을 겁니다.

**야영 — 전투 밖**
광대의 진가는 깜빡이는 야영지 불꽃 옆에 앉아, 류트를 들고 재치있는 농담을 던져 동료들이 공포와 스트레스를 견딜 수 있게 해줍니다. 광대는 응원을 통해 전투력을 고양시켜주거나, 일행 중 한 명을 골라 신랄한 조롱을 선사해 일행의 사기를 되살리기도 합니다.

**직업 치명타 버프** (2턴): 스트레스 회복 +40%

**전용 장신구 8개**

- **어둠의 탬버린** — death_blow +12% / stress_dmg_received_percent -25% [lightbelow:26] / resolve_check_percent +10% [lightbelow:26]
- **빛의 탬버린** — stress_dmg_received_percent -25% [lightabove:75] / stress_dmg_received_percent +15% [lightbelow:51] / stress_heal_percent +20%
- **치명타의 주사위** — crit_chance +7%
- **행운의 주사위** — attack_rating +4% / defense_rating +4%
- **핏빛 주사위** — bleed_chance +30% / bleed -10%
- **폭군의 시음용 잔** — stress_heal_percent +33% / stress_dmg_received_percent +25%
- **폭군의 손가락뼈** — speed_rating +3 [in_rank] / defense_rating +20% [in_rank]
- **포식당한 자들을 위한 비가** — stress_heal_percent +25% / damage_low +25% [has_item_id:laudanum] / damage_high +25% [has_item_id:laudanum] / stress_dmg_received_percent +10%

---

## 석궁사수 (`arbalest`)

> **[선조]** 석궁과 붕대를 들고 적군을 약탈하구나, 그대 전장을 누비는 무용가여!

**길드 — 전투 역할**
탈영 군인인 석궁사수는 최고의 후열 전사라 할 수 있습니다. 적에게 제압사격을 퍼붓고, 두드러지는 대상을 저격하며 매우 효과적인 응급 치료를 할 수 있는 그녀는 결집소이자 포탑이며 어둠 속의 횃불입니다.

**대장간 — 무기·방어**
석궁사수의 이름은 전투에 매고 가는 거대한 석궁에서 따왔습니다. 그녀는 무수히 많은 화살을 쏟아내며 원거리에서 적들을 제거하고, 쏟아질 반격으로부터 몸을 더 잘 보호하기 위해 중갑을 입습니다…

**야영 — 전투 밖**
석궁사수는 전장에서나 야영지에서나 한결같이 행동합니다. 쉬는 시간을 쪼개 동료들에게 전문적인 응급처치를 제공하고, 다음 여정을 위해 최적의 행군 계획을 짜며 새 활시위를 꺼내 팽팽하게 걸어둡니다.

**직업 치명타 버프** (2턴): 표식 대상 피해 +33%

**전용 장신구 8개**

- **분노의 두건** — damage_low +25% [in_rank:3] / damage_high +25% [in_rank:3] / debuff_chance +30% / hp_heal_percent -50%
- **백발백중의 두건** — attack_rating +8% / crit_chance +5% / defense_rating -4%
- **간호병의 각반** — hp_heal_percent +33%
- **튼튼한 각반** — move +30% / move_chance +30% / speed_rating -1
- **복수의 각반** — crit_chance +3%
- **잠잘 때 듣는 이야기** — attack_rating +15% [actorStatus:tagged] / crit_chance +8% [actorStatus:tagged] / debuff_chance +35% / move_chance +35%
- **유년기의 보물** — hp_heal_percent +30% / hp_heal_percent +20% [in_camp] / stress_dmg_received_percent -15%
- **애가의 화살** — damage_low +20% / damage_high +20% / crit_chance +7% [rangedonly]

---

## 나병환자 (`leper`)

> **[선조]** 이 자는 삶과 죽음이 떼놓을 수 없는 관계임을 몸으로 체득하고 있구나.

**길드 — 전투 역할**
나병환자는 무너져가는 인간이고, 전사이자, 시인입니다. 일단 자신의 대검을 제대로 겨냥할 시간만 준다면 최고의 전투력을 보여줄 수 있습니다. 허나 검을 휘두르면, 그 효과는 모 아니면 도입니다 - 파괴적인 피해를 입히거나, 그냥 헛손질이 되는 것이죠. 고통으로 얼룩진 자신의 생명으로부터 힘을 뽑아내어 치료와 보호, 그리고 가차없는 분노로 치환하는 그의 모습은 가히 스스로 오롯한 인간이라 하겠습니다.

**대장간 — 무기·방어**
나병환자는 육중하고 갑갑한 청동 갑옷을 걸치고 있어 그 어떤 타격이든 받아낼 수 있습니다. 또한 그 자신이 들고 있는 대검은 매우 느리게 휘두를 수 밖에 없지만, 사정권 안에만 들어온 희생자는 그 막을 수 없는 힘에 파괴적인 피해를 입고 말 것입니다.

**야영 — 전투 밖**
나병환자는 사회로부터 추방당해 떠돌아다니는 몸으로, 일행 속에서도 겉도는 경향이 있습니다. 자신의 죽어가는 몸을 들켜봐야 돌아올 것은 공포 뿐이란 사실을 너무나 잘 알기 때문이죠. 문둥이는 가면을 벗는 것으로 스트레스를 줄일 수 있지만 그것도 주변에 동료들이 확실히 없을 때에나 가능합니다.

**직업 치명타 버프** (2턴): 명중 +10

**전용 장신구 8개**

- **광전사의 가면** — crit_chance +8% / speed_rating +3 / resolve_check_percent -10% / hp_heal_received_percent -33%
- **면역의 가면** — stun +40% / poison +30% / bleed +30% / max_hp -10%
- **행운의 팔찌** — attack_rating +8% / crit_chance +3% / stress_dmg_received_percent +10%
- **참회의 팔찌** — damage_low +15% [in_rank] / damage_high +15% [in_rank] / resolve_check_percent -3%
- **치유의 팔찌** — hp_heal_received_percent +20%
- **주석 플루트** — stress_dmg_received_percent -20% / stress_heal_percent +33% [in_camp]
- **마지막 유언장** — protection_rating +15% / max_hp +15% / death_blow -10%
- **결정화된 목걸이** — attack_rating +10% [has_item_id:bandage] / max_hp +15% / bleed -15%

---

## 조련사 (`houndmaster`)

> **[선조]** 정의의 집행자와 충성스러운 짐승이라. 저 둘은  전투와 전투를 넘어, 핏줄처럼 끈적하게 이어져 있다.

**길드 — 전투 역할**
조련사는 강인하며 드물게도 배려심 많던 법관이었습니다. 그는 충성스러운 늑대개와 힘을 합쳐 적을 쓰러트리고 무고한 자들을 지킵니다. 그들은 함께 후열에 접근해 괴롭히고, 깨물고, 후려치며 혼란을 일으킵니다. 전세가 기울 때면 이 둘은 약자를 보호하고 고통을 받은 자들을 부축하며 동료 일행을 지원할 수 있습니다.

**대장간 — 무기·방어**
조련사는 헌병 시절 입었던 낡은 제복을 아직도 걸치고 있으며, 공격을 받아내기보다는 아예 회피하는 쪽을 선호합니다. 그 손에 쥐어진 곤봉은 적을 효과적으로 기절시키지만, 진짜 치명타는 사냥개가 먹입니다. 특히 기운을 내는 간식을 먹인다면 더욱 날뛰지요!

**야영 — 전투 밖**
영리한 집행관은 탄탄한 대비와 정보의 중요성을 알고 있는 법입니다. 고로 조련사는 늑대개를 정찰에 내보내거나 밤에 경비로 세울 수 있습니다. 일행의 사기가 너무 낮다 해도 충성스러운 개와 정서적 교감을 나눈다면, 감정은 누그러지고 마음도 안정될 것입니다.

**직업 치명타 버프** (2턴): 출혈 확률 +20

**전용 장신구 8개**

- **징 박힌 목걸이** — damage_low +20% / damage_high +20% / bleed_chance +30% / hp_heal_received_percent -20% / hp_heal_percent -50%
- **보호의 목걸이** — defense_rating +12% / damage_low -15% / damage_high -15%
- **무거운 곤봉** — stun_chance +25% / speed_rating -1
- **민첩의 호각** — defense_rating +4% / speed_rating +1 / debuff -20%
- **정찰 호각** — scouting_chance +20% [lightbelow:51] / trap +20%
- **낡아빠진 보안관 배지** — attack_rating +15% [rangedonly] / stress_heal_percent +50% [in_camp] / hp_heal_percent +25% / stun -20% / debuff -20%
- **부패의 증거물** — scouting_chance +25% / party_surprise_chance -15% / stress_dmg_received_percent +10%
- **허물송곳니 호루라기** — bleed_chance +50% [has_item_id:dog_treats] / stress_heal_percent +40% [is_guarding] / defense_rating -10% / guard_duration_percent +66%

---

## 괴인 (`abomination`)

> **[선조]** 세상으로부터 소외된 채 오래도록 고통받은 자로다.  놈은 겉보기보다 훨씬 위험할 게다.

**길드 — 전투 역할**
괴인은 수십년간 갇힌 채 감히 입에 담을 수 없는 학대를 견디고 낙인까지 찍힌 자로, 스스로 사람들을 피해 살고 있습니다. 하지만 그 인두겁 밑에는 핏줄에 흐르는 맹독으로부터 얻는 기이한 힘이라는 끔찍한 비밀을 숨기고 있지요. 전투가 시작되면 괴인은 야수로 변신해, 무시무시한 야성을 표출해냅니다!

**대장간 — 무기·방어**
괴인은 저주받은 사슬과 두껍고도 질긴 가죽을 두르고 있어, 최전방 전투에서도 튼튼한 방어력을 자랑합니다. 괴물의 끔찍한 발톱은 하나하나가 단검만하고, 인두겁 밑에서 끊임없이 일어나는 변이는 이루 말할 수 없는 힘과 속도, 그리고 끔찍한 분비물을 만들어냅니다.

**야영 — 전투 밖**
괴인은 휴식하는 도중에도 자신의 괴이한 증상에 파묻혀 지냅니다. 스스로 맥박을 솟구치게 하여 전투에서의 공격성을 훨씬 증대시킬 수도 있고, 자신의 끔찍한 충동을 최대한 억눌러 원정대의 걱정을 덜어줄 수도 있습니다.

**직업 치명타 버프** (2턴): 피해 +20%

**전용 장신구 8개**

- **인내의 자물쇠** — resolve_check_percent +10%
- **전환의 자물쇠** — stun_chance +20% / poison_chance +20%
- **보호의 자물쇠** — protection_rating +15% / speed_rating -1
- **분노의 자물쇠** — damage_low +10% / damage_high +10% / speed_rating +3 / max_hp -10%
- **억제의 자물쇠** — stress_dmg_percent -40% [skill:transform] / mode -40%
- **수치스러운 외투** — stress_dmg_received_percent -15% / defense_rating +10%
- **오스먼드의 사슬** — damage_low +20% [rangedonly] / damage_high +20% [rangedonly] / crit_chance +8% [rangedonly]
- **부러진 열쇠** — attack_rating +15% / stun_chance +35% / stress_dmg_received_percent +10%

---

## 유물수집상 (`antiquarian`)

> **[선조]** 이 여성은 아무도 가지 않는 곳에서, 아무도 찾지 못한 물건을 찾는 눈을 가졌지.

**길드 — 전투 역할**
유물수집상은 학자이며 연구자이자, 날카로운 눈을 가진 고고학자입니다. 전투에는 소질이 없지만 호신술에는 도가 텄지요. 본인이 직접 싸우지는 않고 동료들에게 지켜달라고 하는 게 문제긴 하지만, 어쨌든 자신은 살아남으니 말입니다. 정 싸움을 피할 수 없다면, 유물수집상은 자신의 향로에서 연기를 뿜어, 동료들을 치유하고 그 감각을 고양시킵니다… 뭐 가끔은 적들을 중독시키기도 하고요.

**대장간 — 무기·방어**
유물수집상은 딱히 방어구를 걸치지 않습니다. 대신 그동안 수집한 수많은 유물과 부적들을 두르고 미신적인 마법에 기대죠. 또한 들고 있는 향로에서 뿜어져 나오는 증기로 감각을 고양시켜, 온갖 귀중한 유물을 찾아내기도 합니다. 조금… 난처한 상황에 빠졌을 때에도, 이 증기를 활용해 동료들의 전투를 도와줄 수 있지요.

**야영 — 전투 밖**
학문의 탐구에는 쉴 틈이 없습니다! 유물수집상은 야영지를 샅샅이 뒤져, 동료들이 미처 발견하지 못한 보급품이나 장신구를 발견해냅니다. 또한 기묘한 주문들과 마법 가루를 통해 동료들의 마음을 안정시키거나, 전투력을 고강하게 해주기도 하죠.

**직업 치명타 버프** (2턴): 회피 +10

**전용 장신구 8개**

- **구슬주머니** — defense_rating +10%
- **핏줄의 메달** — hp_heal_received_percent +33%
- **등딱지 우상** — protection_rating +25%
- **민첩의 주화** — speed_rating +4 / debuff_chance +20%
- **생명의 촛대** — hp_heal_percent +50% / max_hp +15%
- **셋 중의 둘** — damage_low +50% [actorStatus:poisoned] / damage_high +50% [actorStatus:poisoned] / crit_chance +8% [actorStatus:poisoned]
- **대가의 정수** — hp_heal_percent +50% / poison_chance +35% / debuff_chance +35%
- **연기 나는 해골** — defense_rating +35% [has_item_id:spice] / attack_rating -15% / attack_rating -15%

---

## 총사 (`musketeer`)

> **[선조]** 사격의 달인이로구나. 새로운 도전을 찾아온 것일까.

**길드 — 전투 역할**
총사는 사격 대회에는 많이 나가봤으나 실전 경험은 별로 없는 인물이라, 적들과 거리를 좀 두는 쪽을 선호합니다. 하지만 그 날카로운 눈에는 빈틈이 없고 화승총을 장전하는 손은 신속하여, 믿음직한 원거리 공격수로 활약하지요. 또한 연막탄과 응급처치, 스키트 사격 등의 기술을 통해 지원 역할도 맡을 수 있습니다.

**대장간 — 무기·방어**
총사가 입고 있는 예복은 겉보기와 달리 무두질한 가죽으로 덧대어져 있어 매우 튼튼하기 때문에, 착용자로 하여금 사격에만 전념할 수 있게 해줍니다. 또한 각종 특수탄을 발사하는 화승총과 든든한 권총이 함께라면, 원거리에서도 상당한 피해를 입힐 수 있습니다.

**야영 — 전투 밖**
총사는 자신의 무기가 매우 예민한 장비이므로, 전투가 끝나면 정비를 적절히 해주어야 한단 점을 잘 알고 있습니다. 또한 응급처치를 통해 동료들의 상태도 적절하게 정비하는 데에도 도가 텄지요. 어쨌든 적들이 가까이 오지 못하게 할 장애물은 필요하잖습니까.

**직업 치명타 버프** (2턴): 표식 대상 피해 +33%

**전용 장신구 8개**

- **분노의 모자** — damage_low +25% [in_rank:3] / damage_high +25% [in_rank:3] / debuff_chance +30% / hp_heal_percent -50%
- **명중의 모자** — attack_rating +8% / crit_chance +5% / defense_rating -4%
- **위생병의 장화** — hp_heal_percent +33%
- **튼튼한 장화** — move +30% / move_chance +30% / speed_rating -1
- **복수의 장화** — crit_chance +3%
- **은 화승총 탄환** — attack_rating +15% [actorStatus:tagged] / crit_chance +8% [actorStatus:tagged] / debuff_chance +35% / move_chance +35%
- **준우승 트로피** — hp_heal_percent +30% / hp_heal_percent +20% [in_camp] / stress_dmg_received_percent -15%
- **이십면체 머스킷 총알** — damage_low +20% / damage_high +20% / random_target_attack_chance +20%

---

## 방패 파괴자 (`shieldbreaker`)

**길드 — 전투 역할**
방패 파괴자는 우아함과 격노가 뒤섞인 모래폭풍 같은 기세로 전열을 넘나들며 강력한 힘으로 정밀하게 공격을 꽂아 넣습니다. 적의 갑옷을 찢고, 전열을 무너뜨리며, 가는 자리마다 독을 남기니, 그녀는 실로 무자비한 전투원이라 할 수 있습니다.

**대장간 — 무기·방어**
방패 파괴자는 창 한 자루와 방패를 사용하며, 인상적인 사정거리와 약간의 방어 능력을 발휘합니다. 하지만 걸치고 있는 의복은 던전보다 무대에 더 어울리는 것이라, 살아남기 위해서는 발 빠르게 움직여야 합니다.

**야영 — 전투 밖**
방패 파괴자는 모닥불이 피어오르는 앞에서 침묵을 지키고 앉아있지만, 그 내면에서는 과거의 악몽에 시달리고 있습니다. 이런 악몽은 꿈속에서 매우 강력한 환상으로 출몰하며, 이를 이겨내지 못하면 잠에서 깨어난 후에도 여전히 느리고 피곤하며 스트레스를 받은 상태일 것입니다.

**직업 치명타 버프** (2턴): 방어도 +15%

**전용 장신구 8개**

- **맹독을 담은 병** — poison_chance +30% / poison -10%
- **빛나는 비늘** — protection_rating +10% / stress_dmg_received_percent +5%
- **무희의 발싸개** — move +40% / speed_rating +2
- **송곳니 창끝** — damage_low +35% [actorStatus:tagged] / damage_high +35% [actorStatus:tagged] / damage_low -10% / damage_high -10%
- **퀴어부이** — max_hp +33% / speed_rating -2
- **흑요석 단검** — debuff_chance +40% / poison_chance +40%
- **잘린 손** — poison +50% / stress_dmg_received_percent -10%
- **공허한 창끝** — damage_low +15% / random_target_attack_chance +5% / poison_chance +20% / max_hp +15% / damage_high +15%

---

## 고행자 (`flagellant`)

**길드 — 전투 역할**
고행자는 교회 내의 급진파에 속해 있으며, 사람들은 그를 공포, 경외, 그리고 혐오가 뒤섞인 눈길로 바라보곤 합니다. 고행자가 스스로를 혹사함으로써 얻는 힘은 효과적인 만큼 보는 이들을 불안에 떨게 합니다. 한순간 치유의 힘이 샘솟는 존재였다가도, 어느샌가 끔찍한 공포를 내뿜는 자로 돌변하기 때문입니다. 그의 진가는 광기 또는 죽음 직전의 순간에서야 나타납니다.

**대장간 — 무기·방어**
고행자는 자신의 몸을 뒤덮은 흉터와 상처들로부터 기쁨을 얻으며, 불가해하게도 자신의 살점을 스스로 찢음으로써 더욱 견고해집니다. 잔인하고 자비 없는 그의 도리깨는 적들과 자신의 피로 물들어 있습니다.

**야영 — 전투 밖**
고행자는 다른 이들과 함께 행동하는 것을 꺼리며, 야영 시 화톳불로부터 돌아앉습니다. 불의 온기를 느끼며 편히 쉬는 대신, 고행자는 스스로를 무자비하게 채찍질합니다. 그는 자신의 육체와 피를 대상으로 끝나지 않는 전투를 하고 있습니다.

**직업 치명타 버프** (2턴): 출혈 확률 +20

**전용 장신구 8개**

- **부러진 이빨** — max_hp +20% / move +35%
- **유리 조각** — bleed_chance +35% / bleed -20%
- **영겁의 목걸이** — death_blow +10% / defense_rating +20% [at_deaths_door] / damage_low +20% [stress_above:85] / damage_high +20% [stress_above:85]
- **고통의 목걸이** — bleed +20% [hpbelow:0.4] / poison +20% [hpbelow:0.4] / max_hp +10%
- **형벌의 두건** — bleed_chance +20% / damage_low +15% [hpbelow:0.4] / damage_high +15% [hpbelow:0.4] / hp_heal_percent -20%
- **부활의 목걸이** — hp_heal_percent +33% / bleed_chance -15%
- **심장파열의 두건** — speed_rating +4 [hpbelow:0.4]
- **산성 허물 정수** — max_hp -25% / damage_low +30% / damage_high +30% / bleed_chance +30% [monsterType:husk] / hp_heal_received_percent +25% [hpbelow:0.2]

---

## 결투가 (`duelist`)

> **[선조]** 세검의 칼날을 따라 완벽이 번뜩이누나.

**길드 — 전투 역할**
검술의 달인 결투가는 치명적인 기량을 바탕으로 다양한 태세를 자유자재로 오가며 싸웁니다. 방어 자세는 적의 모든 공격을 기회로 전환하는 반면, 공격 태세는 파괴적인 연타를 퍼붓는 식입니다. 그래서 적절한 타이밍과 적의 행동을 예측하는 것을 가장 강력한 무기로 써먹습니다.

**대장간 — 무기·방어**
결투가는 우아하면서도 무자비한 무기, 가느다란 레이피어를 휘두릅니다. 펜싱 복장의 방호력 자체는 별로지만, 자신의 전투 스타일에 필수적인 자유로운 동작을 보장해 줍니다.

**야영 — 전투 밖**
결투가는 휴식 시간에도 침묵 속에서 칼날을 갈고 동작을 연습합니다. 또한 틈날 때마다 엄격하고 흔들림 없는 규율을 발휘해 동료들을 혹독하게 훈련시킵니다.

**직업 치명타 버프** (2턴): on_crit_duelist_def

**전용 장신구 8개**

- **철테 두른 장화** — stun_chance +10% / crit_chance +4% [in_mode:stance_aggressive]
  > 쇠테를 두른 결투용 장화. 턱을 박살내기 충분할 정도로 무겁다.
- **동백 기름** — crit_chance +4% [meleeonly]
  > 살육의 칼날을 날카롭게 연마하는 고급 기름.
- **금박 망토** — crit_received_chance -6% / crit_received_chance -6% [is_actor_status:tagged] / defense_rating +10% [is_actor_status:tagged]
  > 결투 대회 챔피언이 걸치는 화려한 망토.
- **면도날 힐트** — ignore_protection +1 [actorStatus:bleeding] / bleed -20%
  > 아름다운 꽃에는 치명적인 가시가 있는 법.
- **챔피언의 망토** — damage_low +20% [in_rank:1] / damage_high +20% [in_rank:1] / damage_low +20% [in_rank:3] / damage_high +20% [in_rank:3] / defense_rating -10% [in_rank] / defense_rating -10% [in_rank:2]
  > 결투 대회 우승자에게 주어지는 하나뿐인 망토.
- **아카데미 반지** — debuff_chance +35% / crit_chance +8% [riposte]
  > 결투 학교의 인장 반지.
- **연인의 장갑** — attack_rating +10% [in_mode:stance_aggressive]
  > 한 숙녀의 장갑. 잃어버린 사랑의 증표다.
- **망령의 재치** — damage_low +50% [hpabove:0.99] / damage_high +50% [hpabove:0.99] / bleed +25% / poison +25% / max_hp -33%
  > 섬뜩한 독기가 풍기는 수정.

---

## 도망자 (`runaway`)

> **[선조]** 불타는 생존 의지 말고는 아무것도 남지 않았네.

**길드 — 전투 역할**
외로운 떠돌이, 도망자는 불을 무기와 방패 모두로 활용합니다. 도망자는 깊이, 또 널리 화상을 퍼뜨려 자신에게 해를 끼치려는 자들을 구워 버립니다. 또한 민첩하고 기지가 뛰어나서 온 전장을 불길로 뒤덮은 뒤, 자기는 그림자 속으로 슬그머니 사라지곤 합니다.

**대장간 — 무기·방어**
도망자는 급조한 발화 도구와 재치로 싸웁니다. 복장도 가볍고 실용적이라, 흔적을 남기지 않고 재빨리 움직여야 하는 이들에게 잘 어울립니다.

**야영 — 전투 밖**
도망자는 모닥불 곁에서 제 본색을 드러냅니다. 노련한 솜씨로 불을 지피고, 흔들림 없는 손길로 상처를 지져 치료하며, 방심한 이들에게서 귀중품을 훔쳐내는 데 일가견을 보여줍니다.

**직업 치명타 버프** (2턴): 속도 +2

**전용 장신구 11개**

- **온기의 스카프** — defense_rating +10%
- **가연성 액체** — 
  > 접촉 즉시 불이 붙는 휘발성 혼합물.
- **숯덩이 인형** — 
  > 반쯤 타버린 나무 인형. 투박하게 생겼지만 마음을 편안하게 해 준다.
- **구출자의 륙색** — max_hp +20% / crit_chance -10% / hp_heal_dot_duration_received_percent -50%
  > 낡고 닳은 가방. 연고와 붕대로 가득 차 있다.
- **지옥불 석탄** — speed_rating +3 [any_is_burning] / wildfire_apply_adjacent_targets +0%
  > 불타는 듯한 나선형 무늬가 새겨진 석탄.
- **깎아 만든 장난감** — attack_rating +15% [rangedonly] / crit_chance +12% [target_is_burning] / stun -15% / bleed -15%
  > 불 붙은 채 앞발을 치켜든 나무 말.
- **뜨개질 담요** — protection_rating +33% / hp_heal_received_percent +33% [is_stealthed]
  > 재로 변해버린 편안함.
- **꺼져버린 태양돌** — speed_rating -2
  > 위험이 다가오면 희미하게 웅웅거리는, 무딘 느낌의 차가운 돌.
- **달궈진 태양돌** — speed_rating +1
  > 안에서 빛이 나고, 만지면 따뜻하다.
- **이글거리는 태양돌** — speed_rating +2 / hp_dot_burn_amount_percent +33%
  > 표면 아래에서 거세게 소용돌이치는 불씨.
- **불타는 태양돌** — speed_rating +4 / hp_dot_burn_amount_percent +50%
  > 태양의 축소판. 쥐고 있기에는 위험하지만 버리는 것도 불가능하다.

---

