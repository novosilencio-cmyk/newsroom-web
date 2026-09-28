import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'


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
        self.assertIn('lokale lagring', source)


if __name__ == '__main__':
    unittest.main()
