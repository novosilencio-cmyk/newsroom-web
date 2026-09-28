import os
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SITE = ROOT / '_site'


class AnalyticsContractTests(unittest.TestCase):
    def test_configuration_is_enabled_for_consent_gated_use(self):
        source = (PUBLIC / 'analytics-config.js').read_text()
        self.assertRegex(source, r"provider:\s*'umami'")
        self.assertRegex(source, r'enabled:\s*true')
        self.assertIn("scriptUrl: 'https://cloud.umami.is/script.js'", source)
        self.assertIn("websiteId: 'fc60f1cf-5256-43fe-87aa-975f3b44709c'", source)

    def test_adapter_requires_opt_in_and_sends_minimal_pageview(self):
        source = (PUBLIC / 'analytics.js').read_text()
        self.assertIn("savedChoice() !== 'granted'", source)
        self.assertIn("script.dataset.doNotTrack = 'true';", source)
        self.assertIn("script.dataset.autoTrack = 'false';", source)
        self.assertIn("url: window.location.pathname", source)
        self.assertNotIn("window.location.search", source)
        self.assertNotIn("document.referrer", source)
        self.assertEqual(source.count("window.umami.track({"), 1)
        self.assertNotRegex(source, re.compile(r'dataset\.(?:click|events?|performance)', re.I))

    def test_privacy_notice_describes_gate_and_choice_control(self):
        source = (PUBLIC / 'privacy.html').read_text()
        self.assertIn('frivillig valg', source)
        self.assertIn('data-analytics-consent-reopen', source)
        self.assertIn('lagres lokalt i nettleseren', source)


    def test_generated_site_loads_consent_gated_analytics_on_every_page(self):
        pages = sorted(SITE.rglob('*.html'))
        self.assertGreater(len(pages), 0, 'static site build must create HTML pages')
        self.assertTrue((SITE / 'analytics-config.js').is_file())
        self.assertTrue((SITE / 'analytics.js').is_file())
        for page in pages:
            source = page.read_text()
            relative = Path(os.path.relpath(SITE, page.parent)).as_posix()
            prefix = '' if relative == '.' else f'{relative}/'
            for asset in ('analytics-config.js', 'analytics.js'):
                src = f'src="{prefix}{asset}"'
                self.assertIn(src, source, f'{page.relative_to(SITE)} must load {asset}')
                self.assertEqual((page.parent / f'{prefix}{asset}').resolve(), (SITE / asset).resolve())
if __name__ == '__main__':
    unittest.main()
