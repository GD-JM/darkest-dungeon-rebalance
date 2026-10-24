# Claude Code · Codex 공통: Rebalance 의도 기록과 push 배포

적용 저장소: `https://github.com/GD-JM/darkest-dungeon-rebalance.git`.
게임 설치본: `C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon/mods/Rebalance`.
배포 대상은 기존 전체 DLC판 `3821353035`와 `design/workshop/modules.json`에 고정 등록한 선택형 6개 항목이다. 2026-10-24 사용자 원문 "별도 선택형 패키지 제공 허용"으로 본편 15영웅판 및 결투가·도망자·고행자·방패 파괴자·총사 패치 추가를 승인했다. 기존 전체판은 유지하며 선택형과 함께 활성화하지 않는다. 새 항목을 더 만들 권한은 포함하지 않는다.

사용자는 2026-10-23 이 PC의 공통 푸시 명령이 성공하면 즉시 기존 창작마당을 갱신하도록 승인했다. 커밋/병합 자동 push 훅과 60초 감시는 해제됐다. main만 공개 게시하며 test는 GitHub에만 올린다. 이 명령 외의 일반 git push나 GitHub Desktop push는 배포를 실행하지 않는다.

## 변경을 채택할 때 반드시 기록

1. 사용자 원문은 그대로 보존한다. 수치/기능을 바꾸는 이유, 원하는 장단점, 제약, 비교 대상, 기존안 번복 이유를 분리해 적는다. 제안과 채택을 섞지 않는다.
2. 원래 프로젝트의 `// ID + 의도`와 `design/changes/<hero>.md` 규칙을 계속 따른다. `why.json`과 카드 기록도 최신 승인과 일치하게 유지한다.
3. **커밋 전에** `design/workshop/intents/<고유이름>.json`에 다음 형식의 기록을 추가한다. 여러 결정이면 배열도 가능하다.

```json
{
  "id": "실제 변경 ID 또는 새 고유 결정 ID",
  "decision": "adopted",
  "original_quote": "이번 변경을 승인한 사용자의 정확한 원문",
  "rationale_ko": "원문에 근거한 의도와 트레이드오프. 원문에서 확인되지 않은 추정은 따로 표시",
  "source": {
    "product": "claude",
    "reference": "실제 세션/메시지 위치 또는 사용자 메모 파일과 줄",
    "session_id": null,
    "message_id": null,
    "event_id": null
  },
  "files": ["heroes/실제영웅/실제파일.info.darkest", "effects/실제효과.effects.darkest"],
  "supersedes": []
}
```

실제 생성 시 예시 문구를 남기지 않는다. `source.product`는 claude/codex/user-file 중 실제 출처를 쓴다. 모르는 ID는 null로 남기고 실제 원문을 찾을 수 있는 reference를 적는다. 이어담에서 아직 수집되지 않은 eventId를 만들지 않는다. 원문이 확인되지 않으면 adopted로 꾸며 쓰지 않는다.

"해봐", "그렇게 해"처럼 짧은 승인은 승인 대상이었던 직전 제안도 `context_quotes` 배열에 원문/화자/출처와 함께 연결한다. 사용자 원문 자체를 긴 의역으로 바꾸지 않는다. 앞뒤 맥락 없이 수치나 승인 범위를 추측하지 않는다.

`files`에는 이번 의도가 설명하는 **실제 변경된 게임 입력 파일과 게시 자료 원본**을 명시한다. why.json, hero_cards.json, 직접 편집한 설명·제목·대표 이미지도 포함한다. 와일드카드는 쓰지 않는다. 삭제된 파일도 포함한다. 기존 기록을 지우지 말고 새 기록의 supersedes로 번복을 연결한다. 원문 인용을 이유 요약으로 대체하지 않는다. 기록은 이번 push에 포함되어야 한다. description_built/patch_notes/loc2처럼 빌드가 다시 만드는 파생물만 달라졌다면 새 배포를 만들지 않는다.

## 공통 push 명령

Claude/Codex 모두 커밋을 마친 뒤 이 명령을 사용한다. `--repo`에는 실제 작업한 체크아웃 경로, `--branch`에는 승인된 대상 main 또는 test를 지정한다. 사용자 요청 없이 test 전체를 main으로 합치지 않는다.

```powershell
& 'C:/Users/lemm1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B 'C:/Users/lemm1/Documents/Codex/2026-10-04/new-chat-2/workshop-sync/push.py' --repo 'C:/Program Files (x86)/Steam/steamapps/common/DarkestDungeon/mods/Rebalance' --branch test
```

공개 배포는 main 체크아웃 경로와 `--branch main`을 사용한다. 명령은 정확한 커밋을 GitHub로 push하고 성공 후 main만 배포한다. 실패한 push로는 게시하지 않는다. 잠금으로 한 번에 하나씩 처리한다. 명령 종료까지 결과를 확인한다.

GitHub push는 성공했지만 Steam/Codex 단계가 실패했다면 push 성공과 배포 실패를 구분해 보고한다. 원인을 해결한 뒤 같은 명령을 다시 실행하면 새 커밋 없이 배포를 재시도한다. 성공한 SHA는 다시 게시하지 않는다. 이벤트·오류는 `runtime/events/` 및 `health.json`, 각 job의 `publish-state.json`에서 확인한다.

배포 의도 기록 없이 게임 수치만 push하면 배포를 중단한다. 실제 원문을 찾아 기록을 추가하고 다시 공통 명령으로 push한다. 원문을 꾸며 쓰지 않는다. 주기적인 네트워크 조회나 상주 감시 작업은 없다. PC/Steam이 준비되어야 실제 배포가 성공한다.

## 게시 자료

- 업데이트 노트: 마지막 성공 배포 → 이번 push. 영어+중국어 간체. 실제 변경과 이유.
- 영웅 이미지: 바닐라 → 현재 배포본의 누적 차이. 긴 카드는 기술 묶음 경계에서2장, 기존 글자 크기 유지. 2장에도 안 들어가면 게시 전에 오류를 알린다.
- 설명: 기존10개 언어를 동일 승인 내용으로 갱신한다.
- 데이터는 승인된 runtime 파일만 빌드한다. effects_edit 시트 후보를 자동 적용하지 않는다.
- 선택형 6개는 동일 main SHA에서 분리한다. 모든 패키지 파일 검증 후 선택형→전체판 순서로 게시하고 모두 끝나야 성공으로 기록한다. 각 패키지별 제출 기록을 보존하여 재시도에서 업데이트 노트를 중복 게시하지 않는다. 각 DLC 패치는 본편판과 해당 DLC 영웅 활성화가 필요하며 다른 DLC 패치를 요구하지 않는다. 파일 검증은 실제 게임 실행 검증이 아니다.
- 한 항목의 Steam 제출 거부·결과 미확정은 해당 항목에 남기고 다른 승인된 항목은 계속 처리한다. 검증·소유권 불일치는 전체 중단한다. 일부 성공은 `batch-state.json`에 따로 기록하며 전체 성공으로 승격하지 않는다. Steam 콘텐츠 검토 보류는 재생성·필터 우회로 해제하지 않고 정상 검토 결과를 기다린다.
- 배포 프로그램 추적 소스는 저장소 `tools/workshop_sync/`에 보존한다. 이 PC 실행본은 위 `workshop-sync/` 경로이며 변경 시 양쪽을 동기화한다. runtime·로그·설정·계정 정보는 저장소에 넣지 않는다.
- 자동 문안 작성은 게임 수치·밸런스 결정을 새로 만들 권한이 없다.
- 상태: `workshop-sync/runtime/state.json`, `health.json`, `worker.log`와 각 배포의 `release.json`/`publish-state.json`을 확인한다. 실제 완료가 확인되기 전 '게시 완료'라 말하지 않는다.
- 관련 없는 개인 대화를 수집하지 않는다. 이어담 on/off를 변경하지 않는다. 이 공통 계약은 각 도구가 현재 작업의 원문을 기록하도록 연결하며, 다른 앱의 대화 입력을 가로채지 않는다.
