"""Self-contained HTML dashboard (one file, no network, works from file://).

Safety model for untrusted skill text (snippets, titles, descriptions, paths):
* every value is redacted and path-cleaned before it is embedded;
* static HTML built here goes through html.escape();
* table data travels as JSON inside <script type="application/json"> with <, > and & escaped, and the page's own
  script renders it with textContent only (never innerHTML);
* a Content-Security-Policy allows exactly this page's script (by SHA-256 hash), no network and no other scripts, so
  even markup that slipped through could not execute.
"""

import base64
import hashlib
import html
import json
import math
import os
from pathlib import Path

import pandas as pd

from .model import SEVERITY_ORDER, TIER_LABELS, TIER_ORDER, analyzer_info
from .redaction import clean_frame, clean_text

SNIPPET_CHARS = 800
TEXT_CHARS = 400

SEVERITY_COLORS = {"CRITICAL": "#d03b3b", "HIGH": "#ec835a", "MEDIUM": "#fab219", "LOW": "#b5b3ab", "INFO": "#d9d7cf"}
OUTCOME_COLORS = {"complete": "#0ca30c", "contract_only": "#fab219", "partial": "#ec835a", "failed": "#d03b3b",
                  "excluded_incomplete_folder": "#898781", "missing": "#c3c2b7"}
DARK_INK = {"MEDIUM", "LOW", "INFO", "contract_only", "missing"}       # fills that need dark text on top

OUTCOME_HELP = {
    "complete": "valid report; every requested analyzer ran without a reported failure. Only these enter the primary analysis.",
    "contract_only": "valid report whose only problem is Cisco's known rule-registration error; used only in sensitivity analysis.",
    "partial": "a report exists but an analyzer failed or is missing; findings are preliminary evidence only.",
    "failed": "no usable report (timeout, scanner error, invalid JSON, hash mismatch, export error).",
    "excluded_incomplete_folder": "design exclusion: GitSkills lacks some supporting files, so the full-folder scan was not run.",
    "missing": "reanalysis only: the saved run has no report for this configuration.",
}
GLOSSARY = [
    ("Scan", "One Cisco run over one skill in one configuration (skill x configuration)."),
    ("Configuration", "Scope (SKILL.md only, or the full skill folder) x analyzer mode (static, behavioral, LLM, meta)."),
    ("Primary analysis", "Uses only COMPLETE scans. Anything else is reported separately, never as zero findings."),
    ("Alert row", "One finding Cisco reported in one scan. The same alert seen in four configurations is four rows."),
    ("Distinct alert location", "Rule + file + line within one skill, merged across configurations. The unit used for review."),
    ("finding_kind", "Our classification: security (counted as alerts), metadata_quality (license, description, naming) or "
                     "scan_coverage (binary files, analysis-incomplete notes)."),
    ("Evidence check", "exact: Cisco's evidence is on the reported line; ambiguous / mismatch: it is elsewhere or unclear; "
                       "unavailable: nothing to check. A pointer for reviewers, not a correction."),
    ("Comparison change", "additional: present only in the later configuration (e.g. full folder); removed: only in the earlier one; "
                          "unchanged: in both. Pairs are 'eligible' only when both scans are COMPLETE."),
    ("Redacted", "Text that looks like a secret is replaced with [REDACTED] before it reaches any report file."),
]


# ---------------------------------------------------------------- helpers

def esc(value):
    if value is None or (not isinstance(value, (str, list, dict)) and pd.isna(value)):
        return ""
    return html.escape(str(value), quote=True)


def clip(value, n):
    if not isinstance(value, str):
        return value
    return value if len(value) <= n else value[:n] + f" … [{len(value) - n} more characters in the CSV]"


def records(df, portable, columns=None, clip_map=None):
    if df is None or df.empty:
        return []
    df = df[[c for c in (columns or df.columns) if c in df.columns]]
    df = clean_frame(df, portable)
    for col, n in (clip_map or {}).items():
        if col in df:
            df[col] = df[col].map(lambda v: clip(v, n))
    out = []
    for row in df.to_dict("records"):
        out.append({k: (None if (not isinstance(v, (str, list, dict, bool)) and v is not None and pd.isna(v)) else
                        (int(v) if isinstance(v, float) and v.is_integer() and k.endswith(("line_number", "rows", "count"))
                         else v.item() if hasattr(v, "item") else v)) for k, v in row.items()})
    return out


def json_for_script(value):
    text = json.dumps(value, ensure_ascii=True, default=str, allow_nan=False)
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def ink(key):
    return "#0b0b0b" if key in DARK_INK else "#ffffff"


# ---------------------------------------------------------------- SVG charts (static, escaped)

def stacked_bars(rows, segments, colors, title, unit, width=760):
    """Horizontal 100%-width stacked bars: rows = [(label, {segment: count})]."""
    if not rows:
        return "<p class='muted'>No data.</p>"
    label_w, bar_h, gap, top = 210, 22, 14, 6
    total_max = max(sum(v.values()) for _, v in rows) or 1
    plot_w = width - label_w - 60
    h = top + len(rows) * (bar_h + gap)
    parts = [f"<svg class='chart' viewBox='0 0 {width} {h}' role='img' aria-label='{esc(title)}'>"]
    for i, (label, values) in enumerate(rows):
        y = top + i * (bar_h + gap)
        parts.append(f"<text x='{label_w - 8}' y='{y + bar_h * 0.68}' text-anchor='end' class='axis-label'>{esc(label)}</text>")
        x, total = label_w, sum(values.values())
        for seg in segments:
            n = values.get(seg, 0)
            if not n:
                continue
            w = max(plot_w * n / total_max - 2, 1.5)
            parts.append(f"<g class='mark'><rect x='{x:.1f}' y='{y}' width='{w:.1f}' height='{bar_h}' rx='3' fill='{colors[seg]}'>"
                         f"<title>{esc(label)}: {esc(seg)} = {n} {esc(unit)}</title></rect>")
            if w > 22:
                parts.append(f"<text x='{x + w / 2:.1f}' y='{y + bar_h * 0.68}' text-anchor='middle' class='seg-label' "
                             f"fill='{ink(seg)}'>{n}</text>")
            parts.append("</g>")
            x += w + 2
        parts.append(f"<text x='{x + 6:.1f}' y='{y + bar_h * 0.68}' class='axis-label'>{total}</text>")
    parts.append("</svg>")
    legend = "".join(f"<span class='key'><i style='background:{colors[s]}'></i>{esc(s)}</span>" for s in segments
                     if any(v.get(s) for _, v in rows))
    return f"<figure><figcaption>{esc(title)}</figcaption>{''.join(parts)}<div class='legend'>{legend}</div></figure>"


def simple_bars(rows, title, unit, width=760, max_rows=25):
    """Single-series horizontal bars: rows = [(label, count)]."""
    rows = rows[:max_rows]
    if not rows:
        return "<p class='muted'>No data.</p>"
    label_w, bar_h, gap = 300, 16, 8
    vmax = max(n for _, n in rows) or 1
    plot_w = width - label_w - 50
    h = len(rows) * (bar_h + gap) + 4
    parts = [f"<svg class='chart' viewBox='0 0 {width} {h}' role='img' aria-label='{esc(title)}'>"]
    for i, (label, n) in enumerate(rows):
        y = 2 + i * (bar_h + gap)
        w = max(plot_w * n / vmax, 1.5)
        parts.append(f"<text x='{label_w - 8}' y='{y + bar_h * 0.75}' text-anchor='end' class='axis-label'>{esc(label)}</text>"
                     f"<g class='mark'><rect x='{label_w}' y='{y}' width='{w:.1f}' height='{bar_h}' rx='3' class='series1'>"
                     f"<title>{esc(label)}: {n} {esc(unit)}</title></rect></g>"
                     f"<text x='{label_w + w + 6:.1f}' y='{y + bar_h * 0.75}' class='axis-label'>{n}</text>")
    parts.append("</svg>")
    return f"<figure><figcaption>{esc(title)}</figcaption>{''.join(parts)}</figure>"


# ---------------------------------------------------------------- page

def tile(value, label, help_text, tone=""):
    return (f"<div class='tile {tone}'><div class='tile-value'>{esc(value)}</div><div class='tile-label'>{esc(label)}</div>"
            f"<div class='tile-help'>{esc(help_text)}</div></div>")


def static_table(df, columns, labels=None, numeric=()):
    if df is None or df.empty:
        return "<p class='muted'>None.</p>"
    head = "".join(f"<th>{esc((labels or {}).get(c, c))}</th>" for c in columns)
    body = "".join("<tr>" + "".join(f"<td class='{'num' if c in numeric else ''}'>{esc(row.get(c))}</td>" for c in columns) + "</tr>"
                   for row in df.to_dict("records"))
    return f"<div class='table-wrap'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def render(ctx):
    s, c, v, portable = ctx["source"], ctx["counts"], ctx["validation"], ctx["portable"]
    o = c["scans_by_outcome"]
    tiers = v["locations_by_tier"]
    total_loc = sum(tiers.values())
    report_dir = Path("..")                      # dashboard lives in 01_IMPORTANT_RESULTS/

    # ---- data for the interactive tables
    data = {
        "locations": records(ctx["key"], portable, ["severity", "rule_id", "skill_id", "repo", "file_path", "reported_line_number",
                                                     "configurations", "run_outcomes", "in_primary_analysis", "cisco_category",
                                                     "research_category", "analyzers", "evidence_status", "title", "snippet",
                                                     "finding_ids", "review_id", "validation_tier", "behavior_group",
                                                     "suggested_interpretation", "provisional_label", "final_label"],
                             {"snippet": SNIPPET_CHARS, "title": TEXT_CHARS}),
        "rows": records(ctx["annotated"], portable, ["severity", "rule_id", "skill_id", "repo", "file_path", "reported_line_number",
                                                      "configuration", "analyzer_mode", "run_outcome", "finding_kind", "cisco_category",
                                                      "research_category", "analyzer", "evidence_status", "title", "description",
                                                      "snippet", "finding_id", "review_id", "validation_tier", "provisional_label",
                                                      "final_label"],
                        {"snippet": SNIPPET_CHARS, "title": TEXT_CHARS, "description": TEXT_CHARS}),
        "skills": records(ctx["skills"], portable),
        "tiers": TIER_LABELS,
        "severityOrder": SEVERITY_ORDER,
        "configurations": [x["configuration"] for x in s.configurations],
    }

    # ---- static sections
    overview = "".join([
        tile(c["skills_selected"], "skills selected", "Skills chosen for this experiment (sample manifest or selection)."),
        tile(c["skills_scanned"], "skills scanned", f"At least one Cisco scan executed. {c['export_errors']} export error(s)."),
        tile(f"{o['complete']} / {c['scans_planned']}", "scans complete / planned",
             f"{c['skills_exported']} skills x {c['configurations']} configurations. Only COMPLETE scans enter the primary analysis."),
        tile(c["skills_with_security_alert_primary"], "skills with security alerts",
             f"At least one security alert in a COMPLETE scan ({c['skills_with_security_alert_any']} including partial scans). "
             "Metadata-quality notes are not counted."),
        tile(c["security_locations_primary"], "distinct alert locations",
             f"Rule + file + line per skill, merged across configurations ({c['security_rows_primary']} alert rows)."),
        tile(tiers["human_validated"], "human-validated", "Alert locations a human reviewer has adjudicated (final_label filled).",
             "tone-good" if tiers["human_validated"] else "tone-warn"),
        tile(tiers["provisional"], "provisional labels", "AI-assisted, researcher-approved labels. Not independent human review."),
    ])
    sk = c["skills_by_coverage"]
    from .tables import SKILL_COVERAGE
    skill_cov = "".join(tile(sk[k], k.replace("_", " "), SKILL_COVERAGE[k]) for k in SKILL_COVERAGE)

    cov = ctx["coverage"]
    cov_rows = [(r["configuration"], {k: r[k] for k in OUTCOME_COLORS}) for r in cov.to_dict("records") if r["configuration"] != "All configurations"]
    coverage_chart = stacked_bars(cov_rows, list(OUTCOME_COLORS), OUTCOME_COLORS, "Scan outcome by configuration (number of skills)", "skills")
    outcome_help = "".join(f"<dt><span class='swatch' style='background:{OUTCOME_COLORS[k]}'></span>{esc(k)}</dt><dd>{esc(t)}</dd>"
                           for k, t in OUTCOME_HELP.items())

    sev = ctx["severity"]
    sev_cols = [x for x in SEVERITY_ORDER if x in sev.columns] + [x for x in sev.columns if x not in SEVERITY_ORDER and x.isupper()]
    sev_rows = [(r["configuration"], {k: r.get(k, 0) for k in sev_cols}) for r in sev.to_dict("records")]
    sev_chart = stacked_bars(sev_rows, sev_cols, {**SEVERITY_COLORS, **{k: "#898781" for k in sev_cols if k not in SEVERITY_COLORS}},
                             "Security alert rows in COMPLETE scans, by severity and configuration", "alert rows")

    funnel = [("alert rows (all configurations)", c["security_rows_any"]), ("distinct alert locations", total_loc),
              ("in the review queue", total_loc - tiers["not_in_review"]), ("with a provisional label", tiers["provisional"] + tiers["human_validated"]),
              ("human-validated", tiers["human_validated"])]
    funnel_chart = simple_bars(funnel, "From scanner alert to validated finding", "")

    rules = ctx["rules"]
    sec_rules = rules[rules["finding_kind"] == "security"] if not rules.empty else rules
    rule_chart = simple_bars([(r["rule_id"], r["rows_all_readable_scans"]) for r in sec_rules.to_dict("records")],
                             "Security rules by alert rows (all readable scans)", "alert rows")

    comp = ctx["comparisons"]
    comp_html = static_table(comp, ["comparison", "kind", "pair_status", "change", "rows", "skills"], numeric=("rows", "skills")) \
        if not comp.empty else "<p class='muted'>No comparison files in this run.</p>"

    configs_html = static_table(ctx["configs"], ["configuration", "analyzer", "about"])
    from .build import LLM_META_SECTIONS, _overview_rows, llm_meta_tables
    llm_meta = llm_meta_tables(s)
    llm_meta_parts = []
    for name, heading, columns, about in LLM_META_SECTIONS:
        frame = llm_meta.get(name)
        if frame is None or frame.empty:
            continue
        cols = [c for c in (columns or list(frame.columns)) if c in frame.columns]
        numeric = tuple(c for c in cols if pd.api.types.is_numeric_dtype(frame[c]))
        llm_meta_parts.append(f"<h3>{esc(heading)}</h3><p class='muted'>{esc(about)}</p>"
                              + static_table(frame.head(60), cols, numeric=numeric))
    llm_meta_section = ("<section id='llm-meta'><h2>LLM Analyzer and Meta-Analyzer</h2><p class='lede'>Full tables in "
                        "<code>02_DETAILED_ANALYSIS/llm_meta/</code>. LLM and Meta output is nondeterministic and depends on "
                        "the model; scanner disagreement marks candidates for targeted manual investigation.</p>"
                        + "".join(llm_meta_parts) + "</section>") if llm_meta_parts else ""
    llm_meta_nav = "<a href='#llm-meta'>LLM / Meta</a>" if llm_meta_parts else ""
    details = "".join(f"<tr><th>{esc(k)}</th><td>{esc(clean_text(str(val), portable))}</td></tr>" for k, val in _overview_rows(ctx))
    files_html = "".join(
        f"<tr><td>{esc(q)}</td><td><a href='{esc(Path(os.path.relpath(f, '01_IMPORTANT_RESULTS')).as_posix())}'>{esc(f)}</a></td>"
        f"<td>{esc(what)}</td></tr>" for q, f, what in ctx["files"])
    limitations = "".join(f"<li>{esc(clean_text(x, portable)).replace('**', '')}</li>" for x in ctx["limitations"])
    glossary = "".join(f"<dt>{esc(k)}</dt><dd>{esc(t)}</dd>" for k, t in GLOSSARY)
    tier_help = (
        "<div class='tiers'>"
        f"<div><span class='badge t-scanner_alert'>⚠ Scanner alert</span><p>Cisco reported it. Nothing more is known. "
        f"<b>{tiers['awaiting_review'] + tiers['not_in_review']}</b> locations.</p></div>"
        f"<div><span class='badge t-provisional'>◐ Provisional</span><p>Researcher-approved, AI-assisted label. Useful for triage; "
        f"<b>not</b> an independent human review. <b>{tiers['provisional']}</b> locations.</p></div>"
        f"<div><span class='badge t-human_validated'>✔ Human-validated</span><p>final_label filled and adjudicated. Only this tier may be "
        f"reported as a validated finding. <b>{tiers['human_validated']}</b> locations.</p></div></div>")
    review_note = (f"Worksheet: <code>{esc(portable.path(ctx['review'].folder))}</code> ({esc(ctx['review'].match)})."
                   if ctx["review"] is not None else "No manual-review worksheet exists for this run yet.")

    script = SCRIPT
    script_hash = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode()
    csp = (f"default-src 'none'; script-src 'sha256-{script_hash}'; style-src 'unsafe-inline'; img-src data:; "
           "base-uri 'none'; form-action 'none'")
    banner_tone = "warn" if tiers["human_validated"] == 0 else "info"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{esc(csp)}">
<meta name="referrer" content="no-referrer">
<title>{esc(s.experiment)} · Cisco scan report</title>
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="eyebrow">Cisco Skill Scanner · {esc(s.metadata.get('scanner', {}).get('installed_version') or '')} · {esc(s.run_mode)}</div>
    <h1>{esc(s.experiment)}</h1>
    <div class="sub">Report <code>{esc(s.report_id)}</code> · generated {esc(ctx['generated_at'])} · source <code>{esc(portable.path(s.folder))}</code></div>
  </div>
</header>
<nav class="sections" aria-label="Sections"><div class="wrap">
    <a href="#overview">Overview</a><a href="#coverage">Coverage</a><a href="#severity">Severity</a><a href="#alerts">Alerts explorer</a>
    <a href="#validation">Validation</a><a href="#comparisons">Comparisons</a>{llm_meta_nav}<a href="#rules">Rules</a><a href="#skills">Skills</a>
    <a href="#files">Files</a><a href="#limitations">Limitations</a><a href="#glossary">Glossary</a>
</div></nav>
<main class="wrap">
<div class="banner {banner_tone}" role="note"><b>Scanner alerts are not vulnerabilities.</b> Every count below is Cisco output
unless it says human-validated. Human-validated so far: <b>{tiers['human_validated']} of {total_loc}</b> distinct alert locations (all readable scans).</div>

<section id="overview"><h2>Overview</h2>
<p class="lede">What was scanned, how much of it completed, and how many alerts exist at each level of validation. Each tile explains its own definition.</p>
<div class="tiles">{overview}</div>
<details><summary>Run details and configurations</summary><div class="table-wrap"><table class="kv">{details}</table></div>{configs_html}</details>
</section>

<section id="coverage"><h2>Coverage</h2>
<p class="lede">Every skill is planned once per configuration. A skill is fully covered only when all its planned scans are COMPLETE.
Incomplete coverage is reported, never treated as "zero findings".</p>
<div class="tiles small">{skill_cov}</div>
{coverage_chart}
{static_table(cov, ["configuration", "planned", "executed", "complete", "contract_only", "partial", "failed", "excluded_incomplete_folder", "missing", "complete_pct_of_planned"],
              {"excluded_incomplete_folder": "excluded (incomplete folder)", "complete_pct_of_planned": "% complete"},
              numeric=("planned", "executed", "complete", "contract_only", "partial", "failed", "excluded_incomplete_folder", "missing", "complete_pct_of_planned"))}
<details><summary>What each outcome means</summary><dl class="defs">{outcome_help}</dl></details>
</section>

<section id="severity"><h2>Severity by configuration</h2>
<p class="lede">Security alert rows from COMPLETE scans only. Severity is Cisco's, not ours. Compare rows to see what scope and analyzer add.</p>
{sev_chart}
{static_table(sev, ["configuration"] + sev_cols + ["security_rows", "distinct_locations", "skills_with_alerts"],
              {"security_rows": "alert rows", "distinct_locations": "distinct locations", "skills_with_alerts": "skills"},
              numeric=tuple(sev_cols) + ("security_rows", "distinct_locations", "skills_with_alerts"))}
</section>

<section id="alerts"><h2>Alerts explorer</h2>
<p class="lede">Search and filter every alert. <b>Distinct locations</b> merge the same alert across configurations (the unit reviewers label);
<b>finding rows</b> show one row per scan and include metadata-quality and coverage notes. Click a row for its evidence. Snippets are
untrusted skill text shown as plain text, redacted where they look like secrets.</p>
<div class="filters" id="filters">
  <label>Unit <select id="f-unit"><option value="locations">Distinct alert locations</option><option value="rows">Finding rows (per scan)</option></select></label>
  <label class="grow">Search <input id="f-q" type="search" placeholder="rule, skill, file, snippet…" autocomplete="off"></label>
  <label>Severity <select id="f-severity"></select></label>
  <label>Validation <select id="f-tier"></select></label>
  <label>Rule <select id="f-rule"></select></label>
  <label>Skill <select id="f-skill"></select></label>
  <label data-unit="rows">Kind <select id="f-kind"></select></label>
  <label data-unit="rows">Configuration <select id="f-config"></select></label>
  <label class="check"><input id="f-primary" type="checkbox"> COMPLETE scans only</label>
  <button id="f-reset" type="button">Reset</button>
  <button id="f-csv" type="button">Download filtered CSV</button>
</div>
<p class="count" id="count" aria-live="polite"></p>
<div class="table-wrap"><table id="explorer"><thead></thead><tbody></tbody></table></div>
<button id="more" type="button" hidden>Show more</button>
</section>

<section id="validation"><h2>Validation</h2>
<p class="lede">Three tiers are kept apart everywhere in this report. {review_note}</p>
{tier_help}
{funnel_chart}
</section>

<section id="comparisons"><h2>Configuration comparisons</h2>
<p class="lede"><b>additional</b>: only in the later configuration (full folder, or the behavioral / LLM / meta analyzer);
<b>removed</b>: only in the earlier one; <b>unchanged</b>: in both. Pairs are <b>eligible</b> only when both scans are COMPLETE.</p>
{comp_html}
</section>
{llm_meta_section}

<section id="rules"><h2>Rules</h2>
<p class="lede">Which Cisco rules produced security alerts. The full table, including metadata-quality rules, is in
<code>02_DETAILED_ANALYSIS/rule_breakdown.csv</code>.</p>
{rule_chart}
{static_table(sec_rules, ["rule_id", "max_severity", "cisco_category", "research_category", "analyzers", "rows_primary", "rows_all_readable_scans", "skills_all", "distinct_locations_primary"],
              {"rows_primary": "rows (complete)", "rows_all_readable_scans": "rows (all)", "skills_all": "skills", "distinct_locations_primary": "locations (complete)"},
              numeric=("rows_primary", "rows_all_readable_scans", "skills_all", "distinct_locations_primary"))}
</section>

<section id="skills"><h2>Skills</h2>
<p class="lede">Every scanned skill with its coverage and finding counts. "Alerts" filters the explorer to that skill; "page" opens its detail page.</p>
<div class="filters"><label class="grow">Search skills <input id="s-q" type="search" placeholder="skill, repo, stratum…" autocomplete="off"></label>
<label class="check"><input id="s-sec" type="checkbox"> only skills with security alerts</label></div>
<div class="table-wrap"><table id="skills-table"><thead></thead><tbody></tbody></table></div>
</section>

<section id="files"><h2>Which file to open</h2>
<div class="table-wrap"><table><thead><tr><th>Question</th><th>File</th><th>What it holds</th></tr></thead><tbody>{files_html}</tbody></table></div>
</section>

<section id="limitations"><h2>Limitations and incomplete results</h2><ul class="limits">{limitations}</ul></section>

<section id="glossary"><h2>Glossary</h2><dl class="defs">{glossary}</dl></section>
<footer>Generated by gitskills_reports from the CSV files of <code>{esc(portable.path(s.folder))}</code>. Self-contained: no network access.</footer>
</main>
<script type="application/json" id="report-data">{json_for_script(data)}</script>
<script>{script}</script>
</body>
</html>
"""


def render_index(entries, legacy):
    rows = "".join(
        f"<tr class='{'rec' if e['recommended'] else ''}'><td>{'★' if e['recommended'] else ''}</td>"
        f"<td><a href='{esc(e['report'])}/01_IMPORTANT_RESULTS/dashboard.html'>{esc(e['report_id'])}</a></td>"
        f"<td>{esc(e['role'])}</td><td class='num'>{e['counts']['skills_selected']}</td>"
        f"<td class='num'>{e['counts']['scans_by_outcome']['complete']} / {e['counts']['scans_planned']}</td>"
        f"<td class='num'>{e['counts']['skills_with_security_alert_primary']}</td>"
        f"<td class='num'>{sum(e['validation']['locations_by_tier'].values())}</td>"
        f"<td class='num'>{e['validation']['locations_by_tier']['human_validated']}</td>"
        f"<td><a href='{esc(e['report'])}/01_IMPORTANT_RESULTS/START_HERE.md'>START_HERE.md</a></td></tr>" for e in entries)
    legacy_html = ("<p class='muted'>Not reported (legacy layout without a run ID, untouched): "
                   + ", ".join(f"<code>{esc(p)}</code>" for p in legacy) + "</p>") if legacy else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'">
<title>Cisco scan reports</title><style>{CSS}</style></head>
<body><header class="top"><div class="wrap"><div class="eyebrow">GitSkills · MSR 2027</div><h1>Cisco scanner reports</h1>
<div class="sub">One report per saved run. ★ = open this one first (latest analysis of each scan).</div></div></header>
<main class="wrap"><div class="banner warn" role="note">Alerts are Cisco scanner output, not vulnerabilities; only the
human-validated column counts reviewed results.</div>
<div class="table-wrap"><table><thead><tr><th></th><th>Report (dashboard)</th><th>Role</th><th>Skills</th><th>Scans complete / planned</th>
<th>Skills with security alerts</th><th>Alert locations</th><th>Human-validated</th><th>Start page</th></tr></thead><tbody>{rows}</tbody></table></div>
{legacy_html}</main></body></html>
"""


CSS = """
:root{--page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--grid:#e1e0d9;--base:#c3c2b7;
--s1:#2a78d6;--good:#0ca30c;--warn:#fab219;--crit:#d03b3b;--warnbg:#fff6e0;--infobg:#e9f2fc;--row:#f1f0ec}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--page:#0d0d0d;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;
--grid:#2c2c2a;--base:#383835;--s1:#3987e5;--warnbg:#2d2410;--infobg:#132235;--row:#222220}}
:root[data-theme="dark"]{--page:#0d0d0d;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--grid:#2c2c2a;--base:#383835;--s1:#3987e5;
--warnbg:#2d2410;--infobg:#132235;--row:#222220}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
header.top{background:var(--surface);padding:14px 0 10px}
nav.sections{background:var(--surface);border-bottom:1px solid var(--grid);position:sticky;top:0;z-index:5}
.eyebrow{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
h1{margin:2px 0 2px;font-size:24px}
.sub{color:var(--ink2);font-size:13px;overflow-wrap:anywhere}
nav.sections .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:6px;padding-bottom:6px}
nav a{white-space:nowrap;color:var(--ink2);text-decoration:none;padding:4px 10px;border-radius:999px;font-size:13px}
nav a:hover,nav a:focus{background:var(--row);color:var(--ink)}
section{margin:28px 0;scroll-margin-top:56px}
h2{font-size:19px;margin:0 0 6px}
.lede{color:var(--ink2);margin:0 0 14px;max-width:880px}
.banner{margin:18px 0 0;padding:12px 14px;border-radius:8px;border:1px solid var(--grid)}
.banner.warn{background:var(--warnbg)} .banner.info{background:var(--infobg)}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:14px}
.tile{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:12px 14px}
.tile-value{font-size:28px;font-weight:650;font-variant-numeric:tabular-nums}
.tiles.small .tile-value{font-size:22px}
.tile-label{font-weight:600;margin-top:2px}
.tile-help{color:var(--ink2);font-size:12.5px;margin-top:4px}
.tile.tone-warn{border-left:4px solid var(--warn)} .tile.tone-good{border-left:4px solid var(--good)}
figure{overflow-x:auto;margin:10px 0 14px;background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:12px}
figcaption{font-weight:600;margin-bottom:6px}
svg.chart{width:100%;min-width:560px;height:auto;display:block}
.axis-label{font-size:12px;fill:var(--ink2)} .seg-label{font-size:11px;font-weight:600}
.series1{fill:var(--s1)}
.mark rect{transition:opacity .1s} svg.chart:hover .mark rect{opacity:.55} svg.chart .mark:hover rect{opacity:1}
.legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px;font-size:12.5px;color:var(--ink2)}
.key i,.swatch{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.table-wrap{overflow-x:auto;background:var(--surface);border:1px solid var(--grid);border-radius:10px;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--grid);vertical-align:top}
th{font-weight:600;color:var(--ink2);background:var(--surface)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
td{overflow-wrap:anywhere}
table.kv th{width:240px}
#explorer th,#skills-table th{cursor:pointer;user-select:none}
#explorer th[aria-sort=ascending]::after{content:" ▲"} #explorer th[aria-sort=descending]::after{content:" ▼"}
#skills-table th[aria-sort=ascending]::after{content:" ▲"} #skills-table th[aria-sort=descending]::after{content:" ▼"}
#explorer tbody tr.item{cursor:pointer} #explorer tbody tr.item:hover{background:var(--row)}
tr.detail td{background:var(--row)}
.detail-grid{display:grid;grid-template-columns:170px 1fr;gap:4px 12px;font-size:13px}
.detail-grid b{color:var(--ink2);font-weight:600}
pre.snippet{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--surface);border:1px solid var(--grid);border-radius:6px;padding:8px;margin:8px 0 0;font-size:12.5px;max-height:320px;overflow:auto}
.filters{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:flex-end;background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:10px 12px}
.filters label{display:flex;flex-direction:column;font-size:12px;color:var(--ink2);gap:3px}
.filters label.grow{flex:1 1 220px} .filters label.check{flex-direction:row;align-items:center;gap:6px;font-size:13px;color:var(--ink)}
input[type=search],select{font:inherit;font-size:13.5px;padding:5px 8px;border:1px solid var(--base);border-radius:6px;background:var(--page);color:var(--ink);max-width:260px}
input[type=search]{width:100%;max-width:none}
button{font:inherit;font-size:13px;padding:6px 12px;border-radius:6px;border:1px solid var(--base);background:var(--page);color:var(--ink);cursor:pointer}
button:hover{background:var(--row)}
.count{color:var(--ink2);font-size:13px;margin:8px 2px}
.badge{display:inline-block;font-size:12px;padding:1px 8px;border-radius:999px;white-space:nowrap;border:1px solid var(--base)}
.t-human_validated{background:var(--good);color:#fff;border-color:var(--good)}
.t-provisional{border:1.5px dashed var(--s1);color:var(--s1)}
.t-scanner_alert,.t-awaiting_review,.t-not_in_review{color:var(--ink2)}
.sev{display:inline-block;white-space:nowrap;font-size:11.5px;font-weight:650;padding:1px 7px;border-radius:4px}
.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.tiers>div{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:10px 12px}
.tiers p{margin:6px 0 0;color:var(--ink2);font-size:13px}
dl.defs{display:grid;grid-template-columns:minmax(140px,220px) 1fr;gap:6px 14px;font-size:13.5px}
dl.defs dt{font-weight:600} dl.defs dd{margin:0;color:var(--ink2)}
details{margin:10px 0} summary{cursor:pointer;color:var(--s1);font-weight:600}
ul.limits li{margin:6px 0}
p,li,dd,figcaption{overflow-wrap:anywhere}
code{font-size:12.5px;background:var(--row);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
a{color:var(--s1)}
.muted{color:var(--muted)}
tr.rec td{font-weight:600}
footer{color:var(--muted);font-size:12px;margin:30px 0 40px}
@media (max-width:640px){h1{font-size:20px}.detail-grid,dl.defs{grid-template-columns:1fr}table.kv th{width:auto}}
"""

SCRIPT = r"""
(function () {
  "use strict";
  var D = JSON.parse(document.getElementById("report-data").textContent);
  var SEV = {CRITICAL: ["#d03b3b", "#fff"], HIGH: ["#ec835a", "#fff"], MEDIUM: ["#fab219", "#0b0b0b"], LOW: ["#b5b3ab", "#0b0b0b"], INFO: ["#d9d7cf", "#0b0b0b"]};
  var ICON = {human_validated: "✔ ", provisional: "◐ ", awaiting_review: "⚠ ", not_in_review: "⚠ "};
  var PAGE = 200;

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) { if (k === "class") e.className = attrs[k]; else e.setAttribute(k, attrs[k]); }
    if (text !== undefined && text !== null) e.textContent = String(text);
    return e;
  }
  function str(v) { return v === null || v === undefined ? "" : String(v); }
  function sevBadge(s) {
    var c = SEV[s] || ["#898781", "#fff"], b = el("span", {"class": "sev"}, s || "");
    b.style.background = c[0]; b.style.color = c[1]; return b;
  }
  function tierBadge(t) {
    if (!t) return el("span", {"class": "muted"}, "n/a (not a security alert)");
    return el("span", {"class": "badge t-" + t}, (ICON[t] || "") + (t === "awaiting_review" || t === "not_in_review" ? "Scanner alert" : t === "provisional" ? "Provisional" : "Human-validated"));
  }
  function sevRank(s) { var i = D.severityOrder.indexOf(s); return i < 0 ? 99 : i; }

  // ---------------------------------------------------------------- alerts explorer
  var COLS = {
    locations: [["severity", "Severity"], ["rule_id", "Rule"], ["skill_id", "Skill"], ["file_path", "File"], ["reported_line_number", "Line"],
                ["configurations", "Seen in"], ["validation_tier", "Validation"], ["provisional_label", "Provisional label"], ["final_label", "Human label"]],
    rows: [["severity", "Severity"], ["finding_kind", "Kind"], ["rule_id", "Rule"], ["skill_id", "Skill"], ["file_path", "File"],
           ["reported_line_number", "Line"], ["configuration", "Configuration"], ["run_outcome", "Scan outcome"], ["validation_tier", "Validation"]]
  };
  var DETAIL = {
    locations: [["title", "Title"], ["repo", "Repository"], ["cisco_category", "Cisco category"], ["research_category", "Research category"],
                ["analyzers", "Analyzer"], ["run_outcomes", "Scan outcomes"], ["evidence_status", "Evidence check"], ["review_id", "Review ID"],
                ["behavior_group", "Behavior group"], ["suggested_interpretation", "Draft suggestion (not a label)"], ["finding_ids", "Cisco finding IDs"]],
    rows: [["title", "Title"], ["description", "Description"], ["repo", "Repository"], ["cisco_category", "Cisco category"],
           ["research_category", "Research category"], ["analyzer", "Analyzer"], ["evidence_status", "Evidence check"], ["finding_id", "Finding ID"],
           ["review_id", "Review ID"], ["provisional_label", "Provisional label"], ["final_label", "Human label"]]
  };
  var state = {unit: "locations", sort: null, dir: 1, shown: PAGE, open: {}};
  var $ = function (id) { return document.getElementById(id); };

  function options(select, values, allLabel) {
    var cur = select.value; select.textContent = "";
    select.appendChild(el("option", {value: ""}, allLabel));
    values.forEach(function (v) { var o = el("option", {value: v}, v); select.appendChild(o); });
    if (values.indexOf(cur) >= 0) select.value = cur;
  }
  function uniq(data, key, sorter) {
    var seen = {}; data.forEach(function (r) { var v = r[key]; if (v !== null && v !== undefined && v !== "") seen[v] = 1; });
    return Object.keys(seen).sort(sorter);
  }
  function data() { return state.unit === "locations" ? D.locations : D.rows; }

  function refreshOptions() {
    var d = data();
    options($("f-severity"), uniq(d, "severity", function (a, b) { return sevRank(a) - sevRank(b); }), "All");
    var tiers = uniq(d, "validation_tier");
    var sel = $("f-tier"), cur = sel.value; sel.textContent = ""; sel.appendChild(el("option", {value: ""}, "All"));
    tiers.forEach(function (t) { sel.appendChild(el("option", {value: t}, D.tiers[t] || t)); }); if (tiers.indexOf(cur) >= 0) sel.value = cur;
    options($("f-rule"), uniq(d, "rule_id"), "All");
    options($("f-skill"), uniq(d, "skill_id"), "All");
    options($("f-kind"), uniq(D.rows, "finding_kind"), "All");
    options($("f-config"), D.configurations, "All");
    document.querySelectorAll("[data-unit=rows]").forEach(function (n) { n.style.display = state.unit === "rows" ? "" : "none"; });
  }

  function filtered() {
    var q = $("f-q").value.trim().toLowerCase(), sev = $("f-severity").value, tier = $("f-tier").value, rule = $("f-rule").value,
        skill = $("f-skill").value, kind = $("f-kind").value, cfg = $("f-config").value, prim = $("f-primary").checked;
    var out = data().filter(function (r) {
      if (sev && r.severity !== sev) return false;
      if (tier && r.validation_tier !== tier) return false;
      if (rule && r.rule_id !== rule) return false;
      if (skill && r.skill_id !== skill) return false;
      if (state.unit === "rows") { if (kind && r.finding_kind !== kind) return false; if (cfg && r.configuration !== cfg) return false; }
      if (prim && !(state.unit === "rows" ? r.run_outcome === "complete" : r.in_primary_analysis)) return false;
      if (q) {
        var hay = [r.rule_id, r.skill_id, r.repo, r.file_path, r.title, r.snippet, r.description, r.review_id, r.cisco_category, r.configuration, r.configurations]
                  .map(str).join(" \u0001 ").toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });
    if (state.sort) {
      var k = state.sort, dir = state.dir;
      out = out.slice().sort(function (a, b) {
        var x = a[k], y = b[k];
        if (k === "severity") { x = sevRank(x); y = sevRank(y); }
        if (x === null || x === undefined) return 1; if (y === null || y === undefined) return -1;
        if (typeof x === "number" && typeof y === "number") return (x - y) * dir;
        return String(x).localeCompare(String(y), undefined, {numeric: true}) * dir;
      });
    }
    return out;
  }

  function cell(key, r) {
    var td = el("td");
    if (key === "severity") td.appendChild(sevBadge(r.severity));
    else if (key === "validation_tier") td.appendChild(tierBadge(r.validation_tier));
    else td.textContent = str(r[key]);
    if (key === "reported_line_number") td.className = "num";
    return td;
  }

  function detailRow(r, ncols) {
    var tr = el("tr", {"class": "detail"}), td = el("td", {colspan: String(ncols)}), grid = el("div", {"class": "detail-grid"});
    DETAIL[state.unit].forEach(function (p) {
      var v = r[p[0]]; if (v === null || v === undefined || v === "") return;
      grid.appendChild(el("b", null, p[1])); grid.appendChild(el("span", null, str(v)));
    });
    td.appendChild(grid);
    td.appendChild(el("div", {"class": "muted"}, "Evidence snippet (untrusted skill text, shown verbatim as plain text after redaction):"));
    td.appendChild(el("pre", {"class": "snippet"}, str(r.snippet) || "(no snippet)"));
    tr.appendChild(td); return tr;
  }

  function render() {
    var cols = COLS[state.unit], rows = filtered(), thead = document.querySelector("#explorer thead"), tbody = document.querySelector("#explorer tbody");
    thead.textContent = ""; tbody.textContent = "";
    var hr = el("tr");
    cols.forEach(function (c) {
      var th = el("th", {scope: "col", tabindex: "0"}, c[1]);
      if (state.sort === c[0]) th.setAttribute("aria-sort", state.dir > 0 ? "ascending" : "descending");
      var go = function () { if (state.sort === c[0]) state.dir = -state.dir; else { state.sort = c[0]; state.dir = 1; } render(); };
      th.addEventListener("click", go); th.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    rows.slice(0, state.shown).forEach(function (r, i) {
      var id = (r.finding_id || r.finding_ids || "") + "|" + r.skill_id + "|" + (r.configuration || "") + "|" + r.rule_id + "|" + r.reported_line_number;
      var tr = el("tr", {"class": "item", tabindex: "0", "aria-expanded": state.open[id] ? "true" : "false"});
      cols.forEach(function (c) { tr.appendChild(cell(c[0], r)); });
      var toggle = function () { state.open[id] = !state.open[id]; render(); };
      tr.addEventListener("click", toggle); tr.addEventListener("keydown", function (e) { if (e.key === "Enter") toggle(); });
      tbody.appendChild(tr);
      if (state.open[id]) tbody.appendChild(detailRow(r, cols.length));
    });
    if (!rows.length) { var tr = el("tr"); tr.appendChild(el("td", {colspan: String(cols.length), "class": "muted"}, "No alerts match these filters.")); tbody.appendChild(tr); }
    var total = data().length, unit = state.unit === "locations" ? "distinct alert locations" : "finding rows";
    $("count").textContent = "Showing " + Math.min(rows.length, state.shown) + " of " + rows.length + " matching " + unit + " (" + total + " in total).";
    $("more").hidden = rows.length <= state.shown;
  }

  function csvCell(v) {
    var s = str(v);
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;          // keep spreadsheets from evaluating untrusted text as a formula
    return /[",\n\r]/.test(s) ? "\"" + s.replace(/"/g, "\"\"") + "\"" : s;
  }
  function downloadCsv() {
    var rows = filtered(); if (!rows.length) return;
    var keys = Object.keys(rows[0]);
    var text = [keys.join(",")].concat(rows.map(function (r) { return keys.map(function (k) { return csvCell(r[k]); }).join(","); })).join("\n");
    var a = el("a", {href: URL.createObjectURL(new Blob([text], {type: "text/csv"})), download: "filtered_" + state.unit + ".csv"});
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }

  ["f-q", "f-severity", "f-tier", "f-rule", "f-skill", "f-kind", "f-config", "f-primary"].forEach(function (id) {
    $(id).addEventListener(id === "f-q" ? "input" : "change", function () { state.shown = PAGE; render(); });
  });
  $("f-unit").addEventListener("change", function () { state.unit = this.value; state.sort = null; state.open = {}; state.shown = PAGE; refreshOptions(); render(); });
  $("f-reset").addEventListener("click", function () {
    ["f-q", "f-severity", "f-tier", "f-rule", "f-skill", "f-kind", "f-config"].forEach(function (id) { $(id).value = ""; });
    $("f-primary").checked = false; state.sort = null; state.open = {}; state.shown = PAGE; render();
  });
  $("f-csv").addEventListener("click", downloadCsv);
  $("more").addEventListener("click", function () { state.shown += PAGE; render(); });

  // ---------------------------------------------------------------- skills table
  var SCOLS = [["skill_id", "Skill"], ["repo", "Repository"], ["sample_stratum", "Stratum"], ["coverage", "Coverage"],
               ["complete_scans", "Complete / planned"], ["security_locations_any", "Alert locations"], ["max_security_severity", "Max severity"],
               ["metadata_quality_rows", "Metadata notes"], ["review_items", "Review items"], ["human_validated_items", "Human-validated"], ["_actions", ""]];
  var sstate = {sort: "security_locations_any", dir: -1};
  function renderSkills() {
    var q = $("s-q").value.trim().toLowerCase(), only = $("s-sec").checked;
    var rows = D.skills.filter(function (r) {
      if (only && !r.security_locations_any) return false;
      return !q || [r.skill_id, r.repo, r.skill_path, r.sample_stratum, r.coverage].map(str).join(" ").toLowerCase().indexOf(q) >= 0;
    }).sort(function (a, b) {
      var k = sstate.sort, x = a[k], y = b[k];
      if (k === "max_security_severity") { x = sevRank(x); y = sevRank(y); }
      if (typeof x === "number" && typeof y === "number") return (x - y) * sstate.dir;
      return str(x).localeCompare(str(y), undefined, {numeric: true}) * sstate.dir;
    });
    var thead = document.querySelector("#skills-table thead"), tbody = document.querySelector("#skills-table tbody");
    thead.textContent = ""; tbody.textContent = "";
    var hr = el("tr");
    SCOLS.forEach(function (c) {
      var th = el("th", {scope: "col", tabindex: "0"}, c[1]);
      if (sstate.sort === c[0]) th.setAttribute("aria-sort", sstate.dir > 0 ? "ascending" : "descending");
      if (c[0] !== "_actions") th.addEventListener("click", function () { if (sstate.sort === c[0]) sstate.dir = -sstate.dir; else { sstate.sort = c[0]; sstate.dir = 1; } renderSkills(); });
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    rows.forEach(function (r) {
      var tr = el("tr");
      SCOLS.forEach(function (c) {
        var td = el("td");
        if (c[0] === "complete_scans") { td.textContent = r.complete_scans + " / " + r.planned_scans; td.className = "num"; }
        else if (c[0] === "max_security_severity") { if (r.max_security_severity) td.appendChild(sevBadge(r.max_security_severity)); }
        else if (c[0] === "_actions") {
          if (r.security_locations_any) {
            var b = el("button", {type: "button"}, "Alerts");
            b.addEventListener("click", function () { $("f-unit").value = "locations"; state.unit = "locations"; refreshOptions(); $("f-skill").value = r.skill_id; state.shown = PAGE; render(); location.hash = "#alerts"; });
            td.appendChild(b);
          }
          if (r.detail_page) { var a = el("a", {href: "../" + r.detail_page}, " page"); td.appendChild(a); }
        } else { td.textContent = str(r[c[0]]); if (typeof r[c[0]] === "number") td.className = "num"; }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }
  $("s-q").addEventListener("input", renderSkills); $("s-sec").addEventListener("change", renderSkills);

  refreshOptions(); render(); renderSkills();
})();
"""
