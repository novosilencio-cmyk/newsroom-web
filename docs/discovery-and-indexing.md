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
