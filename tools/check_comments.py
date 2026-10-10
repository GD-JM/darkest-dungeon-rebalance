"""Require traceable comments on changed hero data and every changed effect.

Consecutive changed rows of one skill/stat series may share a note below the run.
Effect sheets and generated effects require an ID + explanation immediately below
each changed/new effect. RB references count as changes. No game files are written.
"""
import argparse
from collections import Counter
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from effect_common import paths, vanilla_hero_file, norm_ws, effect_files, imported_hero

CHANGE_ID = re.compile(r'\b[A-Z][A-Z0-9]{1,7}-\d{2,3}\b')

def read_lines(path):
    return Path(path).read_bytes().decode('utf-8', errors='replace').splitlines()

def info_key(line):
    kind = line.split(':', 1)[0]
    ident = re.search(r'\.(?:id|name)\s+"?([^" ]+)', line)
    level = re.search(r'\.level\s+(\d+)', line)
    return kind, ident[1] if ident else '', level[1] if level else ''

def series_key(line):
    kind, ident, _ = info_key(line)
    if kind in ('weapon', 'armour'):
        ident = re.sub(r'_\d+$', '', ident)
    return kind, ident

def data_map(lines):
    result, count = {}, Counter()
    for line in lines:
        if not line.strip() or line.startswith('//'):
            continue
        key = info_key(line)
        count[key] += 1
        result[key + (count[key],)] = norm_ws(line)
    return result

def note_error(line, known_ids):
    if not line.startswith('//') or line.startswith('//#'):
        return '바로 아래 // 변경 ID·설명 주석 없음'
    ids = CHANGE_ID.findall(line)
    if not ids:
        return '변경 ID 없음'
    if any(i not in known_ids for i in ids):
        return '의도 문서에 없는 ID: ' + ', '.join(i for i in ids if i not in known_ids)
    description = CHANGE_ID.sub('', line[2:]).strip(' /,;:[]-')
    if not description:
        return '변경 설명/의도 연결 없음'
    return None

def check_info(lines, vanilla, known_ids):
    original = data_map(vanilla)
    changed, seen, count = set(), set(), Counter()
    for i, line in enumerate(lines):
        if not line.strip() or line.startswith('//'):
            continue
        key = info_key(line)
        count[key] += 1
        key += (count[key],)
        seen.add(key)
        if original.get(key) != norm_ws(line):
            changed.add(i)
    errors = []
    for i in sorted(changed):
        j = i + 1
        while j < len(lines):
            if not lines[j].strip() or lines[j].startswith('//#'):
                j += 1
            elif j in changed and series_key(lines[j]) == series_key(lines[i]):
                j += 1
            else:
                break
        error = note_error(lines[j] if j < len(lines) else '', known_ids)
        if error:
            errors.append((i + 1, error, lines[i]))
    for key in original.keys() - seen:
        # MUS-001: a removed upstream row requires an exact, traceable deletion
        # record. A generic ID note cannot silence an accidental missing row.
        marker = 'removed-original: ' + original[key] + ' | '
        found = any(marker in l and note_error(l, known_ids) is None and l.split(marker, 1)[1].strip()
                    for l in lines if l.startswith('//'))
        if not found:
            errors.append((0, '원본 줄 삭제: 삭제 위치의 의도 기록을 검토하세요', str(key)))
    return errors

def check_effects(lines, vanilla_effects, known_ids, generated=False):
    errors = []
    for i, line in enumerate(lines):
        if not line.startswith('effect:'):
            continue
        match = re.search(r'\.name\s+"([^"]+)"', line)
        name = match[1] if match else ''
        if not generated and norm_ws(line) in vanilla_effects.get(name, set()):
            continue
        error = note_error(lines[i + 1] if i + 1 < len(lines) else '', known_ids)
        if error:
            errors.append((i + 1, error, name))
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mod')
    parser.add_argument('--game')
    parser.add_argument('heroes', nargs='*')
    args = parser.parse_args(argv)
    mod, game = paths(args.mod, args.game)
    mod = Path(mod)
    known = set()
    for path in (mod / 'design' / 'changes').glob('*.md'):
        for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
            if line.startswith(('#', '|')):
                known.update(CHANGE_ID.findall(line))
    effects = {}
    for path in effect_files(game):
        for line in read_lines(path):
            if line.startswith('effect:'):
                match = re.search(r'\.name\s+"([^"]+)"', line)
                if match:
                    effects.setdefault(match[1], set()).add(norm_ws(line))
    errors, checked_heroes = 0, 0
    for hero in sorted(p for p in (mod / 'heroes').iterdir() if p.is_dir()):
        if args.heroes and hero.name not in args.heroes:
            continue
        checked_heroes += 1
        files = [(hero / (hero.name + '.info.darkest'), 'info'),
                 (hero / (hero.name + '.effects_edit.txt'), 'edit'),
                 (mod / 'effects' / ('rebalance_' + hero.name + '.effects.darkest'), 'generated')]
        imported = imported_hero(str(mod), hero.name)
        if imported:
            files.append((mod / imported['runtime_effects'], 'generated'))
        for path, kind in files:
            if not path.exists():
                continue
            lines = read_lines(path)
            found = (check_info(lines, read_lines(vanilla_hero_file(game, hero.name)), known)
                     if kind == 'info' else check_effects(lines, effects, known, kind == 'generated'))
            for number, error, source in found:
                print('[%s/%s] %s행 %s: %s' % (hero.name, kind, number or '-', error, source[:120]))
            errors += len(found)
    print('주석 규칙 위반 %d건' % errors if errors else
          '주석 규칙: %d명 모든 변경에 ID·설명 주석 있음 (효과는 행별 검사)' % checked_heroes)
    # SYS-102: modfiles.txt 크기가 실제 파일과 다르면 게임이 파일을 잘라 읽는다(노상강도 기술 선택 설정 유실, 2026-10-10).
    stale = []
    mf = mod / 'modfiles.txt'
    if mf.exists():
        for line in mf.read_text(encoding='utf-8').splitlines():
            rel, _, size = line.strip().rpartition(' ')
            if rel and rel != 'modfiles.txt':
                f = mod / rel
                if not f.exists() or str(f.stat().st_size) != size:
                    stale.append(rel)
    if stale:
        print('modfiles.txt 크기 불일치 %d건 -> python tools/make_modfiles.py 실행 필요: %s' % (len(stale), ', '.join(stale[:5])))
    return 1 if (errors or stale) else 0

if __name__ == '__main__':
    raise SystemExit(main())
