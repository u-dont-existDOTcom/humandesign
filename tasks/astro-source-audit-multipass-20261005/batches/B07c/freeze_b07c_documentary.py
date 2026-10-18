#!/usr/bin/env python3
"""Original Lilly 1647 CXLIX: freeze historical occupation aphorisms, not people."""

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
valid = read("PROFESSION_VALIDATION_REQUIREMENTS_V1.json")
assert a["batch"] == "B07c"
assert a["printed_chapter"] == "CXLIX"
assert a["body_pdf_frames"] == list(range(660, 669))
assert a["next_source"] == "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS"
assert a["next_original_pdf"] == 668
assert a["following_numbered_printed"] == "CL"
assert len(a["groups"]) == 14
assert valid["explicit_nonpromotion"]
assert valid["real_human_occupation_validation"] == valid["runtime_promotions"] == 0

records, mapped = [], []
for idx, source in enumerate(a["groups"], 1):
    span = f"B07c-S{idx:03d}"
    assert source["source_span"] == span
    assert set(source["original_pdf_frames"]) <= set(range(660, 669))
    these = []
    for clause in source["claims"]:
        n = 9527 + len(records)
        rid = f"R{n}"
        assert clause["id"] == rid
        assert len(clause["original_anchor_not_diplomatic"]) >= 5
        assert len(clause["historical_meaning_only"]) >= 38
        assert clause["source_only"]
        assert not clause["independent_person_occupation_validated"]
        assert not clause["real_person_social_criminality_forecast_authorized"]
        assert not clause["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": n,
                "batch": "B07c",
                "source_span": span,
                "original_pdf_frames": source["original_pdf_frames"],
                "role": clause["role"],
                "original_anchor_not_diplomatic": clause["original_anchor_not_diplomatic"],
                "source_meaning_historical_only": clause["historical_meaning_only"],
                "qualification": clause["qualification"],
                "source_documentary_accepted": True,
                "independent_real_occupation_category_accuracy_validated": False,
                "independent_real_work_skill_or_income_validated": False,
                "independent_real_religion_or_occult_ability_validated": False,
                "independent_real_violence_crime_or_personality_validated": False,
                "modern_occupation_code_mapping_verified": False,
                "original_albubater_attribution_crosscollated": False,
                "person_level_employment_or_danger_prediction_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        these.append(rid)
    mapped.append(
        {
            "source_span": span,
            "original_pdf_frames": source["original_pdf_frames"],
            "source_group": source["topic"],
            "mapped_record_ids": these,
        }
    )
assert len(records) == 251
assert [x["record_number"] for x in records] == list(range(9527, 9778))
assert [x["id"] for x in records if x["role"].startswith("navigation_")] == [
    "R9775",
    "R9776",
    "R9777",
]
assert len({x["id"] for x in records}) == 251

images = {}
for n in range(660, 671):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": (
            "CXLIX_profession_aphorisms_original_body"
            if n <= 668
            else "following_unnumbered_friends_context_only"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07c",
        "original_source": (
            "William Lilly Christian Astrology original 1647 first edition Wellcome b30338724"
        ),
        "complete_first_edition_source_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": list(range(660, 669)),
        "following_unnumbered_eleventh_heading_frame": 668,
        "following_numbered_CL_heading_frame": 670,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07c",
        "source_groups": mapped,
        "source_group_count": 14,
        "record_count": 251,
        "substantive": 248,
        "following_unnumbered_navigation": 3,
        "modern_validation_guard": "PROFESSION_VALIDATION_REQUIREMENTS_V1.json",
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07c",
        "issues": [
            (
                "Printed CXLIX runs from middle PDF660/printed626 "
                "to original PDF668/printed634 before an entirely "
                "separate substantive UNNUMBERED eleventh-house "
                "intro Of Friends, not a continuation of profession."
            ),
            (
                "The chapter repeatedly names Mercury, Venus and Mars "
                "as possible or joint profession significators, but "
                "other planets, zodiac sign, house, relative strength "
                "and overriding partile aspects may completely change "
                "the claimed profession; no fixed priority score "
                "for all contradictory combinations is supplied."
            ),
            (
                "An occupation label, interest, income, lifelong main "
                "activity, performance quality, social esteem and "
                "family role are separate outcomes. Professional "
                "success/fame subsection must not be counted as "
                "correct career type in any future evaluation."
            ),
            (
                "Most of the old occupational lists allow many jobs "
                "under a single configuration, often spanning "
                "scholarly disciplines, commerce, warfare, cooking, "
                "farm work and even clergy, thereby providing "
                "very low post-hoc discriminative specificity."
            ),
            (
                "Several source claims stigmatize poorer classes "
                "and assert thieves, murderers, poisoning, lying "
                "or sex-work roles from astrological placements. "
                "No character, crime, violent risk or protected "
                "religious classification about any real "
                "person may be inferred from these historical labels."
            ),
            (
                "The text alleges divination, prophetic interests, "
                "magical practice and sorcery from sign and planet "
                "aspects. It does not establish actual "
                "supernatural powers or medical/mental diagnoses."
            ),
            (
                "Cazimi is explicitly an exception to combustion "
                "for Mercury-Sun and Venus-Sun in earlier and "
                "current material; a single burn/combustion "
                "predicate cannot be used blindly."
            ),
            (
                "Mercury-Jupiter may be associated with respected "
                "lawful speakers, while Mercury-Saturn or "
                "Mercury-Mars variants include both legitimate "
                "crafts and unsupported criminal accusations. "
                "The author therefore supplies contradictory "
                "profession classes under nearby natal predicates."
            ),
            (
                "Venus-Mercury, Mars-Mercury and Venus-Mars compound "
                "rules can depend on additional Saturn, Jupiter, "
                "Moon, Sun, relative dignity and zodiac sign, "
                "and some planetary glyph combinations "
                "require independent diplomatic collation."
            ),
            (
                "The original profession success section requires "
                "source significator essential dignity, "
                "absence of malignant partile contact, "
                "angularity and orientality; weak/cadent/"
                "occidental variants make pejorative "
                "assertions about craft skill and industry."
            ),
            (
                "Source zodiac taxonomy includes movable, "
                "fixed EXCEPT Scorpio, humane, water/earth, "
                "quadruped; the passage attributes additional "
                "elemental jobs to ALBUBATER, whose own "
                "original writing remains uncollated."
            ),
            (
                "A previous Lilly general planetary-nature section "
                "at printed pages 57–83 is cited but not "
                "re-extracted in this specific chapter."
            ),
            (
                "No frozen occupation ontology, measured modern "
                "job distributions, birth-time-confirmed real "
                "cohort, education/class/location controls, "
                "negative prediction denominator or chart "
                "calculation implementation used here."
            ),
            (
                "Following printed CHAP CL on quality of friends "
                "starts PDF670 AFTER unnumbered eleventh-house "
                "friendship introduction PDF668–669. The "
                "immediate next canonical source must be "
                "unnumbered and add ZERO numbered chapters."
            ),
            (
                "The packet uses reversible short photographed "
                "original text anchors and historical paraphrases, "
                "not a full diplomatic facsimile transcription. "
                "Claims are not validated human forecasts."
            ),
        ],
        "original_all_glyphs_and_orbs_resolved": False,
        "original_albubater_attribution_independently_collated": False,
        "modern_occupation_mapping_and_baselines_defined": False,
        "real_person_profession_predictions_validated": 0,
        "actual_person_crime_morality_religion_or_spiritual_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07c",
        "status": "ORIGINAL_1647_CXLIX_OLD_OCCUPATION_APHORISMS_HISTORICAL_ONLY",
        "printed_chapter": "CXLIX",
        "record_count": 251,
        "first_record": "R9527",
        "last_record": "R9777",
        "substantive": 248,
        "following_unnumbered_navigation": 3,
        "source_groups": 14,
        "body_original_pdf_frames": list(range(660, 669)),
        "next_unnumbered_section": "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS",
        "next_original_pdf": 668,
        "following_printed_CL_frame": 670,
        "modern_validation_guard": "PROFESSION_VALIDATION_REQUIREMENTS_V1.json",
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_human_profession_accuracy_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07c",
        "status": "ORIGINAL_CXLIX_PROFESSION_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 9526,
        "new_historical_annotations": 251,
        "lilly_if_published": 9777,
        "ptolemy_retained": 1066,
        "combined_if_published": 10843,
        "substantive": 248,
        "navigation": 3,
        "source_groups": 14,
        "new_numbered_chapters": 1,
        "next_source": "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS",
        "next_original_pdf": 668,
        "following_printed_chapter": "CL",
        "following_printed_heading_pdf": 670,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "scope_guard_sha256": sha(B / "PROFESSION_VALIDATION_REQUIREMENTS_V1.json"),
        "empirical_validations": 0,
        "real_profession_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07c original CXLIX: 251 source annotations R9527–R9777, next UNNUMBERED eleventh.")
