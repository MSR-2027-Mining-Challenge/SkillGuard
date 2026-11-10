"""Loading saved Cisco runs (and combined pilot reports) into one in-memory shape the report builders share.

Nothing here writes anything. Run folders are read exactly as notebook 01 / 02 left them.
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# Same status -> outcome mapping as notebook 01 (Section 8). The status column is authoritative: older runs
# wrote outcome "skipped" where newer ones write "excluded_incomplete_folder".
STATUS_OUTCOME = {"COMPLETE": "complete", "CONTRACT_ONLY": "contract_only", "PARTIAL": "partial",
                  "SKIPPED_INCOMPLETE_FOLDER": "excluded_incomplete_folder", "MISSING_REPORT": "missing"}
OUTCOME_ORDER = ["complete", "contract_only", "partial", "failed", "excluded_incomplete_folder", "missing"]
NOT_EXECUTED_STATUSES = ("SKIPPED_INCOMPLETE_FOLDER", "MISSING_REPORT", "EXPORT_ERROR")
SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

# What each analyzer mode means. Unknown modes (a future Cisco analyzer) get a generic description, so a new
# configuration never breaks a report; add an entry here once its behavior is confirmed.
ANALYZER_MODES = {
    "default": {"label": "Static", "deterministic": True,
                "about": "Cisco's static analyzer only: signature (YAML/YARA) rules and Python checks over the files."},
    "behavioral": {"label": "Static + behavioral", "deterministic": True,
                   "about": "Static analyzer plus Cisco's behavioral dataflow analyzer over the skill's scripts."},
    "llm": {"label": "Static + LLM", "deterministic": False,
            "about": "Static analyzer plus Cisco's LLM Analyzer, an LLM judge reading SKILL.md and scripts. "
                     "Results can vary between runs and depend on the provider and model recorded in run_metadata.json; "
                     "skill content is sent to that provider."},
    "meta": {"label": "Meta-Analyzer", "deterministic": False,
             "about": "Cisco's Meta-Analyzer, a second LLM pass over other analyzers' findings (for example to filter "
                      "likely false positives). Compare it with the configuration it post-processes; its findings are "
                      "not independent detections."},
    # Verified against the installed Cisco 2.3.1 code (docs/cisco_llm_meta_analyzers.md).
    "behavioral_llm": {"label": "B: static + behavioral + LLM", "deterministic": False,
                       "about": "Behavioral baseline plus Cisco's LLM Analyzer (--use-llm): one LLM call per scan over SKILL.md, "
                                "manifest, code and referenced files within Cisco's prompt budgets, enriched with the "
                                "deterministic findings. Static/behavioral findings are unchanged; LLM findings carry "
                                "analyzer 'llm'. Results depend on the model recorded in run_metadata.json."},
    "behavioral_meta": {"label": "C-det: static + behavioral + Meta", "deterministic": False,
                        "about": "Behavioral baseline plus Cisco's Meta-Analyzer (--enable-meta) without the LLM Analyzer. "
                                 "Meta post-processes the deterministic findings: it is skipped when there are none, makes "
                                 "no LLM call when every finding is clear deterministic evidence, and otherwise marks "
                                 "findings as false positives (kept here via --verbose) or adds 'missed threats'. It never "
                                 "changes severity."},
    "behavioral_llm_meta": {"label": "C: static + behavioral + LLM + Meta", "deterministic": False,
                            "about": "B plus the Meta-Analyzer over all findings, including the LLM Analyzer's. The LLM "
                                     "Analyzer runs again inside this scan, so its findings can differ from B's (see "
                                     "llm_run_stability)."},
}


def analyzer_info(mode):
    return ANALYZER_MODES.get(str(mode), {"label": str(mode), "deterministic": None,
                                          "about": f"Analyzer mode '{mode}' has no description yet (add it to ANALYZER_MODES)."})


def outcome_of(status):
    return STATUS_OUTCOME.get(status, "failed")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path):
    if not Path(path).is_file():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:              # a table with no rows and no columns (e.g. nothing to compare yet)
        return pd.DataFrame()


def find_root(start=None):
    start = Path(start or Path.cwd()).resolve()
    return next(f for f in (start, *start.parents) if (f / "notebooks").is_dir() and (f / "results").is_dir())


def experiment_name(run_id):
    """'2026-11-03_173516_sample30-seed2027' -> 'sample30-seed2027'."""
    return re.sub(r"^\d{4}-\d{2}-\d{2}_\d{6}_", "", str(run_id))


@dataclass
class Source:
    """One saved Cisco run (kind 'run') or one notebook-02 combined report (kind 'combined')."""
    kind: str
    report_id: str
    db_tag: str
    folder: Path
    metadata: dict
    scans: pd.DataFrame
    findings: pd.DataFrame
    comparisons: pd.DataFrame
    template: pd.DataFrame
    configurations: list
    inputs: dict                      # name -> Path of every file read
    figures: list = field(default_factory=list)
    summary_md: Path = None
    member_runs: dict = field(default_factory=dict)   # combined only: label -> run folder
    extra_tables: dict = field(default_factory=dict)  # LLM/Meta runs: llm_meta_analysis/<name>.csv -> DataFrame

    @property
    def run_mode(self):
        return self.metadata.get("run_mode", "combined" if self.kind == "combined" else "unknown")

    @property
    def experiment(self):
        return experiment_name(self.report_id)


def _normalize(scans, findings):
    if not scans.empty:
        scans = scans.copy()
        scans["outcome"] = scans["status"].map(outcome_of)
        scans["scan_executed"] = ~scans["status"].isin(NOT_EXECUTED_STATUSES)
    if not findings.empty:
        findings = findings.copy()
        findings["run_outcome"] = findings["run_status"].map(outcome_of)
        findings["severity"] = findings["severity"].fillna("UNKNOWN").astype(str).str.upper()
        if "finding_kind" not in findings:
            findings["finding_kind"] = "security"
    return scans, findings


def _configurations(metadata, scans):
    configs = (metadata.get("scanner") or {}).get("configurations") or []
    configs = [{k: c.get(k) for k in ("configuration", "scope", "analyzer_mode", "report_file")} for c in configs]
    known = {c["configuration"] for c in configs}
    if not scans.empty:                                    # anything scanned but not declared (older metadata)
        for row in scans.drop_duplicates("configuration").itertuples():
            if row.configuration not in known:
                configs.append({"configuration": row.configuration, "scope": row.scope, "analyzer_mode": row.analyzer_mode,
                                "report_file": None})
    return configs


def load_run(run_dir):
    run_dir = Path(run_dir).resolve()
    meta_path = run_dir / "run_metadata.json"
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    if not metadata.get("run_id"):
        raise ValueError(f"{run_dir} has no run_id in run_metadata.json (legacy layout); it is not reported.")
    inputs = {"run_metadata.json": meta_path}
    frames = {}
    for name in ("scan_summary", "individual_findings", "context_comparison", "analyzer_comparison", "manual_review_template"):
        path = run_dir / f"{name}.csv"
        frames[name] = read_csv(path)
        if path.is_file():
            inputs[path.name] = path
    # Any further *_comparison.csv (e.g. a future default -> llm file) is picked up automatically.
    extra = sorted(p for p in run_dir.glob("*_comparison.csv") if p.stem not in ("context_comparison", "analyzer_comparison"))
    comparisons = [frames["context_comparison"], frames["analyzer_comparison"]] + [read_csv(p) for p in extra]
    inputs.update({p.name: p for p in extra})
    for sample_file in ("sample/sample_manifest.csv", "sample/sampling_metadata.json"):
        if (run_dir / sample_file).is_file():
            inputs[sample_file] = run_dir / sample_file
    summary = run_dir / "results_summary.md"
    if summary.is_file():
        inputs["results_summary.md"] = summary
    extra_tables = {}                                       # written by gitskills_cisco_llm (LLM / Meta experiments)
    for path in sorted((run_dir / "llm_meta_analysis").glob("*.csv")):
        inputs[f"llm_meta_analysis/{path.name}"] = path
        extra_tables[path.stem] = read_csv(path)
    scans, findings = _normalize(frames["scan_summary"], frames["individual_findings"])
    comparisons = pd.concat([c for c in comparisons if not c.empty], ignore_index=True) if any(not c.empty for c in comparisons) else pd.DataFrame()
    db_tag = (metadata.get("database") or {}).get("tag") or run_dir.parent.parent.name
    return Source(kind="run", report_id=metadata["run_id"], db_tag=db_tag, folder=run_dir, metadata=metadata, scans=scans,
                  findings=findings, comparisons=comparisons, template=frames["manual_review_template"],
                  configurations=_configurations(metadata, scans), inputs=inputs,
                  figures=sorted((run_dir / "figures").glob("*.png")), summary_md=summary if summary.is_file() else None,
                  extra_tables=extra_tables)


def load_combined(combined_dir, root):
    combined_dir = Path(combined_dir).resolve()
    meta_path = combined_dir / "combined_metadata.json"
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    inputs = {"combined_metadata.json": meta_path}
    names = {"scans": "combined_scan_summary.csv", "findings": "combined_findings.csv",
             "comparisons": "combined_comparison_findings.csv", "template": "combined_manual_review.csv"}
    frames = {}
    for key, name in names.items():
        frames[key] = read_csv(combined_dir / name)
        if (combined_dir / name).is_file():
            inputs[name] = combined_dir / name
    members = {label: (Path(root) / info["folder"]).resolve() for label, info in (metadata.get("runs") or {}).items()}
    configs = [{"configuration": c} for c in metadata.get("configurations", [])]
    scans, findings = _normalize(frames["scans"], frames["findings"])
    if not scans.empty:
        lookup = scans.drop_duplicates("configuration").set_index("configuration")[["scope", "analyzer_mode"]].to_dict("index")
        configs = [{**c, **lookup.get(c["configuration"], {}), "report_file": None} for c in configs]
    metadata = {**metadata, "run_mode": "combined",
                "scanner": {"installed_version": metadata.get("scanner_version"), "policy_setting": metadata.get("policy")}}
    summary = combined_dir / "combined_report.md"
    if summary.is_file():
        inputs["combined_report.md"] = summary
    return Source(kind="combined", report_id=combined_dir.name, db_tag=combined_dir.parent.parent.name, folder=combined_dir,
                  metadata=metadata, scans=scans, findings=findings, comparisons=frames["comparisons"], template=frames["template"],
                  configurations=configs or _configurations({}, scans), inputs=inputs,
                  figures=sorted((combined_dir / "figures").glob("*.png")), summary_md=summary if summary.is_file() else None,
                  member_runs=members)


def discover(cisco_root):
    """(run folders, combined folders, legacy folders) under results/cisco_dataset_runs."""
    cisco_root = Path(cisco_root)
    runs, combined, legacy = [], [], []
    for meta in sorted(cisco_root.glob("*/runs/*/run_metadata.json")):
        runs.append(meta.parent)
    for meta in sorted(cisco_root.glob("*/combined/*/combined_metadata.json")):
        combined.append(meta.parent)
    for meta in sorted(cisco_root.glob("*/run_metadata.json")):
        try:
            if not json.loads(meta.read_text(encoding="utf-8")).get("run_id"):
                legacy.append(meta.parent)
        except json.JSONDecodeError:
            legacy.append(meta.parent)
    return runs, combined, legacy


# ---------------------------------------------------------------- human validation

@dataclass
class Review:
    folder: Path
    metadata: dict
    items: pd.DataFrame          # one row per review_id, with validation_tier
    files: dict                  # name -> Path of the worksheet files
    match: str                   # why this worksheet belongs to the run


TIER_LABELS = {
    "human_validated": "Human-validated",
    "provisional": "Provisional label (AI-assisted, not independent human review)",
    "awaiting_review": "Scanner alert, awaiting human review",
    "not_in_review": "Scanner alert, not in the review queue",
}
TIER_ORDER = list(TIER_LABELS)


def _filled(series):
    return series.notna() & series.astype(str).str.strip().ne("") & series.astype(str).str.lower().ne("nan")


def find_review(source, root):
    """The manual-review worksheet built from this run: same run ID, or the same manual_review_template.csv bytes
    (so a reanalysis with identical review IDs shares the worksheet of its source scan)."""
    template = source.inputs.get("manual_review_template.csv")
    template_sha = sha256_of(template) if template else None
    for meta_path in sorted((Path(root) / "results" / "manual_review").glob("*/worksheet_metadata.json")):
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        pinned = ((metadata.get("inputs") or {}).get("manual_review_template") or {}).get("sha256")
        if metadata.get("source_run_id") == source.report_id:
            match = "worksheet was generated from this run"
        elif template_sha and pinned == template_sha:
            match = (f"worksheet was generated from run {metadata.get('source_run_id')}; this run's "
                     "manual_review_template.csv is byte-identical (same SHA-256), so the review IDs are the same")
        else:
            continue
        folder = meta_path.parent
        files = {p.name: p for p in sorted(folder.glob("manual_review_worksheet*")) if p.suffix in (".csv", ".md")}
        files["worksheet_metadata.json"] = meta_path
        # The provisional CSV is the worksheet plus provisional_* columns; prefer it when present.
        csv = folder / "manual_review_worksheet_provisional.csv"
        csv = csv if csv.is_file() else folder / "manual_review_worksheet.csv"
        items = pd.read_csv(csv)
        tier = pd.Series("awaiting_review", index=items.index)
        if "provisional_label" in items:
            tier[_filled(items["provisional_label"])] = "provisional"
        if "final_label" in items:
            done = _filled(items["final_label"]) & (_filled(items["adjudicated_by"]) if "adjudicated_by" in items else True)
            tier[done] = "human_validated"
        items["validation_tier"] = tier
        items["worksheet_file"] = csv.name
        return Review(folder=folder, metadata=metadata, items=items, files=files, match=match)
    return None
