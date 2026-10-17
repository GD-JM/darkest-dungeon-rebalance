"""창작마당판 빌드: 커스텀판(이 폴더) − 제외 목록 → mods/RebalanceWorkshop.

규칙 (2026-10-17 제작자 결정): 커스텀판 변경 중 원칙 위배·근거 없음·타 제작자 콘텐츠만 뺀다.
- design/workshop/changes.json
  - exclude_heroes: 통째로 빼는 영웅(바닐라 유지 = 파일을 넣지 않음)
  - revert: [{id, hero, ops, ko, en}] — 커스텀판 줄을 바닐라로 되돌림.
      ops: ["vanilla_skill", 기술id] / ["vanilla_line", 정규식] / ["skill", 기술id, 필드, 값(5개 또는 1개)]
  - pending: 제작자 답을 기다리는 항목(빌드에서는 revert와 같게 처리)
  - notes: {변경 ID: {principles, ko, en}} — 패치 노트 문구 덮어쓰기(없으면 데이터 주석에서 뽑음)
- 출력은 게임 파일만. 커스텀판이 쓰는 RB 효과·강화는 실제로 참조되는 것만 자동 복사.
- 패치 노트(ko/en): 바닐라와 다른 기술·줄마다, 그 밑 `// ID ...` 주석(영문=ASCII, 한글)을 모아 만든다.
  원칙 번호는 design/changes/<영웅>.md 해당 ID 절의 G-/P-/R- 번호.
사용: python tools/build_workshop.py
"""
import os, re, json, shutil, glob, sys

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.dirname(os.path.dirname(M))
OUT = os.path.join(os.path.dirname(M), 'RebalanceWorkshop')
W = os.path.join(M, 'design', 'workshop')
sys.path.insert(0, os.path.join(M, 'tools'))
import effect_common as ec
import strength as S


def rd(p):
    return open(p, 'rb').read().decode('utf-8')


def data_lines(text):
    return [l for l in text.splitlines()]


def apply_revert(lines, van, op, cid):
    kind = op[0]
    if kind == 'vanilla_skill':
        pat = r'combat_skill: \.id "%s" \.level \d' % re.escape(op[1])
        ci = [i for i, l in enumerate(lines) if re.match(pat, l)]
        vl = [l for l in van if re.match(pat, l)]
        assert ci and len(ci) == len(vl), (cid, op)
        for i, l in zip(ci, vl):
            lines[i] = l
    elif kind == 'vanilla_line':
        ci = [i for i, l in enumerate(lines) if re.match(op[1], l)]
        vl = [l for l in van if re.match(op[1], l)]
        assert ci and len(ci) == len(vl), (cid, op)
        for i, l in zip(ci, vl):
            lines[i] = l
    elif kind == 'vanilla_field':
        _, rx, field = op
        ci = [i for i, l in enumerate(lines) if re.match(rx, l)]
        vl = [l for l in van if re.match(rx, l)]
        assert ci and len(ci) == len(vl), (cid, op)
        fr = r'\.%s [^ ]+(?: (?!\.)[^ ]+)*' % field     # 값 토큰들 (다음 " ." 전까지, 예: ".dmg 10 19", ".def 7.5%")
        for i, l in zip(ci, vl):
            vm = re.search(fr, l); assert vm, (cid, l)
            new, n = re.subn(fr, lambda m: vm.group(0), lines[i], count=1); assert n == 1, (cid, lines[i])
            lines[i] = new
    elif kind == 'skill':
        _, sid, field, vals = op
        ci = [i for i, l in enumerate(lines) if re.match(r'combat_skill: \.id "%s" \.level \d' % re.escape(sid), l)]
        assert len(ci) == 5, (cid, op)
        for k, i in enumerate(ci):
            v = vals[k] if isinstance(vals, list) else vals
            new, n = re.subn(r'\.%s -?[\d.]+%%?' % field, '.%s %s' % (field, v), lines[i], count=1)
            assert n == 1, (cid, lines[i])
            lines[i] = new
    else:
        raise ValueError(kind)


def principles_of(hero, cid):
    p = os.path.join(M, 'design', 'changes', hero + '.md')
    if not os.path.exists(p):
        return []
    s = rd(p)
    out = []
    for m in re.finditer(r'^### ([^\n]*)\n(.*?)(?=^### |\Z)', s, re.S | re.M):
        if re.search(r'\b%s\b' % re.escape(cid), m.group(1)):
            for x in re.findall(r'\b([GP]-\d\d|R-[A-Z]+-\d\d)\b', m.group(2)):
                if x not in out:
                    out.append(x)
    return out


def main():
    spec = json.load(open(os.path.join(W, 'changes.json'), encoding='utf-8'))
    excl = set(spec.get('exclude_heroes', []))
    reverts = spec.get('revert', []) + spec.get('pending', [])
    notes_over = spec.get('notes', {})
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    van_eff = ec.load_vanilla_effects(G)
    cust_eff = {}
    for f in glob.glob(os.path.join(M, 'effects', 'rebalance_*.effects.darkest')):
        for l in rd(f).splitlines():
            m = re.match(r'effect:\s*\.name\s+"([^"]+)"', l)
            if m:
                cust_eff[m.group(1)] = l
    notes = []      # (hero, 대상, [ID], en 주석들, ko 주석들)
    heroes = []
    for hero in S.KO:
        cf = os.path.join(M, 'heroes', hero, hero + '.info.darkest')
        if hero in excl or not os.path.exists(cf):
            continue
        raw = rd(cf)
        eol = '\r\n' if '\r\n' in raw else '\n'
        lines = raw.split(eol)
        van = rd(ec.vanilla_hero_file(G, hero)).splitlines()
        for r in reverts:
            if r['hero'] == hero:
                for op in r['ops']:
                    apply_revert(lines, van, op, r['id'])
        data = [l for l in lines if l.strip() and not l.startswith('//')]
        vdata = [l for l in van if l.strip() and not l.startswith('//')]
        if data == vdata:
            continue        # 남은 변경 없음 → 파일 넣지 않음
        heroes.append(hero)
        # 패치 노트: 바닐라와 다른 데이터 줄 → 그 블록 밑 주석
        vset = set(vdata)
        i = 0
        while i < len(lines):
            l = lines[i]
            if l.strip() and not l.startswith('//') and l not in vset:
                m = re.match(r'combat_skill: \.id "(\w+)"', l)
                key = m.group(1) if m else l.split(':')[0]
                j = i
                while j + 1 < len(lines) and (lines[j + 1].startswith('combat_skill: .id "%s"' % key) if m else False):
                    j += 1
                k = j + 1
                cm = []
                while k < len(lines) and lines[k].startswith('//'):
                    cm.append(lines[k][2:].strip()); k += 1
                ids = []
                for c in cm:
                    for x in re.findall(r'\b([A-Z]{2,4}-\d{3}|MARK-\d\d)\b', c):
                        if x not in ids:
                            ids.append(x)
                notes.append((hero, key, ids, [c for c in cm if c.isascii()], [c for c in cm if not c.isascii()]))
                i = k
                continue
            i += 1
        dst = os.path.join(OUT, 'heroes', hero, hero + '.info.darkest')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(eol.join(lines).encode('utf-8'))
    # 의존 효과·강화
    need = []
    for hero in heroes:
        for l in rd(os.path.join(OUT, 'heroes', hero, hero + '.info.darkest')).splitlines():
            if l.startswith('combat_skill:'):
                for n in ec.effect_names_in(l):
                    if n not in van_eff and n not in need:
                        assert n in cust_eff, ('정의 없는 효과', hero, n)
                        need.append(n)
    effects = [cust_eff[n] for n in need]
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
    if effects:
        p = os.path.join(OUT, 'effects', 'rebalance_workshop.effects.darkest')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(('// Rebalance - effects used by the changed skills (copied from the author build)\r\n' + '\r\n'.join(effects) + '\r\n').encode('utf-8'))
    if need_b:
        p = os.path.join(OUT, 'shared', 'buffs', 'rebalance_workshop.buffs.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump({'buffs': need_b}, open(p, 'w', encoding='utf-8'), indent='\t')
    # 패치 노트 (전체, ko/en)
    names = {}
    for f in glob.glob(os.path.join(G, 'localization', '*.string_table.xml')) + glob.glob(os.path.join(G, 'dlc', '*', 'localization', '*.string_table.xml')):
        t = rd(f)
        for lang in ('english', 'koreana'):
            i0 = t.find('<language id="%s">' % lang)
            if i0 < 0:
                continue
            j0 = t.find('</language>', i0)
            for m in re.finditer(r'<entry id="combat_skill_name_(\w+?)"><!\[CDATA\[(.*?)\]\]>', t[i0:j0]):
                names.setdefault((lang, m.group(1)), m.group(2))
    EN_HERO = {h: h.replace('_', ' ').title() for h in S.KO}
    for lang, lk in (('en', 'english'), ('ko', 'koreana')):
        L = ['# Rebalance — %s' % ('Patch notes (full)' if lang == 'en' else '패치 노트 (전체)'), '']
        cur = None
        for hero, key, ids, en, ko in notes:
            if hero != cur:
                L += ['', '## %s' % (EN_HERO[hero] if lang == 'en' else S.KO[hero])]; cur = hero
            nm = names.get((lk, '%s_%s' % (hero, key)), key)
            pr = []
            for x in ids:
                for y in notes_over.get(x, {}).get('principles') or principles_of(hero, x):
                    if y not in pr:
                        pr.append(y)
            text = []
            for x in ids:
                if x in notes_over and notes_over[x].get(lang):
                    text.append(notes_over[x][lang])
            if not text:
                text = [re.sub(r'^\w+-\d+(·\w+-\d+)* ', '', c) for c in (en if lang == 'en' else (ko or en)) if '[trace' not in c] or \
                       [re.sub(r'^.*?\] ', '', c) for c in en]
            L.append('- **%s** [%s]%s — %s' % (nm, ', '.join(ids) or '-', (' (%s)' % ', '.join(pr)) if pr else '', ' / '.join(text)))
        open(os.path.join(W, 'patch_notes_%s.md' % lang), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    # 설명문: 원칙 + 영웅별 바뀐 기술 요약 (전체 노트는 patch_notes_*.md → 창작마당 토론 글/변경 기록)
    for lang, lk in (('en', 'english'), ('ko', 'koreana')):
        d0 = rd(os.path.join(W, 'description_%s.txt' % lang)).strip()
        by = {}
        for hero, key, ids, en, ko in notes:
            nm = names.get((lk, '%s_%s' % (hero, key)), key)
            if key in ('weapon', 'armour', 'resistances', 'mode', 'tag', 'generation'):
                nm = {'weapon': 'weapon' if lang == 'en' else '무기', 'armour': 'armor' if lang == 'en' else '방어구',
                      'resistances': 'resists' if lang == 'en' else '저항', 'mode': 'form' if lang == 'en' else '형태'}.get(key, key)
            by.setdefault(hero, [])
            if nm not in by[hero]:
                by[hero].append(nm)
        items = ['[*][b]%s[/b]: %s' % (EN_HERO[h] if lang == 'en' else S.KO[h], ', '.join(v)) for h, v in by.items()]
        d0 = d0.replace('{PATCH_%s}' % lang.upper(), '[list]\n' + '\n'.join(items) + '\n[/list]')
        open(os.path.join(W, 'description_built_%s.txt' % lang), 'w', encoding='utf-8').write(d0 + '\n')
        print('description', lang, len(d0), 'chars (Steam limit 8000)')
        assert len(d0) <= 8000, lang
    shutil.copy(os.path.join(M, 'preview_icon.png'), os.path.join(OUT, 'preview_icon.png'))
    proj = rd(os.path.join(W, 'project.template.xml'))
    desc = rd(os.path.join(W, 'description_built_en.txt')).strip()
    proj = proj.replace('{MOD_DATA_PATH}', OUT.replace('\\', '/') + '/').replace('{DESCRIPTION}', desc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    open(os.path.join(OUT, 'project.xml'), 'w', encoding='utf-8').write(proj)
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
    print('built', OUT, '| heroes:', len(heroes), ', '.join(heroes), '| notes:', len(notes), '| effects:', len(effects), '| buffs:', len(need_b))


if __name__ == '__main__':
    main()
