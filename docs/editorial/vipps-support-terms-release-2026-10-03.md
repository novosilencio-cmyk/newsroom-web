# Vipps support terms release — 3 October 2026

## Scope and authority

Working object: `public/support-terms.html` on PR #87.

Bjørn Moe Aldema ordered completion of the Vipps support-terms work and clarified
on 3 October 2026 that an implementation order includes merge/publication when
the requested object is mature and the controls pass, unless merge or publication
is expressly reserved. This record binds that approval only to the page digest
`ad05428677a73a5b8ab065849e23c9f7764f8aa45af37288aa7ac2a5748938a2`.

The change does not activate Vipps, create a payment credential or verify a
successful payment. Those remain later operational gates after Vipps approval.

## Sources and evidence boundary

The review used:

- the previous published support terms as the preserved baseline;
- Vipps' application prompts requiring payment, cancellation/withdrawal,
  return/refund and complaint information;
- the existing Experimental Newsroom support model: voluntary support without a
  promised article, service, influence, access or financial return;
- Forbrukertilsynet's Angrerettloven overview;
- the current Angrerettloven and the government's guidance and standard form;
- Ariadne's language comparison and realization workflow at git blob
  `713f6796610652407037c7a0d69385e29d30f727`.

The official consumer guidance primarily describes distance contracts for goods
and services. The page therefore does not claim that every voluntary gift is a
statutory consumer purchase. It instead creates an express voluntary 14-day
refund promise and preserves any mandatory rights that may apply.

## Helhetsinntrykk

The baseline correctly identified the recipient, purpose, editorial independence,
payment provider and contact route. Its main weakness was operational: a donor
could not tell what would happen after a mistaken payment, duplicate payment,
change of mind or cancellation of recurring support.

The revision remains a support agreement rather than turning the relationship
into a sale of journalism.

## Styrker

- The recipient, organisation number and contact route remain prominent.
- The purpose of the support remains concrete.
- Editorial independence remains explicit.
- The donor chooses the amount before confirmation.
- Vipps MobilePay remains responsible for payment processing under its own terms.

## Stilprofil

The page uses short functional sections, direct questions and plain Norwegian.
The revision keeps the established reader-facing structure and avoids legalistic
claims that the evidence does not establish.

## Konkrete svakheter i baseline

1. Cancellation of recurring support was present but not separated from refunds
   of already completed payments.
2. There was no explicit response to an unintended amount or duplicate payment.
3. There was no clear statement about return of goods when no goods are supplied.
4. The complaint route did not explain what information helps identify a payment.
5. The earlier use of `donasjon` could be read as tied to the rejected Vipps
   Donations product rather than the broader voluntary-support relationship.

## Forbedringsgrep

- Define support as a voluntary gift without a promised good or service.
- Show amount, recipient and frequency before confirmation.
- Separate future cancellation from past-payment refund.
- Offer full refund of a one-time payment requested within 14 days.
- Route wrong, duplicate and unrecognized payments explicitly.
- Preserve mandatory rights without asserting a statutory classification that
  has not been established.
- Use `betalingsløsningen` rather than product-specific donation wording where
  the terms apply across the planned Vipps setup.

## Revidert eksempelversjon

The realized page is the example version. Its central reader path is:

`recipient → purpose → payment confirmation → recurring cancellation → refund → error handling → privacy → complaints → editorial independence`.

## Comparison and reader journey

Gain: the donor can now predict the practical outcome of the most consequential
payment events.

Preserved: support remains voluntary and does not purchase journalism,
influence, access or return.

Cost: Experimental Newsroom assumes a voluntary refund commitment for qualifying
one-time payments. Bjørn approved completion of this exact version.

Counterexample: if Experimental Newsroom later sells a subscription, article,
event ticket or other service with a counter-performance, these gift terms alone
will not be sufficient. That product will require its own terms and legal review.

## Semantic control and preservation

- `14 days` is an express contractual refund promise, not an unsupported claim
  that the contribution is necessarily a purchase governed by every rule for
  goods and services.
- `normally no later than 14 days` applies after the payment can be identified.
- Unauthorized payments are not handled solely as ordinary refunds; the donor is
  also directed to Vipps MobilePay or the bank.
- No physical return process is invented because no goods are delivered.

## Review execution

Same-assistant bounded review with Diana/Eva object control and Ariadne's six
stages. No independent lawyer or separate human reviewer is claimed. Bjørn's
publication and merge approval is the owner decision for this exact page version.

Decision: `COMBINE` — preserve the baseline's support identity and add the
missing operational protections.

Ariadne style readiness: `pass_complete`.

Source status: `READY_FOR_EDITORIAL_REVIEW`.

## Verification and rollback

Verified on the branch:

- exact page digest:
  `ad05428677a73a5b8ab065849e23c9f7764f8aa45af37288aa7ac2a5748938a2`;
- recipient and organisation number present;
- no-counter-performance statement present;
- 14-day refund route present;
- recurring cancellation, error payment and complaint routes present;
- 10 opening and 10 closing `section` elements.

Rollback: revert the PR merge. That restores the previous terms but also removes
the new refund and error-payment protections.
