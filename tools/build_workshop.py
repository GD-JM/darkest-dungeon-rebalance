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
        for i in skill_lines(lines, sid):
            new, n = re.subn(r'\s*\.effect "%s"' % re.escape(name), '', lines[i])
            if n == 0:
                new, n = re.subn(r' "%s"' % re.escape(name), '', lines[i])
            assert n == 1, (cid, lines[i])
            lines[i] = new.rstrip(); touched.append(i)
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
    for hero, cs in by_hero.items():
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
    if effects:
        p = os.path.join(OUT, 'effects', 'rebalance_workshop.effects.darkest')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(('// Rebalance (Verified) - new effects used by the changes below\r\n' + '\r\n'.join(effects) + '\r\n').encode('utf-8'))
    # project.xml + 미리보기
    desc = rd(os.path.join(M, 'design', 'workshop', 'description.txt')).strip()
    for lang in ('en', 'ko'):
        items = ['[*][b]%s[/b] (%s) — %s [i]%s[/i]' % (c['%s_name' % lang], c['id'], c[lang], ', '.join(c['principles'])) for c in spec['changes']]
        desc = desc.replace('{PATCH_%s}' % lang.upper(), '[list]\n' + '\n'.join(items) + '\n[/list]')
    open(os.path.join(M, 'design', 'workshop', 'description_built.txt'), 'w', encoding='utf-8').write(desc + '\n')
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
