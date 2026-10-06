"""Bounded source-definition fragments for Ptolemy III.1–III.5.

Not a natal rectifier or predictive engine. All examples/tests are synthetic.
The counting helper checks FIVE distinct forms, not weighted Lilly dignities.
The astronomy needed to supply syzygies, visibility, rulers and angles is NOT
implemented here; ambiguous source interpretations remain in the source ledger.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
import math
from typing import Literal

Tri = bool | None
FORM_KEYS = frozenset({'trine', 'house', 'exaltation', 'term', 'phase', 'aspect'})
FIVE_FORMS = ('trine', 'house', 'exaltation', 'term', 'phase_or_aspect')


def _tri(value: Tri) -> Tri:
    if value is not None and type(value) is not bool:
        raise ValueError('A relation must be True, False, or None; numbers are not evidence.')
    return value


def tri_or(left: Tri, right: Tri) -> Tri:
    """Inclusive OR without converting unresolved evidence into false."""
    left, right = _tri(left), _tri(right)
    if left is True or right is True:
        return True
    if left is None or right is None:
        return None
    return False


def count_distinct_forms(relations: Mapping[str, Tri]) -> tuple[int, int]:
    """Lower/upper supported counts; phase OR aspect contributes at most one.

    Calling these counts a source-weighted score, probability, or a complete
    topical ruler selection would exceed this fixture's scope.
    """
    if set(relations) != FORM_KEYS:
        raise ValueError('Supply the six raw checks for five forms; no face/decan substitution.')
    values = [_tri(relations[key]) for key in FIVE_FORMS[:-1]]
    values.append(tri_or(relations['phase'], relations['aspect']))
    lower = sum(v is True for v in values)
    return lower, lower + sum(v is None for v in values)


def possible_maximal_claimants(candidates: Mapping[str, Mapping[str, Tri]]) -> dict:
    """Conservative count comparison, not the complete source judgement.

    Unknown evidence may preserve several possibilities. Source-specific power,
    proximity, centre/sect and synthesis decisions are intentionally not invented.
    """
    if not candidates or any(not isinstance(k, str) or not k.strip() for k in candidates):
        raise ValueError('At least one named candidate is required.')
    ranges = {name: count_distinct_forms(row) for name, row in candidates.items()}
    best_lower = max(lo for lo, hi in ranges.values())
    possible = sorted(name for name, (lo, hi) in ranges.items() if hi > 0 and hi >= best_lower)
    if not possible:
        return {'status': 'NO_SUPPORTED_FORM', 'candidates': [], 'ranges': ranges}
    all_known = all(lo == hi for lo, hi in ranges.values())
    status = ('COUNT_UNIQUE' if len(possible) == 1 else 'COUNT_TIE') if all_known else 'UNRESOLVED_COUNTS'
    return {'status': status, 'candidates': possible, 'ranges': ranges}


@dataclass(frozen=True)
class Syzygy:
    event_id: str
    instant: datetime
    kind: Literal['NEW_MOON', 'FULL_MOON']


def latest_preceding_syzygy(events: Sequence[Syzygy], birth: datetime) -> dict:
    """Order supplied exact event instants, without solving astronomical roots.

    The exact-coincident case is unresolved: the passage says 'preceding' but
    does not supply a same-instant policy. No rounding or arbitrarily selected
    future event is used.
    """
    if not isinstance(birth, datetime) or birth.utcoffset() is None:
        raise ValueError('Birth must be a timezone-aware instant.')
    ids = set()
    for event in events:
        if not isinstance(event, Syzygy) or not event.event_id or event.event_id in ids:
            raise ValueError('Events must have distinct nonempty identifiers.')
        ids.add(event.event_id)
        if event.kind not in {'NEW_MOON', 'FULL_MOON'}:
            raise ValueError('The source admits a conjunction or opposition, not any lunar phase.')
        if not isinstance(event.instant, datetime) or event.instant.utcoffset() is None:
            raise ValueError('Event instants must be timezone-aware.')
    simultaneous = [e for e in events if e.instant == birth]
    prior = [e for e in events if e.instant < birth]
    nearest = max((e.instant for e in prior), default=None)
    selected = [e for e in prior if e.instant == nearest]
    if simultaneous:
        return {'status': 'UNRESOLVED_AT_BIRTH', 'selected': [],
                'preceding_candidates': sorted(e.event_id for e in selected),
                'simultaneous_candidates': sorted(e.event_id for e in simultaneous)}
    if not selected:
        return {'status': 'NO_PRECEDING_EVENT_SUPPLIED', 'selected': []}
    if len(selected) > 1:
        return {'status': 'CONFLICTING_PRECEDING_EVENTS', 'selected': [],
                'conflicting_candidates': sorted(e.event_id for e in selected)}
    return {'status': 'SELECTED_PRECEDING', 'selected': [selected[0].event_id]}


def corresponding_degree(planet_longitude: float, admitted_sign: int) -> float:
    """Project continuous [0,30) degree into an ALREADY admitted sign.

    A computational convention for the explicit fragment, not an interpretation
    of every ordinal degree, a sign selection, or birth-time inversion.
    """
    if isinstance(planet_longitude, bool) or not isinstance(planet_longitude, (float, int)):
        raise ValueError('Longitude must be numerical.')
    if not math.isfinite(planet_longitude) or not 0 <= planet_longitude < 360:
        raise ValueError('Longitude must be finite and normalized to [0,360).')
    if type(admitted_sign) is not int or not 0 <= admitted_sign < 12:
        raise ValueError('The separately admitted sign index must be 0..11.')
    return 30 * admitted_sign + planet_longitude % 30


def parent_significators(parent: str, sect: str | None) -> dict:
    """III.4: preserve the natural pair; sect selects a preference, not erasure."""
    if parent not in {'father', 'mother'} or sect not in {'DAY', 'NIGHT', None}:
        raise ValueError('Use father/mother and DAY/NIGHT/None.')
    natural = {'father': ['SUN', 'SATURN'], 'mother': ['MOON', 'VENUS']}
    focus = {'father': {'DAY': 'SUN', 'NIGHT': 'SATURN'},
             'mother': {'DAY': 'VENUS', 'NIGHT': 'MOON'}}
    return {'natural_pair': natural[parent], 'sect_focus': focus[parent].get(sect),
            'status': 'DEFINED_SOURCE_FOCUS' if sect else 'UNRESOLVED_SECT_FOCUS'}


def major_topic_eligibility(original_familiarity: Tri) -> str:
    """III.4 'no great influence' is not 'no conceivable influence'."""
    value = _tri(original_familiarity)
    return ('ELIGIBLE_FOR_FURTHER_TOPIC_ANALYSIS' if value is True else
            'NOT_ADMITTED_AS_MAJOR_TOPIC_CAUSE' if value is False else
            'UNRESOLVED_ORIGINAL_FAMILIARITY')
