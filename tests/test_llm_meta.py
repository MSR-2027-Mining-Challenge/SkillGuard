"""Validation tests for src/gitskills_cisco_llm (the Cisco LLM Analyzer / Meta-Analyzer experiment).

Run from the repository root:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

* NotebookParityTests execute the classification cells of notebooks/01_cisco_scanner_dataset_ready.ipynb and check that
  gitskills_cisco_llm.rules is the same code: same constants, and identical rows when both flatten every saved baseline
  report of the 30-skill sample.
* RunnerTests drive the runner with a fake `skill-scanner` (no Cisco, no LLM, no network) and check checkpointing,
  resume without duplicate (paid) calls, bounded retries of transient LLM errors, budget stop, fingerprint protection,
  exclusions with denominators, and that the source run is never modified.
* LiveRunTests check the real LLM/Meta run (when it exists on this machine): the reused baseline findings reproduce the
  baseline individual_findings.csv exactly.
"""

import csv
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gitskills_cisco_llm import rules  # noqa: E402
from gitskills_cisco_llm.analyze import analyze, load_tables  # noqa: E402
from gitskills_cisco_llm.experiment import BASELINE_CONFIGS, Experiment, LLMSettings  # noqa: E402
from gitskills_cisco_llm.runner import Runner, prepare  # noqa: E402

NOTEBOOK = ROOT / "notebooks" / "01_cisco_scanner_dataset_ready.ipynb"
RUNS = ROOT / "results" / "cisco_dataset_runs" / "agent_skills_sample" / "runs"
SCAN = RUNS / "2026-11-03_173516_sample30-seed2027"
LIVE = sorted(RUNS.glob("*_sample30-seed2027-llm-meta-*"))


def tree_hashes(folder):
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(folder).rglob("*")) if p.is_file()}


def notebook_namespace():
    """Execute notebook 01's status (Section 8) and classification (Section 9) definitions, without running scans."""
    import hashlib as _h, re as _re, tempfile as _t
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    sources = ["".join(c["source"]) for c in cells if c["cell_type"] == "code"]
    wanted = [s for s in sources if "def assess_report" in s or "def classify_finding_kind" in s
              or "def verify_evidence" in s or "def flatten_findings" in s]
    ns = {"json": json, "re": _re, "hashlib": _h, "tempfile": _t, "Path": Path, "pd": pd}
    for src in wanted:
        if "def flatten_findings" in src:
            src = src.split("finding_rows = []")[0]           # keep the definitions, skip the run-specific loop
        exec(src, ns)
    return ns


@unittest.skipUnless(NOTEBOOK.is_file(), "notebook 01 not found")
class NotebookParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb = notebook_namespace()

    def test_constants_match_notebook(self):
        for name in ("METADATA_QUALITY_RULES", "SCAN_COVERAGE_RULES", "RESEARCH_CATEGORIES", "RESEARCH_CATEGORY_BY_CISCO_CATEGORY",
                     "RESEARCH_CATEGORY_BY_RULE_PREFIX", "STATUS_OUTCOME", "KNOWN_CONTRACT_CODES", "METADATA_FIELDS_TO_KEEP",
                     "FINDING_COLUMNS", "NOT_EXECUTED_STATUSES"):
            self.assertEqual(getattr(rules, name), self.nb[name], name)
        self.assertEqual([(p.pattern, r) for p, r in rules.SECRET_PATTERNS], [(p.pattern, r) for p, r in self.nb["SECRET_PATTERNS"]])

    @unittest.skipUnless(SCAN.is_dir(), "30-skill baseline run not on this machine")
    def test_flatten_and_assess_identical_on_every_baseline_report(self):
        compared = 0
        for skill_dir in sorted(p for p in SCAN.iterdir() if (p / "manifest.json").is_file()):
            for cfg in BASELINE_CONFIGS:
                report_path = skill_dir / "reports" / cfg["report_file"]
                if not report_path.is_file():
                    continue
                report = json.loads(report_path.read_text(encoding="utf-8"))
                self.assertEqual(rules.assess_report(report, cfg, 0), self.nb["assess_report"](report, cfg, 0))
                run = {"skill_id": skill_dir.name, "repo": "r", "skill_path": "p", "sample_stratum": "s", "status": "COMPLETE",
                       "outcome": "complete", **{k: cfg[k] for k in ("configuration", "scope", "analyzer_mode")}}
                folder = skill_dir / ("only" if cfg["scope"] == "SKILL.md only" else "full")
                ours = [{k: r[k] for k in rules.FINDING_COLUMNS} for r in rules.flatten_findings(report, run, folder)]
                self.assertEqual(ours, self.nb["flatten_findings"](report, run, folder))
                compared += 1
        self.assertEqual(compared, 114)


# ---------------------------------------------------------------- fake scanner

FAKE_SCANNER = r'''#!{python}
import json, os, sys, pathlib
args = sys.argv[1:]
if args == ["--version"]:
    print("skill-scanner 2.3.1"); sys.exit(0)
log = pathlib.Path(os.environ["FAKE_CALL_LOG"])
key = " ".join(a for a in args if a.startswith("--use") or a == "--enable-meta") + " " + pathlib.Path(args[1]).parent.name + "/" + pathlib.Path(args[1]).name
calls = log.read_text().splitlines() if log.exists() else []
log.write_text("\n".join(calls + [key]) + "\n")
nth = sum(1 for c in calls if c == key) + 1
findings = [{{"id": "lic", "rule_id": "MANIFEST_MISSING_LICENSE", "category": "policy_violation", "severity": "INFO",
             "title": "t", "description": "d", "file_path": "SKILL.md", "line_number": None, "snippet": None,
             "analyzer": "static", "metadata": {{}}}}]
used = ["static_analyzer", "bytecode", "pipeline", "correlation"]
if "--use-behavioral" in args: used.append("behavioral_analyzer")
usage = None
if "--use-llm" in args:
    used.append("llm_analyzer"); usage = {{"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100}}
    if os.environ.get("FAKE_FAIL_FIRST") and nth == 1:
        findings.append({{"id": "f", "rule_id": "LLM_ANALYSIS_FAILED", "category": "policy_violation", "severity": "INFO",
                         "title": "LLM analysis failed", "description": "x", "file_path": None, "line_number": None,
                         "snippet": None, "analyzer": "llm",
                         "metadata": {{"error": "RateLimitError: 429 Too Many Requests", "error_type": "RateLimitError"}}}})
    else:
        findings.append({{"id": "l1", "rule_id": "LLM_COMMAND_INJECTION", "category": "command_injection", "severity": "HIGH",
                         "title": "llm says", "description": "d", "file_path": "SKILL.md", "line_number": None,
                         "snippet": "curl x | sh", "analyzer": "llm",
                         "metadata": {{"model": "m", "llm_verdict": "TRUE_POSITIVE", "llm_confidence": "MEDIUM"}}}})
sm = {{"policy_name": "default", "policy_preset_base": "balanced", "policy_fingerprint_sha256": "f",
      "rule_contract": {{"status": "passed"}}}}
if "--enable-meta" in args:
    used.append("meta_analyzer")
    sm["meta_risk_assessment"] = {{"risk_level": "LOW", "skill_verdict": "SAFE", "meta_delta": "FALSE_POSITIVE_SUPPRESSED"}}
    for f in findings:
        f["metadata"]["meta_false_positive"] = f["analyzer"] == "llm"
    if usage: usage = {{k: v * 2 for k, v in usage.items()}}
report = {{"skill_name": "s", "skill_path": args[1], "is_safe": True, "max_severity": "HIGH", "findings_count": len(findings),
          "findings": findings, "scan_duration_seconds": 0.1, "analyzers_used": used, "timestamp": "t", "scan_metadata": sm}}
if usage: report["llm_usage"] = usage
out = args[args.index("--output-json") + 1]
pathlib.Path(out).write_text(json.dumps(report))
'''


def make_source(root, n_skills=3, incomplete=("s2",)):
    """A minimal notebook-01 scan run with exported folders and baseline reports."""
    src = root / "results" / "cisco_dataset_runs" / "db" / "runs" / "2026-01-01_000000_src"
    (src / "sample").mkdir(parents=True)
    rows = []
    for i in range(n_skills):
        sid = f"s{i}"
        rows.append({"skill_id": sid, "repo": f"o/r{i}", "skill_path": "SKILL.md", "stratum": "scripts"})
        d = src / sid
        for sub in ("only", "full"):
            (d / sub).mkdir(parents=True)
            (d / sub / "SKILL.md").write_text(f"---\nname: {sid}\n---\nbody {i}\n")
        sha = hashlib.sha256((d / "only" / "SKILL.md").read_bytes()).hexdigest()
        (d / "manifest.json").write_text(json.dumps({"skill_id": sid, "files": [{"path": "SKILL.md", "sha256": sha}],
                                                     "skill_md_sha256": sha, "folder_complete": sid not in incomplete,
                                                     "missing_files": ["x.py"] if sid in incomplete else []}))
        (d / "reports").mkdir()
        for cfg in BASELINE_CONFIGS:
            if cfg["scope"] == "Full folder" and sid in incomplete:
                continue
            rep = {"skill_name": sid, "skill_path": str(d / "only"), "is_safe": True, "max_severity": "INFO", "findings": [],
                   "analyzers_used": cfg["required_analyzers"], "scan_metadata": {}}
            (d / "reports" / cfg["report_file"]).write_text(json.dumps(rep))
            sha_r = hashlib.sha256((d / "reports" / cfg["report_file"]).read_bytes()).hexdigest()
            (d / "reports" / (Path(cfg["report_file"]).stem + ".run.json")).write_text(json.dumps({"exit_code": 0, "report_sha256": sha_r, "wall_seconds": 5}))
    with open(src / "sample" / "sample_manifest.csv", "w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    sha_m = hashlib.sha256((src / "sample" / "sample_manifest.csv").read_bytes()).hexdigest()
    (src / "run_metadata.json").write_text(json.dumps({"run_id": src.name, "run_mode": "scan", "sample": {"manifest_sha256": sha_m},
                                                       "database": {"tag": "db"}}))
    return src


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "notebooks").mkdir()
        bin_dir = self.tmp / ".venv" / "bin"
        bin_dir.mkdir(parents=True)
        scanner = bin_dir / "skill-scanner"
        scanner.write_text(FAKE_SCANNER.format(python=sys.executable))
        scanner.chmod(scanner.stat().st_mode | stat.S_IEXEC)
        self.log = self.tmp / "calls.log"
        self.env = {"FAKE_CALL_LOG": str(self.log), "SKILL_SCANNER_LLM_API_KEY": "test-not-a-real-key"}
        self.old_env = {k: os.environ.get(k) for k in list(self.env) + ["FAKE_FAIL_FIRST"]}
        os.environ.update(self.env)
        self.source = make_source(self.tmp)

    def tearDown(self):
        for k, v in self.old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)

    def experiment(self, **kw):
        llm = LLMSettings(model="claude-sonnet-5-5")
        return Experiment(name="t", modes=["behavioral_llm", "behavioral_meta", "behavioral_llm_meta"], llm=llm,
                          budget_usd=kw.pop("budget_usd", 10.0), backoff_seconds=0, **kw)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_plan_denominators_and_source_untouched(self):
        before = tree_hashes(self.source)
        run = prepare(self.tmp, self.source, self.experiment(), run_id="r", log=lambda *_: None)
        plan = pd.read_csv(run / "plan.csv")
        self.assertEqual(len(plan), 3 * 10)
        self.assertEqual(plan["action"].value_counts().to_dict(), {"scan": 15, "reuse": 10, "exclude": 5})
        self.assertTrue(plan.loc[plan["action"].eq("exclude"), "reason"].str.startswith("SKIPPED_INCOMPLETE_FOLDER").all())
        self.assertEqual(before, tree_hashes(self.source))

    def test_resume_never_repeats_finished_scans(self):
        run = prepare(self.tmp, self.source, self.experiment(), run_id="r", log=lambda *_: None)
        Runner(self.tmp, run, log=lambda *_: None).execute(modes={"behavioral_llm"})
        first = len(self.calls())
        self.assertEqual(first, 5)                               # 3 SKILL.md-only + 2 complete full folders
        Runner(self.tmp, run, log=lambda *_: None).execute()     # resume: only the other modes run
        self.assertEqual(len(self.calls()), 15)
        Runner(self.tmp, run, log=lambda *_: None).execute()     # nothing left: zero calls
        self.assertEqual(len(self.calls()), 15)
        ledger = [json.loads(l) for l in (run / "attempts.jsonl").read_text().splitlines()]
        self.assertEqual(sum(e["event"] == "end" for e in ledger), 15)
        _, _, scans, findings = load_tables(run)
        self.assertEqual(scans["status"].value_counts().to_dict(), {"COMPLETE": 25, "SKIPPED_INCOMPLETE_FOLDER": 5})
        # Meta marked the LLM finding as a false positive: kept (verbose) but not visible after Meta.
        c = findings[findings["analyzer_mode"].eq("behavioral_llm_meta") & findings["analyzer"].eq("llm")]
        self.assertTrue(len(c) and c["meta_false_positive"].eq(True).all() and (~c["post_meta_visible"]).all())

    def test_transient_llm_error_is_retried_once_and_counted(self):
        os.environ["FAKE_FAIL_FIRST"] = "1"
        run = prepare(self.tmp, self.source, self.experiment(), run_id="r", log=lambda *_: None)
        Runner(self.tmp, run, log=lambda *_: None).execute(modes={"behavioral_llm"}, skills={"s0"})
        self.assertEqual(len(self.calls()), 4)                   # 2 scopes x (failed attempt + retry)
        record = json.loads((run / "s0" / "reports" / "skill_only_behavioral_llm.run.json").read_text())
        self.assertEqual(record["status"], "COMPLETE")
        self.assertEqual([a["status"] for a in record["attempts"]], ["PARTIAL", "COMPLETE"])
        self.assertTrue((run / "s0" / "reports" / "attempts" / "skill_only_behavioral_llm.attempt1.json").is_file())
        spent = sum(json.loads(l).get("cost_usd") or 0 for l in (run / "attempts.jsonl").read_text().splitlines())
        self.assertAlmostEqual(spent, 4 * (1000 * 2 + 100 * 10) / 1e6)   # failed attempts are paid and counted

    def test_budget_stops_before_overspending(self):
        run = prepare(self.tmp, self.source, self.experiment(budget_usd=0.007), run_id="r", log=lambda *_: None)
        state = Runner(self.tmp, run, log=lambda *_: None).execute(modes={"behavioral_llm"})
        self.assertEqual(state, "stopped")
        self.assertEqual(len(self.calls()), 2)                   # $0.003 each; a third would exceed $0.007
        status = json.loads((run / "execution_status.json").read_text())
        self.assertIn("budget", status["stop_reason"])

    def test_paid_run_requires_key_and_budget(self):
        run = prepare(self.tmp, self.source, self.experiment(budget_usd=None), run_id="r", log=lambda *_: None)
        with self.assertRaisesRegex(RuntimeError, "budget"):
            Runner(self.tmp, run, log=lambda *_: None).execute()
        self.assertEqual(self.calls(), [])

    def test_changed_settings_refuse_to_mix(self):
        run = prepare(self.tmp, self.source, self.experiment(), run_id="r", log=lambda *_: None)
        spec = json.loads((run / "experiment.json").read_text())
        spec["experiment"]["llm"]["model"] = "claude-opus-5-5"
        (run / "experiment.json").write_text(json.dumps(spec))
        with self.assertRaisesRegex(RuntimeError, "fingerprint"):
            Runner(self.tmp, run, log=lambda *_: None)


@unittest.skipUnless(LIVE and SCAN.is_dir(), "LLM/Meta run not on this machine")
class LiveRunTests(unittest.TestCase):
    def test_reused_baseline_reproduces_baseline_findings(self):
        _, _, scans, findings = load_tables(LIVE[-1])
        tmp = Path(tempfile.mkdtemp()) / "ours.csv"            # same CSV round trip as the saved baseline table
        findings[findings["analyzer_mode"].isin(["default", "behavioral"])].to_csv(tmp, index=False)
        ours = pd.read_csv(tmp)
        ours["reported_line_number"] = ours["reported_line_number"].astype("Int64")
        shutil.rmtree(tmp.parent)
        base = pd.read_csv(SCAN / "individual_findings.csv")
        base["reported_line_number"] = base["reported_line_number"].astype("Int64")
        # reported_file_path / metadata_json hold Cisco's absolute scan path, which names the run folder that was scanned.
        cols = [c for c in rules.FINDING_COLUMNS if c not in ("reported_file_path", "metadata_json")]
        key = ["skill_id", "configuration", "finding_key"]
        a = ours[cols].astype(str).sort_values(key).reset_index(drop=True)
        b = base[cols].astype(str).sort_values(key).reset_index(drop=True)
        self.assertEqual(len(a), len(b))
        a = a.replace({"<NA>": "nan", "None": "nan"})
        b = b.replace({"<NA>": "nan", "None": "nan"})
        pd.testing.assert_frame_equal(a, b)
        base_scans = pd.read_csv(SCAN / "scan_summary.csv")
        reused = scans[scans["analyzer_mode"].isin(["default", "behavioral"])]
        self.assertEqual(sorted(reused["status"].astype(str)), sorted(base_scans["status"].astype(str)))


if __name__ == "__main__":
    unittest.main()
