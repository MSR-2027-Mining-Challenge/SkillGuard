"""Run SkillGuard V1 over the Nov-3 Cisco 30-skill baseline, read-only.

Reproduce (from the repository root, with the project venv):

    .venv/bin/python -I results/skillguard_runs/sample30-seed2027/run_skillguard_sample30.py

What it does
  * Imports SkillGuard from src/skillguard_capabilities.py and calls scan() on
    each <skill>/full folder of the baseline run. Skill content is only read
    and parsed (ast / shlex); nothing from a skill is imported or executed.
  * Writes a NEW timestamped folder next to this script and refuses to reuse
    an existing one. Cisco results and the baseline folders are only read.
  * Joins SkillGuard findings to the Cisco Static/Behavioral findings of the
    same run (individual_findings.csv, scan_summary.csv) and to the manual
    gap-analysis candidates (results/gap_analysis/sample30-seed2027).

Matching rules (automatic, documented so they can be re-checked)
  * Only Cisco findings with finding_kind == "security" count as detections;
    metadata_quality (e.g. MANIFEST_MISSING_LICENSE) and scan_coverage rows
    are listed separately.
  * "Cisco at location": a Cisco security finding in the same skill + file whose
    reported line is within +/-LINE_WINDOW of the SkillGuard line, any of the
    four configurations.
  * "Cisco scanned file": SKILL.md counts as scanned if a SKILL.md-only
    configuration completed; other files only if a full-folder configuration
    completed (Cisco skipped full folders for skills with missing files).
  * Gap candidates: hand-transcribed expected locations (EXPECTED below),
    taken from candidate_classifications.csv. A location counts as detected if
    a SkillGuard finding of the listed capability falls inside its line range.

The manual false-positive / duplicate review is NOT produced here; it lives in
manual_review.csv in the run folder and is written separately by a reviewer.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BASELINE = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027"
GAP = REPO / "results/gap_analysis/sample30-seed2027/candidate_classifications.csv"
SKILLGUARD_SRC = REPO / "src/skillguard_capabilities.py"
SKILLGUARD_TESTS = REPO / "tests/test_skillguard_capabilities.py"
LINE_WINDOW = 3

sys.path.insert(0, str(REPO / "src"))
import skillguard_capabilities as sg  # noqa: E402

# Gap candidates whose behavior belongs to a SkillGuard V1 capability family.
# Everything else in candidate_classifications.csv is outside V1's scope.
EXPECTED = [
    # (candidate, capability, file, (start, end), note)
    ("G01", "scheduler_invocation", "scripts/set_reminder.py", (128, 133), "crontab -l / crontab - in the bundled script"),
    ("G01", "scheduler_invocation", "scripts/set_reminder.py", (47, 51), "crontab calls inside the generated-script template string"),
    ("G05", "agent_config_modification", "scripts/run_eval.py", (126, 158), "create/write temp SKILL.md in agent skill dirs"),
    ("G05", "agent_config_modification", "scripts/run_eval.py", (205, 218), "cleanup of the temp skill"),
    ("G06", "nested_agent_invocation", "scripts/run_eval.py", (170, 191), "agent -p --trust / claude -p / opencode run"),
    ("G06", "nested_agent_invocation", "scripts/run_loop.py", (175, 198), "agent -p / claude -p / opencode run"),
    ("G07", "agent_env_marker_removal", "scripts/run_eval.py", (182, 186), "drop CLAUDECODE/OPENCODE/... to allow nesting"),
    ("G07", "agent_env_marker_removal", "scripts/run_loop.py", (186, 190), "drop CLAUDECODE/OPENCODE/... to allow nesting"),
    ("G11", "scheduler_invocation", "SKILL.md", (128, 128), "agent cronjob(action='create', ...) in prose / inline code"),
    ("G11", "scheduler_invocation", "SKILL.md", (357, 357), "agent cron pattern in prose"),
    ("G11", "scheduler_invocation", "SKILL.md", (395, 395), "cronjob(no_agent=true, script=...) in prose"),
]
EXPECTED_SKILL = {"G01": "set-reminder-7652ed9105a8", "G05": "skill-creator-484c59f65787",
                  "G06": "skill-creator-484c59f65787", "G07": "skill-creator-484c59f65787",
                  "G11": "youtube-content-7162d1c45997"}


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False).stdout.strip()
    except OSError:
        return ""


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in row.items()})


def source_line(folder, rel, line):
    try:
        lines = (folder / rel).read_text(encoding="utf-8").splitlines()
        return lines[line - 1].strip()[:200] if 0 < line <= len(lines) else ""
    except (OSError, UnicodeError):
        return ""


def load_cisco():
    findings = defaultdict(list)  # (skill, file) -> [(line or None, rule, config, severity, analyzer)]
    with (BASELINE / "individual_findings.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            line = row["reported_line_number"]
            findings[(row["skill_id"], row["file_path"])].append(
                (int(line) if line.strip().isdigit() else None, row["rule_id"], row["configuration"],
                 row["severity"], row["finding_kind"]))
    status = {}
    with (BASELINE / "scan_summary.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            status[(row["skill_id"], row["configuration"])] = row["status"]
    return findings, status


def cisco_scanned(status, skill, rel):
    configs = ["SKILL.md only | default", "SKILL.md only | behavioral"] if rel == "SKILL.md" else []
    configs += ["Full folder | default", "Full folder | behavioral"]
    done = [c for c in configs if status.get((skill, c)) in {"COMPLETE", "PARTIAL"}]
    return done


def dedent_sensitivity(folder, rel, line):
    """Re-parse a Markdown Python block after textwrap.dedent (analysis only)."""
    source = (folder / rel).read_text(encoding="utf-8")
    for language, body, first_line in sg._markdown_blocks(source):
        if language in sg.PYTHON_TAGS and first_line <= line < first_line + body.count("\n") + 1:
            try:
                hits = sg._analyze_python(textwrap.dedent(body), first_line, "markdown_python_example", rel)
                return "parses_after_dedent", len(hits)
            except SyntaxError:
                return "still_fails_after_dedent", 0
    return "block_not_found", 0


def main():
    started = dt.datetime.now().astimezone()
    out = Path(__file__).resolve().parent / f"{started:%Y-%m-%d_%H%M%S}_skillguard-v1"
    out.mkdir(parents=False, exist_ok=False)
    (out / "raw").mkdir()

    cisco, cisco_status = load_cisco()
    skills = sorted(p.parent for p in BASELINE.glob("*/manifest.json"))

    finding_rows, coverage_rows, skill_rows, input_hashes, sensitivity_rows = [], [], [], [], []
    for skill_dir in skills:
        skill = skill_dir.name
        manifest = json.loads((skill_dir / "manifest.json").read_text(encoding="utf-8"))
        full = skill_dir / "full"
        present = sorted(p for p in full.rglob("*") if p.is_file())
        for p in present:
            input_hashes.append({"skill_id": skill, "file": p.relative_to(full).as_posix(), "sha256": sha256_file(p)})

        result = sg.scan(full)
        (out / "raw" / f"{skill}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

        for item in result["coverage"]:
            row = {"skill_id": skill, **{k: item.get(k, "") for k in ("file", "status", "carrier", "first_line", "line")},
                   "skipped_fences": item.get("skipped_fences", ""),
                   "is_limitation": item["status"] not in {"analyzed", "analyzed_with_skipped_fences"}}
            coverage_rows.append(row)
            if item["status"] == "parse_error":
                verdict, hits = dedent_sensitivity(full, item["file"], item["line"])
                sensitivity_rows.append({"skill_id": skill, "file": item["file"], "line": item["line"],
                                         "dedent_result": verdict, "findings_after_dedent": hits})
        for missing in manifest.get("missing_files", []):
            coverage_rows.append({"skill_id": skill, "file": missing, "status": "missing_from_snapshot",
                                  "is_limitation": True})

        for f in result["findings"]:
            d = f["details"]
            near, same_file, non_security = [], set(), set()
            for c_line, rule, config, sev, kind in cisco.get((skill, f["file"]), []):
                if kind != "security":  # metadata_quality / scan_coverage notes are not detections
                    non_security.add(rule)
                    continue
                same_file.add(rule)
                if c_line is not None and abs(c_line - f["line"]) <= LINE_WINDOW:
                    near.append(f"{rule}@{c_line} [{config}]")
            scanned = cisco_scanned(cisco_status, skill, f["file"])
            if not scanned:
                relation = "cisco_did_not_scan_file"
            elif near:
                relation = "cisco_flagged_same_location"
            elif same_file:
                relation = "cisco_flagged_file_elsewhere"
            else:
                relation = "cisco_silent_on_file"
            gap_ids = sorted({cid for cid, cap, file, (a, b), _ in EXPECTED
                              if EXPECTED_SKILL[cid] == skill and file == f["file"] and cap == f["capability"]
                              and a <= f["line"] <= b})
            finding_rows.append({
                "skill_id": skill, "file": f["file"], "line": f["line"], "carrier": f["carrier"],
                "capability": f["capability"],
                "command": d.get("command", ""), "trust_flags": d.get("trust_flags", ""),
                "operation": d.get("operation", ""), "targets": d.get("targets", ""),
                "env_removed": d.get("removed", d.get("env_markers_removed", "")),
                "mechanism": d.get("mechanism", ""), "resolved_from": d.get("resolved_from", ""),
                "definition_lines": d.get("definition_lines", ""),
                "source_text": source_line(full, f["file"], f["line"]),
                "cisco_relation": relation, "cisco_at_location": near,
                "cisco_security_rules_same_file": sorted(same_file),
                "cisco_non_security_rules_same_file": sorted(non_security),
                "cisco_configs_scanned_file": scanned,
                "gap_candidates": gap_ids,
            })

        limits = sg.limitations(result)
        caps = Counter(f["capability"] for f in result["findings"])
        skill_rows.append({
            "skill_id": skill, "repo": manifest.get("repo", ""),
            "files_present": len(present), "files_missing_from_snapshot": len(manifest.get("missing_files", [])),
            "code_blocks_analyzed": sum(c["status"] == "analyzed" for c in result["coverage"]),
            "findings": len(result["findings"]),
            **{f"n_{k}": caps.get(k, 0) for k in ("nested_agent_invocation", "agent_config_modification",
                                                   "agent_env_marker_removal", "scheduler_invocation")},
            "limitations": len(limits),
            "limitation_breakdown": dict(Counter(c["status"] for c in limits)),
            "cisco_full_folder_default": cisco_status.get((skill, "Full folder | default"), ""),
            "cisco_full_folder_behavioral": cisco_status.get((skill, "Full folder | behavioral"), ""),
        })

    # Gap-candidate recall for in-scope candidates.
    recall_rows = []
    for cid, cap, file, (a, b), note in EXPECTED:
        hits = [r for r in finding_rows if r["skill_id"] == EXPECTED_SKILL[cid] and r["file"] == file
                and r["capability"] == cap and a <= r["line"] <= b]
        recall_rows.append({"candidate": cid, "skill_id": EXPECTED_SKILL[cid], "file": file, "lines": f"{a}-{b}",
                            "capability": cap, "note": note, "detected": bool(hits),
                            "skillguard_lines": sorted({r["line"] for r in hits})})

    finding_fields = list(finding_rows[0].keys()) if finding_rows else ["skill_id"]
    write_csv(out / "findings.csv", finding_rows, finding_fields)
    write_csv(out / "coverage.csv", coverage_rows,
              ["skill_id", "file", "status", "carrier", "first_line", "line", "skipped_fences", "is_limitation"])
    write_csv(out / "per_skill_summary.csv", skill_rows, list(skill_rows[0].keys()))
    write_csv(out / "gap_candidate_recall.csv", recall_rows, list(recall_rows[0].keys()))
    write_csv(out / "parse_error_dedent_sensitivity.csv", sensitivity_rows,
              ["skill_id", "file", "line", "dedent_result", "findings_after_dedent"])
    write_csv(out / "input_file_hashes.csv", input_hashes, ["skill_id", "file", "sha256"])

    limits = [r for r in coverage_rows if r["is_limitation"]]
    metadata = {
        "run_id": out.name,
        "started_at": started.isoformat(),
        "finished_at": dt.datetime.now().astimezone().isoformat(),
        "baseline_run": str(BASELINE.relative_to(REPO)),
        "skills_scanned": len(skills),
        "skillguard": {"source": str(SKILLGUARD_SRC.relative_to(REPO)), "sha256": sha256_file(SKILLGUARD_SRC),
                       "tests_sha256": sha256_file(SKILLGUARD_TESTS),
                       "uncommitted_changes": bool(git("status", "--porcelain", "--", str(SKILLGUARD_SRC)))},
        "git_head": git("rev-parse", "HEAD"),
        "python": platform.python_version(),
        "runner_sha256": sha256_file(Path(__file__)),
        "line_window": LINE_WINDOW,
        "totals": {
            "findings": len(finding_rows),
            "skills_with_findings": len({r["skill_id"] for r in finding_rows}),
            "findings_by_capability": dict(Counter(r["capability"] for r in finding_rows)),
            "findings_by_carrier": dict(Counter(r["carrier"] for r in finding_rows)),
            "findings_by_cisco_relation": dict(Counter(r["cisco_relation"] for r in finding_rows)),
            "files_present": len(input_hashes),
            "coverage_limitations": len(limits),
            "limitations_by_status": dict(Counter(r["status"] for r in limits)),
            "skills_with_missing_files": sum(1 for r in skill_rows if r["files_missing_from_snapshot"]),
        },
        "executed_skill_code": False,
    }
    (out / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata["totals"], indent=2))
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
