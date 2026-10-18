#!/usr/bin/env python3
"""Freeze 1647 Lilly CLIII enemy types as historical source, no actual danger labels."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B07h"
assert a["printed_chapter"] == "CLIII"
assert a["body_original_pdf_frames"] == [674, 675]
assert a["next_printed"] == "CLIIII"
assert a["next_heading_pdf"] == 675
assert len(a["groups"]) == 4

rows, inverse = [], []
for i, g in enumerate(a["groups"], 1):
    sid = f"B07h-S{i:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {674, 675}
    ids = []
    for claim in g["claims"]:
        no = 10043 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 39
        assert claim["source_only"] and not claim["real_enemy_character_accuracy_validated"]
        assert not claim["person_danger_or_hidden_intent_prediction_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "batch": "B07h",
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "independent_real_enemy_identity_or_quality_validated": False,
                "independent_real_open_vs_covert_hostility_validated": False,
                "independent_real_enemy_social_power_validated": False,
                "independent_real_person_morality_or_safety_validated": False,
                "person_enemy_danger_or_moral_classification_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    inverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 40
assert [r["record_number"] for r in rows] == list(range(10043, 10083))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R10081", "R10082"]

photos = {}
for n in range(674, 678):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "CLIII_enemy_quality_source_body" if n <= 675 else "following_CLIIII_and_CLV_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07h",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "source_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [674, 675],
        "following_printed_CLIIII_heading_pdf": 675,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07h",
        "source_groups": inverse,
        "source_group_count": 4,
        "records": 40,
        "substantive": 38,
        "following_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07h",
        "issues": [
            (
                "Printed CLIII on enemy TYPE, apparent openness/"
                "concealment and social power follows an unnumbered "
                "12th-house ENEMY COUNT source and must not merge "
                "with separately printed CLIIII on overcoming enemies."
            ),
            (
                "First-edition chapter starts original PDF674 mid "
                "and ends PDF675 upper; printed CLIIII begins after "
                "divider on PDF675. No separate CLII observed "
                "in earlier physical source transition."
            ),
            (
                "Seventh planets or planetary opposition to "
                "luminaries are said to denote openly expressed "
                "malice, whereas twelfth planets signify "
                "covert conduct. Neither is real hidden intent."
            ),
            (
                "The eleventh ruler in seventh can allegedly "
                "indicate a former friend becoming an opponent; "
                "favorable versus adverse directions allegedly "
                "change relationship over time with no objective "
                "time/accuracy data."
            ),
            (
                "The twelfth ruler placed in Ascendant is an "
                "explicit contrary source case, allegedly "
                "making adversaries closer to friends than enemies."
            ),
            (
                "Source suggests enemy SOCIAL POWER from three "
                "ranked inputs: intrinsic planet type, natal house "
                "position, and essential dignity. No predeclared "
                "relative weights or confidence score."
            ),
            (
                "BENEFIC planets are paradoxically assigned "
                "powerful enemies, MALefic signs obscure opponents; "
                "angulary and essential dignity again contribute "
                "to powerful class even for malefic planets."
            ),
            (
                "Succedent and lesser triplicity/term/face "
                "conditions supposedly give mid/low-status "
                "adversaries; cadent, peregrine, detriment "
                "or fall supposedly obscure people."
            ),
            (
                "No real person enemy identity, safety threat, "
                "hidden hostility, social class or moral "
                "behavior was independently observed or scored. "
                "Do not use these claims for personal warnings."
            ),
            (
                "Original source packet is photo-anchored "
                "qualified paraphrase, not complete diplomatic "
                "edition or executable astrological code."
            ),
        ],
        "source_planet_fortitude_weights_and_glyphs_fully_verified": False,
        "real_person_enemy_quality_accuracy_validated": 0,
        "real_person_enmity_danger_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07h",
        "status": "ORIGINAL_1647_CLIII_ENEMY_QUALITY_SOCIAL_RANK_HISTORICAL_ONLY",
        "printed_chapter": "CLIII",
        "record_count": 40,
        "first_record": "R10043",
        "last_record": "R10082",
        "substantive": 38,
        "following_navigation": 2,
        "source_groups": 4,
        "body_original_pdf_frames": [674, 675],
        "next_printed": "CLIIII",
        "next_original_pdf": 675,
        "empirical_validations": 0,
        "actual_real_enemy_quality_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07h",
        "status": "ORIGINAL_CLIII_ENEMY_QUALITY_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10042,
        "new_historical_annotations": 40,
        "lilly_if_published": 10082,
        "ptolemy_retained": 1066,
        "combined_if_published": 11148,
        "substantive": 38,
        "navigation": 2,
        "source_groups": 4,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CLIIII",
        "next_original_pdf": 675,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "human_enemy_quality_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07h original printed CLIII enemy types: 40 historical source notes R10043–R10082")
