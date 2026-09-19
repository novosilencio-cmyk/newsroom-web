import importlib.util
import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE = "https://experimentalnewsroom.org/"
SPEC = importlib.util.spec_from_file_location("build_discovery", ROOT / "scripts/build_discovery.py")
DISCOVERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISCOVERY)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.jsonld = []
        self.in_json = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_json = False

    def handle_data(self, data):
        if self.in_json:
            self.jsonld.append(json.loads(data))


class ArticleLanguagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stories = json.loads((PUBLIC / "content/articles.json").read_text())
        cls.article = next(a for a in cls.stories if a["id"] == "sierra-leone-school-meals-2026")
        cls.versions = cls.article["translations"]

    def test_each_language_is_indexable_and_switches_to_the_same_story(self):
        self.assertEqual(set(self.versions), {"nb", "en", "fr"})
        for lang, translation in self.versions.items():
            with self.subTest(lang=lang):
                page = Page((PUBLIC / translation["url"]).read_text())
                root = next(attrs for tag, attrs in page.elements if tag == "html")
                self.assertEqual(root["lang"], lang)
                canonical = [attrs["href"] for tag, attrs in page.elements if tag == "link" and attrs.get("rel") == "canonical"]
                self.assertEqual(canonical, [BASE + translation["url"]])
                alternates = {attrs["hreflang"]: attrs["href"] for tag, attrs in page.elements if tag == "link" and "hreflang" in attrs}
                self.assertEqual(alternates, {**{code: BASE + version["url"] for code, version in self.versions.items()}, "x-default": BASE + self.versions["en"]["url"]})
                language_links = [attrs for tag, attrs in page.elements if tag == "a" and "hreflang" in attrs]
                self.assertEqual(len(language_links), 3)
                current = [attrs for attrs in language_links if attrs.get("aria-current") == "page"]
                self.assertEqual([attrs["hreflang"] for attrs in current], [lang])
                for link in language_links:
                    self.assertEqual(link["lang"], link["hreflang"])
                    target = (PUBLIC / translation["url"]).parent / link["href"]
                    self.assertEqual(target.resolve(), (PUBLIC / self.versions[link["lang"]]["url"]).resolve())
                    self.assertNotIn("onclick", link)
                article = next(data for data in page.jsonld if data.get("@type") == "NewsArticle")
                self.assertEqual(article["inLanguage"], [lang])
                self.assertEqual(article["headline"], translation["title"])
                self.assertEqual(article["description"], translation["summary"])
                self.assertEqual(article["mainEntityOfPage"]["@id"], canonical[0])
                rss = [attrs["href"] for tag, attrs in page.elements if attrs.get("type") == "application/rss+xml"]
                self.assertEqual(len(rss), 1)
                self.assertTrue(((PUBLIC / translation["url"]).parent / rss[0]).is_file())

    def test_translations_have_three_sitemap_entries_but_one_story_in_feed(self):
        sitemap = ET.parse(PUBLIC / "sitemap.xml")
        urls = [entry.text for entry in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        for translation in self.versions.values():
            self.assertEqual(urls.count(BASE + translation["url"]), 1)
        feed = ET.parse(PUBLIC / "feed.xml")
        items = [item for item in feed.findall(".//item") if "sierra-leone-school-meals-2026" in item.findtext("link", "")]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].findtext("title"), self.versions["en"]["title"])

    def test_article_available_from_entrances_without_javascript(self):
        for entrance, lang in [("index.html", "en"), ("en/index.html", "en"), ("nb/index.html", "nb")]:
            path = PUBLIC / entrance
            page = Page(path.read_text())
            cards = [attrs for tag, attrs in page.elements if attrs.get("data-article-id") == self.article["id"]]
            self.assertEqual(len(cards), 1)
            targets = {(path.parent / attrs["href"]).resolve() for tag, attrs in page.elements if tag == "a" and "href" in attrs and not attrs["href"].startswith(("http", "#"))}
            for translation in self.versions.values():
                self.assertIn((PUBLIC / translation["url"]).resolve(), targets)

    def test_legacy_articles_keep_their_existing_single_entry(self):
        legacy = {"url": "articles/existing.html", "title": "Existing", "summary": "Existing text"}
        self.assertEqual(DISCOVERY.article_versions(legacy), [legacy])

    def test_translation_paths_cannot_escape_the_public_surface(self):
        for url in ["../../private.txt", "/outside.html", "https://example.com/fr.html", "//example.com/fr.html"]:
            malformed = {"url": url, "translations": {"fr": {"url": url, "title": "Titre", "summary": "Résumé"}}}
            with self.subTest(url=url), self.assertRaises(ValueError):
                DISCOVERY.article_versions(malformed)


if __name__ == "__main__":
    unittest.main()
