#!/usr/bin/env python3
"""Freeze original 1647 CLVIII Ascendant to Saturn as historical, never medical prediction."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
guard = j("CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json")
assert a["batch"] == "B07o"
assert a["printed_chapter"] == "CLVIII"
assert a["body_original_pdf_frames"] == [690, 691]
assert a["next_printed"] == "CLIX"
assert a["following_heading_pdf"] == 691
assert len(a["groups"]) == 6
assert guard["real_human_medical_accuracy_validated"] == 0
assert guard["real_human_mortality_predictions_validated"] == 0
assert guard["runtime_promotions"] == 0
assert not guard["original_anareta_selection_verified"]
assert not guard["mathematical_aspects_or_stellar_parity_verified"]

rows, inverses = [], []
for n, g in enumerate(a["groups"], 1):
    sid = f"B07o-S{n:03d}"
    assert g["source_span"] == sid
    assert set(g["original_pdf_frames"]) <= {690, 691}
    ids = []
    for claim in g["claims"]:
        number = 10658 + len(rows)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["source_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 37
        assert claim["source_only"]
        assert not claim["real_human_health_safety_prediction_validated"]
        assert not claim["person_level_mortality_medical_claim_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": g["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["source_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "source_documentary_accepted": True,
                "real_person_health_or_clinical_accuracy_validated": False,
                "real_person_mortality_or_danger_accuracy_validated": False,
                "real_person_cognition_character_or_morality_validated": False,
                "real_person_property_or_business_success_validated": False,
                "historical_direction_anareta_orb_geometry_verified": False,
                "individual_diagnostic_or_mortality_prediction_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    inverses.append(
        {
            "source_span": sid,
            "original_pdf_frames": g["original_pdf_frames"],
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 75
assert [x["record_number"] for x in rows] == list(range(10658, 10733))
assert [x["id"] for x in rows if x["role"] == "next_navigation"] == ["R10731", "R10732"]
assert len({x["id"] for x in rows}) == 75

images = {}
for n in [690, 691, 692]:
    path = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "original_Ascendant_to_Saturn_CLVIII" if n <= 691 else "next_printed_CLIX_context_only"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07o",
        "source": (
            "William Lilly Christian Astrology first edition 1647 Wellcome Collection b30338724"
        ),
        "original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": [690, 691],
        "following_printed_CLIX_heading_pdf": 691,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07o",
        "source_groups": inverses,
        "source_group_count": 6,
        "record_count": 75,
        "substantive": 73,
        "following_numbered_navigation": 2,
        "high_stakes_nonpromotion_guard": ("CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07o",
        "issues": [
            (
                "Original CLVIII heading names FIVE Hylegiacall places, "
                "but this particular numbered source's substantive "
                "claims concern Ascendant directed Saturn's body, "
                "sextile/trine, square/opposition and Saturn's terms. "
                "Next separately printed CLIX on Jupiter begins "
                "mid/lower original PDF691 after divider."
            ),
            (
                "Saturn bodily meeting gives many alternate antiquarian "
                "health, humoral, sex/age-specific and behavioral "
                "accusations; these are NOT modern diagnoses "
                "or accurately established person characteristics."
            ),
            (
                "For water danger the author adds a watery zodiac sign "
                "and vicinity of violent fixed stars; original orb "
                "and exact fixed-star modern positions not independently verified."
            ),
            (
                "Favorable Saturn sextile/trine examples combine "
                "social reputation, rural farming, construction, "
                "rental property, inherited wealth, mines if present, "
                "and family obedience. These are very broad alternative "
                "endpoints not one precise financial prediction."
            ),
            (
                "Adverse Saturn square/opposition/terms source expressly "
                "conditions historical death/danger language on "
                "ADDITIONAL malevolent Promittors concurring OR "
                "Saturn designated Anareta. Saturn alone does not "
                "satisfy its own catastrophic source case."
            ),
            (
                "The original provides a very long list of alleged "
                "old diseases and injuries, including gouts, fevers, "
                "bowel conditions, tumors and sexual/genital disorders. "
                "These cannot be used for clinical or safety advice."
            ),
            (
                "A sign-dependent humoral taxonomy adds fiery dryness, "
                "watery moisture/phlegm, airy blood problems and "
                "earthy melancholy. It is period medicine, "
                "not a validated physical disease classifier."
            ),
            (
                "The original Anareta selection algorithm, "
                "primary direction arc/key and natal event windows "
                "were not calculated or cross-checked with modern "
                "Swiss ephemeris/Regiomontanus geometry."
            ),
            (
                "No independent humans, known birth times, illnesses, "
                "death records, personality measures, socioeconomic "
                "status or matched null were used for validation."
            ),
            (
                "Photographic original page/short qualified paraphrase "
                "is not a complete diplomatic original edition "
                "or source for real-world individual predictions."
            ),
        ],
        "original_anareta_selection_algorithm_verified": False,
        "source_directions_and_fixed_stars_computationally_verified": False,
        "human_medical_or_social_prediction_accuracy": 0,
        "individual_mortality_or_clinical_claim_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07o",
        "status": "ORIGINAL_1647_CLVIII_ASC_SATURN_HISTORY_ONLY_NOT_MEDICAL",
        "printed_chapter": "CLVIII",
        "record_count": 75,
        "first_record": "R10658",
        "last_record": "R10732",
        "substantive": 73,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [690, 691],
        "next_printed_chapter": "CLIX",
        "following_heading_pdf": 691,
        "zero_human_prediction_validations": True,
        "full_primary_direction_geometry": False,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07o",
        "status": "FIRST_EDITION_CLVIII_ORIGINAL_SATURN_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10657,
        "new_historical_annotations": 75,
        "lilly_if_published": 10732,
        "ptolemy_retained": 1066,
        "combined_if_published": 11798,
        "substantive": 73,
        "navigation": 2,
        "source_groups": 6,
        "new_numbered_chapters": 1,
        "next_printed": "CLIX",
        "next_pdf": 691,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "guard_sha256": sha(B / "CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
        "empirical_validations": 0,
        "real_human_health_and_safety_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original 1647 CLVIII Ascendant to Saturn 75 historical notes R10658–R10732.")
