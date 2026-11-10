"""Prepare and execute an LLM/Meta experiment run folder: checkpointed, resumable, bounded retries, budget-guarded.

Layout (same as notebook 01 runs, so gitskills_reports reads it without changes):
    results/cisco_dataset_runs/<db>/runs/<YYYY-mm-dd_HHMMSS>_<name>/
        experiment.json        what is run (configurations, LLM settings) + fingerprint
        plan.csv               one row per skill x configuration: reuse / scan / exclude (with reason)
        attempts.jsonl         append-only ledger: every scan attempt (start/end), tokens, cost, status
        sample/                copy of the source run's sample manifest (hash-checked)
        <skill_id>/            manifest.json, only/, full/  (copied from the source run, file hashes verified)
            reports/<config>.json + .run.json      one checkpoint per finished scan
            reports/attempts/<config>.attemptN.json  reports of failed attempts that were retried
Baseline reports are copied from the source run and their SHA-256 checked; the source run is never modified.
"""

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from . import rules
from .experiment import (BASELINE_CONFIGS, COMMON_ARGS, Experiment, api_key_present, environment_info, ollama_info,
                         resolved_request_settings, scanner_path, scope_folder)

PLAN_COLUMNS = ["skill_id", "repo", "skill_path", "sample_stratum", "configuration", "scope", "analyzer_mode", "report_file",
                "action", "reason"]
TRANSIENT_ERROR = re.compile(r"rate.?limit|\b429\b|\b5(?:00|02|03|04|29)\b|timed? ?out|timeout|overloaded|connection|"
                             r"ServiceUnavailable|InternalServerError|APIConnectionError|temporarily", re.I)
EXIT_CONFIGURATION_ERROR = 2          # skill_scanner/cli/cli.py


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_atomic(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".tmp_", suffix=path.suffix,
                                     delete=False) as tmp:
        tmp.write(text)
    Path(tmp.name).replace(path)


def write_json(path, value):
    write_atomic(path, json.dumps(value, indent=2, sort_keys=False, default=str) + "\n")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, columns):
    with tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", dir=Path(path).parent, delete=False) as tmp:
        writer = csv.DictWriter(tmp, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    Path(tmp.name).replace(path)


def run_record_path(report_path):
    return report_path.with_name(report_path.stem + ".run.json")


# ---------------------------------------------------------------- prepare

def prepare(root, source_run, experiment, run_id=None, dest_parent=None, log=print):
    """Create a new run folder from a finished notebook-01 run (same sample, same exported skill folders)."""
    root, source_run = Path(root).resolve(), Path(source_run).resolve()
    source_meta = json.loads((source_run / "run_metadata.json").read_text(encoding="utf-8"))
    if source_meta.get("run_mode") != "scan":
        raise ValueError(f"{source_run} is a {source_meta.get('run_mode')} run; use the original scan run as the source "
                         "(it holds the exported skill folders and the reports).")
    run_id = run_id or f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_{experiment.name}"
    run_dir = Path(dest_parent or source_run.parent).resolve() / run_id
    if run_dir.exists():
        raise FileExistsError(f"{run_dir} exists; resume it with `execute` instead of preparing it again.")
    run_dir.mkdir(parents=True)

    sample_src = source_run / "sample" / "sample_manifest.csv"
    expected = (source_meta.get("sample") or {}).get("manifest_sha256")
    if sha256_file(sample_src) != expected:
        raise ValueError("sample_manifest.csv in the source run does not match the SHA-256 recorded in its run_metadata.json")
    shutil.copytree(source_run / "sample", run_dir / "sample")
    sample = read_csv(run_dir / "sample" / "sample_manifest.csv")

    plan, integrity = [], []
    configs = BASELINE_CONFIGS + experiment.configs()
    for row in sample:
        skill_id = row["skill_id"]
        src, dst = source_run / skill_id, run_dir / skill_id
        identity = {"skill_id": skill_id, "repo": row["repo"], "skill_path": row["skill_path"],
                    "sample_stratum": row["stratum"]}
        problem = None
        if not (src / "manifest.json").is_file():
            problem = "skill folder missing in the source run"
        else:
            dst.mkdir()
            shutil.copy2(src / "manifest.json", dst / "manifest.json")
            manifest = json.loads((dst / "manifest.json").read_text(encoding="utf-8"))
            for sub in ("only", "full"):
                if (src / sub).is_dir():
                    shutil.copytree(src / sub, dst / sub)
            bad = [f["path"] for f in manifest.get("files", [])
                   if not (dst / "full" / f["path"]).is_file() or sha256_file(dst / "full" / f["path"]) != f["sha256"]]
            if not (dst / "only" / "SKILL.md").is_file() or sha256_file(dst / "only" / "SKILL.md") != manifest.get("skill_md_sha256"):
                bad.append("only/SKILL.md")
            if bad:
                problem = f"exported files do not match manifest.json hashes: {bad[:5]}"
            integrity.append({"skill_id": skill_id, "files_checked": len(manifest.get("files", [])) + 1, "mismatches": len(bad)})
        for cfg in configs:
            entry = {**identity, **{k: cfg[k] for k in ("configuration", "scope", "analyzer_mode", "report_file")}}
            if problem:
                entry.update(action="exclude", reason=f"EXPORT_ERROR: {problem}")
            elif cfg["scope"] == "Full folder" and not manifest.get("folder_complete"):
                entry.update(action="exclude", reason="SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this "
                                                      f"folder (missing: {len(manifest.get('missing_files') or [])})")
            elif cfg in BASELINE_CONFIGS:
                entry.update(action="reuse", reason=f"baseline report copied from {source_meta['run_id']}")
                _copy_baseline_report(src, dst, cfg)
            else:
                entry.update(action="scan", reason="")
            plan.append(entry)

    write_csv(run_dir / "plan.csv", plan, PLAN_COLUMNS)
    scanner = scanner_path(root)
    env = environment_info(scanner)
    fingerprint, payload = experiment.fingerprint(env["scanner_version"])
    write_json(run_dir / "experiment.json", {"experiment": experiment.to_json(), "fingerprint": fingerprint,
                                             "fingerprint_payload": payload, "prepared_at": now_utc(),
                                             "source_run": {"run_id": source_meta["run_id"],
                                                            "path": source_run.relative_to(root).as_posix()},
                                             "integrity": integrity})
    counts = {a: sum(1 for p in plan if p["action"] == a) for a in ("reuse", "scan", "exclude")}
    log(f"prepared {run_dir}: {len(sample)} skills, {len(configs)} configurations, {counts}")
    return run_dir


def _copy_baseline_report(src, dst, cfg):
    (dst / "reports").mkdir(exist_ok=True)
    report = src / "reports" / cfg["report_file"]
    record = run_record_path(report)
    if not report.is_file():
        return                                                  # analysis records it as MISSING_REPORT
    shutil.copy2(report, dst / "reports" / report.name)
    if record.is_file():
        shutil.copy2(record, dst / "reports" / record.name)
        expected = json.loads(record.read_text(encoding="utf-8")).get("report_sha256")
        if expected and sha256_file(dst / "reports" / report.name) != expected:
            raise ValueError(f"copied baseline report {report} does not match its recorded SHA-256")


# ---------------------------------------------------------------- execute

class Ledger:
    """Append-only JSONL log of every scan attempt. Used for cost accounting and to show interrupted (paid) attempts."""

    def __init__(self, path):
        self.path, self.lock = Path(path), threading.Lock()

    def append(self, **entry):
        with self.lock, open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": now_utc(), **entry}, default=str) + "\n")

    def entries(self):
        if not self.path.is_file():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def spent_usd(self):
        return sum(e.get("cost_usd") or 0 for e in self.entries() if e.get("event") == "end")


def assess_llm_meta(report, cfg, stderr):
    """LLM / Meta-specific status on top of notebook 01's assess_report. Returns (llm, meta, extra_reasons, retryable)."""
    findings = [f for f in report.get("findings") or [] if isinstance(f, dict)]
    used = report.get("analyzers_used") or []
    reasons, retryable = [], False
    llm = {}
    if cfg.get("uses_llm"):
        failed = [f for f in findings if f.get("rule_id") == "LLM_ANALYSIS_FAILED"]
        llm["budget_exceeded_items"] = sum(f.get("rule_id") == "LLM_CONTEXT_BUDGET_EXCEEDED" for f in findings)
        if failed:
            meta = failed[0].get("metadata") or {}
            llm["status"] = "failed"
            llm["error_type"] = meta.get("error_type")
            llm["error"] = rules.redact(str(meta.get("error") or failed[0].get("description")))[:500]
            retryable = bool(TRANSIENT_ERROR.search(f"{llm['error_type']} {llm['error']}"))
        elif any(f.get("rule_id") == "LLM_PROMPT_INJECTION_DETECTED" for f in findings):
            llm["status"] = "not_queried_delimiter_injection"
        else:
            llm["status"] = "ok"
        llm["findings"] = sum(f.get("analyzer") == "llm" and f.get("rule_id") not in
                              ("LLM_ANALYSIS_FAILED", "LLM_CONTEXT_BUDGET_EXCEEDED") for f in findings)
    meta = {}
    if cfg.get("uses_meta"):
        pre_meta = [f for f in findings if f.get("analyzer") != "meta"]
        assessment = (report.get("scan_metadata") or {}).get("meta_risk_assessment") or {}
        if "meta_analyzer" in used:
            state = assessment.get("meta_analysis_status")
            meta["status"] = {"skipped_clear_deterministic": "skipped_clear_deterministic", "degraded": "degraded"}.get(state, "ran")
            if state == "degraded":
                reasons.append(f"Meta-Analyzer degraded: {assessment.get('meta_analysis_warnings')}")
        elif not pre_meta:
            meta["status"] = "not_invoked_no_findings"
        else:
            meta["status"] = "failed"
            line = next((l for l in stderr.splitlines() if "Meta-analysis failed" in l), "")
            meta["error"] = rules.redact(line)[:500] or "meta_analyzer missing from analyzers_used (no warning captured)"
            reasons.append(f"Meta-Analyzer did not complete: {meta['error']}")
            retryable = retryable or bool(TRANSIENT_ERROR.search(line))
        meta["false_positives"] = sum((f.get("metadata") or {}).get("meta_false_positive") is True for f in findings)
        meta["missed_threats_added"] = sum(f.get("analyzer") == "meta" for f in findings)
        meta["risk_level"] = assessment.get("risk_level")
        meta["skill_verdict"] = assessment.get("skill_verdict")
        meta["meta_delta"] = assessment.get("meta_delta")
    return llm, meta, reasons, retryable


class Runner:
    def __init__(self, root, run_dir, log=print, retry_failed=False):
        self.root, self.run_dir, self.log = Path(root).resolve(), Path(run_dir).resolve(), log
        spec = json.loads((self.run_dir / "experiment.json").read_text(encoding="utf-8"))
        self.spec, self.experiment = spec, Experiment.from_json(spec["experiment"])
        self.configs = {c["configuration"]: c for c in self.experiment.configs()}
        self.plan = read_csv(self.run_dir / "plan.csv")
        self.scanner = scanner_path(self.root)
        self.env_info = environment_info(self.scanner)
        fingerprint, _ = self.experiment.fingerprint(self.env_info["scanner_version"])
        if fingerprint != spec["fingerprint"]:
            raise RuntimeError("The installed scanner or the experiment settings differ from experiment.json "
                               f"(fingerprint {fingerprint[:12]} vs {spec['fingerprint'][:12]}). Start a new run instead "
                               "of mixing results.")
        self.fingerprint = fingerprint
        self.ledger = Ledger(self.run_dir / "attempts.jsonl")
        self.retry_failed = retry_failed
        self.stop = threading.Event()
        self.stop_reason = None

    # -- bookkeeping
    def report_path(self, row):
        return self.run_dir / row["skill_id"] / "reports" / row["report_file"]

    def is_done(self, row):
        record_path = run_record_path(self.report_path(row))
        if not record_path.is_file():
            return False
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if record.get("fingerprint") != self.fingerprint:
            raise RuntimeError(f"{record_path} was produced with another experiment fingerprint")
        if self.retry_failed and record.get("status") not in ("COMPLETE", "CONTRACT_ONLY"):
            return False
        report = self.report_path(row)
        return record.get("final") is True and (not report.is_file() or sha256_file(report) == record.get("report_sha256"))

    def pending(self, modes=None, skills=None):
        rows = [r for r in self.plan if r["action"] == "scan"]
        if modes:
            rows = [r for r in rows if r["analyzer_mode"] in modes]
        if skills:
            rows = [r for r in rows if r["skill_id"] in skills]
        # All B scans first, then C-det, then C, so an interrupted run still has complete comparisons for the early modes.
        modes_order = self.experiment.modes
        rows = sorted(rows, key=lambda r: (modes_order.index(r["analyzer_mode"]), r["skill_id"], r["scope"]))
        return [r for r in rows if not self.is_done(r)]

    def check_ready(self):
        llm = self.experiment.llm
        if llm.is_local:
            info = ollama_info(llm.model)
            if "error" in info or not info.get("digest"):
                raise RuntimeError(f"Local Ollama model {llm.model} is not available: {info}")
            return {"ollama": info}
        if not api_key_present():
            raise RuntimeError("SKILL_SCANNER_LLM_API_KEY is not set; no paid LLM scan was started.")
        if self.experiment.budget_usd is None:
            raise RuntimeError("Paid provider without an approved budget: set budget_usd in the experiment.")
        if llm.prices()[0] is None:
            raise RuntimeError(f"No price known for {llm.model}; pass price_in_per_mtok/price_out_per_mtok.")
        return {}

    def _over_budget(self, mode):
        budget = self.experiment.budget_usd
        if budget is None or self.experiment.llm.is_local:
            return False
        ends = [e for e in self.ledger.entries() if e.get("event") == "end"]
        spent = sum(e.get("cost_usd") or 0 for e in ends)
        same = [e.get("cost_usd") or 0 for e in ends if e.get("analyzer_mode") == mode]
        next_cost = max(same) if same else 0.0
        return spent + next_cost > budget

    # -- one scan, with bounded retries
    def run_one(self, row):
        cfg = self.configs[row["configuration"]]
        folder = self.run_dir / row["skill_id"] / scope_folder(row["scope"])
        report_path = self.report_path(row)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        llm = self.experiment.llm
        env = {**os.environ, **llm.env()} if (cfg["uses_llm"] or cfg["uses_meta"]) else dict(os.environ)
        attempts = []
        for attempt in range(1, self.experiment.max_attempts + 1):
            if self.stop.is_set():
                return None
            if self._over_budget(row["analyzer_mode"]):
                self.stop_reason = f"budget of ${self.experiment.budget_usd} would be exceeded"
                self.stop.set()
                return None
            with tempfile.TemporaryDirectory(dir=report_path.parent) as tmp:
                out = Path(tmp) / "report.json"
                cmd = [self.scanner, "scan", str(folder), *COMMON_ARGS, *cfg["extra_args"],
                       *(llm.cli_args() if cfg["uses_llm"] or cfg["uses_meta"] else []), "--output-json", str(out)]
                started, t0 = now_utc(), time.monotonic()
                self.ledger.append(event="start", skill_id=row["skill_id"], configuration=row["configuration"],
                                   analyzer_mode=row["analyzer_mode"], attempt=attempt)
                try:
                    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=self.experiment.timeout_seconds)
                    exit_code, stderr = proc.returncode, proc.stderr or ""
                except subprocess.TimeoutExpired as exc:
                    exit_code, stderr = None, f"TIMEOUT after {self.experiment.timeout_seconds}s\n{exc.stderr or ''}"
                wall = round(time.monotonic() - t0, 2)
                report, status, reasons, failures = None, None, [], []
                if out.is_file():
                    try:
                        report = json.loads(out.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as exc:
                        status, reasons = "FAILED_INVALID_JSON", [str(exc)]
                if report is not None:
                    status, reasons, failures = rules.assess_report(report, cfg, exit_code)
                    llm_info, meta_info, extra, retryable = assess_llm_meta(report, cfg, stderr)
                    if extra and status in ("COMPLETE", "CONTRACT_ONLY"):
                        status = "PARTIAL"
                    reasons += extra
                    usage = report.get("llm_usage") or {}
                else:
                    status = status or ("FAILED_TIMEOUT" if exit_code is None else
                                        "FAILED_CONFIGURATION" if exit_code == EXIT_CONFIGURATION_ERROR else "FAILED_NO_REPORT")
                    reasons = reasons or [rules.redact(stderr.strip().splitlines()[-1] if stderr.strip() else "no output")]
                    llm_info, meta_info, usage = {}, {}, {}
                    retryable = status in ("FAILED_TIMEOUT", "FAILED_NO_REPORT") or bool(TRANSIENT_ERROR.search(stderr))
                cost = llm.cost_usd(usage.get("input_tokens"), usage.get("output_tokens")) if usage else (0.0 if llm.is_local else None)
                record = {"configuration": row["configuration"], "command": cmd, "scanner_version": self.env_info["scanner_version"],
                          "started_at": started, "finished_at": now_utc(), "report_file": row["report_file"],
                          "exit_code": exit_code, "wall_seconds": wall, "stderr_tail": rules.redact(stderr[-2000:]),
                          "status": status, "status_reasons": reasons, "analyzer_failures": failures,
                          "attempt": attempt, "llm_model": llm.model if cfg["uses_llm"] or cfg["uses_meta"] else None,
                          "llm_usage": usage, "cost_usd": cost, "llm": llm_info, "meta": meta_info,
                          "fingerprint": self.fingerprint}
                self.ledger.append(event="end", skill_id=row["skill_id"], configuration=row["configuration"],
                                   analyzer_mode=row["analyzer_mode"], attempt=attempt, status=status, exit_code=exit_code,
                                   wall_seconds=wall, input_tokens=usage.get("input_tokens"),
                                   output_tokens=usage.get("output_tokens"), cost_usd=cost, retryable=retryable)
                attempts.append({k: record[k] for k in ("attempt", "status", "wall_seconds", "cost_usd")})
                last = attempt == self.experiment.max_attempts
                if status == "FAILED_CONFIGURATION":
                    self.stop_reason = f"configuration error from Cisco: {reasons[0]}"
                    self.stop.set()
                if retryable and not last and not self.stop.is_set():
                    if out.is_file():
                        keep = report_path.parent / "attempts" / f"{report_path.stem}.attempt{attempt}.json"
                        keep.parent.mkdir(exist_ok=True)
                        shutil.copy2(out, keep)
                    delay = min(self.experiment.backoff_seconds * 2 ** (attempt - 1), 900)
                    self.log(f"  retry {row['skill_id']} | {row['configuration']}: {status} ({reasons[:1]}); waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                if out.is_file():
                    shutil.move(out, report_path)
                    record["report_sha256"] = sha256_file(report_path)
                record.update(final=True, attempts=attempts)
                write_json(run_record_path(report_path), record)
                return record
        return None

    def execute(self, modes=None, skills=None, log_every=1):
        extra = self.check_ready()
        todo = self.pending(modes, skills)
        self._write_status("running", extra)
        self.log(f"{len(todo)} scan(s) to run ({sum(1 for r in self.plan if r['action'] == 'scan')} planned new scans; "
                 f"finished ones are skipped)")
        done = 0
        with ThreadPoolExecutor(max_workers=max(1, self.experiment.workers)) as pool:
            futures = {pool.submit(self.run_one, row): row for row in todo}
            for future in as_completed(futures):
                row, record = futures[future], future.result()
                if record is None:
                    continue
                done += 1
                if done % log_every == 0:
                    usage = record.get("llm_usage") or {}
                    self.log(f"[{done}/{len(todo)}] {row['skill_id']} | {row['configuration']}: {record['status']} "
                             f"{record['wall_seconds']}s in={usage.get('input_tokens')} out={usage.get('output_tokens')} "
                             f"llm={record['llm'].get('status')} meta={record['meta'].get('status')}")
        state = "stopped" if self.stop.is_set() else "complete" if not self.pending(modes, skills) else "incomplete"
        self._write_status(state, extra)
        if self.stop_reason:
            self.log(f"STOPPED: {self.stop_reason}")
        return state

    def _write_status(self, state, extra):
        entries = self.ledger.entries()
        starts = {(e["skill_id"], e["configuration"], e["attempt"]) for e in entries if e["event"] == "start"}
        ends = {(e["skill_id"], e["configuration"], e["attempt"]) for e in entries if e["event"] == "end"}
        write_json(self.run_dir / "execution_status.json", {
            "state": state, "stop_reason": self.stop_reason, "updated_at": now_utc(), "environment": self.env_info,
            "llm_request_settings": resolved_request_settings(self.experiment.llm), **extra,
            "attempts_started": len(starts), "attempts_finished": len(ends),
            "attempts_interrupted": len(starts - ends), "spent_usd": round(self.ledger.spent_usd(), 6),
            "pending": len(self.pending()),
        })
