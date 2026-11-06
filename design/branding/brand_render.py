# Darkest Refined 브랜드 이미지 엔진 — 규칙은 BRAND_STYLE.md, 아트는 brand_art.json, 문구는 brand_content.json
# [사용자 2026-10-29: "레이아웃의 폰트라든지 배치라든지 아트스타일이라든지 이런거를 고정해서 원칙으로 md로 박아두고 … 똑같은 아트 스타일로 이미지 뽑고 수정"]
# 사용: python design/branding/brand_render.py            → brand_content.json 전부
#       python design/branding/brand_render.py intro_1    → out 이름에 'intro_1'이 들어간 것만
#       python design/branding/brand_render.py --lang ko [이름]  → 한국어판: brand_content_ko.json → darkest_refined_draft/ko/
#       python design/branding/brand_render.py --groups [--lang ko]  → 스포트라이트 4명 묶음 5장 → darkest_refined_draft/spotlight_groups/<lang>/
# [2026-11-05 한국어판 추가] 한국어 설명에는 한국어 이미지만, 영어 설명에는 영어 이미지만("온전한 한국어판, 온전한 영어판").
#   글자 그리기만 언어별로 갈린다(heading·text·lines·label·tag). 영어 경로는 예전 호출 그대로라 영어 출력은 픽셀 단위로 같다.
#   한국어 글꼴 = 게임 한국어판 비트맵 글꼴(제목 EBS주시경, 본문 이순신 돋움) — page_tools/gamefont.py를 가져다 쓴다.
import json, os, random, re, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))      # DarkestDungeon 설치 폴더 (게임 글꼴)
SRC = os.path.join(HERE, 'source_art')
OUT = os.path.join(HERE, 'darkest_refined_draft')
WINFONT = 'C:/Windows/Fonts/'

# ── 색 (BRAND_STYLE.md §2) ─────────────────────────────────────────────
INK = (10, 9, 8)            # 바탕
EMBER = (66, 15, 11)        # 붉은 잔광
GOLD = (206, 168, 98)       # 제목 그라데이션 아래, 규칙선, 글머리
GOLD_HI = (240, 214, 150)   # 제목 그라데이션 위, 항목 이름
IVORY = (226, 214, 190)     # 부제·리드
BODY = (206, 196, 176)      # 본문
DIM = (150, 138, 120)       # 꼬리말
CREDIT_C = (118, 108, 94)   # 저작권 표기
FRAME = (92, 72, 44)        # 바깥 금테
FRAME_IN = (48, 38, 26)     # 안쪽 가는 테
CELL_LINE = (214, 196, 160) # 만화 칸 안쪽 상아 선
CREDIT = 'Art © Red Hook Studios'


def font(name, size):
    """palab=Palatino Linotype Bold, pala=Regular, palai=Italic (BRAND_STYLE.md §3)."""
    return ImageFont.truetype(WINFONT + name + '.ttf', size)


# ── 제목 글꼴: 게임 비트맵 글꼴 DwarvenAxe ───────────────────────────────
class BMFont:
    def __init__(self, name):
        txt = open(os.path.join(G, 'fonts', name + '.fnt'), encoding='utf-8').read()
        self.line = int(re.search(r'lineHeight=(\d+)', txt).group(1))
        page = re.search(r'page id=0 file="([^"]+)"', txt).group(1)
        self.page = Image.open(os.path.join(G, 'fonts', page)).getchannel('A')
        self.chars, self.kern = {}, {}
        for m in re.finditer(r'^char (.*)$', txt, re.M):
            d = dict(kv.split('=') for kv in m.group(1).split())
            self.chars[int(d['id'])] = {k: int(v) for k, v in d.items() if k != 'chnl'}
        for m in re.finditer(r'^kerning first=(\d+)\s+second=(\d+)\s+amount=(-?\d+)', txt, re.M):
            self.kern[(int(m.group(1)), int(m.group(2)))] = int(m.group(3))

    def mask(self, text, height, tracking=0.0):
        w, prev = 0, None
        for ch in text:
            c = self.chars[ord(ch)]
            w += c['xadvance'] + self.kern.get((prev, ord(ch)), 0) + tracking
            prev = ord(ch)
        m = Image.new('L', (int(w + 20), self.line + 30), 0)
        x, prev = 10, None
        for ch in text:
            c = self.chars[ord(ch)]
            x += self.kern.get((prev, ord(ch)), 0)
            g = self.page.crop((c['x'], c['y'], c['x'] + c['width'], c['y'] + c['height']))
            box = (int(x + c['xoffset']), c['yoffset'])
            m.paste(ImageChops.lighter(m.crop(box + (box[0] + c['width'], box[1] + c['height'])), g), box)
            x += c['xadvance'] + tracking
            prev = ord(ch)
        m = m.crop(m.getbbox())
        s = height / self.line
        big = m.resize((max(1, int(m.width * s)), max(1, int(m.height * s))), Image.LANCZOS)
        return big.point(lambda v: 0 if v < 70 else 255 if v > 170 else int((v - 70) * 2.55))


_AXE = None


def title(im, xy, text, height, anchor='mm', tracking=2.0, max_width=None):
    """금색 그라데이션 + 검은 외곽 + 그림자. anchor: l/m/r × t/m."""
    global _AXE
    _AXE = _AXE or BMFont('dwarvenaxe-xl')
    m = _AXE.mask(text, height, tracking)
    if max_width and m.width > max_width:
        m = _AXE.mask(text, int(height * max_width / m.width), tracking)
    x, y = xy
    x -= {'l': 0, 'm': m.width // 2, 'r': m.width}[anchor[0]]
    y -= {'t': 0, 'm': m.height // 2}[anchor[1]]
    grad = Image.new('RGB', m.size)
    gd = ImageDraw.Draw(grad)
    for yy in range(m.height):
        t = yy / max(1, m.height - 1)
        gd.line((0, yy, m.width, yy), fill=tuple(int(GOLD_HI[i] * (1 - t) + GOLD[i] * t * 0.85) for i in range(3)))
    sh = Image.new('L', (m.width + 40, m.height + 40), 0)
    sh.paste(m, (20, 20))
    sh = sh.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.8))
    im.paste(Image.new('RGB', sh.size, (0, 0, 0)), (x - 16, y - 14), sh)
    im.paste(Image.new('RGB', m.size, (20, 12, 6)), (x, y), m.filter(ImageFilter.MaxFilter(5)))
    im.paste(grad, (x, y), m)
    return (x, y, x + m.width, y + m.height)


# ── 공통 효과 ──────────────────────────────────────────────────────────
def canvas(w, h, glow_box):
    im = Image.new('RGB', (w, h), INK)
    if glow_box:
        g = Image.new('L', (w, h), 0)
        ImageDraw.Draw(g).ellipse(glow_box, fill=110)
        im = Image.composite(Image.new('RGB', (w, h), EMBER), im, g.filter(ImageFilter.GaussianBlur(min(w, h) // 7)))
    return im


def grain(im, amount=6):
    random.seed(7)
    n = Image.effect_noise(im.size, 40).point(lambda v: 128 + (v - 128) * amount // 40)
    return ImageChops.overlay(im, Image.merge('RGB', (n, n, n)))


def frame(im, inset=12, inner=True):
    d = ImageDraw.Draw(im)
    w, h = im.size
    d.rectangle((inset, inset, w - 1 - inset, h - 1 - inset), outline=FRAME, width=3)
    if inner:
        d.rectangle((inset + 10, inset + 10, w - 11 - inset, h - 11 - inset), outline=FRAME_IN, width=1)


def rule(d, x0, x1, y, diamond=True):
    d.line((x0, y, x1, y), fill=GOLD, width=2)
    if diamond:
        c = (x0 + x1) // 2
        d.polygon([(c, y - 7), (c + 7, y), (c, y + 7), (c - 7, y)], fill=INK, outline=GOLD)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def spaced(text):
    return '   '.join(' '.join(word) for word in text.split(' '))


# ── 언어별 글자 그리기 (한국어판) ──────────────────────────────────────
# 영어(LANG 'en')는 예전 코드와 같은 호출을 그대로 한다. 한국어는 게임 한국어 글꼴 체인(gamefont.py)으로 그린다.
LANG = 'en'
PAGE_TOOLS = 'C:/Users/lemm1/Documents/DarkestRefined/page_tools'      # gamefont.py 위치(복사하지 않고 가져다 쓴다)
STR = {'footer': 'DARKEST REFINED  ·  Hero Rebalance & Reworks'}     # 언어별 고정 문구(문구 파일 "strings"로 덮어쓴다)
# 한국어 글자 크기 = 영어 크기 × 비율. 제목(EBS주시경)은 DwarvenAxe보다 획이 가늘어 같은 px로 높이를 맞추고,
# 라벨은 영어의 띄어 쓴 대문자만큼 눈에 띄게 키운다. 줄 간격은 한글이 빽빽해 영어 줄 간격 × KO_LH.
KO_SCALE = {'title': 1.0, 'pala': 1.0, 'palai': 0.96, 'palab': 1.0, 'label': 1.22}
KO_LH = 1.08
GF = KO = None          # gamefont 모듈, (제목, 본문, 굵은 본문) 체인
NOBREAK = []            # 줄을 나누지 않는 공식 이름(영웅·기술, 띄어쓰기 포함) — set_lang('ko')에서 loc.json으로 채운다
NOBREAK_EXTRA = ['가장 어두운 던전', '영웅 등급', '전용 장신구', '이동 저항', '죽음의 일격']


def set_lang(lang, strings=None):
    """'en' 또는 'ko'. 한국어는 gamefont를 불러 게임 한국어 글꼴 체인을 쓴다."""
    global LANG, GF, KO
    LANG = lang
    STR.update(strings or {})
    if lang == 'ko' and KO is None:
        if PAGE_TOOLS not in sys.path:
            sys.path.insert(0, PAGE_TOOLS)
        import gamefont
        GF = gamefont

        class Head(gamefont.Chain):
            """제목 체인: 한글 제목 글꼴에 없는 쉼표·숫자·라틴은 DwarvenAxe에서 오는데, 기준선이 한글보다 높아
            쉼표가 따옴표처럼 뜬다(‘다듬고, 계속’). 그 글자만 0.28px 내려 한글 높이 가운데에 맞춘다."""
            def glyph(self, ch, px):
                g = super().glyph(ch, px)
                if g and self.find(ch)[0] == 1:
                    return (g[0], g[1], g[2] + px * 0.28, g[3])
                return g

        class Body(gamefont.Chain):
            """본문 체인: ubuntu의 물결표는 옆 여백이 거의 없어 '−30~−40%'가 '~~'처럼 붙는다 → 양옆에 0.06px씩 띄운다."""
            def glyph(self, ch, px):
                g = super().glyph(ch, px)
                if g and ch == '~':
                    return (g[0], g[1] + px * 0.06, g[2], g[3] + px * 0.12)
                return g

        gamefont.set_lang('ko')
        gamefont.HEAD = Head(['korean_dwarven_axe_l', 'dwarvenaxe-l', 'korean_ubuntu_m'], [1.0, 1.12, 0.95])  # fonts()와 같은 구성
        gamefont.BODY = Body(['korean_ubuntu', 'ubuntu'], [1.0, 0.98])
        gamefont.BODYB = Body(['korean_ubuntu_m', 'ubuntu_m'], [1.0, 0.98])
        KO = gamefont.fonts()               # gold()가 쓰는 전역 제목 글꼴도 이 체인
        # 영웅 20명의 공식 한국어 직업·기술 이름 중 띄어쓰기가 있는 것(제압 사격, 결집 신호탄 …)은 한 덩어리로 줄바꿈
        loc = json.load(open(os.path.join(PAGE_TOOLS, 'loc.json'), encoding='utf-8'))
        ko = dict(loc['vanilla']['koreana'], **loc['mod']['koreana'])
        heroes = [k[len('hero_class_name_'):] for k in ko if k.startswith('hero_class_name_')]
        names = {v for k, v in ko.items() for h in heroes
                 if k == 'hero_class_name_' + h or k.startswith(('combat_skill_name_' + h + '_', 'combat_move_skill_name_' + h))}
        NOBREAK[:] = sorted({n for n in names | set(NOBREAK_EXTRA) if ' ' in n}, key=len, reverse=True)


def kpx(face, size):
    return max(8, round(size * KO_SCALE[face]))


def lh(n):
    """줄 간격: 영어는 그대로, 한국어는 KO_LH배."""
    return n if LANG != 'ko' else round(n * KO_LH)


def chain(face):
    return KO[2] if face in ('palab', 'label') else KO[1]


def heading(im, xy, text, height, anchor='mm', tracking=2.0, max_width=None):
    """금색 제목. 영어 = title()(DwarvenAxe). 한국어 = gamefont.gold()(EBS주시경), 위치는 글자 실제 상자 기준으로 title()과 같게 맞춘다."""
    if LANG != 'ko':
        return title(im, xy, text, height, anchor, tracking, max_width)
    H = KO[0]
    px = kpx('title', height)
    if max_width and H.width(text, px, 1) > max_width:
        px = int(px * max_width / H.width(text, px, 1))
    bb = H.mask(GF.norm(text), px, 1).getbbox()
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    x, y = xy
    x -= {'l': 0, 'm': w // 2, 'r': w}[anchor[0]]
    y -= {'t': 0, 'a': 0, 'm': h // 2}[anchor[1]]
    # gold(anchor 'la')는 마스크 왼쪽 위를 (x - 0.1px, y - 0.22px)에 둔다 → 글자 상자 왼쪽 위가 (x, y)에 오게 되돌린다
    GF.gold(im, (x - bb[0] + px * 0.1 + 0.5, y - bb[1] + px * 0.22 + 0.5), text, px, anchor='la', tracking=1)
    return (x, y, x + w, y + h)


def text(im, d, xy, s, face, size, fill, anchor=None):
    """한 줄 글. 영어 = d.text(Palatino). 한국어 = gamefont.draw(이순신 돋움), 기울임은 한글에 없어 바른 글꼴."""
    if LANG != 'ko':
        d.text(xy, s, font=font(face, size), fill=fill, anchor=anchor)
        return
    a = anchor or 'la'
    GF.draw(im, xy, s, chain(face), kpx(face, size), fill, anchor=a[0] + {'t': 'a', 's': 'a'}.get(a[1], a[1]))


def lines(d, s, face, size, width):
    """줄바꿈. 영어 = wrap()(단어). 한국어 = 어절(띄어쓰기) 단위, 문구 속 '\\n'은 강제 줄바꿈."""
    if LANG != 'ko':
        return wrap(d, s, font(face, size), width)
    ch, px, nb = chain(face), kpx(face, size), ' '
    out = []
    for para in s.split('\n'):
        for n in NOBREAK:                       # 공식 이름 속 띄어쓰기는 줄을 나누지 않는 칸으로
            para = para.replace(n, n.replace(' ', nb))
        para = re.sub(r' (?=[+\-−–]\d)', nb, para)   # '피해 −40%'처럼 능력치와 부호 붙은 수치는 붙여 둔다
        cur = ''
        for word in para.split(' '):
            t = (cur + ' ' + word).strip(' ')
            if not cur or ch.width(t.replace(nb, ' '), px) <= width:
                cur = t
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    out = [o.replace(nb, ' ') for o in out]
    # 한 어절이 칸보다 길면 gamefont.wrap으로 글자 단위로 자른다(드묾)
    return [p for o in out for p in (GF.wrap(o, ch, px, width) if ch.width(o, px) > width else [o])]


def label(im, d, xy, s, size, fill):
    """작은 금색 라벨(THE PROBLEM 등). 영어 = 글자 사이를 띄운 Palatino Bold. 한국어 = 굵은 본문 글꼴, 자간만 조금."""
    if LANG != 'ko':
        d.text(xy, spaced(s), font=font('palab', size), fill=fill)
        return
    GF.draw(im, xy, s, chain('label'), kpx('label', size), fill, tracking=1)


def tag(im, d, x, y, s, size=15):
    """꼬리표(REWORKED 등). 한국어는 같은 상자에 굵은 한글. 오른쪽 끝 x를 돌려준다."""
    if LANG != 'ko':
        return badge(d, x, y, s, size)
    px = kpx('label', size)
    w, h = int(KO[2].width(s, px, 1)) + 22, size + 13
    d.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=EMBER, outline=GOLD, width=2)
    GF.draw(im, (x + w // 2, y + h // 2 + 1), s, KO[2], px, GOLD_HI, anchor='mm', tracking=1)
    return x + w


def badge(d, x, y, text, size=15):
    """잔광색 작은 꼬리표(REWORKED·NEW SKILL). 왼쪽 위 (x, y)에 그리고 오른쪽 끝 x를 돌려준다."""
    f = font('palab', size)
    t = spaced(text)
    w, h = int(d.textlength(t, font=f)) + 22, size + 13
    d.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=EMBER, outline=GOLD, width=2)
    d.text((x + w // 2, y + h // 2 + 1), t, font=f, fill=GOLD_HI, anchor='mm')
    return x + w


# ── 아트 ───────────────────────────────────────────────────────────────
ART = {k: v for k, v in json.load(open(os.path.join(HERE, 'brand_art.json'), encoding='utf-8')).items() if not k.startswith('_')}


def art_source(key):
    a = ART[key]
    if a['type'] == 'comic':
        page = Image.open(os.path.join(SRC, f"comic_{a['hero']}.png")).convert('RGB')
        k = page.width / 560
        return page.crop(tuple(int(v * k) for v in a['grid560'])), a['focus']
    im = Image.open(os.path.join(SRC, a['src'])).convert('RGB')
    return (im.crop(tuple(a['box'])) if a.get('box') else im), a['focus']


def fit(key, w, h):
    """비율이 다르면 focus를 중심으로 잘라 칸을 채운다(cover)."""
    src, (fx, fy) = art_source(key)
    sw, sh = src.size
    if sw / sh > w / h:
        cw = int(sh * w / h)
        cx = max(0, min(sw - cw, int(sw * fx - cw / 2)))
        src = src.crop((cx, 0, cx + cw, sh))
    else:
        ch = int(sw * h / w)
        cy = max(0, min(sh - ch, int(sh * fy - ch / 2)))
        src = src.crop((0, cy, sw, cy + ch))
    return src.resize((w, h), Image.LANCZOS)


def aspect(key):
    src, _ = art_source(key)
    return src.width / src.height


def cell(im, key, box):
    """만화 칸: 3px 검은 홈 + 1px 상아 안선 (BRAND_STYLE.md §4)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    im.paste(fit(key, x1 - x0, y1 - y0), (x0, y0))
    d = ImageDraw.Draw(im)
    d.rectangle((x0 - 1, y0 - 1, x1, y1), outline=(8, 6, 5), width=3)
    d.rectangle((x0 + 2, y0 + 2, x1 - 3, y1 - 3), outline=CELL_LINE, width=1)


def column(im, keys, x0, x1, y0, y1, gap=14):
    """세로 열에 칸을 원래 비율대로 쌓고, 넘치면 폭을 줄여 가운데 정렬."""
    asp = [aspect(k) for k in keys]
    w = x1 - x0
    hs = [w / a for a in asp]
    if sum(hs) + gap * (len(hs) - 1) > y1 - y0:
        w = (y1 - y0 - gap * (len(hs) - 1)) / sum(1 / a for a in asp)
        hs = [w / a for a in asp]
    total = sum(hs) + gap * (len(hs) - 1)
    x, y = x0 + ((x1 - x0) - w) / 2, y0 + ((y1 - y0) - total) / 2
    for k, h in zip(keys, hs):
        cell(im, k, (x, y, x + w, y + h))
        y += h + gap


def dark_left(im, solid, fade):
    """왼쪽 글 영역을 바탕색으로 덮고 오른쪽으로 부드럽게 푼다."""
    w, h = im.size
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    for x in range(solid + fade):
        d.line((x, 0, x, h), fill=245 if x < solid else int(245 * (1 - (x - solid) / fade) ** 1.5))
    return Image.composite(Image.new('RGB', (w, h), INK), im, m)


def dark_top(im, until):
    w, h = im.size
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    for y in range(until):
        d.line((0, y, w, y), fill=int(250 * (1 - y / until) ** 1.4))
    return Image.composite(Image.new('RGB', (w, h), INK), im, m)


def credit(d, xy, anchor='rm', size=15):
    d.text(xy, CREDIT, font=font('palai', size), fill=CREDIT_C, anchor=anchor)


# ── 템플릿 (BRAND_STYLE.md §5) ──────────────────────────────────────────
def square_head(im, c):
    S = im.width
    d = ImageDraw.Draw(im)
    title(im, (S // 2, 104), c['title'][0], 92, tracking=3)
    title(im, (S // 2, 254), c['title'][1], 128, tracking=3)
    rule(d, 250, S - 250, 352)
    d.text((S // 2, 394), c['tagline'], font=font('palai', 40), fill=IVORY, anchor='mm')
    return d


def square_foot(im, c, y=None):
    S = im.width
    d = ImageDraw.Draw(im)
    d.text((S // 2, y or S - 30), spaced(c['footer']), font=font('pala', 20), fill=GOLD, anchor='mm')
    frame(im, 14)


def square_comic_grid(c):
    """1024²: 제목 + 넓은 칸 1 + 세로 칸 3."""
    S = 1024
    im = canvas(S, S, (S * 0.15, -S * 0.25, S * 0.85, S * 0.45))
    a = c['art']
    cell(im, a[0], (42, 436, 982, 664))
    w3 = (940 - 28) // 3
    for i, k in enumerate(a[1:4]):
        x = 42 + i * (w3 + 14)
        cell(im, k, (x, 678, x + w3, 968))
    d = square_head(im, c)
    credit(d, (S - 34, 414), size=14)
    square_foot(im, c)
    return grain(im)


def square_keyart(c):
    """1024²: 키아트 한 장을 꽉 채우고, 영화 포스터처럼 제목을 아래에 둔다(위쪽 얼굴을 가리지 않게)."""
    S = 1024
    im = fit(c['art'], S, S)
    g = Image.new('L', (S, S), 0)
    gd = ImageDraw.Draw(g)
    for y in range(480, S):
        gd.line((0, y, S, y), fill=int(250 * min(1, (y - 480) / 300) ** 1.2))
    im = Image.composite(Image.new('RGB', (S, S), INK), im, g)
    d = ImageDraw.Draw(im)
    title(im, (S // 2, 672), c['title'][0], 84, tracking=3)
    title(im, (S // 2, 800), c['title'][1], 116, tracking=3)
    rule(d, 260, S - 260, 888)
    d.text((S // 2, 926), c['tagline'], font=font('palai', 36), fill=IVORY, anchor='mm')
    credit(d, (S - 34, 40), anchor='rm', size=14)
    square_foot(im, c, y=S - 40)
    return grain(im)


def square_triptych(c):
    """1024²: 제목 + 세로 칸 3 (포스터·키아트)."""
    S = 1024
    im = canvas(S, S, (S * 0.15, -S * 0.25, S * 0.85, S * 0.45))
    w3 = (940 - 28) // 3
    for i, k in enumerate(c['art'][:3]):
        x = 42 + i * (w3 + 14)
        cell(im, k, (x, 436, x + w3, 968))
    d = square_head(im, c)
    credit(d, (S - 34, 414), size=14)
    square_foot(im, c)
    return grain(im)


def panel_text(im, c, right_limit=640):
    """1200×800 왼쪽 글 영역: 제목·규칙선·리드·항목 4개·꼬리말."""
    W, H = im.size
    d = ImageDraw.Draw(im)
    heading(im, (70, 92), c['title'], 62, anchor='lm', max_width=right_limit - 40)
    rule(d, 70, right_limit, 140, diamond=False)
    y = 172
    for line in lines(d, c['lead'], 'palai', 28, right_limit - 30):
        text(im, d, (70, y), line, 'palai', 28, IVORY)
        y += lh(38)
    y += 18
    for name, body, *tg in c['items']:
        d.polygon([(76, y + 15), (84, y + 7), (92, y + 15), (84, y + 23)], fill=GOLD)
        text(im, d, (104, y), name, 'palab', 26, GOLD_HI)
        if tg:      # 세 번째 칸 = 꼬리표(예: REWORKED)
            nw = d.textlength(name, font=font('palab', 26)) if LANG != 'ko' else KO[2].width(name, kpx('palab', 26))
            tag(im, d, 104 + int(nw) + 14, y + 2, tg[0], size=13)
        y += lh(34)
        for line in lines(d, body, 'pala', 23, right_limit - 80):
            text(im, d, (104, y), line, 'pala', 23, BODY)
            y += lh(30)
        y += 14
    text(im, d, (70, H - 42), STR['footer'], 'pala', 20, DIM, anchor='lm')
    credit(d, (W - 36, H - 22))
    fits(c, y - 14, H - 66)
    return d


def panel_comic(c):
    """1200×800: 왼쪽 글 + 오른쪽 만화 칸 2~3개 세로 쌓기."""
    W, H = 1200, 800
    im = canvas(W, H, (W * 0.45, H * 0.05, W * 1.25, H * 1.2))
    column(im, c['art'], 712, W - 36, 40, H - 40)
    im = dark_left(im, 560, 200)
    panel_text(im, c)
    frame(im, 10, inner=False)
    return grain(im, 7)


def panel_poster(c):
    """1200×800: 왼쪽 글 + 오른쪽 포스터 한 장(전체 높이 칸)."""
    W, H = 1200, 800
    im = canvas(W, H, (W * 0.45, H * 0.05, W * 1.25, H * 1.2))
    a = aspect(c['art'])
    h = H - 80
    w = min(int(h * a), W - 36 - 700)
    x = W - 36 - w
    cell(im, c['art'], (x, 40, x + w, 40 + h))
    im = dark_left(im, 560, 120)
    panel_text(im, c)
    frame(im, 10, inner=False)
    return grain(im, 7)


def hero_spotlight(c, part=False):
    """1200×800. 고해상도 세로 아트(포스터)만 왼쪽 큰 칸. 코믹스 칸(가로든 세로든 작음)은 원본 크기 근처로
    왼쪽 위에 두는 위 띠 + 아래 두 단 — 작은 칸을 키우면 뭉개진다.
    part=True: 묶음용 블록(꼬리말·테·그레인 없이) → (그림, 내용 아래 끝 y)."""
    if aspect(c['art']) > 1.0 or art_source(c['art'])[0].height < 600:
        return hero_spotlight_wide(c, part)
    W, H = 1200, 800
    im = canvas(W, H, (-W * 0.2, H * 0.05, W * 0.55, H * 1.2)) if not part else Image.new("RGB", (W, H), INK)
    cell(im, c['art'], (40, 40, 520, H - 40))
    d = ImageDraw.Draw(im)
    x0, xr = 572, W - 56
    if c.get('badge'):
        tag(im, d, x0, 22, c['badge'])
    heading(im, (x0, 88), c['hero'], 64, anchor='lm', max_width=xr - x0)
    rule(d, x0, xr, 134, diamond=False)
    y = 156
    for line in lines(d, c['tagline'], 'palai', 28, xr - x0):
        text(im, d, (x0, y), line, 'palai', 28, IVORY)
        y += lh(38)
    y += 16
    for lab, body in c['rows']:
        label(im, d, (x0, y), lab, 19, GOLD)
        y += lh(30)
        for line in lines(d, body, 'pala', 23, xr - x0):
            text(im, d, (x0, y), line, 'pala', 23, BODY)
            y += lh(30)
        y += 16
    if part:
        fits(c, y - 16, H - 40)
        return im, max(H - 40, y - 16)
    text(im, d, (x0, H - 42), STR['footer'], 'pala', 20, DIM, anchor='lm')
    credit(d, (W - 36, H - 22))
    fits(c, y - 16, H - 66)
    frame(im, 10, inner=False)
    return grain(im, 7)


def hero_spotlight_wide(c, part=False):
    W, H = 1200, 800
    im = canvas(W, H, (W * 0.1, H * 0.55, W * 0.9, H * 1.4)) if not part else Image.new("RGB", (W, H), INK)
    # 넓은 칸은 원본 크기 근처(최대 1.25배)로만 키워 왼쪽 위에 두고, 오른쪽에 이름·한 줄
    src, _ = art_source(c['art'])
    bh = 300
    aw = min(W - 80 - 380, int(bh * aspect(c['art'])), int(src.width * 1.25))
    bh = min(bh, int(aw / aspect(c['art'])))
    cell(im, c['art'], (40, 40, 40 + aw, 40 + bh))
    d = ImageDraw.Draw(im)
    x0 = 40 + aw + 44
    if c.get('badge'):      # 이름 위 꼬리표(리워크 영웅)
        tag(im, d, x0, 40 + bh // 2 - 112, c['badge'])
    heading(im, (x0, 40 + bh // 2 - 40), c['hero'], 60, anchor='lm', max_width=W - 60 - x0)
    y = 40 + bh // 2 + 6
    for line in lines(d, c['tagline'], 'palai', 28, W - 60 - x0):
        text(im, d, (x0, y), line, 'palai', 28, IVORY)
        y += lh(36)
    ry = 40 + bh + 34
    rule(d, 70, W - 70, ry, diamond=False)
    colw, xs = (W - 140 - 40) // 2, (70, 70 + (W - 140 - 40) // 2 + 40)
    top = ry + 26
    for r in range(0, len(c['rows']), 2):      # 두 칸씩 한 줄, 다음 줄은 긴 쪽 아래에서 시작
        bottom = top
        for x, (lab, body) in zip(xs, c['rows'][r:r + 2]):
            y = top
            label(im, d, (x, y), lab, 18, GOLD)
            y += lh(28)
            for line in lines(d, body, 'pala', 22, colw):
                text(im, d, (x, y), line, 'pala', 22, BODY)
                y += lh(28)
            bottom = max(bottom, y)
        top = bottom + 26
    if part:
        fits(c, top - 26, H - 40)
        return im, max(40 + bh, top - 26)
    text(im, d, (70, H - 30), STR['footer'], 'pala', 20, DIM, anchor='lm')
    credit(d, (W - 36, H - 30))
    fits(c, top - 26, H - 54)
    frame(im, 10, inner=False)
    return grain(im, 7)


def banner(c):
    """1200×400: 넓은 칸 한 장 꽉 채움 + 왼쪽 큰 제목·부제."""
    W, H = 1200, 400
    im = Image.new('RGB', (W, H), INK)
    im.paste(fit(c['art'], 820, H), (W - 820, 0))
    im = dark_left(im, 470, 240)
    d = ImageDraw.Draw(im)
    title(im, (64, 168), c['title'], 96, anchor='lm', max_width=500)
    rule(d, 64, 600, 236, diamond=False)
    d.text((64, 272), c['subtitle'], font=font('palai', 30), fill=IVORY, anchor='lm')
    credit(d, (W - 30, H - 24))
    frame(im, 10, inner=False)
    return grain(im, 7)


def update(c):
    """1200×800: 위 띠(넓은 칸, 280) + 제목·부제 + 변경 목록."""
    W, H = 1200, 800
    im = canvas(W, H, (W * 0.1, H * 0.6, W * 0.9, H * 1.4))
    cell(im, c['art'], (40, 40, W - 40, 300))
    d = ImageDraw.Draw(im)
    title(im, (W // 2, 374), c['title'], 72, anchor='mm', max_width=W - 200)
    rule(d, 300, W - 300, 424)
    d.text((W // 2, 460), c['subtitle'], font=font('palai', 27), fill=IVORY, anchor='mm')
    y, fb = 506, font('pala', 24)
    for item in c['items']:
        d.polygon([(96, y + 15), (104, y + 7), (112, y + 15), (104, y + 23)], fill=GOLD)
        for i, line in enumerate(wrap(d, item, fb, W - 220)):
            d.text((126, y), line, font=fb, fill=BODY)
            y += 32
        y += 10
    d.text((70, H - 30), 'DARKEST REFINED  ·  Hero Rebalance & Reworks', font=font('pala', 20), fill=DIM, anchor='lm')
    credit(d, (W - 36, H - 30))
    frame(im, 10, inner=False)
    return grain(im, 7)


def quote(c):
    """1200×600: 원화 배경을 어둡게 + 가운데 인용 한 줄."""
    W, H = 1200, 600
    im = fit(c['art'], W, H)
    im = Image.blend(Image.new('RGB', (W, H), INK), im, 0.45)
    d = ImageDraw.Draw(im)
    fq = font('palai', 46)
    lines = wrap(d, '“' + c['quote'] + '”', fq, W - 160)
    y = H // 2 - (len(lines) * 64) // 2 - 20
    for line in lines:
        d.text((W // 2 + 3, y + 3), line, font=fq, fill=(0, 0, 0), anchor='mt')
        d.text((W // 2, y), line, font=fq, fill=IVORY, anchor='mt')
        y += 64
    rule(d, W // 2 - 160, W // 2 + 160, y + 26)
    d.text((W // 2, y + 64), spaced(c['attribution']), font=font('pala', 22), fill=GOLD, anchor='mm')
    credit(d, (W - 30, H - 24))
    frame(im, 10, inner=False)
    return grain(im, 7)


# ── 설명란 꾸밈 (BRAND_STYLE.md §5-B) ───────────────────────────────────
# 창작마당 설명은 가로 약 636px로 줄여 보이므로 2배 가까운 해상도(1100)로 만든다.
def section_header(c):
    """1100×120: 섹션 머리 띠. 왼쪽 금색 제목, 오른쪽에 섹션마다 다른 B컷이 어둠에서 떠오른다."""
    W, H = 1100, 120
    im = Image.new('RGB', (W, H), INK)
    im.paste(fit(c['art'], 560, H), (W - 560, 0))
    im = dark_left(im, 560, 300)
    d = ImageDraw.Draw(im)
    d.polygon([(30, 60), (40, 50), (50, 60), (40, 70)], fill=GOLD)
    heading(im, (66, 62), c['title'], 58, anchor='lm', max_width=620)
    frame(im, 4, inner=False)
    d.rectangle((12, 12, W - 13, H - 13), outline=FRAME_IN, width=1)
    return grain(im, 6)


def title_banner(c):
    """1100×340: 설명 맨 위 간판. 그림 위에 DARKEST / REFINED와 대표 문구."""
    W, H = 1100, 340
    im = Image.new('RGB', (W, H), INK)
    im.paste(fit(c['art'], 700, H), (W - 700, 0))
    if LANG == 'ko':    # 영문 로고는 브랜드라 그대로 두고 조금 줄인 뒤, 아래에 한국어 이름과 두 줄 소개
        im = dark_left(im, 470, 300)
        d = ImageDraw.Draw(im)
        title(im, (60, 62), c['title'][0], 48, anchor='lm', tracking=3)
        r = title(im, (60, 128), c['title'][1], 72, anchor='lm', tracking=3)
        n = heading(im, (62, r[3] + 12), c['name'], 46, anchor='lt')
        rule(d, 60, 520, n[3] + 14, diamond=False)
        y = n[3] + 30
        for line in lines(d, c['tagline'], 'palai', 26, 600):
            text(im, d, (60, y), line, 'palai', 26, IVORY)
            y += 32
        fits(c, y - 8, H - 14)
    else:
        im = dark_left(im, 420, 300)
        d = ImageDraw.Draw(im)
        title(im, (60, 104), c['title'][0], 66, anchor='lm', tracking=3)
        title(im, (60, 196), c['title'][1], 96, anchor='lm', tracking=3)
        rule(d, 60, 470, 262, diamond=False)
        d.text((60, 296), c['tagline'], font=font('palai', 28), fill=IVORY, anchor='lm')
    credit(d, (W - 22, H - 18), size=13)
    frame(im, 6, inner=False)
    return grain(im, 6)


def button(c):
    """300×66: 링크 버튼(설명란 한 줄에 두 개). 어두운 바탕, 금테, 가운데 금색 글자, 양옆 마름모."""
    W, H = 300, 66
    im = canvas(W, H, (-W * 0.2, -H * 0.5, W * 1.2, H * 1.6))
    d = ImageDraw.Draw(im)
    heading(im, (W // 2, H // 2 + 2), c['title'], 30, max_width=W - 76)
    for x in (20, W - 20):
        d.polygon([(x, H // 2 - 7), (x + 7, H // 2), (x, H // 2 + 7), (x - 7, H // 2)], fill=GOLD)
    d.rectangle((2, 2, W - 3, H - 3), outline=FRAME, width=3)
    d.rectangle((8, 8, W - 9, H - 9), outline=FRAME_IN, width=1)
    return grain(im, 5)


FACE_X = {'crusader': 0.56, 'arbalest': 0.5, 'antiquarian': 0.42, 'abomination': 0.36, 'musketeer': 0.46, 'occultist': 0.46,
          'leper': 0.26, 'shieldbreaker': 0.42, 'jester': 0.72, 'highwayman': 0.47, 'vestal': 0.36, 'man_at_arms': 0.5,
          'plague_doctor': 0.44, 'hellion': 0.47, 'houndmaster': 0.42, 'grave_robber': 0.66, 'bounty_hunter': 0.6, 'flagellant': 0.5}


def face(hero, size):
    """게임 길드 헤더 원화(만화풍)에서 얼굴 쪽 정사각을 잘라 밝힌다."""
    import glob
    from PIL import ImageEnhance
    path = (glob.glob(os.path.join(G, 'heroes', hero, hero + '_guild_header.png')) +
            glob.glob(os.path.join(G, 'dlc', '**', 'heroes', hero, hero + '_guild_header.png'), recursive=True))[0]
    a = Image.open(path).convert('RGBA')
    a = Image.alpha_composite(Image.new('RGBA', a.size, INK + (255,)), a).convert('RGB')
    side = int(a.height * 0.5)
    cx = int(a.width * FACE_X.get(hero, 0.5))
    x0 = max(0, min(a.width - side, cx - side // 2))
    f = a.crop((x0, 0, x0 + side, side)).resize((size, size), Image.LANCZOS)
    return ImageEnhance.Brightness(ImageEnhance.Contrast(f).enhance(1.1)).enhance(1.9)


def roster_strip(c):
    """1100×H: 바뀐 영웅 초상 줄(9명씩). 칸 테두리는 만화 칸과 같은 규칙."""
    W, per, size, gap = 1100, c.get('per', 9), c.get('size', 104), c.get('gap', 14)   # 20명은 10명씩 두 줄
    names = c['heroes']
    rows = (len(names) + per - 1) // per
    H = 30 + rows * (size + 40) + 10
    im = canvas(W, H, (W * 0.1, -H * 0.3, W * 0.9, H * 1.3))
    d = ImageDraw.Draw(im)
    for i, (hero, name) in enumerate(names):
        r, k = divmod(i, per)
        n_row = min(per, len(names) - r * per)
        x0 = (W - (n_row * size + (n_row - 1) * gap)) // 2 + k * (size + gap)
        y0 = 26 + r * (size + 40)
        im.paste(face(hero, size), (x0, y0))
        d.rectangle((x0 - 1, y0 - 1, x0 + size, y0 + size), outline=(8, 6, 5), width=3)
        d.rectangle((x0 + 2, y0 + 2, x0 + size - 3, y0 + size - 3), outline=CELL_LINE, width=1)
        text(im, d, (x0 + size // 2, y0 + size + 16), name, 'pala', 16, BODY, anchor='mm')
    frame(im, 4, inner=False)
    return grain(im, 5)


LAYOUTS = {f.__name__: f for f in (square_comic_grid, square_keyart, square_triptych, panel_comic, panel_poster,
                                   hero_spotlight, banner, update, quote, section_header, title_banner, button,
                                   roster_strip)}


# 한국어판을 그릴 수 있는 레이아웃(설명란 간판·섹션 머리·버튼·초상 줄·소개 패널·스포트라이트). 나머지는 영어 전용.
KO_LAYOUTS = {'title_banner', 'section_header', 'button', 'roster_strip', 'panel_comic', 'panel_poster', 'hero_spotlight'}
OVERFLOW = []
KO_TAGS = {'REWORKED': '개편', 'NEW SKILL': '새 기술'}


def fits(c, bottom, limit):
    """글이 칸 아래(꼬리말 자리)를 넘으면 경고만 남긴다(그림은 그대로)."""
    if bottom > limit:
        OVERFLOW.append(c['out'])
        print(f"  !! 넘침 {c['out']}: 글 끝 {int(bottom)} > 한도 {limit}")


def intro_override(renders):
    """소개 패널 한국어 문구: page_tools/combined_intro_ko.json이 있으면 그 문구(title·lead·items)를 쓴다.
    받는 모양: {"renders":[{out,...}]} / [{out,...}] / {"intro_1_healing": {...}} (out 파일 이름 또는 intro_N 접두로 맞춘다)."""
    p = os.path.join(PAGE_TOOLS, 'combined_intro_ko.json')
    if not os.path.exists(p):
        return renders
    src = json.load(open(p, encoding='utf-8'))
    items = src.get('renders', src) if isinstance(src, dict) else src
    if isinstance(items, dict):
        items = [dict(v, out=k) for k, v in items.items() if not k.startswith('_') and isinstance(v, dict)]
    by = {}
    for it in items:
        k = os.path.splitext(os.path.basename(it.get('out', '')))[0]
        by[k] = it
        by['_'.join(k.split('_')[:2])] = it
    for c in renders:
        k = os.path.splitext(os.path.basename(c['out']))[0]
        it = by.get(k) or by.get('_'.join(k.split('_')[:2]))
        if it and c['layout'] in ('panel_comic', 'panel_poster'):
            c.update({f: it[f] for f in ('title', 'lead', 'items') if f in it})
            if 'sub' in it and 'lead' not in it:        # 그 파일은 리드 줄을 'sub'로 쓴다
                c['lead'] = it['sub']
            # 꼬리표: null = 없음, 영어 꼬리표 단어는 한국어판에 맞게 바꾼다
            c['items'] = [[n, b] + ([KO_TAGS.get(t[0], t[0])] if t and t[0] else []) for n, b, *t in c['items']]
            print('  intro text <-', os.path.basename(p), k)
    return renders


# ── 스포트라이트 묶음 (설명란용) ─────────────────────────────────────
# [2026-11-05 구성 확정] 스포트라이트는 갤러리에서 빼고 설명란 안에 언어별로 넣는다. 설명란 용량 때문에 영웅 4명씩
# 세로로 이어 붙인 묶음 5장(정보 손실 없이 영웅마다 4문단 그대로). 순서 = 영어 이름 알파벳순(초상 줄과 같음).
GROUP_ORDER = ['abomination', 'antiquarian', 'arbalest', 'bounty_hunter', 'crusader', 'duelist', 'flagellant', 'grave_robber',
               'hellion', 'highwayman', 'houndmaster', 'jester', 'leper', 'man_at_arms', 'musketeer', 'occultist',
               'plague_doctor', 'runaway', 'shieldbreaker', 'vestal']
GROUP_W, GROUP_MAX = 1100, 1_000_000      # 설명란 이미지 폭, 업로드 한도(1MB 미만, 여유 두고 10진 1MB)


def spotlight_group(cs):
    """스포트라이트 블록(꼬리말·테 없이 내용 높이로 자름)을 세로로 잇고, 사이에 금색 구분선, 맨 아래 꼬리말 한 번, 전체 테 하나.
    1200폭으로 그린 뒤 1100으로 줄이고 그레인은 마지막에 한 번."""
    blocks = []
    for c in cs:
        im, bottom = hero_spotlight(c, part=True)
        blocks.append(im.crop((0, 0, im.width, min(im.height, bottom + 40))))
    W, foot = 1200, 64
    H = sum(b.height for b in blocks) + foot
    im = Image.new('RGB', (W, H), INK)
    d = ImageDraw.Draw(im)
    y, cuts = 0, []
    for b in blocks:
        im.paste(b, (0, y))
        y += b.height
        cuts.append(y)
    for y in cuts[:-1]:         # 구분선은 블록을 다 붙인 뒤에(다음 블록에 덮이지 않게)
        rule(d, 70, W - 70, y, diamond=True)
    text(im, d, (70, H - 34), STR['footer'], 'pala', 20, DIM, anchor='lm')
    credit(d, (W - 36, H - 34))
    frame(im, 10, inner=False)
    im = im.resize((GROUP_W, round(H * GROUP_W / W)), Image.LANCZOS)
    return grain(im, 7)


def save_small(im, path):
    """1MB 미만 PNG: 그대로 저장해 보고 넘으면 256색으로 줄인다. 크기(바이트)를 돌려준다."""
    im.save(path, optimize=True)
    if os.path.getsize(path) >= GROUP_MAX:
        im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)
    return os.path.getsize(path)


def groups(renders, lang, per=4):
    """묶음 그리기. 한 장이라도 1MB 이상이면 한 장에 넣는 영웅 수를 하나 줄여 다시 그린다(4명 5장 → 3명 7장).
    그레인(BRAND_STYLE §4)이 용량 대부분이라 4명 묶음은 256색으로도 1MB 언저리다(2026-11-05 측정 영어 995~1074KB)."""
    import glob
    by = {os.path.splitext(os.path.basename(c['out']))[0]: c for c in renders if c['layout'] == 'hero_spotlight'}
    out_dir = os.path.join(OUT, 'spotlight_groups', lang)
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, 'group_*.png')):     # 예전 묶음(장 수가 달랐을 수 있음) 지우기
        os.remove(f)
    sizes = []
    for g in range(0, len(GROUP_ORDER), per):
        names = GROUP_ORDER[g:g + per]
        p = os.path.join(out_dir, f'group_{g // per + 1}.png')
        im = spotlight_group([by[n] for n in names])
        sizes.append(save_small(im, p))
        print(f"saved spotlight_groups/{lang}/group_{g // per + 1}.png {im.size} {sizes[-1] / 1024:.0f}KB", ', '.join(names))
    if max(sizes) >= GROUP_MAX and per > 1:
        print(f'!! 1MB 이상 묶음이 있어 {per}명 → {per - 1}명씩 다시 그린다')
        return groups(renders, lang, per - 1)
    return sizes


def main(only=None, lang='en', group=False, per=4):
    """lang 'en' = brand_content.json(예전과 같음), 'ko' = brand_content_ko.json(out은 ko/ 아래).
    group=True: 스포트라이트 묶음만 그린다(darkest_refined_draft/spotlight_groups/<lang>/group_N.png)."""
    name = 'brand_content.json' if lang == 'en' else f'brand_content_{lang}.json'
    data = json.load(open(os.path.join(HERE, name), encoding='utf-8'))
    set_lang(lang, data.get('strings'))
    renders = data['renders']
    if group:
        return groups(renders, lang, per)
    if lang == 'ko':
        renders = intro_override(renders)
    for c in renders:
        if only and only not in c['out']:
            continue
        if lang != 'en' and c['layout'] not in KO_LAYOUTS:
            raise SystemExit(f"{c['out']}: {c['layout']} 레이아웃은 아직 영어 전용")
        out = os.path.join(OUT, c['out'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        LAYOUTS[c['layout']](c).save(out, optimize=True)
        print('saved', c['out'], c['layout'])
    if OVERFLOW:
        print('넘침', len(OVERFLOW), '장:', ', '.join(OVERFLOW))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    lang = 'en'
    if '--lang' in args:
        i = args.index('--lang')
        lang = args[i + 1]
        del args[i:i + 2]
    group = '--groups' in args          # 스포트라이트 묶음: brand_render.py --groups [--lang ko] [--per 3]
    per = 4
    if '--per' in args:
        i = args.index('--per')
        per = int(args[i + 1])
        del args[i:i + 2]
    args = [a for a in args if a != '--groups']
    main(args[0] if args else None, lang, group, per)
