"""Compact, source-preserving contexts for semantic routing.

The full frozen survey stays server-side and remains the validation authority.
Only the minimum source and route material needed for one semantic decision is
sent to a model.
"""

from __future__ import annotations

import json
from typing import Iterable

from .domain import bank, guide

MAX_ROUTE_SHORTLIST = 12
RECENT_TURN_COUNT = 4


def answered_route_ids(state: dict) -> set[str]:
    return {
        str(turn["canonical_question_id"])
        for turn in state.get("turns", [])
        if turn.get("canonical_question_id")
        and turn.get("answer_text") is not None
        and not turn.get("quarantined")
        and turn.get("turn_role", "behavioral") == "behavioral"
    }


def presented_route_ids(state: dict) -> set[str]:
    return {
        str(turn["canonical_question_id"])
        for turn in state.get("turns", [])
        if turn.get("canonical_question_id")
        and not turn.get("quarantined")
        and turn.get("turn_role", "behavioral") == "behavioral"
    }


def correction_closure(state: dict, seed_ids: Iterable[str]) -> set[str]:
    """Return correction links in both directions until stable."""
    wanted = {str(value) for value in seed_ids}
    turns = [turn for turn in state.get("turns", []) if not turn.get("quarantined")]
    changed = True
    while changed:
        changed = False
        for turn in turns:
            turn_id = str(turn["turn_id"])
            parent = turn.get("correction_of")
            if parent and (turn_id in wanted or str(parent) in wanted):
                before = len(wanted)
                wanted.add(turn_id)
                wanted.add(str(parent))
                changed = changed or len(wanted) != before
    return wanted


def evidence_source_ids(items: Iterable[dict]) -> set[str]:
    return {
        str(quote["turn_id"])
        for item in items
        for quote in item.get("source_quotes", [])
        if isinstance(quote, dict) and quote.get("turn_id")
    }


def covered_facets(state: dict) -> set[str]:
    out: set[str] = set()
    for item in state.get("evidence", []):
        if item.get("review_status") == "superseded_by_participant_correction":
            continue
        out.update(str(value) for value in item.get("candidate_facet_ids", []))
    return out


def eligible_routes(state: dict, instrument: dict) -> list[dict]:
    questions = bank(instrument)["questions"]
    answered = answered_route_ids(state)
    presented = presented_route_ids(state)
    addressed = set(state.get("addressed_routes", {}))

    ranked: list[tuple[int, dict]] = []
    for position, route in enumerate(questions):
        route_id = route["id"]
        if route_id in presented or route_id in addressed:
            continue
        if (
            route.get("kind") == "optional_retrospective"
            and state.get("collection_preferences", {}).get("retrospective_questions_welcome")
            is not True
        ):
            continue
        sources = set(route.get("context_sources") or [])
        self_contained = str(route.get("context_requirement", "")).startswith("Self-contained")
        exact_dependency = bool(sources & answered)
        if not self_contained and not exact_dependency:
            continue

        # Eligibility is not a coverage score. Preserve stable bank order here;
        # the shortlist builder below mixes fresh scenes with newly triggered
        # follow-ups so the bank stays a menu rather than a coverage queue.
        ranked.append((position, route))

    ranked.sort(key=lambda row: row[0])
    return [route for _, route in ranked]


def route_card(route: dict, *, include_limits: bool) -> dict:
    self_contained = str(route.get("context_requirement", "")).startswith("Self-contained")
    card = {
        "id": route["id"],
        "question": route["question"],
        "kind": route.get("kind"),
        "family": route.get("family"),
        "planning_targets": route.get("planning_targets") or [],
        "context_sources": route.get("context_sources") or [],
        "self_contained": self_contained,
        "admission": route.get("admission"),
    }
    if not self_contained:
        card["context_requirement"] = route.get("context_requirement")
    if include_limits:
        card["interpretation_limit"] = route.get("interpretation_limit")
        card["context_binding_rule"] = route.get("context_binding_rule")
        card["live_pilot_guards"] = route.get("live_pilot_guards") or []
    return card


def route_cards(
    state: dict,
    instrument: dict,
    *,
    bulk_import: bool,
    pending_ids: Iterable[str] = (),
    limit: int = MAX_ROUTE_SHORTLIST,
) -> list[dict]:
    if bulk_import:
        retrospective_ok = (
            state.get("collection_preferences", {}).get("retrospective_questions_welcome") is True
        )
        already_presented = presented_route_ids(state)
        already_addressed = set(state.get("addressed_routes", {}))
        routes = [
            route
            for route in bank(instrument)["questions"]
            if route["id"] not in already_presented
            and route["id"] not in already_addressed
            and (route.get("kind") != "optional_retrospective" or retrospective_ok)
        ]
        return [route_card(route, include_limits=False) for route in routes]

    questions = bank(instrument)["questions"]
    route_map = {route["id"]: route for route in questions}
    turn_map = {turn["turn_id"]: turn for turn in state.get("turns", [])}
    pending_route_ids = {
        turn_map[turn_id].get("canonical_question_id")
        for turn_id in pending_ids
        if turn_id in turn_map
        and turn_map[turn_id].get("canonical_question_id")
        and not turn_map[turn_id].get("quarantined")
    }

    eligible = eligible_routes(state, instrument)
    fresh = [
        route
        for route in eligible
        if str(route.get("context_requirement", "")).startswith("Self-contained")
    ]
    followups = [
        route
        for route in eligible
        if not str(route.get("context_requirement", "")).startswith("Self-contained")
    ]
    triggered = [
        route
        for route in followups
        if set(route.get("context_sources") or []).intersection(pending_route_ids)
    ]
    triggered_ids = {route["id"] for route in triggered}
    other_followups = [route for route in followups if route["id"] not in triggered_ids]

    cards: list[dict] = []
    # The route just answered is present only as a repair candidate. It can never
    # be repeated canonically; the planner may use it only when the response
    # itself shows that the original scene/question was not answerable.
    for route_id in pending_route_ids:
        route = route_map.get(route_id)
        if not route:
            continue
        if (
            route.get("kind") == "optional_retrospective"
            and state.get("collection_preferences", {}).get("retrospective_questions_welcome")
            is not True
        ):
            continue
        card = route_card(route, include_limits=True)
        card["repair_only"] = True
        cards.append(card)
        break

    remaining = max(0, limit - len(cards))
    followup_budget = min(4, remaining)
    fresh_budget = max(0, remaining - followup_budget)
    selected = fresh[:fresh_budget] + triggered[:followup_budget]
    if len(triggered) < followup_budget:
        selected.extend(other_followups[: followup_budget - len(triggered)])

    used = {card["id"] for card in cards}
    for route in selected:
        if route["id"] not in used and len(cards) < limit:
            cards.append(route_card(route, include_limits=True))
            used.add(route["id"])

    if len(cards) < limit:
        for route in fresh + triggered + other_followups:
            if route["id"] in used:
                continue
            cards.append(route_card(route, include_limits=True))
            used.add(route["id"])
            if len(cards) >= limit:
                break
    return cards


def guide_cards(instrument: dict, route_ids: Iterable[str] | None = None) -> list[dict]:
    wanted = None if route_ids is None else set(route_ids)
    cards = []
    for item in guide(instrument):
        routes = set(item.get("question_routes") or [])
        if wanted is not None and not routes.intersection(wanted):
            continue
        cards.append(
            {
                "facet_id": item["facet_id"],
                "supported": item.get("narrow_supported_reading"),
                "unsupported_extension": item.get("unsupported_extension"),
                "question_routes": item.get("question_routes") or [],
            }
        )
    return cards


def turn_context_card(turn: dict) -> dict:
    card = {
        "turn_id": turn["turn_id"],
        "question_text": turn.get("question_text"),
        "answer_text": turn.get("answer_text"),
        "canonical_question_id": turn.get("canonical_question_id"),
        "question_wording_status": turn.get("question_wording_status"),
    }
    for key in ("antecedent_turn_ids", "conditions", "corrections", "process_feedback"):
        value = turn.get(key)
        if value:
            card[key] = value
    if turn.get("correction_of") is not None:
        card["correction_of"] = turn.get("correction_of")
    if turn.get("is_review_correction"):
        card["is_review_correction"] = True
    return card


def relevant_turns(
    state: dict,
    instrument: dict,
    route_ids: Iterable[str],
    pending_ids: Iterable[str],
) -> list[dict]:
    wanted_ids = set(pending_ids)
    route_map = {row["id"]: row for row in bank(instrument)["questions"]}
    bank_route_sources: set[str] = set()
    for route_id in route_ids:
        bank_route_sources.update(route_map.get(route_id, {}).get("context_sources") or [])

    turns = state.get("turns", [])
    for turn in turns[-RECENT_TURN_COUNT:]:
        if turn.get("turn_role", "behavioral") == "behavioral":
            wanted_ids.add(turn["turn_id"])
    for turn in turns:
        if turn.get("canonical_question_id") in bank_route_sources:
            wanted_ids.add(turn["turn_id"])

    route_targets = {
        target
        for route_id in route_ids
        for target in (route_map.get(route_id, {}).get("planning_targets") or [])
    }
    related_evidence = [
        item
        for item in state.get("evidence", [])
        if item.get("review_status") != "superseded_by_participant_correction"
        and route_targets.intersection(item.get("candidate_facet_ids") or [])
    ]
    wanted_ids.update(evidence_source_ids(related_evidence))
    wanted_ids = correction_closure(state, wanted_ids)

    # Evidence remains compact in the ledger, but the exact source is reattached
    # whenever it can change routing, correction handling, or nonredundancy.
    return [
        turn_context_card(turn)
        for turn in turns
        if turn["turn_id"] in wanted_ids
        and not turn.get("quarantined")
        and turn.get("turn_role", "behavioral") == "behavioral"
    ]


def compact_existing_evidence(state: dict) -> list[dict]:
    return [
        {
            "evidence_id": item.get("evidence_id"),
            "source_quotes": item.get("source_quotes") or [],
            "observation": item.get("observation"),
            "conditions": item.get("conditions") or [],
            "time_frame": item.get("time_frame"),
            "relationship_context": item.get("relationship_context"),
            "candidate_facet_ids": item.get("candidate_facet_ids") or [],
            "supported_scope": item.get("supported_scope"),
            "unsupported_extensions": item.get("unsupported_extensions") or [],
            "review_status": item.get("review_status"),
        }
        for item in state.get("evidence", [])
        if item.get("review_status") != "superseded_by_participant_correction"
    ]


def make_context(
    state: dict,
    instrument: dict,
    pending_ids: list[str],
    *,
    bulk_import: bool,
) -> dict:
    cards = route_cards(state, instrument, bulk_import=bulk_import, pending_ids=pending_ids)
    route_ids = [row["id"] for row in cards]
    if bulk_import:
        source_turns = [
            turn_context_card(turn)
            for turn in state.get("turns", [])
            if str(turn.get("turn_source", "")).startswith("import-")
            and not turn.get("quarantined")
            and turn.get("turn_role", "behavioral") == "behavioral"
        ]
        guides = guide_cards(instrument)
    else:
        source_turns = relevant_turns(state, instrument, route_ids, pending_ids)
        turn_map = {turn["turn_id"]: turn for turn in state.get("turns", [])}
        answered_route_ids_for_pending = {
            turn_map[turn_id].get("canonical_question_id")
            for turn_id in pending_ids
            if turn_id in turn_map and turn_map[turn_id].get("canonical_question_id")
        }
        guides = guide_cards(instrument, set(route_ids) | answered_route_ids_for_pending)
        correction_scope = correction_closure(state, pending_ids)
        correction_relevant_evidence = [
            item
            for item in state.get("evidence", [])
            if item.get("review_status") != "superseded_by_participant_correction"
            and evidence_source_ids([item]).intersection(correction_scope)
        ]
        if state.get("review_only") or state.get("review", {}).get("shown_at"):
            correction_relevant_evidence = [
                item
                for item in state.get("evidence", [])
                if item.get("review_status") != "superseded_by_participant_correction"
            ]
        correction_facets = {
            str(facet)
            for item in correction_relevant_evidence
            for facet in item.get("candidate_facet_ids", [])
        }
        if correction_facets:
            existing_facets = {item["facet_id"] for item in guides}
            guides.extend(
                item
                for item in evidence_guide_for_facets(instrument, correction_facets)
                if item["facet_id"] not in existing_facets
            )
        if state.get("review_only") or state.get("review", {}).get("shown_at"):
            review_source_ids = evidence_source_ids(state.get("evidence", []))
            review_source_ids.update(pending_ids)
            review_source_ids = correction_closure(state, review_source_ids)
            existing = {turn["turn_id"] for turn in source_turns}
            source_turns.extend(
                turn_context_card(turn)
                for turn in state.get("turns", [])
                if turn["turn_id"] in review_source_ids
                and turn["turn_id"] not in existing
                and not turn.get("quarantined")
                and turn.get("turn_role", "behavioral") == "behavioral"
            )

    return {
        "turns": source_turns,
        "pending_turn_ids": pending_ids,
        "import_bulk_review": bulk_import,
        "review_only": bool(state.get("review_only") or state.get("review", {}).get("shown_at")),
        "existing_evidence": compact_existing_evidence(state),
        "correction_relevant_evidence": (
            [
                item
                for item in compact_existing_evidence(state)
                if item.get("evidence_id")
                in {
                    source.get("evidence_id")
                    for source in (correction_relevant_evidence if not bulk_import else [])
                }
            ]
        ),
        "candidate_routes": cards,
        "candidate_evidence_guide": guides,
    }


def serialized_chars(context: dict) -> int:
    return len(json.dumps(context, ensure_ascii=False, separators=(",", ":")))


def full_route_cards(instrument: dict, route_ids: Iterable[str]) -> list[dict]:
    wanted = set(route_ids)
    return [
        {
            "id": route["id"],
            "question": route["question"],
            "kind": route.get("kind"),
            "family": route.get("family"),
            "planning_targets": route.get("planning_targets") or [],
            "context_sources": route.get("context_sources") or [],
            "context_requirement": route.get("context_requirement"),
            "admission": route.get("admission"),
            "interpretation_limit": route.get("interpretation_limit"),
            "context_binding_rule": route.get("context_binding_rule"),
            "live_pilot_guards": route.get("live_pilot_guards") or [],
        }
        for route in bank(instrument)["questions"]
        if route["id"] in wanted
    ]


def evidence_guide_for_facets(instrument: dict, facet_ids: Iterable[str]) -> list[dict]:
    wanted = set(facet_ids)
    return [
        {
            "facet_id": item["facet_id"],
            "supported": item.get("narrow_supported_reading"),
            "unsupported_extension": item.get("unsupported_extension"),
            "question_routes": item.get("question_routes") or [],
        }
        for item in guide(instrument)
        if item["facet_id"] in wanted
    ]


def make_review_context(
    state: dict,
    instrument: dict,
    planner_context: dict,
    proposed_plan: dict,
    *,
    bulk_import: bool,
) -> dict:
    route_id = (proposed_plan.get("question") or {}).get("route_id")
    addressed_route_ids = [
        str(item.get("route_id"))
        for item in proposed_plan.get("addressed_routes", [])
        if isinstance(item, dict) and item.get("route_id")
    ]
    route_ids = ([route_id] if route_id else []) + addressed_route_ids
    route_map = {row["id"]: row for row in bank(instrument)["questions"]}
    facet_ids = {
        str(facet)
        for item in proposed_plan.get("evidence", [])
        for facet in item.get("candidate_facet_ids", [])
    }

    source_turn_ids = set(planner_context.get("pending_turn_ids", []))
    source_turn_ids.update(
        str(quote.get("turn_id"))
        for item in proposed_plan.get("evidence", [])
        for quote in item.get("source_quotes", [])
        if quote.get("turn_id")
    )
    source_turn_ids.update(
        str(value) for value in (proposed_plan.get("question") or {}).get("antecedent_turn_ids", [])
    )
    control = proposed_plan.get("control_quote")
    if isinstance(control, dict) and control.get("turn_id"):
        source_turn_ids.add(str(control["turn_id"]))

    amendment_ids = {
        str(value)
        for item in proposed_plan.get("evidence", [])
        for value in item.get("amends_evidence_ids", [])
    }
    old_evidence = [
        item for item in state.get("evidence", []) if item.get("evidence_id") in amendment_ids
    ]
    source_turn_ids.update(evidence_source_ids(old_evidence))

    correction_scope = correction_closure(state, planner_context.get("pending_turn_ids", []))
    correction_relevant_evidence = [
        item
        for item in state.get("evidence", [])
        if item.get("review_status") != "superseded_by_participant_correction"
        and evidence_source_ids([item]).intersection(correction_scope)
    ]
    if state.get("review_only") or state.get("review", {}).get("shown_at"):
        correction_relevant_evidence = [
            item
            for item in state.get("evidence", [])
            if item.get("review_status") != "superseded_by_participant_correction"
        ]
    source_turn_ids.update(evidence_source_ids(correction_relevant_evidence))

    # Nonredundancy and dropped-condition checks must use authoritative server
    # source, not only the planner-selected subset. Pull source already tied to
    # the selected route's targets and to explicit bulk-address metadata.
    route_targets = {
        target
        for selected in route_ids
        for target in (route_map.get(selected, {}).get("planning_targets") or [])
    }
    relevant_prior_evidence = [
        item
        for item in state.get("evidence", [])
        if item.get("review_status") != "superseded_by_participant_correction"
        and route_targets.intersection(item.get("candidate_facet_ids") or [])
    ]
    source_turn_ids.update(evidence_source_ids(relevant_prior_evidence))
    for selected in route_ids:
        source_turn_ids.update(state.get("addressed_routes", {}).get(selected, []))

    if state.get("review_only") or state.get("review", {}).get("shown_at"):
        source_turn_ids.update(evidence_source_ids(state.get("evidence", [])))

    if bulk_import:
        source_turn_ids.update(
            turn["turn_id"]
            for turn in state.get("turns", [])
            if not turn.get("quarantined") and turn.get("turn_role", "behavioral") == "behavioral"
        )

    source_turn_ids = correction_closure(state, source_turn_ids)
    turns = [
        turn_context_card(turn)
        for turn in state.get("turns", [])
        if turn["turn_id"] in source_turn_ids
        and not turn.get("quarantined")
        and turn.get("turn_role", "behavioral") == "behavioral"
    ]

    admission_plan = proposed_plan
    selected_routes = full_route_cards(instrument, route_ids)
    bulk_projection = None
    if bulk_import:
        # The admission pass already receives every exact imported source turn.
        # Omit planner-emitted unassessed dispositions because source_review_complete
        # makes their meaning deterministic, and use compact route cards for routes
        # that are only being marked addressed. Keep full route controls for the
        # actual proposed next question. This is a source-preserving, semantics-preserving transport projection:
        # no source text, evidence, addressed-route binding, or question is removed.
        admission_plan = json.loads(json.dumps(proposed_plan))
        admission_plan["dispositions"] = [
            item
            for item in admission_plan.get("dispositions", [])
            if item.get("status") != "unassessed"
            or item.get("conditions")
            or item.get("process_feedback_quotes")
        ]
        full_question_ids = {route_id} if route_id else set()
        selected_routes = full_route_cards(instrument, full_question_ids)
        selected_full_ids = {item["id"] for item in selected_routes}
        for addressed_id in addressed_route_ids:
            if addressed_id in selected_full_ids:
                continue
            route = route_map.get(addressed_id)
            if route is not None:
                selected_routes.append(route_card(route, include_limits=False))
        bulk_projection = "implicit_unassessed_dispositions_omitted_and_addressed_routes_compacted"

    return {
        "turns": turns,
        "source_scope": (
            "complete_imported_record"
            if bulk_import
            else "authoritative_server_source_for_proposal"
        ),
        "pending_turn_ids": planner_context.get("pending_turn_ids", []),
        "review_only": bool(state.get("review_only") or state.get("review", {}).get("shown_at")),
        "import_bulk_review": bulk_import,
        "proposed_plan": admission_plan,
        "bulk_admission_projection": bulk_projection,
        "selected_routes": selected_routes,
        "selected_evidence_guide": evidence_guide_for_facets(
            instrument,
            facet_ids
            | {
                str(facet)
                for item in correction_relevant_evidence + relevant_prior_evidence
                for facet in item.get("candidate_facet_ids", [])
            },
        ),
        "prior_evidence_being_amended": old_evidence,
        "correction_relevant_evidence": correction_relevant_evidence,
        "related_prior_evidence": relevant_prior_evidence,
        "addressed_route_sources": {
            selected: list(state.get("addressed_routes", {}).get(selected, []))
            for selected in route_ids
            if state.get("addressed_routes", {}).get(selected)
        },
    }
