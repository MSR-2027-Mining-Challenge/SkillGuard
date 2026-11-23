"""Three-way analysis of the next 1,000-skill experiment: Cisco (core and core+ATR), MalSkills, SkillGuard.

    PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/next1000/analyze_next1000.py <run_dir> [<run_dir> ...]

Inputs per notebook-01 run (all read-only): the run's scan_summary.csv / individual_findings.csv,
and next1000/{exports,cisco_atr,skillguard,malskills}/<run>/ written by the runners (open and
sealed tables). Output: next1000/analysis/<timestamp>/ (new folder, never overwritten).

Lockbox protection: aggregate statistics use all 1,000 skills (allowed by LOCKBOX_POLICY.md).
Item-level tables (per-skill comparison, location matches) are written for OPEN skills only; the
lockbox rows go to sealed/ with their sha256. This script never prints item-level lockbox data.

Statistics: share of skills with >= 1 item; stratified estimate with design weights N_h/n_h and
finite-population-corrected normal 95% CI (same formulas as main1000/analyze_main1000.py), over the
skills for which the tool's scan is usable (denominators reported). Agreement between tools is
reported as counts; it is not accuracy, and a missing alert is not a false negative.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import lockbox_ids, write_csv  # noqa: E402

REPO = HERE.parents[2]
SAMPLE = REPO / "results/samples/agent_skills_sample_seed2031_scripts400_supporting_no_scripts300_skill_md_only300/sample_manifest.csv"
FLAGS = HERE / "manifests/research_corpus_flags.csv"
STRATA = ["scripts", "supporting_no_scripts", "skill_md_only"]
WINDOW = 3
CORE_PRIMARY = "Full folder | behavioral"
CORE_CONFIGS = ["SKILL.md only | default", "SKILL.md only | behavioral", "Full folder | default", "Full folder | behavioral"]

# Category crosswalk to the SkillGuard taxonomy (T1-T9). Informational: the tools define categories differently.
CISCO_TO_T = {
    "Prompt injection / instruction manipulation": "T1", "Excessive permissions / privilege escalation": "T2",
    "Credential / secret access or exposure": "T4", "External network communication / data exfiltration": "T5",
    "Command execution / dangerous shell operations": "T6", "Supply-chain / dependency risks": "T7",
    "Other (obfuscation)": "T9", "File system modification": "T3", "Malware": "T6",
}
MALSKILLS_TO_T = {"sensitive_data_access": "T4", "network_access": "T5", "payload_execution": "T6",
                  "process_operation": "T6", "software_installation": "T7", "system_configuration": "T3",
                  "cryptography": "T9", "file_operation": "file (no T mapping)"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def weighted(flags, design):
    N = sum({s: n for s, n, _ in design.values()}.values())
    by = defaultdict(list)
    for sid, y in flags.items():
        by[design[sid][0]].append(y)
    est, var = 0.0, 0.0
    for stratum, ys in by.items():
        Nh = next(v[1] for v in design.values() if v[0] == stratum)
        nh = len(ys)
        ph = sum(ys) / nh
        est += Nh / N * ph
        if nh > 1:
            var += (Nh / N) ** 2 * (1 - nh / Nh) * ph * (1 - ph) / (nh - 1)
    se = math.sqrt(var)
    return est, max(0.0, est - 1.96 * se), min(1.0, est + 1.96 * se)


def pct(x):
    return None if x is None else round(100 * x, 2)


def read(path):
    p = Path(path)
    return list(csv.DictReader(p.open(encoding="utf-8"))) if p.is_file() else []


def both(folder, name):
    """Open + sealed rows of a runner table (sealed rows are used for aggregates only)."""
    return read(Path(folder) / f"{name}.csv") + read(Path(folder) / "sealed" / f"{name}.csv")


def jl(value):
    try:
        return json.loads(value) if value else []
    except json.JSONDecodeError:
        return []


def main():
    runs = [Path(r).resolve() for r in sys.argv[1:]]
    out = HERE / "analysis" / dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out.mkdir(parents=True)
    manifest = {r["skill_id"]: r for r in csv.DictReader(SAMPLE.open(encoding="utf-8"))}
    design = {s: (r["stratum"], int(r["population_N"]), int(r["sample_n"])) for s, r in manifest.items()}
    sealed = lockbox_ids()
    research = {r["skill_id"] for r in read(FLAGS)}

    core_status, core_find = defaultdict(dict), defaultdict(list)
    atr_status, atr_find = {}, defaultdict(list)
    ms_status, ms_find, ms_verdict = {}, defaultdict(list), {}
    sg_per, sg32_beh, sg31_beh, sg_chains = {}, defaultdict(list), defaultdict(list), defaultdict(list)
    exports = {}
    missing_inputs = []
    for run in runs:
        for r in read(run / "scan_summary.csv"):
            core_status[r["skill_id"]][r["configuration"]] = r["status"]
        for r in read(run / "individual_findings.csv"):
            if r.get("finding_kind") == "security":
                core_find[r["skill_id"]].append(r)
        a = HERE / "cisco_atr" / run.name
        for r in read(a / "scans.csv"):
            atr_status[r["skill_id"]] = r["status"]
        for r in both(a, "findings"):
            if r["severity"] != "INFO":
                atr_find[r["skill_id"]].append(r)
        g = HERE / "skillguard" / run.name
        for r in both(g, "per_skill"):
            sg_per[r["skill_id"]] = r
        for r in both(g, "v32_behaviors"):
            sg32_beh[r["skill_id"]].append(r)
        for r in both(g, "v31_behaviors"):
            sg31_beh[r["skill_id"]].append(r)
        for r in both(g, "v32_chains"):
            sg_chains[r["skill_id"]].append(r)
        e = HERE / "exports" / run.name / "export_summary.csv"
        for r in read(e):
            exports[r["skill_id"]] = r
        ms_dirs = [d for d in [HERE / "malskills" / f"{run.name}__malskills_output"] if d.is_dir()]  # not archived __run1_* folders
        if not ms_dirs:
            missing_inputs.append(f"malskills:{run.name}")
        for d in ms_dirs:
            for r in read(d / "scans.csv"):
                ms_status[r["skill_id"]] = r["status"]
                ms_verdict[r["skill_id"]] = r.get("verdict")
            for r in both(d, "sso_findings"):
                ms_find[r["skill_id"]].append(r)
        for name, folder in (("cisco_atr", a), ("skillguard", g)):
            if not folder.is_dir():
                missing_inputs.append(f"{name}:{run.name}")

    skills = sorted(core_status)
    # ------------------------------------------------------------ execution / coverage
    def core_ok(s):
        return all(core_status[s].get(c) == "COMPLETE" for c in CORE_CONFIGS)
    execution = {
        "skills_in_runs": len(skills), "manifest_skills": len(manifest),
        "cisco_core_scans": dict(Counter(st for s in skills for st in core_status[s].values())),
        "cisco_core_all4_complete": sum(core_ok(s) for s in skills),
        "cisco_atr_scans": dict(Counter(atr_status.get(s, "missing") for s in skills)),
        "malskills_scans": dict(Counter(ms_status.get(s, "missing") for s in skills)),
        "skillguard_scanned": sum(s in sg_per for s in skills),
        "export_byte_mismatch_skills": sum(int(exports.get(s, {}).get("byte_mismatches", 0) or 0) > 0 for s in skills),
        "folders_with_missing_files": sum(int(exports.get(s, {}).get("files_missing_text", 0) or 0) > 0 for s in skills),
        "folders_with_truncated_listing": sum(exports.get(s, {}).get("listing_truncated") == "True" for s in skills),
        "missing_runner_outputs": missing_inputs,
    }
    incomplete = [{"skill_id": s, "stratum": design[s][0],
                   "cisco_core": {c: core_status[s].get(c, "missing") for c in CORE_CONFIGS if core_status[s].get(c) != "COMPLETE"},
                   "cisco_atr": atr_status.get(s, "missing"), "malskills": ms_status.get(s, "missing"),
                   "folder_missing_files": exports.get(s, {}).get("files_missing_text"),
                   "listing_truncated": exports.get(s, {}).get("listing_truncated")}
                  for s in skills if not core_ok(s) or atr_status.get(s) != "COMPLETE" or ms_status.get(s) != "ok"]
    # open file: open skills only; lockbox rows go to sealed/, the open summary keeps only their counts
    write_csv(out / "incomplete_scans.csv", [r for r in incomplete if r["skill_id"] not in sealed])
    (out / "sealed").mkdir(exist_ok=True)
    write_csv(out / "sealed" / "incomplete_scans.csv", [r for r in incomplete if r["skill_id"] in sealed])
    summary_execution_lockbox_incomplete = dict(Counter(r["stratum"] for r in incomplete if r["skill_id"] in sealed))

    # ------------------------------------------------------------ per-skill indicators
    def reviewable(b):
        return b["supporting"] != "True" and b["review_priority"] != "none"
    ind = {}
    for s in skills:
        full_beh = [f for f in core_find[s] if f["configuration"] == CORE_PRIMARY]
        ind[s] = {
            "cisco_core_full_behavioral": int(bool(full_beh)),
            "cisco_core_skillmd_default": int(any(f["configuration"] == "SKILL.md only | default" for f in core_find[s])),
            "cisco_atr_any": int(bool(atr_find[s])),
            "cisco_atr_rules_any": int(any(f["atr_rule"] == "True" for f in atr_find[s])),
            "malskills_malicious": int(ms_verdict.get(s) == "malicious"),
            "malskills_any_sso": int(bool(ms_find[s])),
            "skillguard_v31_any": int(bool(sg31_beh[s])),
            "skillguard_v32_reviewable": int(any(reviewable(b) for b in sg32_beh[s])),
            "skillguard_v32_high": int(any(b["review_priority"] == "high" and b["supporting"] != "True" for b in sg32_beh[s])
                                       or any(c["review_priority"] == "high" for c in sg_chains[s])),
            "skillguard_v32_agent_specific": int(any(reviewable(b) and b["capability"] not in {"tool_preapproval", "in_host_delegation"}
                                                     for b in sg32_beh[s])),
        }
    usable = {
        "cisco_core_full_behavioral": [s for s in skills if core_ok(s)],
        "cisco_core_skillmd_default": [s for s in skills if core_ok(s)],
        "cisco_atr_any": [s for s in skills if atr_status.get(s) == "COMPLETE"],
        "cisco_atr_rules_any": [s for s in skills if atr_status.get(s) == "COMPLETE"],
        "malskills_malicious": [s for s in skills if ms_status.get(s) == "ok"],
        "malskills_any_sso": [s for s in skills if ms_status.get(s) == "ok"],
        **{k: [s for s in skills if s in sg_per] for k in ("skillguard_v31_any", "skillguard_v32_reviewable",
                                                          "skillguard_v32_high", "skillguard_v32_agent_specific")},
    }

    def rate_rows(subset_name, keep):
        rows = []
        for measure, members in usable.items():
            members = [s for s in members if keep(s)]
            flags = {s: ind[s][measure] for s in members}
            row = {"subset": subset_name, "measure": measure, "n": len(members), "skills_flagged": sum(flags.values())}
            for st in STRATA:
                m = [s for s in members if design[s][0] == st]
                k = sum(flags[s] for s in m)
                lo, hi = wilson(k, len(m))
                row[f"{st}_pct"] = pct(k / len(m)) if m else None
                row[f"{st}_wilson95"] = [pct(lo), pct(hi)]
            est, lo, hi = weighted(flags, design) if members else (None, None, None)
            row.update({"weighted_pct": pct(est), "weighted_ci95": [pct(lo), pct(hi)]})
            rows.append(row)
        return rows
    rates = rate_rows("all usable", lambda s: True)
    rates += rate_rows("excluding research-corpus repositories", lambda s: s not in research)
    rates += rate_rows("complete folders only", lambda s: manifest[s]["folder_complete"] == "True")
    write_csv(out / "prevalence.csv", rates)

    # ------------------------------------------------------------ overlap (skills usable by all three)
    common = [s for s in skills if core_ok(s) and ms_status.get(s) == "ok" and s in sg_per]
    venn = Counter((ind[s]["cisco_core_full_behavioral"], ind[s]["malskills_any_sso"], ind[s]["skillguard_v32_reviewable"])
                   for s in common)
    venn_mal = Counter((ind[s]["cisco_core_full_behavioral"], ind[s]["malskills_malicious"], ind[s]["skillguard_v32_high"])
                       for s in common)
    overlap = {"skills_usable_by_all_three": len(common),
               "cisco_core_x_malskills_sso_x_sg32_reviewable": {f"cisco={a} malskills_sso={b} sg32={c}": n
                                                                 for (a, b, c), n in sorted(venn.items())},
               "cisco_core_x_malskills_malicious_x_sg32_high": {f"cisco={a} malskills_malicious={b} sg32_high={c}": n
                                                                 for (a, b, c), n in sorted(venn_mal.items())}}

    # ------------------------------------------------------------ category crosswalk (skills)
    cat = defaultdict(lambda: Counter())
    for s in common:
        for t in {CISCO_TO_T.get(f["research_category"], "unmapped") for f in core_find[s] if f["configuration"] == CORE_PRIMARY}:
            cat[t]["cisco_core"] += 1
        for t in {MALSKILLS_TO_T.get(f["category"], "unmapped") for f in ms_find[s]}:
            cat[t]["malskills_sso"] += 1
        for t in {b["category"] for b in sg32_beh[s] if reviewable(b)}:
            cat[t]["skillguard_v32"] += 1
        for t in {"T1" if "prompt" in (f["category"] or "") else "atr:" + (f["category"] or "?") for f in atr_find[s]
                  if f["atr_rule"] == "True"}:
            cat[t]["cisco_atr_rules"] += 1
    write_csv(out / "category_crosswalk_skills.csv",
              [{"category": k, **{c: v.get(c, 0) for c in ("cisco_core", "cisco_atr_rules", "malskills_sso", "skillguard_v32")}}
               for k, v in sorted(cat.items())])

    # ------------------------------------------------------------ location agreement
    def near(locs, file, line):
        return any(f == file and l is not None and abs(l - line) <= WINDOW for f, l in locs)

    def to_int(x):
        try:
            return int(float(x))
        except (TypeError, ValueError):
            return None
    loc_rows = []
    agree = Counter()
    for s in common:
        cisco_locs = [(f["file_path"], to_int(f["reported_line_number"])) for f in core_find[s] if f["configuration"].startswith("Full folder")]
        atr_locs = [(f["file_path"], to_int(f["line"])) for f in atr_find[s] if f["atr_rule"] == "True"]
        ms_locs = [(f["file"], to_int(f["line"])) for f in ms_find[s]]
        for b in sg32_beh[s]:
            if not reviewable(b):
                continue
            for loc in jl(b["locations"])[:1]:
                file, _, line = loc.rpartition(":")
                line = to_int(line)
                row = {"skill_id": s, "capability": b["capability"], "category": b["category"],
                       "review_priority": b["review_priority"], "file": file, "line": line,
                       "cisco_core_near": near(cisco_locs, file, line), "cisco_atr_near": near(atr_locs, file, line),
                       "malskills_near": near(ms_locs, file, line)}
                loc_rows.append(row)
                agree["sg32_reviewable_behaviors"] += 1
                for k in ("cisco_core_near", "cisco_atr_near", "malskills_near"):
                    agree[k] += row[k]
        for file, line in set(cisco_locs):
            if line is None:
                continue
            agree["cisco_core_locations"] += 1
            agree["cisco_core_locations_with_malskills_near"] += near(ms_locs, file, line)
    open_locs = [r for r in loc_rows if r["skill_id"] not in sealed]
    write_csv(out / "sg32_location_agreement_open.csv", open_locs)
    agree_by_cap = defaultdict(Counter)
    for r in loc_rows:
        c = agree_by_cap[r["capability"]]
        c["behaviors"] += 1
        for k in ("cisco_core_near", "cisco_atr_near", "malskills_near"):
            c[k] += r[k]
    write_csv(out / "sg32_location_agreement_by_capability.csv",
              [{"capability": k, **v} for k, v in sorted(agree_by_cap.items(), key=lambda kv: -kv[1]["behaviors"])])

    # ------------------------------------------------------------ per-skill table (open skills only)
    per = [{"skill_id": s, "stratum": design[s][0], "research_corpus": s in research,
            "folder_complete": manifest[s]["folder_complete"], **ind[s],
            "cisco_core_complete": core_ok(s), "cisco_atr_status": atr_status.get(s, "missing"),
            "malskills_status": ms_status.get(s, "missing"),
            "sg32_capabilities": sorted({b["capability"] for b in sg32_beh[s] if reviewable(b)}),
            "sg32_chain_rules": sorted({c["rule"] for c in sg_chains[s]}),
            "malskills_categories": sorted({f["category"] for f in ms_find[s]}),
            "cisco_core_categories": sorted({f["research_category"] for f in core_find[s] if f["configuration"] == CORE_PRIMARY})}
           for s in skills]
    write_csv(out / "per_skill_three_way_open.csv", [r for r in per if r["skill_id"] not in sealed])
    write_csv(out / "sealed" / "per_skill_three_way.csv", [r for r in per if r["skill_id"] in sealed])
    sg32_caps = Counter(b["capability"] for s in skills for b in sg32_beh[s] if reviewable(b))
    summary = {"runs": [r.name for r in runs], "execution": execution, "overlap": overlap,
               "location_agreement": dict(agree),
               "sg32_reviewable_behaviors_by_capability": dict(sg32_caps.most_common()),
               "sg_v31_behaviors": sum(len(v) for v in sg31_beh.values()),
               "sg_v32_chains_by_rule": dict(Counter(c["rule"] for v in sg_chains.values() for c in v).most_common()),
               "malskills_verdicts": dict(Counter(ms_verdict.get(s) for s in skills)),
               "atr_findings_total": sum(1 for v in atr_find.values() for f in v if f["atr_rule"] == "True"),
               "atr_top_rules": dict(Counter(f["rule_id"] for v in atr_find.values() for f in v if f["atr_rule"] == "True").most_common(10)),
               "core_full_behavioral_findings": sum(1 for v in core_find.values() for f in v if f["configuration"] == CORE_PRIMARY),
               "lockbox_skills_in_runs": sum(s in sealed for s in skills),
               "lockbox_incomplete_scan_skills_by_stratum": summary_execution_lockbox_incomplete,
               "prevalence_all_usable": {r["measure"]: {"n": r["n"], "flagged": r["skills_flagged"], "weighted_pct": r["weighted_pct"],
                                                       "ci95": r["weighted_ci95"]} for r in rates if r["subset"] == "all usable"}}
    summary["location_agreement_scope"] = "open skills only (lockbox item-level locations are not compared during development)"
    summary["v31_any_x_v32_reviewable"] = {f"v31={a} v32={b}": n for (a, b), n in sorted(Counter(
        (ind[s]["skillguard_v31_any"], ind[s]["skillguard_v32_reviewable"]) for s in skills).items())}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    sums = [f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}" for f in sorted((out / "sealed").glob("*.csv"))]
    (out / "sealed" / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    print(json.dumps(summary, indent=2))
    print("written", out)


if __name__ == "__main__":
    main()
