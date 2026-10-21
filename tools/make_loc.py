"""기술 이름 현지화: localization/*.string_table.xml → <창작마당 번호>_<언어>.loc2 (MUS-110).
게임 도구 _windows/win32/localization.exe로 컴파일한다(memory: dd-korean-patches 방식). 커스텀판·창작마당판 공용.
- 파일 이름은 스팀 창작마당 관례 <PublishedFileId>_<언어>.loc2 (구독 모드 전부 이 형식, 2026-10-22 확인).
- local=True(커스텀판 mods/Rebalance): 로컬 모드는 한국어로 해도 *_english.loc2만 읽는다(dd-korean-patches 메모, 10-09 확인)
  → 영어 칸에 한국어 이름을 넣은 english.loc2를 만든다. 창작마당판(local=False)은 언어별 원문 그대로.
사용: python tools/make_loc.py            (커스텀판 localization/ 갱신)"""
import os, re, glob, shutil, subprocess, tempfile, sys

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.dirname(os.path.dirname(M))
PFID = '3821353035'


def main(out_dir=None, local=True):
    loc_dir = os.path.join(M, 'localization')
    out_dir = out_dir or loc_dir
    xmls = glob.glob(os.path.join(loc_dir, '*.string_table.xml'))
    if not xmls:
        return []
    tmp = tempfile.mkdtemp(prefix='rb_loc_')
    loc = os.path.join(tmp, 'localization'); os.makedirs(loc); os.makedirs(os.path.join(tmp, 'colours'))
    for f in glob.glob(os.path.join(G, 'colours', '*.colours.darkest')):
        shutil.copy(f, os.path.join(tmp, 'colours'))
    for f in xmls:
        t = open(f, encoding='utf-8').read()
        if local:   # 영어 칸을 한국어 칸으로 바꿔 넣는다
            ko = re.search(r'<language id="koreana">(.*?)</language>', t, re.S).group(1)
            t = re.sub(r'<language id="english">.*?</language>', lambda m: '<language id="english">' + ko + '</language>', t, flags=re.S)
        open(os.path.join(loc, os.path.basename(f)), 'w', encoding='utf-8').write(t)
    open(os.path.join(loc, 'project_paths.txt'), 'w').write('..')
    res = subprocess.run([os.path.join(G, '_windows', 'win32', 'localization.exe')], cwd=loc, input=b'\n', capture_output=True).stdout.decode('cp949', 'ignore')
    assert 'SUCCESS' in res and 'Error' not in res, res
    os.makedirs(out_dir, exist_ok=True)
    if out_dir == loc_dir:
        for old in glob.glob(os.path.join(loc_dir, '*.loc2')):
            os.remove(old)
    out = []
    for f in glob.glob(os.path.join(loc, '*.loc2')):
        dst = os.path.join(out_dir, '%s_%s' % (PFID, os.path.basename(f)))
        shutil.copy(f, dst); out.append(dst)
    shutil.rmtree(tmp)
    return out


if __name__ == '__main__':
    print(len(main()), 'loc2')
