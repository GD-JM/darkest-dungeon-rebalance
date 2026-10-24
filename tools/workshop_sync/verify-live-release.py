"""WS-VERIFY-001: read back a published release; optionally refresh its subscribed download."""
import argparse
import ctypes as C
import hashlib
import html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import time
from urllib.request import urlopen
from urllib.error import HTTPError

from common import read_json, sha256, write_json
from steam import Steam, ITEM_ID
from sync import marker_of, verify_phase


def plain(value):
    value = re.sub(r'<[^>]*>', '', value)
    value = re.sub(r'\[/?(?:b|i|u|list|olist|h[123])\]|\[\*\]', '', value)
    return ''.join(html.unescape(value).split())


def verify(config, job, refresh_download=False):
    release = read_json(job/'release.json')
    report = {'source_sha':release['source_sha'], 'version':release['version']}
    with Steam(config['game_root']) as steam:
        remote = steam.query()
        verify_phase(remote,release,'assets')
        if marker_of(remote).get('digest') != release['digest']:
            raise ValueError('Live release checkpoint mismatch')
        report['descriptions'] = {}
        for desc in release['descriptions']:
            detail = remote if desc['language']=='english' else steam.query(desc['language'])
            verify_phase(detail,release,'assets' if desc['language']=='english' else desc['language'])
            report['descriptions'][desc['language']]=True
        expected = {Path(p['path']).name:p['sha256'] for p in release['images']}
        def image_hash(p):
            with urlopen(p['url'],timeout=60) as response:
                digest=hashlib.sha256(response.read(2_000_000)).hexdigest()
            return {'filename':p['filename'],'matches':digest==expected[p['filename']], 'sha256':digest}
        with ThreadPoolExecutor(max_workers=4) as pool:
            report['images']=list(pool.map(image_hash,[p for p in remote['previews'] if p['filename'] in expected]))
        try:
            with urlopen('https://steamcommunity.com/sharedfiles/filedetails/changelog/'+str(ITEM_ID),timeout=60) as response:
                body=response.read().decode('utf-8')
            (job/'public-changelog.html').write_text(body,encoding='utf-8')
        except HTTPError as exc:
            # Preserve successful API/CDN checks and continue download verification.
            report['changelog_http_error']={'status':exc.code,'retry_after':exc.headers.get('Retry-After')}
            body=''
        entries=re.findall(r'<p id="(\d+)">(.*?)</p>',body,re.S)
        report['matching_note_ids']=[id for id,text in entries if plain(release['note'])==plain(text)]
        report['version_note_count']=sum('Update '+release['version'] in html.unescape(re.sub(r'<[^>]*>','',text)) for _,text in entries)
        size=C.c_uint64(); stamp=C.c_uint32(); folder=C.create_string_buffer(4096)
        def installed():
            ok=steam.fn('ISteamUGC_GetItemInstallInfo',C.c_bool,C.c_void_p,C.c_uint64,C.POINTER(C.c_uint64),C.c_char_p,C.c_uint32,C.POINTER(C.c_uint32))(steam.ugc,ITEM_ID,C.byref(size),folder,len(folder),C.byref(stamp))
            return Path(folder.value.decode('utf-8')) if ok else None
        def mismatches(path):
            return [rel for rel,digest in release['payload_hashes'].items() if path is None or not (path/rel).is_file() or sha256(path/rel)!=digest]
        path=installed(); missing=mismatches(path)
        if missing and refresh_download:
            ok=steam.fn('ISteamUGC_DownloadItem',C.c_bool,C.c_void_p,C.c_uint64,C.c_bool)(steam.ugc,ITEM_ID,True)
            report['download_requested']=bool(ok)
            deadline=time.monotonic()+120
            while ok and missing and time.monotonic()<deadline:
                steam.fn('RunCallbacks',None)()
                time.sleep(1)
                path=installed(); missing=mismatches(path)
        report['installed_path']=str(path) if path else None
        report['payload_files']=len(release['payload_hashes'])
        report['payload_mismatches']=missing
        report['all_passed']=(len(report['images'])==len(expected) and all(p['matches'] for p in report['images']) and len(report['matching_note_ids'])==1 and report['version_note_count']==1 and not missing)
    write_json(job/'live-verification.json',report)
    print({k:v for k,v in report.items() if k not in ('images','descriptions')})
    return 0 if report['all_passed'] else 1


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--job',required=True,type=Path)
    p.add_argument('--refresh-download',action='store_true')
    args=p.parse_args()
    raise SystemExit(verify(read_json(Path(__file__).parent/'config.json'),args.job,args.refresh_download))
