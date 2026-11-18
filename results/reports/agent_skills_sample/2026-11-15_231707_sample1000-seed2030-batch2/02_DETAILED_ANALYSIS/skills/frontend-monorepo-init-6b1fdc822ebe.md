# Skill `frontend-monorepo-init-6b1fdc822ebe`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | SunWind2000/skill-hub |
| SKILL.md path | frontend-monorepo-init/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 28 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 28 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · HIDDEN_DATA_FILE · assets/template/.agents/skills/frontend-monorepo-coder/SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1e651dd033 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · HIDDEN_DATA_FILE · assets/template/.agents/skills/frontend-monorepo-coder/agents/openai.yaml:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a02ca730f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · HIDDEN_DATA_FILE · assets/template/.agents/skills/frontend-ui-module-coder/SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5cf266e18b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · HIDDEN_DATA_FILE · assets/template/.agents/skills/frontend-ui-module-coder/agents/openai.yaml:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b89db05917 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · FILE_MAGIC_MISMATCH · assets/template/README.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b9386db887 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/apps/demo/package.json:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c38f0bc64a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vue": "^3.5.34"
```
### MEDIUM · FILE_MAGIC_MISMATCH · assets/template/eslint.config.ts:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 26eed8d1dd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 97b5d693ee |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@eslint/js": "^10.0.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 102dae4f5b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@types/node": "^24.10.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:20
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 40847960f2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@vitejs/plugin-vue": "^6.0.7"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1d6391fa93 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@vue/eslint-config-typescript": "^14.7.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 51c630a768 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@vue/test-utils": "^2.4.10"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f6b0e0443c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"eslint": "^10.4.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:24
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5b1d1aecbe |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"eslint-plugin-vue": "^10.9.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5ad3f24cd1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"globals": "^16.5.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 013482aea5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"jsdom": "^27.2.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 16e3014d5c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"jiti": "^2.6.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:28
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e4ceb8aeef |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"typescript": "^6.0.3"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eb1102f5d0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"typescript-eslint": "^8.59.4"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:30
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d20f4fbd6b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vite": "^8.0.13"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:31
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e0101c2053 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vite-plugin-dts": "^5.0.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a4f5d34ba |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vitest": "^4.1.7"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/package.json:33
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 11a9877bdb |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vue-tsc": "^3.3.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/packages/ui/package.json:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2e2585a726 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vue": "^3.5.34"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/playground/package.json:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e48cefd81b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vue": "^3.5.34"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/tests/ui/package.json:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f5e991a700 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@vue/test-utils": "^2.4.10"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · assets/template/tests/ui/package.json:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 11af7f527c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"vue": "^3.5.34"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
