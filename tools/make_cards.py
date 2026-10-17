# 창작마당용 전/후 비교 카드: 게임의 기술 아이콘·영웅 초상화 + 바닐라/리밸런스 수치
# 사용: python tools/make_cards.py  → design/workshop/cards/*.png
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

G = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(os.path.dirname(__file__), '..', 'design', 'workshop', 'cards')
F = 'C:/Windows/Fonts/'
BG, PANEL, LINE = (18, 15, 13), (32, 27, 23), (88, 70, 48)
GOLD, TEXT, DIM, OLD, NEW = (214, 180, 112), (226, 218, 200), (150, 140, 124), (176, 92, 80), (132, 190, 120)

CARDS = [
    dict(file='hellion_yawp', hero='hellion', icon='three',
         title='Barbaric YAWP!', sub='Hellion',
         old=['Stuns ranks 1-2', 'Self: DMG -20%, SPD -3', '(exhaustion lasts all battle)', '3 uses per battle'],
         new=['Self: ACC +5%, DMG +20%', 'All enemies: DMG -10% (3 turns)', 'Clears corpses', 'No use limit'],
         why='A war cry that fires her up, not one that exhausts her.'),
    dict(file='vestal_illumination', hero='vestal', icon='six',
         title='Illumination', sub='Vestal',
         old=['Usable from ranks 1-3', 'ACC 90', 'Target: dodge -20%'],
         new=['Usable from any rank', 'ACC 95', 'Target: damage taken +20% (3 turns)', 'Burn 1'],
         why='Holy light exposes and burns evil, and a front-rank Vestal has a tool.'),
    dict(file='bh_uppercut', hero='bounty_hunter', icon='four',
         title='Uppercut', sub='Bounty Hunter',
         old=['Targets ranks 1-2', 'ACC 90, CRIT 0%', 'Stun 100%'],
         new=['Targets rank 1 only', 'ACC 95, CRIT 9%', 'Strong stun 110%'],
         why='A front-rank execution stun, distinct from Flashbang.'),
]


def font(name, size):
    return ImageFont.truetype(F + name, size)


def card(c):
    W, H = 1200, 520
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    # 바탕 비네팅
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-200, -260, W + 200, H + 260), fill=60)
    im = Image.composite(Image.new('RGB', (W, H), (40, 32, 26)), im, glow.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, W - 15, H - 15), outline=LINE, width=2)
    # 머리: 초상화 + 아이콘 + 이름
    por = Image.open(os.path.join(G, 'heroes', c['hero'], c['hero'] + '_A', c['hero'] + '_portrait_roster.png')).convert('RGB').resize((96, 96), Image.LANCZOS)
    ico = Image.open(os.path.join(G, 'heroes', c['hero'], '%s.ability.%s.png' % (c['hero'], c['icon']))).convert('RGB').resize((96, 96), Image.LANCZOS)
    im.paste(por, (48, 40)); d.rectangle((47, 39, 144, 136), outline=LINE, width=2)
    im.paste(ico, (160, 40)); d.rectangle((159, 39, 256, 136), outline=GOLD, width=2)
    d.text((284, 46), c['title'], font=font('palab.ttf', 46), fill=GOLD)
    d.text((286, 102), c['sub'], font=font('palai.ttf', 26), fill=DIM)
    # 두 칸: 원작 / 리밸런스
    top, colw = 168, (W - 48 * 2 - 40) // 2
    for i, (lab, rows, col) in enumerate((('VANILLA', c['old'], OLD), ('REBALANCE', c['new'], NEW))):
        x = 48 + i * (colw + 40)
        d.rectangle((x, top, x + colw, top + 250), fill=PANEL, outline=LINE, width=1)
        d.text((x + 24, top + 16), lab, font=font('palab.ttf', 24), fill=col)
        for j, r in enumerate(rows):
            d.text((x + 24, top + 62 + j * 42), r, font=font('pala.ttf', 28), fill=TEXT)
    # 화살표
    ax, ay = 48 + colw + 20, top + 125
    d.polygon([(ax - 10, ay - 16), (ax + 12, ay), (ax - 10, ay + 16)], fill=GOLD)
    d.text((48, H - 82), c['why'], font=font('palai.ttf', 27), fill=DIM)
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, c['file'] + '.png')
    im.save(p)
    return p


if __name__ == '__main__':
    for c in CARDS:
        print(card(c))
