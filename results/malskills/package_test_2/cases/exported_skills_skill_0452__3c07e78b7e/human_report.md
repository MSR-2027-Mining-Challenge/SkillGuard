# Analysis Report: /mnt/c/Users/rio/Desktop/msr/SkillGuard/exported_skills/skill_0452

- Verdict: `malicious`
- Malicious patterns: Malware_Delivery, Remote_Code_Execution

## Artifact Inventory

- Artifacts: 23
- SSO findings: 20
- Operand resolutions: 0
- SSO facts: 20
- Operand facts: 20
- Value facts: 20

## Triggered Patterns
- `Malware_Delivery` [formal] (high, matches=1): Received content flows directly into execution or is executed through the same resolved payload object.
  - Rules: formal.graph.malware_delivery_memory
  - SSO IDs: sso_00000, sso_00001
- `Remote_Code_Execution` [formal] (high, matches=1): Network-controlled input flows into an execution-capable operation.
  - Rules: formal.graph.remote_code_execution
  - SSO IDs: sso_00000, sso_00001

## SSO Counts

- `data_receive`: 2
- `dynamic_code_execution`: 2
- `external_component_installation`: 2
- `package_installation`: 7
- `system_command_execution`: 6
- `system_configuration_modify`: 1
