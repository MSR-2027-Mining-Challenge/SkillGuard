# Cisco Skill Scanner 2.3.1: LLM Analyzer and Meta-Analyzer (verified from the installed code)

Source of truth: `.venv/lib/python3.14/site-packages/skill_scanner/` (`cisco-ai-skill-scanner==2.3.1`, checked
2026-11-07). Paths below are relative to that folder. Where this disagrees with Cisco's docs, the code wins.

## Flags (`skill-scanner scan --help`)

| flag | effect |
|---|---|
| `--use-llm` | adds the LLM Analyzer (`core/analyzer_factory.py:195`) |
| `--enable-meta` | builds the Meta-Analyzer after the scan (`cli/cli.py:334`) |
| `--llm-provider {anthropic,openai,openai-compatible}` | provider shortcut; otherwise inferred from the model id |
| `--llm-max-tokens N` | max output tokens (default 8192 from `llm_analysis.max_output_tokens`) |
| `--llm-reasoning-effort LEVEL` | disabled/minimal/low/medium/high/xhigh/max; unset = provider default |
| `--llm-consensus-runs N` | N LLM runs, keep majority findings (N x cost) |
| `--llm-decompose` | one LLM pass per focus (about 3x calls) |
| `--adjudicate` | per-finding LLM check of deterministic HIGH/CRITICAL findings, demote-only |
| `--verbose` | keeps findings Meta marks as false positives (`meta_false_positive: true`) and adds per-finding policy metadata (`cli/cli.py:226`, `:649`) |

There is no CLI flag for the model, key, base URL or temperature. They come from environment variables:
`SKILL_SCANNER_LLM_MODEL`, `SKILL_SCANNER_LLM_API_KEY`, `SKILL_SCANNER_LLM_BASE_URL`, `SKILL_SCANNER_LLM_API_VERSION`,
`SKILL_SCANNER_LLM_PROVIDER`, `SKILL_SCANNER_LLM_TEMPERATURE` (`none` omits it). Meta has `SKILL_SCANNER_META_LLM_*`
overrides that fall back to the same variables (`cli/cli.py:353-356`).

## Providers, models, local inference

- Default model: `claude-sonnet-5-5` (`config/constants.py:31`). Provider defaults are in `core/analyzers/llm_analyzer.py:342`
  (openai `gpt-4o`, bedrock `bedrock/us.anthropic.claude-sonnet-5-5`, vertex `vertex_ai/gemini-3.8-flash`, ollama
  `ollama/llama2`, openrouter, orcarouter, azure, apple-fm).
- All calls go through LiteLLM (installed: 1.106.6). Gemini can also use google-genai.
- **Local inference is supported** through Ollama: a model id `ollama/<name>`. The endpoint must be a loopback `http://`
  URL (default `http://127.0.0.1:11434`, `core/analyzers/llm_provider_config.py:40`, `:75`). No API key is needed. For
  Ollama, Cisco always sends `reasoning_effort=none`, i.e. `think=false` (`llm_provider_config.py:477`), and forces
  LiteLLM's bundled cost map (`core/analyzers/llm_request_handler.py:213`). Cisco does **not** set `num_ctx`, so the
  Ollama server's context length applies. Prompts longer than it are silently truncated by Ollama, so this project uses
  `configs/ollama/skillscan-qwen3-4b-ctx64k.Modelfile` (num_ctx 65536).
- Credentials: `SKILL_SCANNER_LLM_API_KEY` for every hosted provider, AWS credentials for Bedrock, ADC for Vertex, and
  Entra ID for Azure.

## Request settings

- Temperature: 0.0 for the LLM Analyzer and 0.1 for Meta. Cisco omits temperature for models that reject it:
  Claude Sonnet 5.x, Opus 4.7 and later, Fable, Mythos, and OpenAI reasoning models (`llm_request_handler.py:257`).
  Claude Haiku 5.5 is *not* in that list, so on the current Anthropic API a Haiku run needs
  `SKILL_SCANNER_LLM_TEMPERATURE=none`.
- Retries: 3 retries with exponential backoff (2 s base) and a 120 s timeout per request (`llm_request_handler.py:344`).
  These cannot be set from the CLI.
- Prompt budgets (`data/default_policy.yaml:655`): SKILL.md body 20k chars, each code file 15k, each referenced file 10k,
  100k total. Meta gets 3x those budgets. Content that does not fit becomes an INFO finding `LLM_CONTEXT_BUDGET_EXCEEDED`
  instead of being cut silently.

## How the LLM Analyzer works

1. The deterministic analyzers run first: static, bytecode, pipeline and correlation, plus behavioral when requested.
2. **Phase 2** (`core/scanner.py:925`): the LLM Analyzer receives enrichment context built from those findings.
3. It makes **one call per scan** (unless consensus or decompose is set). The call contains the manifest, the SKILL.md
   body, code files and referenced files within the budgets, and a fixed system prompt that defines AITech categories
   and asks for a structured verdict.
4. Each returned finding gets `analyzer: "llm"`, a rule id such as `LLM_PROMPT_INJECTION` or `LLM_COMMAND_INJECTION`,
   and metadata `model`, `llm_verdict` (TRUE_POSITIVE / CONTEXTUAL_RISK), `llm_confidence` and `evidence_ids`. The line
   number is usually null.
5. Failures do **not** fail the scan. The exit code stays 0 and the report gets an INFO finding `LLM_ANALYSIS_FAILED`
   with `metadata.error` / `error_type` (`llm_analyzer.py:939`). A delimiter-injection attempt short-circuits with
   `LLM_PROMPT_INJECTION_DETECTED` and no LLM call (`:879`).
6. Deterministic findings are not changed by the LLM Analyzer. This was verified for every B/C scan; see
   `deterministic_reproducibility.csv`.

## How the Meta-Analyzer works

- **It is not independent.** It only post-processes the findings of the other analyzers (`MetaAnalyzer.analyze()` is
  a no-op that logs a warning). The CLI requires at least 2 analyzers (`cli/cli.py:348`). Static, bytecode, pipeline and
  correlation always count, so `--enable-meta` works **without `--use-llm`**, on deterministic findings only.
- It runs only if the scan has findings (`cli/cli.py:607`).
- **Routing** (`core/analyzers/meta_analyzer.py:1079`, `:1183`): Meta makes no LLM call when there are no findings, or
  when every finding is "clear deterministic evidence". That means INFO findings, and HIGH/CRITICAL findings from
  behavioral, bytecode, pipeline, analyzability, virustotal or correlation-with-flows (`:89`). Findings from `llm`,
  LLM-confidence LOW/MEDIUM, documentation/example contexts and non-INFO **static** findings are "ambiguous" and are
  sent to the LLM.
- Output (`apply_meta_analysis_to_results`, `:2525`): every original finding is kept, with
  `meta_false_positive`, `meta_reason`, `meta_confidence`, `meta_validated`, `meta_priority`; "missed threats" are added
  as findings with `analyzer: "meta"` and `metadata.meta_detected: true`. Without `--verbose`, the CLI then deletes the
  false positives (`cli/cli.py:649`). **Meta never changes severity.**
- Scan-level output: `scan_metadata.meta_risk_assessment` (risk_level, skill_verdict, meta_delta, and
  `meta_analysis_status` = `skipped_clear_deterministic` / `degraded`), `meta_correlations`, `meta_recommendations`;
  `"meta_analyzer"` is appended to `analyzers_used`.
- Failures are silent: an exception only logs `Meta-analysis failed: ...` to stderr, the exit code stays 0, and
  `meta_analyzer` is missing from `analyzers_used` (`cli/cli.py:646`). A malformed model response is retried once with a
  "contract repair" prompt. If that also fails, the batch is kept unchanged and marked `meta_analysis_degraded`.
  `gitskills_cisco_llm` reports both cases as PARTIAL with `meta_status` failed or degraded.

## Provenance in saved reports

- `analyzers_used`: `llm_analyzer`, `meta_analyzer`. Per finding: `analyzer` = `static` / `behavioral` / `pipeline` /
  ... / `llm` / `meta`.
- `llm_usage` (top level): `input_tokens`, `output_tokens`, `total_tokens`, summed over the LLM Analyzer, Meta and the
  adjudicator (`core/scanner.py:1078`, `meta_analyzer.py:2623`). It is **not split by analyzer**, has no cost field, and
  has no per-call latency.
- `scan_metadata.llm_overall_assessment` and `llm_primary_threats` (LLM Analyzer verdict).
- `--verbose` changes `policy_fingerprint_sha256`, because it changes finding-output flags. Only metadata differs; the
  deterministic findings were identical to the non-verbose baseline in every scan of this experiment.

## Tokens and cost

Cisco does not price calls. `gitskills_cisco_llm` multiplies `llm_usage` by the prices in `experiment.PRICES_PER_MTOK`
(Claude Sonnet 5.5 $2 in / $10 out per million tokens; Haiku 5.5 $0.10 / $0.50; Opus 5.5 $4 / $20). It then estimates
the cost of the same experiment from the tokens measured in this run (`llm_meta_analysis/cost_estimate_claude_sonnet_5_5.csv`).
