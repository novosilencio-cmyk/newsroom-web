"""Offline interest summary for the existing editorial queue, not a queue owner.

Inputs must eventually come from verified provider events. This prototype accepts
explicit coverage periods so monthly and annual payers can be compared fairly.
No amount weighting, payment execution, persistent reader data or publication.
"""
from datetime import date


def summarize(events, facets, start, end):
    start, end = date.fromisoformat(start), date.fromisoformat(end)
    if start >= end or len(facets) != len(set(facets)) or not facets:
        raise ValueError('Invalid observation window or facets')
    readers = {f: set() for f in facets}
    payments = {f: 0 for f in facets}
    seen = {}
    for e in events:
        required = {'event_id', 'supporter_id', 'facet', 'status', 'coverage_start', 'coverage_end'}
        if not required <= e.keys() or not e['event_id'] or not e['supporter_id']:
            raise ValueError('Missing event identity or coverage')
        if e['facet'] not in readers or e['status'] not in {'paid', 'failed', 'refunded', 'disputed'}:
            raise ValueError('Unknown facet or payment status')
        coverage_start = date.fromisoformat(e['coverage_start'])
        coverage_end = date.fromisoformat(e['coverage_end'])
        if coverage_start >= coverage_end:
            raise ValueError('Invalid coverage')
        if e['event_id'] in seen:
            if seen[e['event_id']] != e:
                raise ValueError('Conflicting event replay; reconcile first')
            continue
        seen[e['event_id']] = dict(e)
        if e['status'] != 'paid' or coverage_start >= end or coverage_end <= start:
            continue
        readers[e['facet']].add(e['supporter_id'])
        payments[e['facet']] += 1
    result = [{'facet': f, 'paid_readers': len(readers[f]),
               'paid_events_covering_window': payments[f],
               'interpretation': 'OBSERVED_SIGNAL_NOT_EDITORIAL_AUTHORITY'} for f in facets]
    # Stable tie order preserves the existing facet order; zero is not low value.
    return sorted(result, key=lambda r: -r['paid_readers'])


def review_candidates(candidates, signals, facets):
    """Separate first-interest candidates, remaining coverage and source holds.

    Callers pass existing queue IDs. This does not create or rewrite a story queue.
    Corrections/urgent public-interest work are surfaced separately for the editor.
    """
    ranks = {s['facet']: i for i, s in enumerate(signals) if s['paid_readers'] > 0}
    first, rest, holds, urgent = [], [], [], []
    seen = set()
    for c in candidates:
        if not {'id', 'facet', 'source_ready', 'constructive_question', 'urgent'} <= c.keys():
            raise ValueError('Candidate must declare readiness, question and urgency')
        if c['id'] in seen or not c['id'] or c['facet'] not in facets:
            raise ValueError('Unknown facet or duplicate queue identity')
        if type(c['source_ready']) is not bool or type(c['urgent']) is not bool:
            raise ValueError('Readiness and urgency must be booleans')
        seen.add(c['id'])
        if not c['source_ready'] or not isinstance(c['constructive_question'], str) or not c['constructive_question'].strip():
            holds.append({'id': c['id'], 'reason': 'SOURCE_OR_CONSTRUCTIVE_BASIS_MISSING'})
        elif c['urgent']:
            urgent.append(c['id'])
        elif c['facet'] in ranks:
            first.append(c)
        else:
            rest.append(c['id'])
    first.sort(key=lambda c: ranks[c['facet']])
    return {'first_interest': [c['id'] for c in first], 'remaining_coverage': rest,
            'urgent_editor_review': urgent, 'source_holds': holds,
            'unrepresented_facets': [f for f in facets if not any(c['facet'] == f for c in candidates)],
            'automatic_publication': False}
