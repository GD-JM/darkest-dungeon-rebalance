"""기절 전수 조사: 모든 영웅 기술(1~5렙)·연결 효과, 기절 관련 장신구·기벽 강화, 몬스터 열별 수치.
사용: python tools/stun_survey.py  -> design/analysis/stun_survey.md
손으로 고른 목록 없음 — 영웅 파일 전체에서 대상에게 .stun 을 거는 효과를 찾는다."""
import sys, io, os, re, glob, json, statistics as st, subprocess, datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
import strength as S

G = S.G
OUT = os.path.join(os.path.dirname(__file__), '..', 'design', 'analysis', 'stun_survey.md')


def effects(mode):
    return S.load_effects(mode)


def ko_names():
    ko = {}
    for f in glob.glob(os.path.join(G, 'localization', '*.string_table.xml')) + glob.glob(os.path.join(G, 'dlc', '*', 'localization', '*.string_table.xml')):
        t = open(f, 'rb').read().decode('utf-8', 'ignore')
        i = t.find('<language id="koreana">')
        if i < 0:
            continue
        j = t.find('</language>', i)
        for m in re.finditer(r'<entry id="(combat_skill_name_\w+?|trinket_name_\w+?|str_\w+?)"><!\[CDATA\[(.*?)\]\]>', t[i:j]):
            ko.setdefault(m.group(1), m.group(2))
    return ko


KO = ko_names()


def eff_summary(line):
    k = S.kv(line)
    tgt = S.first(k, 'target', '')
    bits = []
    for key in ('stun', 'push', 'pull', 'shuffletarget', 'tag', 'unstealth', 'heal', 'healstress', 'dotBleed', 'dotPoison', 'dotBurn', 'torch_increase', 'torch_decrease', 'kill_enemy_types', 'clearDebuff'):
        if key in k:
            v = S.first(k, key, '')
            bits.append(key + ('' if v in ('', '1', 'true') else ' ' + v))
    for key in k:
        if key.endswith(('_add', '_multiply')):
            bits.append('%s %s' % (key.replace('_rating_add', '').replace('_multiply', '×'), S.first(k, key)))
    if 'buff_ids' in k:
        bits.append('buffs ' + ','.join(b.strip('"') for b in k['buff_ids']))
    if 'buff_type' in k:
        bits.append('%s %s' % (S.first(k, 'buff_type'), S.first(k, 'buff_amount')))
    ch = S.first(k, 'chance', '100')
    dur = S.first(k, 'duration', '')
    return '%s[%s%s%s]' % (tgt, ' '.join(bits), (' ' + ch) if ch else '', (' %st' % dur) if dur else '')


def survey(mode):
    E = effects(mode)
    rows = []
    for hero in S.KO:
        t = open(S.hero_file(hero, mode), encoding='utf-8', errors='ignore').read()
        lines = [l for l in t.splitlines() if l.startswith('combat_skill:')]
        by = {}
        for l in lines:
            d = S.kv(l)
            sid, lv = S.first(d, 'id'), int(S.first(d, 'level', '0'))
            by.setdefault((sid, S.first(d, 'valid_modes', '')), {})[lv] = (l, d)
        for (sid, modes), lvs in by.items():
            l0, d0 = lvs[min(lvs)]
            names = S.ec.effect_names_in(l0)
            stun_names = [n for n in names if '.stun' in E.get(n, '') and '"target"' in E.get(n, '')]
            if not stun_names:
                continue
            ch = []
            for lv in sorted(lvs):
                ln = [n for n in S.ec.effect_names_in(lvs[lv][0]) if '.stun' in E.get(n, '')]
                ch.append(S.first(S.kv(E[ln[0]]), 'chance', '?').rstrip('%') if ln else '-')
            others = [eff_summary(E[n]) for n in names if n not in stun_names and n in E]
            rows.append(dict(hero=hero, ko=S.KO[hero], sid=sid, name=KO.get('combat_skill_name_%s_%s' % (hero, sid), sid), modes=modes,
                             type=S.first(d0, 'type', ''), atk=S.first(d0, 'atk', '-'), dmg=S.first(d0, 'dmg', '-'), crit=S.first(d0, 'crit', '-'),
                             crit_ok=S.first(d0, 'is_crit_valid', 'True'), launch=S.first(d0, 'launch', ''), target=S.first(d0, 'target', ''),
                             limit=S.first(d0, 'per_battle_limit', ''), move=' '.join(d0.get('move', [])), stun=ch,
                             stun_eff=stun_names[0], others=others,
                             extra=' '.join(x for x in ('ignore_stealth', 'ignore_protection', 'ignore_guard') if S.first(d0, x, 'false').lower() == 'true')))
    return rows


def buffs_related():
    """기절 확률(stun_chance)·기절 저항을 올리고 내리는 장신구·기벽·강화"""
    buffs = S.ec.load_buffs(G, S.M_ROOT)
    ids = {k: b for k, b in buffs.items() if b.get('stat_type') == 'stun_chance'}
    out = []
    for f in glob.glob(os.path.join(G, 'trinkets', '*.json')) + glob.glob(os.path.join(G, 'dlc', '*', 'trinkets', '*.json')):
        try:
            d = json.load(open(f, encoding='utf-8-sig'))
        except Exception:
            continue
        for t in d.get('entries', []):
            hit = [i for i in t.get('buffs', []) if i in ids]
            if hit:
                out.append(('장신구', t['id'], KO.get('str_inventory_title_trinket' + t['id'], t['id']), ','.join(t.get('hero_class_requirements', [])) or '공용', t.get('rarity', ''),
                            ' / '.join('%+.0f%%p%s' % (ids[i]['amount'] * 100, '' if ids[i].get('rule_type') in (None, 'always') else ' [%s %s]' % (ids[i]['rule_type'], ids[i]['rule_data'].get('string') or ids[i]['rule_data'].get('float'))) for i in hit)))
    for f in glob.glob(os.path.join(G, 'shared', 'quirk', '*.json')) + glob.glob(os.path.join(G, 'dlc', '*', 'shared', 'quirk', '*.json')):
        try:
            d = json.load(open(f, encoding='utf-8-sig'))
        except Exception:
            continue
        for q in d.get('quirks', []):
            hit = [i for i in q.get('buffs', []) if i in ids]
            if hit:
                out.append(('기벽', q['id'], q['id'], '공용', 'positive' if q.get('is_positive') else 'negative',
                            ' / '.join('%+.0f%%p' % (ids[i]['amount'] * 100) for i in hit)))
    return out


def monster_ranks():
    sh = S.stress_value(dict(S.PARAM, STRESS_TAKEN=2 * S.monster_stress_per_action() / 4))
    tau, mult, act, entries, rho = S.formation_stats(sh)
    return tau, mult, rho, act


def main():
    head = subprocess.run(['git', 'log', '--oneline', '-1'], capture_output=True, text=True, encoding='utf-8', cwd=S.M_ROOT).stdout.strip()
    R = {m: survey(m) for m in ('vanilla', 'rb')}
    allr = S.run()
    L = ['# 기절 전수 조사 (영웅 20명 전체, 1~5렙, 바닐라·RB)', '',
         '- 생성: %s, 데이터 커밋 `%s`, `python tools/stun_survey.py`로 다시 만든다.' % (datetime.date.today(), head),
         '- 영웅 파일 전체에서 대상에게 `.stun`을 거는 효과가 연결된 기술을 모두 찾았다(손으로 고른 목록 없음).',
         '- 명중·치명 보정은 1렙(레벨당 +5 / +1). 기절 확률은 1~5렙 전부. 모델은 모델(5렙), 표준 평타 7.7 HP 기준 %p.', '']
    for mode in ('rb', 'vanilla'):
        L += ['## %s 기절 기술 %d개' % ('RB(현재)' if mode == 'rb' else '바닐라', len(R[mode])), '',
              '| 영웅 | 기술 | 형태 | 사용 → 대상 | 명중 | 피해 | 치명 보정 | 기절 확률 1~5렙 | 제한·모드 | 그 밖의 효과 | 모델(5렙) |', '|---|---|---|---|---|---|---|---|---|---|---|']
        for r in sorted(R[mode], key=lambda x: (x['ko'], x['sid'])):
            sk = allr[mode][r['hero']]['skills'].get(r['sid'])
            val = '%+.0f' % ((sk[0] / 7.7 - 1) * 100) if sk else '-'
            lim = ' '.join(x for x in (('전투당 %s회' % r['limit']) if r['limit'] else '', r['modes'], ('이동 ' + r['move']) if r['move'] else '', r['extra'], '' if r['crit_ok'].lower() == 'true' else '치명 불가') if x)
            L.append('| %s | %s | %s | %s → %s | %s | %s | %s | %s | %s | %s | %s |' % (
                r['ko'], r['name'], '근접' if r['type'] == 'melee' else '원거리', '·'.join(r['launch']), r['target'], r['atk'], r['dmg'], r['crit'],
                '/'.join(r['stun']), lim or '-', '; '.join(r['others']) or '-', val))
        L.append('')
    L += ['## 기절 확률을 바꾸는 장신구·기벽', '', '| 종류 | id | 이름 | 직업 | 등급 | 기절 확률 |', '|---|---|---|---|---|---|']
    for row in sorted(buffs_related()):
        L.append('| %s |' % ' | '.join(str(x) for x in row))
    L.append('')
    tau, mult, rho, act = monster_ranks()
    stun_res = {r: [] for r in (1, 2, 3, 4)}
    L += ['## 몬스터 열별 (영웅 등급 편성)', '', '| 열 | 행동당 위협도(HP+스트레스) | 평균 대비 | 영웅 피해 기술이 닿는 비율 |', '|---|---|---|---|']
    for r in (1, 2, 3, 4):
        L.append('| %d | %.2f | %.2f | %.2f |' % (r, tau[r], mult[r], rho[r]))
    L += ['', '- 몬스터 1행동 평균 위협 %.2f HP. 단일 기절은 닿는 열 중 가장 위협적인 열을 고른다고 본다(모델 `rw = max(mult)`).' % act,
          '- 영웅 등급 몬스터 기절 저항: 평균 %.0f%%, 중앙값 %.0f%% (%d종).' % (st.mean(m['stun'] for m in S.MONS) * 100 if st.mean(m['stun'] for m in S.MONS) < 5 else st.mean(m['stun'] for m in S.MONS),
                                                                       st.median(m['stun'] for m in S.MONS) * 100 if st.median(m['stun'] for m in S.MONS) < 5 else st.median(m['stun'] for m in S.MONS), len(S.MONS)), '']
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
    print('ok', len(R['rb']), len(R['vanilla']))


if __name__ == '__main__':
    main()
