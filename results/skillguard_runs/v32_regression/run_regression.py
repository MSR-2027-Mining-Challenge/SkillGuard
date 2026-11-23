"""Regression comparison: frozen SkillGuard V3.1 vs V3.2 on previously exported research samples.

    PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/v32_regression/run_regression.py

Inputs (read-only; nothing is modified, nothing from a skill is executed):
  * seed-2030 1,000-skill run exports: results/cisco_dataset_runs/agent_skills_sample/runs/*sample1000-seed2030-batch*/<skill>/full
  * seed-2027 30-skill run:            .../runs/2026-11-03_173516_sample30-seed2027/<skill>/full
  * held-out seed 2028 (H1, H2) and fresh seed 2029 (R100): results/skillguard_runs/heldout/*/<set>/<skill>/full
These folders are local (untracked); the script records which were found.
Cisco core findings (finding_kind == security) of the seed-2030 runs are used for the location overlap
(same file, within +/-3 lines), exactly as in the 1,000-skill report.

Outputs: results/skillguard_runs/v32_regression/<timestamp>/ (new folder; never overwritten):
  per_skill.csv, v32_behaviors.csv, v31_vs_v32_locations.csv, summary.json, REPORT_regression.md
Raw per-skill JSON is not written (results contain absolute local paths); every number is in the CSVs.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import importlib.util
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "src"))
from skillguard import scan as scan32  # noqa: E402
from skillguard.scanner import _tool_sha  # noqa: E402

V31 = REPO / "results/skillguard_runs/versions/skillguard_capabilities_v3.1_eebc59e7.py"
RUNS = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs"
HELDOUT = REPO / "results/skillguard_runs/heldout"
WINDOW = 3
# V3.1's agent-specific capability families and their V3.2 counterparts.
V31_TO_V32 = {"scheduler_invocation": "scheduler_invocation", "agent_config_modification": "agent_config_modification",
              "agent_env_marker_removal": "agent_env_marker_removal", "agent_credential_access": "agent_credential_access",
              "approval_bypass_instruction": "approval_bypass_instruction",
              "suspicious_agent_instruction": "suspicious_agent_instruction"}


def load_v31():
    assert hashlib.sha256(V31.read_bytes()).hexdigest().startswith("eebc59e7")
    spec = importlib.util.spec_from_file_location("sg31", V31)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corpora():
    sets = []
    for run in sorted(RUNS.glob("*sample1000-seed2030-batch*")):
        sets += [("seed2030_main1000", p.parent.name, p) for p in sorted(run.glob("*/full"))]
    s30 = RUNS / "2026-11-03_173516_sample30-seed2027"
    sets += [("seed2027_sample30", p.parent.name, p) for p in sorted(s30.glob("*/full"))]
    for sub in ("2026-11-13_heldout-seed2028/H1_random", "2026-11-13_heldout-seed2028/H2_enriched",
                "2026-11-13_fresh100-seed2029/R100"):
        sets += [(f"heldout_{sub.split('/')[-1]}", p.parent.name, p) for p in sorted((HELDOUT / sub).glob("*/full"))]
    return sets


def v31_map(f):
    cap = f["capability"]
    if cap == "nested_agent_invocation":
        mech = f["details"].get("mechanism", "")
        return "in_host_delegation" if mech in {"agent_spawn_instruction", "agent_tool_call"} else "external_agent_launch"
    return V31_TO_V32.get(cap, cap)


def cisco_index():
    idx = defaultdict(list)
    for run in sorted(RUNS.glob("*sample1000-seed2030-batch*")):
        path = run / "individual_findings.csv"
        if not path.is_file():
            continue
        for r in csv.DictReader(path.open(encoding="utf-8")):
            if r.get("finding_kind") != "security" or not r.get("configuration", "").startswith("Full folder"):
                continue
            line = int(r["reported_line_number"]) if r["reported_line_number"].strip().isdigit() else None
            idx[(r["skill_id"], r["file_path"])].append((line, r["rule_id"]))
    return idx


def write_csv(path, rows):
    fields = list(rows[0].keys()) if rows else ["empty"]
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in r.items()})


def main():
    v31 = load_v31()
    out = HERE / dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out.mkdir(parents=True, exist_ok=False)
    cisco = cisco_index()
    per_skill, behaviors, locations = [], [], []
    seen_ids = set()
    t31 = t32 = 0.0
    cov31, cov32 = Counter(), Counter()
    for corpus, skill_id, folder in corpora():
        dup = skill_id in seen_ids
        seen_ids.add(skill_id)
        a = time.perf_counter()
        r31 = v31.scan(folder)
        b = time.perf_counter()
        r32 = scan32(folder)
        c = time.perf_counter()
        t31 += b - a
        t32 += c - b
        files31 = {}
        for item in r31["coverage"]:  # V3.1 lists one entry per analyzed block; count each file once
            ok = item["status"] in v31.COVERED_STATUSES
            files31[item["file"]] = files31.get(item["file"], False) or ok
        for file, ok in files31.items():
            cov31[Path(file).suffix.lower() or "(none)", ok] += 1
        for item in r32["coverage"]["files"]:
            cov32[Path(item["file"]).suffix.lower() or "(none)", item["status"] in
                  {"analyzed", "analyzed_with_parse_errors", "markdown_instructions_only", "disguised_text_scanned",
                   "parsed_no_agent_config"}] += 1
        # behaviors
        b31 = Counter()
        for beh in r31["behaviors"]:
            cap = beh["capability"]
            if cap == "nested_agent_invocation":
                cap = "in_host_delegation" if beh["key"] == "agent_tool" else "external_agent_launch"
            b31[cap] += 1
        prim = [x for x in r32["behaviors"] if not x["supporting"]]
        agent_specific = [x for x in prim if x["capability"] != "in_host_delegation"]
        for beh in prim:
            near = []
            for loc in beh["locations"]:
                file, _, line = loc.rpartition(":")
                for cl, rule in cisco.get((skill_id, file), []):
                    if cl is not None and abs(cl - int(line)) <= WINDOW:
                        near.append(rule)
            behaviors.append({"corpus": corpus, "skill_id": skill_id, "behavior_id": beh["behavior_id"],
                              "capability": beh["capability"], "category": beh["category"],
                              "subcategory": beh["subcategory"], "evidence_level": beh["evidence_level"],
                              "severity": beh["severity"], "confidence": beh["confidence"],
                              "review_priority": beh["review_priority"], "risk_indicators": beh["risk_indicators"],
                              "locations": beh["locations"][:5], "cisco_security_near": sorted(set(near))})
        # location-level comparison of the capability families both versions know
        loc31 = {(v31_map(f), f["file"], f["line"]) for f in r31["findings"]}
        loc32 = {(f["capability"], f["file"], f["line"]) for f in r32["findings"]}
        for cap, file, line in sorted(loc31 | {x for x in loc32 if x[0] in set(V31_TO_V32.values()) |
                                               {"external_agent_launch", "in_host_delegation"}}):
            locations.append({"corpus": corpus, "skill_id": skill_id, "capability": cap, "file": file, "line": line,
                              "in_v31": (cap, file, line) in loc31, "in_v32": (cap, file, line) in loc32})
        per_skill.append({
            "corpus": corpus, "skill_id": skill_id, "duplicate_of_earlier_corpus": dup,
            "v31_behaviors": sum(b31.values()), "v31_agent_specific_excl_delegation": sum(v for k, v in b31.items()
                                                                                         if k != "in_host_delegation"),
            "v31_high_priority": sum(1 for x in r31["behaviors"] if x["review_priority"] == "high"),
            "v32_primary_behaviors": len(prim), "v32_agent_specific_excl_delegation": len(agent_specific),
            "v32_high_priority": sum(1 for x in prim if x["review_priority"] == "high"),
            "v32_reviewable_behaviors": sum(1 for x in prim if x["review_priority"] != "none"),
            "v32_chains": len(r32["chains"]), "v32_chain_rules": sorted({ch["rule"] for ch in r32["chains"]}),
            "v32_highest_priority": r32["summary"]["highest_priority"],
            "v32_files_not_analyzed": r32["coverage"]["summary"]["not_analyzed"],
            "v31_files_not_analyzed": len(v31.limitations(r31)),
        })
    write_csv(out / "per_skill.csv", per_skill)
    write_csv(out / "v32_behaviors.csv", behaviors)
    write_csv(out / "v31_vs_v32_locations.csv", locations)

    uniq = [p for p in per_skill if not p["duplicate_of_earlier_corpus"]]
    beh_uniq = [b for b in behaviors if any(p["skill_id"] == b["skill_id"] and p["corpus"] == b["corpus"] for p in uniq)]
    loc_counter = Counter((l["capability"], l["in_v31"], l["in_v32"]) for l in locations)
    summary = {
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "v32_tool_sha256": _tool_sha(), "v31_sha256_prefix": "eebc59e7",
        "skills_scanned": len(per_skill), "unique_skills": len(uniq),
        "by_corpus": dict(Counter(p["corpus"] for p in per_skill)),
        "runtime_seconds": {"v31": round(t31, 1), "v32": round(t32, 1)},
        "skills_with_any": {
            "v31_any_behavior": sum(p["v31_behaviors"] > 0 for p in uniq),
            "v31_excluding_delegation": sum(p["v31_agent_specific_excl_delegation"] > 0 for p in uniq),
            "v32_any_primary_behavior": sum(p["v32_primary_behaviors"] > 0 for p in uniq),
            "v32_excluding_delegation": sum(p["v32_agent_specific_excl_delegation"] > 0 for p in uniq),
            "v32_any_reviewable_behavior_priority_low_or_higher": sum(p["v32_reviewable_behaviors"] > 0 for p in uniq),
            "v31_high_priority": sum(p["v31_high_priority"] > 0 for p in uniq),
            "v32_high_priority_behavior": sum(p["v32_high_priority"] > 0 for p in uniq),
            "v32_any_chain": sum(p["v32_chains"] > 0 for p in uniq),
            "v32_highest_priority_high_incl_chains": sum(p["v32_highest_priority"] == "high" for p in uniq),
        },
        "v32_behaviors_by_capability": dict(Counter(b["capability"] for b in beh_uniq).most_common()),
        "v32_behaviors_by_evidence_level": dict(Counter(b["evidence_level"] for b in beh_uniq).most_common()),
        "v32_behaviors_by_priority": dict(Counter(b["review_priority"] for b in beh_uniq).most_common()),
        "v32_chain_rules_skills": dict(Counter(r for p in uniq for r in p["v32_chain_rules"]).most_common()),
        "location_comparison": {f"{cap}|v31={a}|v32={b}": n for (cap, a, b), n in sorted(loc_counter.items())},
        "files_analyzed_by_suffix": {
            "v31": {f"{s}|{'analyzed' if ok else 'not'}": n for (s, ok), n in sorted(cov31.items())},
            "v32": {f"{s}|{'analyzed' if ok else 'not'}": n for (s, ok), n in sorted(cov32.items())}},
        "v32_behaviors_near_cisco_seed2030": sum(1 for b in behaviors if b["corpus"] == "seed2030_main1000"
                                                 and b["cisco_security_near"]),
        "v32_behaviors_seed2030": sum(1 for b in behaviors if b["corpus"] == "seed2030_main1000"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("written", out)


if __name__ == "__main__":
    main()
