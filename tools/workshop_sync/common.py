"""WS-CORE-001: durable state and fixed repository identity for push-triggered releases."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

REMOTE = 'https://github.com/GD-JM/darkest-dungeon-rebalance.git'
LANGUAGES = ('english', 'koreana', 'schinese', 'tchinese', 'french', 'german', 'russian', 'spanish', 'polish', 'brazilian')


def read_json(path, default=None):
    p = Path(path)
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(argv, *, cwd=None, timeout=180, input=None):
    env = os.environ.copy()
    env.update(GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    r = subprocess.run([str(x) for x in argv], cwd=cwd, input=input, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=timeout, env=env, creationflags=flags,
                       encoding='utf-8', errors='replace')
    if r.returncode:
        raise RuntimeError(f'{Path(argv[0]).name} failed ({r.returncode}): {r.stderr[-4000:]}\n{r.stdout[-2000:]}')
    return r.stdout


class WorkerLock:
    def __init__(self, path):
        self.path = Path(path)

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.f = self.path.open('a+b')
        self.f.seek(0)
        if not self.f.read(1):
            self.f.write(b'0')
            self.f.flush()
        self.f.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.f.close()
            raise RuntimeError('Another Workshop Sync process is already running')
        return self

    def __exit__(self, *_):
        self.f.close()
