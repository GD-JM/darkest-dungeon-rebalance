20영웅 동일 조건 분석 보관 — 2026-11-02

사용자 요청: "커밋 하고 푸쉬하자". 직전 화톳불/광휘 커밋 및20영웅 분석을 이어서 보관하고 test에 푸시한다. 신규 밸런스안 채택이나 main 배포가 아니다.

분석 기준 게임 커밋: f7ab1577d3f35fd4e9f6393f6e0ec83fe90aaf7a.
all-heroes-20261102/review.md가 종합 보고서, skill-details.md가140기술 표다. JSON은 당시 계산 결과이며 문서의 미푸시 표기는 분석 시점의 상태다.

재현: 게임 설치본과 이 저장소의 tools가 필요하다. 이 폴더에서 Python으로 audit20-inspect.py → audit20-model.py → audit20-gear.py → audit20-extra.py → audit20-report.py → audit20-sets.py 순서로 실행한다. extra는 synergy를 함께 실행한다. 모델/게임 데이터를 다른 커밋으로 바꾸면 결과도 달라진다. 동일 원본 입력은 audit-validation.json의 해시로 확인한다.

공통 strength.py 자체의 추가 수정은 없으며, 시체 제외·화상 타이밍·기간 일치는 감사 실행의 보정이다. 장신구 전체 조합과 전투AI를 최적화한 시뮬레이터가 아니다. 기술/장비5에서 평가하며1레벨 균형의 증명으로 쓰지 않는다. 기존 원문/의도 기록은 design/workshop/intents/20261102-hearth-illumination-finalize.json에 연결된다.
