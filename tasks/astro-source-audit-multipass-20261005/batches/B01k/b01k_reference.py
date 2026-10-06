"""Bounded IV.5-IV.6 source references, not a natal prediction engine.

Geometric phase labels follow the declared English convention only. All
interpretive lookups require caller-established eligibility. Historical
sexual-role claims are not exposed through a classifier.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from typing import Iterable

DATA = json.loads(Path(__file__).with_name('RELATIONSHIP_FAMILY_TABLES.json').read_text())
PLANETS = frozenset({'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'})


def _truth(value: bool | None) -> bool | None:
    if value is not None and type(value) is not bool:
        raise TypeError('Condition must be True, False, or None (unknown).')
    return value


def _all(*values: bool | None) -> bool | None:
    for value in values:
        _truth(value)
    return False if False in values else None if None in values else True


def _any(*values: bool | None) -> bool | None:
    for value in values:
        _truth(value)
    return True if True in values else None if None in values else False


def lunar_phase_quadrant(elongation_deg: float, *, body: str = 'Moon') -> dict:
    """Classify *directed* Sun-to-Moon elongation; do not reuse for the Sun.

    Exact phase boundaries abstain. No empirical/rounding tolerance is invented.
    Inputs are angular differences, not dates, houses or inferred relationships.
    """
    if body != 'Moon':
        raise ValueError('IV.5 solar quadrants require a horizon reference, not lunar elongation.')
    if isinstance(elongation_deg, bool) or not isinstance(elongation_deg, (int, float)):
        raise TypeError('Elongation must be a finite number of degrees.')
    if not math.isfinite(elongation_deg):
        raise ValueError('Elongation must be finite.')
    angle = elongation_deg % 360.0
    if angle in {0.0, 90.0, 180.0, 270.0}:
        label = 'UNRESOLVED_EXACT_PHASE_BOUNDARY'
    else:
        label = 'EASTERN' if 0 < angle < 90 or 180 < angle < 270 else 'WESTERN'
    return {'quadrant': label, 'directed_elongation_deg': angle,
            'frame': 'LUNAR_PHASE_NOT_NATAL_HOUSE',
            'source_ref': DATA['quadrants']['Moon']['rule_ref']}


def spouse_reference(native_branch: str, planet: str, *, qualified: bool | None) -> dict:
    """Retrieve a historical spouse-description row, not the native's character."""
    if native_branch not in DATA['spouse_profiles']:
        raise ValueError('Use a declared historical source branch, male_native or female_native.')
    if planet not in PLANETS:
        raise ValueError('Unknown planet name.')
    _truth(qualified)
    if qualified is None:
        return {'status': 'UNRESOLVED_QUALIFICATION', 'rows': []}
    if not qualified:
        return {'status': 'NOT_APPLICABLE', 'rows': []}
    row = DATA['spouse_profiles'][native_branch].get(planet)
    if row is None:
        return {'status': 'NO_LISTED_SOURCE_PROFILE', 'rows': []}
    return {'status': 'CALLER_QUALIFIED_SOURCE_REFERENCE', 'rows': [row]}


def relationship_reference(geometry: str | None, *, benefic: bool | None,
                           malefic: bool | None, cross_chart_qualified: bool | None) -> dict:
    """Return all supported cells; mixed/unknown testimony never becomes a score."""
    if geometry not in {None, 'HARMONIOUS', 'INHARMONIOUS'}:
        raise ValueError('Geometry must be source-qualified HARMONIOUS, INHARMONIOUS, or None.')
    for value in [benefic, malefic, cross_chart_qualified]:
        _truth(value)
    if cross_chart_qualified is False:
        return {'status': 'NOT_APPLICABLE', 'rows': []}
    if cross_chart_qualified is None or geometry is None:
        return {'status': 'UNRESOLVED_QUALIFICATION', 'rows': []}
    rows = [DATA['relationship_continuity_quality'][f'{geometry}:{group}']
            for group, flag in [('BENEFIC', benefic), ('MALEFIC', malefic)] if flag is True]
    if benefic is True and malefic is True:
        status = 'UNRESOLVED_MIXED_TESTIMONY'
    elif benefic is None or malefic is None:
        status = 'PARTIAL_KNOWN_SUPPORT_OTHER_TESTIMONY_UNKNOWN' if rows else 'UNRESOLVED_TESTIMONY'
    elif rows:
        status = 'CALLER_QUALIFIED_SOURCE_REFERENCE'
    else:
        status = 'BASELINE_ONLY_NO_TESTIMONY_MODIFIER'
    return {'status': status, 'rows': rows,
            'baseline_geometry': geometry, 'probability': None}


def _planet_set(items: Iterable[str] | None) -> list[str] | None:
    if items is None:
        return None
    if isinstance(items, (str, bytes)):
        raise TypeError('Use a collection of planet names, or None for unknown.')
    values = list(items)
    if any(not isinstance(v, str) or v not in PLANETS for v in values):
        raise ValueError('Unknown planet name in collection.')
    return sorted(set(values))


def children_reference_route(primary: Iterable[str] | None,
                             opposite: Iterable[str] | None) -> dict:
    """Reconcile already-qualified planet sets, not house/angle astronomy."""
    primary, opposite = _planet_set(primary), _planet_set(opposite)
    if primary is None:
        return {'status': 'UNRESOLVED_PRIMARY', 'planets': []}
    if primary:
        return {'status': 'PRIMARY', 'planets': primary}
    if opposite is None:
        return {'status': 'UNRESOLVED_FALLBACK', 'planets': []}
    return {'status': 'OPPOSITE_FALLBACK' if opposite else 'NO_QUALIFYING_SOURCE_PLANET',
            'planets': opposite}


def children_group(planet: str) -> dict:
    """Topic vocabulary only; not general sect, benefic status or fertility advice."""
    if planet not in PLANETS:
        raise ValueError('Unknown planet name.')
    group = next(k for k, members in DATA['children']['groups'].items() if planet in members)
    return {'planet': planet, 'group': group,
            'scope': 'IV.6_CHILDREN_NOT_DIURNAL_NOCTURNAL_SECT',
            'source_ref': DATA['children']['group_rule_ref']}


def multiplicity_reference_flags(*, donor_qualified: bool | None, alone: bool | None,
                                 bicorporeal: bool | None, feminine: bool | None,
                                 fecund: bool | None) -> dict:
    """Preserve AND/OR and co-triggering in the declared English wording.

    This checks supplied predicates only, without giving a child count for a
    person. Both branches can be true; no source priority is invented.
    """
    for flag in [donor_qualified, alone, bicorporeal, feminine, fecund]:
        _truth(flag)
    one = _all(donor_qualified, alone)
    multiple = _all(donor_qualified, _any(_all(bicorporeal, feminine), fecund))
    if one is True and multiple is True:
        status = 'UNRESOLVED_CO_TRIGGERED_SOURCE_CLAUSES'
    elif one is None or multiple is None:
        status = 'PARTLY_UNRESOLVED_PREDICATES'
    else:
        status = 'PREDICATE_FLAGS_ONLY'
    return {'status': status, 'single_clause_supported': one,
            'multiple_clause_supported': multiple, 'exact_child_count': None}
