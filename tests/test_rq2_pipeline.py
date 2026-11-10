"""Synthetic, offline tests for SkillGuard RQ2 reporting and safe P5 evidence."""
from __future__ import annotations
import csv, importlib.util, json, pathlib, tempfile, unittest

HERE=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rq2_pipeline',HERE/'scripts/rq2_pipeline.py')
pipeline=importlib.util.module_from_spec(spec);spec.loader.exec_module(pipeline)
pspec=importlib.util.spec_from_file_location('rq2_p5_probe',HERE/'scripts/rq2_p5_probe.py')
p5=importlib.util.module_from_spec(pspec);pspec.loader.exec_module(p5)

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.tmp.name)
        (self.root/'results').mkdir()
        (self.root/'notebooks').mkdir()
        self.run=self.root/'results/cisco_dataset_runs/agent_skills_sample/runs/test-run'
        self.skill=self.run/'s1'
        (self.skill/'full/scripts').mkdir(parents=True)
        (self.skill/'full/SKILL.md').write_text('---\nname: sample-one\ndescription: Testing.\n---\n',encoding='utf-8')
        script='''#!/usr/bin/env python3
"""Docstring\nmentions deletion here\n"""
# remove comment
import os
os.kill(12345, 15)
'''
        (self.skill/'full/scripts/test.py').write_text(script,encoding='utf-8')
        (self.skill/'manifest.json').write_text(json.dumps({'skill_id':'s1','files':[],'folder_complete':True}),encoding='utf-8')
        self.csv_path=self.root/'results/rq2/seed2027_defect_screening/rq2_defect_candidates.csv'
        rows=[{'candidate_id':'abc123','rule_id':'P4','rule_name':'Side effect',
               'skill_id':'s1','file_path':'scripts/test.py','line_number':'5',
               'candidate_status':'false_positive','investigation_notes':'research note',
               'signal':'Potential write','supporting_excerpt':'# remove comment',
               'impact':'','recommended_fix':'','repo':'test/demo'},
              {'candidate_id':'def456','rule_id':'P4','rule_name':'Side effect',
               'skill_id':'s1','file_path':'scripts/test.py','line_number':'7',
               'candidate_status':'candidate','investigation_notes':'',
               'signal':'Potential signal','supporting_excerpt':'os.kill(12345, 15)',
               'impact':'','recommended_fix':'','repo':'test/demo'}]
        pipeline.write_csv(self.csv_path,rows,list(rows[0]))
        tax=self.root/'docs/rq2/rq2_defect_taxonomy_v0_1.json';tax.parent.mkdir(parents=True)
        tax.write_text('{}',encoding='utf-8')
        self.tax=tax

    def tearDown(self):self.tmp.cleanup()

    def test_build_report_preserves_human_labels(self):
        original=self.csv_path.read_bytes()
        out=self.root/'results/rq2/reports'
        meta=pipeline.report(self.root,self.csv_path,self.run,out,self.tax,{})
        self.assertEqual(meta['candidate_locations'],2)
        self.assertEqual(meta['annotated_candidates'],1)
        self.assertEqual(self.csv_path.read_bytes(),original)
        self.assertTrue((out/'index.html').is_file())
        self.assertTrue((out/'01_IMPORTANT_RESULTS/dashboard.html').is_file())
        self.assertIn('false_positive',(out/'04_HUMAN_VALIDATION/annotation_snapshot.csv').read_text())
        self.assertIn('line context', (out/'02_DETAILED_ANALYSIS/README.md').read_text())

    def test_comment_filter_and_source_evidence(self):
        path=self.skill/'full/scripts/test.py'
        self.assertEqual(pipeline.code_line_type(path,5),'comment')
        self.assertEqual(pipeline.code_line_type(path,7),'code')
        original_rows,_=pipeline.load_candidates(self.csv_path)
        self.assertEqual(pipeline.suggested_review(original_rows[0],path,'comment')[0], 'trace_to_executable_code')
        self.assertEqual(pipeline.suggested_review(original_rows[1],path,'code')[0],'needs_review')

    def test_macos_style_alias_paths(self):
        # Simulate a Mac /var -> /private/var path alias on any platform.
        alias = self.root.parent / (self.root.name + '-alias')
        alias.symlink_to(self.root, target_is_directory=True)
        try:
            rel_csv = self.csv_path.relative_to(self.root)
            rel_run = self.run.relative_to(self.root)
            rel_tax = self.tax.relative_to(self.root)
            out = alias/'results/rq2/alias_report'
            meta = pipeline.report(alias, alias/rel_csv, alias/rel_run, out, alias/rel_tax, {})
            self.assertEqual(meta['candidate_locations'], 2)
            self.assertTrue((out/'index.html').is_file())
            # The source remains accessible, rather than falsely marked outside root.
            rows,_ = pipeline.load_candidates(self.csv_path)
            self.assertIsNotNone(pipeline.source_file(self.root.resolve(), self.run.resolve(), rows[0]))
        finally:
            alias.unlink()

    def test_macos_style_alias_p5(self):
        alias = self.root.parent / (self.root.name + '-alias')
        alias.symlink_to(self.root, target_is_directory=True)
        try:
            path = self.skill/'full/scripts/set_reminder.py'
            path.write_text("""def _to_cron(dt):\n    return f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"\n""", encoding='utf-8')
            result = p5.run(alias, str(path.relative_to(self.root)), 'results/rq2/fix_experiments/alias')
            self.assertEqual(result['original_cron_2027'], result['original_cron_2028'])
        finally:
            alias.unlink()

    def test_actual_path_escape_is_rejected(self):
        outside = self.root.parent / 'outside-rq2-sensitive-file'
        with self.assertRaises(ValueError):
            pipeline.repo_path(self.root, '../outside-rq2-sensitive-file')
        with self.assertRaises(ValueError):
            p5.run(self.root, '../outside-rq2-sensitive-file', 'results/rq2/fix_experiments/test')
        with self.assertRaises(ValueError):
            p5.run(self.root, 'results/rq2/missing.py', '../outside-rq2-output')

    def test_redaction(self):
        self.assertNotIn('samantha',pipeline.redact('/Users/samantha/Downloads/x'))
        self.assertNotIn('1234567890',pipeline.redact('token="1234567890"'))

    def test_p5_year_gate(self):
        from datetime import datetime
        a=datetime(2027,1,1,9);b=datetime(2028,1,1,9)
        self.assertEqual(p5.cron_expression(a),p5.cron_expression(b))
        self.assertFalse(p5.is_target_instant(a,b))
        self.assertTrue(p5.is_target_instant(b,b))

    def test_p5_reads_source_but_does_not_execute(self):
        path=self.skill/'full/scripts/set_reminder.py'
        path.write_text('''from datetime import datetime\ndef _to_cron(dt: datetime) -> str:\n    return f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"\n''',encoding='utf-8')
        result=p5.run(self.root,str(path.relative_to(self.root)),'results/rq2/fix_experiments/test')
        self.assertEqual(result['original_cron_2027'],result['original_cron_2028'])
        self.assertTrue((self.root/'results/rq2/fix_experiments/test/p5_safe_probe.json').is_file())

if __name__ == '__main__':unittest.main()

class SingleResearcherSchemaTests(unittest.TestCase):
    def test_editor_removes_unused_legacy_columns_and_preserves_notes(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as folder:
            csvpath = pathlib.Path(folder)/'candidates.csv'
            old_one = 'reviewer_' + str(1)
            old_two = 'reviewer_' + str(2)
            records = [{
                'candidate_id': 'ab123', 'skill_id': 'sample', 'rule_id': 'P4',
                'file_path': 'scripts/a.py', 'line_number': '2',
                'candidate_status': 'confirmed_in_snapshot',
                'impact': 'Possible file loss', 'recommended_fix': 'Guard cleanup',
                'investigation_notes': 'Manually verified',
                old_one: 'old', old_two: 'unused',
                old_two + '_label': 'unused', 'final_label': 'old'
            }]
            pipeline.write_csv(csvpath, records, list(records[0]))
            command = [sys.executable, str(HERE/'scripts/rq2_edit.py'),
                       '--csv', str(csvpath), '--clean-legacy-columns', '--yes']
            subprocess.run(command, check=True, capture_output=True, text=True)
            with csvpath.open(newline='') as fh:
                rd = csv.DictReader(fh)
                row = next(rd)
                self.assertTrue(set(rd.fieldnames).isdisjoint(
                    {old_one, old_two, old_two + '_label', 'final_label'}))
            self.assertEqual(row['candidate_status'], 'confirmed_in_snapshot')
            self.assertEqual(row['investigation_notes'], 'Manually verified')
            self.assertEqual(row['impact'], 'Possible file loss')
            self.assertTrue(csvpath.with_name(csvpath.name+'.bak').exists())

    def test_notebook_output_schema_is_single_researcher(self):
        nb = json.loads((HERE/'notebooks/06_rq2_defect_detection_automated.ipynb').read_text())
        source = '\n'.join(''.join(c.get('source', [])) for c in nb['cells'])
        self.assertNotIn('reviewer_' + str(2),source)
        self.assertNotIn('reviewer_' + str(1),source)
        self.assertIn('"candidate_status", "impact", "recommended_fix", "investigation_notes"',source)
