# Rebalance 작업 안내

## 폴더

```
mods/Rebalance/
  heroes/<영웅>/<영웅>.info.darkest   ← 수정하는 파일 (게임이 읽음)
  heroes/<영웅>/<영웅>.vanilla.txt    ← 바닐라 참고 시트 (게임이 안 읽음, 배포 제외)
  design/
    intent.md        기획 의도·목표(G-xx)·수정 원칙(P-xx)
    rules.md         원본 수치 규칙(R-xx) + 원칙 이탈 목록
    analysis/        근거 자료 (회복 분석, DLC 패치 이력 …)
    changes/<영웅>.md 영웅별 변경 항목
    vanilla/         총사 바닐라 시트 (총사는 모드에서 제외 중)
  tools/make_modfiles.py   파일 목록(modfiles.txt) 다시 만들기
  project.xml / preview_icon.png   모드 목록·창작마당 정보
```

## 수정 절차

1. `heroes/<영웅>/<영웅>.info.darkest`를 메모장으로 고친다. 바닐라 수치는 같은 폴더의 `.vanilla.txt`에서 본다.
2. 바꾼 줄 바로 밑에 `// <항목 ID>` 한 줄을 넣는다. 예: `// MAA-002`
3. `design/changes/<영웅>.md`에 항목을 추가한다.
   - 최소한 **제목, 목표, 의도, 근거**만 적으면 된다. 원본값·변경값·원칙 대조는 점검 때 채운다.
   - 해보고 접은 안도 지우지 말고 `상태: 기각`으로 남긴다.
4. GitHub Desktop에서 커밋한다. 커밋 메시지 첫 줄에 항목 ID를 넣는다. 예: `MAA-002 응징 피해 보정 조정`
5. 새 파일(효과 파일 등)을 모드에 추가했으면 `python tools/make_modfiles.py`를 실행하거나 Claude에게 요청한다.

- 기술 효과 수치는 영웅 파일이 아니라 `effects/*.effects.darkest`에 있다. 효과를 바꾸려면 해당 효과 파일을 모드에 복사해야 하니 요청할 것.
- 기술 ID(`.id "..."`)는 바꾸거나 지우지 않는다(P-04, 세이브 호환).

## 항목 ID

`<영웅 약어>-<세 자리 번호>`. 여러 영웅에 걸친 공통 변경은 `SYS`.

| 약어 | 영웅 | 약어 | 영웅 |
|---|---|---|---|
| ABO | 괴인 | HWY | 노상강도 |
| ANT | 유물수집상 | HM | 조련사 |
| ARB | 석궁사수 | JES | 광대 |
| BH | 현상금 사냥꾼 | LEP | 나병환자 |
| CRU | 성전사 | MAA | 중보병 |
| DUE | 결투가 | MUS | 총사 |
| FLA | 고행자 | OCC | 신비학자 |
| GR | 도굴꾼 | PD | 역병 의사 |
| HEL | 야만인 | RUN | 도망자 |
| SB | 방패 파괴자 | VES | 성녀 |

## 항목 틀

```
### MAA-002 제목
- 상태: 적용 / 보류 / 기각
- 분류: 원칙복원 / 신규규칙 / 의도적예외
- 목표: G-0x
- 의도:
- 근거:
- 따르는 원칙: R-...
- 어기는 원칙: 없음 (있으면 이유)
- 영향: 다른 항목·영웅에 미치는 영향
- 변경: (점검 때 채워도 됨)
- 검증: (플레이 후 기록)
```

## GitHub Desktop 연결

File → Add local repository → `C:\Program Files (x86)\Steam\steamapps\common\DarkestDungeon\mods\Rebalance`

## 일관성 점검 / 배포

- 점검: 전체 조정 후 또는 중간에 요청. 원본 대비 변경, 항목 누락, 원칙 위반, 항목 간 충돌을 보고서로 만든다.
- 배포: 요청 시 원본과 다른 파일만 담은 업로드 폴더 + changes.txt + 창작마당 설명을 만든다.
