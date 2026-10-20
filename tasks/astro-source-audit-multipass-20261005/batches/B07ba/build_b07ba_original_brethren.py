#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete source-specific historical statements.
"""Original Lilly CLXXVIII Brethren: source claim versus author-known outcome.

The author says Ptolemy would suggest few siblings, then reports seven
brothers and one sister; extra source factors are deployed after this.
Such an unblinded report is NOT independent natal predictive verification.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
WHOLE = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


previous = j(WEST)
chinese = j(CHINA)
assert previous["records_count"] == 12969 and previous["batches"][-1]["id"] == "B07az"
assert previous["next"]["chapter"] == "CLXXVIII" and previous["next"]["pdf_page"] == 785
assert chinese["sum_source_annotations"] == 355
assert previous["source_sha256"] == WHOLE
prior = j(BASE / "B07az/ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
prevphotos = prior["original_1647_and_1659_six_source_photo_witnesses"]
images = {
    "751": {
        "first_1647": ROOT / prevphotos["751"]["first_original_1647"]["relative_path"],
        "typeset_1659": ROOT / prevphotos["751"]["independently_typeset_1659"]["relative_path"],
    },
    "752": {
        "first_1647": BASE / "B07az/evidence/1647_original-786.jpg",
        "typeset_1659": B / "evidence/1659_original_djvu_781.jpg",
    },
}
photorecord = {}
for folio, parts in images.items():
    photorecord[folio] = {}
    for typ, path in parts.items():
        assert path.is_file()
        photorecord[folio][typ] = {
            "relative_original_source_image": str(path.relative_to(ROOT)),
            "sha256": sha(path),
            "bytes": path.stat().st_size,
            "original_printed_folio": int(folio),
            "source_first_edition_PDF_frame": int(folio) + 34 if typ == "first_1647" else None,
            "source_second_edition_DjVu_frame": int(folio) + 29 if typ == "typeset_1659" else None,
        }
assert (
    photorecord["751"]["first_1647"]["sha256"] == prevphotos["751"]["first_original_1647"]["sha256"]
)
assert (
    photorecord["751"]["typeset_1659"]["sha256"]
    == prevphotos["751"]["independently_typeset_1659"]["sha256"]
)

ITEMS = [
    (
        751,
        "CHAPTER_HEAD",
        "SOURCE_BOUNDARY",
        "Original 1647 CHAP CLXXVIII Of Brethren starts below CLXXVII on printed751.",
    ),
    (
        751,
        "PTOLEMY_FEW_BRETHREN_IF_STRICT",
        "CONDITIONAL_SOURCE_COUNTERSIGNAL",
        "Lilly writes that strict Ptolemaic reasoning would imply not many siblings.",
    ),
    (
        751,
        "BARREN_THIRD_AND_LORD",
        "CONDITIONAL_ASTRO_RULE",
        "The third-house sign and its lord's sign are described as barren.",
    ),
    (
        751,
        "JUPITER_SEXTILE_THIRD_CUSP",
        "CONDITIONAL_ASTRO_RULE",
        "Jupiter sextile the third cusp is invoked as a competing indication of siblings.",
    ),
    (
        751,
        "MARS_SEXTILE_FERTILE_LIBRA",
        "CONDITIONAL_ASTRO_RULE",
        "Mars in sextile to three planets in fecund Libra is another contrary indicator.",
    ),
    (
        751,
        "HISTORICAL_AUTHOR_REPORTS_SEVEN_BROTHERS",
        "AUTHOR_KNOWN_OUTCOME_NOT_EXTERNAL",
        "Lilly reports that this already-known merchant has had seven brothers.",
    ),
    (
        751,
        "AD_HOC_PLANET_COUNT_ALLOCATION",
        "RETROSPECTIVE_RECONCILIATION",
        "Two brothers assigned to Jupiter, one to Mars, and the rest to Mercury Venus and Sun; no frozen counting algorithm.",
    ),
    (
        751,
        "MOON_SISTERS_SIG",
        "CONDITIONAL_ASTRO_RULE",
        "Moon is treated as a general significator of sisters and said to aspect many planets.",
    ),
    (
        751,
        "HISTORICAL_AUTHOR_REPORTS_ONE_SISTER",
        "AUTHOR_KNOWN_OUTCOME_NOT_EXTERNAL",
        "Despite Moon aspects, Lilly reports this merchant had one sister.",
    ),
    (
        751,
        "SOURCE_ADMITS_COUNTING_DIFFICULT",
        "EXPLICIT_METHOD_LIMITATION",
        "Lilly explicitly says the number of brothers and sisters is very difficult to judge from an elder brother's nativity.",
    ),
    (
        751,
        "MARS_ACCIDENTAL_STRENGTH",
        "CONDITIONAL_ASTRO_RULE",
        "Mars strength, Saturn's square and sextiles to Sun Venus Mercury are considered for sibling fate.",
    ),
    (
        751,
        "SOME_BROTHERS_DIE_YOUNG_CLAIM",
        "HISTORICAL_MORTALITY_PROGNOSIS_UNVERIFIED",
        "Source conjectures some brothers will not reach adulthood; no independently checked biographies.",
    ),
    (
        751,
        "OTHER_BROTHERS_GOOD_STANDING",
        "HISTORICAL_STATUS_PROGNOSIS_UNVERIFIED",
        "Source conjectures other brothers will retain good social rank or standing.",
    ),
    (
        751,
        "SISTER_SICKLY_SHORTER_LIFE",
        "HISTORICAL_HEALTH_PROGNOSIS_UNVERIFIED",
        "From Moon near Oculus Taurus and its Mars aspect, source predicts illness and shorter life for sister.",
    ),
    (
        752,
        "UNITY_SUBHEADING",
        "SECTION_BOUNDARY",
        "Unnumbered Unity subsection begins at top of printed752, still part of CLXXVIII.",
    ),
    (
        752,
        "SATURN_MARS_FUTURE_DISCORD",
        "HISTORICAL_RELATIONSHIP_PROGNOSIS_UNVERIFIED",
        "Saturn–Mars square is linked to future sibling enmity and discord.",
    ),
    (
        752,
        "MARS_SEVENTH_OPPOSES_ASCENDANT",
        "CONDITIONAL_ASTRO_RULE",
        "Mars in seventh opposite the ascendant is presented as a conflict signifier.",
    ),
    (
        752,
        "WOMEN_MERCHANDISE_CONTRACT_CONFLICT",
        "HISTORICAL_RELATIONSHIP_PROGNOSIS_UNVERIFIED",
        "Possible sibling disputes are attributed to women, trade, contracts and bargains.",
    ),
    (
        752,
        "SUN_EIGHTH_HOUSE_LEGACY",
        "CONDITIONAL_ASTRO_RULE",
        "The Sun as dispositor of Mars and lord of eighth is linked to legacies, land or gifts of the dead.",
    ),
    (
        752,
        "DERIVATIVE_HOUSE_UNCLE_CONTEXT",
        "CONDITIONAL_ASTRO_RULE",
        "Seventh as second from sixth, with sixth described as uncles/father's kindred, frames a cousin/uncle inheritance context.",
    ),
    (
        752,
        "UNCLES_ESTATE_FUTURE_CONTROVERSY",
        "HISTORICAL_LEGAL_PROGNOSIS_UNVERIFIED",
        "Lilly speculates about controversy between the merchant and a brother over an uncle's estate.",
    ),
    (
        752,
        "CLXXIX_PARENTS_BOUNDARY",
        "NEXT_SOURCE_BOUNDARY",
        "Original CLXXVIII ends above the fourth-house divider; distinct CHAP CLXXIX Of Parents begins on printed752.",
    ),
]
assert len(ITEMS) == 22
records = []
for i, (folio, role, layer, summary) in enumerate(ITEMS):
    photo = photorecord[str(folio)]
    records.append(
        {
            "id": f"R{12970 + i}",
            "record_number": 12970 + i,
            "batch": "B07ba",
            "original_printed_folio": folio,
            "original_pdf_frames": [folio + 34],
            "original_second_edition_DjVu_frame": folio + 29,
            "source_span": f"B07ba-S{folio - 750:03d}",
            "role": role,
            "historical_evidence_type": layer,
            "source_non_diplomatic_locator": role.lower().replace("_", " "),
            "source_historical_interpretation": summary,
            "original_1647_image_sha256": photo["first_1647"]["sha256"],
            "original_1659_image_sha256": photo["typeset_1659"]["sha256"],
            "natal_case_was_known_to_Lilly": True,
            "author_statement_about_siblings_not_externally_correlated": True,
            "source_prospective_prediction_frozen_before_human_outcomes": False,
            "historical_person_biography_verified_independently": False,
            "this_is_heldout_real_person_prediction_accuracy": False,
            "source_independent_expert_textual_critical_review_complete": False,
            "high_stakes_health_lifespan_or_relationship_risk_advice_authorized": False,
            "runtime_model_promoted": False,
        }
    )
assert records[0]["id"] == "R12970" and records[-1]["id"] == "R12991"
assert records[-1]["role"] == "CLXXIX_PARENTS_BOUNDARY"
source = {
    "schema": "LILLY_1647_1659_CLXXVIII_BRETHREN_SOURCE_22_NOTES_V1",
    "batch": "B07ba",
    "full_original_1647_Wellcome_pdf_SHA256": WHOLE,
    "source_original_chapter": "CLXXVIII Of BRETHREN",
    "original_physical_first_edition_printed_folios": [751, 752],
    "original_first_PDF_frames": [785, 786],
    "independent_1659_print_DjVu_frames": [780, 781],
    "original_two_editions_four_source_page_images": photorecord,
    "source_author_reports_sibling_count_brothers": 7,
    "source_author_reports_sibling_count_sisters": 1,
    "source_strict_ptolemy_interpretation_predicts_few_siblings": True,
    "source_known_seven_brothers_context_posthoc_reconciled_with_extra_factors": True,
    "source_explicitly_warns_exact_sibling_counts_difficult": True,
    "source_reports_not_independently_1847_or_1616_family_verified": True,
    "reported_sibling_count_independent_validation_count": 0,
    "sister_health_mortality_claims_independently_verified": 0,
    "sibling_estate_disputes_independently_verified": 0,
    "source_next_distinct_CLXXIX_parents_begins_same_final_printed752": True,
    "historical_natal_chart_engine_verified": False,
    "independent_expert_original_text_collation_complete": False,
    "independent_prospective_real_human_prediction_successes": 0,
    "runtime_promotions": 0,
    "record_count": len(records),
    "first_record": "R12970",
    "last_record": "R12991",
    "next_record": "R12992",
    "next_original_PDF_frame": 786,
    "next_printed_folio": 752,
    "records": records,
}
save(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json", source)
rules = {
    "batch": "B07ba",
    "status": "LILLY_ORIGINAL_CLXXVIII_BRETHREN_DOCUMENTARY_SOURCE_NOT_EMPIRICAL",
    "record_count": 22,
    "first_record": "R12970",
    "last_record": "R12991",
    "source_groups": 2,
    "body_pdf_frames": [785, 786],
    "original_physical_CHAP_CLXXVIII_source_span_documented": True,
    "author_initial_sibling_count_doctrine_counterclaim_retained": True,
    "author_retrospective_seven_brother_one_sister_report_not_external_validation": True,
    "all_health_and_family_prognoses_unverified": True,
    "real_human_blind_prediction_successes": 0,
    "runtime_promotions": 0,
    "rules": records,
}
save(B / "RULES.json", rules)
accept = {
    "batch": "B07ba",
    "prior_Lilly": 12969,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "historical_source_note_count": 22,
    "Lilly_after_if_accepted": 12991,
    "Western_after_if_accepted": 14057,
    "next_R": "R12992",
    "next_original_pdf": 786,
    "next_printed_folio": 752,
    "next_original_physically_distinct_chapter": "CLXXIX",
    "physical_CLXXVIII_source_span_complete": True,
    "historical_source_known_case_not_Blind": True,
    "source_counts_7_brothers_1_sister_reported_not_verified": True,
    "person_level_family_health_or_legal_outcomes_validated": 0,
    "original_1616_chart_ephemeris_validated": False,
    "source_notes_sha256": sha(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "notes": 22,
            "first": "R12970",
            "last": "R12991",
            "next": "R12992",
            "author_reported_brothers": 7,
            "author_reported_sisters": 1,
            "source_count_was_outcome_blinded": False,
            "source_notes_SHA256": accept["source_notes_sha256"],
            "rules_SHA256": accept["rules_sha256"],
        },
        indent=2,
    )
)
