import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_subscription_pages import build, catalogue, offer_body

class SubscriptionTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'public/content/subscriptions.json').read_text())

    def check_config(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'content').mkdir()
            (p/'content/subscriptions.json').write_text(json.dumps(data))
            return catalogue(p)

    def test_sales_cannot_open_with_missing_links_or_unverified_lifecycle(self):
        self.data['sales_enabled']=True
        self.data.pop('hosted_checkout_verification', None)
        with self.assertRaises(ValueError): self.check_config(self.data)
        for p in self.data['offers']: p['checkout_url']='https://buy.stripe.com/test_example'
        with self.assertRaises(ValueError): self.check_config(self.data)

    def test_changed_price_or_non_stripe_destination_is_rejected(self):
        changed=copy.deepcopy(self.data); changed['offers'][0]['amount_nok']=78
        with self.assertRaises(ValueError): self.check_config(changed)
        self.data['offers'][0]['checkout_url']='https://buy.stripe.com.evil.example/pay'
        with self.assertRaises(ValueError): self.check_config(self.data)

    def test_enabled_offer_has_eight_explicit_links_and_honest_billing_periods(self):
        self.data['sales_enabled']=True; self.data['lifecycle_verified']=True
        for p in self.data['offers']: p['checkout_url']='https://buy.stripe.com/test_'+p['key']
        self.check_config(self.data)
        html=offer_body(self.data,True)
        self.assertEqual(html.count('href="https://buy.stripe.com/'),8)
        self.assertEqual(html.count('Fornyes hver måned'),4)
        self.assertEqual(html.count('Fornyes hvert år'),4)
        self.assertEqual(html.count('Engangsbetaling. Avsluttes automatisk.'),0)
        self.assertIn('1 490 kr / år',html)
        self.assertIn('Ingen ekstra bindingstid',html)

    def test_current_build_is_truthful_and_forms_never_collect_card_details(self):
        html=offer_body(self.data,True)
        self.assertEqual(html.count('href="https://buy.stripe.com/'),8)
        self.assertNotIn('disabled>',html)
        self.assertNotIn('Checkout is not open',html)
        self.assertIn('Åpne kundesiden',html)
        self.assertFalse(self.data['lifecycle_verified'])
        self.assertNotIn('<form',html)
        for file in ['subscription-terms.html','subscription-terms.en.html']:
            source=(ROOT/'public'/file).read_text()
            self.assertIn('id="withdrawal"',source)
            self.assertIn('927 532 573',source)
            self.assertIn('support@experimentalnewsroom.org',source)


    def test_registered_address_only_in_dedicated_contact_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            public = Path(tmp) / 'public'
            (public / 'content').mkdir(parents=True)
            (public / 'content/subscriptions.json').write_text(
                (ROOT / 'public/content/subscriptions.json').read_text())
            rows = {
                'nb': {'file': 'support.html', 'name': 'Norsk', 'page_title': 'Abonnement', 'deck': 'Støtt arbeidet'},
                'en': {'file': 'support.en.html', 'name': 'English', 'page_title': 'Subscribe', 'deck': 'Support journalism'},
            }
            build(public, rows)
            for filename in ['contact.html', 'contact.en.html']:
                html = (public / filename).read_text()
                self.assertIn('Andreas Nordlands veg 10', html)
                self.assertIn('927 532 573', html)
                self.assertIn('support@experimentalnewsroom.org', html)
            for filename in ['support.html', 'support.en.html', 'subscription-terms.html', 'subscription-terms.en.html']:
                html = (public / filename).read_text()
                self.assertNotIn('Andreas Nordlands veg 10', html)
                self.assertIn('927 532 573', html)
                self.assertIn('contact.html' if filename in ('support.html', 'subscription-terms.html') else 'contact.en.html', html)
            privacy = (ROOT / 'public/privacy.html').read_text()
            self.assertNotIn('Andreas Nordlands veg 10', privacy)
            self.assertNotIn('GitHub Pages', privacy)
            self.assertIn('one.com', privacy)

    def test_activation_requires_real_scope_and_each_distinct_offer(self):
        for field in ['charges_enabled', 'payouts_enabled', 'portal_active']:
            changed=copy.deepcopy(self.data)
            changed['hosted_checkout_verification'][field]=False
            with self.assertRaises(ValueError): self.check_config(changed)
        changed=copy.deepcopy(self.data)
        changed['offers'][1]['checkout_url']=changed['offers'][0]['checkout_url']
        with self.assertRaises(ValueError): self.check_config(changed)

if __name__=='__main__': unittest.main()
