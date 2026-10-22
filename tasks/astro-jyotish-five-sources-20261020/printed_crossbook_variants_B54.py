"""Diagnostic-only source variants of classical Jyotish texts.

Not a birth-chart engine. No natal chart, ephemeris, human outcome, evidence score,
production rule or modern occupation prediction is calculated here.
"""
from dataclasses import dataclass
from typing import Literal

ClaimScope = Literal['SOURCE_ONLY_NO_SCORE']

@dataclass(frozen=True)
class Wording:
    family: str
    witness: str
    printed_verse: str
    electronic_verse: str | None
    predicate: str
    result_class: str
    scope: ClaimScope = 'SOURCE_ONLY_NO_SCORE'

    def __post_init__(self):
        if self.scope != 'SOURCE_ONLY_NO_SCORE':
            raise ValueError('Predictive promotion forbidden')
        if not self.witness or not self.family:
            raise ValueError('Witness and family are required')


def nonidentical_predicate_witnesses(*, synthetic: bool, with_saturn: bool,
                                    eighth_lord_conjoined: bool,
                                    eighth_lord_aspects: bool,
                                    cruel_varga_or_angle: bool) -> dict:
    """Illustrative Boolean independence; actual lord computation intentionally absent."""
    if not synthetic:
        raise ValueError('Synthetic-only source-fidelity diagnostic')
    if any(type(x) is not bool for x in (with_saturn, eighth_lord_conjoined,
                                        eighth_lord_aspects, cruel_varga_or_angle)):
        raise TypeError('Require explicit symbolic Boolean predicates')
    common = with_saturn and cruel_varga_or_angle
    return {
        'sarvartha_1929_conjunction_version': common and eighth_lord_conjoined,
        'jataka_1922_aspect_version': common and eighth_lord_aspects,
        'canonical_rule_selected': None,
        'score_allowed': False,
    }


def edition_verse_alignment(printed_verse: str, electronic_verse: str,
                            *, same_sanskrit_lemma_verified: bool) -> dict:
    if not printed_verse or not electronic_verse:
        raise ValueError('Verse labels must be supplied')
    return {
        'printed_verse': printed_verse,
        'electronic_verse': electronic_verse,
        'same_clause_recognized': bool(same_sanskrit_lemma_verified),
        'global_offset_assumed': False,
        'score_allowed': False,
    }


def occupational_disjunction(labels: tuple[str, ...], *, synthetic: bool) -> dict:
    """Reports claim breadth, never recalibrates a broad OR as a single hit."""
    if not synthetic or not labels:
        raise ValueError('Synthetic-only and nonempty labels required')
    if any(not isinstance(x, str) or not x.strip() for x in labels):
        raise ValueError('Nonblank labels only')
    categories = sorted(set(labels))
    return {
        'distinct_possible_categories': len(categories),
        'categories': categories,
        'unique_occupation_prediction': len(categories) == 1,
        'probabilities_estimated': False,
        'prediction_allowed': False,
    }


def income_source_vs_occupation(*, wealth_provider: str, job_sector: str) -> dict:
    if not wealth_provider or not job_sector:
        raise ValueError('Source-of-funds and work sector are separate')
    return {
        'wealth_provider': wealth_provider,
        'job_sector': job_sector,
        'same_observable': False,
        'independent_prediction_confirmations': 0,
    }


def textual_dependency(verse_a: Wording, verse_b: Wording,
                       *, shared_substantial_wording: bool) -> dict:
    if verse_a.family != verse_b.family:
        raise ValueError('Cannot assign shared source family without evidence')
    return {
        'source_family': verse_a.family,
        'shared_transmitted_pattern': bool(shared_substantial_wording),
        'wording_identical': verse_a.predicate == verse_b.predicate,
        'copying_direction_proven': False,
        'independent_human_confirmations': 0,
        'score_allowed': False,
    }
