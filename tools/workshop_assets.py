"""WS-ASSET-001: package committed skill icons omitted by the older builder."""
from pathlib import Path
import re
import shutil

def copy_skill_icons(hero_folder, output_folder, hero):
    source, output = Path(hero_folder).resolve(), Path(output_folder)
    copied = []
    for icon in sorted(source.glob(f'{hero}.ability.*.png')):
        if not re.fullmatch(re.escape(hero)+r'\.ability\.(one|two|three|four|five|six|seven)\.png',icon.name):
            continue
        if icon.is_symlink() or icon.resolve().parent != source:
            raise ValueError('Skill icon must be a regular file in the hero folder')
        output.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(icon,output/icon.name)
        copied.append(icon.name)
    return copied
