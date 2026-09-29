"""강함 순위 모델 v2 (R-VALUE-04). 바닐라와 RB를 같은 방식으로 계산해 비교한다.

사용: python tools/strength.py [--detail 영웅id] [--sens]
- 5레벨 기술 / 무기·방어구 5단계 / 영웅 등급(_C) 일반 몬스터 모집단(보스·오브젝트 제외).
- 모든 가치는 HP 환산. 기술 목록은 평타 배수(R-VALUE-02)로도 표기.
- 파라미터와 출처는 PARAM 에 모아 둔다. 바꾸면 design/analysis/hero_power_v2.md 도 갱신할 것.
"""
import os, re, glob, sys, io, math, argparse, json, functools, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import effect_common as ec

M_ROOT, G = ec.paths()

# ---------------------------------------------------------------- 파라미터 (출처)
PARAM = dict(
    MON_HIT=102.5,        # 몬스터 명중 중앙값 (hero_power.md 4-1)
    ENEMY_ACT=4.26,       # 몬스터 1행동 = 5.5 x (102.5-25)% (R-STRAT-01)
    ALLY_ATK=7.17,        # 아군 1공격 가치 (hero_power.md 4-1)
    E_SGL=1.00, E_DOT_SGL=0.90, E_AOE=0.85, E_DOT_AOE=0.40,   # 행동 경제 유효율 (R-STRAT-02)
    AOE_PER_RANK=0.8,     # 적 광역 대상 = 칸 수 x 0.8 -> 4칸 3.2명 (R-STRAT-02)
    ALLY_AOE_HEAL=0.7,    # 아군 광역 회복 과회복 보정 (hero_power.md 4-2)
    CRIT_EFF=0.20,        # 치명타 시 효과 확률 +20%p (R-CMB-08)
    CRIT_DOT_DUR=1.5,     # 치명타 시 출혈·중독 지속 x1.5 올림 (R-CMB-08)
    CRIT_STRESS=3 + 3 * 0.25 * 3,   # 본인 -3 + 아군 3명 x 25% x -3 = 5.25 (R-CMB-08), 스트레스 단위
    STRESS_HP=None,       # 스트레스 1 = HP 몇? None 이면 게임 가격에서: (영지 스트레스 회복 금화/점) / (야영 식사 체력 회복 금화/점). R-VALUE-06
    CRIT_BUFF_DUR=2,      # 직업 치명타 버프 2턴 (R-CMB-08)
    STUN_MULT=1.0,        # 기절 = 성공률 x 몬스터 1행동. 행동 경제 프리미엄은 민감도로만 본다
    SUPPORT_MULT=1.0,     # 회복·보호·스트레스 회복. 프리미엄 없음(R-STRAT-01 3) -> 민감도로만
    PUSH=1.0,             # 밀치기·섞기: 실측 가격표의 1/3 (stun.md 10-6)
    PULL=3.0,             # 당기기: 후열 스트레스 발생원을 끌어냄 [사용자]
    MARK_PARTY=2.0,       # 표식 파티 활용분 (hero_power.md 4-2)
    CORPSE=0.5,           # 시체 제거. 시뮬레이션: 메인 전략(3·4열 먼저)이면 1·2열로 끌어오는 적 0명, 무작위 처치면 0.32명 x 당기기 3.0 = 1.0 -> 중간값 0.5 (arbalest.md 참고 아님, man_at_arms.md MAA 검토)
    COND_SELF=0.6, COND_OTHER=0.3, COND_STUN=0.67,  # 조건 유지율 (hero_power.md 4-2). 적 유형 조건은 실측 비율
    LOW_HP_SELF=0.6, LOW_HP_OTHER=0.3,  # '체력 X% 이하에서만' 사용 가능 기술. 스스로 체력을 깎는 기술이 있으면 0.6 (가정, 조건 유지율과 같은 규칙)
    BUFF_DUR_CAP=2,       # 강화·약화·보호 지속 상한. 전투 2.55라운드(R-STRAT-02), 사용 시점의 평균 잔여 = v1 자기 강화 규칙과 같은 2
    DEFAULT_DUR=3,
    KILL_SHARE=1.57 / 4,  # 영웅 1명이 라운드당 처치하는 적 수 (R-STRAT-01: 파티 1.57명/라운드)
    DEATH_RATE=0.393,     # 적 1명이 한 라운드에 죽을 확률 (R-STRAT-02)
    STRESS_TAKEN=None,    # 영웅 1명이 라운드당 받는 스트레스. None 이면 몬스터 AI 가중치로 계산 (생존 적 2명 x 1행동 기대 스트레스 / 4)
    HITS_TAKEN=0.5,       # 영웅 1명이 라운드당 받는 공격. 적 4명이 2.55라운드에 걸쳐 선형 감소 -> 평균 2명 생존 -> 2회를 4명이 나눔 (R-STRAT-02)
    ACT_TOP=3,            # 행동 가치 = 상위 3기술 평균 (4칸 중 1칸은 이동·상황기)
)
W = {'기본': (50, 30, 10, 10), '균등': (25, 25, 25, 25), '행동 중시': (70, 20, 5, 5)}
RES_BASE = dict(stun=40, poison=30, bleed=30, debuff=30)   # R-RES-01

KO = dict(abomination='괴인', antiquarian='유물수집상', arbalest='석궁사수', bounty_hunter='현상금 사냥꾼',
          crusader='성전사', duelist='결투가', flagellant='고행자', grave_robber='도굴꾼', hellion='야만인',
          highwayman='노상강도', houndmaster='조련사', jester='광대', leper='나병환자', man_at_arms='중보병',
          musketeer='총사', occultist='신비학자', plague_doctor='역병 의사', runaway='도망자',
          shieldbreaker='방패 파괴자', vestal='성녀')
DLC = {'duelist', 'flagellant', 'musketeer', 'runaway', 'shieldbreaker'}


def kv(line):
    """'.key v1 v2' -> {key: [values]}.
    이름은 먼저 떼어낸다: 바닐라에 '.name "HM Dmg Marked 5".target' 처럼 공백 없이 붙은 줄이 있다."""
    line = re.sub(r'\.name\s+"[^"]*"', ' ', line)
    line = re.sub(r'"(?=\.)', '" ', line)
    line = re.sub(r'(?<=[^\s\d.])\.(?=[a-z_]{3,})', ' .', line)   # '.crit 7%.required_...' 처럼 붙은 키 (고행자)
    return {m.group(1): m.group(2).split() for m in re.finditer(r'\.(\w+)((?:\s+(?!\.)[^\s]+)*)', line)}


def num(v, default=0.0):
    try:
        return float(str(v).strip('"').rstrip('%'))
    except (TypeError, ValueError):
        return default


def first(d, k, default=''):
    v = d.get(k)
    return v[0].strip('"') if v else default


# ---------------------------------------------------------------- 몬스터 모집단
def load_monsters():
    fs = glob.glob(os.path.join(G, 'monsters', '**', '*_C.info.darkest'), recursive=True) + \
         glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*_C.info.darkest'), recursive=True)
    mons = []
    for f in fs:
        pf = ec.P(f)
        if 'arena' in pf or '/modes/' in pf:
            continue
        t = open(f, encoding='utf-8', errors='ignore').read()
        if re.search(r'^tag:\s*\.id\s*"boss"', t, re.M):
            continue
        m = re.search(r'^stats:(.*)$', t, re.M)
        if not m:
            continue
        d = {k: num(v[0]) for k, v in kv(m.group(1)).items() if v}
        if d.get('def', 0) <= 0:                       # 시체·석상 등 오브젝트
            continue
        prot = d.get('prot', 0)
        typ = re.search(r'enemy_type:\s*\.id\s*"?(\w+)', t)
        mons.append(dict(name=os.path.basename(f).split('.')[0], dodge=d['def'], prot=prot if prot <= 1 else prot / 100, spd=d.get('spd', 0),
                         stun=d.get('stun_resist', 0), poison=d.get('poison_resist', 0), bleed=d.get('bleed_resist', 0),
                         debuff=d.get('debuff_resist', 0), move=d.get('move_resist', 0),
                         type=typ.group(1) if typ else '?'))
    return mons


MONS = load_monsters()
N_MON = len(MONS)


def type_share(t):
    return sum(1 for m in MONS if m['type'] == t) / N_MON


def hit(m, acc):
    return max(0.0, min(95.0, acc - m['dodge'])) / 100


def apply_rate(m, chance, res_key):
    return max(0.0, min(1.0, (chance - (m[res_key] if res_key else 0)) / 100))


INIT_RAND = int(json.load(open(os.path.join(G, 'shared', 'rules.json'), encoding='utf-8-sig')).get('initiative_base', 8))
# 행동 순서 = 속도 + 1~INIT_RAND 무작위 (가정, 검증 V-09). 두 무작위 값의 차 분포
_D = {k: (INIT_RAND - abs(k)) / INIT_RAND ** 2 for k in range(-INIT_RAND + 1, INIT_RAND)}


def p_before(h, m):
    """속도 h인 영웅이 속도 m인 몬스터보다 먼저 행동할 확률 (동률은 절반)"""
    return sum(p * (1.0 if k > m - h else 0.5 if k == m - h else 0.0) for k, p in _D.items())


@functools.lru_cache(maxsize=None)
def dp_self(h, s):
    """영웅 속도 +s일 때 몬스터보다 먼저 행동할 확률의 평균 증가 (몬스터 모집단 평균)"""
    return st.mean(p_before(h + s, m['spd']) - p_before(h, m['spd']) for m in MONS)


@functools.lru_cache(maxsize=None)
def dp_enemy(s):
    """적 속도 -s일 때 영웅(속도 중앙값)이 먼저 행동할 확률의 평균 증가"""
    return st.mean(p_before(HERO_MED_SPD, m['spd'] - s) - p_before(HERO_MED_SPD, m['spd']) for m in MONS)


def monster_stress_per_action():
    """몬스터 1행동이 파티에 주는 기대 스트레스.
    몬스터 AI(skill_selection_desires의 base_chance) 가중치, 영웅 회피 25, 광역 칸 x 0.8, 몬스터 치명타 스트레스(+10 / 동료 50% +5) 포함"""
    eff = {}
    for f in glob.glob(os.path.join(G, '**', '*.effects.darkest'), recursive=True):
        if 'mods' in ec.P(f) or 'arena' in ec.P(f):
            continue
        for raw in open(f, encoding='utf-8', errors='ignore'):
            if raw.startswith('effect:'):
                m = re.search(r'\.name\s+"([^"]+)"', raw)
                if m:
                    eff.setdefault(m.group(1), raw.rstrip())
    brains = {}
    for f in glob.glob(os.path.join(G, '**', '*.monster_brains.json'), recursive=True):
        if 'arena' in ec.P(f) or 'mods' in ec.P(f):
            continue
        for b in json.load(open(f, encoding='utf-8-sig')).get('monster_brains', []):
            brains.setdefault(b['id'], b)
    names = {m['name'] for m in MONS}
    out = []
    for f in glob.glob(os.path.join(G, 'monsters', '**', '*_C.info.darkest'), recursive=True) + \
             glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*_C.info.darkest'), recursive=True):
        if os.path.basename(f).split('.')[0] not in names:
            continue
        t = open(f, encoding='utf-8', errors='ignore').read()
        bid = re.search(r'monster_brain:\s*\.id\s*(\S+)', t)
        w = {}
        for dsr in brains.get(bid.group(1) if bid else '', {}).get('skill_selection_desires', []):
            if dsr['type'] == 'specific_skill':
                sid = dsr['data']['combat_skill_id']
                w[sid] = w.get(sid, 0) + dsr['data'].get('base_chance', 1)
        vals, ws = [], []
        for l in re.findall(r'^skill:.*$', t, re.M):
            d = kv(l)
            tgt = first(d, 'target')
            nt = len(re.sub('[^1-4]', '', tgt)) * 0.8 if '~' in tgt else 1
            h = max(0, min(95, num(first(d, 'atk')) - 25)) / 100
            sv = 0.0
            for en in ec.effect_names_in(l):
                k = kv(eff.get(en, ''))
                if 'stress' in k and first(k, 'target', 'target') == 'target':
                    hit_ = 1 if first(k, 'on_miss', 'false').lower() == 'true' else h
                    sv += num(first(k, 'stress')) * hit_ * min(1, num(first(k, 'chance', '100')) / 100)
            dm = d.get('dmg') or ['0']
            cr = num(first(d, 'crit')) / 100 if num(dm[-1]) > 0 and first(d, 'is_crit_valid', 'True').lower() == 'true' else 0
            vals.append(sv * nt + h * cr * (10 + 3 * 0.5 * 5))
            ws.append(w.get(first(d, 'id'), 0))
        if vals:
            ws = ws if sum(ws) else [1] * len(vals)
            out.append(sum(a * b for a, b in zip(ws, vals)) / sum(ws))
    return st.mean(out)


# ---------------------------------------------------------------- 데이터 적재
def load_effects(mode):
    eff = {k: v[0] for k, v in ec.load_vanilla_effects(G).items()}
    if mode == 'rb':
        for f in glob.glob(os.path.join(M_ROOT, 'effects', '*.effects.darkest')):
            for raw in open(f, encoding='utf-8', errors='ignore'):
                if raw.startswith('effect:'):
                    n = re.search(r'\.name\s+"([^"]+)"', raw)
                    if n:
                        eff[n.group(1)] = raw.rstrip('\r\n')
    return eff


def hero_file(hero, mode):
    if mode == 'vanilla':
        return ec.vanilla_hero_file(G, hero)
    f = os.path.join(M_ROOT, 'heroes', hero, hero + '.info.darkest')
    return f if os.path.exists(f) else ec.vanilla_hero_file(G, hero)   # 모드에서 뺀 영웅(총사)은 바닐라


def load_hero(hero, mode):
    t = open(hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
    H = dict(id=hero, skills=[], crit_effects=[])
    for l in t.splitlines():
        if l.strip().startswith('//'):
            continue
        d = kv(l)
        if l.startswith('weapon:') and '_weapon_4' in l:
            H['dmg'] = (num(d['dmg'][0]), num(d['dmg'][1])); H['wcrit'] = num(d['crit'][0]); H['spd'] = num(d['spd'][0])
        elif l.startswith('armour:') and '_armour_4' in l:
            H['def'] = num(d['def'][0]); H['hp'] = num(d['hp'][0])
        elif l.startswith('resistances:'):
            H['res'] = {k: num(v[0]) for k, v in d.items()}
        elif l.startswith('riposte_skill:'):
            H['riposte'] = d
        elif l.startswith('crit:'):
            H['crit_effects'] = ec.effect_names_in(l.replace('.effects', '.effect'))
        elif l.startswith('combat_skill:') and first(d, 'level') == '4':
            H['skills'].append((l, d))
    return H


# ---------------------------------------------------------------- 가치 계산
class Ctx:
    def __init__(s, H, eff, buffs, P):
        s.H, s.eff, s.buffs, s.P = H, eff, buffs, P
        lo, hi = H['dmg']
        s.avg, s.max = (lo + hi) / 2, hi
        s.med_hp = PARAM_MED_HP
        s.self_wound = any('.target "performer"' in eff.get(n, '') and '.dotBleed' in eff.get(n, '')
                           for l, d in H['skills'] for n in ec.effect_names_in(l))
        s.self_status = set()            # 이 영웅이 스스로 걸 수 있는 상태 -> 조건 유지율 0.6
        for l, d in H['skills']:
            for n in ec.effect_names_in(l):
                e = eff.get(n, '')
                for key, stt in (('.tag ', 'tagged'), ('.stun ', 'stunned'), ('.dotBleed', 'bleeding'),
                                 ('.dotPoison', 'poisoned'), ('.dotBurn', 'burning')):
                    if key in e:
                        s.self_status.add(stt)

    def riposte(s, k):
        """반격 1회 기대 피해: 영웅의 riposte_skill 명중·피해·치명타 + 반격 효과의 피해·치명타 보정"""
        r = s.H.get('riposte', {})
        atk = num(first(r, 'atk', '85'))
        dm = num(first(r, 'dmg', '0')) / 100 + num(first(k, 'damage_low_multiply', '0')) / 100
        cr = (num(first(r, 'crit', '0')) + num(first(k, 'crit_chance_add', '0')) + s.H['wcrit']) / 100
        per = ((1 - cr) * s.avg + cr * s.max * 1.5) * max(0.0, 1 + dm)
        return st.mean(hit(m, atk) * per * (1 - m['prot']) for m in MONS)

    def cond_uptime(s, k):
        if 'monsterType' in k:
            return type_share(first(k, 'monsterType'))
        stt = first(k, 'keyStatus')
        u = s.P['COND_SELF'] if stt in s.self_status else s.P['COND_OTHER']
        return u * (s.P['COND_STUN'] if stt == 'stunned' else 1)

    def stat_value(s, stat, amt, dur, who):
        """강화 수치 -> HP (대상 1명, dur 턴)"""
        P = s.P
        atk_val = s.avg * 0.8 * 0.83 if who == 'self' else P['ALLY_ATK']
        if stat in ('damage_low', 'damage_high'):
            return atk_val * amt * 0.5 * dur          # low/high 각각 절반
        if stat == 'attack_rating':
            return atk_val * amt * 100 / 82.5 * dur
        if stat == 'crit_chance':
            return atk_val * amt * dur
        if stat == 'defense_rating':
            return P['ENEMY_ACT'] * P['HITS_TAKEN'] * amt * 100 / 77.5 * dur
        if stat == 'protection_rating':
            return P['ENEMY_ACT'] * P['HITS_TAKEN'] * amt * dur
        if stat == 'speed_rating':                  # amt = 속도 점수(원값). 먼저 행동해 죽이는 적의 행동을 지운다
            h = s.H['spd'] if who == 'self' else HERO_MED_SPD
            return P['KILL_SHARE'] * dp_self(h, amt) * P['ENEMY_ACT'] * dur
        return 0.0

    def stress_resist_value(s, amt, dur):
        """받는 스트레스 amt(음수 = 감소) -> HP. 대상 1명, dur 턴"""
        return -amt * s.P['STRESS_TAKEN'] * dur * s.P['STRESS_HP']

    def buff_ids_value(s, ids, dur, who):
        v = 0.0
        for b in ids:
            B = s.buffs.get(b.strip('"'))
            if not B:
                continue
            cm = 1.0 if B.get('rule_type') in (None, 'always') else s.P['COND_OTHER']
            if B.get('stat_type') == 'stress_dmg_received_percent':
                v += cm * s.stress_resist_value(B['amount'], dur)
            elif B.get('stat_type') in ('combat_stat_add', 'combat_stat_multiply'):
                v += cm * s.stat_value(B['stat_sub_type'], B['amount'], dur, who)
        return v


def skill_value(C, l, d):
    P, H = C.P, C.H
    tgt = first(d, 'target')
    ally, aoe, self_only = '@' in tgt, '~' in tgt, tgt == ''     # '@~1234' 와 '~@1234' 두 표기가 모두 있다
    enemy = not ally and not self_only
    ranks = len(re.sub(r'[^1-4]', '', tgt))
    atk = num(first(d, 'atk', '0')); dmgm = num(first(d, 'dmg', '0')) / 100
    crit_valid = first(d, 'is_crit_valid', 'True').lower() == 'true'
    crit = (num(first(d, 'crit', '0')) + H['wcrit']) / 100 if crit_valid else 0.0
    ign_prot = first(d, 'ignore_protection', 'false').lower() == 'true'
    limit = num(first(d, 'per_battle_limit', '0'))
    effs = [C.eff.get(n, '') for n in ec.effect_names_in(l)]
    parts = {}

    def add(k, v):
        if v:
            parts[k] = parts.get(k, 0) + v

    n_t = ranks * P['AOE_PER_RANK'] if (aoe and enemy) else (ranks if (aoe and ally) else 1)
    does_dmg = enemy and dmgm > -1 and atk > 0

    # 조건부 피해 보너스 (가산, V-01 작업 가정)
    cond_bonus = 0.0
    for e in effs:
        k = kv(e)
        if first(k, 'target') == 'performer' and ('keyStatus' in k or 'monsterType' in k) and 'damage_low_multiply' in k:
            lo = num(first(k, 'damage_low_multiply')); hi = num(first(k, 'damage_high_multiply', str(lo)))
            cond_bonus += (lo + hi) / 200 * C.cond_uptime(k)

    # 직접 피해 (몬스터 분포 평균, 치명타 = 최대값 x 1.5)
    p_any_crit = 0.0
    if does_dmg:
        mult = max(0.0, 1 + dmgm + cond_bonus)
        dm = ((1 - crit) * C.avg + crit * C.max * 1.5) * mult
        per = st.mean(hit(m, atk) * dm * (1 if ign_prot else 1 - m['prot']) for m in MONS)
        add('직접', per * n_t * (P['E_AOE'] if aoe else P['E_SGL']))
        ph = st.mean(hit(m, atk) for m in MONS) * crit
        p_any_crit = 1 - (1 - ph) ** n_t

    for e in effs:
        if not e:
            continue
        k = kv(e)
        who = first(k, 'target', 'target')
        chance = num(first(k, 'chance', '100'))
        on_hit = first(k, 'on_hit', 'true').lower() == 'true'
        dur = num(first(k, 'duration', str(P['DEFAULT_DUR']))) or P['DEFAULT_DUR']
        if first(k, 'buff_duration_type') == 'combat_end':          # '.duration 1 .buff_duration_type combat_end' = 전투 끝까지
            dur = P['BUFF_DUR_CAP']
        if who in ('target', 'target_group') and enemy:          # target_group = 적 그룹 전체 (시체 제거)
            def ev(res_key, fn=None):
                tot = 0.0
                for m in MONS:
                    h = hit(m, atk) if (on_hit and atk > 0) else 1.0
                    a0 = apply_rate(m, chance, res_key)
                    a1 = apply_rate(m, chance + P['CRIT_EFF'] * 100, res_key)
                    tot += h * ((1 - crit) * (fn(a0, False) if fn else a0) + crit * (fn(a1, True) if fn else a1))
                return tot / N_MON
            if 'stun' in k:
                add('기절', ev('stun') * P['ENEMY_ACT'] * P['STUN_MULT'] * n_t)
            for key, rk, nm in (('dotBleed', 'bleed', '출혈'), ('dotPoison', 'poison', '중독'), ('dotBurn', None, '화상')):
                if key in k:
                    per_tick = num(first(k, key))
                    cd = math.ceil(dur * P['CRIT_DOT_DUR']) if rk else dur
                    val = ev(rk, fn=lambda a, c: a * per_tick * (cd if c else dur))
                    add(nm, val * n_t * (P['E_DOT_AOE'] if aoe else P['E_DOT_SGL']))
            if 'push' in k or 'shuffletarget' in k:
                add('이동', ev('move') * P['PUSH'] * n_t)
            if 'pull' in k:
                add('이동', ev('move') * P['PULL'] * n_t)
            if 'tag' in k:
                add('표식', st.mean(hit(m, atk) for m in MONS) * P['MARK_PARTY'] * n_t)
            if 'kill_enemy_types' in k:
                add('시체', P['CORPSE'])
            if 'combat_stat_buff' in k:
                v = 0.0
                for key in k:
                    if not key.endswith(('_add', '_multiply')):
                        continue
                    x = -num(first(k, key)) / 100
                    if x <= 0:
                        continue
                    if key == 'speed_rating_add':           # 속도 점수 원값. 적이 늦어져 먼저 죽는다
                        v += P['DEATH_RATE'] * dp_enemy(x * 100) * P['ENEMY_ACT']
                        continue
                    if key.startswith('damage_'):
                        v += P['ENEMY_ACT'] * x * 0.5
                    elif key == 'attack_rating_add':
                        v += P['ENEMY_ACT'] * x * 100 / 77.5
                    elif key == 'defense_rating_add':
                        v += P['ALLY_ATK'] * x * 100 / 82.5 * 1.5
                    elif key == 'protection_rating_add':
                        v += P['ALLY_ATK'] * x * 1.5
                add('약화', ev('debuff') * v * min(dur, P['BUFF_DUR_CAP']) * n_t)
        else:
            if who == 'performer' and ('keyStatus' in k or 'monsterType' in k):
                continue                                       # 조건부 피해 (위에서 처리)
            tgt_n = 1 if (who == 'performer' or self_only or not ally) else n_t
            if who == 'performer_group_other':             # 자신을 뺀 아군 전원 (결집 신호탄)
                tgt_n = 3
            elif who == 'performer_group':
                tgt_n = 4
            ch = min(1.0, chance / 100)
            heal_n = tgt_n * (P['ALLY_AOE_HEAL'] if tgt_n > 1 else 1)
            sm = P['SUPPORT_MULT']
            if 'heal' in k:
                add('회복', num(first(k, 'heal')) * ch * heal_n * sm)
            if 'healstress' in k:
                add('스트레스', num(first(k, 'healstress')) * ch * heal_n * sm * P['STRESS_HP'])
            if 'dotHpHeal' in k:
                add('회복', num(first(k, 'dotHpHeal')) * dur * ch * heal_n * sm)
            if 'heal_percent' in k:
                x = num(first(k, 'heal_percent')); x = x if x <= 1 else x / 100      # 0.43 = 43%
                base_hp = H['hp'] if who == 'performer' else C.med_hp
                add('회복', x * base_hp * ch * (1 if who == 'performer' else heal_n) * sm)
            if 'guard' in k:
                add('보호', P['ENEMY_ACT'] * P['HITS_TAKEN'] * min(dur, P['BUFF_DUR_CAP']) * ch * sm)
            if 'health_damage_blocks' in k:
                add('보호', P['ENEMY_ACT'] * num(first(k, 'health_damage_blocks')) * ch * sm)
            if 'riposte' in k:
                add('반격', C.riposte(k) * P['HITS_TAKEN'] * min(dur, P['BUFF_DUR_CAP']) * ch)
            if 'combat_stat_buff' in k:
                cm = P['COND_OTHER'] if 'keyStatus' in k else 1.0
                wh = 'self' if tgt_n == 1 and who == 'performer' else 'ally'
                dd = min(dur, P['BUFF_DUR_CAP'])
                for key in k:
                    x = num(first(k, key)) / 100
                    if key == 'speed_rating_add':
                        x = num(first(k, key))                # 속도는 % 가 아니라 점수
                    # 자기 약화(탈진 등)는 대가로 뺀다. buff_ids 경로와 같은 처리
                    if key.endswith(('_add', '_multiply')) and (x > 0 or wh == 'self'):
                        stat = key.replace('_add', '').replace('_multiply', '')
                        add('강화' if x > 0 else '대가', C.stat_value(stat, x, dd, wh) * tgt_n * ch * cm)
            if 'buff_ids' in k:
                wh = 'self' if who == 'performer' else 'ally'
                v = C.buff_ids_value(k['buff_ids'], min(dur, P['BUFF_DUR_CAP']), wh) * tgt_n * ch
                add('강화' if v > 0 else '대가', v)
            if who == 'performer':                          # 자해 지속 피해(고행자 재기)는 자기 저항 적용 후 대가
                for key, rk in (('dotBleed', 'bleed'), ('dotPoison', 'poison')):
                    if key in k:
                        a = max(0.0, min(1.0, (chance - H['res'].get(rk, 0)) / 100))
                        add('대가', -num(first(k, key)) * dur * a)
            if 'stress' in k and who == 'performer':
                add('대가', -num(first(k, 'stress')) * ch * P['STRESS_HP'])
    if 'heal' in d and len(d['heal']) >= 2:                  # 기술 줄의 .heal lo hi
        amt = (num(d['heal'][0]) + num(d['heal'][1])) / 2
        hn = n_t * (P['ALLY_AOE_HEAL'] if n_t > 1 else 1) if ally else 1
        add('회복', amt * hn * P['SUPPORT_MULT'])

    # 치명타 부수 효과: 스트레스 회복 + 직업 버프 2턴. 광역도 1회만 (R-CMB-08)
    if p_any_crit > 0:
        cb = sum(C.buff_ids_value(kv(C.eff.get(n, '')).get('buff_ids', []), P['CRIT_BUFF_DUR'], 'self')
                 for n in H['crit_effects'])
        add('치명타', p_any_crit * (P['CRIT_STRESS'] * P['STRESS_HP'] + cb))

    tot = sum(parts.values())
    if limit:
        tot *= min(1.0, limit / 3)
    if 'required_performer_hp_range' in d:
        tot *= P['LOW_HP_SELF'] if C.self_wound else P['LOW_HP_OTHER']
    return tot, parts


PARAM_MED_HP = 43.0      # evaluate()에서 바닐라 5레벨 체력 중앙값으로 덮어쓴다
HERO_MED_SPD = 7.0
_STRESS_CACHE = None


def stress_price_ratio():
    """R-VALUE-06 스트레스 회복 난이도: 원 개발사가 매긴 가격 비율.
    스트레스: 수도원·여관 기본 단계 활동의 금화 / 회복량 평균.
    체력: 야영 '식사'(음식 1개 = 75금화)가 최대 체력 10% 회복 (shared/rules.json meals_table full), 체력 중앙값 기준.
    가격으로 보면 한계선 비율(체력 중앙값/100)은 상쇄되어, 결과가 곧 '스트레스 1 = HP 몇'이다."""
    per = []
    for b in ('abbey', 'tavern'):
        f = os.path.join(G, 'campaign', 'town', 'buildings', b, b + '.building.json')
        d = json.loads(re.sub(r',\s*([}\]])', r'\1', open(f, encoding='utf-8-sig').read()))
        for a in d['data']['activities']:
            dd = a['data']
            if 'stress_upgrades' in dd and 'cost_upgrades' in dd:
                per.append(dd['cost_upgrades'][0]['cost_currency']['amount'] / dd['stress_upgrades'][0]['heal_low'])
    gold_per_stress = st.mean(per)
    rules = json.load(open(os.path.join(G, 'shared', 'rules.json'), encoding='utf-8-sig'))
    full = [m for m in rules['meals_table'] if m['type'] == 'full'][0]
    food = 75.0
    for l in open(os.path.join(G, 'inventory', 'base.supply.inventory.items.darkest'), encoding='utf-8', errors='ignore'):
        if '.type "provision"' in l:
            food = num(first(kv(l), 'purchase_gold_value', '75'))
    gold_per_hp = food * full['rations_per'] / (full['healing'] * stress_hp('vanilla') * 100)
    return gold_per_stress / gold_per_hp, gold_per_stress, gold_per_hp


def stress_hp(mode):
    hps = [load_hero(h, mode)['hp'] for h in KO]
    return st.median(hps) / 100


def evaluate(mode, P=PARAM):
    global PARAM_MED_HP, HERO_MED_SPD, _STRESS_CACHE
    PARAM_MED_HP = stress_hp('vanilla') * 100
    HERO_MED_SPD = st.median(load_hero(h, 'vanilla')['spd'] for h in KO)
    if P['STRESS_TAKEN'] is None:
        if _STRESS_CACHE is None:
            _STRESS_CACHE = 2 * monster_stress_per_action() / 4
        P = dict(P, STRESS_TAKEN=_STRESS_CACHE)
    if P['STRESS_HP'] is None:
        P = dict(P, STRESS_HP=stress_price_ratio()[0])     # R-VALUE-06 가격 비율
    eff = load_effects(mode)
    buffs = ec.load_buffs(G)
    out = {}
    for hero in KO:
        H = load_hero(hero, mode)
        C = Ctx(H, eff, buffs, P)
        wc = H['wcrit'] / 100
        base = st.mean(hit(m, 105) * ((1 - wc) * C.avg + wc * C.max * 1.5) * (1 - m['prot']) for m in MONS)
        sk = {}
        for l, d in H['skills']:
            sid = first(d, 'id')
            v, parts = skill_value(C, l, d)
            launch = re.sub(r'[^1-4]', '', first(d, 'launch'))
            if sid not in sk or v > sk[sid][0]:                 # 모드별 중복(괴인 등)은 큰 쪽
                sk[sid] = (v, parts, launch)
        vals = sorted((v[0] for v in sk.values()), reverse=True)
        act = st.mean(vals[:P['ACT_TOP']])
        top2 = sorted(sk, key=lambda s: -sk[s][1].get('직접', 0))[:2]

        def pts(s):
            p = sk[s][1]
            return 2 if (s in top2 or any(p.get(x, 0) > 0 for x in ('회복', '기절', '보호', '표식'))) else 1
        rank_pts = [sum(pts(s) for s in sk if str(r) in sk[s][2]) for r in (1, 2, 3, 4)]
        best = max(rank_pts)
        opt = sum(1 for x in rank_pts if x >= 0.9 * best)
        sub = sum(1 for x in rank_pts if 0.6 * best <= x < 0.9 * best)
        rmean = st.mean(H['res'].get(k, 0) for k in RES_BASE) - st.mean(RES_BASE.values())
        surv = H['hp'] / ((P['MON_HIT'] - H['def']) / 100) * (1 + rmean / 200)
        out[hero] = dict(act=act, surv=surv, spd=H['spd'], flex=opt + 0.5 * sub, base=base, skills=sk, rank_pts=rank_pts)
    return out


def score(allres, wkey):
    """바닐라+RB 40행을 한 번에 0~100 정규화 -> 두 상태의 점수가 같은 눈금"""
    rows = [r for res in allres.values() for r in res.values()]
    rng = {k: (min(r[k] for r in rows), max(r[k] for r in rows)) for k in ('act', 'surv', 'spd', 'flex')}
    for r in rows:
        n = [(r[k] - rng[k][0]) / ((rng[k][1] - rng[k][0]) or 1) * 100 for k in ('act', 'surv', 'spd', 'flex')]
        r.setdefault('score', {})[wkey] = sum(a * b for a, b in zip(n, W[wkey])) / 100


def ranking(res, wkey):
    order = sorted(res, key=lambda h: -res[h]['score'][wkey])
    return {h: i + 1 for i, h in enumerate(order)}, order


def run(P=PARAM):
    allres = {m: evaluate(m, P) for m in ('vanilla', 'rb')}
    for wk in W:
        score(allres, wk)
    return allres


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--detail'); ap.add_argument('--sens', action='store_true')
    a = ap.parse_args()
    allres = run()
    print(f'몬스터 모집단: 영웅 등급 일반 몬스터 {N_MON}종 (보스·오브젝트 제외) / 스트레스 1 = HP {stress_price_ratio()[0]:.2f} (가격 비율, R-VALUE-06)\n')
    rv = ranking(allres['vanilla'], '기본')[0]
    rr, orr = ranking(allres['rb'], '기본')
    # 표시 단위 = 환산 피해 보정(%p) [제작자 지정, R-VALUE-02 개정]. HP는 내부 계산에만 쓴다.
    #   기술: "이 기술 1회 = 그 영웅 무기로 피해 보정 X%인 단일 공격 1회" (평타 = 피해 보정 0%)
    #   행동 가치: 표준 평타(바닐라 20영웅 평타 중앙값) 기준 -> 영웅끼리 비교 가능
    std = st.median(r['base'] for r in allres['vanilla'].values())
    pp = lambda v, base: (v / base - 1) * 100
    print(f'표준 평타 = 바닐라 20영웅 평타 중앙값 (1%p = {std / 100:.3f} HP)\n')
    print('| RB 순위 | 영웅 | 총점 | 행동 가치 (표준 평타 기준 %p) | 유효 체력 | 속도 | 유연성 | 바닐라 순위 (총점) | 균등 / 행동 중시 | 상위 기술 (자기 무기 기준 환산 피해 보정) |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for h in orr:
        r, v = allres['rb'][h], allres['vanilla'][h]
        top = sorted(r['skills'].items(), key=lambda x: -x[1][0])[:3]
        ts = ', '.join(f'{s} {pp(x[0], r["base"]):+.0f}%p' for s, x in top)
        oth = '/'.join(str(ranking(allres['rb'], wk)[0][h]) for wk in ('균등', '행동 중시'))
        print(f'| {rr[h]} | {KO[h]}{"*" if h in DLC else ""} | {r["score"]["기본"]:.0f} | {pp(r["act"], std):+.0f}%p | {r["surv"]:.0f} | '
              f'{r["spd"]:.0f} | {r["flex"]:.1f} | {rv[h]} ({v["score"]["기본"]:.0f}) | {oth} | {ts} |')
    if a.detail:
        for mode in ('vanilla', 'rb'):
            r = allres[mode][a.detail]
            print(f'\n[{mode}] {KO[a.detail]} (자기 무기 기준, 평타 = 피해 보정 0% 단일 공격)  열 점수 {r["rank_pts"]}')
            for s, (v, parts, launch) in sorted(r['skills'].items(), key=lambda x: -x[1][0]):
                print(f'  {s:24s} 환산 {pp(v, r["base"]):+5.0f}%p  사용 {launch:5s} 구성: ' +
                      ' '.join(f'{k}{x / r["base"] * 100:+.0f}' for k, x in parts.items()))
    if a.sens:
        variants = {'스트레스=HP 0.43(한계선)': dict(STRESS_HP=0.43), '스트레스=HP 1(v1)': dict(STRESS_HP=1.0), '기절 x1.3': dict(STUN_MULT=1.3), '지원 x0.7': dict(SUPPORT_MULT=0.7),
                    '광역 직접 0.75': dict(E_AOE=0.75), '조건 유지율 0.45/0.2': dict(COND_SELF=0.45, COND_OTHER=0.2),
                    '저체력 조건 0.3': dict(LOW_HP_SELF=0.3)}
        rows = {h: [rr[h]] for h in KO}
        for ch in variants.values():
            rk = ranking(run(dict(PARAM, **ch))['rb'], '기본')[0]
            for h in KO:
                rows[h].append(rk[h])
        print('\n민감도 (RB, 기본 가중치 순위)\n| 영웅 | 기본 | ' + ' | '.join(variants) + ' | 범위 |')
        print('|---' * (len(variants) + 3) + '|')
        for h in orr:
            x = rows[h]
            print(f'| {KO[h]} | ' + ' | '.join(map(str, x)) + f' | {min(x)}~{max(x)} |')


if __name__ == '__main__':
    main()
