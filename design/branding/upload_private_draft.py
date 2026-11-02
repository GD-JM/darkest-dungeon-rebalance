"""Darkest Refined 시안 전용 비공개 창작마당 아이템 생성·업로드 (BRAND_STYLE.md §8)
사용: workshop-sync 파이썬으로 실행 — & <codex python> -B design/branding/upload_private_draft.py [--templates]
  기본 = 실제 공개 페이지처럼(제목·10개 언어 설명·갤러리 = 소개 이미지 + 영웅마다 스포트라이트 → 그 영웅 카드)
  모든 언어 설명에 이미 [img]로 들어간 이미지(소개 1~3, 두 개편 스포트라이트)는 갤러리에서 뺀다.
  --templates = 템플릿 견본도 갤러리에 추가(검토용)
 [사용자 2026-10-29: "비공개 아이템 만들어서 올려줘" / "진짜처럼 만들어서 비공개로 올리자"]
 [사용자 2026-10-29: "영웅별로 … 뭐가 문제이고 패치 방향성 무엇으로 잡았고 어떻게 해결했는지 그래서 저거를 전부
  창작마당 이미지에 넣고 이미 설명과 본글에서 활용된 이미지는 저기서는 뺐으면 좋겠어"]
기존 공개 아이템 3821353035은 건드리지 않는다. 생성은 한 번만: 결과가 애매하면 재시도하지 않고 멈춘다.
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

WS = Path('C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync')
sys.path.insert(0, str(WS))
from common import read_json, write_json, WorkerLock
from steam import Steam, SteamError, ITEM_ID

GAME = 'C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon'
DRAFT = Path(GAME) / 'mods/Rebalance/design/branding/darkest_refined_draft'
HERE = Path(__file__).resolve().parent
UP = HERE / 'darkest_refined_draft' / '_upload'
JOURNAL = HERE / 'private_draft_item.json'
LANGS = ['english', 'koreana', 'brazilian', 'french', 'german', 'polish', 'russian', 'schinese', 'spanish', 'tchinese']
TITLES = {'english': 'Darkest Refined — Hero Rebalance & Reworks',
          'koreana': '다키스트 리파인드 — 영웅 리밸런스 & 리워크',
          'brazilian': 'Darkest Refined — Rebalanceamento e reformulações de heróis',
          'french': 'Darkest Refined — Rééquilibrage et refontes des héros',
          'german': 'Darkest Refined — Helden-Rebalance & Überarbeitungen',
          'polish': 'Darkest Refined — Balans i przebudowy bohaterów',
          'russian': 'Darkest Refined — ребаланс и переработка героев',
          'schinese': 'Darkest Refined — 英雄再平衡与重做',
          'spanish': 'Darkest Refined — Reajuste y reworks de héroes',
          'tchinese': 'Darkest Refined — 英雄再平衡與重製'}


def description(lang):
    """꾸민 설명(build_descriptions.py → final/, Steam 이미지 주소로 만든 것)이 있으면 그것, 없으면 원문."""
    final = DRAFT / 'final' / f'description_{lang}.txt'
    if final.exists() and 'images.steamusercontent.com' in final.read_text(encoding='utf-8'):
        f = final
    else:
        f = DRAFT / ('description_en.txt' if lang == 'english' else 'description_ko.txt' if lang == 'koreana'
                     else f'i18n/description_{lang}.txt')
    text = f.read_text(encoding='utf-8').strip()
    assert len(text.encode('utf-8')) + text.count(chr(10)) < 8000, lang  # Steam 한도: 줄바꿈은 CRLF 2바이트
    return text


def in_description():
    """모든 언어의 꾸민 설명에 [img]로 들어간 이미지(초안 폴더 기준 경로). 한 언어라도 빠졌으면 갤러리에 남긴다."""
    urls = json.loads((HERE / 'desc_asset_urls.json').read_text(encoding='utf-8'))
    texts = [description(lang) for lang in LANGS]
    used = set()
    for name, url in urls.items():          # 자산 이름: intro_1_healing.png / spotlight_antiquarian.png
        if all(url in t for t in texts):
            used.add(name.replace('spotlight_', 'spotlights/', 1) if name.startswith('spotlight_') else name)
    return used


def fit_png(im, out, width):
    """Steam 갤러리 PNG 1MB 미만: 넘으면 조금씩 줄인다."""
    while True:
        g = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS) if width != im.width else im
        g.save(out, optimize=True)
        if out.stat().st_size < 990_000:
            return width
        width = int(width * 0.93)


def prepare(templates=False):
    if UP.exists():
        shutil.rmtree(UP)
    UP.mkdir()
    im = Image.open(DRAFT / 'preview_darkest_refined.png').convert('RGB')
    im.save(UP / 'thumb.jpg', 'JPEG', quality=92)
    used = in_description()
    files = []

    def add(f, name):
        if f.relative_to(DRAFT).as_posix() in used:
            return
        src = Image.open(f).convert('RGB')
        fit_png(src, UP / name, src.width)
        files.append(UP / name)

    for f in sorted(DRAFT.glob('intro_[0-9]_*.png')):
        add(f, f.name)
    for f in sorted((DRAFT / 'templates').glob('*.png')) if templates else []:
        add(f, 'tpl_' + f.name)
    shown = set()
    for f in sorted((DRAFT / 'cards').glob('*.png')):      # 01_bounty_hunter_p1.png → bounty_hunter
        hero = f.stem[3:].removesuffix('_p1').removesuffix('_p2')
        spot = DRAFT / 'spotlights' / f'{hero}.png'
        if hero not in shown and spot.exists():
            add(spot, f'spot_{hero}.png')
        shown.add(hero)
        files.append(Path(shutil.copy(f, UP / ('card_' + f.name))))
    for f in files + [UP / 'thumb.jpg']:
        assert 0 < f.stat().st_size < 1_000_000, f
    return files


def main(templates=False):
    files = prepare(templates)
    state = read_json(JOURNAL, {})
    with WorkerLock(WS / 'runtime' / 'worker.lock'):
        if state.get('status') == 'creating':
            raise SteamError('Earlier creation outcome unknown; check owned items before any retry')
        if 'item_id' not in state:
            with Steam(GAME) as steam:
                if not steam.query()['owned']:
                    raise SteamError('Logged-in Steam user does not own the Rebalance item')
                def before():
                    state['status'] = 'creating'
                    write_json(JOURNAL, state)
                state.update(steam.create_item(before), status='created')
                write_json(JOURNAL, state)
        item = int(state['item_id'])
        assert item != ITEM_ID
        with Steam(GAME, item) as steam:
            # 재업로드: 이미 올린 시안 이미지 슬롯을 제자리 교체(중복 추가 방지, 남는 슬롯은 제거)
            owned = {p['filename'] for p in steam.query()['previews'] if p['type'] == 0}
            r = steam.update(title=TITLES['english'], description=description('english'), visibility=2,
                             thumbnail=UP / 'thumb.jpg', replace_previews=(owned, files), language='english')
            state.update(status='uploaded_en', previews=len(r['previews']), mode='templates' if templates else 'release-like')
            write_json(JOURNAL, state)
            for lang in LANGS[1:]:
                steam.update(title=TITLES[lang], description=description(lang), language=lang)
                state.update(status='uploaded_' + lang)
                write_json(JOURNAL, state)
            state.update(status='uploaded', url=f'https://steamcommunity.com/sharedfiles/filedetails/?id={item}')
            write_json(JOURNAL, state)
    print(json.dumps(state, ensure_ascii=False))


if __name__ == '__main__':
    main('--templates' in sys.argv)
