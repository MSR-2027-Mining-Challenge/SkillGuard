"""Finding normalization shared with notebook 01 (Sections 8-9), so LLM/Meta scans are classified exactly like the baseline.

The constants and functions below are copied from notebooks/01_cisco_scanner_dataset_ready.ipynb (cells "Section 8" and
"Section 9"). tests/test_llm_meta.py executes those notebook cells and fails if the two copies drift apart, and checks
that flattening the saved baseline reports here reproduces the baseline individual_findings.csv.
"""

import hashlib
import json
import re
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------- scan status (notebook 01, Section 8)

STATUS_OUTCOME = {"COMPLETE": "complete", "CONTRACT_ONLY": "contract_only", "PARTIAL": "partial",
                  "SKIPPED_INCOMPLETE_FOLDER": "excluded_incomplete_folder", "MISSING_REPORT": "missing"}
NOT_EXECUTED_STATUSES = ("SKIPPED_INCOMPLETE_FOLDER", "MISSING_REPORT", "EXPORT_ERROR")
KNOWN_CONTRACT_CODES = {"UNKNOWN_BUNDLED_PYTHON_RULE"}


def outcome_of(status):
    return STATUS_OUTCOME.get(status, "failed")


def validate_report(obj):
    """Return None if `obj` looks like a Cisco single-skill report, otherwise a short reason."""
    if not isinstance(obj, dict):
        return "top level is not a JSON object"
    for key, expected_type in (("findings", list), ("is_safe", bool), ("max_severity", str)):
        if not isinstance(obj.get(key), expected_type):
            return f"missing or wrong type for '{key}'"
    return None


def is_known_contract_issue(entry):
    error = str(entry.get("error", ""))
    if not error.startswith("FindingContract:"):
        return False
    codes = {code.strip() for code in error.rsplit(":", 1)[-1].split(",") if code.strip()}
    return bool(codes) and codes <= KNOWN_CONTRACT_CODES


def failure_type(entry):
    error = str(entry.get("error", ""))
    if is_known_contract_issue(entry):
        return "finding contract: unregistered rule (known Cisco issue)"
    if error.startswith("FindingContract:"):
        return "finding contract: other violation"
    if entry.get("analyzer") == "skill_loader":
        return "skill loader"
    return "analyzer error"


def assess_report(report, cfg, exit_code=None):
    """Classify one parsed report: (status, reasons, analyzer_failures). Same rules as notebook 01."""
    problem = validate_report(report)
    if problem:
        return "FAILED_INVALID_FORMAT", [problem], []
    contract_reasons, other_reasons, failures = [], [], []
    for entry in report.get("analyzers_failed") or []:
        error = str(entry.get("error", ""))
        failures.append({"analyzer": entry.get("analyzer"), "error": entry.get("error"), "type": failure_type(entry),
                         "rule_id": error.split(":")[1] if error.startswith("FindingContract:") else None})
        reason = f"Cisco reported an analyzer failure ({entry.get('analyzer')}: {error})"
        (contract_reasons if is_known_contract_issue(entry) else other_reasons).append(reason)
    contract = (report.get("scan_metadata") or {}).get("rule_contract") or {}
    if contract.get("status") == "failed" and not any(str(f["error"]).startswith("FindingContract:") for f in failures):
        other_reasons.append(f"Cisco rule-contract check failed for {contract.get('invalid_findings')} finding(s)")
    not_run = sorted(set(cfg["required_analyzers"]) - set(report.get("analyzers_used") or []))
    if not_run:
        other_reasons.append(f"requested analyzer(s) missing from analyzers_used: {not_run}")
    if any(isinstance(f, dict) and f.get("rule_id") == "LLM_ANALYSIS_FAILED" for f in report["findings"]):
        other_reasons.append("the LLM analyzer could not review the skill (LLM_ANALYSIS_FAILED)")
    if exit_code not in (None, 0):
        other_reasons.append(f"scanner exit code {exit_code}")
    if other_reasons:
        status = "PARTIAL"
    elif contract_reasons:
        status = "CONTRACT_ONLY"
    else:
        status = "COMPLETE"
    return status, contract_reasons + other_reasons, failures


# ---------------------------------------------------------------- research classification (notebook 01, Section 9)

METADATA_QUALITY_RULES = {
    "MANIFEST_MISSING_LICENSE", "MANIFEST_INVALID_NAME", "MANIFEST_DESCRIPTION_TOO_LONG", "MANIFEST_METADATA_INCOMPLETE",
    "MISSING_STRUCTURED_METADATA", "INVALID_STRUCTURED_METADATA", "MALFORMED_YAML_FRONTMATTER",
    "SKILL_METADATA_SIZE_LIMIT_EXCEEDED", "SOCIAL_ENG_VAGUE_DESCRIPTION",
    "TRIGGER_VAGUE_DESCRIPTION", "TRIGGER_OVERLY_GENERIC", "TRIGGER_DESCRIPTION_TOO_SHORT",
}
SCAN_COVERAGE_RULES = {
    "LOW_ANALYZABILITY", "UNANALYZABLE_BINARY", "BINARY_FILE_DETECTED", "ARCHIVE_FILE_DETECTED", "PYCACHE_FILES_DETECTED",
    "OVERSIZED_FILE", "EXCESSIVE_FILE_COUNT", "SKILL_LOAD_FALLBACK_USED", "SKILL_LOAD_FAILED", "SKILL_LOAD_REJECTED_LIMIT",
    "SYMLINK_NOT_SCANNED", "UNICODE_ANALYSIS_INCOMPLETE", "BEHAVIOR_DATAFLOW_ANALYSIS_INCOMPLETE",
    "BYTECODE_ANALYSIS_UNAVAILABLE", "ARCHIVE_EXTRACTION_FAILED",
    "LLM_ANALYSIS_FAILED", "LLM_CONTEXT_BUDGET_EXCEEDED", "META_CONTEXT_BUDGET_EXCEEDED",
}

RESEARCH_CATEGORIES = [
    "Credential / secret access or exposure",
    "External network communication / data exfiltration",
    "Command execution / dangerous shell operations",
    "File-system access or modification",
    "Prompt injection / instruction manipulation",
    "Excessive permissions / privilege escalation",
    "Supply-chain / dependency risks",
    "Account modification / sensitive external actions",
]
RESEARCH_CATEGORY_BY_CISCO_CATEGORY = {
    "hardcoded_secrets": RESEARCH_CATEGORIES[0],
    "data_exfiltration": RESEARCH_CATEGORIES[1],
    "command_injection": RESEARCH_CATEGORIES[2],
    "prompt_injection": RESEARCH_CATEGORIES[4],
    "unicode_steganography": RESEARCH_CATEGORIES[4],
    "social_engineering": RESEARCH_CATEGORIES[4],
    "unauthorized_tool_use": RESEARCH_CATEGORIES[5],
    "autonomy_abuse": RESEARCH_CATEGORIES[5],
    "tool_chaining_abuse": RESEARCH_CATEGORIES[5],
    "transitive_trust_abuse": RESEARCH_CATEGORIES[5],
    "skill_discovery_abuse": RESEARCH_CATEGORIES[5],
    "supply_chain_attack": RESEARCH_CATEGORIES[6],
}
RESEARCH_CATEGORY_BY_RULE_PREFIX = {
    "SECRET_": RESEARCH_CATEGORIES[0],
    "DATA_EXFIL_SENSITIVE_FILE": RESEARCH_CATEGORIES[0],
    "DATA_EXFIL_ENV": RESEARCH_CATEGORIES[0],
    "BEHAVIOR_CREDENTIAL_FILE_ACCESS": RESEARCH_CATEGORIES[0],
    "BEHAVIOR_ENV_VAR_HARVESTING": RESEARCH_CATEGORIES[0],
    "PATH_TRAVERSAL": RESEARCH_CATEGORIES[3],
    "GLOB_HIDDEN_FILE_TARGETING": RESEARCH_CATEGORIES[3],
    "PIPELINE_TAINT_FLOW": RESEARCH_CATEGORIES[2],
    "MDBLOCK_PYTHON_SUBPROCESS": RESEARCH_CATEGORIES[2],
    "MDBLOCK_PYTHON_EVAL_EXEC": RESEARCH_CATEGORIES[2],
    "BEHAVIOR_EVAL_SUBPROCESS": RESEARCH_CATEGORIES[2],
    "BEHAVIOR_BASH_TAINT_FLOW": RESEARCH_CATEGORIES[2],
    "SUPPLY_CHAIN_": RESEARCH_CATEGORIES[6],
    "TOOL_ABUSE_SYSTEM_PACKAGE_INSTALL": RESEARCH_CATEGORIES[6],
    "TOOL_ABUSE_UNTRUSTED_PACKAGE_SOURCE": RESEARCH_CATEGORIES[6],
}


def classify_finding_kind(rule_id):
    if rule_id in METADATA_QUALITY_RULES:
        return "metadata_quality"
    if rule_id in SCAN_COVERAGE_RULES:
        return "scan_coverage"
    return "security"


def research_category(rule_id, cisco_category):
    for prefix in sorted(RESEARCH_CATEGORY_BY_RULE_PREFIX, key=len, reverse=True):
        if str(rule_id).startswith(prefix):
            return RESEARCH_CATEGORY_BY_RULE_PREFIX[prefix]
    return RESEARCH_CATEGORY_BY_CISCO_CATEGORY.get(cisco_category, f"Other ({cisco_category})")


SECRET_PATTERNS = [
    (re.compile(r"(?i)((?:password|passwd|secret|token|api[_-]?key|access[_-]?key)\w*['\"]?\s*[=:]\s*)(['\"])([^'\"\s]{4,})\2"), r"\1\2[REDACTED]\2"),
    (re.compile(r"(?i)((?:password|passwd|secret|token|api[_-]?key)\w*\s*=\s*)(?![$%{(])([A-Za-z0-9_\-/+]{8,})(?![\w.(\[])"), r"\1[REDACTED]"),
    (re.compile(r"(://[^/\s:@]+:)[^@\s]+@"), r"\1[REDACTED]@"),
    (re.compile(r"\b(AKIA|ASIA|ghp_|gho_|github_pat_|xox[bap]-|AIza|sk-)[A-Za-z0-9_\-]{8,}"), r"\1[REDACTED]"),
]


def redact(text):
    if not isinstance(text, str):
        return text
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def normalize_file_path(raw_path, report_root, scanned_folder):
    """Return (path relative to the scanned folder or None, note). The raw Cisco value is stored separately."""
    if not raw_path:
        return None, "no file reported"
    path = Path(raw_path)
    if not path.is_absolute():
        return path.as_posix(), "relative path as reported"
    for base in (report_root, scanned_folder):
        if not base:
            continue
        for candidate_base, candidate_path in ((Path(base), path), (Path(base).resolve(), path.resolve())):
            try:
                return candidate_path.relative_to(candidate_base).as_posix(), "absolute path made relative to the scanned folder"
            except ValueError:
                pass
    return raw_path, "absolute path outside the scanned folder (kept as reported)"


MASK = re.compile(r"\*{4,}")


def collapse_whitespace(text):
    return re.sub(r"\s+", " ", text.strip())


def verify_evidence(file_path, reported_line, evidence, scanned_folder):
    """Look for Cisco's evidence text in the exported file. Returns (status, detail, candidate_lines)."""
    if file_path is None or Path(file_path).is_absolute():
        return "unavailable", "no file (inside the scanned folder) reported", ""
    path = Path(scanned_folder) / file_path
    if not path.is_file():
        return "unavailable", "reported file is not in the exported folder", ""
    lines = [collapse_whitespace(line) for line in path.read_text(encoding="utf-8", errors="replace").splitlines()]
    has_line = reported_line is not None and not pd.isna(reported_line)
    if not isinstance(evidence, str) or not evidence.strip():
        where = f"; reported line {reported_line} exists" if has_line and 1 <= reported_line <= len(lines) else ""
        return "unavailable", "no evidence text" + where, ""

    evidence_lines = [line for line in evidence.splitlines() if line.strip()]
    first = re.sub(r"(\.\.\.|…)$", "", collapse_whitespace(evidence_lines[0])).strip()
    pieces = MASK.split(first)
    pattern = re.compile(".*?".join(re.escape(piece) for piece in pieces))
    literal_chars = sum(len(piece.strip()) for piece in pieces)
    candidates = [number for number, line in enumerate(lines, start=1) if pattern.search(line)]
    shown = ", ".join(map(str, candidates[:10])) + (" ..." if len(candidates) > 10 else "")
    note = " (first line of a multi-line snippet checked)" if len(evidence_lines) > 1 else ""

    if not has_line:
        return "unavailable", f"no line number reported; evidence occurs on {len(candidates)} line(s){note}", shown
    reported_line = int(reported_line)
    if not 1 <= reported_line <= len(lines):
        return "mismatch", f"reported line {reported_line} is past the end of the file ({len(lines)} lines){note}", shown
    if literal_chars < 6:
        return "ambiguous", f"evidence text too short to identify a line{note}", shown
    if reported_line in candidates:
        return "exact", f"evidence on the reported line{note}", shown
    if not candidates:
        return "mismatch", f"evidence text not found in the file{note}", shown
    if len(candidates) == 1:
        return "mismatch", f"evidence not on the reported line; it occurs only on line {candidates[0]}{note}", shown
    return "ambiguous", f"evidence not on the reported line; it occurs on {len(candidates)} other lines{note}", shown


METADATA_FIELDS_TO_KEEP = ["matched_text", "matched_pattern", "signature_context", "scanner_category", "aitech", "aitech_name",
                           "aisubtech", "aisubtech_name", "files_involved", "evidence", "from_code_block", "block_language",
                           "deduped_rule_ids", "threat_type"]
FINDING_COLUMNS = (["skill_id", "repo", "skill_path", "sample_stratum", "configuration", "scope", "analyzer_mode", "run_status", "run_outcome",
                    "finding_id", "rule_id", "cisco_category", "severity", "analyzer", "title", "description",
                    "reported_file_path", "reported_line_number", "file_path", "path_note", "location",
                    "snippet", "snippet_redacted", "evidence_source", "evidence_status", "evidence_detail", "evidence_candidate_lines",
                    "remediation", "cisco_rule_contract", "finding_kind", "research_category", "location_key", "finding_key"]
                   + [f"meta_{name}" for name in METADATA_FIELDS_TO_KEEP] + ["metadata_json"])

# Extra columns for LLM / Meta-Analyzer provenance (not in notebook 01). They are appended after FINDING_COLUMNS so the
# baseline columns keep their order. "meta_*" metadata keys written by Cisco's apply_meta_analysis_to_results().
LLM_META_COLUMNS = ["llm_model", "llm_verdict", "llm_confidence", "meta_false_positive", "meta_reason", "meta_confidence",
                    "meta_validated", "meta_detected", "meta_priority", "meta_analysis_degraded", "post_meta_visible"]


def as_cell_value(value):
    return json.dumps(value, sort_keys=True) if isinstance(value, (list, dict)) else value


def describe_location(file_path):
    if file_path is None:
        return "whole skill (no file)"
    return "SKILL.md" if file_path == "SKILL.md" else "supporting file"


def flatten_findings(report, run, scanned_folder):
    """One flat row per finding in `report` (identical to notebook 01), plus the LLM/Meta provenance columns."""
    rows = []
    for finding in report["findings"]:
        if not isinstance(finding, dict):
            continue
        meta = finding.get("metadata") or {}
        raw_path, raw_line = finding.get("file_path"), finding.get("line_number")
        file_path, path_note = normalize_file_path(raw_path, report.get("skill_path"), scanned_folder)
        if finding.get("snippet"):
            evidence, evidence_source = finding["snippet"], "snippet"
        elif meta.get("matched_text"):
            evidence, evidence_source = meta["matched_text"], "matched_text"
        else:
            evidence, evidence_source = None, "none"
        status, detail, candidates = verify_evidence(file_path, raw_line, evidence, scanned_folder)
        location_key = f"{finding.get('rule_id')}|{file_path}|{raw_line}"
        snippet = finding.get("snippet")
        row = {
            "skill_id": run["skill_id"], "repo": run["repo"], "skill_path": run["skill_path"], "sample_stratum": run["sample_stratum"],
            "configuration": run["configuration"], "scope": run["scope"], "analyzer_mode": run["analyzer_mode"],
            "run_status": run["status"], "run_outcome": run["outcome"],
            "finding_id": finding.get("id"), "rule_id": finding.get("rule_id"), "cisco_category": finding.get("category"),
            "severity": finding.get("severity"), "analyzer": finding.get("analyzer"),
            "title": finding.get("title"), "description": redact(finding.get("description")),
            "reported_file_path": raw_path, "reported_line_number": raw_line,
            "file_path": file_path, "path_note": path_note, "location": describe_location(file_path),
            "snippet": redact(snippet), "snippet_redacted": isinstance(snippet, str) and redact(snippet) != snippet,
            "evidence_source": evidence_source, "evidence_status": status, "evidence_detail": detail,
            "evidence_candidate_lines": candidates,
            "remediation": finding.get("remediation"), "cisco_rule_contract": (meta.get("rule_contract") or {}).get("status"),
            "finding_kind": classify_finding_kind(finding.get("rule_id")),
            "research_category": research_category(finding.get("rule_id"), finding.get("category")),
            "location_key": location_key,
            "finding_key": f"{location_key}|{hashlib.sha256(str(evidence).encode()).hexdigest()[:10]}",
            "metadata_json": json.dumps(meta, sort_keys=True, default=str),
        }
        for name in METADATA_FIELDS_TO_KEEP:
            row[f"meta_{name}"] = as_cell_value(meta.get(name))
        row.update({
            "llm_model": meta.get("model") or meta.get("llm_model"), "llm_verdict": meta.get("llm_verdict"),
            "llm_confidence": meta.get("llm_confidence"), "meta_false_positive": meta.get("meta_false_positive"),
            "meta_reason": redact(meta.get("meta_reason")), "meta_confidence": meta.get("meta_confidence"),
            "meta_validated": meta.get("meta_validated"), "meta_detected": meta.get("meta_detected"),
            "meta_priority": meta.get("meta_priority"), "meta_analysis_degraded": meta.get("meta_analysis_degraded"),
            # What Cisco shows without --verbose: everything the Meta-Analyzer did not mark as a false positive.
            "post_meta_visible": meta.get("meta_false_positive") is not True,
        })
        rows.append(row)
    return rows
