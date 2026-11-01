"""R-DLC-029: state-conditioned corrections to the shared HP valuation.

All seven skills of each Fires Edge hero are dispatched explicitly. This is a
finite-exposure valuation, NOT a whole-game AI simulator. Scenario values are
assumptions, never observations. The caller can pin ranks/HP/burn/stance/turns.
No equipment is assumed; equipment-derived modifiers can be supplied explicitly.
"""
from dataclasses import dataclass, replace
import math
import re
import statistics as st

SKILLS = {
 'duelist': ('anticipation','touche','feint','disengage','fleche','coup_de_grace','the_boot'),
 'runaway': ('searing_strike','firefly','run_and_hide','ransack','hearthlight','controlled_burn','backdraft'),
}

@dataclass(frozen=True)
class State:
    # None rank = legal-use valuation, not permission to execute from any rank.
    rank: int | None = None
    target_rank: int | None = None
    stance: str = 'stance_defensive'
    target_hp: float | None = None  # None uses each monster's full HP.
    target_stunned: bool = False
    burn: int = 0
    rear_burn: int = 0
    rear_exists: bool = True
    rear_hp: float | None = None
    remaining_enemies: int = 2
    rounds: int = 3
    actions_per_round: int = 1
    target_acted: bool = False
    zone_entries: tuple = ()  # actual successful additional entries per round
    slow: float = 0.0
    slow_events: int = 0
    slow_layers: tuple = ()  # Additional (amount, remaining target-action events).
    riposte_active: bool = True
    marked: bool = False
    stealthed: bool = False
    any_position: bool = False
    cb_uses: int = 0
    turn_uses: int = 0
    missing_hp: float = 15.0
    future_hot_ticks: int = 1
    party_followup_attacks: float = 3.0
    followup_action_hp: float = 7.17
    riposte_damage_bonus: float = 0.0
    damage_bonus: float = 0.0
    acc_bonus: float = 0.0
    crit_bonus: float = 0.0
    burn_bonus: float = 0.0
    dodge_bonus: float = 0.0
    corpses: int = 0
    # No population claim: explicit conditional probabilities for generic tables.
    stunned_share: float = 0.201
    burning_share: float = 0.3
    guarded_share: float = 0.0
    followup_target_rank: int | None = None  # None averages four desired ranks equally.
    rank4_windows: float = 1.0  # Future exposure after Disengage; not measured uptime.

def state(C):
    return State(**C.P.get('DLC_STATE', {}))

def rule_weight(C,b):
    """Known state predicates; None delegates unchanged shared-model rules."""
    if C.H['id'] not in SKILLS or not C.P.get('DLC_MODEL',True):return None
    q=state(C);rule=b.get('rule_type');data=b.get('rule_data') or {}
    if rule=='has_buff' and data.get('string')=='riposte':return float(q.riposte_active)
    if b.get('id','').startswith('DUELIST_DISENGAGE_DODGEBUFF'):
        # Casting from rank 1/2 retreats to 4 BEFORE the defensive exposure.
        return min(1.,max(0.,q.rank4_windows)/C.P['BUFF_DUR_CAP'])
    if C.P.get('DLC_STATE'):
        if rule=='in_rank' and q.rank is not None:return float(q.rank==int(data['float'])+1)
        if rule=='in_mode':return float(q.stance==data['string'])
        if rule=='is_stealthed':return float(q.stealthed)
        if rule in ('actorStatus','is_actor_status') and data.get('string')=='burning':return float(q.burn>0)
    return None

def decay(burn, slow=0.):
    """REA 1405ba630: split integer loss before applying recovery fraction."""
    b=max(0,int(burn)); return b//2 + int((b-b//2)*max(0.,min(1.,slow)))

def burn_trace(initial, rounds=3, zone=0, zone_rounds=0, actions=1,
               acted=False, slow=0., slow_events=0, entries=(), hp=None, slow_layers=()):
    """Zone lifetime is round-based; burn/slow lifetime is target-action-based.

    Ground triggers before burn. Entries must be successful entries, NOT attempts.
    Survivors are explicit. Damage is capped to remaining HP when supplied.
    On death the trace exposes burn to a corpse/wildfire recipient; it does not
    invent adjacency or add a free party-wide explosion.
    """
    b=int(initial); left=float('inf') if hp is None else hp; total=0; trace=[]
    layers=[[float(s),int(n)] for s,n in slow_layers]
    for r in range(rounds):
        if r < zone_rounds: b += zone*(entries[r] if r<len(entries) else 0)
        count=actions-(1 if r==0 and acted else 0)
        for _ in range(max(0,count)):
            if left<=0: break
            if r<zone_rounds:b+=zone
            hit=min(left,b); left-=hit; total+=hit
            trace.append({'round':r,'stacks':b,'damage':hit,'dead':left<=0})
            if left<=0:return total,b,trace
            b=decay(b,(slow if slow_events>0 else 0.)+sum(s for s,n in layers if n>0))
            slow_events=max(0,slow_events-1)
            for layer in layers:layer[1]=max(0,layer[1]-1)
    return total,b,trace

def wildfire_payload(stacks, corpse_left, adjacent_count, both=False):
    """Glossary: corpse retains burn; otherwise half to one random neighbour.
    Odd-stack rounding is a declared floor assumption, not runtime verification.
    """
    if corpse_left or adjacent_count<=0:return 0,0
    return int(stacks)//2, min(adjacent_count,2) if both else 1

def consume_dodge_factor(hit_with_buff, expected_attacks):
    """Poisson exposure: E[active attacks]/E[attacks], buff ends on first dodge."""
    x=max(0.,expected_attacks)*(1-hit_with_buff)
    return -math.expm1(-x)/x if x else 1.

def kill_probability(normal, critical, crit, hit, hp):
    return hit*((1-crit)*sum(x>=hp for x in normal)/len(normal)+crit*(critical>=hp))

def legal(S, d, q):
    if q.rank is not None and not q.any_position and str(q.rank) not in S.first(d,'launch'):return False
    if q.target_rank is not None and not q.any_position and S.first(d,'target') and str(q.target_rank) not in S.first(d,'target'):return False
    if 'valid_modes' in d and q.stance not in d['valid_modes']:return False
    if S.first(d,'requires_burning')=='true' and q.burn<=0:return False
    if 'per_battle_limit' in d and q.cb_uses>=S.num(S.first(d,'per_battle_limit')):return False
    if 'per_turn_limit' in d and q.turn_uses>=S.num(S.first(d,'per_turn_limit')):return False
    return True

def transition(S, d, q):
    """Deterministic launch/movement/stance/limit part of a successful cast."""
    if not legal(S,d,q):raise ValueError('illegal skill in pinned state')
    sid=S.first(d,'id'); r=q.rank
    if r is not None and 'move' in d:r=max(1,min(4,r+int(d['move'][0])-int(d['move'][1])))
    kw={'rank':r}
    if sid=='anticipation':kw.update(stance='stance_aggressive' if q.stance=='stance_defensive' else 'stance_defensive',riposte_active=True,turn_uses=q.turn_uses+1)
    if sid=='controlled_burn':kw['cb_uses']=q.cb_uses+1
    if sid=='disengage':kw['any_position']=True
    if sid=='run_and_hide':kw['stealthed']=r is None or r>=3
    elif S.first(d,'target'):kw['stealthed']=False
    return replace(q,**kw)

def next_wave(q, refresh=True):
    return replace(q, cb_uses=0 if refresh else q.cb_uses, turn_uses=0)

def effects(S,C,line):
    return [S.kv(C.eff[n]) for n in S.ec.effect_names_in(line) if n in C.eff]

def buff_rows(S,C,es):
    return [(e,C.buffs[n.strip('"')]) for e in es for n in e.get('buff_ids',[]) if n.strip('"') in C.buffs]

def prepare(S,C,line,d):
    """Only the source stance's transition effects fire, not both lists."""
    if C.H['id']!='duelist' or S.first(d,'id')!='anticipation':return line,d
    q=state(C); chosen=q.stance+'_effects'
    selected=re.search(r'\.'+chosen+r'\b(.*?)(?=\s+\.[A-Za-z_]|$)',line)
    line=re.sub(r'\.stance_(?:defensive|aggressive)_effects\b.*?(?=\s+\.[A-Za-z_]|$)','',line)
    if selected:line+=' .effect '+selected.group(1).strip()
    return line,S.kv(line)

def direct(S,C,d,q,burn=0,stunned=False,modifier=None,enemy=None):
    monsters=[enemy] if enemy is not None else S.MONS
    cp=min(1.,max(0.,(C.H['wcrit']+S.num(S.first(d,'crit'))+q.crit_bonus)/100))
    es=effects(S,C,next((l for l,k in C.H['skills'] if S.first(k,'id')==S.first(d,'id')),''))
    bonus=q.damage_bonus
    for e in es:
        key=S.first(e,'keyStatus')
        if key=='stunned' and stunned:cp=min(1.,cp+S.num(S.first(e,'crit_chance_add'))/100)
        if key=='burning' and burn>0:bonus+=S.num(S.first(e,'damage_low_multiply'))/100
    bonus+=S.num(S.first(d,'dmg_per_burn_stack'))*burn
    acc=S.num(S.first(d,'atk'))+q.acc_bonus
    if q.stealthed and S.first(d,'id')=='ransack':
        for e,b in buff_rows(S,C,es):
            if b.get('rule_type')=='is_stealthed' and b.get('stat_sub_type')=='attack_rating':acc+=b['amount']*100
    dmg=S.num(S.first(d,'dmg')) if modifier is None else modifier
    vals=[];kills=[]
    for m in monsters:
        prot=0 if S.first(d,'ignore_protection')=='true' else m['prot']
        ns,cs=S.damage_distribution(C.H['dmg'],dmg,prot,bonus,C.P['DMG_STACK'])
        hit=S.hit_probability(acc,m['dodge']);hp=q.target_hp if q.target_hp is not None else m['hp']
        vals.append(hit*((1-cp)*st.mean(min(hp,x) for x in ns)+cp*min(hp,cs)))
        kills.append(kill_probability(ns,cs,cp,hit,hp))
    return st.mean(vals),st.mean(kills),cp,st.mean(S.hit_probability(acc,m['dodge']) for m in monsters)

def reach_delta(S,C,q,after_rank=4):
    """Next direct attack with/without Disengage override, same target profile.
    Desired rank is explicit or an equal four-rank sensitivity assumption.
    No fixed invented price; no free attack is awarded, only increased access.
    """
    gains=[]
    for target in ([q.followup_target_rank] if q.followup_target_rank else range(1,5)):
        ordinary=[0.]; unrestricted=[0.]
        for _,k in C.H['skills']:
            if S.num(S.first(k,'atk'))<=0 or S.num(S.first(k,'dmg'))<=-100:continue
            v=direct(S,C,k,q,burn=q.burn,stunned=q.target_stunned)[0]
            unrestricted.append(v)
            if str(after_rank) in S.first(k,'launch') and str(target) in S.first(k,'target'):ordinary.append(v)
        gains.append(max(unrestricted)-max(ordinary))
    return st.mean(gains)

def correct(S,C,line,d,parts):
    hero=C.H['id'];sid=S.first(d,'id')
    if hero not in SKILLS:return parts
    if sid not in SKILLS[hero]:raise ValueError('Uncovered DLC skill: '+sid)
    q=state(C);p=dict(parts);es=effects(S,C,line);bs=buff_rows(S,C,es)
    # Rankless tables mean conditional legal use. Pinned scenarios enforce ranks,
    # stance, counters, and target conditions instead of valuing impossible casts.
    explicit=bool(C.P.get('DLC_STATE'))
    if not explicit and sid in ('backdraft','hearthlight'):
        q=replace(q,burn=int(C.burn_left))
    if explicit and not legal(S,d,q):return {'사용 불가':0.}
    ranks=tuple(int(x) for x in re.sub('[^1-4]','',S.first(d,'target')))
    rw=max(S.formation_stats(C.P['STRESS_HP'])[1][r] for r in ranks) if ranks and C.P['RANK_MODEL'] else 1.
    dmg,kill,cp,hit=direct(S,C,d,q,burn=q.burn,stunned=q.target_stunned)
    if S.first(d,'is_crit_valid').lower()=='false':cp=0.
    if S.num(S.first(d,'atk'))>0 and S.num(S.first(d,'dmg'))>-100:
        if sid=='coup_de_grace' and not explicit:
            d2,k2,c2,_=direct(S,C,d,q,stunned=True)
            s=q.stunned_share;dmg=dmg*(1-s)+d2*s;kill=kill*(1-s)+k2*s;cp=cp*(1-s)+c2*s
        if sid=='searing_strike' and not explicit:
            d2,_,_,_=direct(S,C,d,q,burn=1);dmg=dmg*(1-q.burning_share)+d2*q.burning_share
        p['직접']=dmg*rw
        cb=sum(C.buff_ids_value(S.kv(C.eff.get(n,'')).get('buff_ids',[]),C.P['CRIT_BUFF_DUR'],'self') for n in C.H['crit_effects'])
        p['치명타']=hit*cp*(C.P['CRIT_STRESS']*C.P['STRESS_HP']+cb)
    if hero=='duelist':
        def riposte_crit_value():
            r=C.H.get('riposte',{});cp=(C.H['wcrit']+S.num(S.first(r,'crit'))+q.crit_bonus)/100
            h=st.mean(S.hit_probability(S.num(S.first(r,'atk'))+q.acc_bonus,m['dodge']) for m in S.MONS)
            cb=sum(C.buff_ids_value(S.kv(C.eff.get(n,'')).get('buff_ids',[]),C.P['CRIT_BUFF_DUR'],'self') for n in C.H['crit_effects'])
            return h*min(1,cp)*(C.P['CRIT_STRESS']*C.P['STRESS_HP']+cb)
        if sid=='touche':
            for e,b in bs:
                if b['id'].startswith('DUELIST_TOUCHE_DODGE_'):
                    duration=min(S.effect_duration(e,C.P),C.P['BUFF_DUR_CAP'])
                    full=C.stat_value('defense_rating',b['amount'],duration,'self')
                    h=st.mean(S.hit_probability(a,C.H['def']+q.dodge_bonus+b['amount']*100) for a in S.monster_attack_accs())
                    rate=C.P['HITS_TAKEN']/S.hit_probability(C.P['MON_HIT'],C.H['def']+q.dodge_bonus)
                    p['회피 소모 보정']=-full*(1-consume_dodge_factor(h,rate*duration))
        if sid=='coup_de_grace':
            p['처치 후 추가 행동']=kill*q.followup_action_hp*(q.remaining_enemies>1)
        if sid=='feint':
            # Remove generic normal-attack valuation of a riposte-only buff.
            for e,b in bs:
                if b.get('rule_type')=='riposte' and b.get('stat_sub_type') in ('damage_low','damage_high'):
                    dur=min(S.effect_duration(e,C.P),C.P['BUFF_DUR_CAP'])
                    old=C.P['COND_OTHER']*C.stat_value(b['stat_sub_type'],b['amount'],dur,'self')
                    p['반격 강화 정정']=p.get('반격 강화 정정',0)-old
            amount=max((b['amount'] for e,b in bs if b.get('rule_type')=='riposte'),default=0)
            if q.riposte_active:
                attempts=C.P['HITS_TAKEN']/S.hit_probability(C.P['MON_HIT'],C.H['def'])*C.P['BUFF_DUR_CAP']*C.P['MARK_DRAW']
                old=C.riposte(S.kv('.damage_low_multiply '+str(q.riposte_damage_bonus*100)+'%'))
                new=C.riposte(S.kv('.damage_low_multiply '+str((q.riposte_damage_bonus+amount)*100)+'%'))
                p['반격 강화 정정']=p.get('반격 강화 정정',0)+(new-old)*attempts
        if sid in ('feint','fleche') and q.riposte_active and not q.marked:
            attempts=C.P['HITS_TAKEN']/S.hit_probability(C.P['MON_HIT'],C.H['def'])*C.P['BUFF_DUR_CAP']*(C.P['MARK_DRAW']-1)
            # The mark refreshes; it does not stack. For recurring-action tables
            # amortize it like the free riposte upkeep, not a new 2-turn mark per turn.
            if not explicit:attempts/=C.P['BUFF_DUR_CAP']
            p['표식 반격 연계']=(C.riposte({})+riposte_crit_value())*attempts
        if sid=='disengage':p['다음 공격 사거리']=reach_delta(S,C,q)
        # Attack-stance-only Fleche drawback is data-driven, including proposals.
        for e,b in bs:
            if b.get('rule_type')=='in_mode' and b.get('stat_sub_type')=='defense_rating' and b['amount']<0:
                dur=min(S.effect_duration(e,C.P),C.P['BUFF_DUR_CAP'])
                p['자세 약화 정정']=C.stat_value('defense_rating',b['amount'],dur,'self')*(1-C.P['COND_OTHER'])
        if sid=='anticipation':
            # Start riposte is already active before a first skill. Price only the
            # opening -50% modifier during the declared pre-action exposure;
            # do not add a second free activation's full damage.
            # evaluate() divides the free skill by BUFF_DUR_CAP once more.
            opening=C.P.get('DLC_OPENING_EXPOSURE',0.5)*C.P['BUFF_DUR_CAP']/C.P['FIGHT_ACTS']
            p['개전 반격 대가']=(C.riposte(S.kv('.damage_low_multiply -50%'))-C.riposte({}))*opening
            attempts=C.P['HITS_TAKEN']/S.hit_probability(C.P['MON_HIT'],C.H['def'])*C.P['BUFF_DUR_CAP']
            p['반격 치명 부수효과']=attempts*riposte_crit_value()
        return p

    # Runaway: all burn terms are incremental against the SAME pre-existing burn.
    def trace(b,zone=0,zrounds=0,slow=None,events=None,hp=None):
        layers=list(q.slow_layers)
        if slow is not None and q.slow_events>0:layers.append((q.slow,q.slow_events))
        return burn_trace(b,q.rounds,zone,zrounds,q.actions_per_round,q.target_acted,
            q.slow if slow is None else slow,q.slow_events if events is None else events,q.zone_entries,hp,layers)[0]
    burn_eff=next((e for e in es if 'dotBurn' in e),None)
    zone_eff=next((e for e in es if 'controlled_burn_amount' in e),None)
    slow_buffs=[(e,b) for e,b in bs if b.get('stat_type')=='hp_dot_burn_decay_percent']
    if burn_eff or zone_eff or sid=='hearthlight':
        p.pop('화상',None)
        total=0.
        for m in S.MONS:
            h=S.hit_probability(S.num(S.first(d,'atk'))+q.acc_bonus,m['dodge'])
            slow=q.slow;events=q.slow_events;prob_slow=0.
            if slow_buffs:
                e,b=slow_buffs[0];requires=b.get('rule_type')=='is_actor_status' or S.first(e,'keyStatus')=='burning'
                if not requires or q.burn>0:
                    prob_slow=max(0,min(1,S.num(S.first(e,'chance','100'))/100-m['debuff']/100))
                    slow=b['amount']
                    raw=int(S.effect_duration(e,C.P))
                    events=raw if S.first(e,'buff_duration_type')=='after_turn' else max(0,raw-1)
            amount=S.num(S.first(burn_eff,'dotBurn')) if burn_eff else 0
            zone=int(S.num(S.first(zone_eff,'controlled_burn_amount'))) if zone_eff else 0
            zr=int(S.num(S.first(zone_eff,'controlled_burn_duration'))) if zone_eff else 0
            # Conditional finite-horizon damage; shared existing burn is subtracted.
            for iscrit,w in [(False,1-cp),(True,cp)]:
                if S.first(d,'is_crit_valid').lower()=='false':
                    if iscrit:continue
                    w=1.
                add=math.ceil(amount*(1+q.burn_bonus)*(1.5 if iscrit else 1))
                ps=min(1,prob_slow+(.2 if iscrit and prob_slow>0 else 0))
                z_hit=h if zone_eff and S.first(zone_eff,'on_miss')!='true' else 1.
                # Controlled Burn zone exists even on a missed initial hit.
                if zone_eff:
                    gain=h*trace(q.burn+add,zone,zr,hp=q.target_hp)+(z_hit-h)*trace(q.burn,zone,zr,hp=q.target_hp)+(1-z_hit)*trace(q.burn,hp=q.target_hp)-trace(q.burn,hp=q.target_hp)
                else:
                    # Respect damage before DOT and overkill at a pinned HP.
                    dm=S.num(S.first(d,'dmg'))
                    bonus=q.damage_bonus
                    if sid=='searing_strike' and q.burn>0:
                        bonus+=sum(S.num(S.first(e,'damage_low_multiply'))/100 for e in es if S.first(e,'keyStatus')=='burning')
                    ns,cs=S.damage_distribution(C.H['dmg'],dm,m['prot'],bonus,C.P['DMG_STACK'])
                    damage_cases=[cs] if iscrit else ns
                    if dm<=-100:damage_cases=[0]
                    gain=0.
                    for dhp in damage_cases:
                        hp=None if q.target_hp is None else max(0,q.target_hp-dhp)
                        gain+=h*((1-ps)*trace(q.burn+add,hp=hp)+ps*trace(q.burn+add,slow=slow,events=events,hp=hp)-trace(q.burn,hp=q.target_hp))/len(damage_cases)
                total+=w*gain/len(S.MONS)
        targets=len(ranks)*C.P['AOE_PER_RANK'] if '~' in S.first(d,'target') else 1
        p['화상 상태 변화']=total*targets*C.P['E_DOT_SGL']*rw
        if sid=='hearthlight' and not explicit:p['화상 상태 변화']*=q.burning_share
    if sid=='backdraft':
        if q.burn<=0:return {'화상 대상 필요':0.}
        rear=replace(q,burn=q.rear_burn,target_hp=q.rear_hp)
        rear_damage,_,rearcrit,rearhit=direct(S,C,d,rear,burn=q.rear_burn)
        p['직접']=dmg*rw
        if q.rear_exists:
            rear_rw=max(S.formation_stats(C.P['STRESS_HP'])[1][min(r+1,4)] for r in ranks) if ranks and C.P['RANK_MODEL'] else 1.
            p['뒤 대상 직접']=rear_damage*rear_rw
            cb=sum(C.buff_ids_value(S.kv(C.eff.get(n,'')).get('buff_ids',[]),C.P['CRIT_BUFF_DUR'],'self') for n in C.H['crit_effects'])
            p['치명타']=hit*(cp+rearcrit-cp*rearcrit)*(C.P['CRIT_STRESS']*C.P['STRESS_HP']+cb)
        before=trace(q.burn,hp=q.target_hp)+trace(q.rear_burn,hp=q.rear_hp)
        # Both targets share the attack roll if dodge is equal (default profile).
        if q.rear_exists:
            after=0.
            for m in S.MONS:
                ns,cs=S.damage_distribution(C.H['dmg'],S.num(S.first(d,'dmg')),m['prot'],q.damage_bonus+S.num(S.first(d,'dmg_per_burn_stack'))*q.rear_burn,C.P['DMG_STACK'])
                for crit_branch,weight,damages in [(False,1-rearcrit,ns),(True,rearcrit,(cs,))]:
                    copied=math.ceil(q.burn*(1+q.burn_bonus)*(1.5 if crit_branch else 1))
                    for dhp in damages:
                        rear_left=None if q.rear_hp is None else max(0,q.rear_hp-dhp)
                        after+=weight*trace(q.rear_burn+copied,hp=rear_left)/len(damages)/len(S.MONS)
        else:after=trace(q.rear_burn,hp=q.rear_hp)
        p['화상 전이 순증감']=hit*(after-before)*C.P['E_DOT_SGL']*rw
        # Guard ignore is an access rule, not extra damage on an already reached target.
    if sid=='run_and_hide':
        hot=max((b['amount'] for e,b in bs if b.get('stat_type')=='hp_dot_heal'),default=0)
        p['회복']=min(q.missing_hp,hot*q.future_hot_ticks)
        # It is a buff-based stealth, absent from the old inline stealth parser.
        p['은신 보호']=C.P['STEALTH']*C.P['ENEMY_ACT']*C.P['HITS_TAKEN']*min(q.future_hot_ticks,C.P['BUFF_DUR_CAP'])
    if sid=='ransack':
        # Rank displacement and corpse removal already priced by the base model;
        # only explicitly present corpses/ground entries may add scenario benefit.
        if explicit and not q.corpses:p.pop('시체',None)
    return p

def coverage():
    return {
      'duelist':dict(zip(SKILLS['duelist'],[
       'exclusive stance, free action, per-turn limit, riposte',
       'direct/crit, retreat, consume-on-dodge finite exposure',
       'direct/crit, self mark, PROT/conditional ACC debuff, riposte-only damage',
       'direct/crit, retreat, ACC/SPD/rank4 dodge, next-attack rank override, weakening',
       'direct/crit, advance, self mark, optional stance dodge drawback',
       'armor ignore, stun crit, joint damage-survival-kill, extra action only if another enemy',
       'direct/crit, joint survivor stun, knockback, advance'])),
      'runaway':dict(zip(SKILLS['runaway'],[
       'direct/crit, burning conditional damage, added burn',
       'direct/crit burn quantity, resisted decay debuff with actual duration',
       'retreat, conditional stealth, finite missing-HP-capped HoT',
       'stealthed ACC, direct/crit, pull, corpses, advance',
       'party ACC/conditional CRIT, destealth, resisted conditional decay, advance',
       'initial burn vs miss-independent zone, round vs action clocks, move entries, use/wave limit',
       'requires burn, guard ignore, per-target own-stack direct, rear existence, burn transfer/cure'])),
      'explicit_limits':[
       'No fitted target-state distribution: DLC_STATE is an explicit scenario.',
       'No full enemy-AI or party-composition search; movement is legality/state, not arbitrary HP.',
       'Equipment procs require separate event schedules; no all-trinket aggregate is claimed.',
       'Wildfire helper requires corpse/adjacency facts; no invented wildfire bonus in global scores.',
       'Extra action uses stated followup_action_hp and remaining enemies; recursive chains require explicit sequence.',
       'Backdraft evaluates each rear damage/crit branch before HP-capped transferred burn; default targets share dodge/protection population.',
       'Torch/stall flags remain deliberately unpriced; no silent combat-power bonus.',
      ]}
