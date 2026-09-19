import copy
import importlib.util
from pathlib import Path
import unittest
import json
import subprocess
import sys
import tempfile
from unittest.mock import patch

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


class GeneratedReviewTests(unittest.TestCase):
    """Exercise real Git history and generation, not a mocked receipt comparison."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in ('public/norway', 'public/content', 'scripts', 'docs/editorial'):
            (self.root / directory).mkdir(parents=True)
        self.target = self.root / 'public/norway/index.html'
        self.target.write_text('<p>Tracked source before generation.</p>')
        (self.root / 'public/content/articles.json').write_text('{"title":"Baseline title"}')
        self.generator = self.root / 'scripts/build_discovery.py'
        self.generator.write_text(
            'import json\nfrom pathlib import Path\n'
            'root = Path(__file__).resolve().parents[1]\n'
            'title = json.loads((root / "public/content/articles.json").read_text())["title"]\n'
            '(root / "public/norway/index.html").write_text("<p>Generated: " + title + "</p>")\n'
        )
        (self.root / m.RECEIPTS).write_text('{}')
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Test fixture')
        self.git('add', '.')
        self.git('commit', '-qm', 'Frozen synthetic baseline')
        baseline = self.git('rev-parse', 'HEAD').strip()
        self.baseline_patch = patch.object(m, 'BASELINE', baseline)
        self.baseline_patch.start()
        self.addCleanup(self.baseline_patch.stop)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def build(self):
        subprocess.run([sys.executable, str(self.generator)], cwd=self.root,
                       check=True, capture_output=True)

    def receipt(self, data):
        row = {k: 'fixture:evidence' for k in (
            'case_id', 'reviewer', 'execution_context', 'reviewed_at',
            'comparison_ref', 'reader_journey_ref', 'semantic_control_ref')}
        row.update(sha256=m.digest(data),
                   loaded_modules=[dict(source='fixture', revision='fixture', application_ref='fixture')],
                   stages={s: 'fixture:evidence' for s in m.STAGES}, decision='KEEP',
                   ariadne_style_readiness='pass_complete', source_status='READY_FOR_EDITORIAL_REVIEW',
                   publication_approval=dict(approved=True, by='Bjørn', reference='fixture-only',
                                             sha256=m.digest(data)))
        (self.root / m.RECEIPTS).write_text(json.dumps({'public/norway/index.html': row}))

    def test_unchanged_generated_baseline_is_exempt(self):
        self.build()
        self.assertEqual(m.check(self.root), [])

    def test_generator_only_reader_text_change_requires_review(self):
        self.generator.write_text(self.generator.read_text().replace('Generated:', 'Changed claim:'))
        self.build()
        self.assertTrue(any('public/norway/index.html: missing receipt' in e for e in m.check(self.root)))

    def test_json_only_generated_reader_text_change_requires_review(self):
        (self.root / 'public/content/articles.json').write_text('{"title":"Changed conclusion"}')
        self.build()
        self.assertTrue(any('public/norway/index.html: missing receipt' in e for e in m.check(self.root)))

    def test_prebuild_receipt_rejected_after_generation(self):
        self.receipt(self.target.read_bytes())
        self.build()
        self.assertTrue(any('another content version' in e for e in m.check(self.root)))

    def test_changed_final_bytes_accept_matching_receipt(self):
        (self.root / 'public/content/articles.json').write_text('{"title":"Changed conclusion"}')
        self.build()
        self.receipt(self.target.read_bytes())
        self.assertEqual(m.check(self.root), [])
