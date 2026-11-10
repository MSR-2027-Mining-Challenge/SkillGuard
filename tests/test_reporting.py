"""Validation tests for src/gitskills_reports.

Run from the repository root:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

* PilotRunTests rebuild the reports of the 30-skill systematic sample (scan 173516 and reanalysis 195654) into a
  temporary folder and check every headline number against an independent recount from the raw Cisco JSON files.
  They are skipped when the git-ignored run folders are not on this machine.
* SafetyTests build a synthetic run whose skill content is hostile (HTML/script injection, secrets, absolute paths)
  and whose configurations include LLM, Meta-Analyzer and an unknown future analyzer mode.

Nothing is written outside temporary folders, and source files are hashed before and after to prove they are untouched.
"""

import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gitskills_reports import build_report, load_run  # noqa: E402
from gitskills_reports.build import md  # noqa: E402
from gitskills_reports.redaction import HOME, audit_tree, redact  # noqa: E402

RUNS = ROOT / "results" / "cisco_dataset_runs" / "agent_skills_sample" / "runs"
SCAN = RUNS / "2026-11-03_173516_sample30-seed2027"
REANALYSIS = RUNS / "2026-11-03_195654_sample30-seed2027-reanalysis"
REVIEW = ROOT / "results" / "manual_review" / "sample30-seed2027"


def tree_hashes(*folders):
    out = {}
    for folder in folders:
        for p in sorted(Path(folder).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def text_of(folder):
    return {p: p.read_text(encoding="utf-8") for p in Path(folder).rglob("*") if p.suffix in (".md", ".csv", ".json", ".html")}


def embedded_data(html):
    match = re.search(r'<script type="application/json" id="report-data">(.*?)</script>', html, re.S)
    return json.loads(match.group(1))


@unittest.skipUnless(SCAN.is_dir() and REANALYSIS.is_dir(), "30-skill pilot run folders are not on this machine")
class PilotRunTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="reports-test-"))
        cls.before = tree_hashes(SCAN, REANALYSIS, REVIEW)
        cls.reports = {}
        for folder in (SCAN, REANALYSIS):
            cls.reports[folder.name] = build_report(load_run(folder), ROOT, cls.tmp)
        cls.after = tree_hashes(SCAN, REANALYSIS, REVIEW)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def manifest(self, name):
        return json.loads((self.reports[name] / "report_manifest.json").read_text(encoding="utf-8"))

    # -- source data is never modified
    def test_sources_untouched(self):
        self.assertEqual(self.before, self.after)

    # -- headline numbers, recounted independently from the raw Cisco reports
    def test_counts_match_independent_recount(self):
        reports = [p for p in SCAN.glob("*/reports/*.json") if not p.name.endswith(".run.json")]
        raw_findings = sum(len(json.loads(p.read_text())["findings"]) for p in reports)
        for name in self.reports:
            c = self.manifest(name)["counts"]
            with self.subTest(run=name):
                self.assertEqual(c["skills_selected"], 30)
                self.assertEqual(c["skills_exported"], 30)
                self.assertEqual(c["skills_scanned"], 30)
                self.assertEqual(c["scans_planned"], 120)
                self.assertEqual(c["scans_executed"], len(reports))          # 114 report files on disk
                self.assertEqual(c["scans_by_outcome"], {"complete": 110, "contract_only": 0, "partial": 4, "failed": 0,
                                                         "excluded_incomplete_folder": 6, "missing": 0})
                self.assertEqual(c["skills_by_coverage"], {"complete": 26, "complete_except_excluded": 3, "partially_complete": 0,
                                                           "no_complete_scan": 1, "not_scanned": 0})
                self.assertEqual(c["finding_rows"], raw_findings)              # 141
                self.assertEqual(c["finding_rows_by_kind"], {"metadata_quality": 114, "security": 23, "scan_coverage": 4})
                self.assertEqual(c["skills_with_security_alert_primary"], 4)
                self.assertEqual(c["security_rows_primary"], 23)
                self.assertEqual(c["security_locations_primary"], 11)

    def test_raw_index_hashes_verify(self):
        for name, report in self.reports.items():
            raw = pd.read_csv(report / "03_RAW_SCANNER_OUTPUT" / "raw_report_index.csv")
            with self.subTest(run=name):
                self.assertEqual(len(raw), 120)
                self.assertEqual(int(raw["report_exists"].sum()), 114)
                present = raw[raw["report_exists"]]
                self.assertTrue(present["sha256_matches_record"].all())
                missing = raw[~raw["report_exists"]]
                self.assertEqual(set(missing["status"]), {"SKIPPED_INCOMPLETE_FOLDER"})
                for row in present.head(5).itertuples():        # spot-check: index hash == file on disk
                    self.assertEqual(row.report_sha256, hashlib.sha256((ROOT / row.report_file).read_bytes()).hexdigest())

    def test_validation_tiers(self):
        for name, report in self.reports.items():
            m = self.manifest(name)
            with self.subTest(run=name):
                self.assertEqual(m["validation"]["review_items"], 11)
                self.assertEqual(m["validation"]["locations_by_tier"],
                                 {"human_validated": 0, "provisional": 11, "awaiting_review": 0, "not_in_review": 0})
                self.assertEqual(m["validation"]["provisional_labels"], {"intentional": 5, "scanner_parser_issue": 4, "uncertain": 2})
                key = pd.read_csv(report / "01_IMPORTANT_RESULTS" / "key_security_findings.csv")
                self.assertEqual(len(key), 11)
                self.assertEqual(key["review_id"].nunique(), 11)
        self.assertIn("generated from this run", self.manifest(SCAN.name)["review_match"])
        self.assertIn("byte-identical", self.manifest(REANALYSIS.name)["review_match"])

    def test_start_here_and_dashboard_agree(self):
        for name, report in self.reports.items():
            start = (report / "01_IMPORTANT_RESULTS" / "START_HERE.md").read_text(encoding="utf-8")
            html = (report / "01_IMPORTANT_RESULTS" / "dashboard.html").read_text(encoding="utf-8")
            data = embedded_data(html)
            with self.subTest(run=name):
                self.assertIn("**120 planned**", start)
                self.assertIn("**114 executed**", start)
                self.assertIn("**4 of 30 scanned skills**", start)
                self.assertIn("Human-validated so far: **0** of 11", start)
                self.assertEqual(len(data["locations"]), 11)
                self.assertEqual(len(data["rows"]), 141)
                self.assertEqual(len(data["skills"]), 30)
                self.assertIn("0 of 11</b>", html)

    def test_outputs_safe_and_portable(self):
        for name, report in self.reports.items():
            with self.subTest(run=name):
                self.assertEqual(audit_tree(report, ROOT), [])
                m = self.manifest(name)
                for entry in m["inputs"].values():
                    self.assertFalse(entry["path"].startswith("/"), entry["path"])
                for out in m["outputs"]:
                    path = report / out["path"]
                    self.assertEqual(out["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), out["path"])

    def test_links_in_reports_resolve(self):
        for name, report in self.reports.items():
            for page in report.rglob("*.md"):
                for target in re.findall(r"\]\(([^)#]+)\)", page.read_text(encoding="utf-8")):
                    with self.subTest(page=page.name, target=target):
                        self.assertTrue((page.parent / target.replace("%20", " ")).exists())
            html = (report / "01_IMPORTANT_RESULTS" / "dashboard.html").read_text(encoding="utf-8")
            for target in re.findall(r"href='([^'#]+)'", html):
                with self.subTest(dashboard=name, target=target):
                    self.assertTrue((report / "01_IMPORTANT_RESULTS" / target).exists())

    def test_rebuild_replaces_only_generated_folder(self):
        target = self.reports[SCAN.name]
        build_report(load_run(SCAN), ROOT, self.tmp)               # second build of the same report is allowed
        self.assertTrue((target / "report_manifest.json").is_file())
        other = self.tmp / "foreign"
        foreign = other / "agent_skills_sample" / REANALYSIS.name
        foreign.mkdir(parents=True)
        (foreign / "notes.md").write_text("hand-written", encoding="utf-8")     # a folder this generator did not write
        with self.assertRaises(FileExistsError):
            build_report(load_run(REANALYSIS), ROOT, other)
        self.assertEqual((foreign / "notes.md").read_text(encoding="utf-8"), "hand-written")
        self.assertEqual(self.before, tree_hashes(SCAN, REANALYSIS, REVIEW))


SECRETS = ["sk-ant-api03-SUPERSECRETVALUE1234567890", "AKIAIOSFODNN7EXAMPLE", "ghp_abcdefghijklmnopqrstuvwxyz0123456789",
           "hunter2hunter2", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"]
HOSTILE = ("</script><img src=x onerror=alert(1)> <!-- [click](javascript:alert(1)) | `rm -rf` "
           f"api_key = \"{SECRETS[0]}\" AWS {SECRETS[1]} token={SECRETS[2]} password: '{SECRETS[3]}' Bearer {SECRETS[4]} "
           "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA\n-----END RSA PRIVATE KEY-----")
CONFIGS = [("SKILL.md only | default", "SKILL.md only", "default", "skill_only_default.json"),
           ("SKILL.md only | llm", "SKILL.md only", "llm", "skill_only_llm.json"),
           ("Full folder | meta", "Full folder", "meta", "full_folder_meta.json"),
           ("Full folder | future", "Full folder", "future_mode", "full_folder_future.json")]


class SafetyTests(unittest.TestCase):
    """A synthetic repository with one hostile skill, scanned in four configurations (two never executed)."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix="reports-synthetic-")).resolve()
        (cls.root / "notebooks").mkdir()
        run = cls.root / "results" / "cisco_dataset_runs" / "synthdb" / "runs" / "2026-01-01_000000_hostile"
        skill = run / "evil-skill-000000000000"
        (skill / "reports").mkdir(parents=True)
        (skill / "manifest.json").write_text(json.dumps({"files": [{"path": "SKILL.md"}]}))
        statuses = ["COMPLETE", "COMPLETE", "PARTIAL", "MISSING_REPORT"]
        for (cfg, scope, mode, report), status in zip(CONFIGS, statuses):
            if status != "MISSING_REPORT":
                (skill / "reports" / report).write_text(json.dumps({"findings": [{}]}))
                (skill / "reports" / report.replace(".json", ".run.json")).write_text(json.dumps(
                    {"exit_code": 0, "stderr_tail": f"warning in {cls.root}/x and {HOME}/y", "command": [str(cls.root)]}))
        absolute = f"{cls.root}/results/cisco_dataset_runs/synthdb/runs/x/SKILL.md"
        scans = pd.DataFrame([{"skill_id": skill.name, "repo": "evil/repo", "skill_path": "SKILL.md", "sample_stratum": "scripts",
                               "configuration": c, "scope": s, "analyzer_mode": m, "status": st, "outcome": "", "folder_complete": True,
                               "findings_count": 1, "max_severity": "CRITICAL", "status_detail": HOSTILE, "report_sha256": None,
                               "report_file": r} for (c, s, m, r), st in zip(CONFIGS, statuses)])
        findings = pd.DataFrame([{"skill_id": skill.name, "repo": "evil/repo", "skill_path": "SKILL.md", "configuration": c,
                                  "scope": s, "analyzer_mode": m, "run_status": st, "finding_id": f"F_{i}", "rule_id": "<b>RULE</b>",
                                  "cisco_category": "command_injection", "severity": "critical", "analyzer": f"{m}_analyzer",
                                  "title": HOSTILE, "description": HOSTILE, "file_path": absolute, "reported_line_number": 3.0,
                                  "location_key": "RULE|SKILL.md|3", "snippet": HOSTILE, "evidence_status": "exact",
                                  "finding_kind": "security", "metadata_json": json.dumps({"matched_text": HOSTILE})}
                                 for i, ((c, s, m, r), st) in enumerate(zip(CONFIGS, statuses)) if st != "MISSING_REPORT"])
        scans.to_csv(run / "scan_summary.csv", index=False)
        findings.to_csv(run / "individual_findings.csv", index=False)
        (run / "results_summary.md").write_text(f"# Summary\n\n{HOSTILE}\n\nRun folder: {run}\n")
        (run / "run_metadata.json").write_text(json.dumps({
            "run_id": run.name, "run_mode": "scan", "database": {"tag": "synthdb", "path": str(cls.root / "data/x.db")},
            "scanner": {"installed_version": "skill-scanner 2.3.1",
                        "configurations": [{"configuration": c, "scope": s, "analyzer_mode": m, "report_file": r} for c, s, m, r in CONFIGS]},
            "settings": {"LLM_API_KEY": SECRETS[0]}, "skills": [{"skill_id": skill.name, "folder_complete": True}]}))
        cls.run_dir = run
        cls.before = tree_hashes(run)
        cls.report = build_report(load_run(run), cls.root, cls.root / "results" / "reports")
        cls.texts = text_of(cls.report)
        cls.html = (cls.report / "01_IMPORTANT_RESULTS" / "dashboard.html").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def test_no_secret_reaches_any_output(self):
        for path, text in self.texts.items():
            for secret in SECRETS:
                self.assertNotIn(secret, text, f"{secret[:12]}... leaked into {path.name}")
            self.assertNotIn("MIIEpAIBAAKCAQEA", text, path.name)
        self.assertTrue(any("[REDACTED]" in t for t in self.texts.values()))

    def test_no_absolute_paths(self):
        for path, text in self.texts.items():
            self.assertNotIn(str(self.root), text, path.name)
            self.assertNotIn(HOME, text, path.name)
        self.assertEqual(audit_tree(self.report, self.root), [])

    def test_html_is_inert(self):
        html = self.html
        self.assertNotIn("<img", html)
        self.assertNotIn("<b>RULE", html)
        self.assertEqual(html.count("<script"), 2)                  # the JSON data block and the page's own script
        self.assertEqual(len(re.findall(r"</script>", html)), 2)
        self.assertNotIn("innerHTML", html)
        csp = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', html).group(1)
        self.assertIn("default-src &#x27;none&#x27;", csp)
        script = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
        import base64
        digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
        self.assertIn(f"sha256-{digest}", csp)                     # only this exact script may run
        data = embedded_data(html)                                 # the hostile text survives as data, not markup
        self.assertIn("onerror", data["locations"][0]["snippet"])

    def test_markdown_is_inert(self):
        start = self.texts[self.report / "01_IMPORTANT_RESULTS" / "START_HERE.md"]
        self.assertNotIn("<b>RULE</b>", start)
        self.assertIn("\\<b\\>RULE\\</b\\>", start)
        page = next((self.report / "02_DETAILED_ANALYSIS" / "skills").glob("*.md")).read_text()
        outside_fences = re.sub(r"(`{3,})text\n.*?\n\1", "", page, flags=re.S)
        self.assertIsNone(re.search(r"(?<!\\)<(img|script|/script|!--)", outside_fences))   # every < outside fences is escaped
        self.assertIn("\\[click\\](javascript", outside_fences)  # ... and no live link
        self.assertEqual(md("a|b<c>[d](e)`f`"), "a\\|b\\<c\\>\\[d\\](e)\\`f\\`")

    def test_llm_meta_and_unknown_modes(self):
        coverage = pd.read_csv(self.report / "01_IMPORTANT_RESULTS" / "coverage_summary.csv")
        self.assertEqual(list(coverage["configuration"][:4]), [c[0] for c in CONFIGS])
        self.assertEqual(int(coverage.loc[coverage["configuration"] == "Full folder | future", "missing"].iloc[0]), 1)
        configs = pd.read_csv(self.report / "02_DETAILED_ANALYSIS" / "configurations.csv")
        about = dict(zip(configs["analyzer_mode"], configs["about"]))
        self.assertIn("LLM Analyzer", about["llm"])
        self.assertIn("Meta-Analyzer", about["meta"])
        self.assertIn("no description yet", about["future_mode"])
        start = self.texts[self.report / "01_IMPORTANT_RESULTS" / "START_HERE.md"]
        self.assertIn("`llm` are not deterministic", start)
        self.assertIn("`meta` are not deterministic", start)
        self.assertIn("Configured but never executed: `Full folder | future`", start)
        analyzers = pd.read_csv(self.report / "02_DETAILED_ANALYSIS" / "analyzer_breakdown.csv")
        self.assertIn("llm_analyzer", set(analyzers["analyzer"]))   # complete LLM scan counted; partial meta scan is not primary

    def test_source_untouched(self):
        self.assertEqual(self.before, tree_hashes(self.run_dir))

    def test_redact_unit(self):
        self.assertEqual(redact('password = "abc12345"'), 'password = "[REDACTED]"')
        self.assertEqual(redact("https://user:pw@host/x"), "https://user:[REDACTED]@host/x")
        self.assertEqual(redact("export API_KEY=$API_KEY"), "export API_KEY=$API_KEY")   # variable reference kept


if __name__ == "__main__":
    unittest.main()
