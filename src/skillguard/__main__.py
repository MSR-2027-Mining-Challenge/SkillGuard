"""Command line: PYTHONPATH=src python -m skillguard <skill-folder> [--json] [--all] [--validations FILE]"""

import argparse
import json
import sys

from .scanner import format_text, scan


def main(argv=None):
    parser = argparse.ArgumentParser(prog="skillguard", description="SkillGuard V3.2 static skill analysis "
                                     "(read-only; findings are not vulnerability verdicts)")
    parser.add_argument("skill_folder")
    parser.add_argument("--json", action="store_true", help="print the machine-readable result (schema 5.0)")
    parser.add_argument("--all", action="store_true", help="text mode: also list supporting / info findings")
    parser.add_argument("--no-instructions", action="store_true", help="disable the Markdown instruction layer")
    parser.add_argument("--validations", help="JSON list of human validation records (fingerprint, status, reviewer)")
    args = parser.parse_args(argv)
    validations = None
    if args.validations:
        with open(args.validations, encoding="utf-8") as handle:
            validations = json.load(handle)
    result = scan(args.skill_folder, instructions=not args.no_instructions, validations=validations)
    if args.json:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(format_text(result, show_all=args.all))


if __name__ == "__main__":
    main()
