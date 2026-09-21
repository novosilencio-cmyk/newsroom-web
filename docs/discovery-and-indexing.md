# Discovery and indexing standard

Experimental Newsroom treats discoverability as reader service, not keyword stuffing.

## Public discovery surfaces
- `/robots.txt` — crawler access and sitemap pointer.
- `/sitemap.xml` — canonical crawlable URLs.
- `/feed.xml` — RSS 2.0 feed.
- `/llms.txt` — plain-text machine orientation; useful, but not treated as a formal web standard.
- `/content/articles.json` — publication registry used to generate discovery outputs.
- `/norway/` — geographic reader view generated from the same registry.

## Article semantics
The deploy build adds a canonical URL when missing, an RSS discovery link and Schema.org `NewsArticle` JSON-LD to every registered journalism page. Metadata must not strengthen the claims in the article.

## Language
Language and geography remain separate. Existing bilingual single-URL articles are preserved. A later migration to distinct nb/en URLs should use reciprocal `hreflang` and a link-preserving redirect/canonical plan.

## AI crawlers
The public robots policy explicitly allows OpenAI search discovery and user-requested browsing. The general crawler rule allows other public crawlers. Training-specific restrictions are a separate editorial/rights decision and are not silently introduced here.

## Maintenance
The Pages workflow runs `python3 scripts/build_discovery.py` before tests and again before the public artifact is uploaded. New or updated registry entries therefore regenerate sitemap, feed, Norway view and article discovery metadata automatically.

## Reader guide

`/sitemap.html` (Norwegian) and `/sitemap.en.html` (English) provide a static reader-facing directory. `scripts/build_reader_navigation.py`, called by the existing discovery build, combines the publication registry with an explicit list of published service pages. Story language links use registered translations or the existing bilingual panels. Missing destinations fail the build.

The optional local filter matches titles, short descriptions and country names; it is not full-text article search. Norwegian country aliases are index-only additions. All entries remain usable when JavaScript is unavailable. The build also adds idempotent skip links and guide access to public page shells, excluding the embedded artwork viewer. Changes to generated HTML still require the normal final-content review receipts.
