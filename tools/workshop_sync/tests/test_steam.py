import ctypes as C
from pathlib import Path
import sys
import unittest
import tempfile
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from steam import Steam, SteamError, SubmissionUnknown, _DetailsHead, _CreateResult, _DependencyResult, _SubmitResult, APP_ID, ITEM_ID


class SteamTests(unittest.TestCase):
    def test_preview_update_preserves_slots_and_user_video_without_delete_readd(self):
        client=object.__new__(Steam)
        client.ugc,client.utils=1,2
        client._wait=Mock()
        client.query=Mock(return_value={'owned':True,'previews':[
            {'index':0,'type':0,'filename':'old.png'},
            {'index':1,'type':1,'filename':'video'},
            {'index':2,'type':0,'filename':'surplus.png'}]})
        calls=[]
        def binder(name,*_):
            def call(*args):
                calls.append((name,args))
                if name=='ISteamUtils_GetAPICallResult':
                    result=_SubmitResult(result=1,needs_agreement=False,id=ITEM_ID)
                    C.memmove(args[2],C.byref(result),C.sizeof(result))
                return 1
            return call
        client.fn=binder
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            image=Path(folder)/'current.png'
            image.write_bytes(b'valid size fixture')
            client.update(replace_previews=({'old.png','surplus.png'},[image]))
        updates=[args[2] for name,args in calls if name=='ISteamUGC_UpdateItemPreviewFile']
        removals=[args[2] for name,args in calls if name=='ISteamUGC_RemoveItemPreview']
        self.assertEqual(updates,[0])
        self.assertEqual(removals,[2])
        self.assertFalse(any(name=='ISteamUGC_AddItemPreviewFile' for name,_ in calls))

    def test_new_item_callback_abi_and_durable_order(self):
        self.assertEqual(C.sizeof(_CreateResult), 24)
        self.assertEqual(_CreateResult.id.offset, 8)
        self.assertEqual(_CreateResult.needs_agreement.offset, 16)
        client = object.__new__(Steam)
        client.ugc, client.utils = 1, 2
        client._wait = Mock()
        events=[]
        def binder(name, *_):
            def call(*args):
                events.append(name)
                if name == 'ISteamUtils_GetAPICallResult':
                    self.assertEqual(args[-2],3403)
                    result=_CreateResult(result=1,id=12345,needs_agreement=False)
                    C.memmove(args[2],C.byref(result),C.sizeof(result))
                return 1
            return call
        client.fn=binder
        result=client.create_item(lambda:events.append('journal'))
        self.assertEqual(events[0],'journal')
        self.assertEqual(result,{'item_id':12345,'needs_agreement':False})

    def test_dependency_uses_module_identity_and_checks_callback(self):
        client=object.__new__(Steam)
        client.ugc,client.utils,client.item_id=1,2,777
        client.query=Mock(return_value={'owned':True})
        client._wait=Mock()
        def binder(name,*_):
            def call(*args):
                if name=='ISteamUGC_AddDependency': self.assertEqual(args[1:],(777,888))
                if name=='ISteamUtils_GetAPICallResult':
                    self.assertEqual(args[-2],3412)
                    result=_DependencyResult(result=1,id=777,child=888)
                    C.memmove(args[2],C.byref(result),C.sizeof(result))
                return 1
            return call
        client.fn=binder
        self.assertEqual(client.add_dependency(888),{'parent':777,'child':888,'result':1})

    def test_query_requests_full_text_and_validates_identity_and_ownership(self):
        client = object.__new__(Steam)
        client.ugc, client.user_id = 1, 42
        client._wait = Mock()
        calls = []
        def binder(name, *_):
            def call(*args):
                calls.append((name, args))
                if name == 'ISteamUGC_GetQueryUGCResult':
                    h = _DetailsHead(id=ITEM_ID,result=1,creator=APP_ID,consumer=APP_ID,owner=42,title=b'Title',description=b'Complete description')
                    C.memmove(args[-1], C.byref(h), C.sizeof(h))
                    return True
                if name == 'ISteamUGC_GetQueryUGCNumAdditionalPreviews': return 0
                return 1
            return call
        client.fn = binder
        result = client.query('koreana')
        self.assertTrue(result['owned'])
        self.assertEqual(result['description'],'Complete description')
        flags = {name: args[-1] for name,args in calls if name.startswith('ISteamUGC_Set')}
        self.assertIs(flags['ISteamUGC_SetReturnLongDescription'], True)
        self.assertEqual(flags['ISteamUGC_SetAllowCachedResponse'], 0)
        self.assertEqual(flags['ISteamUGC_SetLanguage'], b'koreana')

    def test_nonowner_is_rejected_before_staging_any_write(self):
        client=object.__new__(Steam)
        client.query=Mock(return_value={'owned':False})
        client.fn=Mock()
        with self.assertRaises(SteamError): client.update(description='Change')
        client.fn.assert_not_called()

    def test_submission_timeout_is_distinct_from_safe_query_timeout(self):
        client=object.__new__(Steam)
        client.fn=Mock(return_value=lambda *args:False)
        with self.assertRaises(SubmissionUnknown): client._wait(1,timeout=0,submission=True)
        with self.assertRaises(SteamError) as error: client._wait(1,timeout=0,submission=False)
        self.assertNotIsInstance(error.exception,SubmissionUnknown)


if __name__=='__main__': unittest.main()
