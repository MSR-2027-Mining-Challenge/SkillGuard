"""Compare SkillGuard V3.2 with the existing MalSkills results on the skills both have analyzed.

    PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/v32_scanner_comparison/compare_malskills_overlap.py

MalSkills results: branch origin/rio, results/malskills/package_test_2 (1,000 skills, static profile,
no LLM stage; run by a team member on a Windows/WSL export). Its skills are mapped to DB identities
(file_sha) with next1000/build_exclusions.py's normalizations; the overlap with the seed-2030 sample
is analyzed here using the seed-2030 exported folders (byte-identical to the DB).

Caveats recorded in the report: MalSkills scanned a CRLF-translated copy (same lines, different
bytes), and its sibling files came from the same DB. Agreement is not accuracy.
Outputs: <timestamp>/overlap_skills.csv, location_matches.csv, summary.json, REPORT.md
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path[:0] = [str(REPO / "src"), str(REPO / "results/skillguard_runs/next1000")]
from build_exclusions import variants  # noqa: E402
from malskills_runner import map_line  # noqa: E402
from skillguard import scan  # noqa: E402

BASE = "results/malskills/package_test_2"
SAMPLE = REPO / "results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/sample_manifest.csv"
RUNS = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs"
WINDOW = 3


def git_show(path):
    return subprocess.run(["git", "show", f"origin/rio:{path}"], capture_output=True, text=True, cwd=REPO).stdout


def main():
    recs = [json.loads(l) for l in git_show(f"{BASE}/scan_results.jsonl").splitlines()]
    con = sqlite3.connect((REPO / "data/sample/agent_skills_sample.db").as_uri() + "?mode=ro", uri=True)
    want = {r["skill_content_sha256"]: r for r in recs}
    by_sha = {}
    for content, fsha in con.execute("SELECT content, file_sha FROM artifacts WHERE content IS NOT NULL"):
        for v in variants(content).values():
            h = hashlib.sha256(v.encode("utf-8")).hexdigest()
            if h in want:
                by_sha[want[h]["package"]] = fsha
    sample = {r["file_sha"]: r for r in csv.DictReader(SAMPLE.open(encoding="utf-8"))}
    folders = {p.parent.name: p for p in RUNS.glob("*sample1000-seed2030-batch*/*/full")}
    out = HERE / ("malskills_overlap_" + dt.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    out.mkdir(parents=True)
    skills, matches = [], []
    for rec in recs:
        fsha = by_sha.get(rec["package"])
        row = sample.get(fsha)
        if not row or row["skill_id"] not in folders:
            continue
        folder = folders[row["skill_id"]]
        result = scan(folder)
        prim = [f for f in result["findings"] if not f["supporting"]]
        case = rec["retained_output"]
        arts = {a["artifact_id"]: a for a in json.loads(git_show(f"{BASE}/{case}/artifacts.json") or "[]")}
        ssos = json.loads(git_show(f"{BASE}/{case}/sso_findings.json") or "[]")
        mapped = [(map_line(f, arts), f.get("category")) for f in ssos]
        near_any = 0
        for f in prim:
            hits = sorted({cat for (file, line), cat in mapped
                           if file == f["file"] and line is not None and abs(int(line) - f["line"]) <= WINDOW})
            near_any += bool(hits)
            matches.append({"skill_id": row["skill_id"], "file": f["file"], "line": f["line"], "capability": f["capability"],
                            "severity": f["severity"], "review_priority": f["review_priority"],
                            "malskills_sso_categories_near": hits})
        skills.append({"skill_id": row["skill_id"], "stratum": row["stratum"], "malskills_package": rec["package"],
                       "malskills_verdict": rec["verdict"], "malskills_patterns": rec["patterns"],
                       "malskills_sso_count": rec["sso_count"], "malskills_sso_categories": sorted({c for _, c in mapped}),
                       "v32_primary_findings": len(prim),
                       "v32_reviewable": sum(f["review_priority"] != "none" for f in prim),
                       "v32_capabilities": sorted({f["capability"] for f in prim}),
                       "v32_findings_near_malskills_sso": near_any, "v32_chains": len(result["chains"])})
    for name, rows in (("overlap_skills.csv", skills), ("location_matches.csv", matches)):
        with (out / name).open("w", newline="", encoding="utf-8") as h:
            w = csv.DictWriter(h, fieldnames=list(rows[0].keys()) if rows else ["empty"], lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow({k: json.dumps(v) if isinstance(v, list) else v for k, v in r.items()})
    both = sum(1 for s in skills if s["malskills_sso_count"] and s["v32_reviewable"])
    summary = {
        "overlap_skills": len(skills), "strata": dict(Counter(s["stratum"] for s in skills)),
        "malskills_malicious": sum(s["malskills_verdict"] == "malicious" for s in skills),
        "malskills_any_sso": sum(bool(s["malskills_sso_count"]) for s in skills),
        "v32_any_reviewable": sum(bool(s["v32_reviewable"]) for s in skills),
        "both": both,
        "v32_reviewable_findings": sum(1 for m in matches if m["review_priority"] != "none"),
        "v32_reviewable_findings_with_malskills_sso_within_3_lines":
            sum(1 for m in matches if m["review_priority"] != "none" and m["malskills_sso_categories_near"]),
        "v32_capabilities_without_nearby_sso": dict(Counter(m["capability"] for m in matches
                                                            if m["review_priority"] != "none"
                                                            and not m["malskills_sso_categories_near"]).most_common()),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), out)


if __name__ == "__main__":
    main()
