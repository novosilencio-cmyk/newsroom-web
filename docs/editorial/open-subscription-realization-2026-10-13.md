# Åpen abonnementsmodell — realisering 001

Opphav: Bjørn Moe Aldema. Status: intern kodeprototype, ikke aktiv betaling eller offentlig tilbud. Bestillingen 13. oktober 2026 innebærer fortsatt utvikling og realisering med ASA, K38 og W-linsen; særlig konstruktive saker først i fasetter det betales hyppigere for, deretter andre områder i hele avisens fasettutvalg.

## Betydningsåpning og valgt kandidat

«Betales hyppigere» kan bety flere trekk, flere betalende personer eller sterkere vedvarende interesse. Fransk fréquence de paiement beskriver hendelser, mens soutien régulier beskriver kontinuitet. Engelsk reader demand viser etterspørsel, men ikke automatisk allmennverdi. Tysk Schwerpunkt kan være et midlertidig tyngdepunkt, ikke eksklusivitet. Japansk 継続的な支援 peker mot vedvarende støtte. Ingen av disse gir betaleren rett til en bestemt konklusjon.

Vi bevarer derfor to signaler i prototypen: antall betalingseventer som dekker observasjonsperioden, og antall forskjellige betalende lesere per fasett. Den foreslåtte redaksjonelle vekten bruker sistnevnte, uten beløpsvekting. Dette er en assistentvalgt kandidat, ikke en påstand om at Bjørn allerede har godkjent den nøyaktige måledefinisjonen. Månedlige og årlige abonnement sammenlignes gjennom faktisk dekket periode. Ingen virkelig betalingshistorikk brukes i testen.

En interesseoversikt gir en første gruppe kildeklare konstruktive kandidater i de mest støttede fasettene. Den eksisterende sakskøen beholder eierskap, tilstand, pauser og publiseringsporter. Andre fasetter og fraværende områder vises samtidig. Redaktøren tar en konkret neste handling, og vurderer hele porteføljen før en ny runde; ingen evig forrang eller fast kvote etableres. Rettelser og akutte allmennhensyn sendes til særskilt redaktørvurdering, ikke gjemmes i en pengeskår.

## Hva konstruktiv betyr

En sak skal undersøke hvordan noe kan virke: konkret behov, respons/mekanisme, dokumentert gjennomføring, hvem som får nytte, kostnader og byrder, motfunn, usikkerhet og neste observasjon. «Konstruktiv» er ikke reklame, optimisme eller bestilt støtte til en foretrukket løsning. En konstruktiv undersøkelse kan avdekke at tiltaket ikke virker.

Fasetten «En åpen, flerspråklig redaksjon» er en kapasitetspreferanse, ikke automatisk et stoffområde. Den kan gi mer kilde-/oversettelsesarbeid på tvers. Dersom den rangerer høyt og ingen passende eksisterende sakskandidat finnes, viser prototypen gapet; den oppfinner ikke en nyhetsartikkel bare for å fylle en kategori.

## ASA — status per relevant akse

| Akse | Observert status | Neste grep |
|---|---|---|
| Retning og funksjon | Bjørn har bestemt abonnementsretning og fasettbasert interesse | Bevar opphav, test konkret beslutningsstøtte |
| Utførelse | Lokal config, oppsummering og tester finnes | Valider determinisme, moteksempler og tapsgrenser |
| Observasjon/effekt | Bare syntetiske tester; ingen leser- eller betalingseffekt | Senere én faktisk anonymisert periode etter godkjent aktivering |
| Myndighet/provider | Intern utvikling autorisert; Stripe-vurdering fortsatt åpen | Ingen nye betalinger, klageinnsending eller abonnement aktiveres |
| Vedvarende drift | Ingen runtime, providerinngang eller abonnentlevering koblet | Avklar priser, levering, hendelser og oppsigelse før pilot |

ASA åpnes fordi «start realisering» ellers kan feiltolkes som «aktivt abonnement». Svakeste beslutningsrelevante akse for kodeprototypen er om rå trekkhyppighet gir feil prioritering. Den minste informative testen sammenligner én stor/oftetrekkende leser med flere uavhengige betalende lesere, samt år/måned, refusjon, nullgrunnlag og kildehold. Stripe-godkjenning kan ikke avgjøres av denne testen.

## K38 — faktisk bruk

- Objekt: lesernes verdsetting og redaksjonell oppmerksomhet.
- Verdsetting: signal om hvilke fasetter betalende lesere vil se videreført.
- Oppmerksomhetsendring: første kildeklare undersøkelse vurderes i tydelig støttede fasetter.
- Nye detaljer: årsbetaling, månedstrekk, replay, reversering og økonomisk skjevhet kan forvrenge rå frekvens.
- Oppdaget mønster: flest trekk er ikke nødvendigvis flest interesserte lesere.
- Blindsoner: dem uten betalingsevne, fremtidige behov, barn/natur og fasetter med få data.
- Orienteringsgevinst: bevar rå signal og en normalisert alternativtolkning; behold øvrig portefølje og menneskelig vurdering.
- Valg: test ikke-beløpsvektet interesseoversikt før aktivering.
- Konsekvens: observeres kun i syntetiske moteksempler nå; virkelig redaksjonell effekt ukjent.

## W-linsen — materielt delta

W1: abonnementsbeskrivelse er ikke abonnementsdrift; syntetisk interesse er ikke faktiske betalinger.
W2/W3: penger kan snevre inn oppmerksomheten; hele fasettutvalget og relevante ikke-betalende perspektiver beholdes.
W5: Bjørns livs-/samfunnsformål og åpne tilgang er overordnet finansieringsmålet.
W7/W8: realiser en liten intern adapter med negative tester; ikke bygg en ny kø eller universell totalskår.
W10/W12: kildeport, redaktøransvar og providerkrav stopper aktivering og publisering.

## Leveranse og resterende porter

Config: config/open-subscriptions.json. Adapter: scripts/facet_interest.py. Tester: tests/test_facet_interest.py. Adapteren returnerer interessegrupper, øvrig dekning, kildehold, akutte vurderingsbehov og porteføljegap. Den skriver ingen kø og har ingen nettverk/payment-kode.

Neste praktiske trinn: beslutt reell abonnentlevering og priser; klargjør avtalevilkår/gaveflyt og skatt/MVA; få Stripe-vurdering; bygg sandbox Billing/Checkout, kundeadministrasjon og obligatorisk verifisert hendelseshåndtering. Ikke legg persondata eller rå betalinger i offentlig repo. Historiske engangslenker og samtykker skal ikke konverteres til faste trekk.

## Kilder lest

- OOS-Core core/loops/K38-OPPMERKSOMHETSSYKLUSEN.md, blob 4ea6235a9e87b70145a253148de85d65f4af4359.
- OOS_MASTER/CORE/CONTROL/AXIS_STATUS_RECONCILIATION_PROFILE_001.md, blob 09145af5eb39cc1f142add188475075578a32263.
- OOS_MASTER/CORE/CONTROL/ASA_WORK_JOURNAL_001.md.
- OOS_MASTER/CORE/RESEARCH/HIGH_VALUE_DISCOVERY/OOS_WISDOM_SUPPORTING_CAPACITY_DBO_TEST_001_2026_10_03.md, blob 15f5b027d388768c33da52797fd9ccabaffdc36a.
- OOS_MASTER/CORE/COMPONENTS/ESTABLISHED/EVA_EXECUTIVE_TASK_CONTROL_001_2026_07_02.md, blob 1682376f62955cbbe1d6c3302f5f8496e142dbe4.
- Dianas model- og Stripe-kontinuitet i PR1511; faktisk publisert nettsted bevart fra newsroom main 8e9e586fe0d57b8ba47bf6d3f3969c510c83e346.

Same-assistant metodeanvendelse og kodetest; ingen separat evaluator eller målt leservirkning hevdes.
