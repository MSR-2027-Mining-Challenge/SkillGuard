"""Cisco skill-scanner with the optional ATR rule pack on the exported full folders of a run.

    .venv/bin/python -I results/skillguard_runs/next1000/run_cisco_atr.py <cisco_run_dir>

Configuration "Full folder | behavioral + ATR": `skill-scanner scan <full> --format json
--policy balanced --use-behavioral --rule-packs atr` (the 4 core configurations come from notebook 01,
exactly as in main1000). Folder digests are checked before and after every scan.
Status per scan: COMPLETE (JSON parsed, no failed analyzer), PARTIAL (JSON parsed, some analyzer
failed or skill loader fallback), FAILED (no JSON / non-zero exit with no report), MODIFIED_INPUT
(folder digest changed: stops the run).
Outputs: next1000/cisco_atr/<run_id>/raw/<skill>.json (local; absolute paths replaced by <skill>),
scans.csv, findings.csv (+ sealed/ for lockbox skills), summary.json.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I does not add the script folder
from common import HERE, REPO, folder_digest, skill_dirs, write_csv, write_split, reset_sealed

SCANNER = str(REPO / ".venv/bin/skill-scanner")
ARGS = ["--format", "json", "--policy", "balanced", "--use-behavioral", "--rule-packs", "atr"]


def main():
    run = Path(sys.argv[1]).resolve()
    out = HERE / "cisco_atr" / run.name
    (out / "raw").mkdir(parents=True, exist_ok=True)
    reset_sealed(out)
    version = subprocess.run([SCANNER, "--version"], capture_output=True, text=True).stdout.strip()
    scans, findings = [], []
    for skill_id, folder in skill_dirs(run):
        before = folder_digest(folder)
        start = time.time()
        proc = subprocess.run([SCANNER, "scan", str(folder), *ARGS], capture_output=True, text=True, timeout=600)
        seconds = round(time.time() - start, 2)
        after = folder_digest(folder)
        if after != before:
            scans.append({"skill_id": skill_id, "status": "MODIFIED_INPUT"})
            write_csv(out / "scans.csv", scans)
            raise SystemExit(f"input folder changed during scan: {skill_id}")
        try:
            report = json.loads(proc.stdout)
            failed = report.get("scan_metadata", {}).get("analyzers_failed") or []
            fallback = any(f.get("rule_id") == "SKILL_LOAD_FALLBACK_USED" for f in report.get("findings", []))
            status = "PARTIAL" if failed or fallback else "COMPLETE"
        except json.JSONDecodeError:
            report, failed, status = None, [], "FAILED"
        raw = json.dumps(report if report is not None else {"stderr": proc.stderr[-4000:]}, indent=1)
        (out / "raw" / f"{skill_id}.json").write_text(raw.replace(str(folder), "<skill>"))
        scans.append({"skill_id": skill_id, "status": status, "exit_code": proc.returncode, "seconds": seconds,
                      "analyzers_failed": failed, "folder_digest": before})
        for f in (report or {}).get("findings", []):
            path = (f.get("file_path") or "").replace(str(folder) + "/", "")
            findings.append({"skill_id": skill_id, "configuration": "Full folder | behavioral + ATR",
                             "rule_id": f.get("rule_id"), "category": f.get("category"), "severity": f.get("severity"),
                             "analyzer": f.get("analyzer"), "file_path": path, "line": f.get("line_number"),
                             "atr_rule": str(f.get("rule_id", "")).upper().startswith("ATR")})
    write_split(out, "scans", scans)  # lockbox rows (statuses) go to sealed/ as well
    n_open, n_lock = write_split(out, "findings", findings)
    summary = {"run": run.name, "scanner": version, "args": ARGS, "scans": len(scans),
               "statuses": dict(Counter(s["status"] for s in scans)), "findings_open": n_open,
               "findings_sealed": n_lock, "atr_findings_total": sum(f["atr_rule"] for f in findings)}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
