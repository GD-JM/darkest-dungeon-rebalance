"""기절 전수 감사. 기존 단일 점수와 원문을 보존하며 조건별로 분리 계산한다.

python tools/stun_audit.py --output <json_path>
--mod-root defaults to this script's repository. No hero/effect data is written.
"""
from pathlib import Path
import sys, importlib.util, json, re, statistics as st, hashlib, collections, copy, math, os, argparse
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--mod-root',type=Path,default=Path(__file__).resolve().parents[1])
ap.add_argument('--output',type=Path)
args=ap.parse_args()
M=args.mod_root.resolve();G=M.parents[1]
OUT=(args.output or M/'design/analysis/stun-reassessment.json').resolve()
sys.path.insert(0,str(M/'tools'))
import strength as s
import effect_common as ec
K=ec.load_korean(s.G); B=ec.load_buffs(s.G)
VE=ec.load_vanilla_effects(s.G)
P=dict(s.PARAM,STRESS_HP=s.stress_value(),STRESS_TAKEN=2*s.monster_stress_per_action()/4,
       HEAL_FOLLOWUP_AMOUNT=s.followup_heal_amount(),MARK_DAMAGE_BONUS=s.marked_damage_bonus())
s.PARAM_MED_HP=s.stress_hp('vanilla')*100
s.HERO_MED_SPD=st.median(s.load_hero(h,'vanilla')['spd'] for h in s.KO)
BASES={}
for hero in s.KO:
    H=s.load_hero(hero,'vanilla');a=sum(H['dmg'])/2;hi=H['dmg'][1];c=H['wcrit']/100
    BASES[hero]=st.mean(s.hit(m,105)*((1-c)*a+c*hi*1.5)*(1-m['prot']) for m in s.MONS)
STD=st.median(BASES.values())
pp=lambda x:x/STD*100
def buff_list(effects,E):
    return [dict(effect=n,raw=E.get(n),buffs=[B.get(b.strip('"'),dict(id=b,missing=True)) for b in s.kv(E.get(n,'')).get('buff_ids',[])]) for n in effects]

rows=[]; accuracy=[]; coverage=[]
for mode in ['vanilla','rb']:
    E=s.load_effects(mode)
    for hero in s.KO:
        f=Path(s.hero_file(hero,mode));t=f.read_text(encoding='utf-8');lines=t.splitlines()
        combat=[(i+1,l,s.kv(l)) for i,l in enumerate(lines) if l.startswith('combat_skill:')]
        coverage.append(dict(mode=mode,hero=hero,path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),combat_lines=len(combat)))
        for ln,l,d in combat:
            if s.first(d,'level')!='0':continue
            sid=s.first(d,'id');valid=s.first(d,'valid_modes');tgt=s.first(d,'target')
            if mode=='vanilla' and tgt and '@' not in tgt and s.num(s.first(d,'atk'))>0:
                accuracy.append(dict(hero=hero,id=sid,type=s.first(d,'type'),acc1=s.num(s.first(d,'atk')),dmg=s.num(s.first(d,'dmg')),target=tgt))
            stun=[n for n in ec.effect_names_in(l) if 'stun' in s.kv(E.get(n,'')) and s.first(s.kv(E[n]),'target') in ['target','target_group']]
            if not stun:continue
            H=s.load_hero(hero,mode);C=s.Ctx(H,E,B,P)
            levels=[]
            for lev in range(5):
                no,ll,dd=next(x for x in combat if s.first(x[2],'id')==sid and s.first(x[2],'level')==str(lev) and s.first(x[2],'valid_modes')==valid)
                names=ec.effect_names_in(ll)
                ee=next(n for n in names if 'stun' in s.kv(E.get(n,'')))
                k=s.kv(E[ee]);chance=s.num(s.first(k,'chance'))
                levels.append(dict(level=lev+1,line=no,raw=ll,fields=dd,effects=buff_list(names,E),stun_effect=ee,chance=chance))
            L=levels[-1];dd=L['fields'];ll=L['raw'];atk=s.num(s.first(dd,'atk'));dmg=s.num(s.first(dd,'dmg'))/100
            cv=s.first(dd,'is_crit_valid','true').lower()=='true' and dmg>-1
            cr=(s.num(s.first(dd,'crit'))+H['wcrit'])/100 if cv else 0
            a=sum(H['dmg'])/2;hi=H['dmg'][1];chance=L['chance']
            value,parts=s.skill_value(C,ll,dd)
            nr,np=s.skill_value(s.Ctx(H,E,B,dict(P,RANK_MODEL=False)),ll,dd)
            tgt=s.first(dd,'target');aoe='~' in tgt;nt=len(re.sub('[^1-4]','',tgt))*P['AOE_PER_RANK'] if aoe else 1
            ranktuple=tuple(map(int,re.sub('[^1-4]','',tgt)))
            tau,mult,act,_,rho=s.formation_stats(P['STRESS_HP'])
            rw=st.mean(mult[r] for r in ranktuple) if aoe else max(mult[r] for r in ranktuple)
            probs=[]
            for extra in [0,20,25,40,45,50,60]:
                for recovery in [0,50]:
                    rates=[s.hit(m,atk)*((1-cr)*s.apply_rate(dict(m,stun=m['stun']+recovery),chance+extra,'stun')+cr*s.apply_rate(dict(m,stun=m['stun']+recovery),chance+extra+20,'stun')) for m in s.MONS]
                    probs.append(dict(extra=extra,recovery_resist=recovery,mean=st.mean(rates)))
            samples=[]
            for dodge in [10,20,30,40]:
                for res in [50,70,90,100,120]:
                    m=dict(dodge=dodge,stun=res)
                    h=s.hit(m,atk);nc=s.apply_rate(m,chance,'stun');cc=s.apply_rate(m,chance+20,'stun')
                    samples.append(dict(dodge=dodge,resist=res,hit=h,normal_stun=nc,crit_stun=cc,success=h*((1-cr)*nc+cr*cc)))
            changes=[]
            for field,newval in [('atk',atk-5),('atk',atk+5),('crit',0),('dmg',-50),('stun',chance-10),('stun',chance+10),('target','12'),('target','123'),('target','234')]:
                if field=='stun':
                    EE=dict(E);raw=EE[L['stun_effect']];EE[L['stun_effect']]=re.sub(r'\.chance\s+[-\d.]+%',f'.chance {newval}%',raw);line=ll
                else:
                    EE=E;line=re.sub(r'\.'+field+r'\s+\S+',f'.{field} {newval}'+('%' if field in ['atk','crit','dmg'] else ''),ll)
                v,pt=s.skill_value(s.Ctx(H,EE,B,P),line,s.kv(line))
                changes.append(dict(field=field,to=newval,delta_pp=pp(v-value),value_pp=pp(v)-100,parts_pp={k:pp(x) for k,x in pt.items()}))
            rows.append(dict(mode=mode,hero=hero,hero_name=s.KO[hero],id=sid,name=K.get('combat_skill_name_'+hero+'_'+sid,sid),source=str(f),line1=ln,
                             levels=levels,hero5=H,crit_effects=buff_list(H['crit_effects'],E),skill_accuracy1=s.num(s.first(d,'atk')),skill_crit1=s.num(s.first(d,'crit')),
                             total_crit5=cr,crit_valid=cv,rank_weight=rw,expected_targets=nt,
                             noncrit_damage5=[H['dmg'][0]*max(0,1+dmg),hi*max(0,1+dmg)],crit_damage5=hi*1.5*max(0,1+dmg) if cv else 0,
                             hit_mean=st.mean(s.hit(m,atk) for m in s.MONS),success_samples=samples,success_sensitivity=probs,
                             before_action_mean=st.mean(s.p_before(H['spd'],m['spd']) for m in s.MONS),
                             legacy_value_pp=pp(value)-100,legacy_parts_pp={k:pp(v) for k,v in parts.items()},
                             neutral_value_pp=pp(nr)-100,neutral_parts_pp={k:pp(v) for k,v in np.items()},counterfactuals=changes))

# Full trinket inventory. Keep source and raw rules; do not assume conditional bonuses always active.
trinkets=[];stunheroes={r['hero'] for r in rows}
for f in sorted(Path(s.G).rglob('*.entries.trinkets.json')):
    if 'mods' in f.parts or '1117860_arena_mp' in f.parts:continue
    data=json.loads(f.read_text(encoding='utf-8-sig'))
    for item in data.get('entries',[]):
        hero=item.get('hero_class_requirements',[])
        if any(h in stunheroes for h in hero) or not hero:
            ids=item.get('buffs',[]);buffs=[B.get(x,dict(id=x,missing=True)) for x in ids]
            if hero or any(b.get('stat_type') in ['stun_chance','stun_chance_percent'] for b in buffs):
                trinkets.append(dict(id=item['id'],name=K.get('str_inventory_title_trinket'+item['id'],K.get('str_inventory_title_trinket_'+item['id'],item['id'])),heroes=hero,buffs=buffs,raw=item,source=str(f)))

rules=json.loads((Path(s.G)/'shared/rules.json').read_text(encoding='utf-8-sig'))
data=dict(date='2026-10-05',purpose='기절 등급·명중·치명·범위·장신구·모형 누락을 분리한 전수 감사; 수치 변경 없음',
          std_basic_internal_hp=STD,parameters=P,monster_sample=s.MONS,rank_stats=dict(threat=tau,mult=mult,enemy_act=act,reach=rho),
          coverage=coverage,rows=rows,accuracy=accuracy,trinkets=trinkets,
          rules={k:v for k,v in rules.items() if any(x in k for x in ['stun','crit','cutoff','initiative'])},
          stun_recovery_buff=B.get('STUNRECOVERYBUFF'))
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


p=json.loads(OUT.read_text(encoding='utf-8'))
STD=p['std_basic_internal_hp'];P=p['parameters'];E={k:v[0] for k,v in ec.load_vanilla_effects(str(G)).items()}
for f in (M/'effects').glob('*.darkest'):
    for l in f.read_text(encoding='utf-8').splitlines():
        m=re.search(r'\.name\s+"([^"]+)"',l)
        if l.startswith('effect:') and m:E[m.group(1)]=l
def kv(l):
    l=re.sub(r'\.name\s+"[^\"]*"',' ',l)
    l=re.sub(r'"(?=\.)','" ',l)
    l=re.sub(r'(?<=[^\s\d.])\.(?=[a-z_]{3,})',' .',l)
    return {m.group(1):m.group(2).split() for m in re.finditer(r'\.(\w+)((?:\s+(?!\.)[^\s]+)*)',l)}
def first(d,k,v=''):return (d.get(k) or [v])[0].strip('"')
def num(x):
    try:return float(str(x).strip('"').rstrip('%'))
    except (ValueError,TypeError):return 0.
def hit(a,dodge,hidden=0):
    x=a+hidden-dodge
    if hidden:return min(1.,max(0.,x/100))
    return 1. if x>=95 else max(0.,x/100)
def apply(c,res):return min(1.,max(0.,(c-res)/100))
pp=lambda x:x/STD*100
for r in p['rows']:
    H=r['hero5'];d=r['levels'][-1]['fields'];c=r['total_crit5'];a=num(first(d,'atk'));chance=r['levels'][-1]['chance'];mul=max(0.,1+num(first(d,'dmg'))/100)
    hero_source=Path(r['source']).read_text(encoding='utf-8')
    r['hero_context_lines']=[l for l in hero_source.splitlines() if l.startswith(('skill_selection:','crit:','mode:','armour:','resistances:'))]
    r['raw_attack_type']=first(d,'type');r['crit_proc_mean']=r['hit_mean']*c
    generic=r['crit_proc_mean']*P['CRIT_STRESS']*P['STRESS_HP']
    r['crit_breakdown_pp']=dict(direct_critical_damage=r['neutral_parts_pp'].get('직접',0)-pp(st.mean(hit(a,m['dodge'])*st.mean(H['dmg'])*mul*(1-m['prot']) for m in p['monster_sample'])),
                                 stun_critical_bonus=pp(st.mean(hit(a,m['dodge'])*c*(apply(chance+20,m['stun'])-apply(chance,m['stun'])) for m in p['monster_sample'])*P['ENEMY_ACT']*r['expected_targets']),
                                 generic_stress=pp(generic),legacy_class_buff=r['legacy_parts_pp'].get('치명타',0)-pp(generic))
    heal=[];bleed=[]
    for ll,dd in H['skills']:
        tg=first(dd,'target');hn=ec.effect_names_in(ll)
        if '@' in tg and '~' not in tg and len(dd.get('heal',[]))>=2:
            lo,hi=map(num,[dd['heal'][0],dd['heal'][-1]])
            heal.append(dict(id=first(dd,'id'),amount=(lo+hi)/2*(1+P['HEAL_CRIT_SGL'])))
        for nm in hn:
            ek=kv(E.get(nm,''))
            if 'dotBleed' in ek and first(ek,'target')=='target' and tg and '@' not in tg:
                bc=(num(first(dd,'crit'))+H['wcrit'])/100 if first(dd,'is_crit_valid','true').lower()=='true' else 0
                dur=num(first(ek,'duration','3'));tick=num(first(ek,'dotBleed'));ch=num(first(ek,'chance','100'));acc=num(first(dd,'atk'))
                gain=st.mean(hit(acc,m['dodge'])*tick*((1-bc)*dur*(apply(ch+20,m['bleed'])-apply(ch,m['bleed']))+bc*math.ceil(dur*1.5)*(apply(ch+40,m['bleed'])-apply(ch+20,m['bleed']))) for m in p['monster_sample'])
                count=len(re.sub('[^1-4]','',tg))*P['AOE_PER_RANK'] if '~' in tg else 1
                eff=P['E_DOT_AOE'] if '~' in tg else P['E_DOT_SGL']
                bleed.append(dict(id=first(dd,'id'),raw_gain_hp=gain*count,effective_gain_hp=gain*count*eff,bonus_pp=pp(gain*count*eff)*r['crit_proc_mean']))
    fut=[]
    for ce in r['crit_effects']:
        for b in ce['buffs']:
            stat=b['stat_type'];sub=b['stat_sub_type'];amt=b['amount'];
            if stat=='hp_heal_percent':
                best=max(heal,key=lambda x:x['amount']) if heal else None
                per=best['amount']*amt if best else 0
                fut.append(dict(kind='이후 본인이 회복1회',followup=best,extra_if_active_pp=pp(per),expected_added_pp=pp(per)*r['crit_proc_mean'],scored_by_legacy=False))
            elif stat=='bleed_chance':
                fut.append(dict(kind='이후 출혈 공격1회',alternatives=bleed,scored_by_legacy=False))
            elif stat=='poison_chance':
                fut.append(dict(kind='이후 중독 확률 강화',expected_added_pp=0,reason='이 기절 기술은 치명 불가; 발동하지 않음',scored_by_legacy=False))
    r['class_crit_followups']=fut
    missing=max((x.get('expected_added_pp',max((z['bonus_pp'] for z in x.get('alternatives',[])),default=0)) for x in fut),default=0)
    r['legacy_plus_one_followup_pp']=r['legacy_value_pp']+missing
    # Same concrete target, no rank multiplier. Values and event probabilities remain separate.
    cases=[]
    for dodge,res,prot in [(20,90,0),(20,50,0),(30,120,.3),(20,140,0)]:
        h=hit(a,dodge);nc=apply(chance,res);cc=apply(chance+20,res)
        normal=st.mean(H['dmg'])*mul*(1-prot);critical=H['dmg'][1]*1.5*mul*(1-prot) if c else 0
        suc=h*((1-c)*nc+c*cc)
        cases.append(dict(dodge=dodge,resist=res,prot=prot,hit=h,crit=c,success=suc,
                          expected_damage_contribution_pp=pp(h*((1-c)*normal+c*critical)),
                          stun_one_target_pp=pp(suc*P['ENEMY_ACT']),stun_all_expected_targets_pp=pp(suc*P['ENEMY_ACT']*r['expected_targets']),
                          success_hidden_plus5=hit(a,dodge,5)*((1-c)*nc+c*cc)))
    r['same_target_cases']=cases
    # The old sum counts stun even on killing hits. Continuous uniform roll avoids assuming rounding semantics.
    overlaps=[]
    lo,hi=r['noncrit_damage5']; cd=r['crit_damage5']
    for hp in [2,5,10,20]:
        survival=1. if not mul else (0. if hp<=lo else (1. if hp>hi else (hp-lo)/(hi-lo) if hi>lo else float(hp>lo)))
        cs=float(hp>cd) if cd else 1
        h=hit(a,20);nc=apply(chance,90);cc=apply(chance+20,90)
        full=h*((1-c)*nc+c*cc);surv=h*((1-c)*survival*nc+c*cs*cc)
        overlaps.append(dict(enemy_hp=hp,conditional_survival_noncrit=survival,stun_without_kill_filter=full,stun_surviving_hit=surv,
                             overlap_stun_pp=pp((full-surv)*P['ENEMY_ACT']),critical_kill_probability=h*c*(1-cs),
                             critical_corpse_removed_upper_bound_pp=pp(h*c*(1-cs)*P['CORPSE'])))
    r['kill_overlap_cases']=overlaps
    r['conditional_adjustments']=dict(
        critical_stress_pp_by_recoverable_fraction={str(u):r['crit_breakdown_pp']['generic_stress']*u for u in [0,.25,.5,1]},
        clear_corpses_pp_if_any=(pp(P['CORPSE'])*r['hit_mean'] if any('kill_enemy_types' in kv(e['raw'] or '') for e in r['levels'][-1]['effects']) else 0),
        guard_break='기절로 보호 제공자가 멈추면 보호가 해제됨. 보호가 없는 기준 상태는0; 보호된 후열에 대한 다음 공격의 접근 변화이며 평타1회를 공짜로 더하지 않음',
        self_move='0/1(0칸 후퇴·1칸 전진). 도착 열에서 다음 기술과 동료 기술의 사용 가능 여부를 검사; 자동 피해 감점/반격 보너스 없음',
        stall_flag=first(d,'is_stall_invalidating','미지정: 엔진 기본값 확인 필요'))
    joints=[]
    for ex in r['levels'][-1]['effects']:
        k=kv(ex['raw'] or '')
        if any(x in k for x in ['push','pull','shuffletarget']):
            mc=num(first(k,'chance','100'));h=hit(a,20);qs,qsc=apply(chance,90),apply(chance+20,90);qm,qmc=apply(mc,90),apply(mc+20,90)
            both=h*((1-c)*qs*qm+c*qsc*qmc);sonly=h*((1-c)*qs*(1-qm)+c*qsc*(1-qmc));monly=h*((1-c)*(1-qs)*qm+c*(1-qsc)*qmc)
            joints.append(dict(effect=ex['effect'],dodge=20,stun_resist=90,move_resist=90,both=both,stun_only=sonly,move_only=monly,neither=1-both-sonly-monly,assumption='적중 판정 공유; 적중·치명 분기 안에서 두 효과의 저항 판정은 독립이라는 작업 가정'))
    r['joint_stun_move_cases']=joints

# Match actual formation ranks, resistance/dodge/speed, and that same monster's threat.
# Only the four base dungeons, Champion formation files; no bosses or objects.
infos={};brains={}
for root in [G/'monsters',G/'dlc']:
    for dr,ds,fs in os.walk(root):
        ds[:]=[x for x in ds if x not in ['heroes','anim','fx','panels','localization','audio','1117860_arena_mp']]
        for fn in fs:
            f=Path(dr)/fn
            if fn.endswith('.info.darkest') and '/monsters/' in f.as_posix():infos.setdefault(fn.split('.')[0],str(f))
            elif fn.endswith('.monster_brains.json'):
                for bb in json.loads(f.read_text(encoding='utf-8-sig')).get('monster_brains',[]):brains.setdefault(bb['id'],bb)
profiles={}
def profile(mid):
    if mid in profiles:return profiles[mid]
    t=Path(infos[mid]).read_text(encoding='utf-8');stats=kv(re.search(r'^stats:(.*)$',t,re.M).group(1))
    size=int(num(first(kv(re.search(r'^display:(.*)$',t,re.M).group(1)),'size','1')))
    bid=re.search(r'monster_brain:\s*\.id\s*(\S+)',t);weights={}
    for ds in brains.get(bid.group(1) if bid else '',{}).get('skill_selection_desires',[]):
        if ds['type']=='specific_skill':
            sid=ds['data']['combat_skill_id'];weights[sid]=weights.get(sid,0)+ds['data'].get('base_chance',1)
    skills=[]
    for l in re.findall(r'^skill:.*$',t,re.M):
        d=kv(l);tg=first(d,'target');n=len(re.sub('[^1-4]','',tg))*.8 if '~' in tg else 1
        hh=max(0,min(95,num(first(d,'atk'))-25))/100;dm=d.get('dmg') or ['0'];low,high=num(dm[0]),num(dm[-1]);cr=num(first(d,'crit'))/100 if high>0 and first(d,'is_crit_valid','true').lower()=='true' else 0
        hp=((1-cr)*(low+high)/2+cr*high*1.5)*hh*n if not tg.startswith('@') else 0
        stress=0
        for name in ec.effect_names_in(l):
            k=kv(E.get(name,''))
            if 'stress' in k and first(k,'target','target')=='target':stress+=num(first(k,'stress'))*(1 if first(k,'on_miss','false').lower()=='true' else hh)*min(1,num(first(k,'chance','100'))/100)
        stress=stress*n+hh*cr*(10+3*.5*5)
        skills.append(dict(launch=re.sub('[^1-4]','',first(d,'launch')),value=hp+stress*P['STRESS_HP'],weight=weights.get(first(d,'id'),0)))
    prot=num(first(stats,'prot'));prot=prot if prot<=1 else prot/100
    profiles[mid]=dict(id=mid,source=infos[mid],size=size,boss=bool(re.search(r'^tag:\s*\.id\s*"boss"',t,re.M)),dodge=num(first(stats,'def')),resist=num(first(stats,'stun_resist')),prot=prot,speed=num(first(stats,'spd')),maxhp=num(first(stats,'hp')),skills=skills)
    return profiles[mid]
def threat(m,ranks):
    sk=[x for x in m['skills'] if any(str(r) in x['launch'] for r in ranks)]
    if not sk:return 0
    ws=[x['weight'] for x in sk]
    if not sum(ws):ws=[1]*len(sk)
    return sum(w*x['value'] for w,x in zip(ws,sk))/sum(ws)
forms=[]
for f in sorted((G/'dungeons').glob('*/*.5.mash.darkest')):
    for no,l in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
        mm=re.match(r'^(hall|room):\s*\.chance\s+([\d.]+)\s+\.types\s+(.*)$',l.strip())
        if not mm:continue
        mons=[profile(x) for x in mm.group(3).split() if x in infos]
        if any(m['boss'] for m in mons):continue
        rr=1;units=[]
        for m in mons:
            ranks=list(range(rr,min(4,rr+m['size']-1)+1));units.append(dict(id=m['id'],ranks=ranks,threat=threat(m,ranks)));rr+=m['size']
            if rr>4:break
        forms.append(dict(source=str(f),line=no,weight=float(mm.group(2)),units=units))
for r in p['rows']:
    dd=r['levels'][-1]['fields'];target=set(map(int,re.sub('[^1-4]','',first(dd,'target'))));aoe='~' in first(dd,'target');atk=num(first(dd,'atk'));cr=r['total_crit5'];chance=r['levels'][-1]['chance'];spd=r['hero5']['spd'];rand=P.get('INIT_RAND',8)
    ws=succ=prevent=immediate=damage=critproc=0.;selected=collections.Counter();nt=0
    for fm in forms:
        us=[u for u in fm['units'] if target.intersection(u['ranks']) and profiles[u['id']]['dodge']>0]
        if not us:continue
        if not aoe:us=[max(us,key=lambda u:u['threat'])]
        ww=fm['weight'];ws+=ww;stuns=prev=early=dmg=cp=0
        for u in us:
            m=profiles[u['id']];h=hit(atk,m['dodge']);prob=h*((1-cr)*apply(chance,m['resist'])+cr*apply(chance+20,m['resist']))
            eb=sum((rand-abs(k))/rand**2 for k in range(-rand+1,rand) if k>=m['speed']-spd)
            stuns+=prob;prev+=prob*u['threat'];early+=prob*eb
            dm=(st.mean(r['noncrit_damage5'])*(1-cr)+r['crit_damage5']*cr)*(1-m['prot'])*h
            dmg+=dm;cp+=h*cr
            selected[u['id']]+=ww/len(us)
        nt+=ww*len(us);succ+=ww*stuns;prevent+=ww*prev;immediate+=ww*early;damage+=ww*dmg;critproc+=ww*cp
    r['formation_matched']=dict(policy='각 편성에서 닿는 적 중 행동 위협도가 가장 큰 적1명; 광역은 실제 유닛을 한 번씩 센다',expected_targets=nt/ws,
                               expected_stuns=succ/ws,expected_same_round_prevented=immediate/ws,
                               stun_threat_contribution_pp=pp(prevent/ws),unweighted_direct_contribution_pp=pp(damage/ws),
                               selected_monsters=dict(selected),crit_proc_mean=critproc/ws)
    r['field_coverage']={k:('기절 수치/직접 피해/부가 효과로 계산' if k in ['atk','dmg','crit','effect','is_crit_valid','target','per_battle_limit'] else
                                 '상태별 사용 가능 조건; 별도 열/태세 검사' if k in ['launch','valid_modes','move','stance_effects','stance_move','apply_stance_effects'] else
                                 '식별/표현/엔진 플래그; 원문 보존') for k in dd}

builds={
 'abomination':[['com_abom_broken_key'],['com_abom_broken_key','padlock_2']],
 'crusader':[['paralyzers_crest'],['paralyzers_crest','com_cru_non_euclidean_hilt']],
 'houndmaster':[['cudgel_weight']],
 'occultist':[['demons_cauldron'],['demons_cauldron','cc_set_occ_vial_of_sand'],['demons_cauldron','focus_ring']],
 'plague_doctor':[['blasphemous_vial'],['blasphemous_vial','witchs_vial']],
 'man_at_arms':[['rampart_shield'],['rampart_shield','cc_set_maa_old_unit_banner']],
 'duelist':[['duelist_steel_tip_boots']],
 'vestal':[['sacred_scroll'],['haste_chalice']],
 'bounty_hunter':[['wounding_helmet']],
}
trinks={x['id']:x for x in p['trinkets']};buffs=ec.load_buffs(str(G));K=ec.load_korean(str(G))
for root in [G/'trinkets',G/'dlc']:
    for f in root.rglob('*.entries.trinkets.json'):
        if '1117860_arena_mp' in f.parts:continue
        for t in json.loads(f.read_text(encoding='utf-8-sig')).get('entries',[]):
            if t['id']=='focus_ring':trinks[t['id']]=dict(id=t['id'],name=K.get('str_inventory_title_trinket'+t['id'],t['id']),buffs=[buffs[x] for x in t['buffs']],source=str(f),heroes=[])
for r in p['rows']:
    samples=[];d=r['levels'][-1]['fields']
    for ids in builds.get(r['hero'],[]):
        if any(i not in trinks for i in ids):raise ValueError(ids)
        acc=stun=cri=speed=0;used=[]
        for i in ids:
            t=trinks[i]
            for b in t['buffs']:
                rule=b.get('rule_type','always');active=(rule=='always' or rule=='has_item_id' or rule=='firstroundonly' or rule==r['raw_attack_type']+'only' or (rule=='in_mode' and b['rule_data']['string']==first(d,'valid_modes')))
                if not active:continue
                stat=b['stat_type'];sub=b['stat_sub_type'];amt=b['amount']
                if stat=='stun_chance':stun+=amt*100
                elif stat=='combat_stat_add' and sub=='attack_rating':acc+=amt*100
                elif stat=='combat_stat_add' and sub=='crit_chance':cri+=amt
                elif stat=='combat_stat_add' and sub=='speed_rating':speed+=amt
                used.append(b)
        cr=min(1,max(0,r['total_crit5']+cri)) if r['crit_valid'] else 0
        a=num(first(d,'atk'))+acc;ch=r['levels'][-1]['chance']+stun
        sp=r['hero5']['spd']+speed
        rates=[]
        for res in [50,90,120,140]:
            h=hit(a,20);rates.append(dict(dodge=20,resist=res,hit=h,success=h*((1-cr)*apply(ch,res)+cr*apply(ch+20,res))))
        samples.append(dict(ids=ids,names=[trinks[i]['name'] for i in ids],accuracy5=a,stun5=ch,total_crit5=cr,speed5=sp,
                            active_buffs=used,all_buffs=[trinks[i] for i in ids],same_target_rates=rates,
                            assumptions=['성수 보유/공격 태세/첫 라운드 조건은 해당 샘플에서 충족','표식·기벽·빛·영지·야영 효과 제외','칼자루의 무작위 대상5%는 성공률 계산과 별도: 의도한 대상을 제어할 확률과 다름']))
    r['fixed_trinket_scenarios']=samples
    # CRU's future strong-stun proposal: probability gain plus damage payment by the same target model.
    if r['hero']=='crusader':
        variants=[]
        for chance,dmg in [(140,-50),(150,-50),(150,-55),(150,-60)]:
            c=r['total_crit5'];a=num(first(d,'atk'));hh=hit(a,20);m=1+dmg/100
            dmgval=pp(hh*((1-c)*st.mean(r['hero5']['dmg'])+c*r['hero5']['dmg'][1]*1.5)*m)
            for res in [90,140]:
                prob=hh*((1-c)*apply(chance,res)+c*apply(chance+20,res))
                variants.append(dict(chance=chance,damage_modifier=dmg,resist=res,success=prob,direct_pp=dmgval,control_pp=pp(prob*P['ENEMY_ACT'])))
        r['crusader_variants_same_target']=variants

# Follow-up attack synergies are separate from the stun's own damage.
synergies=[];K=ec.load_korean(str(G));VB=ec.load_vanilla_effects(str(G))
for src in p['coverage']:
    mode=src['mode'];EE={k:x[0] for k,x in VB.items()} if mode=='vanilla' else E
    for no,l in enumerate(Path(src['path']).read_text(encoding='utf-8').splitlines(),1):
        if not l.startswith('combat_skill:'):continue
        d=kv(l)
        if first(d,'level')!='4':continue
        matched=[];loadd=hiadd=cradd=0
        for n in ec.effect_names_in(l):
            k=kv(EE.get(n,''))
            if first(k,'keyStatus')=='stunned' and first(k,'target')=='performer':
                matched.append(dict(name=n,raw=EE[n]));loadd+=num(first(k,'damage_low_multiply'))/100;hiadd+=num(first(k,'damage_high_multiply'))/100;cradd+=num(first(k,'crit_chance_add'))/100
        if not matched:continue
        H=next(x['hero5'] for x in p['rows'] if x['mode']==mode and x['hero']==src['hero'])
        cr=(H['wcrit']+num(first(d,'crit')))/100;mul=max(0,1+num(first(d,'dmg'))/100);low,high=H['dmg'];cc=min(1,cr+cradd)
        base=(1-cr)*(low+high)/2*mul+cr*high*1.5*mul
        boosted=(1-cc)*(low*(1+loadd)+high*(1+hiadd))/2*mul+cc*high*(1+hiadd)*1.5*mul
        hh=hit(num(first(d,'atk')),20)
        bonus=pp(hh*(boosted-base));stressbonus=pp(hh*(cc-cr)*P['CRIT_STRESS']*P['STRESS_HP'])
        kills=[]
        for hp in [5,10,20]:
            l0,h0=low*mul,high*mul;l1,h1=l0*(1+loadd),h0*(1+hiadd)
            def kill_fraction(lo,hi):return 1. if hp<=lo else (0. if hp>hi else (hi-hp)/(hi-lo) if hi>lo else float(hp<=lo))
            k0=hh*((1-cr)*kill_fraction(l0,h0)+cr*float(h0*1.5>=hp));k1=hh*((1-cc)*kill_fraction(l1,h1)+cc*float(h1*1.5>=hp))
            kills.append(dict(enemy_hp=hp,kill_without_stun=k0,kill_with_stun=k1))
        synergies.append(dict(mode=mode,hero=src['hero'],id=first(d,'id'),name=K.get('combat_skill_name_'+src['hero']+'_'+first(d,'id'),first(d,'id')),raw=l,source=src['path'],line=no,
                              matched_effects=matched,low_bonus=loadd,high_bonus=hiadd,critical_bonus=cradd,critical_without=cr,critical_with=cc,
                              direct_extra_if_stunned_pp=bonus,critical_stress_extra_if_recoverable_pp=stressbonus,
                              incoming_stun_probability_marginals=[dict(stun_hero=x['hero'],stun_id=x['id'],damage_bonus_pp=x['same_target_cases'][0]['success']*bonus) for x in p['rows'] if x['mode']==mode],
                              kill_cases=kills,other_effects=[dict(name=n,raw=EE.get(n)) for n in ec.effect_names_in(l) if not any(z['name']==n for z in matched)],
                              assumptions=['이후 공격자의 사용열/대상열이 맞고 적이 아직 기절했으며 생존한 상태','기절 대상 보너스 외 출혈·표식·인종 보너스0;표준 상대 회피20·방어0','기절 영웅별 한계 곱은기절 성공 후 후속 공격1회가 실제로 가능할 때의조건부 전망;추가 행동을무료로 더하지 않음','처치/치명 판정의반올림은연속 균등분포근사']))
p['stunned_target_followups']=synergies
p['formation_model']=dict(count=len(forms),forms=forms,profiles=profiles,assumptions=['기본4지역 영웅 등급 초기 편성','지역/통로/방의 실제 방문 빈도 대신 기존 mash chance를 그대로 합산한 비교 표본','처치·전멸·중복 제어·현재 HP·다음 행동 선택은 따로 민감도에 기록','위협도 동률은 파일 순서; 아직 아무도 쓰러지지 않은 초기 상태'])
tests=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    tests.append(name)
check('20 classes in both modes, all1400 combat lines captured',len(p['coverage'])==40 and sum(x['combat_lines'] for x in p['coverage'])==1400)
check('12 original/11 current stun variants;115 level lines',collections.Counter(r['mode'] for r in p['rows'])=={'vanilla':12,'rb':11} and sum(len(r['levels']) for r in p['rows'])==115)
by={r['hero']+'/'+r['id']:r for r in p['rows'] if r['mode']=='rb'}
check('Same-target Manacles includes11% total critical chance',abs(by['abomination/manacles']['same_target_cases'][0]['success']-.422)<1e-12)
check('Same-target Crusader includes hit90% and11% total critical chance',abs(by['crusader/stunning_blow']['same_target_cases'][0]['success']-.4698)<1e-12)
check('Same-target Abyss includes hit90% and23% total critical chance',abs(by['occultist/hands_from_abyss']['same_target_cases'][0]['success']-.5814)<1e-12)
check('A single reachable3rd rank is not an extra target',by['abomination/manacles']['expected_targets']==1)
check('Nondamaging skills cannot trigger an on-critical buff',all(r['crit_proc_mean']==0 and r['crit_damage5']==0 for r in p['rows'] if not r['crit_valid']))
check('Class healing buffs are on outgoing healer, not target received healing',all(x['followup']['id'] in ['wyrd_reconstruction','divine_grace'] for r in p['rows'] for x in r['class_crit_followups'] if x['kind']=='이후 본인이 회복1회'))
check('Critical corpse credit requires a killing crit',all(r['kill_overlap_cases'][-1]['critical_corpse_removed_upper_bound_pp']==0 for r in p['rows']))
check('Full-hit kill has no simultaneous living-target stun',by['abomination/manacles']['kill_overlap_cases'][0]['stun_surviving_hit']==0)
check('Previous stun recovery is exactly+50 for2turns in source',p['stun_recovery_buff']['amount']==.5 and p['stun_recovery_buff']['duration']==2)
check('Matched forms count large units once, not once per occupied slot',all(r['formation_matched']['expected_targets']<=2 for r in p['rows']))
check('Duelist stunned-target critical effect is included and capped',all(x['critical_with']==1 for x in synergies if x['hero']=='duelist'))
check('BH asymmetric low/high stunned-target damage bonuses preserved',any(x['mode']=='rb' and x['hero']=='bounty_hunter' and x['low_bonus']==.6 and x['high_bonus']==1 for x in synergies))
for r in p['rows']:
    rate={(x['extra'],x['recovery_resist']):x['mean'] for x in r['success_sensitivity']}
    check('Stun chance improvement is monotone '+r['mode']+'/'+r['id'],all(rate[(a,0)]<=rate[(b,0)]+1e-12 for a,b in zip([0,20,25,40,45,50],[20,25,40,45,50,60])))
    check('Recovery resistance does not improve success '+r['mode']+'/'+r['id'],all(rate[(x,50)]<=rate[(x,0)] for x in [0,20,25,40,45,50,60]))
    check('All attached skill fields preserved '+r['mode']+'/'+r['id'],set(r['field_coverage'])==set(r['levels'][-1]['fields']))
    check('Joint move/stun outcomes sum to1 '+r['mode']+'/'+r['id'],all(abs(sum(j[k] for k in ['both','stun_only','move_only','neither'])-1)<1e-12 for j in r['joint_stun_move_cases']))
check('Live source hashes match captured analysis inputs',all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in p['coverage']))
p['tests']=dict(count=len(tests),passed=tests,game_engine_test=False)
p['source_notes']=dict(primary_accuracy_intent='https://store.steampowered.com/news/posts/?appids=262060&enddate=1453243045',
                      primary_accuracy_quote_date='2015-12-21: status-skill accuracy raised to shift burden to resistance rolls',
                      guard_break_primary_same_source='2016-01-19: stunning guard casters removes guard on target',
                      primary2018_unreadable='Steam2018 공지 본문이 도구에서 읽히지 않아 근거로 사용하지 않음',
                      unknowns=['명중 숨은+5/동률 우선순위/효과와buff JSON의 지속 우선순위/변신·태세 및 이동 상세/시체·기절 처리 순서는 실게임 확인 필요',
                                '전체 strength.py의 단일 점수에는 위 누락이 남아 있음; 이번 감사는 분리 계산이며 영웅수치·효과·기존 순위 모델을 바꾸지 않음'])
OUT.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(output=str(OUT),variants=len(p['rows']),skill_lines=115,formation_count=len(forms),checks_passed=len(tests)),ensure_ascii=False))
