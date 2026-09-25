"""Direct endpoint tests for the experimental answer-conditioned decoder."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from hdmatch.api.birth_test_api import (
    SourceAnswer,
    install_birth_test,
    interpret_answers,
    question_bank,
    utc_from_local,
)
from hdmatch.evaluation.astrohd_v15_decoder import (
    MODEL_PATH,
    answer_signs,
    candidate_minutes,
    content_hash,
    load_model,
    mask_at,
    normalize_profile,
    rank_against,
    run_panel,
    score_mask,
    validate_location,
)


def profile(state="supported"):
    return {d["id"]: state for d in load_model()[2]["domains"]}


@pytest.fixture
def ephe():
    path = Path(os.environ.get("HDMATCH_EPHEMERIS_PATH", "/opt/swisseph"))
    if not (path / "sepl_18.se1").exists():
        pytest.skip("Production Swiss files are required for direct astronomy tests")
    return path


def test_all_positive_exactly_preserves_every_old_six_bit_score():
    signs = answer_signs(profile())
    assert signs == (1,) * 6
    assert all(score_mask(mask, signs) == mask.bit_count() for mask in range(64))


def test_explicit_relevant_answer_change_flips_comparison_without_refitting():
    original = profile()
    changed = {**original, "insight_translation": "contradicted"}
    assert score_mask(1, answer_signs(original)) > score_mask(0, answer_signs(original))
    assert score_mask(1, answer_signs(changed)) < score_mask(0, answer_signs(changed))
    assert (
        load_model()[0]["selected_rule_ids"]
        == json.loads(MODEL_PATH.read_text())["selected_rule_ids"]
    )


def test_unknown_is_neither_support_nor_contradiction():
    signs = answer_signs(profile("unknown"))
    assert signs == (0,) * 6
    assert all(score_mask(mask, signs) == 0 for mask in range(64))


def test_missing_astronomical_clause_never_predicts_absent_trait():
    assert score_mask(0, answer_signs(profile("contradicted"))) == 0
    assert score_mask(63, answer_signs(profile("contradicted"))) == -6


def test_or_bridge_requires_both_alternatives_explicitly_contradicted():
    p = profile("unknown")
    p["romantic_attachment"] = "contradicted"
    assert answer_signs(p)[3] == 0
    p["persuasion_strategy"] = "contradicted"
    assert answer_signs(p)[3] == -1
    p["persuasion_strategy"] = "supported"
    assert answer_signs(p)[3] == 1


def test_identical_features_stay_tied_for_every_answer_state():
    for state in ("supported", "contradicted", "mixed", "unknown", "not_applicable"):
        signs = answer_signs(profile(state))
        assert score_mask(63, signs) == score_mask(63, signs)
        rank = rank_against([score_mask(63, signs)], score_mask(63, signs))
        assert (rank["rank_best"], rank["rank_worst"]) == (1, 2)


def test_candidate_panels_are_unique_nested_and_target_independent():
    a, b, c = [candidate_minutes(n) for n in (99, 999, 9999)]
    assert len(set(c)) == 9999
    assert a == b[:99] == c[:99]
    assert b == c[:999]
    assert candidate_minutes(999) == b
    with pytest.raises(ValueError):
        candidate_minutes(1000)


def test_equivalent_profile_order_does_not_change_signs_or_hash():
    a = profile()
    b = dict(reversed(list(a.items())))
    assert answer_signs(a) == answer_signs(b)
    assert content_hash(normalize_profile(a)) == content_hash(normalize_profile(b))


def test_extra_unknown_or_missing_domains_are_not_silently_scored():
    with pytest.raises(ValueError):
        normalize_profile({**profile(), "invented": "supported"})
    with pytest.raises(ValueError):
        normalize_profile({})
    with pytest.raises(ValueError):
        normalize_profile({**profile(), "romantic_attachment": "maybe"})


def test_selected_scenarios_are_the_existing_bank_with_context():
    bank, nodes = question_bank()
    ids = load_model()[2]["focused_question_ids"]
    assert bank["version"] == "scenario-bank-v7.0-20260922"
    assert all(key in nodes for key in ids)
    assert "G06" in nodes["R02"]["context_sources"]
    assert ids.index("G06") < ids.index("R02")
    assert "planning_targets" not in {k: nodes["G06"][k] for k in ("id", "question")}


def test_local_time_conversion_and_dst_are_not_guessed():
    assert utc_from_local("1985-01-29T05:25:00", "America/New_York") == datetime(
        1985, 1, 29, 10, 25, tzinfo=UTC
    )
    with pytest.raises(ValueError, match="ambiguous"):
        utc_from_local("2024-11-03T01:30:00", "America/New_York")
    with pytest.raises(ValueError, match="did not exist"):
        utc_from_local("2024-03-10T02:30:00", "America/New_York")


def test_invalid_locations_rejected_before_astronomy():
    for lat, lon in [(float("nan"), 0), (90, 0), (0, 181)]:
        with pytest.raises(ValueError):
            validate_location(lat, lon)


class NeutralInterpreter:
    def __init__(self, forged=False):
        self.forged = forged
        self.payload = None

    def _conversation_call_json(self, **kwargs):
        self.payload = kwargs["payload"]
        return {
            "interpretations": [
                {
                    "domain_id": d["id"],
                    "state": "supported" if d["id"] == "insight_translation" else "unknown",
                    "summary": "Only the reported explanation is established.",
                    "evidence": [
                        {
                            "question_id": "G02",
                            "quote": "an invented sentence"
                            if self.forged
                            else "I explain the discrepancy.",
                        }
                    ]
                    if d["id"] == "insight_translation"
                    else [],
                }
                for d in load_model()[2]["domains"]
            ]
        }


def test_interpreter_uses_actual_quote_and_receives_no_birth_or_chart():
    model = NeutralInterpreter()
    result = interpret_answers(
        [SourceAnswer(question_id="G02", text="I explain the discrepancy.")], model
    )
    assert result["review_required"]
    assert result["structured_birth_or_chart_fields_supplied"] is False
    assert set(model.payload) == {"definitions", "responses"}
    assert result["interpretations"][0]["evidence"][0]["quote"] == "I explain the discrepancy."


def test_forged_interpreter_evidence_is_rejected():
    with pytest.raises(ValueError, match="source verification"):
        interpret_answers(
            [SourceAnswer(question_id="G02", text="I explain the discrepancy.")],
            NeutralInterpreter(True),
        )


def test_import_preserves_existing_text_without_requiring_new_scenarios():
    class UnknownInterpreter:
        def _conversation_call_json(self, **kwargs):
            assert kwargs["payload"]["responses"][0]["answer"] == "Existing private interview text."
            return {
                "interpretations": [
                    {
                        "domain_id": d["id"],
                        "state": "unknown",
                        "summary": "Insufficient",
                        "evidence": [],
                    }
                    for d in load_model()[2]["domains"]
                ]
            }

    out = interpret_answers(
        [SourceAnswer(question_id="imported", text="Existing private interview text.")],
        UnknownInterpreter(),
    )
    assert len(out["interpretations"]) == 5


def test_direct_original_scores_and_tied_minutes(ephe):
    p = profile()
    for hour, minute, expected in [(10, 25, 6), (10, 24, 6), (10, 27, 5)]:
        mask = mask_at(datetime(1985, 1, 29, hour, minute, tzinfo=UTC), 39.9526, -75.1652, ephe)
        assert score_mask(mask, answer_signs(p)) == expected
    mask = mask_at(datetime(2013, 1, 28, 8, 30, tzinfo=UTC), 39.9526, -75.1652, ephe)
    assert score_mask(mask, answer_signs(p)) == 1


def test_real_candidate_scores_respond_to_answers_not_target_optimization(ephe):
    p = profile()
    base = run_panel(p, latitude=39.9526, longitude=-75.1652, count=99, ephemeris_root=ephe)
    changed = run_panel(
        {**p, "romantic_attachment": "contradicted", "persuasion_strategy": "contradicted"},
        latitude=39.9526,
        longitude=-75.1652,
        count=99,
        ephemeris_root=ephe,
    )
    assert base["model_id"] == changed["model_id"]
    assert base["panel_sha256"] == changed["panel_sha256"]
    assert base["profile_sha256"] != changed["profile_sha256"]
    assert base["top_candidates"] != changed["top_candidates"]
    with pytest.raises(ValueError, match="No scored evidence"):
        run_panel(
            profile("unknown"), latitude=39.9526, longitude=-75.1652, count=99, ephemeris_root=ephe
        )


def test_http_consumer_profile_change_and_frozen_reveal(ephe):
    app = FastAPI()
    install_birth_test(app, ephemeris_root=ephe, interpreter=NeutralInterpreter())
    client = TestClient(app)
    assert client.get("/birth-test").status_code == 200
    assert len(client.get("/birth-test/api/contract").json()["questions"]) == 9
    body = {
        "consent": True,
        "reviewed": True,
        "profile": profile(),
        "source_answers_sha256": "a" * 64,
        "latitude": 39.9526,
        "longitude": -75.1652,
        "decoy_count": 99,
    }
    assert client.post("/birth-test/api/run", json={**body, "reviewed": False}).status_code == 400
    assert (
        client.post("/birth-test/api/run", json={**body, "birth_date": "1985-01-29"}).status_code
        == 422
    )
    first = client.post("/birth-test/api/run", json=body)
    assert first.status_code == 200, first.text
    first = first.json()
    changed = client.post(
        "/birth-test/api/run", json={**body, "profile": profile("contradicted")}
    ).json()
    assert changed["model_id"] == first["model_id"]
    assert changed["profile_sha256"] != first["profile_sha256"]
    checked = client.post(
        "/birth-test/api/check",
        json={
            "run_id": first["run_id"],
            "birth_local": "1985-01-29T05:25:00",
            "timezone": "America/New_York",
            "time_source": "record",
        },
    )
    assert checked.status_code == 200, checked.text
    assert checked.json()["score"] == 6
    assert checked.json()["profile_sha256"] == first["profile_sha256"]
    assert checked.json()["result_class"] == "FIRST_REVEAL_FROZEN_MODEL_TEST"
    assert client.delete("/birth-test/api/run/" + first["run_id"]).status_code == 200
    assert (
        client.post(
            "/birth-test/api/check",
            json={
                "run_id": first["run_id"],
                "birth_local": "1985-01-29T05:25:00",
                "timezone": "America/New_York",
            },
        ).status_code
        == 404
    )


def test_obvious_birth_key_in_import_is_not_sent_to_interpreter():
    model = NeutralInterpreter()
    with pytest.raises(ValueError, match="birth/chart"):
        interpret_answers(
            [SourceAnswer(question_id="imported", text="I was born 1985-01-29.")], model
        )
    assert model.payload is None
