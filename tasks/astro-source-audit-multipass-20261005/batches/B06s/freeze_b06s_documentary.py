#!/usr/bin/env python3
"""Original Lilly 1647 CXXXIX travel yes/no, direction and mode as historical."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
method = j("TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json")
assert a["batch"] == "B06s"
assert a["printed_chapter"] == "CXXXIX"
assert a["body_pdf_frames"] == [640, 641, 642]
assert a["next_printed"] == "CXL"
assert a["next_heading_pdf"] == 643
assert len(a["groups"]) == 11
assert method["schema"] == "LILLY_1647_TRAVEL_DIRECTION_MODE_HISTORICAL_SOURCES_V1"
assert len(method["source_methods"]) == 7
assert method["human_travel_predictions_verified"] == 0
assert method["runtime_promotions"] == 0

records, inverse = [], []
for index, g in enumerate(a["groups"], 1):
    sid = f"B06s-S{index:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {640, 641, 642, 643}
    ids = []
    for c in g["clauses"]:
        number = 8706 + len(records)
        rid = f"R{number}"
        assert c["id"] == rid
        assert len(c["anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 40
        assert not c["human_outcome_independently_validated"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": c["role"],
                "anchor_not_diplomatic": c["anchor_not_diplomatic"],
                "historical_source_meaning_only": c["historical_meaning_only"],
                "qualification": c["source_qualification"],
                "original_documentary_accepted": True,
                "independent_travel_occurrence_frequency_validated": False,
                "independent_travel_destination_geography_validated": False,
                "independent_travel_duration_profit_or_mode_validated": False,
                "independent_travel_life_hazard_validated": False,
                "real_person_travel_wealth_or_religion_inference_authorized": False,
                "source_math_directed_compass_executable": False,
                "original_ptolemy_source_collated": False,
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
assert len(records) == 101
assert [x["record_number"] for x in records] == list(range(8706, 8807))
assert [x["id"] for x in records if x["role"] == "next_chapter_navigation"] == ["R8805", "R8806"]
assert len({x["id"] for x in records}) == 101

images = {}
for n in [640, 641, 642, 643]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "path": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "travel_yesno_mode_body" if n <= 642 else "following_travel_cause_chapter_context_only"
        ),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06s",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "original_first_edition_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [640, 641, 642],
        "following_printed_CXL_heading_pdf": 643,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06s",
        "groups": inverse,
        "source_group_count": 11,
        "historical_records": 101,
        "substantive": 99,
        "navigation": 2,
        "competing_historical_methods": 7,
        "method_spec_file": "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json",
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06s",
        "issues": [
            (
                "Travel occurrence, journey count/frequency, duration "
                "abroad, economic benefit, destination, transportation "
                "mode and life-hazard are different targets, "
                "not interchangeable successes."
            ),
            (
                "Moon and Mercury receive priority in the source, "
                "but one early original aspect glyph between "
                "reception and first/ninth lord is still unclear."
            ),
            (
                "Solar reception and conjunction branches, "
                "Moon/Mercury reciprocal domiciles and ninth/first "
                "lord placements are multiple alternative "
                "potential travel indicators."
            ),
            (
                "Travel no/rare/many continuous and movable/fixed "
                "signs lack exact event count, calendar age, "
                "duration or economic profit thresholds."
            ),
            (
                "Original compass planet mapping is Sun/Saturn "
                "East, Venus South, Jupiter North, Mars/Moon West; "
                "Mercury is conditional on aspects and may be "
                "neutral when conjunct luminaries without dignity."
            ),
            (
                "Elemental signs represent Fire East, Air West, "
                "Earth South, Water North, which can contradict "
                "the planetary direction and other testimony."
            ),
            (
                "Ptolemy-attributed source instead uses natal "
                "Sun/Moon Oriental/Occidental houses "
                "and permits East/Southeast versus West/North "
                "respectively; original Ptolemy text "
                "not yet independently collated."
            ),
            (
                "Lilly then uses Mars/Moon celestial ecliptic "
                "latitude to propose North/South directions; "
                "opposite latitudes and contradictory "
                "compass indicators lack a prescribed solution."
            ),
            (
                "The author's simple majority instruction "
                "does not specify eligible-indicator weights, "
                "ties, dominant region or no-prediction threshold. "
                "Retroactive choice among seven methods "
                "would make success claims meaningless."
            ),
            (
                "Land versus water branches overlap with "
                "water-or-land permissive case and "
                "historical horse/coach/on-foot categories. "
                "These are not uniquely equivalent to "
                "modern multimodal transport or flight."
            ),
            (
                "No complete astrological directional "
                "calculation, forecast window, country "
                "geometry, signifier-selection precedence "
                "or real travel itinerary data were used."
            ),
            (
                "Dangerous travel, relocation wealth "
                "and religious beliefs are unsupported "
                "high-stakes or personal hypotheses, "
                "not actual individual forecasts."
            ),
            (
                "Original printed CHAP CXL on causes of travel "
                "begins on PDF643 after CXXXIX mode "
                "subsection ends PDF642. This source "
                "must not absorb next chapter."
            ),
            (
                "Historical source paragraph anchors "
                "are selective paraphrases not a "
                "complete diplomatic first-edition "
                "glyph-by-glyph transcription."
            ),
        ],
        "planetary_glyphs_all_verified": False,
        "original_ptolemy_travel_source_collated": False,
        "complete_travel_direction_engine": False,
        "real_person_travel_destination_or_safety_accuracy_validated": 0,
        "person_geography_profit_faith_or_life_risk_predictions_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06s",
        "status": "ORIGINAL_1647_TRAVEL_YESNO_DIRECTION_MODE_HISTORICAL_ONLY",
        "printed_chapter": "CXXXIX",
        "editorial_chapter": "CXL",
        "record_count": 101,
        "first_record": "R8706",
        "last_record": "R8806",
        "substantive": 99,
        "following_numbered_navigation": 2,
        "source_groups": 11,
        "travel_direction_methods": 7,
        "original_body_pdf_frames": [640, 641, 642],
        "following_printed_CXL_pdf": 643,
        "complete_diplomatic_transcription": False,
        "original_math_scoring_executable": False,
        "empirical_validations": 0,
        "independent_real_travel_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06s",
        "status": "ORIGINAL_CXXXIX_JOURNEYS_SOURCE_LOCALLY_FROZEN",
        "previous_lilly": 8705,
        "new_historical_annotations": 101,
        "lilly_if_published": 8806,
        "ptolemy_retained": 1066,
        "combined_if_published": 9872,
        "substantive": 99,
        "navigation": 2,
        "source_groups": 11,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXL",
        "next_original_pdf_frame": 643,
        "rules_sha256": sha(B / "RULES.json"),
        "source_authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "direction_method_sha256": sha(B / "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json"),
        "empirical_validations": 0,
        "travel_person_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06s Lilly original CXXXIX 101 historic travel source notes R8706–R8806")
