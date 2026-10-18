# ruff: noqa: E501  # The historical claim evidence includes long, verbatim-locator descriptions.
"""Reproducible natal-source → observed-domain → questionnaire coverage matrix.

Inputs are versioned historical source inventories, with the two Lilly
snapshots copied byte-identically from exact separate research commits.
This is a DOMAIN AUDIT, never a validated astrological prediction rule.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
INPUTS = TASK / "input-snapshots"
OUT = TASK / "SOURCE-TO-SURVEY-CROSSWALK-v2.json"
PLANET_OUT = TASK / "CF003-PLANET-MAPPING-GAPS-v1.json"
EXPECTED_SNAPSHOTS = {
    "LILLY3-NATAL-DOMAIN-CENSUS-v1.json": {
        "sha256": "0e62ce02d703fff539603b2e8342ee945054a471edc93331d32d8759a94bef37",
        "commit": "e26338838c757ef2450edacedf7854b3b97f98a9",
        "rows": 29,
        "source_status": "CONTENTS_ONLY_NOT_RULE_LEVEL_OR_PREDICTIVE_VALIDATION",
    },
    "LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json": {
        "sha256": "9de2eaaae83c528f56adcf999a3263af21f0775f29f0f8741965fbe0daad8e91",
        "commit": "61781f3fab2b9587635aa686ee90e61384c641c8",
        "rows": 31,
        "source_status": "SOURCE_TWIN_WITNESS_TEXT_AUDIT_FACSIMILE_SYMBOLS_NOT_YET_ADJUDICATED",
    },
}
TOC_DOMAINS = [
    "natal_technical_preconditions",  # 001 Trutine, rectification
    "natal_technical_preconditions",
    "high_stakes_health_death_confinement",
    "natal_technical_preconditions",
    "physical_vitality_appearance",
    "personality_emotional_temperament",
    "cognitive_style_and_learning",
    "physical_vitality_appearance",
    "overall_life_circumstances",
    "actual_finances_resources",
    "kinship_siblings",
    "parents_home_roots",
    "high_stakes_health_death_confinement",
    "historical_servitude_livestock",
    "actual_marriage_partnership_history",
    "parenthood_caregiving",
    "actual_foreign_travel_migration",
    "religious_spiritual_disposition",
    "dream_content_and_tone",
    "actual_public_rank_and_recognition",
    "actual_occupation_and_vocation",
    "friendship_conflict_longterm",
    "friendship_conflict_longterm",
    "high_stakes_health_death_confinement",
    "high_stakes_health_death_confinement",
    "natal_timing_techniques",
    "natal_timing_techniques",
    "natal_timing_techniques",
    "natal_timing_techniques",
]
PT3_DOMAINS = {
    "PT-MIND-REASON": "cognitive_style_and_learning",
    "PT-MYSTERY-INTEREST": "esoteric_interests_omens_divination",
    "PT-OMENS": "esoteric_interests_omens_divination",
    "PT-DREAM-INTERPRET": "dream_interpretation_and_beliefs",
    "PT-RELIGIOUS-OBSERVANCE": "spiritual_or_ritual_practice",
    "PT-JUPITER-DEVOTION": "religious_spiritual_disposition",
    "PT-JUPITER-MERCURY-PHILOSOPHY": "philosophical_scientific_curiosity",
    "PT-VENUS-DREAM-TONE": "dream_content_and_tone",
    "PT-VENUS-ART": "creative_production",
    "PT-MUSIC": "aesthetic_music_engagement",
    "PT-REVISION-VERSATILITY": "opinion_revision_and_flexibility",
    "PT-NATURE-INQUIRY": "philosophical_scientific_curiosity",
    "PT-RELIGIOUS-SIGNS": "religious_spiritual_disposition",
    "LILLY-NINTH-RELIGION": "religious_spiritual_disposition",
    "LILLY-NINTH-DREAMS": "dream_content_and_tone",
    "LILLY-JUPITER-NINTH": "religious_spiritual_disposition",
    "LILLY-TENTH-WORK": "actual_occupation_and_vocation",
}
PT4_DOMAINS = {
    "actual_financial_fortune": "actual_finances_resources",
    "actual_status_esteem_public_rank": "actual_public_rank_and_recognition",
    "real_occupation_vocation_mystery_professions": "actual_occupation_and_vocation",
    "marriage_history_and_pair_outcomes": "actual_marriage_partnership_history",
    "children_parenthood_and_family": "parenthood_caregiving",
    "lasting_friendship_conflict_life_history": "friendship_conflict_longterm",
    "real_foreign_travel_and_relations_abroad": "actual_foreign_travel_migration",
    "mortality_cause_and_medical_risk": "high_stakes_health_death_confinement",
    "event_timing_and_life_phases": "actual_life_turning_points",
}
RELIGION_CHANGE = {1, 14, 16, 17, 18}
RELIGION_PRACTICE = {2, 6, 8, 9, 11}
RELIGION_DIVINATION = {7, 12}


def load_json(file: Path) -> dict[str, Any]:
    data = json.loads(file.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def source_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    census = load_json(INPUTS / "LILLY3-NATAL-DOMAIN-CENSUS-v1.json")
    religion = load_json(INPUTS / "LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json")
    for filename, settings in EXPECTED_SNAPSHOTS.items():
        raw = (INPUTS / filename).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == settings["sha256"]
        doc = census if filename.startswith("LILLY3-") else religion
        assert len(doc["records"]) == settings["rows"]
        assert doc["status"] == settings["source_status"]
    ptolemy = load_json(
        ROOT / "tasks/astrology-phenomenology-source-anchors-20261017/"
        "PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json"
    )
    book4 = load_json(
        ROOT / "tasks/astrology-phenomenology-source-anchors-20261017/"
        "PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json"
    )
    assert len(ptolemy["claim_anchors"]) == 17
    assert len(book4["domains"]) == 9
    return census, religion, ptolemy, book4


def domains() -> list[dict[str, Any]]:
    with (TASK / "DOMAIN-REGISTRY-SOURCE.psv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="|"))
    actual_v7 = {
        q["id"]
        for q in load_json(
            ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"
        )["questions"]
    }
    actual_tf1 = {
        q["id"]
        for q in load_json(
            ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
        )["questions"]
    }
    em_ids = {
        item["id"]
        for item in load_json(
            ROOT / "apps/life-patterns-participant/participant/static/experience-meaning-v2.json"
        )["items"]
    }
    options = {
        q["id"] for q in load_json(TASK / "ADAPTIVE-QUESTION-CANDIDATES-v1.json")["questions"]
    }
    result = []
    for row in rows:
        links = [s for s in row["nearest_previous_questions"].split(",") if s]
        em = [s for s in row["em_direct"].split(",") if s]
        new = [s for s in row["optional_questions"].split(",") if s]
        assert set(em) <= em_ids, row
        assert set(new) <= options, row
        for link in links:
            assert link in actual_tf1 if link.startswith("TF1-") else link in actual_v7, link
        assert row["kind"]
        assert row["v7_status"] in {"direct", "partial", "proxy_only", "absent", "outside_scope"}
        assert row["tf1_status"] in {"direct", "partial", "proxy_only", "absent", "outside_scope"}
        result.append(
            {
                "domain_id": row["domain_id"],
                "label": row["label"],
                "outcome_kind": row["kind"],
                "v7_questionnaire_coverage": row["v7_status"],
                "tf1_questionnaire_coverage": row["tf1_status"],
                "em_v2_direct_question_ids": em,
                "optional_future_question_ids": new,
                "related_existing_questions_not_necessarily_direct": links,
                "interpretation_limit": row["interpretation_limit"],
                "historical_source_claim_ids": [],
                "historically_attested_in_this_snapshot": False,
            }
        )
    assert len(result) == len({r["domain_id"] for r in result})
    assert em_ids == set.union(*(set(r["em_v2_direct_question_ids"]) for r in result))
    assert options == set.union(*(set(r["optional_future_question_ids"]) for r in result))
    return result


def assemble() -> dict[str, Any]:
    census, lilly, ptolemy, book4 = source_inputs()
    domain_rows = domains()
    by_domain = {row["domain_id"]: row for row in domain_rows}
    claims = []
    seen: set[str] = set()

    def append(row: dict[str, Any]) -> None:
        claim_id = row["claim_id"]
        domain_id = row["domain_id"]
        assert claim_id not in seen, claim_id
        assert domain_id in by_domain, domain_id
        assert not row["prediction_validated"]
        seen.add(claim_id)
        claims.append(row)
        by_domain[domain_id]["historical_source_claim_ids"].append(claim_id)
        by_domain[domain_id]["historically_attested_in_this_snapshot"] = True

    for i, item in enumerate(census["records"]):
        assert item["id"] == f"L3-TOC-{i + 1:03}"
        append(
            {
                "claim_id": item["id"],
                "domain_id": TOC_DOMAINS[i],
                "source_type": "lilly_book3_1647_natal_contents",
                "evidence_level": "contents_heading_only",
                "historical_subject_paraphrase": item["topic_for_source_inventory_only"],
                "source_locator": f"printed p. {item['printed_pages_from_contents']} (OCR contents estimate)",
                "source_condition": None,
                "prediction_validated": False,
                "source_caution": "Table of contents: NOT original rule predicates.",
            }
        )
    assert len(TOC_DOMAINS) == 29
    for entry in lilly["records"]:
        eid = entry["id"]
        if eid.startswith("LILLY3-R"):
            n = int(eid[-2:])
            if n == 20:
                domain_id = "interpretive_freedom_and_non_determinism"
            elif n in RELIGION_CHANGE:
                domain_id = "belief_conversion_or_worldview_change"
            elif n in RELIGION_PRACTICE:
                domain_id = "spiritual_or_ritual_practice"
            elif n in RELIGION_DIVINATION:
                domain_id = "esoteric_interests_omens_divination"
            else:
                domain_id = "religious_spiritual_disposition"
        elif eid.startswith("LILLY3-D"):
            domain_id = (
                "dream_interpretation_and_beliefs"
                if int(eid[-2:]) <= 4
                else "dream_content_and_tone"
            )
        else:
            raise AssertionError(eid)
        append(
            {
                "claim_id": eid,
                "domain_id": domain_id,
                "source_type": "lilly_book3_1647_religion_dreams",
                "evidence_level": "original_OCR_plus_retyped_witness_glyphs_pending_v1",
                "historical_subject_paraphrase": entry["traditional_assertion"],
                "source_locator": f"Book III {entry['chapter']} printed p.{entry['original_printed_page']}",
                "source_condition": entry["chart_condition"],
                "prediction_validated": False,
                "source_caution": "Historical evaluative vocabulary is not endorsed; symbols unresolved in this exact committed v1.",
            }
        )
    for entry in ptolemy["claim_anchors"]:
        eid = entry["id"]
        assert eid in PT3_DOMAINS, eid
        source_kind = (
            "ptolemy_book3_natal_soul_quality"
            if eid.startswith("PT-")
            else "lilly_house_topic_horary_intro"
        )
        append(
            {
                "claim_id": eid,
                "domain_id": PT3_DOMAINS[eid],
                "source_type": source_kind,
                "evidence_level": (
                    "passage_anchored_natal"
                    if eid.startswith("PT-")
                    else "house_topic_only_nonnatal"
                ),
                "historical_subject_paraphrase": entry["source_claim_paraphrase"],
                "source_locator": entry["section_locator"],
                "source_condition": entry["traditional_chart_condition_or_topic"],
                "prediction_validated": False,
                "source_caution": "Source report, not a quantitatively validated modern measure.",
            }
        )
    assert len(PT3_DOMAINS) == 17
    for entry in book4["domains"]:
        domain_id = PT4_DOMAINS[entry["domain"]]
        append(
            {
                "claim_id": "PT-IV-" + entry["chapter"].split(".")[1].zfill(2),
                "domain_id": domain_id,
                "source_type": "ptolemy_book4_natal_life_topic",
                "evidence_level": "chapter_level_life_domain_summary",
                "historical_subject_paraphrase": entry["claim_summary"],
                "source_locator": "Tetrabiblos " + entry["chapter"],
                "source_condition": None,
                "prediction_validated": False,
                "source_caution": "Chapter domain, not full literal conditional horoscope algorithm.",
            }
        )
    for claim_id, domain_id, chapter_page, synopsis, condition in [
        (
            "PT-III-MARS-VENUS-PLAY",
            "play_humor_spontaneous_enjoyment",
            "Tetrabiblos Book III.13, printed p.355",
            "In one qualified Mars with Venus configuration, Ptolemy depicts play, cheerfulness, dancing and artistic pursuits.",
            "Mars with Venus in honorable positions; counterconditions also stated.",
        ),
        (
            "PT-III-MARS-ACTION",
            "motivation_action_initiation",
            "Tetrabiblos Book III.13, printed p.353",
            "Ptolemy describes martial spirit, initiative, assertiveness and force under one Mars-dominant configuration.",
            "Mars alone dominating the soul in honorable position; contrasts with opposite positions.",
        ),
    ]:
        append(
            {
                "claim_id": claim_id,
                "domain_id": domain_id,
                "source_type": "ptolemy_book3_natal_soul_quality",
                "evidence_level": "new_direct_primary_passage_check",
                "historical_subject_paraphrase": synopsis,
                "source_locator": chapter_page,
                "source_condition": condition,
                "prediction_validated": False,
                "source_url": "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/3D%2A.html",
                "source_caution": "Historically asserted character tendency, never modern frequency or validity proof.",
            }
        )

    # Source-scope extension: four verse-level conditions for ascetic paths.
    # This public rendering includes Sanskrit and secondary English translation,
    # with explicit unresolved readings; no independent Sanskrit edition adjudication.
    jyotish_verses = [
        (
            "BJ-15.1",
            "Four or more strong planets in one sign are linked to named ascetic paths, with qualification for falling away.",
            "A multi-planet strength conjunction and its qualified cancellation.",
        ),
        (
            "BJ-15.2",
            "Planetary combustion or defeat is described as qualifying formal initiation or continued devotion.",
            "Sun rays or defeated/aspected planets; online translator explicitly calls readings uncertain.",
        ),
        (
            "BJ-15.3",
            "Initiation is discussed with Saturn's aspects, Moon-sign ruler and lunar divisional placements.",
            "Saturn with the Moon-sign lord, or Moon divisional placements and Saturn aspects.",
        ),
        (
            "BJ-15.4",
            "A ninth-house and Raja Yoga combination is linked to a spiritual leader or ruler entering religious initiation.",
            "Ninth house Jupiter or Saturn combined with lunar, ascendant and Saturn relationships.",
        ),
    ]
    for claim_id, synopsis, condition in jyotish_verses:
        append(
            {
                "claim_id": claim_id,
                "domain_id": "ascetic_renunciation_and_initiation",
                "source_type": "brihat_jataka_ch15_natal_yoga",
                "evidence_level": "online_secondary_translation_with_sanskrit_verse",
                "historical_subject_paraphrase": synopsis,
                "source_locator": f"Varahamihira Brhat Jataka Chapter XV verse {claim_id.split('.')[1]}",
                "source_condition": condition,
                "source_url": "https://vedicpupil.in/library/books/brihat-jataka/chapter-15",
                "source_caution": (
                    "Online Sanskrit + translator exposition, some readings uncertain; "
                    "not original manuscript verification or empirical chart validation."
                ),
                "prediction_validated": False,
            }
        )

    assert len(claims) == 29 + 31 + 17 + 9 + 2 + 4, len(claims)
    assert all(by_domain[r["domain_id"]]["historically_attested_in_this_snapshot"] for r in claims)
    survey_stat = Counter()
    for row in domain_rows:
        survey_stat[row["v7_questionnaire_coverage"]] += 1
    registry_status = {
        "all_historical_claim_ids_accounted_for": len(claims),
        "unique_domain_ids": len(domain_rows),
        "historically_attested_domains": sum(
            x["historically_attested_in_this_snapshot"] for x in domain_rows
        ),
        "domains_only_modern_extrapolation": sum(
            not x["historically_attested_in_this_snapshot"] for x in domain_rows
        ),
        "survey_v7_domain_counts": dict(survey_stat),
        "all_em8_ids_covered": True,
        "candidate_questions_grounded_to_one_or_more_domains": True,
        "predictive_accuracy_established": False,
    }
    return {
        "schema": "life-patterns-source-first-chart-domain-audit-v2",
        "status": "HISTORICAL_CLAIMS_AND_SURVEY_COVERAGE_ONLY_NOT_PREDICTION_VALIDATION",
        "audit_date": "2026-10-18",
        "owner_issue": (
            "Comprehensive audit of historical chart claims versus existing actual "
            "questionnaire domains, after earlier survey-first promise was not completed."
        ),
        "source_types_and_limits": {
            "ptolemy_book3_natal_soul_quality": "13 claims already source-anchored + two new direct checked conditions",
            "lilly_house_topic_horary_intro": "4 subject headings, not natal horoscope rules",
            "ptolemy_book4_natal_life_topic": "9 chapter topics, no full calculation or prospectively tested natal rules",
            "lilly_book3_1647_natal_contents": "29 original contents topics only",
            "lilly_book3_1647_religion_dreams": "31 source candidate rules, glyph uncertainty in pinned committed v1",
            "brihat_jataka_ch15_natal_yoga": (
                "4 verse-level natal conditions from online Sanskrit/English rendering; "
                "translation ambiguities, not manuscript-verified"
            ),
        },
        "pinned_external_lilly_snapshot_provenance": EXPECTED_SNAPSHOTS,
        "accepted_local_source_paths": [
            "tasks/astrology-phenomenology-source-anchors-20261017/PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json",
            "tasks/astrology-phenomenology-source-anchors-20261017/PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json",
        ],
        "surveys_compared": {
            "v7_route_count": 79,
            "tendency_first_v1_direct_question_count": 25,
            "experience_meaning_v2_question_count": 8,
            "cf003_addendum_questions": 3,
            "role_entry_v33": "small optional role inventory only",
            "idiographic_unusual_behavior_v3": "free self-reported unique behaviors; not automatic chart prediction",
        },
        "denominator_cautions": [
            "Number of source records is not a count of distinct astrological rules or validated testable hypotheses.",
            "A documented house topic does not prove a natal calculation predicts that topic.",
            "Direct questionnaire sampling does not establish validity, respondent coverage, or independent astrology predictions.",
            "Missing psych constructs are not necessarily missing claims in every astrology system.",
            "This is not exhaustive for Hellenistic, Jyotish, Dariot or modern astrology.",
        ],
        "counts": registry_status,
        "domains": domain_rows,
        "historical_source_claims": claims,
    }


def planet_audit(crosswalk: dict[str, Any]) -> dict[str, Any]:
    plan = load_json(ROOT / "reference/empirical_astrology/cf003_behavioral_planet_map_v0.json")
    assert len(plan["mapping"]) == 10
    mapping = {
        "venus": (
            "semantic_narrowing_or_divergence",
            "PT-VENUS-ART;PT-VENUS-DREAM-TONE",
            "Historical Venus passages address art/beauty/pleasure as well as social relations, unlike an exclusive ethics/boundaries target.",
        ),
        "pluto": (
            "not_derived_from_checked_classical_seven_planet_texts",
            "",
            "Modern Pluto is not a planet in the original Ptolemy/Lilly seven-planet clauses checked; separate modern rule source required.",
        ),
        "moon": (
            "different_construct_emphasis",
            "PT-MIND-REASON",
            "Ptolemy chiefly assigns the Moon sensory/affective soul qualities here, not a single recurring motive or action-pressure scale.",
        ),
        "saturn": (
            "partial_adjacent_not_conditionally_equivalent",
            "PT-MIND-REASON",
            "Duty/discipline has adjacent character vocabulary, but Saturn natal judgments depend on dignity/aspects and cannot be reduced to role labels.",
        ),
        "sun": (
            "partial_adjacent_not_conditionally_equivalent",
            "PT-IV-03",
            "Solar/luminary public dignity claims are not identical to inner self-expression or feeling central.",
        ),
        "uranus": (
            "not_derived_from_checked_classical_seven_planet_texts",
            "",
            "Uranus is outside these 1647 and ancient seven-planet natal predicates. This does not reject later modern Uranus astrology.",
        ),
        "mercury": (
            "semantic_narrowing",
            "PT-MIND-REASON;PT-NATURE-INQUIRY",
            "Ptolemy emphasizes reason, mind, speculation, inquiry and invention; an expression/communication target captures only a subset.",
        ),
        "jupiter": (
            "semantic_divergence_with_overlap",
            "PT-JUPITER-DEVOTION;PT-JUPITER-MERCURY-PHILOSOPHY",
            "Religious conviction, generosity and philosophical inquiry are only partly mirrored in the project growth/expansion role.",
        ),
        "mars": (
            "partial_overlap_missing_configuration",
            "PT-III-MARS-ACTION;PT-III-MARS-VENUS-PLAY",
            "Historical Mars assertion/action overlaps the role, but joint Mars–Venus playfulness cannot be assigned to Mars alone.",
        ),
        "neptune": (
            "not_derived_from_checked_classical_seven_planet_texts",
            "",
            "Neptune spirituality/mystery construct is not an ancient or Lilly original seven-planet natal rule; conditional sources needed.",
        ),
    }
    rows = []
    ids = {claim["claim_id"] for claim in crosswalk["historical_source_claims"]}
    for target in plan["mapping"]:
        planet = target["planet"].lower()
        relation, supporting, note = mapping[planet]
        anchors = [item for item in supporting.split(";") if item]
        assert set(anchors) <= ids
        rows.append(
            {
                "construct_id": target["construct_id"],
                "planet": planet,
                "existing_mapping_role": target.get("existing_chart_blind_role_text"),
                "actual_development_contract": target["target_contract_definition"],
                "source_lineage": "project Human Design role meaning; CF003 development proxy is not a classical natal meaning table",
                "relationship_to_checked_classical_sources": relation,
                "historical_claim_ids": anchors,
                "limitation": note,
                "translation_into_computational_natal_rule_admitted": False,
                "new_predictive_weight_or_score": None,
            }
        )
    assert {x["planet"] for x in rows} == set(mapping)
    return {
        "schema": "life-patterns-cf003-planet-role-vs-classical-natal-source-audit-v1",
        "status": "SOURCE_FIDELITY_COMPARISON_NOT_ASTROLOGY_REJECTION_OR_REPLACEMENT_MODEL",
        "source_model": "reference/empirical_astrology/cf003_behavioral_planet_map_v0.json",
        "source_claim_crosswalk": OUT.name,
        "source_status": plan["status"],
        "counts": {
            "existing_mappings_checked": len(rows),
            "classical_natal_predicates_replaced": 0,
            "out_of_checked_seven_planet_source": sum(
                r["relationship_to_checked_classical_sources"]
                == "not_derived_from_checked_classical_seven_planet_texts"
                for r in rows
            ),
            "astrology_predictive_validation_results": 0,
        },
        "mechanical_mismatch": (
            "Ancient and Lilly source claims can be conditional chains involving Moon and "
            "Mercury, ninth-house rulerships, dignity, angles, Lot of Fortune, aspects "
            "and combinations; a ten single-planet role label cannot stand in for these "
            "natal predicates. Do not treat the mismatch as proof of false astrology."
        ),
        "rows": rows,
        "owner_outcome": (
            "Replace missing source-to-question mappings as a future independently "
            "frozen hypothesis lane; do not retroactively fit to participant responses."
        ),
    }


def write(path: Path, doc: dict[str, Any]) -> None:
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    crosswalk = assemble()
    write(OUT, crosswalk)
    planets = planet_audit(crosswalk)
    write(PLANET_OUT, planets)
    print(
        json.dumps(
            {
                "crosswalk": OUT.name,
                "historical_source_rows": len(crosswalk["historical_source_claims"]),
                "distinct_domains": len(crosswalk["domains"]),
                "v7_coverage_counts": crosswalk["counts"]["survey_v7_domain_counts"],
                "planet_mapping_rows": len(planets["rows"]),
                "modern_extrapolated_domains": crosswalk["counts"][
                    "domains_only_modern_extrapolation"
                ],
            }
        )
    )
