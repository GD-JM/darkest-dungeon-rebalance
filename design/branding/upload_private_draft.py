"""Darkest Refined 시안 전용 비공개 창작마당 아이템 생성·업로드 (BRAND_STYLE.md §8)
사용: workshop-sync 파이썬으로 실행 — & <codex python> -B design/branding/upload_private_draft.py
 [사용자 2026-10-29: "비공개 아이템 만들어서 올려줘"]
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
TITLE = '[PRIVATE DRAFT] Darkest Refined — Hero Rebalance & Reworks'


def fit_png(im, out, width):
    """Steam 갤러리 PNG 1MB 미만: 넘으면 조금씩 줄인다."""
    while True:
        g = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS) if width != im.width else im
        g.save(out, optimize=True)
        if out.stat().st_size < 990_000:
            return width
        width = int(width * 0.93)


def prepare():
    if UP.exists():
        shutil.rmtree(UP)
    UP.mkdir()
    im = Image.open(DRAFT / 'preview_darkest_refined.png').convert('RGB')
    im.save(UP / 'thumb.jpg', 'JPEG', quality=92)
    fit_png(im, UP / '00_preview.png', 900)
    files = [UP / '00_preview.png']
    for f in sorted(DRAFT.glob('intro_*.png')):
        src = Image.open(f).convert('RGB')
        fit_png(src, UP / f.name, src.width)
        files.append(UP / f.name)
    for f in sorted((DRAFT / 'templates').glob('*.png')):
        src = Image.open(f).convert('RGB')
        fit_png(src, UP / ('tpl_' + f.name), src.width)
        files.append(UP / ('tpl_' + f.name))
    for f in sorted((DRAFT / 'cards').glob('*.png')):
        files.append(shutil.copy(f, UP / ('card_' + f.name)))
    files = [Path(f) for f in files]
    for f in files + [UP / 'thumb.jpg']:
        assert 0 < f.stat().st_size < 1_000_000, f
    return files


def main():
    files = prepare()
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
            en = (DRAFT / 'description_en.txt').read_text(encoding='utf-8').strip()
            ko = (DRAFT / 'description_ko.txt').read_text(encoding='utf-8').strip()
            # 재업로드: 이미 올린 시안 이미지 슬롯을 제자리 교체(중복 추가 방지)
            owned = {p['filename'] for p in steam.query()['previews'] if p['type'] == 0}
            r = steam.update(title=TITLE, description=en, visibility=2, thumbnail=UP / 'thumb.jpg',
                             replace_previews=(owned, files), language='english')
            state.update(status='uploaded_en', previews=len(r['previews']))
            write_json(JOURNAL, state)
            steam.update(title=TITLE, description=ko, language='koreana')
            state.update(status='uploaded', url=f'https://steamcommunity.com/sharedfiles/filedetails/?id={item}')
            write_json(JOURNAL, state)
    print(json.dumps(state, ensure_ascii=False))


if __name__ == '__main__':
    main()
