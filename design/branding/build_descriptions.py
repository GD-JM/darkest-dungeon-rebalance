"""설명란 꾸밈 빌더 (BRAND_STYLE.md §5-B)
원문(darkest_refined_draft/description_*.txt, i18n/)을 받아 [h1]은 간판 이미지로, [h2]는 섹션 머리 이미지로 바꾸고
섹션 안에 소개·스포트라이트·초상 줄·버튼을 넣어 darkest_refined_draft/final/에 쓴다.
사용: python design/branding/build_descriptions.py           # Steam 주소(desc_asset_urls.json) 사용
      python design/branding/build_descriptions.py --local   # 로컬 파일 경로(목업 확인용)
각 언어 원문의 [h2] 순서는 고정: 조정 원칙 → 해볼 것 → 두 개편 → 이미지 → 피드백 → 설치.
8000바이트(줄바꿈 CRLF 2바이트) 안에 들지 않으면 선택 이미지를 소개 → 스포트라이트 → 초상 줄 순서로 뺀다.
"""
import json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT = HERE / 'darkest_refined_draft'
OUT = DRAFT / 'final'
LANGS = ['english', 'koreana', 'brazilian', 'french', 'german', 'polish', 'russian', 'schinese', 'spanish', 'tchinese']
HEADERS = ['h_tuned', 'h_try', 'h_reworks', 'h_images', 'h_listening', 'h_install']
ITEM = 3828956017   # [2026-11-05] 통합본 자기 업데이트 기록·댓글로 연결(예전엔 기존판 3821353035로 걸려 있었음)
CHANGELOG = f'https://steamcommunity.com/sharedfiles/filedetails/changelog/{ITEM}'
COMMENTS = f'https://steamcommunity.com/sharedfiles/filedetails/comments/{ITEM}'
BUDGET = 7990   # [2026-11-06] 7,971바이트(줄바꿈 2바이트 계산) 업로드 성공을 확인하고 7900→7990. 한도는 8000.


def source(lang):
    # Darkest Refined 출시 원본(design/refined/description/<언어>.txt)이 있으면 그것, 없으면 시안 원본
    rel = HERE.parent / 'refined' / 'description' / f'{lang}.txt'
    if rel.exists():
        return rel.read_text(encoding='utf-8').strip()
    return (DRAFT / ('description_en.txt' if lang == 'english' else 'description_ko.txt' if lang == 'koreana'
                     else f'i18n/description_{lang}.txt')).read_text(encoding='utf-8').strip()


def size(text):
    return len(text.encode('utf-8')) + text.count('\n')


FOCUS = ['antiquarian', 'musketeer']   # [사용자 2026-11-06] 설명란 스포트라이트는 두 개편만, 20명 전원은 갤러리에


def asset_lang(lang):
    """한국어 설명은 한국어 이미지, 나머지 언어는 영어 이미지. [사용자 2026-11-05] "온전한 한국어판 온전한 영어판" """
    return 'ko' if lang == 'koreana' else 'en'


def build(text, img, optional, lang='english'):
    """[2026-11-06] 설명란 '모든 변경은 이미지에'에는 두 개편(FOCUS) 스포트라이트만 언어별로 넣고, 20명 전원은 갤러리에 둔다.
    롤스터는 뺐다. optional = {'intros'}만."""
    tag = lambda name: f'[img]{img(name)}[/img]'
    text = re.sub(r'\[h1\].*?\[/h1\]\n?', tag('title_banner') + '\n', text, count=1)
    if lang in ('english', 'koreana'):  # 대표 문구는 그 언어 간판 이미지에 이미 있다
        text = re.sub(r'(\[/img\]\n)\[i\][^\n]*\[/i\]\n', r'\1', text, count=1)
    parts = re.split(r'\[h2\].*?\[/h2\]\n?', text)
    assert len(parts) == len(HEADERS) + 1, f'expected {len(HEADERS)} [h2] sections, got {len(parts) - 1}'
    out = [parts[0].rstrip('\n') + '\n\n']
    for key, body in zip(HEADERS, parts[1:]):
        body = body.strip('\n')
        if key == 'h_try' and 'intros' in optional:
            body += '\n' + '\n'.join(tag(n) for n in ('intro_1_healing', 'intro_2_armor', 'intro_3_builds'))
        if key == 'h_images':
            body += '\n' + '\n'.join(tag(f'spot_{h}') for h in FOCUS)
        if key == 'h_listening':
            body = re.sub(r'\[url=[^\]]*changelog[^\]]*\].*?\[/url\]', '', body).rstrip()
            body += (f'\n[url={CHANGELOG}]{tag("btn_history")}[/url] [url={COMMENTS}]{tag("btn_feedback")}[/url]')
        if key == 'h_install':
            lines = body.split('\n')
            k = max(i for i, l in enumerate(lines) if l.startswith('[i]'))
            body = '\n'.join(lines[:k]).rstrip('\n') + '\n\n' + tag('h_credits') + '\n' + '\n'.join(lines[k:])
        out.append(tag(key) + '\n' + body + '\n\n')
    return ''.join(out).strip() + '\n'


def asset_key(name):
    """설명 [img] 이름 → 이미지 파일 상대 경로(언어 폴더 기준)."""
    if name.startswith('spot_'):
        return 'spotlights/' + name[5:] + '.png'
    if name.startswith('intro_'):
        return name + '.png'
    return 'desc/' + name + '.png'


def main(local=False):
    if local:
        def img_for(lang):
            base = 'ko/' if asset_lang(lang) == 'ko' else ''
            return lambda n: base + asset_key(n)
    else:
        urls = json.loads((HERE / 'desc_asset_urls.json').read_text(encoding='utf-8'))
        img_for = lambda lang: (lambda n: urls[asset_lang(lang)][asset_key(n)])
    OUT.mkdir(exist_ok=True)
    report = {}
    for lang in LANGS:
        text = source(lang)
        optional = ['intros']
        while True:
            final = build(text, img_for(lang), set(optional), lang)
            if size(final) < BUDGET or not optional:
                break
            optional.pop(0)
        assert size(final) < 8000, (lang, size(final))
        (OUT / f'description_{lang}.txt').write_text(final, encoding='utf-8')
        report[lang] = (size(final), optional)
    for k, v in report.items():
        print(k, v)


if __name__ == '__main__':
    main('--local' in sys.argv)
