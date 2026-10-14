"""열 조건으로 영웅 기술 전수 조사 (RB, 1렙 수치 + 효과 1~5렙, 모델(5렙)).
사용: python tools/reach34_survey.py          -> design/analysis/reach34_survey.md (3·4열을 칠 수 있는 기술)
      python tools/reach34_survey.py aoe23    -> design/analysis/aoe23_survey.md  (2·3열을 동시에 치는 광역)"""
import sys, io, os, re, subprocess, datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
import strength as S
import stun_survey as SS

MODE = sys.argv[1] if len(sys.argv) > 1 else 'reach34'
OUT = os.path.join(os.path.dirname(__file__), '..', 'design', 'analysis', '%s_survey.md' % MODE)
TITLE = {'reach34': '3·4열을 칠 수 있는 기술', 'aoe23': '2·3열을 동시에 치는 광역 기술'}[MODE]


def want(tg):
    if '@' in tg:
        return False
    if MODE == 'aoe23':
        return tg.startswith('~') and '2' in tg and '3' in tg
    return bool(re.search(r'[34]', tg))
E = S.load_effects('rb')


def per_level(lvs, key):
    """레벨별 같은 자리 효과의 key 값 (예: dotBleed 1/1/2/2/3)"""
    out = []
    for lv in sorted(lvs):
        names = S.ec.effect_names_in(lvs[lv][0])
        v = '-'
        for n in names:
            k = S.kv(E.get(n, ''))
            if key in k and S.first(k, 'target', '') in ('target', 'target_group'):
                v = S.first(k, key).rstrip('%')
                if key in ('dotBleed', 'dotPoison', 'dotBurn'):
                    v += '×' + S.first(k, 'duration', '?')
                break
        out.append(v)
    return '/'.join(out) if any(x != '-' for x in out) else ''


def main():
    head = subprocess.run(['git', 'log', '--oneline', '-1'], capture_output=True, text=True, encoding='utf-8', cwd=S.M_ROOT).stdout.strip()
    R = S.run()['rb']
    rows = []
    for hero in S.KO:
        t = open(S.hero_file(hero, 'rb'), encoding='utf-8', errors='ignore').read()
        by = {}
        for l in t.splitlines():
            if l.startswith('combat_skill:'):
                d = S.kv(l)
                by.setdefault((S.first(d, 'id'), S.first(d, 'valid_modes', '')), {})[int(S.first(d, 'level', '0'))] = (l, d)
        for (sid, modes), lvs in by.items():
            l0, d0 = lvs[min(lvs)]
            tg = S.first(d0, 'target', '')
            if not want(tg):
                continue
            dmg = S.num(S.first(d0, 'dmg', '-100'))
            names = S.ec.effect_names_in(l0)
            others = [SS.eff_summary(E[n]) for n in names if n in E]
            sk = R[hero]['skills'].get(sid)
            rows.append(dict(ko=S.KO[hero], name=SS.KO.get('combat_skill_name_%s_%s' % (hero, sid), sid), sid=sid, modes=modes, type=S.first(d0, 'type', ''),
                             launch='·'.join(S.first(d0, 'launch', '')), target=tg, atk=S.first(d0, 'atk', '-'), dmg=dmg, crit=S.first(d0, 'crit', '-'),
                             limit=S.first(d0, 'per_battle_limit', ''), bleed=per_level(lvs, 'dotBleed'), poison=per_level(lvs, 'dotPoison'),
                             burn=per_level(lvs, 'dotBurn'), stun=per_level(lvs, 'stun') and per_level(lvs, 'chance'),
                             ign=' '.join(x for x in ('ignore_protection', 'ignore_guard', 'ignore_stealth') if S.first(d0, x, 'false').lower() == 'true'),
                             eff='; '.join(others), val=((sk[0] / 7.7 - 1) * 100) if sk else None,
                             parts={k: round(x / 7.7 * 100) for k, x in sk[1].items()} if sk else {}))
    L = ['# %s 전수 조사 (RB)' % TITLE, '',
         '- 생성: %s, 데이터 커밋 `%s`, `python tools/reach34_survey.py%s`로 다시 만든다.' % (datetime.date.today(), head, '' if MODE == 'reach34' else ' ' + MODE),
         '- 조건: %s, 적 대상 기술 전부(손으로 고른 목록 없음).' % TITLE + ' 명중·치명 보정은 1렙, 지속 피해는 "턴당×턴" 1~5렙, 모델(5렙) 표준 평타 7.7 HP 기준 %p.', '']
    for title, cond in (('피해 있는 공격', lambda r: r['dmg'] > -100), ('피해 없는 기술', lambda r: r['dmg'] <= -100)):
        sel = sorted([r for r in rows if cond(r)], key=lambda r: (r['target'].lstrip('~'), r['ko']))
        L += ['## %s %d개' % (title, len(sel)), '',
              '| 영웅 | 기술 | 형태 | 사용 → 대상 | 명중 | 피해 | 치명 | 출혈 | 중독 | 화상 | 제한·모드·관통 | 모델(5렙) | 구성 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        for r in sel:
            lim = ' '.join(x for x in (('전투당 %s회' % r['limit']) if r['limit'] else '', r['modes'], r['ign']) if x)
            L.append('| %s | %s | %s | %s → %s | %s | %+.0f%% | %s | %s | %s | %s | %s | %s | %s |' % (
                r['ko'], r['name'], '근접' if r['type'] == 'melee' else '원거리', r['launch'], r['target'], r['atk'], r['dmg'], r['crit'],
                r['bleed'] or '-', r['poison'] or '-', r['burn'] or '-', lim or '-', ('%+.0f' % r['val']) if r['val'] is not None else '-',
                ' '.join('%s%+d' % (k, v) for k, v in r['parts'].items())))
        L.append('')
    L += ['## 효과 원문 (1렙)', '']
    for r in sorted(rows, key=lambda r: (r['ko'], r['sid'])):
        L.append('- %s %s: %s' % (r['ko'], r['name'], r['eff'] or '-'))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('ok', len(rows))


if __name__ == '__main__':
    main()
