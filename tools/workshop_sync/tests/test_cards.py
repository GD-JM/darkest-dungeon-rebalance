"""WS-CARD-001: exercise pagination through real Pillow output, without Steam."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from unittest.mock import patch

from PIL import Image, ImageDraw

MODULE = Path(__file__).resolve().parents[1] / "cards.py"
if MODULE.exists():
    spec = importlib.util.spec_from_file_location("workshop_cards", MODULE)
    cards = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = cards
    spec.loader.exec_module(cards)
else:
    cards = None


def sample(hero="example", count=1, rows=1):
    return {hero: {
        "name": "Example Hero", "tagline": "Every skill stays readable.",
        "skills": [{"key": f"{hero}|skill_{i}", "name": f"Skill {i}", "icon": "one",
                    "old": [f"Old-{i}-{j}" for j in range(rows)],
                    "new": [f"New-{i}-{j}" for j in range(rows)]}
                   for i in range(count)]}}


class CardTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(cards, "independent cards.py renderer has not been implemented")
        self.tmp = tempfile.TemporaryDirectory(dir=MODULE.parent, prefix=".card-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.game = self.root / "game"
        self.game.mkdir()
        self.asset("example")
        self.out = self.root / "cards"

    def asset(self, hero, prefix="heroes"):
        folder = self.game / prefix / hero
        (folder / f"{hero}_A").mkdir(parents=True)
        Image.new("RGB", (120, 120), (80, 35, 15)).save(
            folder / f"{hero}_A" / f"{hero}_portrait_roster.png")
        Image.new("RGB", (72, 72), (110, 70, 20)).save(folder / f"{hero}.ability.one.png")
        return folder

    def render(self, data=None, **kwargs):
        return cards.render_cards(data or sample(), self.game, self.out, **kwargs)

    def test_single_page_manifest_and_lossless_png(self):
        data = sample()
        original = copy.deepcopy(data)
        result = self.render(data)
        self.assertEqual(data, original)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertEqual((item["hero"], item["page"], item["pages"]), ("example", 1, 1))
        self.assertEqual(item["path"], "01_example.png")
        self.assertEqual(item["skill_keys"], ["example|skill_0"])
        raw = (self.out / item["path"]).read_bytes()
        self.assertEqual(item["size"], len(raw))
        self.assertLess(len(raw), 1_000_000)
        self.assertEqual(item["sha256"], hashlib.sha256(raw).hexdigest())
        with Image.open(self.out / item["path"]) as im:
            self.assertEqual(im.format, "PNG")
            self.assertEqual(im.mode, "RGB")
            self.assertEqual(im.size, (1200, item["height"]))
            self.assertEqual(item["width"], 1200)
            self.assertEqual(im.getpixel((70, 70)), (80, 35, 15))

    def test_committed_skill_icon_overrides_vanilla_without_changing_it(self):
        folder = self.game / 'heroes/example'
        original = (folder/'example.ability.one.png').read_bytes()
        mod = self.root/'source'
        custom = mod/'heroes/example/example.ability.one.png'
        custom.parent.mkdir(parents=True)
        Image.new('RGB',(72,72),(5,99,201)).save(custom)
        art = cards._skill_art(folder,self.game,'example','one',mod)
        self.assertEqual(art.getpixel((30,30)),(5,99,201))
        self.assertEqual((folder/'example.ability.one.png').read_bytes(),original)
        self.assertEqual(cards._skill_art(folder,self.game,'example','one').getpixel((30,30)),(110,70,20))

    def test_requested_steam_cards_split_even_under_height_cap(self):
        for hero in cards.TWO_PAGE_HEROES:
            self.asset(hero)
            self.out = self.root / hero
            data = sample(hero, count=4)
            result = self.render(data)
            self.assertEqual([p['pages'] for p in result], [2, 2])
            self.assertEqual([k for p in result for k in p['skill_keys']],
                             [s['key'] for s in data[hero]['skills']])

    def test_height_boundary_and_balanced_split_preserve_every_drawn_row(self):
        data = sample(count=4, rows=2)
        full = self.render(data)[0]["height"]
        self.out = self.root / "exact"
        self.assertEqual(len(self.render(data, max_height=full)), 1)
        self.out = self.root / "split"
        calls = []
        real_text = ImageDraw.ImageDraw.text

        def record(draw, xy, text, *args, **kwargs):
            calls.append((text, kwargs.get("font")))
            return real_text(draw, xy, text, *args, **kwargs)

        with patch.object(ImageDraw.ImageDraw, "text", record):
            manifest = self.render(data, max_height=full - 1)
        self.assertEqual([m["path"] for m in manifest], ["01_example_p1.png", "01_example_p2.png"])
        self.assertEqual([m["pages"] for m in manifest], [2, 2])
        self.assertEqual([len(m["skill_keys"]) for m in manifest], [2, 2])
        self.assertEqual(manifest[0]["height"], manifest[1]["height"])
        self.assertEqual([k for m in manifest for k in m["skill_keys"]],
                         [s["key"] for s in data["example"]["skills"]])
        rendered = Counter(t for t, _ in calls)
        for skill in data["example"]["skills"]:
            for row in skill["old"] + skill["new"]:
                self.assertEqual(rendered[row], 1)
        for label in ["Example Hero", "Every skill stays readable.", "VANILLA", "REBALANCE"]:
            self.assertEqual(rendered[label], 2)
        self.assertEqual(rendered["Part 1/2"], 1)
        self.assertEqual(rendered["Part 2/2"], 1)
        self.assertEqual({font.size for text, font in calls if text.startswith(("Old-", "New-"))}, {25})

    def test_long_words_titles_taglines_and_rows_fit_without_shrinking(self):
        data = sample()
        data["example"]["name"] = "Extraordinary" * 9
        data["example"]["tagline"] = "Unbreakable" * 30
        skill = data["example"]["skills"][0]
        skill["name"] = "SkillTitle" * 30
        skill["old"] = ["W" * 65, "First line\nSecond line"]
        skill["new"] = ["Ágj" * 45]
        seen = []
        real_text = ImageDraw.ImageDraw.text

        def record(draw, xy, text, *args, **kwargs):
            font = kwargs["font"]
            bbox = draw.textbbox(xy, text, font=font)
            seen.append((font.size, text, bbox))
            self.assertGreaterEqual(bbox[0], 0)
            self.assertLessEqual(bbox[2], 1160)
            self.assertGreaterEqual(bbox[1], 0)
            self.assertLessEqual(bbox[3], draw._image.height)
            if font.size == 25:
                self.assertLessEqual(bbox[2], 640 if xy[0] < 700 else 1140)
            return real_text(draw, xy, text, *args, **kwargs)

        with patch.object(ImageDraw.ImageDraw, "text", record):
            self.render(data, max_height=4000)
        for size, source in [(56, data["example"]["name"]), (28, data["example"]["tagline"]),
                             (30, skill["name"])]:
            actual = "".join(t for sz, t, _ in seen if sz == size)
            self.assertEqual("".join(actual.split()), "".join(source.split()))
        actual = "".join(t for sz, t, _ in seen if sz == 25)
        self.assertEqual("".join(actual.split()), "".join("".join(skill["old"] + skill["new"]).split()))
        # Baselines must also keep tall/accented glyphs vertically separated.
        for size in [56, 28, 30]:
            boxes = [b for sz, _, b in seen if sz == size]
            for a, b in zip(boxes, boxes[1:]):
                self.assertLess(a[3], b[1])

    def record_rows(self, data):
        calls = []
        real_text = ImageDraw.ImageDraw.text

        def record(draw, xy, text, *args, **kwargs):
            if kwargs["font"].size == 25:
                calls.append((xy[0], xy[1], text))
            return real_text(draw, xy, text, *args, **kwargs)

        with patch.object(ImageDraw.ImageDraw, "text", record):
            manifest = self.render(data)
        return manifest, calls

    def test_followup_pairs_align_after_either_side_wraps(self):
        for swap in (False, True):
            with self.subTest(swap=swap):
                self.out = self.root / f"paired-{swap}"
                data = sample()
                skill = data["example"]["skills"][0]
                # Opposing wraps must accumulate padding per original pair,
                # not merely equalize the final column lengths.
                left = ["W" * 65, "Left second", "Left final"]
                right = ["Right first", "Right second\nRight continuation", "Right final"]
                skill["old"], skill["new"] = (right, left) if swap else (left, right)
                manifest, calls = self.record_rows(data)
                positions = {text: y for _, y, text in calls if text}
                self.assertEqual(positions["Left second"], positions["Right second"])
                self.assertEqual(positions["Left final"], positions["Right final"])
                self.assertGreater(positions["Left second"], positions["Right first"])
                self.assertEqual(positions["Left final"] - positions["Left second"], 68)
                for x, side in [(210, "old"), (710, "new")]:
                    rendered = "".join(t for xx, _, t in calls if xx == x)
                    self.assertEqual("".join(rendered.split()), "".join("".join(skill[side]).split()))
                self.assertEqual(manifest[0]["skill_keys"], [skill["key"]])

    def test_unequal_original_row_counts_pad_without_losing_tail_text(self):
        for longer_side in ("old", "new"):
            with self.subTest(longer_side=longer_side):
                self.out = self.root / f"unequal-{longer_side}"
                data = sample()
                skill = data["example"]["skills"][0]
                skill["old"] = ["Original first", "Original next"]
                skill["new"] = ["Changed first", "Changed next"]
                skill[longer_side] += ["Tail first\nTail continuation", "Tail final"]
                _, calls = self.record_rows(data)
                positions = {text: y for _, y, text in calls if text}
                self.assertEqual(positions["Original next"], positions["Changed next"])
                short_x = 710 if longer_side == "old" else 210
                for text in ["Tail first", "Tail continuation", "Tail final"]:
                    self.assertEqual(sum(t == text for _, _, t in calls), 1)
                    self.assertIn((short_x, positions[text], ""), calls)
                # Blank counterparts must not change the original 34px leading.
                self.assertEqual(positions["Tail final"] - positions["Tail first"], 68)

    def test_barbaric_yawp_use_limit_matches_use_limit_after_wrapping(self):
        data = sample()
        skill = data["example"]["skills"][0]
        skill["name"] = "Barbaric YAWP!"
        skill["old"] = ["Stuns ranks 1-2, chance 110-150%",
                        "Self: DMG -20%, SPD -3 (all battle)",
                        "No corpse clearing", "3 uses per battle"]
        skill["new"] = ["Self: ACC +5-10%, DMG +20-30%",
                        "All enemies: DMG -10 to -20% (3 turns)",
                        "Clears corpses", "No use limit"]
        _, calls = self.record_rows(data)
        positions = {text: y for _, y, text in calls if text}
        self.assertEqual(positions["No corpse clearing"], positions["Clears corpses"])
        self.assertEqual(positions["3 uses per battle"], positions["No use limit"])
        self.assertEqual(positions["3 uses per battle"] - positions["Clears corpses"], 34)

    def test_oversized_skill_and_three_page_content_fail_without_output(self):
        for data, limit in [(sample(rows=80), 1500), (sample(count=12, rows=4), 800)]:
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "example"):
                self.render(data, max_height=limit)
            self.assertFalse(self.out.exists())

    def test_nonuniform_blocks_use_optimal_boundary_and_exact_minimum(self):
        data = sample(count=5)
        data["example"]["skills"][0]["old"] = [f"Tall row {i}" for i in range(7)]
        # Original metrics: overhead 310, seven rows 302, one row 98.
        # Splitting 1|4 gives 612/702; splitting by skill count gives 710/604.
        result = self.render(data, max_height=702)
        self.assertEqual([m["height"] for m in result], [612, 702])
        self.assertEqual([len(m["skill_keys"]) for m in result], [1, 4])
        self.out = self.root / "one_pixel_too_short"
        with self.assertRaisesRegex(ValueError, "example.*702"):
            self.render(data, max_height=701)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.render(sample(), max_height=408)[0]["height"], 408)
        self.out = self.root / "individual_too_short"
        with self.assertRaisesRegex(ValueError, "example.*individual skill"):
            self.render(sample(), max_height=407)

    def test_identical_input_produces_identical_bytes_and_manifest(self):
        first = self.render(sample(count=5), max_height=700)
        self.out = self.root / "repeat"
        second = self.render(sample(count=5), max_height=700)
        self.assertEqual(first, second)

    def test_asset_symlink_escape_is_rejected(self):
        folder = self.game / "heroes" / "example"
        icon = folder / "example.ability.one.png"
        outside = self.root / "outside.png"
        icon.replace(outside)
        try:
            icon.symlink_to(outside)
        except OSError:
            self.skipTest("host does not permit creating symlinks")
        with self.assertRaisesRegex(ValueError, "example.*escapes game_root"):
            self.render()
        self.assertFalse(self.out.exists())

    def test_existing_output_is_never_reused_or_deleted(self):
        self.out.mkdir()
        marker = self.out / "user.png"
        marker.write_bytes(b"preserve me")
        with self.assertRaises(FileExistsError):
            self.render()
        self.assertEqual(marker.read_bytes(), b"preserve me")
        self.assertEqual(list(self.out.iterdir()), [marker])
        marker.unlink()
        with self.assertRaises(FileExistsError):
            self.render()

    def test_invalid_input_and_unsafe_paths_fail_before_writes(self):
        bad = [None, [], {}, {"example": None}, sample(count=0)]
        for field, value in [("name", ""), ("tagline", 42), ("skills", {})]:
            data = sample()
            data["example"][field] = value
            bad.append(data)
        for field, value in [("key", ""), ("old", "not a list"), ("new", []),
                             ("old", [None]), ("new", ["bad\x00text"]),
                             ("icon", "../../escape"), ("icon", "C:\\escape"),
                             ("name", "")]:
            data = sample()
            data["example"]["skills"][0][field] = value
            bad.append(data)
        duplicate = sample(count=2)
        duplicate["example"]["skills"][1]["key"] = "example|skill_0"
        bad.append(duplicate)
        for hero in ["../escape", "/absolute", "C:\\escape", "foo/bar", "foo\\bar", "CON", "foo:bar"]:
            bad.append(sample(hero))
        for data in bad:
            with self.subTest(data=data), self.assertRaises(ValueError):
                cards.render_cards(data, self.game, self.out)
            self.assertFalse(self.out.exists())
        for limit in [0, -1, True, 1.5, "1500", None]:
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                self.render(max_height=limit)
        with self.assertRaises(ValueError):
            cards.render_cards(sample(), self.game, self.game / "forbidden")
        self.assertFalse((self.game / "forbidden").exists())

    def test_showcase_first_dlc_lookup_and_missing_assets_fail_closed(self):
        self.asset("bounty_hunter", "dlc/example/heroes")
        self.asset("musketeer", "dlc/example/features/musketeer/heroes")
        data = sample() | sample("musketeer") | sample("bounty_hunter")
        result = self.render(data)
        self.assertEqual([m["hero"] for m in result], ["bounty_hunter", "example", "musketeer"])
        self.assertEqual([m["path"] for m in result],
                         ["01_bounty_hunter.png", "02_example.png", "03_musketeer.png"])
        self.out = self.root / "missing"
        with self.assertRaisesRegex(FileNotFoundError, "missing"):
            self.render(sample() | sample("missing"))
        self.assertFalse(self.out.exists())

    def test_png_limit_is_strict_and_does_not_publish_partial_batch(self):
        # Inject just the encoder boundary; all layout and Pillow drawing stay real.
        def oversized_save(image, fp, *args, **kwargs):
            fp.write(b"x" * 1_000_000)
        with patch.object(Image.Image, "save", oversized_save):
            with self.assertRaisesRegex(ValueError, "example.*1,?000,?000"):
                self.render()
        self.assertFalse(self.out.exists())

    def test_cli_outputs_json_manifest_and_refuses_existing_directory(self):
        source = self.root / "input.json"
        source.write_text(json.dumps(sample()), encoding="utf-8")
        command = [sys.executable, "-B", str(MODULE), "--input", str(source),
                   "--game-root", str(self.game), "--out", str(self.out), "--max-height", "1500"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["path"], "01_example.png")
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_installed_corpus_every_row_drawn_once_inside_its_panel(self):
        # Optional integration test: reads real input/art only, never writes to
        # the game. Override this path when running on another installation.
        game = Path(os.environ.get("DD_GAME_ROOT", "C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon"))
        source = game / "mods/Rebalance/design/workshop/hero_cards.json"
        if not source.is_file():
            self.skipTest("installed hero_cards.json unavailable")
        data = json.loads(source.read_text(encoding="utf-8-sig"))
        original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        row_text = []
        panels = {}
        real_rectangle, real_text = ImageDraw.ImageDraw.rectangle, ImageDraw.ImageDraw.text

        def rectangle(draw, xy, *args, **kwargs):
            if xy[0] == 40 and xy[2] == 1159:
                panels[id(draw)] = xy
            return real_rectangle(draw, xy, *args, **kwargs)

        def text(draw, xy, value, *args, **kwargs):
            font = kwargs["font"]
            if font.size == 25:
                row_text.append(value)
                bbox = draw.textbbox(xy, value, font=font)
                panel = panels[id(draw)]
                self.assertGreaterEqual(bbox[1], panel[1])
                self.assertLess(bbox[3], panel[3])
                self.assertGreaterEqual(bbox[0], 210 if xy[0] < 700 else 710)
                self.assertLessEqual(bbox[2], 640 if xy[0] < 700 else 1140)
            return real_text(draw, xy, value, *args, **kwargs)

        with patch.object(ImageDraw.ImageDraw, "rectangle", rectangle), patch.object(ImageDraw.ImageDraw, "text", text):
            result = cards.render_cards(data, game, self.out)
        order = (["bounty_hunter"] if "bounty_hunter" in data else []) + [h for h in data if h != "bounty_hunter"]
        expected = [row for h in order for s in data[h]["skills"] for side in ("old", "new") for row in s[side]]
        self.assertEqual("".join("".join(row_text).split()), "".join("".join(expected).split()))
        self.assertEqual([k for m in result for k in m["skill_keys"]],
                         [s["key"] for h in order for s in data[h]["skills"]])
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_hash)
        for item in result:
            self.assertLessEqual(item["height"], 1500)
            self.assertLessEqual(item["pages"], 2)
            self.assertLess(item["size"], 1_000_000)
            payload = (self.out / item["path"]).read_bytes()
            self.assertEqual(item["sha256"], hashlib.sha256(payload).hexdigest())
            with Image.open(self.out / item["path"]) as im:
                self.assertEqual(im.size, (1200, item["height"]))


if __name__ == "__main__":
    unittest.main()
