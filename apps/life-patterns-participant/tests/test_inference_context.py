from participant.domain import Admission, Plan, bank, import_record, new_state
from participant.engine import PLANNER, REVIEWER
from participant.inference_context import (
    MAX_ROUTE_SHORTLIST,
    make_context,
    make_review_context,
    serialized_chars,
)
from participant.store import canonical
from test_participant import Fake, authority


def imported_state(turn_count=96):
    state = new_state("test", "openai-gpt-56-sol", "xhigh")
    state.update(session_id="s", revision=0, consent=True, phase="ready")
    for number in range(1, turn_count + 1):
        state["turns"].append(
            {
                "turn_id": f"import-{number:04d}",
                "sequence": number,
                "turn_source": "import-1",
                "canonical_question_id": None,
                "question_wording_status": "received_edited_or_unverified",
                "question_text": f"Edited historical question {number}?",
                "answer_text": (
                    "Synthetic development answer with a condition, an exception, and enough "
                    "detail to resemble a conversational response without using participant data. "
                    f"Fixture {number}."
                ),
                "correction_of": None,
            }
        )
    return state


def test_bulk_import_context_has_hard_compact_budget():
    instrument = authority()
    state = imported_state()
    pending = [turn["turn_id"] for turn in state["turns"]]
    context = make_context(state, instrument, pending, bulk_import=True)

    assert len(context["turns"]) == 96
    assert len(context["candidate_routes"]) == 78
    assert "G24" not in {route["id"] for route in context["candidate_routes"]}

    state["collection_preferences"]["retrospective_questions_welcome"] = True
    with_retrospective = make_context(state, instrument, pending, bulk_import=True)
    assert len(with_retrospective["candidate_routes"]) == 79
    assert "G24" in {route["id"] for route in with_retrospective["candidate_routes"]}
    assert serialized_chars(context) < 100_000

    request_chars = (
        len(PLANNER) + serialized_chars(context) + len(canonical(Plan.model_json_schema()))
    )
    assert request_chars < 110_000


def test_post_import_clarification_rechecks_full_import_for_nonredundancy():
    instrument = authority()
    state = imported_state()
    fake = Fake()
    pending = [turn["turn_id"] for turn in state["turns"]]
    bulk = make_context(state, instrument, pending, bulk_import=True)
    bulk["additional_pending_batches"] = False
    plan, _ = fake.call(PLANNER, bulk, Plan, state["model"], state["effort"])

    for turn_id in pending:
        state["dispositions"][turn_id] = {
            "turn_id": turn_id,
            "status": "unassessed",
            "conditions": [],
            "process_feedback_quotes": [],
            "reason": "Synthetic bulk routing review.",
        }
    for item in plan.evidence:
        state["evidence"].append(
            item.model_dump()
            | {
                "review_status": "independent_semantic_admission_passed",
                "source_turn_ids": [quote.turn_id for quote in item.source_quotes],
            }
        )

    state["turns"].append(
        {
            "turn_id": "clarification-1",
            "sequence": 97,
            "turn_source": "railway_participant",
            "canonical_question_id": "G23",
            "question_wording_status": "rendered_v2",
            "question_text": "Synthetic current question",
            "answer_text": "Synthetic current clarification answer.",
            "correction_of": None,
        }
    )

    context = make_context(state, instrument, ["clarification-1"], bulk_import=False)
    context["additional_pending_batches"] = False
    assert len(context["candidate_routes"]) <= MAX_ROUTE_SHORTLIST
    assert context["historical_import_recheck"] is True
    assert {turn["turn_id"] for turn in context["turns"]} >= {
        "import-0001",
        "import-0096",
        "clarification-1",
    }
    assert serialized_chars(context) < 110_000

    pending_guides = {
        route for item in context["candidate_evidence_guide"] for route in item["question_routes"]
    }
    assert "G23" in pending_guides
    supplied_routes = {route["id"] for route in context["candidate_routes"]} | {"G23"}
    assert all(
        set(item["question_routes"]).intersection(supplied_routes)
        for item in context["candidate_evidence_guide"]
    )

    ordinary_plan, _ = fake.call(PLANNER, context, Plan, state["model"], state["effort"])
    reviewer = make_review_context(
        state, instrument, context, ordinary_plan.model_dump(), bulk_import=False
    )
    assert "candidate_routes" not in reviewer
    assert reviewer["source_scope"] == "authoritative_server_source_including_recovered_import"
    assert {turn["turn_id"] for turn in reviewer["turns"]} >= {
        "import-0001",
        "import-0096",
        "clarification-1",
    }
    assert serialized_chars(reviewer) < 110_000

    pair_chars = (
        len(PLANNER)
        + serialized_chars(context)
        + len(canonical(Plan.model_json_schema()))
        + len(REVIEWER)
        + serialized_chars(reviewer)
        + len(canonical(Admission.model_json_schema()))
    )
    assert pair_chars < 220_000


def test_route_shortlist_is_deterministic_and_dependency_bound():
    instrument = authority()
    state = new_state("test", "openai-gpt-56-sol", "xhigh")
    state["turns"] = [
        {
            "turn_id": "t-a0",
            "canonical_question_id": "A0",
            "question_text": "A0",
            "answer_text": "Synthetic answer",
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        }
    ]
    context = make_context(state, instrument, ["t-a0"], bulk_import=False)
    ids = [route["id"] for route in context["candidate_routes"]]

    assert ids[0] == "A0"
    assert context["candidate_routes"][0]["repair_only"] is True
    assert "G23" in ids  # fresh everyday setting remains available
    assert "G24" not in ids  # optional retrospective route requires explicit collection preference
    assert "R02" not in ids  # requires G06, which has not been answered
    assert ids.count("A0") == 1  # presented route appears only as repair-only candidate
    assert len(ids) <= MAX_ROUTE_SHORTLIST

    state["collection_preferences"]["retrospective_questions_welcome"] = True
    ids_with_retrospective = [
        route["id"]
        for route in make_context(state, instrument, ["t-a0"], bulk_import=False)[
            "candidate_routes"
        ]
    ]
    assert "G24" in ids_with_retrospective


def test_reviewer_reattaches_all_pending_source_not_just_planner_quotes():
    instrument = authority()
    state = new_state("test", "m", "x")
    state["turns"] = [
        {
            "turn_id": "p1",
            "question_text": "What do you do when you disagree?",
            "answer_text": "I usually speak up when I disagree.",
            "canonical_question_id": "G05",
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        },
        {
            "turn_id": "p2",
            "question_text": "Any exceptions?",
            "answer_text": "Except with my dad—there I go quiet.",
            "canonical_question_id": None,
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        },
    ]
    planner_context = {
        "turns": [state["turns"][0]],
        "pending_turn_ids": ["p1", "p2"],
        "existing_evidence": [],
    }
    proposed = {
        "action": "review",
        "dispositions": [],
        "evidence": [
            {
                "evidence_id": "e1",
                "source_quotes": [{"turn_id": "p1", "quote": "I usually speak up"}],
                "candidate_facet_ids": [],
                "amends_evidence_ids": [],
            }
        ],
        "question": None,
        "control_quote": None,
        "addressed_routes": [],
        "source_review_complete": False,
        "reason": "fixture",
    }
    review = make_review_context(state, instrument, planner_context, proposed, bulk_import=False)
    assert {turn["turn_id"] for turn in review["turns"]} == {"p1", "p2"}


def test_pending_correction_reattaches_original_source_bidirectionally():
    instrument = authority()
    state = new_state("test", "m", "x")
    state["turns"] = [
        {
            "turn_id": "old",
            "question_text": "Original question",
            "answer_text": "I always speak up.",
            "canonical_question_id": "G05",
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        },
        *[
            {
                "turn_id": f"filler-{number}",
                "question_text": "Unrelated",
                "answer_text": f"Unrelated answer {number}",
                "canonical_question_id": None,
                "question_wording_status": "rendered_v2",
                "correction_of": None,
            }
            for number in range(5)
        ],
        {
            "turn_id": "new",
            "question_text": "Correction",
            "answer_text": "Correction: not with my father.",
            "canonical_question_id": None,
            "question_wording_status": "rendered_v2",
            "correction_of": "old",
        },
    ]
    context = make_context(state, instrument, ["new"], bulk_import=False)
    assert {"old", "new"} <= {turn["turn_id"] for turn in context["turns"]}


def test_review_correction_context_includes_all_admitted_evidence_sources():
    instrument = authority()
    state = new_state("test", "m", "x")
    state["review_only"] = True
    state["turns"] = [
        {
            "turn_id": "source",
            "question_text": "Earlier",
            "answer_text": "I usually ask first.",
            "canonical_question_id": "G05",
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        },
        *[
            {
                "turn_id": f"review-filler-{number}",
                "question_text": "Unrelated",
                "answer_text": f"Unrelated review answer {number}",
                "canonical_question_id": None,
                "question_wording_status": "rendered_v2",
                "correction_of": None,
            }
            for number in range(5)
        ],
        {
            "turn_id": "correction",
            "question_text": "Review correction",
            "answer_text": "Only with close friends.",
            "canonical_question_id": None,
            "question_wording_status": "rendered_v2",
            "correction_of": None,
            "is_review_correction": True,
        },
    ]
    state["evidence"] = [
        {
            "evidence_id": "e-old",
            "source_quotes": [{"turn_id": "source", "quote": "I usually ask first."}],
            "observation": "Scoped old reading",
            "conditions": [],
            "time_frame": "current",
            "relationship_context": "general",
            "candidate_facet_ids": [],
            "supported_scope": "source only",
            "unsupported_extensions": [],
            "review_status": "independent_semantic_admission_passed",
        }
    ]
    context = make_context(state, instrument, ["correction"], bulk_import=False)
    assert {"source", "correction"} <= {turn["turn_id"] for turn in context["turns"]}


def test_import_exact_question_recovers_route_without_claiming_verified_original():
    instrument = authority()
    state = new_state("test", "m", "x")
    a0 = next(route for route in bank(instrument)["questions"] if route["id"] == "A0")
    import_record(
        state,
        {
            "turns": [
                {
                    "question_text": a0["question"],
                    "answer_text": "Synthetic answer.",
                }
            ]
        },
        "edited_response_record",
        instrument,
    )
    turn = state["turns"][0]
    assert turn["canonical_question_id"] == "A0"
    assert turn["id_basis"] == "exact_canonical_question_text"
    assert turn["question_wording_status"] == "received_edited_or_unverified"


def test_collection_metadata_turn_is_preserved_but_not_behavior_pending():
    instrument = authority()
    state = new_state("test", "m", "x")
    import_record(
        state,
        {
            "turns": [
                {
                    "turn_role": "collection_metadata",
                    "question_text": "Voice or typing?",
                    "answer_text": "Mostly voice.",
                },
                {
                    "question_text": "Behavior question",
                    "answer_text": "Behavior answer",
                },
            ]
        },
        "prior_json",
        instrument,
    )
    assert state["turns"][0]["turn_role"] == "collection_metadata"
    assert state["dispositions"]["import-0001"]["status"] == "process_only"
    pending = [
        turn["turn_id"] for turn in state["turns"] if turn["turn_id"] not in state["dispositions"]
    ]
    assert pending == ["import-0002"]


def test_bulk_addressed_route_is_removed_from_future_shortlist():
    instrument = authority()
    state = new_state("test", "m", "x")
    state["turns"] = [
        {
            "turn_id": "t-a0",
            "canonical_question_id": "A0",
            "question_text": "A0",
            "answer_text": "Synthetic answer",
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        }
    ]
    state["addressed_routes"] = {"G19": ["t-a0"]}
    context = make_context(state, instrument, ["t-a0"], bulk_import=False)
    assert "G19" not in {route["id"] for route in context["candidate_routes"]}


def test_review_correction_adds_corrected_evidence_facet_to_guide_and_reviewer():
    instrument = authority()
    state = new_state("test", "m", "x")
    state["review_only"] = True
    facet = "D01.approach"
    state["turns"] = [
        {
            "turn_id": "old-source",
            "question_text": "Earlier source",
            "answer_text": "I usually start by checking what is concrete.",
            "canonical_question_id": None,
            "question_wording_status": "rendered_v2",
            "correction_of": None,
        },
        *[
            {
                "turn_id": f"filler-correction-{number}",
                "question_text": "Unrelated",
                "answer_text": f"Unrelated {number}",
                "canonical_question_id": None,
                "question_wording_status": "rendered_v2",
                "correction_of": None,
            }
            for number in range(5)
        ],
        {
            "turn_id": "review-fix",
            "question_text": "Review correction",
            "answer_text": "Only when I have enough information.",
            "canonical_question_id": None,
            "question_wording_status": "rendered_v2",
            "correction_of": None,
            "is_review_correction": True,
        },
    ]
    state["evidence"] = [
        {
            "evidence_id": "e-corrected",
            "source_quotes": [
                {
                    "turn_id": "old-source",
                    "quote": "I usually start by checking what is concrete.",
                }
            ],
            "observation": "Old scoped reading.",
            "conditions": [],
            "time_frame": "current",
            "relationship_context": "general",
            "candidate_facet_ids": [facet],
            "supported_scope": "old source",
            "unsupported_extensions": [],
            "review_status": "disputed_by_later_correction",
        }
    ]
    context = make_context(state, instrument, ["review-fix"], bulk_import=False)
    assert facet in {item["facet_id"] for item in context["candidate_evidence_guide"]}
    assert "e-corrected" in {
        item["evidence_id"] for item in context["correction_relevant_evidence"]
    }

    proposed = {
        "action": "review",
        "dispositions": [
            {
                "turn_id": "review-fix",
                "status": "conditional",
                "conditions": ["enough information"],
                "process_feedback_quotes": [],
                "reason": "fixture",
            }
        ],
        "evidence": [],
        "question": None,
        "control_quote": None,
        "addressed_routes": [],
        "source_review_complete": False,
        "reason": "fixture",
    }
    review = make_review_context(state, instrument, context, proposed, bulk_import=False)
    assert "e-corrected" in {item["evidence_id"] for item in review["correction_relevant_evidence"]}
    assert facet in {item["facet_id"] for item in review["selected_evidence_guide"]}


def test_post_clarification_finalization_uses_reviewed_delta_not_full_import():
    instrument = authority()
    state = imported_state()
    for turn in state["turns"]:
        state["dispositions"][turn["turn_id"]] = {
            "turn_id": turn["turn_id"],
            "status": "unassessed",
            "conditions": [],
            "process_feedback_quotes": [],
            "reason": "Synthetic prior complete-source review.",
        }
    state["evidence"] = [
        {
            "evidence_id": "prior-admitted",
            "source_quotes": [
                {"turn_id": "import-0001", "quote": state["turns"][0]["answer_text"]}
            ],
            "observation": "Synthetic admitted prior evidence.",
            "conditions": [],
            "time_frame": "historical",
            "relationship_context": "general",
            "candidate_facet_ids": [],
            "supported_scope": "fixture",
            "unsupported_extensions": [],
            "review_status": "independent_semantic_admission_passed",
        }
    ]
    state["turns"].append(
        {
            "turn_id": "clarification-1",
            "sequence": 97,
            "turn_source": "railway_participant",
            "canonical_question_id": "G23",
            "question_wording_status": "rendered_v2",
            "question_text": "Synthetic admitted clarification",
            "answer_text": "Synthetic clarification answer.",
            "correction_of": None,
        }
    )
    state["review_only"] = True
    state["review_finalization_after_clarification"] = True

    context = make_context(state, instrument, ["clarification-1"], bulk_import=False)

    ids = {turn["turn_id"] for turn in context["turns"]}
    assert context["review_only"] is True
    assert context["review_finalization_after_clarification"] is True
    assert context["historical_import_recheck"] is False
    assert "clarification-1" in ids
    assert "import-0001" in ids
    assert "import-0050" not in ids
    assert len(context["turns"]) < 15
    assert serialized_chars(context) < 35_000


def test_bulk_admission_compacts_only_redundant_projection_material():
    instrument = authority()
    state = imported_state(turn_count=96)
    state["collection_preferences"]["retrospective_questions_welcome"] = True
    pending = [turn["turn_id"] for turn in state["turns"]]
    planner_context = make_context(state, instrument, pending, bulk_import=True)
    route_ids = [route["id"] for route in planner_context["candidate_routes"]]
    exact_quote = state["turns"][0]["answer_text"][:40]
    proposed = {
        "action": "review",
        "dispositions": [
            {
                "turn_id": turn_id,
                "status": "unassessed",
                "conditions": [],
                "process_feedback_quotes": [],
                "reason": "Implicit unassessed source after complete review. " + ("x" * 250),
            }
            for turn_id in pending
        ],
        "evidence": [
            {
                "evidence_id": "bulk-e1",
                "source_quotes": [{"turn_id": pending[0], "quote": exact_quote}],
                "candidate_facet_ids": [],
                "amends_evidence_ids": [],
                "observation": "Synthetic scoped observation",
            }
        ],
        "question": None,
        "control_quote": None,
        "addressed_routes": [
            {"route_id": route_id, "source_turn_ids": [pending[0]]}
            for route_id in route_ids
        ],
        "source_review_complete": True,
        "reason": "Synthetic complete-source proposal.",
    }

    review = make_review_context(
        state, instrument, planner_context, proposed, bulk_import=True
    )

    assert len(review["turns"]) == 96
    assert {turn["turn_id"] for turn in review["turns"]} == set(pending)
    assert review["proposed_plan"]["evidence"] == proposed["evidence"]
    assert review["proposed_plan"]["addressed_routes"] == proposed["addressed_routes"]
    assert review["proposed_plan"]["dispositions"] == []
    assert review["bulk_admission_projection"].startswith("implicit_unassessed")
    assert {route["id"] for route in review["selected_routes"]} == set(route_ids)
    assert all("interpretation_limit" not in route for route in review["selected_routes"])
    assert serialized_chars(review) < 110_000
