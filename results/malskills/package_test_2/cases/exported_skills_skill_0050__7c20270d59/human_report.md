# Analysis Report: /mnt/c/Users/rio/Desktop/msr/SkillGuard/exported_skills/skill_0050

- Verdict: `malicious`
- Malicious patterns: Malware_Delivery, Remote_Code_Execution

## Artifact Inventory

- Artifacts: 34
- SSO findings: 17
- Operand resolutions: 0
- SSO facts: 17
- Operand facts: 17
- Value facts: 17

## Triggered Patterns
- `Malware_Delivery` [formal] (high, matches=1): Received content flows directly into execution or is executed through the same resolved payload object.
  - Rules: formal.graph.malware_delivery_memory
  - SSO IDs: sso_00000, sso_00001
- `Remote_Code_Execution` [formal] (high, matches=1): Network-controlled input flows into an execution-capable operation.
  - Rules: formal.graph.remote_code_execution
  - SSO IDs: sso_00000, sso_00001

## SSO Counts

- `data_receive`: 2
- `external_component_installation`: 2
- `file_read`: 1
- `system_command_execution`: 9
- `system_configuration_modify`: 1
- `system_information_access`: 2
