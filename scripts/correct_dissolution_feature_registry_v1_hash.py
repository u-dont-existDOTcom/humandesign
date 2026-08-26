#!/usr/bin/env python3
"""One-time audited pre-feature correction for dissolution feature registry V1.

The first frozen registry commit contained a transcription-only duplication in
the pinned sepl_18.se1 SHA string. No astronomical feature has yet been generated.
This script changes only that exact string and fails closed if the expected typo
is not present.
"""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "reference" / "research" / "adb_broad_exact_pair_dissolution_feature_registry_v1.json"
BAD = "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66a1cbc9b22225872dbe4ccd99a66"
GOOD = "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66"
text = P.read_text(encoding="utf-8")
if text.count(BAD) != 1:
    raise SystemExit("expected exactly one frozen-registry SHA transcription error")
P.write_text(text.replace(BAD, GOOD), encoding="utf-8")
print("corrected registry planetary SHA only")
