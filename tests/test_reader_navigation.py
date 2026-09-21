import importlib.util
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_reader_navigation as navigation
PUBLIC = ROOT / 'public'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.hidden_ancestors = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a': self.links.append(attrs)


class ReaderNavigationTests(unittest.TestCase):
    def test_all_generated_links_and_fragments_resolve(self):
        for filename in ('sitemap.html', 'sitemap.en.html'):
            parser = Links()
            parser.feed((PUBLIC / filename).read_text())
            self.assertEqual(len(parser.ids), len(set(parser.ids)))
            for link in parser.links:
                url = urlsplit(link['href'])
                self.assertFalse(url.scheme)
                file = PUBLIC / (url.path or filename)
                if url.path.endswith('/') or url.path == './': file /= 'index.html'
                self.assertTrue(file.is_file(), link)
                if url.fragment:
                    target = Links(); target.feed(file.read_text())
                    self.assertIn(unquote(url.fragment), target.ids, link)

    def test_registered_language_destinations_are_present_without_javascript(self):
        articles = json.loads((PUBLIC / 'content/articles.json').read_text())
        for filename in ('sitemap.html', 'sitemap.en.html'):
            parser = Links(); parser.feed((PUBLIC / filename).read_text())
            urls = {link['href'] for link in parser.links}
            for article in articles:
                for version in navigation.versions(PUBLIC, article):
                    self.assertIn(version['url'], urls)
                    link = next(x for x in parser.links if x['href'] == version['url'] and 'hreflang' in x)
                    self.assertEqual(link['hreflang'], version['language'])

    def test_registry_missing_target_fails_closed(self):
        with self.assertRaises(ValueError):
            navigation.local_file(PUBLIC, 'articles/not-published.html')
        with self.assertRaises(ValueError):
            navigation.local_file(PUBLIC, '../README.md')

    def test_bilingual_titles_are_read_from_actual_panels(self):
        articles = json.loads((PUBLIC / 'content/articles.json').read_text())
        article = next(a for a in articles if a['id'] == 'ask-before-you-buy-2026')
        vv = navigation.versions(PUBLIC, article)
        self.assertEqual(vv[0]['title'], 'Spør før dere kjøper')
        self.assertEqual(vv[0]['url'], 'articles/ask-before-you-buy-2026.html?lang=no#norsk')
        self.assertEqual(vv[1]['title'], 'Ask before you buy')

    def test_shared_shell_and_viewer_boundary(self):
        for path in PUBLIC.rglob('*.html'):
            source = path.read_text()
            if 'data-visualize-standalone' in source:
                self.assertNotIn('reader-navigation.css', source)
                continue
            self.assertIn('reader-navigation.css', source, path)
            self.assertTrue('reader-skip' in source or 'skip-link' in source, path)
            self.assertRegex(source, r'<main[^>]+tabindex="-1"')

    def test_render_is_deterministic(self):
        articles = json.loads((PUBLIC / 'content/articles.json').read_text())
        for lang, filename in [('nb', 'sitemap.html'), ('en', 'sitemap.en.html')]:
            self.assertEqual(navigation.render(PUBLIC, articles, lang), (PUBLIC / filename).read_text())

if __name__ == '__main__': unittest.main()
