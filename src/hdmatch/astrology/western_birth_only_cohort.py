"""Deterministic, event-inaccessible roster partition for retrospective pilot.

Consumes *birth metadata only* from a later separately authorized parser.
Never opens Astro-Databank <events> or exposes real people in Git. A high-
entropy private key is required to generate irreversibly labelled roster IDs.
The free C initial-name sample is nonrepresentative of the wider population.
"""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Sequence
from dataclasses import dataclass

ROSTER_SEED = "ADB-C-FREE-2026-BIRTH-ONLY-DEVELOPMENT-SPLIT-V0"
EXPECTED_SOURCE_KIND = "Public Figure"


@dataclass(frozen=True)
class BirthOnlyMetadata:
    """No field can hold names, occupations, events, ratings of behavior."""

    source_record_id: int
    rodden_rating: str
    birth_year: int
    source_data_kind: str
    exact_birth_time_verified: bool
    normalized_utc_and_location_available: bool

    def __post_init__(self) -> None:
        if type(self.source_record_id) is not int or self.source_record_id <= 0:
            raise ValueError("valid source integer record ID required")
        if not 1500 <= self.birth_year <= 2500:
            raise ValueError("birth year outside declared source metadata domain")
        if self.rodden_rating not in ("AA", "A", "B", "C", "DD", "X", "XX"):
            raise ValueError("invalid Rodden rating category")


@dataclass(frozen=True)
class SelectionResult:
    """Pseudo-ID rosters returned privately; never committed as source data."""

    cohort_source_sha256: str
    selected_total: int
    development_pseudonyms: tuple[str, ...]
    untouched_candidate_pseudonyms: tuple[str, ...]
    excluded_by_reason: tuple[tuple[str, int], ...]
    status: str = "BIRTH_ONLY_NOT_HUMAN_PREDICTION_VALIDATION"


def select_birth_only_rosters(
    birth_only: Sequence[BirthOnlyMetadata],
    *,
    source_file_sha256: str,
    pseudonymization_secret: bytes,
) -> SelectionResult:
    """Selection/split uses NO life-event occurrence, outcome or career data.

    Public deterministic 20% development / 80% untouched-candidate split is
    derived solely from stable source integer ID. The 'untouched' designation
    is a PLAN, not evidence that anyone has independently sequestered answers.
    """
    if len(source_file_sha256) != 64 or any(
        c not in "0123456789abcdef" for c in source_file_sha256
    ):
        raise ValueError("exact immutable source archive hash required")
    if not isinstance(pseudonymization_secret, bytes) or len(pseudonymization_secret) < 32:
        raise ValueError("high-entropy external pseudonymization secret required")
    ids = [p.source_record_id for p in birth_only]
    if len(set(ids)) != len(ids):
        raise ValueError("one source record per stable source integer ID")
    accepted_dev: list[str] = []
    accepted_holdout: list[str] = []
    excluded: dict[str, int] = {}
    for person in sorted(birth_only, key=lambda x: x.source_record_id):
        if person.source_data_kind != EXPECTED_SOURCE_KIND:
            reason = "NON_PUBLIC_RECORD"
        elif person.rodden_rating != "AA":
            reason = "NOT_AA_DOCUMENTED_TIME"
        elif not 1800 <= person.birth_year < 2000:
            reason = "OUTSIDE_PINNED_ADULT_STUDY_BIRTH_RANGE"
        elif not (
            person.exact_birth_time_verified and person.normalized_utc_and_location_available
        ):
            reason = "BIRTH_TIME_OR_UTC_LOCATION_UNRESOLVED"
        else:
            reason = ""
        if reason:
            excluded[reason] = excluded.get(reason, 0) + 1
            continue
        stable = f"{ROSTER_SEED}:{person.source_record_id}".encode()
        fingerprint = hmac.new(pseudonymization_secret, stable, hashlib.sha256).hexdigest()
        pseudonym = "ADB-C-" + fingerprint[:20]
        # Publicly declared split does not use outcome categories or dates.
        group = int(hashlib.sha256(stable).hexdigest()[:8], 16) % 5
        if group == 0:
            accepted_dev.append(pseudonym)
        else:
            accepted_holdout.append(pseudonym)
    return SelectionResult(
        cohort_source_sha256=source_file_sha256,
        selected_total=len(accepted_dev) + len(accepted_holdout),
        development_pseudonyms=tuple(accepted_dev),
        untouched_candidate_pseudonyms=tuple(accepted_holdout),
        excluded_by_reason=tuple(sorted(excluded.items())),
    )
