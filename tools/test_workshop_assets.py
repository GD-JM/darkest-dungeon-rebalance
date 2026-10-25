import tempfile, unittest
from pathlib import Path
from workshop_assets import copy_skill_icons

class WorkshopAssetTests(unittest.TestCase):
    def test_only_runtime_skill_icons_are_copied_byte_exact(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/'src'; src.mkdir(); out=root/'out'
            for name in ['leper.ability.seven.png','leper.ability.seven-original.png','other.ability.one.png','draft.png']:
                (src/name).write_bytes(b'approved icon bytes')
            self.assertEqual(copy_skill_icons(src,out,'leper'),['leper.ability.seven.png'])
            self.assertEqual((out/'leper.ability.seven.png').read_bytes(),(src/'leper.ability.seven.png').read_bytes())
            self.assertEqual(len(list(out.iterdir())),1)
