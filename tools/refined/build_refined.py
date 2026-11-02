"""Darkest Refined 빌드 — 기존 창작마당판(3821353035, tools/build_workshop.py)과 별개인 새 아이템용 빌더.

[사용자 2026-11-02] "기존거를 수정하는 식으로 작업하지 말고 새로 만들어서 너가 따로 작업해서 업로드하고,
기존 꺼는 그 형식 그대로 그냥 코덱스가 DLC 영웅만 빼는 식으로 작업할거야"
→ build_workshop.py·workshop-sync는 고치지 않는다. 공용 도우미(effect_common, workshop_assets, make_loc)는 불러 쓰기만 한다.

꾸러미(package) = 영웅 묶음 + 아이템 번호. 지금은 합본(20명) 하나, 나중에 영웅 단독판을 같은 빌더로 만든다.
- 원본은 git archive <ref>로 뽑은 커밋 스냅샷(작업 트리의 미커밋 변경이 섞이지 않게).
- 출력 파일 이름은 꾸러미 키로 고유하게: effects/dr_<key>.effects.darkest, shared/buffs/dr_<key>.buffs.json,
  localization/<아이템번호>_<언어>.loc2 — 기존 창작마당판(rebalance_workshop.*, 3821353035_*)과 경로가 겹치지 않는다.
- 영웅 파일(heroes/<영웅>/…)은 게임 규칙상 같은 경로 전체 교체다. 같은 커밋으로 만든 꾸러미끼리는 내용이 같다.

사용: python tools/refined/build_refined.py --item <아이템번호> --out <출력 폴더> [--ref main] [--package refined]
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tarfile, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
GAME = os.path.dirname(os.path.dirname(REPO))
CONF = os.path.join(REPO, 'design', 'refined')


def rd(p):
    return open(p, 'rb').read().decode('utf-8')


def snapshot(ref, dst):
    """git archive <ref> → dst (커밋된 내용만)."""
    with tempfile.TemporaryDirectory() as t:
        tar = os.path.join(t, 'src.tar')
        subprocess.run(['git', '-C', REPO, 'archive', '--format=tar', '-o', tar, ref], check=True)
        with tarfile.open(tar) as tf:
            tf.extractall(dst, filter='data')
    sha = subprocess.run(['git', '-C', REPO, 'rev-parse', ref], capture_output=True, text=True, check=True).stdout.strip()
    return sha


def build(src, out, item, package, heroes=None):
    """src = 커밋 스냅샷 폴더(저장소 루트와 같은 구조). 반환: 요약 dict."""
    sys.path.insert(0, os.path.join(REPO, 'tools'))   # 도우미 코드는 작업 트리, 게임 데이터(src)는 스냅샷
    import effect_common as ec
    import strength as S
    from workshop_assets import copy_skill_icons
    pkg = json.load(open(os.path.join(CONF, 'packages.json'), encoding='utf-8'))[package]   # 도구 설정은 작업 트리, 게임 데이터는 스냅샷
    heroes = heroes or pkg.get('heroes') or list(S.KO)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    van_eff = ec.load_vanilla_effects(GAME)
    cust_eff = {}
    for f in glob.glob(os.path.join(src, 'effects', 'rebalance_*.effects.darkest')):
        for l in rd(f).splitlines():
            m = re.match(r'effect:\s*\.name\s+"([^"]+)"', l)
            if m:
                cust_eff[m.group(1)] = l
    built = []
    for hero in heroes:
        cf = os.path.join(src, 'heroes', hero, hero + '.info.darkest')
        raw = rd(cf)
        van = rd(ec.vanilla_hero_file(GAME, hero)).splitlines()
        data = [l for l in raw.splitlines() if l.strip() and not l.startswith('//')]
        vdata = [l for l in van if l.strip() and not l.startswith('//')]
        if data == vdata:
            continue
        dst = os.path.join(out, 'heroes', hero, hero + '.info.darkest')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(raw.encode('utf-8'))
        copy_skill_icons(os.path.dirname(cf), os.path.dirname(dst), hero)
        art = os.path.join(os.path.dirname(cf), hero + '.art.darkest')
        if os.path.exists(art):
            shutil.copy(art, os.path.join(os.path.dirname(dst), hero + '.art.darkest'))
        built.append(hero)
    # 실제로 참조되는 RB 효과·강화만 (SYS-103: 치명·형태·반응 효과도 포함되게 효과 이름 전수)
    need = []
    for hero in built:
        for l in rd(os.path.join(out, 'heroes', hero, hero + '.info.darkest')).splitlines():
            if l.strip() and not l.lstrip().startswith('//'):
                for n in ec.effect_names_in(l):
                    if n not in van_eff and n not in need:
                        assert n in cust_eff, ('정의 없는 효과', hero, n)
                        need.append(n)
    effects = [cust_eff[n] for n in need]
    van_buffs = ec.load_buffs(GAME)
    cust_buffs = {}
    for f in glob.glob(os.path.join(src, 'shared', 'buffs', 'rebalance_*.buffs.json')):
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
    key = pkg['key']
    if effects:
        p = os.path.join(out, 'effects', 'dr_%s.effects.darkest' % key)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(('// Darkest Refined - effects used by the changed skills\r\n' + '\r\n'.join(effects) + '\r\n').encode('utf-8'))
    if need_b:
        p = os.path.join(out, 'shared', 'buffs', 'dr_%s.buffs.json' % key)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump({'buffs': need_b}, open(p, 'w', encoding='utf-8'), indent='\t')
    # 기술 이름 현지화: 스냅샷의 localization/*.string_table.xml → <아이템번호>_<언어>.loc2 (make_loc 공용, 번호만 바꿔 부른다)
    import make_loc
    make_loc.M, make_loc.G = src, GAME
    make_loc.PFID = str(item)
    make_loc.main(out_dir=os.path.join(out, 'localization'), local=False)
    shutil.copy(os.path.join(CONF, 'preview_icon.png'), os.path.join(out, 'preview_icon.png'))
    proj = rd(os.path.join(CONF, 'project.template.xml'))
    desc = rd(os.path.join(CONF, 'description', 'english.txt')).strip()
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    proj = proj.replace('{ITEM_ID}', str(item)).replace('{MOD_DATA_PATH}', out.replace('\\', '/') + '/')
    proj = proj.replace('{DESCRIPTION}', esc(desc)).replace('{UPDATE_DETAILS}', esc(pkg.get('note', 'Update')))
    open(os.path.join(out, 'project.xml'), 'w', encoding='utf-8', newline='\n').write(proj.replace('\r\n', '\n'))
    entries = []
    for root, _, files in os.walk(out):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), out).replace('\\', '/')
            entries.append('%s %d' % (rel, os.path.getsize(os.path.join(root, f))))
    entries.sort()
    body = '\n'.join(entries)
    size = 0
    for _ in range(5):   # SYS-102: 게임은 적힌 크기만큼만 읽으므로 자기 크기까지 정확해야 한다
        size = len((body + '\nmodfiles.txt %d' % size).encode('utf-8'))
    open(os.path.join(out, 'modfiles.txt'), 'w', encoding='utf-8', newline='\n').write(body + '\nmodfiles.txt %d' % size)
    return {'package': package, 'item': item, 'heroes': built, 'effects': len(effects), 'buffs': len(need_b), 'files': len(entries) + 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--item', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--ref', default='main')
    ap.add_argument('--package', default='refined')
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as t:
        sha = snapshot(a.ref, t)
        r = build(t, os.path.abspath(a.out), a.item, a.package)
    r['sha'] = sha
    print(json.dumps(r, ensure_ascii=False))


if __name__ == '__main__':
    main()
