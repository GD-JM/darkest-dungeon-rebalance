"""Shared helpers for the effect edit workflow (vanilla effects, hero skills, names)."""
import os, re, glob, json
from collections import defaultdict

ABBR = dict(abomination='ABO', antiquarian='ANT', arbalest='ARB', bounty_hunter='BH', crusader='CRU', duelist='DUE',
            flagellant='FLA', grave_robber='GR', hellion='HEL', highwayman='HWY', houndmaster='HM', jester='JES',
            leper='LEP', man_at_arms='MAA', musketeer='MUS', occultist='OCC', plague_doctor='PD', runaway='RUN',
            shieldbreaker='SB', vestal='VES')

P = lambda p: p.replace('\\', '/')
norm_ws = lambda s: re.sub(r'\s+', ' ', s.strip())
# effect names are usually quoted, but some vanilla lines use bare names (duelist: .effect duelist_riposte)
EFFECT_LIST = re.compile(r'(\.effects?)((?:\s+(?:"[^"]*"|(?!\.)[^\s"]+))+)')
EFFECT_TOKEN = re.compile(r'"([^"]*)"|([^\s"]+)')


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
    return [a if a or not b else b for a, b in EFFECT_TOKEN.findall(m.group(2))] if m else []


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


def effect_sig(line):
    """Name-independent signature of an effect line: frozenset of (key, value).

    Two effects with the same signature are functionally identical, so one can be
    reused instead of creating a duplicate "RB ..." copy (rules.md R-DATA-01).
    """
    body = re.sub(r'^\s*effect:\s*', '', line.strip())
    m = re.search(r'\.name\s*"[^"]*"', body)
    if m:
        body = body[:m.start()] + ' ' + body[m.end():]
    return frozenset(re.findall(r'\.(\w+)\s*((?:"[^"]*"|[^\s.]+)?)', body))


FAMILY = lambda nm: re.sub(r'\s*\d+$', '', nm).strip()


def _tier(nm):
    """('Hero Strong Stun 5') -> ('Hero Strong Stun', '5'); ('Stacking Heal') -> ('Stacking Heal', '')."""
    m = re.match(r'^(.*?)\s*(\d*)$', nm.strip())
    return m.group(1).strip(), m.group(2)


def reuse_candidate(name, line, eff, index):
    """An existing vanilla effect identical to `line`, or None.

    Only ONE relation is accepted: the candidate is the plainer tier of the SAME
    effect at the SAME level - its family is a trailing part of this one and the
    level number is identical.
        "Hero Strong Stun 5" -> "Stun 5"        (110->140 becomes the plain tier)
        "GR Blight 1"        -> "Blight 1"
    Also accepted: the same effect at another level, when a value was flattened across
    levels ("HM Dmg Marked 3" -> "HM Dmg Marked 1"). The caller must refuse any target
    that is itself edited, otherwise editing that level later would silently move this
    one too - references are matched by name, not by level.
    Rejected: an unrelated hero's or a monster's effect, which would create hidden coupling.
    Ties break on fewest words, then alphabetically.
    """
    fam, lvl = _tier(name)
    best = []
    for cand in index.get(effect_sig(line), ()):
        if cand == name or cand.startswith('RB '):
            continue
        cfam, clvl = _tier(cand)
        if cfam == fam:
            rank = 1          # same effect, another level: "HM Dmg Marked 3" -> "HM Dmg Marked 1"
        elif clvl == lvl and fam.endswith(' ' + cfam):
            rank = 0          # plainer tier, same level: "Hero Strong Stun 5" -> "Stun 5"
        else:
            continue
        best.append((rank, len(cand.split()), cand))
    return min(best)[2] if best else None


def vanilla_index(eff):
    """signature -> [names], for reuse_candidate."""
    idx = defaultdict(list)
    for nm, (line, _src) in eff.items():
        idx[effect_sig(line)].append(nm)
    return idx
