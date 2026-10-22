"""B56 source-variant argala diagnostics. Not a chart calculator or predictive model.

References are literal synthetic 0-indexed zodiac signs. Competing editorial
readings are deliberately unranked. No empirical predictions may be scored.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PRIMARY = ((2, 12), (4, 10), (11, 3))
SECONDARY_TEXTUALLY_SHARED = ((5, 9),)


def sign_at_house(reference_sign: int, house: int, reverse: bool = False) -> int:
    if not isinstance(reference_sign, int) or isinstance(reference_sign, bool) or not 0 <= reference_sign < 12:
        raise ValueError('Reference sign must be an integer 0..11')
    if not isinstance(house, int) or isinstance(house, bool) or not 1 <= house <= 12:
        raise ValueError('House ordinal must be an integer 1..12')
    delta = house - 1
    return (reference_sign - delta if reverse else reference_sign + delta) % 12


def primary_pairs(reference_sign: int, *, reverse: bool = False) -> tuple[tuple[int, int], ...]:
    return tuple((sign_at_house(reference_sign, a, reverse), sign_at_house(reference_sign, b, reverse)) for a, b in PRIMARY)


def third_house_special_versions(malefics_third: int, planets_eleventh: int) -> dict:
    """Never pick a winner; Venkatesha's alternative as read in 2010 translation.

    RATH_AND_VENKATESHA_GENERAL: any malefic creates a third-house argala.
    RATH_UNOBSTRUCTED: Rath states a special third argala has no obstruction.
    VENKATESHA_UNOBSTRUCTED: 'many' malefics; 3+ operational proxy because
    the commentary explicitly distinguishes one/two from the many case.
    BPHS_ENGLISH_3PLUS: 3+ in Santhanam/Kerr paraphrase, whereas source
    Sanskrit 31.4 `vyadhikah` does not explicitly state integer three.
    """
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 or n > 9 for n in (malefics_third, planets_eleventh)):
        raise ValueError('Nonnegative synthetic occupancies required')
    has = malefics_third > 0
    return {
        'source_version': 'MULTIPLE_UNADJUDICATED',
        'RATH_third_argala_exists': has,
        'RATH_third_argala_unobstructed': has,
        'VENKATESHA_third_argala_exists': has,
        'VENKATESHA_many_malefics_unobstructed_proxy_3plus': malefics_third >= 3,
        'VENKATESHA_obstruction_admissible_for_one_or_two': has and malefics_third <= 2 and planets_eleventh > 0,
        'BPHS_TRANSLATED_viparita_argala_3plus': malefics_third >= 3,
        'BPHS_SANSKRIT_exact_three_threshold_verified': False,
        'RATH_VENKATESHA_conflict': has and malefics_third <= 2 and planets_eleventh > 0,
        'score_allowed': False,
    }


def node_reference_versions(reference: int, node: Literal['RAHU', 'KETU']) -> dict:
    if node not in ('RAHU','KETU'):
        raise ValueError('Node must be RAHU or KETU')
    direct = primary_pairs(reference, reverse=False)
    anti = primary_pairs(reference, reverse=True)
    return {
        'RATH_JAIMINI_SUTRA': anti if node == 'KETU' else direct,
        'BPHS_PORTUGUESE_INTERPRETATION': anti,
        'BPHS_SANSKRIT_31_6_editorial_dispute': 'TAMOGRAHA_REVERSE_SCOPE_UNRESOLVED',
        'variants_disagree': node == 'RAHU',
        'score_allowed': False,
    }


def obstruction_by_count(supporters: int, blockers: int) -> dict:
    if any(not isinstance(x,int) or isinstance(x,bool) or x<0 or x>9 for x in (supporters,blockers)):
        raise ValueError('Integer count 0..9 required')
    return {
        'RATH_equal_bandhana_if_nonempty': supporters == blockers and supporters > 0,
        'VYAKHYA_and_BPHS_fewer_obstructors_ineffective': blockers < supporters,
        'equal_outcome_canonical': None,
        'full_planetary_strength_unverified': True,
        'score_allowed': False,
    }


def caturthamsa_quarter(degree_in_sign: float) -> int:
    if not isinstance(degree_in_sign,(int,float)) or isinstance(degree_in_sign,bool) or not (0 <= degree_in_sign < 30):
        raise ValueError('Synthetic degree must be in [0,30)')
    return int(degree_in_sign//7.5)+1


def opposing_quarter_pair(a: float,b:float) -> bool:
    return caturthamsa_quarter(a)+caturthamsa_quarter(b)==5


@dataclass(frozen=True)
class EpistemicGate:
    raw_printed_original_sanskrit_manuscript_reviewed: bool = False
    edition_reconciled: bool = False
    strengths_defined: bool = False
    natal_or_human_scoring: bool = False

    @property
    def score_allowed(self) -> bool:
        return False
