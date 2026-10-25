"""Independent Workshop hero cards; no mod edits, deletion, or publishing.

WS-CARD-001 (2026-10-23): approved two-page automation renderer. Retain the
original make_hero_cards.py artwork, 1200px width and Palatino font sizes;
wrap rather than shrink, and split only between complete skill blocks.

render_cards returns JSON-ready manifest entries. `path` is a filename relative
to out_dir (never an absolute path). out_dir must not already exist. Validation,
layout, assets and PNG limits are checked for the whole batch before creating it.
An OS write failure may leave a partial NEW directory; callers must not publish
without a successfully returned manifest, and must choose a fresh directory on
retry. Existing output is never deleted or overwritten.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from io import BytesIO
from itertools import zip_longest
import json
from pathlib import Path
import re
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH = 1200
# WS-CARD-002: user screenshots show these cards are too dense at Steam display
# size even below the pixel-height cap. Keep their skill groups on two pages.
TWO_PAGE_HEROES = frozenset({'highwayman', 'houndmaster', 'man_at_arms', 'shieldbreaker', 'vestal'})
PNG_LIMIT = 1_000_000  # Strictly below the Workshop additional-image limit.
BG, PANEL, LINE = (18, 15, 13), (30, 25, 21), (88, 70, 48)
GOLD, TEXT, DIM = (214, 180, 112), (226, 218, 200), (150, 140, 124)
OLD, NEW = (176, 92, 80), (132, 190, 120)
FOOTER = "Every Hero Worth Taking  ·  values at level 1, ranges = levels 1-5"
FONT_SPECS = {"hero": ("palab.ttf", 56), "tag": ("palai.ttf", 28),
              "col": ("palab.ttf", 22), "skill": ("palab.ttf", 30),
              "row": ("pala.ttf", 25), "foot": ("palai.ttf", 20)}
SAFE_COMPONENT = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*\Z")
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}


def _fonts() -> dict:
    # Fail explicitly if the original fonts are unavailable; no silent fallback
    # to a smaller or differently measured font at publication time.
    return {key: ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)
            for key, (name, size) in FONT_SPECS.items()}


def _text(value: Any, context: str) -> None:
    if (not isinstance(value, str) or not value.strip()
            or any((ord(c) < 32 and c != "\n") or ord(c) == 127 for c in value)):
        raise ValueError(f"{context}: expected nonempty printable text")


def _component(value: Any, context: str) -> None:
    if not isinstance(value, str) or not SAFE_COMPONENT.fullmatch(value) or value in RESERVED:
        raise ValueError(f"{context}: unsafe asset/path component {value!r}")


def _validate(data: dict, max_height: int) -> None:
    if type(max_height) is not int or max_height <= 0:
        raise ValueError("max_height must be a positive integer")
    if not isinstance(data, dict) or not data:
        raise ValueError("cards must be a nonempty hero mapping")
    for hero, card in data.items():
        _component(hero, "hero")
        if not isinstance(card, dict):
            raise ValueError(f"{hero}: expected a card object")
        for field in ("name", "tagline"):
            _text(card.get(field), f"{hero}.{field}")
        skills = card.get("skills")
        if not isinstance(skills, list) or not skills:
            raise ValueError(f"{hero}: skills must be a nonempty list")
        keys = set()
        for skill in skills:
            if not isinstance(skill, dict):
                raise ValueError(f"{hero}: expected a skill object")
            for field in ("key", "name"):
                _text(skill.get(field), f"{hero}.skill.{field}")
            if skill["key"] in keys:
                raise ValueError(f"{hero}: duplicate skill key {skill['key']!r}")
            keys.add(skill["key"])
            if skill.get("icon") is not None:
                _component(skill["icon"], f"{hero}.{skill['key']}.icon")
            for side in ("old", "new"):
                values = skill.get(side)
                if not isinstance(values, list) or not values:
                    raise ValueError(f"{hero}.{skill['key']}.{side}: expected nonempty row list")
                for value in values:
                    _text(value, f"{hero}.{skill['key']}.{side}")


def _span(draw, text, font) -> float:
    left, _, right, _ = draw.textbbox((0, 0), text, font=font)
    return max(right, draw.textlength(text, font=font)) - min(left, 0)


def _wrap(draw, text: str, font, width: int) -> tuple[str, ...]:
    """Wrap every explicit line; split oversized words at measured characters."""
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            proposed = f"{current} {word}" if current else word
            if _span(draw, proposed, font) <= width:
                current = proposed
                continue
            if current:
                lines.append(current)
            current = ""
            for char in word:
                if _span(draw, char, font) > width:
                    raise ValueError("a single glyph exceeds the available text width")
                if current and _span(draw, current + char, font) > width:
                    lines.append(current)
                    current = ""
                current += char
        lines.append(current)
    return tuple(lines)


def _leading(draw, lines, font, minimum: int) -> int:
    # The original baselines are sufficient for ordinary English. Tall glyphs
    # expand spacing, never reduce font size or intrude into another block.
    # Alignment padding has no ink and must not enlarge the original leading.
    boxes = [draw.textbbox((0, 0), text, font=font) for text in lines if text]
    if not boxes:
        return minimum
    return max(minimum, max(b[3] for b in boxes) - min(b[1] for b in boxes) + 4)


@dataclass(frozen=True)
class Block:
    key: str
    icon: str | None
    title: tuple[str, ...]
    old: tuple[str, ...]
    new: tuple[str, ...]
    title_step: int
    row_step: int
    row_y: int
    height: int


@dataclass(frozen=True)
class Layout:
    title: tuple[str, ...]
    tagline: tuple[str, ...]
    title_step: int
    tag_step: int
    tag_y: int
    top: int
    blocks: tuple[Block, ...]

    @property
    def overhead(self):
        return self.top + 40 + 70


def _measure(card, fonts) -> Layout:
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    title = _wrap(draw, card["name"], fonts["hero"], 950)
    tagline = _wrap(draw, card["tagline"], fonts["tag"], 950)
    title_step = _leading(draw, title, fonts["hero"], 68)
    tag_step = _leading(draw, tagline, fonts["tag"], 36)
    tag_y = 116 + (len(title) - 1) * title_step
    tag_bottom = tag_y + (len(tagline) - 1) * tag_step + max(
        draw.textbbox((0, 0), line, font=fonts["tag"])[3] for line in tagline)
    # Reserve a line for repeated Part 1/2 markers even in one-page layout;
    # this makes height thresholds independent of the pagination decision.
    top = max(200, tag_bottom + 44)
    blocks = []
    for skill in card["skills"]:
        name = _wrap(draw, skill["name"], fonts["skill"], 930)
        # WS-CARD-001 correction: independent column wrapping shifted later
        # comparisons (e.g. YAWP use limit vs corpse clearing). Keep each source
        # row pair together, including unmatched tails, before starting the next.
        old, new = (), ()
        for old_row, new_row in zip_longest(skill["old"], skill["new"], fillvalue=""):
            old_lines = _wrap(draw, old_row, fonts["row"], 430)
            new_lines = _wrap(draw, new_row, fonts["row"], 430)
            pair_height = max(len(old_lines), len(new_lines))
            old += old_lines + ("",) * (pair_height - len(old_lines))
            new += new_lines + ("",) * (pair_height - len(new_lines))
        title_step_skill = _leading(draw, name, fonts["skill"], 38)
        row_step = _leading(draw, old + new, fonts["row"], 34)
        row_y = 52 + (len(name) - 1) * title_step_skill
        bottom = max(draw.textbbox((0, 0), line, font=fonts["row"])[3] for line in old + new)
        count = max(len(old), len(new))
        height = max(98, row_y + (count - 1) * row_step + max(46, bottom + 20))
        blocks.append(Block(skill["key"], skill.get("icon"), name, old, new,
                            title_step_skill, row_step, row_y, height))
    return Layout(title, tagline, title_step, tag_step, tag_y, top, tuple(blocks))


def _paginate(hero: str, layout: Layout, max_height: int) -> list[tuple[Block, ...]]:
    heights = [b.height for b in layout.blocks]
    for block in layout.blocks:
        required = layout.overhead + block.height
        if required > max_height:
            raise ValueError(f"{hero}: individual skill {block.key!r} needs height {required}; "
                             f"max_height={max_height} (no clipping permitted)")
    total = sum(heights)
    if layout.overhead + total <= max_height and (hero not in TWO_PAGE_HEROES or len(heights) < 2):
        return [layout.blocks]
    prefix = 0
    choices = []
    for cut, height in enumerate(heights[:-1], 1):
        prefix += height
        choices.append((layout.overhead + max(prefix, total - prefix), cut))
    required, cut = min(choices)
    if required > max_height:
        raise ValueError(f"{hero}: no one/two-page layout fits max_height={max_height}; "
                         f"minimum two-page max_height={required}")
    return [layout.blocks[:cut], layout.blocks[cut:]]


def _within(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"asset escapes game_root: {path}")
    return resolved


def _hero_dir(root: Path, hero: str) -> Path:
    candidates = [root / "heroes" / hero]
    candidates += sorted(root.glob(f"dlc/*/heroes/{hero}"))
    candidates += sorted(root.glob(f"dlc/*/features/{hero}/heroes/{hero}"))
    for candidate in candidates:
        candidate = _within(candidate, root)
        portrait = _within(candidate / f"{hero}_A" / f"{hero}_portrait_roster.png", root)
        if portrait.is_file():
            return candidate
    raise FileNotFoundError(f"{hero}: roster portrait not found under {root}")


def _art(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        return source.convert("RGB").resize(size, Image.Resampling.LANCZOS)


def _put(draw, xy, text, font, color, width):
    # WS-CARD-001: measure ink as well as advance (italic bearings can overflow).
    # Every actual text draw is guarded; an impossible glyph fails explicitly.
    x, y = xy
    left, _, _, _ = draw.textbbox((0, 0), text, font=font)
    position = (x - min(left, 0), y)
    box = draw.textbbox(position, text, font=font)
    if box[0] < x or box[2] > x + width or box[1] < 0 or box[3] > draw._image.height:
        raise ValueError(f"text overflow: {text!r}")
    draw.text(position, text, font=font, fill=color)


def _draw_page(layout, blocks, fonts, portrait, icons, page, pages):
    height = layout.overhead + sum(b.height for b in blocks)
    image = Image.new("RGB", (WIDTH, height), BG)
    glow = Image.new("L", (WIDTH, height), 0)
    ImageDraw.Draw(glow).ellipse((-200, -300, WIDTH + 200, height + 300), fill=55)
    image = Image.composite(Image.new("RGB", image.size, (40, 32, 26)), image,
                            glow.filter(ImageFilter.GaussianBlur(140)))
    draw = ImageDraw.Draw(image)
    draw.rectangle((14, 14, WIDTH - 15, height - 15), outline=LINE, width=2)
    image.paste(portrait, (48, 40))
    draw.rectangle((47, 39, 168, 160), outline=LINE, width=3)
    for i, text in enumerate(layout.title):
        _put(draw, (196, 48 + i * layout.title_step), text, fonts["hero"], GOLD, 950)
    for i, text in enumerate(layout.tagline):
        _put(draw, (198, layout.tag_y + i * layout.tag_step), text, fonts["tag"], DIM, 950)
    if pages == 2:
        _put(draw, (198, layout.top - 30), f"Part {page}/{pages}", fonts["foot"], DIM, 950)
    for x, text, color in [(210, "VANILLA", OLD), (710, "REBALANCE", NEW)]:
        _put(draw, (x, layout.top), text, fonts["col"], color, 430)
    y = layout.top + 40
    for block in blocks:
        draw.rectangle((40, y, WIDTH - 41, y + block.height - 10),
                       fill=PANEL, outline=(60, 48, 36), width=1)
        if block.icon is not None:
            image.paste(icons[block.icon], (56, y + 12))
            draw.rectangle((55, y + 11, 128, y + 84), outline=GOLD, width=2)
        for i, text in enumerate(block.title):
            _put(draw, (210, y + 10 + i * block.title_step), text, fonts["skill"], GOLD, 930)
        for x, rows in [(210, block.old), (710, block.new)]:
            for i, text in enumerate(rows):
                _put(draw, (x, y + block.row_y + i * block.row_step), text, fonts["row"], TEXT, 430)
        ay = y + block.row_y + 14
        draw.polygon([(676, ay - 10), (692, ay), (676, ay + 10)], fill=GOLD)
        y += block.height
    _put(draw, (48, height - 52), FOOTER, fonts["foot"], DIM, 1100)
    return image


def _skill_art(folder, game_root, hero, icon, mod_root=None):
    # WS-ASSET-001: use committed custom skill art, with vanilla fallback.
    if mod_root is not None:
        candidate = Path(mod_root) / 'heroes' / hero / f'{hero}.ability.{icon}.png'
        if candidate.exists():
            return _art(_within(candidate, Path(mod_root).resolve(strict=True)), (72, 72))
    return _art(_within(folder / f'{hero}.ability.{icon}.png', game_root), (72, 72))


def render_cards(cards: dict, game_root: Path, out_dir: Path, max_height: int = 1500, mod_root: Path | None = None) -> list[dict]:
    """Render one or two readable PNGs per hero; return relative-path manifest.

    Short cards stay on one page. Long cards use the ordered skill boundary
    minimizing the taller page; ties use the earlier boundary. All source rows
    appear once, in source order. Bounty Hunter is first when present, followed
    by input insertion order. Missing required art is an error, not a blank icon.
    """
    _validate(cards, max_height)
    game_root, out_dir = Path(game_root).resolve(strict=True), Path(out_dir)
    if not game_root.is_dir():
        raise ValueError("game_root must be a directory")
    if out_dir.exists() or out_dir.is_symlink():
        raise FileExistsError(f"output directory must be new: {out_dir}")
    if out_dir.resolve().is_relative_to(game_root):
        raise ValueError("out_dir must be outside game_root; game files are read-only")
    fonts = _fonts()
    order = (["bounty_hunter"] if "bounty_hunter" in cards else []) + [h for h in cards if h != "bounty_hunter"]
    prepared = []
    for index, hero in enumerate(order, 1):
        try:
            layout = _measure(cards[hero], fonts)
            pages = _paginate(hero, layout, max_height)
            folder = _hero_dir(game_root, hero)
            portrait = _art(_within(folder / f"{hero}_A" / f"{hero}_portrait_roster.png", game_root), (120, 120))
            icons = {b.icon: _skill_art(folder, game_root, hero, b.icon, mod_root)
                     for b in layout.blocks if b.icon is not None}
            for page, blocks in enumerate(pages, 1):
                image = _draw_page(layout, blocks, fonts, portrait, icons, page, len(pages))
                buffer = BytesIO()
                image.save(buffer, format="PNG", optimize=True)
                payload = buffer.getvalue()
                if len(payload) >= PNG_LIMIT:
                    raise ValueError(f"PNG page {page} is {len(payload)} bytes; must be <1,000,000; "
                                     "no lossy compression or shrinking permitted")
                suffix = f"_p{page}" if len(pages) == 2 else ""
                item = {"hero": hero, "page": page, "pages": len(pages),
                        "path": f"{index:02d}_{hero}{suffix}.png", "width": image.width,
                        "height": image.height, "sha256": hashlib.sha256(payload).hexdigest(),
                        "size": len(payload), "skill_keys": [b.key for b in blocks]}
                prepared.append((item, payload))
        except ValueError as exc:
            raise ValueError(f"{hero}: {exc}") from exc
    # WS-CARD-001: no stale-file cleanup. Exclusive creation also catches another
    # renderer racing for this output path after the initial existence check.
    out_dir.mkdir(parents=True, exist_ok=False)
    for item, payload in prepared:
        with (out_dir / item["path"]).open("xb") as target:
            target.write(payload)
    return [item for item, _ in prepared]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--game-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-height", type=int, default=1500)
    parser.add_argument("--mod-root", type=Path)
    args = parser.parse_args(argv)
    try:
        with args.input.open(encoding="utf-8-sig") as source:
            data = json.load(source)
        manifest = render_cards(data, args.game_root, args.out, args.max_height, mod_root=args.mod_root)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"cards: {exc}\n")
    print(json.dumps(manifest, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
