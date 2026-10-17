#!/usr/bin/env python3
"""Original first-edition Lilly 1647 child-count chapter source-only freeze."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


author = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06q"
assert author["printed_chapter"] == "CXXXVIII"
assert author["body_pdf_frames"] == [638, 639, 640]
assert author["next_unnumbered"] == "NINTH_HOUSE_JOURNEYS_RELIGIONS"
assert author["next_section_heading_frame"] == 640
assert author["following_printed"] == "CXXXIX"
assert author["following_printed_frame"] == 640
assert len(author["source_groups"]) == 6

records, mapdata = [], []
for n, group in enumerate(author["source_groups"], 1):
    span = f"B06q-S{n:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {638, 639, 640}
    ids = []
    for c in group["claims"]:
        num = 8603 + len(records)
        rid = f"R{num}"
        assert c["id"] == rid
        assert len(c["original_anchor_not_diplomatic"]) >= 6
        assert len(c["historical_only_meaning"]) >= 43
        assert not c["independent_human_child_related_outcome_validated"]
        assert not c["clinical_mortality_sex_or_child_morality_inference_authorized"]
        assert not c["runtime_promoted"]
        records.append(
            {
                "id": rid,
                "record_number": num,
                "batch": "B06q",
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": c["role"],
                "original_anchor_not_diplomatic": c["original_anchor_not_diplomatic"],
                "source_meaning_historical_only": c["historical_only_meaning"],
                "qualification": c["qualification"],
                "historical_documentary_accepted": True,
                "independent_actual_live_birth_count_validated": False,
                "independent_child_sex_accuracy_validated": False,
                "independent_child_survival_age_validated": False,
                "independent_parent_child_emotional_accuracy_validated": False,
                "clinical_health_or_child_mortality_forecast_authorized": False,
                "person_level_moral_or_gender_label_authorized": False,
                "ptolemy_source_attribution_independently_verified": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapdata.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 78
assert [x["record_number"] for x in records] == list(range(8603, 8681))
assert [x["id"] for x in records if x["role"] == "next_section_navigation"] == ["R8679", "R8680"]
assert len({x["id"] for x in records}) == 78

images = {}
for n in range(638, 644):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(file.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(file),
        "printed_folio": str(n - 34),
        "role": (
            "numbered_children_count_body" if n <= 640 else "following_ninth_house_journeys_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06q",
        "source": (
            "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724"
        ),
        "full_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [638, 639, 640],
        "following_unnumbered_ninth_house_start_pdf": 640,
        "following_printed_CXXXIX_heading_pdf": 640,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06q",
        "source_groups": mapdata,
        "source_groups_count": 6,
        "record_count": 78,
        "substantive": 76,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06q",
        "issues": [
            (
                "The original child-count chapter uses fruitful "
                "fifth/eleventh planets and fertile sign labels, "
                "with double-count for bicorporeal and triple-count "
                "for fruitful signs. A sign can be in both categories "
                "and the original supplies no disambiguating precedence."
            ),
            (
                "The source predicts a number of children, not "
                "precisely defined legal offspring, biological "
                "live births, fetal losses, surviving or cared-for "
                "children, adoption, or adult dependants."
            ),
            (
                "Child-sex rules impose planet, zodiac house, "
                "sign and degree masculine classifications, "
                "while Moon/Venus feminine predicates also "
                "require occidental status. These traditional "
                "labels have no reproductive biology validity."
            ),
            (
                "The separate claimed longevity/fame/happiness, "
                "obedience and parental profit outcomes cannot "
                "substitute for actual child numbers."
            ),
            (
                "The father's relationship with child is alleged "
                "from favorable/hostile aspects between first "
                "and fifth house lords, without longitudinal "
                "dyad records or validated relationship measurement."
            ),
            (
                "The attributed Albubater aphorisms allege "
                "early child death, no offspring remaining, "
                "death order versus parent and malefic aspects. "
                "They are not independently collated with "
                "original Albubater text."
            ),
            (
                "Several glyphs in Saturn/Mercury/Sun "
                "Taurus Midheaven and later fifth-ruler "
                "sign/aspect branches are uncertain, "
                "not operationally executable."
            ),
            (
                "The author attributes a rival tenth, eleventh, "
                "fourth and fifth house method to Ptolemy "
                "and says later authors differed. This "
                "attribution has not been independently "
                "verified against original Ptolemy."
            ),
            (
                "The chosen contemporary fifth-house priority "
                "from prior unnumbered source therefore "
                "must not be silently represented as "
                "Ptolemy's independent confirming method."
            ),
            (
                "No verified natal charts or birth times, "
                "registered pregnancies and births, "
                "sex ratios, child survival records, "
                "mortality denominators or independently "
                "blinded comparisons are supplied."
            ),
            (
                "No human clinical, reproductive, child mortality "
                "or family therapy recommendations may be "
                "made from period astrological claims."
            ),
            (
                "The next immediate source is the separate "
                "unnumbered ninth-house travel/religion "
                "introduction on PDF640 before next "
                "printed numbered CHAP CXXXIX on the SAME page."
            ),
            (
                "Source integrity and photographic"
                " verification do not validate astrology's"
                " predictive success or create a runtime rule."
            ),
            (
                "The extraction selectively paraphrases qualified "
                "historical content; not a diplomatic original "
                "glyph-by-glyph publication."
            ),
        ],
        "original_glyphs_fully_verified": False,
        "original_ptolemy_disagreement_collated": False,
        "human_fertility_child_survival_prediction_validations": 0,
        "medical_or_child_mortality_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06q",
        "status": "ORIGINAL_FIRST_EDITION_CHILD_COUNT_HISTORICAL_ONLY",
        "printed_chapter": "CXXXVIII",
        "editorial_chapter": "CXXXIX",
        "record_count": 78,
        "first_record": "R8603",
        "last_record": "R8680",
        "substantive": 76,
        "following_unnumbered_navigation": 2,
        "source_groups": 6,
        "body_pdf_frames": [638, 639, 640],
        "next_unnumbered_section": "NINTH_HOUSE_JOURNEYS_RELIGIONS",
        "next_unnumbered_section_pdf": 640,
        "following_printed_chapter": "CXXXIX",
        "following_printed_heading_pdf": 640,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "child_mortality_or_count_predictive_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06q",
        "status": "FIRST_EDITION_CHILD_COUNT_DOCUMENTARY_LOCALLY_FROZEN",
        "previous_lilly": 8602,
        "new_historical_annotations": 78,
        "lilly_if_published": 8680,
        "ptolemy_retained": 1066,
        "combined_if_published": 9746,
        "substantive": 76,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_source": "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS",
        "next_original_pdf": 640,
        "following_printed_chapter": "CXXXIX",
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_child_sex_count_or_survival_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print(
    "Original CXXXVIII children count R8603–R8680: 78 historical items; Ptolemy disagreement kept."
)
