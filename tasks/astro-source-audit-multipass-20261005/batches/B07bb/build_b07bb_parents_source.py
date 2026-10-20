#!/usr/bin/env python3
# ruff: noqa: E501
"""Source-only first 1647 and second 1659 CLXXIX Parents chapter.

A merchant is already known to Lilly. Original claims about parental
affection, health/lifespan, stature and estate are not verified personal
predictions; source-derived parent chart needs independently verified
historical house tables and latitude/RA math.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
SOURCE_BOOK_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


previous = load(INDEX)
chinese = load(CHINA)
assert previous["records_count"] == 12991 and previous["batches"][-1]["id"] == "B07ba"
assert previous["next"]["chapter"] == "CLXXIX" and previous["next"]["pdf_page"] == 786
assert chinese["sum_source_annotations"] == 355
assert previous["source_sha256"] == SOURCE_BOOK_SHA
prior = load(BASE / "B07ba/ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
old = prior["original_two_editions_four_source_page_images"]["752"]
imgs = {
    "752": {
        "1647": ROOT / old["first_1647"]["relative_original_source_image"],
        "1659": ROOT / old["typeset_1659"]["relative_original_source_image"],
    },
    "753": {
        "1647": B / "evidence/1647_original-787.jpg",
        "1659": B / "evidence/1659_original_djvu_782.jpg",
    },
}
photos = {}
for n, mp in imgs.items():
    photos[n] = {}
    for edition, path in mp.items():
        assert path.is_file()
        photos[n][edition] = {
            "original_source_repo_relative_file": str(path.relative_to(ROOT)),
            "original_folio": int(n),
            "original_photo_pdf_or_djvu_frame": int(n) + (34 if edition == "1647" else 29),
            "source_ed": int(edition),
            "sha256": sha(path),
            "bytes": path.stat().st_size,
        }
assert photos["752"]["1647"]["sha256"] == old["first_1647"]["sha256"]
assert photos["752"]["1659"]["sha256"] == old["typeset_1659"]["sha256"]

# Source-printed claims and procedural instructions, independently categorized.
# These glosses are researcher notes and deliberately not diplomatic quotations.
CLAIMS = [
    (
        752,
        "CLXXIX_PARENTS_HEAD",
        "CHAPTER_BOUNDARY",
        "Original CLXXIX Of Parents begins below the CLXXVIII third-house divider on printed 752.",
    ),
    (
        752,
        "FOURTH_HOUSE_CONSIDERED",
        "HISTORICAL_SOURCE_CONTEXT",
        "The source turns to fourth-house parents within a merchant's known natal case.",
    ),
    (
        752,
        "SOLAR_ELEVATION_FORTY",
        "SOURCE_NUMERICAL_CONVENTION",
        "Lilly adopts polar elevation 40 degrees of the Sun's circle for judging the father.",
    ),
    (
        752,
        "MOTHER_SAME_POSITION_CIRCLE",
        "SOURCE_CONDITIONAL_CONVENTION",
        "In this particular nativity father and mother are treated as nearly sharing one circle of position.",
    ),
    (
        752,
        "SUN_UNAFFLICTED",
        "SOURCE_ASTRO_PREDICATE",
        "The Sun is said not to suffer a malevolent aspect and is received by Venus.",
    ),
    (
        752,
        "SUN_VENUS_CONJUNCTION",
        "SOURCE_ASTRO_PREDICATE",
        "Sun and Venus conjoin, attributed to describing the father's dispositions.",
    ),
    (
        752,
        "FATHER_HUMANE_RATIONAL",
        "UNVERIFIED_AUTHOR_KNOWN_FAMILY_DESCRIPTION",
        "The father is conjectured humane and rational, of a pleasant manner.",
    ),
    (
        752,
        "FATHER_PERSONABLE_STATURE",
        "UNVERIFIED_AUTHOR_KNOWN_FAMILY_DESCRIPTION",
        "The father is described as personable or of good stature.",
    ),
    (
        752,
        "FATHERS_ESTATE_MARS_LEO",
        "UNVERIFIED_FINANCIAL_FAMILY_CLAIM",
        "Mars in Leo is used to suggest the father's estate not very great.",
    ),
    (
        752,
        "FATHER_SUBSTANCE_DIMINISHED_BY_PRETENDED_FRIENDS",
        "UNVERIFIED_FINANCIAL_FAMILY_CLAIM",
        "Lilly conjectures diminution by false friends, soldiers and other persons.",
    ),
    (
        752,
        "VENUS_CAZIMI_SUN",
        "SOURCE_ASTRO_PREDICATE",
        "Venus is asserted to be cazimi with Sun and used to explain marital harmony.",
    ),
    (
        752,
        "FATHER_MOTHER_MARITAL_HARMONY",
        "UNVERIFIED_FAMILY_RELATIONSHIP_CLAIM",
        "The parents' marriage is described as well agreed, based on Venus cazimi.",
    ),
    (
        752,
        "MOTHER_OUTLIVE_FATHER",
        "UNVERIFIED_PARENTAL_MORTALITY_CLAIM",
        "Stronger Venus than Sun is said to suggest mother may outlive father.",
    ),
    (
        752,
        "SATURN_VENUS_MUTUAL_RECEPTION",
        "SOURCE_ASTRO_PREDICATE",
        "Saturn, described as the native's significator, receives Venus and vice versa.",
    ),
    (
        752,
        "MOTHER_MORE_AFFECTION",
        "UNVERIFIED_FAMILY_PSYCHOLOGY_CLAIM",
        "Lilly conjectures the mother's affection for the native exceeds the father's.",
    ),
    (
        753,
        "PTOLEMY_FIRSTBORN_DERIVED_PARENT_CHART",
        "SOURCE_PROCEDURAL_CONVENTION",
        "The source cites Ptolemy's procedure to construct parents' natal configurations from a firstborn child's horoscope.",
    ),
    (
        753,
        "PTOLEMY_DAY_NIGHT_FATHER_SIGNIFICATOR",
        "SOURCE_CONDITIONAL_PROCEDURE",
        "Father: daytime natal Sun; the printed margin indicates Saturn in a night nativity.",
    ),
    (
        753,
        "PTOLEMY_DAY_NIGHT_MOTHER_SIGNIFICATOR",
        "SOURCE_CONDITIONAL_PROCEDURE",
        "Mother: printed margin names Venus for daytime and Moon for nocturnal birth.",
    ),
    (
        753,
        "SOURCE_DAY_BIRTH_SUN_POSITION",
        "SOURCE_PROCEDURAL_CONVENTION",
        "Day birth: determine the Sun and its circle of position as father's source.",
    ),
    (
        753,
        "SOURCE_USE_PARENT_CIRCLE_POLE_ELEVATION",
        "SOURCE_PROCEDURAL_CONVENTION",
        "Erect hypothetical parent chart under the elevation of the Sun's circle, not a confirmed birth time.",
    ),
    (
        753,
        "SOURCE_TABLE_OF_HOUSES_OPTION",
        "SOURCE_PROCEDURAL_CONVENTION",
        "A corresponding table of houses may be used if one is available at that elevation.",
    ),
    (
        753,
        "SOURCE_ADD_THIRTY_OBLIQUE_ASC",
        "SOURCE_NUMERICAL_CONVENTION",
        "Otherwise add 30 degrees to the Sun's oblique ascension for a derived house calculation.",
    ),
    (
        753,
        "REGIOMONTANUS_HOUSE_POLE",
        "SOURCE_PROCEDURAL_REFERENCE",
        "The source cites Regiomontanus for derived house elevations and ecliptic intersections.",
    ),
    (
        753,
        "SOURCE_FATHER_ASC_LIBRA_6_37",
        "SOURCE_NUMERICAL_EXAMPLE",
        "The example claims father's ascendant 6 degrees 37 minutes Libra under pole40.",
    ),
    (
        753,
        "SOURCE_FULL_DERIVED_CHART_UNVERIFIED",
        "SOURCE_CRITICAL_LIMIT",
        "No separately timed parent's birth, ephemeris, Regiomontanus implementation or original sample chart parity is supplied.",
    ),
    (
        753,
        "CLXXX_SICKNESS_SERVANTS_BOUNDARY",
        "NEXT_CHAPTER_BOUNDARY",
        "CLXXIX ends above divider; CLXXX Sicknesse, Servants begins on the same printed753.",
    ),
]
assert len(CLAIMS) == 26
records = []
for i, (folio, role, kind, description) in enumerate(CLAIMS):
    row = photos[str(folio)]
    records.append(
        {
            "id": f"R{12992 + i}",
            "record_number": 12992 + i,
            "batch": "B07bb",
            "source_span": f"B07bb-S{folio - 751:03d}",
            "original_first_edition_pdf_frame": folio + 34,
            "original_second_edition_djvu_frame": folio + 29,
            "original_printed_folio": folio,
            "original_paper_first_1647_sha256": row["1647"]["sha256"],
            "independently_typeset_paper_1659_sha256": row["1659"]["sha256"],
            "role": role,
            "evidence_layer": kind,
            "non_diplomatic_locator": role.replace("_", " ").lower(),
            "historical_gloss_not_author_quotation": description,
            "merchant_known_to_Lilly_before_description": True,
            "source_parent_actual_birth_data_independently_verified": False,
            "source_1616_natal_full_chart_ephemeris_verified": False,
            "source_derived_parent_chart_algorithm_expert_verified": False,
            "historical_mother_outliving_father_observed_result_verified": False,
            "independent_actual_person_prediction_result_validated": False,
            "medicine_or_high_stakes_family_advice_authorized": False,
            "runtime_model_promoted": False,
        }
    )
assert records[-1]["id"] == "R13017"
assert records[-1]["role"] == "CLXXX_SICKNESS_SERVANTS_BOUNDARY"
archive = {
    "schema": "LILLY_ORIGINAL_1647_1659_CLXXIX_PARENTS_SOURCE_26_NOTES_V1",
    "batch": "B07bb",
    "source_full_original_Wellcome_1647_PDF_sha256": SOURCE_BOOK_SHA,
    "original_first_1647_printed_folios": [752, 753],
    "original_first_1647_pdf_frames": [786, 787],
    "original_separate_1659_typeset_djvu_frames": [781, 782],
    "two_original_printings_four_page_photo_witnesses": photos,
    "source_author_knew_merchants_history": True,
    "source_has_parent_chart_derived_from_first_born_not_real_parent_birth": True,
    "original_solar_oblique_asc_plus_30_degree_method_unverified": True,
    "source_father_example_6deg37_Libra_pole40": [6, 37, 40],
    "source_origin_full_1647_book_is_not_early_separate_independent_predictive_test": True,
    "independently_validated_mother_outlived_father_history": 0,
    "independently_reconstructed_parent_natal_charts": 0,
    "independently_validated_real_human_outcomes": 0,
    "runtime_promotions": 0,
    "new_source_only_historical_annotations": len(records),
    "first_record": "R12992",
    "last_record": "R13017",
    "next_record": "R13018",
    "next_source_pdf_frame": 787,
    "next_original_folio": 753,
    "next_printed_chapter": "CLXXX",
    "records": records,
}
save(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json", archive)
rules = {
    "batch": "B07bb",
    "status": "ORIGINAL_CLXXIX_PARENTS_DOCUMENTARY_SOURCE_NOT_PROGNOSES",
    "record_count": 26,
    "first_record": "R12992",
    "last_record": "R13017",
    "source_groups": 2,
    "body_pdf_frames": [786, 787],
    "first_original_CLXXIX_physical_chapter_covered": True,
    "parental_lifespan_claim_not_verified": True,
    "derived_parent_chart_not_verified": True,
    "independent_prospective_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "rules": records,
}
save(B / "RULES.json", rules)
accept = {
    "batch": "B07bb",
    "Lilly_before": 12991,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "new_historical_source_only_notes": 26,
    "Lilly_after_if_accepted": 13017,
    "Western_after_if_accepted": 14083,
    "next_historical_R": "R13018",
    "next_original_PDF_frame": 787,
    "next_printed_folio": 753,
    "next_printed_chapter": "CLXXX",
    "next_heading": "Sicknesse, Servants",
    "source_original_physical_CLXXIX_covered": True,
    "source_expert_diplomatic_collation_complete": False,
    "parent_chart_historical_algorithm_math_engine_verified": False,
    "actual_human_parental_longevity_predictions_validated": 0,
    "source_notes_sha256": sha(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "original_1647_1659_source_photos": 4,
            "new_source_records": 26,
            "first": "R12992",
            "last": "R13017",
            "next": "R13018",
            "original_parental_outcomes_verified": 0,
            "notes_sha256": accept["source_notes_sha256"],
        },
        indent=2,
    )
)
