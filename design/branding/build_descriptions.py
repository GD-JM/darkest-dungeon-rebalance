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
BUDGET = 7900


def source(lang):
    # Darkest Refined 출시 원본(design/refined/description/<언어>.txt)이 있으면 그것, 없으면 시안 원본
    rel = HERE.parent / 'refined' / 'description' / f'{lang}.txt'
    if rel.exists():
        return rel.read_text(encoding='utf-8').strip()
    return (DRAFT / ('description_en.txt' if lang == 'english' else 'description_ko.txt' if lang == 'koreana'
                     else f'i18n/description_{lang}.txt')).read_text(encoding='utf-8').strip()


def size(text):
    return len(text.encode('utf-8')) + text.count('\n')


def build(text, img, optional, lang='english'):
    """optional: 넣을 선택 이미지 집합 {'intros', 'spotlights', 'roster'}."""
    tag = lambda name: f'[img]{img(name)}[/img]'
    text = re.sub(r'\[h1\].*?\[/h1\]\n?', tag('title_banner') + '\n', text, count=1)
    if lang == 'english':  # 영어 대표 문구는 간판 이미지에 이미 있다
        text = re.sub(r'(\[/img\]\n)\[i\][^\n]*\[/i\]\n', r'\1', text, count=1)
    parts = re.split(r'\[h2\].*?\[/h2\]\n?', text)
    assert len(parts) == len(HEADERS) + 1, f'expected {len(HEADERS)} [h2] sections, got {len(parts) - 1}'
    out = [parts[0].rstrip('\n') + '\n\n']
    for key, body in zip(HEADERS, parts[1:]):
        body = body.strip('\n')
        if key == 'h_try' and 'intros' in optional:
            body += '\n' + '\n'.join(tag(n) for n in ('intro_1_healing', 'intro_2_armor', 'intro_3_builds'))
        if key == 'h_reworks' and 'spotlights' in optional:
            body += '\n' + '\n'.join(tag(n) for n in ('spotlight_antiquarian', 'spotlight_abomination'))
        if key == 'h_images' and 'roster' in optional:
            body = tag('roster') + '\n' + body
        if key == 'h_listening':
            body = re.sub(r'\[url=[^\]]*changelog[^\]]*\].*?\[/url\]', '', body).rstrip()
            body += (f'\n[url={CHANGELOG}]{tag("btn_history")}[/url] [url={COMMENTS}]{tag("btn_feedback")}[/url]')
        if key == 'h_install':
            lines = body.split('\n')
            k = max(i for i, l in enumerate(lines) if l.startswith('[i]'))
            body = '\n'.join(lines[:k]).rstrip('\n') + '\n\n' + tag('h_credits') + '\n' + '\n'.join(lines[k:])
        out.append(tag(key) + '\n' + body + '\n\n')
    return ''.join(out).strip() + '\n'


def main(local=False):
    if local:
        # 목업(darkest_refined_draft/mock_workshop_page.html) 기준 상대 경로
        img2 = lambda n: (n.replace('spotlight_', 'spotlights/', 1) if n.startswith('spotlight_')
                          else n if n.startswith('intro_') else 'desc/' + n) + '.png'
    else:
        urls = json.loads((HERE / 'desc_asset_urls.json').read_text(encoding='utf-8'))
        img2 = lambda n: urls[n + '.png']
    OUT.mkdir(exist_ok=True)
    report = {}
    for lang in LANGS:
        text = source(lang)
        optional = ['intros', 'spotlights', 'roster']
        while True:
            final = build(text, img2, set(optional), lang)
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
