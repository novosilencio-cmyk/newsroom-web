# Reader navigation release — 21 September 2026

## Scope and authority

Experimental Newsroom adds a Norwegian and English reader guide, local directory search, language filtering, skip links and consistent footer access to the guide. The compact masthead now uses its intended size; existing sidebar qualifications remain visible on mobile. Article text, source qualifications, payment behavior and unpublished work are unchanged.

Bjørn Moe Aldema authorized completion and publication of this bounded reader-experience work after team reconciliation on 21 September 2026. The executing assistant binds that scoped instruction to the final page hashes in `language-reviews.json`; this is not a claim that Bjørn personally reviewed each hash or each page. No unrelated article publication is included.

## Review sequence

A separate Ariadne AI execution loaded the existing six-stage workflow and the standard, Norwegian-English, language-harvest and editorial-transfer repertoires. Separate Alma production and Magnus technical executions reviewed the same bounded implementation. These are role-based AI checks, not independent human reviews.

1. **Helhetsinntrykk:** A coherent directory leads from purpose to search, sections, story entries and actual language destinations.
2. **Styrker:** Concise actions, source-preserved headlines and descriptions, explicit language labels and a recoverable empty state.
3. **Stilprofil:** Practical, calm and reader-directed. “Finn frem” and “Find your way” have equivalent navigational purpose.
4. **Konkrete svakheter:** The initial introduction implied every destination offered a language choice. English-only country metadata missed ordinary Norwegian country searches.
5. **Forbedringsgrep:** Describe language labelling accurately; add Norwegian search aliases without changing the article registry or story text.
6. **Revidert eksempelversjon:** “Finn saker, serier, kunst og kurs. Språk er merket ved lenkene.” / “Explore stories, series, art and courses. Reading languages are shown beside the links.” These revisions are realized in the generated pages.

## Comparison and reader journey

The revised introduction trades a small imperative invitation for accuracy about single-language destinations. A language-choice instruction remains useful where actual alternatives exist. This is a local correction, not a general ban.

The journey is entry, purpose, search or section, story title/description, and available reading-language link. Search explicitly covers directory titles, short descriptions and country names. Empty results offer a shorter search, another language or reset. All guide entries remain available without JavaScript. No personal search data is sent or stored by the new filter.

## Semantic control and preservation

Titles and descriptions come from the existing publication registry or actual bilingual article panels. No language version is invented. Article uncertainty and source status are retained. Norwegian country aliases improve retrieval only. Guide-language titles may accompany links to other available reading languages; each destination is labelled.

Ariadne compared all 38 changed existing public HTML pages with the base: their main inner content is byte-identical. All 15 changed article bodies are also byte-identical. Magnus separately built the base with its own generator and confirmed preserved article content. Existing reviewed pages retain their previous receipts under `previous_review`; legacy pages receive a bounded navigation-delta review, not retroactive factual certification. Existing generator metadata is preserved as generated output.

The French shell labels “Aller au contenu” and “Plan du site (en anglais)” were checked for their two navigation functions. This does not constitute a new review of the French article. Older bilingual pages keep their original Norwegian shell when switching the story to English; their links still work.

## Loaded module evidence

- Canonical Ariadne workflow Git blob: `713f6796610652407037c7a0d69385e29d30f727`.
- Ariadne standard repertoire SHA-256: `ad1e98caca6fc791cad0aafb572c1153f30c532536ecba4adc4fbc705d4de34d`.
- Norwegian-English module SHA-256: `2c9f090bd628d2424263e4cfbd60f200f34a27e2b5828dc3c3e0d357b77ecbd8`.
- Language-harvest module SHA-256: `6bdbc56c27018a7c684bb7df27781756d0f1869e5d493db67fcc5cb9ff5584a7`.
- Editorial-transfer module SHA-256: `aced74ca292ae33a5e6c3427da3d08fcda5e21e800bea0def509fcb27a26138d`.

## Design sources

The Exeter site map inspired the grouped overview; the smaller publication uses a shallow, text-first structure. W3C guidance informed alternative routes, keyboard access, responsive reflow and announced search results. These controls do not by themselves establish complete WCAG conformance or measured reader benefit.

- https://www.exeter.ac.uk/about/sitemap/
- https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html
- https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html
- https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

## Validation

- 37 unit tests pass, including actual link/fragment resolution, registered language destinations, missing-target rejection and deterministic generation.
- Existing language, publication-marker, Norwegian style and reader-sequence checks pass.
- Complete public tree rebuild is byte-idempotent.
- Headless Chromium checks pass at 320, 390, 768 and 1280 CSS pixels for both maps, the international front page, Norwegian entrance and an existing bilingual article.
- Keyboard skip-to-main, query results, empty state, reset, French filtering, real bilingual deep link, JavaScript-disabled complete directory and absence of script exceptions pass.
- Visual inspection of desktop and mobile maps confirms readable hierarchy and a single mobile column. Browser testing found a narrow-screen heading overflow on the existing front page; wrapping long headings resolved it without changing text.
- These are bounded release checks, not an assertion of complete accessibility conformance or measured user outcomes.
