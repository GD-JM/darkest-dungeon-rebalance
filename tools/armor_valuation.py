"""R-AUDIT-26: finite-budget HP-equivalent ledger for armor-support skills.

No game writes. Raw HP damage, conditional prevention, and explicit valuation
priors are kept as separate contributions before one fixed-unit conversion.
"""
import copy, functools, itertools, math, pathlib, re, statistics as st
import strength as S
import damage_support as D

STANDARD = 8.14872802734375

def score(hp): return hp / STANDARD * 100 - 100
def contribution(hp): return hp / STANDARD * 100

@functools.lru_cache(maxsize=None)
def monster_pool(tier='C'):
    """Combatants, including zero-DODGE armor carriers. Dodge is not an object flag."""
    _,_,files=S._monster_db();out=[]
    for name,file in files.items():
        if not name.endswith('_'+tier):continue
        text=pathlib.Path(file).read_text(encoding='utf-8',errors='ignore')
        if re.search(r'^tag:\s*\.id\s*"boss"',text,re.M) or not re.search(r'^skill:',text,re.M):continue
        match=re.search(r'^stats:(.*)$',text,re.M)
        if not match:continue
        d={k:S.num(v[0]) for k,v in S.kv(match[1]).items() if v}
        if d.get('hp',0)<=0:continue
        size=re.search(r'^display:.*?\.size\s+(\d+)',text,re.M)
        typ=re.search(r'enemy_type:\s*\.id\s*"?(\w+)',text)
        prot=d.get('prot',0)
        out.append(dict(name=name,dodge=d.get('def',0),prot=prot if prot<=1 else prot/100,spd=d.get('spd',0),hp=d['hp'],
                        stun=d.get('stun_resist',0),poison=d.get('poison_resist',0),bleed=d.get('bleed_resist',0),debuff=d.get('debuff_resist',0),move=d.get('move_resist',0),
                        type=typ[1] if typ else '?',size=int(size[1]) if size else 1))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def rank_cases(tier='C'):
    """Base-dungeon initial formations; weights are mash weights, not play logs."""
    pool={m['name']:m for m in monster_pool(tier)}
    _,_,files=S._monster_db()
    rows=[];skipped=[]
    dungeon_level={'A':1,'B':3,'C':5}[tier]
    for file in sorted((pathlib.Path(S.G)/'dungeons').glob(f'*/*.{dungeon_level}.mash.darkest')):
        for line in file.read_text(encoding='utf-8',errors='ignore').splitlines():
            match=re.match(r'^(hall|room):\s*\.chance\s+([\d.]+)\s+\.types\s+(.*)$',line.strip())
            if not match:continue
            names=match[3].split()
            if not all(n in pool for n in names):
                skipped.append(names);continue # bosses/objects/missing sample explicitly excluded
            units=[];pos=1
            for name in names:
                m=dict(pool[name]);m['ranks']=tuple(range(pos,min(5,pos+m['size'])))
                units.append(m);pos+=m['size']
            rows.append((float(match[2]),tuple(units)))
    return tuple(rows),tuple(skipped)


def target_cases(ranks,aoe,tier='C',scenario='ranks'):
    if scenario!='ranks':
        pool=monster_pool(tier)
        if scenario.startswith('prot'):
            value=float(scenario[4:])/100
            pool=[dict(m,prot=value) for m in pool]
        count=3.2 if aoe else 1.
        return [(m,count/len(pool)) for m in pool],dict(units=count,availability=1.,sample=len(pool),scenario=scenario)
    rows,skipped=rank_cases(tier);total=sum(w for w,_ in rows);available=0.;cases=[]
    for w,units in rows:
        targets=[m for m in units if set(m['ranks'])&set(ranks)]
        if not targets:continue
        available+=w
        for m in targets:
            cases.append((m,w/total if aoe else w/total/len(targets)))
    # Collapse identical enemy/rank cases, preserving all measured weights.
    merged={}
    for m,w in cases:
        key=(m['name'],m.get('ranks'))
        if key not in merged:merged[key]=[m,0.]
        merged[key][1]+=w
    return list(merged.values()),dict(units=sum(w for _,w in cases),availability=available/total if total else 0.,sample=len(rows),excluded=len(skipped),scenario=scenario)


def effect_mods(text,buffs,marked=False):
    k=S.kv(text);out=D.modifiers(S,k,buffs,marked)
    if 'combat_stat_buff' in k:
        for field in ('attack_rating_add','crit_chance_add','damage_low_multiply','damage_high_multiply'):
            if field in k:out[field]=-S.num(S.first(k,field))/100
        if 'speed_rating_add' in k:out['speed']=-S.num(S.first(k,'speed_rating_add'))
    for name in k.get('buff_ids',[]):
        b=buffs.get(name.strip('"'),{});rule=b.get('rule_type','always')
        if rule not in ('always',None):
            if rule=='actorStatus' and b.get('rule_data',{}).get('string')=='tagged' and b.get('stat_sub_type')=='attack_rating':
                out['attack_marked_add']=out.get('attack_marked_add',0)-b.get('amount',0)
            continue
        sub=b.get('stat_sub_type');typ=b.get('stat_type');a=-b.get('amount',0)
        if typ=='combat_stat_add' and sub in ('attack_rating','crit_chance'):out[sub+'_add']=out.get(sub+'_add',0)+a
        if typ=='combat_stat_add' and sub=='speed_rating':out['speed']=out.get('speed',0)+a
        if typ=='combat_stat_multiply' and sub in ('damage_low','damage_high'):out[sub+'_multiply']=out.get(sub+'_multiply',0)+a
    return out


@functools.lru_cache(maxsize=None)
def enemy_actions(name,ranks):
    effects,brains,files=S._monster_db();text=pathlib.Path(files[name]).read_text(encoding='utf-8',errors='ignore')
    bid=re.search(r'monster_brain:\s*\.id\s*(\S+)',text);weights={}
    for desire in brains.get(bid[1] if bid else '',{}).get('skill_selection_desires',[]):
        if desire['type']=='specific_skill':
            data=desire['data'];key=data['combat_skill_id'];weights[key]=weights.get(key,0)+data.get('base_chance',1)
    result=[]
    for row in text.splitlines():
        if not row.startswith('skill:'):continue
        k=S.kv(row);launch=set(map(int,re.findall('[1-4]',S.first(k,'launch'))))
        if ranks and not launch.intersection(ranks):continue
        target=S.first(k,'target');raw=k.get('dmg',['0','0'])
        friendly='@' in target or not target
        result.append(dict(acc=S.num(S.first(k,'atk')),crit=S.num(S.first(k,'crit'))/100 if S.first(k,'is_crit_valid','True').lower()=='true' else 0.,
            weapon=(0.,0.) if friendly else (S.num(raw[0]),S.num(raw[-1])),effects=tuple(effects.get(n,'') for n in S.ec.effect_names_in(row)),friendly=friendly,
            count=len(re.findall('[1-4]',target))*.8 if '~' in target else 1.,weight=weights.get(S.first(k,'id'),0)))
    total=sum(a['weight'] for a in result)
    for a in result:a['weight']=(a['weight']/total if total else 1/len(result))
    return tuple(result)


def enemy_action_hp(m,mods,P):
    """AI-weighted direct HP, stress, DOT and stunned-ally action loss.
    DOT ticks/resists and stun action availability are explicit scenario inputs.
    Disease, shuffle and enemy healing/summoning are not silently equated to HP.
    """
    total=0.
    for a in enemy_actions(m['name'],tuple(m.get('ranks',()))):
        if a['friendly']:continue
        lo,hi=a['weapon'];changed=(lo*max(0.,1-mods.get('damage_low_multiply',0)),hi*max(0.,1-mods.get('damage_high_multiply',0)))
        h=S.hit_probability(a['acc']-mods.get('attack_rating_add',0)*100,P.get('ALLY_DODGE',25))
        if mods.get('attack_marked_add',0):
            p=min(1.,1/a['count']) if a['count']>1 and P.get('MARKED_VICTIM_SHARE',0) else P.get('MARKED_VICTIM_SHARE',0)
            h=(1-p)*h+p*S.hit_probability(a['acc']-(mods.get('attack_rating_add',0)+mods['attack_marked_add'])*100,P.get('ALLY_DODGE',25))
        c=D.clamp(a['crit']-mods.get('crit_chance_add',0))
        dmg=S.damage_mean(changed,0,c,P.get('ALLY_PROT',0))
        stress=status=0.
        for text in a['effects']:
            k=S.kv(text)
            if S.first(k,'target','target')=='target' and 'stress' in k:
                chance=D.clamp(S.num(S.first(k,'chance','100'))/100)
                activation=1. if S.first(k,'on_miss')=='true' else h
                stress+=S.num(S.first(k,'stress'))*chance*activation
            if S.first(k,'target','target')!='target' or S.first(k,'keyStatus'):continue
            chance=S.num(S.first(k,'chance','100'))/100
            activation=1. if S.first(k,'on_miss')=='true' else h
            for field,res in (('dotBleed','ALLY_BLEED_RESIST'),('dotPoison','ALLY_BLIGHT_RESIST')):
                if field not in k:continue
                resist=P.get(res,.6);ticks=min(S.effect_duration(k,P),P.get('ENEMY_DOT_TICKS',2.))
                success=(1-c)*D.clamp(chance-resist)+c*D.clamp(chance+P['CRIT_EFF']-resist)
                status+=S.num(S.first(k,field))*ticks*success*activation
            if 'stun' in k:
                resist=P.get('ALLY_STUN_RESIST',.8)
                success=(1-c)*D.clamp(chance-resist)+c*D.clamp(chance+P['CRIT_EFF']-resist)
                status+=success*activation*P.get('ALLY_ACTION_HP',STANDARD)*P.get('ALLY_STUN_ACTION_AVAILABLE',1.)
        critstress=h*c*P['CRIT_RECV_STRESS'] if hi>0 else 0.
        total+=a['weight']*a['count']*(h*dmg+status+(stress+critstress)*P['STRESS_HP']*(1+P.get('ALLY_STRESS_MULTIPLIER',0)))
    return total


def prevention(C,row,m,P):
    """Joint target ACC/DMG/CRIT prevention plus speed's separate action prior."""
    d=S.kv(row);crit=D.clamp((S.num(S.first(d,'crit'))+C.H['wcrit'])/100)
    if S.first(d,'is_crit_valid','True').lower()!='true':crit=0.
    acc=S.num(S.first(d,'atk'));h=S.hit(m,acc);dmg=S.num(S.first(d,'dmg'))
    normal,critical=S.damage_distribution(C.H['dmg'],dmg,m['prot']) if dmg>-100 else ((0,),0)
    qn=st.mean(float(n<m['hp']) for n in normal);qc=float(critical<m['hp'])
    groups=[]
    for name in S.ec.effect_names_in(row):
        text=C.eff.get(name,'');k=S.kv(text)
        if S.first(k,'target')!='target':continue
        mods=effect_mods(text,C.buffs)
        mods={key:v for key,v in mods.items() if key in ('attack_rating_add','attack_marked_add','crit_chance_add','damage_low_multiply','damage_high_multiply','speed') and v>0}
        if mods:groups.append((mods,S.num(S.first(k,'chance','100'))/100,int(S.effect_duration(k,P)),S.first(k,'crit_doesnt_apply_to_roll')=='true'))
    if not groups:return 0.,0.
    before=enemy_action_hp(m,{},P);prevent=spd=0.
    for iscrit,bp in ((False,h*(1-crit)*qn),(True,h*crit*qc)):
        probabilities=[D.clamp(ch+(.2 if iscrit and not exception else 0)-m['debuff']/100) for _,ch,_,exception in groups]
        for bits in itertools.product((0,1),repeat=len(groups)):
            prob=math.prod(p if bit else 1-p for bit,p in zip(bits,probabilities))
            if not prob:continue
            for t in range(min(3,max(x[2] for x in groups))):
                mods={}
                for bit,(gm,_,duration,_) in zip(bits,groups):
                    if bit and t<duration:
                        for key,v in gm.items():mods[key]=mods.get(key,0)+v
                exposure=P['DEBUFF_W1'] if t==0 else (1-P['DEATH_RATE'])**t
                active_P=P
                if t>=P.get('SELF_MARK_DURATION',99):active_P=dict(P,MARKED_VICTIM_SHARE=0.)
                after=enemy_action_hp(m,mods,active_P)
                prevent+=bp*prob*exposure*(before-after)
                # Initiative model and probability that acting first removes the action are priors.
                # Use post-debuff threat to avoid counting full speed and DMG prevention twice.
                delta=S.p_before(P.get('ALLY_SPEED',7),m['spd']-mods.get('speed',0))-S.p_before(P.get('ALLY_SPEED',7),m['spd'])
                spd+=bp*prob*exposure*P['DEATH_RATE']*delta*after
    return prevent,spd


def strip_armor(effects,buffs):
    result={}
    for name,text in effects.items():
        text=re.sub(r'\.protection_rating_add\s+-[\d.]+%?', '',text)
        k=S.kv(text)
        for b in k.get('buff_ids',[]):
            v=buffs.get(b.strip('"'),{})
            if v.get('stat_sub_type')=='protection_rating' and v.get('amount',0)<0:
                text=text.replace(b,'')
        result[name]=text
    return result


def only_armor(effects,buffs):
    result={}
    for name,text in effects.items():
        text=re.sub(r'\.defense_rating_add\s+-[\d.]+%?', '',text)
        text=re.sub(r'\.buff_type\s+crit_received_chance\s+\.buff_amount\s+[\d.]+%?', '',text)
        for b in S.kv(text).get('buff_ids',[]):
            v=buffs.get(b.strip('"'),{})
            if v.get('stat_type') in ('crit_received_chance','damage_received_percent') or v.get('stat_sub_type')=='defense_rating':text=text.replace(b,'')
        result[name]=text
    return result


def evaluate_skill(H,row,eff,buffs,P,scenario='ranks',ripostes=0.,armor_only=False):
    d=S.kv(row);level=int(S.first(d,'level'));ranks=tuple(map(int,re.findall('[1-4]',S.first(d,'target'))));aoe='~' in S.first(d,'target')
    tier=('A','A','B','B','C')[level];cases,meta=target_cases(ranks,aoe,tier,scenario)
    params=dict(P,RANK_MODEL=False,FRONT_REACH=False)
    if H['id']=='duelist' and S.first(d,'id')=='feint':
        params['MARKED_VICTIM_SHARE']=P.get('MARKED_VICTIM_SHARE',.556)
        params['SELF_MARK_DURATION']=2
    C=S.Ctx(H,eff,buffs,params)
    _,parts=S.skill_value(C,row,d)
    # Keep explicitly priced utility; replace core damage/debuff estimates below.
    for key in ('직접','후속 직접 피해','후속 치명 부수효과','약화','치명타'):parts.pop(key,None)
    crit=D.clamp((S.num(S.first(d,'crit'))+H['wcrit'])/100) if S.first(d,'is_crit_valid','True').lower()=='true' else 0.
    acc=S.num(S.first(d,'atk'));dmg=S.num(S.first(d,'dmg'));count=meta['units'];wtotal=sum(w for _,w in cases)
    direct=sum(w*S.hit(m,acc)*S.damage_mean(H['dmg'],dmg,crit,m['prot'],current_hp=m['hp']) for m,w in cases) if dmg>-100 else 0.
    parts['직접']=direct
    effects=[eff.get(n,'') for n in S.ec.effect_names_in(row)]
    armorless=strip_armor({n:eff.get(n,'') for n in S.ec.effect_names_in(row)},buffs)
    without=[armorless.get(n,'') for n in S.ec.effect_names_in(row)]
    just_armor=only_armor({n:eff.get(n,'') for n in S.ec.effect_names_in(row)},buffs)
    just=[just_armor.get(n,'') for n in S.ec.effect_names_in(row)]
    # AOE spreads the same three companions' attack budget; never N * 1.5 attacks.
    attacks=P['PARTY_ATTACKS'] if aoe else P['PARTY_ATTACKS']*P['FOCUS_SHARE']
    support=side=noarmor=armor_alone=0.
    for m,w in cases:
        cc=S.Ctx(H,eff,buffs,dict(params,TGT_ATTACKS=attacks))
        val,cside=D.support_value(S,cc,row,d,effects,[m]);plain,_=D.support_value(S,cc,row,d,without,[m])
        solo,_=D.support_value(S,cc,row,d,just,[m])
        support+=w/wtotal*val;side+=w/wtotal*cside;noarmor+=w/wtotal*plain;armor_alone+=w/wtotal*solo
    # Two-group Shapley attribution divides interaction instead of crediting it all to armor.
    parts['방어도 감소']=(armor_alone+support-noarmor)/2
    parts['기타 공격 지원']=(noarmor+support-armor_alone)/2
    parts['후속 치명 부수효과']=side
    prev=slow=0.
    for m,w in cases:
        v,s=prevention(C,row,m,params);prev+=w*v;slow+=w*s
    parts['피해·명중 약화 예방']=prev;parts['속도 약화']=slow
    # Critical side effects are separate from damage, with class-specific healing proc added.
    cb=sum(C.buff_ids_value(S.kv(eff.get(n,'')).get('buff_ids',[]),P['CRIT_BUFF_DUR'],'self') for n in H['crit_effects'])
    healproc=0.
    for n in H['crit_effects']:
        for bid in S.kv(eff.get(n,'')).get('buff_ids',[]):
            b=buffs.get(bid.strip('"'),{})
            if b.get('stat_type')=='hp_heal_percent':
                heals=[sum(map(S.num,k['heal']))/2 for _,k in H['skills'] if len(k.get('heal',[]))==2 and '@' in S.first(k,'target') and '~' not in S.first(k,'target')]
                if heals:healproc+=b['amount']*max(heals)*(1+P['HEAL_CRIT_SGL'])*P['HEAL_FOLLOWUP_RATE']*P['CRIT_BUFF_DUR']
    ch=sum(w*S.hit(m,acc)*crit for m,w in cases)
    parts['치명 부수효과']=ch*(P['CRIT_STRESS']*P['STRESS_HP']+cb+healproc)
    if H['id']=='duelist' and S.first(d,'id')=='feint':
        parts.pop('강화',None)
        # Feint does not itself activate riposte. Zero follow-up ripostes => zero buff payoff.
        bonus=0.
        for text in effects:
            for b in S.kv(text).get('buff_ids',[]):
                x=buffs.get(b.strip('"'),{})
                if x.get('rule_type')=='riposte' and x.get('stat_sub_type')=='damage_low':bonus+=x['amount']
        rr=H['riposte'];ra=S.num(S.first(rr,'atk'));rc=(S.num(S.first(rr,'crit'))+H['wcrit'])/100+H.get('gear_riposte_crit',0)
        parts['반격 강화']=ripostes*sum(w/wtotal*S.hit(m,ra)*(S.damage_mean(H['dmg'],S.num(S.first(rr,'dmg')),rc,m['prot'],bonus=bonus)-S.damage_mean(H['dmg'],S.num(S.first(rr,'dmg')),rc,m['prot'])) for m,w in cases)
    if any('pull' in S.kv(x) for x in effects):
        dist=max(S.num(S.first(S.kv(x),'pull')) for x in effects)
        mv=S.move_value('pull',int(dist),ranks,P['STRESS_HP'],P['DEATH_RATE'],2,P['FOCUS_FIRE'],P['KILL_SHARE'],P['PUSH_WRAP'])
        probability=0.
        for m,w in cases:
            for text in effects:
                k=S.kv(text)
                if 'pull' not in k:continue
                chance=S.num(S.first(k,'chance'))/100
                probability+=w/wtotal*S.hit(m,acc)*((1-crit)*D.clamp(chance-m['move']/100)+crit*D.clamp(chance+.2-m['move']/100))
        parts['이동']=mv*probability
    armor_groups=D.groups(S,effects,buffs,P,False)
    armor_groups=[g for g in armor_groups if g['mods'].get('protection_rating',0)>0]
    probability=0.
    for m,w in cases:
        q0=1-math.prod(1-D.clamp(g['chance']-m['debuff']/100) for g in armor_groups)
        q1=1-math.prod(1-D.clamp(g['chance']+g['crit_bonus']-m['debuff']/100) for g in armor_groups)
        probability+=w/wtotal*S.hit(m,acc)*((1-crit)*q0+crit*q1)
    total=sum(parts.values())
    return dict(hp=total,pp=score(total),basic_percent=contribution(total),parts_pp={k:contribution(v) for k,v in parts.items() if abs(v)>1e-10},meta=meta,launch=S.first(d,'launch'),target=S.first(d,'target'),followup_budget=attacks,
                gross_hit=sum(w/wtotal*S.hit(m,acc) for m,w in cases),crit_conditional=crit,
                prot_probability=probability)
