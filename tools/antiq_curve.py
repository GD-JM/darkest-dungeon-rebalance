"""P-25 (2026-10-27) 유물수집상 레벨 곡선 계산: 모든 영웅을 기술 1~5렙(장비 같은 단계)으로 평가하고,
유물수집상에게만 전용 장신구 조합을 적용해 비교한다. strength.py는 고치지 않고 함수만 바꿔 끼운다.
- 비교 기준(제작자 10-27): 다른 영웅은 장신구 없이. 5렙(=챔피언, 의지 5에서만 열림)에서 장신구 낀 유물수집상이 비등,
  1~4렙(베테랑까지)은 낮게.
- 장신구 근사: 회복 % -> 기술 회복량 배율, 중독·약화 확률 -> 유물수집상 효과의 .chance 가산,
  중독 대상 피해·치명(셋 중의 둘) -> 무기 피해·치명 x 자기 상태 유지율(COND_SELF 0.6), 능력치 -> 영웅 수치.
사용: python tools/antiq_curve.py [--variant 파일.json]   (variant = 유물수집상 기술/효과 시안)"""
import os, re, sys, json, argparse, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
import strength as S

# 전용 장신구 (데이터: trinkets/base.entries + crimson_court.entries/sets)
TRINKETS = {
    'beads': dict(def_=10),                                    # 구슬주머니
    'medal': dict(heal_recv=0.33),                             # 핏줄의 메달 (자기 받는 회복, 모델 생존에 미반영)
    'idol': dict(prot=0.25),                                   # 등딱지 우상
    'coin': dict(spd=4, debuff=20),                            # 민첩의 주화
    'candle': dict(heal=0.5, hp_mult=0.15),                    # 생명의 촛대
    'two_of_three': dict(dmg_poisoned=0.5, crit_poisoned=8),   # 셋 중의 둘
    'essence': dict(heal=0.5, poison=35, debuff=35),           # 대가의 정수
}
SETS = {('two_of_three', 'essence'): dict(spd=4, def_=10)}     # cc_anti 세트
LOADOUTS = {'없음': (), '피의 궁정 세트': ('two_of_three', 'essence'), '촛대+정수': ('candle', 'essence'),
            '주화+정수': ('coin', 'essence')}

LEVEL = 4
LOAD = ()
VARIANT = {}      # {'info': 기술 줄 텍스트 치환 [(old, new)], 'effects': {이름: 줄}}


def mods():
    m = {}
    for t in LOAD:
        for k, v in TRINKETS[t].items():
            m[k] = m.get(k, 0) + v
    for combo, bonus in SETS.items():
        if all(c in LOAD for c in combo):
            for k, v in bonus.items():
                m[k] = m.get(k, 0) + v
    return m


def antiq_text(mode):
    t = open(S.hero_file('antiquarian', mode), encoding='utf-8', errors='ignore').read()
    if mode == 'rb':
        for old, new in VARIANT.get('info', []):
            t = t.replace(old, new)
        h = mods().get('heal', 0)
        if h:
            t = re.sub(r'(combat_skill:[^\n]*?\.heal )(\d+(?:\.\d+)?) (\d+(?:\.\d+)?)',
                       lambda m: f'{m.group(1)}{float(m.group(2)) * (1 + h):g} {float(m.group(3)) * (1 + h):g}', t)
    return t


def load_hero(hero, mode, level=None):
    if hero == 'antiquarian':
        H = S.parse_hero(hero, antiq_text(mode), LEVEL)
        if mode == 'rb':
            m = mods()
            H['spd'] += m.get('spd', 0)
            H['def'] += m.get('def_', 0)
            H['hp'] *= 1 + m.get('hp_mult', 0)
            u = S.PARAM['COND_SELF']
            H['dmg'] = tuple(x * (1 + m.get('dmg_poisoned', 0) * u) for x in H['dmg'])
            H['wcrit'] += m.get('crit_poisoned', 0) * u
        return H
    t = open(S.hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
    return S.parse_hero(hero, t, LEVEL)


_orig_effects = S.load_effects


def load_effects(mode):
    E = dict(_orig_effects(mode))
    if mode != 'rb':
        return E
    E.update(VARIANT.get('effects', {}))
    m = mods()
    names = {n for l, d in S.parse_hero('antiquarian', antiq_text('rb'), LEVEL)['skills'] for n in S.ec.effect_names_in(l)}
    for n in names:
        line = E.get(n, '')
        add = 0
        if '.dotPoison' in line:
            add += m.get('poison', 0)
        elif '"negative"' in line and '.target "target"' in line:
            add += m.get('debuff', 0)
        if add:
            E[n] = re.sub(r'\.chance\s+(\d+)%', lambda x: f'.chance {int(x.group(1)) + add}%', line, count=1)
    return E


S.load_hero = load_hero
S.load_effects = load_effects


# ---- 모델 확장 (2026-10-27, 제작자 "모델 개선해"). strength.py에 R-HP-028 미커밋 작업이 있어 섞지 않고 여기서 덧씌운다.
# 1) 아군 받는 치명 감소(buff_type crit_received_chance 음수, 아군 대상): R-VALUE-22 enemy_crit_value 재사용.
#    파티 전체가 받으므로 살아 있는 적 평균 2명(R-STRAT-02)의 모든 공격 치명이 -x, 지속은 buff_rounds 가중.
# 2) 스택 힐(받는 회복 증가, 지속 없음 = 전투 끝까지 쌓임): 같은 대상에게 앞서 건 횟수 STACK_PRIOR(가정 0.5회)만큼
#    이번 회복이 커진다 -> 회복 가치 x 수치 x STACK_PRIOR 를 더한다(다른 회복의 증폭은 기존 계산에 이미 있음).
# 3) 아군에게 거는 반격(유물 날 지켜줘): 기존 계산은 시전자(유물)의 무기·회피·반격 기술로 셌다.
#    -> 반격하는 아군 = 표준 아군 공격 ALLY_ATK x 반격 기술 피해(새 반격 기술 -50%) x (1+효과 보너스),
#       받는 공격 = 중앙 회피 영웅 기준, 대상에게 표식이 같이 걸리면 표식 지속 동안 MARK_DRAW.
STACK_PRIOR = 1.0   # 가정: 3턴 지속 안에 같은 대상에게 매 턴 쓰면 앞선 스택 0,1,2개 -> 평균 1개
DODGE_STACK = 20   # 가정: 회피 조합에서 대상이 이미 가진 다른 회피 강화(움츠리기·결투가·조련사·장신구 등) 합
OWN_RIPOSTE = {'highwayman': -0.15, 'man_at_arms': -0.20, 'duelist': 0.0}   # 반격 기술 피해(노상·중보는 자기 5렙 반격 값으로 고정)
RIPOSTE_BONUS = [0.10, 0.11, 0.12, 0.14, 0.15]   # 유물 반격 전용 피해 강화(2턴), 레벨별
ALLY_RIPOSTE_DMG = -0.5   # 반격 기술이 없던 16명에게 넣는 새 반격 기술의 피해 보정(빌린 반격)
_sv0 = S.skill_value
_wcache = {}


def ally_riposte_damage(mod, P):
    """반격 1회 기대 피해 (2026-10-28 개정). 지켜 주는 아군은 누구든 될 수 있어 이 레벨 각 영웅의 실제 무기로 계산해 평균.
    피해 = 영웅 반격 기술 피해(자기 반격이 있는 노상강도·중보병·결투가 0%, 나머지 ALLY_RIPOSTE_DMG)
           x (1 + 유물 반격 상태 보정 mod + 유물 반격 전용 강화 RIPOSTE_BONUS[레벨])  (강화끼리 가산, V-01)
    반격 상태는 덮어쓰기라 노상강도·중보병 자기 보정은 유물 보정으로 바뀐다(같은 레벨이면 노상강도 곡선과 같음)."""
    key = (LEVEL, round(mod, 3))
    if key not in _wcache:
        vals = []
        for h in S.KO:
            if h == 'antiquarian':
                continue
            H = S.parse_hero(h, open(S.hero_file(h, 'rb'), encoding='utf-8', errors='ignore').read(), LEVEL)
            sk = OWN_RIPOSTE.get(h, ALLY_RIPOSTE_DMG)
            atk = 100 if h == 'duelist' else 85 if h != 'man_at_arms' else 90
            vals.append(st.mean(S.hit(m, atk) * S.damage_mean(H['dmg'], sk * 100, H['wcrit'] / 100, m['prot'],
                                                              mod + RIPOSTE_BONUS[LEVEL], P.get('DMG_STACK', 'mult')) for m in S.MONS))
        _wcache[key] = st.mean(vals)
    return _wcache[key]


def ally_weapon_scale():
    """ALLY_ATK(7.17)는 5렙 기준 상수 -> 현재 레벨의 영웅 무기 평균 피해 중앙값 / 5렙 중앙값으로 줄인다."""
    if LEVEL not in _wcache:
        def med(lv):
            return st.median(sum(S.parse_hero(h, open(S.hero_file(h, 'rb'), encoding='utf-8', errors='ignore').read(), lv)['dmg']) / 2 for h in S.KO)
        _wcache[LEVEL] = med(LEVEL) / med(4)
    return _wcache[LEVEL]


def skill_value(C, l, d):
    v, parts = _sv0(C, l, d)
    parts = dict(parts)
    P = C.P
    tg = S.first(d, 'target')
    effs = [C.eff.get(n, '') for n in S.ec.effect_names_in(l)]
    for e in effs:
        k = S.kv(e)
        if S.first(k, 'target') != 'target' or '@' not in tg:
            continue
        if S.first(k, 'buff_type') == 'crit_received_chance' and S.num(S.first(k, 'buff_amount')) < 0:
            x = -S.num(S.first(k, 'buff_amount'))
            extra = S.enemy_crit_value(x, P) * 2 * S.buff_rounds(S.effect_duration(k, P), P)
            v += extra; parts['받는 치명 감소'] = parts.get('받는 치명 감소', 0) + extra
        if S.first(k, 'buff_type') == 'hp_heal_received_percent' and parts.get('회복', 0) > 0:
            # 스택 힐(지속 3턴, 쓸 때마다 중첩 40->80->120%): 기존 계산은 다른 회복 증폭만 센다.
            # 같은 대상에게 3턴 안에 매 턴 쓰면 앞선 스택이 평균 STACK_PRIOR개 -> 이번 자기 회복도 그만큼 커진다.
            amt = S.num(S.first(k, 'buff_amount')) / 100
            own = parts['회복'] * amt * STACK_PRIOR
            v += own; parts['스택 중첩'] = own
        if 'combat_stat_buff' in k and S.num(S.first(k, 'defense_rating_add', '0')) > 0:
            # 회피는 스트레스 공격도 막고, 다른 회피 강화와 겹칠수록 남은 피격 대비 효과가 커진다(EHP).
            # 기본 모델은 중앙 회피(25)에서 선형 -> 회피 조합 기준(중앙 + DODGE_STACK)에서 EHP 가중으로 다시 센다.
            x = S.num(S.first(k, 'defense_rating_add'))
            dd = S.buff_rounds(S.effect_duration(k, P), P)
            n = 4 if '~' in tg else 1
            lin = S.dodge_value(S.HERO_MED_DEF, x, dd, P)
            ehp = S.dodge_value(S.HERO_MED_DEF + DODGE_STACK, x, dd, dict(P, DODGE_EHP=True))
            extra = (ehp - lin) * n * P['SUPPORT_MULT']
            v += extra; parts['회피 겹침'] = extra
        if 'riposte' in k:
            old = parts.get('반격', 0)
            rd = min(S.effect_duration(k, P), P['BUFF_DUR_CAP'])
            md = 0
            for e2 in effs:
                k2 = S.kv(e2)
                if S.first(k2, 'target') == 'target' and 'tag' in k2:
                    md = min(S.effect_duration(k2, P), rd)
            hits = P['HITS_TAKEN'] * (md * P['MARK_DRAW'] + (rd - md)) / max(0.05, S.hit_probability(P['MON_HIT'], S.HERO_MED_DEF))
            mod = S.num(S.first(k, 'damage_low_multiply', '0')) / 100
            new = ally_riposte_damage(mod, P) * hits
            v += new - old; parts['반격'] = new
    return v, parts


S.skill_value = skill_value


# ---- EHP 확장 (2026-10-28, 제작자 "EHP 적용할 곳 찾아서 넣어")
# 회피(DODGE_EHP)와 같은 원리: 줄이는 비율이 클수록 남은 피해 대비 효과가 커진다.
# 1) 방어 강화: 받는 피해 비율 (1-방어). 선형 값 x (1-기준 방어)/(1-기준 방어-x). 기준 = 자기 방어(자신) / 0(아군).
# 2) 받는 스트레스 감소: 선형 값 x 1/(1-감소율).
# 제외(이유): 적 명중·피해 약화는 적 1명에게만 걸려 파티 전체 피격·피해 비율이 거의 안 변한다(strength.py enemy_acc_value 설명과 같은 판단).
_stat0 = S.Ctx.stat_value
_stress0 = S.Ctx.stress_resist_value


def _stat_value(self, stat, amt, dur, who):
    v = _stat0(self, stat, amt, dur, who)
    if stat == 'protection_rating' and amt > 0:
        base = self.H.get('prot', 0) if who == 'self' else 0.0
        v *= (1 - base) / max(0.05, 1 - base - amt)
    return v


def _stress_value(self, amt, dur, who='ally'):
    v = _stress0(self, amt, dur, who)
    if amt < 0:
        v *= 1 / max(0.05, 1 + amt)
    return v


S.Ctx.stat_value = _stat_value
S.Ctx.stress_resist_value = _stress_value


# ---- 죽음의 일격 저항 (2026-10-28, 기존 모델은 0으로 계산)
# 가치 = 죽음의 문턱에 있을 라운드 확률(DD_RISK, 가정) x 그 라운드에 받는 공격 수(자기 표식이면 MARK_DRAW배)
#       x 전투 라운드 x 저항 증가 x 영웅을 잃는 값(최대 체력 x DEATH_MULT, 가정: 영웅 1명 = 파티 전력 1/4의 영구 손실).
DD_RISK = 0.05
DEATH_MULT = 3.0
_sv1 = S.skill_value


def _sv_deathblow(C, l, d):
    v, parts = _sv1(C, l, d)
    P = C.P
    effs = [S.kv(C.eff.get(n, '')) for n in S.ec.effect_names_in(l)]
    marked = any(S.first(k, 'target') == 'performer' and 'tag' in k for k in effs)
    for k in effs:
        if S.first(k, 'target') != 'performer':
            continue
        for b in k.get('buff_ids', []):
            B = C.buffs.get(b.strip('"'), {})
            if B.get('stat_type') == 'resistance' and B.get('stat_sub_type') == 'death_blow' and B.get('amount', 0) > 0:
                hits = P['HITS_TAKEN'] * (P['MARK_DRAW'] if marked else 1)
                extra = DD_RISK * hits * P['FIGHT_ACTS'] * B['amount'] * DEATH_MULT * C.H['hp']
                v += extra; parts = dict(parts); parts['죽음의 일격 저항'] = parts.get('죽음의 일격 저항', 0) + extra
    return v, parts


S.skill_value = _sv_deathblow


def evaluate_level(level, loadout):
    global LEVEL, LOAD
    LEVEL, LOAD = level, loadout
    S.hero_file.cache_clear() if hasattr(S.hero_file, 'cache_clear') else None
    res = {m: S.evaluate(m) for m in ('vanilla', 'rb')}
    S.score(res, '기본')
    return res


def table(variant=None):
    global VARIANT
    VARIANT = variant or {}
    out = {}
    for lv in range(5):
        # 다른 영웅(장신구 없음)은 조합과 무관하므로 '없음'에서 한 번 계산
        base = evaluate_level(lv, ())
        others = [base['rb'][h] for h in S.KO if h != 'antiquarian']
        row = dict(level=lv + 1, med_score=st.median(r['score']['기본'] for r in others), med_act=st.median(r['act'] for r in others))
        for name, lo in LOADOUTS.items():
            res = base if not lo else evaluate_level(lv, lo)
            a = res['rb']['antiquarian']
            # 점수 눈금은 행 전체 정규화라 조합마다 미세하게 달라진다 -> 다른 영웅 대비 순위·act 차이로 본다
            oth = sorted([res['rb'][h]['score']['기본'] for h in S.KO if h != 'antiquarian'], reverse=True)
            rank = 1 + sum(1 for x in oth if x > a['score']['기본'])
            row[name] = dict(score=round(a['score']['기본'], 1), act=round(a['act'], 2), rank=rank,
                             skills={s: round(v[0], 2) for s, v in a['skills'].items()})
        out[lv + 1] = row
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant')
    a = ap.parse_args()
    var = json.load(open(a.variant, encoding='utf-8')) if a.variant else None
    T = table(var)
    print(json.dumps(T, ensure_ascii=False, indent=1))
