"""Darkest Refined 게시 — 새 창작마당 아이템(합본)을 만들고 내용·페이지를 올린다. 기존 3821353035과 workshop-sync는 건드리지 않는다.

[사용자 2026-11-02] "응 합본 먼저로 확정하고 출시 준비 진행해" / "기존거를 수정하는 식으로 작업하지 말고 새로 만들어서 너가 따로 작업해서 업로드하고"
흐름: 아이템 확보(처음 한 번만 생성, 비공개) → main 스냅샷 빌드(build_refined) → 비교 카드(workshop-sync cards.render_cards 불러 쓰기)
      → 갤러리(소개 4 + 영웅마다 스포트라이트 → 카드, 설명에 이미 쓴 이미지는 제외) → 10개 언어 제목·꾸민 설명 → 소유자 조회로 확인.
공개 전환은 --public을 줄 때만(사용자가 비공개로 확인·승인한 뒤).
상태·작업 폴더: %USERPROFILE%/Documents/DarkestRefined/runtime (저장소 밖). 아이템 번호 등록표: design/refined/items.json.
사용: <codex python> -B tools/refined/publish_refined.py [--ref main] [--public]
"""
import argparse, json, os, re, shutil, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
GAME = REPO.parent.parent
WS = Path('C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync')
RUNTIME = Path(os.path.expanduser('~')) / 'Documents' / 'DarkestRefined' / 'runtime'
ITEMS = REPO / 'design' / 'refined' / 'items.json'
BRAND = REPO / 'design' / 'branding'
DRAFT = BRAND / 'darkest_refined_draft'
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
OLD_ITEM = 3821353035

sys.path.insert(0, str(WS))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BRAND))
from common import read_json, write_json, WorkerLock      # noqa: E402  (workshop-sync: 불러 쓰기만)
from steam import Steam, SteamError                        # noqa: E402
import build_refined                                       # noqa: E402


def fit_png(src, dst):
    """Steam 미리보기: 1MB 미만 PNG. 그대로 → 256색 → 폭 축소."""
    from PIL import Image
    im = Image.open(src).convert('RGB')
    im.save(dst, optimize=True)
    if dst.stat().st_size < 990_000:
        return dst
    im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(dst, optimize=True)
    w = im.width
    while dst.stat().st_size >= 990_000:
        w = int(w * 0.93)
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).quantize(256, method=Image.Quantize.MEDIANCUT).save(dst, optimize=True)
    return dst


def ensure_item(state):
    items = read_json(ITEMS, {})
    if items.get('refined'):
        return int(items['refined'])
    if state.get('create') == 'creating':
        raise SteamError('Earlier creation outcome unknown; check owned items before any retry')
    with Steam(str(GAME)) as root:
        if not root.query()['owned']:
            raise SteamError('Logged-in Steam user does not own the Rebalance item')
        def before():
            state['create'] = 'creating'
            write_json(RUNTIME / 'state.json', state)
        made = root.create_item(before)
    state['create'] = 'created'
    write_json(RUNTIME / 'state.json', state)
    items['refined'] = int(made['item_id'])
    ITEMS.write_text(json.dumps(items, indent=1) + '\n', encoding='utf-8')
    return items['refined']


def descriptions():
    """10개 언어 꾸민 설명(design/branding/build_descriptions.py, Steam 이미지 주소)."""
    import build_descriptions as BD
    BD.main(local=False)
    out = {}
    for lang in LANGS:
        t = (DRAFT / 'final' / f'description_{lang}.txt').read_text(encoding='utf-8')
        assert 'images.steamusercontent.com' in t and len(t.encode('utf-8')) + t.count('\n') < 8000, lang
        out[lang] = t
    return out


def gallery(cards, job, used_urls):
    """소개 4 → 영웅마다 스포트라이트 → 비교 카드. 모든 언어 설명에 이미 [img]로 들어간 이미지는 뺀다."""
    urls = json.loads((BRAND / 'desc_asset_urls.json').read_text(encoding='utf-8'))
    in_desc = {n for n, u in urls.items() if u in used_urls}
    up = job / 'gallery'
    up.mkdir()
    files = []
    if 'intro_4_refined.png' not in in_desc:
        files.append(fit_png(DRAFT / 'intro_4_refined.png', up / 'intro_4_refined.png'))
    shown = set()
    for c in cards:
        h = c['hero']
        spot = DRAFT / 'spotlights' / f'{h}.png'
        if h not in shown and spot.exists() and f'spotlight_{h}.png' not in in_desc:
            files.append(fit_png(spot, up / f'spot_{h}.png'))
        shown.add(h)
        files.append(fit_png(job / 'cards' / c['path'], up / ('card_' + c['path'])))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='main')
    ap.add_argument('--public', action='store_true')
    a = ap.parse_args()
    RUNTIME.mkdir(parents=True, exist_ok=True)
    state = read_json(RUNTIME / 'state.json', {})
    with WorkerLock(WS / 'runtime' / 'worker.lock'):
        item = ensure_item(state)
        assert item != OLD_ITEM
        job = Path(tempfile.mkdtemp(prefix='refined_', dir=RUNTIME))
        src = job / 'source'
        src.mkdir()
        sha = build_refined.snapshot(a.ref, str(src))
        summary = build_refined.build(str(src), str(job / 'payload'), item, 'refined')
        import cards as WSC
        card_data = json.loads((src / 'design' / 'workshop' / 'hero_cards.json').read_text(encoding='utf-8'))
        manifest = WSC.render_cards(card_data, GAME, job / 'cards', 1500, mod_root=src)
        descs = descriptions()
        used = set(re.findall(r'\[img\](.*?)\[/img\]', '\n'.join(descs.values())))
        files = gallery(manifest, job, used)
        thumb = fit_png(DRAFT / 'final_pages' / 'cover_all.png', job / 'thumb.png')
        note = json.load(open(REPO / 'design' / 'refined' / 'packages.json', encoding='utf-8'))['refined']['note']
        with Steam(str(GAME), item) as st:
            owned = {p['filename'] for p in st.query()['previews'] if p['type'] == 0}
            st.update(title=TITLES['english'], description=descs['english'], language='english', content=job / 'payload',
                      thumbnail=thumb, replace_previews=(owned, files), visibility=0 if a.public else 2, note=note)
            for lang in LANGS[1:]:
                st.update(title=TITLES[lang], description=descs[lang], language=lang)
            check = {lang: st.query(lang) for lang in ('english', 'koreana')}
        result = {'item': item, 'sha': sha, 'heroes': len(summary['heroes']), 'effects': summary['effects'], 'buffs': summary['buffs'],
                  'gallery': len(files), 'url': f'https://steamcommunity.com/sharedfiles/filedetails/?id={item}',
                  'visibility': 'public' if a.public else 'private',
                  'check': {k: {'title': v.get('title'), 'previews': len(v['previews']), 'img': v.get('description', '').count('[img]')}
                            for k, v in check.items()}}
        state.update(last=result)
        write_json(RUNTIME / 'state.json', state)
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
