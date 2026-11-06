import unittest
from scripts.reader_community import Community, Context

class ReaderCommunityTest(unittest.TestCase):
    def setUp(self):
        self.community = Community({'article-1'})
        self.reader = Context('reader-1', True, True)
    def reaction(self, identifier='r1', action='reaction.set', language='nb'):
        return dict(event_id=identifier, action=action, article_id='article-1', language=language)
    def comment(self):
        return dict(event_id='c1', action='comment.submit', article_id='article-1',
                    comment_id='comment-1', text='<script>example</script>', language='nb', content_version='v1')
    def test_translations_share_one_reaction_and_undo(self):
        self.community.apply(self.reaction(), self.reader)
        self.community.apply(self.reaction('r2', language='en'), self.reader)
        self.assertEqual(len(self.community.reactions), 1)
        self.community.apply(self.reaction('r3', 'reaction.remove'), self.reader)
        self.assertFalse(self.community.reactions)
    def test_duplicate_and_conflicting_replay(self):
        event = self.reaction()
        self.community.apply(event, self.reader)
        self.assertEqual(self.community.apply(event, self.reader), 'duplicate')
        with self.assertRaises(ValueError):
            self.community.apply(self.reaction(action='reaction.remove'), self.reader)
    def test_unverified_and_inactive_contexts_rejected(self):
        for ctx in [Context('',True,True), Context('r',False,True), Context('r',True,False), Context('r',True,True,False)]:
            with self.assertRaises(PermissionError):
                self.community.apply(self.reaction(), ctx)
        self.assertFalse(self.community.reactions)
    def test_comments_pending_and_moderator_role_required(self):
        self.community.apply(self.comment(), self.reader)
        self.assertFalse(self.community.public_comments('article-1'))
        moderation = dict(event_id='m1', action='comment.moderate', comment_id='comment-1', status='published')
        with self.assertRaises(PermissionError):
            self.community.apply(moderation, self.reader)
        self.community.apply(moderation, Context('mod', True, True, moderator=True))
        public = self.community.public_comments('article-1')
        self.assertNotIn('user_id', public[0])
        self.assertEqual(public[0]['text'], '<script>example</script>')
    def test_unknown_article_and_missing_version_rejected(self):
        event = self.reaction(); event['article_id'] = 'unregistered'
        with self.assertRaises(ValueError): self.community.apply(event, self.reader)
        event = self.comment(); del event['content_version']
        with self.assertRaises(ValueError): self.community.apply(event, self.reader)
        self.assertFalse(self.community.comments)
    def test_erasure_removes_participation(self):
        self.community.apply(self.reaction(), self.reader)
        self.community.apply(self.comment(), self.reader)
        self.community.erase_account(self.reader.user_id)
        self.assertFalse(self.community.reactions)
        self.assertFalse(self.community.comments)
        self.assertFalse(self.community.receipts)

if __name__ == '__main__': unittest.main()
