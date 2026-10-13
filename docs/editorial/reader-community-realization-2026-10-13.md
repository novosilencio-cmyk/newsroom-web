# Leserdeltakelse i Experimental Newsroom

Status: intern prototype, ikke aktivert. **Senere rettelse fra Bjørn: «Dette var nyttig» er forkastet. Gjeldende kandidat er «Bra jobba» og «Spennende», med privat kritisk tilbakemelding uten registrering. Se `forum-broad-search-2026-10-13.md`. Den tidligere leverandøranbefalingen nedenfor er historikk og står nå åpen etter bredere søk.** Bestilling: Bjørn Moe Aldema, 13. oktober 2026. Fortsett abonnementsmodellen med Nova, Sjeherasad, Orfeus fra Atriet og Nansen; undersøk tommel opp, kommentarer, menneskekontroll, enkel profil og eksisterende forum/innlogging.

## Produkt og plassering

Et lite felt etter saken og kildene: «Hva tar du med deg fra denne saken?» Knappen «Dette var nyttig» og en invitasjon til å utdype, korrigere eller spørre. Åpen lesing uten innlogging. Gratis deltakelse, også uten abonnement. Be om innlogging når leseren ønsker å reagere eller kommentere, ikke før de får lese. Behold eksisterende tilbakemeldingsfunksjon som lager et e-postutkast for rettelser og kildetips; denne er ikke et offentlig kommentarsystem.

Profilen har visningsnavn (pseudonym tillatt) og foretrukket språk. Interesser er valgfrie. E-post og intern bruker-ID er private. Redaksjonen får en administrasjonsflate med begrensede roller; ingen delte kontopassord. Avsenderen kan bruke e-postinnlogging, og eventuelt støttede eksterne innlogginger etter separat leverandøroppsett.

Bekreftet e-post dokumenterer kontroll over adressen. Botkontroll reduserer automatisk misbruk. Ingen av delene beviser unik fysisk person eller at saken er lest og forstått. Vi setter ingen «verifisert menneske»-etikett. Reaksjoner gjelder én konto per stabil saks-ID på tvers av språk og kan trekkes tilbake. Kommentarer knyttes også til tekstversjon og språk. Første lansering krever forhåndsmoderering, rapportering, blokkering og kapasitetsgrenser.

## De fire rolleinnspillene

- Nova: minst mulig gjentatt administrasjon; én leseridentitet og et leverandøruavhengig grensesnitt. Hyvor er raskere å integrere, men reaksjoner kan ikke eksporteres individuelt og ønsket botkontroll må avklares.
- Sjeherasad: en invitasjon til saklig uenighet, erfaringer og kilder. «Hva vil du utdype, korrigere eller spørre om?» Betaling, reaksjoner og argumentenes kvalitet er ulike signaler.
- Orfeus: minimal profil, stabil saks-ID, separate rettigheter og testbar hendelsesmodell. Atriets arkitekturrolle brukes i denne konteksten uten å endre rollemyndighet andre steder.
- Nansen: synlig abonnementsverdi selv om artiklene er åpne. Kandidat: en samlet månedlig leserutgave med utvalg, kilder, rettelser og videre lesning, først som norsk/engelsk pilot. Dette er et forslag, ikke en levert tjeneste eller et aktivt salgsløfte.

## Alternativer undersøkt

| Alternativ | Egnet bruk | Vesentlig avklaring |
|---|---|---|
| Supabase Auth + Cloudflare Turnstile | Samme leseridentitet for kommentarer og senere abonnement | Krever egen serverintegrasjon, datalagring, tilgangsregler og modereringsflate. Ingen tjeneste opprettet. |
| Hyvor Talk | Ferdig kommentarfelt med reaksjoner og moderering | Individuelle reaksjoner/vurderinger/stemmer eksporteres ikke; anti-spamflyt må verifiseres. |
| Discourse | Et eget samtaleforum og større leserfellesskap | Mer drift og administrasjon; hosted CAPTCHA oppgis på Pro/Business/Enterprise. |
| giscus | GitHub-orientert lesergruppe | GitHub-innlogging øker terskelen for avislesere. |
| Remark42 | Egen drift med kontroll over kommentarer | Krever drift, e-post/OAuth og separat avklaring av botkontroll; ikke komplett saksreaksjon. |

Foretrukket kandidat er Supabase + Turnstile fordi det kan gi en enkel profil som også brukes senere for abonnementsadministrasjon. Dette er en arkitekturvurdering, ikke dokumentasjon på leverandørens Stripe-godkjenning, ferdig menneskekontroll eller gjeldende totalkostnad. Ingen konto, abonnement eller integrasjon er bestilt. Stripe Directory var ikke tilgjengelig som fungerende oppslag; alternativene er derfor undersøkt i leverandørenes egne kilder.

## Hva som faktisk er realisert

`config/reader-community.json` låser produktkrav og lanseringsporter. `scripts/reader_community.py` er en offline hendelsesmodell med reaksjon/angring, kommentarer som venter på moderering, serverrolle for publisering, idempotens, konfliktavvisning og kontosletting. Den implementerer ikke innlogging, CAPTCHA, database, HTML-rendering eller et offentlig kommentarfelt. Serveradapteren må lage den betrodde konteksten; klienten skal aldri kunne velge verifiserings- eller moderatorflagg. Publiserte kommentarer utleverer ikke privat bruker-ID. Kommentarer er ren tekst som en framtidig renderer må escape.

Seks nye tester kontrollerer språkdeling av reaksjoner, angring, gjentakelser, konflikt, ubekreftet/inaktiv konto, modereringsrettighet, ventende kommentarer, ukjent sak, manglende versjon og sletting. Samlet testkjøring: 60 tester bestått etter statisk bygg. Ingen offentlige sidefiler endret.

## Fasetter, ASA, K38 og W-linsen

Bygger på metodebindingene i `open-subscription-realization-2026-10-13.md`; ingen nye kanoniske metodebetydninger er oppfunnet. ASA: skill aktivitet, signal og redaksjonelt arbeid. K38: bevar kilde og versjon, og merk uavklarte leveranser. W-linsen: inkluder dem som ikke betaler, ikke kommenterer eller bruker mindre synlige språk. Betalte fasettvalg kan hjelpe redaksjonen å starte konstruktive undersøkelser i etterspurte områder, men penger kjøper ikke konklusjoner eller individuell styring. Reaksjoner og kommentarer skal ikke blandes inn i betalingsrangeringen. Andre fasetter skal fortsatt dekkes.

## Videre realisering

Velg og konfigurer leverandør først etter gjennomgang av faktisk pris, dataregion og nødvendige funksjoner. Deretter serverautentisering, botkontroll, databaseregler, moderering og flerspråklig visning. Språksett følger eksisterende side: norsk, engelsk, fransk, spansk for Argentina, tysk, forenklet/tradisjonell kinesisk, japansk, portugisisk for Brasil, koreansk og arabisk. Ingen betalingskrav for deltakelse. Abonnement trenger konkret leveranse, priser, vilkår og fortsatt kontospesifikk Stripe-avklaring; gaveabonnement skal ha fast periode og ingen automatisk opprettelse av mottakerprofil eller fornyelse.

## Primærkilder kontrollert 13. oktober 2026

- https://supabase.com/docs/guides/auth/auth-captcha
- https://developers.cloudflare.com/turnstile/turnstile-analytics/challenge-outcomes/
- https://hyvor.com/talk/docs/export
- https://www.discourse.org/plugins/captcha
- https://giscus.app/
- https://remark42.com/docs/configuration/authorization/
