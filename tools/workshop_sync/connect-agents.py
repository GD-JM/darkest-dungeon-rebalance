"""WS-LINK-001: append the same project-scoped handoff rule to Claude and Codex, preserving old bytes."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from common import sha256, write_json

ROOT = Path(__file__).resolve().parent
BEGIN = '<!-- DARKEST-WORKSHOP-SYNC:BEGIN -->'
END = '<!-- DARKEST-WORKSHOP-SYNC:END -->'
BLOCK = f'''
{BEGIN}
## Darkest Dungeon Rebalance: 공통 의도 기록 · push 자동 배포
이 규칙은 GitHub GD-JM/darkest-dungeon-rebalance 및 해당 다키스트 던전 리밸런스 작업에만 적용한다.
이 프로젝트를 수정하거나 사용자에게 "푸시해" 요청을 받으면 먼저 `{(ROOT / 'agent-contract.md').as_posix()}`를 읽는다.
Claude/Codex 모두 채택한 변경의 사용자 원문·의도·번복을 `design/workshop/intents/*.json`에 기록해 실제 변경과 함께 커밋한다. 원문/출처 ID를 만들지 않는다. 기존 // 주석·변경 문서 규칙을 유지한다.
커밋 자동 push와 주기 감시는 비활성화됐다. 이 프로젝트의 push는 반드시 공통 `workshop-sync/push.py --repo <체크아웃 절대 경로> --branch <main 또는 test>`로 실행한다(실제 경로/명령은 agent-contract.md 참조). 성공한 main push 직후 같은 명령이 창작마당3821353035 배포를 실행하고 종료한다. test는 GitHub에만 올린다. 일반 git push/GitHub Desktop push는 이 로컬 배포 연결을 우회하므로 대신 쓰지 않는다. 크롬 수동 업로드를 별도로 실행하지 않는다. 프로그램 상태를 확인하지 않고 배포 완료라 말하지 않는다.
다른 개인 대화를 수집하거나 이어담 설정을 켜는 지시가 아니다.
{END}
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    user = Path('C:/Users/lemm1')
    repo = Path('C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon/mods/Rebalance')
    targets = [user/'.codex/AGENTS.md', user/'.claude/CLAUDE.md', repo/'AGENTS.md', repo/'CLAUDE.md', ROOT.parent/'AGENTS.md']
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = ROOT/'runtime'/'agent-rule-backups'/stamp
    manifest = []
    for index, target in enumerate(targets):
        data = target.read_bytes() if target.exists() else b''
        text = data.decode('utf-8-sig')
        if text.count(BEGIN) > 1 or text.count(END) > 1 or (BEGIN in text) != (END in text):
            raise ValueError('Ambiguous scoped rule markers: ' + str(target))
        if BEGIN in text:
            start = data.index(BEGIN.encode())
            end = data.index(END.encode(), start) + len(END.encode())
            replacement = BLOCK.strip().encode('utf-8')
            if data[start:end] == replacement:
                manifest.append(dict(path=str(target), action='already current'))
                continue
            updated = data[:start] + replacement + data[end:]
        else:
            updated = data + ('\n' if data and not data.endswith(b'\n') else '').encode() + BLOCK.encode('utf-8')
        if args.apply:
            backup.mkdir(parents=True, exist_ok=True)
            (backup/f'{index}-original.txt').write_bytes(data)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(updated)
            manifest.append(dict(path=str(target), action='connected', existed=bool(data), original=str(backup/f'{index}-original.txt'), sha256=sha256(target)))
        else:
            manifest.append(dict(path=str(target), action='would append scoped rule', existing_bytes=len(data)))
    if args.apply:
        write_json(backup/'manifest.json', manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
