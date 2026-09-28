import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'


class AnalyticsContractTests(unittest.TestCase):
    def test_configuration_is_fail_closed_and_version_bound(self):
        source = (PUBLIC / 'analytics-config.js').read_text()
        self.assertRegex(source, r"provider:\s*'umami'")
        self.assertRegex(source, r'enabled:\s*false')
        self.assertIn("scriptUrl: 'https://cloud.umami.is/script.js'", source)
        self.assertIn("websiteId: 'fc60f1cf-5256-43fe-87aa-975f3b44709c'", source)

    def test_adapter_is_pageview_only_by_source_contract(self):
        source = (PUBLIC / 'analytics.js').read_text()
        self.assertIn("config.provider === 'umami' && config.enabled", source)
        self.assertIn("script.dataset.websiteId = config.websiteId;", source)
        self.assertIn("script.dataset.domains = window.location.hostname;", source)
        self.assertIn("script.dataset.doNotTrack = 'true';", source)
        self.assertIn("script.dataset.autoTrack = 'false';", source)
        self.assertIn("script.addEventListener('load'", source)
        self.assertIn("window.umami.track();", source)
        self.assertEqual(source.count("window.umami.track();"), 1)
        self.assertNotRegex(source, re.compile(r'dataset\.(?:click|events?|performance)', re.I))


if __name__ == '__main__':
    unittest.main()
