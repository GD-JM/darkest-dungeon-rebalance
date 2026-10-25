"""LEP-007: build the Sunder (갑옷 쪼개기) skill icon -> heroes/leper/leper.ability.seven.png.

Made only from vanilla Leper icon pixels so it keeps the game's art style:
- shield = Leper "six" (Withstand) split along its center seam, halves tilted apart;
- background = "six" teal glow gradient-mapped onto the warm palette of Leper "two" (Hew);
- frame = Leper "one" (Chop) grey attack frame;
- bolt in the split uses only colors found in vanilla icons (no white/yellow core, see design/changes/leper.md LEP-007).
Run from the mod root: python tools/make_sunder_icon.py
"""
import bisect, colorsys, os, random
from PIL import Image, ImageChops, ImageDraw, ImageFilter

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.dirname(os.path.dirname(MOD))
load = lambda n: Image.open(os.path.join(GAME, 'heroes', 'leper', 'leper.ability.%s.png' % n)).convert('RGBA')
one, two, six = load('one'), load('two'), load('six')
N = 72; IN = 6  # icon size, interior starts inside the frame
BOLT_CORE = (205, 112, 20, 255)  # typical bright orange of vanilla icons (runaway one 90th pct)
BOLT_RIM = (159, 49, 0, 255)     # leper two 90th pct warm
BOLT_GRAIN = (184, 91, 48, 255)  # leper four median warm
lum = lambda c: 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
hsv = lambda c: colorsys.rgb_to_hsv(*[v/255 for v in c[:3]])

pal = sorted((two.getpixel((x, y))[:3] for y in range(IN, N-IN) for x in range(IN, N-IN) if hsv(two.getpixel((x, y)))[1] > 0.35), key=lum)
src = sorted(lum(six.getpixel((x, y))) for y in range(IN, N-IN) for x in range(IN, N-IN) if hsv(six.getpixel((x, y)))[1] > 0.25)
def gradmap(c, boost=0.0):
    # luminance quantile in the teal background -> same quantile of the warm palette
    q = min(0.999, bisect.bisect_left(src, lum(c)) / len(src) + boost)
    return pal[int(q * len(pal))] + (255,)

def light_mask(im, vmin, smax):
    m = Image.new('L', im.size, 0); pm = m.load()
    for y in range(IN, N-IN):
        for x in range(IN, N-IN):
            h, s, v = hsv(im.getpixel((x, y)))
            if v > vmin and s < smax: pm[x, y] = 255
    return m

shield_mask = light_mask(six, 0.45, 0.25).filter(ImageFilter.MaxFilter(5))
back = six.copy(); pb = back.load()
for y in range(N):
    for x in range(N):
        c = six.getpixel((x, y))
        if hsv(c)[1] > 0.25:
            pb[x, y] = gradmap(c, boost=0.18 * (1 - abs(x - 36) / 36) ** 2)
# dark grainy gap behind the shield so the bolt reads
random.seed(3)
fill = Image.new('RGBA', (N, N)); pf = fill.load()
for y in range(N):
    for x in range(N):
        q = 0.03 + 0.10 * (1 - y / N) + random.uniform(-0.02, 0.04)
        pf[x, y] = pal[int(max(0.02, min(0.995, q)) * len(pal))] + (255,)
back = Image.composite(fill, back, shield_mask)

# shield: parchment + ink only (drop the teal fringe of the dilated outline)
shield = Image.new('RGBA', (N, N), (0, 0, 0, 0)); ps = shield.load()
for y in range(N):
    for x in range(N):
        if shield_mask.getpixel((x, y)):
            c = six.getpixel((x, y)); h, s, v = hsv(c)
            ps[x, y] = c if s < 0.25 else (int(v*40), int(v*38), int(v*34), 255)
sw = int(N * 0.86)  # shrink so both tilted halves stay inside the frame
tmp = Image.new('RGBA', (N, N), (0, 0, 0, 0)); tmp.paste(shield.resize((sw, sw), Image.NEAREST), ((N - sw)//2, (N - sw)//2 + 3)); shield = tmp

crack = [(36, 0), (37, 14), (34, 22), (38, 31), (33, 40), (37, 49), (35, 58), (36, N)]
def half(left):
    m = Image.new('L', (N, N), 0)
    ImageDraw.Draw(m).polygon(([(0, 0)] + crack + [(0, N)]) if left else ([(N, 0)] + crack + [(N, N)]), fill=255)
    h = Image.new('RGBA', (N, N), (0, 0, 0, 0)); h.paste(shield, (0, 0), m)
    a = h.getchannel('A'); edge = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(3)), a)
    ol = Image.new('RGBA', (N, N), (0, 0, 0, 255)); ol.putalpha(edge); ol.alpha_composite(h); return ol
left = half(True).rotate(11, resample=Image.NEAREST, center=(14, 64), translate=(-3, 0))
right = half(False).rotate(-11, resample=Image.NEAREST, center=(58, 64), translate=(3, 0))

img = back.copy()
random.seed(11)
bolt = [(36, 6), (35, 16), (37, 26), (34, 36), (37, 46), (35, 56), (36, 66)]
lay = Image.new('RGBA', (N, N), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
ld.line(bolt, fill=BOLT_RIM, width=4)
ld.line(bolt, fill=BOLT_CORE, width=2)
pl = lay.load()
for y in range(N):  # grain so the stroke reads hand-painted like vanilla light
    for x in range(N):
        if pl[x, y][3] and random.random() < 0.18: pl[x, y] = BOLT_GRAIN
img.alpha_composite(lay)
img.alpha_composite(left); img.alpha_composite(right)

out = one.copy(); box = (IN, IN, N-IN, N-IN); out.paste(img.crop(box), box[:2])
out.save(os.path.join(MOD, 'heroes', 'leper', 'leper.ability.seven.png'))
