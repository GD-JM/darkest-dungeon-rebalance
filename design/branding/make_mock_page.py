# Darkest Refined 시안을 창작마당 페이지처럼 보는 로컬 HTML 목업(업로드 없음)
# 사용: python design/branding/make_mock_page.py [영웅 카드 이미지 폴더]
import base64, glob, html, io, os, re, shutil, sys
from PIL import Image

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'darkest_refined_draft')
CARDS_SRC = sys.argv[1] if len(sys.argv) > 1 else None


def bbcode(text):
    t = html.escape(text.strip())
    t = re.sub(r'\[url=([^\]]+)\](.*?)\[/url\]', r'<a href="\1">\2</a>', t)
    for tag, rep in (('h1', 'div class="bb_h1"'), ('h2', 'div class="bb_h2"'), ('b', 'b'), ('i', 'i')):
        t = t.replace(f'[{tag}]', f'<{rep}>').replace(f'[/{tag}]', f'</{rep.split()[0]}>')
    t = t.replace('[list]', '<ul>').replace('[/list]', '</ul>')
    t = re.sub(r'\[\*\](.*)', r'<li>\1</li>', t)
    t = re.sub(r'\n{2,}', '<br><br>', t).replace('\n', '<br>')
    return re.sub(r'(<br>)+(<(?:ul|/ul|li|div class="bb_h2"))', r'\2', re.sub(r'(</ul>|</li>|</div>)(<br>)+', r'\1', t))


def data_uri(rel):
    """목업 하나로 열리도록 이미지를 JPEG data URI로 넣는다(원본 PNG는 그대로 둔다)."""
    im = Image.open(os.path.join(D, rel)).convert('RGB')
    im.thumbnail((1000, 1000), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=80, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def main():
    os.makedirs(os.path.join(D, 'cards'), exist_ok=True)
    if CARDS_SRC:
        for f in glob.glob(os.path.join(CARDS_SRC, '*.png')):
            shutil.copy(f, os.path.join(D, 'cards', os.path.basename(f)))
    gallery = ['preview_darkest_refined.png'] + sorted(os.path.basename(f) for f in glob.glob(os.path.join(D, 'intro_*.png')))
    gallery += ['cards/' + os.path.basename(f) for f in sorted(glob.glob(os.path.join(D, 'cards', '*.png')))]
    en = bbcode(open(os.path.join(D, 'description_en.txt'), encoding='utf-8').read())
    ko = bbcode(open(os.path.join(D, 'description_ko.txt'), encoding='utf-8').read())
    gallery = [data_uri(g) for g in gallery]
    thumbs = ''.join(f'<img class="thumb{" on" if i == 0 else ""}" src="{g}" data-i="{i}">' for i, g in enumerate(gallery))
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Darkest Refined mockup</title><style>
:root{{--bg:#1b2838;--panel:#16202d;--text:#acb2b8;--title:#fff;--accent:#66c0f4;--gold:#d6b470}}
body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.6 "Segoe UI",Arial,sans-serif}}
.wrap{{max-width:1000px;margin:0 auto;padding:16px}}
.note{{background:#3a2a10;color:#f0d9a8;border:1px solid #6b4f20;padding:8px 12px;border-radius:3px;margin-bottom:14px;font-size:13px}}
.crumbs{{color:#8f98a0;font-size:12px}} h1.t{{color:var(--title);font-weight:300;font-size:26px;margin:4px 0 14px}}
.top{{display:flex;gap:16px;flex-wrap:wrap}} .viewer{{flex:1 1 620px;min-width:0;background:#000}}
.viewer .main{{width:100%;display:block;max-height:560px;object-fit:contain;background:#000}}
.strip{{display:flex;gap:6px;overflow-x:auto;padding:8px;background:#0e141b}}
.thumb{{height:62px;cursor:pointer;opacity:.6;border:2px solid transparent}} .thumb.on{{opacity:1;border-color:var(--accent)}}
.side{{flex:0 0 300px;background:var(--panel);padding:12px;box-sizing:border-box}} .side img{{width:100%;display:block}}
.btn{{display:block;margin-top:12px;background:linear-gradient(90deg,#75b022,#588a1b);color:#d2efa9;text-align:center;padding:8px;border-radius:2px}}
.stats{{margin-top:12px;font-size:12px;color:#8f98a0}} .tabs{{margin:18px 0 0;display:flex;gap:4px}}
.tabs button{{background:#2a3f5a;color:#c7d5e0;border:0;padding:6px 14px;cursor:pointer}} .tabs button.on{{background:#4b6a8f;color:#fff}}
.desc{{background:var(--panel);padding:16px 18px;margin-top:0}} .desc a{{color:var(--accent)}}
.bb_h1{{font-size:22px;color:#fff;margin:0 0 6px}} .bb_h2{{font-size:17px;color:var(--accent);margin:18px 0 6px;font-weight:600}}
ul{{margin:4px 0 4px 18px;padding:0}} li{{margin:4px 0}}
</style></head><body><div class="wrap">
<div class="note">로컬 시안 미리보기입니다. 창작마당에 올라가지 않았습니다. 대표 이미지·소개 이미지 4장·소개글은 새 시안이고, 영웅 비교 이미지는 현재 배포본(2.5.8) 그대로입니다.</div>
<div class="crumbs">Darkest Dungeon &gt; Workshop &gt; Items</div>
<h1 class="t">Darkest Refined — Hero Rebalance &amp; Reworks</h1>
<div class="top"><div class="viewer"><img class="main" id="main" src="{gallery[0]}"><div class="strip">{thumbs}</div></div>
<div class="side"><img src="{gallery[0]}" alt=""><span class="btn">+ Subscribe</span>
<div class="stats">File size · Posted · Updated — 시안이라 비어 있음</div></div></div>
<div class="tabs"><button class="on" data-l="en">English</button><button data-l="ko">한국어</button></div>
<div class="desc" id="en">{en}</div><div class="desc" id="ko" style="display:none">{ko}</div>
</div><script>
const g={gallery!r};
document.querySelectorAll('.thumb').forEach(t=>t.onclick=()=>{{document.getElementById('main').src=g[t.dataset.i];
document.querySelectorAll('.thumb').forEach(x=>x.classList.toggle('on',x===t));}});
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{['en','ko'].forEach(l=>document.getElementById(l).style.display=l===b.dataset.l?'':'none');
document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));}});
</script></body></html>'''
    open(os.path.join(D, 'mock_workshop_page.html'), 'w', encoding='utf-8').write(page)
    for lang in ('en', 'ko'):
        t = open(os.path.join(D, f'description_{lang}.txt'), encoding='utf-8').read().strip()
        print(lang, len(t.encode('utf-8')) + t.count('\n'), 'bytes incl. CRLF (Steam limit 8000)')
    print('mock:', os.path.join(D, 'mock_workshop_page.html'))


if __name__ == '__main__':
    main()
