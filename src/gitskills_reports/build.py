"""Write a report folder for one saved run (or combined report), and the index of all reports.

Layout of results/reports/<database>/<run ID>/ (combined reports: results/reports/<database>/combined/<ID>/):

    01_IMPORTANT_RESULTS/   START_HERE.md, dashboard.html, headline tables, the run's own summary
    02_DETAILED_ANALYSIS/   per-skill pages, rule / analyzer breakdowns, full (redacted) finding tables, figures
    03_RAW_SCANNER_OUTPUT/  index of the raw Cisco reports (paths + SHA-256, nothing copied), metadata copies
    04_HUMAN_VALIDATION/    validation status and snapshots of the manual-review worksheet (when one exists)
    report_manifest.json    every input and output with its SHA-256

Source folders are only read. Every text output is redacted and made path-portable, and the finished folder is
audited for secrets and absolute paths before it replaces an earlier build of the same report.
"""

import json
import os
import re
import shutil
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from . import dashboard, tables
from .model import (TIER_LABELS, TIER_ORDER, analyzer_info, discover, experiment_name, find_review, load_combined, load_run,
                    sha256_of)
from .redaction import Portable, audit_tree, clean_frame, clean_json, clean_text, count_redactions, dumps

GENERATOR = "gitskills_reports"
GENERATOR_VERSION = "1.0"
FOLDERS = ("01_IMPORTANT_RESULTS", "02_DETAILED_ANALYSIS", "03_RAW_SCANNER_OUTPUT", "04_HUMAN_VALIDATION")


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------- Markdown helpers (untrusted text stays inert)

def md(value):
    """A table-cell-safe, inert Markdown rendering of any value (no HTML, links or emphasis can come through)."""
    if value is None or (not isinstance(value, (list, dict, str)) and pd.isna(value)):
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    text = str(value).replace("\r", " ").replace("\n", " ")
    return re.sub(r"([\\`*\[\]<>|])", r"\\\1", text)     # no HTML, links, code spans, emphasis or cell breaks


def md_table(df, columns=None, max_rows=None, labels=None, raw_columns=()):
    """raw_columns hold Markdown this module wrote itself (links); every other cell is escaped with md()."""
    if df is None or df.empty:
        return "_None._\n"
    df = df[columns] if columns else df
    shown = df if max_rows is None else df.head(max_rows)
    head = [md((labels or {}).get(c, c)) for c in df.columns]
    raw = [c in raw_columns for c in df.columns]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(str(v) if r else md(v) for v, r in zip(row, raw)) + " |" for row in shown.itertuples(index=False)]
    if max_rows is not None and len(df) > max_rows:
        lines.append(f"\n_{len(df) - max_rows} more row(s) in the CSV._")
    return "\n".join(lines) + "\n"


def code_block(text):
    text = "" if text is None or (not isinstance(text, str) and pd.isna(text)) else str(text)
    fence = "`" * max(3, max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
    return f"{fence}text\n{text}\n{fence}\n"


def link(from_dir, target, label=None):
    rel = Path(os.path.relpath(target, from_dir)).as_posix()
    return f"[{md(label or Path(target).name)}]({rel.replace(' ', '%20')})"


# ---------------------------------------------------------------- writers

def frame_redactions(df):
    return sum(count_redactions(v) for col in df.columns
               if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]) for v in df[col])


class Writer:
    """Writes cleaned outputs into the staging folder and remembers each one for the manifest."""

    def __init__(self, stage, portable):
        self.stage, self.portable, self.outputs, self.redactions = stage, portable, [], 0

    def _record(self, path, kind, source=None):
        self.outputs.append({"path": path.relative_to(self.stage).as_posix(), "kind": kind,
                             "derived_from": self.portable.path(source) if source else None})

    def text(self, rel, text, kind="generated", source=None):
        if not str(rel).endswith(".html"):
            text = clean_text(text, self.portable)
        path = self.stage / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        self._record(path, kind, source)
        return path

    def csv(self, rel, df, kind="generated", source=None):
        cleaned = clean_frame(df, self.portable)
        self.redactions += frame_redactions(cleaned) - frame_redactions(df)
        return self.text(rel, cleaned.to_csv(index=False, lineterminator="\n"), kind, source)

    def copy_text(self, rel, source, kind="redacted copy", rewrite=None):
        original = Path(source).read_text(encoding="utf-8")
        cleaned = clean_text(original, self.portable)
        if rewrite:
            cleaned = cleaned.replace(*rewrite)
        self.redactions += count_redactions(cleaned) - count_redactions(original)
        return self.text(rel, cleaned, kind, source)

    def copy_csv(self, rel, source):
        return self.csv(rel, pd.read_csv(source), "redacted copy", source)

    def json(self, rel, value, kind="generated", source=None):
        return self.text(rel, dumps(clean_json(value, self.portable)), kind, source)

    def copy_binary(self, rel, source):
        path = self.stage / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, path)
        self._record(path, "copy", source)
        return path


# ---------------------------------------------------------------- the report

def report_dir_for(source, out_root):
    base = Path(out_root) / source.db_tag
    return base / "combined" / source.report_id if source.kind == "combined" else base / source.report_id


def build_report(source, root, out_root=None, review="auto"):
    """Build (or rebuild) the report for one loaded Source. Returns the report folder."""
    root = Path(root).resolve()
    out_root = Path(out_root or root / "results" / "reports").resolve()
    portable = Portable(root)
    if review == "auto":
        review = find_review(source, root) if source.kind == "run" else None
    source, review = _cleaned(source, review, portable)
    target = report_dir_for(source, out_root)
    stage = target.with_name(target.name + ".building")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    w = Writer(stage, portable)
    try:
        ctx = _write_all(source, review, w, root, target)
        problems = audit_tree(stage, root)
        if problems:
            listing = "\n".join(f"  {p.relative_to(stage)}: {why}: {excerpt!r}" for p, why, excerpt in problems[:20])
            raise RuntimeError(f"Safety audit failed for {source.report_id}; nothing was published:\n{listing}")
        w.json("report_manifest.json", _manifest(source, review, w, portable, ctx))
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    if target.exists():
        manifest = target / "report_manifest.json"
        if not manifest.is_file() or GENERATOR not in manifest.read_text(encoding="utf-8"):
            shutil.rmtree(stage, ignore_errors=True)
            raise FileExistsError(f"{target} exists and was not written by {GENERATOR}; refusing to replace it.")
        shutil.rmtree(target)                     # an earlier build of this same generated report
    stage.rename(target)
    return target


def _cleaned(source, review, portable):
    """Redacted, path-portable copies of every table and metadata value, so no later step can leak raw text."""
    source = replace(source, metadata=clean_json(source.metadata, portable), scans=clean_frame(source.scans, portable),
                     findings=clean_frame(source.findings, portable), comparisons=clean_frame(source.comparisons, portable),
                     template=clean_frame(source.template, portable),
                     extra_tables={k: clean_frame(v, portable) for k, v in source.extra_tables.items()})
    if review is not None:
        review = replace(review, items=clean_frame(review.items, portable), match=clean_text(review.match, portable))
    return source, review


def _write_all(source, review, w, root, target):
    portable = w.portable
    annotated = tables.annotate_findings(source, review)
    key = tables.key_security_findings(annotated, source)
    counts = tables.run_counts(source)
    validation = tables.validation_counts(key, review)
    coverage = tables.coverage_by_configuration(source)
    severity = tables.severity_by_configuration(source)
    comparisons = tables.comparison_summary(source)
    rules = tables.rule_breakdown(source)
    analyzers = tables.analyzer_breakdown(source)
    configs = tables.config_table(source)

    sec_skills = list(dict.fromkeys(key["skill_id"])) if not key.empty else []
    detail_pages = {s: f"02_DETAILED_ANALYSIS/skills/{re.sub(r'[^A-Za-z0-9_.-]', '_', s)}.md" for s in sec_skills}
    skills = tables.skills_index(source, annotated, detail_pages) if not source.scans.empty else pd.DataFrame()

    I, D, R, H = (Path(f) for f in FOLDERS)
    w.csv(I / "coverage_summary.csv", coverage)
    w.csv(I / "key_security_findings.csv", key)
    w.csv(I / "severity_by_configuration.csv", severity)
    w.csv(I / "comparison_summary.csv", comparisons)
    if source.summary_md:            # its figure links point at figures/ next to it; the copies live in 02_DETAILED_ANALYSIS
        w.copy_text(I / source.summary_md.name, source.summary_md, rewrite=("](figures/", "](../02_DETAILED_ANALYSIS/figures/"))

    w.csv(D / "skills_index.csv", skills)
    w.csv(D / "rule_breakdown.csv", rules)
    w.csv(D / "analyzer_breakdown.csv", analyzers)
    w.csv(D / "configurations.csv", configs)
    if not annotated.empty:
        w.csv(D / "individual_findings_annotated.csv", annotated, "redacted copy + review columns",
              source.inputs.get("individual_findings.csv") or source.inputs.get("combined_findings.csv"))
        w.csv(D / "metadata_and_coverage_findings.csv", annotated[annotated["finding_kind"] != "security"])
    for name in ("context_comparison.csv", "analyzer_comparison.csv", "combined_comparison_findings.csv"):
        if name in source.inputs:
            w.copy_csv(D / name, source.inputs[name])
    for extra in (n for n in source.inputs if n.endswith("_comparison.csv") and n not in ("context_comparison.csv", "analyzer_comparison.csv")):
        w.copy_csv(D / extra, source.inputs[extra])
    for name, frame in source.extra_tables.items():          # LLM / Meta comparison tables (already redacted)
        w.csv(D / "llm_meta" / f"{name}.csv", frame, "redacted copy", source.inputs.get(f"llm_meta_analysis/{name}.csv"))
    for fig in source.figures:
        w.copy_binary(D / "figures" / fig.name, fig)
    for skill in sec_skills:
        w.text(detail_pages[skill], _skill_page(skill, source, annotated, skills, review, target))

    raw = pd.DataFrame()
    if source.kind == "run":
        raw = tables.raw_report_index(source.folder, source.configurations, source.scans, portable)
        w.csv(R / "raw_report_index.csv", raw)
        w.copy_csv(R / "scan_summary.csv", source.inputs["scan_summary.csv"])
        w.json(R / "run_metadata.json", source.metadata, "redacted copy", source.inputs["run_metadata.json"])
        for name in ("sample/sample_manifest.csv", "sample/sampling_metadata.json"):
            if name in source.inputs:
                (w.copy_csv if name.endswith(".csv") else w.copy_text)(R / Path(name).name, source.inputs[name])
    else:
        members = []
        for label, folder in source.member_runs.items():
            try:
                member = load_run(folder)
            except (FileNotFoundError, ValueError):
                continue
            idx = tables.raw_report_index(member.folder, member.configurations, member.scans, portable)
            members.append(idx.assign(member=label))
        raw = pd.concat(members, ignore_index=True) if members else raw
        w.csv(R / "raw_report_index.csv", raw)
        w.copy_csv(R / "combined_scan_summary.csv", source.inputs["combined_scan_summary.csv"])
        w.json(R / "combined_metadata.json", source.metadata, "redacted copy", source.inputs["combined_metadata.json"])
    w.text(R / "README.md", _raw_readme(source, raw, portable))

    if review is not None:
        w.csv(H / "review_items.csv", _review_items(review, key))
        for name, path in review.files.items():
            (w.copy_csv if name.endswith(".csv") else w.copy_text)(H / "snapshots" / name, path)
    w.text(H / "validation_status.md", _validation_md(source, review, key, validation, portable))

    ctx = {"source": source, "counts": counts, "validation": validation, "coverage": coverage, "severity": severity,
           "comparisons": comparisons, "rules": rules, "analyzers": analyzers, "configs": configs, "key": key,
           "annotated": annotated, "skills": skills, "review": review, "raw": raw, "root": root, "portable": portable,
           "limitations": _limitations(source, counts, validation, review, raw), "generated_at": now_utc(),
           "files": _rq_files(source, review)}
    w.text(I / "START_HERE.md", _start_here(ctx))
    w.text(I / "dashboard.html", dashboard.render(ctx))
    return ctx


def _manifest(source, review, w, portable, ctx):
    inputs = {name: {"path": portable.path(p), "sha256": sha256_of(p)} for name, p in source.inputs.items()}
    if review is not None:
        inputs.update({f"review/{n}": {"path": portable.path(p), "sha256": sha256_of(p)} for n, p in review.files.items()})
    outputs = [{**o, "sha256": sha256_of(w.stage / o["path"]), "bytes": (w.stage / o["path"]).stat().st_size} for o in w.outputs]
    return {"generator": GENERATOR, "generator_version": GENERATOR_VERSION, "generated_at": ctx["generated_at"],
            "kind": source.kind, "report_id": source.report_id, "run_mode": source.run_mode, "db_tag": source.db_tag,
            "experiment": source.experiment, "source_folder": portable.path(source.folder),
            "source_run": (source.metadata.get("source_run") or {}).get("path") if source.run_mode == "reanalyze" else None, "review_folder": portable.path(review.folder) if review else None,
            "review_match": review.match if review else None, "counts": ctx["counts"], "validation": ctx["validation"],
            "redactions_applied": w.redactions, "safety_audit": "passed: no secret patterns or absolute local paths in any text output",
            "rebuild": "python -m gitskills_reports --run " + portable.path(source.folder) if source.kind == "run"
            else "python -m gitskills_reports --combined " + portable.path(source.folder),
            "inputs": inputs, "outputs": outputs}


# ---------------------------------------------------------------- page content

SKILL_COVERAGE = tables.SKILL_COVERAGE


def _limitations(source, counts, validation, review, raw):
    out = []
    o = counts["scans_by_outcome"]
    v = validation["locations_by_tier"]
    total_locations = sum(v.values())
    if v.get("human_validated", 0) == 0 and total_locations:
        out.append(f"**No security alert has been validated by a human yet.** All {total_locations} distinct alert locations are "
                   "Cisco scanner output; none of them is a confirmed vulnerability.")
    if v.get("provisional", 0):
        out.append(f"{v['provisional']} alert location(s) carry a *provisional* label. These are researcher-approved, AI-assisted "
                   "decisions, **not** independent human-review results, and must not be reported as validated.")
    if o["excluded_incomplete_folder"]:
        n = counts["skills_by_coverage"]["complete_except_excluded"]
        out.append(f"{o['excluded_incomplete_folder']} configuration(s) were excluded by design: GitSkills did not store every "
                   f"supporting file of {n} skill(s), so their full-folder scans were not run. Those skills drop out of the "
                   "SKILL.md-only vs full-folder comparison.")
    if o["partial"] or o["contract_only"]:
        out.append(f"{o['partial']} partial and {o['contract_only']} contract-only scan(s) are kept but excluded from the primary "
                   "analysis (see the status definitions); their findings appear only as preliminary / sensitivity evidence.")
    if o["failed"] or o["missing"] or counts["export_errors"]:
        out.append(f"{o['failed']} failed scan(s), {o['missing']} missing report(s) and {counts['export_errors']} export error(s): "
                   "these skills have incomplete coverage and are not \"zero findings\".")
    kinds = counts["finding_rows_by_kind"]
    if kinds.get("metadata_quality", 0) > kinds.get("security", 0):
        out.append(f"Most finding rows ({kinds.get('metadata_quality', 0)} of {counts['finding_rows']}) are metadata-quality notes "
                   "(missing license, vague description, ...), not security alerts. \"Skills with findings\" therefore overstates "
                   f"security exposure; use skills with security alerts ({counts['skills_with_security_alert_primary']}).")
    modes = {c.get("analyzer_mode") for c in source.configurations}
    for mode in sorted(m for m in modes if analyzer_info(m)["deterministic"] is False):
        out.append(f"Configurations using `{mode}` are not deterministic: {analyzer_info(mode)['about']}")
    unexecuted = [c["configuration"] for c in source.configurations
                  if source.scans.empty or not source.scans.loc[source.scans["configuration"] == c["configuration"], "scan_executed"].any()]
    if unexecuted:
        out.append("Configured but never executed: " + ", ".join(f"`{c}`" for c in unexecuted) + ".")
    if source.run_mode == "reanalyze":
        src = (source.metadata.get("source_run") or {}).get("path")
        out.append(f"This is a reanalysis: Cisco was not executed in this run. Its reports were copied from `{src}` and analysed "
                   "again with the current notebook code.")
    if review is not None and "byte-identical" in review.match:
        out.append("The manual-review worksheet was built from another run; it is attached here because " + review.match + ".")
    if not raw.empty and raw["sha256_matches_record"].eq(False).any():
        out.append(f"{int(raw['sha256_matches_record'].eq(False).sum())} raw report(s) no longer match the hash recorded at scan time.")
    out.append("Snippets and other text from skills are redacted where they look like secrets, and absolute local paths are "
               "rewritten as repository-relative ones. Cisco's raw reports (local only, not committed) keep the original text.")
    return out


def _rq_files(source, review):
    """Which file answers which research question (paths relative to the report folder)."""
    rows = [
        ("Start here", "01_IMPORTANT_RESULTS/START_HERE.md", "this overview"),
        ("Start here", "01_IMPORTANT_RESULTS/dashboard.html", "interactive tables and charts; open in any browser, works offline"),
        ("Coverage / reliability (RQ1-C)", "01_IMPORTANT_RESULTS/coverage_summary.csv", "planned vs executed scans and outcomes per configuration"),
        ("Coverage / reliability (RQ1-C)", "02_DETAILED_ANALYSIS/skills_index.csv", "coverage class and finding counts for every skill"),
        ("Context and detection (RQ1-A)", "01_IMPORTANT_RESULTS/comparison_summary.csv", "SKILL.md-only vs full-folder: additional / removed / unchanged findings"),
        ("Context and detection (RQ1-A)", "02_DETAILED_ANALYSIS/context_comparison.csv", "finding-level comparison rows"),
        ("Behavior coverage (RQ1-B)", "01_IMPORTANT_RESULTS/key_security_findings.csv", "one row per distinct security alert location, with validation tier"),
        ("Behavior coverage (RQ1-B)", "02_DETAILED_ANALYSIS/rule_breakdown.csv", "which Cisco rules fired, how often, in how many skills"),
        ("Analyzer configuration (RQ1-C)", "01_IMPORTANT_RESULTS/severity_by_configuration.csv", "security alerts by severity and configuration"),
        ("Analyzer configuration (RQ1-C)", "02_DETAILED_ANALYSIS/analyzer_comparison.csv", "default vs behavioral (and future LLM / meta) finding-level comparison"),
        ("Analyzer configuration (RQ1-C)", "02_DETAILED_ANALYSIS/analyzer_breakdown.csv", "security alerts per Cisco analyzer"),
        ("Validation", "04_HUMAN_VALIDATION/validation_status.md", "what has and has not been validated"),
        ("Reproducibility", "03_RAW_SCANNER_OUTPUT/README.md", "where the raw Cisco reports are, with their hashes"),
        ("Reproducibility", "report_manifest.json", "every input and output with SHA-256"),
    ]
    if source.kind == "combined":
        rows = [r for r in rows if "context_comparison" not in r[1] and "analyzer_comparison" not in r[1]]
        rows.insert(5, ("Context and detection (RQ1-A)", "02_DETAILED_ANALYSIS/combined_comparison_findings.csv", "finding-level comparison rows of every pilot"))
    if review is not None:
        rows.insert(-2, ("Validation", "04_HUMAN_VALIDATION/review_items.csv", "every review item with its tier and labels"))
    for name in source.extra_tables:
        rows.insert(-2, ("LLM / Meta analyzers", f"02_DETAILED_ANALYSIS/llm_meta/{name}.csv", LLM_META_ABOUT.get(name, name)))
    return rows


# The LLM / Meta tables shown in START_HERE and the dashboard: (table, heading, columns, explanation). Tables a run lacks
# are skipped; every table is also written in full to 02_DETAILED_ANALYSIS/llm_meta/.
LLM_META_SECTIONS = [
    ("research_insights", "Research insights (gap analysis; provisional, not validated)", ["n", "insight", "evidence", "implication"],
     "Curated from the saved scans and the skills' source code; details in docs/cisco_security_gap_analysis.md. "
     "Alerts and candidates are not confirmed vulnerabilities."),
    ("gap_candidates", "Candidate detection gaps (hand-classified, provisional)",
     ["candidate_id", "skill_id", "file_path", "lines", "behavior", "cisco_deterministic", "classification"],
     "Class 1 only against an explicitly stated requirement (R1-R11 in the gap-analysis document); "
     "'not reported' alone is never treated as a false negative."),
    ("coverage_by_configuration", "Coverage and denominators",
     ["label", "configuration", "planned", "executed", "complete", "partial", "failed", "excluded_incomplete_folder",
      "not_run_or_missing", "primary_core_complete", "llm_ok", "llm_failed", "meta_ran", "meta_skipped_clear_deterministic",
      "meta_not_invoked_no_findings", "meta_degraded", "meta_failed"],
     "Planned = skills x configuration. Primary = static/behavioral(/LLM) core COMPLETE and, for LLM configurations, the LLM "
     "call succeeded. Meta status is counted separately: a degraded or failed Meta run keeps every finding unreviewed."),
    ("findings_by_configuration", "Security findings per configuration (primary scans)", None,
     "Raw rows include findings Meta marked as false positives; 'after_meta' is what Cisco shows without --verbose."),
    ("llm_added_findings_summary", "What the LLM Analyzer adds", None,
     "Each LLM security finding compared with the deterministic alerts of the behavioral baseline for the same skill and scope."),
    ("meta_decision_summary", "Meta-Analyzer: retained, suppressed, unreviewed, added", None,
     "Cisco 2.3.1 Meta never changes severity; it marks false positives, validates, or adds 'missed threats'."),
    ("deterministic_reproducibility_summary", "Are static/behavioral findings unchanged when LLM / Meta are on?", None,
     "Identical = same findings (rule, file, line, evidence hash, severity) as the reused baseline scan."),
    ("llm_run_stability_summary", "LLM run-to-run stability", None,
     "B and the LLM part of C analyse the same input with the same settings; differences are model nondeterminism."),
    ("unique_by_configuration", "Alerts unique to / shared by configurations", None,
     "Only skill-scope pairs with a primary scan in every configuration. Alert = rule+file+line (deterministic) or "
     "analyzer+category+file (LLM / Meta)."),
    ("severity_changes", "Severity changes", None, "Same alert key, different severity across configurations."),
    ("runtime_and_cost", "Runtime, tokens and cost",
     ["label", "configuration", "scans_timed", "wall_seconds_median", "wall_seconds_p90", "wall_seconds_total",
      "input_tokens_total", "output_tokens_total", "actual_cost_usd", "same_tokens_at_claude-sonnet-5-5_usd", "model"],
     "Wall time per Cisco CLI call. Local-model tokens priced at Claude Sonnet 5.5 rates are an approximation (different tokenizer)."),
    ("triage_queue_summary", "Targeted manual-investigation queue", None,
     "Disagreement buckets with a seeded sample per bucket; candidates for review, not findings."),
    ("case_studies", "The 11 manually inspected findings (provisional labels, not ground truth)", None, ""),
]
LLM_META_ABOUT = {
    "research_insights": "curated research insights from the gap analysis (docs/cisco_security_gap_analysis.md)",
    "gap_candidates": "hand-classified candidate detection gaps with file, line and Cisco coverage",
    "gap_pattern_summary": "systematic pattern-search hits per behavior family and how many Cisco reported",
    "coverage_by_configuration": "planned / executed / complete / excluded scans, LLM and Meta status per configuration",
    "findings_by_configuration": "security rows, skills with alerts, before / after Meta",
    "deterministic_reproducibility": "static/behavioral findings with LLM / Meta switched on vs the baseline",
    "llm_added_findings": "every LLM-analyzer security finding with its relation to deterministic alerts",
    "llm_view_of_deterministic_alerts": "for each deterministic alert, whether the LLM reported the same file + category",
    "meta_decisions": "every finding Meta saw and what it decided",
    "meta_decision_summary": "Meta decision counts",
    "severity_changes": "same alert, different severity",
    "category_by_configuration": "research category x configuration",
    "unique_by_configuration": "alerts by the configurations that report them",
    "runtime_and_cost": "wall time, tokens and cost per configuration",
    "llm_run_stability": "LLM findings in two runs on identical input",
    "alert_groups": "deduplicated alert groups across configurations (raw rows kept elsewhere)",
    "triage_queue": "candidates for targeted manual investigation",
    "case_studies": "the 11 manually inspected findings vs LLM and Meta",
    "cost_estimate_claude_sonnet_5_5": "estimated cost of the experiment at Claude Sonnet 5.5 prices for 30-1,000 skills",
}


def llm_meta_tables(source):
    """Tables for the LLM / Meta sections, with small derived summaries. Empty dict for other runs."""
    t = dict(source.extra_tables)
    if not t:
        return {}
    if "llm_added_findings" in t and not t["llm_added_findings"].empty:
        t["llm_added_findings_summary"] = (t["llm_added_findings"].groupby(["scope", "relation"])
                                           .agg(llm_security_rows=("finding_id", "size"), skills=("skill_id", "nunique")).reset_index())
    if "deterministic_reproducibility" in t and not t["deterministic_reproducibility"].empty:
        d = t["deterministic_reproducibility"]
        t["deterministic_reproducibility_summary"] = (d.groupby("comparison")["identical"]
                                                      .agg(identical_pairs="sum", pairs="size").reset_index())
    if "llm_run_stability" in t and not t["llm_run_stability"].empty:
        s = t["llm_run_stability"]
        t["llm_run_stability_summary"] = pd.DataFrame([{
            "skill_scope_pairs": len(s), "identical_alert_keys": int(s["identical_keys"].sum()),
            "identical_keys_and_severity": int(s["identical_keys_and_severity"].sum()),
            "mean_jaccard": round(float(s["jaccard"].mean()), 3), "llm_alerts_run1": int(s["llm_alerts_run1_B"].sum()),
            "llm_alerts_run2": int(s["llm_alerts_run2_C"].sum()), "shared": int(s["shared"].sum())}])
    if "triage_queue" in t and not t["triage_queue"].empty:
        t["triage_queue_summary"] = t["triage_queue"].drop_duplicates("bucket")[["bucket", "why", "bucket_size", "selected", "selection"]]
    return t


def _overview_rows(ctx):
    s, c = ctx["source"], ctx["counts"]
    meta, scanner = s.metadata, s.metadata.get("scanner") or {}
    sample = meta.get("sample") or {}
    db = meta.get("database") or {}
    rows = [("Experiment", s.experiment), ("Report ID", s.report_id),
            ("Kind", {"scan": "scan (Cisco was executed in this run)", "reanalyze": "reanalysis of a saved run (Cisco not executed)",
                      "combined": "combined report over several runs (notebook 02)"}.get(s.run_mode, s.run_mode))]
    if s.run_mode == "reanalyze":
        rows.append(("Source run", (meta.get("source_run") or {}).get("path")))
    if s.kind == "combined":
        rows.append(("Runs combined", ", ".join(f"{k} ({Path(v).name})" for k, v in s.member_runs.items())))
    rows += [("Scanner", scanner.get("installed_version")), ("Policy", scanner.get("policy_setting")),
             ("Database", f"{db.get('path')} (SHA-256 {str(db.get('sha256'))[:12]}...)" if db else None),
             ("Sample", f"{sample.get('sample_id')} ({sample.get('skills')} skills; strata "
                        + ", ".join(f"{k} {v}" for k, v in (sample.get("strata") or {}).items()) + ")" if sample else None),
             ("Run started (UTC)", meta.get("run_started_at")), ("Report generated (UTC)", ctx["generated_at"])]
    return [(k, v) for k, v in rows if v]


def _start_here(ctx):
    s, c, v = ctx["source"], ctx["counts"], ctx["validation"]
    o = c["scans_by_outcome"]
    L = [f"# START HERE: {md(s.experiment)}\n",
         f"Generated by `{GENERATOR}` {GENERATOR_VERSION} from `{ctx['portable'].path(s.folder)}`. Every number below is "
         "computed from that folder's CSV files; nothing here is edited by hand. Open **dashboard.html** (same folder) for "
         "searchable tables and charts.\n",
         "> **Scanner alerts are not vulnerabilities.** Cisco reports *alerts*. An alert becomes a validated finding only "
         f"when a human reviewer labels it in the manual-review worksheet. Human-validated so far: "
         f"**{v['locations_by_tier']['human_validated']}** of {sum(v['locations_by_tier'].values())} alert locations.\n",
         "## 1. What was run\n"]
    L.append(md_table(pd.DataFrame(_overview_rows(ctx), columns=["", "value"])))
    L.append("\nConfigurations (each skill is planned once per configuration):\n")
    L.append(md_table(ctx["configs"], ["configuration", "analyzer", "about"]))

    L.append("\n## 2. Coverage: what was selected, attempted, completed, skipped or failed\n")
    sk = c["skills_by_coverage"]
    L.append(md_table(pd.DataFrame([
        ("Skills selected", c["skills_selected"], "skills chosen for this experiment (sample manifest or selection)"),
        ("Skills exported", c["skills_exported"], f"exported from the database for scanning ({c['export_errors']} export errors)"),
        ("Skills scanned", c["skills_scanned"], "at least one Cisco scan was executed"),
        ("... all configurations COMPLETE", sk["complete"], SKILL_COVERAGE["complete"]),
        ("... COMPLETE except design exclusions", sk["complete_except_excluded"], SKILL_COVERAGE["complete_except_excluded"]),
        ("... partially complete", sk["partially_complete"], SKILL_COVERAGE["partially_complete"]),
        ("... no COMPLETE scan", sk["no_complete_scan"], SKILL_COVERAGE["no_complete_scan"]),
        ("Skills not scanned", sk["not_scanned"], SKILL_COVERAGE["not_scanned"]),
    ], columns=["skills", "count", "meaning"])))
    L.append(f"\nScans: **{c['scans_planned']} planned** ({c['skills_exported']} skills x {c['configurations']} configurations), "
             f"**{c['scans_executed']} executed**: {o['complete']} complete, {o['contract_only']} contract-only, {o['partial']} partial, "
             f"{o['failed']} failed. Not executed: {o['excluded_incomplete_folder']} excluded by design (incomplete folder), "
             f"{o['missing']} missing.\n")
    L.append(md_table(ctx["coverage"], ["configuration", "planned", "executed", "complete", "contract_only", "partial", "failed",
                                         "excluded_incomplete_folder", "missing"]))
    L.append("\nOnly COMPLETE scans enter the primary analysis. CONTRACT_ONLY, PARTIAL and FAILED scans are never counted as "
             "\"zero findings\".\n")

    L.append("\n## 3. What Cisco reported\n")
    kinds = c["finding_rows_by_kind"]
    L.append(f"- **{c['skills_with_security_alert_primary']} of {c['skills_scanned']} scanned skills** have at least one *security* "
             f"alert in a COMPLETE scan ({c['skills_with_security_alert_any']} counting partial / contract-only scans too).\n"
             f"- {c['security_rows_primary']} security alert rows in COMPLETE scans (one row per skill x configuration x alert), "
             f"which collapse to **{c['security_locations_primary']} distinct alert locations** (rule + file + line per skill).\n"
             f"- {c['finding_rows']} finding rows overall: " + ", ".join(f"{k} {n}" for k, n in kinds.items()) +
             f". {c['skills_with_any_finding']} skills have *any* finding, mostly metadata-quality notes; do not read that as "
             "security exposure.\n")
    L.append("\nSecurity alert rows in COMPLETE scans, by severity and configuration:\n")
    sev = ctx["severity"]
    L.append(md_table(sev, [col for col in sev.columns if col != "analyzer_mode"]))
    if not ctx["rules"].empty:
        L.append("\nSecurity rules that fired:\n")
        rules = ctx["rules"][ctx["rules"]["finding_kind"] == "security"]
        L.append(md_table(rules, ["rule_id", "max_severity", "cisco_category", "rows_primary", "skills_all", "distinct_locations_primary"]))
    if not ctx["key"].empty:
        L.append("\nDistinct security alert locations (all tiers; details in `key_security_findings.csv` and the per-skill pages):\n")
        L.append(md_table(ctx["key"], ["severity", "rule_id", "skill_id", "file_path", "reported_line_number", "validation_tier_label",
                                       "provisional_label", "final_label"], max_rows=40,
                          labels={"validation_tier_label": "validation", "reported_line_number": "line"}))

    L.append("\n## 4. Validation status\n")
    L.append(md_table(pd.DataFrame([(TIER_LABELS[t], v["locations_by_tier"][t]) for t in TIER_ORDER],
                                   columns=["tier", "distinct alert locations"])))
    if v["provisional_labels"]:
        L.append("\nProvisional labels: " + ", ".join(f"{md(k)} {n}" for k, n in v["provisional_labels"].items()) + ".\n")
    L.append("\nSee `04_HUMAN_VALIDATION/validation_status.md`.\n")

    llm_meta = llm_meta_tables(s)
    if llm_meta:
        L.append("\n## 4b. LLM Analyzer and Meta-Analyzer\n")
        L.append("Every table is in full in `02_DETAILED_ANALYSIS/llm_meta/`. LLM and Meta output is nondeterministic and "
                 "model-dependent; disagreements are candidates for targeted manual investigation, not results.\n")
        for name, heading, columns, about in LLM_META_SECTIONS:
            frame = llm_meta.get(name)
            if frame is None or frame.empty:
                continue
            L.append(f"\n**{heading}.** {about}\n")
            L.append(md_table(frame, [c for c in (columns or frame.columns) if c in frame.columns], max_rows=25))

    L.append("\n## 5. Which file to open\n")
    L.append(md_table(pd.DataFrame(ctx["files"], columns=["question", "file", "what it holds"])))

    L.append("\n## 6. Limitations and incomplete results\n")
    L += [f"- {item}\n" for item in ctx["limitations"]]

    L.append("\n## 7. Reproducibility\n")
    L.append(f"- Source folder (local only, not committed): `{ctx['portable'].path(s.folder)}`\n"
             f"- Raw Cisco reports are indexed with SHA-256 in `03_RAW_SCANNER_OUTPUT/raw_report_index.csv` and not copied.\n"
             f"- Every input and output hash: `report_manifest.json`.\n"
             f"- Rebuild: `notebooks/05_build_reports.ipynb`, or from the repository root\n"
             f"  `.venv/bin/python -m gitskills_reports --{'run' if s.kind == 'run' else 'combined'} {ctx['portable'].path(s.folder)}` "
             "(with `src` on `PYTHONPATH`).\n")
    return "\n".join(x.rstrip("\n") for x in L) + "\n"          # a blank line between blocks


def _skill_page(skill, source, annotated, skills, review, target):
    f = annotated[annotated["skill_id"] == skill]
    info = skills[skills["skill_id"] == skill].iloc[0]
    scans = source.scans[source.scans["skill_id"] == skill]
    L = [f"# Skill `{md(skill)}`\n",
         f"[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)\n",
         md_table(pd.DataFrame([("Repository", info["repo"]), ("SKILL.md path", info["skill_path"]),
                                ("Sample stratum", info["sample_stratum"]), ("Folder complete in GitSkills", info["folder_complete"]),
                                ("Coverage", f"{info['coverage']}: {SKILL_COVERAGE.get(info['coverage'], '')}")], columns=["", "value"])),
         "\n## Scans\n",
         md_table(scans, ["configuration", "status", "findings_count", "max_severity", "status_detail"]),
         "\n## Security alerts\n",
         "Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a "
         "secret; they are untrusted skill content, shown as plain text.\n"]
    sec = f[f["finding_kind"] == "security"]
    for loc, g in sec.groupby("location_key", sort=False):
        first = g.iloc[0]
        L.append(f"\n### {md(first['severity'])} · {md(first['rule_id'])} · {md(first['file_path'])}:{md(first['reported_line_number'])}\n")
        L.append(md_table(pd.DataFrame([
            ("Validation", TIER_LABELS.get(first["validation_tier"], "")), ("Review ID", first["review_id"]),
            ("Provisional label", first["provisional_label"]), ("Final (human) label", first["final_label"]),
            ("Configurations", tables.join_unique(g["configuration"])), ("Scan outcomes", tables.join_unique(g["run_outcome"])),
            ("Cisco category", first["cisco_category"]), ("Analyzer", tables.join_unique(g["analyzer"])),
            ("Evidence check", tables.join_unique(g["evidence_status"])), ("Title", first["title"])], columns=["", "value"])))
        L.append("\nEvidence snippet:\n\n" + code_block(first["snippet"]))
    other = f[f["finding_kind"] != "security"]
    L.append(f"\n## Other notes\n\n{len(other)} metadata-quality / scan-coverage rows: "
             + ", ".join(f"{md(r)} ({n})" for r, n in other["rule_id"].value_counts().items()) + ".\n")
    return "\n".join(x.strip("\n") for x in L) + "\n"          # a blank line between blocks


def _raw_readme(source, raw, portable):
    L = ["# Raw Cisco scanner output\n",
         "The raw reports are **not copied** here: they stay in the source run folder, which is git-ignored because it holds "
         "exported, untrusted skill files. This folder holds an index of them with SHA-256 hashes, plus redacted copies of the "
         "small metadata files.\n",
         f"- Source folder: `{portable.path(source.folder)}`\n"]
    if source.kind == "run":
        L.append("- Per skill: `<skill_id>/manifest.json` (export provenance and file hashes), `only/SKILL.md`, `full/**` "
                 "(exported files), `reports/<configuration>.json` (Cisco JSON exactly as printed) and "
                 "`reports/<configuration>.run.json` (command, exit code, timing, stderr tail).\n")
    if not raw.empty:
        n_ok = int(raw["sha256_matches_record"].eq(True).sum())
        L.append(f"\n`raw_report_index.csv`: {len(raw)} report slots, {int(raw['report_exists'].sum())} report files present, "
                 f"{n_ok} hash(es) verified against the value recorded at scan time, "
                 f"{int(raw['sha256_matches_record'].eq(False).sum())} mismatch(es). Slots without a file are design exclusions "
                 "or failures (see `status`).\n")
    L.append("\nFiles: `raw_report_index.csv`, `scan_summary.csv` / `combined_scan_summary.csv`, `run_metadata.json` / "
             "`combined_metadata.json`, and the sample manifest when the run used one.\n")
    return "\n".join(x.strip("\n") for x in L) + "\n"


def _review_items(review, key):
    cols = [c for c in ("review_id", "priority", "behavior_group", "skill_id", "rule_id", "severity_reported", "file_path",
                        "reported_line_number", "configurations", "suggested_interpretation", "suggested_confidence",
                        "provisional_label", "provisional_label_status", "final_label", "adjudicated_by", "review_date",
                        "validation_tier") if c in review.items]
    items = review.items[cols].copy()
    items["validation_tier_label"] = items["validation_tier"].map(TIER_LABELS)
    return items


def _validation_md(source, review, key, validation, portable):
    v = validation["locations_by_tier"]
    L = ["# Human validation status\n",
         "Three tiers are kept strictly apart in every table of this report:\n",
         "1. **Scanner alert**: Cisco reported it. Nothing more is known.\n"
         "2. **Provisional**: a researcher-approved, AI-assisted label (`provisional_label`). Useful for triage, but **not** an "
         "independent human review, and never reported as validated.\n"
         "3. **Human-validated**: `final_label` is filled and `adjudicated_by` names the adjudicator.\n",
         "\n" + md_table(pd.DataFrame([(TIER_LABELS[t], v[t]) for t in TIER_ORDER], columns=["tier", "distinct alert locations"]))]
    if review is None:
        L.append("\nNo manual-review worksheet exists for this run yet. Create one with `notebooks/04_manual_review_worksheet.ipynb`.\n")
        return "\n".join(x.strip("\n") for x in L) + "\n"
    L.append(f"\nWorksheet: `{portable.path(review.folder)}` ({review.match}). {validation['review_items']} review items: "
             + ", ".join(f"{TIER_LABELS[t]} {n}" for t, n in validation["review_items_by_tier"].items() if n) + ".\n")
    if validation["provisional_labels"]:
        L.append("\nProvisional labels: " + ", ".join(f"{md(k)} {n}" for k, n in validation["provisional_labels"].items()) + ".\n")
    L.append(f"\nFinal human labels: {', '.join(f'{md(k)} {n}' for k, n in validation['final_labels'].items()) or 'none yet'}.\n")
    L.append("\n`snapshots/` holds redacted copies of the worksheet files as they were when this report was built (hashes in "
             "`report_manifest.json`). Edit the originals in `results/manual_review/`, never the snapshots, then rebuild.\n")
    return "\n".join(x.strip("\n") for x in L) + "\n"


# ---------------------------------------------------------------- everything at once, and the index

def build_all(root=None, out_root=None, log=print):
    root = Path(root or Path.cwd()).resolve()
    out_root = Path(out_root or root / "results" / "reports").resolve()
    runs, combined, legacy = discover(root / "results" / "cisco_dataset_runs")
    built = []
    for folder in runs:
        built.append(build_report(load_run(folder), root, out_root))
        log(f"built {Portable(root).path(built[-1])}")
    for folder in combined:
        built.append(build_report(load_combined(folder, root), root, out_root))
        log(f"built {Portable(root).path(built[-1])}")
    refresh_index(root, out_root)
    return built


def refresh_index(root=None, out_root=None):
    """Rewrite results/reports/README.md and index.html from the report manifests already on disk (no rebuild)."""
    root = Path(root or Path.cwd()).resolve()
    out_root = Path(out_root or root / "results" / "reports").resolve()
    entries = []
    for path in sorted(out_root.glob("**/report_manifest.json")):
        if ".building" in path.parent.name:
            continue
        m = json.loads(path.read_text(encoding="utf-8"))
        if m.get("generator") != GENERATOR:
            continue
        entries.append({"report_id": m["report_id"], "kind": m["kind"], "run_mode": m["run_mode"], "db_tag": m.get("db_tag"),
                        "experiment": m.get("experiment"), "source_run": m.get("source_run"), "folder": m["source_folder"],
                        "report": path.parent.relative_to(out_root).as_posix(), "counts": m["counts"],
                        "validation": m["validation"], "review": m["review_folder"]})
    _, _, legacy = discover(root / "results" / "cisco_dataset_runs")
    write_index(entries, legacy, root, out_root)
    return out_root / "index.html"


def write_index(entries, legacy, root, out_root):
    """results/reports/README.md + index.html: every report, its role, and which one to open first."""
    portable = Portable(root)
    by_folder = {e["folder"]: e for e in entries}
    for e in entries:
        e["role"] = {"scan": "original scan", "reanalyze": "reanalysis", "combined": "combined pilots"}.get(e["run_mode"], e["run_mode"])
    reanalyses = {}
    for e in sorted(entries, key=lambda e: e["report_id"]):
        if e["run_mode"] == "reanalyze":
            reanalyses.setdefault(e["source_run"], []).append(e)
    for src, group in reanalyses.items():
        for older in group[:-1]:
            older["role"] = f"superseded by {group[-1]['report_id']}"
        if src in by_folder:
            by_folder[src]["role"] = f"original scan (latest reanalysis: {group[-1]['report_id']})"
    for e in entries:
        e["recommended"] = (e["run_mode"] == "reanalyze" and not e["role"].startswith("superseded")) or \
                           (e["run_mode"] == "scan" and e["folder"] not in reanalyses) or e["run_mode"] == "combined"
    entries.sort(key=lambda e: (not e["recommended"], e["kind"], e["report_id"]))
    df = pd.DataFrame([{
        "open": "★" if e["recommended"] else "", "report": e["report_id"], "role": e["role"],
        "skills": e["counts"]["skills_selected"], "scans (complete/planned)": f"{e['counts']['scans_by_outcome']['complete']}/{e['counts']['scans_planned']}",
        "skills with security alerts": e["counts"]["skills_with_security_alert_primary"],
        "alert locations": sum(e["validation"]["locations_by_tier"].values()),
        "human-validated": e["validation"]["locations_by_tier"]["human_validated"],
        "start page": f"{e['report']}/01_IMPORTANT_RESULTS/START_HERE.md"} for e in entries])
    L = ["# Cisco scanner reports\n\n",
         "Generated by `notebooks/05_build_reports.ipynb` (or notebook 01's last section). One folder per saved run; each has "
         "`01_IMPORTANT_RESULTS/START_HERE.md` and a self-contained `dashboard.html`. ★ marks the report to open first for each "
         "experiment: the latest analysis of each scan. Older reanalyses are kept for traceability.\n",
         "\n" + md_table(df.drop(columns="start page").assign(report=[f"[{md(e['report_id'])}]({e['report']}/01_IMPORTANT_RESULTS/START_HERE.md)"
                                                                        for e in entries]), raw_columns=("report",)),
         "\nAlerts are Cisco scanner output, not vulnerabilities; only the human-validated column counts reviewed results.\n"]
    if legacy:
        L.append("\nNot reported (legacy flat layout without a run ID, kept untouched): "
                 + ", ".join(f"`{portable.path(p)}`" for p in legacy) + ".\n")
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "README.md").write_text("".join(L), encoding="utf-8")
    (out_root / "index.html").write_text(dashboard.render_index(entries, [portable.path(p) for p in legacy]), encoding="utf-8")
    problems = [p for p in audit_tree(out_root, root) if p[0].parent == out_root]
    if problems:
        raise RuntimeError(f"Safety audit failed for the report index: {problems[:5]}")
