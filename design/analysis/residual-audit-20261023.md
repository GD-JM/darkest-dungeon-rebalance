# 잔차·피해량 환산 계산기 수정 및 REA 검증

사용자가 승인한 확정 오류 수정·엔진 확인·동일 입력 비교 결과다. 게임 영웅/효과 수치를 바꾼 결과가 아니라 `tools/strength.py` 분석 계산기의 오류를 정정한 결과다.

## 가장 중요한 정정

실행 파일의 실제 판정은 `roll ≤ 0 → 실패`, `roll ≥ 0.95 → 성공`, 그 사이에서 `roll < 명중−회피 → 성공`이다. 일반적인 추가 상태 없는 기준에서 `P(hit)=0.05+clamp((ACC−DODGE)/100,0,0.95)`로 환산된다. 80은 약85%, 95 이상은100%다. UI 표시용 95% 상한과 실제 판정은 달랐다.

설정 로더 → Battle 난수 객체 → MINSTD 난수 → 공격 호출 → 최종 비교 어셈블리까지 REA로 확인했다. 정적 분석이며 실전 전투 재현 실험으로 표시하지 않는다. 연속 실패 보정(+0.04 누적/성공 시 초기화), 기벽, 강제 판정, 대상별 상태는 기본 확률과 분리했다. 상세 주소와 evidence ID는 [REA 분석](C:/Users/lemm1/Documents/AI_Knowledge_Vault/topics/darkest-dungeon/residual-balance/annotations/audits/residual-fix-20261023/rea-hit-findings.md)에 있다.

## 고친 구현 오류

- 속도 약화 JSON의 -3을 -300으로 해석하던 단위 오류.
- 일반 몬스터 평가에 범위 밖 몬스터가 섞이던 명중/치명 표본: 214 →142개 공격행.
- 사용 제한·저체력·화상 조건 할인 후 총값과 세부 항목 합계가 달랐던 문제.
- 시체 제거의 명시 확률/발동 조건 누락.
- 이동 계산의 FOCUS_FIRE·KILL_SHARE·PUSH_WRAP 입력과 캐시 누락.
- 고통 반응 빈도 설정 누락, 스트레스 계산의 가변 전역 체력 의존, 후속 회복 치명 매개변수 누락.
- 명중 함수를 통일해 직접 피해·효과·회피·적 명중 감소·치명·몬스터 위협/스트레스·표식·반격 노출·생존값에 연결.

## 동일 입력 비교

223개 입력 파일 바이트와 SHA-256, 파일 열거·존재 응답을 고정했다. 기준 실행·재실행·추가 캐시 없는 실행은 동일했다. 수정 전 표준 평타7.665748535156HP를 양쪽에 동일하게 사용한다. 따라서 표준1%p=0.07665748535156HP다.

**280개 기술 중273개 변경, 7개 불변. 모든284개 원시 기술 계산과280개 선택 기술은 수정 후 합계와 세부 항목이 일치한다.** 일반 오류만 수정한 중간 결과(75개 변경)도 `confirmed-stage`에 보존해 명중식 변경 단계와 구별한다.

아래는 **RB−원본 상대 환산 격차**다. 양쪽 값이 같이 바뀔 수 있으므로 개별 기술의 변화와 구별한다.

| 기술 | 수정 전 격차 %p | 수정 후 격차 %p | 차이 %p |
|---|---:|---:|---:|
| 광대 / 독주 |104.5295|88.0286|−16.5009|
| 야만인 / 야만스러운 함성 |115.3105|102.4140|−12.8965|
| 결투가 / 찌르기 |−144.5043|−150.9345|−6.4302|

[전체 비교표](C:/Users/lemm1/Documents/AI_Knowledge_Vault/topics/darkest-dungeon/residual-balance/annotations/audits/residual-fix-20261023/comparison/comparison.md) · [기술280개·상대 격차140개 JSON](C:/Users/lemm1/Documents/AI_Knowledge_Vault/topics/darkest-dungeon/residual-balance/annotations/audits/residual-fix-20261023/comparison/comparison.json)

스트레스1점 환산은 기본 평가 실행에서 **1.668036850929 → 1.661573343762HP**다. 명중을 반영한 영웅당 스트레스 유입은 **1.680107855952 → 1.790151892117**다. 가격 비율이나10라운드 정책을 새로 채택한 결과가 아니다.

## 검증과 한계

확정 오류 회귀11개, 명중·연결8개, 고정 입력 비교8개: **27개 검사 통과**. 별도 float32 난수/분기 재구성의 경계10개도 연속 확률 근사와1e-7 미만 오차로 일치했다. `engine_replay.py`와 `engine-replay.json`에 재현 방법을 보존한다.

**이 값은 OLS 회귀 잔차가 아니다.** 현재 `strength.py`는 피해량 환산값을 계산한다. 과거 회귀 원문·실행 결과는 회수했지만 당시 설계행렬 전체를 고정해 재추정한 것은 아니다. 개별 기술 값은 `HP/고정표준평타×100−100`, 구성요소 기여는 `HP/고정표준평타×100`이다.

아직 가정인 부분은 [목록](C:/Users/lemm1/Documents/AI_Knowledge_Vault/topics/darkest-dungeon/residual-balance/annotations/audits/residual-fix-20261023/assumptions.json)에 별도 저장했다. 회피의 상대 생존 가중, 스트레스 가격·고통 기간, 피격 노출, 조건 유지율, 보호·은신·시체·이동의 전술 효용, 표본 가중은 그대로다. ENEMY_ACT4.26 등 과거 보정 상수와 일부 고통/미덕의77.5 기반 근사는 새 엔진 사실과 구별해 유지했다. 전체 공식을 실전 검증 완료했다고 주장하지 않는다.

조건부 치명의 현재 공격/이후 적용 시점(C02), 적 약화 rule_type 조건(C03), 일부 지원·추가 행동 가치 누락(STR02), 저항 포화/후속 기술 분포는 미해결이다. 임의 계수로 메우지 않았다. '원본' 비교는 프로젝트의 `.info원본.darkest` 사본이며 배포 원본의 완전한 무결성 인증은 아니다.

## 보존·연결

`before/strength.py`, `confirmed-stage/strength.py`, `after/strength.py`, 동결 입력, 검사, diff와 REA 증거 묶음을 보존한다. `manifest.json`은 파일별 해시다. 이어담 주제 `topic:darkest-dungeon:residual-balance`의 최신 개정에 연결하고 과거 식과 번복 이유를 삭제하지 않는다. 기존 MCP 회피 실행 어댑터는 역사 모델이므로 이번 전체 계산을 그 실행으로 오인하지 않는다.

재현: `python -B comparison/compare.py run-after` → `python -B comparison/compare.py compare` → `python -B comparison/test_comparison.py`. Windows 설치 경로의 존재를 기대하는 구조지만 계산 입력은 동결본에서만 읽는다. 회귀 단위 검사는 실제 설치 데이터도 읽는다.

수정 전 SHA-256: `a7714636b6a60614172ad7fae63978bf2f69119cf9379e6c833f97c5c266d15d`

수정 후 SHA-256: `938d6d1bb0fa041197a1e25a116b1a4631fee52291acaf67474788f370d332d5`

입력 manifest: `a6612f29a0c69f592c5f389b5bcc8bf941b9ea97a2ff750744b162361cb5e391`
