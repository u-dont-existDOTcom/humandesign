#!/usr/bin/env python3
"""Freeze Lilly 1647 first-edition CLVI historical mortality source; no person predictions."""

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
guard = read("MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json")
stars = read("VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json")
assert a["batch"] == "B07l"
assert a["printed_chapter"] == "CLVI"
assert a["body_original_pdf_frames"] == list(range(678, 685))
assert a["next_unnumbered"] == "THE_EFFECTS_OF_DIRECTIONS"
assert a["next_original_frame"] == 685
assert len(a["groups"]) == 11
assert len(stars["table"]) == 6
assert not stars["modern_star_identity_parity_verified"]
assert not guard["nonpromotion"]["individual_death_timing_inference_allowed"]
assert not guard["nonpromotion"]["individual_death_type_inference_allowed"]
assert guard["real_human_deaths_predicted_or_validated"] == 0

rows, group_inverse = [], []
for idx, group in enumerate(a["groups"], 1):
    span = f"B07l-S{idx:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= set(range(678, 686))
    mapped = []
    for clause in group["claims"]:
        number = 10247 + len(rows)
        rid = f"R{number}"
        assert clause["id"] == rid
        assert len(clause["original_anchor_not_diplomatic"]) >= 5
        assert len(clause["historical_meaning_only"]) >= 38
        assert clause["historical_source_only"]
        assert not clause["real_person_mortality_accuracy_validated"]
        assert not clause["real_person_medical_crime_or_safety_inference_authorized"]
        assert not clause["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07l",
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": clause["role"],
                "original_anchor_not_diplomatic": clause["original_anchor_not_diplomatic"],
                "historical_meaning_only": clause["historical_meaning_only"],
                "qualification": clause["qualification"],
                "documentary_source_accepted": True,
                "independent_human_natural_vs_violent_death_validated": False,
                "independent_human_death_age_or_date_validated": False,
                "independent_human_cause_of_death_validated": False,
                "independent_human_injury_violence_or_morality_validated": False,
                "source_fixed_star_natal_parity_verified": False,
                "source_other_authors_independently_collated": False,
                "real_person_medical_criminality_or_mortality_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        mapped.append(rid)
    group_inverse.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": mapped,
        }
    )
assert len(rows) == 222
assert [r["record_number"] for r in rows] == list(range(10247, 10469))
assert [r["id"] for r in rows if r["role"] == "next_section_navigation"] == ["R10467", "R10468"]
assert len({r["id"] for r in rows}) == 222

photos = {}
for n in range(678, 686):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    photos[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(data),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "role": (
            "original_CLVI_mortality_text"
            if n <= 684
            else "following_separate_unnumbered_directions_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07l",
        "first_edition_source": (
            "William Lilly Christian Astrology 1647 first edition Wellcome b30338724"
        ),
        "original_full_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": list(range(678, 685)),
        "next_unnumbered_directions_starts_pdf": 685,
        "original_source_images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07l",
        "source_groups": group_inverse,
        "source_group_count": 11,
        "historical_annotations": 222,
        "substantive": 220,
        "navigation": 2,
        "historic_fixed_star_table": "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json",
        "mortality_quarantine": "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07l",
        "issues": [
            (
                "These are historic astrological assertions about death, self-harm, "
                "injury, poisoning and criminal violence. No clinical, police, "
                "personal legal, medical or mortality predictions are authorized."
            ),
            (
                "This seven-page first-edition source is CLVI PDF678–684; "
                "the new decorated separate unnumbered EFFECTS OF DIRECTIONS "
                "starts PDF685, not part of mortality aphorisms. "
                "Numbered CLVII starts later PDF688."
            ),
            (
                "The six fixed-star original source longitudes on PDF678 are "
                "historical position descriptions, NOT modern astronomical "
                "ephemeris coordinates. Original glyph precision and star/"
                "sign identification remain partly uncertain."
            ),
            (
                "The opening source uses Sun/Moon, Saturn/Mars, eighth house "
                "ruler, Ascendant lord and named fixed stars as different "
                "tiers; later mortality-mode claims require chosen strongest "
                "afflicting significator AND sign/house; avoid isolated rule."
            ),
            (
                "The first-edition original source lists alternatives with "
                "numerous different alleged causes of death under identical "
                "configurations; no unique target or probability is supplied."
            ),
            (
                "Several claims require two or three concordant testimonies "
                "rather than one; no quantitative tie-breaking or finite "
                "event horizon is defined. Actual natal geometry not computed."
            ),
            (
                "PDF679 explicit broad exception: one beneficial planet "
                "in Ascendant and the other in eighth is claimed to "
                "NEGATE all preceding supposed violent death indications."
            ),
            (
                "PDF681: Lilly explicitly says benefic planets MITIGATE "
                "Saturn's supposed fatal outcomes. Do not ignore this."
            ),
            (
                "PDF682: ALL preceding Mars-violent-death aphorisms require "
                "configuration with at least one luminary or the "
                "judgment is INVALID, an explicit prerequisite."
            ),
            (
                "PDF684: isolated old aphorisms do not themselves operate "
                "without serious mixture with principal significators. "
                "Lilly cites his experience but provides no "
                "independently auditable hit/miss dataset."
            ),
            (
                "PDF684 source negative alternative: if none of the "
                "violent-death patterns is present, the author "
                "supposes natural death with disease, using "
                "eighth-house strongest planet or eighth lord."
            ),
            (
                "PDF684 Lilly explicitly warns astrologers against "
                "positively predicting the TIME OF DEATH, claims "
                "it rests in God's hands, and asks for modesty. "
                "No death time output is legitimate."
            ),
            (
                "The quality-of-death source adds moral, criminal and "
                "class labels about thieves, murderers, 'heretics', "
                "royalty and public punishment, reflecting period "
                "biases, not any real person's behavior or risk."
            ),
            (
                "Ptolemy, Schoner, Cardanus, Albubater, Haly and "
                "Origanus are cited as authorities for some "
                "historical rules, but their ORIGINAL texts "
                "were not cross-collated for this batch."
            ),
            (
                "Old fixed-star/planetary statements include "
                "injury or loss of vision that is NOT death. "
                "Keep fatal and non-fatal outcomes separate."
            ),
            (
                "The original first-edition page transcription "
                "remains selective reversible clauses/anchors, "
                "not an exact diplomatic reproduction of "
                "every glyph or an executable score engine."
            ),
        ],
        "original_all_glyphs_and_orbs_verified": False,
        "original_fixed_star_modern_parity_verified": False,
        "original_Ptolemy_Haly_Albubater_Cardanus_Schoner_cited_sources_collated": False,
        "mortality_scoring_engine_computable": False,
        "independently_verified_human_death_predictions": 0,
        "person_mortality_medical_crime_or_self_harm_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07l",
        "status": "ORIGINAL_1647_CLVI_MORTALITY_HISTORICAL_TEXT_ONLY",
        "printed_chapter": "CLVI",
        "record_count": 222,
        "first_record": "R10247",
        "last_record": "R10468",
        "substantive": 220,
        "following_navigation": 2,
        "source_groups": 11,
        "body_pdf_frames": list(range(678, 685)),
        "following_unnumbered": "THE_EFFECTS_OF_DIRECTIONS",
        "following_heading_pdf": 685,
        "historic_fixed_star_table": "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json",
        "source_quarantine": "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json",
        "complete_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independently_verified_death_timing_results": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07l",
        "status": "FIRST_EDITION_CLVI_MORTALITY_HISTORICAL_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10246,
        "new_historical_annotations": 222,
        "lilly_if_published": 10468,
        "ptolemy_retained": 1066,
        "combined_if_published": 11534,
        "substantive": 220,
        "navigation": 2,
        "source_groups": 11,
        "new_numbered_chapters": 1,
        "next_unnumbered_section": "THE_EFFECTS_OF_DIRECTIONS",
        "next_original_pdf": 685,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "star_source_table_sha256": sha(B / "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json"),
        "nonpromotion_guard_sha256": sha(B / "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
        "empirical_validations": 0,
        "actual_person_death_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print(
    "B07l first edition CLVI source: 222 historic annotations R10247-R10468; "
    "life or death prediction prohibited."
)
