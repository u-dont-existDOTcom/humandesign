"""Historical Jyotish source-criticism checks only; NEVER a production natal predictor.

Scopes, dates and alternative ages are source metadata. We deliberately do not
score human outcomes or guess a precedence that the inspected text lacks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Scope = Literal["UNSPECIFIED_MARRIAGE", "FIRST_MARRIAGE", "SECOND_MARRIAGE", "THIRD_MARRIAGE", "SPOUSE_LOSS"]


@dataclass(frozen=True)
class AgeClaim:
    verse: str
    age_options: frozenset[int]
    scope: Scope
    qualifier: str = "UNQUANTIFIED"

    def __post_init__(self) -> None:
        if not self.age_options or any(age < 1 or age > 120 for age in self.age_options):
            raise ValueError("Each source age claim needs valid discrete ages")


def inclusive_relative_house(origin: int, number_from_origin: int) -> int:
    """Whole-sign inclusive count: ninth from ninth == fifth from Lagna."""
    if not (1 <= origin <= 12 and 1 <= number_from_origin <= 12):
        raise ValueError("Whole-sign house ordinals must range from 1 to 12")
    return ((origin + number_from_origin - 2) % 12) + 1


def age_interpretation_difference(options: frozenset[int]) -> dict[str, object]:
    """Quantify erroneous widening of a disjunct age set into an interval."""
    if not options:
        raise ValueError("Source options are required")
    interval = frozenset(range(min(options), max(options) + 1))
    return {"literal_disjunction": sorted(options),
            "wrong_contiguous_interval": sorted(interval),
            "new_age_values_mistakenly_admitted": sorted(interval - options)}


def age_claim_collision(claims: tuple[AgeClaim, ...]) -> dict[str, object]:
    """Report source relations; never select or score a favorable rule.

    A generic marriage rule is NOT silently assigned to first marriage.
    If several unindexed rules coactivate, the hypothetical single-event
    intersection is informative but does not resolve event identity.
    """
    if not claims:
        return {"status": "NO_SOURCE_CONDITION", "source_only": True,
                "score_allowed": False}
    if len(set(c.verse for c in claims)) != len(claims):
        raise ValueError("Do not double-count the same verse")
    generic = [c for c in claims if c.scope == "UNSPECIFIED_MARRIAGE"]
    indexed = [c for c in claims if c.scope in ("FIRST_MARRIAGE", "SECOND_MARRIAGE", "THIRD_MARRIAGE")]
    if generic:
        same_event_intersection = set(generic[0].age_options)
        for c in generic[1:]:
            same_event_intersection.intersection_update(c.age_options)
        status = "UNRESOLVED_EVENT_INDEX_AND_DISJOINT_AGES" if len(generic) >= 2 and not same_event_intersection else "UNRESOLVED_EVENT_INDEX"
    else:
        same_event_intersection = None
        status = "ORDINAL_EXPLICIT_REQUIRES_SOURCE_CONDITION_AND_EMPIRICAL_FREEZE"
    return {"status": status,
            "unindexed_claims": [c.verse for c in generic],
            "explicitly_indexed_claims": [c.verse for c in indexed],
            "single_event_age_intersection_if_assumed": (sorted(same_event_intersection) if same_event_intersection is not None else None),
            "alternatives": [{"verse": c.verse, "ages": sorted(c.age_options),
                              "scope": c.scope, "qualifier": c.qualifier} for c in claims],
            "probabilities_calibrated": False, "source_only": True,
            "score_allowed": False, "canonical_selection": None}


def verse_21_partial(venus_sign_index: int, ruler_sign_index: int,
                     seventh_lord_strong: bool | None) -> str:
    """B47 synthetic example, 0=Aries, 3=Cancer, 11=Pisces.

    Does NOT compute full planetary shadbala. Venus exalted in Pisces
    with its ruler Jupiter exalted in Cancer still leaves the source's
    'seventh lord strong' condition unresolved.
    """
    if not all(0 <= x <= 11 for x in (venus_sign_index, ruler_sign_index)):
        raise ValueError("Sign index outside 0..11")
    if venus_sign_index != 11 or ruler_sign_index != 3:
        return "FIRST_TWO_CONDITIONS_NOT_SATISFIED_FOR_THIS_SPECIAL_CASE"
    if seventh_lord_strong is None:
        return "UNRESOLVED_SEVENTH_LORD_STRENGTH"
    return "FULL_CONDITION_SATISFIED" if seventh_lord_strong else "SEVENTH_LORD_STRENGTH_CONDITION_FAILS"


B47_22 = AgeClaim("BPHS.18.22", frozenset({5, 9}), "UNSPECIFIED_MARRIAGE", "PRAYASHAH_UNQUANTIFIED")
B47_23 = AgeClaim("BPHS.18.23", frozenset({7, 11}), "UNSPECIFIED_MARRIAGE", "PRAYASHAH_UNQUANTIFIED")
EXPLICIT_40 = AgeClaim("BPHS.18.40", frozenset({10}), "FIRST_MARRIAGE")
EXPLICIT_41_SECOND = AgeClaim("BPHS.18.41.second", frozenset({22}), "SECOND_MARRIAGE")
EXPLICIT_41_THIRD = AgeClaim("BPHS.18.41.third", frozenset({33}), "THIRD_MARRIAGE")


if __name__ == "__main__":
    import json
    print(json.dumps({"B47_reconciliation": age_claim_collision((B47_22, B47_23)),
                      "BPHS_18_30_translation_spread": age_interpretation_difference(frozenset({22, 27})),
                      "relative_house_checks": {"ninth_from_ninth": inclusive_relative_house(9, 9),
                                                "seventh_from_ninth": inclusive_relative_house(9, 7)},
                      "B47_partial_multi_spouse_condition": verse_21_partial(11, 3, None)},
                     ensure_ascii=False, indent=2))
