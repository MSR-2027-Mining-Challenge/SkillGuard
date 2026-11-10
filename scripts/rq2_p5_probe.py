#!/usr/bin/env python3
"""Non-destructive RQ2 P5 demonstration: compare year-blind cron with year-aware gating.

Only reads the sampled source and does NOT import/execute it. Does not run crontab.
This is a proposed design experiment, not validation of a patched production skill.
"""
from __future__ import annotations
import argparse, ast, hashlib, json
from datetime import datetime
from pathlib import Path
from datetime import timezone

DEFAULT_SOURCE='results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-09_135034_sam-sample30-seed2027/set-reminder-7652ed9105a8/full/scripts/set_reminder.py'
DEFAULT_OUT='results/rq2/fix_experiments/P5_set_reminder'

def cron_expression(dt):
    # Model of the observed 5-field expression, not imported code from the skill.
    return f'{dt.minute} {dt.hour} {dt.day} {dt.month} *'

def is_target_instant(now, target):
    # Proposed additional gate for a one-off reminder (minute resolution).
    return (now.year,now.month,now.day,now.hour,now.minute)==(target.year,target.month,target.day,target.hour,target.minute)

def run(repo:Path, source:str, output:str):
    # Resolve the base path too: macOS maps /var/... to /private/var/....
    repo = Path(repo).resolve()
    sourcepath=(repo/source).resolve(); dest=(repo/output).resolve()
    if not sourcepath.is_relative_to(repo) or not dest.is_relative_to(repo):
        raise ValueError('Source and output must be within repository')
    if not sourcepath.is_file():
        raise FileNotFoundError(f'Exported reminder source not found: {sourcepath}')
    src=sourcepath.read_text(encoding='utf-8',errors='replace')
    tree=ast.parse(src)  # parse only; no execution
    funcs=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=='_to_cron']
    if len(funcs)!=1:
        raise ValueError('Expected exactly one _to_cron function; manual inspection required')
    snippet=ast.get_source_segment(src,funcs[0]) or ''
    if not all(x in snippet for x in ['dt.minute','dt.hour','dt.day','dt.month']):
        raise ValueError('Unexpected _to_cron body; do not assume a yearless cron generator')
    a=datetime(2027,1,1,9,0); b=datetime(2028,1,1,9,0)
    assert cron_expression(a)==cron_expression(b)
    tests=[
        {'clock':'2027-01-01T09:00','requested':'2028-01-01T09:00','cron_matches':True,
         'proposed_gate_allows_delivery':is_target_instant(a,b)},
        {'clock':'2028-01-01T09:00','requested':'2028-01-01T09:00','cron_matches':True,
         'proposed_gate_allows_delivery':is_target_instant(b,b)},
        {'clock':'2029-01-01T09:00','requested':'2028-01-01T09:00','cron_matches':True,
         'proposed_gate_allows_delivery':is_target_instant(datetime(2029,1,1,9),b)},
    ]
    assert [t['proposed_gate_allows_delivery'] for t in tests]==[False,True,False]
    dest.mkdir(parents=True,exist_ok=True)
    record={'experiment':'P5 year-blind cron vs proposed target-year gate',
            'source_path':str(sourcepath.relative_to(repo)),
            'source_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),
            'generated_utc':datetime.now(timezone.utc).isoformat(),
            'original_cron_2027':cron_expression(a),'original_cron_2028':cron_expression(b),
            'results':tests,'safe_static_inspection_only':True,
            'limitation':'Pure-function demonstration only; no modified skill or live cron testing.'}
    (dest/'p5_safe_probe.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    (dest/'TEST_PLAN.md').write_text('''# P5 — Isolated repair experiment

The sampled `set_reminder.py` is inspected with AST; it is **not executed**. This
non-destructive probe demonstrates why five-field cron schedules cannot enforce
a future target year and evaluates a proposed *additional year-aware guard*.

## Observations

- Jan 1 2027 09:00 and Jan 1 2028 09:00 generate the same five-field cron expression.
- The proposed year-aware condition rejects the early 2027 run, accepts the 2028
  target, and rejects a 2029 repeat.

## Remaining work (not claimed as completed)

1. Implement the guard in an **isolated copy** of the generated reminder script.
2. Ensure failed delivery does not delete the reminder prematurely (separate P4 defect).
3. Test timezones, daylight-saving transitions, leap dates, and retries.
4. Check whether another one-time scheduler is preferable.
5. Run a sandboxed integration test with no real notifications or crontab changes.

Do not describe this mathematical demonstration as a deployed or fully validated repair.
''',encoding='utf-8')
    print('Saved static P5 experiment:',dest/'p5_safe_probe.json')
    return record

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',default='.')
    p.add_argument('--source',default=DEFAULT_SOURCE)
    p.add_argument('--output',default=DEFAULT_OUT)
    x=p.parse_args();run(Path(x.repo).resolve(),x.source,x.output)
if __name__=='__main__':main()
