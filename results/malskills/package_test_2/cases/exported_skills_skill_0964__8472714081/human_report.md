# Analysis Report: /mnt/c/Users/rio/Desktop/msr/SkillGuard/exported_skills/skill_0964

- Verdict: `malicious`
- Malicious patterns: Malware_Delivery, Remote_Code_Execution

## Artifact Inventory

- Artifacts: 5
- SSO findings: 10
- Operand resolutions: 0
- SSO facts: 10
- Operand facts: 10
- Value facts: 10

## Triggered Patterns
- `Malware_Delivery` [formal] (high, matches=1): Received content flows directly into execution or is executed through the same resolved payload object.
  - Rules: formal.graph.malware_delivery_memory
  - SSO IDs: sso_00000, sso_00001
- `Remote_Code_Execution` [formal] (high, matches=1): Network-controlled input flows into an execution-capable operation.
  - Rules: formal.graph.remote_code_execution
  - SSO IDs: sso_00000, sso_00001

## SSO Counts

- `data_receive`: 3
- `external_component_installation`: 3
- `file_write`: 1
- `system_command_execution`: 3
