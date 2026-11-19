"""Offline private intake contract; no mail, database, CAPTCHA or HTTP endpoint.
Reception context is supplied only by a future server adapter, never the browser.
"""
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass(frozen=True)
class Reception:
    request_id: str
    anti_spam_verified: bool
    within_limits: bool

@dataclass
class PrivateFeedback:
    article_ids: set
    _messages: dict = field(default_factory=dict)

    def receive(self, payload, reception):
        if not (reception.request_id and reception.anti_spam_verified and reception.within_limits):
            raise PermissionError('server anti-spam and limits required; no reader account required')
        if payload.get('visibility', 'private') != 'private':
            raise ValueError('this channel accepts private messages only')
        article = payload.get('article_id')
        if article not in self.article_ids:
            raise ValueError('unknown canonical article')
        text = payload.get('text')
        if not isinstance(text, str) or not 1 <= len(text.strip()) <= 4000:
            raise ValueError('message length must be 1–4000')
        email = payload.get('reply_email', '')
        if not isinstance(email, str) or len(email) > 254 or any(ord(c) < 32 for c in email):
            raise ValueError('invalid reply email')
        email = email.strip()
        if email:
            # Basic form boundary, not full RFC validation or proof of mailbox ownership.
            parts = email.split('@')
            if (len(parts) != 2 or not all(parts) or any(c.isspace() for c in email)
                    or '.' not in parts[1] or any(not label for label in parts[1].split('.'))):
                raise ValueError('invalid reply email')
        name = payload.get('name', '')
        if not isinstance(name, str) or len(name) > 120:
            raise ValueError('optional name too long')
        message = {'article_id':article, 'text':text.strip(), 'name':name.strip(),
                   'reply_email':email.strip(), 'visibility':'private', 'status':'received'}
        previous = self._messages.get(reception.request_id)
        if previous:
            if previous['original'] != message:
                raise ValueError('conflicting request replay')
            return {'request_id':reception.request_id, 'status':'received_in_offline_model', 'duplicate':True}
        self._messages[reception.request_id] = {'original':deepcopy(message), 'message':message}
        return {'request_id':reception.request_id, 'status':'received_in_offline_model', 'duplicate':False}

    def read_for_editor(self, *, authorized=False):
        if not authorized:
            raise PermissionError('server editorial role required')
        return deepcopy([row['message'] for row in self._messages.values()])
