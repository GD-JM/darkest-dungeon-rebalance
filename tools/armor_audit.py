import pathlib,json,re,copy,statistics as st,time,hashlib,argparse
import strength as S
import armor_valuation as V
from armor_inventory import build_inventory

def equip(H,row,eff,buffs,ids,trinkets):
    H=copy.deepcopy(H);eff=dict(eff);d=S.kv(row);attack=S.first(d,'type');mods={};ignored=[];active=[]
    for id in ids:
        t=trinkets[id]
        assert not t['heroes'] or H['id'] in t['heroes']
        for b in t['buffs']:
            rule=b.get('rule_type','always');stat=b.get('stat_type');sub=b.get('stat_sub_type');a=b.get('amount',0)
            ok=rule in ('always',None,attack+'only')
            if rule=='riposte' and stat=='combat_stat_add' and sub=='crit_chance':
                H['gear_riposte_crit']=H.get('gear_riposte_crit',0)+a;active.append(b);continue
            if not ok:ignored.append(b);continue
            active.append(b)
            key=(stat,sub);mods[key]=mods.get(key,0)+a
    acc=100*mods.get(('combat_stat_add','attack_rating'),0);crit=100*mods.get(('combat_stat_add','crit_chance'),0)
    H['wcrit']+=crit;H['def']+=100*mods.get(('combat_stat_add','defense_rating'),0);H['spd']+=mods.get(('combat_stat_add','speed_rating'),0)
    H['dmg']=(H['dmg'][0]*(1+mods.get(('combat_stat_multiply','damage_low'),0)),H['dmg'][1]*(1+mods.get(('combat_stat_multiply','damage_high'),0)))
    row=re.sub(r'\.atk ([\d.]+)%',lambda m:f'.atk {float(m[1])+acc:g}%',row)
    deb=100*mods.get(('debuff_chance',''),0);mov=100*mods.get(('move_chance',''),0)
    for name in S.ec.effect_names_in(row):
        text=eff.get(name,'');k=S.kv(text);who=S.first(k,'target','target')
        bonus=mov if 'pull' in k or 'push' in k else deb if who=='target' and V.effect_mods(text,buffs,True) else 0.
        if bonus:eff[name]=re.sub(r'\.chance ([\d.]+)%',lambda m:f'.chance {float(m[1])+bonus:g}%',text)
    return H,row,eff,dict(ids=ids,names=[trinkets[i]['name'] for i in ids],acc=acc,crit=crit,debuff=deb,move=mov,active=active,conditional_not_assumed=ignored)

def run(output):
    R=pathlib.Path(output);R.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();print('Initialize...',flush=True)
    inventory=build_inventory()
    (R/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    base=S.evaluate('vanilla')
    P=dict(S.PARAM,STRESS_HP=S.stress_value(S.PARAM,median_hp=S.PARAM_MED_HP),STRESS_TAKEN=S._STRESS_CACHE,MARK_DAMAGE_BONUS=S.marked_damage_bonus(),HEAL_FOLLOWUP_AMOUNT=S.followup_heal_amount(S.PARAM['HEAL_CRIT_SGL']),PARTY_ATTACKS=3.,FOCUS_SHARE=.5,
           ENEMY_DOT_TICKS=2.,ALLY_BLEED_RESIST=.6,ALLY_BLIGHT_RESIST=.6,ALLY_STUN_RESIST=.8,ALLY_STUN_ACTION_AVAILABLE=1.,ALLY_ACTION_HP=V.STANDARD,ALLY_DODGE=25,ALLY_SPEED=7)
    trinkets={t['id']:t for t in inventory['trinkets']}
    classgear={'antiquarian':'cc_set_anti_the_masters_essence','duelist':'duelist_set_academie_ring','leper':'debuff_amulet','man_at_arms':'cc_set_maa_old_unit_banner','musketeer':'cc_set_musk_silver_bullet','occultist':'demons_cauldron','shieldbreaker':'sb_set_1','vestal':'debuff_amulet','bounty_hunter':'debuff_amulet','houndmaster':'debuff_amulet'}


    out=dict(model='R-AUDIT-26',base_commit=inventory['head'],standard_hp=V.STANDARD,parameters=P,skills={},trinkets=inventory['trinkets'],game_data_writes=False,
             source_hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in (R/'inventory.json',pathlib.Path(V.__file__),pathlib.Path(__file__))})
    for key,entry in inventory['skills'].items():
        hero,id=key.split('|');out['skills'][key]={}
        for mode in ('vanilla','rb'):
            r=entry[mode][-1];H=S.load_hero(hero,mode);eff=S.load_effects(mode);buffs=S.ec.load_buffs(S.G,S.M_ROOT if mode=='rb' else None)
            data={}
            for scenario in ('uniform','ranks'):
                data[scenario]=V.evaluate_skill(H,r['row'],eff,buffs,P,scenario)
            if mode=='rb':
                data['gear']=[]
                for ids in ([classgear[hero]],[classgear[hero],'focus_ring']):
                    hh,row,ee,gear=equip(H,r['row'],eff,buffs,ids,trinkets)
                    v=V.evaluate_skill(hh,row,ee,buffs,P,'ranks');v['equipment']=gear
                    stress=sum(b.get('amount',0) for b in gear['active'] if b.get('stat_type')=='stress_dmg_received_percent')
                    v['gear_exposure_hp_per_enemy_action']=st.mean(V.enemy_action_hp(m,{},dict(P,ALLY_DODGE=hh['def'],ALLY_STRESS_MULTIPLIER=stress))-V.enemy_action_hp(m,{},dict(P,ALLY_DODGE=H['def'])) for m in V.monster_pool('C'))
                    data['gear'].append(v)
                data['armor_scenarios']={}
                for prot in (0,20,40,60):
                    data['armor_scenarios'][str(prot)]=V.evaluate_skill(H,r['row'],eff,buffs,P,'prot'+str(prot))
                if hero=='duelist':
                    data['ripostes']={str(n):V.evaluate_skill(H,r['row'],eff,buffs,P,'ranks',ripostes=n) for n in (1,2)}
                data['followups']={str(n):V.evaluate_skill(H,r['row'],eff,buffs,dict(P,PARTY_ATTACKS=n),'ranks') for n in (0,1,2,4)}
                physical=tuple((S.load_hero(h,'rb')['dmg'],105,S.load_hero(h,'rb')['wcrit']/100,0.) for h in ('crusader','leper','bounty_hunter'))
                data['physical_party']=V.evaluate_skill(H,r['row'],eff,buffs,dict(P,SUPPORT_PROFILES=physical),'prot40')
            data['levels']=[]
            for level in range(5):
                hh=S.load_hero(hero,mode,level);lr=entry[mode][level]['row']
                lp=dict(P,ALLY_DODGE=5+level*5,ALLY_SPEED=6,ALLY_BLEED_RESIST=.2+level*.1,ALLY_BLIGHT_RESIST=.2+level*.1,ALLY_STUN_RESIST=.4+level*.1)
                data['levels'].append(V.evaluate_skill(hh,lr,eff,buffs,lp,'ranks'))
            out['skills'][key][mode]=data
            print(key,mode,'uniform',round(data['uniform']['pp'],1),'ranks',round(data['ranks']['pp'],1),data['ranks']['parts_pp'],flush=True)
    out['elapsed']=time.monotonic()-start
    (R/'comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',out['elapsed'],flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description='R-AUDIT-26 armor support audit; no game writes')
    ap.add_argument('--output',required=True,type=pathlib.Path)
    args=ap.parse_args();run(args.output)
    from armor_scenarios import run as extra
    extra(args.output)
