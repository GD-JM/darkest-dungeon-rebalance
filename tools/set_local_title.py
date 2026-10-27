"""P-28: show which main build the local test mod is based on, in the in-game mod list title.
Title (test branch): "Rebalance Test [base 2.5.7 +13 main 32c03d6]"
  2.5.7   = last version published to the Workshop (workshop-sync runtime/state.json)
  +13     = main commits after that published commit (not yet on the Workshop)
  32c03d6 = main commit the test branch is built on (merge-base of test and main)
On main the title is "Rebalance Main [2.5.7 +13 32c03d6]". Only project.xml <Title> is changed.
Usage: python tools/set_local_title.py   (run after rebasing test onto main or switching branches)"""
import json, os, re, subprocess

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = 'C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync/runtime/state.json'


def git(*a):
    return subprocess.run(['git', *a], cwd=M, capture_output=True, text=True, encoding='utf-8').stdout.strip()


def published():
    try:
        st = json.load(open(STATE, encoding='utf-8'))
        return st['last_release']['version'], st['last_published_sha']
    except (OSError, KeyError, ValueError):
        notes = sorted(os.listdir(os.path.join(M, 'design', 'workshop', 'changenotes')))
        m = re.search(r'Update ([\d.]+)', open(os.path.join(M, 'design', 'workshop', 'changenotes', notes[-1]), encoding='utf-8').read())
        return (m.group(1) if m else '?'), None


ver, pub_sha = published()
branch = git('branch', '--show-current')
base = git('merge-base', 'HEAD', 'main') if branch != 'main' else git('rev-parse', 'HEAD')
ahead = git('rev-list', '--count', f'{pub_sha}..{base}') if pub_sha else '?'
short = base[:7]
title = f'Rebalance Test [base {ver} +{ahead} main {short}]' if branch != 'main' else f'Rebalance Main [{ver} +{ahead} {short}]'
p = os.path.join(M, 'project.xml')
s = open(p, encoding='utf-8', newline='').read()
s2 = re.sub(r'<Title>[^<]*</Title>', f'<Title>{title}</Title>', s, count=1)
open(p, 'w', encoding='utf-8', newline='').write(s2)
print(title)
