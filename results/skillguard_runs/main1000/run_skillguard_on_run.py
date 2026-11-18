"""Run frozen SkillGuard V3.1 on the exact folders exported by a notebook-01 Cisco run.

    .venv/bin/python -I results/skillguard_runs/main1000/run_skillguard_on_run.py <cisco_run_dir>

Inputs: <cisco_run_dir>/<skill_id>/full (exported by notebook 01) plus its manifest.json, and the
run's individual_findings.csv / scan_summary.csv. Uses versions/skillguard_capabilities_v3.1_eebc59e7.py
(hash-checked). Nothing from a skill is imported or executed.
Outputs: results/skillguard_runs/main1000/skillguard/<run_id>/ (new folder, never overwritten):
raw/<skill>.json (written per skill as it finishes), behaviors.csv, coverage.csv, per_skill.csv,
summary.json. Behavior-level Cisco overlap = a Cisco finding with finding_kind == "security" in the
same skill and file within +/-3 lines of any behavior location.
"""

import csv
import hashlib
import importlib.util
import json
import platform
import statistics
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TOOL = REPO / "results/skillguard_runs/versions/skillguard_capabilities_v3.1_eebc59e7.py"
TOOL_SHA_PREFIX = "eebc59e7"
WINDOW = 3


def write_csv(path, rows):
    fields = list(rows[0].keys()) if rows else ["empty"]
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in r.items()})


def main():
    run = Path(sys.argv[1]).resolve()
    sha = hashlib.sha256(TOOL.read_bytes()).hexdigest()
    assert sha.startswith(TOOL_SHA_PREFIX), f"frozen tool hash mismatch: {sha}"
    spec = importlib.util.spec_from_file_location("skillguard_v31", TOOL)
    sg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sg)
    out = HERE / "skillguard" / run.name
    (out / "raw").mkdir(parents=True, exist_ok=False)

    cisco = defaultdict(list)
    for r in csv.DictReader((run / "individual_findings.csv").open(encoding="utf-8")):
        if r.get("finding_kind") == "security":
            line = int(r["reported_line_number"]) if r["reported_line_number"].strip().isdigit() else None
            cisco[(r["skill_id"], r["file_path"])].append((line, r["rule_id"], r["configuration"]))
    statuses = defaultdict(dict)
    for r in csv.DictReader((run / "scan_summary.csv").open(encoding="utf-8")):
        statuses[r["skill_id"]][r["configuration"]] = r["status"]

    b_rows, cov_rows, skill_rows, times = [], [], [], []
    for manifest in sorted(run.glob("*/manifest.json")):
        skill_dir = manifest.parent
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        full = skill_dir / "full"
        t0 = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # ast SyntaxWarnings from skill strings
            result = sg.scan(full)
        elapsed = time.perf_counter() - t0
        times.append(elapsed)
        (out / "raw" / f"{skill_dir.name}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        files = defaultdict(set)
        for c in result["coverage"]:
            files[c["file"]].add(c["status"])
            cov_rows.append({"skill_id": skill_dir.name, "file": c["file"], "status": c["status"]})
        for b in result["behaviors"]:
            lines = [(l["file"], l["line"]) for l in b["locations"] + b["documentation"]]
            near = sorted({f"{rule}@{f}:{cl}" for f, ln in lines for cl, rule, _ in cisco.get((skill_dir.name, f), [])
                           if cl is not None and abs(cl - ln) <= WINDOW})
            b_rows.append({"skill_id": skill_dir.name, "behavior_id": b["behavior_id"], "capability": b["capability"],
                           "evidence_level": b["evidence_level"], "review_priority": b["review_priority"],
                           "risk_signals": b["risk_signals"], "locations": [f"{f}:{l}" for f, l in lines],
                           "cisco_security_near": near, "folder_complete": meta.get("folder_complete")})
        skill_rows.append({
            "skill_id": skill_dir.name, "folder_complete": meta.get("folder_complete"),
            "listing_complete": meta.get("listing_complete"), "missing_files": len(meta.get("missing_files", [])),
            "files_exported": len(files),
            "files_code_analyzed": sum(1 for s in files.values() if s & {"analyzed", "analyzed_with_skipped_fences"}),
            "files_text_heuristic_only": sum(1 for s in files.values() if s and s <= {"markdown_instructions_only", "disguised_text_scanned"}),
            "files_not_analyzed": sum(1 for s in files.values() if not s & sg.COVERED_STATUSES),
            "parse_errors": sum(c["status"] == "parse_error" for c in result["coverage"]),
            "findings": len(result["findings"]), "behaviors": len(result["behaviors"]),
            "cisco_security_findings": sum(len(v) for (s, _), v in cisco.items() if s == skill_dir.name),
            "cisco_statuses": statuses.get(skill_dir.name, {}), "skillguard_seconds": round(elapsed, 4)})

    write_csv(out / "behaviors.csv", b_rows)
    write_csv(out / "coverage.csv", cov_rows)
    write_csv(out / "per_skill.csv", skill_rows)
    summary = {"cisco_run": str(run.relative_to(REPO)), "tool": str(TOOL.relative_to(REPO)), "tool_sha256": sha,
               "python": platform.python_version(), "skills": len(skill_rows),
               "files": sum(r["files_exported"] for r in skill_rows),
               "files_code_analyzed": sum(r["files_code_analyzed"] for r in skill_rows),
               "files_text_heuristic_only": sum(r["files_text_heuristic_only"] for r in skill_rows),
               "files_not_analyzed": sum(r["files_not_analyzed"] for r in skill_rows),
               "behaviors": len(b_rows), "behaviors_by_capability": dict(Counter(b["capability"] for b in b_rows)),
               "behaviors_with_cisco_security_near": sum(bool(b["cisco_security_near"]) for b in b_rows),
               "cisco_security_findings": sum(r["cisco_security_findings"] for r in skill_rows),
               "seconds": {"total": round(sum(times), 3), "mean": round(statistics.mean(times), 4), "max": round(max(times), 4)},
               "executed_skill_code": False}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
