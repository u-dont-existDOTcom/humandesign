"""Bounded source-table/geometry references; no personal or clinical prediction.

The caller supplies qualification as an assertion. This module does not determine
whether a chart satisfies Ptolemy's topical rulership or placement conditions.
"""
from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any, Sequence

HERE = Path(__file__).resolve().parent
PLANETS = ("Saturn", "Jupiter", "Mars", "Venus", "Mercury")


def nodal_quadrature_points(ascending_node_degrees: float) -> dict[str, float]:
    """Return node/opposite/quadrature longitudes; no proximity or disease rule."""
    if isinstance(ascending_node_degrees, bool) or not isinstance(
        ascending_node_degrees, (int, float)
    ):
        raise TypeError("Node longitude must be a real finite number, not a boolean")
    if not math.isfinite(ascending_node_degrees):
        raise ValueError("Node longitude must be finite")
    n = ascending_node_degrees % 360.0
    return {
        "ascending_node": n,
        "quadrature_plus_90": (n + 90.0) % 360.0,
        "descending_node": (n + 180.0) % 360.0,
        "quadrature_plus_270": (n + 270.0) % 360.0,
    }


def read_profile_table() -> dict[str, Any]:
    return json.loads((HERE / "SOUL_PROFILE_TABLES.json").read_text())


def profile_reference(
    planets: Sequence[str], *, topical_qualified: bool | None, placement: str | None
) -> dict[str, Any]:
    """Retrieve an archived branch only after supplied qualification.

    This is a source lookup, not the algorithm for choosing rulers, determining
    dignity, diagnosing a person, or calculating modern personality traits.
    """
    if isinstance(planets, (str, bytes)) or not isinstance(planets, (tuple, list)):
        raise TypeError("Use a list or tuple of distinct source ruler names")
    if not planets or any(not isinstance(p, str) for p in planets):
        raise ValueError("At least one source ruler name is required")
    if len(set(planets)) != len(planets):
        raise ValueError("Duplicate names cannot create corroboration")
    if any(p not in PLANETS for p in planets):
        raise ValueError("This particular table has five governing planets")
    if topical_qualified is not None and type(topical_qualified) is not bool:
        raise TypeError("Qualification must be True, False, or None")
    if placement not in {None, "HONOURABLE", "CONTRARY", "MIXED", "UNRESOLVED"}:
        raise ValueError("Unknown source placement branch")
    if topical_qualified is False:
        return {"status": "NOT_APPLICABLE", "reason": "Topic authority not satisfied"}
    if topical_qualified is None:
        return {"status": "UNRESOLVED", "reason": "Topic authority not established"}
    if placement in {None, "MIXED", "UNRESOLVED"}:
        return {"status": "UNRESOLVED", "reason": "No unique supplied placement branch"}
    if len(planets) > 2:
        return {"status": "UNRESOLVED", "reason": "No three-plus mixture supplied by this table"}
    selected = next(p for p in read_profile_table()["profiles"] if set(p["planets"]) == set(planets))
    return {
        "status": "SOURCE_REFERENCE_ONLY",
        "profile_id": selected["profile_id"],
        "source_locator": deepcopy(selected["source_locator"]),
        "placement_branch": placement,
        "description": deepcopy(selected["placement_branches"][placement]),
        "qualification_origin": "CALLER_ASSERTION_NOT_VERIFIED_BY_THIS_HELPER",
        "is_prediction": False,
    }
