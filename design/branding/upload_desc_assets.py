"""설명란 꾸밈 이미지 보관용 비공개 창작마당 아이템 (BRAND_STYLE.md §5-B, §8)
사용: & <codex python> -B design/branding/upload_desc_assets.py
- darkest_refined_draft/desc/*.png + 설명 안에 넣는 소개·스포트라이트 이미지를 갤러리로 올리고,
  Steam이 준 이미지 주소를 desc_asset_urls.json에 저장한다(설명 [img] 태그용).
- 생성은 한 번만: 결과가 애매하면 재시도하지 않고 멈춘다. 공개 아이템 3821353035은 건드리지 않는다.
 [사용자 2026-10-29: "첨부 이미지처럼 설명도 꾸밀 수가 있어 … 우리 스타일에 어울릴만한 것들 찾아서 적용해봐봐"]
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

WS = Path('C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync')
sys.path.insert(0, str(WS))
from common import read_json, write_json, WorkerLock
from steam import Steam, SteamError, ITEM_ID

GAME = 'C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon'
HERE = Path(__file__).resolve().parent
DRAFT = HERE / 'darkest_refined_draft'
UP = DRAFT / '_upload_assets'
JOURNAL = HERE / 'private_assets_item.json'
URLS = HERE / 'desc_asset_urls.json'
TITLE = 'Darkest Refined — description assets (private)'
INLINE = ['intro_1_healing.png', 'intro_2_armor.png', 'intro_3_builds.png',
          'spotlights/antiquarian.png', 'spotlights/abomination.png']


def _nonce_info():
    """[2026-11-05] 같은 이미지를 같은 자리에 다시 올리면 스팀 등록만 남고 파일이 사라져 404가 났다(DLC 단독판 시안).
    업로드 PNG마다 실행별 nonce 텍스트를 넣어 바이트를 바꾼다."""
    import os, time
    from PIL.PngImagePlugin import PngInfo
    global _NONCE
    try:
        _NONCE
    except NameError:
        _NONCE = f'{time.time_ns()}-{os.getpid()}'
    info = PngInfo()
    info.add_text('upload', _NONCE)
    return info


def fit_png(im, out):
    width = im.width
    while True:
        g = im if width == im.width else im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        g.save(out, optimize=True, pnginfo=_nonce_info())
        if out.stat().st_size < 990_000:
            return
        width = int(width * 0.93)


def prepare():
    if UP.exists():
        shutil.rmtree(UP)
    UP.mkdir()
    files = []
    for f in sorted((DRAFT / 'desc').glob('*.png')) + [DRAFT / p for p in INLINE]:
        out = UP / ('d_' + ('spotlight_' if f.parent.name == 'spotlights' else '') + f.name)
        fit_png(Image.open(f).convert('RGB'), out)
        files.append(out)
    Image.open(DRAFT / 'desc' / 'title_banner.png').convert('RGB').save(UP / 'thumb.jpg', 'JPEG', quality=90)
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
            owned = {p['filename'] for p in steam.query()['previews'] if p['type'] == 0}
            r = steam.update(title=TITLE, description='Image storage for the Darkest Refined description. Not a mod.',
                             visibility=2, thumbnail=UP / 'thumb.jpg', replace_previews=(owned, files), language='english')
            urls = {p['filename'][2:]: p['url'] for p in r['previews'] if p['filename'].startswith('d_')}
            state.update(status='uploaded', previews=len(r['previews']))
            write_json(JOURNAL, state)
    URLS.write_text(json.dumps(urls, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(state, ensure_ascii=False), len(urls), 'urls')


if __name__ == '__main__':
    main()
