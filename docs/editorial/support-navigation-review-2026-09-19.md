# Support navigation review — 19 September 2026

Scope: version-bound language and semantic review of the single reader-navigation sentence added to `public/support.html` on `fix/support-legal-navigation-refresh-20260919@69fd654783cf14236e1b7585758d994fe69e8d76`. The underlying support offer, payment state and legal texts are unchanged. This is an internal editorial review, not publication approval or evidence of reader utility.

## Review sequence

1. **Helhetsinntrykk:** The page already gives a clear three-purpose support structure and repeatedly says that payments are not open. The new sentence belongs in the payment section because it lets a reader inspect terms and privacy information before any payment route becomes active.
2. **Styrker:** Both link labels name their destinations and identify that the linked texts are in Norwegian. Relative links keep the reader within the same public site. The sentence does not suggest that payment is available or that the terms themselves prove legal compliance.
3. **Stilprofil:** Compact, factual English service copy. The middle dot presents two equally important reader routes without adding a new hierarchy or promotional claim.
4. **Konkrete svakheter:** No material language weakness was found in the added sentence. Its only substantive limit is external to the wording: repository presence and local tests do not prove publication, successful live HTTP retrieval or actual reader use.
5. **Forbedringsgrep:** `KEEP`. Further rewriting would add length without improving orientation. Do not replace “Norwegian” with a broader availability claim, and do not imply that payments have opened.
6. **Revidert eksempelversjon:** `Read the support terms (Norwegian) · Read the privacy notice (Norwegian)` — identical to the candidate because the review found no justified text change.

## Semantic and reader-journey control

- Agency is unchanged: the newsroom supplies information; the reader chooses whether to inspect it.
- Epistemic status is unchanged: payment options are still being prepared and the buttons remain inactive.
- The links improve discoverability only. They do not establish legal adequacy, publication, live availability, consent, payment activation or observed reader benefit.
- The intended journey is support purpose → payment state → terms/privacy information. No forced detour or hidden prerequisite is introduced.
- The terms and privacy files exist in the exact branch tree. Their separate content review is outside this navigation-only scope.

## Authority

The six-stage review is complete and the exact candidate bytes are editorially ready. No version-bound publication approval for this support-page change was granted in the present task. The machine receipt therefore records `approved: false`, and the language-review gate must remain red until the repository receives a separate, explicit approval tied to these exact bytes.

No PR, merge, deployment, payment activation or public-state claim follows from this review.
