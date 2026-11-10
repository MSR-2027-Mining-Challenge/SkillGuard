"""What one LLM/Meta experiment runs: scan configurations, LLM provider settings, prices and the configuration fingerprint.

Facts about Cisco Skill Scanner 2.3.1 that this module relies on were read from the installed package
(skill_scanner/cli/cli.py, core/analyzer_factory.py, core/analyzers/{llm_analyzer,meta_analyzer,llm_request_handler}.py);
docs/cisco_llm_meta_analyzers.md lists them with file references.
"""

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Baseline configurations produced by notebook 01. They are reused (copied, hash-checked), never re-run.
BASELINE_CONFIGS = [
    {"configuration": "SKILL.md only | default", "scope": "SKILL.md only", "analyzer_mode": "default",
     "report_file": "skill_only_default.json", "extra_args": [], "required_analyzers": ["static_analyzer"]},
    {"configuration": "SKILL.md only | behavioral", "scope": "SKILL.md only", "analyzer_mode": "behavioral",
     "report_file": "skill_only_behavioral.json", "extra_args": ["--use-behavioral"],
     "required_analyzers": ["static_analyzer", "behavioral_analyzer"]},
    {"configuration": "Full folder | default", "scope": "Full folder", "analyzer_mode": "default",
     "report_file": "full_folder_default.json", "extra_args": [], "required_analyzers": ["static_analyzer"]},
    {"configuration": "Full folder | behavioral", "scope": "Full folder", "analyzer_mode": "behavioral",
     "report_file": "full_folder_behavioral.json", "extra_args": ["--use-behavioral"],
     "required_analyzers": ["static_analyzer", "behavioral_analyzer"]},
]

# New configurations. All keep --use-behavioral so each differs from the "behavioral" baseline by exactly one switch
# (B = +LLM, C_det = +Meta, C = +LLM +Meta). --verbose only adds per-finding policy metadata and keeps the findings the
# Meta-Analyzer marks as false positives (with meta_false_positive=true) instead of deleting them; it is set on every
# new configuration so they are identical apart from the analyzer switches.
NEW_MODES = {
    "behavioral_llm": {"label": "B: static + behavioral + LLM", "flags": ["--use-behavioral", "--use-llm"],
                       "required_analyzers": ["static_analyzer", "behavioral_analyzer", "llm_analyzer"],
                       "uses_llm": True, "uses_meta": False},
    "behavioral_meta": {"label": "C-det: static + behavioral + Meta", "flags": ["--use-behavioral", "--enable-meta"],
                        "required_analyzers": ["static_analyzer", "behavioral_analyzer"],
                        "uses_llm": False, "uses_meta": True},
    "behavioral_llm_meta": {"label": "C: static + behavioral + LLM + Meta",
                            "flags": ["--use-behavioral", "--use-llm", "--enable-meta"],
                            "required_analyzers": ["static_analyzer", "behavioral_analyzer", "llm_analyzer"],
                            "uses_llm": True, "uses_meta": True},
}
SCOPES = {"SKILL.md only": ("skill_only", "only"), "Full folder": ("full_folder", "full")}
COMMON_ARGS = ["--format", "json", "--policy", "balanced"]
VERBOSE_ARGS = ["--verbose"]


def new_configs(modes):
    out = []
    for scope, (prefix, _) in SCOPES.items():
        for mode in modes:
            spec = NEW_MODES[mode]
            out.append({"configuration": f"{scope} | {mode.replace('_', '+')}", "scope": scope, "analyzer_mode": mode,
                        "report_file": f"{prefix}_{mode}.json", "extra_args": spec["flags"] + VERBOSE_ARGS,
                        "required_analyzers": spec["required_analyzers"], "uses_llm": spec["uses_llm"],
                        "uses_meta": spec["uses_meta"]})
    return out


def scope_folder(scope):
    return SCOPES[scope][1]


# USD per million tokens. Anthropic first-party rates from the claude-api reference (cached 2026-10-06), which match
# LiteLLM 1.106.6's bundled cost map. Haiku 5.5 has a higher rate above 100K-token prompts; Cisco's budgets keep
# prompts below that for the LLM Analyzer. A model missing here has unknown cost: paid runs then need explicit prices.
PRICES_PER_MTOK = {
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5": (2.00, 10.00),
    "gpt-4o": (2.50, 10.00),
    "gpt-5-mini": (0.25, 2.00),
}
PRICE_SOURCE = "claude-api reference pricing table (cached 2026-10-06), cross-checked with LiteLLM 1.106.6 model_cost"


@dataclass
class LLMSettings:
    """LLM provider settings passed to Cisco through its own environment variables (never via argv)."""
    model: str                                   # e.g. "ollama/skillscan-qwen3-4b-ctx64k" or "claude-sonnet-5-5"
    provider: str | None = None                  # SKILL_SCANNER_LLM_PROVIDER (None: Cisco infers it from the model)
    base_url: str | None = None
    temperature: str | None = None               # SKILL_SCANNER_LLM_TEMPERATURE; None keeps Cisco's default
    meta_model: str | None = None                # SKILL_SCANNER_META_LLM_MODEL; None = same model
    max_output_tokens: int | None = None         # --llm-max-tokens; None keeps the policy default (8192)
    reasoning_effort: str | None = None          # --llm-reasoning-effort; None keeps the provider default
    price_in_per_mtok: float | None = None
    price_out_per_mtok: float | None = None

    @property
    def is_local(self):
        return self.model.lower().startswith("ollama/")

    def prices(self):
        if self.is_local:
            return 0.0, 0.0
        if self.price_in_per_mtok is not None and self.price_out_per_mtok is not None:
            return self.price_in_per_mtok, self.price_out_per_mtok
        return PRICES_PER_MTOK.get(self.model.split("/")[-1], (None, None))

    def cost_usd(self, input_tokens, output_tokens):
        p_in, p_out = self.prices()
        if p_in is None:
            return None
        return round((input_tokens or 0) * p_in / 1e6 + (output_tokens or 0) * p_out / 1e6, 6)

    def env(self):
        """Environment for the Cisco subprocess. The API key is inherited from the caller's environment, never stored."""
        env = {"SKILL_SCANNER_LLM_MODEL": self.model, "LITELLM_LOCAL_MODEL_COST_MAP": "True"}
        for key, value in (("SKILL_SCANNER_LLM_PROVIDER", self.provider), ("SKILL_SCANNER_LLM_BASE_URL", self.base_url),
                           ("SKILL_SCANNER_LLM_TEMPERATURE", self.temperature),
                           ("SKILL_SCANNER_META_LLM_MODEL", self.meta_model)):
            if value is not None:
                env[key] = value
        return env

    def cli_args(self):
        args = []
        if self.max_output_tokens:
            args += ["--llm-max-tokens", str(self.max_output_tokens)]
        if self.reasoning_effort:
            args += ["--llm-reasoning-effort", self.reasoning_effort]
        return args


def resolved_request_settings(llm):
    """Temperature and max output tokens Cisco will actually send, computed with Cisco's own resolver functions."""
    out = {}
    try:
        from skill_scanner.core.analyzers.llm_request_handler import model_rejects_temperature
        from skill_scanner.core.scan_policy import ScanPolicy
        rejects = model_rejects_temperature(llm.model)
        explicit = llm.temperature
        if explicit is not None:
            value = None if explicit.strip().lower() in {"none", "null", "unset", "omit", "skip"} else float(explicit)
            out["llm_temperature"] = out["meta_temperature"] = value
        else:
            out["llm_temperature"] = None if rejects else 0.0     # LLMRequestHandler default
            out["meta_temperature"] = None if rejects else 0.1    # MetaAnalyzer default
        out["model_rejects_temperature"] = rejects
        out["max_output_tokens"] = llm.max_output_tokens or ScanPolicy.default().llm_analysis.max_output_tokens
        lp = ScanPolicy.default().llm_analysis
        out["llm_budgets_chars"] = {"max_instruction_body_chars": lp.max_instruction_body_chars,
                                    "max_code_file_chars": lp.max_code_file_chars,
                                    "max_referenced_file_chars": lp.max_referenced_file_chars,
                                    "max_total_prompt_chars": lp.max_total_prompt_chars,
                                    "meta_budget_multiplier": lp.meta_budget_multiplier}
        out["cisco_retry_policy"] = {"max_retries": 3, "rate_limit_delay_seconds": 2.0, "timeout_seconds": 120,
                                     "note": "LLMRequestHandler/MetaAnalyzer defaults (not configurable from the CLI)"}
        out["ollama_think"] = False if llm.is_local else None    # Cisco sends reasoning_effort=none -> think=false
    except Exception as exc:                                       # never fail a run over provenance
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


def ollama_info(model):
    """Digest, parameters and loaded context length of a local Ollama model (provenance)."""
    name = model.split("/", 1)[1]
    info = {"model": name}
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/show", data=json.dumps({"model": name}).encode(),
                                     headers={"Content-Type": "application/json"})
        show = json.loads(urllib.request.urlopen(req, timeout=10).read())
        info["parameters"] = show.get("parameters")
        info["details"] = show.get("details")
        info["num_ctx"] = next((int(line.split()[-1]) for line in (show.get("parameters") or "").splitlines()
                                if line.startswith("num_ctx")), None)
        tags = json.loads(urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10).read())
        info["digest"] = next((m["digest"] for m in tags["models"] if m["name"] in (name, f"{name}:latest")), None)
        version = json.loads(urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=10).read())
        info["ollama_version"] = version.get("version")
    except Exception as exc:
        info["error"] = f"{type(exc).__name__}: {exc}"
    return info


def scanner_path(root):
    for candidate in (Path(root) / ".venv/bin/skill-scanner", Path(root) / ".venv/Scripts/skill-scanner.exe"):
        if candidate.is_file():
            return str(candidate)
    return shutil.which("skill-scanner")


def environment_info(scanner):
    version = subprocess.run([scanner, "--version"], capture_output=True, text=True, timeout=60)
    pkgs = {}
    try:
        from importlib.metadata import version as pkg_version
        for name in ("cisco-ai-skill-scanner", "litellm", "pandas"):
            pkgs[name] = pkg_version(name)
    except Exception:
        pass
    return {"scanner_version": (version.stdout or version.stderr).strip(), "python": sys.version.split()[0],
            "platform": platform.platform(), "packages": pkgs}


@dataclass
class Experiment:
    name: str
    modes: list
    llm: LLMSettings
    timeout_seconds: int = 1800
    max_attempts: int = 3                 # per scan, including the first; Cisco itself also retries each request 3x
    backoff_seconds: float = 30.0         # base of the exponential backoff between attempts (capped at 15 min)
    workers: int = 1
    budget_usd: float | None = None       # required for paid providers; scans stop before exceeding it
    extra: dict = field(default_factory=dict)

    def configs(self):
        return new_configs(self.modes)

    def fingerprint(self, scanner_version):
        """Everything that changes what a scan returns. Resume refuses to mix results with different fingerprints."""
        llm = asdict(self.llm)
        for key in ("price_in_per_mtok", "price_out_per_mtok"):
            llm.pop(key)
        payload = {"scanner_version": scanner_version, "common_args": COMMON_ARGS, "llm": llm,
                   "configs": [{k: c[k] for k in ("configuration", "extra_args")} for c in self.configs()]}
        text = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(text.encode()).hexdigest(), payload

    def to_json(self):
        return {"name": self.name, "modes": self.modes, "llm": asdict(self.llm), "timeout_seconds": self.timeout_seconds,
                "max_attempts": self.max_attempts, "backoff_seconds": self.backoff_seconds, "workers": self.workers,
                "budget_usd": self.budget_usd, "extra": self.extra}

    @classmethod
    def from_json(cls, data):
        data = dict(data)
        data["llm"] = LLMSettings(**data["llm"])
        return cls(**data)


def api_key_present():
    return bool(os.environ.get("SKILL_SCANNER_LLM_API_KEY") or os.environ.get("SKILL_SCANNER_META_LLM_API_KEY"))
