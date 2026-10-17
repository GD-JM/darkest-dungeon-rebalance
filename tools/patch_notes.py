"""패치 노트의 '무엇이 바뀌었나'를 바닐라 vs 창작마당판 데이터에서 자동으로 만든다(주석에 의존하지 않음).
build_workshop.py가 사용. 단독 실행: python tools/patch_notes.py <출력 폴더>  → 영웅별 차이 미리보기."""
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
import strength as S
import effect_common as ec

G = S.G
LBL = {
    'en': dict(atk='Accuracy', dmg='Damage', crit='Crit', launch='Usable ranks', target='Targets', per_battle_limit='Uses per battle', per_turn_limit='Uses per turn', ignore_protection='Ignores armor', ignore_stealth='Ignores stealth', ignore_guard='Ignores guard',
               move='Move', is_crit_valid='Can crit', added='Added', removed='Removed', changed='Changed', lvl='Lv1–5',
               weapon='Weapon', armour='Armor', resistances='Resists', mode='Form', none='none'),
    'ko': dict(atk='명중', dmg='피해', crit='치명 보정', launch='사용 열', target='대상', per_battle_limit='전투당 사용', per_turn_limit='턴당 사용', ignore_protection='방어 무시', ignore_stealth='은신 무시', ignore_guard='보호 무시', move='이동',
               is_crit_valid='치명 가능', added='추가', removed='제거', changed='변경', lvl='1~5렙',
               weapon='무기', armour='방어구', resistances='저항', mode='형태', none='없음'),
}
EFF_K = {
    'en': dict(stun='stun', bleed='bleed', poison='blight', burn='burn', heal='heal', healstress='stress heal', stress='stress',
               push='push', pull='pull', tag='mark', unstealth='destealth', corpse='clear corpses', guard='guard', torch_up='light +',
               torch_down='light −', cure='cure bleed/blight', self='self', party='party', ally='ally', t='turns', chance='chance',
               crit_received='crits taken', dmg_received='damage taken', shuffle='shuffle', acc='accuracy', dodge='dodge', prot='protection',
               spd='speed', dmgmod='damage', critc='crit', res='resist', stun_res='stun res', blight_res='blight res', bleed_res='bleed res',
               debuff_res='debuff res', move_res='move res', heal_recv='healing received', stress_recv='stress taken',
               stress_heal_recv='stress healing received', ignore_prot='armor piercing', cure_bleed='cure bleed', cure_poison='cure blight',
               untag='remove mark', unstun='remove stun', clear_debuff='clear debuffs', clear_riposte='end riposte', combat_end='until combat ends',
               is_guarded='while guarded', rule='if'),
    'ko': dict(stun='기절', bleed='출혈', poison='중독', burn='화상', heal='회복', healstress='스트레스 회복', stress='스트레스',
               push='밀치기', pull='당기기', tag='표식', unstealth='은신 해제', corpse='시체 제거', guard='보호', torch_up='횃불 +',
               torch_down='횃불 −', cure='출혈·중독 치료', self='자신', party='아군 전체', ally='아군', t='턴', chance='확률',
               crit_received='받는 치명타', dmg_received='받는 피해', shuffle='위치 섞기', acc='명중', dodge='회피', prot='방어',
               spd='속도', dmgmod='피해', critc='치명타', res='저항', stun_res='기절 저항', blight_res='중독 저항', bleed_res='출혈 저항',
               debuff_res='약화 저항', move_res='이동 저항', heal_recv='받는 회복', stress_recv='받는 스트레스',
               stress_heal_recv='받는 스트레스 회복', ignore_prot='방어 무시', cure_bleed='출혈 치료', cure_poison='중독 치료',
               untag='표식 해제', unstun='기절 해제', clear_debuff='약화 해제', clear_riposte='반격 종료', combat_end='전투 끝까지',
               is_guarded='보호받는 동안', rule='조건'),
}
STAT = {'attack_rating': 'acc', 'defense_rating': 'dodge', 'protection_rating': 'prot', 'speed_rating': 'spd',
        'damage_low': 'dmgmod', 'damage_high': 'dmgmod', 'crit_chance': 'critc'}
RES = {'stun': 'stun_res', 'poison': 'blight_res', 'bleed': 'bleed_res', 'debuff': 'debuff_res', 'move': 'move_res'}
BT = {'crit_received_chance': 'crit_received', 'damage_received_percent': 'dmg_received', 'hp_heal_received_percent': 'heal_recv',
      'stress_dmg_received_percent': 'stress_recv', 'stress_heal_received_percent': 'stress_heal_recv', 'ignore_protection': 'ignore_prot'}


def num(x):
    return S.num(x)


def pct(v):
    v = round(v, 2)
    return ('%+g%%' % v)


class Ctx:
    def __init__(self, eff, buffs):
        self.eff, self.buffs = eff, buffs

    def summary(self, name, lang):
        """효과 하나 → 짧은 문구 (대상·수치·확률·지속)"""
        L = EFF_K[lang]
        line = self.eff.get(name, '')
        k = S.kv(line)
        if not k:
            return name
        tgt = S.first(k, 'target', 'target')
        who = {'performer': L['self'], 'performer_group': L['party'], 'performer_group_other': L['party'], 'global': ''}.get(tgt, '')
        parts = []
        dur = S.first(k, 'duration', '')
        ch = S.first(k, 'chance', '')
        def add(s):
            parts.append(s)
        if 'stun' in k: add(L['stun'])
        for key, nm in (('dotBleed', 'bleed'), ('dotPoison', 'poison')):
            if key in k: add('%s %s×%s%s' % (L[nm], S.first(k, key), dur or '3', L['t'] if lang == 'ko' else 't'))
        if 'dotBurn' in k: add('%s %s' % (L['burn'], S.first(k, 'dotBurn')))
        if 'heal' in k: add('%s %s' % (L['heal'], S.first(k, 'heal')))
        if 'healstress' in k: add('%s %s' % (L['healstress'], S.first(k, 'healstress')))
        if 'stress' in k: add('%s +%s' % (L['stress'], S.first(k, 'stress')))
        if 'push' in k: add('%s %s' % (L['push'], S.first(k, 'push')))
        if 'pull' in k: add('%s %s' % (L['pull'], S.first(k, 'pull')))
        if 'tag' in k: add(L['tag'])
        if 'unstealth' in k: add(L['unstealth'])
        if 'shuffletarget' in k: add(L['shuffle'])
        if 'kill_enemy_types' in k: add(L['corpse'])
        if 'guard' in k: add(L['guard'])
        if 'cure' in k: add(L['cure'])
        for key in ('cure_bleed', 'cure_poison', 'untag', 'unstun', 'clear_debuff', 'clear_riposte'):
            if key in k: add(L[key])
        if 'torch_increase' in k: add('%s%s' % (L['torch_up'], S.first(k, 'torch_increase')))
        if 'torch_decrease' in k: add('%s%s' % (L['torch_down'], S.first(k, 'torch_decrease')))
        for key in k:
            if key.endswith(('_add', '_multiply')) and 'rating' in key or key in ('damage_low_multiply', 'crit_chance_add'):
                base = key.replace('_add', '').replace('_multiply', '')
                if base == 'damage_high':
                    continue
                st = STAT.get(base)
                if st:
                    v = num(S.first(k, key))
                    add('%s %s' % (L[st], ('%+g' % v) if base == 'speed_rating' else pct(v)))
        if 'buff_type' in k:
            bt = S.first(k, 'buff_type'); a = str(S.first(k, 'buff_amount'))
            v = num(a) if a.endswith('%') else num(a) * 100
            add('%s %s' % (L.get(BT.get(bt, ''), bt), pct(v)))
        for bid in k.get('buff_ids', []):
            B = self.buffs.get(bid.strip('"'))
            if not B:
                continue
            st_, sub, amt = B.get('stat_type'), B.get('stat_sub_type', ''), B.get('amount', 0)
            rt = B.get('rule_type', 'always')
            if rt not in ('always', None, ''):
                rd_ = B.get('rule_data', {}).get('string', '')
                ST = {'tagged': ('marked', '표식'), 'stunned': ('stunned', '기절'), 'bleeding': ('bleeding', '출혈'), 'poisoned': ('blighted', '중독')}
                if rt in ('actorStatus', 'is_actor_status') and rd_ in ST:
                    rs = ('while %s' if lang == 'en' else '%s 상태일 때') % ST[rd_][0 if lang == 'en' else 1]
                elif rt == 'skill':
                    sn = next((v for k_, v in getattr(self, 'skill_names', {}).get(lang, {}).items() if k_.endswith('_' + rd_)), rd_.replace('_', ' ').title())
                    rs = ('%s only' if lang == 'en' else '%s 전용') % sn
                else:
                    rs = L.get(rt) or '%s %s' % (L['rule'], rt)
                add = lambda x, rs=rs: parts.append('%s (%s)' % (x, rs))
            else:
                add = parts.append
            if st_ in ('combat_stat_add', 'combat_stat_multiply') and STAT.get(sub):
                if sub == 'damage_high':
                    continue
                add('%s %s' % (L[STAT[sub]], ('%+g' % amt) if sub == 'speed_rating' else pct(amt * 100)))
            elif st_ == 'resistance' and sub in RES:
                add('%s %s' % (L[RES[sub]], pct(amt * 100)))
            elif st_ in BT:
                add('%s %s' % (L[BT[st_]], pct(amt * 100)))
        if not parts:
            return None
        s = ', '.join(parts)
        cond = S.first(k, 'keyStatus', '').strip('"')
        mt = S.first(k, 'monsterType', '').strip('"')
        if cond or mt:
            cn = {'tagged': ('vs marked', '표식 대상'), 'stunned': ('vs stunned', '기절 대상'), 'bleeding': ('vs bleeding', '출혈 대상'),
                  'poisoned': ('vs blighted', '중독 대상'), 'burning': ('vs burning', '화상 대상')}.get(cond, (cond, cond)) if cond else                  (('vs ' + mt, mt + ' 대상'))
            s = '%s: %s' % (cn[0] if lang == 'en' else cn[1], s)
            who = ''
        if who:
            s = '%s: %s' % (who, s)
        if ch and ch.rstrip('%') not in ('100', '') and ('stun' in k or 'dotBleed' in k or 'dotPoison' in k or 'push' in k or 'pull' in k or 'buff_ids' in k or 'combat_stat_buff' in k or 'buff_type' in k or 'healstress' in k):
            s += ' (%s)' % ch
        if S.first(k, 'buff_duration_type', '') == 'combat_end':
            s += ' ' + L['combat_end']
        elif dur and not ('dotBleed' in k or 'dotPoison' in k):
            s += ' %s%s' % (dur, L['t'] if lang == 'ko' else 't')
        return s


def fmt_ranks(s, lang):
    s = s or ''
    aoe = s.startswith('~') or '~' in s
    ally = '@' in s
    r = '·'.join(re.sub(r'[^1-4]', '', s))
    if not r:
        return '—'
    pre = ('AoE ' if lang == 'en' else '광역 ') if aoe else ''
    pre += ('ally ' if lang == 'en' else '아군 ') if ally else ''
    return pre + r


def seq(vals):
    vals = [v for v in vals]
    return vals[0] if len(set(vals)) == 1 else '/'.join(vals)


def skill_diff(sid, vl, wl, ctx, lang):
    """같은 기술의 바닐라 줄들 vs 창작마당 줄들 → 문구 목록"""
    L = LBL[lang]
    out = []
    vd = [S.kv(l) for l in vl]; wd = [S.kv(l) for l in wl]
    for f in ('atk', 'dmg', 'crit'):
        a = [S.first(d, f, '') for d in vd]; b = [S.first(d, f, '') for d in wd]
        if a != b:
            if f in ('atk', 'crit'):
                out.append('%s %s → %s' % (L[f], a[0] or '—', b[0] or '—'))      # 1렙 값(성장 고정)
            else:
                out.append('%s %s → %s' % (L[f], seq(a), seq(b)))
    for f in ('launch', 'target'):
        a, b = S.first(vd[0], f, ''), S.first(wd[0], f, '')
        if a != b:
            out.append('%s %s → %s' % (L[f], fmt_ranks(a, lang), fmt_ranks(b, lang)))
    a = [' '.join(d.get('heal', [])) for d in vd]; b = [' '.join(d.get('heal', [])) for d in wd]
    if a != b:
        hl = 'Heal' if lang == 'en' else '회복'
        def f1(x):
            x = [v.replace(' ', '-') or '—' for v in x]
            return x[0] if len(set(x)) == 1 else '%s … %s' % (x[0], x[-1])
        out.append('%s %s → %s' % (hl, f1(a), f1(b)))
    for f in ('per_battle_limit', 'per_turn_limit', 'move', 'is_crit_valid', 'ignore_protection', 'ignore_stealth', 'ignore_guard'):
        a = ' '.join(vd[0].get(f, [])) or L['none']; b = ' '.join(wd[0].get(f, [])) or L['none']
        if a != b:
            out.append('%s %s → %s' % (L[f], a, b))
    # 효과: 레벨마다 요약 목록을 만들고 차이를 모은다
    def effs(l):
        return [ctx.summary(n, lang) for n in ec.effect_names_in(l)]
    va = [[x for x in effs(l) if x] for l in vl]; wa = [[x for x in effs(l) if x] for l in wl]
    if va != wa:
        rem = {}; addd = {}
        for lv, (a, b) in enumerate(zip(va, wa)):
            for x in a:
                if x not in b: rem.setdefault(lv, []).append(x)
            for x in b:
                if x not in a: addd.setdefault(lv, []).append(x)
        def agg(d):
            if not d:
                return None
            lv_lists = [tuple(d.get(i, [])) for i in range(len(vl))]
            if len(set(lv_lists)) == 1:
                return '; '.join(lv_lists[0])
            f = lambda x: '; '.join(x) if x else ('unchanged' if lang == 'en' else '변화 없음')
            return '%s1 %s … %s5 %s' % ('Lv' if lang == 'en' else '', f(lv_lists[0]), 'Lv' if lang == 'en' else '', f(lv_lists[-1])) if lang == 'en' else                    '1렙 %s … 5렙 %s' % (f(lv_lists[0]), f(lv_lists[-1]))
        r, a2 = agg(rem), agg(addd)
        if r and a2:
            out.append('%s → %s' % (r, a2))
        elif a2:
            out.append('%s: %s' % (L['added'], a2))
        elif r:
            out.append('%s: %s' % (L['removed'], r))
    return out


def line_diff(kind, vl, wl, lang):
    L = LBL[lang]
    out = []
    if kind == 'weapon':
        for f in ('dmg', 'crit', 'spd'):
            a = [' '.join(S.kv(l).get(f, [])) for l in vl]; b = [' '.join(S.kv(l).get(f, [])) for l in wl]
            if a != b:
                out.append('%s %s %s → %s' % (L['weapon'], f, ' / '.join(a), ' / '.join(b)))
    elif kind == 'armour':
        for f in ('def', 'prot', 'hp', 'spd'):
            a = [' '.join(S.kv(l).get(f, [])) for l in vl]; b = [' '.join(S.kv(l).get(f, [])) for l in wl]
            if a != b:
                out.append('%s %s %s → %s' % (L['armour'], f, ' / '.join(a), ' / '.join(b)))
    elif kind == 'resistances':
        a, b = S.kv(vl[0]), S.kv(wl[0])
        for k in a:
            if S.first(a, k) != S.first(b, k):
                out.append('%s %s %s → %s' % (L['resistances'], k, S.first(a, k), S.first(b, k)))
    else:
        out.append('%s → %s' % (vl[0].split(':', 1)[1].strip()[:80], wl[0].split(':', 1)[1].strip()[:80]))
    return out


def hero_diff(hero, wfile, ctx, lang):
    """[(블록키, [문구])] — 기술은 combat_skill id(모드별 분리), 그 밖은 줄 종류"""
    van = [l for l in open(ec.vanilla_hero_file(G, hero), encoding='utf-8', errors='ignore').read().splitlines() if l.strip() and not l.startswith('//')]
    wor = [l for l in open(wfile, encoding='utf-8', errors='ignore').read().splitlines() if l.strip() and not l.startswith('//')]
    res = []
    def groups(lines):
        g = {}
        for l in lines:
            if l.startswith('combat_skill:'):
                d = S.kv(l); key = ('skill', S.first(d, 'id'), S.first(d, 'valid_modes', ''))
            else:
                key = (l.split(':')[0], '', '')
            g.setdefault(key, []).append(l)
        return g
    gv, gw = groups(van), groups(wor)
    for key in gw:
        a, b = gv.get(key, []), gw[key]
        if a == b:
            continue
        if key[0] == 'skill' and len(a) == len(b):
            dl = skill_diff(key[1], a, b, ctx, lang)
            if dl:
                res.append((key, dl))
        elif key[0] in ('weapon', 'armour', 'resistances') and len(a) == len(b):
            res.append((key, line_diff(key[0], a, b, lang)))
        elif key[0] == 'mode':
            for x, y in zip(a, b):
                if x != y:
                    m1 = re.search(r'\.stress_damage_per_turn (\d+)', x); m2 = re.search(r'\.stress_damage_per_turn (\d+)', y)
                    if m1 and m2:
                        res.append((key, ['%s %s → %s' % ('Beast stress per turn' if lang == 'en' else '짐승 형태 턴당 스트레스', m1.group(1), m2.group(1))]))
        elif a != b:
            res.append((key, ['(%s)' % key[0]]))
    return res


def make_ctx(out_dir):
    eff = {k: v[0] for k, v in ec.load_vanilla_effects(G).items()}
    for f in glob.glob(os.path.join(out_dir, 'effects', '*.effects.darkest')):
        for l in open(f, encoding='utf-8').read().splitlines():
            m = re.match(r'effect:\s*\.name\s+"([^"]+)"', l)
            if m:
                eff[m.group(1)] = l
    buffs = ec.load_buffs(G)
    for f in glob.glob(os.path.join(out_dir, 'shared', 'buffs', '*.json')):
        for b in json.load(open(f, encoding='utf-8'))['buffs']:
            buffs[b['id']] = b
    return Ctx(eff, buffs)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    out = sys.argv[1]
    ctx = make_ctx(out)
    for f in sorted(glob.glob(os.path.join(out, 'heroes', '*', '*.info.darkest'))):
        hero = os.path.basename(f).split('.')[0]
        print('==', hero)
        for key, lines in hero_diff(hero, f, ctx, 'en'):
            print('  ', key[1] or key[0], '|', ' ; '.join(lines))
