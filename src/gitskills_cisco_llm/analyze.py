"""Analysis of an LLM/Meta run folder: notebook-01-shaped scan/finding tables plus the LLM/Meta comparison tables.

Writes into the run folder (never into the source run):
    scan_summary.csv, individual_findings.csv     same columns as notebook 01, plus LLM/Meta provenance columns
    llm_comparison.csv, meta_comparison.csv       finding-level comparisons in the *_comparison.csv shape the reports read
    llm_meta_analysis/*.csv                       the comparison tables listed in TABLES below
    run_metadata.json, results_summary.md
and then rebuilds the report under results/reports/ with gitskills_reports.

Units: a "scan" is one skill x configuration; a "finding row" is one Cisco finding in one scan; an "alert" is a
deduplicated security finding (deterministic: rule + file + line; LLM: research category + file, because LLM findings
carry no stable rule ID or line). Scanner alerts are candidates, never confirmed vulnerabilities.
"""

import json
import math
import random
from pathlib import Path

import pandas as pd

from . import rules
from .experiment import BASELINE_CONFIGS, NEW_MODES, PRICES_PER_MTOK, Experiment, new_configs, scope_folder
from .runner import assess_llm_meta, now_utc, read_csv, run_record_path, sha256_file, write_json

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
READABLE = ("COMPLETE", "CONTRACT_ONLY", "PARTIAL")
META_OK = ("ran", "skipped_clear_deterministic", "not_invoked_no_findings")
NON_DETECTION_ANALYZERS = ("llm", "meta")          # everything else is a deterministic Cisco analyzer
SHORT = {"default": "A_static", "behavioral": "A_behavioral", "behavioral_llm": "B_llm",
         "behavioral_meta": "Cdet_meta", "behavioral_llm_meta": "C_llm_meta"}
REFERENCE_PAID_MODEL = "claude-sonnet-5-5"          # Cisco 2.3.1's DEFAULT_LLM_MODEL
TRIAGE_SEED = 2027
TRIAGE_CAP_PER_BUCKET = 10

SCAN_COLUMNS = ["skill_id", "repo", "skill_path", "sample_stratum", "configuration", "scope", "analyzer_mode", "status", "outcome",
                "status_detail", "analyzer_failure_count", "analyzer_failure_types", "analyzers_failed", "rule_contract_status",
                "required_analyzers", "analyzers_used", "exit_code", "wall_seconds", "scan_seconds", "is_safe", "max_severity",
                "findings_count", "folder_complete", "files_missing", "frontmatter_valid", "policy_name", "policy_preset",
                "policy_fingerprint", "scanner_version", "scanner_version_source", "report_timestamp", "report_sha256",
                "report_file",
                # LLM / Meta provenance (not in notebook 01)
                "result_origin", "core_status", "llm_model", "llm_status", "llm_error_type", "llm_findings",
                "llm_budget_exceeded_items", "meta_status", "meta_false_positives", "meta_missed_threats_added",
                "meta_risk_level", "meta_delta", "input_tokens", "output_tokens", "total_tokens", "cost_usd", "attempts"]
TABLES = {
    "coverage_by_configuration": "Planned / executed / complete / partial / failed / excluded scans, LLM and Meta status",
    "findings_by_configuration": "Security finding rows and skills with alerts per configuration (primary scans)",
    "deterministic_reproducibility": "Do static/behavioral findings stay identical when LLM / Meta are switched on?",
    "llm_added_findings": "Every LLM-analyzer security finding (B), with corroboration by deterministic alerts",
    "llm_view_of_deterministic_alerts": "For each deterministic alert: did the LLM report the same file + category?",
    "meta_decisions": "Every finding Meta saw (C-det, C): retained / suppressed / unreviewed / added",
    "meta_decision_summary": "Meta decision counts by configuration and finding kind",
    "severity_changes": "Same alert, different severity across configurations / LLM runs",
    "category_by_configuration": "Research category x configuration (security rows, primary scans)",
    "unique_by_configuration": "Alerts by the set of configurations that report them",
    "runtime_and_cost": "Wall time, tokens and cost per configuration (+ the same tokens priced at Claude Sonnet 5.5)",
    "llm_run_stability": "LLM findings in B vs the LLM part of C: same input, same settings, two runs",
    "alert_groups": "Deduplicated alert groups (skill + file + research category) across configurations; raw rows kept",
    "triage_queue": "Candidates for targeted manual investigation (bucketed, seeded sample per bucket)",
    "case_studies": "The 11 manually inspected findings (provisional labels) vs LLM and Meta behaviour",
}


def _all_configs(experiment):
    out = {c["configuration"]: {**c, "uses_llm": False, "uses_meta": False} for c in BASELINE_CONFIGS}
    out.update({c["configuration"]: c for c in new_configs(experiment.modes)})
    return out


def _sev_rank(sev):
    return SEVERITY_ORDER.index(sev) if sev in SEVERITY_ORDER else len(SEVERITY_ORDER)


# ---------------------------------------------------------------- scans and findings

def load_tables(run_dir):
    run_dir = Path(run_dir)
    spec = json.loads((run_dir / "experiment.json").read_text(encoding="utf-8"))
    experiment = Experiment.from_json(spec["experiment"])
    configs = _all_configs(experiment)
    plan = read_csv(run_dir / "plan.csv")
    scans, findings = [], []
    for row in plan:
        cfg = configs[row["configuration"]]
        skill_dir = run_dir / row["skill_id"]
        manifest = json.loads((skill_dir / "manifest.json").read_text(encoding="utf-8")) if (skill_dir / "manifest.json").is_file() else {}
        scan = {k: row[k] for k in ("skill_id", "repo", "skill_path", "sample_stratum", "configuration", "scope", "analyzer_mode",
                                    "report_file")}
        scan.update(folder_complete=manifest.get("folder_complete"), files_missing=len(manifest.get("missing_files") or []),
                    frontmatter_valid=manifest.get("frontmatter_valid"), required_analyzers="|".join(cfg["required_analyzers"]),
                    result_origin={"reuse": "baseline (copied)", "scan": "new scan", "exclude": "not scanned"}[row["action"]])
        report_path = skill_dir / "reports" / row["report_file"]
        record_path = run_record_path(report_path)
        record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.is_file() else {}
        if row["action"] == "exclude":
            scan.update(status=row["reason"].split(":")[0], status_detail=row["reason"])
        elif not report_path.is_file():
            pending = row["action"] == "scan" and not record
            scan.update(status="MISSING_REPORT" if not record else record.get("status"),
                        status_detail="not run yet (or interrupted before finishing)" if pending else
                        "; ".join(record.get("status_reasons") or []) or "report missing")
            scan.update(_record_fields(record))
        else:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            core_status, core_reasons, failures = rules.assess_report(report, cfg, record.get("exit_code"))
            llm, meta, meta_reasons, _ = assess_llm_meta(report, cfg, record.get("stderr_tail") or "")
            if row["action"] == "scan":
                status, reasons = record.get("status"), record.get("status_reasons") or []
                llm, meta = record.get("llm") or llm, record.get("meta") or meta
            else:
                status, reasons = core_status, core_reasons
            sm = report.get("scan_metadata") or {}
            scan.update(
                status=status, core_status=core_status,
                status_detail="; ".join(reasons) or f"exit code {record.get('exit_code')}",
                analyzer_failure_count=len(failures), analyzer_failure_types="|".join(sorted({f["type"] for f in failures})),
                analyzers_failed=json.dumps(failures) if failures else "", rule_contract_status=(sm.get("rule_contract") or {}).get("status"),
                analyzers_used="|".join(report.get("analyzers_used") or []), scan_seconds=report.get("scan_duration_seconds"),
                is_safe=report.get("is_safe"), max_severity=report.get("max_severity"), findings_count=len(report.get("findings") or []),
                policy_name=sm.get("policy_name"), policy_preset=sm.get("policy_preset_base"),
                policy_fingerprint=sm.get("policy_fingerprint_sha256"), scanner_version_source="run record",
                report_timestamp=report.get("timestamp"), report_sha256=sha256_file(report_path),
                llm_status=llm.get("status"), llm_error_type=llm.get("error_type"), llm_findings=llm.get("findings"),
                llm_budget_exceeded_items=llm.get("budget_exceeded_items"), meta_status=meta.get("status"),
                meta_false_positives=meta.get("false_positives"), meta_missed_threats_added=meta.get("missed_threats_added"),
                meta_risk_level=meta.get("risk_level"), meta_delta=meta.get("meta_delta"))
            scan.update(_record_fields(record))
            usage = report.get("llm_usage") or {}
            scan.update(input_tokens=usage.get("input_tokens"), output_tokens=usage.get("output_tokens"),
                        total_tokens=usage.get("total_tokens"))
            if status in READABLE:
                run = {**scan, "status": status, "outcome": rules.outcome_of(status)}
                folder = skill_dir / scope_folder(row["scope"])
                findings.extend(rules.flatten_findings(report, run, folder))
        scan["outcome"] = rules.outcome_of(scan["status"])
        scans.append(scan)
    scans = pd.DataFrame(scans).reindex(columns=SCAN_COLUMNS)
    findings = pd.DataFrame(findings, columns=rules.FINDING_COLUMNS + rules.LLM_META_COLUMNS)
    if not findings.empty:
        findings["reported_line_number"] = findings["reported_line_number"].astype("Int64")
    return experiment, spec, scans, findings


def _record_fields(record):
    return {"exit_code": record.get("exit_code"), "wall_seconds": record.get("wall_seconds"),
            "scanner_version": record.get("scanner_version"), "llm_model": record.get("llm_model"),
            "cost_usd": record.get("cost_usd"), "attempts": len(record.get("attempts") or []) or (1 if record else None)}


# ---------------------------------------------------------------- helpers for the comparisons

def _alert_key(f):
    """Deterministic: Cisco rule + file + line. LLM / Meta: analyzer + research category + file (no stable rule/line)."""
    if f["analyzer"] in NON_DETECTION_ANALYZERS:
        return f"{f['analyzer'].upper()}|{f['research_category']}|{f['file_path']}"
    return f["location_key"]


def _primary_scans(scans):
    """Scans whose static/behavioral/LLM core is COMPLETE (CONTRACT_ONLY is a sensitivity tier, as in notebook 01)."""
    ok = scans["core_status"].eq("COMPLETE")
    llm_needed = scans["analyzer_mode"].isin([m for m, s in NEW_MODES.items() if s["uses_llm"]])
    ok &= ~llm_needed | scans["llm_status"].eq("ok")
    return scans[ok]


def _security(findings):
    return findings[findings["finding_kind"].eq("security")]


def _pair_frame(scans, mode_a, mode_b):
    """(skill, scope) pairs where both configurations have a primary scan; returns the pair keys."""
    prim = _primary_scans(scans)
    a = prim[prim["analyzer_mode"].eq(mode_a)][["skill_id", "scope"]]
    b = prim[prim["analyzer_mode"].eq(mode_b)][["skill_id", "scope"]]
    return a.merge(b, on=["skill_id", "scope"])


def _in_pairs(findings, pairs, mode):
    part = findings[findings["analyzer_mode"].eq(mode)]
    return part.merge(pairs, on=["skill_id", "scope"])


# ---------------------------------------------------------------- the comparison tables

def coverage_by_configuration(scans):
    rows = []
    for (cfg, mode), part in scans.groupby(["configuration", "analyzer_mode"], sort=False):
        outcome = part["outcome"].value_counts()
        row = {"configuration": cfg, "analyzer_mode": mode, "label": SHORT.get(mode, mode), "planned": len(part),
               "excluded_incomplete_folder": int(part["status"].eq("SKIPPED_INCOMPLETE_FOLDER").sum()),
               "export_error": int(part["status"].eq("EXPORT_ERROR").sum()),
               "not_run_or_missing": int(part["status"].eq("MISSING_REPORT").sum())}
        row["executed"] = row["planned"] - row["excluded_incomplete_folder"] - row["export_error"] - row["not_run_or_missing"]
        for o in ("complete", "contract_only", "partial", "failed"):
            row[o] = int(outcome.get(o, 0))
        row["primary_core_complete"] = int(len(_primary_scans(part)))
        if NEW_MODES.get(mode, {}).get("uses_llm"):
            llm = part["llm_status"].value_counts()
            row.update(llm_ok=int(llm.get("ok", 0)), llm_failed=int(llm.get("failed", 0)),
                       llm_not_queried=int(llm.get("not_queried_delimiter_injection", 0)),
                       llm_prompt_budget_exceeded=int(part["llm_budget_exceeded_items"].fillna(0).gt(0).sum()))
        if NEW_MODES.get(mode, {}).get("uses_meta"):
            meta = part["meta_status"].value_counts()
            row.update({f"meta_{k}": int(meta.get(k, 0)) for k in
                        ("ran", "skipped_clear_deterministic", "not_invoked_no_findings", "degraded", "failed")})
        row["denominator_note"] = (f"{row['executed']} executed of {row['planned']} planned; "
                                   f"{row['excluded_incomplete_folder']} excluded by design (incomplete folder)")
        rows.append(row)
    return pd.DataFrame(rows)


def findings_by_configuration(scans, findings):
    prim = _primary_scans(scans)
    rows = []
    for (cfg, mode), part in prim.groupby(["configuration", "analyzer_mode"], sort=False):
        f = findings.merge(part[["skill_id", "configuration"]], on=["skill_id", "configuration"])
        sec = _security(f)
        visible = sec[sec["post_meta_visible"]]
        row = {"configuration": cfg, "label": SHORT.get(mode, mode), "primary_scans": len(part),
               "security_rows_raw": len(sec), "security_rows_after_meta": len(visible),
               "security_rows_deterministic": int((~sec["analyzer"].isin(NON_DETECTION_ANALYZERS)).sum()),
               "security_rows_llm": int(sec["analyzer"].eq("llm").sum()), "security_rows_meta_added": int(sec["analyzer"].eq("meta").sum()),
               "skills_with_security_alert": sec["skill_id"].nunique(),
               "skills_with_security_alert_after_meta": visible["skill_id"].nunique(),
               "pct_scans_with_security_alert": round(100 * sec["skill_id"].nunique() / len(part), 1) if len(part) else None}
        for sev in SEVERITY_ORDER[:4]:
            row[f"{sev.lower()}_rows"] = int(sec["severity"].eq(sev).sum())
        rows.append(row)
    return pd.DataFrame(rows)


def deterministic_reproducibility(scans, findings):
    rows = []
    for mode in [m for m in NEW_MODES if m in set(scans["analyzer_mode"])]:
        pairs = _pair_frame(scans, "behavioral", mode)
        for pair in pairs.itertuples(index=False):
            def keys(m):
                part = findings[(findings["skill_id"] == pair.skill_id) & (findings["scope"] == pair.scope)
                                & findings["analyzer_mode"].eq(m) & ~findings["analyzer"].isin(NON_DETECTION_ANALYZERS)]
                return sorted(part["finding_key"] + "|" + part["severity"].astype(str))
            base, new = keys("behavioral"), keys(mode)
            rows.append({"comparison": f"A_behavioral -> {SHORT[mode]}", "skill_id": pair.skill_id, "scope": pair.scope,
                         "deterministic_rows_baseline": len(base), "deterministic_rows_new": len(new), "identical": base == new,
                         "only_in_baseline": "; ".join(sorted(set(base) - set(new))), "only_in_new": "; ".join(sorted(set(new) - set(base)))})
    return pd.DataFrame(rows)


def llm_added_findings(scans, findings):
    """LLM security findings in B, classified against the deterministic alerts of A_behavioral (same skill + scope)."""
    pairs = _pair_frame(scans, "behavioral", "behavioral_llm")
    det = _security(_in_pairs(findings, pairs, "behavioral"))
    llm = _security(_in_pairs(findings, pairs, "behavioral_llm"))
    llm = llm[llm["analyzer"].eq("llm")].copy()
    if llm.empty:
        return llm.assign(relation=pd.Series(dtype=str))

    def relation(f):
        same = det[(det["skill_id"] == f["skill_id"]) & (det["scope"] == f["scope"])]
        if same[(same["file_path"] == f["file_path"]) & (same["research_category"] == f["research_category"])].shape[0]:
            return "corroborated: deterministic alert in same file and category"
        if same[same["research_category"] == f["research_category"]].shape[0]:
            return "partly corroborated: same category, other file"
        if same[same["file_path"] == f["file_path"]].shape[0]:
            return "partly corroborated: same file, other category"
        return "LLM-only"
    llm["relation"] = llm.apply(relation, axis=1)
    llm["alert_key"] = llm.apply(_alert_key, axis=1)
    return llm[["skill_id", "repo", "sample_stratum", "scope", "configuration", "severity", "rule_id", "research_category",
                "file_path", "reported_line_number", "title", "description", "snippet", "llm_verdict", "llm_confidence",
                "relation", "alert_key", "finding_id"]]


def llm_view_of_deterministic_alerts(scans, findings):
    pairs = _pair_frame(scans, "behavioral", "behavioral_llm")
    det = _security(_in_pairs(findings, pairs, "behavioral")).drop_duplicates(["skill_id", "scope", "location_key"])
    llm = _security(_in_pairs(findings, pairs, "behavioral_llm"))
    llm = llm[llm["analyzer"].eq("llm")]
    rows = []
    for f in det.to_dict("records"):
        same = llm[(llm["skill_id"] == f["skill_id"]) & (llm["scope"] == f["scope"])]
        match = same[(same["file_path"] == f["file_path"]) & (same["research_category"] == f["research_category"])]
        cat = same[same["research_category"] == f["research_category"]]
        rows.append({"skill_id": f["skill_id"], "scope": f["scope"], "rule_id": f["rule_id"], "severity": f["severity"],
                     "research_category": f["research_category"], "file_path": f["file_path"],
                     "reported_line_number": f["reported_line_number"], "location_key": f["location_key"],
                     "llm_view": "LLM reports same file + category" if len(match) else
                                 "LLM reports same category elsewhere" if len(cat) else "LLM silent",
                     "llm_titles": " | ".join(match["title"].astype(str).head(3))})
    return pd.DataFrame(rows)


def meta_decisions(scans, findings):
    rows = []
    for mode in ("behavioral_meta", "behavioral_llm_meta"):
        part_scans = scans[scans["analyzer_mode"].eq(mode) & scans["status"].isin(READABLE)]
        for scan in part_scans.to_dict("records"):
            f = findings[(findings["skill_id"] == scan["skill_id"]) & (findings["configuration"] == scan["configuration"])]
            for x in f.to_dict("records"):
                if x["analyzer"] == "meta":
                    decision = "added by Meta (missed threat)"
                elif scan["meta_status"] == "not_invoked_no_findings":
                    decision = "not reviewed: Meta not invoked"
                elif scan["meta_status"] == "skipped_clear_deterministic":
                    decision = "retained: routing skipped (clear deterministic evidence, no LLM call)"
                elif x["meta_false_positive"] is True:
                    decision = "suppressed as false positive"
                elif x["meta_analysis_degraded"] is True or scan["meta_status"] == "degraded":
                    decision = "retained unreviewed: Meta response malformed (degraded)"
                elif scan["meta_status"] == "failed":
                    decision = "retained unreviewed: Meta failed"
                elif x["meta_validated"] is True:
                    decision = "retained: validated by Meta"
                else:
                    decision = "retained: reviewed, not flagged"
                rows.append({"configuration": scan["configuration"], "label": SHORT[mode], "skill_id": x["skill_id"],
                             "scope": x["scope"], "meta_status": scan["meta_status"], "core_status": scan["core_status"],
                             "analyzer": x["analyzer"], "finding_kind": x["finding_kind"], "severity": x["severity"],
                             "rule_id": x["rule_id"], "research_category": x["research_category"], "file_path": x["file_path"],
                             "reported_line_number": x["reported_line_number"], "location_key": x["location_key"],
                             "decision": decision, "meta_reason": x["meta_reason"], "meta_confidence": x["meta_confidence"],
                             "meta_priority": x["meta_priority"], "title": x["title"], "finding_id": x["finding_id"]})
    return pd.DataFrame(rows)


def meta_decision_summary(decisions):
    if decisions.empty:
        return pd.DataFrame()
    out = (decisions.assign(kind=decisions["finding_kind"].where(decisions["finding_kind"].eq("security"), "metadata / coverage"))
           .groupby(["label", "kind", "analyzer", "decision"]).agg(rows=("finding_id", "size"), skills=("skill_id", "nunique"))
           .reset_index())
    return out


def severity_changes(scans, findings):
    """Deterministic alerts whose severity differs between configurations, and LLM alerts whose severity differs between
    the two LLM runs (B and the LLM part of C). Meta never rewrites severity in Cisco 2.3.1; this checks that."""
    prim = _primary_scans(scans)
    f = _security(findings.merge(prim[["skill_id", "configuration"]], on=["skill_id", "configuration"]))
    f = f.assign(alert_key=f.apply(_alert_key, axis=1) if not f.empty else pd.Series(dtype=str))
    rows = []
    for (skill, scope, key), part in f.groupby(["skill_id", "scope", "alert_key"]):
        sevs = part.groupby("analyzer_mode")["severity"].agg(lambda s: "/".join(sorted(set(s.astype(str)), key=_sev_rank)))
        if part["severity"].nunique() > 1:
            rows.append({"skill_id": skill, "scope": scope, "alert_key": key, "analyzer": part["analyzer"].iloc[0],
                         **{f"severity_{SHORT.get(m, m)}": v for m, v in sevs.items()},
                         "note": "LLM alert keys are coarse (category + file); several LLM findings can share one key"
                         if part["analyzer"].iloc[0] in NON_DETECTION_ANALYZERS else "deterministic alert"})
    return pd.DataFrame(rows)


def category_by_configuration(scans, findings):
    prim = _primary_scans(scans)
    f = _security(findings.merge(prim[["skill_id", "configuration"]], on=["skill_id", "configuration"]))
    if f.empty:
        return pd.DataFrame()
    f = f.assign(source=f["analyzer"].where(f["analyzer"].isin(NON_DETECTION_ANALYZERS), "deterministic"),
                 label=f["analyzer_mode"].map(SHORT))
    out = f.pivot_table(index=["research_category", "source"], columns="label", values="finding_id", aggfunc="count", fill_value=0)
    return out.reset_index()


def unique_by_configuration(scans, findings):
    """Alert membership across configurations, restricted to (skill, scope) pairs where every compared configuration has a
    primary scan. Meta configurations use what Cisco shows without --verbose (findings not marked false positive)."""
    prim = _primary_scans(scans)
    modes = [m for m in SHORT if m in set(prim["analyzer_mode"])]
    complete_pairs = prim.groupby(["skill_id", "scope"])["analyzer_mode"].agg(set)
    complete_pairs = complete_pairs[complete_pairs.map(lambda s: set(modes) <= s)].reset_index()[["skill_id", "scope"]]
    f = _security(findings.merge(complete_pairs, on=["skill_id", "scope"]))
    f = f[f["analyzer_mode"].isin(modes) & f["post_meta_visible"]]
    if f.empty:
        return pd.DataFrame(), len(complete_pairs)
    f = f.assign(alert_key=f.apply(_alert_key, axis=1))
    member = f.groupby(["skill_id", "scope", "alert_key"]).agg(
        configurations=("analyzer_mode", lambda s: "+".join(SHORT[m] for m in modes if m in set(s))),
        analyzer=("analyzer", "first"), max_severity=("severity", lambda s: min(s.astype(str), key=_sev_rank))).reset_index()
    out = member.groupby(["configurations", "analyzer"]).agg(alerts=("alert_key", "size"), skills=("skill_id", "nunique")).reset_index()
    out.insert(0, "skill_scope_pairs_compared", len(complete_pairs))
    return out.sort_values("alerts", ascending=False), len(complete_pairs)


def runtime_and_cost(scans, experiment):
    executed = scans[scans["result_origin"].ne("not scanned") & scans["wall_seconds"].notna()]
    p_in, p_out = PRICES_PER_MTOK[REFERENCE_PAID_MODEL]
    rows = []
    for (cfg, mode), part in executed.groupby(["configuration", "analyzer_mode"], sort=False):
        wall = part["wall_seconds"].astype(float)
        tin, tout = part["input_tokens"].fillna(0).astype(float), part["output_tokens"].fillna(0).astype(float)
        rows.append({"configuration": cfg, "label": SHORT.get(mode, mode), "scans_timed": len(part),
                     "origin": part["result_origin"].iloc[0], "wall_seconds_median": round(wall.median(), 1),
                     "wall_seconds_mean": round(wall.mean(), 1), "wall_seconds_p90": round(wall.quantile(0.9), 1),
                     "wall_seconds_total": round(wall.sum(), 1), "input_tokens_total": int(tin.sum()),
                     "output_tokens_total": int(tout.sum()), "input_tokens_mean": round(tin.mean(), 1),
                     "output_tokens_mean": round(tout.mean(), 1),
                     "actual_cost_usd": round(part["cost_usd"].fillna(0).astype(float).sum(), 4),
                     f"same_tokens_at_{REFERENCE_PAID_MODEL}_usd": round(tin.sum() * p_in / 1e6 + tout.sum() * p_out / 1e6, 4),
                     "model": experiment.llm.model if NEW_MODES.get(mode, {}).get("uses_llm") or NEW_MODES.get(mode, {}).get("uses_meta") else "none"})
    return pd.DataFrame(rows)


def llm_run_stability(scans, findings):
    pairs = _pair_frame(scans, "behavioral_llm", "behavioral_llm_meta")
    rows = []
    for pair in pairs.itertuples(index=False):
        def keys(mode):
            part = findings[(findings["skill_id"] == pair.skill_id) & (findings["scope"] == pair.scope)
                            & findings["analyzer_mode"].eq(mode) & findings["analyzer"].eq("llm") & findings["finding_kind"].eq("security")]
            return {(_alert_key(r), r["severity"]) for r in part.to_dict("records")}
        b, c = keys("behavioral_llm"), keys("behavioral_llm_meta")
        kb, kc = {k for k, _ in b}, {k for k, _ in c}
        union = kb | kc
        rows.append({"skill_id": pair.skill_id, "scope": pair.scope, "llm_alerts_run1_B": len(kb), "llm_alerts_run2_C": len(kc),
                     "shared": len(kb & kc), "jaccard": round(len(kb & kc) / len(union), 3) if union else 1.0,
                     "identical_keys": kb == kc, "identical_keys_and_severity": b == c,
                     "only_run1": "; ".join(sorted(kb - kc)), "only_run2": "; ".join(sorted(kc - kb))})
    return pd.DataFrame(rows)


def alert_groups(findings):
    sec = _security(findings)
    if sec.empty:
        return pd.DataFrame()
    sec = sec.assign(label=sec["analyzer_mode"].map(SHORT), file=sec["file_path"].fillna("(no file)"))
    out = sec.groupby(["skill_id", "file", "research_category"]).agg(
        max_severity=("severity", lambda s: min(s.astype(str), key=_sev_rank)), raw_rows=("finding_id", "size"),
        configurations=("label", lambda s: "; ".join(sorted(set(s)))), scopes=("scope", lambda s: "; ".join(sorted(set(s)))),
        analyzers=("analyzer", lambda s: "; ".join(sorted(set(s)))), rules=("rule_id", lambda s: "; ".join(sorted(set(s)))),
        lines=("reported_line_number", lambda s: ", ".join(str(int(v)) for v in sorted(set(s.dropna())))),
        deterministic_rows=("analyzer", lambda s: int((~s.isin(NON_DETECTION_ANALYZERS)).sum())),
        llm_rows=("analyzer", lambda s: int(s.eq("llm").sum())),
        meta_suppressed_rows=("meta_false_positive", lambda s: int((s == True).sum())),  # noqa: E712
    ).reset_index()
    out["support"] = out.apply(lambda r: "deterministic + LLM" if r["deterministic_rows"] and r["llm_rows"] else
                                         "deterministic only" if r["deterministic_rows"] else "LLM / Meta only", axis=1)
    out.insert(0, "group_id", [f"G{i + 1:03d}" for i in range(len(out))])
    return out.sort_values(["max_severity", "skill_id"], key=lambda s: s.map(_sev_rank) if s.name == "max_severity" else s)


def triage_queue(llm_added, llm_view, decisions, stability, review, seed=TRIAGE_SEED, cap=TRIAGE_CAP_PER_BUCKET):
    """Buckets of scanner disagreement for targeted manual investigation. Each bucket keeps every candidate when it has at
    most `cap`, otherwise a seeded random sample (unbiased within the bucket); `bucket_size` keeps the denominator."""
    reviewed = {}
    if review is not None:
        for r in review.to_dict("records"):
            reviewed[(r["skill_id"], r["rule_id"], r["file_path"])] = r["review_id"]
    buckets = []
    if not llm_added.empty:
        x = llm_added[llm_added["relation"].eq("LLM-only") & llm_added["severity"].isin(["CRITICAL", "HIGH", "MEDIUM"])]
        buckets.append(("T1 LLM-only alert (MEDIUM+)", "possible new detection or LLM false alarm", x))
        y = llm_added[llm_added["relation"].ne("LLM-only")]
        buckets.append(("T5 control: LLM corroborated by deterministic alert", "calibration sample (agreement)", y))
    if not llm_view.empty:
        z = llm_view[llm_view["llm_view"].eq("LLM silent") & llm_view["severity"].isin(["CRITICAL", "HIGH"])]
        buckets.append(("T3 HIGH+ deterministic alert, LLM silent", "possible deterministic false alarm or LLM miss", z))
    if not decisions.empty:
        s = decisions[decisions["decision"].eq("suppressed as false positive") & decisions["finding_kind"].eq("security")]
        buckets.append(("T2 suppressed by Meta", "check whether the suppression is justified", s))
        a = decisions[decisions["decision"].eq("added by Meta (missed threat)")]
        buckets.append(("T4b added by Meta", "possible new detection by Meta", a))
    if not stability.empty:
        u = stability[~stability["identical_keys"]]
        buckets.append(("T4 LLM run-to-run disagreement", "unstable LLM output on identical input", u))
    rng, rows = random.Random(seed), []
    for name, why, frame in buckets:
        recs = frame.to_dict("records")
        chosen = recs if len(recs) <= cap else rng.sample(recs, cap)
        for rec in chosen:
            rows.append({"bucket": name, "why": why, "bucket_size": len(recs), "selected": len(chosen),
                         "selection": "all" if len(recs) <= cap else f"random sample, seed {seed}",
                         "skill_id": rec.get("skill_id"), "scope": rec.get("scope"), "severity": rec.get("severity"),
                         "rule_id": rec.get("rule_id"), "research_category": rec.get("research_category"),
                         "file_path": rec.get("file_path"), "line": rec.get("reported_line_number"),
                         "title": rec.get("title") or rec.get("llm_titles"),
                         "detail": rec.get("relation") or rec.get("decision") or rec.get("llm_view") or
                                   (f"only run1: {rec.get('only_run1')} | only run2: {rec.get('only_run2')}" if "only_run1" in rec else None),
                         "existing_review_id": reviewed.get((rec.get("skill_id"), rec.get("rule_id"), rec.get("file_path")))})
    return pd.DataFrame(rows)


def case_studies(review, findings, llm_view, decisions):
    if review is None or review.empty:
        return pd.DataFrame()
    rows = []
    for r in review.to_dict("records"):
        out = {k: r.get(k) for k in ("review_id", "skill_id", "rule_id", "severity_reported", "file_path", "reported_line_number",
                                     "configurations")}
        out["provisional_label"] = f"{r.get('provisional_label')} (provisional, AI-assisted; not ground truth)"
        for scope in ("SKILL.md only", "Full folder"):
            tag = "skillmd" if scope == "SKILL.md only" else "full"
            v = llm_view[(llm_view["skill_id"] == r["skill_id"]) & (llm_view["scope"] == scope) & (llm_view["rule_id"] == r["rule_id"])
                         & (llm_view["file_path"] == r["file_path"])] if not llm_view.empty else llm_view
            out[f"{tag}_llm_view"] = v["llm_view"].iloc[0] if len(v) else "alert not in this scope's primary B pair"
            for label in ("Cdet_meta", "C_llm_meta"):
                d = decisions[(decisions["skill_id"] == r["skill_id"]) & (decisions["scope"] == scope)
                              & (decisions["rule_id"] == r["rule_id"]) & (decisions["file_path"] == r["file_path"])
                              & decisions["label"].eq(label)] if not decisions.empty else decisions
                out[f"{tag}_{label}_decision"] = "; ".join(sorted(set(d["decision"]))) if len(d) else "not present"
        rows.append(out)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- cost estimate (no API calls)

def estimate_costs(root, run_dir, model=REFERENCE_PAID_MODEL, skills_n=(30, 100, 300, 1000)):
    """Expected cost of B + C-det + C for N skills at `model` prices, from the tokens measured in this run.

    Local (qwen3) token counts stand in for Claude's tokenizer: the 'high' column adds 35 % to input tokens (Claude's
    newer tokenizer uses ~1.0-1.35x the tokens of older ones) and assumes at least 4,000 output tokens per model call
    (adaptive thinking is billed as output; Cisco sets no effort level, so the model default applies). Scaling to N skills
    assumes the same stratum mix as the measured sample; skills with large folders cost more (prompt budgets cap them)."""
    _, _, scans, _ = load_tables(run_dir)
    p_in, p_out = PRICES_PER_MTOK[model]
    executed = scans[scans["analyzer_mode"].isin(list(NEW_MODES)) & scans["result_origin"].eq("new scan")
                     & scans["wall_seconds"].notna()]
    rows = []
    for mode, part in executed.groupby("analyzer_mode"):
        n_skills = part["skill_id"].nunique()                   # skills with at least one finished scan of this mode
        tin, tout = part["input_tokens"].fillna(0).astype(float), part["output_tokens"].fillna(0).astype(float)
        per_skill_in, per_skill_out = tin.sum() / n_skills, tout.sum() / n_skills
        # Model calls per scan that used tokens: B 1 (LLM); C-det 1 (Meta, when routed); C 2 (LLM + Meta, when routed).
        calls_per_scan = 2 if NEW_MODES[mode]["uses_llm"] and NEW_MODES[mode]["uses_meta"] else 1
        calls = tin.gt(0).sum() * calls_per_scan / n_skills
        central = per_skill_in * p_in / 1e6 + per_skill_out * p_out / 1e6
        high = per_skill_in * 1.35 * p_in / 1e6 + max(per_skill_out, calls * 4000) * p_out / 1e6
        rows.append({"mode": SHORT[mode], "skills_measured": n_skills, "scans_measured": len(part),
                     "model_calls_per_skill_approx": round(calls, 2), "input_tokens_per_skill": round(per_skill_in),
                     "output_tokens_per_skill": round(per_skill_out), "usd_per_skill_central": round(central, 4),
                     "usd_per_skill_high": round(high, 4)})
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    total = {"mode": "TOTAL (B + C-det + C)", **{c: out[c].sum() for c in out.columns
                                                  if c.startswith("usd") or c.endswith("_per_skill") or c.endswith("_approx")}}
    total = {k: round(v, 4) if isinstance(v, float) else v for k, v in total.items()}
    out = pd.concat([out, pd.DataFrame([total])], ignore_index=True)
    for n in skills_n:
        out[f"usd_{n}_skills_central"] = (out["usd_per_skill_central"] * n).round(2)
        out[f"usd_{n}_skills_high"] = (out["usd_per_skill_high"] * n).round(2)
    out.attrs["model"] = model
    return out


# ---------------------------------------------------------------- driver

def _review_items(root):
    path = Path(root) / "results" / "manual_review" / "sample30-seed2027" / "manual_review_worksheet_provisional.csv"
    return pd.read_csv(path) if path.is_file() else None


def analyze(root, run_dir, build_report=True, log=print):
    root, run_dir = Path(root).resolve(), Path(run_dir).resolve()
    experiment, spec, scans, findings = load_tables(run_dir)
    out = run_dir / "llm_meta_analysis"
    out.mkdir(exist_ok=True)
    review = _review_items(root)

    scans.to_csv(run_dir / "scan_summary.csv", index=False)
    findings.to_csv(run_dir / "individual_findings.csv", index=False)
    t = {"coverage_by_configuration": coverage_by_configuration(scans),
         "findings_by_configuration": findings_by_configuration(scans, findings),
         "deterministic_reproducibility": deterministic_reproducibility(scans, findings)}
    t["llm_added_findings"] = llm_added_findings(scans, findings)
    t["llm_view_of_deterministic_alerts"] = llm_view_of_deterministic_alerts(scans, findings)
    t["meta_decisions"] = meta_decisions(scans, findings)
    t["meta_decision_summary"] = meta_decision_summary(t["meta_decisions"])
    t["severity_changes"] = severity_changes(scans, findings)
    t["category_by_configuration"] = category_by_configuration(scans, findings)
    t["unique_by_configuration"], pairs_compared = unique_by_configuration(scans, findings)
    t["runtime_and_cost"] = runtime_and_cost(scans, experiment)
    t["llm_run_stability"] = llm_run_stability(scans, findings)
    t["alert_groups"] = alert_groups(findings)
    t["triage_queue"] = triage_queue(t["llm_added_findings"], t["llm_view_of_deterministic_alerts"], t["meta_decisions"],
                                     t["llm_run_stability"], review)
    t["case_studies"] = case_studies(review, findings, t["llm_view_of_deterministic_alerts"], t["meta_decisions"])
    for name, frame in t.items():
        frame.to_csv(out / f"{name}.csv", index=False)
    _comparison_files(run_dir, t)
    estimate = estimate_costs(root, run_dir)
    estimate.to_csv(out / "cost_estimate_claude_sonnet_5_5.csv", index=False)
    _run_metadata(root, run_dir, spec, experiment, scans, findings)
    (run_dir / "results_summary.md").write_text(_summary_md(run_dir, experiment, spec, scans, findings, t, estimate, pairs_compared),
                                                encoding="utf-8")
    log(f"analysis written to {out} ({len(scans)} scan rows, {len(findings)} finding rows)")
    if build_report:
        from gitskills_reports import build_report as _build, load_run, refresh_index
        target = _build(load_run(run_dir), root)
        refresh_index(root)
        log(f"report: {target.relative_to(root)}")
    return t


def _comparison_files(run_dir, t):
    """Finding-level rows in the *_comparison.csv shape (comparison, pair_status, change, finding_id, ...) the reports read."""
    llm = t["llm_added_findings"]
    if not llm.empty:
        rows = llm.assign(comparison="A_behavioral -> B_llm (" + llm["scope"] + ")", pair_status="both primary",
                          change="added by LLM: " + llm["relation"], finding_kind="security", analyzer_mode="behavioral_llm")
        rows.to_csv(run_dir / "llm_comparison.csv", index=False)
    d = t["meta_decisions"]
    if not d.empty:
        rows = d.assign(comparison="pre-Meta -> post-Meta, " + d["label"] + " (" + d["scope"] + ")",
                        pair_status="meta " + d["meta_status"].astype(str), change=d["decision"])
        rows.to_csv(run_dir / "meta_comparison.csv", index=False)


def _run_metadata(root, run_dir, spec, experiment, scans, findings):
    source = Path(root) / spec["source_run"]["path"]
    source_meta = json.loads((source / "run_metadata.json").read_text(encoding="utf-8"))
    status_path = run_dir / "execution_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.is_file() else {}
    configs = [{k: v for k, v in c.items()} for c in BASELINE_CONFIGS + new_configs(experiment.modes)]
    write_json(run_dir / "run_metadata.json", {
        "run_id": run_dir.name, "run_mode": "scan", "stage": status.get("state", "unknown"),
        "run_started_at": spec.get("prepared_at"), "written_at": now_utc(),
        "source_run": {"run_id": spec["source_run"]["run_id"], "path": spec["source_run"]["path"],
                       "use": "sample manifest, exported skill folders and the four baseline reports (copied, SHA-256 checked)"},
        "database": source_meta.get("database"),
        "scanner": {"installed_version": (status.get("environment") or {}).get("scanner_version"),
                    "policy_setting": "balanced", "common_args": ["--format", "json", "--policy", "balanced"],
                    "configurations": configs,
                    "policy_fingerprints_seen": sorted(scans["policy_fingerprint"].dropna().unique().tolist())},
        "llm": {"settings": experiment.to_json()["llm"], "request_settings": status.get("llm_request_settings"),
                "ollama": status.get("ollama"), "api_key_recorded": False,
                "price_source": "local model: no API cost" if experiment.llm.is_local else "experiment.PRICES_PER_MTOK"},
        "experiment": spec["experiment"], "fingerprint": spec["fingerprint"],
        "settings": {"SELECTION_MODE": "manifest", "LENIENT": False, "ALLOW_INCOMPLETE_FOLDERS": False,
                     "SCAN_TIMEOUT_SECONDS": experiment.timeout_seconds, "ENABLE_LLM_CONFIGS": True},
        "environment": status.get("environment"),
        "sample": source_meta.get("sample"), "skills": source_meta.get("skills"),
        "execution": {k: status.get(k) for k in ("attempts_started", "attempts_finished", "attempts_interrupted", "spent_usd",
                                                 "pending", "stop_reason")},
        "run_status_counts": scans["status"].value_counts().to_dict(), "finding_rows": len(findings),
    })


def _md_table(df, max_rows=40):
    if df is None or df.empty:
        return "_(no rows)_\n"
    df = df.head(max_rows)
    cells = lambda v: "" if (v is None or (isinstance(v, float) and math.isnan(v))) else str(v).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(cells(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines) + "\n"


def _summary_md(run_dir, experiment, spec, scans, findings, t, estimate, pairs_compared):
    cov, fbc = t["coverage_by_configuration"], t["findings_by_configuration"]
    rep, stab = t["deterministic_reproducibility"], t["llm_run_stability"]
    llm, dec = t["llm_added_findings"], t["meta_decision_summary"]
    status = json.loads((run_dir / "execution_status.json").read_text(encoding="utf-8")) if (run_dir / "execution_status.json").is_file() else {}
    L = [f"# {run_dir.name}: Cisco LLM Analyzer and Meta-Analyzer on the 30-skill sample\n",
         f"Source run: `{spec['source_run']['path']}` (same sample manifest, seed 2027, same exported files; baseline reports "
         "copied and SHA-256 checked). Model: `" + experiment.llm.model + "` "
         + ("(local Ollama, no API cost)" if experiment.llm.is_local else "") + f". Execution state: **{status.get('state')}**.\n",
         "Scanner alerts are candidates for investigation, not confirmed vulnerabilities. Provisional labels from the manual-review "
         "worksheet are AI-assisted and are not ground truth.\n",
         "## Configurations\n",
         "- A_static / A_behavioral: notebook-01 baseline (`default`, `--use-behavioral`), reused.\n"
         "- B_llm: `--use-behavioral --use-llm --verbose`\n- Cdet_meta: `--use-behavioral --enable-meta --verbose` (Meta over "
         "deterministic findings only)\n- C_llm_meta: `--use-behavioral --use-llm --enable-meta --verbose`\n",
         "All new configurations use `--format json --policy balanced` like the baseline. `--verbose` keeps findings that Meta marks "
         "as false positives (flag `meta_false_positive`) instead of deleting them.\n",
         "## Coverage (denominators)\n", _md_table(cov.drop(columns=["denominator_note"], errors="ignore")),
         "## Security findings per configuration (primary scans: static/behavioral/LLM core COMPLETE, LLM ok)\n", _md_table(fbc),
         "## Deterministic findings unchanged by LLM / Meta?\n"]
    if not rep.empty:
        summary = rep.groupby("comparison")["identical"].agg(["sum", "size"]).reset_index()
        L.append(_md_table(summary.rename(columns={"sum": "identical_pairs", "size": "pairs"})))
    L.append("\n## LLM-analyzer findings (B) vs deterministic alerts\n")
    L.append(_md_table(llm.groupby(["scope", "relation"]).size().reset_index(name="llm_security_rows")) if not llm.empty else "_(none)_\n")
    L.append("\n## Meta-Analyzer decisions\n")
    L.append(_md_table(dec))
    L.append("\n## LLM run-to-run stability (B vs LLM part of C, identical input and settings)\n")
    if not stab.empty:
        L.append(f"{int(stab['identical_keys'].sum())} of {len(stab)} skill-scope pairs gave the same LLM alert keys; "
                 f"mean Jaccard {stab['jaccard'].mean():.2f}.\n")
    L.append("\n## Alerts unique to / shared by configurations\n")
    L.append(f"Restricted to {pairs_compared} skill-scope pairs with a primary scan in every configuration.\n\n")
    L.append(_md_table(t["unique_by_configuration"]))
    L.append("\n## Runtime and cost\n")
    L.append(_md_table(t["runtime_and_cost"]))
    L.append(f"\n## Estimated cost of the same experiment at {REFERENCE_PAID_MODEL} (no API call was made)\n")
    L.append(_md_table(estimate))
    L.append("\n## Files\n")
    L += [f"- `llm_meta_analysis/{name}.csv`: {about}\n" for name, about in TABLES.items()]
    return "".join(x if x.endswith("\n") else x + "\n" for x in L)
