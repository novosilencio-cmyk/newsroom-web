"""Offline community contract. Trusted context must come from a future server adapter.
This module implements neither authentication nor CAPTCHA verification nor storage.
"""
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass(frozen=True)
class Context:
    user_id: str
    email_verified: bool
    anti_spam_verified: bool
    active: bool = True
    moderator: bool = False

@dataclass
class Community:
    article_ids: set
    reactions: set = field(default_factory=set)
    comments: dict = field(default_factory=dict)
    receipts: dict = field(default_factory=dict)

    def apply(self, event, context):
        if not (context.user_id and context.active and context.email_verified and context.anti_spam_verified):
            raise PermissionError('verified active server context required')
        if not isinstance(event.get('event_id'), str) or not event['event_id'].strip():
            raise ValueError('event_id required')
        receipt_key = (context.user_id, event['event_id'])
        receipt = (deepcopy(event), context.moderator)
        if receipt_key in self.receipts:
            if self.receipts[receipt_key] != receipt:
                raise ValueError('conflicting replay')
            return 'duplicate'
        action = event.get('action')
        if action in ('reaction.set', 'reaction.remove', 'comment.submit'):
            article = event.get('article_id')
            if article not in self.article_ids:
                raise ValueError('unknown canonical article')
            if action.startswith('reaction.'):
                kind = event.get('kind', 'good_job')
                if kind not in ('good_job', 'exciting'):
                    raise ValueError('unknown reaction kind')
                key = (context.user_id, article, kind)
                if action == 'reaction.set':
                    self.reactions.add(key)
                else:
                    self.reactions.discard(key)
            else:
                body = event.get('text')
                if not isinstance(body, str) or not 1 <= len(body.strip()) <= 3000:
                    raise ValueError('comment length must be 1–3000')
                if not event.get('language') or not event.get('content_version'):
                    raise ValueError('language and content version required')
                comment_id = event.get('comment_id')
                if not isinstance(comment_id, str) or not comment_id.strip() or comment_id in self.comments:
                    raise ValueError('unique comment_id required')
                self.comments[comment_id] = {
                    'user_id': context.user_id, 'article_id': article,
                    'text': body.strip(), 'language': event['language'],
                    'content_version': event['content_version'], 'status': 'pending',
                }
        elif action == 'comment.moderate':
            if not context.moderator:
                raise PermissionError('server moderator role required')
            comment = self.comments.get(event.get('comment_id'))
            if comment is None or event.get('status') not in ('published', 'rejected'):
                raise ValueError('known comment and valid moderation status required')
            comment['status'] = event['status']
        else:
            raise ValueError('unknown action')
        self.receipts[receipt_key] = receipt
        return 'applied'

    def public_comments(self, article_id):
        # A future HTML renderer must escape text; never render it as markup.
        return [{k: v for k, v in row.items() if k != 'user_id'}
                for row in self.comments.values()
                if row['article_id'] == article_id and row['status'] == 'published']

    def erase_account(self, user_id):
        self.reactions = {r for r in self.reactions if r[0] != user_id}
        self.comments = {k: v for k, v in self.comments.items() if v['user_id'] != user_id}
        self.receipts = {k: v for k, v in self.receipts.items() if k[0] != user_id}
