"""Create heroes/<id>/<id>.vanilla.txt: a read-only reference sheet of the vanilla hero (stats, skills, effect lines, full file).

Vanilla = <id>.info원본.darkest in the game folder (the backup of the official file). The game never reads the sheet.
Regenerate after an official patch changes a hero (the 원본 backup must be updated first).
Usage: python tools/make_vanilla_sheet.py hero [hero ...]
"""
import os, re, sys, time
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from effect_common import P, paths, load_vanilla_effects, load_korean, vanilla_hero_file, effect_names_in

M, G = paths()
EFF = load_vanilla_effects(G)
KO = load_korean(G)
RES = [('stun', '기절'), ('poison', '중독'), ('bleed', '출혈'), ('disease', '질병'), ('move', '이동'), ('debuff', '약화'),
       ('death_blow', '죽음의 일격'), ('trap', '함정')]
EXTRA_LISTS = re.compile(r'\.(\w+_effects)((?:\s+(?:"[^"]*"|(?!\.)[^\s"]+))+)')   # 괴인·결투가 모드별 효과 목록


def kv(line):
    d = OrderedDict()
    for k, v in re.findall(r'\.(\w+)((?:\s+(?!\.)(?:"[^"]*"|[^\s"]+))*)', line):
        d[k] = [x.strip('"') for x in re.findall(r'"[^"]*"|[^\s"]+', v)]
    return d


def pct(v):
    return v.rstrip('%') if v else ''


def row(label, vals, w=9):
    return '  ' + label.ljust(12) + ''.join(str(x).ljust(w) for x in vals)


def skill_effects(line):
    names = effect_names_in(line)
    for _, lst in EXTRA_LISTS.findall(line):
        names += [a or b for a, b in re.findall(r'"([^"]*)"|([^\s"]+)', lst)]
    return names


def sheet(hero):
    src = vanilla_hero_file(G, hero)
    live = src.replace('.info원본.darkest', '.info.darkest')
    raw = open(src, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').rstrip('\n').split('\n')
    ko = KO.get('hero_class_name_' + hero, hero)
    stamp = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(src)))
    out = ['[바닐라 원본] %s (%s)' % (ko, hero),
           '게임 원본 수치 참고용. 게임은 이 파일을 읽지 않고, 배포에도 포함되지 않음. 수정은 %s.info.darkest 에서.' % hero,
           '원본 위치: %s' % P(os.path.relpath(live, G)),
           '기준 파일: %s (게임 파일 날짜 %s). tools/make_vanilla_sheet.py 로 생성' % (os.path.basename(src), stamp), '']

    weapons = [kv(l) for l in raw if l.startswith('weapon:')]
    armours = [kv(l) for l in raw if l.startswith('armour:')]
    out += ['■ 장비 (레벨 1~5)', '  ' + ' ' * 12 + ''.join(str(i).ljust(7) for i in range(1, 6))]
    out.append(row('최대 체력', [a['hp'][0] for a in armours], 7))
    out.append(row('회피', [pct(a['def'][0]) for a in armours], 7))
    out.append(row('방어', [pct(a['prot'][0]) for a in armours], 7))
    out.append(row('속도(무기)', [w['spd'][0] for w in weapons], 7))
    out.append(row('피해', ['%s-%s' % tuple(w['dmg'][:2]) for w in weapons], 7))
    out.append(row('치명타', [w['crit'][0] for w in weapons], 7))
    out.append('')

    res = kv([l for l in raw if l.startswith('resistances:')][0])
    out += ['■ 저항', '  ' + ' | '.join('%s %s' % (k2, res[k][0]) for k, k2 in RES if k in res), '']

    skills = OrderedDict()
    for l in raw:
        if l.startswith('combat_skill:'):
            d = kv(l)
            skills.setdefault(d['id'][0], []).append((l, d))
    out.append('■ 전투 기술 (레벨 1~5)')
    for sid, lv in skills.items():
        lv.sort(key=lambda x: int(x[1]['level'][0]))
        d0 = lv[0][1]
        name = KO.get('combat_skill_name_%s_%s' % (hero, sid), sid)
        tgt = ' '.join(d0.get('target', [])) or '자신'
        lim = ''
        if 'per_battle_limit' in d0:
            lim += '  전투당 제한 ' + d0['per_battle_limit'][0]
        if 'per_turn_limit' in d0:
            lim += '  턴당 제한 ' + d0['per_turn_limit'][0]
        modes = '  태세 ' + ' '.join(d0['valid_modes']) if 'valid_modes' in d0 else ''
        out += ['', '  %s (%s)  종류 %s  사용 열 %s  대상 %s%s%s' % (
            name, sid, (d0.get('type') or ['-'])[0], ''.join(d0.get('launch', [])), tgt, lim, modes)]
        out.append(row('명중', [pct(d.get('atk', [''])[0]) for _, d in lv]))
        out.append(row('피해 보정', [pct(d.get('dmg', [''])[0]) for _, d in lv]))
        out.append(row('치명타 보정', [pct(d.get('crit', [''])[0]) for _, d in lv]))
        if any('heal' in d for _, d in lv):
            out.append(row('체력 회복', ['-'.join(d.get('heal', [])) for _, d in lv]))
        effs = [', '.join(skill_effects(l)) for l, _ in lv]
        if any(effs):
            if len(set(effs)) == 1:
                out.append('  ' + '효과'.ljust(12) + effs[0] + ' (전 레벨 동일)')
            else:
                out += ['  ' + ('효과 L%d' % (i + 1)).ljust(12) + e for i, e in enumerate(effs)]
    out += ['', '■ 기타 기술 줄'] + ['  ' + l.rstrip() for l in raw if l.startswith(('combat_move_skill:', 'riposte_skill:'))]

    groups = OrderedDict()
    seen = set()
    for l in raw:
        if l.startswith(('combat_skill:', 'riposte_skill:')):
            for n in skill_effects(l):
                if n in seen:
                    continue
                seen.add(n)
                line, f = EFF.get(n, ('// (효과 파일에서 찾지 못함: "%s")' % n, '?'))
                groups.setdefault(f, []).append(line)
    out += ['', '■ 이 영웅 기술이 쓰는 효과 줄 원본 (효과 파일은 영웅 파일과 따로 있음)']
    for f, lines in groups.items():
        out += ['  -- ' + f] + ['  ' + x.rstrip() for x in lines]
    out += ['', '■ 원본 파일 전문 (%s.info.darkest)' % hero, '-' * 60] + raw
    return '\r\n'.join(out) + '\r\n'


if __name__ == '__main__':
    for h in sys.argv[1:]:
        p = os.path.join(M, 'heroes', h, h + '.vanilla.txt')
        open(p, 'wb').write(sheet(h).encode('utf-8'))
        print(h, '->', P(os.path.relpath(p, M)))
