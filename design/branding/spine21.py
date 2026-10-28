# Darkest Dungeon 영웅 Spine 2.1.27 바이너리(.skel)+아틀라스(.atlas) → 셋업 포즈 전신 이미지 (브랜딩 시안용, 읽기 전용)
# 형식: Esoteric Spine 2.1 SkeletonBinary (bones → ik → slots → skins). 애니메이션은 읽지 않는다.
import math, os, struct
from PIL import Image


class R:
    def __init__(self, b):
        self.b, self.p = b, 0

    def byte(self):
        v = self.b[self.p]
        self.p += 1
        return v

    def bool(self):
        return self.byte() != 0

    def varint(self):
        v, shift = 0, 0
        while True:
            c = self.byte()
            v |= (c & 0x7F) << shift
            if not c & 0x80:
                return v
            shift += 7

    def int(self):
        v = struct.unpack('>i', self.b[self.p:self.p + 4])[0]
        self.p += 4
        return v

    def float(self):
        v = struct.unpack('>f', self.b[self.p:self.p + 4])[0]
        self.p += 4
        return v

    def short(self):
        v = struct.unpack('>h', self.b[self.p:self.p + 2])[0]
        self.p += 2
        return v

    def str(self):
        n = self.varint()
        if n == 0:
            return None
        s = self.b[self.p:self.p + n - 1].decode('utf-8')
        self.p += n - 1
        return s

    def floats(self):
        return [self.float() for _ in range(self.varint())]

    def shorts(self):
        return [self.short() for _ in range(self.varint())]


def read_skel(path):
    r = R(open(path, 'rb').read())
    sk = {'hash': r.str(), 'version': r.str(), 'width': r.float(), 'height': r.float()}
    nonessential = r.bool()
    if nonessential:
        r.str()
    bones = []
    for _ in range(r.varint()):
        name = r.str()
        parent = r.varint() - 1
        b = dict(name=name, parent=parent, x=r.float(), y=r.float(), sx=r.float(), sy=r.float(), rot=r.float(), length=r.float(),
                 flipX=r.bool(), flipY=r.bool(), inhScale=r.bool(), inhRot=r.bool())
        if nonessential:
            r.int()
        bones.append(b)
    for _ in range(r.varint()):  # ik constraints
        r.str()
        [r.varint() for _ in range(r.varint())]
        r.varint()
        r.float()
        r.byte()
    slots = []
    for _ in range(r.varint()):
        slots.append(dict(name=r.str(), bone=r.varint(), color=r.int(), attachment=r.str(), additive=r.bool()))
    skin = {}
    for _ in range(r.varint()):
        si = r.varint()
        for _ in range(r.varint()):
            key = r.str()
            name = r.str() or key
            t = r.byte()
            if t == 0:
                a = dict(type='region', path=r.str() or name, x=r.float(), y=r.float(), sx=r.float(), sy=r.float(), rot=r.float(),
                         w=r.float(), h=r.float(), color=r.int())
            elif t == 1:
                a = dict(type='bbox', v=r.floats())
            elif t == 2:
                a = dict(type='mesh', path=r.str() or name, uvs=r.floats(), tris=r.shorts(), v=r.floats(), color=r.int(), hull=r.varint())
                if nonessential:
                    r.shorts(); r.float(); r.float()
            elif t == 3:
                path = r.str() or name
                uvs, tris = r.floats(), r.shorts()
                n = r.varint()
                verts, i = [], 0
                while i < n:
                    bc = int(r.float())
                    infl = []
                    for _ in range(bc):
                        infl.append((int(r.float()), r.float(), r.float(), r.float()))
                    verts.append(infl)
                    i += 1 + bc * 4
                a = dict(type='skinned', path=path, uvs=uvs, tris=tris, verts=verts, color=r.int(), hull=r.varint())
                if nonessential:
                    r.shorts(); r.float(); r.float()
            else:
                raise ValueError('attachment type %d at %d' % (t, r.p))
            a['name'] = name
            skin[(si, key)] = a
    sk.update(bones=bones, slots=slots, skin=skin)
    return sk


def read_atlas(path, page_dir=None):
    regions, cur, page = {}, None, None
    for line in open(path, encoding='utf-8').read().splitlines():
        if not line.strip():
            page = None
            continue
        if page is None:
            page = os.path.join(page_dir or os.path.dirname(path), line.strip())
            continue
        if ':' not in line:
            cur = regions.setdefault(line.strip(), {'page': page})
            continue
        k, v = [x.strip() for x in line.split(':', 1)]
        if cur is not None and k in ('rotate', 'xy', 'size', 'orig', 'offset', 'index'):
            cur[k] = v if k == 'rotate' else [int(x) for x in v.split(',')]
    return regions


def world(bones):
    """Spine 2.1 Bone.updateWorldTransform (setup pose)."""
    for b in bones:
        if b['parent'] < 0:
            b['wx'], b['wy'] = b['x'], b['y']
            b['wsx'], b['wsy'], b['wr'] = b['sx'], b['sy'], b['rot']
            b['wfx'], b['wfy'] = b['flipX'], b['flipY']
        else:
            p = bones[b['parent']]
            b['wx'] = b['x'] * p['m00'] + b['y'] * p['m01'] + p['wx']
            b['wy'] = b['x'] * p['m10'] + b['y'] * p['m11'] + p['wy']
            b['wsx'] = p['wsx'] * b['sx'] if b['inhScale'] else b['sx']
            b['wsy'] = p['wsy'] * b['sy'] if b['inhScale'] else b['sy']
            b['wr'] = p['wr'] + b['rot'] if b['inhRot'] else b['rot']
            b['wfx'] = p['wfx'] != b['flipX']
            b['wfy'] = p['wfy'] != b['flipY']
        rad = math.radians(b['wr'])
        c, s = math.cos(rad), math.sin(rad)
        b['m00'], b['m01'] = c * b['wsx'], -s * b['wsy']
        b['m10'], b['m11'] = s * b['wsx'], c * b['wsy']
        if b['wfx']:
            b['m00'], b['m01'] = -b['m00'], -b['m01']
        if b['wfy']:
            b['m10'], b['m11'] = -b['m10'], -b['m11']


def _region_image(reg, cache):
    page = cache.setdefault(reg['page'], Image.open(reg['page']).convert('RGBA'))
    x, y = reg['xy']
    w, h = reg['size']
    if reg.get('rotate') == 'true':
        return page.crop((x, y, x + h, y + w)).transpose(Image.ROTATE_270)
    return page.crop((x, y, x + w, y + h))


def _tri_warp(canvas, src, s_tri, d_tri):
    """Affine-map one source triangle onto the canvas (meshes)."""
    (x0, y0), (x1, y1), (x2, y2) = d_tri
    (u0, v0), (u1, v1), (u2, v2) = s_tri
    minx, miny = int(math.floor(min(x0, x1, x2))), int(math.floor(min(y0, y1, y2)))
    maxx, maxy = int(math.ceil(max(x0, x1, x2))), int(math.ceil(max(y0, y1, y2)))
    if maxx <= minx or maxy <= miny:
        return
    det = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    if abs(det) < 1e-6:
        return
    # inverse affine: dest(x,y) -> src(u,v)
    a = ((u1 - u0) * (y2 - y0) - (u2 - u0) * (y1 - y0)) / det
    b = ((u2 - u0) * (x1 - x0) - (u1 - u0) * (x2 - x0)) / det
    c = u0 - a * x0 - b * y0
    d = ((v1 - v0) * (y2 - y0) - (v2 - v0) * (y1 - y0)) / det
    e = ((v2 - v0) * (x1 - x0) - (v1 - v0) * (x2 - x0)) / det
    f = v0 - d * x0 - e * y0
    w, h = maxx - minx, maxy - miny
    patch = src.transform((w, h), Image.AFFINE, (a, b, a * minx + b * miny + c, d, e, d * minx + e * miny + f), Image.BILINEAR)
    from PIL import ImageDraw
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).polygon([(x0 - minx, y0 - miny), (x1 - minx, y1 - miny), (x2 - minx, y2 - miny)], fill=255)
    m = Image.composite(patch.getchannel('A'), Image.new('L', (w, h), 0), m)
    patch.putalpha(m)
    canvas.alpha_composite(patch, (minx, miny)) if minx >= 0 and miny >= 0 else canvas.paste(patch, (minx, miny), patch)


def render(skel_path, atlas_path, scale=1.0, pad=40, page_dir=None):
    sk = read_skel(skel_path)
    atlas = read_atlas(atlas_path, page_dir)
    bones = sk['bones']
    world(bones)
    draws = []  # (kind, data) in world coords (y up)
    for si, slot in enumerate(sk['slots']):
        if not slot['attachment']:
            continue
        a = sk['skin'].get((si, slot['attachment']))
        if not a or a['type'] == 'bbox':
            continue
        reg = atlas.get(a['path'])
        if reg is None:
            continue
        b = bones[slot['bone']]
        if a['type'] == 'region':
            rad = math.radians(a['rot'])
            c, s = math.cos(rad), math.sin(rad)
            hw, hh = a['w'] / 2 * a['sx'], a['h'] / 2 * a['sy']
            local = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]  # BL, BR, TR, TL
            pts = []
            for lx, ly in local:
                x = lx * c - ly * s + a['x']
                y = lx * s + ly * c + a['y']
                pts.append((x * b['m00'] + y * b['m01'] + b['wx'], x * b['m10'] + y * b['m11'] + b['wy']))
            draws.append(('region', reg, pts, slot['additive']))
        elif a['type'] == 'mesh':
            v = a['v']
            pts = [(v[i] * b['m00'] + v[i + 1] * b['m01'] + b['wx'], v[i] * b['m10'] + v[i + 1] * b['m11'] + b['wy']) for i in range(0, len(v), 2)]
            draws.append(('mesh', reg, (pts, a['uvs'], a['tris']), slot['additive']))
        elif a['type'] == 'skinned':
            pts = []
            for infl in a['verts']:
                wx = wy = 0.0
                for bi, vx, vy, wgt in infl:
                    bb = bones[bi]
                    wx += (vx * bb['m00'] + vy * bb['m01'] + bb['wx']) * wgt
                    wy += (vx * bb['m10'] + vy * bb['m11'] + bb['wy']) * wgt
                pts.append((wx, wy))
            draws.append(('mesh', reg, (pts, a['uvs'], a['tris']), slot['additive']))
    allpts = [p for d in draws for p in (d[2] if d[0] == 'region' else d[2][0])]
    minx, maxx = min(p[0] for p in allpts), max(p[0] for p in allpts)
    miny, maxy = min(p[1] for p in allpts), max(p[1] for p in allpts)
    W, H = int((maxx - minx) * scale) + pad * 2, int((maxy - miny) * scale) + pad * 2
    to = lambda p: ((p[0] - minx) * scale + pad, (maxy - p[1]) * scale + pad)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cache = {}
    for kind, reg, data, additive in draws:
        img = _region_image(reg, cache)
        if additive:
            continue  # 빛 효과 슬롯은 브랜딩 정지 이미지에서 생략
        if kind == 'region':
            q = [to(p) for p in data]
            iw, ih = img.size
            _tri_warp(canvas, img, [(0, ih), (iw, ih), (iw, 0)], [q[0], q[1], q[2]])
            _tri_warp(canvas, img, [(0, ih), (iw, 0), (0, 0)], [q[0], q[2], q[3]])
        else:
            pts, uvs, tris = data
            page = cache.setdefault(reg['page'], Image.open(reg['page']).convert('RGBA'))
            q = [to(p) for p in pts]
            rx, ry = reg['xy']
            rw, rh = reg['size']
            # 메쉬 UV는 영역 기준(0~1). 회전된 영역은 Spine MeshAttachment.updateUVs와 같게 축을 바꾼다.
            if reg.get('rotate') == 'true':
                src = [(rx + uvs[i + 1] * rh, ry + rw - uvs[i] * rw) for i in range(0, len(uvs), 2)]
            else:
                src = [(rx + uvs[i] * rw, ry + uvs[i + 1] * rh) for i in range(0, len(uvs), 2)]
            for t in range(0, len(tris), 3):
                i0, i1, i2 = tris[t], tris[t + 1], tris[t + 2]
                _tri_warp(canvas, page, [src[i0], src[i1], src[i2]], [q[i0], q[i1], q[i2]])
    return canvas


if __name__ == '__main__':
    import sys
    G = 'C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon'
    hero, anim = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'combat'
    base = os.path.join(G, 'heroes', hero, 'anim', f'{hero}.sprite.{anim}')
    sk = read_skel(base + '.skel')
    kinds = {}
    for a in sk['skin'].values():
        kinds[a['type']] = kinds.get(a['type'], 0) + 1
    print(sk['version'], len(sk['bones']), 'bones', len(sk['slots']), 'slots', kinds)
    im = render(base + '.skel', base + '.atlas', page_dir=os.path.join(G, 'heroes', hero, hero + '_A', 'anim'))
    out = sys.argv[3] if len(sys.argv) > 3 else f'{hero}_{anim}.png'
    im.save(out)
    print(out, im.size)
