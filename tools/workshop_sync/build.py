"""WS-BUILD-001: reuse the approved builder in an isolated directory, with explicit game roots."""
import argparse
import importlib
import os
from pathlib import Path
import sys
import tempfile


def build(source, game_root, output):
    source, game_root, output = (Path(x).resolve() for x in (source, game_root, output))
    # Existing builder removes OUT first. Constrain it to a sibling of this job's source.
    if output.name != 'payload' or output.parent != source.parent or source.name != 'source':
        raise ValueError('Build output must be the isolated job/payload next to job/source')
    if output.is_symlink() or output == game_root or game_root in output.parents or source == game_root:
        raise ValueError('Build output must not be inside the installed game')
    temp = source.parent / 'tmp'
    temp.mkdir(exist_ok=True)
    tempfile.tempdir = str(temp)
    os.environ['TEMP'] = os.environ['TMP'] = str(temp)
    sys.path.insert(0, str(source / 'tools'))
    ec = importlib.import_module('effect_common')
    ec.paths = lambda mod_root=None, game_root_arg=None: (str(mod_root or source), str(game_root_arg or game_root))
    builder = importlib.import_module('build_workshop')
    builder.G = str(game_root)
    builder.OUT = str(output)
    builder.S.G = builder.PN.G = str(game_root)
    builder.S.M_ROOT = str(source)
    loc = importlib.import_module('make_loc')
    loc.M, loc.G = str(source), str(game_root)
    # No apply_effect_edits: only committed runtime values are packaged.
    builder.main()
    return output


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--game-root', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    build(args.source, args.game_root, args.output)
