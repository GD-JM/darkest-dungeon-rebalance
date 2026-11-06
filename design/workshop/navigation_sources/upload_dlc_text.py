"""영웅 단독판 설명란(10개 언어). 설명 = 간판 이미지 → 본문('@@sheet_x.png' 줄 자리에 시트) → 맨 밑 다른 영웅 링크.
언어별 원고: desc_<영웅>_ko.txt(한국어), desc_<영웅>_<언어>.txt(english, brazilian, french, german, polish, russian, schinese, spanish, tchinese).
이미지: 한국어 설명 = 한국어 이미지(<영웅>_ko_*), 나머지 언어 = 영어 이미지(<영웅>_en_*). 갤러리 = 표지만.
[사용자 2026-11-03] "실제 게시하는 느낌으로 설명 란에 전부 작성해줘" / [2026-11-04] 맨 밑 다른 영웅 링크
[사용자 2026-11-06] "원래 다 번역하고 그 나라 언어권 사람이 누르면 그 언어로 뜨게 만들고 공개했어야 했는데" → 10개 언어.
출시한 영웅(RELEASED)은 공개 유지(visibility 0), 아직 아니면 비공개(2). [2026-11-06] 예전 판은 늘 비공개로 되돌렸다.
사용: <codex python> -B upload_dlc_text.py musketeer flagellant ...
"""
import importlib, json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
WS = Path('C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync')
sys.path.insert(0, str(WS))
from common import read_json, WorkerLock
from steam import Steam
from upload_dlc_pages import png, GAME, HP, PROTECT

STATE = HERE / 'dlc_pages_items.json'
PAGE = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'
LANGS = ['english', 'koreana', 'brazilian', 'french', 'german', 'polish', 'russian', 'schinese', 'spanish', 'tchinese']
FILE = {'koreana': 'ko'}   # 원고 파일 접미사(나머지는 언어 이름 그대로)
NAMES = json.loads((HERE / 'hero_names_official.json').read_text(encoding='utf-8'))   # 게임 공식 영웅 이름(언어별)
# 출시 순서 = 번호 [사용자 2026-11-04]. 출시한 영웅만 링크, 나머지는 '준비 중'(링크 없음).
RELEASED = ['musketeer', 'flagellant', 'shieldbreaker', 'runaway', 'duelist']
NEXT = ['antiquarian']   # 번호가 정해진 다음 순서
OTHERS = ['abomination', 'arbalest', 'bounty_hunter', 'crusader', 'grave_robber', 'hellion', 'highwayman', 'houndmaster',
          'jester', 'leper', 'man_at_arms', 'occultist', 'plague_doctor', 'vestal']
UI = {   # (다른 영웅 보기, 지금 보는 페이지, 준비 중, 제목 앞부분)
    'koreana': ('다른 영웅 보기', '(지금 보는 페이지)', '준비 중:', '다키스트 리파인드'),
    'english': ('Other heroes', '(this page)', 'Coming soon:', 'Darkest Refined'),
    'brazilian': ('Outros heróis', '(esta página)', 'Em breve:', 'Darkest Refined'),
    'french': ('Autres héros', '(cette page)', 'Bientôt :', 'Darkest Refined'),
    'german': ('Weitere Helden', '(diese Seite)', 'Demnächst:', 'Darkest Refined'),
    'polish': ('Inni bohaterowie', '(ta strona)', 'Wkrótce:', 'Darkest Refined'),
    'russian': ('Другие герои', '(эта страница)', 'Скоро:', 'Darkest Refined'),
    'schinese': ('其他英雄', '（当前页面）', '即将推出：', 'Darkest Refined'),
    'spanish': ('Otros héroes', '(esta página)', 'Próximamente:', 'Darkest Refined'),
    'tchinese': ('其他英雄', '（目前頁面）', '即將推出：', 'Darkest Refined'),
}


def name(h, lang):
    return NAMES[lang][h]


def title(h, lang):
    no = RELEASED.index(h) + 1 if h in RELEASED else len(RELEASED) + NEXT.index(h) + 1
    t = f'{UI[lang][3]} No.{no:02d} — {name(h, lang)}'
    return t if h in RELEASED else t + (' (시안)' if lang == 'koreana' else ' (draft)')


def _alive(url):
    """설명란 이미지가 실제로 열리는지(404 아님) 확인. [2026-11-05] 같은 이미지 재업로드 404 사고 뒤 추가."""
    import urllib.request
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'Range': 'bytes=0-15'}), timeout=30) as r:
            return r.status in (200, 206)
    except Exception:
        return False


def nav(h, state, lang='koreana'):
    head, here, soon, _ = UI[lang]
    sep = '、' if lang in ('schinese', 'tchinese') else ', '
    rows = []
    for i, k in enumerate(RELEASED, 1):
        label = f'No.{i:02d} {name(k, lang)}'
        rows.append(f'[*][b]{label}[/b] {here}' if k == h else f"[*][url={PAGE.format(state[k]['item_id'])}]{label}[/url]")
    nxt = [f'[b]No.{len(RELEASED) + j:02d} {name(k, lang)}[/b] {here}' if k == h else f'No.{len(RELEASED) + j:02d} {name(k, lang)}'
           for j, k in enumerate(NEXT, 1)]
    return (f'[h1]{head}[/h1]\n[list]\n' + '\n'.join(rows) + '\n[/list]\n'
            + f'{soon} ' + sep.join(nxt + [name(k, lang) for k in OTHERS]))


def place(body, C, h, urls, il='ko'):
    """'@@sheet_x.png' 줄을 그 시트 이미지로 바꾼다. 시트는 모두 정확히 한 번씩 들어가야 한다."""
    files = [sh['file'] for sh in C['sheets']] + [pl['file'] for pl in C.get('plays', [])]
    seen = re.findall(r'^@@(\S+)\s*$', body, re.M)
    assert sorted(seen) == sorted(files), (h, il, '시트 자리 불일치', set(files) ^ set(seen), seen)
    return re.sub(r'^@@(\S+)\s*$', lambda m: f"[img]{urls[f'{h}_{il}_{Path(m.group(1)).stem}.png']}[/img]", body, flags=re.M)


from refined_navigation import banner as navigation_banner


def build(h, state, urls, lang='koreana'):
    il = 'ko' if lang == 'koreana' else 'en'
    body = (HERE / f'desc_{h}_{FILE.get(lang, lang)}.txt').read_text(encoding='utf-8').replace('\r\n', '\n').strip()
    C = importlib.import_module('content_' + h + ('' if il == 'ko' else '_en')).C
    desc = navigation_banner(lang) + f"[img]{urls[f'{h}_{il}_title.png']}[/img]\n" + place(body, C, h, urls, il) + '\n\n' + nav(h, state, lang) + '\n'
    n = len(desc.encode('utf-8')) + desc.count('\n')
    assert n < 7990, (h, lang, n)
    return desc, n


def main(heroes):
    state = read_json(STATE, {})
    out = {}
    with WorkerLock(WS / 'runtime' / 'worker.lock'):
        for h in heroes:
            item, assets = int(state[h]['item_id']), int(state[h + '_assets']['item_id'])
            assert item not in PROTECT and assets not in PROTECT
            with Steam(GAME, assets) as st:
                urls = {p['filename']: p['url'] for p in st.query()['previews']}
            descs = {lang: build(h, state, urls, lang) for lang in LANGS}
            up = HERE / '_dlc_text' / h
            if up.exists():
                shutil.rmtree(up)
            up.mkdir(parents=True)
            for lang, (d, _) in descs.items():
                (up / f'desc_{lang}.txt').write_text(d, encoding='utf-8')
            cover = png(HP / h / 'cover.png', up / f'{h}_cover.png')
            vis = 0 if h in RELEASED else 2
            with Steam(GAME, item) as st:
                owned = {p['filename'] for p in st.query()['previews'] if p['type'] == 0}
                st.update(title=title(h, 'english'), description=descs['english'][0], language='english', visibility=vis,
                          thumbnail=cover, replace_previews=(owned, [cover]))
                for lang in LANGS[1:]:
                    st.update(title=title(h, lang), description=descs[lang][0], language=lang)
                check = {lang: st.query(lang) for lang in LANGS}
            imgs = set()
            for d, _ in descs.values():
                imgs |= set(re.findall(r'\[img\](.*?)\[/img\]', d))
            broken = [u for u in imgs if not _alive(u)]
            out[h] = {'url': PAGE.format(item), 'visibility': vis, 'broken_images': len(broken),
                      'langs': {lang: {'title': q.get('title'), 'bytes': descs[lang][1], 'img': q.get('description', '').count('[img]')}
                                for lang, q in check.items()}}
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1:])
