"""Apply heroes/<id>/<id>.effects_edit.txt to the game data (idempotent).

For each hero:
  - effect lines that differ from vanilla -> if an EXISTING vanilla effect is already identical, the
    skill is pointed at that one instead (no duplicate is created; see rules.md R-DATA-01);
    otherwise written as "RB <ABBR> <name>" to effects/rebalance_<id>.effects.darkest
  - this hero's .info.darkest references to those effects -> renamed to the RB name
  - effects edited back to vanilla -> RB copy removed, references restored to the vanilla name
  - mod-only new effects (name starts with "RB <ABBR> " and has no vanilla counterpart) -> copied as-is
    (attaching them to skills is done in the hero .info.darkest; this tool only checks the references)
  - ASCII-only "// ..." note lines directly under an effect line are copied into the generated file
    (Korean notes stay in the edit file and go to design/changes at "정리")
Only the hero's own files are touched. Vanilla effect files are never overridden.
Usage: python tools/apply_effect_edits.py [--mod PATH] [--game PATH] [--dry-run] [hero ...]
"""
import os, glob, re, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from effect_common import (ABBR, P, paths, load_vanilla_effects, norm_ws, EFFECT_LIST, EFFECT_TOKEN,
                           effect_names_in, reuse_candidate, vanilla_index,
                           edit_effect_baseline, imported_hero)

args = sys.argv[1:]
opt = lambda k: args[args.index(k) + 1] if k in args else None
M, G = paths(opt('--mod'), opt('--game'))
dry = '--dry-run' in args
skip_vals = {opt('--mod'), opt('--game')}
only = [a for a in args if not a.startswith('--') and a not in skip_vals]
nrm = lambda l: re.sub(r'"\.(?=[A-Za-z_])', '" .', l)

report = []
pending_writes = {}  # SYS-101: validate the complete requested batch before mutating files.
for hero in sorted(d for d in os.listdir(os.path.join(M, 'heroes')) if os.path.isdir(os.path.join(M, 'heroes', d))):
    if only and hero not in only:
        continue
    edit = os.path.join(M, 'heroes', hero, hero + '.effects_edit.txt')
    info = os.path.join(M, 'heroes', hero, hero + '.info.darkest')
    if not os.path.exists(edit) or not os.path.exists(info):
        continue
    EFF = edit_effect_baseline(M, G, hero)
    VIDX = vanilla_index(EFF)
    imported = imported_hero(M, hero)
    abbr = ABBR[hero]
    prefix = 'RB %s ' % abbr

    def rb_of(base):
        # "GR Blight 1" already carries the hero abbreviation -> "RB GR Blight 1", not "RB GR GR Blight 1"
        return 'RB ' + base if base.startswith(abbr + ' ') else prefix + base

    def base_of(nm):
        if nm in back:
            return back[nm]
        if nm.startswith('RB '):
            c = nm[3:]
            if c in EFF:
                return c
            if nm.startswith(prefix):
                return nm[len(prefix):]
        return nm

    changed, custom, notes, errors = {}, {}, {}, []
    back = {}  # reused vanilla name -> edit-file name, filled after parsing
    current = None
    for raw in open(edit, encoding='utf-8', errors='replace'):
        line = raw.rstrip('\r\n')
        if line.startswith('//'):
            if current and not line.startswith('//#') and line.isascii():
                notes.setdefault(current, []).append(line)
            continue
        if not line.startswith('effect:'):
            current = None if line.strip() else current
            continue
        m = re.search(r'\.name\s+"([^"]+)"', line)
        if not m:
            errors.append('이름 없는 효과 줄: %s' % line[:80])
            current = None
            continue
        name = m.group(1)
        current = name
        if name not in EFF:
            if name.startswith('RB '):
                custom[name] = line
            else:
                errors.append('원본에 없는 효과 이름(원본 효과는 이름을 바꾸지 말고, 신규 효과는 "%s"로 시작): %s' % (prefix, name))
            continue
        if norm_ws(line) != norm_ws(EFF[name][0]):
            changed[name] = line

    # 1a) an identical vanilla effect already exists -> reuse it instead of making a duplicate
    reuse = {}
    for name in list(changed):
        cand = reuse_candidate(name, changed[name], EFF, VIDX)
        if cand and cand in changed:
            continue  # target is itself edited -> reusing it would couple the two (see reuse_candidate)
        if cand:
            reuse[name] = cand
            back[cand] = name
            del changed[name]

    # mod-only effects that duplicate a vanilla one: warn (they are attached by hand in the .info)
    for nm, ln in custom.items():
        same = [c for c in VIDX.get(__import__('effect_common').effect_sig(ln), ()) if not c.startswith('RB ')]
        if same:
            errors.append('(경고) 신규 효과가 기존 효과와 완전히 동일 -> 기존 것을 쓰세요: %s == %s' % (nm, ', '.join(sorted(same)[:3])))

    # 1b) rebalance effects file
    reb = os.path.join(M, 'effects', 'rebalance_%s.effects.darkest' % hero)
    if changed or custom or reuse:
        body = ['// Rebalance mod - %s effects from heroes/%s/%s.effects_edit.txt' % (hero, hero, hero),
                '// Generated by tools/apply_effect_edits.py. Do not edit here; edit the effects_edit.txt and re-apply.', '']
        for name in sorted(reuse):
            body.append('// reuse: %s -> %s (identical vanilla effect, no copy made)' % (name, reuse[name]))
        if reuse:
            body.append('')
        for name, line in changed.items():
            body.append('// edited vanilla effect (from %s)' % EFF[name][1])
            body.append(line.replace('"%s"' % name, '"%s"' % rb_of(name), 1))
            body.extend(notes.get(name, []))
        if custom:
            body.append('')
            body.append('// mod-only new effects')
            for name, line in custom.items():
                body.append(line)
                body.extend(notes.get(name, []))
        new_text = '\r\n'.join(body) + '\r\n'
        old_bytes = open(reb, 'rb').read() if os.path.exists(reb) else None
        if old_bytes != new_text.encode('utf-8'):
            pending_writes[reb] = new_text.encode('utf-8')
    elif os.path.exists(reb):
        pending_writes[reb] = None

    # 2) hero info references
    data = open(info, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in data else '\n'
    renamed = []

    def fix_list(m):
        def fix_name(nm):
            base = base_of(nm)
            if base not in EFF:
                return nm  # mod-only effect or unknown: leave as is
            target = reuse.get(base) or (rb_of(base) if base in changed else base)
            if target != nm:
                renamed.append('%s -> %s' % (nm, target))
            return target
        def fix_token(q):
            quoted = q.group(1) is not None
            nm = q.group(1) if quoted else q.group(2)
            new = fix_name(nm)
            return q.group(0) if (new == nm and not quoted) else '"%s"' % new
        return m.group(1) + EFFECT_TOKEN.sub(fix_token, m.group(2))

    new_lines = []
    for l in data.split(nl):
        n = nrm(l)
        if l.startswith('//') or not EFFECT_LIST.search(n):
            new_lines.append(l)
            continue
        fixed = EFFECT_LIST.sub(fix_list, n)
        new_lines.append(fixed if fixed != n else l)
    new_data = nl.join(new_lines)
    if new_data != data:
        pending_writes[info] = new_data.encode('utf-8')

    # MUS-001: imported effects can also be referenced by riposte, actor DOTs,
    # and trinkets. Restore from pinned baselines on every run, then remap only
    # effect-reference fields; buff IDs and effect definition names stay intact.
    if imported:
        import json
        def mapped(name):
            base = base_of(name)
            return reuse.get(base) or (rb_of(base) if base in changed else base)
        effect_keys = {'increment_effects', 'completion_effects',
                       'attack_skill_additional_effects', 'friendly_skill_additional_effects',
                       'riposte_skill_additional_effects'}
        def remap_json(o):
            if isinstance(o, dict):
                return {k: ([mapped(x) for x in v] if k in effect_keys else remap_json(v)) for k, v in o.items()}
            if isinstance(o, list):
                return [remap_json(x) for x in o]
            return o
        for ref in imported['reference_files']:
            baseline = os.path.join(M, ref['baseline'])
            target = os.path.join(M, ref['runtime'])
            original = open(baseline, 'rb').read()
            current_bytes = open(target, 'rb').read() if os.path.exists(target) else original
            if ref['kind'] == 'effects':
                text = original.decode('utf-8')
                new = re.sub(r'(\.riposte_effect\s+)"([^"]+)"',
                             lambda m: m[1] + '"' + mapped(m[2]) + '"', text).encode('utf-8')
            else:
                # Keep user changes to other trinkets/fields. Only effect-name
                # references are managed by this workflow. Exact pinned bytes
                # are restored only if the entire parsed document matches.
                data = json.loads(current_bytes.decode('utf-8-sig'))
                fixed = remap_json(data)
                if fixed == json.loads(original.decode('utf-8-sig')):
                    new = original
                elif fixed == data:
                    new = current_bytes
                else:
                    new = (json.dumps(fixed, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
            if new != current_bytes:
                pending_writes[target] = new

    # 3) checks for mod-only effects
    refs = set()
    for l in new_data.split(nl):
        if l.startswith('//'):
            continue
        refs.update(x for x in effect_names_in(nrm(l)) if x.startswith('RB ') and base_of(x) not in EFF)
    # 다른 영웅의 RB 효과를 그대로 빌려 쓰는 참조는 허용(VES-013 광휘 = 유물수집상 RB ANT Flash Burn 재사용, R-DATA-01)
    other_rb = set()
    for f in glob.glob(os.path.join(M, 'effects', 'rebalance_*.effects.darkest')):
        if os.path.basename(f) != 'rebalance_%s.effects.darkest' % hero:
            other_rb.update(re.findall(r'^effect:\s*\.name\s+"([^"]+)"', open(f, encoding='utf-8', errors='ignore').read(), re.M))
    for nm in sorted(refs - set(custom) - other_rb):
        errors.append('기술이 참조하는 신규 효과가 편집 사본에 없음: %s' % nm)
    for nm in sorted(set(custom) - refs):
        errors.append('(경고) 편집 사본의 신규 효과를 쓰는 기술이 없음: %s' % nm)

    if changed or renamed or errors or custom or reuse:
        report.append((hero, sorted(changed), sorted(custom), renamed, errors, reuse))

if not report:
    print('변경된 효과 없음 (게임 데이터 수정 없음)')
for hero, ch, cu, rn, er, ru in report:
    print('[%s] 수정된 원본 효과 %d개: %s' % (hero, len(ch), ', '.join(ch) or '-'))
    print('   신규 효과 %d개: %s' % (len(cu), ', '.join(cu) or '-'))
    if ru:
        print('   기존 효과 재사용 %d개 (사본 안 만듦): %s' % (len(ru), '; '.join('%s -> %s' % (k, v) for k, v in sorted(ru.items()))))
    print('   참조 변경 %d곳%s' % (len(rn), (': ' + '; '.join(sorted(set(rn)))[:400]) if rn else ''))
    for e in er:
        print('   오류:', e)
fatal = [e for _, _, _, _, errors, _ in report for e in errors if not e.startswith('(경고)')]
if fatal:
    print('검증 실패: 요청한 영웅 일괄 적용을 취소했습니다. 게임 파일과 파일 목록은 변경하지 않았습니다.')
    raise SystemExit(1)
if pending_writes and not dry:
    # SYS-101: malformed/unknown/missing effects are rejected before all writes.
    for target, payload in pending_writes.items():
        if payload is None:
            os.remove(target)
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'wb') as fh:
                fh.write(payload)
    mk = os.path.join(M, 'tools', 'make_modfiles.py')
    if os.path.exists(mk):
        print(subprocess.run([sys.executable, mk], capture_output=True, text=True).stdout.strip())
