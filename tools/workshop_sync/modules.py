"""WS-MODULAR-001: split one validated release without changing hero data.

Only base + explicitly enabled DLC hero packages are combined. Native effects
are resolved against the same DLC selection, never the all-DLC installation.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
from common import LANGUAGES, read_json, sha256, write_json
from release import validate_payload

DLC = {'duelist':'4964110_fires_edge/features/duelist',
       'runaway':'4964110_fires_edge/features/runaway',
       'flagellant':'580100_crimson_court/features/flagellant',
       'shieldbreaker':'702540_shieldbreaker', 'musketeer':'445700_musketeer'}
KEYS = ('base', *DLC)
# Registered once with the owner's explicit approval, not arbitrary repository IDs.
APPROVED = dict(zip(KEYS,(3826129567,3826129595,3826129618,3826129642,3826129659,3826129680)))
FIELDS = re.compile(r'\.([A-Za-z_][A-Za-z_0-9]*)\s+((?:"[^"]*"|[^.\s][^\s]*)(?:\s+(?:"[^"]*"|(?!\.)[^\s]+))*)')
TOKENS = re.compile(r'"([^"]*)"|(\S+)')
EFFECT_FIELDS = {'effect','effects','human_effects','beast_effects','riposte_effect','riposte_effects',
                 'battle_start_effect_ids','stance_defensive_effects','stance_aggressive_effects','enter_effects'}
BUFF_FIELDS = {'buff_ids','buffs','recovery_buffs','recovery_heart_attack_buffs'}


def fields(line):
    return {m[1]:[a or b for a,b in TOKENS.findall(m[2])] for m in FIELDS.finditer(line.split('//',1)[0])}


def refs(text):
    effects, buffs = set(), set()
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('//'): continue
        for key, values in fields(line).items():
            if key in EFFECT_FIELDS: effects.update(values)
            elif key in BUFF_FIELDS: buffs.update(values)
    return effects, buffs


def effect_map(paths):
    result={}
    for path in sorted(paths):
        for line in path.read_text(encoding='utf-8-sig',errors='replace').splitlines():
            if not line.startswith('effect:'): continue
            name=fields(line).get('name',[])
            if not name: raise ValueError('Effect without name: '+str(path))
            if name[0] in result and result[name[0]] != line:
                # Native files can contain same-name definitions; first loaded wins.
                continue
            result.setdefault(name[0],line)
    return result


def buff_map(paths):
    result={}
    for path in sorted(paths):
        for buff in read_json(path,{}).get('buffs',[]):
            result.setdefault(buff['id'],buff)
    return result


def native(game, selected):
    roots=[game]+[game/'dlc'/DLC[key] for key in selected]
    effects={}; buffs={}
    for root in roots:
        # Root base must not recursively include every DLC or installed mod.
        ep=list((root/'effects').glob('*.effects.darkest'))
        bp=list((root/'shared/buffs').glob('*.json'))
        if root != game:
            ep=list(root.rglob('*.effects.darkest'))
            bp=list(root.rglob('*.buffs.json'))
        ep=[p for p in ep if 'modes' not in p.parts and 'arena_mp' not in str(p)]
        bp=[p for p in bp if 'modes' not in p.parts and 'arena_mp' not in str(p)]
        effects.update(effect_map(ep)); buffs.update(buff_map(bp))
    return effects,buffs


def closure(texts, custom_e, custom_b, native_e, native_b, extra=()):
    needed_e=set(); needed_b=set(); visited=set(); pending=list(extra); buffs=set()
    for text in texts:
        er,br=refs(text); pending.extend(er); buffs.update(br)
    while pending:
        name=pending.pop()
        if name in visited: continue
        visited.add(name)
        if name in custom_e:
            needed_e.add(name); line=custom_e[name]
        elif name in native_e: line=native_e[name]
        else: raise ValueError('Unavailable effect for selected DLC: '+name)
        if 'actor_dot' in fields(line): raise ValueError('Actor DOT dependency requires explicit packaging support: '+name)
        er,br=refs(line); pending.extend(er); buffs.update(br)
    visited_b=set()
    while buffs:
        name=buffs.pop()
        if name in visited_b: continue
        visited_b.add(name)
        if name in custom_b:
            needed_b.add(name); buff=custom_b[name]
        elif name in native_b: buff=native_b[name]
        else: raise ValueError('Unavailable buff for selected DLC: '+name)
        buffs.update(buff.get('clear_buffs_on_rule_active',[]))
    return needed_e,needed_b


def manifest(payload):
    path=payload/'modfiles.txt'
    path.write_text('',encoding='utf-8')
    for _ in range(20):
        value=''.join(f'{p.relative_to(payload).as_posix()} {p.stat().st_size}\n'
                      for p in sorted(payload.rglob('*')) if p.is_file())
        old=path.read_text(encoding='utf-8')
        path.write_text(value,encoding='utf-8',newline='\n')
        if old==value: return validate_payload(payload)
    raise ValueError('Manifest size did not converge')


TEXT = {
 'english':('Base game — 15 heroes','Optional hero patch','No DLC is required.','Enable this base package and only the hero patches whose DLC heroes are enabled in your save.','Requires the base package and this hero’s official DLC, with the hero enabled in your save.','Do not enable alongside the all-DLC edition.','Same approved rebalance; no additional balance changes. See the hero comparison images.','File dependencies checked; in-game launch testing is still pending.','Base package','All-DLC edition'),
 'koreana':('본편 — 15영웅','선택 영웅 패치','DLC가 필요하지 않습니다.','이 본편판과 영지에서 해당 DLC 영웅을 켠 패치만 활성화하세요.','본편판과 해당 영웅의 공식 DLC가 필요하며 영지에서 해당 영웅을 켜야 합니다.','기존 전체 DLC판과 함께 활성화하지 마세요.','승인된 동일 리밸런스이며 추가 수치 변경은 없습니다. 영웅 비교 이미지를 참고하세요.','파일 의존성을 검사했으며 게임 실행 검증은 아직 남아 있습니다.','본편판','전체 DLC판'),
 'schinese':('本体版 — 15位英雄','可选英雄补丁','不需要任何DLC。','启用本体版，只添加存档中已启用对应DLC英雄的补丁。','需要本体版和该英雄的官方DLC，并在存档中启用该英雄。','请勿与全DLC版同时启用。','采用同一套已确定的平衡调整，没有额外数值改动。详情见英雄对比图片。','已检查文件依赖；游戏启动测试仍待完成。','本体版','全DLC版'),
 'tchinese':('本體版 — 15位英雄','可選英雄補丁','不需要任何DLC。','啟用本體版，只加入存檔中已啟用對應DLC英雄的補丁。','需要本體版與該英雄的官方DLC，並在存檔中啟用該英雄。','請勿與全DLC版同時啟用。','採用同一套已確定的平衡調整，沒有額外數值變更。詳見英雄對比圖片。','已檢查檔案依賴；遊戲啟動測試仍待完成。','本體版','全DLC版'),
 'french':('Jeu de base — 15 héros','Patch de héros facultatif','Aucun DLC requis.','Activez cette base et uniquement les patchs des héros DLC activés dans votre sauvegarde.','Nécessite la base et le DLC officiel de ce héros, activé dans la sauvegarde.','Ne pas activer avec l’édition tous DLC.','Même rééquilibrage validé, sans modification supplémentaire. Voir les images comparatives.','Dépendances des fichiers vérifiées ; test de lancement en jeu encore à faire.','Base','Édition tous DLC'),
 'german':('Grundspiel — 15 Helden','Optionaler Heldenpatch','Kein DLC erforderlich.','Aktiviere diese Basis und nur Patches für DLC-Helden, die im Spielstand aktiviert sind.','Benötigt die Basis und den offiziellen DLC dieses Helden; der Held muss im Spielstand aktiviert sein.','Nicht zusammen mit der Ausgabe für alle DLCs aktivieren.','Dieselben bestätigten Balanceänderungen, keine zusätzlichen Werteänderungen. Siehe Vergleichsbilder.','Dateiabhängigkeiten geprüft; Starttest im Spiel steht noch aus.','Basispaket','Ausgabe für alle DLCs'),
 'russian':('Основная игра — 15 героев','Дополнительный патч героя','DLC не требуются.','Включите эту основу и только патчи героев DLC, включённых в сохранении.','Нужны основа и официальный DLC этого героя; герой должен быть включён в сохранении.','Не включайте вместе с версией для всех DLC.','Те же утверждённые изменения баланса, без дополнительных правок. Смотрите изображения сравнения.','Зависимости файлов проверены; запуск в игре ещё не проверен.','Основной пакет','Версия для всех DLC'),
 'spanish':('Juego base — 15 héroes','Parche de héroe opcional','No requiere DLC.','Activa esta base y solo los parches de héroes DLC activados en tu partida.','Requiere la base y el DLC oficial de este héroe, con el héroe activado en la partida.','No activar junto a la edición con todos los DLC.','Mismo reequilibrado aprobado, sin cambios adicionales. Consulta las imágenes comparativas.','Dependencias verificadas; la prueba de inicio en el juego sigue pendiente.','Paquete base','Edición con todos los DLC'),
 'polish':('Gra podstawowa — 15 bohaterów','Opcjonalna łatka bohatera','DLC nie są wymagane.','Włącz tę podstawę i tylko łatki bohaterów DLC włączonych w zapisie gry.','Wymaga podstawy i oficjalnego DLC tego bohatera oraz włączenia bohatera w zapisie gry.','Nie włączaj razem z wersją dla wszystkich DLC.','Te same zatwierdzone zmiany balansu, bez dodatkowych zmian. Zobacz obrazy porównawcze.','Sprawdzono zależności plików; test uruchomienia w grze pozostaje do wykonania.','Pakiet podstawowy','Wersja dla wszystkich DLC'),
 'brazilian':('Jogo base — 15 heróis','Patch opcional de herói','Não requer DLC.','Ative esta base e apenas os patches dos heróis de DLC ativados no seu save.','Requer a base e o DLC oficial deste herói, com o herói ativado no save.','Não ative junto com a edição de todos os DLCs.','Mesmo rebalanceamento aprovado, sem alterações adicionais. Veja as imagens comparativas.','Dependências dos arquivos verificadas; teste de inicialização no jogo ainda pendente.','Pacote base','Edição de todos os DLCs')}


def descriptions(key, registry):
    result=[]
    for lang in LANGUAGES:
        t=TEXT[lang]; scope=t[0] if key=='base' else key.replace('_',' ').title()+' — '+t[1]
        body=f'[h1]Every Hero Worth Taking — {scope}[/h1]\n\n'+(t[2]+' '+t[3] if key=='base' else t[4])+'\n\n[b]'+t[5]+'[/b]\n\n'+t[6]+'\n\n'+t[7]+'\n\n'
        body+=f'[url=https://steamcommunity.com/sharedfiles/filedetails/?id={registry["base"]["item_id"]}]{t[8]}[/url]\n'
        if key=='base':
            body+='\n'.join(f'[url=https://steamcommunity.com/sharedfiles/filedetails/?id={registry[k]["item_id"]}]{k.title()}[/url]' for k in DLC)+'\n'
        body+=f'[url=https://steamcommunity.com/sharedfiles/filedetails/?id=3821353035]{t[9]}[/url]'
        result.append({'language':lang,'title':'Every Hero Worth Taking — '+scope,'body':body})
    return result


def prepare_modules(config, job, release, registry):
    if set(registry)!=set(KEYS) or any(int(registry[k]['item_id'])!=APPROVED[k] for k in KEYS):
        raise ValueError('Module registry differs from the six explicitly approved items')
    game=Path(config['game_root']); aio=Path(release['payload'])
    if validate_payload(aio)!=release['payload_hashes']: raise ValueError('AIO payload changed')
    for rel in release['payload_hashes']:
        if rel in {'project.xml','modfiles.txt','preview_icon.png'}: continue
        if rel.startswith(('heroes/','effects/','shared/buffs/','localization/')): continue
        raise ValueError('New payload category requires an explicit module packaging rule: '+rel)
    all_heroes={p.name for p in (aio/'heroes').iterdir() if p.is_dir()}
    if len(all_heroes)!=20 or not set(DLC)<=all_heroes: raise ValueError('Expected approved 20-hero roster')
    groups={k:({k} if k!='base' else all_heroes-set(DLC)) for k in KEYS}
    custom_e=effect_map((aio/'effects').glob('*.effects.darkest'))
    custom_b=buff_map((aio/'shared/buffs').glob('*.json'))
    texts={k:[p.read_text(encoding='utf-8-sig') for h in groups[k] for p in (aio/'heroes'/h).glob('*.darkest')] for k in KEYS}
    needs={k:closure(texts[k],custom_e,custom_b,*native(game,[] if k=='base' else [k])) for k in KEYS}
    # Shared custom definitions live once in base; duplicate file-order overrides are avoided.
    shared_e={n for n in custom_e if sum(n in needs[k][0] for k in KEYS)>1}
    shared_b={n for n in custom_b if sum(n in needs[k][1] for k in KEYS)>1}
    extra_e,extra_b=closure([],custom_e,custom_b,*native(game,[]),extra=shared_e)
    needs['base'][0].update(extra_e); needs['base'][1].update(extra_b|shared_b)
    for k in DLC:
        needs[k][0].difference_update(needs['base'][0]); needs[k][1].difference_update(needs['base'][1])
    report={'source_sha':release['source_sha'],'runtime_tested':False,'combinations':[]}
    for count in range(6):
        for combo in itertools.combinations(DLC,count):
            keys=('base',*combo)
            es=[n for k in keys for n in needs[k][0]]; bs=[n for k in keys for n in needs[k][1]]
            if len(es)!=len(set(es)) or len(bs)!=len(set(bs)): raise ValueError('Duplicate custom definitions')
            closure([t for k in keys for t in texts[k]],{n:custom_e[n] for n in es},{n:custom_b[n] for n in bs},*native(game,combo))
            report['combinations'].append({'dlc_heroes':list(combo),'hero_count':15+count,'effects':len(es),'buffs':len(bs),'passed':True})
    write_json(job/'modules-validation.json',report)
    releases={}
    for key in KEYS:
        child=job/'modules'/key; child.mkdir(parents=True,exist_ok=True)
        previous=read_json(child/'release.json')
        if previous:
            if previous.get('parent_digest')!=release['digest'] or previous.get('item_id')!=APPROVED[key]: raise ValueError('Prepared module input changed')
            if validate_payload(Path(previous['payload']))!=previous['payload_hashes']: raise ValueError('Prepared module payload changed')
            for image in previous['images']:
                if sha256(Path(previous['image_dir'])/image['path'])!=image['sha256']: raise ValueError('Prepared module image changed')
            releases[key]=previous; continue
        payload=child/'payload'
        if payload.exists(): raise ValueError('Incomplete module build exists; inspect before retry: '+str(payload))
        payload.mkdir()
        for hero in sorted(groups[key]): shutil.copytree(aio/'heroes'/hero,payload/'heroes'/hero)
        if key=='base' and (aio/'localization').exists(): shutil.copytree(aio/'localization',payload/'localization')
        (payload/'effects').mkdir()
        (payload/'effects'/f'rebalance_{key}_module.effects.darkest').write_text('\n'.join(custom_e[n] for n in sorted(needs[key][0]))+'\n',encoding='utf-8')
        write_json(payload/'shared/buffs'/f'rebalance_{key}_module.buffs.json',{'buffs':[custom_b[n] for n in sorted(needs[key][1])]})
        shutil.copy2(aio/'preview_icon.png',payload/'preview_icon.png')
        desc=descriptions(key,registry)
        tree=ET.parse(aio/'project.xml'); root=tree.getroot()
        values={'PublishedFileId':str(APPROVED[key]),'Title':desc[0]['title'],'ItemDescription':desc[0]['body'],
                'ItemDescriptionShort':desc[0]['title'],'ModDataPath':str(payload.resolve()).replace('\\','/')+'/', 'Visibility':'public','UpdateDetails':release['note']}
        for tag,value in values.items():
            node=root.find(tag)
            if node is None: node=ET.SubElement(root,tag)
            node.text=value
        tree.write(payload/'project.xml',encoding='utf-8',xml_declaration=True)
        image_dir=child/'images'; image_dir.mkdir(); images=[]
        for image in release['images']:
            if image['hero'] not in groups[key]: continue
            src=Path(release['image_dir'])/image['path']
            if sha256(src)!=image['sha256']: raise ValueError('AIO image changed')
            shutil.copy2(src,image_dir/src.name); images.append(dict(image,path=src.name))
        if not images: raise ValueError('Module has no corresponding hero images')
        child_release={k:release[k] for k in ('source_sha','previous_sha','version','note')}
        child_release.update(item_id=APPROVED[key],parent_digest=release['digest'],descriptions=desc,images=images,
                             image_dir=str(image_dir.resolve()),payload=str(payload.resolve()),payload_hashes=manifest(payload))
        child_release['digest']=hashlib.sha256(json.dumps(child_release,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        write_json(child/'release.json',child_release); releases[key]=child_release
    return releases
