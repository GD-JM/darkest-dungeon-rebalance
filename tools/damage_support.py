"""R-AUDIT-25: same-target offensive debuffs, measured in expected HP loss.

Engine primitives are injected from strength.py. This is a counterfactual model,
not a recovered full engine or fitted empirical regression. Separate effect rolls
are assumed independent conditional on the opening hit/crit and marked state.
"""
import functools
import itertools
import math
import statistics as st
import glob
import os
import re

OFFENSIVE = {'defense_rating', 'protection_rating', 'crit_received', 'dmg_received'}


def clamp(x):
    return max(0., min(1., x))


def ehp(hp, prot):
    """Continuous diagnostic only; never added to damage gain. No rounding here."""
    return hp / (1 - prot) if prot < 1 else math.inf


@functools.lru_cache(maxsize=None)
def destealth_coverage(S, ranks):
    """Fraction of stealth encounters with a reachable initially stealthed unit.

    Uses the existing model's base-dungeon mash weights; not a campaign encounter
    frequency estimate. Missing monster definitions are excluded, never guessed.
    Absolute DESTEALTH HP price remains a separate, visible prior.
    """
    _, _, info = S._monster_db()
    stealth = {}
    total = reachable = 0.
    count = eligible = 0
    for file in sorted(glob.glob(os.path.join(S.G, 'dungeons', '*', '*.5.mash.darkest'))):
        with open(file, encoding='utf-8', errors='ignore') as src:
            for line in src:
                m = re.match(r'^(hall|room):\s*\.chance\s+([\d.]+)\s+\.types\s+(.*)$', line.strip())
                if not m:
                    continue
                names = m.group(3).split()
                if not all(name in info for name in names):
                    continue
                prof = [S._monster_profile(name) for name in names]
                if any(x[1] for x in prof):
                    continue
                r = 1
                occupied = set()
                for name, (size, _, _) in zip(names, prof):
                    if name not in stealth:
                        with open(info[name], encoding='utf-8', errors='ignore') as src:
                            stealth[name] = bool(re.search(r'^spawn:.*\bStealth2\b', src.read(), re.M))
                    if stealth[name]:
                        occupied.update(range(r, min(5, r+size)))
                    r += size
                if occupied:
                    count += 1
                    total += float(m.group(2))
                    if occupied.intersection(ranks):
                        eligible += 1
                        reachable += float(m.group(2))
    return dict(fraction=reachable/total if total else 0., weighted_all=total,
                weighted_reachable=reachable, rows_all=count, rows_reachable=eligible)


def modifiers(S, k, buffs, marked=False):
    """Return offensive modifiers; unsupported conditional buffs are excluded."""
    result = {}
    def add(name, x):
        if name in OFFENSIVE and x > 0:
            result[name] = result.get(name, 0.) + x
    if 'combat_stat_buff' in k:
        for key in ('defense_rating_add', 'protection_rating_add'):
            add(key[:-4], -S.num(S.first(k, key)) / 100)
    for name in k.get('buff_ids', []):
        b = buffs.get(name.strip('"'), {})
        rule = b.get('rule_type')
        if rule not in (None, 'always'):
            if rule != 'is_actor_status' or b.get('rule_data', {}).get('string') != 'tagged' or b.get('is_false_rule', False) or not marked:
                continue
        stat, sub, amount = b.get('stat_type'), b.get('stat_sub_type'), b.get('amount', 0.)
        if stat in ('combat_stat_add', 'combat_stat_multiply'):
            add(sub, -amount)
        elif stat == 'crit_received_chance':
            add('crit_received', amount)
        elif stat == 'damage_received_percent':
            add('dmg_received', amount)
    if S.first(k, 'buff_type') == 'crit_received_chance':
        a = S.first(k, 'buff_amount')
        add('crit_received', S.num(a) / 100 if a.endswith('%') else S.num(a))
    return result


def groups(S, effects, buffs, P, marked):
    out = []
    for text in effects:
        k = S.kv(text)
        if S.first(k, 'target', 'target') not in ('target', 'target_group'):
            continue
        if S.first(k, 'keyStatus') and not (S.first(k, 'keyStatus') == 'tagged' and marked):
            continue
        active = k if P.get('DEBUFF_FORMATS', True) else {key:val for key,val in k.items() if key not in ('buff_ids', 'buff_type', 'buff_amount')}
        mods = modifiers(S, active, buffs, marked)
        if not P.get('DMG_RECEIVED', True):
            mods.pop('dmg_received', None)
        if not mods:
            continue
        out.append(dict(mods=mods, chance=S.num(S.first(k, 'chance', '100')) / 100,
                        duration=int(S.effect_duration(k, P)),
                        hit=S.first(k, 'on_hit', 'true') == 'true',
                        miss=S.first(k, 'on_miss', 'false') == 'true',
                        crit_bonus=0 if S.first(k, 'crit_doesnt_apply_to_roll') == 'true' else P['CRIT_EFF']))
    return out


@functools.lru_cache(maxsize=None)
def profiles(S, level=4):
    """Frozen vanilla equipment basis, equally weighted classes, no trinkets.

    These are standardized basic attacks, not a guessed party skill rotation.
    Specific physical-party profiles can be supplied in SUPPORT_PROFILES.
    """
    return tuple((tuple(H['dmg']), 85 + 5 * level, H['wcrit'] / 100, 0.)
                 for h in S.KO for H in [S.load_hero(h, 'vanilla', level)])


@functools.lru_cache(maxsize=100000)
def followup(S, profile_set, dodge, prot, armor, dodge_down, crit_up, received_up, side_hp):
    """Same enemy, same weapons; mitigation/crit evaluated before averaging.

    damage_received_percent order is not engine verified: post-mitigation
    multiplicative sensitivity only, explicitly separate from PROT/dodge/crit.
    """
    total = critical = 0.
    for weapon, acc, crit, dmg in profile_set:
        h = S.hit_probability(acc, dodge - dodge_down * 100)
        c = clamp(crit + crit_up)
        total += h * S.damage_mean(weapon, dmg, c, max(0., prot - armor)) * (1 + received_up)
        critical += h * c * side_hp
    n = len(profile_set)
    return total / n, critical / n


def support_value(S, C, row, d, effects, monsters=None):
    """Marginal follow-up damage and crit side-effects; EHP is not included.

    Opening hit/crit, status resistance and opening survival remain correlated.
    Future death is a visible survival prior, NOT a simulated sequence of kills.
    Use finite_sequence for HP-capped follow-up scenarios in the audit.
    """
    P, H = C.P, C.H
    level = int(S.first(d, 'level', '4'))
    ps = tuple(P.get('SUPPORT_PROFILES') or profiles(S, level))
    pool = monsters if monsters is not None else S.MONS
    crit = clamp(S.f32(S.percent32(S.num(S.first(d, 'crit'))) + S.percent32(H['wcrit'])))
    if S.first(d, 'is_crit_valid', 'true').lower() != 'true':
        crit = 0.
    atk = S.num(S.first(d, 'atk'))
    dmg = S.num(S.first(d, 'dmg'))
    has_damage = atk > 0 and dmg > -100
    total = side = 0.
    marked_chance = clamp(P.get('SUPPORT_MARKED', P['COND_OTHER']))
    side_hp = S.CRIT_SIDE_HP if P.get('CRIT_SIDE', True) else 0.
    for marked, pm in ((False, 1 - marked_chance), (True, marked_chance)):
        if not pm:
            continue
        gs = groups(S, effects, C.buffs, P, marked)
        if not gs:
            continue
        for m in pool:
            h = S.hit(m, atk) if atk else 1.
            target_hp = P.get('SUPPORT_TARGET_HP')
            if target_hp is None and P.get('SUPPORT_OPENING_SURVIVAL', True):
                target_hp = m.get('hp')
            normal, critical = S.damage_distribution(H['dmg'], dmg, 0 if S.first(d, 'ignore_protection') == 'true' else m['prot']) if has_damage else ((0,), 0)
            survival_n = 1. if target_hp is None else st.mean(float(x < target_hp) for x in normal)
            survival_c = 1. if target_hp is None else float(critical < target_hp)
            baseline = followup(S, ps, m['dodge'], m['prot'], 0., 0., 0., 0., side_hp)
            for landed, is_crit, branch in ((False, False, 1-h), (True, False, h*(1-crit)*survival_n), (True, True, h*crit*survival_c)):
                if not branch:
                    continue
                probs = [clamp(g['chance'] + (g['crit_bonus'] if is_crit else 0) - m['debuff']/100)
                         if g['hit' if landed else 'miss'] else 0. for g in gs]
                for bits in itertools.product((0, 1), repeat=len(gs)):
                    prob = math.prod(p if bit else 1-p for bit,p in zip(bits, probs))
                    if not prob:
                        continue
                    horizon = min(max(g['duration'] for g in gs), int(P.get('SUPPORT_HORIZON', 3)))
                    for turn in range(horizon):
                        mods = {k: 0. for k in OFFENSIVE}
                        for bit, g in zip(bits, gs):
                            if bit and turn < g['duration']:
                                for key, val in g['mods'].items():
                                    mods[key] += val
                        if not any(mods.values()):
                            continue
                        changed = followup(S, ps, m['dodge'], m['prot'], mods['protection_rating'], mods['defense_rating'], mods['crit_received'], mods['dmg_received'], side_hp)
                        alive = (P['DEBUFF_W1'] if turn == 0 else (1-P['DEATH_RATE'])**turn) if P.get('DEBUFF_TIMING', True) else 1.
                        weight = pm * branch * prob * alive * P['TGT_ATTACKS'] / len(pool)
                        total += (changed[0]-baseline[0]) * weight
                        side += (changed[1]-baseline[1]) * weight
    return total, side


def finite_sequence(S, weapon, acc, crit, modifier, hp, dodge, prot, attacks):
    """Exact finite HP-loss distribution for repeated identical direct attacks.

    No external deaths, DOT, initiative, kill side effects or status retries.
    It bounds overkill in scenario checks; not added to the weighted prior above.
    """
    h = S.hit_probability(acc, dodge)
    normal, critical = S.damage_distribution(weapon, modifier, prot)
    outcomes = [(0, 1-h), (critical, h*crit)] + [(x, h*(1-crit)/len(normal)) for x in normal]
    distribution = {hp: 1.}
    for _ in range(attacks):
        nxt = {}
        for left, p in distribution.items():
            for damage, q in outcomes:
                end = max(0, left-damage)
                nxt[end] = nxt.get(end, 0.) + p*q
        distribution = nxt
    return hp - sum(left*p for left,p in distribution.items())
