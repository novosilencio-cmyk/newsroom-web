# Reader-facing sequence presentation — transition standard

**Date:** 2026-09-18  
**Form lead:** Alma Riis, role-based AI function for Experimental Newsroom form and production  
**Status:** TRANSITION_ACTIVE

## Reader rule

Compressed sequences such as `HISTORY → LEGAL BASIS → PRACTICE → ACCOUNTABILITY` may remain useful as internal editorial shorthand. On reader-facing pages, the same structure should normally be expressed as questions, short explanatory sentences or clearly labelled blocks.

An arrow may remain when it acts as a navigation affordance inside a link, such as `Read the report →`.

## Phase 1 — active now

- replace explanatory arrow chains on the main reader surfaces;
- turn the institution-series method into four plain-language questions;
- rewrite relational arrow labels in published stories when a question is clearer;
- show the date when an editorial presentation is materially revised;
- use CI to prevent new explanatory arrow chains outside links.

## Transition toward fuller capacity

Alma's next-level review extends beyond arrows. It should progressively examine:
- heading hierarchy and competing labels;
- density of metadata before the story begins;
- mobile reading rhythm and card stacking;
- whether visual grouping explains or merely decorates;
- whether dates, sources, corrections and uncertainty stay easy to find;
- whether Norwegian and English surfaces feel native rather than mechanically mirrored.

Full capacity means the presentation system can maintain these qualities as new sections, countries, series and article types are added, without requiring a one-off redesign each time.

## Boundary

Form may clarify evidence; it may never upgrade evidence. Source status, uncertainty, disagreement and editorial responsibility remain visible even when a cleaner layout would make them easier to hide.


## Standing fordypningsmodul

Når en sak har et reelt teknisk, metodisk eller strukturelt fordypningslag som ville bremse hovedløpet, skal redaksjonen som standard vurdere den semantiske utfellingskomponenten.

Foretrukket HTML:

```html
<details class="reader-depth">
  <summary>Fordypning: [konkret tema]</summary>
  ...
</details>
```

Eksisterende `details.depth` støttes fortsatt.

### Bruk den når

- hovedteksten kan være fullt sann og forståelig uten at modulen åpnes;
- fordypningen gir reell verdi til lesere som ønsker mekanisme, tall, metode, tabeller, ligninger, kronologi eller spesialistdetaljer;
- modulen reduserer kognitiv belastning i hovedløpet uten å fjerne substans fra artikkelen.

### Legg aldri dette bare i en lukket modul

- et forbehold som er nødvendig for å forstå styrken i hovedpåstanden;
- vesentlige motfunn;
- usikkerhet som endrer meningen;
- den eneste dokumentasjonen for at overskrift eller ingress er korrekt avgrenset.

Praktisk test:

**Hvis en leser som aldri åpner fordypningen sitter igjen med en materielt sterkere eller feilaktig påstand, er modulen brukt feil.**

### Leseropplevelse og tilgjengelighet

- Bruk konkret `summary`-tekst, normalt `Fordypning: ...`, ikke bare `Les mer`.
- Native `details/summary` foretrekkes fremfor spesialbygget JavaScript.
- Tastaturfokus skal være tydelig.
- Tabeller og tekniske elementer må fungere på mobil.
- Fordypningen er del av artikkelen og følger samme kilde-, rettelses- og evidenskrav.
- `NO_DEPTH_MODULE_NEEDED` er gyldig når saken ikke har et genuint valgfritt fordypningslag.

### Evidens for standardiseringen

Mønsteret ble brukt i den reviderte publiserte saken `Mer musikk, lengre liv`. Etter live-lesing vurderte Bjørn Moe Aldema fordypningsfunksjonen som særlig vellykket og bestemte 4. oktober 2026 at funksjonen skal være standard fremover. Dette er konkret menneskelig editor/leser-feedback, ikke en påstand om generell publikumsrespons.
