# Hosted subscription checkout release — 30 October 2026

## Scope

Open the existing reader and fixed supporter subscription offer. Preserve the eight approved NOK prices and monthly/annual periods, open-access editorial scope, refund terms and all eleven language entrances. Earlier contribution links remain inactive. Gift products remain inactive.

Stripe owns checkout, recurring Billing records and the customer portal. This static site holds no private customer records or paid-access state and grants no entitlements from a success page. Refunds, disputes and support are administered in Stripe and through the published support contact; no custom subscription backend is represented as deployed.

## Verification

The account API reports payments and payouts enabled, no outstanding requirements and no disabled reason. Eight distinct active Payment Links were created and separately read back. Each link's line items were independently retrieved and matched to one existing price, quantity one, NOK amount and monthly/annual recurrence. No custom amount, trial, gift or third-party payment destination is included.

The existing default customer portal is active. Its public login link is enabled, invoices and payment-method updates are available, and cancellation takes effect at period end without proration. The actual live links and portal returned HTTP 200. That confirms reachability, not a completed payment or authenticated customer cancellation.

`lifecycle_verified` remains false: no live purchase, renewal, failed-payment, refund or cancellation transaction was performed. The launch gate now records the narrower observed hosted-checkout and portal configuration instead of falsely marking those end-to-end tests complete. No automatic tax configuration was changed; published prices remain final NOK prices.

Primary integration references: [Stripe no-code overview](https://docs.stripe.com/no-code/get-started), [Payment Links](https://docs.stripe.com/payment-links/create), [customer portal](https://docs.stripe.com/customer-management/activate-no-code-customer-portal). The account's remaining MCC classification request is separate from payment enablement.

## Comparison

Before: prices and terms were visible, but all checkout buttons were disabled and management/provider text described a future opening. After: eight fixed-price links lead to Stripe, the customer portal is directly available, and current payment-provider wording replaces the preparation notice. The publication, prices and substantive terms are retained.

## Reader journey

Read the publication scope; choose reader or supporter and monthly or annual billing; see renewal/refund terms; open Stripe checkout; manage invoices, payment method or period-end cancellation in the hosted portal. No reader account is required to read articles. Other language entrances retain their explicitly identified English service text.

## Semantic control

Payment buys the same ongoing open-access publication at every level. A higher supporter price gives no editorial influence or exclusive access. Recurring billing remains explicit. Source-map changes reflect the updated subscription page text; article prose and destinations are preserved. Account enablement does not prove a completed charge or settlement. No MCC correction is asserted.

## Six stages

1. Overall impression: the existing offer now supports the requested purchase action.
2. Strengths: fixed prices, billing period, editorial independence, withdrawal and support remain visible.
3. Style: plain Norwegian and English service wording; existing language navigation retained.
4. Weaknesses: disabled controls and future-tense management wording would contradict live checkout.
5. Refinement: exact hosted links, portal access and current provider wording, without rewriting substantive terms.
6. Revised version: final generated HTML is bound by exact SHA-256 in the existing review registry. This is an actual same-assistant Ariadne pass, not independent or native-speaker certification.

## Authority and validation

Bjørn Moe Aldema explicitly instructed opening the site's payment channels on 30 October 2026. The existing publication process and exact-page review registry apply. Discovery build, language binding, publication markers, Norwegian style, reader sequence, static build and 53 unit tests passed locally. Deployment and public-site readback are separate receipts.
