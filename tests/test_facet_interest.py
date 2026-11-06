import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from facet_interest import summarize, review_candidates

FACETS = ['society', 'nature', 'culture', 'learning', 'newsroom']

def event(i, reader='a', facet='nature', status='paid', end='2026-11-01'):
    return dict(event_id=i, supporter_id=reader, facet=facet, status=status,
                coverage_start='2026-10-01', coverage_end=end)

class FacetInterestTests(unittest.TestCase):
    def summary(self, es):
        return summarize(es, FACETS, '2026-10-01', '2026-11-01')

    def test_frequency_and_large_amount_do_not_multiply_one_reader(self):
        a=event('1');a['amount']=1000000
        es=[a,event('2'),event('3',reader='b',facet='society'),event('4',reader='c',facet='society')]
        rows=self.summary(es)
        self.assertEqual(rows[0]['facet'],'society')
        self.assertEqual(next(r for r in rows if r['facet']=='nature')['paid_readers'],1)

    def test_annual_and_monthly_coverage_count_once_each(self):
        rows=self.summary([event('1',end='2027-10-01'),event('2',reader='b')])
        self.assertEqual(rows[0]['paid_readers'],2)

    def test_replay_and_reversed_payments(self):
        e=event('1');rows=self.summary([e,e,event('2',reader='b',status='refunded'),event('3',status='failed'),event('4',status='disputed')])
        self.assertEqual(rows[0]['paid_readers'],1)
        self.assertEqual(rows[0]['paid_events_covering_window'],1)
        with self.assertRaises(ValueError):self.summary([e,event('1',status='refunded')])

    def test_unknown_and_invalid_events_fail_closed(self):
        with self.assertRaises(ValueError):self.summary([event('1',facet='fake')])
        with self.assertRaises(ValueError):summarize([],FACETS,'2026-11-01','2026-10-01')

    def test_zero_data_keeps_portfolio_and_no_publication(self):
        c=[dict(id='nature-case',facet='nature',source_ready=True,constructive_question='What worked for whom?',urgent=False)]
        result=review_candidates(c,self.summary([]),FACETS)
        self.assertEqual(result['first_interest'],[])
        self.assertEqual(result['remaining_coverage'],['nature-case'])
        self.assertFalse(result['automatic_publication'])
        self.assertIn('culture',result['unrepresented_facets'])

    def test_source_gate_and_urgent_work_survive_payment_interest(self):
        cs=[dict(id='weak',facet='nature',source_ready=False,constructive_question='Question',urgent=False),
            dict(id='first',facet='nature',source_ready=True,constructive_question='Question',urgent=False),
            dict(id='other',facet='culture',source_ready=True,constructive_question='Question',urgent=False),
            dict(id='correction',facet='society',source_ready=True,constructive_question='Question',urgent=True)]
        result=review_candidates(cs,self.summary([event('1')]),FACETS)
        self.assertEqual(result['first_interest'],['first'])
        self.assertEqual(result['remaining_coverage'],['other'])
        self.assertEqual(result['urgent_editor_review'],['correction'])
        self.assertEqual(result['source_holds'][0]['id'],'weak')
