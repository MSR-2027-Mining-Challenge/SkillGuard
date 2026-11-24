"""Detailed findings analysis of the next1000 experiment on the OPEN subset (750 skills).

Reads only open tables (never sealed/): cisco_core/, cisco_atr/, malskills/, skillguard/ of the four batch
runs and analysis/2026-11-23_040133/per_skill_three_way_open.csv. Writes small aggregate tables to
analysis/findings_open/ that ANALYSIS_next1000.md and the figures cite. Whole-sample (1,000-skill)
aggregates come from analyze_next1000.py, not from here.

    .venv/bin/python -I results/skillguard_runs/next1000/analyze_findings_open.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import HERE, lockbox_ids, write_csv  # noqa: E402

RUNS = ["2026-11-22_223501_next1000-seed2031-batch1", "2026-11-23_000733_next1000-seed2031-batch2",
        "2026-11-23_013501_next1000-seed2031-batch3", "2026-11-23_024754_next1000-seed2031-batch4"]
PER_SKILL = HERE / "analysis/2026-11-23_040133/per_skill_three_way_open.csv"
OUT = HERE / "analysis/findings_open"
PRIMARY = "Full folder | behavioral"
CONFIGS = ["SKILL.md only | default", "SKILL.md only | behavioral", "Full folder | default", PRIMARY]
SEV = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]


def read(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(line.replace("\0", "") for line in h))


def jl(v):
    try:
        return json.loads(v) if v else []
    except json.JSONDecodeError:
        return []


def file_type(path):
    p = (path or "").split(":")[0].strip().lower()
    name = p.rsplit("/", 1)[-1]
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    if name == "skill.md":
        return "SKILL.md" if "/" not in p else "nested SKILL.md"
    if ext in ("md", "mdx", "txt", "rst"):
        return "other Markdown/text"
    if ext == "py":
        return "Python"
    if ext in ("sh", "bash", "zsh", "ps1", "bat", "cmd"):
        return "shell/PowerShell"
    if ext in ("js", "mjs", "cjs", "ts", "tsx", "jsx", "mts", "cts"):
        return "JavaScript/TypeScript"
    if ext in ("json", "jsonc", "yaml", "yml", "toml", "ini", "cfg", "conf", "env") or name.startswith(".env"):
        return "config/data (JSON/YAML/TOML/INI)"
    if not p:
        return "(no file)"
    return "other"


def loc_file(loc):
    return loc.rsplit(":", 1)[0] if ":" in loc else loc


def main():
    sealed = lockbox_ids()
    per = {r["skill_id"]: r for r in read(PER_SKILL)}
    assert not (set(per) & sealed), "open per-skill table contains lockbox skills"
    core, core_scans, atr, ms, ms_pat, ms_scan = defaultdict(list), defaultdict(dict), defaultdict(list), defaultdict(list), defaultdict(list), {}
    sg32, sg31, chains, cov = defaultdict(list), defaultdict(list), defaultdict(list), []
    for run in RUNS:
        for r in read(HERE / "cisco_core" / run / "findings.csv"):
            if r["finding_kind"] == "security":
                core[r["skill_id"]].append(r)
        for r in read(HERE / "cisco_core" / run / "scans.csv"):
            core_scans[r["skill_id"]][r["configuration"]] = r
        for r in read(HERE / "cisco_atr" / run / "findings.csv"):
            if r["severity"] != "INFO":
                atr[r["skill_id"]].append(r)
        m = HERE / "malskills" / f"{run}__malskills_output"
        for r in read(m / "sso_findings.csv"):
            ms[r["skill_id"]].append(r)
        for r in read(m / "pattern_verdicts.csv"):
            ms_pat[r["skill_id"]].append(r)
        for r in read(m / "scans.csv"):
            ms_scan[r["skill_id"]] = r
        g = HERE / "skillguard" / run
        for r in read(g / "v32_behaviors.csv"):
            sg32[r["skill_id"]].append(r)
        for r in read(g / "v31_behaviors.csv"):
            sg31[r["skill_id"]].append(r)
        for r in read(g / "v32_chains.csv"):
            chains[r["skill_id"]].append(r)
        cov += read(g / "v32_coverage.csv")
    for table in (core, core_scans, atr, ms, ms_pat, ms_scan, sg32, sg31, chains):
        assert not (set(table) & sealed), "open table contains lockbox rows"
    skills = sorted(per)
    usable = [s for s in skills if per[s]["cisco_core_complete"] == "True"]
    OUT.mkdir(parents=True, exist_ok=True)
    info = {"open_skills": len(skills), "open_skills_cisco_core_complete": len(usable)}

    # ---------------------------------------------------------------- Cisco core
    by_conf = []
    for c in CONFIGS:
        flagged = [s for s in usable if any(f["configuration"] == c for f in core[s])]
        by_conf.append({"configuration": c, "skills_usable": len(usable), "skills_flagged": len(flagged),
                        "pct": round(100 * len(flagged) / len(usable), 2),
                        "findings": sum(1 for s in usable for f in core[s] if f["configuration"] == c)})
    write_csv(OUT / "cisco_core_by_configuration.csv", by_conf)

    prim = [(s, f) for s in usable for f in core[s] if f["configuration"] == PRIMARY]
    agg = defaultdict(lambda: {"findings": 0, "skills": set(), "sev": Counter(), "ft": Counter()})
    for s, f in prim:
        a = agg[(f["rule_id"], f["research_category"], f["cisco_category"], f["analyzer"])]
        a["findings"] += 1
        a["skills"].add(s)
        a["sev"][f["severity"]] += 1
        a["ft"][file_type(f["file_path"])] += 1
    write_csv(OUT / "cisco_core_rules_full_behavioral.csv", sorted(
        [{"rule_id": k[0], "research_category": k[1], "cisco_category": k[2], "analyzer": k[3], "findings": v["findings"],
          "skills": len(v["skills"]), "severities": dict(v["sev"]), "file_types": dict(v["ft"])} for k, v in agg.items()],
        key=lambda r: (-r["skills"], -r["findings"], r["rule_id"])))
    cat = defaultdict(lambda: [0, set()])
    for s, f in prim:
        cat[f["research_category"]][0] += 1
        cat[f["research_category"]][1].add(s)
    write_csv(OUT / "cisco_core_categories_full_behavioral.csv", sorted(
        [{"research_category": k, "findings": v[0], "skills": len(v[1]),
          "pct_of_flagged_skills": round(100 * len(v[1]) / max(1, len({s for s, _ in prim})), 1)} for k, v in cat.items()],
        key=lambda r: -r["skills"]))
    ft = defaultdict(lambda: [0, set()])
    for s, f in prim:
        ft[file_type(f["file_path"])][0] += 1
        ft[file_type(f["file_path"])][1].add(s)
    write_csv(OUT / "cisco_core_file_types_full_behavioral.csv", sorted(
        [{"file_type": k, "findings": v[0], "skills": len(v[1])} for k, v in ft.items()], key=lambda r: -r["findings"]))
    an = Counter((f["configuration"], f["analyzer"]) for s in usable for f in core[s])
    write_csv(OUT / "cisco_core_analyzers.csv", [{"configuration": c, "analyzer": a, "findings": n} for (c, a), n in sorted(an.items())])
    rules_def = {f["rule_id"] for s in usable for f in core[s] if f["configuration"] == "Full folder | default"}
    beh_only = Counter(f["rule_id"] for s, f in prim if f["rule_id"] not in rules_def)
    beh_skills = defaultdict(set)
    for s, f in prim:
        if f["rule_id"] not in rules_def:
            beh_skills[f["rule_id"]].add(s)
    write_csv(OUT / "cisco_core_behavioral_only_rules.csv",
              [{"rule_id": r, "findings": n, "skills": len(beh_skills[r])} for r, n in beh_only.most_common()])
    trans = Counter()
    for s in usable:
        a = any(f["configuration"] == "SKILL.md only | behavioral" for f in core[s])
        b = any(f["configuration"] == PRIMARY for f in core[s])
        d = any(f["configuration"] == "Full folder | default" for f in core[s])
        trans[("skillmd_behavioral=%d" % a, "full_default=%d" % d, "full_behavioral=%d" % b)] += 1
    write_csv(OUT / "cisco_core_configuration_transitions.csv",
              [{"skillmd_behavioral": k[0][-1], "full_default": k[1][-1], "full_behavioral": k[2][-1], "skills": n}
               for k, n in sorted(trans.items())])
    maxsev = Counter()
    for s in usable:
        sev = [f["severity"] for f in core[s] if f["configuration"] == PRIMARY]
        maxsev[next((x for x in SEV if x in sev), "none")] += 1
    write_csv(OUT / "cisco_core_max_severity_full_behavioral.csv",
              [{"max_severity": k, "skills": maxsev[k]} for k in SEV + ["none"]])
    flagged_strata = Counter(per[s]["stratum"] for s in usable if any(f["configuration"] == PRIMARY for f in core[s]))
    info["cisco_core_flagged_open_by_stratum"] = dict(flagged_strata)
    info["cisco_core_usable_open_by_stratum"] = dict(Counter(per[s]["stratum"] for s in usable))

    # ---------------------------------------------------------------- ATR
    atr_open = [(s, f) for s in skills for f in atr[s] if f["atr_rule"] == "True"]
    ar = defaultdict(lambda: {"findings": 0, "skills": set(), "sev": Counter(), "ft": Counter(), "cat": Counter()})
    for s, f in atr_open:
        a = ar[f["rule_id"]]
        a["findings"] += 1
        a["skills"].add(s)
        a["sev"][f["severity"]] += 1
        a["ft"][file_type(f["file_path"])] += 1
        a["cat"][f["category"]] += 1
    write_csv(OUT / "atr_rules.csv", sorted(
        [{"rule_id": k, "findings": v["findings"], "skills": len(v["skills"]),
          "max_findings_one_skill": max(Counter(s for s, f in atr_open if f["rule_id"] == k).values()),
          "category": v["cat"].most_common(1)[0][0], "severities": dict(v["sev"]), "file_types": dict(v["ft"])}
         for k, v in ar.items()], key=lambda r: -r["findings"]))
    aft = Counter(file_type(f["file_path"]) for s, f in atr_open)
    write_csv(OUT / "atr_file_types.csv", [{"file_type": k, "findings": n} for k, n in aft.most_common()])
    per_skill_n = sorted((len([1 for f in atr[s] if f["atr_rule"] == "True"]) for s in skills), reverse=True)
    info["atr_open"] = {"findings": len(atr_open), "skills_with_atr": sum(1 for n in per_skill_n if n),
                        "median_findings_per_skill": per_skill_n[len(per_skill_n) // 2],
                        "top10_skills_share_pct": round(100 * sum(per_skill_n[:10]) / max(1, len(atr_open)), 1),
                        "severity": dict(Counter(f["severity"] for s, f in atr_open))}

    # ---------------------------------------------------------------- MalSkills
    mrows = defaultdict(lambda: {"findings": 0, "skills": set(), "ft": Counter()})
    for s in skills:
        for f in ms[s]:
            a = mrows[(f["category"], f["rule_id"])]
            a["findings"] += 1
            a["skills"].add(s)
            a["ft"][file_type(f["file"])] += 1
    write_csv(OUT / "malskills_sso_rules.csv", sorted(
        [{"category": k[0], "rule_id": k[1], "findings": v["findings"], "skills": len(v["skills"]),
          "file_types": dict(v["ft"])} for k, v in mrows.items()], key=lambda r: -r["findings"]))
    mcat = defaultdict(lambda: [0, set()])
    for s in skills:
        for f in ms[s]:
            mcat[f["category"]][0] += 1
            mcat[f["category"]][1].add(s)
    write_csv(OUT / "malskills_sso_categories.csv", sorted(
        [{"category": k, "findings": v[0], "skills": len(v[1])} for k, v in mcat.items()], key=lambda r: -r["skills"]))
    mft = Counter(file_type(f["file"]) for s in skills for f in ms[s])
    write_csv(OUT / "malskills_sso_file_types.csv", [{"file_type": k, "findings": n} for k, n in mft.most_common()])
    info["malskills_open"] = {"verdicts": dict(Counter(ms_scan[s]["verdict"] for s in skills if s in ms_scan)),
                              "skills_with_sso": sum(1 for s in skills if ms[s]),
                              "sso_by_stratum": dict(Counter(per[s]["stratum"] for s in skills if ms[s]))}
    mal = []
    for s in skills:
        if ms_scan.get(s, {}).get("verdict") != "malicious":
            continue
        ids = {i for p in ms_pat[s] for i in jl(p["finding_ids"])}
        for f in ms[s]:
            if f["finding_id"] in ids:
                mal.append({"skill_id": s, "patterns": ";".join(sorted({p["pattern"] for p in ms_pat[s]})),
                            "finding_id": f["finding_id"], "category": f["category"], "rule_id": f["rule_id"],
                            "file": f["file"], "line": f["line"]})
    write_csv(OUT / "malskills_malicious_supporting_findings.csv", mal)

    # ---------------------------------------------------------------- SkillGuard V3.2
    def reviewable(b):
        return b["supporting"] != "True" and b["review_priority"] != "none"
    caps = defaultdict(lambda: {"beh": 0, "skills": set(), "ev": Counter(), "pri": Counter(), "ft": Counter(), "cat": ""})
    for s in skills:
        for b in sg32[s]:
            if not reviewable(b):
                continue
            a = caps[b["capability"]]
            a["beh"] += 1
            a["skills"].add(s)
            a["ev"][b["evidence_level"]] += 1
            a["pri"][b["review_priority"]] += 1
            a["cat"] = f'{b["category"]}/{b["subcategory"]}'
            for t in {file_type(loc_file(x)) for x in jl(b["locations"])}:
                a["ft"][t] += 1
    write_csv(OUT / "sg32_capabilities.csv", sorted(
        [{"capability": k, "category": v["cat"], "behaviors": v["beh"], "skills": len(v["skills"]),
          "evidence_levels": dict(v["ev"]), "review_priority": dict(v["pri"]), "file_types": dict(v["ft"])}
         for k, v in caps.items()], key=lambda r: -r["skills"]))
    nonrev = Counter(b["capability"] for s in skills for b in sg32[s] if not reviewable(b))
    nonrev_sk = defaultdict(set)
    for s in skills:
        for b in sg32[s]:
            if not reviewable(b):
                nonrev_sk[b["capability"]].add(s)
    write_csv(OUT / "sg32_non_reviewable_capabilities.csv",
              [{"capability": k, "behaviors": n, "skills": len(nonrev_sk[k])} for k, n in nonrev.most_common()])
    write_csv(OUT / "sg32_chains.csv", [{"rule": k, "chains": n, "skills": len({s for s in skills for c in chains[s] if c["rule"] == k})}
                                        for k, n in Counter(c["rule"] for s in skills for c in chains[s]).most_common()])
    high = []
    for s in skills:
        for b in sg32[s]:
            if b["review_priority"] == "high":
                high.append({"skill_id": s, "kind": "behavior", "name": b["capability"], "severity": b["severity"],
                             "confidence": b["confidence"], "evidence": b["locations"]})
        for c in chains[s]:
            if c["review_priority"] == "high":
                high.append({"skill_id": s, "kind": "chain", "name": c["rule"], "severity": c["severity"],
                             "confidence": c["confidence"], "evidence": c["evidence"]})
    write_csv(OUT / "sg32_high_priority_open.csv", high)
    cv = defaultdict(Counter)
    for r in cov:
        cv[file_type(r["file"])][r["status"]] += 1
    statuses = sorted({st for v in cv.values() for st in v})
    write_csv(OUT / "sg32_coverage_by_file_type.csv",
              [{"file_type": k, "files": sum(v.values()), **{st: v.get(st, 0) for st in statuses}}
               for k, v in sorted(cv.items(), key=lambda x: -sum(x[1].values()))], fields=["file_type", "files", *statuses])

    # ---------------------------------------------------------------- SG-only skills (open part of the 53)
    allthree = [s for s in usable if per[s]["malskills_status"] == "ok"]
    only = [s for s in allthree if per[s]["skillguard_v32_reviewable"] == "1" and per[s]["cisco_core_full_behavioral"] == "0"
            and per[s]["malskills_any_sso"] == "0"]
    oc = defaultdict(lambda: {"skills": set(), "ev": Counter(), "ft": Counter()})
    for s in only:
        for b in sg32[s]:
            if reviewable(b):
                a = oc[b["capability"]]
                a["skills"].add(s)
                a["ev"][b["evidence_level"]] += 1
                for t in {file_type(loc_file(x)) for x in jl(b["locations"])}:
                    a["ft"][t] += 1
    write_csv(OUT / "sg32_only_skills_by_capability.csv", sorted(
        [{"capability": k, "skills": len(v["skills"]), "evidence_levels": dict(v["ev"]), "file_types": dict(v["ft"])}
         for k, v in oc.items()], key=lambda r: -r["skills"]))
    write_csv(OUT / "sg32_only_skills.csv", [{"skill_id": s, "stratum": per[s]["stratum"],
                                              "capabilities": sorted({b["capability"] for b in sg32[s] if reviewable(b)}),
                                              "chains": sorted({c["rule"] for c in chains[s]}),
                                              "atr_any": per[s]["cisco_atr_rules_any"]} for s in only])
    info["sg32_only_open"] = {"skills": len(only), "by_stratum": dict(Counter(per[s]["stratum"] for s in only)),
                              "with_chain": sum(1 for s in only if chains[s]),
                              "single_capability": sum(1 for s in only if len({b["capability"] for b in sg32[s] if reviewable(b)}) == 1),
                              "atr_also_flags": sum(1 for s in only if per[s]["cisco_atr_rules_any"] == "1")}

    # ---------------------------------------------------------------- V3.1 vs V3.2
    tr = []
    for s in skills:
        a, b = per[s]["skillguard_v31_any"] == "1", per[s]["skillguard_v32_reviewable"] == "1"
        if a != b:
            tr.append({"skill_id": s, "change": "v32_only" if b else "v31_only",
                       "v31_capabilities": sorted({x["capability"] for x in sg31[s]}),
                       "v32_reviewable": sorted({x["capability"] for x in sg32[s] if reviewable(x)}),
                       "v32_non_reviewable": sorted({x["capability"] for x in sg32[s] if not reviewable(x)})})
    write_csv(OUT / "v31_v32_changed_skills.csv", tr)
    c31 = Counter(x["capability"] for s in skills for x in sg31[s])
    c32 = Counter(x["capability"] for s in skills for x in sg32[s] if reviewable(x))
    write_csv(OUT / "v31_v32_capability_counts.csv",
              [{"capability": k, "v31_behaviors": c31.get(k, 0), "v32_reviewable_behaviors": c32.get(k, 0)}
               for k in sorted(set(c31) | set(c32), key=lambda k: (-(c31.get(k, 0) + c32.get(k, 0)), k))])
    info["v31_v32_open"] = {"v32_only": sum(1 for t in tr if t["change"] == "v32_only"),
                            "v31_only": sum(1 for t in tr if t["change"] == "v31_only"),
                            "both": sum(1 for s in skills if per[s]["skillguard_v31_any"] == per[s]["skillguard_v32_reviewable"] == "1")}
    (OUT / "summary.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
