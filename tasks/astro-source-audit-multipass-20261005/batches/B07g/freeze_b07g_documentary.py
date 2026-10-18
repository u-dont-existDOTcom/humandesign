#!/usr/bin/env python3
"""Freeze unnumbered original Lilly enemies-count source with no person accusations."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, item):
    (B / name).write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B07g"
assert a["printed_chapter"] is None
assert a["section"] == "UNNUMBERED_TWELFTH_HOUSE_ENEMIES"
assert a["body_pdf_frames"] == [673, 674]
assert a["next_printed"] == "CLIII"
assert a["next_heading_pdf"] == 674
assert not a["original_intervening_CLII_heading_observed"]
assert len(a["groups"]) == 3

records, inverse = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B07g-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {673, 674}
    ids = []
    for x in group["claims"]:
        n = 10020 + len(records)
        rid = f"R{n}"
        assert x["id"] == rid
        assert len(x["source_anchor_not_diplomatic"]) >= 5
        assert len(x["historical_meaning_only"]) >= 39
        assert x["source_only"]
        assert not x["independent_real_enemy_count_validated"]
        assert not x["real_person_danger_inference_authorized"]
        assert not x["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": n,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": x["role"],
                "anchor_not_diplomatic": x["source_anchor_not_diplomatic"],
                "historical_meaning_only": x["historical_meaning_only"],
                "qualification": x["qualification"],
                "source_documentary_accepted": True,
                "independent_real_enemy_count_accuracy_validated": False,
                "independent_real_relationship_conflict_validated": False,
                "source_nodal_analogies_mathematically_verified": False,
                "real_person_enemy_crime_or_danger_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    inverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 23
assert [x["record_number"] for x in records] == list(range(10020, 10043))
assert [x["id"] for x in records if x["role"] == "next_numbered_navigation"] == ["R10041", "R10042"]

imgs = {}
for n in range(673, 677):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    imgs[str(n)] = {
        "file": str(file.relative_to(B)),
        "sha256": sha(file),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "unnumbered_twelfth_enemies_body" if n <= 674 else "following_CLIII_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07g",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "original_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "unnumbered": True,
        "body_original_pdf_frames": [673, 674],
        "following_printed_CLIII_heading_pdf": 674,
        "intervening_original_CLII_heading_present": False,
        "images": imgs,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07g",
        "source_groups": inverse,
        "source_group_count": 3,
        "record_count": 23,
        "substantive": 21,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07g",
        "issues": [
            (
                "Source UNNUMBERED twelfth-house Enemies starts "
                "lower PDF673, continues upper PDF674, ending "
                "before distinct separately printed CLIII on "
                "the SAME page. Printed CLII not found in "
                "previous CLI to CLIII pages."
            ),
            (
                "Author is discussing supposed NUMBER of adversaries, "
                "not their character, social rank, level of power "
                "or any real person danger risk. The following CLIII "
                "is an independent quality-of-enemies chapter."
            ),
            (
                "Source inputs include seventh or twelfth house "
                "planet occupants or opponents of either luminary. "
                "Alternative MANY and FEW/NONE conditions are "
                "specified with no objective count cutoff."
            ),
            (
                "First and twelfth rulers exchanged, or first and "
                "seventh rulers exchanged, create additional alleged "
                "adversary testimony. A lack of twelfth-lord aspect "
                "to first lord is instead source for few enemies."
            ),
            (
                "Source treats North Node like Jupiter/Venus "
                "and South Node like Saturn/Mars, but original "
                "historic glyph/parity and strength conditions "
                "were not mathematically reconciled."
            ),
            (
                "A native's reported opponents, verified dispute, "
                "mutual hostility, political rival, legal case "
                "and physically dangerous attacker are separate "
                "endpoints and cannot be pooled to rescue a miss."
            ),
            (
                "No real natal chart, human enemies, actual criminal "
                "or legal disputes, confirmed real-world harm, "
                "matched socioeconomic baseline or prospective "
                "prediction test appears in this source lane."
            ),
            (
                "Historical source record extraction is not a "
                "complete diplomatic transcription or executable "
                "astrology model, and may retain uncertain glyphs."
            ),
        ],
        "printed_CLII_heading_observed": False,
        "original_node_glyphs_and_rules_fully_verified": False,
        "complete_enemies_count_executable_method": False,
        "real_person_adversary_accuracy_validated": 0,
        "person_level_crime_danger_or_legal_prediction_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07g",
        "status": "ORIGINAL_1647_UNNUMBERED_TWELFTH_HOUSE_ENEMIES_SOURCE_ONLY",
        "section": "UNNUMBERED_TWELFTH_HOUSE_ENEMIES",
        "original_printed_chapter_number": None,
        "record_count": 23,
        "first_record": "R10020",
        "last_record": "R10042",
        "substantive": 21,
        "following_navigation": 2,
        "source_groups": 3,
        "body_pdf_frames": [673, 674],
        "next_printed": "CLIII",
        "following_heading_pdf": 674,
        "empirical_validations": 0,
        "real_human_adversary_accuracy": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07g",
        "status": "ORIGINAL_UNNUMBERED_TWELFTH_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10019,
        "new_historical_annotations": 23,
        "lilly_if_published": 10042,
        "ptolemy_retained": 1066,
        "combined_if_published": 11108,
        "substantive": 21,
        "navigation": 2,
        "source_groups": 3,
        "numbered_chapters_added": 0,
        "next_printed_chapter": "CLIII",
        "next_original_pdf": 674,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "real_enemy_count_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07g UNNUMBERED twelfth enemies: 23 historic notes R10020–R10042")
