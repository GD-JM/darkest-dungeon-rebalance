"""Shared helpers for the effect edit workflow (vanilla effects, hero skills, names)."""
import os, re, glob, json
from collections import defaultdict

ABBR = dict(abomination='ABO', antiquarian='ANT', arbalest='ARB', bounty_hunter='BH', crusader='CRU', duelist='DUE',
            flagellant='FLA', grave_robber='GR', hellion='HEL', highwayman='HWY', houndmaster='HM', jester='JES',
            leper='LEP', man_at_arms='MAA', musketeer='MUS', occultist='OCC', plague_doctor='PD', runaway='RUN',
            shieldbreaker='SB', vestal='VES')

P = lambda p: p.replace('\\', '/')
norm_ws = lambda s: re.sub(r'\s+', ' ', s.strip())
EFFECT_LIST = re.compile(r'(\.effects?)((?:\s+"[^"]*")+)')


def paths(mod_root=None, game_root=None):
    mod_root = os.path.abspath(mod_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    game_root = os.path.abspath(game_root or os.path.join(mod_root, '..', '..'))
    return mod_root, game_root


def effect_files(G):
    files = sorted(glob.glob(os.path.join(G, 'effects', '*.effects.darkest')))
    files += sorted(glob.glob(os.path.join(G, 'dlc', '**', '*.effects.darkest'), recursive=True))
    return [f for f in files if '/modes/' not in P(f) and 'arena_mp' not in P(f)]


def load_vanilla_effects(G):
    """name -> (raw line without newline, relative source path). First definition wins (base first)."""
    eff = {}
    for f in effect_files(G):
        for raw in open(f, encoding='utf-8', errors='replace'):
            if raw.startswith('effect:'):
                m = re.search(r'\.name\s+"([^"]+)"', raw)
                if m and m.group(1) not in eff:
                    eff[m.group(1)] = (raw.rstrip('\r\n'), P(os.path.relpath(f, G)))
    return eff


def load_korean(G):
    ko = {}
    for f in glob.glob(os.path.join(G, 'localization', '*.string_table.xml')) + \
             glob.glob(os.path.join(G, 'dlc', '**', 'localization', '*.string_table.xml'), recursive=True):
        if 'arena' in P(f):
            continue
        t = open(f, encoding='utf-8', errors='replace').read()
        m = re.search(r'<language id="koreana">(.*?)</language>', t, re.S)
        if m:
            for i, v in re.findall(r'<entry id="([^"]*)"><!\[CDATA\[(.*?)\]\]></entry>', m.group(1), re.S):
                ko.setdefault(i, v)
    return ko


def vanilla_hero_file(G, hero):
    for f in [os.path.join(G, 'heroes', hero, hero + '.info원본.darkest')] + \
             glob.glob(os.path.join(G, 'dlc', '**', 'heroes', hero, hero + '.info원본.darkest'), recursive=True):
        if os.path.exists(f) and 'arena' not in P(f):
            return f
    raise FileNotFoundError(hero)


def effect_names_in(line):
    m = EFFECT_LIST.search(line)
    return re.findall(r'"([^"]*)"', m.group(2)) if m else []


def load_buffs(G):
    def walk(o):
        if isinstance(o, dict):
            yield o
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)
    buffs = {}
    for f in glob.glob(os.path.join(G, 'shared', 'buffs', '*.json')) + glob.glob(os.path.join(G, 'dlc', '**', 'buffs', '*.json'), recursive=True):
        if 'arena' in P(f):
            continue
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for o in walk(d):
            if 'id' in o and 'stat_sub_type' in o:
                buffs.setdefault(o['id'], o)
    return buffs
