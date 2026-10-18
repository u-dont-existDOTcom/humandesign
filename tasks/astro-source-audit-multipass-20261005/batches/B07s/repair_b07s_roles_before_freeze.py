#!/usr/bin/env python3
"""Pre-freeze repair: make repeated historical source roles unique by passage."""

import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARTS = sorted(B.glob("SOURCE_PART_0*.json"))
REPLACE = {
    (1, "saturn_eye"): "saturn_eye_body",
    (3, "saturn_eye"): "saturn_eye_adverse",
    (1, "saturn_fall"): "saturn_fall_body",
    (3, "saturn_fall"): "saturn_fall_adverse",
    (5, "jupiter_wealth"): "jupiter_wealth_body",
    (8, "jupiter_wealth"): "jupiter_wealth_terms",
    (5, "jupiter_king"): "jupiter_king_body",
    (7, "jupiter_king"): "jupiter_king_adverse",
    (9, "mars_fever"): "mars_fever_body",
    (11, "mars_fever"): "mars_fever_adverse",
    (12, "mars_fever"): "mars_fever_terms",
    (14, "venus_women"): "venus_women_benefic",
    (16, "venus_women"): "venus_women_terms",
    (21, "moon_eye"): "moon_eye_body",
    (23, "moon_eye"): "moon_eye_adverse",
    (21, "moon_journey"): "moon_journey_body",
    (22, "moon_journey"): "moon_journey_benefic",
}
i = 0
actual = set()
roles = []
for file in PARTS:
    data = json.loads(file.read_text(encoding="utf-8"))
    for g in data["groups"]:
        for c in g["claims"]:
            key = (i, c["role"])
            if key in REPLACE:
                old = c["role"]
                c["role"] = REPLACE[key]
                actual.add(key)
            roles.append(c["role"])
        i += 1
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert actual == set(REPLACE), (set(REPLACE) - actual, actual - set(REPLACE))
assert len(roles) == 306 and len(set(roles)) == 306
(B / "PRE_FREEZE_ROLE_REPAIR_RECEIPT_V1.json").write_text(
    json.dumps(
        {
            "batch": "B07s",
            "reason": (
                "Preserve identical outcome constructs under distinct "
                "planet/aspect/term passage IDs"
            ),
            "source_roles_before_unique": False,
            "after_unique": True,
            "repaired_roles": len(REPLACE),
            "items": [
                {"source_group_index_zero_based": i, "old_role": r, "new_role": v}
                for (i, r), v in REPLACE.items()
            ],
            "canonical_records_changed": 0,
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
print("Uniquified", len(REPLACE), "roles in", i, "source groups; 306 records")
