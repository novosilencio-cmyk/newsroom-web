import importlib.util
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE = "https://experimentalnewsroom.org/"
sys.path.insert(0, str(ROOT / "scripts"))
from language_registry import direction
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
        cls.translated = [article for article in cls.stories if article.get("translations")]

    def test_each_language_is_indexable_and_switches_to_the_same_story(self):
        self.assertTrue(self.translated)
        for source in self.translated:
            versions = source["translations"]
            fallback = versions.get("en") or next(
                version for version in versions.values() if version["url"] == source["url"]
            )
            for lang, translation in versions.items():
                with self.subTest(article=source["id"], lang=lang):
                    page = Page((PUBLIC / translation["url"]).read_text())
                    root = next(attrs for tag, attrs in page.elements if tag == "html")
                    self.assertEqual(root["lang"], lang)
                    if direction(lang) == "rtl":
                        self.assertEqual(root.get("dir"), "rtl")
                    canonical = [attrs["href"] for tag, attrs in page.elements if tag == "link" and attrs.get("rel") == "canonical"]
                    self.assertEqual(canonical, [BASE + translation["url"]])
                    alternates = {attrs["hreflang"]: attrs["href"] for tag, attrs in page.elements if tag == "link" and "hreflang" in attrs}
                    self.assertEqual(alternates, {**{code: BASE + version["url"] for code, version in versions.items()}, "x-default": BASE + fallback["url"]})
                    language_links = [attrs for tag, attrs in page.elements if tag == "a" and "hreflang" in attrs]
                    self.assertEqual(len(language_links), len(versions))
                    current = [attrs for attrs in language_links if attrs.get("aria-current") == "page"]
                    self.assertEqual([attrs["hreflang"] for attrs in current], [lang])
                    for link in language_links:
                        self.assertEqual(link["lang"], link["hreflang"])
                        target = (PUBLIC / translation["url"]).parent / link["href"]
                        self.assertEqual(target.resolve(), (PUBLIC / versions[link["lang"]]["url"]).resolve())
                        self.assertNotIn("onclick", link)
                    article = next(data for data in page.jsonld if data.get("@type") == "NewsArticle")
                    self.assertEqual(article["inLanguage"], [lang])
                    self.assertEqual(article["headline"], translation["title"])
                    self.assertEqual(article["description"], translation["summary"])
                    self.assertEqual(article["mainEntityOfPage"]["@id"], canonical[0])
                    rss = [attrs["href"] for tag, attrs in page.elements if attrs.get("type") == "application/rss+xml"]
                    self.assertEqual(len(rss), 1)
                    self.assertTrue(((PUBLIC / translation["url"]).parent / rss[0]).is_file())

    def test_translations_have_one_sitemap_entry_per_language_but_one_story_in_feed(self):
        sitemap = ET.parse(PUBLIC / "sitemap.xml")
        urls = [entry.text for entry in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        feed = ET.parse(PUBLIC / "feed.xml")
        for article in self.translated:
            with self.subTest(article=article["id"]):
                for translation in article["translations"].values():
                    self.assertEqual(urls.count(BASE + translation["url"]), 1)
                items = [item for item in feed.findall(".//item") if item.findtext("link") == BASE + article["url"]]
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0].findtext("title"), article["title"])

    def test_article_available_from_entrances_without_javascript(self):
        for article in self.translated:
            version_targets = {(PUBLIC / version["url"]).resolve() for version in article["translations"].values()}
            for entrance in ("index.html", "en/index.html", "nb/index.html"):
                with self.subTest(article=article["id"], entrance=entrance):
                    path = PUBLIC / entrance
                    page = Page(path.read_text())
                    cards = [attrs for tag, attrs in page.elements if attrs.get("data-article-id") == article["id"]]
                    self.assertEqual(len(cards), 1)
                    targets = {(path.parent / attrs["href"]).resolve() for tag, attrs in page.elements if tag == "a" and "href" in attrs and not attrs["href"].startswith(("http", "#"))}
                    self.assertTrue(version_targets.intersection(targets))

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
