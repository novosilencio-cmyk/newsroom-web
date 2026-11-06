# Privat tilbakemelding: første HTTP-/lagringsadapter

Status: IMPLEMENTED_AND_TESTED_LOCAL_HTTP_NOT_PUBLICLY_DEPLOYED. Fortsettelse av Bjørns bestilling og Eva-vurderingen. Eksisterende offentlig e-postutkast og alle artikler er bevart.

## Faktisk levert

- `backend/private_feedback_app.py`: WSGI-adapter med POST `/feedback`, servervalidering av Turnstile, eksakt tillatt origin, størrelses-/belastningsgrenser, melding knyttet til kjent saks-ID, UUID-kvittering og SQLite-lagring før bekreftelse.
- GET `/admin/feedback`: beskyttet redaksjonell lesing, uten offentlig CORS. Ingen offentlig meldingliste eller publiseringsknapp. Nøkkel krever minst 32 tegn og skal være tilfeldig og serverprivat.
- `frontend/private-feedback.js`: deaktivert frem til HTTPS-endpoint, offentlig widgetnøkkel og Turnstile er konfigurert. Innsending med ren tekst; feil bevarer tekst og fornyer bot-token. «Mottatt» krever vellykket respons, riktig status og riktig kvitterings-ID.
- `previews/private-feedback-internal.html`: intern visning av felt/etiketter på elleve språkvarianter og arabisk retning. Sendeknappen er deaktivert; ingen faktisk mottaksadresse eller widget. Hjelpetekst om inaktiv status er foreløpig norsk; øvrig driftsordlyd må oversettes før publisering.

## Hva prøvene faktisk beviser

Åtte nye integrasjonstester starter en ekte HTTP-tjeneste kun på loopback, sender syntetiske meldinger og leser tilbake den lagrede meldingen etter ny databaseåpning. Andre prøver viser avvist offentlig lesing, manglende redaksjonsnøkkel, feil origin, klientforfalskede verifiseringsflagg, offentlig visibility, replay-konflikt, belastningsgrense og manglende verifier/lagring uten falsk kvittering. Filrettighet 0600 kontrollert.

Totalt 75 repositorytester består. Separat Node-prøve bekrefter klientens kvitteringskontroll, nettverks-/HTTP-feil og bevart originaltekst. Verifikatoren er en eksplisitt innsprøytet testdobbel i HTTP-testene; det finnes ingen miljøvariabel som skrur av botkontroll. Den ekte Siteverify-adapteren finnes, men ekstern Cloudflare-verifikasjon er ikke kjørt med en virkelig nøkkel/token. Testene er ikke en penetrasjonstest, skjema-/språk-/tilgjengelighetssertifisering eller komplett RFC-validering av e-post.

## Konkrete tilgangs- og driftsgap

Den observerte expNR-workflowen publiserer til GitHub Pages. Den kan ikke kjøre dette skjemamottaket. Gmail-koblingen gjelder Bjørns personlige Gmail, ikke direkte tilgang til `ai@daena.no`. Ingen direkte Onecom-/SMTP-/bridge-verktøy er tilgjengelig i denne arbeidsflaten. Eksisterende Mac-reply-instruks er lest; faktisk Mac-kjøring er fortsatt NOT_OBSERVED i den kilden, og dens avgrensede readback-ordre gir ikke automatisk webserverdrift.

Det er ikke opprettet ny tjeneste, brukt mailpassord, sendt e-post, flyttet domenet, eksponert serverport eller publisert skjema. SQLite er et faktisk lokalt mottak, men ikke en verifisert redaksjonsmail eller driftsatt tjeneste.

## Lokal kjøring og videre kobling

Kjør som modul fra repoens rot: `python -m backend.private_feedback_app`. Den lokale runneren lytter bevisst bare på `127.0.0.1:8765`. Sett serverens `EXPNR_FEEDBACK_ADMIN_KEY` med en tilfeldig hemmelighet i et beskyttet servermiljø; aldri i chat, public/ eller klientkode. Sett `EXPNR_TURNSTILE_SECRET` for serveren og widgetens action `private-feedback`; hostname må stemme med `EXPNR_FEEDBACK_ORIGIN`. Manglende botkontroll gir 503 uten lagring. Ingen nøkkelverdier leveres eller skrives her.

`EXPNR_FEEDBACK_DB` må i faktisk drift peke til et persistent volum utenfor publiserte/git-sporede filer. Standard `/tmp/expnr-private-feedback/inbox.sqlite3` er bare for lokal utvikling og er ikke en varig produksjonsplassering. Datakatalogen må tilhøre driftsbrukeren med begrenset tilgang; backup, sletting/retensjon, kapasitet og driftsovervåkning skal konfigureres. Prototypegrensene er prosesslokale og erstatter ikke edge-/proxy-grenser ved offentlig eksponering. Reverse-proxyadresser skal ikke stoles på uten særskilt oppsett.

Før offentlig drift: velg reelt hostingsted innen eksisterende kapasitet, bruk egnet WSGI-server/HTTPS og hemmelighetshåndtering, persistent privat volum, begrenset tilgang/backup/retensjon, configure hostname/action og botkontroll, oversett driftsmeldingene, og kontroller faktisk mottak/leseadgang. Ikke eksponer standardbibliotekets utviklingsserver offentlig. Meldinger krypteres ikke av SQLite-adapteren selv; beskyttelse i hvile må løses ved faktisk drift.

E-postvarsling er ikke implementert. Den kan kobles til det eksisterende redaksjonelle mottaket når tilgang er verifisert, uten å sende på nytt fra leserens ubekreftede adresse. Lagrede beskjed-ID-er må brukes i sekretariatets behandling; database er mottak, e-post kan være varsling.

## Primærkilde for botadapter

https://developers.cloudflare.com/turnstile/get-started/server-side-validation/ — lest 13. oktober 2026. Siteverify må kjøres på serveren, tokens er engangsverdier og kortlevde; hostname/action kontrolleres. Ingen bevis-på-menneske-etikett brukes.

Neste returpunkt er et faktisk hosting-/innbokskoblet mottak. Koden og skjemaadapteren er klargjort uten å flytte eksisterende nettsted eller skjule tilgangsgapet.
