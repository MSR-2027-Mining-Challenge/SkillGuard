# Skill `ctf-reverse-72b8c1549125`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | wgpsec/AboutSecurity |
| SKILL.md path | skills/ctf/ctf-reverse/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · references/patterns-ctf.md:204
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 250a79d48c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(
```
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · references/tools-advanced.md:443
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3c81b6b84b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
rip = int(gdb.parse_and_eval('$rip'))
```
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · references/tools-dynamic.md:282
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 23b82361c5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
result = found.solver.eval(flag, cast_to=bytes)
```
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · references/tools-dynamic.md:370
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e71485e30c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
concrete_data = self.state.solver.eval(
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · references/tools-emulation.md:178
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 425ffcce96 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
proc = subprocess.Popen(
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
