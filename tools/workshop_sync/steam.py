"""WS-STEAM-001: official Steam UGC bridge; reuse the logged-in client, never browser cookies."""
from __future__ import annotations

import ctypes as C
import json
import os
import time
from pathlib import Path

APP_ID = 262060
ITEM_ID = 3821353035
INVALID = (1 << 64) - 1


class SteamError(RuntimeError):
    pass


class SubmissionUnknown(SteamError):
    """A submission may have reached Steam; do not blindly repeat its change note."""


class _DetailsHead(C.Structure):
    # UGC016 / Win64 ABI; larger native structure is written into a 16KiB buffer.
    _fields_ = [('id', C.c_uint64), ('result', C.c_int), ('file_type', C.c_int),
                ('creator', C.c_uint32), ('consumer', C.c_uint32),
                ('title', C.c_char * 129), ('description', C.c_char * 8000),
                ('owner', C.c_uint64), ('created', C.c_uint32), ('updated', C.c_uint32)]


class _SubmitResult(C.Structure):
    _fields_ = [('result', C.c_int), ('needs_agreement', C.c_bool), ('id', C.c_uint64)]


class _CreateResult(C.Structure):
    # Valve isteamugc.h: callback 3403, Win64 pack 8.
    _fields_ = [('result', C.c_int), ('id', C.c_uint64), ('needs_agreement', C.c_bool)]


class _DependencyResult(C.Structure):
    _fields_ = [('result', C.c_int), ('id', C.c_uint64), ('child', C.c_uint64)]


def _bytes(s):
    return str(s).encode('utf-8')


class Steam:
    item_id = ITEM_ID

    def __init__(self, game_root, item_id=ITEM_ID):
        if os.name != 'nt' or C.sizeof(C.c_void_p) != 8:
            raise SteamError('64-bit Windows Python required')
        self.game_root = Path(game_root).resolve()
        self.item_id = int(item_id)
        if not 0 < self.item_id < INVALID:
            raise SteamError('Invalid Workshop item ID')
        self.dll_path = self.game_root / '_windows/win64/steam_api64.dll'
        os.environ['SteamAppId'] = str(APP_ID)
        os.environ['SteamGameId'] = str(APP_ID)
        self.dll = C.CDLL(str(self.dll_path))
        self._functions = {}
        self.initialized = False

    def fn(self, name, result, *args):
        key = (name, result, args)
        if key not in self._functions:
            f = getattr(self.dll, name if name.startswith('SteamInternal') else 'SteamAPI_' + name)
            f.restype, f.argtypes = result, list(args)
            self._functions[key] = f
        return self._functions[key]

    def __enter__(self):
        if not self.fn('Init', C.c_bool)():
            raise SteamError('Steam client unavailable. Run under the logged-in Steam user; retry when Steam is ready.')
        self.initialized = True
        try:
            client = self.fn('SteamInternal_CreateInterface', C.c_void_p, C.c_char_p)(b'SteamClient020')
            user = self.fn('GetHSteamUser', C.c_int)()
            pipe = self.fn('GetHSteamPipe', C.c_int)()
            if not client or not user or not pipe:
                raise SteamError('Steam client context unavailable')
            get = self.fn('ISteamClient_GetISteamUGC', C.c_void_p, C.c_void_p, C.c_int, C.c_int, C.c_char_p)
            self.ugc = get(client, user, pipe, b'STEAMUGC_INTERFACE_VERSION016')
            self.utils = self.fn('ISteamClient_GetISteamUtils', C.c_void_p, C.c_void_p, C.c_int, C.c_char_p)(client, pipe, b'SteamUtils010')
            self.user = self.fn('ISteamClient_GetISteamUser', C.c_void_p, C.c_void_p, C.c_int, C.c_int, C.c_char_p)(client, user, pipe, b'SteamUser021')
            if not self.ugc or not self.utils or not self.user:
                raise SteamError('Required Steam interfaces unavailable')
            self.user_id = self.fn('ISteamUser_GetSteamID', C.c_uint64, C.c_void_p)(self.user)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *_):
        if self.initialized:
            self.fn('Shutdown', None)()
            self.initialized = False

    def _wait(self, handle, timeout=60, submission=False):
        error = SubmissionUnknown if submission else SteamError
        if not handle or handle == INVALID:
            raise error('Steam returned an invalid asynchronous handle')
        done = self.fn('ISteamUtils_IsAPICallCompleted', C.c_bool, C.c_void_p, C.c_uint64, C.POINTER(C.c_bool))
        failed = C.c_bool()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self.fn('RunCallbacks', None)()
            if done(self.utils, handle, C.byref(failed)):
                if failed.value:
                    raise error('Steam asynchronous operation failed')
                return
            time.sleep(.1)
        raise error('Steam operation timed out')

    def query(self, language='english'):
        ids = (C.c_uint64 * 1)(self.item_id)
        q = self.fn('ISteamUGC_CreateQueryUGCDetailsRequest', C.c_uint64, C.c_void_p, C.POINTER(C.c_uint64), C.c_uint32)(self.ugc, ids, 1)
        if q == INVALID:
            raise SteamError('Could not create Workshop query')
        try:
            for name, argtype, value in [('SetReturnAdditionalPreviews', C.c_bool, True),
                                        ('SetReturnLongDescription', C.c_bool, True),
                                        ('SetReturnMetadata', C.c_bool, True),
                                        ('SetAllowCachedResponse', C.c_uint32, 0),
                                        ('SetLanguage', C.c_char_p, _bytes(language))]:
                if not self.fn('ISteamUGC_' + name, C.c_bool, C.c_void_p, C.c_uint64, argtype)(self.ugc, q, value):
                    raise SteamError(name + ' failed')
            call = self.fn('ISteamUGC_SendQueryUGCRequest', C.c_uint64, C.c_void_p, C.c_uint64)(self.ugc, q)
            self._wait(call)
            raw = C.create_string_buffer(16384)
            ok = self.fn('ISteamUGC_GetQueryUGCResult', C.c_bool, C.c_void_p, C.c_uint64, C.c_uint32, C.c_void_p)(self.ugc, q, 0, raw)
            head = _DetailsHead.from_buffer_copy(raw)
            if not ok or head.result != 1 or head.id != self.item_id or head.consumer != APP_ID or head.creator != APP_ID:
                raise SteamError(f'Workshop identity/result mismatch: {head.id}, result={head.result}')
            count = self.fn('ISteamUGC_GetQueryUGCNumAdditionalPreviews', C.c_uint32, C.c_void_p, C.c_uint64, C.c_uint32)(self.ugc, q, 0)
            if count > 1000:
                raise SteamError('Implausible preview count')
            previews = []
            get = self.fn('ISteamUGC_GetQueryUGCAdditionalPreview', C.c_bool, C.c_void_p, C.c_uint64, C.c_uint32, C.c_uint32, C.c_char_p, C.c_uint32, C.c_char_p, C.c_uint32, C.POINTER(C.c_int))
            for index in range(count):
                url, name, kind = C.create_string_buffer(8192), C.create_string_buffer(1024), C.c_int()
                if not get(self.ugc, q, 0, index, url, len(url), name, len(name), C.byref(kind)):
                    raise SteamError('Cannot read preview ' + str(index))
                previews.append({'index': index, 'filename': name.value.decode('utf-8'), 'url': url.value.decode('utf-8'), 'type': kind.value})
            meta = C.create_string_buffer(8192)
            self.fn('ISteamUGC_GetQueryUGCMetadata', C.c_bool, C.c_void_p, C.c_uint64, C.c_uint32, C.c_char_p, C.c_uint32)(self.ugc, q, 0, meta, len(meta))
            return dict(item_id=head.id, app_id=head.consumer, owned=head.owner == self.user_id,
                        title=head.title.decode('utf-8'), description=head.description.decode('utf-8'),
                        updated=head.updated, language=language, previews=previews, metadata=meta.value.decode('utf-8'))
        finally:
            self.fn('ISteamUGC_ReleaseQueryUGCRequest', C.c_bool, C.c_void_p, C.c_uint64)(self.ugc, q)

    def update(self, *, description=None, title=None, language='english', content=None,
               thumbnail=None, replace_previews=None, metadata=None, note=None, before_submit=None, visibility=None):
        current = self.query(language)
        if not current['owned']:
            raise SteamError('Active Steam account does not own the configured item')
        h = self.fn('ISteamUGC_StartItemUpdate', C.c_uint64, C.c_void_p, C.c_uint32, C.c_uint64)(self.ugc, APP_ID, self.item_id)
        if not h or h == INVALID:
            raise SteamError('Cannot start item update')

        def set_string(name, value):
            if value is not None:
                if not self.fn('ISteamUGC_' + name, C.c_bool, C.c_void_p, C.c_uint64, C.c_char_p)(self.ugc, h, _bytes(value)):
                    raise SteamError(name + ' rejected the prepared value')

        set_string('SetItemUpdateLanguage', language)
        set_string('SetItemTitle', title)
        if visibility is not None:
            if visibility not in (0, 2) or not self.fn('ISteamUGC_SetItemVisibility', C.c_bool, C.c_void_p, C.c_uint64, C.c_int)(self.ugc, h, visibility):
                raise SteamError('Cannot set requested visibility')
        if description is not None and len(description.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')) >= 8000:
            raise SteamError('Description exceeds the Steam byte budget')
        set_string('SetItemDescription', description)
        if content is not None:
            content = Path(content).resolve(strict=True)
            if not content.is_dir() or not (content / 'modfiles.txt').is_file():
                raise SteamError('Content must be a validated mod build')
            set_string('SetItemContent', content)
        if thumbnail is not None:
            set_string('SetItemPreview', Path(thumbnail).resolve(strict=True))
        if metadata is not None:
            set_string('SetItemMetadata', metadata)
        if replace_previews is not None:
            # WS-GALLERY-001: update existing owned slots in place. Removing and re-adding
            # identical images left live registrations pointing at missing backing files.
            # Keep unrelated images/videos and remove only surplus owned slots.
            old_names, paths = replace_previews
            indices = [p['index'] for p in current['previews'] if p['type'] == 0 and p['filename'] in old_names]
            for position, path in enumerate(paths):
                path = Path(path).resolve(strict=True)
                if path.suffix.lower() != '.png' or not 0 < path.stat().st_size < 1_000_000:
                    raise SteamError('PNG preview must be smaller than 1MB: ' + str(path))
                if position < len(indices):
                    ok = self.fn('ISteamUGC_UpdateItemPreviewFile', C.c_bool, C.c_void_p, C.c_uint64, C.c_uint32, C.c_char_p)(self.ugc, h, indices[position], _bytes(path))
                else:
                    ok = self.fn('ISteamUGC_AddItemPreviewFile', C.c_bool, C.c_void_p, C.c_uint64, C.c_char_p, C.c_int)(self.ugc, h, _bytes(path), 0)
                if not ok:
                    raise SteamError('Steam rejected additional preview: ' + path.name)
            for index in sorted(indices[len(paths):], reverse=True):
                if not self.fn('ISteamUGC_RemoveItemPreview', C.c_bool, C.c_void_p, C.c_uint64, C.c_uint32)(self.ugc, h, index):
                    raise SteamError('Could not stage surplus preview removal')
        # Durable state must say "submitting" BEFORE the only irreversible API call.
        if before_submit:
            before_submit()
        call = self.fn('ISteamUGC_SubmitItemUpdate', C.c_uint64, C.c_void_p, C.c_uint64, C.c_char_p)(self.ugc, h, None if note is None else _bytes(note))
        self._wait(call, timeout=300, submission=True)
        result, failed = _SubmitResult(), C.c_bool()
        ok = self.fn('ISteamUtils_GetAPICallResult', C.c_bool, C.c_void_p, C.c_uint64, C.c_void_p, C.c_int, C.c_int, C.POINTER(C.c_bool))(
            self.utils, call, C.byref(result), C.sizeof(result), 3404, C.byref(failed))
        if not ok or failed.value:
            raise SubmissionUnknown('Submission callback could not be decoded; reconcile remote state before retry')
        if result.result != 1 or result.needs_agreement or result.id != self.item_id:
            raise SteamError(f'Steam submission result={result.result}; agreement_required={result.needs_agreement}')
        return self.query(language)

    def create_item(self, before_create):
        """WS-MODULAR-001: caller journals before creation; ambiguous outcomes must never auto-retry."""
        before_create()
        call = self.fn('ISteamUGC_CreateItem', C.c_uint64, C.c_void_p, C.c_uint32, C.c_int)(self.ugc, APP_ID, 0)
        self._wait(call, timeout=60, submission=True)
        result, failed = _CreateResult(), C.c_bool()
        ok = self.fn('ISteamUtils_GetAPICallResult', C.c_bool, C.c_void_p, C.c_uint64, C.c_void_p, C.c_int, C.c_int, C.POINTER(C.c_bool))(
            self.utils, call, C.byref(result), C.sizeof(result), 3403, C.byref(failed))
        if not ok or failed.value:
            raise SubmissionUnknown('Creation response lost; inspect owned items before any retry')
        if result.result != 1 or not result.id:
            raise SteamError(f'CreateItem failed: {result.result}')
        return {'item_id': result.id, 'needs_agreement': bool(result.needs_agreement)}

    def add_dependency(self, child_id):
        if not self.query()['owned']:
            raise SteamError('Cannot modify dependencies of an unowned item')
        call = self.fn('ISteamUGC_AddDependency', C.c_uint64, C.c_void_p, C.c_uint64, C.c_uint64)(self.ugc, self.item_id, int(child_id))
        self._wait(call, timeout=60, submission=True)
        result, failed = _DependencyResult(), C.c_bool()
        ok = self.fn('ISteamUtils_GetAPICallResult', C.c_bool, C.c_void_p, C.c_uint64, C.c_void_p, C.c_int, C.c_int, C.POINTER(C.c_bool))(
            self.utils, call, C.byref(result), C.sizeof(result), 3412, C.byref(failed))
        if not ok or failed.value or result.result != 1 or result.id != self.item_id or result.child != int(child_id):
            raise SteamError('Steam did not confirm the required base-package dependency')
        return {'parent': result.id, 'child': result.child, 'result': result.result}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Read-only Steam Workshop connectivity check')
    parser.add_argument('--game-root', required=True)
    parser.add_argument('--out')
    args = parser.parse_args()
    with Steam(args.game_root) as steam:
        result = steam.query()
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('description', 'previews', 'metadata')}, ensure_ascii=False))
    print('previews:', len(result['previews']))
