"""Systematic search of an LLM/Meta run's exported skill files for security-relevant behaviors, mapped to Cisco findings.

This is an audit aid for the gap analysis (docs/cisco_security_gap_analysis.md), not a detector: the patterns are broad
on purpose and every hit still needs reading. Nothing is executed; files are read as text.

    PYTHONPATH=src .venv/bin/python -m gitskills_cisco_llm.gap_search <run folder> [--out results/gap_analysis/<name>]

Writes pattern_hits.csv (one row per file line x behavior family) with, for each hit, whether Cisco reported anything
at that location in any of the run's configurations (deterministic: same file within +-LINE_TOLERANCE lines; LLM/Meta:
same file, because their findings carry no line numbers).
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from .rules import redact

LINE_TOLERANCE = 2
TEXT_SUFFIXES = {".py", ".sh", ".bash", ".js", ".mjs", ".ts", ".md", ".yaml", ".yml", ".json", ".toml", ".html", ".txt"}
CODE_SUFFIXES = {".py", ".sh", ".bash", ".js", ".mjs", ".ts"}

# Behavior families. Broad regexes; precision comes from reading each hit (candidate_classifications.csv).
FAMILIES = {
    "process_execution": r"subprocess\.(?:run|Popen|call|check_output|check_call)\b|\bos\.(?:system|popen|exec[lv]p?e?)\b|"
                         r"child_process|execSync|spawnSync|\bshell\s*=\s*True",
    "dynamic_code_execution": r"(?<![\w.])(?:exec|eval|compile)\s*\(|__import__\s*\(|new Function\(",
    "scheduler_persistence": r"\bcrontab\b|\bcronjob\s*\(|\blaunchctl\b|\bschtasks\b|systemctl\s+enable|@reboot",
    "executable_file_creation": r"\bchmod\s+\+?[0-7]*x|\.chmod\(|S_IEXEC|S_IX(?:GRP|OTH)",
    "self_or_artifact_deletion": r"unlink\(__file__|Path\(__file__\)\.unlink|os\.remove\(__file__|rm\s+-f\s+\"?\$0|"
                                 r"\.unlink\(|os\.remove\(|shutil\.rmtree|\brm\s+-rf\b",
    "agent_cli_invocation": r"[\"'](?:claude|agent|codex|opencode|gemini)[\"']\s*,\s*[\"'](?:-p|exec|run)[\"']|"
                            r"\b(?:claude|codex|gemini)\s+-p\b|opencode\s+run|--trust\b|--dangerously|--yolo\b|"
                            r"--full-auto|skip-permissions|--permission-mode",
    "agent_config_write": r"\.claude[/\"' ]|\.cursor[/\"' ]|\.codex[/\"' ]|available_skills|\.claude/commands",
    "env_manipulation": r"os\.environ\.items\(\)|CLAUDECODE|OPENCODE_PID|CURSOR_API_KEY",
    "network_client": r"urllib\.request|urlopen|requests\.(?:get|post|put|delete|request|Session)|httpx|aiohttp|"
                      r"\bfetch\(|axios|http\.client|Elasticsearch\(|\[['\"]curl['\"]|\bcurl\s+-|\bwget\s",
    "network_listener": r"HTTPServer|ThreadingHTTPServer|\.listen\(|--host\s+0\.0\.0\.0|[\"']0\.0\.0\.0[\"']|"
                        r"http\.server|createServer\(",
    "process_termination": r"os\.kill\(|\bkill\s+-9|pkill\b|killall\b|lsof\s+-ti|[\"']lsof[\"']",
    "secret_or_env_read": r"os\.environ\.get|getenv\(|process\.env|\.env\b|API_KEY|_TOKEN\b|\.ssh/|keychain",
    "package_install": r"pip3?\s+install|npm\s+(?:i|install)\b|npx\s|uvx\s|brew\s+install|apt(?:-get)?\s+install|"
                       r"--break-system-packages|git\s+clone",
    "approval_or_control_bypass": r"without\s+(?:asking|prompting|confirmation|user)|no user present|"
                                  r"is blocked in cron|blocked by `?cron_mode|auto-?approve|bypass|"
                                  r"do not ask|skip (?:the )?confirmation|Hard Activation",
}
COMPILED = {name: re.compile(rx, re.I) for name, rx in FAMILIES.items()}


def _line_kinds(path, lines):
    """Per line: 'code' for code files, 'md_code_block' inside ``` fences, 'md_prose' otherwise, 'data' for configs."""
    suffix = path.suffix.lower()
    if suffix in CODE_SUFFIXES:
        return ["code"] * len(lines)
    if suffix != ".md":
        return ["data"] * len(lines)
    kinds, inside = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            kinds.append("md_code_block")
            inside = not inside
            continue
        kinds.append("md_code_block" if inside else "md_prose")
    return kinds


def search(run_dir):
    run_dir = Path(run_dir)
    rows = []
    for skill_dir in sorted(p for p in run_dir.iterdir() if (p / "manifest.json").is_file()):
        manifest = json.loads((skill_dir / "manifest.json").read_text(encoding="utf-8"))
        root = skill_dir / "full"
        for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES):
            rel = path.relative_to(root).as_posix()
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            kinds = _line_kinds(path, lines)
            for number, (line, kind) in enumerate(zip(lines, kinds), start=1):
                for family, rx in COMPILED.items():
                    if rx.search(line):
                        rows.append({"skill_id": skill_dir.name, "sample_stratum": manifest.get("sample_stratum"),
                                     "file_path": rel, "line": number, "line_kind": kind, "family": family,
                                     "text": redact(line.strip())[:240],
                                     "folder_complete": manifest.get("folder_complete"),
                                     "scanned_scopes": "SKILL.md only + Full folder" if rel == "SKILL.md" and manifest.get("folder_complete")
                                     else "SKILL.md only (full folder excluded: incomplete)" if rel == "SKILL.md"
                                     else "Full folder" if manifest.get("folder_complete") else "not scanned (folder incomplete)"})
    return pd.DataFrame(rows)


def map_to_cisco(hits, findings):
    """Attach what Cisco reported at / near each hit, across all configurations of the run."""
    det = findings[~findings["analyzer"].isin(["llm", "meta"]) & findings["finding_kind"].ne("metadata_quality")]
    sem = findings[findings["analyzer"].isin(["llm", "meta"]) & findings["finding_kind"].eq("security")]
    out = []
    for h in hits.to_dict("records"):
        d = det[(det["skill_id"] == h["skill_id"]) & (det["file_path"] == h["file_path"])]
        near = d[(d["reported_line_number"] - h["line"]).abs() <= LINE_TOLERANCE]
        s = sem[(sem["skill_id"] == h["skill_id"]) & (sem["file_path"] == h["file_path"])]
        h["cisco_det_at_line"] = "; ".join(sorted(set(near["rule_id"])))
        h["cisco_det_at_line_configs"] = "; ".join(sorted(set(near["analyzer_mode"])))
        h["cisco_det_same_file"] = "; ".join(sorted(set(d["rule_id"])))
        h["llm_meta_same_file"] = " | ".join(sorted(set(s["analyzer"] + ":" + s["rule_id"] + " (" + s["title"].astype(str) + ")")))[:400]
        out.append(h)
    return pd.DataFrame(out)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="gitskills_cisco_llm.gap_search")
    parser.add_argument("run_dir")
    parser.add_argument("--out", default="results/gap_analysis/sample30-seed2027")
    parser.add_argument("--publish", action="store_true",
                        help="also copy research_insights / candidate tables into the run's llm_meta_analysis/ for the report")
    args = parser.parse_args(argv)
    run_dir, out = Path(args.run_dir), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    findings = pd.read_csv(run_dir / "individual_findings.csv")
    hits = map_to_cisco(search(run_dir), findings)
    hits.to_csv(out / "pattern_hits.csv", index=False)
    summary = (hits.assign(cisco_at_line=hits["cisco_det_at_line"].ne(""))
               .groupby(["family", "line_kind"]).agg(hits=("line", "size"), skills=("skill_id", "nunique"),
                                                     with_cisco_det_at_line=("cisco_at_line", "sum")).reset_index())
    summary.to_csv(out / "pattern_hits_summary.csv", index=False)
    print(summary.to_string(index=False))
    print(f"{len(hits)} hits -> {out / 'pattern_hits.csv'}")
    if args.publish:
        publish(out, run_dir)


# Curated files (written by hand during the gap analysis) that the report shows in its LLM / Meta section.
PUBLISHED = {"research_insights.csv": "research_insights.csv", "candidate_classifications.csv": "gap_candidates.csv",
             "pattern_hits_summary.csv": "gap_pattern_summary.csv"}


def publish(out, run_dir):
    """Copy the gap-analysis tables into <run>/llm_meta_analysis/ so gitskills_reports includes them (new files only)."""
    target = Path(run_dir) / "llm_meta_analysis"
    for src_name, dst_name in PUBLISHED.items():
        src = Path(out) / src_name
        if src.is_file():
            (target / dst_name).write_bytes(src.read_bytes())
            print(f"published {src} -> {target / dst_name}")


if __name__ == "__main__":
    main()
