#!/usr/bin/env python3
"""Freeze Lilly 1647 original unnumbered directions; no real-person event prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, item):
    (B / name).write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
guard = read("DIRECTIONS_EMPIRICAL_FIREWALL_V1.json")
assert a["batch"] == "B07m"
assert a["section"] == "THE_EFFECTS_OF_DIRECTIONS"
assert a["printed_chapter"] is None
assert a["original_body_pdf_frames"] == [685, 686, 687, 688]
assert a["following_printed"] == "CLVII"
assert a["following_heading_pdf"] == 688
assert len(a["groups"]) == 8
assert guard["source_only_documentary_nonpromotion"]
assert guard["independently_tested_real_humans"] == 0
assert guard["runtime_model_promotions"] == 0
assert not guard["full_mathematical_calculator_parity_verified"]

rules, mapping = [], []
for i, group in enumerate(a["groups"], 1):
    span = f"B07m-S{i:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {685, 686, 687, 688}
    ids = []
    for claim in group["claims"]:
        num = 10469 + len(rules)
        rid = f"R{num}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 29
        assert claim["source_only"]
        assert not claim["real_human_event_time_accuracy_validated"]
        assert not claim["source_direction_geometry_verified"]
        assert not claim["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": num,
                "batch": "B07m",
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "real_person_timed_event_accuracy_validated": False,
                "real_person_health_mortality_or_law_accuracy_validated": False,
                "first_edition_direction_geometry_verified": False,
                "rectification_and_holdout_independence_demonstrated": False,
                "correct_direction_promittor_significator_computation_verified": False,
                "real_person_prediction_or_decision_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 127
assert [row["record_number"] for row in rules] == list(range(10469, 10596))
assert [r["id"] for r in rules if r["role"] == "next_printed_navigation"] == ["R10594", "R10595"]
assert len({r["id"] for r in rules}) == 127

photos = {}
for page in range(685, 691):
    file = B / "evidence" / f"pdf_1647-{page}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(page)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(page - 34),
        "source_role": (
            "unnumbered_effects_of_directions_original_source"
            if page <= 688
            else "following_printed_CLVII_CLVIII_context_only"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07m",
        "source": (
            "William Lilly Christian Astrology 1647 first edition Wellcome Collection b30338724"
        ),
        "original_full_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "unnumbered": True,
        "body_original_pdf_frames": [685, 686, 687, 688],
        "following_printed_CLVII_heading_pdf": 688,
        "following_printed_CLVIII_heading_pdf": 690,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07m",
        "source_groups": mapping,
        "source_group_count": 8,
        "record_count": 127,
        "substantive": 125,
        "next_printed_navigation": 2,
        "empirical_firewall": "DIRECTIONS_EMPIRICAL_FIREWALL_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07m",
        "issues": [
            (
                "The unnumbered THE EFFECTS OF DIRECTIONS begins "
                "top original PDF685/printed651 and continues to "
                "upper/mid PDF688/printed654. Original separately "
                "numbered CLVII starts AFTER divider PDF688. "
                "Do not increment printed chapter count for this source."
            ),
            (
                "The author attributes mathematical directions methods "
                "to Regiomontanus, Argolus, Maginus, Leovitius, "
                "Manginus, Zobolus, Ptolemy and Origanus. "
                "Those original authors' numeric algorithms are "
                "NOT cross-collated in this source batch."
            ),
            (
                "Lilly describes a Significator being directed "
                "until an encounter with a Promittor to predict "
                "year, month, week and day of natal event. "
                "This first-edition source does NOT provide "
                "a complete mathematical direction calculator."
            ),
            (
                "Lilly explicitly admits historical timing misses "
                "and argues mistakes reflect insufficiently "
                "rectified birth charts or operator error, "
                "rather than a flaw of astrology. That is an "
                "error-explaining defense, not independent validation."
            ),
            (
                "Original PDF686 explicitly claims only TWO or THREE "
                "degrees of Ascendant longitude error can shift "
                "supposed direction timing by MANY YEARS earlier "
                "or later; errors in MC also allegedly distort results."
            ),
            (
                "Birth-time fitting/rectification events must never "
                "be used again as held-out evidence of success; "
                "no retrospective free years-long tolerance "
                "is allowed after prediction misses."
            ),
            (
                "Interpretation order distinguishes aspect good/evil, "
                "Significator nature and natal house, Promittor "
                "nature and accidental house, house where "
                "direction meets, and separate good/bad branches. "
                "Outcome/event and supposed cause are not the same target."
            ),
            (
                "On PDF687 the text states 'in number five', but "
                "continues to ENUMERATE TEN directed points: "
                "Ascendant, Moon, Sun, MC, Part of Fortune, "
                "Saturn, Jupiter, Mars, Venus, Mercury. "
                "Five hylegiacal versus ten enumerated categories "
                "are distinct authorial labels; do not repair "
                "the inconsistency by deleting Saturn–Mercury."
            ),
            (
                "The author explicitly rejects Part of Fortune "
                "directions as describing bodily effects, "
                "although he acknowledges others who make "
                "that claim. Source has both positive and "
                "negative alternatives, not a general fortune forecast."
            ),
            (
                "Ascendant, Sun, Moon, MC and other planets each "
                "can signify MANY distinct life domains "
                "(health, marriage, trade, reputation, travel, "
                "sibling, money, religion, family). Without frozen "
                "specific target selection, chance apparent "
                "matches after seeing a life history are likely."
            ),
            (
                "No original numeric oblique ascensions, "
                "Regiomontanus chart geometry, arcs, "
                "key-of-time to year conversion, "
                "time zone or planet ephemeris parity "
                "was computed in this historical annotation batch."
            ),
            (
                "No real human time-registered birth data, "
                "untouched dated events, negative windows, "
                "matched calendar baselines or external "
                "prospective test results were analyzed."
            ),
            (
                "Lilly's health, pregnancy, marriage, "
                "death, morality and religion interpretations "
                "are period assertions and may not be "
                "used for real-person medical, legal, "
                "psychological or safety forecasts."
            ),
            (
                "The following separately printed CLVII on "
                "how long effects of a direction last "
                "requires its own complete original source "
                "and separate acceptance; printed CLVIII "
                "starts original PDF690."
            ),
            (
                "Photographic source witness and short qualified "
                "historical paraphrases are NOT a complete "
                "diplomatic full-original transcription."
            ),
        ],
        "source_direction_geometry_and_year_key_verified": False,
        "authorial_five_vs_ten_number_ambiguity_resolved": False,
        "all_original_technical_sources_cross_collated": False,
        "independent_real_birth_time_and_holdout_event_accuracy_validated": 0,
        "clinical_or_mortality_forecasting_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07m",
        "status": "ORIGINAL_1647_UNNUMBERED_EFFECTS_OF_DIRECTIONS_HISTORICAL_ONLY",
        "section": "THE_EFFECTS_OF_DIRECTIONS",
        "original_printed_chapter_number": None,
        "record_count": 127,
        "first_record": "R10469",
        "last_record": "R10595",
        "substantive": 125,
        "following_printed_navigation": 2,
        "source_groups": 8,
        "body_original_pdf_frames": [685, 686, 687, 688],
        "following_printed_chapter": "CLVII",
        "following_heading_pdf": 688,
        "source_life_event_prediction_engine_executable": False,
        "critical_source_2_or_3_degree_birth_time_error_many_years": True,
        "author_does_not_supply_complete_direction_math": True,
        "author_claims_five_but_enumerates_ten": True,
        "source_lilly_disputes_fortuna_body_effect": True,
        "empirical_validations": 0,
        "real_human_event_timing_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07m",
        "status": "FIRST_EDITION_UNNUMBERED_DIRECTIONS_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10468,
        "new_historical_annotations": 127,
        "lilly_if_published": 10595,
        "ptolemy_retained": 1066,
        "combined_if_published": 11661,
        "substantive": 125,
        "navigation": 2,
        "source_groups": 8,
        "numbered_chapters_added": 0,
        "next_printed_chapter": "CLVII",
        "next_original_pdf": 688,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "firewall_sha256": sha(B / "DIRECTIONS_EMPIRICAL_FIREWALL_V1.json"),
        "empirical_validations": 0,
        "real_human_directions_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original Lilly Effects of Directions: 127 historical R10469–R10595.")
