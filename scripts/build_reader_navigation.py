"""Reader navigation from the existing publication registry, without network IO."""
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

COUNTRY_ALIASES = {'Norway': 'Norge', 'Brazil': 'Brasil', 'Denmark': 'Danmark', 'United States': 'USA', 'United Kingdom': 'Storbritannia', 'Global economy': 'Verdensøkonomien'}

LANGUAGES = {'nb': 'Norsk', 'en': 'English', 'fr': 'Français'}
# Published reader destinations, deliberately excluding embedded viewers and drafts.
SECTIONS = [
    ('start', 'Start her', 'Start here', [
        ('nb/', 'Norsk forside', 'nb'), ('en/', 'English front page', 'en'),
        ('', 'International front page', 'en'), ('norway/', 'Norge', 'nb')]),
    ('series', 'Serier', 'Series', [
        ('series/institusjon/nb/', 'Institusjon — makt, kunnskap og staten', 'nb'),
        ('series/institusjon/en/', 'Institution — power, knowledge and the state', 'en')]),
    ('art', 'Kunst og Atriet', 'Art and Atriet', [
        ('atriet.html', 'Atriet — et rom som begynner før bygningen', 'nb'),
        ('art/skisse-2005.html', 'Fra strek til relieff', 'nb'),
        ('art/skisse-2005.en.html', 'From line to relief', 'en'),
        ('art/love-me-to-lunch.html', 'Love me to lunch', 'nb'),
        ('art/love-me-to-lunch.en.html', 'Love me to lunch', 'en')]),
    ('learning', 'Kurs og deltakelse', 'Courses and participation', [
        ('courses/', 'Free writing courses', 'en'),
        ('courses/course-of-the-day.html', 'Daily writing practice', 'en'),
        ('courses/write-vividly-without-inventing.html', 'Write vividly without inventing', 'en'),
        ('courses/news-entry-public-facts.html', 'News entry and public facts', 'en'),
        ('opportunities/writing-course-pilot.html', 'Writing course pilot', 'en')]),
    ('about', 'Om redaksjonen', 'About the newsroom', [
        ('index.html#about', 'About us', 'en'),
        ('how-we-work.html', 'How we work', 'en'),
        ('recognition/', 'Anerkjennelse', 'nb'),
        ('recognition/rcf-sci-2026-09-14.html', 'Felles innsats, synlige bidrag', 'nb')]),
    ('support', 'Støtt arbeidet', 'Support the work', [
        ('support.html', 'Support the work', 'en'),
        ('support-terms.html', 'Avtalevilkår for støtte', 'nb'),
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
    title = 'Finn frem' if no else 'Find your way'
    filename = 'sitemap.html' if no else 'sitemap.en.html'
    intro = ('Finn saker, serier, kunst og kurs. Språk er merket ved lenkene.' if no else
             'Explore stories, series, art and courses. Reading languages are shown beside the links.')
    jump = [('stories', 'Alle saker' if no else 'All stories')] + [(s[0], s[1] if no else s[2]) for s in SECTIONS]
    groups = []
    rows = []
    for a in sorted(articles, key=lambda a: (a['published'], -a.get('priority', 999)), reverse=True):
        vv = versions(public, a)
        chosen = next((v for v in vv if v['language'] == lang), vv[0])
        aliases = ' '.join(nb for en, nb in COUNTRY_ALIASES.items() if en in a.get('country', ''))
        search = ' '.join([aliases, a.get('country', ''), a.get('region', '')] + [v['title'] + ' ' + v.get('summary', '') for v in vv])
        links = ' '.join(f'<a href="{escape(v["url"])}" lang="{escape(v["language"])}" hreflang="{escape(v["language"])}">{escape(LANGUAGES.get(v["language"], v["language"]))}</a>' for v in vv)
        rows.append(f'''<li class="map-entry" data-search="{escape(search)}" data-languages="{' '.join(escape(v['language']) for v in vv)}">
<p class="map-meta"><span lang="en">{escape(a.get('country', ''))}</span> · <time datetime="{escape(a['published'][:10])}">{escape(a['published'][:10])}</time></p>
<h3 lang="{escape(chosen['language'])}"><a href="{escape(chosen['url'])}">{escape(chosen['title'])}</a></h3>
<p class="map-summary" lang="{escape(chosen['language'])}">{escape(chosen.get('summary', ''))}</p>
<p class="map-languages"><span>{'Les på' if no else 'Read in'}</span> {links}</p></li>''')
    groups.append(f'<section class="map-section" id="stories" aria-labelledby="stories-heading"><h2 id="stories-heading">{jump[0][1]}</h2><ul class="map-list map-stories">' + '\n'.join(rows) + '</ul></section>')
    for key, nb, en, entries in SECTIONS:
        rows = []
        for url, label, language in entries:
            local_file(public, url)
            rows.append(f'<li class="map-entry map-page" data-search="{escape(label + " " + nb + " " + en)}" data-languages="{language}"><a href="{escape(url or "./")}" lang="{language}" hreflang="{language}">{escape(label)}</a> <span class="map-page-language" lang="{language}">{LANGUAGES[language]}</span></li>')
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
<script src="reader-navigation.js" defer></script>
</head>
<body class="reader-map">
<a class="reader-skip" href="#main">{'Gå til innholdet' if no else 'Skip to content'}</a>
<header class="map-masthead"><a class="map-brand" href="{'nb/' if no else 'en/'}">Experimental Newsroom</a>
<nav aria-label="{'Språk' if no else 'Language'}"><a href="sitemap.html" lang="nb" hreflang="nb"{' aria-current="page"' if no else ''}>Norsk</a><a href="sitemap.en.html" lang="en" hreflang="en"{'' if no else ' aria-current="page"'}>English</a></nav></header>
<main id="main" tabindex="-1">
<section class="map-intro"><p class="kicker">{'Nettstedskart' if no else 'Site map'}</p><h1>{title}</h1><p class="map-deck">{intro}</p></section>
<form class="map-search" role="search" hidden>
<div class="map-search-field"><label for="map-query">{'Søk i oversikten' if no else 'Search this guide'}</label><input id="map-query" type="search" autocomplete="off" aria-describedby="map-help" placeholder="{'Prøv skolemat, Taiwan eller kunst' if no else 'Try school meals, Taiwan or art'}"/></div>
<div class="map-language-field"><label for="map-language">{'Lesespråk' if no else 'Reading language'}</label><select id="map-language"><option value="">{'Alle språk' if no else 'All languages'}</option><option value="nb">Norsk</option><option value="en">English</option><option value="fr">Français</option></select></div>
<button type="reset">{'Vis alt' if no else 'Show all'}</button>
<p id="map-help">{'Søker i titler, korte beskrivelser og landnavn i denne oversikten.' if no else 'Searches titles, short descriptions and country names in this guide.'}</p>
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
        path.write_text(source, encoding='utf-8')


def build_reader_navigation(public, articles):
    for lang, filename in [('nb', 'sitemap.html'), ('en', 'sitemap.en.html')]:
        (public / filename).write_text(render(public, articles, lang), encoding='utf-8')
    enhance_pages(public)
