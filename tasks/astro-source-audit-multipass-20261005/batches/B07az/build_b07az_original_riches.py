#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete historical source qualification sentences.
"""Lilly 1647/1659 original Riches chapter documentary source-first packet.

A known merchant's horoscope is a historically unblinded case. Wealth,
family disputes, inheritance and social categories are SOURCE CLAIMS, not
verified event outcomes. 1647/1659 are two prints of the same account,
not independent predictive replication.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
P = B.parent
SOURCE_PDF_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# Each entry was located by a single reader in the first-edition 1647 photo.
# Source anchors are descriptive, NOT verbatim quotes or independently checked translations.
# Do not use this known-person retrospective narrative as observed outcome evidence.
ITEMS = [
    (
        749,
        "CHAPTER_HEAD",
        "SOURCE_BOUNDARY",
        "Original 1647 CHAP CLXXVII Of Riches begins below the CLXXVI physical divider.",
    ),
    (
        749,
        "HOUSE_TWO",
        "CHART_CONTEXT",
        "Lilly uses the second house and its lord for wealth judgments.",
    ),
    (
        749,
        "AQUARIUS_23_30",
        "NUMERIC_SOURCE_GLYPH",
        "First-edition printed second-house sign reads Aquarius 23°30′; modern searchable derivative abbreviates to 23.3.",
    ),
    (
        749,
        "SATURN_TAURUS",
        "CHART_CONTEXT",
        "Saturn is presented as lord of the first and second houses and in fixed Taurus.",
    ),
    (
        749,
        "NODE_IN_SECOND",
        "CHART_CONTEXT",
        "North Node is placed in the second house in the historical source account.",
    ),
    (
        749,
        "PISCES_INTERCEPTED",
        "CHART_CONTEXT",
        "Pisces is intercepted in the second house and assigned to Jupiter.",
    ),
    (
        749,
        "JUPITER_TWELFTH",
        "CHART_CONTEXT",
        "Jupiter is said to be strong in the twelfth despite its house placement.",
    ),
    (
        749,
        "FORTUNA_SOUTH_NODE",
        "CHART_CONTEXT",
        "Part of Fortune is in Virgo together with the South Node.",
    ),
    (
        749,
        "MERCURY_COMBUST",
        "CHART_CONTEXT",
        "Mercury, which disposes Part of Fortune, is described as combust in Libra.",
    ),
    (
        749,
        "SECOND_FIXED_SEXTILE_JUPITER",
        "CONDITIONAL_ASTRO_CLAIM",
        "Fixed second house and Jupiter's sinister sextile are given as supporting factors.",
    ),
    (
        749,
        "JUPITER_AS_GENERAL_WEALTH_SIGNIFICATOR",
        "CONDITIONAL_ASTRO_CLAIM",
        "Jupiter's natural wealth role and rulership of intercepted Pisces are invoked.",
    ),
    (
        749,
        "SOURCE_SELF_ACQUIRED_FIXED_ESTATE",
        "HISTORIC_PROSPECTIVE_CLAIM_UNVERIFIED",
        "Lilly forecasts a lasting estate acquired primarily through work, travel and industry.",
    ),
    (
        749,
        "SOURCE_BEFORE_MIDDLE_AGE_THIRTY_FIVE",
        "HISTORIC_TIME_PREDICTION_UNVERIFIED",
        "Wealth is forecast before approximately age 35, qualified by natal circumstances.",
    ),
    (
        749,
        "LATER_QUIET_INTERVAL_IF_NO_GOOD_DIRECTIONS",
        "HISTORIC_TIME_PREDICTION_UNVERIFIED",
        "After age 35 he expects a quieter period conditionally if beneficial directions do not intervene.",
    ),
    (
        750,
        "LATER_INCREASE_SATURN_NORTH_NODE",
        "HISTORIC_TIME_PREDICTION_UNVERIFIED",
        "Saturn and North Node are used to claim a later-life increase in goods and land.",
    ),
    (
        750,
        "SATURN_EARTH_TAURUS_PROPERTY",
        "CONDITIONAL_ASTRO_CLAIM",
        "Saturn in Taurus is connected with property, land, houses and earth-derived trades.",
    ),
    (
        750,
        "EARTHLY_ECONOMIC_DOMAINS",
        "HISTORIC_FINANCIAL_PREDICTION_UNVERIFIED",
        "Lilly proposes pasture, tillage, mines, minerals and sea coal as possible wealth sources.",
    ),
    (
        750,
        "JOVIAL_ASSOCIATES",
        "HISTORIC_SOCIAL_CLAIM_UNVERIFIED",
        "Jupiter is connected with gain through a historical physical/personality stereotype of associates.",
    ),
    (
        750,
        "NORTH_NODE_VENUS_JUPITER_CONFIRMATION",
        "CONDITIONAL_ASTRO_CLAIM",
        "North Node's traditional Jupiter/Venus nature is offered as corroboration.",
    ),
    (
        750,
        "VENUS_WOMEN_TRAVEL_GOODS",
        "HISTORIC_FINANCIAL_PREDICTION_UNVERIFIED",
        "Strong Venus suggests possible wealth through women, spouses, travel, jewelry, linen or related goods.",
    ),
    (
        750,
        "FATHER_MAY_AID_ESTATE",
        "HISTORIC_FAMILY_CLAIM_UNVERIFIED",
        "Reception between Saturn and Venus is used to suggest the father may aid the estate.",
    ),
    (
        750,
        "PATRIMONY_DEPLETION_SISTER_KIN",
        "HISTORIC_FAMILY_CLAIM_UNVERIFIED",
        "Moon square Part of Fortune and South Node are interpreted as inheritance reduced by sister or kinsman.",
    ),
    (
        750,
        "KINSHIP_FIXED_SQUARE",
        "CONDITIONAL_ASTRO_CLAIM",
        "Saturn–Mars square in fixed signs is invoked for difficulties involving brothers or other kin.",
    ),
    (
        750,
        "FORGED_WILL_LAWSUIT",
        "HISTORIC_LEGAL_CLAIM_UNVERIFIED",
        "He speculates about forged testamentary evidence, litigation, or obstruction by relatives.",
    ),
    (
        751,
        "STRONG_WITNESSES_PERSONAL_INDUSTRY",
        "HISTORIC_FINANCIAL_PREDICTION_UNVERIFIED",
        "Original page says favorable fixed stars and Venus/Jupiter favor a substantial estate through industry.",
    ),
    (
        751,
        "ACQUIRE_VERSUS_KEEP",
        "HISTORIC_BEHAVIORAL_CLAIM_UNVERIFIED",
        "The merchant is forecast to be better at acquiring wealth than retaining it.",
    ),
    (
        751,
        "RETROGRADE_SATURN_CADENT_JUPITER",
        "CONDITIONAL_ASTRO_CLAIM",
        "Retrograde Saturn and cadent Jupiter are cited for difficulty preserving gains.",
    ),
    (
        751,
        "LEGACY_LAWSUIT_SOUTH_NODE",
        "HISTORIC_LEGAL_CLAIM_UNVERIFIED",
        "South Node near Fortune is used to forecast patrimony wasted in legacy lawsuits or fraud.",
    ),
    (
        751,
        "CLXXVIII_BRETHREN_BOUNDARY",
        "NEXT_SOURCE_BOUNDARY",
        "CLXXVII physically ends above divider; the distinct CLXXVIII Of Brethren starts on the same printed folio.",
    ),
]
assert len(ITEMS) == 29
old = j(INDEX)
chinese = j(CHINA)
assert old["records_count"] == 12940 and old["batches"][-1]["id"] == "B07ay"
assert old["next"]["chapter"] == "CLXXVII" and old["next"]["pdf_page"] == 783
assert old["read_numbered_chapters"] == list(range(1, 177))
assert chinese["sum_source_annotations"] == 355
prior_photo = j(P / "B07ay/ORIGINAL_PHOTO_WITNESS_V1.json")
assert prior_photo["source_full_Wellcome_1647_original_PDF_SHA256"] == SOURCE_PDF_SHA
photos = {}
for folio in (749, 750, 751):
    first = (
        ROOT / prior_photo["source_1647_1659_page_photos"]["1647_printed_749"]["image_path"]
        if folio == 749
        else B / "evidence" / f"1647_original-{folio + 34}.jpg"
    )
    second = (
        ROOT / prior_photo["source_1647_1659_page_photos"]["1659_printed_749"]["image_path"]
        if folio == 749
        else B / "evidence" / f"1659_original_djvu_{folio + 29}.jpg"
    )
    assert first.is_file() and second.is_file()
    photos[str(folio)] = {
        "first_original_1647": {
            "relative_path": str(first.relative_to(ROOT)),
            "sha256": sha(first),
            "bytes": first.stat().st_size,
            "original_pdf_frame": folio + 34,
        },
        "independently_typeset_1659": {
            "relative_path": str(second.relative_to(ROOT)),
            "sha256": sha(second),
            "bytes": second.stat().st_size,
            "original_djvu_page": folio + 29,
        },
    }
assert (
    photos["749"]["first_original_1647"]["sha256"]
    == prior_photo["source_1647_1659_page_photos"]["1647_printed_749"]["sha256"]
)
assert (
    photos["749"]["independently_typeset_1659"]["sha256"]
    == prior_photo["source_1647_1659_page_photos"]["1659_printed_749"]["sha256"]
)
records = []
for i, (folio, role, layer, meaning) in enumerate(ITEMS):
    rid = f"R{12941 + i}"
    records.append(
        {
            "id": rid,
            "record_number": 12941 + i,
            "batch": "B07az",
            "source_span": f"B07az-S{folio - 748:03d}",
            "original_pdf_frames": [folio + 34],
            "original_printed_folio": folio,
            "separate_1659_DjVu_frame": folio + 29,
            "role": role,
            "source_evidence_layer": layer,
            "source_locator_not_diplomatic_quote": role.replace("_", " ").lower(),
            "historical_source_interpretation": meaning,
            "original_first_1647_photo_SHA256": photos[str(folio)]["first_original_1647"]["sha256"],
            "separate_print_1659_photo_SHA256": photos[str(folio)]["independently_typeset_1659"][
                "sha256"
            ],
            "historic_subject_already_known_to_Lilly": True,
            "this_is_not_observed_independently_verified_outcome": True,
            "source_era_1616_natal_ephemeris_verified": False,
            "source_merchant_biography_independently_verified": False,
            "traditional_chart_to_wealth_claim_falsification_evaluated": False,
            "independent_real_human_prediction_validated": False,
            "runtime_model_promoted": False,
        }
    )
assert records[0]["id"] == "R12941"
assert records[-1]["id"] == "R12969"
assert records[-1]["role"] == "CLXXVIII_BRETHREN_BOUNDARY"
assert all(r["historic_subject_already_known_to_Lilly"] for r in records)
source = {
    "schema": "LILLY_1647_1659_CLXXVII_RICHES_KNOWN_MERCHANT_29_SOURCE_NOTES_V1",
    "batch": "B07az",
    "original_full_1647_PDF_sha256": SOURCE_PDF_SHA,
    "original_printed_chapter": "CLXXVII",
    "original_heading": "Of RICHES",
    "actual_chapter_folios": [749, 750, 751],
    "actual_1647_PDF_frames": [783, 784, 785],
    "separate_printed_1659_DjVu_frames": [778, 779, 780],
    "original_1647_and_1659_six_source_photo_witnesses": photos,
    "prior_original_CLXXVI_end_and_next_divider_shared_folio749": True,
    "next_original_CLXXVIII_starts_shared_folio751": True,
    "first_original_chapter_starts_after_physical_divider_on_printed749": True,
    "subject_was_already_known_to_original_author": True,
    "source_is_retrospective_unblinded_individual_reading": True,
    "historical_moral_financial_family_or_legal_claims_are_unverified": True,
    "original_fixed_second_cusp_print_Aquarius_degree_minute": [23, 30],
    "secondary_searchable_derivative_truncates_minutes": "Aquarius 23.3",
    "first_print_minus_secondary_text_transcription_tenths_dont_interpret_as_arithmetic": True,
    "independent_biographical_wealth_predicted_outcomes_validated": 0,
    "original_17th_century_natal_chart_engine_verified": False,
    "complete_independent_critical_edition_expert_review": False,
    "historical_documentary_annotation_count": len(records),
    "next_source_historical_id": "R12970",
    "next_original_pdf_frame": 785,
    "next_original_printed_folio": 751,
    "next_original_printed_chapter": "CLXXVIII",
    "runtime_promotions": 0,
    "records": records,
}
out = B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"
save(out, source)
rules = {
    "batch": "B07az",
    "status": "ORIGINAL_1647_1659_CLXXVII_RICHES_KNOWN_MERCHANT_DOCUMENTARY",
    "record_count": len(records),
    "first_record": "R12941",
    "last_record": "R12969",
    "source_groups": 3,
    "body_pdf_frames": [783, 784, 785],
    "full_original_CLXXVII_physical_source_span_covered": True,
    "next_original_CLXXVIII_begins_same_final_folio751": True,
    "known_merchant_not_blinded_prediction": True,
    "biographical_events_independently_verified": False,
    "natal_1616_chart_engine_verified": False,
    "empirical_actual_person_outcomes_validated": 0,
    "runtime_promotions": 0,
    "rules": records,
}
save(B / "RULES.json", rules)
accept = {
    "batch": "B07az",
    "Lilly_before": 12940,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "new_source_only_historical_annotations": len(records),
    "Lilly_after_if_accepted": 12969,
    "Western_if_accepted": 14035,
    "next_R": "R12970",
    "next_original_PDF_frame": 785,
    "next_original_printed_folio": 751,
    "next_chapter": "CLXXVIII",
    "next_heading": "Of BRETHREN",
    "original_CLXXVII_physical_span_complete": True,
    "all_source_early_print_critical_expert_review": False,
    "independent_actual_merchant_financial_outcomes_validated": 0,
    "source_photo_witness_SHA256": sha(out),
    "rules_SHA256": sha(B / "RULES.json"),
    "independent_human_predictive_validations": 0,
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "new_source_records": len(records),
            "first": records[0]["id"],
            "last": records[-1]["id"],
            "next": accept["next_R"],
            "first_second_editions_photo_hashes": [
                photos[x]["first_original_1647"]["sha256"] for x in photos
            ],
            "notes_sha256": sha(out),
            "rules_sha256": sha(B / "RULES.json"),
        },
        indent=2,
    )
)
