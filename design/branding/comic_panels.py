# 공식 오리진 코믹스(Red Hook, source_art/comic_*.png) → 칸(패널) 자동 분할 + 번호 붙인 확인용 시트
# 사용: python design/branding/comic_panels.py [출력 폴더]  → panels.json + sheet_<n>.png
import glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source_art')


def panels(path, dark=34, min_frac=0.06):
    """어두운 여백(거터)을 배경으로 보고, 밝은 덩어리의 연결 영역 = 칸."""
    im = Image.open(path).convert('RGB')
    W, H = im.size
    s = 400 / W
    small = im.resize((400, int(H * s)), Image.BILINEAR).convert('L')
    mask = small.point(lambda v: 255 if v > dark else 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    w, h = mask.size
    px = mask.load()
    seen = bytearray(w * h)
    boxes = []
    for y in range(h):
        for x in range(w):
            if px[x, y] and not seen[y * w + x]:
                stack = [(x, y)]
                seen[y * w + x] = 1
                x0 = x1 = x
                y0 = y1 = y
                n = 0
                while stack:
                    cx, cy = stack.pop()
                    n += 1
                    x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and not seen[ny * w + nx]:
                            seen[ny * w + nx] = 1
                            stack.append((nx, ny))
                bw, bh = x1 - x0 + 1, y1 - y0 + 1
                if bw > w * min_frac * 2 and bh > h * min_frac / 1.5 and n > bw * bh * 0.35:
                    boxes.append([int(x0 / s), int(y0 / s), int((x1 + 1) / s), int((y1 + 1) / s)])
    boxes.sort(key=lambda b: (b[1] // 40, b[0]))
    return im.size, boxes


def main(out):
    os.makedirs(out, exist_ok=True)
    data = {}
    for f in sorted(glob.glob(os.path.join(SRC, 'comic_*.png'))):
        hero = os.path.basename(f)[6:-4]
        if hero.endswith('_dup'):
            continue
        size, boxes = panels(f)
        data[hero] = {'file': os.path.basename(f), 'size': size, 'panels': boxes}
    json.dump(data, open(os.path.join(out, 'panels.json'), 'w'), indent=1)
    fnt = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 20)
    heroes = list(data)
    for gi in range(0, len(heroes), 3):
        group = heroes[gi:gi + 3]
        tiles = []
        for hero in group:
            im = Image.open(os.path.join(SRC, data[hero]['file'])).convert('RGB')
            sc = 560 / im.width
            page = im.resize((560, int(im.height * sc)))
            d = ImageDraw.Draw(page)
            for i, (x0, y0, x1, y1) in enumerate(data[hero]['panels']):
                b = [int(v * sc) for v in (x0, y0, x1, y1)]
                d.rectangle(b, outline=(0, 255, 120), width=2)
                d.rectangle((b[0], b[1], b[0] + 34, b[1] + 26), fill=(0, 0, 0))
                d.text((b[0] + 4, b[1] + 1), str(i), font=fnt, fill=(0, 255, 120))
            d.text((6, 4), hero, font=fnt, fill=(255, 220, 90))
            tiles.append(page)
        Hh = max(t.height for t in tiles)
        sheet = Image.new('RGB', (sum(t.width for t in tiles) + 10 * (len(tiles) - 1), Hh), (40, 40, 40))
        x = 0
        for t in tiles:
            sheet.paste(t, (x, 0))
            x += t.width + 10
        sheet.save(os.path.join(out, f'sheet_{gi // 3}.png'))
    for h, v in data.items():
        print(h, v['size'], len(v['panels']))


if __name__ == '__main__':
    main(sys.argv[1])
