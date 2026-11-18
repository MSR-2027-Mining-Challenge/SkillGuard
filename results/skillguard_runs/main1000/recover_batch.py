"""Crash recovery for notebook-01 batch runs (notebook 01 itself cannot resume a run).

    # 1. after a crash: which skills finished, and a manifest for the rest
    .venv/bin/python -I recover_batch.py plan <crashed_run_dir> <batch_manifest.csv> <recovery_manifest.csv>
    # 2. run notebook 01 on <recovery_manifest.csv> (new run folder), and run notebook 01 in
    #    RUN_MODE="reanalyze" on <crashed_run_dir> to get tables for the finished skills
    # 3. merge: finished skills from the reanalysis + all skills from the recovery run
    .venv/bin/python -I recover_batch.py merge <out_dir> <batch_manifest.csv> <reanalysis_run_dir>:<crashed_run_dir> <recovery_run_dir>

A skill counts as finished only if all 4 configuration reports exist with their .run.json records
and parse as JSON (notebook 01 writes each report atomically, so a crash can only leave a
missing report, never a truncated one). Partially scanned skills are re-scanned in full.
The merge refuses to continue unless every manifest skill appears exactly once with 4 configurations.
"""

import csv
import json
import sys
from pathlib import Path

CONFIG_FILES = ["skill_only_default.json", "skill_only_behavioral.json", "full_folder_default.json", "full_folder_behavioral.json"]


def finished(run_dir):
    done, partial = [], []
    for manifest in sorted(Path(run_dir).glob("*/manifest.json")):
        reports = manifest.parent / "reports"
        ok = 0
        for name in CONFIG_FILES:
            report, record = reports / name, reports / name.replace(".json", ".run.json")
            try:
                json.loads(report.read_text(encoding="utf-8"))
                json.loads(record.read_text(encoding="utf-8"))
                ok += 1
            except (OSError, json.JSONDecodeError):
                pass
        (done if ok == len(CONFIG_FILES) else partial).append((manifest.parent.name, ok))
    return done, partial


def plan(crashed, batch_manifest, recovery_manifest):
    done, partial = finished(crashed)
    done_ids = {s for s, _ in done}
    with open(batch_manifest, encoding="utf-8") as h:
        reader = csv.DictReader(h)
        fields, rows = reader.fieldnames, list(reader)
    remaining = [r for r in rows if r["skill_id"] not in done_ids]
    out = Path(recovery_manifest)
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    with out.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(remaining)
    print(json.dumps({"finished_skills": len(done), "partially_scanned_skills": partial,
                      "not_started_or_partial_to_rescan": len(remaining), "recovery_manifest": str(out)}, indent=2))


def merge(out_dir, batch_manifest, reanalysis_spec, recovery_run):
    reanalysis_run, crashed = reanalysis_spec.split(":", 1)
    done_ids = {s for s, _ in finished(crashed)[0]}
    wanted = [r["skill_id"] for r in csv.DictReader(open(batch_manifest, encoding="utf-8"))]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    summary = {}
    for table in ("scan_summary.csv", "individual_findings.csv"):
        merged, fields = [], None
        for run, keep in ((reanalysis_run, lambda s: s in done_ids), (recovery_run, lambda s: s not in done_ids)):
            with open(Path(run) / table, encoding="utf-8") as h:
                reader = csv.DictReader(h)
                fields = fields or reader.fieldnames
                merged.extend(r for r in reader if keep(r["skill_id"]))
        with (out / table).open("w", newline="", encoding="utf-8") as h:
            w = csv.DictWriter(h, fieldnames=fields)
            w.writeheader()
            w.writerows(merged)
        summary[table] = len(merged)
    scans = list(csv.DictReader(open(out / "scan_summary.csv", encoding="utf-8")))
    per_skill = {}
    for r in scans:
        per_skill.setdefault(r["skill_id"], set()).add(r["configuration"])
    problems = [s for s in wanted if len(per_skill.get(s, ())) != 4] + [s for s in per_skill if s not in wanted]
    if problems or len(scans) != 4 * len(wanted):
        raise SystemExit(f"merge incomplete or duplicated: {problems[:10]} rows={len(scans)}")
    summary.update({"skills": len(wanted), "from_crashed_run": len(done_ids), "from_recovery_run": len(wanted) - len(done_ids),
                    "sources": {"reanalysis": reanalysis_run, "crashed": crashed, "recovery": recovery_run}})
    (out / "merge_metadata.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"plan": plan, "merge": merge}[cmd](*args)
