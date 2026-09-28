from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from hdmatch.empirical_astrology import (
    CohortEntities,
    FreezeManifestError,
    ensure_disjoint_cohorts,
    holm_family,
    require_exact_diagnostic_family,
    validate_freeze_manifest,
)
from hdmatch.empirical_astrology.protocol import FREEZE_MANIFEST_REQUIRED_FIELDS


def _manifest() -> dict[str, object]:
    opening = datetime(2027, 1, 1, tzinfo=UTC)
    manifest: dict[str, object] = {
        field: "0" * 64 if field.endswith("sha256") else "frozen"
        for field in FREEZE_MANIFEST_REQUIRED_FIELDS
    }
    manifest["reviewed_evidence_commit"] = "1" * 64
    manifest["software_commit"] = "2" * 64
    manifest["freeze_timestamp_utc"] = (opening - timedelta(days=1)).isoformat()
    manifest["cohort_opening_utc"] = opening.isoformat()
    manifest["cohort_closing_utc"] = (opening + timedelta(days=30)).isoformat()
    return manifest


def test_freeze_manifest_requires_every_field_and_exact_window() -> None:
    validate_freeze_manifest(_manifest())
    missing = _manifest()
    del missing["pair_registry_sha256"]
    with pytest.raises(FreezeManifestError, match="missing"):
        validate_freeze_manifest(missing)
    wrong_window = _manifest()
    wrong_window["cohort_closing_utc"] = (
        datetime.fromisoformat(str(wrong_window["cohort_opening_utc"])) + timedelta(days=29)
    ).isoformat()
    with pytest.raises(FreezeManifestError, match="30"):
        validate_freeze_manifest(wrong_window)


def test_cross_cohort_overlap_fails_for_each_entity_type() -> None:
    empty = frozenset()
    base = CohortEntities(
        frozenset({"P1"}), frozenset({"F1"}), frozenset({"H1"}), frozenset({"N1"})
    )
    disjoint = CohortEntities(
        frozenset({"P2"}), frozenset({"F2"}), frozenset({"H2"}), frozenset({"N2"})
    )
    ensure_disjoint_cohorts(base, disjoint)
    for candidate in (
        CohortEntities(frozenset({"P1"}), empty, empty, empty),
        CohortEntities(empty, frozenset({"F1"}), empty, empty),
        CohortEntities(empty, empty, frozenset({"H1"}), empty),
        CohortEntities(empty, empty, empty, frozenset({"N1"})),
    ):
        with pytest.raises(ValueError, match="overlap"):
            ensure_disjoint_cohorts(base, candidate)


def test_holm_family_preserves_order_and_exact_21_test_gate() -> None:
    results = holm_family([0.001, 0.03, 0.2])
    assert [result.original_index for result in results] == [0, 1, 2]
    assert results[0].rejected is True
    assert results[2].rejected is False
    assert len(require_exact_diagnostic_family([1.0] * 21)) == 21
    with pytest.raises(ValueError, match="21"):
        require_exact_diagnostic_family([1.0] * 20)
