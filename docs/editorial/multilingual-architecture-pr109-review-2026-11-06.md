# PR #109 multilingual architecture — reconciled review

## Scope and authority

Bjørn Moe Aldema's current instruction is to finish the next mature step and the
remaining multilingual-architecture delta. This review binds the bounded PR
candidate only. It does **not** authorize merge, deployment, automatic
translation, creation of empty language front pages, or country/IP redirects.

The candidate is reconciled against newsroom-web main
`32774e5c58fad3dadf1e55a17b31c51678551fd0`. PR #85 remains closed and is
not reused.

## Comparison

Before reconciliation, PR #109 contained a useful shared language registry and
general article-language controls but was 16 commits behind current main.
Current main had meanwhile added topic search and multilingual reader-support
surfaces. The branch now uses current main as its preserved base and reapplies
only the missing architecture delta.

The current publication contains article translations in generic Spanish
(`es`) and Portuguese (`pt`) and reader-support destinations in regional
Spanish (`es-AR`) and Portuguese (`pt-BR`). All four are therefore real
published destinations. Hindi (`hi`) and Hebrew (`he`) remain metadata only.

## Reader journey

The reader-map filter lists a language only when at least one actual article or
registered static destination exists. It does not claim that a support page is a
full language front page. Separate language entrance claims in discovery
surfaces are stricter: they require a real registered
`<language>/index.html` whose root language matches that code.

No new language page is created by this change.

## Semantic control

The architecture preserves the distinction:

`language capability/metadata != published destination != full language entrance`.

Article translations remain separate URLs and the general regression controls
cover self-canonical, reciprocal `hreflang`, `x-default`, explicit language
switching, JSON-LD `inLanguage`, sitemap membership and explicit RTL direction
for a published RTL translation.

## Six-stage review

### Helhetsinntrykk

The change removes duplicated language truth and makes reader/discovery
visibility depend on actual publication objects rather than a wish list.

### Styrker

Current-main search, support and deployment work is preserved. Existing Spanish,
Portuguese, Chinese and Arabic surfaces survive; metadata-only Hindi and Hebrew
stay hidden.

### Stilprofil

Reader-facing changes are limited to accurate native language labels in the
existing filter. No article prose is rewritten.

### Konkrete svakheter

The architecture still intentionally distinguishes full language entrances from
other localized pages. A support translation alone does not make a complete
language edition.

### Forbedringsgrep

Centralize labels/direction, derive filter visibility from real destinations,
derive discovery entrances from real language index pages, and enforce the
distinctions with positive and negative tests.

### Revidert eksempelversjon

The generated Norwegian and English reader maps are the exact candidate bytes
bound in the language-review registry. Their change is confined to the
language-filter representation required by the reconciled publication set.

## Publication-action boundary

The exact candidate bytes are cleared for this bounded PR candidate under
Bjørn's current completion instruction and the earlier direction to include the
additional useful languages. Merge/deployment remains a separate action gate and
is not performed by this review.
