# Analysis Report: /mnt/c/Users/rio/Desktop/msr/SkillGuard/exported_skills/skill_0636

- Verdict: `malicious`
- Malicious patterns: Malware_Delivery, Remote_Code_Execution

## Artifact Inventory

- Artifacts: 17
- SSO findings: 31
- Operand resolutions: 0
- SSO facts: 31
- Operand facts: 31
- Value facts: 31

## Triggered Patterns
- `Malware_Delivery` [formal] (high, matches=1): Received content flows directly into execution or is executed through the same resolved payload object.
  - Rules: formal.graph.malware_delivery_memory
  - SSO IDs: sso_00020, sso_00021
- `Remote_Code_Execution` [formal] (high, matches=1): Network-controlled input flows into an execution-capable operation.
  - Rules: formal.graph.remote_code_execution
  - SSO IDs: sso_00020, sso_00021

## SSO Counts

- `data_receive`: 4
- `external_component_installation`: 2
- `file_delete`: 1
- `file_read`: 2
- `file_write`: 16
- `package_installation`: 2
- `system_command_execution`: 3
- `system_configuration_modify`: 1
