"""강화(버프) 전수 조사 (2026-10-27): 영웅 20명 모든 기술(반격 포함)·1~5렙의 아군·자신 강화를 범주별(바닐라→현재)로.
약화 전수 조사(tools/debuff_survey.py)와 같은 형식. 출력: design/analysis/buff_survey.md (+ .json)
사용: python tools/buff_survey.py"""
import os, re, glob, json, sys, collections, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
import strength as S
ec = S.ec; G = S.G; M = S.M_ROOT
B = ec.load_buffs(G, M)

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
# 수치가 작아져야 좋은 종류 (나머지는 커져야 강화)
DOWN_GOOD = {'damage_received_percent': '받는 피해 감소', 'crit_received_chance': '받는 치명타 감소', 'stress_dmg_received_percent': '받는 스트레스 감소'}
UP_GOOD = {'hp_heal_received_percent': '받는 회복', 'stress_heal_received_percent': '받는 스트레스 회복', 'hp_heal_percent': '주는 회복',
           'stun_chance': '기절 확률', 'bleed_chance': '출혈 확률', 'poison_chance': '중독 확률', 'debuff_chance': '약화 확률',
           'move_chance': '이동 확률', 'ignore_protection': '방어 무시', 'damage_reflect_percent': '피해 반사',
           'stress_heal_percent': '주는 스트레스 회복', 'hp_dot_burn_amount_percent': '화상 피해', 'stealth': '은신',
           'guard_duration_percent': '보호 지속'}
NAME = {**DOWN_GOOD, **UP_GOOD}


def buffs(line):
    """효과 한 줄 -> [(범주, 수치)] 받는 쪽에게 유리한 것만."""
    out = []
    if 'combat_stat_buff' in line:
        for k, nm in STAT.items():
            for m in re.finditer(r'\.' + k + r'_(add|multiply)\s+(-?[\d.]+%?)', line):
                v = float(m.group(2).rstrip('%'))
                if v > 0 and not (k == 'damage_high' and any(c == '피해' for c, _ in out)):
                    out.append((nm, v))
    m = re.search(r'\.buff_type\s+(\w+)\s+\.buff_amount\s+(\S+)', line)
    if m:
        t, a = m.group(1), m.group(2)
        v = float(a.rstrip('%')) if a.endswith('%') else float(a) * 100
        if (t in DOWN_GOOD and v < 0) or (t in UP_GOOD and v > 0):
            out.append((NAME[t], v))
    bm = re.search(r'\.buff_ids\s+(.*?)(?=\s\.[a-z_]+|$)', line)
    for a, b in (re.findall(r'"([^"]+)"|(\S+)', bm.group(1)) if bm else []):
        bf = B.get(a or b)
        if not bf:
            continue
        st_, sub, amt = bf['stat_type'], bf.get('stat_sub_type', ''), bf.get('amount', 0)
        cond = '*' if bf.get('rule_type') not in (None, 'always') else ''
        if st_ in ('combat_stat_add', 'combat_stat_multiply') and sub in STAT and amt > 0:
            if not (sub == 'damage_high' and any(c.startswith('피해') for c, _ in out)):
                out.append((STAT[sub] + cond, amt if sub == 'speed_rating' else amt * 100))
        elif st_ == 'resistance' and amt > 0:
            out.append((RES.get(sub, sub + ' 저항') + cond, amt * 100))
        elif (st_ in DOWN_GOOD and amt < 0) or (st_ in UP_GOOD and amt > 0):
            out.append((NAME[st_] + cond, amt * 100))
    if re.search(r'\.riposte\s+1', line):
        out.append(('반격', 0))
    if re.search(r'\.guard\s+1', line):
        out.append(('보호', 0))
    return out


chance = lambda l: int(re.search(r'\.chance\s+(-?\d+)%', l).group(1)) if re.search(r'\.chance\s+(-?\d+)%', l) else 100
duration = lambda l: int(re.search(r'\.duration\s+(\d+)', l).group(1)) if re.search(r'\.duration\s+(\d+)', l) else None


def skill_lines(text):
    for l in text.splitlines():
        m = re.match(r'(combat_skill|riposte_skill):\s*\.id\s+"(\w+)"\s+\.level\s+(\d)(.*)', l.strip())
        if m:
            yield m.group(1), m.group(2), int(m.group(3)), m.group(4), l


def receiver(eff_target, skill_target):
    """효과를 받는 쪽: 자신 / 아군 1명 / 아군 전체. 적이 받으면 None."""
    if eff_target == 'performer':
        return '자신'
    if eff_target in ('performer_group', 'performer_group_other', 'global'):
        return '아군 전체'
    if eff_target == 'target':
        if not skill_target or skill_target.startswith('.'):
            return '자신'
        if '@' in skill_target:
            return '아군 전체' if '~' in skill_target else '아군 1명'
    return None


def scan(mode):
    E = S.load_effects(mode)
    rows = []
    for hero in S.KO:
        text = open(S.hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
        for kind, sid, lv, rest, raw in skill_lines(text):
            tg = re.search(r'\.target\s+(\S*)', rest)
            tg = tg.group(1) if tg else ''
            for n in ec.effect_names_in(raw):
                line = E.get(n)
                if not line or 'bsrc_crit' in line:
                    continue   # 치명타 전용 강화 제외
                et = re.search(r'\.target\s+"(\w+)"', line)
                side = receiver(et.group(1) if et else '', tg)
                if side is None:
                    continue
                cond = '.keyStatus' in line or '.monsterType' in line   # 표식·종족 대상 조건부 추가 피해
                for cat, v in buffs(line):
                    rows.append(dict(hero=hero, hero_ko=S.KO[hero], skill=sid, skill_ko=KO.get(hero + '_' + sid, sid) + (' (반격)' if kind == 'riposte_skill' else ''),
                                     level=lv, side=side, cat=('조건부 ' if cond else '') + cat, val=round(v, 1),
                                     chance=chance(line), dur=duration(line), eff=n))
    return rows


VAN = scan('vanilla')
rows = scan('rb')
json.dump(dict(rows=rows), open(os.path.join(M, 'design', 'analysis', 'buff_survey.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def fmt(vals, unit):
    vs = [vals[l] for l in sorted(vals)]
    if not vs:
        return ''
    s = lambda x: ('%g' % x) + unit
    return s(vs[0]) if len(set(vs)) == 1 else s(vs[0]) + '→' + s(vs[-1])

UNIT = lambda c: '' if c.rstrip('*').split()[-1] in ('명중', '회피', '속도', '반격', '보호') else '%'
skills = collections.OrderedDict()
for r in rows:
    skills.setdefault((r['hero'], r['skill'], r['cat'], r['side']), {})[r['level']] = r
by_cat = collections.defaultdict(list)
for (h, sid, cat, side), lv in skills.items():
    r0 = lv[min(lv)]
    by_cat[cat.rstrip('*')].append(dict(hero=h, hero_ko=r0['hero_ko'], skill_ko=r0['skill_ko'], side=side, cond=cat.endswith('*'),
                                         val='' if cat in ('반격', '보호') else fmt({l: x['val'] for l, x in lv.items()}, UNIT(cat)),
                                         dur=fmt({l: x['dur'] for l, x in lv.items() if x['dur'] is not None}, '턴') or '기본'))
van = collections.defaultdict(set)
for r in VAN:
    van[r['cat'].rstrip('*')].add((r['hero'], r['skill'], r['side']))

head = subprocess.run(['git', 'log', '--oneline', '-1'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
dirty = subprocess.run(['git', 'status', '--short', '--', 'heroes', 'effects', 'shared'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, encoding='utf-8', cwd=M).stdout.strip()
SIDES = ('자신', '아군 1명', '아군 전체')
L = ['# 강화(버프) 전수 조사', '',
     f'- 생성: {datetime.date.today()} `python tools/buff_survey.py` / 브랜치 `{branch}` / {head}' + (' / **커밋 안 된 게임 데이터 변경 포함(작업 트리 기준)**' if dirty else ''),
     '- 범위: 영웅 20명 모든 전투 기술·반격, 1~5렙. 자신·아군에게 거는 강화(능력치·저항 증가, 받는 피해 감소, 반격, 보호 등). 회복·스트레스 회복 자체, 치명타 전용 효과 제외.',
     '- "조건부" = 표식·종족 대상일 때만 붙는 추가 피해 등. `*` = 조건부 버프(rule). 수치 1렙→5렙, 명중·회피·속도는 점, 나머지 %. 개수는 (기술, 받는 쪽) 단위.', '']
cats = sorted(set(by_cat) | set(van), key=lambda c: (-len(by_cat.get(c, [])), c))
L += ['## 1. 범주별 분포 (바닐라 → 현재)', '', '| 강화 | 기술 수 (바닐라→현재) | 영웅 수 | 자신 | 아군 1명 | 아군 전체 |', '|---|---|---|---|---|---|']
for c in cats:
    lst = by_cat.get(c, [])
    cnt = collections.Counter(x['side'] for x in lst)
    L.append(f'| {c} | {len(van.get(c, ()))}→{len(lst)} | {len({x["hero"] for x in lst})} | ' + ' | '.join(str(cnt.get(s, 0)) for s in SIDES) + ' |')
L += ['', '## 2. 범주별 상세', '']
for c in cats:
    lst = by_cat.get(c)
    if not lst:
        continue
    L += [f'### {c} ({len(lst)}개, {len({x["hero"] for x in lst})}명)', '', '| 영웅 | 기술 | 받는 쪽 | 수치 | 지속 |', '|---|---|---|---|---|']
    for x in sorted(lst, key=lambda x: (x['hero_ko'], x['skill_ko'])):
        L.append(f'| {x["hero_ko"]} | {x["skill_ko"]}{" *" if x["cond"] else ""} | {x["side"]} | {x["val"]} | {x["dur"]} |')
    L += ['']
L += ['## 3. 영웅별', '', '| 영웅 | 강화 기술 수 | 자신 | 아군 1명 | 아군 전체 | 강화 범주 |', '|---|---|---|---|---|---|']
for h, ko in S.KO.items():
    mine = [(sid, side, c) for (hh, sid, c, side) in skills if hh == h]
    cnt = {s: len({sid for sid, sd, _ in mine if sd == s}) for s in SIDES}
    L.append(f'| {ko} | {len({sid for sid, _, _ in mine})} | ' + ' | '.join(str(cnt[s]) for s in SIDES) + f' | {", ".join(sorted({c.rstrip("*") for _, _, c in mine})) or "-"} |')
open(os.path.join(M, 'design', 'analysis', 'buff_survey.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
