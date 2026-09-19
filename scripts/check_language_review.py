#!/usr/bin/env python3
"""Check version-bound editorial attestations, not prose quality or authority truth."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# Migration baseline only: unchanged legacy pages are NOT retroactively reviewed.
BASELINE = '0399388a9f0ec49d79df9af714ef62ff75a0e6a6'
RECEIPTS = 'docs/editorial/language-reviews.json'
STAGES = ('helhetsinntrykk', 'styrker', 'stilprofil', 'konkrete_svakheter',
          'forbedringsgrep', 'revidert_eksempelversjon')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def populated(value):
    return isinstance(value, str) and bool(value.strip())


def receipt_errors(row, data):
    errors = []
    if not isinstance(row, dict):
        return ['missing receipt']
    if row.get('sha256') != digest(data):
        errors.append('review belongs to another content version')
    for field in ('case_id', 'reviewer', 'execution_context', 'reviewed_at',
                  'comparison_ref', 'reader_journey_ref', 'semantic_control_ref'):
        if not populated(row.get(field)):
            errors.append('missing ' + field)
    modules = row.get('loaded_modules')
    if not isinstance(modules, list) or not modules or not all(
        isinstance(m, dict) and all(populated(m.get(k)) for k in ('source', 'revision', 'application_ref'))
        for m in modules
    ):
        errors.append('modules must record source, revision and application')
    stages = row.get('stages')
    if not isinstance(stages, dict) or not all(populated(stages.get(s)) for s in STAGES):
        errors.append('six-stage review evidence missing')
    if row.get('decision') not in ('KEEP', 'REVISE', 'COMBINE'):
        errors.append('language decision unresolved')
    if row.get('ariadne_style_readiness') != 'pass_complete':
        errors.append('language readiness unresolved')
    if row.get('source_status') != 'READY_FOR_EDITORIAL_REVIEW':
        errors.append('source clearance missing or held')
    approval = row.get('publication_approval')
    if not isinstance(approval, dict) or approval.get('approved') is not True or not all(
        populated(approval.get(k)) for k in ('by', 'reference')
    ) or approval.get('sha256') != digest(data):
        errors.append('separate version-bound publication approval missing')
    return errors


def check(root=ROOT):
    errors = []
    try:
        subprocess.run(['git', 'cat-file', '-e', BASELINE + '^{commit}'], cwd=root,
                       check=True, capture_output=True)
        rows = json.loads((root / RECEIPTS).read_text())
        if not isinstance(rows, dict):
            raise ValueError('receipt registry must be an object')
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        return ['cannot establish baseline or receipt registry: ' + str(exc)]
    paths = sorted((root / 'public').rglob('*.html'))
    active = set()
    for path in paths:
        rel = path.relative_to(root).as_posix()
        active.add(rel)
        data = path.read_bytes()
        previous = subprocess.run(['git', 'show', BASELINE + ':' + rel], cwd=root,
                                  capture_output=True)
        if rel not in rows and previous.returncode == 0 and previous.stdout == data:
            continue  # Explicit migration exception, not a language PASS.
        errors.extend(rel + ': ' + e for e in receipt_errors(rows.get(rel), data))
    for rel in rows:
        if rel not in active:
            errors.append(rel + ': receipt target is not an existing public HTML page')
    return errors


if __name__ == '__main__':
    errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    print('Language-review evidence check: ' + ('FAIL' if errors else 'PASS') +
          '. Attestations do not prove editorial quality; unchanged legacy pages are exempt.')
    sys.exit(bool(errors))
