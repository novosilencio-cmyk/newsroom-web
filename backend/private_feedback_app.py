"""Bounded WSGI intake adapter. Local runner only; public hosting remains unconfigured."""
import hmac
import json
import os
import sqlite3
import time
import uuid
from collections import deque
from pathlib import Path
from threading import Lock
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from scripts.private_reader_feedback import PrivateFeedback, Reception

class Inbox:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS feedback (id TEXT PRIMARY KEY, payload TEXT NOT NULL, received_at REAL NOT NULL)')
        os.chmod(self.path, 0o600)

    def put(self, identifier, row):
        serialized = json.dumps(row, sort_keys=True, ensure_ascii=False)
        with sqlite3.connect(self.path, timeout=5) as db:
            old = db.execute('SELECT payload FROM feedback WHERE id=?', (identifier,)).fetchone()
            if old:
                if old[0] != serialized:
                    raise ValueError('conflicting replay')
                return True
            db.execute('INSERT INTO feedback VALUES (?, ?, ?)', (identifier, serialized, time.time()))
        return False  # commit completes before the HTTP acknowledgment

    def rows(self):
        with sqlite3.connect(self.path) as db:
            return [{'receipt_id':r[0], 'message':json.loads(r[1]), 'received_at':r[2]}
                    for r in db.execute('SELECT id,payload,received_at FROM feedback ORDER BY received_at LIMIT 100')]

class Turnstile:
    def __init__(self, secret, hostname):
        self.secret, self.hostname = secret, hostname
    def __call__(self, token):
        if not self.secret:
            return None  # unavailable, not a successful check
        if not isinstance(token, str) or not 1 <= len(token) <= 2048:
            return False
        data = urlencode({'secret':self.secret, 'response':token}).encode()
        try:
            with urlopen(Request('https://challenges.cloudflare.com/turnstile/v0/siteverify',data=data),timeout=8) as r:
                result = json.load(r)
            return (isinstance(result,dict) and result.get('success') is True and result.get('hostname') == self.hostname
                    and result.get('action') == 'private-feedback')
        except (OSError, ValueError):
            return None

class App:
    def __init__(self, inbox, article_ids, origin, admin_key, verifier, per_minute=5, global_per_minute=60):
        if len(admin_key) < 32:
            raise ValueError('editorial key must contain at least 32 characters')
        self.inbox, self.article_ids, self.origin = inbox, article_ids, origin
        self.admin_key, self.verifier = admin_key, verifier
        self.per_minute, self.global_per_minute = per_minute, global_per_minute
        self.attempts = deque(); self.lock = Lock()
    def limited(self, address):
        now = time.monotonic()
        with self.lock:
            while self.attempts and self.attempts[0][0] < now-60:
                self.attempts.popleft()
            if len(self.attempts) >= self.global_per_minute or sum(a==address for _,a in self.attempts) >= self.per_minute:
                return True
            self.attempts.append((now,address)); return False
    def __call__(self, env, start_response):
        origin = env.get('HTTP_ORIGIN','')
        def respond(code, payload, cors=False):
            body = json.dumps(payload, ensure_ascii=False).encode()
            headers=[('Content-Type','application/json; charset=utf-8'),('Content-Length',str(len(body))),
                     ('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Vary','Origin')]
            if cors and origin == self.origin:
                headers += [('Access-Control-Allow-Origin',origin),('Access-Control-Allow-Methods','POST, OPTIONS'),
                            ('Access-Control-Allow-Headers','Content-Type')]
            start_response(str(code)+' '+{200:'OK',202:'Accepted',204:'No Content',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',409:'Conflict',413:'Too Large',415:'Unsupported Media Type',429:'Too Many Requests',500:'Internal Server Error',503:'Service Unavailable'}[code],headers)
            return [body]
        path, method = env.get('PATH_INFO'), env.get('REQUEST_METHOD')
        if path == '/admin/feedback' and method == 'GET':
            if not hmac.compare_digest(env.get('HTTP_AUTHORIZATION','').encode('utf-8'), ('Bearer '+self.admin_key).encode('utf-8')):
                return respond(401,{'error':'unauthorized'})
            try: return respond(200,{'messages':self.inbox.rows()})
            except sqlite3.Error: return respond(503,{'error':'storage_unavailable'})
        if path != '/feedback' or method not in ('POST','OPTIONS'):
            return respond(404,{'error':'not_found'})
        if origin != self.origin:
            return respond(403,{'error':'origin_rejected'})
        if method == 'OPTIONS':
            return respond(200,{'allowed':True},True)
        if self.limited(env.get('REMOTE_ADDR','unknown')):
            return respond(429,{'error':'try_later'},True)
        if env.get('CONTENT_TYPE','').split(';')[0] != 'application/json':
            return respond(415,{'error':'json_required'},True)
        try:
            length = int(env.get('CONTENT_LENGTH','0'))
            if not 0 < length <= 24000:
                return respond(413,{'error':'request_size'},True)
            payload=json.loads(env['wsgi.input'].read(length))
            if not isinstance(payload,dict): raise ValueError()
            identifier=str(uuid.UUID(payload.get('request_id','')))
            token=payload.pop('anti_spam_token',None)
            verified=self.verifier(token)
            if verified is None:
                return respond(503,{'error':'verification_unavailable'},True)
            if verified is not True:
                return respond(403,{'error':'verification_failed'},True)
            validation=PrivateFeedback(self.article_ids)
            validation.receive(payload,Reception(identifier,True,True))
            row=validation.read_for_editor(authorized=True)[0]
            language=payload.get('language','nb')
            if language not in ('nb','en','fr','es-AR','de','zh-Hans','zh-Hant','ja','pt-BR','ko','ar'):
                raise ValueError('unknown language')
            row['language']=language
        except (ValueError, TypeError, AttributeError, UnicodeError):
            return respond(400,{'error':'invalid_message'},True)
        try:
            duplicate=self.inbox.put(identifier,row)
        except ValueError:
            return respond(409,{'error':'conflicting_request'},True)
        except (OSError, sqlite3.Error):
            return respond(503,{'error':'storage_unavailable'},True)
        return respond(202,{'receipt_id':identifier,'status':'stored_privately','duplicate':duplicate},True)

def configured_app():
    root=Path(__file__).resolve().parents[1]
    articles=json.loads((root/'public/content/articles.json').read_text())
    origin=os.environ.get('EXPNR_FEEDBACK_ORIGIN','https://experimentalnewsroom.org')
    key=os.environ.get('EXPNR_FEEDBACK_ADMIN_KEY','')
    inbox=Inbox(os.environ.get('EXPNR_FEEDBACK_DB','/tmp/expnr-private-feedback/inbox.sqlite3'))
    return App(inbox,{a['id'] for a in articles},origin,key,
               Turnstile(os.environ.get('EXPNR_TURNSTILE_SECRET',''),urlparse(origin).hostname))

if __name__=='__main__':
    from wsgiref.simple_server import make_server
    # Deliberately loopback-only. Use a reviewed hosting adapter for public deployment.
    with make_server('127.0.0.1',8765,configured_app()) as server:
        print('Local private intake on 127.0.0.1:8765; not publicly deployed')
        server.serve_forever()
