# WS-MODULAR-001 DLC 선택형 배포 (2026-10-24)

사용자 승인: “별도 선택형 패키지 제공 허용”. 기존 전체판 3821353035를 유지하고 본편 15영웅판과 DLC 영웅별 선택 패치 5개를 제공한다. 모든 항목은 같은 main SHA로 빌드한다. 실제 ID는 ../workshop/modules.json에 기록한다. 선택형 본편판과 기존 전체판은 함께 활성화하지 않는다. DLC 패치는 본편판 및 해당 DLC 영웅 활성화가 필요하다.

## 원인과 접근

전체판은 DLC 영웅의 완전한 heroes/<hero>/<hero>.info.darkest를 루트에 제공한다. 관련 DLC 영웅을 끄면 원본 art/효과/자원은 빠져도 모드가 영웅을 등록하려 한다. 단순 .override.darkest 전환은 기존 효과 목록에 덧붙여지는 경로 때문에 효과 중복 위험이 있다. 기술 전체를 다시 덮는 현재 방식은 보존하고 패키지의 포함 영웅을 분리한다.

설치된 x64 Darkest.exe SHA256: 4d78fbfaa65b7d002d2208d02da809200f4a5723119521180e30100d6f1a75f2.
정적 분석: 0x1403e7fb0은 .info.darkest 검색 후 영웅 로더를 호출한다. 0x1404c5350은 heroes/%s/%s.info.darkest 및 art와 override 경로를 연다. 0x140482810의 effect 필드 경로는 효과 컨테이너에 추가한다. 주소는 이 실행 파일 빌드에만 해당한다. Ghidra -noanalysis 후 지정 함수 디스어셈블/디컴파일로 확인했다. 전체 자동 분석 실패를 성공으로 간주하지 않았다. 로컬 상세 증거는 작업공간 outputs/dlc-compat-research/loader-functions.annotated.c와 loader-files.annotated.c에 보존했다. 게임 바이너리는 저장소에 포함하지 않는다.

## 동반 버그 수정

- FLA-015: 고통의 Cure Debuffs가 방패 파괴자 DLC에만 정의되어 있던 교차 의존을 RB FLA Cure Debuffs로 분리. 원본과 target/chance/clear_debuff/on_hit/on_miss가 동일하다.
- SYS-103: 빌더가 combat_skill 이외의 효과도 수집하여 총사 치명타 RB MUS on_crit_pierce 및 RB_MUS_CRIT_AP가 빠지지 않게 한다. 바닐라의 따옴표 없는 effect 이름도 읽는다.
- 수치 재조정은 없다. 기존 승인된 BH-024/025/026, OCC-015 및 모델 기록은 이번 main 승격 범위에 포함한다.

## 검증 범위와 배포

사용자 “지금은 플레이 중이니 파일 검증부터 해”에 따라 게임 종료, 세이브/DLC 활성화 설정 변경, 플레이 테스트를 하지 않는다. 정적 의존 관계 검증과 게임 실행 검증은 별개다. 본편 및 5개 선택 여부의 32가지 조합을 파일 기준으로 검사한다. 원본 영웅 데이터 보존, 효과/버프 참조, 중복 정의, 모드 파일 목록·크기를 검증한다.

패키지별 이미지/설명/업데이트 노트와 제출 체크포인트를 각각 기록한다. 새 항목 생성은 승인된 6개만, 불명확한 생성 결과는 자동 재시도하지 않는다. main push 성공 후 선택형들과 기존 전체판까지 모두 제출 완료되어야 배포 성공으로 기록한다. test push는 여전히 게시하지 않는다.

Steam API 자료: https://partner.steamgames.com/doc/api/ISteamUGC 및 ValveSoftware/source-sdk-2013/src/public/steam/isteamugc.h의 Win64 콜백 정의. Chrome 로그인이나 쿠키를 사용하지 않고 현재 Steam 클라이언트 공식 API를 사용한다.
