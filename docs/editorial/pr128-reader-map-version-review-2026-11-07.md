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

These hashes cover **generated artifact bytes**, not current checked-in public HTML. **Correction after same-unit measurement:** The apparent 57 kB difference came from incorrectly comparing main JavaScript character counts with generated UTF-8 byte counts. Both generated HTML maps are only **53 UTF-16 code units shorter** than main. Their structure is identical in counts, and the changed extracted-search text is concentrated in three entries. This replaces the earlier "materially enlarged" hypothesis. Equal counts alone still do not prove semantic equivalence. The existing PR109 exact-review attestations **must not be copied** onto these new hashes.

## Exact affected-entry localization — same-unit control

The generated files and current-main source were each split into 235 content lines, removing the trailing empty line from main for like-for-like comparison. Each line was compared by UTF-16 code-unit length and a reproducible 32-bit FNV-1a checksum (not a cryptographic or independent review). When excluding the three known changed **zero-based** line indices `228, 229, 231`, the remaining 232 lines have matching total length and checksum:

| Reader map | Main and generated retained code units | Both retained-line FNV-1a |
| --- | ---: | --- |
| `sitemap.html` | 788217 | `48e89822` |
| `sitemap.en.html` | 788972 | `78ec8385` |

The changed entries have exactly the same position in both maps:

- line index 228: Norwegian subscription terms search entry, changed from 3898 to 3856 code units (−42);
- line index 229: English subscription terms search entry, from 4084 to 4032 (−52);
- line index 231: privacy search entry, from 5181 to 5222 (+41).

The sum is **−53** for each reader map, matching the whole-file difference. No article-entry, language-filter option, link count or other identified search entry differs in the length/checksum comparison. This narrows the exact-version editorial review to the two terms summaries and one privacy summary, but the 32-bit checksum does not independently prove every nonaffected byte unchanged. The added XML sitemap contact URLs are tracked separately.

**Review question:** confirm that each updated search entry accurately represents its corresponding source page (registered address accessible through contact link, no misleading office, one.com provider and consent wording accurate), and that no stale address survives in generated search text. Existing PR109 exact-byte approval remains bound to its historical SHA; a new content-bound receipt is required before release. This is a bounded same-assistant evidence comparison, **not independent editorial acceptance or new publication approval**.

## Verified positive/negative controls

- Generated contacts have self-canonical and reciprocal `nb/en` alternates, explicit language selection and the correct registered business address once each; generated subscription-support and recurring-terms pages have no street-address repetition.
- Six of six bounded subscription tests passed in GitHub Actions before the normal review gate.
- The generated XML sitemap includes one URL each for `contact.html` and `contact.en.html`.
- No new article, language edition, checkout link, payment activation, redirect, DNS or production change is authorized by this PR.
- Existing `build_consciousness_essay.apply_fixed_review()` blocks at `public/sitemap.en.html`: this correctly prevents treating unmatched content as reviewed.

## Open evidence gate and return

1. Confirm the three changed reader-map search entries against the actually generated terms/privacy pages with explicit content-bound language/editorial judgement; retain unchanged-entry controls and check for collision risk in the noncryptographic checksum.
2. Determine whether the changed result is source-aligned; classify each material change and counterexample, including whether the privacy correction eliminates address exposure throughout discovery output.
3. Obtain truthful **new exact-version** language/editorial review and applicable publication approval through the repository's normal authority path. No same-assistant reading is called separate independent review.
4. Only then run full publication/translation/reader/accessibility gates and consider merge and the existing one.com release path.

Status: `EVIDENCE_RECORDED / STRUCTURE_CHECKED / SEMANTIC_REVIEW_PENDING / GATE_BLOCKED / NO_RELEASE`. No forced green or fabricated approval.

## Exact-head continuation — revised contact wording, deterministic maps and 61-unit gate

After the Norwegian contact copy and the consent/DNT notice were corrected to satisfy the established Norwegian-style rule, both reader maps were regenerated **from their source content**, not copied from older review evidence. A reconstruction of the earlier generation reproduced the exact Git blob SHA-1 of the independently captured GitHub Actions artifact, which validated the narrow three-entry regeneration algorithm against the real Python output for that snapshot.

Current committed PR-head map blobs:
- `public/sitemap.html`: `7d06f48dbb66ddf4d71af7e3f8fd11114b3f2db9`.
- `public/sitemap.en.html`: `6d247e114dc13b67d3a71d88ae717cc00fd6584b`.

The new blobs differ from the previous generated-artifact SHA-256 listed above **because the underlying consent paragraph was subsequently edited**. Do not treat the earlier SHA-256 hashes as signatures of the current files.

**Direct same-assistant semantic check of affected entries**: the Norwegian and English subscription terms still state the real publisher and terms, refer to the dedicated business-address contact page, preserve withdrawal/contact instructions, and have no home street address. The privacy summary corresponds to the revised source's one.com hosting and consent/Do Not Track explanation and likewise has no home street address. Language-option and map entry counts remain constant. This review is a **bounded, non-independent preliminary semantic pass**, not an author approval, independent language certification or release clearance.

**GitHub Actions test evidence:** [run 42352370006](https://github.com/novosilencio-cmyk/newsroom-web/actions/runs/42352370006), exact commit `86bcc2e599854f5f20ee819230e9de24ad762201`: **61/61 Python unit tests PASS**, including rendering determinism and Norwegian editorial style. The unchanged subsequent publication gate still stops at `build_consciousness_essay.apply_fixed_review()` for `public/sitemap.en.html`, because the prior language review belongs to earlier content bytes. This is an expected **AUTHORITY/EVIDENCE** gate, not evidence of a remaining deterministic-build failure.

The temporary test-only step was removed again and the original GitHub workflow blob `7e5959f5b4dbd53801db7fb79cb7e3d1bb96b412` was restored. The source and generated HTML remain on **draft branch**, not main or one.com.

**Precise return:** an editor/author-approved, exact-content review record for the current two reader-map blobs (with the changed three entry texts inspected) is required under the existing publication gate; then run the full release checks. Do not backdate, inherit, automatically grant or forge a publication approval. After normal approval, merge and deployment remain separate gates.


## ASA / Glimrende funn — exact current-source reconciliation, 2026-11-07

**Observed source:** `newsroom-web/main@1d8a44b59b6c39a6581f07d71233018802b2bdda` versus the current PR128 generated map blobs `public/sitemap.html@7d06f48dbb66ddf4d71af7e3f8fd11114b3f2db9` and `public/sitemap.en.html@6d247e114dc13b67d3a71d88ae717cc00fd6584b`. Every source file was fetched and read; older artifact hashes are historical.

**Exact text comparison:** Both maps have *only three changed complete HTML lines*, at human line numbers **229, 230 and 232**; all other lines compare equal as strings, not merely in length or 32-bit checksums. The changed lines are the published Norwegian subscription terms search entry, English subscription terms search entry, and privacy entry. These lines contain a computed `data-search` value based on the three actual source pages; their source sections and structural boundaries remain intact. This is stronger than the previous non-cryptographic checksum-only result. No detected article-line, reader-language option, map link or unrelated prose modification.

**Source-to-summary meaning check:**
1. Norwegian subscription terms replaces the repeated residential registration line with `Virksomhetsopplysninger og registrert adresse`, correctly referring to `contact.html`; publisher, financial terms, customer contact and withdrawal wording are preserved.
2. English subscription terms analogously uses `Publisher details and registered address` and `contact.en.html`; publisher, billing periods, consumer remedies and refund information are preserved.
3. Privacy search entry removes the repeated street address, names the contact page as the address source, correctly names one.com as production site host and represents the existing explicit Umami consent / Do Not Track path. No unsupported claim about the visitor's physical office is added.

**Positive and negative source checks at current PR branch:** 10 of 10 direct checks PASS: neither reader map contains the residential street string; both contacts have language-switch links and self canonicals; both terms pages link to the correct publisher contact; the privacy notice links to contact; the XML sitemap contains exactly one URL for each contact page; address appears once on each contact page and zero times in terms pages; existing Stripe terms remain present; both reader maps contain the new source-aligned labels and one.com text. These are *same-assistant deterministic checks* and cannot certify independent editorial judgment.

**ASA status separation:**
- `RECORDED`: PR128 source and exact map diff reviewed here.
- `APPLIED_ON_BRANCH`: pages, generator and XML sitemap exist on the unmerged PR branch.
- `TEST_VERIFIED_BOUNDED`: earlier exact-head 61/61 suite PASS; direct source checks 10/10 PASS.
- `EDITORIAL_BOUNDED_SAME_ASSISTANT_PASS`: narrow changes preserve the described meanings with no observed counterexample in the examined source.
- `EXACT_VERSION_PUBLICATION_APPROVAL`: **NOT OBTAINED**; prior PR109 author approval is not transferred to new SHA/contents.
- `INTEGRATED/ONECOM_DEPLOYED/PUBLIC_EFFECT`: **NOT OBSERVED**.

**Release HOLD:** The required new, honest, version-bound publication approval for the two current map blobs is a legitimate decision/authority boundary. Do not set `publication_approval.approved=true`, copy signatures, modify the gate or declare CI green. After the appropriate approval, update only those two corresponding language-review receipts in the canonical registry, run full publication gates and verify exact post-state before considering release. This same-assistant pass is not a separate reviewer, and approved review does not imply deploy authority.
