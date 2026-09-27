# 총사 (musketeer) 변경 항목

바닐라 수치: `design/vanilla/musketeer.vanilla.txt`

---

### MUS-000 모드에서 제외: 총사는 전부 바닐라 (결정)

- 결정 (제작자, 2026-09-28): 총사는 이 모드에서 **아무것도 바꾸지 않는다.** 제작자는 총사 전용 외부 모드를 함께 쓴다. 같은 영웅 파일을 두 모드가 덮으면 충돌한다.
- 경위: MARK-01(`30e207f`)에서 석궁사수와 공유하는 `Sniper Damage` 효과를 같이 조정하려고 총사를 편입했었다. 석궁사수 쪽 변경은 `RB ARB Sniper Damage` 사본으로 분리되어 있어 **총사를 빼도 석궁사수 변경은 그대로 유지된다.**
- 조치: `heroes/musketeer/`, `effects/rebalance_musketeer.effects.darkest` 삭제, `modfiles.txt` 재생성. 강함 모델(`tools/strength.py`)은 RB 파일이 없는 영웅을 바닐라로 읽는다.
- 앞으로: 석궁사수와 공유하는 바닐라 효과(저격 피해, 무차별 사격, 표식, 사냥돌, 결집 신호탄 스트레스 회복 등)를 석궁사수에서 바꿀 때는 **반드시 `RB ARB` 사본**으로 바꾼다. 도구가 자동으로 그렇게 처리한다(P-17).
