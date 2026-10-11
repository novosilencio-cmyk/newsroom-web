# Multilingual architecture — bounded successor step

## Baseline

The six Økotun language pages are already present on `main`. This step does not
recreate that publication or reuse the closed, unmerged PR #85 as a merge path.

The remaining architecture gap was broader: reader navigation kept a separate
hard-coded language list, while the article regression test exercised only the
three-language Sierra Leone story.

## This step

- adds one shared metadata registry for current and prepared languages;
- derives the reader-map filter from actual article/static destinations;
- keeps metadata-only Hindi, Hebrew and traditional Chinese invisible;
- generalizes canonical, reciprocal `hreflang`, `x-default`, explicit language
  switching, JSON-LD and RTL checks to every article with `translations`;
- requires explicit `dir="rtl"` for every published RTL translation.

No translation, article, entry page, payment flow or public language is added.
The rendered reader maps remain byte-identical because their current languages
already have published destinations.

## Negative boundary

Adding metadata is not publication. A language becomes visible in the filter
only when an actual registered article or static reader destination exists.

## Return point

After this bounded step is reviewed, separately derive discovery entry surfaces
(`sitemap.xml`, `llms.txt` and language entrance pages) from actual published
destinations. Do not create empty entrance pages for metadata-only languages.
