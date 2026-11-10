"""Command line for the Cisco LLM/Meta experiment (run from the repository root with PYTHONPATH=src).

    python -m gitskills_cisco_llm prepare --source RUN_DIR --name NAME --model MODEL [--budget-usd X] [--workers N]
    python -m gitskills_cisco_llm run RUN_DIR [--modes ...] [--skills ...] [--retry-failed]     (resumable; Ctrl-C safe)
    python -m gitskills_cisco_llm status RUN_DIR
    python -m gitskills_cisco_llm estimate RUN_DIR --model claude-sonnet-5-5                   (no API calls)
    python -m gitskills_cisco_llm analyze RUN_DIR                                               (tables + report)
"""

import argparse
import json
from pathlib import Path

from .experiment import NEW_MODES, Experiment, LLMSettings
from .runner import Runner, prepare


def main(argv=None):
    parser = argparse.ArgumentParser(prog="gitskills_cisco_llm")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="create a run folder from a finished notebook-01 scan run")
    p.add_argument("--source", required=True, help="original notebook-01 scan run folder (exported skills + baseline reports)")
    p.add_argument("--name", required=True, help="experiment name, e.g. sample30-seed2027-llm-meta-qwen3-4b")
    p.add_argument("--model", required=True, help="Cisco model id, e.g. ollama/skillscan-qwen3-4b-ctx64k or claude-sonnet-5-5")
    p.add_argument("--modes", nargs="+", default=list(NEW_MODES), choices=list(NEW_MODES))
    p.add_argument("--provider", help="SKILL_SCANNER_LLM_PROVIDER (default: inferred by Cisco from the model)")
    p.add_argument("--temperature", help="SKILL_SCANNER_LLM_TEMPERATURE ('none' omits it)")
    p.add_argument("--max-output-tokens", type=int)
    p.add_argument("--budget-usd", type=float, help="approved spending cap; required for paid providers")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--max-attempts", type=int, default=3)
    p.add_argument("--timeout-seconds", type=int, default=1800)
    p.add_argument("--run-id")
    r = sub.add_parser("run", help="execute (or resume) the pending scans of a run folder")
    r.add_argument("run_dir")
    r.add_argument("--modes", nargs="+", choices=list(NEW_MODES))
    r.add_argument("--skills", nargs="+")
    r.add_argument("--retry-failed", action="store_true", help="re-run scans whose final status was not COMPLETE/CONTRACT_ONLY")
    s = sub.add_parser("status")
    s.add_argument("run_dir")
    e = sub.add_parser("estimate", help="token/cost estimate for a (paid) model, from file sizes and measured tokens")
    e.add_argument("run_dir")
    e.add_argument("--model", default="claude-sonnet-5-5")
    e.add_argument("--skills-n", type=int, nargs="+", default=[30, 100, 300, 1000])
    a = sub.add_parser("analyze")
    a.add_argument("run_dir")
    a.add_argument("--no-report", action="store_true")
    args = parser.parse_args(argv)
    root = Path.cwd()

    if args.command == "prepare":
        llm = LLMSettings(model=args.model, provider=args.provider, temperature=args.temperature,
                          max_output_tokens=args.max_output_tokens)
        exp = Experiment(name=args.name, modes=args.modes, llm=llm, workers=args.workers, budget_usd=args.budget_usd,
                         max_attempts=args.max_attempts, timeout_seconds=args.timeout_seconds)
        print(prepare(root, args.source, exp, run_id=args.run_id))
    elif args.command == "run":
        runner = Runner(root, args.run_dir, retry_failed=args.retry_failed)
        print(runner.execute(set(args.modes) if args.modes else None, set(args.skills) if args.skills else None))
    elif args.command == "status":
        runner = Runner(root, args.run_dir)
        runner._write_status("status-check", {})
        status = json.loads((Path(args.run_dir) / "execution_status.json").read_text())
        status.pop("environment", None)
        print(json.dumps(status, indent=2))
    elif args.command == "estimate":
        from .analyze import estimate_costs
        print(estimate_costs(root, Path(args.run_dir), args.model, args.skills_n).to_string(index=False))
    elif args.command == "analyze":
        from .analyze import analyze
        analyze(root, Path(args.run_dir), build_report=not args.no_report)


if __name__ == "__main__":
    main()
