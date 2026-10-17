# 창작마당 대표 이미지: 비교 카드(make_cards.py)와 같은 톤 — 어두운 갈색 바탕, 청동 테두리, 금색 팔라티노 제목, 게임 초상화
# 사용: python tools/make_preview.py [배경.png]  → design/workshop/cards/preview.png (+ 미리보기 아이콘용 사본)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

G = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
M = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
F = 'C:/Windows/Fonts/'
BG, LINE, GOLD, DIM = (18, 15, 13), (88, 70, 48), (214, 180, 112), (150, 140, 124)
HEROES = ['crusader', 'highwayman', 'plague_doctor', 'vestal', 'leper', 'hellion', 'bounty_hunter', 'occultist', 'grave_robber',
          'jester', 'man_at_arms', 'houndmaster', 'arbalest', 'antiquarian', 'abomination', 'flagellant', 'shieldbreaker', 'runaway', 'duelist']


def portrait(h):
    for root in (os.path.join(G, 'heroes'), *[os.path.join(G, 'dlc', d, 'heroes') for d in os.listdir(os.path.join(G, 'dlc'))],
                 *[os.path.join(G, 'dlc', d, 'features', h, 'heroes') for d in os.listdir(os.path.join(G, 'dlc'))]):
        p = os.path.join(root, h, h + '_A', h + '_portrait_roster.png')
        if os.path.exists(p):
            return Image.open(p).convert('RGB')
    raise FileNotFoundError(h)


def main(bg_path=None):
    S = 1024
    if bg_path:
        im = Image.open(bg_path).convert('RGB').resize((S, S), Image.LANCZOS)
        im = ImageEnhance.Brightness(im).enhance(0.55)
    else:
        im = Image.new('RGB', (S, S), BG)
        glow = Image.new('L', (S, S), 0)
        ImageDraw.Draw(glow).ellipse((-150, -100, S + 150, S + 250), fill=70)
        im = Image.composite(Image.new('RGB', (S, S), (44, 35, 28)), im, glow.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(im)
    d.rectangle((22, 22, S - 23, S - 23), outline=LINE, width=3)
    d.rectangle((34, 34, S - 35, S - 35), outline=(54, 44, 32), width=1)
    # 제목
    tf = ImageFont.truetype(F + 'palab.ttf', 128)
    t = 'REBALANCE'
    w = d.textlength(t, font=tf)
    d.text(((S - w) / 2 + 4, 84 + 4), t, font=tf, fill=(0, 0, 0))
    d.text(((S - w) / 2, 84), t, font=tf, fill=GOLD)
    sf = ImageFont.truetype(F + 'palai.ttf', 46)
    s = 'every hero worth taking'
    w = d.textlength(s, font=sf)
    d.text(((S - w) / 2, 238), s, font=sf, fill=DIM)
    # 초상화 격자 5-5-5-4
    size, gap = 140, 20
    rows = [HEROES[0:5], HEROES[5:10], HEROES[10:15], HEROES[15:19]]
    y = 322
    for r in rows:
        x0 = (S - (len(r) * size + (len(r) - 1) * gap)) / 2
        for i, h in enumerate(r):
            x = int(x0 + i * (size + gap))
            im.paste(portrait(h).resize((size, size), Image.LANCZOS), (x, y))
            d.rectangle((x - 2, y - 2, x + size + 1, y + size + 1), outline=LINE, width=3)
        y += size + gap
    out = os.path.join(M, 'design', 'workshop', 'cards', 'preview.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    print(out, os.path.getsize(out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
