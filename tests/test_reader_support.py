import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC = Path(__file__).resolve().parents[1] / 'public'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.language = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.language = attrs.get('lang')
        if tag in ('a', 'link'): self.links.append((tag, attrs))

class ReaderSupportTests(unittest.TestCase):
    def test_explicit_languages_reciprocal_urls_and_one_payment(self):
        rows = json.loads((PUBLIC / 'content/reader-support.json').read_text())
        self.assertEqual(set(rows), {'nb', 'en', 'fr', 'es-AR', 'de', 'zh-Hans', 'zh-Hant', 'ja', 'pt-BR', 'ko', 'ar'})
        for lang, row in rows.items():
            page = Page(); page.feed((PUBLIC / row['file']).read_text())
            self.assertEqual(page.language, lang)
            alternates = {a.get('hreflang'): a['href'] for tag, a in page.links if tag == 'link' and a.get('rel') == 'alternate'}
            for other, target in rows.items():
                self.assertEqual(alternates[other], 'https://experimentalnewsroom.org/' + target['file'])
            payments = [a for tag, a in page.links if tag == 'a' and urlsplit(a.get('href', '')).netloc == 'donate.stripe.com']
            self.assertEqual(len(payments), 1)
            self.assertEqual(payments[0]['href'], row['url'])
            self.assertNotIn('aria-disabled', payments[0])

    def test_article_links_resolve_and_are_after_article(self):
        for path in (PUBLIC / 'articles').glob('*.html'):
            source = path.read_text()
            if 'data-visualize-standalone' in source or '<main' not in source: continue
            page = Page(); page.feed(source)
            links = [a for tag, a in page.links if tag == 'a' and not urlsplit(a.get('href', '')).scheme and urlsplit(a.get('href', '')).path.startswith('../support')]
            self.assertTrue(links, path)
            for a in links: self.assertTrue((path.parent / urlsplit(a['href']).path).resolve().is_file(), path)
            self.assertLess(source.rfind('</article>'), source.index('reader-support-link'), path)

    def test_local_article_destinations_and_arabic_direction(self):
        destinations = {'pt': 'support.pt-BR.html', 'ko': 'support.ko.html', 'ar': 'support.ar.html'}
        for language, destination in destinations.items():
            for path in (PUBLIC / 'articles').glob('*.' + language + '.html'):
                source = path.read_text()
                self.assertIn('href="../' + destination + '"', source)
        arabic = (PUBLIC / 'support.ar.html').read_text()
        self.assertIn('<html lang="ar" dir="rtl">', arabic)
        self.assertIn('href="tel:+4748448958" dir="ltr"', arabic)
