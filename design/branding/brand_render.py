# Darkest Refined 브랜드 이미지 엔진 — 규칙은 BRAND_STYLE.md, 아트는 brand_art.json, 문구는 brand_content.json
# [사용자 2026-10-29: "레이아웃의 폰트라든지 배치라든지 아트스타일이라든지 이런거를 고정해서 원칙으로 md로 박아두고 … 똑같은 아트 스타일로 이미지 뽑고 수정"]
# 사용: python design/branding/brand_render.py            → brand_content.json 전부
#       python design/branding/brand_render.py intro_1    → out 이름에 'intro_1'이 들어간 것만
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
    title(im, (70, 92), c['title'], 62, anchor='lm', max_width=right_limit - 40)
    rule(d, 70, right_limit, 140, diamond=False)
    y = 172
    fl = font('palai', 28)
    for line in wrap(d, c['lead'], fl, right_limit - 30):
        d.text((70, y), line, font=fl, fill=IVORY)
        y += 38
    y += 18
    fh, fb = font('palab', 26), font('pala', 23)
    for name, text in c['items']:
        d.polygon([(76, y + 15), (84, y + 7), (92, y + 15), (84, y + 23)], fill=GOLD)
        d.text((104, y), name, font=fh, fill=GOLD_HI)
        y += 34
        for line in wrap(d, text, fb, right_limit - 80):
            d.text((104, y), line, font=fb, fill=BODY)
            y += 30
        y += 14
    d.text((70, H - 42), 'DARKEST REFINED  ·  Hero Rebalance & Reworks', font=font('pala', 20), fill=DIM, anchor='lm')
    credit(d, (W - 36, H - 22))
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


def hero_spotlight(c):
    """1200×800. 세로 아트(포스터)는 왼쪽 큰 칸, 가로 아트(코믹스 넓은 칸)는 위 띠 + 아래 두 단."""
    if aspect(c['art']) > 1.0:
        return hero_spotlight_wide(c)
    W, H = 1200, 800
    im = canvas(W, H, (-W * 0.2, H * 0.05, W * 0.55, H * 1.2))
    cell(im, c['art'], (40, 40, 520, H - 40))
    d = ImageDraw.Draw(im)
    x0, xr = 572, W - 56
    title(im, (x0, 88), c['hero'], 64, anchor='lm', max_width=xr - x0)
    rule(d, x0, xr, 134, diamond=False)
    y = 156
    for line in wrap(d, c['tagline'], font('palai', 28), xr - x0):
        d.text((x0, y), line, font=font('palai', 28), fill=IVORY)
        y += 38
    y += 16
    fl, fb = font('palab', 19), font('pala', 23)
    for label, text in c['rows']:
        d.text((x0, y), spaced(label), font=fl, fill=GOLD)
        y += 30
        for line in wrap(d, text, fb, xr - x0):
            d.text((x0, y), line, font=fb, fill=BODY)
            y += 30
        y += 16
    d.text((x0, H - 42), 'DARKEST REFINED  ·  Hero Rebalance & Reworks', font=font('pala', 20), fill=DIM, anchor='lm')
    credit(d, (W - 36, H - 22))
    frame(im, 10, inner=False)
    return grain(im, 7)


def hero_spotlight_wide(c):
    W, H = 1200, 800
    im = canvas(W, H, (W * 0.1, H * 0.55, W * 0.9, H * 1.4))
    # 넓은 칸은 원본 크기 근처(최대 1.25배)로만 키워 왼쪽 위에 두고, 오른쪽에 이름·한 줄
    src, _ = art_source(c['art'])
    bh = 300
    aw = min(W - 80 - 380, int(bh * aspect(c['art'])), int(src.width * 1.25))
    bh = min(bh, int(aw / aspect(c['art'])))
    cell(im, c['art'], (40, 40, 40 + aw, 40 + bh))
    d = ImageDraw.Draw(im)
    x0 = 40 + aw + 44
    title(im, (x0, 40 + bh // 2 - 40), c['hero'], 60, anchor='lm', max_width=W - 60 - x0)
    y = 40 + bh // 2 + 6
    for line in wrap(d, c['tagline'], font('palai', 28), W - 60 - x0):
        d.text((x0, y), line, font=font('palai', 28), fill=IVORY)
        y += 36
    ry = 40 + bh + 34
    rule(d, 70, W - 70, ry, diamond=False)
    fl, fb = font('palab', 18), font('pala', 22)
    colw, xs = (W - 140 - 40) // 2, (70, 70 + (W - 140 - 40) // 2 + 40)
    for i, (label, text) in enumerate(c['rows']):
        x = xs[i % 2]
        y = ry + 26 + (i // 2) * 160
        d.text((x, y), spaced(label), font=fl, fill=GOLD)
        y += 28
        for line in wrap(d, text, fb, colw):
            d.text((x, y), line, font=fb, fill=BODY)
            y += 28
    d.text((70, H - 30), 'DARKEST REFINED  ·  Hero Rebalance & Reworks', font=font('pala', 20), fill=DIM, anchor='lm')
    credit(d, (W - 36, H - 30))
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
    title(im, (66, 62), c['title'], 58, anchor='lm', max_width=620)
    frame(im, 4, inner=False)
    d.rectangle((12, 12, W - 13, H - 13), outline=FRAME_IN, width=1)
    return grain(im, 6)


def title_banner(c):
    """1100×340: 설명 맨 위 간판. 그림 위에 DARKEST / REFINED와 대표 문구."""
    W, H = 1100, 340
    im = Image.new('RGB', (W, H), INK)
    im.paste(fit(c['art'], 700, H), (W - 700, 0))
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
    title(im, (W // 2, H // 2 + 2), c['title'], 30, max_width=W - 76)
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
    W, per, size, gap = 1100, 9, 104, 14
    names = c['heroes']
    rows = (len(names) + per - 1) // per
    H = 30 + rows * (size + 40) + 10
    im = canvas(W, H, (W * 0.1, -H * 0.3, W * 0.9, H * 1.3))
    d = ImageDraw.Draw(im)
    fn = font('pala', 16)
    for i, (hero, label) in enumerate(names):
        r, k = divmod(i, per)
        n_row = min(per, len(names) - r * per)
        x0 = (W - (n_row * size + (n_row - 1) * gap)) // 2 + k * (size + gap)
        y0 = 26 + r * (size + 40)
        im.paste(face(hero, size), (x0, y0))
        d.rectangle((x0 - 1, y0 - 1, x0 + size, y0 + size), outline=(8, 6, 5), width=3)
        d.rectangle((x0 + 2, y0 + 2, x0 + size - 3, y0 + size - 3), outline=CELL_LINE, width=1)
        d.text((x0 + size // 2, y0 + size + 16), label, font=fn, fill=BODY, anchor='mm')
    frame(im, 4, inner=False)
    return grain(im, 5)


LAYOUTS = {f.__name__: f for f in (square_comic_grid, square_keyart, square_triptych, panel_comic, panel_poster,
                                   hero_spotlight, banner, update, quote, section_header, title_banner, button,
                                   roster_strip)}


def main(only=None):
    renders = json.load(open(os.path.join(HERE, 'brand_content.json'), encoding='utf-8'))['renders']
    for c in renders:
        if only and only not in c['out']:
            continue
        out = os.path.join(OUT, c['out'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        LAYOUTS[c['layout']](c).save(out, optimize=True)
        print('saved', c['out'], c['layout'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
