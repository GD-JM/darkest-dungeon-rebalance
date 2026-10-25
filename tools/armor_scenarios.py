"""Finite HP-capped setup versus immediate attack, and complete effect ledger.

The setup comparison deliberately isolates direct damage + armor reduction.
It is not the total value of the skill; no time is allowed for target recasts.
All follow-ups happen before the armor debuff expires.
"""
import sys,pathlib,json,functools,math,statistics as st
import strength as S
import armor_valuation as V
D=V.D

def attack_outcomes(weapon,modifier,crit,acc,dodge,prot):
    h=S.hit_probability(acc,dodge);normal,critical=S.damage_distribution(weapon,modifier,prot)
    return [(0,1-h)]+[(x,h*(1-crit)/len(normal)) for x in normal]+[(critical,h*crit)]

def finite_after_setup(H,row,eff,buffs,prot,hp,n,profiles,dodge=20,resist=.6):
    d=S.kv(row);acc=S.num(S.first(d,'atk'));crit=(H['wcrit']+S.num(S.first(d,'crit')))/100
    if S.first(d,'is_crit_valid','True').lower()!='true':crit=0.
    groups=D.groups(S,[eff.get(x,'') for x in S.ec.effect_names_in(row)],buffs,S.PARAM,False)
    armor=next((g for g in groups if g['mods'].get('protection_rating')),None)
    down=armor['mods']['protection_rating'] if armor else 0.
    @functools.lru_cache(maxsize=None)
    def future(left,n,p):
        if not n or left<=0:return 0.
        total=0.
        for weapon,atk,c,dm in profiles:
            for damage,q in attack_outcomes(weapon,dm,c,atk,dodge,p):
                loss=min(left,damage);total+=q*(loss+future(left-loss,n-1,p))/len(profiles)
        return total
    direct=S.num(S.first(d,'dmg'));normal,critical=S.damage_distribution(H['dmg'],direct,prot)
    if direct<=-100:normal=(0,);critical=0
    h=S.hit_probability(acc,dodge);total=0.
    branches=[(0,1-h,False,False)]+[(x,h*(1-crit)/len(normal),True,False) for x in normal]+[(critical,h*crit,True,True)]
    for damage,p,landed,c in branches:
        left=max(0,hp-damage);q=D.clamp(armor['chance']+(armor['crit_bonus'] if c else 0)-resist) if armor and landed else 0.
        total+=p*(hp-left+q*future(left,n,max(0,prot-down))+(1-q)*future(left,n,prot))
    baseline=0.
    for damage,p in attack_outcomes(H['dmg'],0,H['wcrit']/100,105,dodge,prot):
        left=max(0,hp-damage);baseline+=p*(hp-left+future(left,n,prot))
    return dict(setup_hp=total,basic_hp=baseline,delta_hp=total-baseline,delta_pp=V.contribution(total-baseline))

def run(output):
    R=pathlib.Path(output)
    inv=json.loads((R/'inventory.json').read_text(encoding='utf-8'))
    buffs=S.ec.load_buffs(S.G,S.M_ROOT);eff=S.load_effects('rb')
    profiles=tuple((tuple(S.load_hero(h,'rb')['dmg']),105,S.load_hero(h,'rb')['wcrit']/100,0.) for h in ('crusader','leper','bounty_hunter'))
    out={'finite_scenario':{'hp':60,'dodge':20,'debuff_resist':60,'followup_classes':['crusader','leper','bounty_hunter'],'window':'all followups before expiry','baseline':'same caster actual weapon, basic ACC105, no skill crit'},'skills':{},'monster_counts':{},'ignored_enemy_effect_keys':{}}
    for key,entry in inv['skills'].items():
        h,id=key.split('|');H=S.load_hero(h,'rb');row=entry['rb'][-1]['row']
        armor=any(g['mods'].get('protection_rating',0)>0 for g in D.groups(S,[eff.get(n,'') for n in S.ec.effect_names_in(row)],buffs,S.PARAM,False))
        item={'levels':[], 'effects':[]}
        for r in entry['rb']:
            groups=D.groups(S,r['effects'],buffs,S.PARAM,False);g=next((x for x in groups if x['mods'].get('protection_rating')),None)
            item['levels'].append(dict(level=r['level'],weapon=r['weapon'],weapon_crit=r['weapon_crit'],accuracy=S.num(S.first(r['stats'],'atk')),skill_crit=S.num(S.first(r['stats'],'crit')),damage=S.num(S.first(r['stats'],'dmg')),armor=g))
        for n in S.ec.effect_names_in(row):
            text=eff.get(n,'');k=S.kv(text)
            item['effects'].append(dict(id=n,fields=k,buffs={bid:buffs.get(bid.strip('"')) for bid in k.get('buff_ids',[])}))
        if armor and '~' not in S.first(S.kv(row),'target'):
            item['finite']={str(p):{str(n):finite_after_setup(H,row,eff,buffs,p/100,60,n,profiles) for n in range(5)} for p in (20,40,60)}
        out['skills'][key]=item
    for tier in 'ABC':
        rows,skipped=V.rank_cases(tier);pool=V.monster_pool(tier)
        out['monster_counts'][tier]=dict(combatants=len(pool),formations=len(rows),excluded_formations=len(skipped),zero_dodge=[m['name'] for m in pool if m['dodge']==0],monsters=pool)
    puncture=inv['skills']['shieldbreaker|break_guard']['rb'][-1]['stats']
    opening_hit=S.hit_probability(S.num(S.first(puncture,'atk')),20)
    guard_gain=st.mean(S.hit_probability(acc,20)*(S.damage_mean(weapon,mod,crit,.4)-S.damage_mean(weapon,mod,crit,.75)) for weapon,acc,crit,mod in profiles)
    out['guard_scenario']=dict(guard_protector_prot=75,intended_target_prot=40,dodge=20,opening_hit=opening_hit,notes='Existing guard clears on hit AND miss; preventing a new guard requires hit. Extra armor-free future damage only; no inferred guard encounter frequency',
                              one_followup_hp=guard_gain,one_followup_pp=V.contribution(guard_gain))
    # Inspect native enemy effects to disclose anything beyond direct/stress/DOT/stun.
    known={'effect:','name','target','chance','on_hit','on_miss','queue','stress','dotBleed','dotPoison','stun','duration','curio_result_type','has_description','crit_doesnt_apply_to_roll','dotHpHeal','instant_hp','combat_stat_buff','keyStatus'}
    for m in V.monster_pool('C'):
        for a in V.enemy_actions(m['name'],()):
            for text in a['effects']:
                k=S.kv(text)
                for field in k.keys()-known:
                    out['ignored_enemy_effect_keys'].setdefault(field,[])
                    if m['name'] not in out['ignored_enemy_effect_keys'][field]:out['ignored_enemy_effect_keys'][field].append(m['name'])
    (R/'extra-scenarios.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('finite scenarios',sum(len(v.get('finite',{}))*5 for v in out['skills'].values()))
    for key,v in out['skills'].items():
        if 'finite' in v:print(key,{p:[round(r['delta_hp'],2) for r in rows.values()] for p,rows in v['finite'].items()})
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=pathlib.Path)
    run(ap.parse_args().output)
