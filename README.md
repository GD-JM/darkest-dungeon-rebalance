# 전 영웅 리밸런스 (Every Hero Worth Taking) — Darkest Dungeon

다키스트 던전 20명 영웅을 한 규칙으로 함께 맞춘 밸런스 모드와, 그 설계 기록 전체입니다.

- 스팀 창작마당: https://steamcommunity.com/sharedfiles/filedetails/?id=3821353035
- 목표: "이 영웅 없으면 못 깬다"는 조합(성녀·신비학자·광대 의존)을 없애고, 영웅마다 기술·열 선택지를 늘린다. 게임 전체 난이도는 그대로.

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `heroes/`, `effects/`, `shared/`, `localization/` | 게임이 읽는 모드 데이터. 바뀐 줄마다 아래에 `// 변경ID 의도` 주석 |
| `design/changes/<영웅>.md` | 변경 ID별 기록: 원래 값, 바꾼 값, 의도, 근거, 제작자 결정 |
| `design/rules.md`, `design/intent.md` | 설계 원칙과 수치 규칙, 게임에서 확인할 항목(V-) |
| `design/analysis/` | 전수 조사·분석 표 (목록: `design/analysis/INDEX.md`) |
| `design/workshop/` | 창작마당 설명문(10개 언어)·영웅 카드·패치 노트 |
| `tools/` | 강함 모델(`strength.py`), 창작마당 빌드, 효과 편집·주석 검사 도구 |

## 작업 방식

- `main` = 창작마당에 올라가는 판. `test` = 실험(게임에서 직접 확인한 뒤 main에 합친다).
- 수치 결정은 제작자가 하고, 조사·계산·자동화·기록은 AI(Claude)와 협업했다. 커밋 메시지의 변경 ID로 `design/changes`의 근거를 찾을 수 있다.
