#!/usr/bin/env python3
"""Transport-optimized engineering runner for V4 H3.

This changes only two implementation details before compiling the frozen-rule
H3 source: fixes the known type-annotation bracket typo, and increases the
MediaWiki request batch from 8 to 25 exact ADB-linked titles. Parser, identity,
evidence, precedence, duplicate, and counting rules are unchanged.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "adb_broad_exact_pair_history_v4_h3.py"
source = TARGET.read_text(encoding="utf-8")
syntax_bad = "def fetch_adb_pages(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]]:"
syntax_good = "def fetch_adb_pages(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]:"
if syntax_bad in source:
    source = source.replace(syntax_bad, syntax_good, 1)
if "batch_size = 8" not in source:
    raise SystemExit("expected H3 transport batch size not found; audit before continuing")
source = source.replace("batch_size = 8", "batch_size = 25", 1)
ns = {"__name__": "__main__", "__file__": str(TARGET)}
exec(compile(source, str(TARGET), "exec"), ns, ns)
