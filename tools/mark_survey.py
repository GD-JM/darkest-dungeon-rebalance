"""표식 전수 조사 (2026-10-21): 영웅 기술(표식 걸기·표식 특효·자기 표식·표식 해제), 직업 치명타, 장신구, 야영, 몬스터.
현재 데이터(커스텀=창작마당 통합판) 기준, 1렙·5렙. 출력: design/analysis/mark_survey.md"""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
import strength as S
ec = S.ec; G = S.G; M = S.M_ROOT
E = S.load_effects('rb')
B = ec.load_buffs(G, M)
KO = ec.load_korean(G)
for f in glob.glob(os.path.join(M, 'localization', '*.string_table.xml')):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'<language id="koreana">(.*?)</language>', t, re.S)
    for k, v in re.findall(r'<entry id="([^"]+)"><!\[CDATA\[(.*?)\]\]>', m.group(1)):
        KO[k] = v


def tagged_buff(bid):
    b = B.get(bid.strip('"'), {})
    return b.get('rule_type') in ('actorStatus', 'is_actor_status') and (b.get('rule_data') or {}).get('string') == 'tagged', b


def classify(line):
    out = []
    for n in ec.effect_names_in(line):
        k = S.kv(E.get(n, '')); tgt = S.first(k, 'target', '')
        if 'tag' in k and tgt == 'target':
            out.append(('걸기', n, k))
        if 'tag' in k and tgt == 'performer':
            out.append(('자기 표식', n, k))
        if 'untag' in k:
            out.append(('표식 해제', n, k))
        if S.first(k, 'keyStatus') == 'tagged':
            out.append(('특효', n, k))
        for bid in k.get('buff_ids', []):
            ok, b = tagged_buff(bid)
            if ok:
                out.append(('특효(강화)', n, dict(k, _buff=b)))
    return out


def desc(kind, n, k):
    if kind in ('걸기', '자기 표식'):
        return '표식 %s턴' % S.first(k, 'duration', '?')
    if kind == '표식 해제':
        return '표식 해제'
    if kind == '특효(강화)':
        b = k['_buff']
        return '%s %s %+g%% (%s턴)' % (b['stat_type'], b.get('stat_sub_type', ''), b['amount'] * 100, S.first(k, 'duration', '?'))
    names = {'damage_low_multiply': '피해', 'crit_chance_add': '치명', 'attack_rating_add': '명중'}
    return ', '.join('%s %s' % (names[x], S.first(k, x)) for x in names if x in k)


rows = []
for h in S.KO:
    t = open(S.hero_file(h, 'rb'), encoding='utf-8', errors='ignore').read()
    by = {}
    for l in t.splitlines():
        if l.startswith('combat_skill:'):
            d = S.kv(l)
            by.setdefault(S.first(d, 'id'), {})[int(S.first(d, 'level', '0'))] = (l, d)
    for sid, lv in by.items():
        l0, d0 = lv[min(lv)]; l4, d4 = lv[max(lv)]
        c0, c4 = classify(l0), classify(l4)
        if not c0:
            continue
        if len(c4) != len(c0):
            c4 = c0
        others = [n for n in ec.effect_names_in(l0) if not any(n == x[1] for x in c0)]
        oth = '; '.join(re.sub(r'.*?\.target "([^"]+)" ', r'\1: ', E.get(n, n))[:80] for n in others)
        for (k0, n0, kk0), (k4, n4, kk4) in zip(c0, c4):
            rows.append((S.KO[h], KO.get('combat_skill_name_%s_%s' % (h, sid), sid), k0, S.first(d0, 'launch'), S.first(d0, 'target'),
                         S.first(d0, 'atk', '-'), S.first(d0, 'dmg', '-'), desc(k0, n0, kk0), desc(k4, n4, kk4), oth))

L = ['# 표식 전수 조사 (2026-10-21, 커스텀=창작마당 통합판)', '', '수치는 1렙 / 5렙. 데이터: `tools/mark_survey.py`.', '',
     '## 1. 영웅 기술', '', '| 영웅 | 기술 | 종류 | 사용 | 대상 | 명중(1렙) | 피해 | 1렙 | 5렙 | 같은 기술의 다른 효과(1렙) |',
     '|---|---|---|---|---|---|---|---|---|---|']
for r in sorted(rows, key=lambda r: (r[2], r[0])):
    L.append('| ' + ' | '.join(str(x) for x in r) + ' |')

L += ['', '## 2. 직업 치명타 버프 (표식 관련)', '']
for h in S.KO:
    H = S.load_hero(h, 'rb')
    for n in H['crit_effects']:
        for bid in S.kv(E.get(n, '')).get('buff_ids', []):
            ok, b = tagged_buff(bid)
            if ok:
                L.append('- %s: %s %s %+g%% (표식 대상, 2턴)' % (S.KO[h], b['stat_type'], b.get('stat_sub_type', ''), b['amount'] * 100))

L += ['', '## 3. 장신구 (표식 조건)', '', '| 장신구 | 영웅 | 등급 | 표식 관련 효과 | 다른 효과 |', '|---|---|---|---|---|']
tfs = glob.glob(os.path.join(G, 'trinkets', '*.json')) + glob.glob(os.path.join(G, 'dlc', '**', 'trinkets', '*.json'), recursive=True)
seen = set()
for f in tfs:
    try:
        d = json.load(open(f, encoding='utf-8-sig'))
    except Exception:
        continue
    for e in d.get('entries', []):
        if e['id'] in seen:
            continue
        mk, ot = [], []
        for bid in e.get('buffs', []):
            b = B.get(bid, {}); rd = (b.get('rule_data') or {}).get('string', '')
            s = '%s %s %+g%%' % (b.get('stat_type'), b.get('stat_sub_type', ''), (b.get('amount') or 0) * 100)
            (mk if rd == 'tagged' or 'tag' in (b.get('stat_type') or '') else ot).append(s + (' [%s]' % b.get('rule_type') if rd == 'tagged' else ''))
        if mk:
            seen.add(e['id'])
            L.append('| %s | %s | %s | %s | %s |' % (KO.get('str_inventory_title_trinket' + e['id'], e['id']),
                                                ','.join(S.KO.get(x, x) for x in e.get('hero_class_requirements', [])) or '공용',
                                                e.get('rarity'), '; '.join(mk), '; '.join(ot)))

L += ['', '## 4. 몬스터 (영웅 등급 _C)', '']
mons = {}
for f in glob.glob(os.path.join(G, 'monsters', '**', '*_C.info.darkest'), recursive=True) + \
         glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*_C.info.darkest'), recursive=True):
    t = open(f, encoding='utf-8', errors='ignore').read(); nm = os.path.basename(f).split('.')[0]
    for l in t.splitlines():
        if l.startswith(('combat_skill:', 'skill:')):                     # 몬스터 기술 줄은 'skill:'
            for kind, n, k in classify(l):
                mons.setdefault(kind, set()).add('%s/%s' % (nm, S.first(S.kv(l), 'id')))
for kind, v in mons.items():
    L.append('- %s %d개: %s' % (kind, len(v), ', '.join(sorted(v))))
open(os.path.join(M, 'design', 'analysis', 'mark_survey.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(len(rows), 'skill rows')
