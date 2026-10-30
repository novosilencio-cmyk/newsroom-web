"""Render the subscription offer and terms from one fixed-price catalogue."""
import json
from html import escape as esc
from urllib.parse import urlsplit

BASE = 'https://experimentalnewsroom.org/'
PORTAL = 'https://billing.stripe.com/p/login/aFa14nawe6GBg9b5MjbEA00'
CONTACT = '<a href="mailto:support@experimentalnewsroom.org">support@experimentalnewsroom.org</a> · <a href="tel:+4748448958" dir="ltr">+47 48 44 89 58</a>'
ADDRESS = 'MOE JOE ALDEMA · org.nr. 927 532 573<br/>c/o Bjørn Moe Aldema, Andreas Nordlands veg 10, 2819 Gjøvik, Norge'

def catalogue(public):
    data = json.loads((public / 'content/subscriptions.json').read_text())
    expected = {'reader-month':79, 'reader-year':790, 'supporter149-month':149,
                'supporter1490-year':1490, 'supporter249-month':249, 'supporter2490-year':2490,
                'supporter499-month':499, 'supporter4990-year':4990}
    if {p['key']: p['amount_nok'] for p in data['offers']} != expected:
        raise ValueError('Subscription catalogue differs from approved prices')
    for p in data['offers']:
        if p['checkout_url']:
            url = urlsplit(p['checkout_url'])
            if url.scheme != 'https' or url.netloc != 'buy.stripe.com' or url.query or url.fragment:
                raise ValueError('Expected a verified hosted Stripe subscription link')
    if data['sales_enabled']:
        verification = data.get('hosted_checkout_verification', {})
        # This static publication has no paid access or local subscription state.
        # Stripe Billing and its hosted portal own the recurring lifecycle.
        # An actual paid/renewal/refund test remains separately recorded.
        hosted_ready = (
            verification.get('flow') == 'stripe_hosted_payment_links'
            and verification.get('charges_enabled') is True
            and verification.get('payouts_enabled') is True
            and verification.get('portal_active') is True
            and verification.get('portal_url') == PORTAL
            and verification.get('cancellation_mode') == 'at_period_end'
            and verification.get('verified_offer_keys') == sorted(expected)
        )
        if not hosted_ready or any(not p['checkout_url'] for p in data['offers']):
            raise ValueError('Opening sales requires verified hosted links, account and cancellation portal')
        if len({p['checkout_url'] for p in data['offers']}) != len(expected):
            raise ValueError('Each subscription offer requires its own verified payment link')
    return data

def shell(lang, filename, title, deck, body, alternates='', navigation=''):
    nb = lang == 'nb'
    home = 'nb/' if nb else 'en/'
    return f'''<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if lang == 'ar' else ''}><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} — Experimental Newsroom</title><meta name="description" content="{esc(deck, quote=True)}"/>
<link rel="canonical" href="{BASE}{filename}"/>{alternates}
<link href="styles.css" rel="stylesheet"/><link href="reader-navigation.css" rel="stylesheet"/><link href="reader-support.css" rel="stylesheet"/><link href="subscriptions.css" rel="stylesheet"/>
<link href="favicon.svg" rel="icon" type="image/svg+xml"/></head><body>
<a class="reader-skip" href="#reader-main">{'Gå til innholdet' if nb else 'Skip to content'}</a>
<header class="masthead compact-masthead"><div class="edition-line"><span>Experimental Newsroom</span><a href="{home}">{'Forsiden' if nb else 'Front page'}</a></div>
<h1>{esc(title)}</h1><p class="strapline">{esc(deck)}</p>{navigation}</header>
<main id="reader-main" tabindex="-1">{body}</main>
<footer><p>{ADDRESS}</p><p>{CONTACT}</p><p><a href="support.html" lang="nb">Abonnement</a> · <a href="subscription-terms.html" lang="nb">Vilkår</a> · <a href="subscription-terms.en.html" lang="en">Terms</a> · <a href="privacy.html" lang="nb">Personvern</a> · <a href="{'sitemap.html' if nb else 'sitemap.en.html'}">{'Finn frem' if nb else 'Site map'}</a></p></footer></body></html>
'''

def section(title, text, ident=''):
    return f'<section class="section-block"{(" id=" + chr(34) + ident + chr(34)) if ident else ""}><h2>{title}</h2>{text}</section>'

def paragraph(text):
    return '<p class="measure">' + text + '</p>'

def card(p, nb, enabled):
    group = p['group']
    title = ({'reader':'Leserabonnement', 'supporter':'Støtteabonnement'} if nb else {'reader':'Reader subscription', 'supporter':'Supporter subscription'})[group]
    period = ('måned' if p['interval']=='month' else 'år') if nb else ('month' if p['interval']=='month' else 'year')
    terms = ('Fornyes hver måned til du sier opp.' if p['interval']=='month' else 'Fornyes hvert år til du sier opp.') if nb else ('Renews monthly until cancelled.' if p['interval']=='month' else 'Renews annually until cancelled.')
    amount = f"{p['amount_nok']:,}".replace(',', ' ')
    price = f'{amount} kr / {period}'
    label = f"{'Bestill' if nb else 'Subscribe'} · {price}"
    action = f'<a class="support-button" href="{esc(p["checkout_url"], quote=True)}">{label}</a>' if enabled else f'<button type="button" disabled>{"Betaling klargjøres" if nb else "Checkout being prepared"}</button>'
    return f'<article class="subscription-card"><h3>{title}</h3><p class="subscription-price"><bdi>{price}</bdi></p><p>{terms}</p>{action}</article>'

def offer_body(data, nb):
    body = section('Et abonnement på journalistikken' if nb else 'A subscription to the journalism', paragraph(
        'Experimental Newsroom er en nettpublikasjon med journalistikk, analyser og essays om hvordan samfunnet virker. Abonnementet gjelder den løpende publikasjonen. Artiklene er også åpne for andre lesere. Du trenger ingen leserkonto.' if nb else
        'Experimental Newsroom publishes journalism, analysis and essays about how society works. Your subscription is to the ongoing publication. Articles remain open to other readers too. You do not need a reader account.'))
    if not data['sales_enabled']:
        body += '<p class="subscription-status" role="status">' + ('Tilbudet og prisene vises nedenfor. Betaling åpnes først etter betalingsleverandørens godkjenning og ferdigstilling av bestillingsløsningen. Ingen bestilling eller belastning skjer på denne siden nå.' if nb else 'The offer and prices are shown below. Checkout will open only after payment-provider approval and completion of the ordering service. This page currently creates no order or charge.') + '</p>'
    for group in ['reader', 'supporter']:
        title = ({'reader':'Velg leserabonnement', 'supporter':'Velg støtteabonnement'} if nb else {'reader':'Choose a reader subscription', 'supporter':'Choose a supporter subscription'})[group]
        detail = ''
        if group == 'supporter':
            detail = paragraph('Velg et fast støttenivå. Alle nivåene gir samme publikasjon. Den høyere prisen bidrar til mer økonomisk rom for research, kildearbeid og publisering. Redaksjonen velger selv saker, kilder og konklusjoner.' if nb else 'Choose a fixed supporter level. Every level provides the same publication. The higher price contributes more towards research, source work and publishing. The newsroom makes its own decisions about stories, sources and conclusions.')
        body += section(title, detail + '<div class="subscription-grid">' + ''.join(card(p,nb,data['sales_enabled']) for p in data['offers'] if p['group']==group) + '</div>', group)
    body += section('Pris, fornyelse og oppsigelse' if nb else 'Price, renewal and cancellation', paragraph(
        'Alle priser er sluttpriser i norske kroner (NOK). Måneds- og årsabonnement betales på forskudd og fornyes automatisk for samme periode til du sier opp. Ingen ekstra bindingstid eller oppsigelsesgebyr. Si opp før neste fornyelse; abonnementet løper ut ved slutten av den betalte perioden. Banken kan ta betalt for valutaveksling.' if nb else
        'All prices are final prices in Norwegian kroner (NOK). Monthly and annual subscriptions are paid in advance and renew automatically for the same period until cancelled. There is no additional minimum term or cancellation fee. Cancel before the next renewal; the subscription ends at the end of the paid period. Your bank may charge for currency conversion.'))
    management = ('Se fakturaer, oppdater betalingsmåte eller si opp før neste fornyelse på kundesiden. Oppsigelsen får virkning ved slutten av den betalte perioden.' if nb else 'View invoices, update your payment method or cancel before the next renewal in the customer portal. Cancellation takes effect at the end of the paid period.') if data['sales_enabled'] else ('Når betaling åpnes, vil du få informasjon om hvordan abonnementet administreres. Kontakt oss hvis du har spørsmål.' if nb else 'When checkout opens, you will receive information about managing your subscription. Contact us if you have questions.')
    portal = f'<p><a href="{PORTAL}">{"Åpne kundesiden" if nb else "Open customer portal"}</a></p>' if data['sales_enabled'] else ''
    body += section('Administrer abonnementet' if nb else 'Manage your subscription', paragraph(management) + portal + f'<p>{CONTACT}</p>')
    body += section('Angrerett, refusjon og kundeservice' if nb else 'Withdrawal, refunds and support', paragraph(
        'Du kan angre på en nettbestilling innen 14 dager etter at avtalen er inngått. I tillegg gir vi full refusjon på forespørsel innen 14 dager etter hver abonnementsbetaling. Garantien gjelder også fornyelser og begrenser ingen lovfestede rettigheter. Kontakt oss med kjøpsdato, beløp og e-postadresse brukt ved kjøpet. Kortnummer skal aldri sendes til oss.' if nb else
        'You can withdraw from an online order within 14 days of entering the agreement. We also offer a full refund on request within 14 days of each subscription payment, including renewals. This guarantee does not limit statutory rights. Contact us with the purchase date, amount and email address used at checkout. Never send us card numbers.') + f'<p>{CONTACT}</p><p><a href="subscription-terms{ "" if nb else ".en"}.html">{"Les abonnementsvilkår og angreskjema" if nb else "Read subscription terms and withdrawal form"}</a></p>')
    body += section('Dette inngår i abonnementet' if nb else 'What the subscription includes', paragraph(
        'Abonnementet gjelder nettpublikasjonen, uten eksklusiv tilgang, fast publiseringshyppighet, personlig rådgivning eller redaksjonell innflytelse. Alle artikler kan leses uten betaling. E-postutgave, full oversettelse til alle språk, Atriet og andre fysiske prosjekter ligger utenfor abonnementet. Tidligere engangsstøtte blir aldri omgjort til abonnement.' if nb else
        'The subscription covers the online publication, without exclusive access, a fixed publishing frequency, personal advice or editorial influence. All articles can be read without payment. An email edition, translation of every article into every language, Atriet and other physical projects are outside this subscription. Earlier one-time contributions are never converted into subscriptions.'))
    provider = ('Betaling og løpende fakturering håndteres av Stripe. Les ' if nb else 'Payments and recurring billing are handled by Stripe. Read our ') if data['sales_enabled'] else ('Stripe er planlagt som betalingsleverandør. Les ' if nb else 'Stripe is the intended payment provider. Checkout is not open. Read our ')
    body += paragraph(provider + '<a href="privacy.html" lang="nb">' + ('personvernerklæringen' if nb else 'privacy policy in Norwegian') + '</a>.')
    return body

def terms_body(data, nb):
    groups = [
      ('Avtalepart og kontakt' if nb else 'Publisher and contact', f'<p>{ADDRESS}</p><p>{CONTACT}</p>'),
      ('Publikasjonen' if nb else 'The publication', paragraph('Avtalen gjelder Experimental Newsrooms løpende nettpublikasjon med journalistikk, analyser og essays. Artiklene er åpne for alle. Leserabonnement og alle støttenivåer gir samme publikasjon. Betaling gir ingen redaksjonell innflytelse, eksklusiv tilgang, fast publiseringshyppighet, personlig rådgivning, e-postutgave eller garanti om full oversettelse. Atriet og andre fysiske prosjekter faller utenfor avtalen.' if nb else 'This agreement covers Experimental Newsroom’s ongoing online publication of journalism, analysis and essays. Articles are open to everyone. Reader and supporter subscriptions provide the same publication. Payment does not buy editorial influence, exclusive access, a fixed publishing frequency, personal advice, an email edition or a guarantee of full translation. Atriet and other physical projects are outside this agreement.')),
      ('Priser og betaling' if nb else 'Prices and payment', paragraph('Leser: 79 kr/måned eller 790 kr/år. Støtte: 149, 249 eller 499 kr/måned, eller 1 490, 2 490 eller 4 990 kr/år. Alle beløp er sluttpriser i NOK. Stripe viser valgt pris og betalingsperiode før du bekrefter en bestilling med betalingsplikt. Banken kan ta betalt for valutaveksling. Kvittering og avtalebekreftelse sendes til e-postadressen du oppgir.' if nb else 'Reader: NOK 79/month or NOK 790/year. Supporter: NOK 149, 249 or 499/month, or NOK 1,490, 2,490 or 4,990/year. All amounts are final prices in NOK. Stripe shows the selected price and billing period before you confirm an order with an obligation to pay. Your bank may charge for currency conversion. A receipt and agreement confirmation are sent to the email address you provide.')),
      ('Varighet, fornyelse og oppsigelse' if nb else 'Term, renewal and cancellation', paragraph('Løpende abonnement starter på kjøpsdatoen, betales på forskudd og fornyes automatisk for én måned eller ett år av gangen. Si opp før neste fornyelse via kundesiden eller kontakt oss. Oppsigelsen bekreftes og får virkning ved utløpet av den betalte perioden. Ingen ekstra bindingstid eller oppsigelsesgebyr. Endring av kort avslutter aldri abonnementet; bruk oppsigelsesvalget. Prisendringer varsles før de får virkning, slik at du kan avslutte før ny pris belastes.' if nb else 'A recurring subscription starts on the purchase date, is paid in advance and renews automatically for one month or one year at a time. Cancel before the next renewal through the customer portal or by contacting us. Cancellation is confirmed and takes effect at the end of the paid period. There is no additional minimum term or cancellation fee. Updating a card does not cancel a subscription; use the cancellation option. Price changes are notified before taking effect so you can cancel before a new price is charged.') + f'<p><a href="{PORTAL}">{"Administrer abonnementet" if nb else "Manage subscription"}</a></p>'),
      ('Angrerett og refusjon' if nb else 'Withdrawal and refunds', paragraph('Ved nettbestilling har du 14 dagers angrerett fra dagen etter at avtalen er inngått. Send en tydelig melding til oss før fristen. Du kan bruke angreskjemaet nedenfor eller egne ord, uten å oppgi grunn. Vi krever ingen fraskrivelse av angreretten. Vår tilleggsgaranti gir full refusjon ved forespørsel innen 14 dager etter hver betaling, også fornyelser. Vi betaler tilbake til opprinnelig betalingsmåte senest 14 dager etter mottatt melding. Ved full refusjon avsluttes den tilhørende betalte perioden og videre fornyelse. Lovfestede rettigheter gjelder i tillegg.' if nb else 'For online orders, you have a 14-day right of withdrawal starting the day after entering the agreement. Send us a clear message before the deadline. Use the form below or your own words, without giving a reason. We do not require you to waive this right. Our additional guarantee offers a full refund on request within 14 days of each payment, including renewals. We refund the original payment method within 14 days of receiving your request. A full refund ends the corresponding paid period and future renewal. Statutory rights apply in addition.')),
      ('Feil, mangler og opphør' if nb else 'Errors, defects and closure', paragraph('Kontakt oss ved dobbeltbetaling, ukjent trekk, feil pris, uteblitt bekreftelse eller mangler ved leveransen. Behold kvitteringen og unngå ny bestilling før saken er avklart. Feilbelastninger rettes. Ved nedleggelse stanser vi fremtidige trekk og refunderer uleverte deler av forhåndsbetalte perioder. Tidligere engangsstøtte beholder sine opprinnelige vilkår og blir aldri løpende abonnement.' if nb else 'Contact us about duplicate payments, unknown charges, incorrect prices, missing confirmations or defects in delivery. Keep your receipt and avoid ordering again until the issue is resolved. Incorrect charges are corrected. If the publication closes, we stop future charges and refund undelivered portions of prepaid periods. Earlier one-time contributions retain their original terms and are never converted into recurring subscriptions.') + '<p><a href="support-terms.html" lang="nb">' + ('Vilkår for tidligere engangsstøtte' if nb else 'Earlier one-time contribution terms in Norwegian') + '</a></p>'),
      ('Personvern og klager' if nb else 'Privacy and complaints', paragraph('Opplysninger brukes til avtalen, betaling, kundeservice og lovpålagt regnskap. Markedsføring krever eget grunnlag. Send klagen til oss først. Dersom vi står uten løsning, kan du be Forbrukertilsynet om mekling. Ufravikelige forbrukerrettigheter gjelder uansett disse vilkårene.' if nb else 'Data is used for the agreement, payments, customer support and legally required accounting. Marketing requires a separate basis. Complain to us first. If the matter remains unresolved, you can request mediation from the Norwegian Consumer Authority. Mandatory consumer rights apply regardless of these terms.') + '<p><a href="privacy.html" lang="nb">Personvern</a> · <a href="https://www.forbrukertilsynet.no/har-du-en-klage">Forbrukertilsynet</a></p>')
    ]
    body = paragraph('Vilkårsversjon 29. oktober 2026. Gjelder nye abonnementsbestillinger fra åpningen av bestillingstjenesten.' if nb else 'Terms version 29 October 2026. Applies to new subscription orders from the opening of checkout.')
    body += ''.join(section(t,b) for t,b in groups)
    body += section('Angreskjema' if nb else 'Withdrawal form', paragraph('Fyll ut feltene og send teksten på e-post eller per post dersom du vil angre. Du kan også sende en annen tydelig melding. Underskrift kreves bare på papir.' if nb else 'Complete the fields and send the text by email or post to withdraw. You can also send another clear statement. A signature is needed only on paper.') + f'<div class="withdrawal-form"><p>{"Til" if nb else "To"}: {ADDRESS}<br/>support@experimentalnewsroom.org</p><p>{"Jeg melder at jeg ønsker å gå fra avtalen om følgende abonnement:" if nb else "I give notice that I withdraw from the agreement for the following subscription:"}</p><p>{"Abonnement / ordrenummer" if nb else "Subscription / order number"}: ____________________</p><p>{"Bestilt dato" if nb else "Order date"}: ____________________</p><p>{"Navn" if nb else "Name"}: ____________________</p><p>{"Adresse" if nb else "Address"}: ____________________</p><p>{"E-post brukt ved kjøpet" if nb else "Email used at checkout"}: ____________________</p><p>{"Dato og eventuell underskrift" if nb else "Date and signature, if on paper"}: ____________________</p></div><p><button type="button" onclick="window.print()">{"Skriv ut eller lagre som PDF" if nb else "Print or save as PDF"}</button></p>', 'withdrawal')
    return body

def build(public, rows):
    data = catalogue(public)
    alt = ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{s["file"]}"/>' for lang,s in rows.items()) + f'<link rel="alternate" hreflang="x-default" href="{BASE}support.en.html"/>'
    for lang,s in rows.items():
        nb = lang == 'nb'
        navigation = '<nav class="support-languages" aria-label="Choose a language">' + ' '.join(f'<a href="{r["file"]}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code==lang else '')+f'>{esc(r["name"])}</a>' for code,r in rows.items()) + '</nav>'
        body = offer_body(data, nb)
        if lang not in ('nb','en'):
            body = paragraph(esc(s['deck'])) + '<div lang="en" dir="ltr">' + body + '</div>'
        (public/s['file']).write_text(shell(lang,s['file'],s['page_title'],s['deck'],body,alt,navigation))
    for nb in (True,False):
        file = 'subscription-terms.html' if nb else 'subscription-terms.en.html'
        (public/file).write_text(shell('nb' if nb else 'en',file,'Abonnementsvilkår' if nb else 'Subscription terms','Pris, fornyelse, oppsigelse, angrerett og kundeservice.' if nb else 'Prices, renewals, cancellation, withdrawal and support.',terms_body(data,nb),'<link rel="alternate" hreflang="nb" href="'+BASE+'subscription-terms.html"/><link rel="alternate" hreflang="en" href="'+BASE+'subscription-terms.en.html"/>'))
    (public.parent/'support.html').write_text((public/'support.html').read_text())
