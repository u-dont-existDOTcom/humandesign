"""Fast clarification triage for Life Patterns shadow evaluation."""

from typing import Literal

from pydantic import Field

from .domain import Question, StrictModel, bank
from .inference_context import presented_route_ids, route_card, turn_context_card


class GapTriage(StrictModel):
    decision: Literal["clarification_needed", "review_ready"]
    candidates: list[Question] = Field(default_factory=list, max_length=3)


class GapAdmission(StrictModel):
    approved_route_ids: list[str] = Field(default_factory=list)
    missed_material_gap: Question | None = None
    review_ready_supported: bool
    errors: list[str] = Field(default_factory=list)


GAP_TRIAGE_PROMPT = """Decide only whether a materially useful Life Patterns clarification
remains. Read the complete exact source for nonredundancy. Do not build evidence,
summarize personality, disposition every turn, map every route, or ask for missing
coverage. Return at most 3 independent candidates, preferably fewer. A candidate must
have valid context, not already be answered, and have material expected information
gain. Canonical wording must be exact. If none qualifies, return review_ready."""

GAP_ADMISSION_PROMPT = """Adversarially audit only the clarification decision. Verify each
candidate's exact wording, context or antecedent, nonredundancy and material information
gain. Do not build evidence. Also challenge review_ready by returning one clearly
material missed gap if present. Missing coverage alone is not a gap."""


def source_cards(state: dict) -> list[dict]:
    return [
        turn_context_card(turn)
        for turn in state.get("turns", [])
        if not turn.get("quarantined")
        and turn.get("turn_role", "behavioral") == "behavioral"
    ]


def candidate_route_cards(
    state: dict, instrument: dict, include_limits: bool = False
) -> list[dict]:
    shown = presented_route_ids(state)
    addressed = set(state.get("addressed_routes", {}))
    retrospective_ok = (
        state.get("collection_preferences", {}).get("retrospective_questions_welcome")
        is True
    )
    return [
        route_card(route, include_limits=include_limits)
        for route in bank(instrument)["questions"]
        if route["id"] not in shown
        and route["id"] not in addressed
        and (route.get("kind") != "optional_retrospective" or retrospective_ok)
    ]


def make_triage_context(state: dict, instrument: dict) -> dict:
    return {
        "source_scope": "complete_behavioral_source",
        "turns": source_cards(state),
        "candidate_routes": candidate_route_cards(state, instrument),
    }


def validate_triage(result: GapTriage, state: dict, instrument: dict) -> GapTriage:
    available = {route["id"]: route for route in candidate_route_cards(state, instrument)}
    if result.decision == "review_ready" and result.candidates:
        raise ValueError("review_ready cannot include clarification candidates")
    if result.decision == "clarification_needed" and not result.candidates:
        raise ValueError("clarification_needed requires at least one candidate")
    if len({item.route_id for item in result.candidates}) != len(result.candidates):
        raise ValueError("triage repeated a clarification route")
    for item in result.candidates:
        if item.route_id not in available:
            raise ValueError("triage selected a route outside supplied candidates")
        if item.route_type == "canonical" and item.text != available[item.route_id]["question"]:
            raise ValueError("canonical triage wording must match frozen route")
    return result


def make_admission_context(state: dict, instrument: dict, triage: GapTriage) -> dict:
    full = {
        route["id"]: route
        for route in candidate_route_cards(state, instrument, include_limits=True)
    }
    return {
        "source_scope": "complete_behavioral_source",
        "turns": source_cards(state),
        "triage_decision": triage.model_dump(),
        "selected_routes": [full[item.route_id] for item in triage.candidates],
        "candidate_routes": candidate_route_cards(state, instrument),
    }


def validate_admission(
    result: GapAdmission, triage: GapTriage, state: dict, instrument: dict
) -> GapAdmission:
    proposed = {item.route_id for item in triage.candidates}
    if not set(result.approved_route_ids).issubset(proposed):
        raise ValueError("admission approved an unproposed route")
    available = {route["id"]: route for route in candidate_route_cards(state, instrument)}
    missed = result.missed_material_gap
    if missed is not None:
        if missed.route_id not in available:
            raise ValueError("missed gap is outside supplied routes")
        if (
            missed.route_type == "canonical"
            and missed.text != available[missed.route_id]["question"]
        ):
            raise ValueError("missed canonical wording must match frozen route")
    return result


def admitted_candidates(triage: GapTriage, admission: GapAdmission) -> list[Question]:
    approved = set(admission.approved_route_ids)
    kept = [item for item in triage.candidates if item.route_id in approved]
    missed = admission.missed_material_gap
    if missed is not None and missed.route_id not in {item.route_id for item in kept}:
        kept.append(missed)
    return kept[:3]
