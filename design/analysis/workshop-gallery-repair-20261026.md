# WS-GALLERY-002: 2026-10-26 공개2.5.7 갤러리 복구

사용자 요청: “스팀 창작마당에 사진 이미지가 다 안들어가있어 10몇장밖에 안돼 이거 패치 버전 맞춰서 이미지 다 채워줘”

Steam3821353035의 공개 배포본은2.5.7/source83e4cc9다. 로컬main b37da36의4개 미공개 커밋은 배포하지 않았다.
진단: API상27장 등록 중12장의 URL이 빈 문자열이었다. 나머지15장의 실제 CDN 바이트는2.5.7 원본SHA256과 일치했다. 새 비로그인 공개 DOM에도15개 썸네일만 존재했다. 빈 주소가 생긴 Steam 내부 원인은 이 검사로 특정하지 못했다.

복구: 마지막 성공 배포 job의 원본 PNG12장을 해시 대조하고, 기존슬롯을 UpdateItemPreviewFile로 수정했다. 기존항목 삭제/재생성 없음. 정상15개 슬롯은 API조회 결과까지 그대로 보존. 모드내용/메타데이터/제목/설명/대표썸네일/공개설정/업데이트노트 변경 없음. APIcallback성공과27개 비어있지 않은URL 확인.

검증: 복구된27개 모두 원본SHA256 일치. 새 비로그인 공개 DOM에27개 썸네일 및27개 갤러리 항목.10개 언어설명,2.5.7 노트1792912066이1개 존재함,구독다운로드39파일 모두일치. verify-live-release all_passed=true. 공개HTTP조회429는반복하지않고별도브라우저도구의새 공개DOM을 검증입력으로 사용했다.

증거: outputs/gallery-repair-20261026/{steam-before.json,audit-before.json,repair-state.json,steam-after.json,public-evidence.json,final-live-verification.json,public-gallery.png}. 이들은 이 PC 작업폴더의 실행자료이며 자격증명/개인세션은 포함하지 않는다. 기존 성공검증은 previous-live-verification.json으로 보존했다. 마지막배포SHA/버전/보류상태는 변경하지 않았다.

이번커밋은복구이력만기록하며새패치발행이아니다.4개미공개밸런스커밋은계속로컬에남는다. push없음.
