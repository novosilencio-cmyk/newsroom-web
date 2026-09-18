import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/"public"
BASE="https://experimentalnewsroom.org/"

class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.articles=json.loads((PUBLIC/"content"/"articles.json").read_text(encoding="utf-8"))

    def test_sitemap_and_feed_parse(self):
        ET.parse(PUBLIC/"sitemap.xml"); ET.parse(PUBLIC/"feed.xml")

    def test_every_article_is_discoverable(self):
        sitemap=(PUBLIC/"sitemap.xml").read_text(encoding="utf-8")
        feed=(PUBLIC/"feed.xml").read_text(encoding="utf-8")
        for a in self.articles:
            url=BASE+urlsplit(a["url"]).path
            self.assertIn(url,sitemap)
            self.assertIn(url,feed)

    def test_every_article_has_structured_metadata_after_build(self):
        for a in self.articles:
            path=PUBLIC/urlsplit(a["url"]).path
            text=path.read_text(encoding="utf-8")
            self.assertIn('rel="canonical"',text,path)
            self.assertIn('"@type":"NewsArticle"',text,path)
            self.assertIn('type="application/rss+xml"',text,path)

    def test_ai_search_and_crawler_surfaces(self):
        robots=(PUBLIC/"robots.txt").read_text(encoding="utf-8")
        self.assertIn("OAI-SearchBot",robots)
        self.assertIn("ChatGPT-User",robots)
        self.assertIn("Sitemap: https://experimentalnewsroom.org/sitemap.xml",robots)
        self.assertTrue((PUBLIC/"llms.txt").exists())

    def test_norway_view(self):
        text=(PUBLIC/"norway"/"index.html").read_text(encoding="utf-8")
        self.assertIn("<h2>Norge</h2>",text)
        self.assertIn("Norway",text)

if __name__=="__main__": unittest.main()
