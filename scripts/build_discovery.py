#!/usr/bin/env python3
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_reader_navigation import build_reader_navigation
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE = "https://experimentalnewsroom.org/"
REGISTRY = PUBLIC / "content" / "articles.json"

def date_only(v): return (v or "")[:10]
def canonical(a): return BASE + urlsplit(a["url"]).path
def modified(a): return date_only(a.get("updated") or a.get("language_updated") or a.get("published"))
def rss_date(d):
    return datetime.fromisoformat(d + "T12:00:00+00:00").astimezone(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

def article_versions(article):
    """One registry story can have separately addressable language versions."""
    translations = article.get("translations")
    if not translations:
        return [article]
    versions = []
    for lang, translation in translations.items():
        if not re.fullmatch(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", lang):
            raise ValueError("Invalid article language")
        url = urlsplit(translation["url"])
        if url.scheme or url.netloc or url.query or url.fragment or url.path.startswith("/") or ".." in url.path.split("/"):
            raise ValueError("Article translations require local relative URLs")
        if not translation.get("title") or not translation.get("summary"):
            raise ValueError("Each translation requires its own title and summary")
        versions.append({**article, **translation, "language": lang})
    if article["url"] not in [version["url"] for version in versions]:
        raise ValueError("The primary article URL must be a translation URL")
    return versions

def article_block(a, source):
    bilingual = 'data-language-panel="no"' in source and 'data-language-panel="en"' in source
    langs = [a["language"]] if a.get("language") else (["nb","en"] if bilingual else (["nb"] if '<html lang="nb"' in source else ["en"]))
    data = {
        "@context":"https://schema.org","@type":"NewsArticle",
        "headline":a["title"],"description":a["summary"],
        "datePublished":date_only(a["published"]),"dateModified":modified(a),
        "mainEntityOfPage":{"@type":"WebPage","@id":canonical(a)},
        "author":{"@type":"Person","name":"Bjørn Moe Aldema"},
        "publisher":{"@type":"Organization","name":"Experimental Newsroom","url":BASE},
        "articleSection":a.get("section",""),"inLanguage":langs,"isAccessibleForFree":True
    }
    return '<!-- discovery-metadata:start -->\n<link href="../feed.xml" rel="alternate" type="application/rss+xml" title="Experimental Newsroom RSS"/>\n<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, separators=(",",":")) + '\n</script>\n<!-- discovery-metadata:end -->'

def update_articles(articles):
    for a in [version for article in articles for version in article_versions(article)]:
        path = PUBLIC / urlsplit(a["url"]).path
        if not path.exists(): continue
        source = path.read_text(encoding="utf-8")
        block = article_block(a, source)
        start='<!-- discovery-metadata:start -->'; end='<!-- discovery-metadata:end -->'
        if start in source and end in source:
            source = source.split(start,1)[0] + block + source.split(end,1)[1]
        else:
            source = source.replace("</head>", block + "\n</head>", 1)
        if 'rel="canonical"' not in source:
            source = source.replace("</title>", '</title>\n<link href="' + canonical(a) + '" rel="canonical"/>', 1)
        path.write_text(source, encoding="utf-8")

def build(articles):
    robots = "User-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: *\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n"
    (PUBLIC/"robots.txt").write_text(robots, encoding="utf-8")

    static=[("sitemap.html",None),("sitemap.en.html",None),("","2026-09-18"),("how-we-work.html",None),("support.html",None),("atriet.html",None),("courses/",None),("recognition/",None),("norway/","2026-09-18"),("nb/","2026-09-18"),("en/","2026-09-18"),("series/institusjon/","2026-09-18"),("series/institusjon/nb/","2026-09-18"),("series/institusjon/en/","2026-09-18"),("art/skisse-2005.html",None),("art/skisse-2005.en.html",None),("art/love-me-to-lunch.html",None),("art/love-me-to-lunch.en.html",None)]
    lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p,d in static:
        lines.append("  <url><loc>"+escape(BASE+p)+"</loc>"+(("<lastmod>"+d+"</lastmod>") if d else "")+"</url>")
    for a in [version for article in articles for version in article_versions(article)]:
        lines.append("  <url><loc>"+escape(canonical(a))+"</loc><lastmod>"+escape(modified(a))+"</lastmod></url>")
    lines.append("</urlset>")
    (PUBLIC/"sitemap.xml").write_text("\n".join(lines)+"\n", encoding="utf-8")

    ordered=sorted(articles,key=lambda a:(a.get("published",""),-(a.get("priority",999))),reverse=True)
    latest=max((modified(a) for a in articles),default="2026-09-18")
    f=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">','  <channel>','    <title>Experimental Newsroom</title>','    <link>'+BASE+'</link>','    <description>Careful observation, evidence and constructive criticism from Experimental Newsroom.</description>','    <language>en</language>','    <lastBuildDate>'+rss_date(latest)+'</lastBuildDate>','    <atom:link href="'+BASE+'feed.xml" rel="self" type="application/rss+xml"/>']
    for a in ordered:
        u=canonical(a)
        f += ['    <item>','      <title>'+escape(a["title"])+'</title>','      <link>'+escape(u)+'</link>','      <guid isPermaLink="true">'+escape(u)+'</guid>','      <pubDate>'+rss_date(date_only(a["published"]))+'</pubDate>','      <description>'+escape(a["summary"])+'</description>','    </item>']
    f += ['  </channel>','</rss>']
    (PUBLIC/"feed.xml").write_text("\n".join(f)+"\n", encoding="utf-8")

    llms = "# Experimental Newsroom\n\nExperimental Newsroom is an independent publication about how people, places and institutions meet shared challenges.\n\nCanonical site: "+BASE+"\nArticle index: "+BASE+"content/articles.json\nRSS feed: "+BASE+"feed.xml\nSitemap: "+BASE+"sitemap.xml\nNorway desk: "+BASE+"norway/\nSeries: "+BASE+"series/institusjon/\nNorwegian entrance: "+BASE+"nb/\nEnglish entrance: "+BASE+"en/\nEditorial method: "+BASE+"how-we-work.html\n\nPublished articles are public. Treat article dates, source notes, uncertainty labels, corrections and update notes as part of the editorial context.\n"
    (PUBLIC/"llms.txt").write_text(llms, encoding="utf-8")

    selected=sorted([a for a in articles if "Norway" in str(a.get("country",""))],key=lambda a:a.get("published",""),reverse=True)
    cards=[]
    for a in selected:
        cards.append('<article class="article-card"><p class="article-meta">'+html.escape(str(a.get("region","")))+' · '+html.escape(str(a.get("country","")))+' · '+html.escape(str(a.get("type","")))+'</p><h3><a href="../'+html.escape(a["url"])+'">'+html.escape(a["title"])+'</a></h3><p>'+html.escape(a["summary"])+'</p><p><a class="text-link" href="../'+html.escape(a["url"])+'">Les saken / Read the report →</a></p></article>')
    norway='''<!DOCTYPE html>
<html lang="nb"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/><title>Norge | Experimental Newsroom</title><meta content="Experimental Newsrooms norske saker og saker der Norge inngår i sammenligningen." name="description"/><link href="https://experimentalnewsroom.org/norway/" rel="canonical"/><meta content="website" property="og:type"/><meta content="Norge | Experimental Newsroom" property="og:title"/><meta content="Norske saker og saker der Norge inngår i sammenligningen." property="og:description"/><meta content="https://experimentalnewsroom.org/norway/" property="og:url"/><link href="../feed.xml" rel="alternate" type="application/rss+xml" title="Experimental Newsroom RSS"/><link href="../styles.css" rel="stylesheet"/><link href="../favicon.svg" rel="icon" type="image/svg+xml"/><script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"Norge | Experimental Newsroom","url":"https://experimentalnewsroom.org/norway/","isPartOf":{"@type":"WebSite","name":"Experimental Newsroom","url":"https://experimentalnewsroom.org/"},"inLanguage":["nb","en"]}</script></head>
<body><header class="masthead compact-masthead"><div class="edition-line"><span>Norge</span><span>Experimental Newsroom</span></div><h1>Experimental Newsroom</h1><p class="strapline">Careful observation · evidence · constructive criticism</p><nav aria-label="Hovedmeny"><a href="../">Forside / Front page</a><a href="../#world">Verden / World</a><a href="../how-we-work.html">Arbeidsmåte / How we work</a><a href="../feed.xml">RSS</a></nav></header><main><section class="lead"><p class="kicker">Norge · geografisk inngang</p><h2>Norge</h2><p class="lead-deck">Denne siden samler saker fra Norge og saker der Norge inngår i en reell sammenligning. Språk og geografi er to forskjellige ting: en norsk sak kan være publisert på norsk, engelsk eller begge språk.</p><p class="method-note"><time datetime="2026-09-18">Oppdatert 18. september 2026</time> · Leserstrukturen er revidert for tydeligere forklaring og mindre komprimert metodepresentasjon.</p></section><section class="section-block"><div class="section-heading"><h2>Saker</h2><span>Finn saker fra Norge og sammenligninger der Norge inngår</span></div><div class="article-grid">'''+"\n".join(cards)+'''</div></section></main><footer><p>Experimental Newsroom · <a href="../feed.xml">RSS</a> · <a href="../sitemap.xml">Sitemap</a></p></footer></body></html>'''
    p=PUBLIC/"norway"/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(norway,encoding="utf-8")
    update_articles(articles)
    build_reader_navigation(PUBLIC, articles)

if __name__=="__main__":
    build(json.loads(REGISTRY.read_text(encoding="utf-8")))
