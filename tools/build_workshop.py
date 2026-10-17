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
import patch_notes as PN


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
    # 패치 노트 (영어 = 메인, 한국어): 무엇 = 바닐라 vs 출력 데이터 자동 비교(patch_notes.py), 왜 = design/workshop/why.json(검토된 근거)
    names = {}
    for f in glob.glob(os.path.join(G, 'localization', '*.string_table.xml')) + glob.glob(os.path.join(G, 'dlc', '*', 'localization', '*.string_table.xml')) + glob.glob(os.path.join(G, 'dlc', '*', 'features', '*', 'localization', '*.string_table.xml')):
        t = rd(f)
        for lang in ('english', 'koreana'):
            i0 = t.find('<language id="%s">' % lang)
            if i0 < 0:
                continue
            j0 = t.find('</language>', i0)
            for m in re.finditer(r'<entry id="combat_skill_name_(\w+?)"><!\[CDATA\[(.*?)\]\]>', t[i0:j0]):
                names.setdefault((lang, m.group(1)), m.group(2))
            for m in re.finditer(r'<entry id="hero_class_name_(\w+?)"><!\[CDATA\[(.*?)\]\]>', t[i0:j0]):
                names.setdefault((lang, 'hero:' + m.group(1)), m.group(2))
    why_p = os.path.join(W, 'why.json')
    WHY = json.load(open(why_p, encoding='utf-8')) if os.path.exists(why_p) else {}
    ctx = PN.make_ctx(OUT)
    ctx.skill_names = {lg: {k[1]: v for k, v in names.items() if k[0] == lk} for lg, lk in (('en', 'english'), ('ko', 'koreana'))}
    EN_HERO = {h: names.get(('english', 'hero:' + h), h.replace('_', ' ').title()) for h in S.KO}
    BLOCK = {'en': {'weapon': 'Weapon', 'armour': 'Armor', 'resistances': 'Resistances', 'mode': 'Beast form'},
             'ko': {'weapon': '무기', 'armour': '방어구', 'resistances': '저항', 'mode': '짐승 형태'}}
    summary = {'en': {}, 'ko': {}}
    missing = []
    for lang, lk in (('en', 'english'), ('ko', 'koreana')):
        L = ['# Rebalance — Patch notes' if lang == 'en' else '# 리밸런스 — 패치 노트', '',
             'Each entry: what changed (generated from the game data) — why (principle IDs from the mod description).' if lang == 'en'
             else '항목마다: 무엇이 바뀌었나(게임 데이터에서 자동 생성) — 왜(설명문의 원칙 번호).', '']
        for hero in heroes:
            wf = os.path.join(OUT, 'heroes', hero, hero + '.info.darkest')
            diffs = PN.hero_diff(hero, wf, ctx, lang)
            if not diffs:
                continue
            L += ['## ' + (EN_HERO[hero] if lang == 'en' else S.KO[hero]), '']
            for key, what in diffs:
                blk = key[1] or key[0]
                nm = names.get((lk, '%s_%s' % (hero, blk)), BLOCK[lang].get(blk, blk))
                w = WHY.get('%s|%s' % (hero, blk), {})
                reason = w.get(lang, '')
                if not reason and lang == 'en':
                    missing.append('%s|%s' % (hero, blk))
                pr = ', '.join(w.get('principles', []))
                ids = ', '.join(w.get('ids', []))
                line = '- **%s**: %s' % (nm, '; '.join(what))
                if reason:
                    line += ' — %s' % reason
                tail = ' / '.join(x for x in (pr, ids) if x)
                if tail:
                    line += ' *(%s)*' % tail
                L.append(line)
                summary[lang].setdefault(hero, [])
                if (nm, '%s|%s' % (hero, blk)) not in summary[lang][hero]:
                    summary[lang][hero].append((nm, '%s|%s' % (hero, blk)))
            L.append('')
        open(os.path.join(W, 'patch_notes_%s.md' % lang), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    if missing:
        print('근거(why) 없는 블록 %d개: %s' % (len(missing), ', '.join(missing[:12]) + (' …' if len(missing) > 12 else '')))
    # 설명문 = 스팀 글 1개(8000자), 사람이 읽는 자연어로 손으로 쓴다(description_en/ko.txt) [사용자 10-17: 원칙 코드 금지]
    # 빌드는 바뀐 기술·영웅 이름이 설명문에 전부 나오는지만 확인한다. 전체 근거는 patch_notes_*.md (포트폴리오 기록)
    for lang in ('en', 'ko'):
        d0 = rd(os.path.join(W, 'description_%s.txt' % lang)).replace('\r\n', '\n').strip()
        absent = [nm for h, v in summary[lang].items() for nm, k in v
                  if k.split('|')[1] not in BLOCK['en'] and nm not in d0]
        absent += [h for h in summary[lang] if (EN_HERO[h] if lang == 'en' else S.KO[h]) not in d0]
        assert not absent, ('설명문에 빠진 변경', lang, absent)
        open(os.path.join(W, 'description_built_%s.txt' % lang), 'w', encoding='utf-8', newline='\n').write(d0 + '\n')
        print('description', lang, len(d0), 'chars (Steam limit 8000; line breaks counted twice: %d)' % (len(d0) + d0.count('\n')))
        assert len(d0) + d0.count('\n') <= 8000, lang  # 웹 편집기가 줄바꿈을 CRLF(2자)로 세어도 넘지 않게
    shutil.copy(os.path.join(M, 'preview_icon.png'), os.path.join(OUT, 'preview_icon.png'))
    proj = rd(os.path.join(W, 'project.template.xml'))
    desc = rd(os.path.join(W, 'description_built_en.txt')).strip()
    proj = proj.replace('{MOD_DATA_PATH}', OUT.replace('\\', '/') + '/').replace('{DESCRIPTION}', desc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    open(os.path.join(OUT, 'project.xml'), 'w', encoding='utf-8', newline='\n').write(proj.replace('\r\n', '\n'))
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
