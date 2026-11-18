"""Consolidated analysis of the 1,000-skill Cisco Static/Behavioral run and SkillGuard V3.1.

    .venv/bin/python -I results/skillguard_runs/main1000/analyze_main1000.py <cisco_run_dir> [<cisco_run_dir> ...]

Inputs per run: notebook-01 scan_summary.csv, individual_findings.csv, <skill>/manifest.json;
SkillGuard outputs in results/skillguard_runs/main1000/skillguard/<run>/; the approved sample
manifest (strata, design weights) and overlap_with_previous_samples.csv. Read-only.
Output: results/skillguard_runs/main1000/consolidated/<timestamp>/ (tables/*.csv, figures/*.png,
summary.json). Never overwrites.

Definitions
  * Cisco security finding: notebook-01 finding_kind == "security" (metadata_quality and scan_coverage
    rows are reported separately). Deduplicated per (skill, scope, rule, file, line) when modes are unioned.
  * SkillGuard behavior: V3.1 group_behaviors() output (distinct behaviors, not raw rows).
  * Prevalence: share of skills with >= 1 item. Population estimates use the stratified design weights
    (N_h / n_h) with finite-population-corrected stratified variance and a normal 95% CI (clipped to
    [0, 1]); per-stratum rates use Wilson intervals. Estimates describe the GitSkills sample DB frame
    (11,298 representatives in the three strata), not the full release.
  * Primary Cisco analyses use only skills whose 4 scans are all COMPLETE ("primary analysis set") and
    findings from COMPLETE scans (notebook-01 convention). PARTIAL scans (SKILL.md frontmatter rejected by
    Cisco's skill_loader) and CONTRACT_ONLY scans (known FindingContract issue) are reported as a scan-status
    category and enter only the sensitivity row "all executed scans". SkillGuard prevalence uses all skills.
  * A missing Cisco alert next to a SkillGuard behavior is NOT a Cisco false negative, and a SkillGuard
    behavior is a capability, not a validated security detection. No accuracy metrics are computed here.
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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SAMPLE = REPO / "results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/sample_manifest.csv"
OVERLAP = HERE / "manifests/overlap_with_previous_samples.csv"
STRATA = ["scripts", "supporting_no_scripts", "skill_md_only"]
STRATUM_LABEL = {"scripts": "Scripts", "supporting_no_scripts": "Supporting files, no scripts", "skill_md_only": "SKILL.md only"}
CONFIGS = ["SKILL.md only | default", "SKILL.md only | behavioral", "Full folder | default", "Full folder | behavioral"]
SEV_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
WINDOW = 3
# Reference palette (dataviz skill, light mode).
C = {"s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a", "s4": "#eda100", "surface": "#fcfcfb",
     "text": "#0b0b0b", "text2": "#52514e", "grid": "#e4e3df", "muted": "#b9b8b2"}


# ---------------------------------------------------------------- statistics --
def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def weighted(flags, design):
    """flags: {skill_id: 0/1}; design: {skill_id: (stratum, N_h, n_h)} -> (estimate, lo, hi)."""
    N = sum(design_N for design_N in {s: n for s, n, _ in design.values()}.values())
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


def write_csv(path, rows):
    fields = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields or ["empty"])
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in r.items()})


def pct(x):
    return None if x is None else round(100 * x, 2)


# ------------------------------------------------------------------- figures --
def style(ax, title, xlabel=None):
    ax.set_facecolor(C["surface"])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(C["muted"])
    ax.tick_params(colors=C["text2"], labelsize=9, length=0)
    ax.xaxis.grid(True, color=C["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.figure.suptitle(title, x=0.01, ha="left", fontsize=11, color=C["text"])
    if xlabel:
        ax.set_xlabel(xlabel, color=C["text2"], fontsize=9)


def hbar_ci(path, labels, values, los, his, title, xlabel, color=C["s1"]):
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(labels) + 1.3), facecolor=C["surface"])
    y = list(range(len(labels)))[::-1]
    ax.barh(y, values, height=0.55, color=color)
    xmax = max([h for h in his if h is not None] + values + [1]) * 1.18
    for yi, v, lo, hi in zip(y, values, los, his):
        if lo is not None:
            ax.plot([lo, hi], [yi, yi], color=C["text2"], linewidth=1.2)
        ax.text((hi if hi is not None else v) + 0.012 * xmax, yi, f"{v:.1f}%", va="center", fontsize=8.5, color=C["text"])
    ax.set_yticks(y)
    ax.set_yticklabels(labels, color=C["text"], fontsize=9)
    style(ax, title, xlabel)
    ax.set_xlim(0, xmax)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=200, facecolor=C["surface"])
    plt.close(fig)


def grouped_hbar(path, groups, series, data, title, xlabel):
    """data[series][group] = percent. Up to 4 series (palette slots 1-4, adjacent order)."""
    colors = [C["s1"], C["s2"], C["s3"], C["s4"]]
    fig, ax = plt.subplots(figsize=(8.5, 0.95 * len(groups) * len(series) / 2 + 1.6), facecolor=C["surface"])
    h = 0.8 / len(series)
    for gi, g in enumerate(groups):
        base = (len(groups) - 1 - gi)
        for si, s in enumerate(series):
            yv = base + 0.4 - h * (si + 0.5)
            v = data[s][g]
            ax.barh(yv, v, height=h * 0.86, color=colors[si], label=s if gi == 0 else None)
            ax.text(v + 0.4, yv, f"{v:.1f}%", va="center", fontsize=8, color=C["text"])
    ax.set_yticks(range(len(groups))[::-1])
    ax.set_yticklabels(groups, color=C["text"], fontsize=9)
    style(ax, title, xlabel)
    ax.set_xlim(0, max(max(d.values()) for d in data.values()) * 1.2 + 1)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, labelcolor=C["text2"])
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=200, facecolor=C["surface"])
    plt.close(fig)


def stacked_share(path, groups, parts, data, title, colors, xlabel="share of skills (%)"):
    """data[group][part] = count; 100% stacked horizontal bars with 2px surface gaps."""
    fig, ax = plt.subplots(figsize=(8.5, 0.6 * len(groups) + 1.7), facecolor=C["surface"])
    for gi, g in enumerate(groups):
        total = sum(data[g].values()) or 1
        left = 0
        yv = len(groups) - 1 - gi
        for pi, p in enumerate(parts):
            w = 100 * data[g].get(p, 0) / total
            ax.barh(yv, w, left=left, height=0.55, color=colors[pi], edgecolor=C["surface"], linewidth=2,
                    label=p if gi == 0 else None)
            if w >= 7:
                ax.text(left + w / 2, yv, f"{w:.0f}%", ha="center", va="center", fontsize=8,
                        color="white" if colors[pi] in (C["s1"], C["s2"]) else C["text"])
            left += w
    ax.set_yticks(range(len(groups))[::-1])
    ax.set_yticklabels(groups, color=C["text"], fontsize=9)
    style(ax, title, xlabel)
    ax.set_xlim(0, 100)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=len(parts), labelcolor=C["text2"])
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=200, facecolor=C["surface"])
    plt.close(fig)


# ---------------------------------------------------------------------- main --
def main():
    runs = [Path(p).resolve() for p in sys.argv[1:]]
    started = dt.datetime.now().astimezone()
    out = HERE / "consolidated" / f"{started:%Y-%m-%d_%H%M%S}_{len(runs)}runs"
    (out / "tables").mkdir(parents=True, exist_ok=False)
    (out / "figures").mkdir()

    sample = {r["skill_id"]: r for r in csv.DictReader(SAMPLE.open(encoding="utf-8"))}
    overlap = {r["skill_id"]: r for r in csv.DictReader(OVERLAP.open(encoding="utf-8"))}
    scans, findings, meta, sg_beh, sg_skill, sg_cov = [], [], {}, [], {}, []
    for run in runs:
        scans += list(csv.DictReader((run / "scan_summary.csv").open(encoding="utf-8")))
        findings += list(csv.DictReader((run / "individual_findings.csv").open(encoding="utf-8")))
        for m in run.glob("*/manifest.json"):
            meta[m.parent.name] = json.loads(m.read_text(encoding="utf-8"))
        sg = HERE / "skillguard" / run.name
        sg_beh += list(csv.DictReader((sg / "behaviors.csv").open(encoding="utf-8")))
        sg_skill.update({r["skill_id"]: r for r in csv.DictReader((sg / "per_skill.csv").open(encoding="utf-8"))})
        sg_cov += list(csv.DictReader((sg / "coverage.csv").open(encoding="utf-8")))
    skills = sorted({r["skill_id"] for r in scans})
    design = {s: (sample[s]["stratum"], int(sample[s]["population_N"]), int(sample[s]["sample_n"])) for s in skills}
    stratum_of = {s: design[s][0] for s in skills}
    status_of = defaultdict(dict)
    for r in scans:
        status_of[r["skill_id"]][r["configuration"]] = r["status"]
    primary = [s for s in skills if all(status_of[s].get(c) == "COMPLETE" for c in CONFIGS)]
    primary_set = set(primary)
    excluded = [s for s in skills if s not in primary_set]
    write_csv(out / "tables/scan_status_non_complete.csv",
              [{"skill_id": r["skill_id"], "stratum": stratum_of[r["skill_id"]], "configuration": r["configuration"],
                "status": r["status"], "status_detail": r["status_detail"], "findings_count": r["findings_count"],
                "frontmatter_valid": r["frontmatter_valid"]} for r in scans if r["status"] != "COMPLETE"])
    n_by = Counter(stratum_of.values())
    summary = {"runs": [str(r.relative_to(REPO)) for r in runs], "skills": len(skills), "skills_per_stratum": dict(n_by),
               "generated_at": started.isoformat(), "analysis_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

    def rate_rows(name, flags_by_skill, subset=None):
        subset = subset or primary
        flags = {s: int(bool(flags_by_skill.get(s))) for s in subset}
        row = {"measure": name, "n_skills": len(flags), "skills_flagged": sum(flags.values())}
        for st in STRATA:
            members = [s for s in flags if stratum_of[s] == st]
            k = sum(flags[s] for s in members)
            lo, hi = wilson(k, len(members))
            row.update({f"{st}_k": k, f"{st}_n": len(members), f"{st}_pct": pct(k / len(members)) if members else None,
                        f"{st}_ci95": [pct(lo), pct(hi)]})
        est, lo, hi = weighted(flags, design)
        row.update({"weighted_pct": pct(est), "weighted_ci95": [pct(lo), pct(hi)]})
        return row

    # 1. scan execution ------------------------------------------------------------------------
    walls = [float(r["wall_seconds"]) for r in scans if r["wall_seconds"]]
    summary["scans"] = {"total": len(scans), "statuses": dict(Counter(r["status"] for r in scans)),
                        "by_configuration": {c: dict(Counter(r["status"] for r in scans if r["configuration"] == c)) for c in CONFIGS},
                        "wall_seconds_mean": round(sum(walls) / len(walls), 3), "wall_hours_total": round(sum(walls) / 3600, 2),
                        "primary_analysis_set_skills": len(primary),
                        "primary_analysis_set_by_stratum": dict(Counter(stratum_of[s] for s in primary)),
                        "excluded_from_primary": {
                            "skills": len(excluded), "by_stratum": dict(Counter(stratum_of[s] for s in excluded)),
                            "frontmatter_partial_skills": sum(all(status_of[s].get(c) == "PARTIAL" for c in CONFIGS) for s in excluded),
                            "contract_only_skills": sum("CONTRACT_ONLY" in status_of[s].values() for s in excluded)}}

    # 2. coverage -------------------------------------------------------------------------------
    cov_rows = []
    for s in skills:
        m = meta.get(s, {})
        listing = bool(m.get("listing_complete"))
        complete = bool(m.get("folder_complete"))
        kind = "complete" if complete else ("truncated_listing" if not listing else "files_without_text")
        cov_rows.append({"skill_id": s, "stratum": stratum_of[s], "folder_coverage": kind,
                         "files_exported": len(m.get("supporting_files_written", [])) + 1,
                         "missing_files": len(m.get("missing_files", [])) if listing else "unknown",
                         "previously_examined": s in overlap,
                         "skillguard_files_code": sg_skill.get(s, {}).get("files_code_analyzed"),
                         "skillguard_files_text_only": sg_skill.get(s, {}).get("files_text_heuristic_only"),
                         "skillguard_files_not_analyzed": sg_skill.get(s, {}).get("files_not_analyzed")})
    write_csv(out / "tables/coverage_per_skill.csv", cov_rows)
    cov_kind = {st: Counter(r["folder_coverage"] for r in cov_rows if r["stratum"] == st) for st in STRATA}
    known_missing = sum(r["missing_files"] for r in cov_rows if r["missing_files"] not in ("unknown",))
    fmt = Counter()
    status_by_file = defaultdict(set)
    for r in sg_cov:
        status_by_file[(r["skill_id"], r["file"])].add(r["status"])
    tiers = Counter()
    for (s, f), st in status_by_file.items():
        tier = ("code" if st & {"analyzed", "analyzed_with_skipped_fences"} else
                "text_heuristic" if st & {"markdown_instructions_only", "disguised_text_scanned"} else "not_analyzed")
        tiers[(stratum_of.get(s), tier)] += 1
        if tier == "not_analyzed":
            fmt[Path(f).suffix.lower() or "(none)"] += 1
    cisco_cov = Counter(r["rule_id"] for r in findings if r["finding_kind"] == "scan_coverage")
    summary["coverage"] = {
        "folder_coverage_by_stratum": {st: dict(cov_kind[st]) for st in STRATA},
        "known_missing_files_total": known_missing,
        "truncated_listing_skills_missing_unknown": sum(r["folder_coverage"] == "truncated_listing" for r in cov_rows),
        "skillguard_file_tiers": {f"{a}|{b}": v for (a, b), v in sorted(tiers.items(), key=str)},
        "skillguard_not_analyzed_formats_top": dict(fmt.most_common(15)),
        "cisco_scan_coverage_rules": dict(cisco_cov.most_common()),
        "previously_examined_skills": sum(s in overlap for s in skills)}

    # 3. Cisco per configuration ----------------------------------------------------------------
    sec_all = [r for r in findings if r["finding_kind"] == "security"]
    sec = [r for r in sec_all if r["run_status"] == "COMPLETE" and r["skill_id"] in primary_set]
    by_cfg = defaultdict(lambda: defaultdict(list))
    for r in sec:
        by_cfg[r["configuration"]][r["skill_id"]].append(r)
    cfg_rows = []
    for c in CONFIGS:
        row = rate_rows(f"Cisco security finding: {c}", by_cfg[c])
        row["findings_total"] = sum(len(v) for v in by_cfg[c].values())
        cfg_rows.append(row)
    kinds = {k: rate_rows(f"Cisco {k} finding (any configuration, all executed scans, all skills)",
                          {s: 1 for s in {r['skill_id'] for r in findings if r['finding_kind'] == k}}, skills)
             for k in ("security", "metadata_quality", "scan_coverage")}
    write_csv(out / "tables/cisco_by_configuration.csv", cfg_rows + list(kinds.values()))

    # severity (max per skill, full folder union)
    sev_rows = []
    for scope in ("SKILL.md only", "Full folder"):
        maxsev = {}
        for r in sec:
            if r["scope"] == scope:
                cur = maxsev.get(r["skill_id"])
                if cur is None or SEV_ORDER.index(r["severity"]) < SEV_ORDER.index(cur):
                    maxsev[r["skill_id"]] = r["severity"]
        for sv in SEV_ORDER:
            sev_rows.append(dict(scope=scope, **rate_rows(f"max security severity = {sv}", {s: 1 for s, v in maxsev.items() if v == sv})))
    write_csv(out / "tables/cisco_max_severity.csv", sev_rows)

    # 4. SKILL.md-only vs full folder ------------------------------------------------------------
    def keys(scope, mode=None):
        k = defaultdict(set)
        for r in sec:
            if r["scope"] == scope and (mode is None or r["analyzer_mode"] == mode):
                k[r["skill_id"]].add((r["rule_id"], r["file_path"], r["reported_line_number"]))
        return k
    k_only, k_full = keys("SKILL.md only"), keys("Full folder")
    split = {st: Counter() for st in STRATA}
    scope_rows = []
    for s in primary:
        a, b = bool(k_only.get(s)), bool(k_full.get(s))
        cat = "both" if a and b else "full folder only" if b else "SKILL.md-only scan only" if a else "neither"
        split[stratum_of[s]][cat] += 1
        skill_md_full = {k for k in k_full.get(s, set()) if k[1] == "SKILL.md"}
        scope_rows.append({"skill_id": s, "stratum": stratum_of[s], "category": cat,
                           "skill_only_findings": len(k_only.get(s, ())), "full_folder_findings": len(k_full.get(s, ())),
                           "full_folder_findings_outside_SKILL_md": len([k for k in k_full.get(s, ()) if k[1] != "SKILL.md"]),
                           "SKILL_md_findings_identical_across_scopes": skill_md_full == k_only.get(s, set())})
    write_csv(out / "tables/skill_only_vs_full_per_skill.csv", scope_rows)
    summary["skill_only_vs_full"] = {
        "by_stratum": {st: dict(split[st]) for st in STRATA},
        "skills_with_findings_only_visible_in_full_folder": sum(r["category"] == "full folder only" for r in scope_rows),
        "full_folder_findings_outside_SKILL_md": sum(r["full_folder_findings_outside_SKILL_md"] for r in scope_rows),
        "skills_where_SKILL_md_findings_differ_between_scopes": sum(not r["SKILL_md_findings_identical_across_scopes"] for r in scope_rows)}
    # behavioral vs default (full folder)
    kd, kb = keys("Full folder", "default"), keys("Full folder", "behavioral")
    summary["default_vs_behavioral_full_folder"] = {
        "skills": len(primary),
        "skills_flagged_default": sum(bool(kd.get(s)) for s in primary), "skills_flagged_behavioral": sum(bool(kb.get(s)) for s in primary),
        "skills_flagged_only_with_behavioral": sum(bool(kb.get(s)) and not kd.get(s) for s in primary),
        "findings_only_in_behavioral": sum(len(kb.get(s, set()) - kd.get(s, set())) for s in primary)}

    # 5. Cisco categories / rules (full folder, modes unioned) ----------------------------------
    cat_skills, rule_skills, rule_rows_count = defaultdict(set), defaultdict(set), Counter()
    seen = set()
    for r in sec:
        if r["scope"] != "Full folder":
            continue
        key = (r["skill_id"], r["rule_id"], r["file_path"], r["reported_line_number"])
        if key in seen:
            continue
        seen.add(key)
        cat_skills[r["research_category"]].add(r["skill_id"])
        rule_skills[r["rule_id"]].add(r["skill_id"])
        rule_rows_count[r["rule_id"]] += 1
    cat_rows = sorted((rate_rows(c, {s: 1 for s in v}) for c, v in cat_skills.items()), key=lambda r: -r["weighted_pct"])
    write_csv(out / "tables/cisco_categories_full_folder.csv", cat_rows)
    rule_rows = sorted(({"rule_id": rid, "distinct_findings": rule_rows_count[rid], **rate_rows(rid, {s: 1 for s in v})}
                        for rid, v in rule_skills.items()), key=lambda r: -r["skills_flagged"])
    write_csv(out / "tables/cisco_rules_full_folder.csv", rule_rows)
    summary["cisco_distinct_security_findings_full_folder"] = len(seen)

    # 6. SkillGuard capabilities ------------------------------------------------------------------
    caps = sorted({b["capability"] for b in sg_beh})
    sg_rows = []
    for cap in caps:
        members = [b for b in sg_beh if b["capability"] == cap]
        row = rate_rows(cap, {b["skill_id"]: 1 for b in members}, skills)
        row.update({"behaviors": len(members), "evidence_levels": dict(Counter(b["evidence_level"] for b in members)),
                    "review_priority": dict(Counter(b["review_priority"] for b in members)),
                    "with_cisco_security_within_3_lines": sum(b["cisco_security_near"] not in ("[]", "") for b in members)})
        sg_rows.append(row)
    any_sg = rate_rows("any SkillGuard behavior", {b["skill_id"]: 1 for b in sg_beh}, skills)
    code_sg = rate_rows("any code/generated-code SkillGuard behavior",
                        {b["skill_id"]: 1 for b in sg_beh if b["evidence_level"] in ("code", "generated_code")}, skills)
    high_sg = rate_rows("any high-priority SkillGuard behavior", {b["skill_id"]: 1 for b in sg_beh if b["review_priority"] == "high"}, skills)
    sg_rows.sort(key=lambda r: -r["weighted_pct"])
    write_csv(out / "tables/skillguard_capabilities.csv", sg_rows + [any_sg, code_sg, high_sg])
    write_csv(out / "tables/skillguard_behaviors_all.csv", sg_beh)
    summary["skillguard"] = {"behaviors": len(sg_beh), "skills_with_behavior": any_sg["skills_flagged"],
                             "weighted_pct_any": any_sg["weighted_pct"], "weighted_ci95_any": any_sg["weighted_ci95"],
                             "by_capability": {r["measure"]: r["behaviors"] for r in sg_rows},
                             "evidence_levels": dict(Counter(b["evidence_level"] for b in sg_beh)),
                             "review_priority": dict(Counter(b["review_priority"] for b in sg_beh)),
                             "behaviors_with_cisco_security_within_3_lines": sum(b["cisco_security_near"] not in ("[]", "") for b in sg_beh)}

    # 7. skill-level relationship (descriptive, not accuracy) -------------------------------------
    sg_flag = {b["skill_id"] for b in sg_beh}
    cisco_flag = {s for s in primary if k_full.get(s)}
    table = Counter((s in sg_flag, s in cisco_flag) for s in primary)
    summary["skill_level_cooccurrence_full_folder"] = {
        "skillguard_and_cisco": table[(True, True)], "skillguard_only": table[(True, False)],
        "cisco_only": table[(False, True)], "neither": table[(False, False)],
        "skills": len(primary), "note": "Primary analysis set. Co-occurrence of a capability inventory and a security scanner's alerts; not agreement, recall or precision."}
    cats_in_sg = Counter(c for c, v in cat_skills.items() for s in v if s in sg_flag)
    summary["cisco_categories_in_skills_with_skillguard_behaviors"] = dict(cats_in_sg.most_common())

    # 8. sensitivity --------------------------------------------------------------------------------
    sens = []
    cisco_flag_all = {r["skill_id"] for r in sec_all if r["scope"] == "Full folder"}
    subsets = {"primary (all 4 scans COMPLETE)": primary,
               "primary, excluding_previously_examined": [s for s in primary if s not in overlap],
               "primary, complete_folders_only": [s for s in primary if meta.get(s, {}).get("folder_complete")],
               "primary, excluding_previously_examined, complete_folders_only":
                   [s for s in primary if s not in overlap and meta.get(s, {}).get("folder_complete")]}
    for label, subset in subsets.items():
        sens.append({"subset": label, **rate_rows("Cisco security (full folder)", {s: 1 for s in cisco_flag}, subset)})
        sens.append({"subset": label, **rate_rows("SkillGuard any behavior", {s: 1 for s in sg_flag}, subset)})
    sens.append({"subset": "all skills, all executed scans (incl. PARTIAL/CONTRACT_ONLY findings)",
                 **rate_rows("Cisco security (full folder)", {s: 1 for s in cisco_flag_all}, skills)})
    sens.append({"subset": "all skills", **rate_rows("SkillGuard any behavior", {s: 1 for s in sg_flag}, skills)})
    write_csv(out / "tables/sensitivity.csv", sens)

    # 9. figures ----------------------------------------------------------------------------------
    labels = [STRATUM_LABEL[s] for s in STRATA]
    grouped_hbar(out / "figures/fig1_cisco_flag_rate_by_configuration.png", labels, CONFIGS,
                 {c: {STRATUM_LABEL[st]: next(r for r in cfg_rows if r["measure"].endswith(c))[f"{st}_pct"] or 0 for st in STRATA} for c in CONFIGS},
                 "Skills with ≥1 Cisco security finding, by scan configuration", "share of sampled skills in stratum (%)")
    parts = ["full folder only", "both", "SKILL.md-only scan only", "neither"]
    stacked_share(out / "figures/fig2_skill_only_vs_full_folder.png", labels, parts,
                  {STRATUM_LABEL[st]: split[st] for st in STRATA},
                  "Where Cisco security findings appear: SKILL.md-only vs full-folder scan",
                  [C["s1"], C["s2"], C["s4"], C["grid"]])
    top = cat_rows[:10]
    if top:
        hbar_ci(out / "figures/fig3_cisco_categories_weighted.png", [r["measure"] for r in top], [r["weighted_pct"] for r in top],
                [r["weighted_ci95"][0] for r in top], [r["weighted_ci95"][1] for r in top],
                "Cisco security categories (full folder): weighted share of skills", "estimated share of skills in frame (%), 95% CI")
    if sg_rows:
        hbar_ci(out / "figures/fig4_skillguard_capabilities_weighted.png", [r["measure"] for r in sg_rows], [r["weighted_pct"] for r in sg_rows],
                [r["weighted_ci95"][0] for r in sg_rows], [r["weighted_ci95"][1] for r in sg_rows],
                "SkillGuard capabilities: weighted share of skills (a capability, not a vulnerability)",
                "estimated share of skills in frame (%), 95% CI", color=C["s3"])
    tier_parts = ["code", "text_heuristic", "not_analyzed"]
    stacked_share(out / "figures/fig5_skillguard_file_coverage.png", labels[:2], tier_parts,
                  {STRATUM_LABEL[st]: {t: tiers[(st, t)] for t in tier_parts} for st in STRATA[:2]},
                  "SkillGuard file coverage (all exported files incl. SKILL.md)", [C["s1"], C["s3"], C["grid"]],
                  xlabel="share of exported files (%)")
    folder_parts = ["complete", "files_without_text", "truncated_listing"]
    stacked_share(out / "figures/fig6_folder_completeness.png", labels, folder_parts,
                  {STRATUM_LABEL[st]: cov_kind[st] for st in STRATA},
                  "Folder completeness in the snapshot (truncated listing: missing-file count unknown)",
                  [C["s1"], C["s4"], C["s2"]])

    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("wrote", out.relative_to(REPO))


if __name__ == "__main__":
    main()
