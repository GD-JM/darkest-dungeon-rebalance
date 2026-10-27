"""약화 전수 조사 (2026-10-27): 영웅 20명 모든 기술(반격 포함)·1~5렙의 적 대상 약화, 영웅별 약화 확률 장신구,
몬스터가 영웅에게 거는 약화 종류, 엔진 buff 종류 중 영웅 약화로 아직 배분되지 않은 것.
목적: 약화 분포 평준화 + 미배분 약화로 겹친 약화를 바꿔 다양화 (제작자 10-27 요청).
현재 작업 트리 기준(게임이 실제로 읽는 파일). 출력: design/analysis/debuff_survey.md (+ .json)
사용: python tools/debuff_survey.py"""
import os, re, glob, json, sys, collections, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
import strength as S
ec = S.ec; G = S.G; M = S.M_ROOT
E = S.load_effects('rb')
B = ec.load_buffs(G, M)

# 한국어 기술 이름 (바닐라 -> RB 덮어쓰기)
KO = {}
for f in glob.glob(os.path.join(G, 'localization', '*.string_table.xml')) + glob.glob(os.path.join(G, 'dlc', '**', 'localization', '*.string_table.xml'), recursive=True) \
        + sorted(glob.glob(os.path.join(M, 'localization', '*.string_table.xml'))):
    if 'arena' in f:
        continue
    t = open(f, 'rb').read().decode('utf-8', 'ignore')
    m = re.search(r'<language id="koreana">(.*?)</language>', t, re.S)
    if m:
        for k, v in re.findall(r'<entry id="combat_skill_name_(\w+?)"><!\[CDATA\[(.*?)\]\]>', m.group(1)):
            KO[k] = v

STAT = {'attack_rating': '명중', 'defense_rating': '회피', 'protection_rating': '방어', 'speed_rating': '속도',
        'damage_low': '피해', 'damage_high': '피해', 'crit_chance': '치명타', 'max_hp': '최대 체력'}
RES = {'stun': '기절 저항', 'poison': '중독 저항', 'bleed': '출혈 저항', 'debuff': '약화 저항', 'move': '이동 저항',
       'disease': '질병 저항', 'death_blow': '죽음의 일격 저항', 'trap': '함정 저항'}
# 수치가 커지면 대상에게 나쁜 종류 (나머지는 작아져야 약화)
UP_BAD = {'damage_received_percent': '받는 피해', 'crit_received_chance': '받는 치명타', 'stress_dmg_received_percent': '받는 스트레스',
          'random_target_attack_chance': '무작위 대상 공격', 'tag_blocked': None,
          'hp_dot_burn_decay_percent': '화상 감소 둔화', 'hp_dot_poison_duration_percent': '중독 지속 증가'}
DOWN_BAD = {'hp_heal_received_percent': '받는 회복', 'stress_heal_received_percent': '받는 스트레스 회복', 'hp_heal_percent': '주는 회복',
            'stun_chance': '기절 확률', 'bleed_chance': '출혈 확률', 'poison_chance': '중독 확률', 'debuff_chance': '약화 확률',
            'move_chance': '이동 확률', 'stress_dmg_percent': '주는 스트레스', 'ignore_protection': '방어 무시',
            'damage_reflect_percent': '피해 반사', 'guard_duration_percent': '보호 지속'}
FLAG = {'disable_combat_skill_attribute': '기술 봉인', 'guard_blocked': '보호 불가', 'tag_blocked': '표식 불가'}
NAME = {**UP_BAD, **DOWN_BAD}


def val(a, pct):
    return float(str(a).rstrip('%')) if str(a).endswith('%') or not pct else float(a) * 100


def debuffs(line):
    """효과 한 줄 -> [(범주, 수치)] 대상에게 불리한 것만. 수치는 원값(명중·회피·속도는 점, 나머지 %)."""
    out = []
    if 'combat_stat_buff' in line:
        for k, nm in STAT.items():
            for m in re.finditer(r'\.' + k + r'_(add|multiply)\s+(-?[\d.]+%?)', line):
                v = float(m.group(2).rstrip('%'))
                if v < 0 and not (k == 'damage_high' and any(c == '피해' for c, _ in out)):
                    out.append((nm, v))
    m = re.search(r'\.buff_type\s+(\w+)\s+\.buff_amount\s+(\S+)', line)
    if m:
        t, a = m.group(1), m.group(2)
        v = float(a.rstrip('%')) if a.endswith('%') else float(a) * 100
        if (t in UP_BAD and v > 0) or (t in DOWN_BAD and v < 0):
            out.append((NAME[t], v))
    bm = re.search(r'\.buff_ids\s+(.*?)(?=\s\.[a-z_]+|$)', line)
    for a, b in (re.findall(r'"([^"]+)"|(\S+)', bm.group(1)) if bm else []):
        bf = B.get(a or b)
        if not bf:
            continue
        st_, sub, amt = bf['stat_type'], bf.get('stat_sub_type', ''), bf.get('amount', 0)
        cond = '*' if bf.get('rule_type') not in (None, 'always') else ''
        if st_ in ('combat_stat_add', 'combat_stat_multiply') and sub in STAT and amt < 0:
            if not (sub == 'damage_high' and any(c.startswith('피해') for c, _ in out)):
                out.append((STAT[sub] + cond, amt if sub in ('speed_rating',) else amt * 100))
        elif st_ == 'resistance' and amt < 0:
            out.append((RES.get(sub, sub + ' 저항') + cond, amt * 100))
        elif (st_ in UP_BAD and amt > 0 and UP_BAD[st_]) or (st_ in DOWN_BAD and amt < 0):
            out.append((NAME[st_] + cond, amt * 100))
        elif st_ in FLAG:
            out.append((FLAG[st_] + (':' + sub if sub else '') + cond, 0))
    return out


def chance(line):
    m = re.search(r'\.chance\s+(-?\d+)%', line)
    return int(m.group(1)) if m else 100


def duration(line):
    m = re.search(r'\.duration\s+(\d+)', line)
    return int(m.group(1)) if m else None


def skill_lines(text):
    for l in text.splitlines():
        m = re.match(r'(combat_skill|riposte_skill):\s*\.id\s+"(\w+)"\s+\.level\s+(\d)(.*)', l.strip())
        if m:
            yield m.group(1), m.group(2), int(m.group(3)), m.group(4), l


def target_side(rest):
    tg = re.search(r'\.target\s+(\S*)', rest)
    tg = tg.group(1) if tg else ''
    if not tg or tg.startswith('.') or '@' in tg:
        return None, tg
    return ('광역' if '~' in tg else '단일'), tg


# ---- 영웅 기술 ----
def scan(mode):
    global E
    E = S.load_effects(mode)
    rows = []
    for hero in S.KO:
        text = open(S.hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
        for kind, sid, lv, rest, raw in skill_lines(text):
            side, tg = target_side(rest)
            if side is None:
                continue
            launch = (re.search(r'\.launch\s+(\d+)', rest) or [None, ''])[1] if re.search(r'\.launch\s+(\d+)', rest) else ''
            for n in ec.effect_names_in(raw):
                line = E.get(n)
                if not line or not re.search(r'\.target\s+"target"', line):
                    continue
                if 'bsrc_crit' in line or '.keyStatus' in line or '.monsterType' in line:
                    continue   # 치명타 전용·조건부 추가 피해는 약화가 아님
                for cat, v in debuffs(line):
                    rows.append(dict(hero=hero, hero_ko=S.KO[hero], kind=kind, skill=sid, skill_ko=KO.get(hero + '_' + sid, sid),
                                     level=lv, side=side, target=tg, launch=launch, cat=cat, val=round(v, 1),
                                     chance=chance(line), dur=duration(line), eff=n,
                                     riposte='riposte' in kind))
    return rows


VAN = scan('vanilla')
rows = scan('rb')

# ---- 몬스터 (영웅에게 거는 약화) ----
mon = collections.defaultdict(set)
mfiles = glob.glob(os.path.join(G, 'monsters', '*', '*', '*.info.darkest')) + glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*.info.darkest'), recursive=True)
for f in mfiles:
    if 'arena' in f:
        continue
    mid = os.path.basename(f).split('.')[0]
    for raw in open(f, encoding='utf-8', errors='ignore').read().splitlines():
        if not raw.startswith('skill:'):   # 몬스터 기술은 'skill:' 줄, 레벨 없음
            continue
        side, tg = target_side(raw)
        if side is None:
            continue
        for n in ec.effect_names_in(raw):
            line = E.get(n)
            if line and re.search(r'\.target\s+"target"', line):
                for cat, v in debuffs(line):
                    mon[cat.rstrip('*')].add(re.sub(r'_[A-F]$', '', mid))

# ---- 장신구: 영웅 전용 약화 확률 ----
tr = collections.defaultdict(list)
tfiles = [os.path.join(G, 'trinkets', 'base.entries.trinkets.json')] + glob.glob(os.path.join(G, 'dlc', '**', 'trinkets', '*.entries.trinkets.json'), recursive=True) \
    + glob.glob(os.path.join(M, 'trinkets', '*.entries.trinkets.json'))
for f in tfiles:
    if 'arena' in f:
        continue
    for t in json.load(open(f, encoding='utf-8-sig')).get('entries', []):
        for bid in t.get('buffs', []):
            bf = B.get(bid)
            if bf and bf['stat_type'] == 'debuff_chance' and bf.get('amount', 0) > 0:
                for h in t.get('hero_class_requirements') or ['(공용)']:
                    tr[h].append((t['id'], round(bf['amount'] * 100), t.get('rarity', '')))

# ---- 엔진 buff 종류 전체 (영웅 약화로 쓸 수 있는 후보) ----
engine = collections.Counter()
for bf in B.values():
    st_, sub = bf['stat_type'], bf.get('stat_sub_type', '')
    if st_ == 'resistance':
        engine[RES.get(sub, sub + ' 저항')] += 1
    elif st_ in ('combat_stat_add', 'combat_stat_multiply') and sub in STAT:
        engine[STAT[sub]] += 1
    elif st_ in NAME and NAME[st_]:
        engine[NAME[st_]] += 1
    elif st_ in FLAG:
        engine[FLAG[st_] + (':' + sub if sub else '')] += 1

json.dump(dict(rows=rows, monsters={k: sorted(v) for k, v in mon.items()}, trinkets=tr, engine=engine),
          open(os.path.join(M, 'design', 'analysis', 'debuff_survey.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- 표 ----
def fmt(vals, unit):
    vs = [vals.get(l) for l in range(5)]
    vs = [v for v in vs if v is not None]
    if not vs:
        return ''
    s = lambda x: ('%g' % x) + unit
    return s(vs[0]) if len(set(vs)) == 1 else s(vs[0]) + '→' + s(vs[-1])

UNIT = lambda c: '' if c.rstrip('*') in ('명중', '회피', '속도') else '%'
skills = collections.OrderedDict()   # (hero, skill, cat) -> {level: (val, chance, dur, side)}
for r in rows:
    skills.setdefault((r['hero'], r['skill'], r['cat']), {})[r['level']] = r

by_cat = collections.defaultdict(list)
for (h, sid, cat), lv in skills.items():
    r0 = lv[min(lv)]
    by_cat[cat.rstrip('*')].append(dict(hero=h, hero_ko=r0['hero_ko'], skill_ko=r0['skill_ko'] + (' (반격)' if r0['riposte'] else ''), side=r0['side'],
                                         cond=cat.endswith('*'),
                                         val=fmt({l: x['val'] for l, x in lv.items()}, UNIT(cat)),
                                         ch=fmt({l: x['chance'] for l, x in lv.items()}, '%'),
                                         dur=fmt({l: x['dur'] for l, x in lv.items() if x['dur'] is not None}, '턴') or '기본',
                                         target=r0['target']))

head = subprocess.run(['git', 'log', '--oneline', '-1'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
dirty = subprocess.run(['git', 'status', '--short', '--', 'heroes', 'effects', 'shared'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
L = ['# 약화 전수 조사', '',
     f'- 생성: {datetime.date.today()} `python tools/debuff_survey.py` / 브랜치 `{branch}` / {head}' + (' / **커밋 안 된 게임 데이터 변경 포함(작업 트리 기준)**' if dirty else ''),
     '- 범위: 영웅 20명 모든 전투 기술·반격, 1~5렙. 적에게 거는 약화만(능력치 감소, 저항 감소, 받는 피해·치명타 증가 등). 출혈·중독·기절·이동·표식은 약화가 아니라 제외. 치명타 전용 효과·조건부 추가 피해 제외.',
     '- 수치는 1렙→5렙. 명중·회피·속도는 점, 나머지는 %. 확률은 효과 기본 확률(적 약화 저항 차감 전). `*` = 조건부 버프(rule).', '']

van = collections.defaultdict(set)
for r in VAN:
    van[r['cat'].rstrip('*')].add((r['hero'], r['skill']))
L += ['## 1. 범주별 분포 (바닐라 → 현재)', '', '| 약화 | 기술 수 (바닐라→현재) | 영웅 수 | 몬스터 사용 | 엔진 buff 수 |', '|---|---|---|---|---|']
cats = sorted(set(by_cat) | set(mon) | set(van), key=lambda c: (-len(by_cat.get(c, [])), c))
for c in cats:
    lst = by_cat.get(c, [])
    L.append(f'| {c} | {len(van.get(c, ()))}→{len(lst)} | {len({x["hero"] for x in lst})} | {len(mon.get(c, ()))} | {engine.get(c, 0)} |')
L += ['']

L += ['## 2. 범주별 상세', '']
for c in cats:
    lst = by_cat.get(c)
    if not lst:
        continue
    L += [f'### {c} ({len(lst)}개 기술, {len({x["hero"] for x in lst})}명)', '', '| 영웅 | 기술 | 대상 | 수치 | 확률 | 지속 |', '|---|---|---|---|---|---|']
    for x in sorted(lst, key=lambda x: x['hero_ko']):
        L.append(f'| {x["hero_ko"]} | {x["skill_ko"]}{" *" if x["cond"] else ""} | {x["side"]} {x["target"]} | {x["val"]} | {x["ch"]} | {x["dur"]} |')
    L += ['']

L += ['## 3. 영웅별', '', '| 영웅 | 약화 기술 수 | 약화 범주 | 전용 약화 확률 장신구 |', '|---|---|---|---|']
for h, ko in S.KO.items():
    sk = {sid for (hh, sid, _) in skills if hh == h}
    cs = sorted({c.rstrip('*') for (hh, _, c) in skills if hh == h})
    tl = ', '.join(f'{t} +{a}%' for t, a, _ in tr.get(h, []))
    L.append(f'| {ko} | {len(sk)} | {", ".join(cs) or "-"} | {tl or "-"} |')
L += ['', f'공용 약화 확률 장신구: {", ".join(f"{t} +{a}% ({r})" for t, a, r in tr.get("(공용)", [])) or "-"}', '']

unused = [c for c in sorted(set(mon) | set(engine)) if c not in by_cat]
L += ['## 4. 영웅이 아직 쓰지 않는 약화 (배분 후보)', '', '몬스터가 영웅에게 쓰거나 엔진 buff로 존재하지만 영웅 기술에는 없는 종류. 몬스터에게 실제로 작동하는지는 종류별 게임 검증 필요(질병·함정·죽음의 일격 저항, 받는 스트레스는 영웅 전용 수치라 제외 후보).', '',
      '| 약화 | 몬스터 사용 | 엔진 buff 수 | 사용 몬스터 예 |', '|---|---|---|---|']
for c in unused:
    L.append(f'| {c} | {len(mon.get(c, ()))} | {engine.get(c, 0)} | {", ".join(sorted(mon.get(c, ()))[:5])} |')
open(os.path.join(M, 'design', 'analysis', 'debuff_survey.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
