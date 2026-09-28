#!/usr/bin/env python3
"""Build the deployable site and attach the consent-gated analytics adapter to every HTML page."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE = ROOT / "_site"


def _relative_asset_path(page: Path, asset_name: str) -> str:
    relative = os.path.relpath(SITE, page.parent).replace(os.sep, "/")
    prefix = "" if relative == "." else f"{relative}/"
    return f"{prefix}{asset_name}"


def build() -> int:
    if not PUBLIC.is_dir():
        raise SystemExit(f"Public source directory not found: {PUBLIC}")
    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(PUBLIC, SITE)

    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        raise SystemExit("No HTML pages found in the public site.")

    for page in pages:
        source = page.read_text(encoding="utf-8")
        config_path = _relative_asset_path(page, "analytics-config.js")
        adapter_path = _relative_asset_path(page, "analytics.js")
        additions: list[str] = []
        if not re.search(r"<script\\b[^>]*\\bsrc=[\"'][^\\"']*analytics-config\\.js[\"']", source, re.I):
            additions.append(f'<script src="{config_path}"></script>')
        if not re.search(r"<script\\b[^>]*\\bsrc=[\"'][^\\"']*analytics\\.js[\"']", source, re.I):
            additions.append(f'<script src="{adapter_path}"></script>')
        if not additions:
            continue

        injection = "\\n" + "\\n".join(additions) + "\\n"
        body_close = re.search(r"</body\\s*>", source, re.I)
        if body_close:
            source = source[:body_close.start()] + injection + source[body_close.start():]
        else:
            source += injection
        page.write_text(source, encoding="utf-8")

    print(f"Built {len(pages)} HTML pages with the consent-gated analytics adapter.")
    return len(pages)


if __name__ == "__main__":
    build()
