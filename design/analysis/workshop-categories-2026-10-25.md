# WS-TAGS-001 창작마당 분류 확대

사용자는 Class Tweaks에 한정된 접촉점을 늘려 Gameplay Tweaks, New Class, Overhauls에도 노출하도록 요청했다. 네 분류는 Darkest Dungeon 공식 창작마당 필터에 모두 존재한다.

분류: Overhauls / Gameplay Tweaks / Class Tweaks / New Class. 단독 공개 항목3821353035에 공식 SetItemTags로 태그만 갱신했다. 새 영웅/항목을 만들었다는 뜻은 아니며 사용자 요청에 따른 분류 선택이다. Steam 조회에서는 New Class가 소문자 new class로 정규화되므로 대소문자 차이를 구분하지 않고 대조했다.

기존 제목·설명·이미지27개·배포 메타데이터는 그대로 유지됐고 게임 파일이나 업데이트 노트는 전송하지 않았다. 다음 빌드/수동 업로드의 원본에도 네 분류가 남도록 project.template.xml과 project.xml을 동기화한다. 일반 자동 배포가 태그를 직접 덮어쓰지 않으므로 현재 공개 태그도 유지된다.

main 태그 설정 커밋을 별도 인덱스에서 작성하고 그 태그 커밋만 test에 적용한다. 테스트 중인 RUN-004 판 뒤엎기 바닐라 복원은 main에 넣지 않으며 설치 폴더는 test로 유지한다. GitHub 푸시/전체 게임 재배포는 이 분류 수정에 포함하지 않는다.
