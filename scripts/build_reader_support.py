"""Build explicit reader-support language pages from reviewed copy; no network I/O."""
import json
from html import escape
from urllib.parse import urlsplit

BASE = 'https://experimentalnewsroom.org/'

def support_data(public):
    data = json.loads((public / 'content/reader-support.json').read_text(encoding='utf-8'))
    for lang, row in data.items():
        if '/' in row['file'] or not row['file'].startswith('support'):
            raise ValueError('Invalid support page filename')
        url = urlsplit(row['url'])
        if url.scheme != 'https' or url.netloc != 'donate.stripe.com':
            raise ValueError('Support payment links must use the verified Stripe host')
    return data

def build_reader_support(public):
    data = support_data(public)
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{row["file"]}"/>' for lang, row in data.items())
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{data["en"]["file"]}"/>'
    for lang, s in data.items():
        e = lambda key: escape(s[key], quote=True)
        languages = ' '.join(f'<a href="{row["file"]}" lang="{code}" hreflang="{code}"' + (' aria-current="page"' if code == lang else '') + f'>{escape(row["name"])}</a>' for code, row in data.items())
        home = 'nb/' if lang == 'nb' else 'en/'
        source = f'''<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if lang == 'ar' else ''}>
<head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{e('title')} — Experimental Newsroom</title><meta name="description" content="{e('deck')}"/>
<link rel="canonical" href="{BASE}{s['file']}"/>
{alternates}
<link href="styles.css" rel="stylesheet"/><link href="reader-navigation.css" rel="stylesheet"/><link href="reader-support.css" rel="stylesheet"/><link href="favicon.svg" rel="icon" type="image/svg+xml"/>
</head><body>
<a class="reader-skip" href="#reader-main">{e('skip')}</a>
<header class="masthead compact-masthead"><div class="edition-line"><span>Experimental Newsroom</span><a href="{home}">{e('home')}</a></div>
<h1>{e('title')}</h1><p class="strapline">{e('deck')}</p>
<nav class="support-languages" aria-label="{e('languages')}">{languages}</nav></header>
<main id="reader-main" tabindex="-1">
<section class="lead"><h2>{e('purposeTitle')}</h2><p class="lead-deck">{e('purpose')}</p></section>
<section class="section-block support-payment"><h2>{e('payTitle')}</h2><p class="measure">{e('pay')}</p>
<p><a class="support-button" href="{escape(s['url'], quote=True)}">{e('button')} →</a></p>
<p class="support-recipient">{e('recipient')}: <strong dir="ltr">MOE JOE ALDEMA</strong> · <bdi>927 532 573</bdi></p></section>
<section class="section-block"><h2>{e('independenceTitle')}</h2><p class="measure">{e('independence')}</p></section>
<section class="section-block"><h2>{e('refundTitle')}</h2><p class="measure">{e('refund')}</p>
<p>{e('contact')}: <a href="tel:+4748448958" dir="ltr">+47 48 44 89 58</a> · <a href="mailto:support@experimentalnewsroom.org" dir="ltr">support@experimentalnewsroom.org</a></p>
<p><a href="support-terms.html" lang="nb">{e('terms')}</a></p></section>
<section class="section-block"><p class="measure">{e('data')}</p><p><a href="privacy.html" lang="nb">{e('privacy')}</a></p></section>
<section class="section-block"><h2>{e('otherTitle')}</h2><p class="measure">{e('other')}</p><p><a href="atriet.html" lang="nb">Atriet</a></p></section>
</main><footer><p>Experimental Newsroom</p></footer></body></html>
'''
        (public / s['file']).write_text(source, encoding='utf-8')
    (public.parent / 'support.html').write_text((public / 'support.html').read_text(encoding='utf-8'), encoding='utf-8')
