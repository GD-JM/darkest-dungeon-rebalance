"""R-AUDIT-25 reproducible residual audit. Reads a fixed Git baseline, never edits game files."""
import sys,json,pathlib,time,re,statistics as st,functools,hashlib,argparse,subprocess
import strength as S
import damage_support as D
p=argparse.ArgumentParser()
p.add_argument('--baseline',default='cd4bee0')
p.add_argument('--output',type=pathlib.Path,required=True)
args=p.parse_args()
M=pathlib.Path(S.M_ROOT)
R=args.output.parent
R.mkdir(parents=True,exist_ok=True)
def git(*x):return subprocess.check_output(['git','-C',str(M),*x]).decode('utf-8')
baseline=git('rev-parse',args.baseline).strip()
@functools.lru_cache(maxsize=None)
def source(path):return git('show',baseline+':'+path)
original_hero=S.load_hero
def frozen_hero(hero,mode,level=4):
    if mode=='vanilla':return original_hero(hero,mode,level)
    path=f'heroes/{hero}/{hero}.info.darkest'
    return S.parse_hero(hero,source(path),level)
S.load_hero=frozen_hero
original_effects=S.load_effects
@functools.lru_cache(maxsize=None)
def frozen_effects(mode):
    effects=original_effects('vanilla')
    if mode=='rb':
        for path in git('ls-tree','-r','--name-only',baseline,'effects').splitlines():
            if not path.endswith('.effects.darkest'):continue
            for row in source(path).splitlines():
                match=re.match(r'effect:.*?\.name\s+"([^"]+)"',row)
                if match:effects[match[1]]=row
    return effects
S.load_effects=frozen_effects
t=time.monotonic()
print('Initializing fixed vanilla reference...',flush=True)
vanilla=S.evaluate('vanilla')
standard=8.14872802734375 # R-AUDIT-24 fixed reference; never re-normalize candidates
print('fixed reference',standard,flush=True)
P=dict(S.PARAM,STRESS_HP=S.stress_value(S.PARAM,median_hp=S.PARAM_MED_HP),STRESS_TAKEN=S._STRESS_CACHE,MARK_DAMAGE_BONUS=S.marked_damage_bonus(),HEAL_FOLLOWUP_AMOUNT=S.followup_heal_amount(S.PARAM['HEAL_CRIT_SGL']))
eff=S.load_effects('rb');buffs=S.ec.load_buffs(S.G,S.M_ROOT)
H=S.load_hero('shieldbreaker','rb')
rows={S.first(d,'id'):l for l,d in H['skills']}
def calc(row,extra=None,params=None,hero=H):
 C=S.Ctx(hero,dict(eff,**(extra or {})),buffs,dict(P,**(params or {})))
 v,parts=S.skill_value(C,row,S.kv(row))
 return dict(hp=v,pp=v/standard*100-100,parts={k:x/standard*100 for k,x in parts.items()})
def variant(damage,keep_slow=True,armor=40):
 row=rows['break_guard'].replace('.target 1234','.target 123')
 row=re.sub(r'\.dmg -50%',f'.dmg {damage}%',row)
 if not keep_slow:row=re.sub(r' "Daze Slowdown 5"','',row)
 row+=' "AUDIT ARMOR"' # effect list is final field for this skill; assert below
 assert 'AUDIT ARMOR' in S.ec.effect_names_in(row),row
 extra={'AUDIT ARMOR':f'effect: .name "AUDIT ARMOR" .target target .chance 140% .duration 2 .combat_stat_buff 1 .protection_rating_add -{armor}% .on_hit true .on_miss false'}
 return row,extra
out={'standard_hp':standard,'base_commit':baseline,'model':'R-AUDIT-25','sample':S.MONS,'stealth_coverage':{str(rs):D.destealth_coverage(S,rs) for rs in [(1,2,3),(1,2,3,4)]},'vanilla':vanilla['shieldbreaker']['skills'],'before':{s:calc(rows[s]) for s in ('break_guard','expose')},'puncture_grid':[],'expose_grid':[]}
print('Current',out['before'],flush=True)
for keep in (True,False):
 for damage in (-50,-55,-60,-65,-70,-75,-80):
  row,extra=variant(damage,keep)
  val=calc(row,extra)
  val.update(damage=damage,keep_slow=keep,residual_pp=val['pp']-out['before']['break_guard']['pp'])
  out['puncture_grid'].append(val)
  print('Puncture',damage,keep,round(val['residual_pp'],3),flush=True)
for damage in (-40,-45,-50,-55,-60):
 row=rows['expose'].replace('.target 123','.target 1234').replace('.dmg -40%',f'.dmg {damage}%')
 val=calc(row);val.update(damage=damage,residual_pp=val['pp']-out['before']['expose']['pp']);out['expose_grid'].append(val)
 print('Expose',damage,round(val['residual_pp'],3),flush=True)
out['sensitivity']=[]
for attacks in (0,.5,1.5,3):
 for death in (.2,.393,.6):
  params=dict(TGT_ATTACKS=attacks,DEATH_RATE=death)
  before=calc(rows['break_guard'],params=params)
  for damage,slow in ((-60,True),(-65,True),(-70,True),(-55,False),(-60,False),(-65,False)):
   row,extra=variant(damage,slow);v=calc(row,extra,params)
   out['sensitivity'].append(dict(attacks=attacks,death=death,damage=damage,slow=slow,residual_pp=v['pp']-before['pp']))
out['support_skills']={}
for hero,skill in [('antiquarian','flashpowder'),('vestal','gods_illumination'),('man_at_arms','bellow'),('occultist','weakening_curse')]:
 hh=S.load_hero(hero,'rb');r=next(l for l,d in hh['skills'] if S.first(d,'id')==skill)
 old=calc(r,hero=hh)
 if hero=='antiquarian':
  extra={'RB ANT Flash Armor 5':eff['RB ANT Flash Armor 5'].replace('-20%','-15%')}
  new=calc(r,extra,hero=hh)
 else:new=old
 out['support_skills'][hero]=dict(before=old,after=new)
out['party_gear_sensitivity']=[]
for gear in (0,40):
 for party in ('standard','crusader_leper'):
  extras={}
  for name,text in eff.items():
   if name.startswith('Daze Slowdown '):
    extras[name]=re.sub(r'\.chance ([\d.]+)%',lambda m:f'.chance {float(m[1])+gear:g}%',text)
  ps=tuple((tuple(hh['dmg']),105,hh['wcrit']/100,0.) for h in ('crusader','leper') for hh in [S.load_hero(h,'vanilla')]) if party=='crusader_leper' else None
  params=dict(SUPPORT_PROFILES=ps)
  before=calc(rows['break_guard'],extras,params)
  row,newextra=variant(-55,False)
  newextra['AUDIT ARMOR']=newextra['AUDIT ARMOR'].replace('chance 140%',f'chance {140+gear}%')
  after=calc(row,dict(extras,**newextra),params)
  out['party_gear_sensitivity'].append(dict(gear=gear,party=party,residual_pp=after['pp']-before['pp']))
out['levels']=[]
for level in range(5):
 tier=('A','A','B','B','C')[level]
 hh=S.load_hero('shieldbreaker','rb',level);rr=next(l for l,d in hh['skills'] if S.first(d,'id')=='break_guard')
 armor=(30,32,35,37,40)[level]
 extra={f'AUDIT ARMOR {level}':f'effect: .name "AUDIT ARMOR {level}" .target target .chance {100+10*level}% .duration 2 .combat_stat_buff 1 .protection_rating_add -{armor}%'}
 nr=re.sub(r' "Daze Slowdown \d"','',rr.replace('.dmg -50%','.dmg -55%').replace('.target 1234','.target 123'))+f' "AUDIT ARMOR {level}"'
 cc=S.Ctx(hh,dict(eff,**extra),buffs,P);pool=S.load_monsters(tier)
 gain,_=D.support_value(S,cc,nr,S.kv(nr),[cc.eff.get(n,'') for n in S.ec.effect_names_in(nr)],pool)
 cr=hh['wcrit']/100;acc=90+5*level
 direct_delta=st.mean(S.hit(m,acc)*(S.damage_mean(hh['dmg'],-55,cr,m['prot'])-S.damage_mean(hh['dmg'],-50,cr,m['prot'])) for m in pool)
 out['levels'].append(dict(level=level+1,tier=tier,monsters=len(pool),armor=armor,chance=100+10*level,added_support_hp=gain,direct_delta_hp=direct_delta,note='Direct/support only; excludes lost slow and reach, not full skill balance.'))
out['finite_scenarios']=[]
for hp in (10,30,60):
 for prot in (0,.2,.4,.6):
  for attacks in (1,2,3):
   for hero in ('crusader','leper'):
    hh=S.load_hero(hero,'vanilla');p=dict(weapon=tuple(hh['dmg']),acc=105,crit=hh['wcrit']/100,modifier=0,hp=hp,dodge=20,attacks=attacks)
    before=D.finite_sequence(S,prot=prot,**p);after=D.finite_sequence(S,prot=max(0,prot-.4),**p)
    out['finite_scenarios'].append(dict(hero=hero,hp=hp,prot=prot,attacks=attacks,gain_hp=after-before,ehp_before=D.ehp(hp,prot),ehp_after=D.ehp(hp,max(0,prot-.4))))
out['parameters']=P
out['elapsed']=time.monotonic()-t
out['tool_hashes']={n:hashlib.sha256((pathlib.Path(__file__).parent/n).read_bytes()).hexdigest() for n in ('strength.py','damage_support.py')}
out['game_rules_sha256']=hashlib.sha256((pathlib.Path(S.G)/'shared/rules.json').read_bytes()).hexdigest()
out['baseline_sources_sha256']={p:hashlib.sha256(source(p).encode('utf-8')).hexdigest() for p in git('ls-tree','-r','--name-only',baseline,'heroes','effects').splitlines() if p.endswith(('.info.darkest','.effects.darkest'))}
# This manifest identifies the game data used; it does not claim a frozen binary runtime.
out['game_inputs_sha256']={}
for root in ('heroes','monsters','effects','shared','dlc','dungeons'):
    for file in (pathlib.Path(S.G)/root).rglob('*'):
        if file.is_file() and 'arena' not in file.parts and file.name.endswith(('.info.darkest','.info원본.darkest','.effects.darkest','.buffs.json','.monster_brains.json','.mash.darkest')):
            out['game_inputs_sha256'][str(file.relative_to(S.G))]=hashlib.sha256(file.read_bytes()).hexdigest()

args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',out['elapsed'],flush=True)
