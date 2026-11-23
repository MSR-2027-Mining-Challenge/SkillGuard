"""Run frozen SkillGuard V3.1 and SkillGuard V3.2 on the exported full folders of a run.

    PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/next1000/run_skillguard.py <cisco_run_dir>

V3.1: results/skillguard_runs/versions/skillguard_capabilities_v3.1_eebc59e7.py (hash-checked).
V3.2: src/skillguard (combined source sha256 recorded). Folder digests are checked before/after.
Nothing from a skill is imported or executed.
Outputs: next1000/skillguard/<run_id>/{v31_behaviors,v32_behaviors,v32_chains,v32_coverage,per_skill}.csv
(lockbox rows under sealed/), summary.json. Per-skill raw JSON is not written (absolute paths).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I does not add the script folder
from common import HERE, REPO, folder_digest, skill_dirs, write_split, reset_sealed

sys.path.insert(0, str(REPO / "src"))
from skillguard import scan as scan32  # noqa: E402
from skillguard.scanner import _tool_sha  # noqa: E402

V31 = REPO / "results/skillguard_runs/versions/skillguard_capabilities_v3.1_eebc59e7.py"


def load_v31():
    assert hashlib.sha256(V31.read_bytes()).hexdigest().startswith("eebc59e7"), "frozen V3.1 hash mismatch"
    spec = importlib.util.spec_from_file_location("sg31", V31)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    run = Path(sys.argv[1]).resolve()
    v31 = load_v31()
    out = HERE / "skillguard" / run.name
    out.mkdir(parents=True, exist_ok=True)
    reset_sealed(out)
    b31, b32, chains, cov, per = [], [], [], [], []
    for skill_id, folder in skill_dirs(run):
        before = folder_digest(folder)
        r31 = v31.scan(folder)
        r32 = scan32(folder)
        if folder_digest(folder) != before:
            raise SystemExit(f"input folder changed: {skill_id}")
        for b in r31["behaviors"]:
            b31.append({"skill_id": skill_id, "behavior_id": b["behavior_id"], "capability": b["capability"],
                        "key": b["key"], "evidence_level": b["evidence_level"], "review_priority": b["review_priority"],
                        "locations": [f"{l['file']}:{l['line']}" for l in b["locations"] + b["documentation"]][:8]})
        for b in r32["behaviors"]:
            b32.append({"skill_id": skill_id, **{k: b[k] for k in ("behavior_id", "capability", "key", "category",
                        "subcategory", "layer", "supporting", "evidence_level", "severity", "confidence",
                        "review_priority", "risk_indicators")}, "locations": b["locations"][:8]})
        for c in r32["chains"]:
            chains.append({"skill_id": skill_id, "chain_id": c["chain_id"], "rule": c["rule"], "severity": c["severity"],
                           "confidence": c["confidence"], "scope": c["scope"], "review_priority": c["review_priority"],
                           "evidence": [f"{e['file']}:{e['line']} {e['capability']}" for e in c["evidence"]]})
        for c in r32["coverage"]["files"]:
            cov.append({"skill_id": skill_id, "file": c["file"], "status": c["status"],
                        "analyzers": c.get("analyzers", [])})
        prim = [b for b in r32["behaviors"] if not b["supporting"]]
        per.append({"skill_id": skill_id, "folder_digest": before, "v31_behaviors": len(r31["behaviors"]),
                    "v32_primary_behaviors": len(prim),
                    "v32_reviewable_behaviors": sum(b["review_priority"] != "none" for b in prim),
                    "v32_chains": len(r32["chains"]), "v32_highest_priority": r32["summary"]["highest_priority"],
                    "v32_files_not_analyzed": r32["coverage"]["summary"]["not_analyzed"]})
    counts = {}
    for name, rows in (("v31_behaviors", b31), ("v32_behaviors", b32), ("v32_chains", chains),
                       ("v32_coverage", cov), ("per_skill", per)):
        counts[name] = write_split(out, name, rows)
    summary = {"run": run.name, "v31_sha256_prefix": "eebc59e7", "v32_tool_sha256": _tool_sha(), "skills": len(per),
               "rows_open_sealed": counts,
               "open_skills_v32_priority": dict(Counter(p["v32_highest_priority"] for p in per))}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
