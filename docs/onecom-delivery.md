# Website delivery to one.com

GitHub remains the source of published content. The one.com workflow runs the
same editorial checks and build as GitHub Pages before transferring `_site`.
GitHub Pages remains available as a rollback host.

## Access and destinations

The repository secret `ONECOM_SFTP_PASSWORD` is supplied only to the deployment
step. It must never be put in source, issue comments, output or artifacts.
The SFTP host key is pinned in `scripts/deploy_onecom.py`; a changed key stops
deployment. The initial key was observed on 2026-11-03 before using credentials.

- Staging: `expnr-pages.experimentalnewsroom.org`
- Production: `experimentalnewsroom.org`
- Targets are fixed in the script; workflow inputs cannot supply arbitrary paths.
- Staging sends an HTTP noindex header. Public HTML is unchanged.
- Hosting configuration forces HTTPS and disables directory listings.

## Verification and rollback

Before changing public files, deployment writes and reads back a ZIP backup in
the SFTP user's private home under `onecom-deploy-backups`. This location is
outside the public webroots. Keep these backups until retention is explicitly
decided.

Changed files are uploaded to a staging directory and compared byte for byte
before promotion. Promotion uses atomic per-file rename, with the front page
and manifest last. This is not a whole-site atomic switch. A promotion or final
readback failure triggers restoration of files already changed.

The ZIP contains previous file bytes and `_rollback.json` identifying files
that did not exist before the deployment. For manual recovery, restore the ZIP
contents except `_rollback.json` into its recorded root and remove only the
listed newly-created paths. Validate HTTPS and representative articles after
restoration. A disconnected process may require this manual restoration.

The eight identified migration archives/folders are moved to
`onecom-migration-artifacts` in the private SFTP home on production deployment.
No unrelated web content, mailbox or DNS setting is removed by the script.

DNS rollback uses the preserved pre-migration records in the private operations
return point. Do not reset the domain's entire DNS zone.
