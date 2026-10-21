# 창작마당판 영웅 + 총사 초안으로 강함 모델 실행 (게임 파일은 건드리지 않음)
import sys, os, json, re, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
MR = r'C:\Program Files (x86)\Steam\steamapps\common\DarkestDungeon\mods\Rebalance'
sys.path.insert(0, os.path.join(MR, 'tools'))
import strength as S
WS = os.path.join(MR, '..', 'RebalanceWorkshop'); DR = os.path.join(MR, 'design', 'musketeer', 'draft')
_hf, _le, _lb = S.hero_file, S.load_effects, S.ec.load_buffs
def hero_file(h, mode):
    if mode == 'rb':
        if h == 'musketeer':
            return os.path.join(DR, 'musketeer.info.darkest')
        f = os.path.join(WS, 'heroes', h, h + '.info.darkest')
        if os.path.exists(f):
            return f
    return _hf(h, mode)
def load_effects(mode):
    e = _le(mode)
    if mode == 'rb':
        for f in (os.path.join(WS, 'effects', 'rebalance_workshop.effects.darkest'), os.path.join(DR, 'musketeer_draft.effects.darkest')):
            for raw in open(f, encoding='utf-8'):
                if raw.startswith('effect:'):
                    e[re.search(r'\.name\s+"([^"]+)"', raw).group(1)] = raw.rstrip()
    return e
def load_buffs(G, root=None):
    b = _lb(G, root)
    if root:
        for x in json.load(open(os.path.join(DR, 'musketeer_draft.buffs.json'), encoding='utf-8'))['buffs']:
            b[x['id']] = x
    return b
S.hero_file, S.load_effects, S.ec.load_buffs = hero_file, load_effects, load_buffs
allres = S.run()
std = st.median(r['base'] for r in allres['vanilla'].values())
pp = lambda v, base: (v / base - 1) * 100
rr, orr = S.ranking(allres['rb'], '기본'); rv = S.ranking(allres['vanilla'], '기본')[0]
print('| 순위 | 영웅 | 총점 | 행동 가치 | 유효 체력 | 속도 | 유연성 | 바닐라 순위(총점) |')
for h in orr:
    r, v = allres['rb'][h], allres['vanilla'][h]
    print(f'| {rr[h]} | {S.KO[h]} | {r["score"]["기본"]:.0f} | {pp(r["act"], std):+.0f}%p | {r["surv"]:.0f} | {r["spd"]:.0f} | {r["flex"]:.1f} | {rv[h]} ({v["score"]["기본"]:.0f}) |')
for h in ('musketeer', 'arbalest'):
    for mode in ('vanilla', 'rb'):
        r = allres[mode][h]
        print(f'\n[{mode}] {S.KO[h]} 열 점수 {r["rank_pts"]}')
        for s, (v, parts, launch) in sorted(r['skills'].items(), key=lambda x: -x[1][0]):
            print(f'  {s:22s} {pp(v, r["base"]):+5.0f}%p 사용 {launch:5s} ' + ' '.join(f'{k}{x / r["base"] * 100:+.0f}' for k, x in parts.items()))
