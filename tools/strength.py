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
    TGT_ATTACKS=1.5,      # R-VALUE-19: 약화 걸린 적 1명이 라운드당 받는 아군 공격 수 (v1 hero_power.md 4-2의 x1.5, 집중 공격). 회피·방어·받는 치명타·받는 피해 공통
    ENEMY_DODGE_CAP=True, # R-VALUE-19: 적 회피 감소는 몬스터 회피 분포 + 95% 자동 명중 상한으로 센다
    DMG_RECEIVED=True,    # R-VALUE-18: 적 받는 피해 +x = 그 적을 치는 아군 공격 피해 +x (라운드당 아군 1공격 가정, 받는 치명타와 같은 가정)
    ENEMY_ACC=True,       # R-VALUE-17: 적 명중 감소 = 그 적 명중 분포·영웅 회피·0% 바닥·스트레스 공격까지 (회피 R-VALUE-13의 거울)
    CRIT_SIDE=True,       # R-VALUE-16: 치명타 확률 강화·받는 치명타 약화에 치명타 부수 효과(스트레스 회복 + 직업 치명타 버프)를 더한다
    STUN_MULT=1.0,        # 기절 = 성공률 x 몬스터 1행동. 행동 경제 프리미엄은 민감도로만 본다
    SUPPORT_MULT=1.0,     # 회복·보호·스트레스 회복. 프리미엄 없음(R-STRAT-01 3) -> 민감도로만
    PUSH=1.0,             # 밀치기·섞기: 실측 가격표의 1/3 (stun.md 10-6)
    PULL=3.0,             # 당기기: 후열 스트레스 발생원을 끌어냄 [사용자]
    MARK_PARTY=2.0,       # 표식 파티 활용분 (hero_power.md 4-2)
    CORPSE=0.5,           # 시체 제거. 시뮬레이션: 메인 전략(3·4열 먼저)이면 1·2열로 끌어오는 적 0명, 무작위 처치면 0.32명 x 당기기 3.0 = 1.0 -> 중간값 0.5 (arbalest.md 참고 아님, man_at_arms.md MAA 검토)
    COND_SELF=0.6, COND_OTHER=0.3, COND_STUN=0.67,  # 조건 유지율 (hero_power.md 4-2). 적 유형 조건은 실측 비율
    LOW_HP_SELF=0.6, LOW_HP_OTHER=0.3,  # '체력 X% 이하에서만' 사용 가능 기술. 스스로 체력을 깎는 기술이 있으면 0.6 (가정, 조건 유지율과 같은 규칙)
    RES_DEBUFF=True,      # R-VALUE-15: 적 저항 감소를 센다 (가정값: 아래 4개)
    RES_ATTEMPTS=0.4,     # 그 적에게 아군이 해당 효과를 시도하는 횟수/라운드 (조합 1명이 40% 턴에 사용 가정)
    RES_DOT_HP=12.0,      # 출혈·중독 1회 성공 총량 (5렙 기술 4 x 3턴 수준)
    RES_DEBUFF_HP=3.0,    # 약화 1회 성공 가치
    RES_MOVE_HP=2.0,      # 밀치기·당기기 1회 성공 가치
    PROT_FLOOR=True,      # R-VALUE-14: 방어 감소는 적 방어 0 아래로 안 내려간다 [제작자 확인]
    DODGE_EHP=True,       # R-VALUE-13: 회피 강화는 적 명중 분포·영웅 회피·0% 바닥·유효 체력·스트레스를 반영
    DODGE_STRESS=True,
    DEBUFF_FORMATS=True,  # R-VALUE-12: 적 약화를 buff_ids·buff_type 형식으로 걸어도 센다 (받는 치명타 증가 포함)
    FREE_ACTION=True,     # R-VALUE-11: 무료 행동(.is_continue_turn)은 행동을 대신하지 않고 더한다. 매 턴 다시 쓸 수 있어 행동당 가치 = 기술 가치 / 지속 상한
    BUFF_DUR_CAP=2,       # 강화·약화·보호 지속 상한. 전투 2.55라운드(R-STRAT-02), 사용 시점의 평균 잔여 = v1 자기 강화 규칙과 같은 2
    DEFAULT_DUR=3,
    KILL_SHARE=1.57 / 4,  # 영웅 1명이 라운드당 처치하는 적 수 (R-STRAT-01: 파티 1.57명/라운드)
    DEATH_RATE=0.393,     # 적 1명이 한 라운드에 죽을 확률 (R-STRAT-02)
    STRESS_TAKEN=None,    # 영웅 1명이 라운드당 받는 스트레스. None 이면 몬스터 AI 가중치로 계산 (생존 적 2명 x 1행동 기대 스트레스 / 4)
    RANK_MODEL=True,      # R-VALUE-07: 대상 열 위협도 배수 + 적 1행동 = 편성 위협도 + 당기기·밀치기 재정의. False 면 이전 방식(민감도)
    HITS_TAKEN=0.5,
    MARK_DRAW=1.72,       # 자기 표식 중 받는 공격 배수. 표식 대상이 단일 공격을 받을 확률 55.6%(없으면 25%, 몬스터 AI marked_target 가중치 x 실제 편성 빈도). 몬스터 공격의 15%는 광역이라 표식과 무관 -> (0.85 x 0.556 + 0.15) / (0.85 x 0.25 + 0.15) = 1.72       # 영웅 1명이 라운드당 받는 공격. 적 4명이 2.55라운드에 걸쳐 선형 감소 -> 평균 2명 생존 -> 2회를 4명이 나눔 (R-STRAT-02)
    ACT_TOP=3,            # 행동 가치 = 상위 3기술 평균 (4칸 중 1칸은 이동·상황기)
    # R-VALUE-08 화상 (도망자). 툴팁: 라운드 끝에 중첩만큼 피해, 그 뒤 남은 중첩 절반. 저항 무시. 틱은 DEFAULT_DUR 라운드까지 센다
    BURN_KEEP=0.5,        # 라운드마다 남는 비율 (절반, 내림 - V-12)
    BURN_SLOW_KEEP=0.75,  # '화상 감소 +50%' 약화(흩날리는 불티) 중 남는 비율. 감소를 늦춘다고 가정 (V-12)
    HOT_STEALTH_TICKS=1,  # '은신 중' 턴당 회복: 다음 턴 시작에 1번 받고 공격하면 은신이 풀린다
    # R-VALUE-09 은신 해제: 챔피언 6종이 전투 시작 2라운드 은신(spawn Stealth2). 영웅 등급 편성의 36.9%에 출현.
    # 해제하면 그 적을 지금부터 죽일 수 있다 -> 줄어든 적 행동 x 열 위협도 = 3.94 HP (출현 전투에서 골라 쓸 때).
    # 기술 1회 기대값 = 0.369 x 3.94 x 은신 창 안에서 쓸 확률(2/2.55) = 1.14 HP
    DESTEALTH=1.14,
    # R-VALUE-10 모드 영웅(괴인): 전환 기술에 전투당 제한이 있으면 모드별 계획으로 따로 센다.
    FIGHT_ACTS=2.55,      # 전투 2.55라운드 = 영웅 1명의 행동 수 (R-STRAT-02). 전투당 1회 꾸러미를 행동당으로 나눈다
    # R-VALUE-06 개정(2026-10-03): 스트레스 = 가격 비율 + 고통(붕괴) 비용. 스트레스 100에서 75% 고통 / 25% 미덕
    AFFLICT_ROUNDS=10,    # 고통이 유지되는 라운드 (남은 원정 약 4전투 x 2.55, 영지 귀환 전까지 대개 유지) [가정]
    AFFLICT_EVENTS=1.0,   # 라운드당 고통 영웅이 반응할 사건 수 (적중·빗나감·이동 등) [가정]
    FOCUS_FIRE=True,      # R-VALUE-07 개정: 이동 가치는 우선 처치(닿는 적 중 위협이 큰 적부터 집중)로 센다
    # 2026-10-03 wiki.gg 대조 (analysis/wiki_notes.md)
    DMG_STACK='mult',     # V-01: 기술 피해 보정 x (1 + 강화·조건부 보너스) [위키 계산 예시]. 'add' = 이전 가산 가정(민감도)
    HEAL_CRIT_SGL=0.12, HEAL_CRIT_AOE=0.05,   # 회복 치명타 고정 확률 [위키]: 회복 2배 + 스트레스 −4
    KILL_ON_HIT=1.57 / 4, # '.requires_kill_target' 효과(처치 시에만)의 발동률 = 영웅 1행동당 처치 수 (R-STRAT-01)
    # R-VALUE-11: 같은 대상에게 이후 들어올 회복 행동 수/라운드 [가정, 민감도 대상].
    HEAL_FOLLOWUP_RATE=0.5,
    HEAL_FOLLOWUP_AMOUNT=None,  # None: 원본 영웅별 최대 단일 아군 직접 회복 평균의 중앙값, 회복 치명 포함
    # R-VALUE-12: 표식 특효 피해 비용. None: 일반 몬스터 표본의 AI 기술 가중 피해 비율로 추정.
    MARK_DAMAGE_BONUS=None,
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
    """적중 = 명중 − 회피. 95% 이상이면 무조건 명중(rules.json cutoffAlwaysHit 0.95), 0 이하면 빗나감(cutoffAlwaysMiss 0).
    위키의 '숨은 명중 +5'는 데이터 근거가 없어 넣지 않는다(V-15)."""
    x = acc - m['dodge']
    return 1.0 if x >= 95 else max(0.0, x) / 100


def burn_total(n, keep_rounds=0, P=None):
    """화상 중첩 n 1회가 주는 총 피해 (R-VALUE-08). 라운드 끝마다 중첩만큼 피해 후 남은 중첩 x 비율, 내림.
    keep_rounds = 감소를 늦추는 약화가 걸린 라운드 수."""
    P = P or PARAM
    tot, s = 0, int(n)
    for r in range(int(P['DEFAULT_DUR'])):
        tot += s
        s = math.floor(s * (P['BURN_SLOW_KEEP'] if r < keep_rounds else P['BURN_KEEP']))
        if s <= 0:
            break
    return tot


def burn_zone(z, rounds, P=None):
    """통제된 화상: 대상 열에 '턴 시작 시 화상 z'를 rounds 라운드. 그 열의 적이 라운드마다 1번 행동하고,
    건 라운드에는 이미 행동했을 확률 0.5."""
    P = P or PARAM
    out = 0.0
    for acted in (True, False):
        s, tot = 0, 0
        for r in range(int(P['DEFAULT_DUR'])):
            if r < rounds and not (r == 0 and acted):
                s += z
            tot += s
            s = math.floor(s * P['BURN_KEEP'])
        out += 0.5 * tot
    return out


def apply_rate(m, chance, res_key):
    return max(0.0, min(1.0, (chance - (m[res_key] if res_key else 0)) / 100))


INIT_RAND = int(json.load(open(os.path.join(G, 'shared', 'rules.json'), encoding='utf-8-sig')).get('initiative_base', 8))
# 행동 순서 = 속도 + 1~INIT_RAND 무작위 (가정, 검증 V-09). 두 무작위 값의 차 분포
_D = {k: (INIT_RAND - abs(k)) / INIT_RAND ** 2 for k in range(-INIT_RAND + 1, INIT_RAND)}


def p_before(h, m):
    """속도 h인 영웅이 속도 m인 몬스터보다 먼저 행동할 확률. 동률이면 영웅이 먼저 [위키, V-09]"""
    return sum(p * (1.0 if k >= m - h else 0.0) for k, p in _D.items())


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



@functools.lru_cache(maxsize=None)
def _monster_db():
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
    info = {}
    for f in glob.glob(os.path.join(G, '**', '*.info.darkest'), recursive=True):
        pf = ec.P(f)
        if 'mods' in pf or 'arena' in pf or '/heroes/' in pf:
            continue
        info.setdefault(os.path.basename(f).split('.')[0], f)
    return eff, brains, info


@functools.lru_cache(maxsize=None)
def _monster_profile(mid):
    """(크기, 보스 여부, ((사용열, 행동당 HP, 행동당 스트레스, AI 가중치), ...)) — 영웅 회피 25, 광역 칸 x 0.8, 몬스터 치명타 스트레스 포함"""
    eff, brains, info = _monster_db()
    t = open(info[mid], encoding='utf-8', errors='ignore').read()
    dm_ = re.search(r'^display:(.*)$', t, re.M)
    size = int(num(first(kv(dm_.group(1)), 'size', '1'))) if dm_ else 1
    boss = bool(re.search(r'^tag:\s*\.id\s*"boss"', t, re.M))
    bid = re.search(r'monster_brain:\s*\.id\s*(\S+)', t)
    w = {}
    for dsr in brains.get(bid.group(1) if bid else '', {}).get('skill_selection_desires', []):
        if dsr['type'] == 'specific_skill':
            w[dsr['data']['combat_skill_id']] = w.get(dsr['data']['combat_skill_id'], 0) + dsr['data'].get('base_chance', 1)
    sk = []
    for l in re.findall(r'^skill:.*$', t, re.M):
        d = kv(l)
        tgt = first(d, 'target')
        nt = len(re.sub('[^1-4]', '', tgt)) * 0.8 if '~' in tgt else 1
        h = max(0, min(95, num(first(d, 'atk')) - 25)) / 100
        dm = d.get('dmg') or ['0']
        lo, hi = num(dm[0]), num(dm[-1])
        cr = num(first(d, 'crit')) / 100 if hi > 0 and first(d, 'is_crit_valid', 'True').lower() == 'true' else 0
        hp = ((1 - cr) * (lo + hi) / 2 + cr * hi * 1.5) * h * nt if not tgt.startswith('@') else 0
        s = 0.0
        for en in ec.effect_names_in(l):
            k = kv(eff.get(en, ''))
            if 'stress' in k and first(k, 'target', 'target') == 'target':
                hit_ = 1 if first(k, 'on_miss', 'false').lower() == 'true' else h
                s += num(first(k, 'stress')) * hit_ * min(1, num(first(k, 'chance', '100')) / 100)
        s = s * nt + h * cr * (10 + 3 * 0.5 * 5)
        sk.append((re.sub('[^1-4]', '', first(d, 'launch')), hp, s, w.get(first(d, 'id'), 0)))
    return size, boss, tuple(sk)


def _threat_at(sk, ranks, stress_hp):
    c = [x for x in sk if any(str(r) in x[0] for r in ranks)]
    if not c:
        return 0.0
    ws = [x[3] for x in c]
    if not sum(ws):
        ws = [1] * len(c)
    return sum(wi * (x[1] + x[2] * stress_hp) for wi, x in zip(ws, c)) / sum(ws)


@functools.lru_cache(maxsize=None)
def formation_stats(stress_hp):
    """R-VALUE-07. 기본 던전 4곳 영웅 등급(.5.mash) 통로·방 편성. 보스 태그 몬스터가 든 편성은 뺀다.
    반환: tau{열: 행동당 위협도(HP + 스트레스 x stress_hp)}, mult{열: tau/평균}, act_full(점유 가중 평균 위협도),
          entries[(가중치, 자기 열, (1~4열에 섰을 때 위협도))], rho{열: 영웅 피해 기술이 닿는 비율}"""
    _, _, info = _monster_db()
    slot = {r: [] for r in (1, 2, 3, 4)}
    entries = []
    for f in sorted(glob.glob(os.path.join(G, 'dungeons', '*', '*.5.mash.darkest'))):
        for l in open(f, encoding='utf-8', errors='ignore'):
            m = re.match(r'^(hall|room):\s*\.chance\s+([\d.]+)\s+\.types\s+(.*)$', l.strip())
            if not m:
                continue
            mons = [x for x in m.group(3).split() if x in info]
            prof = [_monster_profile(x) for x in mons]
            if any(p[1] for p in prof):                 # 수집가·휘청이는 자 등 보스 태그 조우
                continue
            ch = float(m.group(2)); r = 1
            for size, _, sk in prof:
                ranks = list(range(r, min(4, r + size - 1) + 1))
                at = tuple(_threat_at(sk, [rr], stress_hp) for rr in (1, 2, 3, 4))
                home = _threat_at(sk, ranks, stress_hp)
                for rr in ranks:
                    slot[rr].append((ch / size, home))
                entries.append((ch, ranks[0], at))
                r += size
                if r > 4:
                    break
    tau = {r: sum(w * v for w, v in slot[r]) / sum(w for w, _ in slot[r]) for r in slot}
    occ = {r: sum(w for w, _ in slot[r]) for r in slot}
    act_full = sum(tau[r] * occ[r] for r in slot) / sum(occ.values())
    mean = st.mean(tau.values())
    # 영웅 쪽 도달률: 바닐라 20영웅 5레벨 피해 기술, 무기 평균 x (1 + 피해 보정)으로 가중
    reach = {r: 0.0 for r in (1, 2, 3, 4)}; tot = 0.0
    for h in KO:
        H = load_hero(h, 'vanilla'); avg = sum(H['dmg']) / 2
        for l, d in H['skills']:
            tg = first(d, 'target')
            dmg = num(first(d, 'dmg', '0')) / 100
            if tg.startswith('@') or tg == '' or dmg <= -1 or num(first(d, 'atk', '0')) <= 0:
                continue
            wv = avg * (1 + dmg); tot += wv
            for rr in re.sub('[^1-4]', '', tg):
                reach[int(rr)] += wv
    rho = {r: reach[r] / tot for r in reach}
    return tau, {r: v / mean for r, v in tau.items()}, act_full, tuple(entries), rho


@functools.lru_cache(maxsize=None)
def formation_lineups(stress_hp):
    """R-VALUE-07 개정(2026-10-03). 편성별 유닛 순서: ((가중치, ((크기, 기술 프로필), ...)), ...). 보스 편성 제외."""
    _, _, info = _monster_db()
    out = []
    for f in sorted(glob.glob(os.path.join(G, 'dungeons', '*', '*.5.mash.darkest'))):
        for l in open(f, encoding='utf-8', errors='ignore'):
            m = re.match(r'^(hall|room):\s*\.chance\s+([\d.]+)\s+\.types\s+(.*)$', l.strip())
            if not m:
                continue
            prof = [_monster_profile(x) for x in m.group(3).split() if x in info]
            if any(p_[1] for p_ in prof):
                continue
            out.append((float(m.group(2)), tuple((size, sk) for size, _, sk in prof)))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def move_value(kind, dist, tranks, stress_hp, death_rate, horizon):
    """당기기·밀치기 1회 성공의 가치(HP). R-VALUE-07 개정(2026-10-03, 제작자 지적):
    대상만이 아니라 **대열 전체**를 다시 세운다 — 대상이 dist칸 움직이면 사이의 적들이 반대로 한 칸씩 움직인다
    (앞열 적을 밀면 3열 적이 2열 근접 사거리로 들어온다 / 뒤 적을 당기면 앞열 적이 뒤로 밀려난다).
    가치 = sum(남은 행동(열) x 그 몬스터의 그 열 위협도) [이동 전 - 이동 후], 대상 열 중 가장 이득인 적을 고른다.
    상태 = 시작 4명 편성과 1명이 죽은 3명 편성(죽는 적은 고르게)의 평균. 크기 2 몬스터는 유닛 단위로 근사."""
    tau, mult, act, entries, rho = formation_stats(stress_hp)
    rbar = st.mean(rho.values())

    def remain(r):
        d = min(0.95, death_rate * rho[r] / rbar)
        return sum((1 - d) ** k for k in range(1, horizon + 1))

    rmax = max(rho.values())

    def lineup(units):
        pos, r = [], 1
        for size, sk in units:
            if r > 4:
                break
            ranks = list(range(r, min(4, r + size - 1) + 1))
            pos.append((r, _threat_at(sk, ranks, stress_hp)))
            r += size
        if PARAM['FOCUS_FIRE']:
            # 우선 처치: 파티(라운드당 1.57명 처치)가 '위협 x 도달률'이 큰 적부터 집중한다 (R-STRAT-01)
            K = PARAM['KILL_SHARE'] * 4
            dd = [0.0] * len(pos)
            for i in sorted(range(len(pos)), key=lambda i: -pos[i][1] * rho[pos[i][0]]):
                dd[i] = min(0.95, K * rho[pos[i][0]] / rmax)
                K = max(0.0, K - dd[i])
            return sum(sum((1 - dd[i]) ** k for k in range(1, horizon + 1)) * pos[i][1] for i in range(len(pos)))
        return sum(remain(p_[0]) * p_[1] for p_ in pos)

    def avg(states):
        tot = wt = 0.0
        for w, us in states:
            best = None
            for i in range(len(us)):
                if 1 + sum(u[0] for u in us[:i]) not in tranks:
                    continue
                mv = list(us); x = mv.pop(i)
                mv.insert(min(len(mv), i + dist) if kind == 'push' else max(0, i - dist), x)
                g = lineup(us) - lineup(mv)
                best = g if best is None else max(best, g)
            if best is not None:
                tot += w * best; wt += w
        return tot / wt if wt else None

    forms = formation_lineups(stress_hp)
    four = avg([(w, us) for w, us in forms])
    three = avg([(w / len(us), us[:k] + us[k + 1:]) for w, us in forms for k in range(len(us))])
    vals = [v for v in (four, three) if v is not None]
    return st.mean(vals) if vals else 0.0


# ---------------------------------------------------------------- 데이터 적재
# ---------------------------------------------------------------- 회피 (R-VALUE-13)
@functools.lru_cache(maxsize=None)
def monster_attack_accs():
    """영웅 등급 몬스터 공격 기술 명중 분포 (명중 50 이상, 근접·원거리)"""
    out = []
    for f in glob.glob(os.path.join(G, 'monsters', '*', '*_C', '*_C.info.darkest')) + \
            glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*_C.info.darkest'), recursive=True):
        for l in open(f, encoding='utf-8', errors='ignore'):
            if l.startswith('skill:') and ('"melee"' in l or '"ranged"' in l):
                m = re.search(r'\.atk ([\d.]+)%', l)
                if m and float(m.group(1)) >= 50:
                    out.append(float(m.group(1)))
    return tuple(out) or (102.5,)


def dodge_value(base, x, dur, P):
    """회피 +x(점수)를 dur턴 받은 영웅 1명의 가치(HP).
    1) 적 명중 분포와 영웅 자신의 회피로 적중률 h0 -> h1 (0% 바닥 반영)
    2) 생존 환산: 유효 체력 = 체력 / 적중률. 같은 적중률 감소도 남은 적중률이 낮을수록 가치가 커진다
       -> 막은 피해 x (기준 적중률 / h1). 기준 적중률(77.5%)에서는 예전 직선 계산과 같다
    3) 명중해야 들어오는 스트레스 공격도 함께 막는다 -> 받는 스트레스를 HP로 더한다"""
    accs = monster_attack_accs()
    h0 = st.mean(max(0.0, min(0.95, (a - base) / 100)) for a in accs)
    h1 = st.mean(max(0.0, min(0.95, (a - base - x) / 100)) for a in accs)
    if h0 <= 0:
        return 0.0
    ref = (P['MON_HIT'] - 25) / 100
    hp_in = P['ENEMY_ACT'] * P['HITS_TAKEN'] / ref
    stress_in = (P['STRESS_TAKEN'] or 0) * P['STRESS_HP'] / ref if P.get('DODGE_STRESS', True) else 0.0
    weight = ref / max(h1, 0.05)
    return (hp_in + stress_in) * (h0 - h1) * weight * dur


def enemy_acc_value(x, P):
    """적 1명 명중 -x(점수), 1라운드 가치(HP). R-VALUE-17
    그 적의 1행동이 영웅(회피 중앙값)에게 들어갈 적중률 h0 -> h1 (몬스터 명중 분포, 0% 바닥).
    1적중 = 체력 피해(ENEMY_ACT/기준 적중률) + 스트레스(1행동 기대 스트레스 2 x STRESS_TAKEN / 기준 적중률).
    회피와 달리 유효 체력 가중은 없다: 적 1명의 명중만 내려가 파티 전체 피격률은 거의 안 변한다"""
    accs = monster_attack_accs()
    h0 = st.mean(max(0.0, min(0.95, (a - HERO_MED_DEF) / 100)) for a in accs)
    h1 = st.mean(max(0.0, min(0.95, (a - HERO_MED_DEF - x) / 100)) for a in accs)
    ref = (P['MON_HIT'] - 25) / 100
    per_hit = (P['ENEMY_ACT'] + 2 * (P['STRESS_TAKEN'] or 0) * P['STRESS_HP']) / ref
    return per_hit * (h0 - h1)


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
    return f if os.path.exists(f) else ec.vanilla_hero_file(G, hero)   # MUS-001: 편입한 총사는 RB 파일, 미편입 영웅만 원본


def load_hero(hero, mode):
    t = open(hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
    H = dict(id=hero, skills=[], crit_effects=[], modes={})
    for l in t.splitlines():
        if l.strip().startswith('//'):
            continue
        d = kv(l)
        if l.startswith('weapon:') and '_weapon_4' in l:
            H['dmg'] = (num(d['dmg'][0]), num(d['dmg'][1])); H['wcrit'] = num(d['crit'][0]); H['spd'] = num(d['spd'][0])
        elif l.startswith('armour:') and '_armour_4' in l:
            H['def'] = num(d['def'][0]); H['hp'] = num(d['hp'][0]); H['prot'] = num(first(d, 'prot', '0'))
        elif l.startswith('resistances:'):
            H['res'] = {k: num(v[0]) for k, v in d.items()}
        elif l.startswith('riposte_skill:'):
            H['riposte'] = d
        elif l.startswith('mode:'):
            H['modes'][first(d, 'id')] = d
        elif l.startswith('crit:'):
            H['crit_effects'] = ec.effect_names_in(l.replace('.effects', '.effect'))
        elif l.startswith('combat_skill:') and first(d, 'level') == '4':
            H['skills'].append((l, d))
    return H


# ---------------------------------------------------------------- 가치 계산
@functools.lru_cache(maxsize=None)
def followup_heal_amount():
    """각 영웅의 최대 단일 아군 직접 회복 평균을 1개씩 집계. 미래 회복 사용 빈도는 별도 가정이다."""
    amounts = []
    for hero in KO:
        vals = [(num(d['heal'][0]) + num(d['heal'][1])) / 2 for l, d in load_hero(hero, 'vanilla')['skills']
                if len(d.get('heal', [])) >= 2 and '@' in first(d, 'target') and '~' not in first(d, 'target')]
        if vals:
            amounts.append(max(vals))
    return st.median(amounts) * (1 + PARAM['HEAL_CRIT_SGL']) if amounts else 0.0


@functools.lru_cache(maxsize=None)
def marked_damage_bonus():
    """표식 대상 추가 직접 피해 / 표식 없는 직접 피해. MONS 동일 표본, specific_skill 기본 AI 가중치.
    표식 뒤 기술 선택 변화·열별 표적 가중치·부가 상태는 시뮬레이션하지 않는다. 추정값을 민감도로 검토한다.
    """
    eff, brains, info = _monster_db()
    base_total = bonus_total = 0.0
    for monster in MONS:
        mid = monster['name']
        if mid not in info:
            continue
        text = open(info[mid], encoding='utf-8', errors='ignore').read()
        bid = re.search(r'monster_brain:\s*\.id\s*(\S+)', text)
        weights = {}
        for desire in brains.get(bid.group(1) if bid else '', {}).get('skill_selection_desires', []):
            if desire['type'] == 'specific_skill':
                data = desire['data']; sid = data['combat_skill_id']
                weights[sid] = weights.get(sid, 0) + data.get('base_chance', 1)
        values = []
        for line in re.findall(r'^skill:.*$', text, re.M):
            d = kv(line); target = first(d, 'target'); damage = d.get('dmg', ['0'])
            if '@' in target or not re.sub('[^1-4]', '', target):
                continue
            low, high = num(damage[0]), num(damage[-1]); crit = num(first(d, 'crit')) / 100
            if first(d, 'is_crit_valid', 'true').lower() == 'false': crit = 0.0
            hit_rate = max(0.0, min(0.95, (num(first(d, 'atk')) - 25) / 100))
            amount = ((low + high) / 2 * (1 - crit) + high * 1.5 * crit) * hit_rate
            bonus = 0.0
            for name in ec.effect_names_in(line):
                e = kv(eff.get(name, ''))
                if first(e, 'target') == 'performer' and first(e, 'keyStatus') == 'tagged':
                    bonus += (num(first(e, 'damage_low_multiply')) + num(first(e, 'damage_high_multiply'))) / 200
            values.append((amount, amount * bonus, weights.get(first(d, 'id'), 0)))
        if values:
            ws = [x[2] for x in values]
            if not sum(ws): ws = [1] * len(values)
            base_total += sum(x[0] * w for x, w in zip(values, ws)) / sum(ws)
            bonus_total += sum(x[1] * w for x, w in zip(values, ws)) / sum(ws)
    return bonus_total / base_total if base_total else 0.0


def effect_duration(k, P):
    """combat_end의 duration1은 1턴이 아니다. 모델은 남은 지속 상한만 계산한다."""
    if first(k, 'buff_duration_type') == 'combat_end':
        return P['BUFF_DUR_CAP']
    return num(first(k, 'duration', str(P['DEFAULT_DUR']))) or P['DEFAULT_DUR']


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
        # 불길 역류처럼 '화상 중첩당 피해'를 쓰는 기술: 이 영웅이 건 화상이 한 라운드 뒤 남기는 중첩 (가장 큰 것)
        s.burn_left = 0
        for l, d in H['skills']:
            for n in ec.effect_names_in(l):
                k = kv(eff.get(n, ''))
                if 'dotBurn' in k and first(k, 'target') == 'target':
                    slow = any(buffs.get(b.strip('"'), {}).get('stat_type') == 'hp_dot_burn_decay_percent' for b in k.get('buff_ids', []))
                    s.burn_left = max(s.burn_left, math.floor(num(first(k, 'dotBurn')) * (P['BURN_SLOW_KEEP'] if slow else P['BURN_KEEP'])))

    def riposte(s, k):
        """반격 1회 기대 피해: 영웅의 riposte_skill 명중·피해·치명타 + 반격 효과의 피해·치명타 보정"""
        r = s.H.get('riposte', {})
        atk = num(first(r, 'atk', '85'))
        sk_dm, buf = num(first(r, 'dmg', '0')) / 100, num(first(k, 'damage_low_multiply', '0')) / 100
        mul = max(0.0, 1 + sk_dm) * (1 + buf) if s.P.get('DMG_STACK') == 'mult' else max(0.0, 1 + sk_dm + buf)
        cr = (num(first(r, 'crit', '0')) + num(first(k, 'crit_chance_add', '0')) + s.H['wcrit']) / 100
        per = ((1 - cr) * s.avg + cr * s.max * 1.5) * mul
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
        if stat == 'hp_heal_received_percent':
            packet = P['HEAL_FOLLOWUP_AMOUNT']
            if packet is None: packet = followup_heal_amount()
            return amt * packet * P['HEAL_FOLLOWUP_RATE'] * dur * P['SUPPORT_MULT']
        atk_val = s.avg * 0.8 * 0.83 if who == 'self' else P['ALLY_ATK']
        if stat in ('damage_low', 'damage_high'):
            return atk_val * amt * 0.5 * dur          # low/high 각각 절반
        if stat == 'attack_rating':
            return atk_val * amt * 100 / 82.5 * dur
        if stat == 'crit_chance':                   # 추가 피해 + 치명타 부수 효과 (R-VALUE-16)
            return (atk_val + CRIT_SIDE_HP) * amt * dur
        if stat == 'defense_rating':
            if not P.get('DODGE_EHP', True):
                return P['ENEMY_ACT'] * P['HITS_TAKEN'] * amt * 100 / 77.5 * dur
            return dodge_value(s.H['def'] if who == 'self' else HERO_MED_DEF, amt * 100, dur, P)
        if stat == 'protection_rating':
            return P['ENEMY_ACT'] * P['HITS_TAKEN'] * amt * dur
        if stat == 'speed_rating':                  # amt = 속도 점수(원값). 먼저 행동해 죽이는 적의 행동을 지운다
            h = s.H['spd'] if who == 'self' else HERO_MED_SPD
            act = formation_stats(P['STRESS_HP'])[2] if P['RANK_MODEL'] else P['ENEMY_ACT']
            return P['KILL_SHARE'] * dp_self(h, amt) * act * dur
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
            elif B.get('stat_type') == 'hp_heal_received_percent':
                v += cm * s.stat_value(B['stat_type'], B['amount'], dur, who)
            elif B.get('stat_type') in ('combat_stat_add', 'combat_stat_multiply'):
                v += cm * s.stat_value(B['stat_sub_type'], B['amount'], dur, who)
        return v


def self_mark_value(C, effects):
    """피격 재배분으로 줄인 파티 HP 피해와 표식 특효의 추가 피해를 따로 계산한다.
    공격 유도 자체는 회복/보호가 아니다. 기준 동료 회피25/방어0; 스트레스 재배분·위기 구출은 제외.
    """
    P, H = C.P, C.H
    self_effects = [kv(e) for e in effects if first(kv(e), 'target') == 'performer']
    marks = [k for k in self_effects if 'tag' in k]
    if not marks:
        return 0.0, 0.0
    mark_duration = min(P['BUFF_DUR_CAP'], max(effect_duration(k, P) for k in marks))
    mark_chance = max(min(1.0, num(first(k, 'chance', '100')) / 100) for k in marks)
    defenses = []
    for k in self_effects:
        if 'keyStatus' in k or 'monsterType' in k:
            continue
        duration = min(mark_duration, effect_duration(k, P))
        chance = min(1.0, num(first(k, 'chance', '100')) / 100)
        if 'combat_stat_buff' in k:
            defenses.append((duration, num(first(k, 'protection_rating_add')) / 100 * chance,
                             num(first(k, 'defense_rating_add')) * chance))
        for name in k.get('buff_ids', []):
            b = C.buffs.get(name.strip('"'), {})
            if b.get('stat_type') == 'combat_stat_add' and b.get('rule_type') in (None, 'always'):
                stat, amount = b.get('stat_sub_type'), b.get('amount', 0)
                defenses.append((duration, amount * chance if stat == 'protection_rating' else 0,
                                 amount * 100 * chance if stat == 'defense_rating' else 0))
    bounds = sorted({0.0, mark_duration, *(duration for duration, _, _ in defenses)})
    bonus = P['MARK_DAMAGE_BONUS']
    if bonus is None: bonus = marked_damage_bonus()
    incoming = P['ENEMY_ACT'] * P['HITS_TAKEN']
    ref_hit = max(0.05, (P['MON_HIT'] - 25) / 100)
    redirect = risk = 0.0
    for start, end in zip(bounds, bounds[1:]):
        prot = max(0.0, min(0.8, H.get('prot', 0) + sum(p for duration, p, _ in defenses if duration > start)))
        dodge = H['def'] + sum(v for duration, _, v in defenses if duration > start)
        hit_ratio = max(0.0, min(0.95, (P['MON_HIT'] - dodge) / 100)) / ref_hit
        remaining = hit_ratio * (1 - prot)
        redirect += incoming * max(0.0, P['MARK_DRAW'] - 1) * (end - start) * (1 - remaining)
        risk += incoming * P['MARK_DRAW'] * (end - start) * bonus * remaining
    return redirect * mark_chance, risk * mark_chance


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
    tranks = tuple(int(c) for c in re.sub(r'[^1-4]', '', tgt))
    if P['RANK_MODEL'] and enemy and tranks:
        tau_, mult_, act_full, _, _ = formation_stats(P['STRESS_HP'])
        rw = st.mean(mult_[r] for r in tranks) if aoe else max(mult_[r] for r in tranks)   # 단일은 가장 위협적인 열을 고른다
    else:
        rw, act_full = 1.0, P['ENEMY_ACT']
    does_dmg = enemy and dmgm > -1 and atk > 0

    # 조건부 피해 보너스 (가산, V-01 작업 가정)
    cond_bonus = 0.0
    for e in effs:
        k = kv(e)
        if first(k, 'target') == 'performer' and ('keyStatus' in k or 'monsterType' in k) and 'damage_low_multiply' in k:
            lo = num(first(k, 'damage_low_multiply')); hi = num(first(k, 'damage_high_multiply', str(lo)))
            cond_bonus += (lo + hi) / 200 * C.cond_uptime(k)

    # 화상 중첩당 피해 (불길 역류, R-VALUE-08): 대상 중첩 = 이 영웅이 건 화상이 한 라운드 뒤 남긴 수
    if 'dmg_per_burn_stack' in d:
        cond_bonus += num(first(d, 'dmg_per_burn_stack')) * C.burn_left

    # 직접 피해 (몬스터 분포 평균, 치명타 = 최대값 x 1.5)
    p_any_crit = 0.0
    if does_dmg:
        mult = (max(0.0, 1 + dmgm) * (1 + cond_bonus)) if P.get('DMG_STACK') == 'mult' else max(0.0, 1 + dmgm + cond_bonus)
        dm = ((1 - crit) * C.avg + crit * C.max * 1.5) * mult
        per = st.mean(hit(m, atk) * dm * (1 if ign_prot else 1 - m['prot']) for m in MONS)
        add('직접', per * n_t * (P['E_AOE'] if aoe else P['E_SGL']) * rw)
        ph = st.mean(hit(m, atk) for m in MONS) * crit
        p_any_crit = 1 - (1 - ph) ** n_t
        if first(d, 'copy_burn_behind').lower() == 'true' and tranks:
            # 대상 뒤 열도 맞는다(비어 있을 수 있어 광역 1칸 취급). 화상은 첫 대상에서 뒤 대상으로 옮겨질 뿐(총량 0)
            rwb = st.mean(mult_[min(4, r + 1)] for r in tranks) if P['RANK_MODEL'] else 1.0
            add('직접', per * P['AOE_PER_RANK'] * P['E_AOE'] * rwb)
            p_any_crit = 1 - (1 - ph) ** (1 + P['AOE_PER_RANK'])

    for e in effs:
        if not e:
            continue
        k = kv(e)
        who = first(k, 'target', 'target')
        chance = num(first(k, 'chance', '100'))
        if first(k, 'requires_kill_target').lower() == 'true':     # 처치했을 때만 (결투가 최후의 일격 등)
            chance *= P['KILL_ON_HIT'] * (st.mean(hit(m, atk) for m in MONS) if atk > 0 else 1)
        on_hit = first(k, 'on_hit', 'true').lower() == 'true'
        dur = effect_duration(k, P)
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
                add('기절', ev('stun') * act_full * P['STUN_MULT'] * n_t * rw)
            for key, rk, nm in (('dotBleed', 'bleed', '출혈'), ('dotPoison', 'poison', '중독')):
                if key in k:
                    per_tick = num(first(k, key))
                    cd = math.ceil(dur * P['CRIT_DOT_DUR'])
                    val = ev(rk, fn=lambda a, c: a * per_tick * (cd if c else dur))
                    add(nm, val * n_t * (P['E_DOT_AOE'] if aoe else P['E_DOT_SGL']) * rw)
            if 'dotBurn' in k:                                  # R-VALUE-08: 중첩 절반 감소, 저항 무시
                slow = any(C.buffs.get(b.strip('"'), {}).get('stat_type') == 'hp_dot_burn_decay_percent' for b in k.get('buff_ids', []))
                bt = burn_total(num(first(k, 'dotBurn')), dur if slow else 0, P)
                add('화상', ev(None, fn=lambda a, c: a * bt) * n_t * (P['E_DOT_AOE'] if aoe else P['E_DOT_SGL']) * rw)
            if 'controlled_burn_amount' in k:                   # 통제된 화상 열 효과 (빗나가도 걸림)
                zb = burn_zone(num(first(k, 'controlled_burn_amount')), num(first(k, 'controlled_burn_duration', '3')), P)
                h_ = 1.0 if first(k, 'on_miss', 'false').lower() == 'true' else st.mean(hit(m, atk) for m in MONS)
                add('화상', h_ * zb * P['E_DOT_SGL'] * rw)
            if P['RANK_MODEL'] and ('push' in k or 'pull' in k) and tranks:
                kind = 'pull' if 'pull' in k else 'push'
                mv = move_value(kind, int(num(first(k, kind))), tranks, P['STRESS_HP'], P['DEATH_RATE'], int(P['BUFF_DUR_CAP']))
                add('이동', ev('move') * mv * n_t)
            elif 'push' in k or 'shuffletarget' in k:
                add('이동', ev('move') * P['PUSH'] * n_t)
            elif 'pull' in k:
                add('이동', ev('move') * P['PULL'] * n_t)
            if P['RANK_MODEL'] and 'shuffletarget' in k and ('push' in k or 'pull' in k):
                pass
            if 'tag' in k:
                add('표식', st.mean(hit(m, atk) for m in MONS) * P['MARK_PARTY'] * n_t * rw)
            if 'kill_enemy_types' in k:
                add('시체', P['CORPSE'])
            if 'unstealth' in k:                                # R-VALUE-09: 광역이어도 가치는 은신 적 1명분
                h_ = 1.0 if aoe else st.mean(hit(m, atk) for m in MONS)
                add('은신 해제', h_ * P['DESTEALTH'])
            # 적 약화: 직접 수치(combat_stat_buff)와 강화 목록(buff_ids)·buff_type 형식을 모두 센다 (R-VALUE-12)
            mods = []                                       # (능력치, 적에게 불리한 양 x>0)
            if 'combat_stat_buff' in k:
                for key in k:
                    if key.endswith(('_add', '_multiply')):
                        x = -num(first(k, key)) / 100
                        mods.append((key.replace('_add', '').replace('_multiply', ''), x * (100 if key == 'speed_rating_add' else 1)))
            if P.get('DEBUFF_FORMATS', True):
                for b in k.get('buff_ids', []):
                    B = C.buffs.get(b.strip('"'), {})
                    if B.get('stat_type') in ('combat_stat_add', 'combat_stat_multiply'):
                        a = -B.get('amount', 0)
                        mods.append((B.get('stat_sub_type', ''), a * 100 if B.get('stat_sub_type') == 'speed_rating' else a))
                    elif B.get('stat_type') == 'crit_received_chance':
                        mods.append(('crit_received', B.get('amount', 0)))
                    elif B.get('stat_type') == 'damage_received_percent' and B.get('rule_type') in (None, 'always') and P.get('DMG_RECEIVED', True):
                        mods.append(('dmg_received', B.get('amount', 0)))   # R-VALUE-18
                    elif B.get('stat_type') == 'resistance' and P.get('RES_DEBUFF', True):      # R-VALUE-15 저항 감소
                        mods.append(('res_' + B.get('stat_sub_type', ''), -B.get('amount', 0)))
                if first(k, 'buff_type') == 'crit_received_chance':
                    a = str(first(k, 'buff_amount'))      # 게임 해석: '10%' -> 0.10, '0.08' -> 0.08 (% 없는 수는 배율)
                    mods.append(('crit_received', num(a) / 100 if a.strip('"').endswith('%') else num(a)))
            v = 0.0
            for stat, x in mods:
                if x <= 0:
                    continue
                if stat == 'speed_rating':                  # 속도 점수 원값. 적이 늦어져 먼저 죽는다
                    v += P['DEATH_RATE'] * dp_enemy(x) * act_full
                elif stat.startswith('damage_'):
                    v += P['ENEMY_ACT'] * x * 0.5
                elif stat == 'attack_rating':
                    v += enemy_acc_value(x * 100, P) if P.get('ENEMY_ACC', True) else P['ENEMY_ACT'] * x * 100 / 77.5
                elif stat == 'defense_rating':             # R-VALUE-19: 명중 105 아군 공격의 적중률 증가분 (95% 이상 자동 명중)
                    if P.get('ENEMY_DODGE_CAP', True):
                        h0 = st.mean(hit(m, 105) for m in MONS)
                        h1 = st.mean(hit(dict(m, dodge=m['dodge'] - x * 100), 105) for m in MONS)
                        v += P['ALLY_ATK'] * (h1 / h0 - 1) * P['TGT_ATTACKS']
                    else:
                        v += P['ALLY_ATK'] * x * 100 / 82.5 * P['TGT_ATTACKS']
                elif stat == 'protection_rating':          # R-VALUE-14: 방어는 0 아래로 안 내려간다 -> 적의 실제 방어만큼만
                    eff_x = st.mean(min(x, m['prot']) for m in MONS) if P.get('PROT_FLOOR', True) else x
                    v += P['ALLY_ATK'] * eff_x * P['TGT_ATTACKS']
                elif stat == 'crit_received':               # 그 적을 치는 아군 공격의 치명타 확률 +x (아군 치명타 강화와 같은 환산)
                    v += (P['ALLY_ATK'] + CRIT_SIDE_HP) * x * P['TGT_ATTACKS']    # 추가 피해 + 스트레스 회복·직업 치명타 버프 (R-VALUE-16, 19)
                elif stat == 'dmg_received':                # R-VALUE-18: 아군 1공격 피해 +x (지속 피해 제외)
                    v += P['ALLY_ATK'] * x * P['TGT_ATTACKS']
                elif stat.startswith('res_'):               # R-VALUE-15: 저항 x 감소 = 아군의 그 효과 성공률 +x (라운드당 시도 RES_ATTEMPTS회 가정)
                    succ = {'res_stun': act_full * P['STUN_MULT'],
                            'res_bleed': P['RES_DOT_HP'] * P['E_DOT_SGL'], 'res_poison': P['RES_DOT_HP'] * P['E_DOT_SGL'],
                            'res_debuff': P['RES_DEBUFF_HP'], 'res_move': P['RES_MOVE_HP']}.get(stat, 0.0)
                    v += x * P['RES_ATTEMPTS'] * succ
            if v:
                add('약화', ev('debuff') * v * min(dur, P['BUFF_DUR_CAP']) * n_t * rw)
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
            hc = P['HEAL_CRIT_SGL'] if tgt_n == 1 else P['HEAL_CRIT_AOE']   # 회복 치명타 [위키]: 2배 + 스트레스 −4
            if 'heal' in k:
                add('회복', num(first(k, 'heal')) * ch * heal_n * sm * (1 + hc))
                add('스트레스', hc * 4 * ch * heal_n * sm * P['STRESS_HP'])
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
                rd = min(dur, P['BUFF_DUR_CAP'])
                # 같은 기술이 자기 표식을 걸면 표식 지속 동안 공격을 끌어와 반격이 더 자주 터진다 (중보병 응징)
                md = 0
                for e2 in effs:
                    k2 = kv(e2)
                    if first(k2, 'target') == 'performer' and 'tag' in k2:
                        md = min(effect_duration(k2, P), rd)
                hits = P['HITS_TAKEN'] * (md * P['MARK_DRAW'] + (rd - md))
                # 반격은 빗나간 공격에도 발동한다(riposte_on_miss_chance_add 100%) -> 맞은 횟수가 아니라 받은 공격 수
                hits /= max(0.05, (P['MON_HIT'] - H['def']) / 100)
                add('반격', C.riposte(k) * hits * ch)
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
                for b in k['buff_ids']:                           # 턴당 회복 강화 (도망자 도피: 은신 중에만)
                    B = C.buffs.get(b.strip('"'), {})
                    if B.get('stat_type') == 'hp_dot_heal':
                        ticks = P['HOT_STEALTH_TICKS'] if B.get('rule_type') == 'is_stealthed' else dur
                        add('회복', B['amount'] * ticks * tgt_n * ch * P['SUPPORT_MULT'])
            if first(k, 'buff_type') == 'hp_heal_received_percent':
                add('회복 증폭', C.stat_value('hp_heal_received_percent', num(first(k, 'buff_amount')) / 100,
                                             min(dur, P['BUFF_DUR_CAP']), 'ally') * tgt_n * ch)
            if who == 'performer':                          # 자해 지속 피해(고행자 재기)는 자기 저항 적용 후 대가
                for key, rk in (('dotBleed', 'bleed'), ('dotPoison', 'poison')):
                    if key in k:
                        a = max(0.0, min(1.0, (chance - H['res'].get(rk, 0)) / 100))
                        add('대가', -num(first(k, key)) * dur * a)
            if 'stress' in k and who == 'performer':
                add('대가', -num(first(k, 'stress')) * ch * P['STRESS_HP'])
            if 'stress' in k and who in ('performer_group_other', 'performer_group'):   # 아군에게 주는 스트레스 (괴인 변신)
                add('대가', -num(first(k, 'stress')) * ch * tgt_n * P['STRESS_HP'])
    if 'heal' in d and len(d['heal']) >= 2:                  # 기술 줄의 .heal lo hi
        amt = (num(d['heal'][0]) + num(d['heal'][1])) / 2
        hn = n_t * (P['ALLY_AOE_HEAL'] if n_t > 1 else 1) if ally else 1
        hc = P['HEAL_CRIT_AOE'] if (ally and n_t > 1) else P['HEAL_CRIT_SGL']
        add('회복', amt * hn * P['SUPPORT_MULT'] * (1 + hc))
        add('스트레스', hc * 4 * hn * P['SUPPORT_MULT'] * P['STRESS_HP'])

    # 치명타 부수 효과: 스트레스 회복 + 직업 버프 2턴. 광역도 1회만 (R-CMB-08)
    if p_any_crit > 0:
        cb = sum(C.buff_ids_value(kv(C.eff.get(n, '')).get('buff_ids', []), P['CRIT_BUFF_DUR'], 'self')
                 for n in H['crit_effects'])
        add('치명타', p_any_crit * (P['CRIT_STRESS'] * P['STRESS_HP'] + cb))

    redirect, mark_risk = self_mark_value(C, effs)
    add('공격 유도', redirect)
    add('표식 위험', -mark_risk)
    tot = sum(parts.values())
    if limit:
        tot *= min(1.0, limit / 3)
    if first(d, 'requires_burning').lower() == 'true':      # 화상 걸린 대상이 있어야 쓸 수 있다: 자기 상태 조건 유지율
        tot *= P['COND_SELF']
    if 'required_performer_hp_range' in d:
        tot *= P['LOW_HP_SELF'] if C.self_wound else P['LOW_HP_OTHER']
    return tot, parts


PARAM_MED_HP = 43.0      # evaluate()에서 바닐라 5레벨 체력 중앙값으로 덮어쓴다
HERO_MED_SPD = 7.0
HERO_MED_DEF = 25.0     # evaluate()에서 바닐라 5레벨 영웅 회피 중앙값으로 덮어쓴다
CRIT_SIDE_HP = 0.0      # evaluate()에서 계산: 아군 치명타 1회의 부수 효과 = 스트레스 회복 + 직업 치명타 버프 중앙값 (R-VALUE-16)
_STRESS_CACHE = None


def mode_plans(C, H, sk, P):
    """R-VALUE-10. 전환 기술(여러 모드 + 전투당 제한)이 있는 영웅은 모드마다 따로 센다.
    모드 m 행동 가치 = m에서 쓸 수 있는 기술 상위 ACT_TOP 평균
                      + (기본 모드가 아니면) [전환 꾸러미 + 전투 끝 복귀 꾸러미 - 모드 턴당 스트레스 x 지속 상한] / FIGHT_ACTS.
    반환 {모드: (행동 가치 HP, 설명)}. 해당 없으면 {}."""
    sw = [(l, d) for l, d in H['skills'] if 'per_battle_limit' in d and len(d.get('valid_modes', [])) > 1
          and any(k.endswith('_effects') and k[:-8] in H['modes'] for k in d)]
    if not sw or not H['modes']:
        return {}
    l, d = sw[0]
    sid = first(d, 'id')
    default = next((m for m, md in H['modes'].items() if first(md, 'is_raid_default') == 'true'), next(iter(H['modes'])))

    def pkg(mode_from):
        lst = d.get(mode_from + '_effects', [])
        if not lst:
            return 0.0, {}
        base = re.sub(r'\.\w+_effects(\s+(?!\.)\S+)*', '', l)
        base = re.sub(r'\.per_battle_limit\s+\S+', '', base)
        line = base + ' .effect ' + ' '.join('"%s"' % x.strip('"') for x in lst)
        return skill_value(C, line, kv(line))

    out = {}
    for m, md in H['modes'].items():
        usable = [s for s, (v, parts, la) in sk.items() if s != sid and m in skill_modes(H, s)]
        if not usable:
            continue
        top = sorted((sk[s][0] for s in usable), reverse=True)[:P['ACT_TOP']]
        v = st.mean(top)
        note = '+'.join(sorted(usable, key=lambda s: -sk[s][0])[:P['ACT_TOP']])
        if m != default:
            go, _ = pkg(default)
            back, _ = pkg(m)
            mode_stress = num(first(md, 'stress_damage_per_turn', '0')) * P['BUFF_DUR_CAP'] * P['STRESS_HP']
            once = go + back - mode_stress
            v += once / P['FIGHT_ACTS']
            note += ' / 전환 1회 %+.1f HP (전환 %+.1f, 복귀 %+.1f, 모드 스트레스 %+.1f)' % (once, go, back, -mode_stress)
        out[m] = (v, note)
    return out


def skill_modes(H, sid):
    for l, d in H['skills']:
        if first(d, 'id') == sid:
            return d.get('valid_modes', list(H['modes']))
    return []


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


def affliction_margin(P=PARAM, sh0=None):
    """R-VALUE-06 개정(2026-10-03). 스트레스 1점이 고통(붕괴)·미덕 판정으로 더하는 HP. 고통 7종·미덕 5종을 효과별로 센다.
    고통 1회(라운드당 x AFFLICT_ROUNDS): 비아냥 스트레스(턴 시작 + 사건 반응 x masterBarkChance, 1회 +6)
      + 행동 손실(명령 무시·임의 명령·자리 이탈) x 영웅 1행동 + 아군 공격·자기 공격·자기 표식 + 능력치 변화 + 회복·강화·이동 거부.
    미덕 1회: 턴 시작 행동 25%(스트레스 회복 15 / 파티 4 / 아군 강화 / 파티 피해 +15% / 자기 회복 10%) + 능력치 + 스트레스 100 -> 45.
    스트레스 1점 = (고통 확률 x 고통 비용 - 미덕 확률 x 미덕 이득) / 100. 반환 (스트레스 1점 HP, 고통 평균, 미덕 평균)."""
    sh0 = sh0 or stress_price_ratio()[0]
    rules = json.load(open(os.path.join(G, 'shared', 'rules.json'), encoding='utf-8-sig'))
    master = rules.get('masterBarkChance', 0.5)
    buffs = ec.load_buffs(G)
    d = json.loads(re.sub(r',\s*([}\]])', r'\1', open(os.path.join(G, 'shared', 'trait', 'trait_library.json'), encoding='utf-8-sig').read()))
    std, hero_act, hp_med = 7.65, 13.2, PARAM_MED_HP          # 표준 평타·영웅 1행동(바닐라 중앙)·체력 중앙
    hit_on_me = P['HITS_TAKEN']; att_on_me = hit_on_me / ((P['MON_HIT'] - 25) / 100)
    ev = dict(comment_self_hit=hit_on_me, comment_self_missed=att_on_me - hit_on_me, comment_ally_hit=3 * hit_on_me,
              comment_ally_missed=3 * (att_on_me - hit_on_me), comment_ally_attack_hit=2.25, comment_ally_attack_missed=0.75, comment_move=0.3)

    def bf(tr):
        o = {}
        for b in tr.get('buff_ids', []):
            x = buffs.get(b, {}); k = x.get('stat_sub_type') or x.get('stat_type')
            o[k] = o.get(k, 0) + x.get('amount', 0)
        return o
    aff, vir = [], []
    for tr in d['traits']:
        ao = [a for a in tr.get('combat_start_turn_act_outs', []) if a.get('chance', 0) > 0 and 'valid_hero_class_ids' not in a]
        b = bf(tr)
        if tr['overstress_type'] == 'affliction' and tr['id'] != 'test':
            af = [a['chance'] for a in tr['combat_start_turn_act_outs'] if a.get('id') == 'attack_friendly' and a.get('chance', 0) > 0]
            afw = st.mean(af) if af else 0
            tot = sum(a['chance'] for a in ao) + afw
            p = lambda ids: sum(a['chance'] for a in ao if a['id'] in ids) / tot
            re_ = {o['id']: o['chance'] for o in tr.get('reaction_act_outs', []) if o.get('chance', 0) > 0}
            # 비아냥 범위(나무위키, 엔진 규칙 V-14): 고통 영웅 자신의 돌발 행동·피격에서 나오면 파티 전체(자신 제외 3명),
            # 다른 영웅의 행동에 반응한 것이면 그 영웅 1명
            own = ('comment_self_hit', 'comment_self_missed')
            bark = (3 * (p(('bark_stress',)) + sum(ev.get(k, 0) * c * master for k, c in re_.items() if k in own))
                    + sum(ev.get(k, 0) * c * master for k, c in re_.items() if k.startswith('comment_') and k not in own))
            dmg = (b.get('damage_low', 0) + b.get('damage_high', 0)) / 2
            per = (bark * 6 * sh0 + p(('ignore_command', 'random_command', 'change_pos', 'retreat_from_combat')) * hero_act
                   + afw / tot * (hero_act + std) + p(('attack_self',)) * 0.1 * hp_med + p(('mark_self',)) * (P['MARK_DRAW'] - 1) * hit_on_me * 8
                   - dmg * std * 0.75 - b.get('attack_rating', 0) * std - b.get('defense_rating', 0) * P['ENEMY_ACT'] * hit_on_me * 100 / 77.5
                   - b.get('speed_rating', 0) * 0.3 + 0.1 * P['ENEMY_ACT'] * hit_on_me * 0.5
                   + re_.get('block_heal', 0) * 0.35 * 6 + re_.get('block_buff', 0) * 0.6 + re_.get('block_move', 0) * 0.1 * hero_act)
            aff.append(per * P['AFFLICT_ROUNDS'])
        elif tr['overstress_type'] == 'virtue':
            tot = sum(a['chance'] for a in ao)
            av = dict(stress_heal_self=15 * sh0, stress_heal_party=4 * 4 * sh0 * 0.7, buff_random_party_member=(10 / 77.5 + 0.10) * std,
                      buff_party=0.15 * std * 0.75 * 4, heal_self=0.1 * hp_med)
            dmg = (b.get('damage_low', 0) + b.get('damage_high', 0)) / 2
            per = (sum(a['chance'] / tot * av.get(a['id'], 0) for a in ao) + dmg * std * 0.75 + b.get('attack_rating', 0) * std
                   + b.get('crit_chance', 0) * std + (b.get('protection_rating', 0) + b.get('defense_rating', 0)) * P['ENEMY_ACT'] * hit_on_me
                   + b.get('speed_rating', 0) * 0.3 + 0.25 * P['ENEMY_ACT'] * 0.3 - b.get('stress_dmg_received_percent', 0) * 1.68 * sh0)
            vir.append(per * P['AFFLICT_ROUNDS'] + (100 - rules['stress_affliction_critically_resisted']) * sh0)
    pa = rules['affliction_base_onset_chance']
    ca, cv = st.mean(aff), st.mean(vir)
    return (pa * ca - (1 - pa) * cv) / 100, ca, cv


def stress_value(P=PARAM):
    sh0 = stress_price_ratio()[0]
    return sh0 + affliction_margin(P, sh0)[0]


def stress_hp(mode):
    hps = [load_hero(h, mode)['hp'] for h in KO]
    return st.median(hps) / 100


def evaluate(mode, P=PARAM):
    global PARAM_MED_HP, HERO_MED_SPD, HERO_MED_DEF, CRIT_SIDE_HP, _STRESS_CACHE
    PARAM_MED_HP = stress_hp('vanilla') * 100
    HERO_MED_SPD = st.median(load_hero(h, 'vanilla')['spd'] for h in KO)
    HERO_MED_DEF = st.median(load_hero(h, 'vanilla')['def'] for h in KO)
    if P['STRESS_TAKEN'] is None:
        if _STRESS_CACHE is None:
            _STRESS_CACHE = 2 * monster_stress_per_action() / 4
        P = dict(P, STRESS_TAKEN=_STRESS_CACHE)
    if P['STRESS_HP'] is None:
        P = dict(P, STRESS_HP=stress_value(P))             # R-VALUE-06 가격 비율 + 고통 비용
    if P['HEAL_FOLLOWUP_AMOUNT'] is None:
        P = dict(P, HEAL_FOLLOWUP_AMOUNT=followup_heal_amount())
    if P['MARK_DAMAGE_BONUS'] is None:
        P = dict(P, MARK_DAMAGE_BONUS=marked_damage_bonus())
    eff = load_effects(mode)
    buffs = ec.load_buffs(G, M_ROOT if mode == 'rb' else None)
    CRIT_SIDE_HP = 0.0
    if P.get('CRIT_SIDE', True):                           # R-VALUE-16: 치명타 1회 부수 효과 (영웅별 직업 버프는 중앙값)
        cbs = []
        for h in KO:
            Hh = load_hero(h, mode)
            Ch = Ctx(Hh, eff, buffs, P)
            cbs.append(sum(Ch.buff_ids_value(kv(eff.get(n, '')).get('buff_ids', []), P['CRIT_BUFF_DUR'], 'self')
                           for n in Hh['crit_effects']))
        CRIT_SIDE_HP = P['CRIT_STRESS'] * P['STRESS_HP'] + st.median(cbs)
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
        # R-VALUE-11 무료 행동: 모드 전환 기술(전투당 제한 + 여러 모드)은 mode_plans가 따로 센다
        free = {first(d, 'id') for l, d in H['skills'] if first(d, 'is_continue_turn') == 'true'
                and not ('per_battle_limit' in d and len(d.get('valid_modes', [])) > 1)} if P.get('FREE_ACTION') else set()
        vals = sorted((v[0] for s, v in sk.items() if s not in free), reverse=True)
        act = st.mean(vals[:P['ACT_TOP']])
        plans = mode_plans(C, H, {s: v for s, v in sk.items() if s not in free}, P)
        if plans:
            act = max(v for v, _ in plans.values())
        free_bonus = sum(max(0.0, sk[s][0]) / P['BUFF_DUR_CAP'] for s in free)
        act += free_bonus
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
        out[hero] = dict(act=act, free=free_bonus, surv=surv, spd=H['spd'], flex=opt + 0.5 * sub, base=base, skills=sk, rank_pts=rank_pts, plans=plans)
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
    print(f'몬스터 모집단: 영웅 등급 일반 몬스터 {N_MON}종 (보스·오브젝트 제외) / 스트레스 1 = HP {stress_value():.2f} (가격 비율 {stress_price_ratio()[0]:.2f} + 고통 비용, R-VALUE-06)\n')
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
            for m, (v, note) in r.get('plans', {}).items():
                print(f'  [모드 {m}] 행동 가치 {pp(v, std):+.0f}%p (표준 평타 기준)  {note}')
    if a.sens:
        variants = {'스트레스=HP 1.22(가격만)': dict(STRESS_HP=1.22), '스트레스=HP 1(v1)': dict(STRESS_HP=1.0), '기절 x1.3': dict(STUN_MULT=1.3), '지원 x0.7': dict(SUPPORT_MULT=0.7),
                    '광역 직접 0.75': dict(E_AOE=0.75), '조건 유지율 0.45/0.2': dict(COND_SELF=0.45, COND_OTHER=0.2),
                    '저체력 조건 0.3': dict(LOW_HP_SELF=0.3), '화상 감소 약화 무시(V-12)': dict(BURN_SLOW_KEEP=0.5),
                    '피해 보정 가산(V-01 이전)': dict(DMG_STACK='add'),
                    '열 모델 끔(이전)': dict(RANK_MODEL=False),
                    '후속 회복 없음': dict(HEAL_FOLLOWUP_RATE=0.0), '후속 회복 1회/라운드': dict(HEAL_FOLLOWUP_RATE=1.0),
                    '표식 유도 없음': dict(MARK_DRAW=1.0), '표식 특효 비용 없음': dict(MARK_DAMAGE_BONUS=0.0)}
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
