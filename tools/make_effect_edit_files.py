"""Create heroes/<id>/<id>.effects_edit.txt: a Notepad-editable copy of the effect lines this hero's skills use.

The game never reads these files. Edited values are applied by tools/apply_effect_edits.py.
Existing edit files are NOT overwritten unless --force is given.
Usage: python tools/make_effect_edit_files.py [--force] [hero ...]
"""
import os, re, sys, glob
from collections import defaultdict, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from effect_common import ABBR, P, paths, load_vanilla_effects, load_korean, vanilla_hero_file, effect_names_in, load_buffs

M, G = paths()
force = '--force' in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith('--')]
EFF = load_vanilla_effects(G)
KO = load_korean(G)
BUFF = load_buffs(G)

heroes = sorted(d for d in os.listdir(os.path.join(M, 'heroes')) if os.path.isdir(os.path.join(M, 'heroes', d)))

# usage maps across all vanilla heroes and monsters
hero_use = defaultdict(set)
for f in glob.glob(os.path.join(G, 'heroes', '*', '*.info원본.darkest')) + glob.glob(os.path.join(G, 'dlc', '**', 'heroes', '*', '*.info원본.darkest'), recursive=True):
    if 'arena' in P(f):
        continue
    h = P(f).split('/')[-1].split('.')[0]
    for line in open(f, encoding='utf-8', errors='replace'):
        for n in effect_names_in(re.sub(r'"\.(?=[A-Za-z_])', '" .', line)):
            hero_use[n].add(h)
mon_use = defaultdict(int)
for f in glob.glob(os.path.join(G, 'monsters', '**', '*.info.darkest'), recursive=True) + glob.glob(os.path.join(G, 'dlc', '**', 'monsters', '**', '*.info.darkest'), recursive=True):
    if 'arena' in P(f):
        continue
    for line in open(f, encoding='utf-8', errors='replace'):
        for n in effect_names_in(re.sub(r'"\.(?=[A-Za-z_])', '" .', line)):
            mon_use[n] += 1

HEADER = """// [편집용 효과 사본] {ko} ({hero})
// 이 파일은 게임이 읽지 않는다. 여기서 고친 수치는 Claude에게 "정리해줘"라고 요청한 뒤에 게임에 적용된다.
//   정리 시: 원본과 달라진 효과만 새 이름("RB {abbr} 원래이름")으로 effects/rebalance_{hero}.effects.darkest 에 추가되고,
//            이 영웅의 기술이 새 효과를 가리키게 바뀐다. 다른 영웅·몬스터는 영향 없음. 원래대로 되돌리면 새 효과도 사라진다.
// 규칙
//   - 수치만 고친다. 효과 줄을 지우거나 효과 이름(.name "...")을 바꾸지 않는다.
//   - 메모는 바꾼 줄 바로 밑에 // 로 쓴다. //# 로 시작하는 줄은 자동 설명이므로 고치지 않는다.
//   - 강화 효과(.buff_ids)의 실제 수치는 이 파일에 없다(shared/buffs JSON). //# 설명에 참고용으로만 적었다. 바꾸려면 요청.
// 자주 쓰는 키
//   .chance 적용 확률 | .duration 지속 턴 | .stun 기절 | .dotBleed 턴당 출혈 | .dotPoison 턴당 중독 | .dotBurn 턴당 화상
//   .push / .pull 밀치기·당기기 칸 | .heal 회복 | .heal_percent 최대 체력 비율 회복 | .dotHpHeal 턴당 회복 | .healstress 스트레스 회복 | .stress 스트레스
//   .combat_stat_buff 1 과 함께: .attack_rating_add 명중 / .defense_rating_add 회피 / .protection_rating_add 방어 / .speed_rating_add 속도
//     / .crit_chance_add 치명타 / .damage_low_multiply · .damage_high_multiply 피해 %
//   .tag 표식 | .riposte 반격 | .guard 보호 | .keyStatus 조건(대상 상태) | .target "performer" = 자신
"""

def describe_buffs(line):
    m = re.search(r'\.buff_ids((?: [\w"]+)+)', line)
    if not m:
        return []
    out = []
    for bid in re.findall(r'"?(\w+)"?', m.group(1)):
        b = BUFF.get(bid)
        if b:
            rule = '' if b.get('rule_type', 'always') == 'always' else ' [%s]' % b.get('rule_type')
            out.append('%s = %s %s%s' % (bid, b.get('stat_sub_type') or b.get('stat_type'), b.get('amount'), rule))
        else:
            out.append('%s = (정의 없음)' % bid)
    return out

written = []
for hero in heroes:
    if only and hero not in only:
        continue
    dst = os.path.join(M, 'heroes', hero, hero + '.effects_edit.txt')
    if os.path.exists(dst) and not force:
        written.append((hero, 'SKIP (이미 있음)', 0))
        continue
    src = vanilla_hero_file(G, hero)
    lines = [re.sub(r'"\.(?=[A-Za-z_])', '" .', l.rstrip('\r\n')) for l in open(src, encoding='utf-8', errors='replace')]
    skills = OrderedDict()
    extra = OrderedDict()
    for l in lines:
        if l.startswith('combat_skill:'):
            sid = re.search(r'\.id\s+"([^"]+)"', l).group(1)
            lv = int(re.search(r'\.level\s+(\d)', l).group(1)) + 1
            skills.setdefault(sid, OrderedDict())[lv] = effect_names_in(l)
        elif effect_names_in(l):
            kind = l.split(':', 1)[0]
            key = (re.search(r'\.id\s+"([^"]+)"', l) or [0, ''])[1]
            extra.setdefault('%s %s' % (kind, key), []).extend(effect_names_in(l))
    first_skill = {}
    skills_of = defaultdict(list)
    for sid, lv in skills.items():
        for names in lv.values():
            for n in names:
                first_skill.setdefault(n, sid)
                if sid not in skills_of[n]:
                    skills_of[n].append(sid)
    ko_skill = lambda sid: KO.get('combat_skill_name_%s_%s' % (hero, sid), sid)

    out = [HEADER.format(ko=KO.get('hero_class_name_' + hero, hero), hero=hero, abbr=ABBR[hero]).rstrip('\n')]
    n_lines = 0
    done = set()

    def emit_effect(n):
        global n_lines
        if n in done:
            return
        done.add(n)
        if n not in EFF:
            out.append('//#   (원본 효과 정의를 찾지 못함: "%s")' % n)
            return
        raw, srcfile = EFF[n]
        out.append(raw)
        n_lines += 1
        notes = []
        others = sorted(hero_use[n] - {hero})
        if others or mon_use[n]:
            parts = []
            if others:
                parts.append('다른 영웅 %d명(%s)' % (len(others), ', '.join(KO.get('hero_class_name_' + o, o) for o in others)))
            if mon_use[n]:
                parts.append('몬스터 기술 %d곳' % mon_use[n])
            notes.append('공유 효과: %s. 여기서 고치면 이 영웅만 바뀐다' % ' / '.join(parts))
        if len(skills_of[n]) > 1:
            notes.append('이 영웅의 다른 기술에서도 사용: %s' % ', '.join(ko_skill(s) for s in skills_of[n] if s != first_skill[n]))
        for b in describe_buffs(raw):
            notes.append('강화 효과 수치(JSON, 참고용): %s' % b)
        notes.append('원본 위치: %s' % srcfile)
        out.extend('//#   ' + x for x in notes)

    for sid, lv in skills.items():
        out.append('')
        out.append('//# ' + '=' * 70)
        out.append('//# 기술: %s (%s)' % (ko_skill(sid), sid))
        out.append('//# 레벨별 효과: ' + ' | '.join('%d레벨 %s' % (k, ', '.join(v) or '없음') for k, v in lv.items()))
        names = []
        for v in lv.values():
            for x in v:
                if x not in names:
                    names.append(x)
        if not names:
            out.append('//#   (효과 없음: 명중·피해·치명타는 영웅 파일에서 조정)')
        for n in names:
            emit_effect(n)
    if extra:
        out.append('')
        out.append('//# ' + '=' * 70)
        out.append('//# 기술 외 효과 (치명타 발동, 자세·모드 등)')
        for key, names in extra.items():
            out.append('//# %s' % key)
            for n in dict.fromkeys(names):
                emit_effect(n)
    with open(dst, 'w', encoding='utf-8', newline='\r\n') as fh:
        fh.write('\n'.join(out) + '\n')
    written.append((hero, P(os.path.relpath(dst, M)), n_lines))

for w in written:
    print('%-14s %-50s 효과 줄 %d' % w)
