"""SkillGuard V3.2: static, read-only security analysis of AI agent skill folders.

Frozen V3.1 remains in src/skillguard_capabilities.py and is not imported by this package.
"""

from .scanner import SCHEMA_VERSION, VERSION, format_text, scan

__all__ = ["scan", "format_text", "VERSION", "SCHEMA_VERSION"]
