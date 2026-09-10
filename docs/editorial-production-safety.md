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
