"""Invented Astro-Databank-like birth-only metadata selection tests.

No source archive, real record ID, occupation or event node is opened.
"""

from __future__ import annotations

import pytest

from hdmatch.astrology.western_birth_only_cohort import (
    BirthOnlyMetadata,
    select_birth_only_rosters,
)


def fake(index: int, **overrides) -> BirthOnlyMetadata:
    data = {
        "source_record_id": 1000000 + index,
        "rodden_rating": "AA",
        "birth_year": 1950 + index % 30,
        "source_data_kind": "Public Figure",
        "exact_birth_time_verified": True,
        "normalized_utc_and_location_available": True,
    }
    data.update(overrides)
    return BirthOnlyMetadata(**data)


def choose(records, key: bytes = b"S" * 32):
    return select_birth_only_rosters(
        records,
        source_file_sha256="a" * 64,
        pseudonymization_secret=key,
    )


def test_split_is_order_invariant_independent_of_any_events() -> None:
    entries = [fake(i) for i in range(100)]
    result = choose(entries)
    reversed_order = choose(list(reversed(entries)))
    assert result == reversed_order
    assert result.selected_total == 100
    assert len(result.development_pseudonyms) > 0
    assert len(result.untouched_candidate_pseudonyms) > 0
    assert len(result.development_pseudonyms) + len(result.untouched_candidate_pseudonyms) == 100
    assert result.status == "BIRTH_ONLY_NOT_HUMAN_PREDICTION_VALIDATION"
    assert len(set((*result.development_pseudonyms, *result.untouched_candidate_pseudonyms))) == 100


def test_only_documented_public_aa_birth_inputs_accepted() -> None:
    records = [
        fake(1),
        fake(2, rodden_rating="A"),
        fake(3, source_data_kind="Private Person"),
        fake(4, birth_year=1700),
        fake(5, exact_birth_time_verified=False),
        fake(6, normalized_utc_and_location_available=False),
    ]
    result = choose(records)
    assert result.selected_total == 1
    assert dict(result.excluded_by_reason) == {
        "BIRTH_TIME_OR_UTC_LOCATION_UNRESOLVED": 2,
        "NON_PUBLIC_RECORD": 1,
        "NOT_AA_DOCUMENTED_TIME": 1,
        "OUTSIDE_PINNED_ADULT_STUDY_BIRTH_RANGE": 1,
    }


def test_pseudonyms_depend_on_private_secret_not_plain_db_id() -> None:
    records = [fake(1), fake(2), fake(3)]
    a = choose(records, b"A" * 32)
    b = choose(records, b"B" * 32)
    assert a.selected_total == b.selected_total == 3
    assert set((*a.development_pseudonyms, *a.untouched_candidate_pseudonyms)) != set(
        (*b.development_pseudonyms, *b.untouched_candidate_pseudonyms)
    )


def test_refuse_duplicate_ids_invalid_birth_and_short_key() -> None:
    with pytest.raises(ValueError, match="one source record"):
        choose([fake(1), fake(1)])
    with pytest.raises(ValueError, match="high-entropy"):
        choose([fake(1)], b"short")
    with pytest.raises(ValueError, match="hash"):
        select_birth_only_rosters(
            [fake(1)], source_file_sha256="NOT-A-HASH", pseudonymization_secret=b"S" * 32
        )
    with pytest.raises(ValueError, match="year"):
        fake(7, birth_year=1000)
    with pytest.raises(ValueError, match="rating"):
        fake(7, rodden_rating="invented")
