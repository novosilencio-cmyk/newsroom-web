"""Render the author's fixed Arabic-for-Hindi correction, not a general rewrite.

Only the existing case's language links and registry entry change. Editorial
attestations are supplied as fixed data; this module cannot approve new bytes.
"""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'not-necessarily-an-order-2026'
BINDING = ROOT / 'docs/editorial/essay-arabic-correction-binding.json'


def prepare():
    public = ROOT / 'public'
    paths = list((public / 'articles').glob(SLUG + '*.html'))
    paths += [public / p for p in ('index.html', 'nb/index.html', 'en/index.html')]
    for path in paths:
        text = path.read_text(encoding='utf-8')
        if SLUG + '.hi.html' not in text:
            continue
        text = text.replace(SLUG + '.hi.html', SLUG + '.ar.html')
        text = text.replace('hreflang="hi"', 'hreflang="ar"').replace('lang="hi"', 'lang="ar"')
        text = text.replace('>हिन्दी</a>', ' dir="rtl">العربية</a>')
        path.write_text(text, encoding='utf-8')
    registry = public / 'content/articles.json'
    articles = json.loads(registry.read_text(encoding='utf-8'))
    case = next(a for a in articles if a['id'] == SLUG)
    case['translations'].pop('hi', None)
    case['translations']['ar'] = {
        'url': 'articles/' + SLUG + '.ar.html',
        'title': 'ليست بالضرورة أمراً',
        'summary': 'يتجادل قادة شركات الذكاء الاصطناعي حول ما إذا كانت الآلات واعية. وتحظى شركاتهم بالانتباه. لكن ماذا يحدث داخلنا ونحن نتابع هذا النقاش؟',
        'published_at': '2026-10-04',
        'updated_at': '2026-10-04'
    }
    registry.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def apply_fixed_review():
    """Load explicit reviewed records only if all declared content hashes match."""
    for name in ('sitemap.html', 'sitemap.en.html'):
        p = ROOT / 'public' / name
        text = p.read_text(encoding='utf-8').replace(
            '<option value="hi">हिन्दी</option>', '<option value="ar">العربية</option>')
        p.write_text(text, encoding='utf-8')
    bound = json.loads(BINDING.read_text(encoding='utf-8'))
    rows_path = ROOT / 'docs/editorial/language-reviews.json'
    rows = json.loads(rows_path.read_text(encoding='utf-8'))
    additions = {}
    for rel, expected in bound['hashes'].items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if rows.get(rel, {}).get('sha256') == actual:
            continue  # A separately recorded later exact review remains authoritative.
        if actual != expected:
            raise ValueError('Arabic correction requires a new exact review: ' + rel)
        row = copy.deepcopy(bound['review'])
        row['sha256'] = expected
        row['publication_approval'] = {**bound['approval'], 'sha256': expected}
        additions[rel] = row
    if (ROOT / ('public/articles/' + SLUG + '.hi.html')).exists():
        raise ValueError('Superseded Hindi page must be removed from the publication source')
    rows.pop('public/articles/' + SLUG + '.hi.html', None)
    rows.update(additions)
    rows_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    phrases_path = ROOT / 'scripts/approved_norwegian_phrases.json'
    phrases = json.loads(phrases_path.read_text(encoding='utf-8'))
    old = 'public/articles/' + SLUG + '.hi.html'
    new = 'public/articles/' + SLUG + '.ar.html'
    phrases[new] = list(dict.fromkeys(phrases.get(new, []) + phrases.pop(old, [])))
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
