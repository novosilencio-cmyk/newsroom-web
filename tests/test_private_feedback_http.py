import json
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from wsgiref.simple_server import make_server, WSGIRequestHandler
from backend.private_feedback_app import App, Inbox, Turnstile

class QuietHandler(WSGIRequestHandler):
    def log_message(self,*args): pass

class IntakeHTTPTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.path=Path(self.temp.name)/'inbox.sqlite3'
        self.key='local-test-only-editorial-key-123456789'
        self.origin='https://experimentalnewsroom.org'
        self.app=App(Inbox(self.path),{'article-1'},self.origin,self.key,lambda token:token=='test-verified')
        self.server=make_server('127.0.0.1',0,self.app,handler_class=QuietHandler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True); self.thread.start()
        self.url='http://127.0.0.1:'+str(self.server.server_port)
        self.payload={'request_id':str(uuid.uuid4()),'article_id':'article-1','text':'Syntetisk privat prøve','anti_spam_token':'test-verified','language':'es-AR'}
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.temp.cleanup()
    def call(self,path='/feedback',payload=None,headers=None,method='POST'):
        data=json.dumps(payload if payload is not None else self.payload).encode() if method=='POST' else None
        req=Request(self.url+path,data=data,method=method,headers=headers or {'Content-Type':'application/json','Origin':self.origin})
        try: response=urlopen(req,timeout=2)
        except HTTPError as e: response=e
        with response: return response.status,json.load(response),dict(response.headers)
    def test_real_http_receipt_and_restart_readback(self):
        code,receipt,_=self.call(); self.assertEqual(code,202); self.assertEqual(receipt['status'],'stored_privately')
        restarted=Inbox(self.path); self.assertEqual(len(restarted.rows()),1)
        self.assertEqual(restarted.rows()[0]['message']['text'],self.payload['text'])
        self.assertEqual(restarted.rows()[0]['message']['language'],'es-AR')
        self.assertEqual(self.path.stat().st_mode & 0o777,0o600)
    def test_private_read_requires_editor_key_and_has_no_cors(self):
        self.call()
        self.assertEqual(self.call('/admin/feedback',method='GET')[0],401)
        code,row,headers=self.call('/admin/feedback',method='GET',headers={'Authorization':'Bearer '+self.key,'Origin':self.origin})
        self.assertEqual(code,200); self.assertEqual(len(row['messages']),1)
        self.assertNotIn('Access-Control-Allow-Origin',headers)
        self.assertEqual(self.call('/feedback',method='GET')[0],404)
    def test_spoofed_flags_cannot_replace_bot_verification(self):
        code,_,_=self.call(payload={**self.payload,'anti_spam_token':'bad','anti_spam_verified':True,'authorized':True})
        self.assertEqual(code,403); self.assertFalse(self.app.inbox.rows())
    def test_origin_and_public_visibility_rejected(self):
        self.assertEqual(self.call(headers={'Content-Type':'application/json','Origin':'https://other.example'})[0],403)
        self.assertEqual(self.call(payload={**self.payload,'visibility':'public'})[0],400)
        self.assertFalse(self.app.inbox.rows())
    def test_idempotent_receipt_and_conflict(self):
        self.call(); code,row,_=self.call(); self.assertEqual(code,202); self.assertTrue(row['duplicate'])
        self.assertEqual(self.call(payload={**self.payload,'text':'changed'})[0],409)
        self.assertEqual(len(self.app.inbox.rows()),1)
    def test_rate_limit(self):
        self.app.per_minute=1
        self.assertEqual(self.call()[0],202); self.assertEqual(self.call()[0],429)
    def test_unavailable_verifier_and_storage_no_false_receipt(self):
        self.app.verifier=lambda token:None
        self.assertEqual(self.call()[0],503); self.assertFalse(self.app.inbox.rows())
        self.app.verifier=lambda token:True
        def broken(*args): raise OSError('test-only write failure')
        self.app.inbox.put=broken
        self.assertEqual(self.call()[0],503)
    def test_missing_secret_is_closed(self):
        self.assertIsNone(Turnstile('', 'experimentalnewsroom.org')('any-token'))
        with self.assertRaises(ValueError): App(self.app.inbox,{'a'},self.origin,'short',lambda token:True)

if __name__=='__main__': unittest.main()
