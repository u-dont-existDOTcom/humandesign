from __future__ import annotations

import inspect

import pytest

from hdmatch.evaluation.participant_adjudicated_v2_prototype import (
    OwnerPrototypeSessionV2,
    run_interactive_owner_demo,
    run_synthetic_owner_demo,
)


def _run(answers: list[str]) -> tuple[dict[str, object] | None, list[str]]:
    values = iter(answers)
    output: list[str] = []
    result = run_interactive_owner_demo(lambda _prompt: next(values), output.append)
    return result, output


def test_interactive_accept_path_uses_owner_inputs() -> None:
    result, _ = _run(["accept", "accept"])
    assert result is not None and result["status"] == "accepted"


def test_interactive_correction_revision_and_arbitrary_wording() -> None:
    result, output = _run(
        [
            "correct",
            "The participant drafted a plan.",
            "revise",
            "I draft plans first.",
            "yes",
            "accept",
        ]
    )
    assert result is not None and result["wording"] == "I draft plans first."
    assert any("Revised candidate question" in line for line in output)


def test_interactive_negative_adjudication_paths() -> None:
    assert _run(["not-supported"])[0] is None
    assert _run(["accept", "reject"])[0]["status"] == "rejected"  # type: ignore[index]
    assert _run(["accept", "unresolved"])[0]["status"] == "unresolved"  # type: ignore[index]


def test_owner_demo_is_human_readable_and_accepted() -> None:
    transcript = run_synthetic_owner_demo()
    assert transcript[0].startswith("Episode:")
    assert any("Candidate question:" in line for line in transcript)
    assert transcript[-1] == "Result: accepted (participant-adjudicated)"


def test_correction_is_append_only_and_unsupported_fact_is_not_operative() -> None:
    session = OwnerPrototypeSessionV2.synthetic()
    session.review_fact("FACT-1", "correct", "The participant wrote a plan before complex work.")
    assert [fact.fact_id for fact in session.record.episode_facts] == ["FACT-1", "FACT-1-R1"]
    assert session.record.episode_facts[1].supersedes_fact_id == "FACT-1"

    unsupported = OwnerPrototypeSessionV2.synthetic()
    unsupported.review_fact("FACT-1", "not-supported")
    with pytest.raises(ValueError, match="usable accepted fact"):
        unsupported.propose_pattern()


def test_pattern_is_provisional_until_adjudication_and_reject_stays_rejected() -> None:
    session = OwnerPrototypeSessionV2.synthetic()
    session.propose_pattern()
    assert session.result()["status"] == "unresolved"
    session.adjudicate("reject")
    assert session.result()["status"] == "rejected"


def test_revise_creates_next_proposal_with_participant_wording() -> None:
    session = OwnerPrototypeSessionV2.synthetic()
    first = session.propose_pattern()
    session.adjudicate("revise", "I plan before complex work.")
    revised = session.refine_once("I plan before complex work.")
    assert revised.revision_index == 1
    assert revised.previous_proposal_id == first.proposal_id
    assert revised.proposition == "I plan before complex work."
    session.adjudicate("accept", revised.proposition)
    assert session.result()["wording"] == "I plan before complex work."


def test_prototype_uses_v2_core_and_not_historical_auto_map() -> None:
    source = inspect.getsource(
        __import__(
            "hdmatch.evaluation.participant_adjudicated_v2_prototype",
            fromlist=["OwnerPrototypeSessionV2"],
        )
    )
    assert "life_patterns_app" not in source
    session = OwnerPrototypeSessionV2.synthetic()
    session.propose_pattern()
    session.adjudicate("unresolved")
    assert session.result()["status"] == "unresolved"
