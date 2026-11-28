# Eva: vurdering av expNR-løsningen

Bestilt av Bjørn Moe Aldema 13. oktober 2026: «Eva undersøk løsningsforslaget».
Vurdert objekt: åpent abonnement, fasettinteresse, to reaksjoner, enkel leserprofil, offentlige kommentarer og privat kritisk tilbakemelding med e-post tillatt.
Kildegrunnlag: fersk Diana-indeks/main-logg, ventende PR1511 post 12–14 og PR116 head `281e6d68f429f807d588162dac984a8a551ea9f1`; faktisk prototypekode og tidligere primærkildeundersøkelse. Trenet Eva-repertoar er lastet og brukt til objektbinding, avhengighetskart, bevaring og rekkefølgevalg. Dette er en kildebundet vurdering utført av samme assistent i Eva-funksjon, ikke en uavhengig ekstern evaluering eller driftstest.

## Konklusjon

Viderefør funksjonsmodellen, men gjør privat redaksjonell innsending til første driftsleveranse. Leverandørvalget er fortsatt åpent. Et fullt forum skal ikke være en avhengighet for reaksjoner eller private meldinger. Abonnementets faktiske leveranse og Stripe-avklaring er et eget økonomispor som ikke løses av flere kommentarfelt.

## Behov, dekning og neste handling

| Behov | Hva vi har | Gap som faktisk gjenstår | Prioritet |
|---|---|---|---|
| Leser kan anerkjenne og vise interesse | «Bra jobba» og «Spennende», angrebar reaksjonsmodell | Virkelig lagring, identitet/botkontroll, UI og prøve på iPad/tastatur | Etter privat mottak |
| Kritikk kan komme uten offentlig eksponering | Separat privat modell; e-post tillatt; konto ikke nødvendig | Skjemamottak, varig lagring eller eksisterende innboks, mottakskvittering og faktisk leseadgang | Først |
| Samtale mellom lesere | Ventende kommentarer og moderatorrolle i offline-modell | Moderatorkapasitet, rapportering/blokkering, autentisering og faktisk visning | Når kapasitet er etablert |
| Flerspråklig tilgang | Elleve tekstkandidater, stabil saks-ID | Språkvurdering, riktig retning og prøve av oversatte/endrede saker | Før offentlig aktivering |
| Økonomisk bærekraft | Tre abonnementsformer og fem fasetter som prototype | Konkret leveranse, pris, vilkår, faktisk betalings-/avmeldingsflyt og Stripe-godkjenning | Parallelt eget spor |
| Diana håndterer beskjedene | Mottaks-/review-intensjon og kontinuitetslogg | Tilgang til riktig innboks og observerbart behandlingstilfelle | Del av første leveranse |

## Det som bør bevares

Åpen lesing og gratis deltakelse. Bjørns to reaksjonstekster. Dobbelt tommel som uttrykk, uten dobbel vekt. Mulighet for pseudonym i offentlig samtale. Private meldinger som eget objekt, uten automatisk publisering. Eksisterende e-postutkast for kildeinnspill/rettelser. Betalt fasettinteresse som eget signal, med redaksjonell uavhengighet og dekning også av stille/mindre etterspurte områder.

Personlig nytte er ikke nødvendig for å verdsette en sak som kan hjelpe en institusjon eller andre mennesker. «Spennende» kan bety interesse uten enighet; «Bra jobba» anerkjenner arbeidet. Vi må derfor ikke presentere reaksjonstall som sannhetsmål, kvalitetspoeng eller institusjonell tilslutning. Reaksjoner fra statsansatte skal ikke tolkes som deres arbeidsgivers standpunkt.

## Svakheter funnet

1. **For tidlig leverandørvalg:** Supabase-forslaget kom før bred sammenligning av ferdige kommentarløsninger. Bredsøket åpnet valget igjen. Supabase er en byggestein for identitet og lagring; å velge den betyr fortsatt å bygge moderering og grensesnitt. Waline/Hyvor bør prøves mot samme konkrete krav før valget låses.
2. **For mange funksjoner som én ferdigmelding:** Forum, reaksjoner, profiler, privat innsending og abonnement har forskjellige avhengigheter. Et lite privat skjema kan skape faktisk mottak før et forum er klart. «67 tester består» betyr testet intern kode, ikke mottatte lesermeldinger eller fungerende abonnement.
3. **Privat er ikke en kommentars status:** Forhåndsmoderering beskytter offentlig visning frem til godkjenning, men er ikke et privat mottak. En privat melding må ikke kunne offentliggjøres gjennom samme godkjenningsknapp. Personlig e-post holdes privat også når offentlig visningsnavn finnes.
4. **Unødvendig offentlig profilinformasjon:** Foretrukket språk brukes for visning og kommunikasjon; det trenger ikke vises i profilen. Konfigurasjonen er derfor redusert til offentlig visningsnavn, mens språkpreferanse/interesser er private valg.
5. **E-postvalidering var for svak:** En faktisk motprøve viste at `@` ble akseptert som svaradresse. Den enkle formvalideringen er rettet: lokale/domenedeler kreves, flere @/tomme domeneledd/kontrolltegn avvises, og ytre mellomrom normaliseres. En ny regresjonstest avviser disse variantene. Dette er ikke full RFC-/internasjonal e-poststøtte eller bevis på at leseren eier adressen. Produksjonsadapteren må bruke en egnet adressetolk/evt. bekreftelse.
6. **Drift og behandling mangler:** Den nåværende private modellen lagrer bare i prosessminne; et restart mister alt. Rettighetsflagg og anti-spamflagg er betrodde testkontekster, ikke virkelig autentisering eller CAPTCHA. Det finnes ennå ingen sikker offentlig HTTP-endpoint, varig database, varsling eller innbokskobling. Å publisere disse skriptene som tjeneste ville være prematurt.

## Første leveranse og akseptanseprøve

En privat inngang etter saken med «Kritisk tilbakemelding», beskjed, valgfritt navn og e-post etter valgt mottaksflyt. Bruk ikke et fullstendig forumregistreringsløp bare for å gi kritikk. Innsendingen knyttes til riktig saks-ID og språk. Teksten sier at meldingen går privat til redaksjonen; det innebærer ikke teknisk anonymitet eller automatisk samtykke til senere publisering.

Prøven må vise alle disse effektene:

- En prøvebeskjed blir faktisk mottatt i riktig innboks/mottak og kan leses ved autorisert redaksjonsarbeid.
- Beskjeden og svaradressen vises aldri i offentlig kommentarliste.
- Feil eller overfylt mottak gir en sannferdig feil og bevarer leserens tekst; ingen falsk «sendt»-kvittering.
- Mottaket har en varig bevaringsmekanisme. E-postvarsling er en separat effekt, ikke selve beviset på lagring.
- Diana kan knytte beskjeden til saken, forberede en vurdering og eventuelt et svar. Reell innbokstilgang og behandling observeres før funksjonen beskrives som operativ.

Det gamle mailto-feltet kan fortsatt brukes mens dette bygges. Det er allerede en tilgjengelig vei til å sende fra egen e-postapp, men må beskrives som e-postutkast og har ikke serverkvittering eller anonymitet. Ingen felt i den offentlige siden er endret i denne vurderingen.

## Leverandørprøve etter privat mottak

**Waline:** undersøk om de dokumenterte tilpassede reaksjonene, språk, Turnstile, moderering og varsling fungerer sammen i en versjonslåst prøve. Spesielt: stabil reaksjonsrekkefølge/ID, datatilgang, sletting og drift.

**Hyvor:** undersøk samme brukerflyt og faktisk kostnad ved nødvendig SSO/API/webhook. Akismet/spamdeteksjon er ikke i seg selv bevis på ønsket menneskekontroll. Manglende eksport av individuelle reaksjoner er et materielt portabilitetsgap.

**Comentario:** behold som kontrollkandidat for roller, modereringsvarsler og eksport. Ikke anta at artikkelreaksjoner/CAPTCHA allerede finnes ferdig.

**Discourse:** behold som mulig senere leserfellesskap hvis det observeres behov for vedvarende samtaler på tvers av saker. En gratis hosted plan reduserer inngangskostnad, men nødvendig domene/API/plugin/innlogging må fortsatt kontrolleres. Ingen forumtjeneste er bestilt.

Detaljer og primærkilder er bevart i `forum-broad-search-2026-10-13.md`; denne vurderingen er ikke et nytt leverandørsøk eller en dokumentert totalpris.

## Verifisert resultat og returpunkt

E-postmotprøven er gjennomført og feilrettet. Alle **67 repositorytester består** etter endringen. Konfigurasjonen beskriver nå rekkefølgen privat mottak → reaksjoner/profil → modererte offentlige kommentarer → eventuelt forum, med private språkpreferanser. Arbeidet ligger som utkast i eksisterende PR116. Ingen publikasjon, provider-opprettelse, faktisk mailtransport eller bakgrunnsarbeid er utført.

Neste konkrete steg er en virkelig privat mottaksprøve med tilgjengelig redaksjonsinnboks eller et valgt skjema-endpoint. Dersom slik tilgang mangler, kan brukergrensesnitt og adapter forberedes internt, men leveringen skal merkes uverifisert. Dette er en teknisk avhengighet, ikke et behov for å be Bjørn bestille det samme arbeidet igjen.
