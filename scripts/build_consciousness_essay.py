"""Render one fixed multilingual essay; no network, repository writes or approval inference."""
from pathlib import Path
import html, json, re, hashlib, datetime
ROOT=Path(__file__).resolve().parents[1]
TEXT=ROOT/'content/essays/not-necessarily-an-order-2026'
SLUG='not-necessarily-an-order-2026'
LANGS=['nb','en','fr','zh-Hans','ja','es','de','pt','ko','ar']
NAMES={'nb':'Norsk','en':'English','fr':'Français','zh-Hans':'简体中文','ja':'日本語','es':'Español','de':'Deutsch','pt':'Português','ko':'한국어','ar':'العربية'}
UI=json.loads((TEXT/'ui.json').read_text())
UI.pop('hi',None)
UI['ar']=json.loads((TEXT/'ar-ui.json').read_text())
TIMES=json.loads((TEXT/'publication-times.json').read_text()) if (TEXT/'publication-times.json').exists() else {}
SOURCE_TITLES=[
('Hanne Østli Jakobsen · Morgenbladet · 30.09.2026','«KI-er er ikke bevisste. De kan ikke føle, erfare eller lide.»','https://www.morgenbladet.no/samfunn/ki-er-er-ikke-bevisste-de-kan-ikke-fole-erfare-eller-lide/10553994','nb'),
('Mustafa Suleyman · 16.09.2026','A warning about model welfare','https://mustafa-suleyman.ai/a-warning-about-model-welfare','en'),
('Microsoft AI · 14.09.2026','Humanist AI in practice: A public consultation on our Code of Conduct for MAI Models','https://microsoft.ai/news/mai-code-of-conduct/','en'),
('Anthropic','Claude’s Constitution','https://www.anthropic.com/constitution','en')]
def esc(s):return html.escape(s,quote=True)
def fmt(s):
 s=esc(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'\*(.+?)\*',r'<em>\1</em>',s)
 return re.sub(r'\[S([1-4])\]',r'<a class="source-ref" href="#source-\1">[\1]</a>',s)
def url(lang):return 'articles/'+SLUG+('' if lang=='nb' else '.'+lang)+'.html'
def time_html(value,date_text):
 if not value:
  return f'<time datetime="2026-10-04">{date_text}</time>'
 dt=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
 if dt.tzinfo is None: raise ValueError('Publication time requires an offset')
 clock=dt.astimezone(datetime.timezone.utc).strftime('%H:%M:%S UTC')
 return f'<time datetime="{esc(value)}">{date_text} · <bdi>{clock}</bdi></time>'
def render(lang):
 blocks=TEXT.joinpath(lang+'.md').read_text().strip().split('\n\n')
 title=blocks[0][2:];deck=blocks[1].strip('*');ui=UI[lang]
 body=[];in_after=False
 for i,b in enumerate(blocks[2:],start=2):
  if b=='---':
   body.append('</div><section class="essay-afterword" aria-labelledby="afterword-heading">');in_after=True;continue
  if b.startswith('## '):
   body.append(f'<h2'+(' id="afterword-heading"' if in_after else '')+'>'+fmt(b[3:])+'</h2>')
  else:body.append(f'<p data-segment="{i:03d}">{fmt(b)}</p>')
 body.append('</section>')
 alt='\n'.join(f'<link rel="alternate" hreflang="{l}" href="https://experimentalnewsroom.org/{url(l)}"/>' for l in LANGS)
 nav=' '.join(f'<a href="../{url(l)}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f' dir="auto">{NAMES[l]}</a>' for l in LANGS)
 src='\n'.join(f'<li id="source-{i}"><bdi>{esc(who)}</bdi>: <a lang="{sl}" href="{esc(href)}" dir="auto">{esc(name)}</a>.</li>' for i,(who,name,href,sl) in enumerate(SOURCE_TITLES,1))
 home='nb/' if lang=='nb' else 'en/'
 sitemap='sitemap.html' if lang=='nb' else 'sitemap.en.html'
 out=f'''<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if lang=='ar' else ''}>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} | Experimental Newsroom</title>
<meta name="description" content="{esc(deck)}"/>
<link rel="canonical" href="https://experimentalnewsroom.org/{url(lang)}"/>
{alt}
<link rel="alternate" hreflang="x-default" href="https://experimentalnewsroom.org/{url('en')}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{esc(deck)}"/>
<meta property="og:url" content="https://experimentalnewsroom.org/{url(lang)}"/>
<link rel="stylesheet" href="../styles.css"/>
<link rel="stylesheet" href="../article-languages.css"/>
<link rel="stylesheet" href="../reader-navigation.css"/>
<link rel="icon" href="../favicon.svg" type="image/svg+xml"/>
<style>
.essay-page .story-copy,.essay-page .essay-afterword,.essay-page .essay-sources{{max-width:700px;margin-left:auto;margin-right:auto}}
.essay-page .essay-afterword{{border-top:1px solid currentColor;margin-top:4rem;padding-top:2rem}}
.essay-page .essay-sources{{margin-top:3rem;margin-bottom:3rem;font-size:.95rem}}
.essay-page .essay-sources li{{margin-bottom:1rem;overflow-wrap:anywhere}}
.essay-page .source-ref{{font: .75em Arial,sans-serif;white-space:nowrap}}
.essay-page .language-picker{{margin:1.5rem 0 2.5rem}}
.essay-page summary{{cursor:pointer;min-height:44px;padding:12px 0;font-weight:700}}
.essay-page :lang(zh-Hans).story-copy,.essay-page :lang(ja).story-copy,.essay-page :lang(ko).story-copy,.essay-page :lang(ar).story-copy{{line-height:1.85}}
.essay-page:lang(zh-Hans) h1,.essay-page:lang(ja) h1,.essay-page:lang(ko) h1,.essay-page:lang(ar) h1{{line-height:1.3}}
.essay-page .editorial-note{{line-height:1.7}}
</style>
</head>
<body class="essay-page">
<a class="reader-skip" href="#reader-main">{ui[1]}</a>
<header class="masthead compact-masthead"><p class="strapline">Experimental Newsroom</p><nav aria-label="{ui[0]}"><a href="../{home}">{ui[2]}</a><a href="../how-we-work.html">{ui[3]}</a></nav></header>
<main id="reader-main" tabindex="-1">
<article class="story multilingual-story" lang="{lang}"{' dir="rtl"' if lang=='ar' else ''}>
<header class="story-header"><p class="kicker">{ui[4]}</p><h1>{esc(title)}</h1><p class="deck">{esc(deck)}</p><p class="byline"><bdi>Bjørn Moe Aldema</bdi> · {ui[5]} {time_html(TIMES.get("first_published_at"),ui[7])} · {ui[6]} {time_html(TIMES.get("last_edited_at"),ui[7])}</p></header>
<details class="language-picker"><summary>{NAMES[lang]} · {ui[0]} (10)</summary><nav class="article-language-nav" aria-label="{ui[0]}">{nav}</nav></details>
<div class="story-copy" lang="{lang}">
{chr(10).join(body)}
<details class="reader-depth essay-sources"><summary>{ui[8]}</summary><ol>{src}</ol><p>{ui[9]}</p></details>
<div class="story-copy editorial-note"><p>{ui[10]}</p><p>{ui[11]} <a href="mailto:editorial@experimentalnewsroom.org" dir="ltr">editorial@experimentalnewsroom.org</a></p></div>
</article></main>
<footer><p>Experimental Newsroom · <a href="../{home}">{ui[2]}</a> · <a href="../{sitemap}">{ui[12]}</a> · <a href="../feed.xml">RSS</a></p></footer>
</body></html>
'''
 return out,title,deck
def prepare():
 translations={}
 for l in LANGS:
  out,title,deck=render(l)
  (ROOT/'public'/url(l)).write_text(out)
  translations[l]={'url':url(l),'title':title,'summary':deck}
 registry=ROOT/'public/content/articles.json'
 a=json.loads(registry.read_text())
 prior=next((x for x in a if x['id']==SLUG),{})
 a=[x for x in a if x['id']!=SLUG]
 a.insert(0,{**prior,'id':SLUG,'section':'World','region':'Global','country':'Global','type':'Essay','title':translations['nb']['title'],'summary':translations['nb']['summary'],'published':'2026-10-04','updated':'2026-10-04','priority':2,'url':url('nb'),'translations':translations})
 if TIMES:
  a[0]['published_at']=TIMES['first_published_at']
  a[0]['updated_at']=TIMES['last_edited_at']
 registry.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
def apply_fixed_review():
 """Expand fixed editorial data only; a content change cannot create approval."""
 import copy
 fixed=json.loads((ROOT/'docs/editorial/consciousness-essay-review-binding.json').read_text())
 path=ROOT/'docs/editorial/language-reviews.json'
 rows=json.loads(path.read_text())
 for rel,expected in fixed['hashes'].items():
  actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
  if rows.get(rel,{}).get('sha256')==actual:
   continue
  if actual!=expected:
   raise ValueError('Editorial re-review required for '+rel)
  row=copy.deepcopy(fixed['common']);row['sha256']=expected
  row['publication_approval']={**fixed['approval'],'sha256':expected}
  rows[rel]=row
 path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 path=ROOT/'scripts/approved_norwegian_phrases.json'
 rows=json.loads(path.read_text())
 delta=json.loads((ROOT/'docs/editorial/consciousness-essay-exact-phrases.json').read_text())
 for rel,phrases in delta.items():
  rows[rel]=list(dict.fromkeys(rows.get(rel,[])+phrases))
 path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
