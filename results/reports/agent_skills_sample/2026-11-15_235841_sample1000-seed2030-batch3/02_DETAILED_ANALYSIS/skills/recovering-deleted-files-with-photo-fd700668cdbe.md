# Skill `recovering-deleted-files-with-photo-fd700668cdbe`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Molly-agi/Molly-Core |
| SKILL.md path | src/skills/registry/skills/cybersecurity/skills/recovering-deleted-files-with-photorec/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 6 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 6 | CRITICAL | exit code 0 |
| Full folder \| default | COMPLETE | 6 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMPOUND_FIND_EXEC · SKILL.md:116
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e35eaaf283 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Discovery and execution chain (find -exec) |
Evidence snippet:

```text
# PhotoRec outputs files into recup_dir.1, recup_dir.2, etc.
ls /cases/case-2024-001/recovered/all/

# Count recovered files by type
find /cases/case-2024-001/recovered/all/ -type f | \
   sed 's/.*\.//' | sort | uniq -c | sort -rn > /cases/case-2024-001/recovered/file_type_summary.txt

# Sort recov
```
### CRITICAL · COMPOUND_FIND_EXEC · SKILL.md:132
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9ec05e6a59 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Discovery and execution chain (find -exec) |
Evidence snippet:

```text
# Verify file integrity using file signatures
find /cases/case-2024-001/recovered/all/ -type f -exec file {} \; \
   > /cases/case-2024-001/recovered/file_signatures.txt

# Find files with mismatched extension/signature
while IFS= read -r line; do
   filepath=$(echo "$line" | cut -d: -f1)
   filetyp
```
### CRITICAL · COMPOUND_FIND_EXEC · SKILL.md:154
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dc6a960aa5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Discovery and execution chain (find -exec) |
Evidence snippet:

```text
# PhotoRec outputs files into recup_dir.1, recup_dir.2, etc.
ls /cases/case-2024-001/recovered/all/

# Count recovered files by type
find /cases/case-2024-001/recovered/all/ -type f | \
   sed 's/.*\.//' | sort | uniq -c | sort -rn > /cases/case-2024-001/recovered/file_type_summary.txt

# Sort recov
```
### HIGH · FIND_EXEC_PATTERN · SKILL.md:155
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d5507b644b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | find command with -exec flag can execute arbitrary commands on discovered files |
Evidence snippet:

```text
find . -name "*.$ext" -exec cp {} /cases/case-2024-001/recovered/sorted/$ext/ \;
```
### CRITICAL · COMPOUND_FIND_EXEC · SKILL.md:170
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2245c9ef72 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | exact |
| Title | Discovery and execution chain (find -exec) |
Evidence snippet:

```text
# Verify file integrity using file signatures
find /cases/case-2024-001/recovered/all/ -type f -exec file {} \; \
   > /cases/case-2024-001/recovered/file_signatures.txt

# Find files with mismatched extension/signature
while IFS= read -r line; do
   filepath=$(echo "$line" | cut -d: -f1)
   filetyp
```
### HIGH · FIND_EXEC_PATTERN · SKILL.md:190
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 67247912bb |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | find command with -exec flag can execute arbitrary commands on discovered files |
Evidence snippet:

```text
find /cases/case-2024-001/recovered/all/ -name "*.jpg" -exec jpeginfo -c {} \; 2>&1 | \
```
## Other notes

0 metadata-quality / scan-coverage rows: .
