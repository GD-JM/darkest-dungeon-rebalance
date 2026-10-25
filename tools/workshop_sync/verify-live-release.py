"""WS-VERIFY-001: read back a published release; optionally refresh its subscribed download."""
import argparse
import ctypes as C
import hashlib
import html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import HTTPError

from common import read_json, sha256, write_json
from steam import Steam, ITEM_ID
from sync import marker_of, verify_phase, verify_public, verify_public_html
from steam import SteamError


def plain(value):
    value = re.sub(r'<[^>]*>', '', value)
    value = re.sub(r'\[/?(?:b|i|u|list|olist|h[123])\]|\[\*\]', '', value)
    return ''.join(html.unescape(value).split())


def verify(config, job, refresh_download=False, public_evidence=None):
    release = read_json(job/'release.json')
    report = {'source_sha':release['source_sha'], 'version':release['version']}
    note, version = release['note'], release['version']
    amendment = read_json(job/'note-amendment.json')
    if amendment:
        if amendment['source_sha'] != release['source_sha'] or amendment['digest'] != release['digest']:
            raise ValueError('Note amendment belongs to a different release')
        version = amendment['version']
        note = release['note'].replace('[b]Update '+release['version']+'[/b]', '[b]Update '+version+'[/b]').replace('[b]更新 '+release['version']+'[/b]', '[b]更新 '+version+'[/b]')
        if not re.fullmatch(r'\d+\.\d+\.\d+', version) or note != amendment['note']:
            raise ValueError('Only an explicit version-heading correction is supported')
        report['submission_version'], report['version'] = release['version'], version
    evidence = read_json(public_evidence) if public_evidence else None
    if evidence:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(evidence['observed_at'].replace('Z','+00:00'))).total_seconds()
        if not 0 <= age < 1800 or evidence['source_sha'] != release['source_sha']:
            raise ValueError('Public browser evidence is stale or belongs to another release')
        if evidence['gallery_url'] != f'https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM_ID}&l=koreana' or evidence['notes_url'] != f'https://steamcommunity.com/sharedfiles/filedetails/changelog/{ITEM_ID}':
            raise ValueError('Unexpected browser evidence origin')
        report['public_evidence'] = str(public_evidence)
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
            try:
                with urlopen(p['url'],timeout=60) as response:
                    digest=hashlib.sha256(response.read(2_000_000)).hexdigest()
                return {'filename':p['filename'],'matches':digest==expected[p['filename']], 'sha256':digest}
            except Exception as exc:
                return {'filename':p['filename'], 'matches':False, 'error':str(exc)}
        with ThreadPoolExecutor(max_workers=4) as pool:
            report['images']=list(pool.map(image_hash,[p for p in remote['previews'] if p['filename'] in expected]))
        # WS-GALLERY-001: CDN bytes and UGC registration do not prove public display.
        try:
            urls = [p['url'] for p in remote['previews'] if p['filename'] in expected]
            report['public_gallery_verified'] = verify_public_html(evidence['gallery_html'], urls) if evidence else verify_public(ITEM_ID, urls)
        except SteamError as exc:
            report['public_gallery_verified'] = False
            report['public_gallery_error'] = str(exc)
        try:
            if evidence:
                body = evidence['notes_html']
            else:
                with urlopen('https://steamcommunity.com/sharedfiles/filedetails/changelog/'+str(ITEM_ID),timeout=60) as response:
                    body=response.read().decode('utf-8')
            (job/'public-changelog.html').write_text(body,encoding='utf-8')
        except HTTPError as exc:
            # Preserve successful API/CDN checks and continue download verification.
            report['changelog_http_error']={'status':exc.code,'retry_after':exc.headers.get('Retry-After')}
            body=''
        entries=re.findall(r'<p id="(\d+)">(.*?)</p>',body,re.S)
        report['matching_note_ids']=[id for id,text in entries if plain(note)==plain(text)]
        report['version_note_count']=sum('Update '+version in html.unescape(re.sub(r'<[^>]*>','',text)) for _,text in entries)
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
        report['all_passed']=(report['public_gallery_verified'] and len(report['images'])==len(expected) and all(p['matches'] for p in report['images']) and len(report['matching_note_ids'])==1 and report['version_note_count']==1 and not missing)
    write_json(job/'live-verification.json',report)
    print({k:v for k,v in report.items() if k not in ('images','descriptions')})
    return 0 if report['all_passed'] else 1


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--job',required=True,type=Path)
    p.add_argument('--refresh-download',action='store_true')
    p.add_argument('--public-evidence',type=Path,help='Fresh public DOM captured by browser tools when HTTP verification is rate limited')
    args=p.parse_args()
    raise SystemExit(verify(read_json(Path(__file__).parent/'config.json'),args.job,args.refresh_download,args.public_evidence))
