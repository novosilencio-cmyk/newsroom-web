# Bredsøk: lesersamtale, reaksjoner og private tilbakemeldinger

Dato: 13. oktober 2026. Opphav til korrigering og bestilling: Bjørn Moe Aldema.
Status: kildebasert sammenligning og testet intern prototype; ingen tjeneste bestilt, ingen forumkonto opprettet og ingen offentlig aktivering.

## Hva korrigeringen endrer

«Dette var nyttig» er forkastet som reaksjonstekst. En leser kan verdsette en sak, en undersøkelse eller en idé selv om den først og fremst angår myndigheter, statsansatte eller andre mennesker. Vi spør derfor ikke om personlig nytte.

| Element | Tekst | Funksjon |
|---|---|---|
| Enkel tommel | 👍 Bra jobba | Anerkjenn arbeidet |
| Dobbelt tommel | 👍👍 Spennende | Uttrykk interesse og undring |
| Privat inngang | Kritisk tilbakemelding | Send rettelse, uenighet, spørsmål eller manglende perspektiv |
| Tekstfelt | Hva bør vi undersøke, rette eller utdype? | Inviter til konkret innhold |
| Frivillig kontakt | E-post hvis du ønsker svar (valgfritt) | Muliggjør svar uten å kreve registrering |
| Innsending | Send privat til redaksjonen | Skill dette fra offentlig kommentar |

«Genialt» beholdes som vurdert alternativ, men «Spennende» er Bjørns foretrukne formulering. «Fortsett» kan enten være instruks om å fortsette arbeidet eller en kandidat til leseroppmuntring; vi legger derfor ikke inn en tredje knapp uten avklaring av betydningen. «Jeg vil lese mer om dette» er en mulig senere interesseknapp, ikke del av den nåværende modellen.

To positive reaksjoner betyr to forskjellige signaler. Dobbelt tommel får ingen dobbel vekt. Én konto kan gi hver reaksjon én gang per stabil saks-ID, også når saken finnes på flere språk. Begge kan angres. Reaksjoner sier ikke noe sikkert om sakens sannhet, leserens embete eller myndighet, og blandes ikke sammen med betalte fasettvalg. Betaling gir ikke moderatorrettigheter eller bedre kommentarplassering.

## Arbeidsgrunnlag og søkedekning

Fersk Diana-indeks og main-kjernelogg er lest. Main har fortsatt de tidligere Stripe-postene, mens PR1511 har de senere abonnement-/leserdeltakelsespostene 05–11. PR116 inneholder en intern prototype; den er ikke merget eller aktivert. Gjeldende bestilling og korreksjon er ført som post 12 i den samme ventende loggen. Ingen pause i dette sporet ble funnet i de faktisk leste relevante postene. Andre pausede prosjektspor er ikke vekket.

Lokale kilder lest: obligatorisk OØS-arbeidsmodell og antiteseprinsippet. Sistnevnte påvirker neste steg konkret: vi velger ikke et helt forum dersom et kommentarfelt og en privat mottaksvei løser behovet med mindre administrasjon. OOS-Core forblir metode-/kontinuitetseier; newsroom-web eier nettstedets implementasjon.

Søkene omfattet engelske, kinesiske, japanske, spanske og tyske søkeinnganger; offisielle språkflater på Waline ble kontrollert. Japansk/spansk ga relevant primærmateriale; det tyske Comentario-søket ga ikke tilstrekkelig tyskspråklig dokumentasjon. Det er et dekningsgap, ikke et fraværsbevis. Vi bruker leverandørdokumentasjon og prosjektets egne kode-/forummiljøer. Søkeresultater med produktnavn-kollisjoner for Commento, Waline og Discourse/Discord er ikke brukt som dokumentasjon på funksjoner eller priser. Ustabile `edge`/`next`-sider er ikke brukt som bevis på tilgjengelig produksjonsfunksjon.

Stripe Directory ble forsøkt før leverandørsøk. CLI finnes ikke her, og Directory-nettsiden ga unsupported content-type ved lesing. Dette gir et konkret Directory-tilgangsgap. Søk i leverandørenes egne offentlige kilder kunne likevel gjennomføres. Ingen Directory-verifisering eller bestilling hevdes.

## Sammenligning

Funksjonene i tabellen er dokumentert der kilden er angitt. Tilpasning til expNR, byrde og prioritering er våre vurderinger. Ingen løsning er driftstestet her.

| System | Hva det faktisk dekker | Innlogging og uregistrerte lesere | Vurdering for expNR |
|---|---|---|---|
| **Waline** | Artikkelreaksjoner med tilpassede bilder/etiketter; kommentargodkjenning; varsling; klient- og serverkonfigurasjon for Turnstile | Valgfri eller tvungen innlogging; anonyme kommentarfelt kan tillates | Sterk kandidat til isolert prøve. Server og lagring kreves. Reaksjonenes integritet, eksport, oversettelses-ID og sletting må prøves. |
| **Hyvor Talk** | Ferdig embed, reaksjoner, moderering, API og varsling; webhooks på Business | Gjester med navn, valgfri e-post; HYVOR-konto eller SSO | Sterk administrert kandidat. Botkontrollkravet er ikke bevist av spamfilter alene. Individuelle reaksjoner/stemmer eksporteres ikke. |
| **Comentario** | Kommentartre, roller, forhåndsmoderering, moderatorvarsler, JSON-eksport, språktilpasning | Uregistrerte kommentarer, lokal konto, sosial innlogging eller SSO | God kontroll-/eksportkandidat. Egen server og database. Tilpassede artikkelreaksjoner og ønsket CAPTCHA-flyt er ikke dokumentert ferdig. |
| **Discourse** | Fullt forum, reaksjonsplugin, samtaler, roller og interaktiv innbygging i nettsider | Konto; Discourse ID og planavhengige innlogginger | Godt dersom vi ønsker et varig fagfellesskap. Mer funksjon enn det lille artikkelfeltet trenger. Gratisplanen er ikke bevis på at ønsket API, domene, plugin eller innlogging er inkludert. |
| **Remark42** | Lett selvdriftet kommentarsystem, adminfunksjoner, OAuth/e-post og anonym tilgang | Anonym innlogging kan aktiveres med et enkelt navn | Relevant når egen drift er ønsket. Separate artikkelreaksjoner, CAPTCHA og nøyaktig godkjenningsflyt krever videre prøve. |
| **Coral** | Spesielt utviklet for redaksjoner; modereringskø, forhåndsgodkjenning og eksterne modereringsfaser | Registrering/integrasjon må konfigureres | Sterk faglig referanse for redaksjonell samtale. Større drifts-/integrasjonsoppgave; tilbudspris fremfor enkel pris som er verifisert her. |
| **Twikoo** | Kommentarsystem for statiske sider; manuell kontroll, e-post/push og API dokumentert | Brukerflyt og identitetskrav må prøves | Asia-kandidat som hindrer for smalt vestlig utvalg. Eksakte reaksjoner, språkdekning, databehandling og CAPTCHA ikke avklart. |
| **giscus** | GitHub Discussions som kommentarer og reaksjoner | GitHub OAuth for å kommentere, offentlig repository | Lav integrasjonsbyrde for tekniske lesere, men for høy GitHub-terskel som hovedløsning for avislesere og statsansatte. |
| **Flarum** | Forum med språkpakker og utvidelser for blant annet likes, approval, flags og audit | Valg av innlogging/utvidelser må konfigureres | Grovsortert som forumalternativ. Ingen komplett artikkelintegrasjon eller anonym privat mottaksvei verifisert. |
| **NodeBB** | Forum, hooks, oversettelser og reaksjonsutvidelse | Gjesteflyt finnes som konfigurasjonsspor, men kildeforumet viser også tidligere problemer med gjest + forhåndsmoderering | Grovsortert; mer drift og utvidelsesavhengighet enn nåværende behov. Historisk feil er ikke bevis på aktuell feil. |
| **Cusdis** | Kandidat for lett kommentarfelt | Ikke tilstrekkelig kontrollert i denne kjøringen | Direkte dokumentasjonslesing feilet. Tredjepartsomtaler er ikke nok; beholdes som uverifisert kandidat. |

WordPress-plugins er ikke førstesporet fordi expNR i den observerte repoen bygges som statiske sider. Et nytt CMS ville skape en større migrasjon som ikke trengs for dette behovet.

## Vesentlige kildefunn som endrer valget

Waline dokumenterer nå både Turnstile-klientnøkkel og serverhemmelighet, tvungen/valgfri innlogging og tilpassede artikkelreaksjoner. Dermed har den flere av de ønskede funksjonene samlet enn tidligere sammenligning viste. Klientreferansen sier maksimalt åtte reaksjoner, mens reaksjonsguiden sier ni: vi trenger bare to, men vil låse faktisk versjon og teste fremfor å ignorere dokumentasjonsavviket. Reaksjoner telles etter posisjon; navn/rekkefølge må ikke endres uten migrasjonsprøve.

Hyvor tillater gjestekommentarer med valgfri e-post, men gjesten kan ikke selv redigere eller slette dem etter publisering. Moderator må håndtere det. Eksporten omfatter ikke individuelle reaksjoner, vurderinger og stemmer; dette svekker portabilitet. Console API kan vise reaksjonsobjekter, men det beviser ikke at full historikk kan gjenopprettes. Webhook-kravet må prises separat.

Comentario støtter uregistrerte kommentarer og moderatorvarsler. Spam-/toxicity-tjenestene Akismet, APILayer og Perspective er særskilt konfigurerte eksterne tjenester. Det er ikke det samme som en ferdig CAPTCHA- eller menneskeverifiseringsfunksjon. Alle nye kommentarer kan settes til moderering; det gjør dem likevel ikke til private redaksjonsmeldinger.

Discourse har en faktisk gratis hosted plan og interaktiv embed fra april 2026. Det gamle argumentet «må alltid betale for å starte forum» er derfor ikke riktig. Gratisplanens funksjonsgrenser må likevel kontrolleres: CAPTCHA-pluginens side oppgir Pro/Business/Enterprise. Hosted funksjonsmatrisens ikoner var ikke entydige i tekstuttrekket; vi utleder derfor ikke alle gratisfunksjoner fra tomme tabellceller. UI-språk og antall automatiske innholdsoversettelser er ulike ting.

## Pris og driftsbyrde kontrollert nå

- Hyvors side viste Personal €5/mnd, fakturert €50 årlig; Premium €12/mnd og Business €40/mnd i det observerte prisuttrekket. Credits, faktureringsvalg og faktisk checkout må kontrolleres før kjøp. SSO/webhooks ligger på Business; billigste plan løser dermed ikke nødvendigvis hele integrasjonen.
- Discourse viste Free, Pro $100/mnd og Business $500/mnd. Egen drift har gratis programvare, men ikke gratis maskin, e-post, backup eller vedlikehold.
- Comentario krever egen nettverkstilkoblet server og database. Waline krever en server-/lagringsløsning. «Open source» og «deploy free» er ikke en verifisert samlet driftspris.
- Formspree er undersøkt separat for private skjema. Gratisnivået har 50 innsendinger/mnd og 30 dagers historikk. Personal er $15/mnd eller $120/år; API finnes fra Professional. Det er et lavterskel mottaksalternativ, men ikke et forum og ikke automatisk varig arkiv eller assistenttilgang.

Ingen valutaomregning, prisgaranti eller tjenestekjøp er gjort.

## Privat kritisk tilbakemelding uten konto

Denne må ha eget mottak som aldri går gjennom en offentlig kommentarliste. En beskjed som står «pending» i et kommentarsystem kan senere publiseres ved en feil; det er derfor utilstrekkelig å bruke modereringskø som privat innboks.

Leseren skriver beskjed; navn og svaradresse er valgfrie. Saken følger med som kjent saks-ID. Botkontroll og belastningsgrenser legges på serveren uten krav om leserprofil. Etter vellykket lagring får leseren en kvittering. E-postvarsling til redaksjonen er en separat effekt, og manglende varsling må ikke slette en mottatt beskjed. HTTP-feil, spamavvisning eller overfylt skjema skal ikke vises som «sendt».

Diana/sekretærfunksjonen kan behandle beskjedene når innboksen faktisk er tilgjengelig under autorisert arbeid: lese, knytte til saken, skille rettelse/kilde/spørsmål/mening, forberede redaksjonell vurdering og foreslå svar. Ingen kontinuerlig bakgrunnslesing eller svartid er aktivert her. Uten oppgitt svaradresse kan vi ikke love personlig svar. Uregistrert og navnløs betyr ikke teknisk sporbarhetsfri; server-/leverandørlogger må beskrives korrekt.

Eksisterende `public/feedback.js` bevares. Den lager e-postutkast og krever per i dag en bekreftelse om redaksjonell innsending; den er derfor verken direkte privat innsending eller garantert anonym. Den nye private inngangen skal supplere denne funksjonen, med egen ordlyd og mottaksprøve. Eksisterende rettelser og kildehenvisninger skal ikke gå tapt.

## Hva som faktisk er realisert

Konfigurasjonen i PR116 er korrigert fra «Dette var nyttig» til `good_job`/`exciting`, med separate signaler uten vekting. Leverandørvalget er åpnet igjen. Tekstkandidater finnes for alle elleve nåværende språkvarianter; de er ikke språksertifisert.

Offline-modellen er utvidet med `PrivateFeedback`: ingen leserkonto kreves, private beskjedfelter er ikke tilgjengelige uten redaksjonell serverrolle, ukjent sak/spam-/grensefeil avvises, og gjentakelse med samme server-ID dedupliseres mens konflikt avvises. Dette er ikke en HTTP-server, et autentiseringssystem, sikker anonym innsendingskanal, varig database eller mailtransport. Flagg for anti-spam, grensekontroll og redaksjonsrolle må komme fra en virkelig serveradapter, aldri brukerkontrollerte felter.

66 repositorytester består. De seks nye prøvene inkluderer innsendelse uten navn/e-post, privat tilgang, bot-/grenseavvisning uten mottak, replay/konflikt, ukjent sak/mail-headeravvisning og separate reaksjonsbetydninger/angring. Ingen faktisk lesermelding eller e-post er sendt i testene. Offentlige sidefiler er ikke endret.

## Anbefalt videreføring etter bredsøket

Ikke lås Supabase som valgt løsning ennå. Første avgrensede prøve bør sammenligne **Waline** (samlet funksjon og egen kontroll) og **Hyvor** (mindre drift) mot samme krav. **Comentario** beholdes som kontrollkandidat for moderering og eksport. Et fullt **Discourse**-forum blir aktuelt hvis vi vil skape løpende samtaler mellom lesere, ikke bare reaksjoner på artikler.

Prøven skal avklare: iPhone/iPad og tastaturbruk; riktig språk og arabisk retning; to reaksjoner med stabile ID-er; CAPTCHA på faktisk handling; obligatorisk profil bare der den trengs; moderatorrolle; eksport og sletting; pris ved faktisk bruk; og private meldinger som ikke kan publiseres via kommentarmoderering. Løsningen med minst samlet administrasjon som består disse prøvene velges. Ingen avtale må inngås for å lage et lokalt sammenligningsgrunnlag.

Privat mottak kan testes uavhengig og komme først. Eksisterende redaksjonsinnboks foretrekkes dersom tilgang og levering kan verifiseres; administrert skjemamottak er et alternativ hvis det reduserer drift. Stripe-abonnementenes supportability-avklaring er fortsatt separat og skal ikke forsinke planleggingen av gratis leserdeltakelse.

## Primærkilder

1. https://waline.js.org/en/reference/client/props.html
2. https://waline.js.org/en/guide/features/reaction.html
3. https://waline.js.org/en/guide/features/safety.html
4. https://waline.js.org/en/guide/features/notification.html
5. https://waline.js.org/ og https://waline.js.org/jp/ og https://waline.js.org/es/
6. https://hyvor.com/talk/docs/commenting
7. https://hyvor.com/talk/docs/export
8. https://hyvor.com/talk/docs/api-console
9. https://hyvor.com/talk/docs/webhooks
10. https://hyvor.com/talk/pricing
11. https://docs.comentario.app/en/about/features/
12. https://docs.comentario.app/en/configuration/frontend/domain/moderation/
13. https://docs.comentario.app/en/configuration/frontend/domain/extensions/
14. https://docs.comentario.app/en/getting-started/self-host/
15. https://www.discourse.org/pricing og https://www.discourse.org/free
16. https://www.discourse.org/plugins/captcha
17. https://meta.discourse.org/t/embed-discourse-as-a-full-comment-system-on-your-site/399743
18. https://remark42.com/docs/configuration/authorization/
19. https://giscus.app/
20. https://docs.coralproject.net/administration og https://coralproject.net/pricing/
21. https://twikoo.js.org/en/intro.html og https://github.com/twikoojs/twikoo
22. https://docs.flarum.org/extensions/ og https://docs.flarum.org/extensions/audit/
23. https://docs.nodebb.org/ og https://docs.nodebb.org/activitypub/fep/c0e0/
24. https://formspree.io/plans og https://help.formspree.io/articles/account-management/account-limits
25. https://developers.cloudflare.com/turnstile/turnstile-analytics/challenge-outcomes/

Noen kilder er funksjonsgrovsortering og noen faktisk åpnede detaljkilder; ingen av dem er runtime- eller leveringsbevis. Cusdis og ønsket Hyvor-CAPTCHA ble ikke tilstrekkelig verifisert.
