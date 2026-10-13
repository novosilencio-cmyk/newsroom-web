import unittest
from scripts.private_reader_feedback import PrivateFeedback, Reception
from scripts.reader_community import Community, Context

class PrivateFeedbackTest(unittest.TestCase):
    def setUp(self):
        self.inbox = PrivateFeedback({'article-1'})
        self.payload = {'article_id':'article-1', 'text':'Dette trenger en bedre kilde.'}
        self.context = Reception('server-request-1', True, True)
    def test_no_profile_name_or_email_required(self):
        result = self.inbox.receive(self.payload,self.context)
        self.assertEqual(result['status'],'received_in_offline_model')
        row=self.inbox.read_for_editor(authorized=True)[0]
        self.assertEqual(row['name'],''); self.assertEqual(row['reply_email'],'')
        self.assertEqual(row['visibility'],'private')
    def test_not_public_or_readable_without_editor_role(self):
        self.inbox.receive(self.payload,self.context)
        with self.assertRaises(PermissionError): self.inbox.read_for_editor()
        with self.assertRaises(ValueError): self.inbox.receive({**self.payload,'visibility':'public'},self.context)
    def test_bot_and_limit_failure_do_not_receive(self):
        for ctx in [Reception('1',False,True),Reception('2',True,False),Reception('',True,True)]:
            with self.assertRaises(PermissionError): self.inbox.receive(self.payload,ctx)
        self.assertFalse(self.inbox.read_for_editor(authorized=True))
    def test_duplicate_and_conflicting_replay(self):
        self.inbox.receive(self.payload,self.context)
        self.assertTrue(self.inbox.receive(self.payload,self.context)['duplicate'])
        with self.assertRaises(ValueError): self.inbox.receive({**self.payload,'text':'Annen tekst'},self.context)
        self.assertEqual(len(self.inbox.read_for_editor(authorized=True)),1)
    def test_bad_target_and_mail_header_rejected(self):
        for change in [{'article_id':'other'},{'reply_email':'x@example.org\nBcc:y@example.org'},{'text':''}]:
            with self.assertRaises(ValueError): self.inbox.receive({**self.payload,**change},self.context)
        self.assertFalse(self.inbox.read_for_editor(authorized=True))
    def test_reply_address_has_local_and_domain_parts(self):
        for address in ['@', 'a@', '@example.org', 'a@@example.org', 'a@.org', 'a@example..org', 'a@example.org\x00']:
            with self.assertRaises(ValueError):
                self.inbox.receive({**self.payload, 'reply_email':address}, self.context)
        self.assertFalse(self.inbox.read_for_editor(authorized=True))
        self.inbox.receive({**self.payload, 'reply_email':' reader@example.org '}, self.context)
        self.assertEqual(self.inbox.read_for_editor(authorized=True)[0]['reply_email'], 'reader@example.org')

    def test_two_reaction_meanings_are_separate_not_weighted(self):
        model=Community({'article-1'}); ctx=Context('reader',True,True)
        for n,kind in enumerate(['good_job','exciting','exciting']):
            model.apply({'event_id':str(n),'action':'reaction.set','article_id':'article-1','kind':kind},ctx)
        self.assertEqual(len(model.reactions),2)
        model.apply({'event_id':'remove','action':'reaction.remove','article_id':'article-1','kind':'exciting'},ctx)
        self.assertEqual(model.reactions,{('reader','article-1','good_job')})
        with self.assertRaises(ValueError):
            model.apply({'event_id':'bad','action':'reaction.set','article_id':'article-1','kind':'useful'},ctx)

if __name__=='__main__': unittest.main()
