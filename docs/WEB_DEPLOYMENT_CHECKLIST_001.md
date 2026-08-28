# Web deployment checklist 001

Status: INTERNAL / DEPLOYMENT PREPARED / NOT DEPLOYED

## Current architecture

Static site in `newsroom-web` with:
- `index.html`
- `support.html`
- `styles.css`
- `script.js`
- structured article/source data
- internal editorial and Argentina working documents

## Deployment mechanism

A guarded GitHub Pages workflow now exists at `.github/workflows/pages.yml`.

It can deploy only when:
1. the workflow is manually dispatched, or
2. the workflow exists on `main` and a push reaches `main`.

Because the workflow currently exists only on the unmerged work branch, adding it does not itself publish the site.

## Before public deployment

1. Review public-facing copy and remove all prototype-only language that should not be public.
2. Confirm which internal files/directories must never be part of a public Pages artifact. Current `docs/` material contains internal working documents and therefore must be excluded from the public deployment artifact before launch.
3. Separate the public web root from internal working documents, or change the Pages upload step to publish only an explicit public directory.
4. Confirm public name/masthead and basic About wording.
5. Confirm support-page legal/accounting wording before activating payment links.
6. Confirm no protected OØS material, private data, credentials or internal-only method files are exposed.
7. Run mobile/desktop accessibility and link checks.
8. Decide domain strategy: temporary GitHub Pages URL first or custom domain.
9. Obtain GK before merge/public deployment.

## Critical finding

**Do not deploy the repository root as-is.**

The repository now contains internal Argentina/team/method documents under `docs/`. A safe public deployment should upload an explicit `public/` directory (or equivalent generated artifact) containing only the files intended for visitors.

## Next reversible step

Create a `public/` deployment surface containing the static site assets and public content only, then update the Pages workflow to upload `public/` rather than the repository root.

This preserves the internal working branch while making the publish boundary explicit.
