"""Figures for the next1000 reports (PNG, light background), drawn only from saved analysis outputs.

Whole-sample figures read analysis/2026-11-23_040133/ (analyze_next1000.py); open-subset figures read
analysis/findings_open/ (analyze_findings_open.py). Every plotted value is in one of those files.

    .venv/bin/python -I results/skillguard_runs/next1000/make_figures.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
A = HERE / "analysis/2026-11-23_040133"
F = HERE / "analysis/findings_open"
OUT = HERE / "figures"
# validated categorical palette (light): blue, orange, aqua, yellow; contrast WARN -> every bar is labelled
CISCO, MAL, SG, ATR = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                     "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left"})


def rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def finish(fig, ax, name, note):
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.text(0.01, 0.01, note, fontsize=8, color=INK2, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def fig1():
    prev = {r["measure"]: r for r in rows(A / "prevalence.csv") if r["subset"] == "all usable"}
    items = [("cisco_core_skillmd_default", "Cisco core · SKILL.md only, default", CISCO),
             ("cisco_core_full_behavioral", "Cisco core · full folder, behavioral", CISCO),
             ("malskills_malicious", "MalSkills · verdict 'malicious'", MAL),
             ("malskills_any_sso", "MalSkills · any security-sensitive operation", MAL),
             ("skillguard_v32_high", "SkillGuard V3.2 · high review priority", SG),
             ("skillguard_v32_reviewable", "SkillGuard V3.2 · any reviewable behavior", SG),
             ("cisco_atr_rules_any", "Cisco + ATR pack · any ATR rule", ATR)][::-1]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    for i, (k, label, color) in enumerate(items):
        r = prev[k]
        lo, hi = json.loads(r["weighted_ci95"])
        v = float(r["weighted_pct"])
        ax.barh(i, v, color=color, height=0.6, edgecolor=SURFACE, linewidth=2)
        ax.plot([lo, hi], [i, i], color=INK, linewidth=1.2)
        ax.text(hi + 1.2, i, f"{v:.2f}%  ({r['skills_flagged']}/{r['n']} skills)", va="center", fontsize=8.5, color=INK)
    ax.set_yticks(range(len(items)), [x[1] for x in items])
    ax.set_xlim(0, 135)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("Weighted share of the sampling frame flagged (%), 95% CI")
    ax.set_title("What each tool counts as a flag")
    finish(fig, ax, "fig1_flag_rates_by_tool.png",
           "Source: analysis/2026-11-23_040133/prevalence.csv (all usable skills; denominators in labels). "
           "Weighted to the 9,264-skill reduced frame. Measures are not comparable detection rates.")


def fig2():
    data = {r["category"]: r for r in rows(A / "category_crosswalk_skills.csv")}
    cats = [("T2", "T2 Autonomy & oversight control"), ("T3", "T3 Agent-environment persistence/config"),
            ("T4", "T4 Credential & secret access"), ("T5", "T5 Data egress"),
            ("T6", "T6 Code execution & destructive ops"), ("T7", "T7 Supply chain & provenance"),
            ("T9", "T9 Evasion artifacts"), ("T1", "T1 Instruction manipulation")][::-1]
    series = [("cisco_core", "Cisco core", CISCO), ("malskills_sso", "MalSkills SSO", MAL), ("skillguard_v32", "SkillGuard V3.2", SG)]
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    h = 0.26
    for j, (col, label, color) in enumerate(series):
        for i, (c, _) in enumerate(cats):
            v = int(data.get(c, {}).get(col, 0) or 0)
            y = i + (1 - j) * h
            ax.barh(y, v, height=h, color=color, edgecolor=SURFACE, linewidth=2, label=label if i == 0 else None)
            ax.text(v + 2, y, str(v), va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(cats)), [x[1] for x in cats])
    ax.set_xlabel("Skills with at least one alert in the category (of 1,000)")
    ax.set_title("Alerts by SkillGuard taxonomy category")
    ax.legend(frameon=False, loc="lower right")
    finish(fig, ax, "fig2_categories_by_tool.png",
           "Source: analysis/2026-11-23_040133/category_crosswalk_skills.csv. Cisco/MalSkills categories mapped to T1-T9 by "
           "analyze_next1000.py (approximate). SkillGuard network send/fetch are supporting capabilities and excluded. "
           "MalSkills file_operation (288 skills) has no T mapping and is not shown.")


def fig3():
    s = json.loads((A / "summary.json").read_text())
    venn = s["overlap"]["cisco_core_x_malskills_sso_x_sg32_reviewable"]
    combos = []
    for k, n in venn.items():
        bits = tuple(int(p.split("=")[1]) for p in k.split())
        if any(bits):
            combos.append((bits, n))
    combos.sort(key=lambda x: -x[1])
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.2, 5.0), height_ratios=[3, 1.3], sharex=True)
    xs = range(len(combos))
    ax.bar(xs, [n for _, n in combos], color=INK2, width=0.6, edgecolor=SURFACE, linewidth=2)
    for x, (_, n) in zip(xs, combos):
        ax.text(x, n + 3, str(n), ha="center", fontsize=9, color=INK)
    ax.set_ylabel("Skills")
    ax.set_title(f"Three-way overlap on the {s['overlap']['skills_usable_by_all_three']} skills usable by all three tools")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    names = [("Cisco core (full, behavioral)", CISCO), ("MalSkills any SSO", MAL), ("SkillGuard V3.2 reviewable", SG)]
    for row, (label, color) in enumerate(names):
        y = 2 - row
        for x, (bits, _) in zip(xs, combos):
            ax2.scatter(x, y, s=70, color=color if bits[row] else GRID, zorder=3)
    ax2.set_yticks([2, 1, 0], [n for n, _ in names])
    ax2.set_ylim(-0.6, 2.6)
    ax2.set_xticks([])
    for sp in ("left", "bottom"):
        ax2.spines[sp].set_visible(False)
    none = venn.get("cisco=0 malskills_sso=0 sg32=0", 0)
    fig.text(0.01, 0.01, f"Source: analysis/2026-11-23_040133/summary.json (overlap). {none} skills are flagged by none of the three. "
             "A filled dot means the tool flags the skill.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(OUT / "fig3_three_way_overlap.png", dpi=200)
    plt.close(fig)


def fig4():
    data = rows(F / "v31_v32_capability_counts.csv")
    data = data[::-1]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    h = 0.38
    for i, r in enumerate(data):
        a, b = int(r["v31_behaviors"]), int(r["v32_reviewable_behaviors"])
        ax.barh(i + h / 2, a, height=h, color="#9a9993", edgecolor=SURFACE, linewidth=2, label="V3.1 behaviors" if i == 0 else None)
        ax.barh(i - h / 2, b, height=h, color=SG, edgecolor=SURFACE, linewidth=2, label="V3.2 reviewable behaviors" if i == 0 else None)
        ax.text(a + 0.8, i + h / 2, str(a), va="center", fontsize=7.5, color=INK2)
        ax.text(b + 0.8, i - h / 2, str(b), va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(data)), [r["capability"] for r in data])
    ax.set_xlabel("Behaviors (open subset, 750 skills)")
    ax.set_title("SkillGuard V3.1 vs V3.2 by capability")
    ax.legend(frameon=False, loc="lower right")
    finish(fig, ax, "fig4_v31_vs_v32_capabilities.png",
           "Source: analysis/findings_open/v31_v32_capability_counts.csv. V3.1 'nested_agent_invocation' is split in V3.2 into "
           "external_agent_launch (reviewable) and in_host_delegation (context, not reviewable: 36 behaviors).")


def fig5():
    s = json.loads((A / "summary.json").read_text())
    caps = list(s["sg32_reviewable_behaviors_by_capability"].items())[::-1]
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    for i, (c, n) in enumerate(caps):
        ax.barh(i, n, color=SG, height=0.62, edgecolor=SURFACE, linewidth=2)
        ax.text(n + 0.8, i, str(n), va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(caps)), [c for c, _ in caps])
    ax.set_xlabel("Reviewable behaviors (all 1,000 skills)")
    ax.set_title("SkillGuard V3.2 reviewable behaviors by capability")
    finish(fig, ax, "fig5_sg32_capabilities.png",
           "Source: analysis/2026-11-23_040133/summary.json (sg32_reviewable_behaviors_by_capability). Supporting capabilities "
           "(network_send, network_fetch) and context signals (in_host_delegation) are excluded.")


def fig6():
    data = rows(F / "sg32_coverage_by_file_type.csv")
    groups = [("Parsed / analyzed", ["analyzed", "analyzed_with_parse_errors", "parsed_no_agent_config", "disguised_text_scanned"], SG),
              ("Markdown instructions only", ["markdown_instructions_only"], "#6250d6"),
              ("Not analyzed (data, unsupported, parse error)", ["data_file_not_analyzed", "unsupported_format", "parse_error"], "#9a9993")]
    data = data[::-1]
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    for i, r in enumerate(data):
        left = 0
        for j, (label, cols, color) in enumerate(groups):
            v = sum(int(r.get(c, 0) or 0) for c in cols)
            ax.barh(i, v, left=left, color=color, height=0.62, edgecolor=SURFACE, linewidth=2, label=label if i == 0 else None)
            left += v
        ax.text(left + 8, i, r["files"], va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(data)), [r["file_type"] for r in data])
    ax.set_xlabel("Files (open subset)")
    ax.set_title("SkillGuard V3.2 file coverage by file type")
    ax.legend(frameon=False, loc="lower right", fontsize=8.5)
    finish(fig, ax, "fig6_sg32_coverage.png",
           "Source: analysis/findings_open/sg32_coverage_by_file_type.csv. Config files 'parsed' includes files parsed "
           "without agent settings. 'other' = unsupported formats (HTML, CSV, binaries, ...).")


def main():
    OUT.mkdir(exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        f()
    print("figures written to", OUT)


if __name__ == "__main__":
    main()
