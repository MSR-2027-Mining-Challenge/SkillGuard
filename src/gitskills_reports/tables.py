"""The research tables of a report, computed from a loaded Source (and its Review, if any). Pure pandas, no I/O."""

import json

import pandas as pd

from .model import OUTCOME_ORDER, SEVERITY_ORDER, TIER_LABELS, TIER_ORDER, analyzer_info, sha256_of


def severity_rank(sev):
    return SEVERITY_ORDER.index(sev) if sev in SEVERITY_ORDER else len(SEVERITY_ORDER)


def max_severity(values):
    values = [v for v in values if isinstance(v, str)]
    return min(values, key=severity_rank) if values else None


def join_unique(values, sep="; "):
    seen = []
    for v in values:
        if pd.notna(v) and str(v) not in seen:
            seen.append(str(v))
    return sep.join(seen)


def config_order(source):
    return [c["configuration"] for c in source.configurations]


# ---------------------------------------------------------------- coverage

def coverage_by_configuration(source):
    rows = []
    scans = source.scans
    for cfg in source.configurations + [{"configuration": "All configurations"}]:
        name = cfg["configuration"]
        part = scans if name == "All configurations" else scans[scans["configuration"] == name]
        counts = part["outcome"].value_counts()
        planned = len(part)
        row = {"configuration": name, "scope": cfg.get("scope", ""), "analyzer_mode": cfg.get("analyzer_mode", ""),
               "planned": planned, "executed": int(part["scan_executed"].sum()) if planned else 0}
        row.update({o: int(counts.get(o, 0)) for o in OUTCOME_ORDER})
        row["complete_pct_of_planned"] = round(100 * row["complete"] / planned, 1) if planned else None
        rows.append(row)
    return pd.DataFrame(rows)


SKILL_COVERAGE = {
    "complete": "every planned configuration produced a COMPLETE scan",
    "complete_except_excluded": "every executed configuration is COMPLETE; full-folder scans were excluded by design "
                                "because GitSkills did not store every supporting file",
    "partially_complete": "some configurations are COMPLETE, others are partial, contract-only or failed",
    "no_complete_scan": "Cisco ran, but no configuration produced a COMPLETE scan",
    "not_scanned": "no scan was executed (export error or missing reports)",
}


def skill_coverage(scans):
    def classify(group):
        outcomes = group["outcome"]
        complete, executed = int((outcomes == "complete").sum()), int(group["scan_executed"].sum())
        if executed == 0:
            return "not_scanned"
        if complete == len(group):
            return "complete"
        if complete == executed:
            return "complete_except_excluded"
        return "partially_complete" if complete else "no_complete_scan"
    return scans.groupby("skill_id", sort=False).apply(classify, include_groups=False).rename("coverage")


def run_counts(source):
    """The headline numbers START_HERE and the dashboard both print (one definition, used twice)."""
    meta, scans, findings = source.metadata, source.scans, source.findings
    skill_ids = list(dict.fromkeys(scans["skill_id"])) if not scans.empty else []
    selected = len(meta.get("selection") or []) or (meta.get("sample") or {}).get("skills") or len(skill_ids)
    exported = len(meta.get("skills") or []) or len(skill_ids)
    coverage = skill_coverage(scans) if not scans.empty else pd.Series(dtype=str)
    security = findings[findings["finding_kind"] == "security"] if not findings.empty else findings
    primary_sec = security[security["run_outcome"] == "complete"] if not security.empty else security
    outcomes = scans["outcome"].value_counts() if not scans.empty else pd.Series(dtype=int)
    return {
        "skills_selected": int(selected),
        "skills_exported": int(exported),
        "export_errors": len(meta.get("export_errors") or []),
        "skills_scanned": int(scans.groupby("skill_id")["scan_executed"].any().sum()) if not scans.empty else 0,
        "skills_by_coverage": {k: int((coverage == k).sum()) for k in SKILL_COVERAGE},
        "configurations": len(source.configurations),
        "scans_planned": len(scans),
        "scans_executed": int(scans["scan_executed"].sum()) if not scans.empty else 0,
        "scans_by_outcome": {o: int(outcomes.get(o, 0)) for o in OUTCOME_ORDER},
        "finding_rows": len(findings),
        "finding_rows_by_kind": findings["finding_kind"].value_counts().to_dict() if not findings.empty else {},
        "skills_with_any_finding": int(findings["skill_id"].nunique()) if not findings.empty else 0,
        "skills_with_security_alert_primary": int(primary_sec["skill_id"].nunique()) if not primary_sec.empty else 0,
        "skills_with_security_alert_any": int(security["skill_id"].nunique()) if not security.empty else 0,
        "security_rows_primary": len(primary_sec),
        "security_rows_any": len(security),
        "security_locations_primary": int(primary_sec.groupby(["skill_id", "location_key"]).ngroups) if not primary_sec.empty else 0,
        "security_locations_any": int(security.groupby(["skill_id", "location_key"]).ngroups) if not security.empty else 0,
        "security_rows_by_severity_primary": {s: int(n) for s, n in sorted(primary_sec["severity"].value_counts().items(),
                                                                         key=lambda kv: severity_rank(kv[0]))} if not primary_sec.empty else {},
    }


# ---------------------------------------------------------------- findings and validation

def review_lookup(source, review):
    """(skill_id, finding_id) -> review_id, from the run's manual_review_template.csv."""
    lookup = {}
    template = source.template
    if template.empty or "cisco_finding_ids" not in template:
        return lookup
    for row in template.itertuples():
        for fid in str(row.cisco_finding_ids).split(";"):
            if fid.strip():
                lookup[(row.skill_id, fid.strip())] = row.review_id
    return lookup


def annotate_findings(source, review):
    """individual findings + review_id, validation_tier and review labels (security findings only get a tier)."""
    findings = source.findings.copy()
    if findings.empty:
        return findings
    lookup = review_lookup(source, review)
    findings["review_id"] = [lookup.get((s, f)) for s, f in zip(findings["skill_id"], findings["finding_id"])]
    items = review.items.set_index("review_id") if review is not None else pd.DataFrame()

    def tier(row):
        if row.finding_kind != "security":
            return None
        if pd.isna(row.review_id):
            return "not_in_review"
        if review is None or row.review_id not in items.index:
            return "awaiting_review"
        return items.at[row.review_id, "validation_tier"]
    findings["validation_tier"] = [tier(r) for r in findings.itertuples()]
    for col in ("provisional_label", "final_label", "suggested_interpretation", "behavior_group"):
        findings[col] = [items.at[r, col] if review is not None and r in items.index and col in items else None
                         for r in findings["review_id"]]
    return findings


def key_security_findings(annotated, source):
    sec = annotated[annotated["finding_kind"] == "security"]
    if sec.empty:
        return pd.DataFrame()
    order = config_order(source)
    rows = []
    for (skill, loc), g in sec.groupby(["skill_id", "location_key"], sort=False):
        g = g.sort_values("configuration", key=lambda s: s.map(lambda c: order.index(c) if c in order else 99))
        first = g.iloc[0]
        rows.append({
            "skill_id": skill, "repo": first["repo"], "skill_path": first["skill_path"],
            "rule_id": first["rule_id"], "severity": max_severity(g["severity"]), "cisco_category": first["cisco_category"],
            "research_category": first.get("research_category"), "analyzers": join_unique(g["analyzer"]),
            "file_path": first["file_path"], "reported_line_number": first["reported_line_number"],
            "evidence_status": join_unique(g["evidence_status"]), "configurations": join_unique(g["configuration"]),
            "run_outcomes": join_unique(g["run_outcome"]), "in_primary_analysis": bool((g["run_outcome"] == "complete").any()),
            "title": first["title"], "snippet": first["snippet"], "finding_ids": join_unique(g["finding_id"]),
            "review_id": first["review_id"], "validation_tier": first["validation_tier"],
            "validation_tier_label": TIER_LABELS.get(first["validation_tier"], ""),
            "behavior_group": first["behavior_group"], "suggested_interpretation": first["suggested_interpretation"],
            "provisional_label": first["provisional_label"], "final_label": first["final_label"], "location_key": loc,
        })
    out = pd.DataFrame(rows)
    out["reported_line_number"] = pd.to_numeric(out["reported_line_number"], errors="coerce").astype("Int64")
    out["_sev"] = out["severity"].map(severity_rank)
    return out.sort_values(["_sev", "skill_id", "rule_id"]).drop(columns="_sev").reset_index(drop=True)


def severity_by_configuration(source):
    f = source.findings
    sec = f[(f["finding_kind"] == "security") & (f["run_outcome"] == "complete")] if not f.empty else f
    present = set(sec["severity"]) if not sec.empty else set()
    sevs = SEVERITY_ORDER + sorted(present - set(SEVERITY_ORDER))     # fixed columns, so runs line up
    rows = []
    for name in config_order(source):
        part = sec[sec["configuration"] == name] if not sec.empty else sec
        row = {"configuration": name, "analyzer_mode": next(c.get("analyzer_mode") for c in source.configurations if c["configuration"] == name)}
        row.update({s: int((part["severity"] == s).sum()) if not part.empty else 0 for s in sevs})
        row["security_rows"] = len(part)
        row["distinct_locations"] = int(part.groupby(["skill_id", "location_key"]).ngroups) if not part.empty else 0
        row["skills_with_alerts"] = int(part["skill_id"].nunique()) if not part.empty else 0
        rows.append(row)
    return pd.DataFrame(rows)


def rule_breakdown(source):
    f = source.findings
    if f.empty:
        return pd.DataFrame()
    rows = []
    for (rule, kind), g in f.groupby(["rule_id", "finding_kind"]):
        prim = g[g["run_outcome"] == "complete"]
        rows.append({"rule_id": rule, "finding_kind": kind, "cisco_category": join_unique(g["cisco_category"]),
                     "research_category": join_unique(g.get("research_category", pd.Series(dtype=str))),
                     "analyzers": join_unique(g["analyzer"]), "max_severity": max_severity(g["severity"]),
                     "rows_primary": len(prim), "rows_all_readable_scans": len(g),
                     "skills_primary": int(prim["skill_id"].nunique()), "skills_all": int(g["skill_id"].nunique()),
                     "distinct_locations_primary": int(prim.groupby(["skill_id", "location_key"]).ngroups) if not prim.empty else 0,
                     "configurations": join_unique(g["configuration"])})
    out = pd.DataFrame(rows)
    out["_k"] = out["finding_kind"].ne("security")
    return out.sort_values(["_k", "rows_primary", "rule_id"], ascending=[True, False, True]).drop(columns="_k").reset_index(drop=True)


def analyzer_breakdown(source):
    """Security rows per Cisco analyzer and configuration: where a new analyzer (LLM, meta) adds or removes alerts."""
    f = source.findings
    sec = f[(f["finding_kind"] == "security") & (f["run_outcome"] == "complete")] if not f.empty else f
    if sec.empty:
        return pd.DataFrame(columns=["configuration", "analyzer", "security_rows", "skills"])
    return (sec.groupby(["configuration", "analyzer"]).agg(security_rows=("finding_id", "size"), skills=("skill_id", "nunique"))
               .reset_index())


def comparison_summary(source):
    c = source.comparisons
    if c.empty or "comparison" not in c:
        return pd.DataFrame()
    c = c.assign(kind=c["finding_kind"].where(c["finding_kind"] == "security", "metadata / coverage"))
    out = (c.groupby(["comparison", "kind", "pair_status", "change"]).agg(rows=("finding_id", "size"), skills=("skill_id", "nunique"))
            .reset_index())
    return out.sort_values(["comparison", "kind", "pair_status", "change"]).reset_index(drop=True)


def skills_index(source, annotated, detail_pages):
    scans = source.scans
    coverage = skill_coverage(scans)
    meta_skills = {s["skill_id"]: s for s in (source.metadata.get("skills") or []) if isinstance(s, dict)}
    rows = []
    for skill, g in scans.groupby("skill_id", sort=False):
        f = annotated[annotated["skill_id"] == skill] if not annotated.empty else annotated
        sec = f[f["finding_kind"] == "security"] if not f.empty else f
        prim = sec[sec["run_outcome"] == "complete"] if not sec.empty else sec
        info = meta_skills.get(skill, {})
        rows.append({
            "skill_id": skill, "repo": g["repo"].iloc[0], "skill_path": g["skill_path"].iloc[0],
            "sample_stratum": g["sample_stratum"].iloc[0] if "sample_stratum" in g else None,
            "folder_complete": info.get("folder_complete", g["folder_complete"].iloc[0] if "folder_complete" in g else None),
            "supporting_files_exported": info.get("supporting_files_exported"),
            "coverage": coverage.get(skill), "complete_scans": int((g["outcome"] == "complete").sum()), "planned_scans": len(g),
            "scan_statuses": join_unique(g["status"]),
            "security_rows_primary": len(prim), "security_locations_any": int(sec.groupby("location_key").ngroups) if not sec.empty else 0,
            "max_security_severity": max_severity(sec["severity"]) if not sec.empty else None,
            "metadata_quality_rows": int((f["finding_kind"] == "metadata_quality").sum()) if not f.empty else 0,
            "scan_coverage_rows": int((f["finding_kind"] == "scan_coverage").sum()) if not f.empty else 0,
            "review_items": int(sec["review_id"].dropna().nunique()) if not sec.empty else 0,
            "human_validated_items": int(sec.loc[sec["validation_tier"] == "human_validated", "review_id"].nunique()) if not sec.empty else 0,
            "detail_page": detail_pages.get(skill),
        })
    return pd.DataFrame(rows)


def validation_counts(key_findings, review):
    tiers = key_findings["validation_tier"].value_counts() if not key_findings.empty else pd.Series(dtype=int)
    counts = {"locations_by_tier": {t: int(tiers.get(t, 0)) for t in TIER_ORDER},
              "review_items": len(review.items) if review is not None else 0,
              "review_items_by_tier": {t: int((review.items["validation_tier"] == t).sum()) for t in TIER_ORDER} if review is not None else {},
              "provisional_labels": review.items["provisional_label"].value_counts().to_dict()
              if review is not None and "provisional_label" in review.items else {},
              "final_labels": review.items["final_label"].dropna().value_counts().to_dict()
              if review is not None and "final_label" in review.items else {}}
    return counts


def raw_report_index(run_dir, configurations, scans, portable):
    """One row per skill x configuration report file, with the hash re-computed from disk (nothing is copied)."""
    rows = []
    by_key = {(r.skill_id, r.configuration): r for r in scans.itertuples()} if not scans.empty else {}
    for manifest in sorted(run_dir.glob("*/manifest.json")):
        skill_dir = manifest.parent
        try:
            files = json.loads(manifest.read_text(encoding="utf-8")).get("files") or []
        except json.JSONDecodeError:
            files = []
        for cfg in configurations:
            report_name = cfg.get("report_file")
            if not report_name:
                continue
            report = skill_dir / "reports" / report_name
            record = report.with_name(report.stem + ".run.json")
            scan = by_key.get((skill_dir.name, cfg["configuration"]))
            rec = {}
            if record.is_file():
                try:
                    rec = json.loads(record.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    rec = {"status": "unreadable run record"}
            actual = sha256_of(report) if report.is_file() else None
            recorded = getattr(scan, "report_sha256", None) if scan is not None else None
            recorded = recorded if isinstance(recorded, str) else rec.get("report_sha256")
            rows.append({
                "skill_id": skill_dir.name, "configuration": cfg["configuration"], "analyzer_mode": cfg.get("analyzer_mode"),
                "status": getattr(scan, "status", None), "report_file": portable.path(report), "report_exists": report.is_file(),
                "report_bytes": report.stat().st_size if report.is_file() else None, "report_sha256": actual,
                "recorded_sha256": recorded, "sha256_matches_record": (actual == recorded) if actual and recorded else None,
                "run_record_file": portable.path(record) if record.is_file() else None,
                "exit_code": rec.get("exit_code"), "wall_seconds": rec.get("wall_seconds"), "started_at": rec.get("started_at"),
                "scanner_version": rec.get("scanner_version"), "stderr_tail": (rec.get("stderr_tail") or "")[:300] or None,
                "stdout_dump": portable.path(report.with_name(report.stem + ".stdout.txt")) if report.with_name(report.stem + ".stdout.txt").is_file() else None,
                "exported_files": len(files),
            })
    return pd.DataFrame(rows)


def config_table(source):
    rows = []
    for c in source.configurations:
        info = analyzer_info(c.get("analyzer_mode"))
        rows.append({"configuration": c["configuration"], "scope": c.get("scope"), "analyzer_mode": c.get("analyzer_mode"),
                     "analyzer": info["label"], "deterministic": info["deterministic"], "about": info["about"]})
    return pd.DataFrame(rows)
