"""창작마당판 빌드: 바닐라 영웅 파일 + design/workshop/changes.json의 검증된 변경(W)만 → mods/RebalanceWorkshop.

- 커스텀판(mods/Rebalance)은 건드리지 않는다. 출력 폴더는 매번 새로 만든다(게임 파일만, 설계 문서·도구·.git 없음).
- 각 변경은 반드시 정확히 적용돼야 한다(맞는 줄이 없으면 실패).
- 바꾼 블록 밑에 `// <ID> <영문 근거>` 주석(P-13).
- 패치 노트(ko/en)는 design/workshop/patch_notes_*.md로 같은 목록에서 생성.
사용: python tools/build_workshop.py
"""
import os, re, json, shutil, glob

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.dirname(os.path.dirname(M))
OUT = os.path.join(os.path.dirname(M), 'RebalanceWorkshop')
SPEC = os.path.join(M, 'design', 'workshop', 'changes.json')
import sys
sys.path.insert(0, os.path.join(M, 'tools'))
import effect_common as ec

CUSTOM = {}   # hero -> 커스텀판 데이터 줄
HERO = None


def rd(p):
    return open(p, 'rb').read().decode('utf-8')


def skill_lines(lines, sid):
    idx = [i for i, l in enumerate(lines) if re.match(r'combat_skill: \.id "%s" \.level \d' % re.escape(sid), l)]
    assert len(idx) == 5, (sid, len(idx))
    return idx


def apply(lines, op, cid, note):
    kind = op[0]
    touched = []
    if kind == 'skill':
        _, sid, field, vals = op
        for k, i in enumerate(skill_lines(lines, sid)):
            v = vals[k] if isinstance(vals, list) else vals
            new, n = re.subn(r'\.%s -?[\d.]+%%?' % field, '.%s %s' % (field, v), lines[i], count=1)
            assert n == 1, (cid, lines[i])
            lines[i] = new; touched.append(i)
    elif kind == 'skill_effect_swap':
        _, sid, old, new, lvs = op
        idx = skill_lines(lines, sid)
        for lv in lvs:
            i = idx[lv - 1]
            a, b = '"%s"' % old.format(n=lv), '"%s"' % new.format(n=lv)
            assert lines[i].count(a) == 1, (cid, lines[i])
            lines[i] = lines[i].replace(a, b); touched.append(i)
    elif kind == 'skill_effect_remove':
        _, sid, name = op
        for k, i in enumerate(skill_lines(lines, sid)):
            nm = name.format(n=k + 1)
            new, n = re.subn(r'\s*\.effect "%s"(?= \.|\s*$)' % re.escape(nm), '', lines[i])
            if n == 0:
                new, n = re.subn(r' "%s"' % re.escape(nm), '', lines[i])
            assert n == 1, (cid, lines[i])
            lines[i] = new.rstrip(); touched.append(i)
    elif kind == 'custom_skill':
        # 커스텀판의 그 기술 줄 전부를 그대로 가져온다(레벨·모드 순서 동일해야 함)
        _, sid = op
        pat = r'combat_skill: \.id "%s" \.level \d' % re.escape(sid)
        vidx = [i for i, l in enumerate(lines) if re.match(pat, l)]
        cl = [l for l in CUSTOM[HERO] if re.match(pat, l)]
        assert vidx and len(vidx) == len(cl), (cid, sid, len(vidx), len(cl))
        for i, l in zip(vidx, cl):
            lines[i] = l.rstrip(); touched.append(i)
    elif kind == 'custom_line':
        _, rx = op
        vidx = [i for i, l in enumerate(lines) if re.match(rx, l)]
        cl = [l for l in CUSTOM[HERO] if re.match(rx, l)]
        assert vidx and len(vidx) == len(cl), (cid, rx)
        for i, l in zip(vidx, cl):
            lines[i] = l.rstrip(); touched.append(i)
    elif kind == 'weapon':
        _, field, vals = op
        idx = [i for i, l in enumerate(lines) if l.startswith('weapon:')]
        assert len(idx) == 5, cid
        for k, i in enumerate(idx):
            if field == 'dmg_max':
                new, n = re.subn(r'(\.dmg \d+ )\d+', lambda m: m.group(1) + vals[k], lines[i])
            else:
                new, n = re.subn(r'\.%s \S+' % field, '.%s %s' % (field, vals[k]), lines[i])
            assert n == 1, (cid, lines[i])
            lines[i] = new; touched.append(i)
    elif kind == 'resist':
        _, key, val = op
        idx = [i for i, l in enumerate(lines) if l.startswith('resistances:')]
        assert len(idx) == 1, cid
        new, n = re.subn(r'\.%s \S+' % key, '.%s %s' % (key, val), lines[idx[0]])
        assert n == 1, (cid, key)
        lines[idx[0]] = new; touched.append(idx[0])
    elif kind == 'add_effects':
        return op[1]
    else:
        raise ValueError(kind)
    return touched


def main():
    spec = json.load(open(SPEC, encoding='utf-8'))
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    by_hero, effects = {}, []
    for c in spec['changes']:
        by_hero.setdefault(c['hero'], []).append(c)
    global HERO
    for hero, cs in by_hero.items():
        HERO = hero
        CUSTOM[hero] = [l for l in rd(os.path.join(M, 'heroes', hero, hero + '.info.darkest')).splitlines() if not l.startswith('//')]
        src = ec.vanilla_hero_file(G, hero)
        raw = rd(src)
        eol = '\r\n' if '\r\n' in raw else '\n'
        lines = raw.split(eol)
        notes = {}   # 주석을 달 줄 번호 -> [주석]
        for c in cs:
            last = None
            for op in c['ops']:
                r = apply(lines, op, c['id'], c['en'])
                if op[0] == 'add_effects':
                    effects += ['// %s %s' % (c['id'], c['en_name'])] + r
                else:
                    last = max(r) if last is None else max(last, max(r))
            if last is not None:
                notes.setdefault(last, []).append('// %s %s (%s)' % (c['id'], c['en'], ', '.join(c['principles'])))
        out = []
        for i, l in enumerate(lines):
            out.append(l)
            out += notes.get(i, [])
        dst = os.path.join(OUT, 'heroes', hero, hero + '.info.darkest')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(eol.join(out).encode('utf-8'))
    # 의존 효과·강화 자동 수집: 출력 영웅 파일이 가리키는 효과 중 바닐라에 없는 것 → 커스텀판 RB 효과에서 복사
    van_eff = ec.load_vanilla_effects(G)
    cust_eff = {}
    for f in glob.glob(os.path.join(M, 'effects', 'rebalance_*.effects.darkest')):
        for l in rd(f).splitlines():
            m = re.match(r'effect:\s*\.name\s+"([^"]+)"', l)
            if m:
                cust_eff[m.group(1)] = l
    defined = {re.match(r'effect:\s*\.name\s+"([^"]+)"', l).group(1) for l in effects if l.startswith('effect:')}
    need = []
    for hero in by_hero:
        for l in rd(os.path.join(OUT, 'heroes', hero, hero + '.info.darkest')).splitlines():
            if l.startswith('combat_skill:'):
                for n in ec.effect_names_in(l):
                    if n not in van_eff and n not in defined and n not in need:
                        assert n in cust_eff, ('정의 없는 효과', hero, n)
                        need.append(n)
    if need:
        effects += ['// copied from the custom build (RB effects used by the changes)'] + [cust_eff[n] for n in need]
    van_buffs = ec.load_buffs(G)
    cust_buffs = {}
    for f in glob.glob(os.path.join(M, 'shared', 'buffs', 'rebalance_*.buffs.json')):
        for b in json.load(open(f, encoding='utf-8-sig'))['buffs']:
            cust_buffs[b['id']] = b
    need_b = []
    for l in effects:
        m = re.search(r'\.buff_ids\s+(.*?)(?=\s\.[a-z_]+|$)', l)
        for a, b in (re.findall(r'"([^"]+)"|(\S+)', m.group(1)) if m else []):
            bid = a or b
            if bid not in van_buffs and bid not in [x['id'] for x in need_b]:
                assert bid in cust_buffs, ('정의 없는 강화', bid)
                need_b.append(cust_buffs[bid])
    if need_b:
        p = os.path.join(OUT, 'shared', 'buffs', 'rebalance_workshop.buffs.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump({'buffs': need_b}, open(p, 'w', encoding='utf-8'), indent='\t')
    if effects:
        p = os.path.join(OUT, 'effects', 'rebalance_workshop.effects.darkest')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(('// Rebalance (Verified) - new effects used by the changes below\r\n' + '\r\n'.join(effects) + '\r\n').encode('utf-8'))
    # project.xml + 미리보기
    built = {}
    for lang in ('en', 'ko'):
        d0 = rd(os.path.join(M, 'design', 'workshop', 'description_%s.txt' % lang)).strip()
        items = ['[*][b]%s[/b] (%s) — %s [i]%s[/i]' % (c['%s_name' % lang], c['id'], c[lang], ', '.join(c['principles'])) for c in spec['changes']]
        d0 = d0.replace('{PATCH_%s}' % lang.upper(), '[list]\n' + '\n'.join(items) + '\n[/list]')
        built[lang] = d0
        open(os.path.join(M, 'design', 'workshop', 'description_built_%s.txt' % lang), 'w', encoding='utf-8').write(d0 + '\n')
        print('description', lang, len(d0), 'chars (Steam limit 8000)')
        assert len(d0) <= 8000, lang
    desc = built['en']
    shutil.copy(os.path.join(M, 'preview_icon.png'), os.path.join(OUT, 'preview_icon.png'))
    proj = open(os.path.join(M, 'design', 'workshop', 'project.template.xml'), encoding='utf-8').read()
    proj = proj.replace('{MOD_DATA_PATH}', OUT.replace('\\', '/') + '/').replace('{DESCRIPTION}', desc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    open(os.path.join(OUT, 'project.xml'), 'w', encoding='utf-8').write(proj)
    # modfiles.txt
    entries = []
    for root, _, files in os.walk(OUT):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), OUT).replace('\\', '/')
            entries.append('%s %d' % (rel, os.path.getsize(os.path.join(root, f))))
    entries.sort()
    body = '\n'.join(entries); size = 0
    for _ in range(5):
        size = len((body + '\nmodfiles.txt %d' % size).encode('utf-8'))
    open(os.path.join(OUT, 'modfiles.txt'), 'w', encoding='utf-8', newline='\n').write(body + '\nmodfiles.txt %d' % size)
    # 패치 노트
    for lang, title in (('ko', '패치 노트'), ('en', 'Patch notes')):
        L = ['# Rebalance (Verified) — %s' % title, '']
        for c in spec['changes']:
            L.append('- **%s** [%s] (%s): %s' % (c['%s_name' % lang], c['id'], ', '.join(c['principles']), c[lang]))
        open(os.path.join(M, 'design', 'workshop', 'patch_notes_%s.md' % lang), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('built', OUT, '| heroes:', ', '.join(sorted(by_hero)), '| changes:', len(spec['changes']), '| files:', len(entries))


if __name__ == '__main__':
    main()
