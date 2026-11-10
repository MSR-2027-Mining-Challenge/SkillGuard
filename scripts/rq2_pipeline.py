#!/usr/bin/env python3
"""RQ2 reproducibility driver: optionally rerun the existing notebook and build reports.

Nothing here executes an exported skill or changes an agent's crontab/processes.
The candidate CSV is read-only during reporting. Running the notebook separately
may regenerate it; a timestamped backup is made first.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tokenize
from io import StringIO

DEFAULT_RUN = 'results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-09_135034_sam-sample30-seed2027'
DEFAULT_CSV = 'results/rq2/seed2027_defect_screening/rq2_defect_candidates.csv'
DEFAULT_OUTPUT = 'results/rq2/reports'
DEFAULT_NOTEBOOK = 'notebooks/06_rq2_defect_detection_automated.ipynb'
DEFAULT_TAXONOMY = 'docs/rq2/rq2_defect_taxonomy_v0_1.json'
HUMAN_COLUMNS = ['candidate_status','impact','recommended_fix','investigation_notes']
ALLOWED_STATUSES = {'candidate','confirmed_in_snapshot','confirmed_defect',
                    'likely_false_positive','false_positive','unresolved','not_evaluable'}
REDACTIONS = [
    (re.compile(r'(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*[\'\"][^\'\"]{4,}[\'\"]'), '[REDACTED_CREDENTIAL]'),
    (re.compile(r'\b(?:AKIA|ASIA|ghp_|gho_|github_pat_|sk-)[A-Za-z0-9_-]{8,}'), '[REDACTED_TOKEN]'),
    (re.compile(r'(/Users|/home)/[A-Za-z0-9_.-]+'), r'\1/[REDACTED_USER]'),
]


def redact(value, limit=1200):
    s = str(value or '')
    for pat, repl in REDACTIONS:
        s = pat.sub(repl, s)
    return s[:limit]


def repo_path(root: Path, path: str, *, must_exist=False) -> Path:
    # macOS may expose the same temp folder as /var/... and /private/var/....
    # Canonicalize both operands before enforcing repository containment.
    root = Path(root).resolve()
    p = (root / path).resolve()
    if not p.is_relative_to(root):
        raise ValueError(f'Path outside repository is not permitted: {path!r}')
    if must_exist and not p.exists():
        raise FileNotFoundError(f'Missing required file or folder: {p}')
    return p


def source_file(root: Path, run: Path, row: dict):
    """Source exports are untrusted. Never follow symlinks, escape, or execute."""
    sid = row.get('skill_id', '')
    rel = row.get('file_path', '')
    if not sid or not rel or Path(sid).name != sid or not (run / sid / 'manifest.json').is_file():
        return None
    folder = (run / sid / 'full').resolve()
    if not folder.is_relative_to(root) or not folder.is_dir():
        return None
    p = (folder / rel).resolve()
    if not p.is_relative_to(folder) or not p.is_file() or p.is_symlink() or p.stat().st_size > 2_000_000:
        return None
    return p


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def load_candidates(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rd = csv.DictReader(f)
        fields = list(rd.fieldnames or [])
        rows = list(rd)
    needed = {'candidate_id', 'rule_id', 'skill_id', 'file_path', 'line_number'}
    if not needed.issubset(fields):
        raise ValueError(f'Candidate CSV lacks columns: {sorted(needed - set(fields))}')
    ids = [r['candidate_id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate candidate_id values in candidate CSV; refusing to summarize.')
    return rows, fields


def annotations(path):
    if not path.exists():
        return {}
    rows, fields = load_candidates(path)
    return {r['candidate_id']: {k: r.get(k,'') for k in HUMAN_COLUMNS if k in fields}
            for r in rows if (r.get('candidate_status','').strip() not in {'','candidate'}
                            or any((r.get(k) or '').strip() for k in HUMAN_COLUMNS if k!='candidate_status'))}


def run_notebook(root, notebook_path, source_run, taxonomy_path, output_csv):
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError as exc:
        raise RuntimeError('Install requirements-rq2.txt to run the notebook (nbclient/nbformat).') from exc
    npath = repo_path(root, notebook_path, must_exist=True)
    runpath = repo_path(root, source_run, must_exist=True)
    if not runpath.is_dir():
        raise ValueError('Source run must be a directory of saved skill manifests.')
    repo_path(root, taxonomy_path, must_exist=True)
    nb = nbformat.read(npath, as_version=4)
    cfg_idx = next((i for i,c in enumerate(nb.cells) if c.cell_type == 'code' and 'SOURCE_RUN =' in c.source and 'OUTPUT_DIR =' in c.source), None)
    if cfg_idx is None:
        raise RuntimeError('Notebook configuration cell not found; cannot parameterize safely.')
    out_dir_rel = str(output_csv.parent.relative_to(root))
    nb.cells[cfg_idx].source = (
        f'SOURCE_RUN = {source_run!r}\n'
        f'TAXONOMY_PATH = {taxonomy_path!r}\n'
        f'OUTPUT_DIR = {out_dir_rel!r}\n'
        'MAX_EVIDENCE_CHARS = 200\n'
    )
    print('Running existing RQ2 detector notebook (static skill inspection only)...', flush=True)
    NotebookClient(nb, timeout=600, kernel_name='python3',
                   resources={'metadata': {'path': str(root)}}, allow_errors=False).execute()
    if not output_csv.is_file():
        raise RuntimeError('Notebook finished without producing the expected candidate CSV.')
    print('Notebook completed:', output_csv)


def code_line_type(path: Path, line_number: int):
    if not path or path.suffix != '.py' or line_number <= 0:
        return 'unknown'
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
        for tok in tokenize.generate_tokens(StringIO(text).readline):
            if tok.start[0] <= line_number <= tok.end[0]:
                if tok.type == tokenize.COMMENT:
                    return 'comment'
                if tok.type == tokenize.STRING and tok.start[0] < line_number:
                    return 'string_or_docstring'
        src = text.splitlines()[line_number - 1].lstrip()
        return 'comment' if src.startswith('#') else 'code'
    except (OSError, IndexError, tokenize.TokenError, IndentationError, SyntaxError):
        return 'unknown'


def read_context(path: Path | None, line: int, radius=3):
    if path is None:
        return 'Source not available in the exported snapshot.'
    try:
        lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    except OSError:
        return 'Source could not be opened.'
    lo, hi = max(1, line-radius), min(len(lines), max(1,line)+radius)
    return '\n'.join(f'{i:5d} {redact(lines[i-1],500)}' for i in range(lo,hi+1))


def suggested_review(row: dict, path: Path | None, syntax_type: str):
    """Evidence-only triage; NEVER changes researcher assessments."""
    rule = row.get('rule_id', '')
    line = int(row.get('line_number') or 0)
    excerpt = row.get('supporting_excerpt','')
    signal = row.get('signal','')
    if path is None:
        return 'needs_review', 'Source export unavailable/incomplete; do not infer a defect.'
    if rule in {'P4', 'R6.4'} and syntax_type in {'comment','string_or_docstring'}:
        if rule == 'R6.4' and 'brew install' in excerpt.lower() and 'pip3 install' in excerpt.lower():
            return 'likely_false_positive', 'Homebrew is documented as an option alongside pip3; check skill-wide requirements.'
        return 'trace_to_executable_code', 'Warning is located in documentation/comment; inspect actual commands elsewhere in the script.'
    if rule == 'P4':
        if re.search(r'crontab.{0,8}-l', excerpt):
            return 'likely_false_positive', 'This crontab -l invocation only reads cron entries; examine separate writes.'
        if re.search(r'os\.kill\s*\(', excerpt):
            return 'needs_review', 'Process termination is executable; check ownership, user approval and call sites.'
        if re.search(r'(?:os\.remove|\.unlink)\s*\(', excerpt):
            return 'needs_review', 'Deletion occurs; trace file provenance, failure path, and retry/checkpoint semantics.'
    if rule == 'P5':
        try:
            src = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            src = ''
        cron_func = re.search(r'def _to_cron.*?(?=\ndef |\Z)', src, re.S)
        if cron_func and '{dt.month}' in cron_func.group(0) and 'dt.year' not in cron_func.group(0):
            return 'reproducible_static_issue', 'Five-field cron output omits year; safe mathematical regression example is in repair plans.'
    if rule == 'S2':
        first = path.read_text(encoding='utf-8', errors='replace').splitlines()[:1]
        if not first or first[0].strip() != '---':
            return 'strong_spec_evidence', 'The SKILL.md file does not begin with the required --- YAML delimiter.'
        try:
            import yaml
            text = path.read_text(encoding='utf-8', errors='replace')
            fm = text.split('---',2)
            if len(fm) >= 3:
                yaml.safe_load(fm[1])
            return 'needs_review', 'The opening delimiter is present; re-check malformed YAML/required keys.'
        except ImportError:
            return 'needs_yaml_parser', 'PyYAML unavailable; YAML syntax needs verification.'
        except Exception as exc:
            return 'strong_spec_evidence', 'YAML parser rejects frontmatter (' + type(exc).__name__ + ').'
    if rule == 'S3':
        skill_path = row.get('skill_path', '')
        return 'strong_spec_evidence', 'Compare YAML name against lowercase-hyphen convention and parent directory: ' + Path(skill_path).parent.name
    if rule == 'P1':
        if 'scripts/tools' in (signal + ' ' + excerpt).lower():
            return 'likely_false_positive', 'Slash-delimited prose can be mistaken for a supporting path; confirm in context.'
        return 'needs_repo_check', 'Relative path may refer to the skill, repository root, or a different skill; export is not a full repository checkout.'
    if rule == 'R6.4':
        return 'needs_review', 'Determine whether the OS-specific utility is required and whether a cross-platform fallback is documented.'
    return 'needs_review', 'Manual interpretation required; rule-level screening alone cannot confirm a defect.'


def compact_name(row):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', row.get('candidate_id','unknown'))[:80]


def score_status(status):
    return status.strip() if status.strip() in ALLOWED_STATUSES else (status.strip() or 'candidate')


def emit_html(destination, review_rows, status_count, rule_counts, metadata):
    data = []
    for r in review_rows:
        data.append({key: redact(r.get(key,''), 300) for key in
            ['candidate_id','rule_id','rule_name','skill_id','file_path','line_number',
             'candidate_status','suggestion','evidence','signal']})
    # Safe to embed untrusted strings in an HTML script; no literal '<' or closing scripts.
    payload = json.dumps(data, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    total = len(data)
    reviewed = sum(1 for r in review_rows if score_status(r.get('candidate_status','')) != 'candidate')
    nskills = len({r['skill_id'] for r in review_rows})
    n_rules = len(rule_counts)
    status_html = ''.join(f'<span class="mini">{html.escape(k)} <b>{v}</b></span>' for k,v in sorted(status_count.items()))
    htmltext = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SkillGuard — RQ2 Defect Screening</title><style>
:root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,Arial,sans-serif}*{box-sizing:border-box}
body{margin:0;background:#0d1117;color:#e6edf3}main{max-width:1280px;margin:auto;padding:34px 26px}
a{color:#6db7ff}h1{font-size:2rem;margin:0 0 6px}h2{font-size:1.35rem;margin-top:34px}
p{color:#9da7b3;line-height:1.6}.eyebrow{color:#7cb5e9;font-size:12px;letter-spacing:.12em;font-weight:750}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:27px 0}.card{background:#151b23;border:1px solid #30363d;border-radius:12px;padding:20px}
.card strong{font-size:1.9rem;display:block}.card small{color:#9da7b3}.minis{display:flex;gap:9px;flex-wrap:wrap}.mini{background:#1b2733;border:1px solid #30363d;border-radius:14px;padding:6px 10px;font-size:12px}
.controls{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}input,select{background:#0d1117;color:#e6edf3;border:1px solid #3b4654;border-radius:8px;padding:10px 13px;font-size:14px}
input{flex:2;min-width:210px}select{flex:1;min-width:150px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #30363d;padding:11px 12px;text-align:left;vertical-align:top}
th{color:#c9d1d9;background:#161b22;position:sticky;top:0}tr:nth-child(even){background:#151b23}code{font-family:ui-monospace,monospace;font-size:12px}
.tag{display:inline-block;border:1px solid #3c5b7b;color:#92caff;background:#17293a;padding:4px 8px;border-radius:7px;white-space:nowrap}
.small{font-size:12px;color:#9da7b3}section{margin:22px 0}.scroll{overflow-x:auto}.notice{border-left:3px solid #d0aa55;padding:9px 14px;background:#211d17;color:#d6c9ab}
@media(max-width:760px){.cards{grid-template-columns:repeat(2,1fr)}main{padding:20px 12px}}
</style></head><body><main><div class="eyebrow">SKILLGUARD / MSR 2027 / RQ2</div>
<h1>Defect screening &amp; review</h1><p>Reproducible candidate screening, provenance, and human-validation status. This report is generated from the existing RQ2 CSV.</p>
<div class="notice"><b>Warnings are not confirmed defects.</b> Automated suggestions are separate from researcher decisions. No sampled skill code is executed.</div>
<div class="cards"><div class="card"><strong>__COUNT__</strong><small>Candidate locations</small></div>
<div class="card"><strong>__SKILLS__</strong><small>Skills flagged</small></div>
<div class="card"><strong>__RULES__</strong><small>Rules triggered</small></div>
<div class="card"><strong>__REVIEWED__</strong><small>Annotated candidates</small></div></div>
<h2>Review status</h2><div class="minis">__STATUSES__</div>
<h2>Searchable candidate explorer</h2><p class="small">Search by skill, candidate ID, rule, path, or finding. Filtering does not change the underlying CSV.</p>
<div class="controls"><input id="q" placeholder="Filter candidate findings…" aria-label="Search candidates"/>
<select id="rule" aria-label="Rule"><option value="">All rules</option></select><select id="status" aria-label="Status"><option value="">All statuses</option></select></div>
<div class="small" id="filtered"></div><div class="scroll"><table><thead><tr><th>Candidate</th><th>Skill / location</th><th>Rule</th><th>Researcher status</th><th>Automated triage hint</th></tr></thead><tbody id="rows"></tbody></table></div>
<h2>Report directory</h2><p><a href="01_IMPORTANT_RESULTS/START_HERE.md">Main summary</a> · <a href="02_DETAILED_ANALYSIS/">Per-candidate evidence</a> · <a href="03_RAW_SCANNER_OUTPUT/">Input provenance</a> · <a href="04_HUMAN_VALIDATION/">Human validation</a></p>
<p class="small">Generated __WHEN__ UTC. Exported code and repository-root scanner data are not embedded in this HTML.</p></main>
<script>const data=__DATA__;const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
const q=document.getElementById('q'),rule=document.getElementById('rule'),status=document.getElementById('status'),body=document.getElementById('rows');
for(const [sel,key] of [[rule,'rule_id'],[status,'candidate_status']]){[...new Set(data.map(r=>r[key]))].sort().forEach(v=>{let o=document.createElement('option');o.value=v;o.textContent=v;sel.appendChild(o)})}
function render(){const text=q.value.toLowerCase();let items=data.filter(r=>(!rule.value||r.rule_id===rule.value)&&(!status.value||r.candidate_status===status.value)&&Object.values(r).some(v=>v.toLowerCase().includes(text)));
document.getElementById('filtered').textContent=`Showing ${items.length} of ${data.length} findings`;
body.innerHTML=items.map(r=>`<tr><td><code>${esc(r.candidate_id)}</code><div class="small">${esc(r.file_path)}:${esc(r.line_number)}</div></td><td>${esc(r.skill_id)}</td><td><span class="tag">${esc(r.rule_id)}</span><div class="small">${esc(r.rule_name)}</div></td><td>${esc(r.candidate_status)}</td><td>${esc(r.suggestion)}<div class="small">${esc(r.evidence)}</div></td></tr>`).join('')}
[q,rule,status].forEach(el=>el.addEventListener('input',render));render();</script></body></html>'''
    replacements = {'__COUNT__':str(total),'__SKILLS__':str(nskills),'__RULES__':str(n_rules),
        '__REVIEWED__':str(reviewed),'__STATUSES__':status_html,'__DATA__':payload,
        '__WHEN__':html.escape(metadata['generated_at_utc'])}
    for k,v in replacements.items(): htmltext = htmltext.replace(k,v)
    destination.write_text(htmltext,encoding='utf-8')


def report(root: Path, csv_path: Path, run: Path, out: Path, taxonomy: Path, original_annotations=None, notebook=DEFAULT_NOTEBOOK):
    # Normalize all paths together to avoid macOS /var and /private/var aliases.
    root = Path(root).resolve()
    csv_path = Path(csv_path).resolve()
    run = Path(run).resolve()
    out = Path(out).resolve()
    taxonomy = Path(taxonomy).resolve()
    rows, fields = load_candidates(csv_path)
    out.mkdir(parents=True,exist_ok=True)
    d1 = out / '01_IMPORTANT_RESULTS'; d2=out/'02_DETAILED_ANALYSIS'
    d3=out/'03_RAW_SCANNER_OUTPUT'; d4=out/'04_HUMAN_VALIDATION'
    for d in (d1,d2,d3,d4,d2/'evidence'):
        d.mkdir(parents=True,exist_ok=True)
    # Remove only previously generated candidate evidence files (never user notes).
    for previous in (d2/'evidence').glob('*.md'):
        if re.fullmatch(r'[0-9a-f]{12}\.md', previous.name):
            previous.unlink()
    generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    review=[]; status_counter=Counter(); groups=defaultdict(list)
    unreviewed=0
    for r in rows:
        p = source_file(root,run,r)
        line = int(r.get('line_number') or 0)
        syntax_type = code_line_type(p,line)
        suggestion, reason = suggested_review(r,p,syntax_type)
        status = score_status(r.get('candidate_status') or '')
        status_counter[status]+=1
        if status=='candidate':unreviewed+=1
        k=(r.get('rule_id',''),r.get('skill_id',''))
        groups[k].append(r)
        reviewrow={**r,'candidate_status':status,'suggestion':suggestion,'evidence':reason,
                   'syntax_type':syntax_type,'source_available':str(p is not None).lower()}
        review.append(reviewrow)
        evidence_text=(
            f'# {r["candidate_id"]} — {redact(r.get("rule_id"),40)}\n\n'
            f'- Skill: `{redact(r.get("skill_id"),120)}`\n'
            f'- Repository: `{redact(r.get("repo"),160)}`\n'
            f'- Source path: `{redact(r.get("file_path"),180)}:{line}`\n'
            f'- Original signal: {redact(r.get("signal"),500)}\n'
            f'- Candidate status (human): **{status}**\n'
            f'- Automated hint (NOT validation): **{suggestion}** — {redact(reason)}\n'
            f'- Token context: `{syntax_type}`\n\n'
            '## Context (redacted; not executed)\n\n```text\n'
            + read_context(p,line).replace('```',"'''") + '\n```\n\n'
            '## Investigation\n\n'
            f'- Impact: {redact(r.get("impact"),1000) or "Not recorded"}\n'
            f'- Recommended fix: {redact(r.get("recommended_fix"),1000) or "Not recorded"}\n'
            f'- Researcher notes: {redact(r.get("investigation_notes"),1200) or "Not recorded"}\n\n'
            'This report is a research aid. It does not establish runtime failure.\n'
        )
        (d2/'evidence'/(compact_name(r)+'.md')).write_text(evidence_text,encoding='utf-8')
    rule_counts=Counter(r.get('rule_id','') for r in rows)
    rule_rows=[{'rule_id':k,'candidate_locations':v,'skills_affected':len({x['skill_id'] for x in rows if x['rule_id']==k}),
                'annotated':sum(score_status(x.get('candidate_status',''))!='candidate' for x in rows if x['rule_id']==k)} for k,v in sorted(rule_counts.items())]
    metadata={'generated_at_utc':generated_at,'candidate_csv':str(csv_path.relative_to(root)),
              'source_run':str(run.relative_to(root)) if run.is_relative_to(root) else str(run),
              'rule_count':len(rule_counts),'candidate_locations':len(rows),
              'skills_flagged':len({r['skill_id'] for r in rows}),
              'annotated_candidates':len(rows)-unreviewed,
              'methodology':'Original notebook detector + evidence-only automated triage; manual labels remain authoritative.'}
    write_csv(d1/'rule_summary.csv',rule_rows,['rule_id','candidate_locations','skills_affected','annotated'])
    suggestion_fields=['candidate_id','skill_id','rule_id','file_path','line_number',
                       'candidate_status','suggestion','evidence','syntax_type','source_available']
    def redacted_rows(items):
        return [{k: redact(v, 2000) for k,v in r.items()} for r in items]
    write_csv(d2/'automated_triage_hints.csv',redacted_rows(review),suggestion_fields)
    write_csv(d2/'candidate_review_queue.csv',redacted_rows(review),
              suggestion_fields+['signal','supporting_excerpt','investigation_notes','impact','recommended_fix'])
    write_csv(d4/'annotation_snapshot.csv',redacted_rows(rows), [c for c in ['candidate_id','skill_id','rule_id']+HUMAN_COLUMNS if c in fields])
    write_csv(d4/'unreviewed_candidates.csv', [r for r in review if r['candidate_status']=='candidate'],suggestion_fields)
    write_csv(d4/'status_summary.csv', [dict(status=k,count=v) for k,v in sorted(status_counter.items())],['status','count'])
    missing=[]
    if original_annotations:
        now_ids={r['candidate_id'] for r in rows}
        missing=[{'candidate_id':k,**v} for k,v in original_annotations.items() if k not in now_ids]
    write_csv(d4/'orphaned_previous_annotations.csv', missing, ['candidate_id']+HUMAN_COLUMNS)
    manifest_rows=[]
    if run.is_dir():
        for p in sorted(run.glob('*/manifest.json')):
            try:
                m=json.loads(p.read_text(encoding='utf-8'))
                manifest_rows.append({'skill_id':p.parent.name,'manifest_sha256':sha256(p),
                                      'folder_complete':m.get('folder_complete',''),
                                      'frontmatter_valid':m.get('frontmatter_valid',''),
                                      'file_count':len(m.get('files',[]))})
            except (OSError,ValueError):
                manifest_rows.append({'skill_id':p.parent.name,'manifest_sha256':'unreadable'})
    write_csv(d3/'manifest_index.csv',manifest_rows,['skill_id','manifest_sha256','folder_complete','frontmatter_valid','file_count'])
    input_files=[p for p in [csv_path,taxonomy,repo_path(root,notebook)] if p.is_file()]
    hashes=[{'repo_relative_path':str(p.relative_to(root)),'sha256':sha256(p),'bytes':p.stat().st_size} for p in input_files]
    write_csv(d3/'input_checksums.csv',hashes,['repo_relative_path','sha256','bytes'])
    metadata['input_checksums']=hashes
    (d3/'run_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    (d3/'README.md').write_text('# Raw input provenance\n\n'
      'Hashes and exported-manifest index only. Raw skill code is **not** copied into the public report.\n'
      'To regenerate it, use the local source run and the original notebook.\n',encoding='utf-8')
    (d2/'README.md').write_text('# Detailed analysis\n\n'
      '- `candidate_review_queue.csv`: candidate information with evidence-only hints.\n'
      '- `automated_triage_hints.csv`: machine suggestions **not written into human labels**.\n'
      '- `evidence/`: redacted line context and existing annotations per candidate.\n',encoding='utf-8')
    (d4/'README.md').write_text('# Human validation\n\n'
      'Only the researcher assessment fields are used: status, impact, fix and notes.\n'
      'No status is assigned by this reporting pipeline. To edit source labels, use:\n\n'
      '`python scripts/rq2_edit.py --ids <candidate-id>`\n\n'
      '`orphaned_previous_annotations.csv` records human annotations from the prior run whose IDs were not regenerated.\n',encoding='utf-8')
    status_lines='\n'.join(f'| {k} | {v} |' for k,v in sorted(status_counter.items()))
    rule_lines='\n'.join(f'| {x["rule_id"]} | {x["candidate_locations"]} | {x["skills_affected"]} | {x["annotated"]} |' for x in rule_rows)
    d1_summary=(f'# RQ2 — Start here\n\n**All scanner output consists of candidates, not confirmed defects.**\n\n'
       f'- **{len(rows)}** candidate locations; **{len(rule_counts)}** rules triggered; '
       f'**{len({r["skill_id"] for r in rows})}** skills flagged.\n'
       f'- **{len(rows)-unreviewed}** candidate statuses annotated by researchers; **{unreviewed}** remain unassessed.\n'
       f'- Source: `{metadata["source_run"]}`\n\n## Status summary\n\n| Status | Count |\n|---|---:|\n{status_lines}\n\n'
       f'## Rule summary\n\n| Rule | Locations | Skills | Annotated |\n|---|---:|---:|---:|\n{rule_lines}\n\n'
       '## Interpretation\n\nCounts represent flagged locations, not unique defects or independently validated failures. '
       'Auto-triage hints are not scientific labels. Missing exported resources may be outside the folder, '
       'and multi-location warnings may refer to the same underlying issue.\n\n'
       'Open `../02_DETAILED_ANALYSIS/candidate_review_queue.csv` for the review queue.\n')
    (d1/'START_HERE.md').write_text(d1_summary,encoding='utf-8')
    (d1/'README.md').write_text('# Important results\n\nStart with `START_HERE.md`. Generate `dashboard.html` locally using the pipeline.\n',encoding='utf-8')
    emit_html(out/'index.html', review, status_counter, rule_counts, metadata)
    # The screenshot uses a dashboard.html inside the important-results folder.
    emit_html(d1/'dashboard.html', review, status_counter, rule_counts, metadata)
    # Fix report-root relative navigation in the copy nested one directory deeper.
    nested=d1/'dashboard.html'
    nested_html=nested.read_text(encoding='utf-8')
    for folder in ('01_IMPORTANT_RESULTS','02_DETAILED_ANALYSIS','03_RAW_SCANNER_OUTPUT','04_HUMAN_VALIDATION'):
        nested_html=nested_html.replace(f'href="{folder}/', f'href="../{folder}/')
    nested.write_text(nested_html,encoding='utf-8')
    (out/'README.md').write_text(
       '# RQ2 — Reports and validation\n\n**Start here:** open `index.html` locally or read '
       '`01_IMPORTANT_RESULTS/START_HERE.md` on GitHub.\n\n'
       '| Folder | What you find there |\n|---|---|\n'
       '| `01_IMPORTANT_RESULTS/` | Published summary and rule counts; dashboard generated locally |\n'
       '| `02_DETAILED_ANALYSIS/` | Detailed evidence and review queues generated locally |\n'
       '| `03_RAW_SCANNER_OUTPUT/` | Input provenance generated locally; raw skill data excluded |\n'
       '| `04_HUMAN_VALIDATION/` | Published status summary; individual annotations remain local |\n\n'
       'The exported skill folders and raw scanner JSON remain local and are not packaged into this report.\n',encoding='utf-8')
    # Centralized LaTeX statistics. Output is user-regeneratable and safe to include.
    (d1/'rq2_auto_macros.tex').write_text(
       '% Generated RQ2 counts; not confirmed defect totals.\n'
       f'\\newcommand{{\\rqTwoCandidateLocations}}{{{len(rows)}}}\n'
       f'\\newcommand{{\\rqTwoRulesTriggered}}{{{len(rule_counts)}}}\n'
       f'\\newcommand{{\\rqTwoSkillsFlagged}}{{{len({r["skill_id"] for r in rows})}}}\n'
       f'\\newcommand{{\\rqTwoAnnotatedCandidates}}{{{len(rows)-unreviewed}}}\n',encoding='utf-8')
    print('Report:',out/'index.html')
    print('Summary:',d1/'START_HERE.md')
    print('Human validation:',d4/'annotation_snapshot.csv')
    print(f'Screening locations: {len(rows)} | Annotated: {len(rows)-unreviewed} | Unreviewed: {unreviewed}')
    if missing:
        print('WARNING: human annotations from vanished candidate IDs preserved at:',d4/'orphaned_previous_annotations.csv')
    return metadata


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default='.', help='SkillGuard repository root')
    p.add_argument('--csv', default=DEFAULT_CSV, help='Candidate CSV path inside repository')
    p.add_argument('--source-run', default=DEFAULT_RUN, help='Saved Cisco export directory inside repository')
    p.add_argument('--taxonomy', default=DEFAULT_TAXONOMY)
    p.add_argument('--notebook', default=DEFAULT_NOTEBOOK)
    p.add_argument('--output', default=DEFAULT_OUTPUT)
    p.add_argument('--execute-notebook',action='store_true',help='Rerun the real notebook before reporting (requires Jupyter deps)')
    args=p.parse_args(argv)
    root=Path(args.repo).expanduser().resolve()
    if not root.is_dir():p.error(f'Repository not found: {root}')
    try:
        csv_path=repo_path(root,args.csv)
        run=repo_path(root,args.source_run)
        taxonomy=repo_path(root,args.taxonomy)
        out=repo_path(root,args.output)
        prev=annotations(csv_path)
        if args.execute_notebook:
            if csv_path.exists():
                backups=repo_path(root,'results/rq2/backups');backups.mkdir(parents=True,exist_ok=True)
                stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
                dest=backups/f'rq2_candidates_before_rerun_{stamp}.csv'
                shutil.copy2(csv_path,dest)
                print('Backup of human-labeled CSV:',dest)
            run_notebook(root,args.notebook,args.source_run,args.taxonomy,csv_path)
        if not csv_path.is_file():
            raise FileNotFoundError(f'Candidate CSV not found: {csv_path}. Run the notebook first or add --execute-notebook.')
        report(root,csv_path,run,out,taxonomy,prev,args.notebook)
        return 0
    except (OSError,ValueError,RuntimeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
