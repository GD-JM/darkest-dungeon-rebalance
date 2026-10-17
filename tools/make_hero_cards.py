# 영웅별 전/후 비교 이미지 (창작마당 추가 이미지): design/workshop/hero_cards.json → design/workshop/cards/heroes/NN_<hero>.png
# 톤은 make_cards.py·make_preview.py와 같다: 어두운 갈색, 청동 테두리, 금색 팔라티노, 게임 초상화·기술 아이콘
import os, json, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

G = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
M = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
W = os.path.join(M, 'design', 'workshop')
OUT = os.path.join(W, 'cards', 'heroes')
F = 'C:/Windows/Fonts/'
BG, PANEL, LINE = (18, 15, 13), (30, 25, 21), (88, 70, 48)
GOLD, TEXT, DIM, OLD, NEW = (214, 180, 112), (226, 218, 200), (150, 140, 124), (176, 92, 80), (132, 190, 120)
WID = 1200
FT = {k: ImageFont.truetype(F + v, s) for k, (v, s) in dict(
    hero=('palab.ttf', 56), tag=('palai.ttf', 28), col=('palab.ttf', 22), skill=('palab.ttf', 30),
    row=('pala.ttf', 25), foot=('palai.ttf', 20)).items()}


def hero_dir(h):
    for p in [os.path.join(G, 'heroes', h)] + glob.glob(os.path.join(G, 'dlc', '*', 'heroes', h)) + \
             glob.glob(os.path.join(G, 'dlc', '*', 'features', h, 'heroes', h)):
        if os.path.exists(os.path.join(p, h + '_A', h + '_portrait_roster.png')):
            return p
    raise FileNotFoundError(h)


def wrap(d, text, font, width):
    out, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            out.append(cur); cur = w
    return out + [cur]


def render(idx, h, c):
    hd = hero_dir(h)
    tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    colw = 450
    rows = []
    for s in c['skills']:
        o = [l for t in s['old'] for l in wrap(tmp, t, FT['row'], colw - 20)]
        n = [l for t in s['new'] for l in wrap(tmp, t, FT['row'], colw - 20)]
        rows.append((s, o, n, max(84, 50 + 34 * max(len(o), len(n)) + 14)))
    top = 200
    H = top + 40 + sum(r[3] for r in rows) + 70
    im = Image.new('RGB', (WID, H), BG)
    glow = Image.new('L', (WID, H), 0)
    ImageDraw.Draw(glow).ellipse((-200, -300, WID + 200, H + 300), fill=55)
    im = Image.composite(Image.new('RGB', (WID, H), (40, 32, 26)), im, glow.filter(ImageFilter.GaussianBlur(140)))
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, WID - 15, H - 15), outline=LINE, width=2)
    por = Image.open(os.path.join(hd, h + '_A', h + '_portrait_roster.png')).convert('RGB').resize((120, 120), Image.LANCZOS)
    im.paste(por, (48, 40)); d.rectangle((47, 39, 168, 160), outline=LINE, width=3)
    d.text((196, 48), c['name'], font=FT['hero'], fill=GOLD)
    d.text((198, 116), c['tagline'], font=FT['tag'], fill=DIM)
    x_old, x_new = 210, 210 + colw + 50
    d.text((x_old, top), 'VANILLA', font=FT['col'], fill=OLD)
    d.text((x_new, top), 'REBALANCE', font=FT['col'], fill=NEW)
    y = top + 40
    for s, o, n, rh in rows:
        d.rectangle((40, y, WID - 41, y + rh - 10), fill=PANEL, outline=(60, 48, 36), width=1)
        ip = os.path.join(hd, '%s.ability.%s.png' % (h, s['icon'])) if s.get('icon') else None
        if ip and os.path.exists(ip):
            im.paste(Image.open(ip).convert('RGB').resize((72, 72), Image.LANCZOS), (56, y + 12))
            d.rectangle((55, y + 11, 128, y + 84), outline=GOLD, width=2)
        d.text((x_old, y + 10), s['name'], font=FT['skill'], fill=GOLD)
        for j, t in enumerate(o):
            d.text((x_old, y + 52 + j * 34), t, font=FT['row'], fill=TEXT)
        for j, t in enumerate(n):
            d.text((x_new, y + 52 + j * 34), t, font=FT['row'], fill=TEXT)
        ay = y + 52 + 14
        d.polygon([(x_new - 34, ay - 10), (x_new - 18, ay), (x_new - 34, ay + 10)], fill=GOLD)
        y += rh
    d.text((48, H - 52), 'Every Hero Worth Taking  ·  values at level 1, ranges = levels 1-5', font=FT['foot'], fill=DIM)
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, '%02d_%s.png' % (idx, h))
    im.save(p, optimize=True)
    return p, os.path.getsize(p), im.size


if __name__ == '__main__':
    data = json.load(open(os.path.join(W, 'hero_cards.json'), encoding='utf-8'))
    for i, (h, c) in enumerate(data.items(), 1):
        print(*render(i, h, c))
