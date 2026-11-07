# PR128 — reader-map version-bound comparison, 7 November 2026

## Scope and provenance

Bjørn's approved privacy-minimization objective: keep the legally correct registered geographic business address available on two bilingual publisher-contact pages while avoiding unnecessary duplication throughout subscription and privacy copy.

Source main `1d8a44b59b6c39a6581f07d71233018802b2bdda`. PR128 generated review snapshot: GitHub Actions run `42350995020`, artifact ID `13565457575`. The source-produced bilingual contact preview came from run `42350478706`, artifact `13565371247`. Both artifacts were actually downloaded and inspected. This is executing-assistant observation, **not** an independent or human editorial review.

## Direct comparison of reader-map structure

| Attribute | Main Norwegian | Generated Norwegian | Main English | Generated English |
| --- | ---: | ---: | ---: | ---: |
| HTML text chars / bytes from inspected sources | 801384 chars | 859177 UTF-8 bytes | 802139 chars | 859806 UTF-8 bytes |
| Published map entries (`.map-entry`) | 67 | 67 | 67 | 67 |
| Anchor links | 294 | 294 | 292 | 292 |
| Reading-language options | 14 | 14 | 14 | 14 |
| Registered private street address present in map search source | YES | NO | YES | NO |

**Exact generated SHA-256:**
- `public/sitemap.html`: `b5c1238c052e5eb3a426dd038a2cc962649230e5b64a16f77854bec2a21dceab`
- `public/sitemap.en.html`: `d0390636b5b9ceca3b6d65b9bc044d6ba05880f5a120cf903431335cb16115fa`

These hashes cover **generated artifact bytes**, not current checked-in public HTML. Main reader-map content is materially different, much more than the removal of postal-address excerpts. Equal entry/anchor counts do **not** prove exact text, links, meaning, quality, or publication readiness. The enlarged generated reader maps therefore require their own content-bound review. The existing PR109 exact-review attestations **must not be copied** onto these new hashes.

## Verified positive/negative controls

- Generated contacts have self-canonical and reciprocal `nb/en` alternates, explicit language selection and the correct registered business address once each; generated subscription-support and recurring-terms pages have no street-address repetition.
- Six of six bounded subscription tests passed in GitHub Actions before the normal review gate.
- The generated XML sitemap includes one URL each for `contact.html` and `contact.en.html`.
- No new article, language edition, checkout link, payment activation, redirect, DNS or production change is authorized by this PR.
- Existing `build_consciousness_essay.apply_fixed_review()` blocks at `public/sitemap.en.html`: this correctly prevents treating unmatched content as reviewed.

## Open evidence gate and return

1. Compare the new reader-map content against old reviewed maps at **entry/text/link** level, including changed search text and any extra article material, not just item counts.
2. Determine whether the changed result is source-aligned; classify each material change and counterexample, including whether the privacy correction eliminates address exposure throughout discovery output.
3. Obtain truthful **new exact-version** language/editorial review and applicable publication approval through the repository's normal authority path. No same-assistant reading is called separate independent review.
4. Only then run full publication/translation/reader/accessibility gates and consider merge and the existing one.com release path.

Status: `EVIDENCE_RECORDED / STRUCTURE_CHECKED / SEMANTIC_REVIEW_PENDING / GATE_BLOCKED / NO_RELEASE`. No forced green or fabricated approval.
