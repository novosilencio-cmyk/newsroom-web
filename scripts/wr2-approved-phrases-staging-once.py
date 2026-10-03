"""One-time materialization of explicitly reviewed W-R2 phrase exceptions.

Remove this staging helper before merge. It does not approve arbitrary prose.
Approval is the exact W-R2 publication order recorded at PR80/comment5973182216.
The existing checker already supports article-scoped exact editor approval.
"""
import copy
import hashlib
import json
from pathlib import Path
import runpy

ARTICLE = 'public/articles/hvem-er-det-vi-ber-om-a-bruke-mindre-2026.html'
SERIES = 'public/series/virkemidlene/nb/index.html'
EXPECTED = {
    ARTICLE: '33460c9a0b1c2833f65242054fbf84970ecf680543ebcf34022f55e10c799ac8',
    SERIES: '80bcea0865c2eacafcf462ee96470e9608a793d69163a0fbcb8d9307e925f900',
}
# Literal text nodes individually inspected in the approved HTML and failed gate.
# Most preserve evidence boundaries; the heading and ending preserve the editor's
# selected rhetoric. Neither category creates a general exemption for new prose.
PHRASES = {
    ARTICLE: [
        'Regnestykket sier heller ikke hva noen vil velge bort. Tenk to husholdninger som får samme ekstra renteutgift: Den ene kan dekke den av oppsparte penger, mens den andre må kutte i forbruket. Forskjellen mellom dem er nettopp noe en undersøkelse av virkningen må fange opp.',
        'Tre banker er ikke hele markedet. Kunngjøringene viser hva disse bankene har besluttet og hvilke datoer de oppgir. De dokumenterer ikke at alle berørte kunder allerede har fått varsel. Nordea og DNB skriver at kundene vil få informasjon; SpareBank 1 Østlandet beskriver hvordan kundene varsles. Vi har ikke kontrollert individuelle kundevarsler eller kontotrekk.',
        'November er ikke en pauseknapp',
        'Datoen en ny rente begynner å løpe, er ikke nødvendigvis datoen for første høyere trekk fra kundens konto. Kunngjøringene alene fastslår heller ikke når en husholdning endrer forbruket.',
        'En låntaker kan for eksempel begynne å spare før den høyere renten trer i kraft. Det er en mulig tilpasning, ikke noe disse kildene viser at husholdningene faktisk gjør nå. Norges Bank beskriver dessuten hvordan forventninger, valutakurs og finansieringsvilkår kan formidle rentevirkninger gjennom økonomien.',
        'Et forbruksfall tidlig i oktober kan derfor ikke uten videre tilskrives høyere renter som først begynner å løpe på de aktuelle eksisterende lånene i november. Men kalenderen beviser heller ikke at rentehevingen er uten virkning frem til da.',
        'Forskningsfunnet viser hvorfor ulik renteeksponering er relevant for forbruket. Det er ikke en prognose for denne høsten. Vi kan ikke bare dele resultatet på fire og kalle det virkningen av septemberøkningen på 0,25 prosentpoeng. Funnene og konklusjonene tilhører forskerne, ikke rentekomiteen.',
        'Tallene beskriver rentenivået før septembervedtaket. De viser ikke virkningen av novemberendringene, og rentestatistikk alene forteller heller ikke hvem som kutter i forbruket.',
        'Belastningen er en del av vurderingen, ikke hele dommen',
        'At låntakere får høyere utgifter, avgjør derfor ikke alene om vedtaket var riktig eller galt.',
        'Høyere innskuddsrente er heller ikke det samme som at en husholdning samlet er en vinner. Renteendringer kan også påvirke arbeidsinntekt, aktivitet og formuesverdier. Den direkte renteregningen er bare én del av bildet.',
        'Seriens neste spørsmål er konkret: Får kundene de varslede renteendringene, og hvordan tilpasser husholdninger med ulik økonomi seg? Bankenes datoer gir et holdepunkt for oppfølging, ikke en fasit. Også etter november må en undersøkelse skille rentevirkningen fra andre endringer i inntekter, priser og forbruk.',
        'Rentevedtaket er felles. Handlingsrommet er det ikke. Skal vi forstå innstrammingen, må vi følge både pengene og menneskene som skal få hverdagen til å gå rundt.',
        'Ingen egne intervjuer er brukt. De tre bankene er eksempler på gjennomføring, ikke en full måling av bankmarkedet.',
    ],
    SERIES: [
        'Samme rentevedtak gir ulikt handlingsrom. Tre bankers kunngjøringer viser når nye renter skal begynne å løpe på eksisterende lån. Det er ikke det samme som når husholdningene endrer forbruket.',
    ],
}
for path, expected in EXPECTED.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
registry = Path('scripts/approved_norwegian_phrases.json')
before = json.loads(registry.read_text(encoding='utf-8'))
rows = copy.deepcopy(before)
for path, phrases in PHRASES.items():
    current = rows.setdefault(path, [])
    for phrase in phrases:
        if phrase not in current:
            current.append(phrase)
assert all(rows[k] == v for k, v in before.items() if k not in PHRASES)
assert all(rows[k][:len(v)] == v for k, v in before.items() if k in PHRASES)
registry.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
module = runpy.run_path('scripts/check_norwegian_editorial_style.py')
parser_type = module['NorwegianProseParser']
root = module['ROOT']
for path, phrases in PHRASES.items():
    page = parser_type(root / path)
    page.feed(Path(path).read_text(encoding='utf-8'))
    assert not page.violations, page.violations
    for phrase in phrases:
        accepted = parser_type(root / path)
        accepted._check(phrase, '<p>')
        assert not accepted.violations
        changed = parser_type(root / path)
        changed._check(phrase + ' ikke', '<p>')
        assert changed.violations, 'Changed wording was incorrectly exempted'
        other = parser_type(root / 'public/articles/wr2-negative-control-not-a-page.html')
        other._check(phrase, '<p>')
        assert other.violations, 'Exemption leaked to another page'
print('15 exact approved phrase exceptions; 30 changed-text/wrong-page negative controls passed; unrelated records preserved.')
