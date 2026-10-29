"""Reader navigation from the existing publication registry, without network IO."""
import html
import hashlib
import re
from build_reader_support import support_data
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, quote

COUNTRY_ALIASES = {'Norway': 'Norge', 'Brazil': 'Brasil', 'Denmark': 'Danmark', 'Germany': 'Tyskland', 'Japan': 'Japan', 'United States': 'USA', 'United Kingdom': 'Storbritannia England', 'Global economy': 'Verdensøkonomien'}

LANGUAGES = {'nb': 'Norsk', 'en': 'English', 'fr': 'Français', 'de': 'Deutsch', 'ja': '日本語', 'ko': '한국어', 'zh-Hans': '简体中文', 'es': 'Español', 'es-AR': 'Español (Argentina)', 'zh-Hant': '繁體中文', 'pt': 'Português', 'pt-BR': 'Português (Brasil)', 'ar': 'العربية'}
# Published reader destinations, deliberately excluding embedded viewers and drafts.
SECTIONS = [
    ('start', 'Start her', 'Start here', [
        ('nb/', 'Norsk forside', 'nb'), ('en/', 'English front page', 'en'),
        ('', 'International front page', 'en'), ('norway/', 'Norge', 'nb')]),
    ('series', 'Serier', 'Series', [
        ('series/virkemidlene/nb/', 'Virkemidlene — økonomi, virkning og fordeling', 'nb'),
        ('series/institusjon/nb/', 'Institusjon — makt, kunnskap og staten', 'nb'),
        ('series/institusjon/en/', 'Institution — power, knowledge and the state', 'en')]),
    ('art', 'Kunst', 'Art', [
        ('art/skisse-2005.html', 'Skisse fra 2005', 'nb'),
        ('art/skisse-2005.en.html', 'Sketch from 2005', 'en'),
        ('art/love-me-to-lunch.html', 'Love me to lunch', 'nb'),
        ('art/love-me-to-lunch.en.html', 'Love me to lunch', 'en')]),
    ('atriet', 'Atriet', 'Atriet', [('atriet.html', 'Atriet — et rom som begynner før bygningen', 'nb')]),
    ('learning', 'Kurs og deltakelse', 'Courses and participation', [
        ('courses/', 'Free writing courses', 'en'),
        ('courses/course-of-the-day.html', 'Daily writing practice', 'en'),
        ('courses/write-vividly-without-inventing.html', 'Write vividly without inventing', 'en'),
        ('courses/news-entry-public-facts.html', 'News entry and public facts', 'en')]),
    ('words', 'Ord og sammenhenger', 'Words and connections', [('ord-og-sammenhenger.html', 'Ord og sammenhenger — verdi og vurdering', 'nb')]),
    ('about', 'Om redaksjonen', 'About the newsroom', [
        ('index.html#about', 'About us', 'en'),
        ('how-we-work.html', 'How we work', 'en'),
        ('manifest.html', 'Hvorfor vi skriver — manifest', 'nb'),
        ('manifest.en.html', 'Why we write — manifesto', 'en'),
        ('recognition/', 'Anerkjennelse', 'nb'),
        ('recognition/rcf-sci-2026-09-14.html', 'Felles innsats, synlige bidrag', 'nb')]),
    ('support', 'Støtt arbeidet', 'Support the work', [
        ('support.html', 'Støtt journalistikken', 'nb'),
        ('support.en.html', 'Support independent journalism', 'en'),
        ('support.fr.html', 'Soutenir un journalisme indépendant', 'fr'),
        ('support.es.html', 'Apoyá el periodismo independiente', 'es-AR'),
        ('support.de.html', 'Unabhängigen Journalismus unterstützen', 'de'),
        ('support.zh-Hans.html', '支持独立新闻报道', 'zh-Hans'),
        ('support.zh-Hant.html', '支持獨立新聞報導', 'zh-Hant'),
        ('support.ja.html', '独立した報道を支える', 'ja'),
        ('support.pt-BR.html', 'Apoie o jornalismo independente', 'pt-BR'),
        ('support.ko.html', '독립적인 언론 활동을 후원해 주세요', 'ko'),
        ('support.ar.html', 'ادعم الصحافة المستقلة', 'ar'),
        ('subscription-terms.html', 'Abonnementsvilkår og angreskjema', 'nb'),
        ('subscription-terms.en.html', 'Subscription terms and withdrawal form', 'en'),
        ('support-terms.html', 'Vilkår for tidligere engangsstøtte', 'nb'),
        ('privacy.html', 'Personvern', 'nb')]),
]


def escape(value):
    return html.escape(str(value), quote=True)


def local_file(public, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or parsed.path.startswith('/') or '..' in parsed.path.split('/'):
        raise ValueError(f'Expected a local publication URL: {url}')
    path = public / parsed.path
    if not parsed.path or parsed.path.endswith('/'):
        path = path / 'index.html'
    if not path.is_file():
        raise ValueError(f'Missing reader destination: {url}')
    return path


class StoryText(HTMLParser):
    """Read existing language-panel titles/decks; never invent translations."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.language = 'en'
        self.panel = None
        self.capture = None
        self.buffer = []
        self.panels = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang', 'en')
        if 'data-language-panel' in attrs:
            self.panel = attrs['data-language-panel']
            self.panels[self.panel] = {}
        if self.panel and (tag == 'h1' or (tag == 'p' and 'deck' in attrs.get('class', '').split())):
            self.capture = tag
            self.buffer = []

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == self.capture:
            self.panels[self.panel]['title' if tag == 'h1' else 'summary'] = ' '.join(''.join(self.buffer).split())
            self.capture = None
        if tag == 'article':
            self.panel = None


class SearchText(HTMLParser):
    """Index published main text, excluding code, styling and navigation."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main = 0
        self.excluded = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'main': self.main += 1
        if tag in ('script', 'style', 'nav'): self.excluded += 1

    def handle_endtag(self, tag):
        if tag == 'main': self.main = max(0, self.main - 1)
        if tag in ('script', 'style', 'nav'): self.excluded = max(0, self.excluded - 1)

    def handle_data(self, data):
        if self.main and not self.excluded: self.parts.append(data)


def searchable_text(public, url):
    parser = SearchText()
    parser.feed(local_file(public, url).read_text(encoding='utf-8'))
    return ' '.join(' '.join(parser.parts).split())


def topic_labels(article, lang):
    return article.get('tags', {}).get(lang, [])


def versions(public, article):
    if article.get('translations'):
        out = [{'language': lang, **value} for lang, value in article['translations'].items()]
        for v in out:
            local_file(public, v['url'])
        return out
    path = local_file(public, article['url'])
    parser = StoryText()
    parser.feed(path.read_text(encoding='utf-8'))
    if 'no' in parser.panels and 'en' in parser.panels:
        out = []
        for panel, lang, fragment in [('no', 'nb', 'norsk'), ('en', 'en', 'english')]:
            value = parser.panels[panel]
            if not value.get('title') or not value.get('summary'):
                raise ValueError(f'Missing existing panel title/deck: {path} {panel}')
            out.append({'language': lang, 'url': f'{urlsplit(article["url"]).path}?lang={panel}#{fragment}', **value})
        return out
    return [{'language': parser.language, 'url': article['url'], 'title': article['title'], 'summary': article['summary']}]


def render(public, articles, lang):
    no = lang == 'nb'
    script_version = hashlib.sha256((public / 'reader-navigation.js').read_bytes()).hexdigest()[:12]
    title = 'Finn frem' if no else 'Find your way'
    filename = 'sitemap.html' if no else 'sitemap.en.html'
    intro = ('Finn saker, serier, kunst, Atriet og kurs. Språk er merket ved lenkene.' if no else
             'Explore stories, series, art, Atriet and courses. Reading languages are shown beside the links.')
    jump = [('stories', 'Alle saker' if no else 'All stories')] + [(s[0], s[1] if no else s[2]) for s in SECTIONS]
    groups = []
    rows = []
    for a in sorted(articles, key=lambda a: (a['published'], -a.get('priority', 999)), reverse=True):
        vv = versions(public, a)
        chosen = next((v for v in vv if v['language'] == lang), vv[0])
        aliases = ' '.join(nb for en, nb in COUNTRY_ALIASES.items() if en in a.get('country', ''))
        tags = topic_labels(a, 'nb') + topic_labels(a, 'en')
        search = ' '.join([aliases, a.get('country', ''), a.get('region', ''), ' '.join(tags)] + [v['title'] + ' ' + v.get('summary', '') + ' ' + searchable_text(public, v['url']) for v in vv])
        tag_links = ' · '.join(f'<a href="{filename}?q={escape(quote(tag))}">{escape(tag)}</a>' for tag in topic_labels(a, lang))
        links = ' '.join(f'<a href="{escape(v["url"])}" lang="{escape(v["language"])}" hreflang="{escape(v["language"])}">{escape(LANGUAGES.get(v["language"], v["language"]))}</a>' for v in vv)
        rows.append(f'''<li class="map-entry" data-search="{escape(search)}" data-languages="{' '.join(escape(v['language']) for v in vv)}">
<p class="map-meta"><span lang="en">{escape(a.get('country', ''))}</span> · <time datetime="{escape(a['published'][:10])}">{escape(a['published'][:10])}</time></p>
<h3 lang="{escape(chosen['language'])}"><a href="{escape(chosen['url'])}">{escape(chosen['title'])}</a></h3>
<p class="map-summary" lang="{escape(chosen['language'])}">{escape(chosen.get('summary', ''))}</p>
<p class="map-tags">{tag_links}</p>
<p class="map-languages"><span>{'Les på' if no else 'Read in'}</span> {links}</p></li>''')
    groups.append(f'<section class="map-section" id="stories" aria-labelledby="stories-heading"><h2 id="stories-heading">{jump[0][1]}</h2><ul class="map-list map-stories">' + '\n'.join(rows) + '</ul></section>')
    for key, nb, en, entries in SECTIONS:
        rows = []
        for url, label, language in entries:
            local_file(public, url)
            rows.append(f'<li class="map-entry map-page" data-search="{escape(label + " " + nb + " " + en + " " + searchable_text(public, url))}" data-languages="{language}"><a href="{escape(url or "./")}" lang="{language}" hreflang="{language}">{escape(label)}</a> <span class="map-page-language" lang="{language}">{LANGUAGES[language]}</span></li>')
        groups.append(f'<section class="map-section" id="{key}" aria-labelledby="{key}-heading"><h2 id="{key}-heading">{escape(nb if no else en)}</h2><ul class="map-list">' + '\n'.join(rows) + '</ul></section>')
    jumps = ' '.join(f'<a href="#{key}">{label}</a>' for key, label in jump)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} — {'Nettstedskart' if no else 'Site map'} | Experimental Newsroom</title>
<meta name="description" content="{escape(intro)}"/>
<link rel="canonical" href="https://experimentalnewsroom.org/{filename}"/>
<link rel="alternate" hreflang="nb" href="https://experimentalnewsroom.org/sitemap.html"/>
<link rel="alternate" hreflang="en" href="https://experimentalnewsroom.org/sitemap.en.html"/>
<link rel="stylesheet" href="styles.css"/><link rel="stylesheet" href="reader-navigation.css"/>
<link rel="icon" href="favicon.svg" type="image/svg+xml"/>
<script src="reader-navigation.js?v={script_version}" defer></script>
</head>
<body class="reader-map">
<a class="reader-skip" href="#main">{'Gå til innholdet' if no else 'Skip to content'}</a>
<header class="map-masthead"><a class="map-brand" href="{'nb/' if no else 'en/'}">Experimental Newsroom</a>
<nav aria-label="{'Språk' if no else 'Language'}"><a href="sitemap.html" lang="nb" hreflang="nb"{' aria-current="page"' if no else ''}>Norsk</a><a href="sitemap.en.html" lang="en" hreflang="en"{'' if no else ' aria-current="page"'}>English</a></nav></header>
<main id="main" tabindex="-1">
<section class="map-intro"><p class="kicker">{'Nettstedskart' if no else 'Site map'}</p><h1>{title}</h1><p class="map-deck">{intro}</p></section>
<form class="map-search" role="search" hidden>
<div class="map-search-field"><label for="map-query">{'Søk i oversikten' if no else 'Search this guide'}</label><input id="map-query" type="search" autocomplete="off" aria-describedby="map-help" placeholder="{'Prøv skolemat, Taiwan eller kurs' if no else 'Try school meals, Taiwan or courses'}"/></div>
<div class="map-language-field"><label for="map-language">{'Lesespråk' if no else 'Reading language'}</label><select id="map-language"><option value="">{'Alle språk' if no else 'All languages'}</option><option value="nb">Norsk</option><option value="en">English</option><option value="fr">Français</option><option value="de">Deutsch</option><option value="ja">日本語</option><option value="ko">한국어</option><option value="zh-Hans">简体中文</option><option value="es-AR">Español (Argentina)</option><option value="zh-Hant">繁體中文</option><option value="pt">Português</option><option value="pt-BR">Português (Brasil)</option><option value="ar">العربية</option></select></div>
<button type="reset">{'Vis alt' if no else 'Show all'}</button>
<p id="map-help">{'Søker i publiserte tekster, titler, emneord og landnavn. Velg et emneord for å finne beslektede saker.' if no else 'Searches published texts, titles, topics and country names. Choose a topic to find related stories.'}</p>
<p id="map-results" role="status" aria-live="polite" aria-atomic="true"></p>
</form>
<nav class="map-jumps" aria-label="{'Deler av nettstedskartet' if no else 'Site map sections'}">{jumps}</nav>
<p id="map-empty" hidden>{'Ingen treff. Prøv et kortere søkeord, velg et annet språk eller trykk «Vis alt».' if no else 'No matches. Try a shorter search, choose another language or select “Show all”.'}</p>
<div class="map-content">{''.join(groups)}</div>
</main>
<footer><p>Experimental Newsroom · <a href="{'nb/' if no else 'en/'}">{'Forsiden' if no else 'Front page'}</a> · <a href="feed.xml">RSS</a> · <a href="sitemap.xml">XML sitemap</a></p></footer>
</body></html>
'''


def enhance_pages(public):
    """Small idempotent shell additions; article bodies and existing anchors survive."""
    support = support_data(public)
    for path in sorted(public.rglob('*.html')):
        source = path.read_text(encoding='utf-8')
        if 'data-visualize-standalone' in source or path.name in ('sitemap.html', 'sitemap.en.html'):
            continue
        if not re.search(r'<main\b', source):
            continue
        lang_match = re.search(r'<html[^>]*\blang=["\']([^"\']+)', source)
        lang = lang_match.group(1) if lang_match else 'en'
        no = lang in ('nb', 'no')
        skip = 'Gå til innholdet' if no else ('Aller au contenu' if lang == 'fr' else 'Skip to content')
        label = 'Finn frem' if no else ('Plan du site (en anglais)' if lang == 'fr' else 'Find your way')
        prefix = '../' * (len(path.relative_to(public).parts) - 1)
        support_lang = 'nb' if no else ('es-AR' if lang.startswith('es') else ('pt-BR' if lang.startswith('pt') else lang))
        support_row = support.get(support_lang, support['en'])
        support_target = prefix + support_row['file']
        support_label = support_row['title']
        target = prefix + ('sitemap.html' if no else 'sitemap.en.html')
        if 'reader-navigation.css' not in source:
            source = source.replace('</head>', f'<link href="{prefix}reader-navigation.css" rel="stylesheet"/>\n</head>', 1)
        main = re.search(r'<main\b[^>]*>', source).group()
        match = re.search(r'\bid=["\']([^"\']+)', main)
        main_id = match.group(1) if match else 'reader-main'
        newmain = main
        if not match:
            newmain = newmain[:-1] + f' id="{main_id}">'
        if 'tabindex=' not in newmain:
            newmain = newmain[:-1] + ' tabindex="-1">'
        source = source.replace(main, newmain, 1)
        if not re.search(r'class=["\'][^"\']*(?:skip-link|reader-skip)', source):
            source = re.sub(r'(<body\b[^>]*>)', rf'\1\n<a class="reader-skip" href="#{main_id}">{skip}</a>', source, count=1)
        # Replace the old reader-facing XML link; XML stays available in the map.
        source = re.sub(r'<a href="(?:\.\./)*sitemap\.xml">Sitemap</a>', f'<a href="{target}">{label}</a>', source)
        if target not in source:
            link = f'<p class="reader-map-link"><a href="{target}">{label}</a></p>'
            at = source.rfind('</footer>')
            if at >= 0:
                source = source[:at] + link + source[at:]
            else:
                source = source.replace('</body>', f'<footer>{link}</footer>\n</body>', 1)
        # One extra entry at the three main entrances; other pages have the footer.
        if path.relative_to(public).as_posix() in ('index.html', 'nb/index.html', 'en/index.html'):
            nav = re.search(r'<nav\b[^>]*>.*?</nav>', source, re.S)
            if nav and target not in nav.group():
                source = source[:nav.start()] + nav.group().replace('</nav>', f'<a href="{target}">{label}</a></nav>') + source[nav.end():]
        rel = path.relative_to(public).as_posix()
        if rel in ('index.html', 'nb/index.html', 'en/index.html'):
            nav = re.search(r'<nav\b[^>]*>.*?</nav>', source, re.S)
            if nav:
                newnav = re.sub(r'<a href="(?:\.\./)?support(?:\.en)?\.html"[^>]*>.*?</a>', '', nav.group())
                code = support_lang if support_lang in support else 'en'
                newnav = newnav.replace('</nav>', f'<a href="{support_target}" lang="{code}">{escape(support_label)}</a></nav>')
                source = source[:nav.start()] + newnav + source[nav.end():]
        if rel.startswith('articles/'):
            code = support_lang if support_lang in support else 'en'
            link = f'<p class="reader-support-link"><a href="{support_target}" lang="{code}">{escape(support_label)} →</a></p>'
            if 'reader-support-link' in source:
                source = re.sub(r'<p class="reader-support-link">.*?</p>', link, source)
            else:
                source = source.replace('</main>', link + '\n</main>', 1)
            if 'reader-support.css' not in source:
                source = source.replace('</head>', f'<link href="{prefix}reader-support.css" rel="stylesheet"/>\n</head>', 1)
        path.write_text(source, encoding='utf-8')


def build_reader_navigation(public, articles):
    enhance_pages(public)
    for lang, filename in [('nb', 'sitemap.html'), ('en', 'sitemap.en.html')]:
        (public / filename).write_text(render(public, articles, lang), encoding='utf-8')
