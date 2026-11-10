"""Secret redaction, path portability and the pre-commit safety audit for generated reports.

Everything a report writes passes through `clean_text` (or `clean_frame` / `clean_json`), so text taken from
untrusted skill files never reaches a report file with a literal secret or an absolute local path in it.
`audit_tree` re-reads every generated text file afterwards and fails the build if anything slipped through.

The first four patterns are the ones notebook 01 applies to snippets (Section 9); keep them in sync.
"""

import json
import re
from pathlib import Path

import pandas as pd

REDACTED = "[REDACTED]"

SECRET_PATTERNS = [
    # quoted assignment: password = "hunter22", "api_key": "abcd..."
    (re.compile(r"(?i)((?:password|passwd|secret|token|api[_-]?key|access[_-]?key)\w*['\"]?\s*[=:]\s*)(['\"])([^'\"\s]{4,})\2"),
     r"\1\2[REDACTED]\2"),
    # unquoted assignment that is not a variable reference ($VAR, %VAR%, {var}, (call))
    (re.compile(r"(?i)((?:password|passwd|secret|token|api[_-]?key)\w*\s*=\s*)(?![$%{(])([A-Za-z0-9_\-/+]{8,})(?![\w.(\[])"),
     r"\1[REDACTED]"),
    (re.compile(r"(://[^/\s:@]+:)[^@\s]+@"), r"\1[REDACTED]@"),                                  # user:password@host
    (re.compile(r"\b(AKIA|ASIA|ghp_|gho_|ghu_|ghs_|ghr_|github_pat_|xox[baprs]-|AIza|sk-ant-|sk-|sk_live_|rk_live_|glpat-)[A-Za-z0-9_\-]{8,}"),
     r"\1[REDACTED]"),
    # additions for reports: private keys, JWTs, bearer tokens, Telegram bot tokens
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|$)", re.S),
     "-----BEGIN PRIVATE KEY-----[REDACTED]"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), REDACTED),
    (re.compile(r"(?i)\b(bearer\s+)(?![$%{<])[A-Za-z0-9._\-]{20,}"), r"\1[REDACTED]"),
    (re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_\-]{33}\b"), REDACTED),
]

# Patterns the audit treats as a leak if they survive redaction. A match that already contains [REDACTED] is fine.
LEAK_PATTERNS = [p for p, _ in SECRET_PATTERNS]
HOME = str(Path.home())        # the local user's home folder: never written to a report


def redact(text):
    if not isinstance(text, str):
        return text
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


class Portable:
    """Rewrites absolute paths under the repository root to repository-relative ones (and hides home folders)."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.prefixes = sorted({str(self.root), str(Path(root))}, key=len, reverse=True)

    def path(self, path):
        """Repository-relative POSIX path when possible."""
        if path is None:
            return None
        p = Path(path)
        if not p.is_absolute():
            return p.as_posix()
        p = p.resolve()
        return p.relative_to(self.root).as_posix() if p.is_relative_to(self.root) else self.text(p.as_posix())

    def text(self, text):
        if not isinstance(text, str):
            return text
        for prefix in self.prefixes:
            text = text.replace(prefix + "/", "").replace(prefix, ".")
        return text.replace(HOME, "~") if len(HOME) > 1 else text


def clean_text(text, portable):
    return portable.text(redact(text)) if isinstance(text, str) else text


def clean_frame(df, portable):
    """Copy of df with every string cell redacted and made path-portable."""
    out = df.copy()
    for col in out.columns:
        if out[col].dtype == object or pd.api.types.is_string_dtype(out[col]):
            out[col] = out[col].map(lambda v: clean_text(v, portable))
    return out


def clean_json(value, portable):
    if isinstance(value, dict):
        return {k: clean_json(v, portable) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_json(v, portable) for v in value]
    return clean_text(value, portable)


def count_redactions(text):
    return text.count(REDACTED) if isinstance(text, str) else 0


TEXT_SUFFIXES = {".md", ".csv", ".json", ".html", ".txt"}


def audit_tree(folder, root):
    """Problems (file, reason, excerpt) in generated text files: surviving secrets or absolute local paths."""
    root_strings = {str(Path(root).resolve()), str(Path(root))}
    problems = []
    for path in sorted(Path(folder).rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in LEAK_PATTERNS:
            for match in pattern.finditer(text):
                if REDACTED not in match.group(0):
                    problems.append((path, "possible secret", match.group(0)[:60]))
        for prefix in root_strings:
            if prefix in text:
                problems.append((path, "absolute repository path", prefix))
        if len(HOME) > 1 and HOME in text:
            problems.append((path, "home-folder path", HOME))
    return problems


def dumps(value):
    return json.dumps(value, indent=2, default=str, ensure_ascii=False) + "\n"
