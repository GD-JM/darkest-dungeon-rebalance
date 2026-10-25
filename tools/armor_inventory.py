import pathlib,json,re,hashlib,subprocess
import strength as S
M=pathlib.Path(S.M_ROOT)

def build_inventory():
    buffs=S.ec.load_buffs(S.G,S.M_ROOT);loc=S.ec.load_korean(S.G)
    out={'skills':{},'trinkets':[],'excluded_files':[],'game':str(S.G),'repo':str(M),'head':subprocess.check_output(['git','-C',str(M),'rev-parse','HEAD']).decode().strip()}
    for mode in ('vanilla','rb'):
     e=S.load_effects(mode);b=S.ec.load_buffs(S.G,S.M_ROOT if mode=='rb' else None)
     for hero in S.KO:
      for level in range(5):
       H=S.load_hero(hero,mode,level)
       for row,k in H['skills']:
        effects=[e.get(n,'') for n in S.ec.effect_names_in(row)]
        armor=[]
        for text in effects:
         z=S.kv(text)
         if S.first(z,'target') not in ('target','target_group'):continue
         if S.num(S.first(z,'protection_rating_add'))<0:armor.append(text)
         for n in z.get('buff_ids',[]):
          q=b.get(n.strip('"'),{})
          if q.get('stat_sub_type')=='protection_rating' and q.get('amount',0)<0:armor.append(text)
        if armor:
         key=hero+'|'+S.first(k,'id');entry=out['skills'].setdefault(key,{})
         entry.setdefault(mode,[]).append(dict(level=level+1,row=row,stats=k,effects=effects,armor=armor,weapon=H['dmg'],weapon_crit=H['wcrit'],crit_effects={n:e.get(n) for n in H['crit_effects']}))
    # Fill counterpart skills even where their armor debuff was added/removed.
    for key,entry in out['skills'].items():
     h,id=key.split('|')
     for mode in ('vanilla','rb'):
      if mode in entry:continue
      e=S.load_effects(mode);entry[mode]=[]
      for level in range(5):
       H=S.load_hero(h,mode,level)
       for row,k in H['skills']:
        if S.first(k,'id')==id:entry[mode].append(dict(level=level+1,row=row,stats=k,effects=[e.get(n,'') for n in S.ec.effect_names_in(row)],armor=[],weapon=H['dmg'],weapon_crit=H['wcrit'],crit_effects={n:e.get(n) for n in H['crit_effects']}))
    heroes={key.split('|')[0] for key in out['skills']}
    entries={}
    for base in (pathlib.Path(S.G)/'trinkets',pathlib.Path(S.G)/'dlc',M/'trinkets',M/'dlc'):
     for file in sorted(base.rglob('*.entries.trinkets.json')):
      if 'arena' in str(file).lower():continue
      try:data=json.loads(file.read_text(encoding='utf-8-sig'))
      except (UnicodeDecodeError,json.JSONDecodeError) as e:
       out['excluded_files'].append(dict(path=str(file),error=str(e),header=file.read_bytes()[:20].hex()));continue
      for item in data.get('entries',[]):
       h=item.get('hero_class_requirements',[])
       if isinstance(h,str):h=[h]
       bs=[buffs.get(n,{}) for n in item.get('buffs',[])]
       related=bool(set(h)&heroes)
       common=not h and any(x.get('stat_type') in ('debuff_chance','combat_stat_add','combat_stat_multiply','move_chance') for x in bs)
       if related or common:
        entries[item['id']]=dict(id=item['id'],name=loc.get('str_inventory_title_trinket'+item['id'],loc.get('str_inventory_title_trinket_'+item['id'],item['id'])),heroes=h,buffs=bs,raw=item,source=str(file))
    out['trinkets']=list(entries.values())
    out['inventory_hashes']={p:hashlib.sha256((M/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','-C',str(M),'ls-files']).decode().splitlines() if (M/p).is_file()}
    return out
