#!/usr/bin/env python3
"""Syntax-only engineering adapter for V4 H3.

Corrects one extra bracket in a return type annotation before compiling the
frozen-rule implementation. No data, source, parser, attribution, or counting
rule changes.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "adb_broad_exact_pair_history_v4_h3.py"
source = TARGET.read_text(encoding="utf-8")
bad = "def fetch_adb_pages(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]]:"
good = "def fetch_adb_pages(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]:"
if bad not in source:
    raise SystemExit("expected syntax-only annotation typo not found")
source = source.replace(bad, good, 1)
ns = {"__name__": "__main__", "__file__": str(TARGET)}
exec(compile(source, str(TARGET), "exec"), ns, ns)
