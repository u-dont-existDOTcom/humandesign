#!/usr/bin/env python3
"""Synthetic-only seal→separate answer→score smoke test for four source anchors.

Neither a verified Zi Wei natal calculator nor calibrated psychology.
Reuses HD project's established tie-aware rankings and seeded label permutation.
NEVER use this program on real-person records or represent toy results as
preregistered human astrology predictive evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from hashlib import sha256
from pathlib import Path

from hdmatch.evaluation.metrics import aggregate_rank_metrics, evaluate_ranked_case
from hdmatch.evaluation.permutation import permutation_test

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
MAP = TASK / "SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
CHARTS = TASK / "SYNTHETIC_CHART_TOKENS_V1.json"
SEALED = TASK / "SYNTHETIC_PRE_RESPONSE_SEAL_V1.json"
QUESTION_KEYS = ("Q_DECISIVE", "Q_ARGUMENT", "Q_HELPING", "Q_COMPETE")
SEAL_TYPE = "ASTROLOGY_SOURCE_CANDIDATE_SYNTHETIC_PRE_RESPONSE_SEAL_V1"
RESPONSE_TYPE = "ASTROLOGY_EXPLICIT_SYNTHETIC_RESPONSE_BATCH_V1"
CHART_TYPE = "ASTROLOGY_EXPLICIT_MOCK_CHART_FEATURES_V1"


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def canon(data: object) -> bytes:
    return json.dumps(
        data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, content: dict) -> None:
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fail(msg: str) -> None:
    raise ValueError("Synthetic-only scorer rejected: " + msg)


def source_mapping():
    m = read(MAP)
    if (
        m.get("status") != "HISTORICAL_SOURCE_GROUNDED_DRAFT_NOT_FROZEN_OR_AUTHORIZED_FOR_HUMANS"
        or m.get("study_has_been_preregistered") is not False
        or m.get("scored_real_human_recruitment_authorized") is not False
        or m.get("human_predictive_validation_count") != 0
        or m.get("production_astrological_rule_promotions") != 0
        or m.get("score_probabilities_calibrated") is not False
    ):
        fail("source map must be provisional and unvalidated")
    if m.get("question_pool_item_count") != 4 or len(m.get("candidates", [])) != 4:
        fail("source map changed number of items")
    if m.get("response_categories_ordinal_0_to_4") != [
        "never",
        "rarely",
        "sometimes",
        "often",
        "almost_always",
    ]:
        fail("source question ordinal categories changed")
    if (
        digest((ROOT / m["original_Wikitext_source_path"]).read_bytes())
        != m["original_Wikitext_raw_SHA256"]
    ):
        fail("original Chinese source text checksum drift")
    if digest((ROOT / m["accepted_V14_index_path"]).read_bytes()) != m["accepted_V14_index_SHA256"]:
        fail("accepted original Chinese source index changed")
    stems = set()
    questions = set()
    for r in m["candidates"]:
        source_file = ROOT / r["source_line_file"]
        if (
            not source_file.is_file()
            or digest(source_file.read_bytes()) != r["source_line_file_sha256"]
        ):
            fail("historical source quote file hash drift")
        d = read(source_file)
        matches = [x for x in d["records"] if x["id"] == r["source_note_id"]]
        if len(matches) != 1:
            fail("source note missing/duplicated")
        orig = matches[0]
        quote = orig["exact_original_Chinese_Wikitext_quote"]
        fragment = r["source_original_Chinese_fragment"]
        if (
            orig["star_group_native"] != r["star_native"]
            or quote.count(fragment) != 1
            or orig["source_quote_sha256_UTF8"] != r["source_full_line_SHA256"]
            or orig["original_absolute_codepoint_offset"] != r["source_full_line_codepoint_offset"]
            or digest(fragment.encode("utf-8")) != r["source_original_fragment_SHA256"]
            or not r["draft_concealed_behavior_first_question"]
            or r["star_native"] in stems
            or r["draft_concealed_question_id"] in questions
        ):
            fail("original phrase, star or candidate behavior mapping mismatch")
        stems.add(r["star_native"])
        questions.add(r["draft_concealed_question_id"])
    if questions != set(QUESTION_KEYS):
        fail("source question IDs changed")
    return m


def synthetic_charts():
    d = read(CHARTS)
    if (
        d.get("schema") != CHART_TYPE
        or d.get("status") != "SYNTHETIC_FEATURE_TOKENS_NOT_CALCULATED_BIRTH_CHARTS"
        or d.get("there_are_no_birth_dates_times_places_or_real_individuals") is not True
        or d.get("original_source_model_is_not_a_verified_natal_calculator") is not True
    ):
        fail("input fake charts not explicitly synthetic")
    if set(d) != {
        "schema",
        "status",
        "there_are_no_birth_dates_times_places_or_real_individuals",
        "original_source_model_is_not_a_verified_natal_calculator",
        "eligibility",
        "declared_nuisance_stratum",
        "charts",
    }:
        fail("unexpected synthetic chart collection keys, possibly real birth data")
    rows = d["charts"]
    known_stars = {x["star_native"] for x in source_mapping()["candidates"]}
    if len(rows) != 4 or len({x["chart_id"] for x in rows}) != 4:
        fail("fixture must be exactly four unique fake charts")
    if len({x["life_palace_main_star_mock"] for x in rows}) != 4:
        fail("fixture must cover each hypothesized star once")
    for row in rows:
        if (
            set(row) != {"chart_id", "life_palace_main_star_mock", "synthetic"}
            or not re.fullmatch(r"SYNTH-CHART-0[1-4]", row["chart_id"])
            or row["life_palace_main_star_mock"] not in known_stars
            or row["synthetic"] is not True
        ):
            fail("invalid fake chart token or any real birth input")
    return d


def code_dependency_sha() -> dict:
    return {
        "scorer": digest(Path(__file__).read_bytes()),
        "hdmatch_metric": digest((ROOT / "src/hdmatch/evaluation/metrics.py").read_bytes()),
        "hdmatch_label_permutation": digest(
            (ROOT / "src/hdmatch/evaluation/permutation.py").read_bytes()
        ),
    }


def seal() -> dict:
    anchors = source_mapping()
    chartdata = synthetic_charts()
    payload = {
        "schema": SEAL_TYPE,
        "status": "SYNTHETIC_ENGINEERING_SEAL_NOT_AUTHENTIC_PREREGISTRATION",
        "source_mapping_SHA256": digest(MAP.read_bytes()),
        "mock_chart_fixture_SHA256": digest(CHARTS.read_bytes()),
        "code_dependency_SHA256": code_dependency_sha(),
        "question_ids": sorted(x["draft_concealed_question_id"] for x in anchors["candidates"]),
        "star_question_pairs": [
            [x["star_native"], x["draft_concealed_question_id"]] for x in anchors["candidates"]
        ],
        "mock_chart_ids": [x["chart_id"] for x in chartdata["charts"]],
        "source_original_rev": anchors["original_Wikitext_oldid"],
        "score_policy": "UNVALIDATED_ORDINAL_SOURCE_SUPPORT_NO_CALIBRATED_PROBABILITIES",
        "toy_response_scale_0_to_4": True,
        "synthetic_null_permutations": 512,
        "synthetic_null_seed": 190526,
        "synthetic_nuisance_stratum": "toy_all_equal_not_a_real_demographic_match",
        "real_world_chart_engine_is_verified": False,
        "source_to_human_questionnaire_mapping_is_frozen": False,
        "scored_actual_human_responses": 0,
        "participant_birth_records_included": 0,
        "mock_case_truth_labels_included": False,
        "real_preregistration_timestamp_exists": False,
        "real_human_prediction_accuracy_claim": False,
    }
    pkg = {"sealed_payload": payload, "sealed_payload_sha256": digest(canon(payload))}
    save(SEALED, pkg)
    return pkg


def verify_seal(p: dict):
    if set(p) != {"sealed_payload", "sealed_payload_sha256"}:
        fail("sealed packet unexpected keys")
    payload = p["sealed_payload"]
    if digest(canon(payload)) != p["sealed_payload_sha256"]:
        fail("sealed packet payload SHA changed")
    if payload.get("schema") != SEAL_TYPE or payload.get("status") != (
        "SYNTHETIC_ENGINEERING_SEAL_NOT_AUTHENTIC_PREREGISTRATION"
    ):
        fail("seal improperly described as a preregistration")
    if (
        payload.get("real_world_chart_engine_is_verified") is not False
        or payload.get("source_to_human_questionnaire_mapping_is_frozen") is not False
        or payload.get("real_human_prediction_accuracy_claim") is not False
        or payload.get("mock_case_truth_labels_included") is not False
        or payload.get("participant_birth_records_included") != 0
        or payload.get("scored_actual_human_responses") != 0
    ):
        fail("synthetic seal claims real human data or validation")
    if (
        payload.get("source_mapping_SHA256") != digest(MAP.read_bytes())
        or payload.get("mock_chart_fixture_SHA256") != digest(CHARTS.read_bytes())
        or payload.get("code_dependency_SHA256") != code_dependency_sha()
    ):
        fail(
            "source mapping, fake charts, scorer or reused HD scorer modified after synthetic seal"
        )
    m = source_mapping()
    d = synthetic_charts()
    if payload.get("mock_chart_ids") != [x["chart_id"] for x in d["charts"]]:
        fail("mock chart IDs modified")
    if payload.get("star_question_pairs") != [
        [x["star_native"], x["draft_concealed_question_id"]] for x in m["candidates"]
    ]:
        fail("candidate star/question support modified")
    if (
        payload.get("score_policy")
        != "UNVALIDATED_ORDINAL_SOURCE_SUPPORT_NO_CALIBRATED_PROBABILITIES"
        or payload.get("toy_response_scale_0_to_4") is not True
        or payload.get("synthetic_null_permutations") != 512
        or payload.get("synthetic_null_seed") != 190526
    ):
        fail("toy evaluation score changed after seal")
    return payload


def validate_mock_responses(d: dict, charts: dict):
    if (
        set(d)
        != {"schema", "status", "scenario", "real_human_data", "actual_birth_chart_data", "cases"}
        or d["schema"] != RESPONSE_TYPE
        or d["status"] != "MOCK_OUTCOMES_CONSTRUCTED_AFTER_DESIGN_FOR_POSITIVE_AND_NULL_TESTS"
        or d["real_human_data"] is not False
        or d["actual_birth_chart_data"] is not False
    ):
        fail("real / untyped outcomes not accepted")
    if d["scenario"] not in {
        "aligned_positive_control",
        "constant_null_control",
        "deliberately_opposite_control",
    }:
        fail("only three explicit constructed synthetic scenarios allowed")
    if len(d["cases"]) != 4:
        fail("exactly four synthetic cases expected")
    casenames = set()
    truecharts = set()
    chartids = {x["chart_id"] for x in charts["charts"]}
    for row in d["cases"]:
        if set(row) != {"case_id", "true_chart_id", "mock_responses", "synthetic_case"}:
            fail("case unexpectedly contains real-person info")
        if (
            not re.fullmatch(r"SYNTH-P0[1-4]", row["case_id"])
            or row["case_id"] in casenames
            or row["true_chart_id"] not in chartids
            or row["true_chart_id"] in truecharts
            or row["synthetic_case"] is not True
        ):
            fail("nonunique fake case or invalid fake chart truth")
        casenames.add(row["case_id"])
        truecharts.add(row["true_chart_id"])
        values = row["mock_responses"]
        if set(values) != set(QUESTION_KEYS) or any(
            type(v) is not int or v not in range(5) for v in values.values()
        ):
            fail("mock response missing, extra or not ordinal 0..4")
    return sorted(d["cases"], key=lambda x: x["case_id"])


def evaluate_mock(packet: dict, responses: dict) -> dict:
    payload = verify_seal(packet)
    chartdata = synthetic_charts()
    cases = validate_mock_responses(responses, chartdata)
    anchors = source_mapping()["candidates"]
    star_to_q = {x["star_native"]: x["draft_concealed_question_id"] for x in anchors}
    charts = chartdata["charts"]
    chart_ids = [c["chart_id"] for c in charts]
    # Different people have different trait prevalences: raw support is
    # NOT calibrated. The chart-independent row average is only a toy control.
    matrix = [
        [
            case["mock_responses"][star_to_q[chart["life_palace_main_star_mock"]]] / 4
            for chart in charts
        ]
        for case in cases
    ]
    true_chart_for_case = {x["case_id"]: x["true_chart_id"] for x in cases}
    scores = []
    ranks = []
    true_deltas = []
    for case, m_row in zip(cases, matrix, strict=True):
        identity = true_chart_for_case[case["case_id"]]
        candidates = [
            {"candidate_id": chart, "toy_source_support_score": float(score)}
            for chart, score in zip(chart_ids, m_row, strict=True)
        ]
        rank = evaluate_ranked_case(
            case_id=case["case_id"],
            candidates=candidates,
            true_candidate_id=identity,
            id_field="candidate_id",
            score_field="toy_source_support_score",
        )
        ranks.append(rank)
        own = m_row[chart_ids.index(identity)]
        fake_nochart = sum(m_row) / len(m_row)
        scores.append(
            {
                "fake_case": case["case_id"],
                "own_chart_score": own,
                "toy_row_mean_without_chart": fake_nochart,
                "own_minus_toy_row_mean": own - fake_nochart,
                "true_chart_midrank": rank.midrank,
                "true_chart_percentile": rank.percentile,
                "top1_tie_aware_credit": rank.top_1_credit,
            }
        )
        true_deltas.append(own - fake_nochart)
    chart_idx = {c: i for i, c in enumerate(chart_ids)}
    cases_idx = {p["case_id"]: i for i, p in enumerate(cases)}

    def null_stat(assignment):
        total = 0.0
        for case_id, donor_id in assignment.items():
            i = cases_idx[case_id]
            j = chart_idx[true_chart_for_case[donor_id]]
            total += matrix[i][j] - (sum(matrix[i]) / len(matrix[i]))
        return total / len(cases)

    observed = sum(true_deltas) / len(true_deltas)
    null = permutation_test(
        [r["case_id"] for r in cases],
        observed_statistic=observed,
        statistic_for_assignment=null_stat,
        strata={r["case_id"]: payload["synthetic_nuisance_stratum"] for r in cases},
        permutations=payload["synthetic_null_permutations"],
        seed=payload["synthetic_null_seed"],
        alternative="greater",
    )
    agg = aggregate_rank_metrics(ranks)
    result = {
        "schema": "ASTROLOGY_SOURCE_FOUR_ANCHORS_SYNTHETIC_SMOKE_RESULT_V1",
        "status": "SYNTHETIC_ANSWERS_NOT_HUMAN_PREDICTIONS",
        "source_model_candidate_is_frozen_for_humans": False,
        "real_chart_engine_implemented_for_this_example": False,
        "ordinal_support_is_calibrated_probability": False,
        "nonastrological_external_baseline_tested": False,
        "stratification_is_real_nuisance_matched": False,
        "actual_preregistration_timestamp_exists": False,
        "source_text_empirical_truth_confirmed": False,
        "human_predictive_validations": 0,
        "scenario": responses["scenario"],
        "sealed_payload_sha256": packet["sealed_payload_sha256"],
        "sealed_mapping_SHA256": payload["source_mapping_SHA256"],
        "mock_responses_SHA256": digest(canon(responses)),
        "toy_candidate_chart_ids": chart_ids,
        "toy_response_to_chart_score_matrix": matrix,
        "mean_diagonal_minus_no_chart_row_mean": observed,
        "toy_case_rank_diagnostics": scores,
        "HD_existing_rank_metrics_reused": agg.model_dump(mode="json"),
        "HD_existing_seeded_label_permutation_reused": null.model_dump(mode="json"),
        "synthetic_only_interpretation": (
            "Simulation proves scoring and tamper checks only. "
            "Its p-value does not test astrology in humans."
        ),
    }
    return result


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seal")
    score = sub.add_parser("evaluate")
    score.add_argument("--responses", required=True, type=Path)
    score.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.cmd == "seal":
        pkg = seal()
        print(
            json.dumps(
                {
                    "stage": "SYNTHETIC_SEALED_NO_HUMANS",
                    "seal_sha256": pkg["sealed_payload_sha256"],
                    "response_data_inside_seal": False,
                },
                indent=2,
            )
        )
    else:
        packet = read(SEALED)
        responses = read(args.responses)
        scored = evaluate_mock(packet, responses)
        save(args.output, scored)
        print(
            json.dumps(
                {
                    "stage": "SYNTHETIC_ONLY",
                    "scenario": scored["scenario"],
                    "mean_diagonal_advantage": scored["mean_diagonal_minus_no_chart_row_mean"],
                    "mean_true_chart_percentile": scored["HD_existing_rank_metrics_reused"][
                        "mean_percentile"
                    ],
                    "toy_null_permutation_p_not_human_evidence": scored[
                        "HD_existing_seeded_label_permutation_reused"
                    ]["p_value"],
                    "actual_human_predictive_validations": 0,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    cli()
