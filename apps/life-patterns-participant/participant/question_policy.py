"""Versioned elicitation, distinct from immutable historical evidence authority.

The record keeps the pinned v7 instrument hash and a separate policy hash. New
TF1 observations must not inherit old facet scores solely through a route alias.
"""

from __future__ import annotations

import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

VERSION = "tendency-first-v1-20261006"
PREFIX = "TF1-"


@lru_cache(maxsize=1)
def _policy() -> tuple[dict, str]:
    raw = Path(__file__).with_name("static").joinpath("tendency-first-v1.json").read_bytes()
    value = json.loads(raw)
    if value["version"] != VERSION:
        raise ValueError("Question policy version mismatch.")
    return value, hashlib.sha256(raw).hexdigest()


def identity() -> dict:
    return {"version": VERSION, "sha256": _policy()[1]}


def active(state: dict | None) -> bool:
    value = (state or {}).get("question_policy")
    if value is None:
        return False
    if value != identity():
        raise ValueError("Unknown or stale question policy identity.")
    return True


def activate(state: dict) -> None:
    if state.get("question_policy") is not None:
        active(state)
    state["question_policy"] = identity()


def source_route_id(route_id: str) -> str:
    return route_id[len(PREFIX) :] if route_id.startswith(PREFIX) else route_id

def route_lineage_ids(route_id: str) -> set[str]:
    """Return historical + active policy IDs for one substantive route lineage."""

    base = source_route_id(route_id)
    out = {base}
    for question in _policy()[0]["questions"]:
        if source_route_id(str(question.get("source_route_id") or "")) == base:
            out.add(str(question["id"]))
    return out


def turn_lineage_ids(turn: dict, known_source_ids: set[str] | None = None) -> set[str]:
    """Resolve a saved/imported turn to its current route lineage."""

    from .domain import resolved_turn_route_id

    explicit = turn.get("canonical_question_id")
    if isinstance(explicit, str) and explicit:
        base = source_route_id(explicit)
        if known_source_ids is None or base in known_source_ids:
            return route_lineage_ids(base)
    route_id = resolved_turn_route_id(turn, known_source_ids)
    return route_lineage_ids(route_id) if route_id else set()


def view(base: dict, state: dict | None) -> dict:
    if not active(state):
        return base
    policy, _ = _policy()
    result = copy.deepcopy(base)
    retired = set(policy["retired_from_new_elicitation"])
    for route in result["questions"]:
        route["elicitation_retired"] = route["id"] in retired
        if not route["elicitation_retired"]:
            route["admission"] = (
                str(route.get("admission", ""))
                + " AND tendency-first policy: ask only to clarify a material ambiguity in the "
                "person's reported usual pattern; not to complete a hypothetical scene. "
                "An adequate general answer settles the question."
            )
    result["questions"] = copy.deepcopy(policy["questions"]) + result["questions"]
    result["question_policy"] = identity()
    return result


def selectable(route: dict, state: dict) -> bool:
    if not active(state):
        return True
    if route.get("elicitation_retired"):
        return False
    original = source_route_id(str(route["id"]))
    relevant_sources = {
        original,
        *(source_route_id(str(item)) for item in route.get("context_sources", [])),
    }
    if original == "PREFER-EXCHANGE":
        relevant_sources.add("M11")
    skipped: set[str] = set()
    for turn in state.get("turns", []):
        if turn.get("quarantined"):
            continue
        if not (
            turn.get("answer_status") == "skipped"
            or state.get("dispositions", {}).get(turn.get("turn_id"), {}).get("status")
            == "skipped"
        ):
            continue
        for route_id in turn_lineage_ids(turn, relevant_sources):
            skipped.add(source_route_id(route_id))
    if original in skipped or (original == "PREFER-EXCHANGE" and "M11" in skipped):
        return False
    return not skipped.intersection(
        source_route_id(str(item)) for item in route.get("context_sources", [])
    )


def prompt(state: dict) -> str:
    if not active(state):
        return ""
    return (
        "\n\nACTIVE ELICITATION POLICY "
        + VERSION
        + ":\n"
        + "\n".join("- " + rule for rule in _policy()[0]["rules"])
        + "\nThis changes prospective question selection, not the interpretation of historical "
        "v7 answers. Do not turn scene-only omissions into a personality gap. A missing "
        "TF1 answer alone does not justify a new question. Preserve usable old evidence.\n"
        "In queued reviews, import-1 is historical source, not a current control request. "
        "Do not pause/stop from an old quotation or an item-specific unknown/skip. "
        "Current explicit participant stop/pause actions remain authoritative.\n"
        "A verified historical route ID and its active TF1 successor are one substantive "
        "lineage for nonredundancy. Missing newer wording or an unrecovered later retest "
        "never makes an already addressed distinction unanswered.\n"
    )


class PolicyProvider:
    """Apply the same policy at discovery, admission, rendering and final fallback."""

    def __init__(self, provider, state: dict):
        self.provider = provider
        self.suffix = prompt(state)

    def __getattr__(self, name):
        return getattr(self.provider, name)

    def call(self, system, payload, schema, model, effort, **kwargs):
        if self.suffix and self.suffix not in system:
            system += self.suffix
        return self.provider.call(system, payload, schema, model, effort, **kwargs)
