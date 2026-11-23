"""SkillGuard V3.2 security taxonomy and capability catalog.

Three layers are kept strictly apart (see docs/skillguard_v3.2_schema.md):

* ``capability``      - something the skill can make the agent or host do. Neutral evidence.
* ``risk_indicator``  - a property or combination that raises review priority. Not a verdict.
* ``confirmed_issue`` - only assigned from an external, human validation record
                        (``--validations``). SkillGuard never assigns it on its own.

Severity  = impact if the capability were abused (info < low < medium < high < critical).
Confidence = how certain the detection itself is (high / medium / low), derived from how the
             evidence was obtained (parsed config or fully resolved code vs prose regex).
These are independent: a high-severity capability can have low confidence and vice versa.

Category IDs follow the SkillGuard V3.2 research plan (T1-T9). Framework mappings are given
only where the plan verified them; they are informational, not claims of equivalence.
"""

from __future__ import annotations

SEVERITIES = ["info", "low", "medium", "high", "critical"]
CONFIDENCES = ["low", "medium", "high"]

CATEGORIES = {
    "T1": "Instruction manipulation and prompt injection",
    "T2": "Autonomy and oversight control",
    "T3": "Agent-environment persistence and configuration tampering",
    "T4": "Credential and secret access",
    "T5": "Data egress",
    "T6": "Code execution and destructive operations",
    "T7": "Supply chain and provenance",
    "T8": "Declaration-behavior consistency and composition",
    "T9": "Evasion artifacts",
}

SUBCATEGORIES = {
    "T1.2": "Hidden instructions (HTML comments, invisible Unicode, disguised files)",
    "T1.3": "Deferred or future-session triggers",
    "T1.4": "Pre-approval or false-authority claims",
    "T2.1": "Approval-bypass instructions",
    "T2.2": "Permission flags, auto-approval settings and tool pre-approval",
    "T2.3": "Outward actions without confirmation",
    "T2.4": "Launching external agent programs",
    "T2.5": "Removing nested-agent guards (environment markers)",
    "T2.6": "Unattended scheduled agent runs",
    "T2.7": "In-host sub-agent delegation (host feature)",
    "T3.1": "Agent settings, hooks and startup commands",
    "T3.2": "MCP server registration",
    "T3.3": "Agent instruction, rules and memory files",
    "T3.4": "Skill installation into agent skill directories",
    "T3.5": "Operating-system persistence (schedulers, autostart, shell rc files)",
    "T3.6": "Model endpoint or proxy override",
    "T4.1": "Agent credential stores",
    "T4.2": "Developer credentials (SSH, cloud, registry tokens)",
    "T4.3": "Bulk environment harvesting",
    "T4.4": "Secrets embedded in configuration",
    "T5.1": "Outbound network transmission",
    "T5.2": "Network retrieval",
    "T6.1": "Remote fetch-and-execute",
    "T7.1": "Unpinned runtime packages",
    "T7.3": "Package registry or index redirection",
    "T7.4": "Install-time hooks",
    "T8.1": "Declared tools vs observed behavior",
    "T8.3": "Instructions that run bundled code",
    "T8.4": "Risky capability combinations",
}

# Framework references verified in the research plan (informational).
FRAMEWORKS = {
    "T1": ["OWASP LLM01:2025 Prompt Injection"],
    "T2": ["OWASP LLM06:2025 Excessive Agency"],
    "T3": ["MITRE ATLAS AML.T0081 Modify AI Agent Configuration (verify ID before citing)"],
    "T4": ["CWE-798 Use of Hard-coded Credentials"],
    "T6": ["CWE-94 Improper Control of Generation of Code"],
    "T7": ["OWASP LLM03:2025 Supply Chain"],
}

# capability -> (category, default subcategory, default severity, supporting, explanation, remediation)
# "supporting" capabilities (plain network use) are inventoried only to build combinations;
# they are excluded from headline counts and never get a review priority on their own.
CAPABILITIES = {
    "in_host_delegation": (
        "T2", "T2.7", "info", False,
        "The skill asks the agent to delegate work to sub-agents through the host's own feature "
        "(e.g. a Task/Agent tool). These run inside the host's permission system.",
        "No action needed unless the delegated work itself is sensitive."),
    "external_agent_launch": (
        "T2", "T2.4", "medium", False,
        "The skill starts a separate AI agent program (CLI). The child agent runs outside the "
        "parent session's approval flow and inherits the process environment.",
        "Prefer in-host delegation. If an external agent is required, document it, pass a "
        "minimal environment, and do not add permission-bypass flags."),
    "agent_env_marker_removal": (
        "T2", "T2.5", "medium", False,
        "Environment markers that agent CLIs use to detect nesting (e.g. CLAUDECODE) are removed, "
        "which defeats the host's guard against recursive agent launches.",
        "Do not strip agent nesting markers; if nesting is intended, document why."),
    "approval_bypass_instruction": (
        "T2", "T2.1", "medium", False,
        "Instruction text tells the agent to act without asking the user or to use a "
        "permission-bypass mode.",
        "Keep the user in the loop for consequential actions; scope any no-confirmation "
        "instruction to clearly harmless, local steps."),
    "auto_approval_setting": (
        "T2", "T2.2", "high", False,
        "A configuration enables auto-approval or a permission-bypass mode for agent actions.",
        "Remove auto-approval / bypass settings from shipped configuration; let users opt in."),
    "tool_preapproval": (
        "T2", "T2.2", "low", False,
        "Tools are pre-approved (allowed without prompting) by skill frontmatter or agent settings.",
        "Scope pre-approved tools to the exact commands the skill needs."),
    "agent_config_modification": (
        "T3", "T3.1", "medium", False,
        "The skill writes, copies into, or deletes agent configuration (settings, hooks, MCP "
        "servers, instruction/memory files, skill directories). Such changes persist beyond "
        "the current session and change how the agent behaves later.",
        "Do not modify agent configuration automatically; show the user the exact change and "
        "ask them to apply it."),
    "agent_hook_command": (
        "T3", "T3.1", "medium", False,
        "Agent configuration defines a command that the agent host runs automatically "
        "(hook, status line, credential helper, notifier).",
        "Avoid shipping hooks; if required, keep the command local, pinned and documented."),
    "mcp_server_definition": (
        "T3", "T3.2", "low", False,
        "Configuration registers an MCP server, i.e. a program or remote endpoint whose tools the "
        "agent will be able to call.",
        "Pin server packages to versions, prefer local servers, and do not auto-enable servers."),
    "scheduler_invocation": (
        "T3", "T3.5", "medium", False,
        "The skill lists or modifies scheduled tasks (cron, launchd, systemd, Windows tasks).",
        "Do not install scheduled jobs without explicit user consent; provide removal steps."),
    "os_persistence_write": (
        "T3", "T3.5", "high", False,
        "The skill writes to an operating-system autostart location (shell rc file, LaunchAgent, "
        "systemd unit, Startup folder).",
        "Do not modify autostart locations; document manual steps instead."),
    "agent_endpoint_override": (
        "T3", "T3.6", "high", False,
        "The model API endpoint or proxy for an agent is redirected. Requests and API keys would "
        "be sent to that endpoint.",
        "Do not override agent API endpoints in shipped code or configuration."),
    "agent_credential_access": (
        "T4", "T4.1", "high", False,
        "Agent login or API credential files are read or copied.",
        "Never read agent credential stores; use the documented authentication flow."),
    "developer_credential_access": (
        "T4", "T4.2", "high", False,
        "Developer credentials (SSH keys, cloud credentials, registry tokens) are read or copied.",
        "Access only credentials the task needs, via documented APIs, and never copy them."),
    "environment_harvesting": (
        "T4", "T4.3", "medium", False,
        "The entire process environment (which commonly contains API keys) is serialized or sent.",
        "Pass only the specific variables required."),
    "embedded_secret": (
        "T4", "T4.4", "medium", False,
        "A configuration contains what looks like a literal secret (value redacted).",
        "Remove the secret, rotate it, and read it from the environment instead."),
    "network_send": (
        "T5", "T5.1", "info", True,
        "Data is sent to a network destination.", ""),
    "network_fetch": (
        "T5", "T5.2", "info", True,
        "Content is retrieved from a network destination.", ""),
    "remote_fetch_execute": (
        "T6", "T6.1", "high", False,
        "Content downloaded from the network is executed directly (e.g. curl ... | sh).",
        "Download to a file, verify a pinned checksum or signature, then execute."),
    "install_time_hook": (
        "T7", "T7.4", "medium", False,
        "A bundled package manifest runs a script automatically at install time.",
        "Avoid install-time scripts; make setup an explicit, documented step."),
    "registry_redirect": (
        "T7", "T7.3", "medium", False,
        "Package installation is redirected to a non-default registry or index.",
        "Use the default registry or document and pin the alternative source."),
    "unpinned_package_execution": (
        "T7", "T7.1", "low", False,
        "A package is fetched and executed without a pinned version (e.g. npx -y pkg, @latest).",
        "Pin the package to an exact version."),
    "suspicious_agent_instruction": (
        "T1", "T1.3", "high", False,
        "A text block combines signals of hidden or deferred instructions aimed at the agent "
        "(future-session triggers, concealment, pre-approval claims, hidden content).",
        "Remove hidden or deferred instructions; state all behavior openly in SKILL.md."),
}

# Risk indicators attached to findings or chains (never verdicts).
RISK_INDICATORS = {
    "bypass_flags": "Permission-bypass or auto-approval flags are passed to an agent program.",
    "env_marker_removal": "Agent nesting guard is removed for this launch.",
    "credential_target": "Targets credential material.",
    "persistent_target": "Targets a location that persists across sessions.",
    "generated_code": "Code is generated into a string/file and runs later.",
    "network_in_command": "The automatically run command uses the network.",
    "fetch_execute_in_command": "The automatically run command downloads and executes code.",
    "non_official_endpoint": "Endpoint is not an official provider host.",
    "outward_action": "The no-confirmation instruction concerns an outward-facing action.",
    "unscoped_shell": "Shell access is pre-approved without a command scope.",
    "auto_enable": "Servers or tools are enabled without per-item user consent.",
    "invoked_by_instruction": "SKILL.md or another instruction tells the agent to run this file.",
    "concealment": "Wording asks to hide the action from the user.",
    "unpinned": "Package is not pinned to a version.",
    "insecure_transport": "Remote endpoint uses plain HTTP.",
}

# Composition chains (T8.4 / T8.3 / T2.6). (severity, explanation, remediation)
CHAINS = {
    "credential_access_with_network_send": (
        "T8.4", "high",
        "Credential material is read and data is sent over the network in the same "
        "{scope}. Together these form a possible exfiltration path (private data + external "
        "communication).",
        "Verify that credentials are only sent to the service they belong to, over TLS."),
    "bypass_with_external_agent": (
        "T8.4", "high",
        "An external agent program is launched while approval checks are disabled "
        "({scope}). The child agent can act without any human confirmation.",
        "Remove the bypass, or run the child agent in a sandbox with a restricted environment."),
    "nesting_guard_removed_for_agent_launch": (
        "T2.5", "high",
        "The nested-agent marker is removed and an external agent is launched ({scope}), which "
        "deliberately defeats the host's recursion guard.",
        "Use in-host delegation instead of spawning nested agent CLIs."),
    "fetch_execute_with_persistence": (
        "T8.4", "critical",
        "Remote code is downloaded and executed, and the skill also installs a persistence "
        "mechanism ({scope}). Remote content could then run repeatedly without review.",
        "Remove the persistence mechanism or pin and verify the downloaded content."),
    "script_installs_agent_config": (
        "T3.1", "high",
        "Code copies a bundled configuration into an agent configuration location, and that "
        "bundled configuration contains security-relevant settings ({scope}).",
        "Do not install agent configuration automatically; ask the user to review it."),
    "instruction_runs_sensitive_script": (
        "T8.3", "medium",
        "Instructions tell the agent to run a bundled file that contains security-relevant "
        "capabilities ({scope}). The capabilities therefore run as part of normal skill use.",
        "Document what the script does in SKILL.md and keep its effects minimal."),
    "scheduled_agent_run": (
        "T2.6", "high",
        "A scheduled task is installed and an external agent program is launched ({scope}), "
        "suggesting unattended agent runs.",
        "Avoid unattended agent runs; require the user to start them."),
    "preapproved_shell_runs_sensitive_script": (
        "T8.1", "high",
        "Shell access is pre-approved without scope, and instructions run a bundled script with "
        "security-relevant capabilities ({scope}); the script would run without a prompt.",
        "Scope allowed-tools to the exact script command, or drop the pre-approval."),
}

# Agent-config target kinds -> subcategory and severity.
CONFIG_TARGET_KINDS = {
    "hooks_or_settings": ("T3.1", "high"),
    "mcp_config": ("T3.2", "high"),
    "instructions_or_memory": ("T3.3", "medium"),
    "skills_dir": ("T3.4", "medium"),
    "rules": ("T3.3", "medium"),
    "agent_dir": ("T3.1", "medium"),
}


def severity_max(*values):
    present = [v for v in values if v in SEVERITIES]
    return max(present, key=SEVERITIES.index) if present else "info"


def severity_min(a, b):
    return min((a, b), key=SEVERITIES.index)


def bump(severity, steps=1):
    i = min(len(SEVERITIES) - 1, max(0, SEVERITIES.index(severity) + steps))
    return SEVERITIES[i]
