# Editorial production-safety standard

Status: active repository standard

## Purpose

Experimental Newsroom keeps editorial reasoning visible during drafting without exposing production notes to readers or placing unpublished working material in this public repository.

## Internal working copy

Internal instructions must be unmistakable, searchable and paired with an explicit removal instruction. Do not use italics alone: italics can be intentional publication typography and are therefore not a reliable safety signal.

Use this form in the private editorial workspace:

```text
[INTERNAL EDITORIAL NOTE — REMOVE BEFORE PUBLICATION]
<What the editor, reporter or fact-checker needs to know.>
[END INTERNAL NOTE]
```

A short form may be used during final proof:

```text
[INTERNAL — NOT FOR PUBLICATION: <short instruction>]
```

Reserved unresolved-work markers include `TK`, `VERIFY` and `SOURCE NEEDED` inside square brackets. These are production controls, never reader-facing labels.

## Crafted openings

A crafted opening does not carry an `Artistic entry` heading in reader-ready or published copy. If its status needs to be recorded during production, place that information in an internal editorial note. The note should state whether the passage is documentary description, reported observation or a crafted framing passage, and confirm that it does not invent a scene, person, quotation, sensory detail or witness position.

## Transfer to the public repository

Only reader-ready material may enter this repository. Before transfer:

1. resolve or remove every internal note and unresolved-work marker;
2. remove draft-only approval metadata;
3. confirm that factual qualifications needed by readers remain in the article itself;
4. retain source and verification records in the authorised editorial evidence system;
5. run `python3 scripts/check_publication_markers.py`.

The removal of an internal marker is not permission to publish. Editorial approval, source control and publication authority remain separate requirements.

## Automated gate

The repository check scans public and source-facing text files. It fails when it detects an internal editorial note, an unresolved-work marker, a do-not-publish instruction or metadata stating that publication has not been approved.

The gate is a leakage safeguard, not a fact-check or an editorial approval system. Passing it does not establish that a story is accurate, complete or authorised for publication.

## Version-bound language programme

Run the discovery build, then `python3 scripts/check_language_review.py` in the existing publication-safety job. Receipts bind the final generated HTML. The job uploads the checked public artifact; deployment consumes that artifact without rebuilding.
New or changed public HTML requires an exact SHA-256 receipt in
`docs/editorial/language-reviews.json`. All language versions are separate targets.
Unchanged generated pages from commit 0399388a9f0ec49d79df9af714ef62ff75a0e6a6 are a
migration exception, not evidence of completed historical review. Do not advance
that baseline to bypass reviews. The checker builds this frozen commit with its own generator in a temporary directory and compares output bytes. Missing history or a failed baseline build fails closed.

Use Ariadne's existing six stages, sentence-whole and reader-journey controls:
https://github.com/novosilencio-cmyk/OOS-Core/blob/main/OOS_MASTER/PMH/PROJECTS/EXPERIMENTAL_NEWSROOM/ARIADNE_LANGUAGE_COMPARISON_AND_REALIZATION_WORKFLOW_001.md

Eira owns editorial purpose, Liv source claims, Ada standards and Alma reader
presentation. Ariadne provides standing language mentorship using loaded skills;
Nansen contributes only where relational or cultural risks warrant it. Eva
coordinates the correct object and receipt. Record same-assistant role passes
honestly; do not label them independent review.

The receipt records module source/revision/application, evidence references for
all six stages, comparison, reader journey and semantic control. KEEP is valid.
Source clearance, language completion and Bjørn's explicit publication approval
remain separate; approval must cite the exact page hash. Any changed bytes
require a refreshed receipt. For formatting-only changes, record a bounded
confirmation reusing the earlier analysis rather than rerunning the whole course.

Keep private drafts, source correspondence and analysis outside this repository.
Only safe evidence identifiers belong in receipts. The validator checks presence
and content binding, not the truth of an attestation or the quality of language.
A human/editorial review must inspect the referenced evidence. No receipt is
created automatically and CI cannot grant approval. Internal drafts with source
holds stay in the private workspace. This gate applies to all public HTML,
including headlines/decks/captions embedded there; JS/JSON-only prose changes
still require the same editorial procedure but are outside this initial byte gate unless they change generated HTML. Generator and registry changes that affect generated HTML require receipts for the resulting pages.
