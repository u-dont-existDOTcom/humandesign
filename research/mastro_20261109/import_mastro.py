#!/usr/bin/env python3
"""Trusted-custodian import of Mastro v7.8 Trees.csv into opaque chart vectors.

Raw chart labels and signatures remain private. This imports scores; it does not
calculate astrology or establish equivalence with the historical Mastro build.
"""
import argparse
import csv
import json
import math
from pathlib import Path

from compare import save_new


def parse_trees(path: Path) -> dict[str, list[dict]]:
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for number, row in enumerate(csv.reader(stream), 1):
            if not row or not any(row):
                continue
            if len(row) != 4 or not row[0] or not row[1]:
                raise ValueError(f"Expected label,word,score,signature at row {number}")
            weight = float(row[2])
            if not math.isfinite(weight):
                raise ValueError(f"Nonfinite score at row {number}")
            result.setdefault(row[0], []).append({"word": row[1], "weight": weight})
    if not result:
        raise ValueError("Empty Mastro export")
    return result


def convert(parsed: dict, opaque_ids: dict) -> list:
    if set(parsed) != set(opaque_ids) or len(set(opaque_ids.values())) != len(opaque_ids):
        raise ValueError("Opaque mapping must cover every chart exactly once")
    if any(not isinstance(v, str) or not v for v in opaque_ids.values()):
        raise ValueError("Nonempty opaque chart IDs required")
    return [{"chart_id": opaque_ids[label], "keywords": words} for label, words in parsed.items()]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--opaque-map", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    if a.opaque_map.resolve().is_relative_to(root):
        raise ValueError("Identifying chart map must stay outside decoder repository")
    save_new(a.out, convert(parse_trees(a.input), json.loads(a.opaque_map.read_text())))


if __name__ == "__main__":
    main()
