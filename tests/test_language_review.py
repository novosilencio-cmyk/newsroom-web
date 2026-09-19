import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('language', Path(__file__).resolve().parents[1] / 'scripts/check_language_review.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = b'<p>A documented observation.</p>'
        self.row = {k: 'evidence:fixture' for k in ('case_id','reviewer','execution_context','reviewed_at','comparison_ref','reader_journey_ref','semantic_control_ref')}
        self.row.update(sha256=m.digest(self.data), loaded_modules=[dict(source='module', revision='abc', application_ref='evidence:application')], stages={s:'evidence:'+s for s in m.STAGES}, decision='KEEP', ariadne_style_readiness='pass_complete', source_status='READY_FOR_EDITORIAL_REVIEW', publication_approval=dict(approved=True, by='Bjørn', reference='fixture-only', sha256=m.digest(self.data)))
    def test_keep_is_valid(self):
        self.assertEqual(m.receipt_errors(self.row,self.data),[])
    def test_material_edit_invalidates_review(self):
        self.assertTrue(m.receipt_errors(self.row,b'<p>Different conclusion.</p>'))
    def test_source_hold_survives_language_pass(self):
        self.row['source_status']='HOLD_SOURCE_GAP'
        self.assertIn('source clearance missing or held',m.receipt_errors(self.row,self.data))
    def test_loading_alone_is_not_execution(self):
        self.row['stages']={}
        self.assertTrue(m.receipt_errors(self.row,self.data))
    def test_publication_approval_separate(self):
        self.row['publication_approval']['approved']=False
        self.assertTrue(m.receipt_errors(self.row,self.data))
    def test_missing_receipt(self):
        self.assertTrue(m.receipt_errors(None,self.data))
    def test_incomplete_module_receipt(self):
        del self.row['loaded_modules'][0]['application_ref']
        self.assertTrue(m.receipt_errors(self.row,self.data))
    def test_residual_risk_cannot_publish(self):
        self.row['ariadne_style_readiness']='residual_risk'
        self.assertTrue(m.receipt_errors(self.row,self.data))
