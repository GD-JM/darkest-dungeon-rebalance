"""기술 이름 현지화: localization/*.string_table.xml → localization/rebalance_<언어>.loc2 (MUS-110).
게임 도구 _windows/win32/localization.exe로 컴파일한다(memory: dd-korean-patches 방식). 커스텀판·창작마당판 공용.
사용: python tools/make_loc.py"""
import os, glob, shutil, subprocess, tempfile, sys

M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.dirname(os.path.dirname(M))


def main():
    loc_dir = os.path.join(M, 'localization')
    xmls = glob.glob(os.path.join(loc_dir, '*.string_table.xml'))
    if not xmls:
        return []
    tmp = tempfile.mkdtemp(prefix='rb_loc_')
    loc = os.path.join(tmp, 'localization'); os.makedirs(loc); os.makedirs(os.path.join(tmp, 'colours'))
    for f in glob.glob(os.path.join(G, 'colours', '*.colours.darkest')):
        shutil.copy(f, os.path.join(tmp, 'colours'))
    for f in xmls:
        shutil.copy(f, loc)
    open(os.path.join(loc, 'project_paths.txt'), 'w').write('..')
    res = subprocess.run([os.path.join(G, '_windows', 'win32', 'localization.exe')], cwd=loc, input=b'\n', capture_output=True).stdout.decode('cp949', 'ignore')
    assert 'SUCCESS' in res and 'Error' not in res, res
    out = []
    for f in glob.glob(os.path.join(loc, '*.loc2')):
        dst = os.path.join(loc_dir, 'rebalance_' + os.path.basename(f))
        shutil.copy(f, dst); out.append(dst)
    shutil.rmtree(tmp)
    return out


if __name__ == '__main__':
    print(len(main()), 'loc2')
