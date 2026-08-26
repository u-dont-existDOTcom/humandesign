#!/usr/bin/env python3
"""Engineering runner for V4 H1/H2 broad-pair history recovery.

Corrects one syntax-only type-annotation bracket in the frozen-rule implementation
before compiling it. No inclusion, source, attribution, timing, or state-history
rule is modified.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "adb_broad_exact_pair_history_v4_h1_h2.py"
source = TARGET.read_text(encoding="utf-8")
bad = "def fetch_people_wikitext(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]]:"
good = "def fetch_people_wikitext(people: dict[int, dict]) -> tuple[dict[int, tuple[str, str]], list[dict]]:"
if bad not in source:
    raise SystemExit("expected syntax-only annotation typo not found; audit runner before continuing")
source = source.replace(bad, good, 1)
ns = {"__name__": "__main__", "__file__": str(TARGET)}
exec(compile(source, str(TARGET), "exec"), ns, ns)
