#!/usr/bin/env python3
"""Freeze Lilly 1647 original dignity/status source as qualified historical text."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
stars = read("REGAL_FIXED_STARS_1647_TABLE_V1.json")
assert a["batch"] == "B06y"
assert a["printed_chapter"] == "CXLIIII"
assert a["body_original_pdf_frames"] == list(range(649, 656))
assert a["next_printed"] == "CXLVI"
assert a["following_heading_original_frame"] == 655
assert not a["intervening_printed_CXLV_observed"]
assert len(a["groups"]) == 12
assert len(stars["entries"]) == 6
assert stars["original_pdf_frame"] == 650
assert all(not x["modern_identification_verified"] for x in stars["entries"])
assert stars["real_person_status_validations"] == stars["runtime_promotions"] == 0

records, source_reverse = [], []
for n, g in enumerate(a["groups"], 1):
    sid = f"B06y-S{n:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= set(range(649, 656))
    ids = []
    for c in g["clauses"]:
        record_number = 9125 + len(records)
        rid = f"R{record_number}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 42
        assert c["source_only"]
        assert not c["independently_validated_person_ranking"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": record_number,
                "batch": "B06y",
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": c["role"],
                "anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "qualification": c["qualification"],
                "source_documentary_accepted": True,
                "independent_real_social_rank_accuracy_validated": False,
                "independent_real_official_career_validated": False,
                "independent_income_or_peer_reputation_validated": False,
                "independent_real_life_span_or_person_violence_validated": False,
                "source_fixed_star_coordinates_independently_verified": False,
                "real_person_social_class_or_moral_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    source_reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 188
assert [r["record_number"] for r in records] == list(range(9125, 9313))
assert [r["id"] for r in records if r["role"] == "next_navigation"] == ["R9310", "R9311"]
assert records[-1]["id"] == "R9312"
assert records[-1]["role"] == "skipped_CXLV"
assert len({r["id"] for r in records}) == 188

pics = {}
for frame in range(649, 661):
    path = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    pics[str(frame)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": str(frame - 34),
        "source_role": (
            "original_dignity_preferment_body"
            if frame <= 655
            else "following_printed_CXLVI_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06y",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": list(range(649, 656)),
        "following_printed_CXLVI_heading_frame": 655,
        "intervening_printed_CXLV_heading_found": False,
        "images": pics,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06y",
        "source_groups": source_reverse,
        "source_group_count": 12,
        "record_count": 188,
        "substantive": 186,
        "following_navigation": 2,
        "source_anomaly_records": ["R9312"],
        "star_source_table": "REGAL_FIXED_STARS_1647_TABLE_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06y",
        "issues": [
            (
                "Original printed CHAP CXLIIII ends on source PDF655 "
                "and next separately printed heading reads CHAP CXLVI. "
                "There is no intervening separately numbered CXLV "
                "in the visually inspected PDF649-655. "
                "Preserve the original printed numbering jump "
                "and do not create a synthetic chapter."
            ),
            (
                "Lilly explicitly says a beggar's child may share "
                "a nativity with a king's child but the social "
                "outcomes of the same favorable direction differ "
                "dramatically according to birth-class opportunity. "
                "An absolute kingship label cannot be replaced "
                "with mere extra alms after seeing a life."
            ),
            (
                "Domicile/exaltation/reception, triplicity/term/face, "
                "peregrine/detriment/fall, angularity/succedency/"
                "cadency are different source hierarchies. "
                "Source groups eighth with cadent despite "
                "eighth technically being succedent."
            ),
            (
                "The original royal fixed-star table has SIX "
                "source epoch zodiac entries, separately frozen "
                "in REGAL_FIXED_STARS_1647_TABLE_V1.json. "
                "Their modern astronomical identity, precession "
                "epoch and geometric parity are unverified."
            ),
            (
                "A specific five-degree distance is provided for "
                "stellar contacts in CHAP CXLIIII; the "
                "earlier unnumbered tenth-house introduction "
                "gave no numeric cusp-distance rule. "
                "Do not silently transfer the number."
            ),
            (
                "Five different compounded Kingly Genitures "
                "and separate Sun/Moon/Midheaven/Ascendant/star "
                "aphorisms are competing or overlapping "
                "source methods with unresolved glyph operators, "
                "not a unique deterministic rank scorer."
            ),
            (
                "The author sometimes asserts kingship or high "
                "office under aspect patterns that include hard "
                "squares, against a generic malefic-square rule. "
                "Preserve exact positive exceptions."
            ),
            (
                "The source states strong royal/star indications "
                "may nevertheless bring sudden later loss, "
                "calamity, illness, casualties or conflict. "
                "Permanently powerful and temporary rise "
                "then fall are distinct outcome variables."
            ),
            (
                "Early part explicitly warns not to issue "
                "positive categorical judgment from a single "
                "aphorism; later an exact solar noon/Aries "
                "condition claims greatness without other "
                "testimony. Preserve the unresolved conflict."
            ),
            (
                "Period occupational/social categories include "
                "aristocracy, military status, clerical honor, "
                "merit, poor-class peer respect and malign "
                "temperament accusations; no real individual "
                "criminality, virtue or moral nature established."
            ),
            (
                "Several first edition glyphs in Kingly, solar, "
                "lunar and stellar combinations are not "
                "professionally transcribed, and cannot enter "
                "an executable source scorer."
            ),
            (
                "Modern star coordinates and country/angle "
                "probabilities, reliable historical birth times, "
                "official appointments and denominators for "
                "failed forecasts were not analyzed."
            ),
            (
                "Source phrase 'many testimonies' has no frozen "
                "weighting, age horizon, necessary/sufficient "
                "conditions or no-prediction threshold."
            ),
            (
                "This is a selective qualified historical "
                "paraphrase with photo/SHA provenance, "
                "not a complete diplomatic edition."
            ),
        ],
        "original_printed_CXLV_found": False,
        "historical_fixed_star_table_modern_parity_passed": False,
        "original_royal_configuration_glyphs_fully_resolved": False,
        "human_social_rank_predictions_validated": 0,
        "personal_morality_crime_or_lifespan_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06y",
        "status": "ORIGINAL_1647_CXLIIII_DIGNITY_PREFERMENT_HISTORICAL_ONLY",
        "printed_chapter": "CXLIIII",
        "editorial_chapter": "CXLV",
        "record_count": 188,
        "first_record": "R9125",
        "last_record": "R9312",
        "substantive": 186,
        "following_navigation": 2,
        "source_groups": 12,
        "body_original_pdf_frames": list(range(649, 656)),
        "following_printed_chapter": "CXLVI",
        "following_heading_pdf": 655,
        "original_CXLV_intervening_heading_present": False,
        "original_regal_star_table": "REGAL_FIXED_STARS_1647_TABLE_V1.json",
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "human_rank_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06y",
        "status": "ORIGINAL_CXLIIII_DIGNITY_SOURCE_LOCALLY_FROZEN",
        "previous_lilly": 9124,
        "new_historical_annotations": 188,
        "lilly_if_published": 9312,
        "ptolemy_retained": 1066,
        "combined_if_published": 10378,
        "substantive": 186,
        "navigation": 2,
        "source_groups": 12,
        "new_numbered_chapters": 1,
        "next_printed_chapter": "CXLVI",
        "next_original_pdf": 655,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "star_table_sha256": sha(B / "REGAL_FIXED_STARS_1647_TABLE_V1.json"),
        "empirical_validations": 0,
        "real_human_honor_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06y original CXLIIII: 188 historical records R9125-R9312; original skips printed CXLV.")
