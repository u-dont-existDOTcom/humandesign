#!/usr/bin/env python3
"""Freeze original 1647 Lilly spouse-origin claims as historical documentation."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06k"
assert author["printed_chapter"] == "CXXXIII"
assert author["body_original_pdf_frames"] == [626, 627]
assert author["next_printed"] == "CXXXIIII"
assert len(author["groups"]) == 6

records, reverse = [], []
for group_no, group in enumerate(author["groups"], 1):
    sid = f"B06k-S{group_no:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {626, 627}
    ids = []
    for claim in group["claims"]:
        no = 8107 + len(records)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_only_meaning"]) >= 45
        assert not claim["independent_spouse_origin_validated"]
        assert not claim["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_only_meaning": claim["historical_only_meaning"],
                "source_qualification": claim["qualification"],
                "historic_documentary_accepted": True,
                "independent_spouse_birthplace_validated": False,
                "actual_spouse_character_religion_or_wealth_validated": False,
                "independent_geographical_distance_validated": False,
                "real_person_spouse_origin_prediction_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 35
assert [x["record_number"] for x in records] == list(range(8107, 8142))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R8140", "R8141"]
assert len({x["id"] for x in records}) == 35

images = {}
for n in (626, 627):
    path = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": "spouse_origin_body",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06k",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_frames": [626, 627],
        "following_printed_CXXXIIII_heading_frame": 627,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06k",
        "source_groups": reverse,
        "source_groups_count": len(reverse),
        "record_count": 35,
        "substantive": 33,
        "next_numbered_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06k",
        "issues": [
            "Lilly expressly states COUNTY not COUNTRY in his initial "
            "spouse-birthplace claim. The targets must not be collapsed.",
            "Later lines say another Country or place, and no exact "
            "geographical or administrative distance threshold is defined.",
            "Original source predicts spouse at birth, not residence "
            "at encounter, marriage location or nationality.",
            "House III or IX, peregrine and 7th/9th ruler exchange are "
            "partly alternative configurations rather than independent "
            "verified couple forecasts.",
            "Venus must rule ninth and be in first OR tenth; Venus "
            "in first alone is insufficient to represent the passage.",
            "A Sun-plus-planet/house aspect glyph in the source "
            "needs first-edition diplomatic specialist checking; "
            "the companion is intentionally unresolved.",
            "Spouse religiousness, wealth and moral virtue are "
            "additional stereotyped outcomes, not measured "
            "geographic evidence and not facts about any partner.",
            "A more benevolent and well-fortified significator "
            "qualifies the favorable spouse-character assertion.",
            "The zodiac sign of seventh, seventh ruler, Venus, "
            "Moon and source-defined quadrants are all considered "
            "but no reproducible direction-to-distance metric supplied.",
            "Counting the greater number of indications enables "
            "substantial interpretive flexibility without a frozen "
            "priority or tie-resolution scheme.",
            "No validated spouse birthplace, real couples' charts, "
            "birth-time source verification, observed distances "
            "or blinded controls are included.",
            "The next printed CHAP CXXXIIII on appearance begins "
            "mid original PDF627 and is not included here.",
            "Selective historical source anchors only; this is "
            "not an original glyph-by-glyph diplomatic edition.",
        ],
        "county_vs_country_ambiguity_preserved": True,
        "source_glyph_fully_resolved": False,
        "independent_spouse_geography_validations": 0,
        "private_partner_character_or_origin_claims_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06k",
        "status": "FIRST_EDITION_CXXXIII_SPOUSE_ORIGIN_HISTORICAL_SOURCE_ONLY",
        "printed_chapter": "CXXXIII",
        "editorial_chapter": "CXXXIV",
        "record_count": 35,
        "first_record": "R8107",
        "last_record": "R8141",
        "substantive_historical": 33,
        "following_numbered_navigation": 2,
        "source_groups": 6,
        "body_pdf_frames": [626, 627],
        "next_heading_pdf": 627,
        "county_vs_country_kept_distinct": True,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_spouse_geography_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06k",
        "status": "FIRST_EDITION_SPOUSE_ORIGIN_DOCUMENTARY_LOCAL_FREEZE_PENDING_REMOTE",
        "prior_lilly": 8106,
        "new_historical_records": 35,
        "lilly_if_published": 8141,
        "ptolemy_retained": 1066,
        "combined_if_published": 9207,
        "substantive": 33,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXXXIIII",
        "next_source_pdf": 627,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_spouse_origin_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06k R8107–R8141: 35 historical source claims, 0 real spouse validations")
