"""Bounded references for Robbins IV.4; no chart computation or prediction.

RouteEvidence is supplied by a caller who has separately established the
source-specific appearance and culmination conditions. These functions do not
establish those conditions, assign an orb, calculate a phase or rate a person.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping, Sequence
import json

PLANETS = frozenset({'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'})
ACTION_PLANETS = frozenset({'Mars', 'Venus', 'Mercury'})
STATES = frozenset({'QUALIFIED', 'ABSENT', 'UNKNOWN'})
BRANCHES = frozenset({'BASE', 'SATURN_TESTIFIES', 'JUPITER_TESTIFIES', 'SUN_ASPECT', 'WITHOUT_SUN'})
TABLE_PATH = Path(__file__).with_name('EXTERNAL_FORTUNE_TABLES.json')

@dataclass(frozen=True)
class RouteEvidence:
    state: Literal['QUALIFIED', 'ABSENT', 'UNKNOWN']
    planet: str | None = None

    def __post_init__(self) -> None:
        if self.state not in STATES:
            raise ValueError('Unrecognized route-evidence state')
        if self.state == 'QUALIFIED':
            if self.planet not in PLANETS:
                raise ValueError('A qualified route needs one of the five planets')
        elif self.planet is not None:
            raise ValueError('An absent or unknown route cannot assert a planet')


def select_action_references(
    appearance: RouteEvidence,
    culmination: RouteEvidence,
    fallback: RouteEvidence = RouteEvidence('UNKNOWN'),
    *, claim_counts: Mapping[str, int] | None = None,
) -> dict:
    """Reconcile caller-qualified routes, retaining both distinct candidates.

    claim_counts are optional externally established, source-convention-bound
    counts, not inferred weights. They only identify precedence; they never
    delete the other route's planet. Ties stay ties. Missing routes stay unknown.
    """
    if not all(isinstance(x, RouteEvidence) for x in (appearance, culmination, fallback)):
        raise TypeError('Routes must be RouteEvidence instances')
    if claim_counts is not None:
        for planet, value in claim_counts.items():
            if planet not in PLANETS or type(value) is not int or value < 0:
                raise ValueError('Claim counts require recognized planets and nonnegative integers')
    base = {'source_chapter': 'IV.4', 'chart_qualification_performed': False,
            'empirical_validation': False, 'selected': [], 'preferred': None,
            'qualification': 'CALLER_SUPPLIED_NOT_VERIFIED_BY_THIS_HELPER'}
    if 'UNKNOWN' in (appearance.state, culmination.state):
        return {**base, 'status': 'UNRESOLVED_PRIMARY_ROUTE', 'mode': 'ABSTAIN'}
    selected = list(dict.fromkeys(x.planet for x in (appearance, culmination) if x.state == 'QUALIFIED'))
    if not selected:
        if fallback.state != 'QUALIFIED':
            return {**base, 'status': 'UNRESOLVED_FALLBACK' if fallback.state == 'UNKNOWN' else 'NO_FALLBACK_REFERENCE', 'mode': 'ABSTAIN'}
        return {**base, 'status': 'REFERENCE_SELECTED', 'mode': 'FALLBACK_OCCASIONAL_ONLY',
                'selected': [fallback.planet], 'preferred': fallback.planet,
                'quality_profile_supported': fallback.planet in ACTION_PLANETS}
    preferred = selected[0] if len(selected) == 1 else None
    if len(selected) == 2 and claim_counts is not None and all(p in claim_counts for p in selected):
        a, b = selected
        if claim_counts[a] != claim_counts[b]:
            preferred = a if claim_counts[a] > claim_counts[b] else b
    return {**base, 'status': 'REFERENCE_SELECTED', 'mode': 'PRIMARY_SINGLE' if len(selected) == 1 else 'PRIMARY_DUAL',
            'selected': selected, 'preferred': preferred,
            'quality_profile_supported': all(p in ACTION_PLANETS for p in selected)}


def action_branch_reference(rulers: Sequence[str], branch: str, *, topical_qualified: bool | None) -> dict:
    """Retrieve a single source row after caller-declared topical qualification.

    The branch label also represents caller-established branch conditions.
    This does not infer a solar aspect or testimony, merge branches, or map
    historical labels onto a contemporary occupation or identity.
    """
    if isinstance(rulers, (str, bytes)) or not rulers:
        raise ValueError('Supply a nonempty sequence of planet names')
    rulers = tuple(rulers)
    if any(p not in PLANETS for p in rulers) or len(set(rulers)) != len(rulers):
        raise ValueError('Only distinct recognized planets are accepted')
    if branch not in BRANCHES:
        raise ValueError('Unrecognized source-branch label')
    if topical_qualified is not None and type(topical_qualified) is not bool:
        raise ValueError('Topical qualification must be True, False or None')
    result = {'source_chapter': 'IV.4', 'records': [], 'chart_qualification_performed': False,
              'empirical_validation': False, 'branch_conditions': 'CALLER_SUPPLIED'}
    if topical_qualified is None:
        return {**result, 'status': 'UNRESOLVED_TOPICAL_QUALIFICATION'}
    if topical_qualified is False:
        return {**result, 'status': 'NOT_APPLICABLE'}
    if len(rulers) > 2 or not set(rulers).issubset(ACTION_PLANETS):
        return {**result, 'status': 'UNSPECIFIED_RULER_COMBINATION'}
    data = json.loads(TABLE_PATH.read_text())
    rows = [r for r in data['occupation_branches'] if set(r['rulers']) == set(rulers) and r['branch'] == branch]
    return {**result, 'status': 'SOURCE_ROW' if rows else 'UNSPECIFIED_BRANCH', 'records': rows}
