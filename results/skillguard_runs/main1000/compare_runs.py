"""Reproducibility check between two notebook-01 runs of the same manifest (plus SkillGuard outputs).

    .venv/bin/python -I results/skillguard_runs/main1000/compare_runs.py <run_a> <run_b> [<out.json>]

Compares: exported skill files (sha256 of every file under <skill>/full and <skill>/only),
scan statuses per (skill, configuration), Cisco findings per (skill, configuration) as a
multiset of (rule_id, file, line, severity) read from the raw reports, and SkillGuard raw
results (findings/behaviors/coverage, ignoring the absolute root path) when present.
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def files(run):
    out = {}
    for p in sorted(run.glob("*/full/**/*")) + sorted(run.glob("*/only/**/*")):
        if p.is_file():
            out[str(p.relative_to(run))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def reports(run):
    out = {}
    for p in sorted(run.glob("*/reports/*.json")):
        if p.name.endswith(".run.json"):
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        key = f"{p.parent.parent.name}/{p.stem}"
        out[key] = Counter((f.get("rule_id"), f.get("file_path"), f.get("line_number"), f.get("severity"))
                           for f in data.get("findings", []))
    return out


def statuses(run):
    import csv
    return {(r["skill_id"], r["configuration"]): (r["status"], r["findings_count"])
            for r in csv.DictReader((run / "scan_summary.csv").open(encoding="utf-8"))}


def skillguard(run):
    base = REPO / "results/skillguard_runs/main1000/skillguard" / run.name / "raw"
    out = {}
    for p in sorted(base.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d.pop("root", None)
        out[p.stem] = json.dumps(d, sort_keys=True)
    return out


def main():
    a, b = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    fa, fb = files(a), files(b)
    ra, rb = reports(a), reports(b)
    sa, sb = statuses(a), statuses(b)
    ga, gb = skillguard(a), skillguard(b)
    result = {
        "run_a": str(a.relative_to(REPO)), "run_b": str(b.relative_to(REPO)),
        "exported_files": {"a": len(fa), "b": len(fb), "identical": fa == fb,
                           "differing": sorted(k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k))[:20]},
        "reports": {"a": len(ra), "b": len(rb), "identical_findings": ra == rb,
                    "differing": sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))},
        "scan_statuses_identical": sa == sb,
        "skillguard": {"a": len(ga), "b": len(gb), "identical": ga == gb and bool(ga)},
    }
    print(json.dumps(result, indent=2))
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
