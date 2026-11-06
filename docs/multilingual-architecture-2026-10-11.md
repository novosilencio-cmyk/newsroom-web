# Multilingual architecture — reconciled successor step

## Baseline

The six Økotun language pages are already present on `main`; this branch does not
recreate or republish them. Since the first PR #109 snapshot, current `main` has
also added real reader-support destinations in several languages, including
Traditional Chinese and Arabic. Those current functions are preserved.

## Completed delta

- one shared language metadata registry supplies labels, English names and text
  direction without treating registry membership as publication;
- the reader-map language filter is derived from real article/static destinations
  rather than a hard-coded wish list;
- metadata-only languages such as Hindi and Hebrew remain invisible until a real
  destination exists;
- multilingual article controls apply to every registry article with `translations`:
  self-canonical, reciprocal `hreflang`, `x-default`, explicit language switching,
  JSON-LD `inLanguage`, one sitemap URL per translation and explicit `dir="rtl"`
  for published RTL translations;
- discovery language entrances are derived from real registered
  `<language>/index.html` pages; `sitemap.xml` and `llms.txt` use those actual
  entrances and do not create empty language surfaces.

## Negative boundary

Adding language metadata is not publication. Support pages are real published
destinations and may therefore appear in reader filtering, but they are not
misrepresented as full language front pages. No article is translated, no empty
Hindi/Hebrew/Chinese entrance is created, and no country/IP redirect is introduced.

## Preservation

The reconciliation is based on current `main`, preserving newer topic search,
reader-support, subscription-language and deployment work that post-dated the
original PR #109 branch. PR #85 remains closed and is not reused as a merge path.

## Return point

Run the full repository gates on the reconciled exact head. Any future language
entrance must first exist as a real reviewed page; registry metadata alone must
continue to fail closed.
