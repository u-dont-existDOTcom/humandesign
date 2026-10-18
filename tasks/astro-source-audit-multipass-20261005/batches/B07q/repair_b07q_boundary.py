#!/usr/bin/env python3
"""One-time B07q correction: CLXII heading belongs outside the CLX photo span."""

import json
from pathlib import Path

B = Path(__file__).resolve().parent
p = B / "SOURCE_PART_04_MOON_HOUSE_CUSPS_20261018.json"
a = json.loads(p.read_text())
claims = a["groups"][-1]["claims"]
if claims[-1]["role"] == "next_CLXII":
    claims.pop()
    p.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n")
assert [r["role"] for r in claims[-2:]] == ["next_CLXI_divider", "next_fixedstars"]
f = B / "freeze_b07q_documentary.py"
s = f.read_text()
for before, after in [
    ("assert len(rules) == 259", "assert len(rules) == 258"),
    ("list(range(11068, 11327))", "list(range(11068, 11326))"),
    (
        '"next_CLXI_divider", "next_fixedstars", "next_CLXII",',
        '"next_CLXI_divider", "next_fixedstars",',
    ),
    ("rules[-3:]", "rules[-2:]"),
    ("len(rules)-3", "len(rules)-2"),
    ("next_navigation=3", "next_navigation=2"),
    ('last_record="R11326"', 'last_record="R11325"'),
    ("new_historical_annotations=259", "new_historical_annotations=258"),
    ("substantive=256, next_navigation=3", "substantive=256, next_navigation=2"),
    ("lilly_if_published=11326", "lilly_if_published=11325"),
    ("combined_if_published=12392", "combined_if_published=12391"),
]:
    if before in s:
        s = s.replace(before, after)
    else:
        assert after in s, f"Missing expected code anchor: {before}"
f.write_text(s)
print("B07q CLXII cross-chapter seam repaired.")
