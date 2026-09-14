"""Regenerate modfiles.txt ("path size" per line, same format as Workshop mods).

Lists only files the game should load: game data folders + project.xml + preview_icon.png.
Excluded: .git, design/, tools/, *.vanilla.txt, *.md, modfiles.txt itself is appended last.
Run:  python tools/make_modfiles.py   (from anywhere)
"""
import os

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'design', 'tools'}
SKIP_ROOT_FILES = {'modfiles.txt', '.gitignore', '.gitattributes'}

entries = []
for root, dirs, files in os.walk(M):
    rel_root = os.path.relpath(root, M).replace('\\', '/')
    if rel_root == '.':
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        rel = f if rel_root == '.' else f'{rel_root}/{f}'
        if rel_root == '.' and (f in SKIP_ROOT_FILES or f.endswith('.md')):
            continue
        if f.endswith('.vanilla.txt') or f.endswith('.md'):
            continue
        entries.append(f'{rel} {os.path.getsize(os.path.join(M, rel))}')

entries.sort()
body = '\n'.join(entries)
size = 0
for _ in range(5):
    size = len((body + f'\nmodfiles.txt {size}').encode('utf-8'))
with open(os.path.join(M, 'modfiles.txt'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(body + f'\nmodfiles.txt {size}')
print(f'modfiles.txt: {len(entries)} files + itself')
