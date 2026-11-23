# Cisco core vs core+ATR on the SkillGuard V3.2 controlled benchmark

Scanner: skill-scanner 2.3.1, policy balanced, behavioral analyzer on. Synthetic fixtures only.

A cell counts an expected V3.2 finding as *located* when the configuration reports a non-INFO finding in the same file within +/-3 lines. Locating is not the same as classifying it the same way.

| Capability (V3.2) | Expected | Cisco core | Cisco core + ATR |
|---|---|---|---|
| agent_config_modification | 4 | 1 | 1 |
| agent_credential_access | 1 | 0 | 0 |
| agent_endpoint_override | 2 | 1 | 1 |
| agent_env_marker_removal | 3 | 1 | 1 |
| agent_hook_command | 1 | 0 | 0 |
| auto_approval_setting | 4 | 0 | 0 |
| developer_credential_access | 1 | 1 | 1 |
| embedded_secret | 1 | 0 | 0 |
| environment_harvesting | 1 | 1 | 1 |
| external_agent_launch | 13 | 4 | 5 |
| in_host_delegation | 2 | 0 | 1 |
| install_time_hook | 1 | 0 | 0 |
| network_fetch | 1 | 1 | 1 |
| network_send | 1 | 1 | 1 |
| os_persistence_write | 4 | 0 | 0 |
| registry_redirect | 1 | 0 | 0 |
| remote_fetch_execute | 6 | 4 | 4 |
| scheduler_invocation | 4 | 2 | 2 |
| suspicious_agent_instruction | 2 | 2 | 2 |
| tool_preapproval | 1 | 0 | 0 |
| **total** | 54 | 19 | 21 |
