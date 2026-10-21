#!/usr/bin/env python3
"""Draft historical-source dependency graph and synthetic chart coverage.

Source-anchored preliminary construct dependencies, not a completed
astrological interpretation, calibrated scoring rule or human test.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
L = (
    ROOT
    / "tasks"
    / "astro-ziwei-behavioral-original-lexemes-20261021"
    / "ZIWEI_LIFE_BEHAVIORAL_LEXEME_OVERLAP_SOURCE_AUDIT_V1.json"
)
C = (
    ROOT
    / "tasks"
    / "astro-ziwei-colocation-source-20261021"
    / "ORIGINAL_FOUR_BEHAVIOR_STAR_COLOCATION_SOURCE_AUDIT_V1.json"
)
READY = ROOT / "tasks/astro-blind-readiness-20261020/READINESS_GATES_V1.json"
LEX_SHA = "d6a89b93b5c4388c7ad993257e4a2c16a00f1f702bab6bc174b7124873cea978"
COL_SHA = "584fb2244a79ae409fda6d32ef0062fc4a5fbb02983c340bfc112ee6d4c6b52c"
READY_SHA = "60dd789bb8455b72116c876d49600e8f46b9ed53d55237c28ab87579ab677958"
ORACLE_COMMIT = "6f4a75febc1624e44b54d724422804a05f31fd12"
ORACLE_FILE = (
    "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12/"
    "IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json"
)
ORACLE_SHA = "01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5"
COLD_ORACLE = B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"
OUTPUT = B / "FOUR_ZIWEI_SOURCE_CONSTRUCT_DEPENDENCY_DRAFT_V1.json"
MAIN = {
    "decision_commitment": {"WuQu"},
    "contentious_disagreement": {"LianZhen"},
    "voluntary_helping": {"TianLiang"},
    "competitive_striving": {"PoJun"},
}
EXTENDED = {k: set(v) for k, v in MAIN.items()}
EXTENDED["voluntary_helping"].add("TaiYang")
CLASSES = {
    ("果决", "WuQu"): (
        "decision_commitment",
        "MAIN_STAR_INTRO_LEXICAL_CANDIDATE",
        "MAIN_STAR_POSITION_CALCULABLE",
    ),
    ("果决", "WenQu"): (
        "decision_commitment",
        "AUXILIARY_CONDITIONAL_CO_PRESENT_STARS",
        "AUXILIARY_PLACEMENT_NOT_VERIFIED",
    ),
    ("果决", "QingYang"): (
        "decision_commitment",
        "AUXILIARY_INTRO_WITH_DIGNITY_CONTEXT_RAW_ONLY",
        "AUXILIARY_PLACEMENT_NOT_VERIFIED",
    ),
    ("好济施", "TaiYang"): (
        "voluntary_helping",
        "MAIN_STAR_INTRO_WITH_DAY_TEMPLE_CONTEXT",
        "MAIN_STAR_POSITION_CALCULABLE_BUT_CONTEXT_UNRESOLVED",
    ),
    ("好济施", "TianLiang"): (
        "voluntary_helping",
        "MAIN_STAR_INTRO_LEXICAL_CANDIDATE",
        "MAIN_STAR_POSITION_CALCULABLE",
    ),
    ("好施济", "YouBi"): (
        "RELATED_GIVING_WORDING_NOT_EQUIVALENT_YET",
        "AUXILIARY_SIMILAR_WORD_ORDER_NOT_VERIFIED_SYNONYM",
        "AUXILIARY_PLACEMENT_NOT_VERIFIED",
    ),
    ("好忿争", "LianZhen"): (
        "contentious_disagreement",
        "MAIN_STAR_INTRO_LEXICAL_CANDIDATE",
        "MAIN_STAR_POSITION_CALCULABLE",
    ),
    ("是非日有", "LianZhen"): (
        "contentious_disagreement",
        "AUXILIARY_QINGYANG_COLOCATION_REQUIRED",
        "AUXILIARY_PLACEMENT_NOT_VERIFIED",
    ),
    ("好争强", "PoJun"): (
        "competitive_striving",
        "MAIN_STAR_INTRO_LEXICAL_CANDIDATE",
        "MAIN_STAR_POSITION_CALCULABLE",
    ),
    ("争斗疾病", "PoJun"): (
        "HISTORICAL_FIGHTING_AND_ILLNESS_NOT_QUESTIONNAIRE_TARGET",
        "MULTISTAR_MALEFIC_FALLEN_HOUSE_HISTORICAL_MEDICAL_CLAIM",
        "MULTIFACTOR_NOT_VERIFIED",
    ),
    ("好勇斗狠", "QingYang"): (
        "HISTORICAL_AGGRESSION_NOT_COMPETITION_TARGET",
        "AGGRESSION_WORDING_NOT_EQUIVALENT_TO_COMPETITION",
        "AUXILIARY_PLACEMENT_NOT_VERIFIED",
    ),
}
DEPENDENCIES = [
    (
        "TaiYang",
        "TianLiang",
        "voluntary_helping",
        "EXACT_IDENTICAL_CHINESE_PHRASE",
        "same helping claim not two independent questionnaire observations",
    ),
    (
        "WuQu",
        "WenQu",
        "decision_commitment",
        "SHARED_LEXICAL_ROOT_ONLY",
        "WenQu quote also requires co-present TianTong/TianLiang/WuQu and favourable palace",
    ),
    (
        "WuQu",
        "QingYang",
        "decision_commitment",
        "SHARED_LEXICAL_ROOT_ONLY",
        "QingYang temple context, auxiliary engine not ready and historical RAW note only",
    ),
    (
        "LianZhen",
        "QingYang",
        "contentious_disagreement",
        "EXPLICIT_AUXILIARY_CONDITIONAL",
        "daily dispute claim needs QingYang, no standalone probability",
    ),
    (
        "PoJun",
        "LianZhen",
        "contentious_disagreement",
        "ADVERSE_MULTI_STAR_CLUSTER_NOT_SIMPLE_PAIR",
        "fallen house with QingYang/TuoLuo/HuoLing and illness phrase; no medical truth",
    ),
]


def sha(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(s: str) -> None:
    raise ValueError("Four-source-construct dependency model draft rejected: " + s)


def load(path: Path, checksum: str) -> dict:
    if not path.is_file() or sha(path.read_bytes()) != checksum:
        fail("accepted source or readiness document SHA drift " + str(path))
    return json.loads(path.read_text(encoding="utf-8"))


def get_data():
    lex = load(L, LEX_SHA)
    coloc = load(C, COL_SHA)
    readiness = load(READY, READY_SHA)
    if (
        lex["human_forward_reverse_validations"] != 0
        or coloc["human_predictive_validations"] != 0
        or readiness["source_provenance"]["independent_real_human_predictive_validations"] != 0
    ):
        fail("source-stage data falsely contains real human success")
    if (
        len(lex["verbatim_behavior_related_lexical_source_witnesses"]) != 11
        or coloc["original_15_grade_line_count"] != 15
        or coloc["original_7_multistar_conditional_cluster_line_count"] != 7
    ):
        fail("original lexical or colocation documentary source coverage changed")
    if (
        len(readiness["candidate_pilot_gates"]) != 10
        or readiness["pilot_eligibility"]["candidate_pilot_ready"] is not False
        or any(
            not p["blocking"] or p["status"] == "verified"
            for p in readiness["candidate_pilot_gates"]
        )
    ):
        fail("real human preregistered study readiness gates have been improperly promoted")
    return lex, coloc, readiness


def oracle_source():
    if COLD_ORACLE.is_file():
        raw = COLD_ORACLE.read_bytes()
    else:
        raw = subprocess.run(
            ["git", "show", f"{ORACLE_COMMIT}:{ORACLE_FILE}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    if len(raw) != 899155 or sha(raw) != ORACLE_SHA:
        fail("accepted synthetic 312 source chart evidence SHA incorrect")
    data = json.loads(raw)
    if len(data["all_312_case_records"]) != 312:
        fail("synthetic source comparator no longer contains 312 original comparison rows")
    return data


def source_claims(lex: dict) -> list[dict]:
    rows = []
    for r in lex["verbatim_behavior_related_lexical_source_witnesses"]:
        key = (r["verbatim_narrow_Chinese_phrase"], r["original_occurrence_source_star"])
        if key not in CLASSES:
            fail("original Chinese source assertion not in predeclared phrase+star context map")
        construct, classification, engine = CLASSES[key]
        if r["source_record_status"].startswith("RAW") and not (
            r["original_occurrence_source_star"] == "QingYang"
            and engine == "AUXILIARY_PLACEMENT_NOT_VERIFIED"
        ):
            fail("unaccepted original auxiliary source line promoted as approved")
        rows.append(
            {
                "source_phrase": key[0],
                "source_star": key[1],
                "tentative_behavioral_construct": construct,
                "verbatim_source_witness_id": r["source_id"],
                "original_Chinese_source_quote_sha256": r["original_full_context_line_sha256_UTF8"],
                "old_accepted_source_annotation_id": r[
                    "already_accepted_historical_source_annotation_id"
                ],
                "original_source_context_class": classification,
                "required_feature_engine_status": engine,
                "semantic_gloss_critical_translation_ready": False,
                "psycho_behavioral_effect_magnitude": None,
                "is_independent_questionnaire_predictive_score": False,
                "this_draft_claim_may_be_used_as_scored_human_prediction": False,
                "tentative_behavior_construct_wording_equivalence_validated": False,
                "clinical_moral_or_gendered_historical_claims_applicable_to_modern_people": False,
                "source_testable_human_hypothesis_frozen": False,
            }
        )
    if len(rows) != 11 or set((r["source_phrase"], r["source_star"]) for r in rows) != set(CLASSES):
        fail("source claims not mapped exactly once by phrase and original star")
    return rows


def dependency_edges() -> list[dict]:
    rows = [
        {
            "left_original_star": a,
            "right_original_star": b,
            "tentative_shared_construct": construct,
            "source_dependency_type": kind,
            "evidence_grade_limit": note,
            "human_trait_correlation_or_effect_size_quantified": False,
            "probabilities_may_be_added_as_independent_model_hits": False,
        }
        for a, b, construct, kind, note in DEPENDENCIES
    ]
    if len(rows) != 5:
        fail("five source-bound dependency cautions no longer fixed")
    return rows


def all_synthetic_chart_options(data: dict) -> dict:
    unique = {}
    for r in data["all_312_case_records"]:
        s = r["source_case"]
        key = (s["gregorian_reference_date"], s["hour_branch"])
        comparison = (s["life_palace"], tuple(sorted(s["star_palaces"].items())))
        if key in unique:
            if unique[key]["geometry"] != comparison:
                fail("source vendor duplicate changed natal geometry")
            unique[key]["all_vendor_match"] &= bool(r["match"])
        else:
            unique[key] = {"chart": s, "geometry": comparison, "all_vendor_match": bool(r["match"])}
    if len(unique) != 120:
        fail("accepted synthetics are not exactly 120 source chart layouts")
    result = Counter()
    sample = []
    for key, row in sorted(unique.items()):
        life = row["chart"]["life_palace"]
        found = {name for name, loc in row["chart"]["star_palaces"].items() if loc == life}
        oldselected = found & set.union(*MAIN.values())
        expanded = found & set.union(*EXTENDED.values())
        constructs = {construct for construct, stars in EXTENDED.items() if found & stars}
        four_main = bool(oldselected)
        five_main = bool(expanded)
        strict = len(found) == len(oldselected) == 1 and row["all_vendor_match"]
        result["synthetic_states"] += 1
        result["strict_sole_star_and_all_vendor_agreement"] += strict
        result["initial_four_main_star_presence"] += four_main
        result["extended_five_main_star_presence"] += five_main
        result["new_states_due_sole_TaiYang_extension"] += five_main and not four_main
        result["two_distinct_target_constructs"] += len(constructs) == 2
        result["number_of_constructs_" + str(len(constructs))] += 1
        result["two_helping_stars_TaiYang_and_TianLiang"] += {"TaiYang", "TianLiang"} <= found
        result["old_selected_star_with_other_principal_present"] += (
            bool(oldselected) and len(found) > 1
        )
        sample.append(
            {
                "synthetic_reference_date": key[0],
                "synthetic_hour_branch": key[1],
                "Life_palace_original_main_stars": sorted(found),
                "source_candidates_original_four_main_stars": sorted(oldselected),
                "source_candidates_with_TaiYang_added": sorted(expanded),
                "distinct_tentative_behavior_constructs_deDuplicated": sorted(constructs),
                "no_outcome_trained_weight_or_questionnaire_response_used": True,
            }
        )
    expected = {
        "synthetic_states": 120,
        "strict_sole_star_and_all_vendor_agreement": 10,
        "initial_four_main_star_presence": 34,
        "extended_five_main_star_presence": 42,
        "new_states_due_sole_TaiYang_extension": 8,
        "two_distinct_target_constructs": 3,
        "number_of_constructs_0": 78,
        "number_of_constructs_1": 39,
        "number_of_constructs_2": 3,
        "two_helping_stars_TaiYang_and_TianLiang": 2,
        "old_selected_star_with_other_principal_present": 22,
    }
    if dict(result) != expected:
        fail("source structural model candidate coverage differs from pinned synthetic cases")
    return {
        "synthetic_chart_option_state_counts": dict(result),
        "all_120_pinned_source_14_main_star_toy_states": sample,
        "no_13000_documentary_rules_count_as_human_sample": True,
        "sampled_dates_not_population_birth_time_prevalence": True,
        "user_or_Hale_inspected_outcomes_not_included": True,
    }


def build():
    lex, coloc, readiness = get_data()
    claims = source_claims(lex)
    edges = dependency_edges()
    toy = all_synthetic_chart_options(oracle_source())
    data = {
        "schema": "HUMANDESIGN_ZIWEI_SOURCE_FOUR_HUMAN_CONSTRUCT_DEPENDENCY_DRAFT_V1",
        "status": (
            "SOURCE_CONTEXT_DEPENDENCIES_AND_SYNTHETIC_COVERAGE_ONLY_NO_FROZEN_ASTROLOGY_MODEL"
        ),
        "original_ZiWei_oldid1963110_source_SHA256": lex["full_original_raw_sha256"],
        "source_11_narrow_lexemes_report_SHA256": LEX_SHA,
        "source_15_same_palace_grade_clauses_report_SHA256": COL_SHA,
        "source_prereg_readiness_gate_matrix_SHA256": READY_SHA,
        "source_312_accepted_original_vendor_oracle_commit": ORACLE_COMMIT,
        "source_312_synthetic_oracle_SHA256": ORACLE_SHA,
        "four_preliminary_behavioral_construct_definitions": {
            name: {
                "main_star_source_intro": sorted(stars),
                "conditional_source_gloss_requires_independent_translation": True,
                "psychometrically_validated_outcome_selected": False,
                "calibrated_probability_weight": None,
            }
            for name, stars in MAIN.items()
        },
        "tentative_TaiYang_helping_extension_for_source_overlap_only": sorted(
            EXTENDED["voluntary_helping"]
        ),
        "all_11_old_chinese_phrase_to_construct_source_dependency_claims": claims,
        "five_original_source_claim_dependency_edges": edges,
        "unverified_benefic_malefic_year_stem_qualifier_source_rule_count": coloc[
            "original_15_grade_line_count"
        ],
        "source_grade_rank_wealth_conditions_not_transferable_to_personality_weights": True,
        (
            "two_hypothesis_models_A_strict_B_presence_are_"
            "ALTERNATIVES_not_copre_registered_primary"
        ): True,
        (
            "model_Bplus_TaiYang_helping_expansion_NOT_test_or_select_after_viewing_human_responses"
        ): True,
        (
            "model_A_strict_mechanics_are_NOT_assumed_original_traditional_conjunction_requirement"
        ): True,
        "model_B_has_no_verified_interactions_or_psychological_calibration": True,
        "source_lexical_occurrences_not_statistically_independent_predictions": True,
        "not_infer_negative_trait_if_few_source_stars_missing": True,
        "unverified_auxiliary_star_positions_cannot_be_scored_or_called_negative": True,
        "clinical_fate_gender_moral_stereotypes_excluded_from_modern_human_prediction": True,
        "comparative_toy_model_structural_coverage": toy,
        "source_frozen_primary_human_prediction_model_selected": False,
        "questionnaire_selected_or_calibrated_for_actual_people": False,
        "matched_decoys_and_non_astrology_baseline_approved": False,
        "real_human_preregistration_completed": False,
        "all_real_human_pilot_readiness_gate_statuses": [
            {"id": r["id"], "status": r["status"], "blocking": r["blocking"]}
            for r in readiness["candidate_pilot_gates"]
        ],
        "number_of_human_ready_gates": 0,
        "actual_real_person_birth_and_response_records": 0,
        "actual_human_predictive_accuracy_trials": 0,
        "production_astrological_rules_promoted": 0,
    }
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    data = build()
    print(
        json.dumps(
            {
                "historical_source_claims": len(
                    data["all_11_old_chinese_phrase_to_construct_source_dependency_claims"]
                ),
                "source_claim_dependency_edges": len(
                    data["five_original_source_claim_dependency_edges"]
                ),
                "synthetic_120_chart_model_coverages": data[
                    "comparative_toy_model_structural_coverage"
                ]["synthetic_chart_option_state_counts"],
                "human_readiness_gates_resolved": data["number_of_human_ready_gates"],
                "actual_human_predictive_trials": 0,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
