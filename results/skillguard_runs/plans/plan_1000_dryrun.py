"""Dry run for the planned 1,000-skill Cisco Static/Behavioral experiment. Launches NO scans.

    .venv/bin/python -I results/skillguard_runs/plans/plan_1000_dryrun.py

Reads only: the notebook-03 sampling frame (strata for all 13,000 representatives), the
GitSkills sample DB (read-only, for file sizes/extensions), the Nov-3 run's scan_summary.csv
(Cisco timings, 4 configurations), the fresh-100 Cisco run records and the V3 evaluation
per_skill.csv (SkillGuard timings), and the manifests of every sample used so far.
Writes dryrun_numbers.json next to this script.
"""

from __future__ import annotations

import csv
import glob
import json
import math
import sqlite3
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FRAME = REPO / "results/samples/agent_skills_sample_seed2027_scripts10_supporting_no_scripts10_skill_md_only10/sampling_frame.csv"
DB = REPO / "data/sample/agent_skills_sample.db"
NOV3 = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027"
FRESH = REPO / "results/skillguard_runs/heldout/2026-11-13_fresh100-seed2029"
EVAL = next(iter(sorted((REPO / "results/skillguard_runs/comparisons").glob("*fresh100*_v1-v2-v3-cisco"))))
STRATA = ["scripts", "supporting_no_scripts", "skill_md_only"]
ALLOCATIONS = {
    "A_recommended_disproportionate": {"scripts": 400, "supporting_no_scripts": 300, "skill_md_only": 300},
    "B_proportional": None,  # filled below
    "C_equal": {"scripts": 334, "supporting_no_scripts": 333, "skill_md_only": 333},
}
SUPPORTED = {".py", ".sh", ".bash", ".zsh", ".ps1", ".psm1", ".md", ".markdown"}


def moe(p, n, N):
    """95% margin of error for a proportion with finite-population correction."""
    if n <= 0:
        return None
    fpc = (N - n) / (N - 1) if N > 1 else 0
    return round(1.96 * math.sqrt(p * (1 - p) / n * fpc), 4)


def main():
    frame = list(csv.DictReader(FRAME.open(encoding="utf-8")))
    used = set()
    used_sources = [NOV3 / "sample/sample_manifest.csv"] + sorted((REPO / "results/skillguard_runs/heldout").glob("*/sample_manifest.csv"))
    for m in used_sources:
        used |= {r["file_sha"] for r in csv.DictReader(m.open(encoding="utf-8"))}

    by = defaultdict(lambda: Counter())
    files_listed = defaultdict(list)
    exclusions = Counter()
    eligible = defaultdict(list)
    for r in frame:
        s = r["stratum"]
        if s not in STRATA:
            exclusions[s] += 1
            continue
        by[s]["N"] += 1
        complete = r["folder_complete"] == "True"
        by[s]["complete"] += complete
        if r["file_sha"] in used:
            by[s]["previously_used"] += 1
            continue
        by[s]["available"] += 1
        by[s]["available_complete"] += complete
        files_listed[s].append(int(float(r["n_files_listed"] or 0)))
        eligible[s].append((r["repo"], r["skill_path"]))

    population = {s: dict(by[s]) for s in STRATA}
    total_N = sum(by[s]["N"] for s in STRATA)
    ALLOCATIONS["B_proportional"] = {s: round(1000 * by[s]["N"] / total_N) for s in STRATA}

    # File sizes and extension mix for eligible folders (supporting files only).
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    sib = defaultdict(list)
    for repo, apath, entry, etype, size in con.execute(
            "SELECT repo_full_name, artifact_path, entry_name, entry_type, entry_size FROM artifact_siblings WHERE entry_type='file'"):
        sib[(repo, apath)].append((entry, size or 0))
    ext_mix, bytes_per = {}, {}
    for s in STRATA:
        c, sizes = Counter(), []
        for key in eligible[s]:
            files = sib.get(key, [])
            sizes.append(sum(sz for _, sz in files))
            for entry, _ in files:
                ext = Path(entry).suffix.lower() or "(none)"
                c[ext] += 1
        total_files = sum(c.values())
        supported = sum(v for k, v in c.items() if k in SUPPORTED)
        ext_mix[s] = {"supporting_files": total_files,
                      "share_in_skillguard_code_or_text_formats": round(supported / total_files, 3) if total_files else None,
                      "top_extensions": dict(c.most_common(12))}
        bytes_per[s] = {"mean_supporting_bytes": round(statistics.mean(sizes)) if sizes else 0,
                        "median_supporting_bytes": round(statistics.median(sizes)) if sizes else 0,
                        "mean_files_listed": round(statistics.mean(files_listed[s]), 2) if files_listed[s] else 0}

    # Cisco timings: Nov-3 (4 configurations, notebook 01) and fresh-100 (2 full-folder configurations).
    t = defaultdict(list)
    for r in csv.DictReader((NOV3 / "scan_summary.csv").open(encoding="utf-8")):
        if r["wall_seconds"]:
            t[(r["sample_stratum"], r["configuration"])].append(float(r["wall_seconds"]))
    nov3 = {f"{s} | {c}": round(statistics.mean(v), 2) for (s, c), v in sorted(t.items())}
    all_nov3 = [x for v in t.values() for x in v]
    fresh_times = []
    for rec in glob.glob(str(FRESH / "cisco/R100/*/full_folder_*.run.json")):
        fresh_times.append(json.loads(Path(rec).read_text())["wall_seconds"])
    report_sizes = [Path(p).stat().st_size for p in glob.glob(str(NOV3 / "*/reports/*.json")) if not p.endswith(".run.json")]
    report_sizes += [Path(p).stat().st_size for p in glob.glob(str(FRESH / "cisco/R100/*/full_folder_*.json")) if not p.endswith(".run.json")]
    sg = [float(r["v3_seconds"]) for r in csv.DictReader((EVAL / "per_skill.csv").open(encoding="utf-8"))]
    sec_per_scan = statistics.mean(all_nov3 + fresh_times)

    plans = {}
    for name, alloc in ALLOCATIONS.items():
        n_incomplete = {s: round(alloc[s] * (1 - by[s]["available_complete"] / by[s]["available"])) for s in STRATA}
        scans_skill_only = 2 * sum(alloc.values())
        scans_full_policy_skip = 2 * sum(alloc[s] - n_incomplete[s] for s in STRATA)
        scans_full_all = 2 * sum(alloc.values())
        plans[name] = {
            "allocation": alloc,
            "design_weights": {s: round(by[s]["N"] / alloc[s], 2) for s in STRATA},
            "sampling_fraction_of_available": {s: round(alloc[s] / by[s]["available"], 3) for s in STRATA},
            "expected_incomplete_folders": n_incomplete,
            "scans": {"skill_md_only_configs": scans_skill_only,
                      "full_folder_configs_complete_only (notebook default)": scans_full_policy_skip,
                      "full_folder_configs_incl_incomplete (ALLOW_INCOMPLETE_FOLDERS=True)": scans_full_all,
                      "total_default": scans_skill_only + scans_full_policy_skip,
                      "total_incl_incomplete": scans_skill_only + scans_full_all},
            "est_hours_sequential_default": round((scans_skill_only + scans_full_policy_skip) * sec_per_scan / 3600, 2),
            "est_hours_sequential_incl_incomplete": round((scans_skill_only + scans_full_all) * sec_per_scan / 3600, 2),
            "moe95_per_stratum_p05": {s: moe(0.05, alloc[s], by[s]["N"]) for s in STRATA},
            "moe95_per_stratum_p50": {s: moe(0.5, alloc[s], by[s]["N"]) for s in STRATA},
        }

    out = {
        "frame": str(FRAME.relative_to(REPO)), "frame_rows": len(frame),
        "excluded_from_strata": dict(exclusions),
        "previously_used_samples": [str(p.relative_to(REPO)) for p in used_sources], "previously_used_file_shas": len(used),
        "population_per_stratum": population, "folder_size": bytes_per, "extension_mix": ext_mix,
        "cisco_timing": {"nov3_mean_wall_seconds_by_stratum_config": nov3,
                         "nov3_mean_wall_seconds_all": round(statistics.mean(all_nov3), 2),
                         "fresh100_full_folder_mean_wall_seconds": round(statistics.mean(fresh_times), 2),
                         "fresh100_full_folder_max_wall_seconds": round(max(fresh_times), 2),
                         "planning_seconds_per_scan": round(sec_per_scan, 2),
                         "report_json_mean_bytes": round(statistics.mean(report_sizes))},
        "skillguard_v3_seconds_per_skill": {"mean": round(statistics.mean(sg), 4), "max": round(max(sg), 3)},
        "plans": plans,
    }
    (HERE / "dryrun_numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
