"""Regression coverage for published corpus coverage and body/tag search."""
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_reader_navigation as navigation
PUBLIC = ROOT / 'public'

class SearchEntries(HTMLParser):
    def __init__(self):
        super().__init__(); self.entries = []; self.tag_queries = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-search' in attrs: self.entries.append(attrs)
        if tag == 'a' and 'q' in parse_qs(urlsplit(attrs.get('href', '')).query):
            self.tag_queries.append(parse_qs(urlsplit(attrs['href']).query)['q'][0])

class TopicSearchTests(unittest.TestCase):
    def setUp(self):
        self.articles = json.loads((PUBLIC / 'content/articles.json').read_text())

    def test_every_published_article_file_is_registered(self):
        registered = {urlsplit(v['url']).path for a in self.articles for v in navigation.versions(PUBLIC, a)}
        actual = {p.relative_to(PUBLIC).as_posix() for p in (PUBLIC / 'articles').glob('*.html')}
        self.assertEqual(actual, registered)

    def test_search_captures_body_but_not_code_or_navigation(self):
        p = navigation.SearchText()
        p.feed('<head><title>HEADONLY</title></head><main><nav>NAVONLY</nav><p>Body <em>detail</em> &amp; meaning.</p><script>CODEONLY</script><style>STYLEONLY</style></main><footer>FOOTONLY</footer>')
        text = ' '.join(p.parts)
        self.assertIn('Body', text); self.assertIn('detail', text); self.assertIn('& meaning.', text)
        for word in ['HEADONLY','NAVONLY','CODEONLY','STYLEONLY','FOOTONLY']: self.assertNotIn(word, text)

    def test_all_topics_have_working_query_links_and_body_terms(self):
        for lang, filename in [('nb','sitemap.html'),('en','sitemap.en.html')]:
            parser = SearchEntries(); parser.feed((PUBLIC / filename).read_text())
            for a in self.articles:
                self.assertGreaterEqual(len(a['tags'][lang]), 3)
                for tag in a['tags'][lang]: self.assertIn(tag, parser.tag_queries)
            # Named only in the full body of the monetary-policy article, not its title/deck/tags.
            self.assertTrue(any('Olav Thon' in e['data-search'] and 'rentemøte' in e['data-search'] for e in parser.entries))
            self.assertIn('Kunst' if lang == 'nb' else 'Art', (PUBLIC / filename).read_text())

    def test_search_engine_map_covers_all_reader_destinations(self):
        import xml.etree.ElementTree as ET
        root = ET.parse(PUBLIC / 'sitemap.xml').getroot()
        urls = [e.text for e in root.findall('{*}url/{*}loc')]
        self.assertEqual(len(urls), len(set(urls)))
        for _, _, _, entries in navigation.SECTIONS:
            for url, _, _ in entries:
                if not urlsplit(url).fragment:
                    self.assertIn('https://experimentalnewsroom.org/' + url, urls)
