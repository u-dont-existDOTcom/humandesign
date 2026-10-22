"""B55 source-only symbolic distinctions for historical Jyotish income verses.

IMPORTANT: This module is *not* an astrology calculator, a predictive model, a
psychological/moral classifier, or a source-precedence resolver. Its inputs are
invented symbolic logic cases, never a person's chart or economic records.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

CLASSICAL = frozenset({'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'})


def _synthetic(yes: bool) -> None:
    if yes is not True:
        raise ValueError('synthetic=True required: real charts and people are out of scope')


def _flag(value: bool, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f'{name} must be a boolean')
    return value


def printed_gain_loss_premises(*, lord11_kendra_or_trikona: bool,
                               malefic_in_11th: bool,
                               lord11_favorable_sign_or_amsa: bool,
                               synthetic: bool = False) -> dict:
    """Antecedents as printed; mutually disagreeing *source clauses* only."""
    _synthetic(synthetic)
    a = _flag(lord11_kendra_or_trikona, 'lord11_kendra_or_trikona')
    b = _flag(malefic_in_11th, 'malefic_in_11th')
    c = _flag(lord11_favorable_sign_or_amsa, 'lord11_favorable_sign_or_amsa')
    return {
        'SC_11_v2_gain': a or b,
        'SC_11_v10_loss': b,
        'JP_XV_v72_gain': a or b or c,
        'source_collision_SC': b,
        'parallel_predicate_not_verbatim_sanskrit': True,
        'canon_rule': None,
        'score_allowed': False,
    }


def printed_income_means(*, benefic_occupants: int,
                         malefic_occupants: int, synthetic: bool = False) -> dict:
    """XV.69 historical evaluative language, expressly NOT a real-person allegation."""
    _synthetic(synthetic)
    if any(type(n) is not int or n < 0 for n in (benefic_occupants, malefic_occupants)):
        raise ValueError('occupant counts must be nonnegative integers')
    if benefic_occupants and malefic_occupants:
        archival_class = 'MIXED_MEANS'
    elif benefic_occupants:
        archival_class = 'FAVORABLE_MEANS'
    elif malefic_occupants:
        archival_class = 'UNFAVORABLE_MEANS'
    else:
        archival_class = 'NO_OCCUPANTS'
    return {
        'archival_evaluative_class': archival_class,
        'quantitative_wealth_prediction': None,
        'personal_moral_allegation_allowed': False,
        'score_allowed': False,
    }


def source_lord_vs_occupant(*, eleventh_lord: str,
                            eleventh_occupants: tuple[str, ...],
                            synthetic: bool = False) -> dict:
    """XV.67–68 refer to occupants; XV.71 refers to the house lord."""
    _synthetic(synthetic)
    if eleventh_lord not in CLASSICAL or any(p not in CLASSICAL for p in eleventh_occupants):
        raise ValueError('Classical seven-planet symbolic vocabulary only')
    if len(set(eleventh_occupants)) != len(eleventh_occupants):
        raise ValueError('Duplicated symbolic occupant')
    return {
        'JP_XV_v67_v68_occupant_indicators': sorted(eleventh_occupants),
        'JP_XV_v71_lord_indicator': eleventh_lord,
        'lord_equals_every_occupant': bool(eleventh_occupants) and all(p == eleventh_lord for p in eleventh_occupants),
        'indicators_have_same_role_by_definition': False,
        'planet_strength_established': False,
        'score_allowed': False,
    }


def target_types():
    """Distinct observational targets; their names are not likelihoods."""
    return frozenset({
        'INCOME_AMOUNT', 'SOURCE_PERSON_OR_INSTITUTION', 'INCOME_MEANS_MORAL_CLAIM',
        'OCCUPATION_ACTIVITY', 'DISTRIBUTION_DONATION', 'DOCUMENTED_DEPRIVATION',
        'FOREIGN_TRADE_ACTIVITY', 'ITINERANT_WANDERING', 'FOREIGN_RESIDENCE'
    })


def compare_event_targets(a: str, b: str, *, synthetic: bool = False) -> dict:
    _synthetic(synthetic)
    if a not in target_types() or b not in target_types():
        raise ValueError('unknown target kind')
    return {'same_observable': a == b, 'score_allowed': False}


@dataclass(frozen=True)
class Witness:
    edition: str
    printed_verse: str
    printed_page: int
    identifier: str


def verse_locator_binding(w: Witness, *, synthetic: bool = False) -> dict:
    _synthetic(synthetic)
    if not w.edition or not w.printed_verse or not w.identifier or type(w.printed_page) is not int or w.printed_page < 1:
        raise ValueError('Incomplete original-source locator')
    return {'citation_key': f'{w.identifier}|{w.edition}|{w.printed_verse}|p{w.printed_page}',
            'global_numbering_offset': None, 'score_allowed': False}
