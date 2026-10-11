"""모든 영웅 5렙 기술의 강화·약화 분포 (RB).
사용: python tools/buff_map.py  -> design/analysis/buff_debuff_map.md (+ .json)
조건부 추가 피해(keyStatus·monsterType)와 치명타 버프는 제외. 이름 뒤 * = 조건부 강화(rule_type)."""
import re, glob, json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'tools')
import strength as S

G = '../..'
SP = sys.argv[1] if len(sys.argv) > 1 else 'design/analysis'

# 한국어 기술 이름
ko = {}
for f in glob.glob(G + '/localization/*.string_table.xml') + glob.glob(G + '/dlc/*/localization/*.string_table.xml'):
    t = open(f, 'rb').read().decode('utf-8', 'ignore')
    i = t.find('<language id="koreana">')
    if i < 0:
        continue
    j = t.find('</language>', i)
    for m in re.finditer(r'<entry id="combat_skill_name_(\w+?)"><!\[CDATA\[(.*?)\]\]>', t[i:j]):
        ko.setdefault(m.group(1), m.group(2))

eff = {}
for f in glob.glob(G + '/effects/*.effects.darkest') + glob.glob(G + '/dlc/**/*.effects.darkest', recursive=True) + glob.glob('effects/*.effects.darkest'):
    if 'arena' in f:
        continue
    for l in open(f, 'rb').read().decode('utf-8', 'ignore').splitlines():
        m = re.match(r'effect:\s*\.name\s+"([^"]+)"', l)
        if m:
            eff[m.group(1)] = l
buffs = {}
for f in glob.glob(G + '/shared/buffs/*.json') + glob.glob(G + '/dlc/**/shared/buffs/*.json', recursive=True) + glob.glob('shared/buffs/*.json'):
    if 'arena' in f:
        continue
    try:
        for b in json.load(open(f, encoding='utf-8-sig'))['buffs']:
            buffs[b['id']] = b
    except Exception:
        pass

STAT = {'attack_rating': '명중', 'defense_rating': '회피', 'protection_rating': '방어', 'speed_rating': '속도',
        'damage_low': '피해', 'damage_high': '피해', 'crit_chance': '치명타'}
RES = {'stun': '기절 저항', 'poison': '중독 저항', 'bleed': '출혈 저항', 'debuff': '약화 저항', 'move': '이동 저항',
       'disease': '질병 저항', 'death_blow': '죽음의 일격 저항', 'trap': '함정 저항'}
BT = {'crit_received_chance': '받는 치명타', 'damage_received_percent': '받는 피해', 'stress_dmg_received_percent': '받는 스트레스',
      'hp_heal_received_percent': '받는 회복', 'stress_heal_received_percent': '받는 스트레스 회복', 'ignore_protection': '방어 무시',
      'hp_heal_percent': '주는 회복', 'stun_chance': '기절 확률', 'bleed_chance': '출혈 확률', 'poison_chance': '중독 확률',
      'debuff_chance': '약화 확률', 'move_chance': '이동 확률'}


def num(x):
    return float(str(x).rstrip('%'))


def stats(l):
    """효과 한 줄 -> [(범주, 수치)] (수치는 대상에게 + = 좋음 기준 아님, 원값)"""
    out = []
    if '.combat_stat_buff 1' in l or 'combat_stat_buff' in l:
        for k, nm in STAT.items():
            for m in re.finditer(r'\.' + k + r'_(add|multiply) (-?[\d.]+%?)', l):
                v = num(m.group(2))
                if k == 'damage_high' and any(c == '피해' for c, _ in out):
                    continue
                out.append((nm, v))
    m = re.search(r'\.buff_type (\w+) \.buff_amount ([^\s]+)', l)
    if m:
        a = m.group(2)
        v = num(a) if a.endswith('%') else float(a) * 100
        out.append((BT.get(m.group(1), m.group(1)), v))
    bm = re.search(r'\.buff_ids\s+(.*?)(?=\s\.[a-z_]+|$)', l)
    for bid in (re.findall(r'"([^"]+)"|(\S+)', bm.group(1)) if bm else []):
        if True:
            bid = bid[0] or bid[1]
            B = buffs.get(bid)
            if not B:
                continue
            st_, sub, a = B['stat_type'], B.get('stat_sub_type', ''), B.get('amount', 0)
            if st_ in ('combat_stat_add', 'combat_stat_multiply'):
                nm = STAT.get(sub)
                if nm and not (sub == 'damage_high' and any(c.startswith('피해') for c, _ in out)):
                    out.append((nm + ('*' if B.get('rule_type') not in (None, 'always') else ''), a if sub == 'speed_rating' else a * 100))
            elif st_ == 'resistance':
                out.append((RES.get(sub, sub + ' 저항'), a * 100))
            elif st_ in BT:
                out.append((BT[st_] + ('*' if B.get('rule_type') not in (None, 'always') else ''), a * 100))
    if re.search(r'\.tag \d', l):
        out.append(('표식', 0))
    if '.unstealth' in l or 'Destealth' in l:
        out.append(('은신 해제', 0))
    if re.search(r'\.guard \d', l):
        out.append(('보호', 0))
    if re.search(r'\.healstress \d', l):
        out.append(('스트레스 회복', num(re.search(r'\.healstress (\d+)', l).group(1))))
    if '.clearDebuff' in l or '.cure ' in l or '.cure' in l:
        pass
    return out


res = S.run()['rb']
rows = []
for f in sorted(glob.glob('heroes/*/*.info.darkest')):
    h = os.path.basename(f).split('.')[0]
    if h not in S.KO:
        continue
    r = res[h]
    for l in open(f, 'rb').read().decode('utf-8', 'ignore').splitlines():
        m = re.match(r'combat_skill: \.id "(\w+)" \.level 4(.*)', l)
        if not m:
            continue
        sid, rest = m.group(1), m.group(2)
        tg = re.search(r'\.target (\S*)', rest)
        tg = tg.group(1) if tg else ''
        if tg.startswith('.'):
            tg = ''
        em = re.search(r'\.effect (.*?)(?= \.[a-z_]+ |$)', rest)
        names = re.findall(r'"([^"]+)"', em.group(1)) if em else []
        for n in names:
            e = eff.get(n)
            if not e:
                continue
            t = re.search(r'\.target "(\w+)"', e)
            t = t.group(1) if t else ''
            if t == 'performer':
                side = '자신'
            elif t in ('performer_group', 'performer_group_other', 'global'):
                side = '아군 전체'
            elif t == 'target':
                if tg == '':
                    side = '자신'
                elif '@' in tg:
                    side = '아군 전체' if '~' in tg else '아군 1명'
                else:
                    side = '적 전체' if '~' in tg else '적 1명'
            else:
                continue
            if 'buff_source_type bsrc_crit' in e or 'on_crit' in n:
                continue
            if '.keyStatus' in e or '.monsterType' in e:     # 조건부 추가 피해(표식·종족 특효)는 강화가 아님
                continue
            for cat, v in stats(e):
                dur = re.search(r'\.duration (\d+)', e)
                cond = 'riposte' in e or '.apply_once' in e
                ch = re.search(r'\.chance (\d+)%', e)
                rows.append(dict(hero=h, hero_ko=S.KO[h], skill=sid, skill_ko=ko.get(h + '_' + sid, sid), side=side, cat=cat, val=v,
                                 dur=int(dur.group(1)) if dur else None, eff=n, chance=int(ch.group(1)) if ch else None,
                                 skill_pp=round((r['skills'].get(sid, (r['base'],))[0] / r['base'] - 1) * 100) if sid in r['skills'] else None))
json.dump(rows, open(os.path.join(SP, 'buff_debuff_map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

import collections, subprocess, datetime
head = subprocess.run(['git', 'log', '--oneline', '-1'], capture_output=True, text=True, encoding='utf-8').stdout.strip()
c = collections.defaultdict(list)
for x in rows:
    if x['val'] == 0 and x['cat'] not in ('표식', '은신 해제', '보호'):
        continue
    c[(x['side'], x['cat'])].append('%s %s%s%s' % (x['hero_ko'], x['skill_ko'], (' %+g' % x['val']) if x['val'] else '', ('/%d턴' % x['dur']) if x['dur'] else ''))
L = ['# 강화·약화 분포 (영웅 5렙 기술, RB)', '',
     '- 생성: %s, 데이터 커밋 `%s`, `python tools/buff_map.py`로 다시 만든다.' % (datetime.date.today(), head),
     '- 조건부 추가 피해(표식·종족 특효)와 치명타 버프는 제외. `*` = 조건부 강화(보호받는 중 등).', '']
for side in ('적 1명', '적 전체', '아군 전체', '아군 1명', '자신'):
    ks = sorted([k for k in c if k[0] == side], key=lambda k: -len(set(c[k])))
    if not ks:
        continue
    L += ['## ' + side, '', '| 능력치 | 수 | 기술 |', '|---|---|---|']
    for k in ks:
        L.append('| %s | %d | %s |' % (k[1], len(set(c[k])), ', '.join(sorted(set(c[k])))))
    L.append('')
open(os.path.join(SP, 'buff_debuff_map.md'), 'w', encoding='utf-8').write('\n'.join(L))
print(len(rows), 'rows ->', os.path.join(SP, 'buff_debuff_map.md'))
