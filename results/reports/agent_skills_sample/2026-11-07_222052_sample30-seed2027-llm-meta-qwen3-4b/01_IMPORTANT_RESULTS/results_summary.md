# 2026-11-07_222052_sample30-seed2027-llm-meta-qwen3-4b: Cisco LLM Analyzer and Meta-Analyzer on the 30-skill sample
Source run: `results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027` (same sample manifest, seed 2027, same exported files; baseline reports copied and SHA-256 checked). Model: `ollama/skillscan-qwen3-4b-ctx64k` (local Ollama, no API cost). Execution state: **complete**.
Scanner alerts are candidates for investigation, not confirmed vulnerabilities. Provisional labels from the manual-review worksheet are AI-assisted and are not ground truth.
## Configurations
- A_static / A_behavioral: notebook-01 baseline (`default`, `--use-behavioral`), reused.
- B_llm: `--use-behavioral --use-llm --verbose`
- Cdet_meta: `--use-behavioral --enable-meta --verbose` (Meta over deterministic findings only)
- C_llm_meta: `--use-behavioral --use-llm --enable-meta --verbose`
All new configurations use `--format json --policy balanced` like the baseline. `--verbose` keeps findings that Meta marks as false positives (flag `meta_false_positive`) instead of deleting them.
## Coverage (denominators)
| configuration | analyzer_mode | label | planned | excluded_incomplete_folder | export_error | not_run_or_missing | executed | complete | contract_only | partial | failed | primary_core_complete | llm_ok | llm_failed | llm_not_queried | llm_prompt_budget_exceeded | meta_ran | meta_skipped_clear_deterministic | meta_not_invoked_no_findings | meta_degraded | meta_failed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKILL.md only \| default | default | A_static | 30 | 0 | 0 | 0 | 30 | 29 | 0 | 1 | 0 | 29 |  |  |  |  |  |  |  |  |  |
| SKILL.md only \| behavioral | behavioral | A_behavioral | 30 | 0 | 0 | 0 | 30 | 29 | 0 | 1 | 0 | 29 |  |  |  |  |  |  |  |  |  |
| Full folder \| default | default | A_static | 30 | 3 | 0 | 0 | 27 | 26 | 0 | 1 | 0 | 26 |  |  |  |  |  |  |  |  |  |
| Full folder \| behavioral | behavioral | A_behavioral | 30 | 3 | 0 | 0 | 27 | 26 | 0 | 1 | 0 | 26 |  |  |  |  |  |  |  |  |  |
| SKILL.md only \| behavioral+llm | behavioral_llm | B_llm | 30 | 0 | 0 | 0 | 30 | 29 | 0 | 1 | 0 | 29 | 30.0 | 0.0 | 0.0 | 3.0 |  |  |  |  |  |
| SKILL.md only \| behavioral+meta | behavioral_meta | Cdet_meta | 30 | 0 | 0 | 0 | 30 | 28 | 0 | 2 | 0 | 29 |  |  |  |  | 0.0 | 27.0 | 1.0 | 1.0 | 1.0 |
| SKILL.md only \| behavioral+llm+meta | behavioral_llm_meta | C_llm_meta | 30 | 0 | 0 | 0 | 30 | 6 | 0 | 24 | 0 | 29 | 30.0 | 0.0 | 0.0 | 3.0 | 6.0 | 0.0 | 0.0 | 23.0 | 1.0 |
| Full folder \| behavioral+llm | behavioral_llm | B_llm | 30 | 3 | 0 | 0 | 27 | 24 | 0 | 3 | 0 | 24 | 25.0 | 2.0 | 0.0 | 3.0 |  |  |  |  |  |
| Full folder \| behavioral+meta | behavioral_meta | Cdet_meta | 30 | 3 | 0 | 0 | 27 | 24 | 0 | 3 | 0 | 26 |  |  |  |  | 2.0 | 21.0 | 1.0 | 2.0 | 1.0 |
| Full folder \| behavioral+llm+meta | behavioral_llm_meta | C_llm_meta | 30 | 3 | 0 | 0 | 27 | 2 | 0 | 25 | 0 | 24 | 25.0 | 2.0 | 0.0 | 3.0 | 2.0 | 0.0 | 0.0 | 24.0 | 1.0 |
## Security findings per configuration (primary scans: static/behavioral/LLM core COMPLETE, LLM ok)
| configuration | label | primary_scans | security_rows_raw | security_rows_after_meta | security_rows_deterministic | security_rows_llm | security_rows_meta_added | skills_with_security_alert | skills_with_security_alert_after_meta | pct_scans_with_security_alert | critical_rows | high_rows | medium_rows | low_rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKILL.md only \| default | A_static | 29 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 3.4 | 0 | 1 | 0 | 0 |
| SKILL.md only \| behavioral | A_behavioral | 29 | 2 | 2 | 2 | 0 | 0 | 1 | 1 | 3.4 | 0 | 1 | 1 | 0 |
| SKILL.md only \| behavioral+llm | B_llm | 29 | 33 | 33 | 2 | 31 | 0 | 29 | 29 | 100.0 | 0 | 16 | 2 | 15 |
| SKILL.md only \| behavioral+meta | Cdet_meta | 29 | 2 | 2 | 2 | 0 | 0 | 1 | 1 | 3.4 | 0 | 1 | 1 | 0 |
| SKILL.md only \| behavioral+llm+meta | C_llm_meta | 29 | 34 | 34 | 2 | 30 | 2 | 29 | 29 | 100.0 | 1 | 15 | 3 | 15 |
| Full folder \| default | A_static | 26 | 9 | 9 | 9 | 0 | 0 | 4 | 4 | 15.4 | 2 | 2 | 4 | 1 |
| Full folder \| behavioral | A_behavioral | 26 | 11 | 11 | 11 | 0 | 0 | 4 | 4 | 15.4 | 2 | 2 | 6 | 1 |
| Full folder \| behavioral+meta | Cdet_meta | 26 | 13 | 13 | 11 | 0 | 2 | 4 | 4 | 15.4 | 4 | 2 | 6 | 1 |
| Full folder \| behavioral+llm | B_llm | 24 | 32 | 32 | 6 | 26 | 0 | 24 | 24 | 100.0 | 2 | 14 | 4 | 12 |
| Full folder \| behavioral+llm+meta | C_llm_meta | 24 | 34 | 34 | 6 | 28 | 0 | 24 | 24 | 100.0 | 2 | 15 | 6 | 11 |
## Deterministic findings unchanged by LLM / Meta?
| comparison | identical_pairs | pairs |
|---|---|---|
| A_behavioral -> B_llm | 53 | 53 |
| A_behavioral -> C_llm_meta | 53 | 53 |
| A_behavioral -> Cdet_meta | 55 | 55 |

## LLM-analyzer findings (B) vs deterministic alerts
| scope | relation | llm_security_rows |
|---|---|---|
| Full folder | LLM-only | 22 |
| Full folder | corroborated: deterministic alert in same file and category | 1 |
| Full folder | partly corroborated: same category, other file | 3 |
| SKILL.md only | LLM-only | 29 |
| SKILL.md only | corroborated: deterministic alert in same file and category | 2 |

## Meta-Analyzer decisions
| label | kind | analyzer | decision | rows | skills |
|---|---|---|---|---|---|
| C_llm_meta | metadata / coverage | llm | retained unreviewed: Meta response malformed (degraded) | 12 | 4 |
| C_llm_meta | metadata / coverage | llm | suppressed as false positive | 1 | 1 |
| C_llm_meta | metadata / coverage | skill_loader | retained unreviewed: Meta failed | 2 | 1 |
| C_llm_meta | metadata / coverage | static | retained unreviewed: Meta response malformed (degraded) | 49 | 27 |
| C_llm_meta | metadata / coverage | static | retained: validated by Meta | 5 | 5 |
| C_llm_meta | metadata / coverage | static | suppressed as false positive | 3 | 3 |
| C_llm_meta | security | behavioral | retained unreviewed: Meta response malformed (degraded) | 2 | 1 |
| C_llm_meta | security | behavioral | retained: validated by Meta | 1 | 1 |
| C_llm_meta | security | llm | retained unreviewed: Meta failed | 2 | 1 |
| C_llm_meta | security | llm | retained unreviewed: Meta response malformed (degraded) | 49 | 27 |
| C_llm_meta | security | llm | retained: validated by Meta | 9 | 7 |
| C_llm_meta | security | meta | added by Meta (missed threat) | 2 | 2 |
| C_llm_meta | security | static | retained unreviewed: Meta response malformed (degraded) | 9 | 4 |
| C_llm_meta | security | static | retained: validated by Meta | 1 | 1 |
| Cdet_meta | metadata / coverage | skill_loader | retained unreviewed: Meta failed | 2 | 1 |
| Cdet_meta | metadata / coverage | static | retained unreviewed: Meta response malformed (degraded) | 3 | 3 |
| Cdet_meta | metadata / coverage | static | retained: routing skipped (clear deterministic evidence, no LLM call) | 52 | 27 |
| Cdet_meta | metadata / coverage | static | retained: validated by Meta | 2 | 2 |
| Cdet_meta | security | behavioral | retained unreviewed: Meta response malformed (degraded) | 1 | 1 |
| Cdet_meta | security | behavioral | retained: validated by Meta | 2 | 1 |
| Cdet_meta | security | meta | added by Meta (missed threat) | 2 | 2 |
| Cdet_meta | security | static | retained unreviewed: Meta response malformed (degraded) | 8 | 3 |
| Cdet_meta | security | static | retained: validated by Meta | 2 | 2 |

## LLM run-to-run stability (B vs LLM part of C, identical input and settings)
47 of 53 skill-scope pairs gave the same LLM alert keys; mean Jaccard 0.90.

## Alerts unique to / shared by configurations
Restricted to 53 skill-scope pairs with a primary scan in every configuration.

| skill_scope_pairs_compared | configurations | analyzer | alerts | skills |
|---|---|---|---|---|
| 53 | B_llm+C_llm_meta | llm | 49 | 29 |
| 53 | A_static+A_behavioral+B_llm+Cdet_meta+C_llm_meta | static | 7 | 3 |
| 53 | C_llm_meta | llm | 6 | 6 |
| 53 | B_llm | llm | 5 | 5 |
| 53 | C_llm_meta | meta | 2 | 2 |
| 53 | A_behavioral+B_llm+Cdet_meta+C_llm_meta | behavioral | 1 | 1 |
| 53 | Cdet_meta | meta | 1 | 1 |

## Runtime and cost
| configuration | label | scans_timed | origin | wall_seconds_median | wall_seconds_mean | wall_seconds_p90 | wall_seconds_total | input_tokens_total | output_tokens_total | input_tokens_mean | output_tokens_mean | actual_cost_usd | same_tokens_at_claude-sonnet-5-5_usd | model |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKILL.md only \| default | A_static | 30 | baseline (copied) | 5.4 | 5.4 | 5.6 | 163.3 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | none |
| SKILL.md only \| behavioral | A_behavioral | 30 | baseline (copied) | 5.4 | 5.4 | 5.6 | 162.7 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | none |
| SKILL.md only \| behavioral+llm | B_llm | 30 | new scan | 33.7 | 35.9 | 44.3 | 1077.0 | 146890 | 10221 | 4896.3 | 340.7 | 0.0 | 0.396 | ollama/skillscan-qwen3-4b-ctx64k |
| SKILL.md only \| behavioral+meta | Cdet_meta | 30 | new scan | 4.9 | 8.5 | 5.0 | 253.9 | 23741 | 1128 | 791.4 | 37.6 | 0.0 | 0.0588 | ollama/skillscan-qwen3-4b-ctx64k |
| SKILL.md only \| behavioral+llm+meta | C_llm_meta | 30 | new scan | 59.2 | 65.3 | 107.9 | 1958.0 | 412814 | 41280 | 13760.5 | 1376.0 | 0.0 | 1.2384 | ollama/skillscan-qwen3-4b-ctx64k |
| Full folder \| default | A_static | 27 | baseline (copied) | 5.3 | 5.4 | 5.6 | 145.9 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | none |
| Full folder \| behavioral | A_behavioral | 27 | baseline (copied) | 5.4 | 5.4 | 5.8 | 147.1 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | none |
| Full folder \| behavioral+llm | B_llm | 27 | new scan | 32.0 | 42.2 | 51.9 | 1138.8 | 127679 | 8313 | 4728.9 | 307.9 | 0.0 | 0.3385 | ollama/skillscan-qwen3-4b-ctx64k |
| Full folder \| behavioral+meta | Cdet_meta | 27 | new scan | 4.9 | 25.1 | 63.2 | 677.5 | 85986 | 4019 | 3184.7 | 148.9 | 0.0 | 0.2122 | ollama/skillscan-qwen3-4b-ctx64k |
| Full folder \| behavioral+llm+meta | C_llm_meta | 27 | new scan | 71.2 | 91.6 | 164.6 | 2472.3 | 437458 | 43608 | 16202.1 | 1615.1 | 0.0 | 1.311 | ollama/skillscan-qwen3-4b-ctx64k |

## Estimated cost of the same experiment at claude-sonnet-5-5 (no API call was made)
| mode | skills_measured | scans_measured | model_calls_per_skill_approx | input_tokens_per_skill | output_tokens_per_skill | usd_per_skill_central | usd_per_skill_high | usd_30_skills_central | usd_30_skills_high | usd_100_skills_central | usd_100_skills_high | usd_300_skills_central | usd_300_skills_high | usd_1000_skills_central | usd_1000_skills_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B_llm | 30.0 | 57.0 | 1.83 | 9152 | 618 | 0.0245 | 0.098 | 0.74 | 2.94 | 2.45 | 9.8 | 7.35 | 29.4 | 24.5 | 98.0 |
| C_llm_meta | 30.0 | 57.0 | 3.8 | 28342 | 2830 | 0.085 | 0.2285 | 2.55 | 6.86 | 8.5 | 22.85 | 25.5 | 68.55 | 85.0 | 228.5 |
| Cdet_meta | 30.0 | 57.0 | 0.17 | 3658 | 172 | 0.009 | 0.0165 | 0.27 | 0.5 | 0.9 | 1.65 | 2.7 | 4.95 | 9.0 | 16.5 |
| TOTAL (B + C-det + C) |  |  | 5.8 | 41152 | 3620 | 0.1185 | 0.343 | 3.56 | 10.29 | 11.85 | 34.3 | 35.55 | 102.9 | 118.5 | 343.0 |

## Files
- `llm_meta_analysis/coverage_by_configuration.csv`: Planned / executed / complete / partial / failed / excluded scans, LLM and Meta status
- `llm_meta_analysis/findings_by_configuration.csv`: Security finding rows and skills with alerts per configuration (primary scans)
- `llm_meta_analysis/deterministic_reproducibility.csv`: Do static/behavioral findings stay identical when LLM / Meta are switched on?
- `llm_meta_analysis/llm_added_findings.csv`: Every LLM-analyzer security finding (B), with corroboration by deterministic alerts
- `llm_meta_analysis/llm_view_of_deterministic_alerts.csv`: For each deterministic alert: did the LLM report the same file + category?
- `llm_meta_analysis/meta_decisions.csv`: Every finding Meta saw (C-det, C): retained / suppressed / unreviewed / added
- `llm_meta_analysis/meta_decision_summary.csv`: Meta decision counts by configuration and finding kind
- `llm_meta_analysis/severity_changes.csv`: Same alert, different severity across configurations / LLM runs
- `llm_meta_analysis/category_by_configuration.csv`: Research category x configuration (security rows, primary scans)
- `llm_meta_analysis/unique_by_configuration.csv`: Alerts by the set of configurations that report them
- `llm_meta_analysis/runtime_and_cost.csv`: Wall time, tokens and cost per configuration (+ the same tokens priced at Claude Sonnet 5.5)
- `llm_meta_analysis/llm_run_stability.csv`: LLM findings in B vs the LLM part of C: same input, same settings, two runs
- `llm_meta_analysis/alert_groups.csv`: Deduplicated alert groups (skill + file + research category) across configurations; raw rows kept
- `llm_meta_analysis/triage_queue.csv`: Candidates for targeted manual investigation (bucketed, seeded sample per bucket)
- `llm_meta_analysis/case_studies.csv`: The 11 manually inspected findings (provisional labels) vs LLM and Meta behaviour
