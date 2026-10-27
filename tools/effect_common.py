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
EFFECT_LIST = re.compile(r'(\.(?:effects?|human_effects|beast_effects|battle_start_effect_ids|stance_defensive_effects|stance_aggressive_effects|enter_effects))((?:\s+(?:"[^"]*"|(?!\.)[^\s"]+))+)')
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
                # SYS-103: vanilla reaction effects may use unquoted names too.
                m = re.search(r'\.name\s+(?:"([^"]+)"|(\S+))', raw)
                name = (m.group(1) or m.group(2)) if m else None
                if name and name not in eff:
                    eff[name] = (raw.rstrip('\r\n'), P(os.path.relpath(f, G)))
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
    # A transform skill carries both human and beast effect lists on the same line.
    return [a if a or not b else b
            for m in EFFECT_LIST.finditer(line)
            for a, b in EFFECT_TOKEN.findall(m.group(2))]


def load_buffs(G, mod_root=None):
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
    if mod_root:
        for f in sorted(glob.glob(os.path.join(mod_root, 'shared', 'buffs', '*.json'))):
            for o in walk(json.load(open(f, encoding='utf-8-sig'))):
                if 'id' in o and 'stat_sub_type' in o:
                    buffs[o['id']] = o
    return buffs


def imported_hero(M, hero):
    """MUS-001: pinned upstream baseline, separate from shared vanilla definitions."""
    f = os.path.join(M, 'design', 'imports', hero, 'manifest.json')
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None


def edit_effect_baseline(M, G, hero):
    effects = load_vanilla_effects(G)
    imported = imported_hero(M, hero)
    if imported:
        for raw in open(os.path.join(M, imported['effect_baseline']), encoding='utf-8'):
            if raw.startswith('effect:'):
                name = re.search(r'\.name\s+"([^"]+)"', raw)[1]
                if name in effects and norm_ws(effects[name][0]) != norm_ws(raw):
                    raise ValueError('Imported effect collides with vanilla: ' + name)
                effects[name] = (raw.rstrip('\r\n'), imported['effect_baseline'])
    return effects


def edit_hero_baseline(M, G, hero):
    imported = imported_hero(M, hero)
    return os.path.join(M, imported['hero_baseline']) if imported else vanilla_hero_file(G, hero)


def load_edit_korean(M, G):
    ko = load_korean(G)
    for f in sorted(glob.glob(os.path.join(M, 'localization', '*.string_table.xml'))):
        t = open(f, encoding='utf-8').read()
        m = re.search(r'<language id="koreana">(.*?)</language>', t, re.S)
        if m:
            ko.update(dict(re.findall(r'<entry id="([^"]*)"><!\[CDATA\[(.*?)\]\]></entry>', m[1], re.S)))
    return ko


def effect_sig(line):
    """SYS-104: compare complete field values, including lists and decimals.

    Field order and the effect name are irrelevant. Value order and every token
    remain significant: sharing just the first buff is not semantic equality.
    """
    body = re.sub(r'^\s*effect:\s*', '', line.strip())
    tokens = re.findall(r'"[^"\n]*"|\.[A-Za-z_]\w*|[^\s"]+', body)
    fields, key, values = [], None, []
    for token in tokens:
        if re.fullmatch(r'\.[A-Za-z_]\w*', token):
            if key is not None and key != 'name':
                fields.append((key, tuple(values)))
            key, values = token[1:], []
        else:
            values.append(token)
    if key is not None and key != 'name':
        fields.append((key, tuple(values)))
    return frozenset(fields)


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
