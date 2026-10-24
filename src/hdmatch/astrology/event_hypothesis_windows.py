"""Exploratory source-attributed event-window projection, NEVER a validated predictor.

The candidate registry is not frozen. No person-specific events or outcomes are
accepted or scored here. Modern timing and direction conventions are diagnostics.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any


def project_unfrozen_candidate_windows(
    timeline: Mapping[str, Any], candidate_registry: Mapping[str, Any]
) -> dict[str, Any]:
    """Group identical geometric exposures without silently pooling method evidence.

    The input MUST be the existing conjunction-only diagnostic timeline.
    Windows are half-open symbolic-age intervals, NOT historical date promises.
    This deliberately rejects other keys and profiles to avoid accidental
    retrospective model selection. It makes no claim of predictive validity.
    """
    if timeline.get("schema_version") != "astro-primary-directions-conjunction-timeline-v1":
        raise ValueError("only conjunction-only primary-direction timeline is admissible")
    if candidate_registry.get("schema") != "ASTRO_PRIMARY_DIRECTION_EVENT_HYPOTHESES_V0":
        raise ValueError("unknown source rule registry")
    if candidate_registry.get("status") != "SOURCE_BACKED_INTERPRETATION_CANDIDATES_UNFROZEN":
        raise ValueError("candidate rules cannot be promoted to frozen via this projector")
    technique = timeline.get("technique_provenance")
    if not isinstance(technique, Mapping) or technique.get("no_event_interpretation") is not True:
        raise ValueError("historical research timeline provenance is required")
    settings = candidate_registry["experimental_pre_freeze_defaults_not_lilly_claims"]
    key = settings["diagnostic_key"]
    if technique.get("time_key") != key:
        raise ValueError("time-key arm must be selected in an independent, explicit protocol")
    if not timeline.get("scope", "").startswith("seven classical body promissors; bodily"):
        raise ValueError("non-bodily profile cannot be used for these bodily rules")
    minimum = float(settings["min_age_years"])
    maximum = float(settings["max_age_years"])
    half_width = float(settings["half_window_width_years"])
    if not (
        math.isfinite(minimum)
        and math.isfinite(maximum)
        and math.isfinite(half_width)
        and 0 <= minimum < maximum
        and 0 < half_width < (maximum - minimum) / 2
    ):
        raise ValueError("invalid pre-freeze window parameters")
    allowed_methods = set(settings["allowed_geometry"])
    rules = candidate_registry["source_to_construct_rules"]
    if len({rule["id"] for rule in rules}) != len(rules):
        raise ValueError("duplicate source rule IDs")
    keys = {(rule["promissor"], rule["target_role"]): rule["id"] for rule in rules}
    if len(keys) != len(rules):
        raise ValueError("duplicate source roles could falsely count twice")
    candidates: list[dict[str, Any]] = []
    raw_matches = 0
    for record in timeline["directions"]:
        if record["direction"] != "direct":
            continue  # Software direction-sense diagnostic, not Lilly-authenticated.
        rule_id = keys.get((record["promissor"], record["significator"]))
        if rule_id is None or record["contact"] != "body_to_angle":
            continue
        if record["method"] not in allowed_methods:
            raise ValueError("undeclared geometry must not be used for source-rule selection")
        if record["time_key"] != key:
            raise ValueError("contact time-key disagrees with timeline metadata")
        age = float(record["symbolic_age_years"])
        if not math.isfinite(age) or age < 0:
            raise ValueError("nonfinite or negative symbolic age")
        if age < minimum or age >= maximum:
            continue
        low = max(minimum, age - half_width)
        high = min(maximum, age + half_width)
        raw_matches += 1
        candidates.append(
            {
                "source_rule_id": rule_id,
                "contact_symbolic_age_years": age,
                "window_age_lower_inclusive": low,
                "window_age_upper_exclusive": high,
                "method_ids": [record["method"]],
                "model_dates_utc": [record["model_date_utc"]],
                "time_key": key,
                "contact_type": "body_to_angle",
            }
        )
    candidates.sort(
        key=lambda item: (
            item["source_rule_id"],
            item["contact_symbolic_age_years"],
            item["method_ids"][0],
        )
    )
    grouped: list[dict[str, Any]] = []
    for candidate in candidates:
        if (
            grouped
            and grouped[-1]["source_rule_id"] == candidate["source_rule_id"]
            and abs(
                grouped[-1]["contact_symbolic_age_years"] - candidate["contact_symbolic_age_years"]
            )
            <= 1e-9
        ):
            # Exactly coincident methods are alternate model labels, not votes.
            shared = grouped[-1]
            shared["method_ids"].extend(candidate["method_ids"])
            shared["model_dates_utc"].extend(candidate["model_dates_utc"])
        else:
            grouped.append(candidate)
    for candidate in grouped:
        candidate["method_ids"] = sorted(set(candidate["method_ids"]))
        candidate["model_dates_utc"] = sorted(set(candidate["model_dates_utc"]))
        candidate["number_of_equivalent_method_records"] = len(candidate["method_ids"])
        candidate["is_not_independent_confirmation"] = len(candidate["method_ids"]) > 1
    return {
        "schema": "ASTRO_PRIMARY_DIRECTION_UNFROZEN_EVENT_WINDOWS_V0",
        "status": "DIAGNOSTIC_ONLY_NO_FROZEN_INTERPRETATION_NO_HUMAN_VALIDATION",
        "source_book": "Lilly Christian Astrology (1647), printed pp.657-659,668-670",
        "key": key,
        "raw_matching_geometry_records": raw_matches,
        "unique_contact_exposure_groups": len(grouped),
        "source_rule_count": len(rules),
        "windows": grouped,
        "warnings": [
            "Do not pool methods; only one exact exposure for same rule/age/key.",
            "All symbolic ages and date conversions are modern engine diagnostics.",
            "Body-only subset; direction sense, geometry and key not study-frozen.",
            "No participant outcome records read and no prediction validity tested.",
        ],
    }
