#!/usr/bin/env python3
"""Freeze original 1647 Lilly CLVII direction magnitude, not human event prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
guard = j("DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json")
assert a["batch"] == "B07n"
assert a["printed_chapter"] == "CLVII"
assert a["body_pdf_frames"] == [688, 689, 690]
assert a["next_printed"] == "CLVIII"
assert a["following_heading_pdf"] == 690
assert len(a["groups"]) == 6
assert guard["independent_human_impact_or_duration_tests"] == 0
assert guard["executable_runtime_rules_promoted"] == 0
assert not guard["numeric_effect_duration_rule_present"]
assert not guard["individual_medical_legal_relationship_risk_predicted"]

rows, inverse = [], []
for n, g in enumerate(a["groups"], 1):
    sid = f"B07n-S{n:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {688, 689, 690}
    ids = []
    for claim in g["claims"]:
        num = 10596 + len(rows)
        rid = f"R{num}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 38
        assert claim["source_only"]
        assert not claim["independent_real_event_duration_validated"]
        assert not claim["clinical_or_mortality_prediction_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": num,
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "original_documentary_claim_accepted": True,
                "independent_real_direction_magnitude_validated": False,
                "independent_real_direction_duration_validated": False,
                "actual_real_person_medical_or_legal_accuracy_validated": False,
                "original_primary_direction_geometry_verified": False,
                "original_profection_revolution_parity_verified": False,
                "real_person_birth_rectification_validation_independent": False,
                "real_person_danger_or_illness_prediction_authorized": False,
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
assert len(rows) == 62
assert [x["record_number"] for x in rows] == list(range(10596, 10658))
assert [x["id"] for x in rows if x["role"] == "next_navigation"] == ["R10656", "R10657"]
assert len({x["id"] for x in rows}) == 62

photos = {}
for n in [688, 689, 690]:
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(file.relative_to(B)),
        "sha256": sha(file),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": ("printed_CLVII_direction_magnitude_original_and_next_seam"),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07n",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [688, 689, 690],
        "next_printed_CLVIII_heading_frame": 690,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07n",
        "source_groups": inverse,
        "source_group_count": 6,
        "records_count": 62,
        "substantive": 60,
        "following_next_chapter_navigation": 2,
        "high_stakes_guard": "DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07n",
        "issues": [
            (
                "CLVII original title asks How long the effects last, but "
                "body chiefly considers MAGNITUDE, clear manifestation, "
                "mitigation and conflicting directions. No independent "
                "numerical years/months duration rule appears here."
            ),
            (
                "Source requires both the directed Significator and "
                "Promittor's original essential dignities and "
                "angularity to assert full outcome."
            ),
            (
                "When one natal actor stronger than other, the author "
                "makes DIFFERENT claims depending whether Significator "
                "or Promittor is stronger, not a symmetric weight."
            ),
            (
                "When both weak, a source effect may be tiny or "
                "nothing at all. Fitted post-hoc threshold cannot "
                "turn an actual no-event into a predictive hit."
            ),
            (
                "Malefic Promittors may allegedly cause less harm "
                "when well dignified or in their own houses. "
                "Blanket malefic predicts danger is inaccurate "
                "as a reading of this original source."
            ),
            (
                "Contradictory good and bad directions in one "
                "calendar year are allowed to coexist if their "
                "subject matters differ. If same natal domain, "
                "the author invokes Professions/annual Profections "
                "and Revolutions, then Promittor strength, "
                "to break conflict. A method chosen AFTER a "
                "future outcome would constitute hindsight fitting."
            ),
            (
                "Original Ascendant square Mars fiery-sign fever "
                "versus Moon good aspect Venus watery-sign relief "
                "is an antiquarian hypothetical medical case, "
                "not an evidence-based clinical decision rule."
            ),
            (
                "The original page geometry, house system, direction "
                "time key, planetary orbit and annual revolution/"
                "profection algorithm have not been independently "
                "implemented and verified in this source batch."
            ),
            (
                "No authenticated birth inputs, registered direction "
                "predictions, measured event durations, clinical "
                "records, no-event windows, birth-time fitting "
                "firewall or random chart baselines were tested."
            ),
            (
                "Following printed CLVIII starts original PDF690 "
                "after divider. Its heading explicitly names "
                "FIVE Hylegiacal Places: Asc, MC, Sun, Moon, "
                "Part of Fortune. This contextualizes earlier "
                "directional list of ten but does not license "
                "silently altering already accepted wording."
            ),
            (
                "The source archive includes short photographed "
                "period anchors and reversible paraphrases, "
                "not a full diplomatic source transcription."
            ),
        ],
        "numeric_event_duration_equation_present": False,
        "annual_profection_revolution_parity_verified": False,
        "source_high_stakes_person_level_predictions_authorized": False,
        "real_human_direction_effects_accuracy_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07n",
        "status": "ORIGINAL_1647_CLVII_EFFECT_DURATION_AND_CONFLICT_HISTORY_ONLY",
        "printed_chapter": "CLVII",
        "record_count": 62,
        "first_record": "R10596",
        "last_record": "R10657",
        "substantive": 60,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [688, 689, 690],
        "next_printed_chapter": "CLVIII",
        "next_printed_heading_pdf": 690,
        "full_numeric_direction_duration_calculator": False,
        "author_allows_nonoccurrence": True,
        "author_good_bad_simultaneous": True,
        "empirical_validations": 0,
        "real_human_duration_effect_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07n",
        "status": "FIRST_EDITION_CLVII_ORIGINAL_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10595,
        "new_historical_annotations": 62,
        "lilly_if_published": 10657,
        "ptolemy_retained": 1066,
        "combined_if_published": 11723,
        "substantive": 60,
        "navigation": 2,
        "source_groups": 6,
        "new_numbered_chapters": 1,
        "next_printed": "CLVIII",
        "next_pdf": 690,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "guard_sha256": sha(B / "DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
        "empirical_validations": 0,
        "real_human_direction_accuracy": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original printed CLVII 62 historical source notes R10596–R10657.")
