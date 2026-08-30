"""Emit a canonical synthetic-only checkpoint-2 foundation audit."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from hdmatch.natal_time.enumerator import enumerate_manifest
from hdmatch.natal_time.evidence import assess_evidence
from hdmatch.natal_time.models import (
    DateEvidence,
    DocumentaryVerification,
    EvidenceLineage,
    EvidenceSource,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayEvidence,
)
from hdmatch.natal_time.provenance import (
    build_engine_provenance,
    full_state_identity_specification,
    synthetic_runtime_digest,
)
from hdmatch.natal_time.public import serialize_synthetic_public_artifact
from hdmatch.natal_time.records import (
    FixtureClassification,
    NatalTimeFreeze,
    NatalTimeManifest,
    TimezoneResolution,
    deterministic_computation_sha256,
)
from hdmatch.natal_time.synthetic import SyntheticAnalyticEphemerisProvider
from hdmatch.util import canonical_json_bytes, sha256_json

CREATED_AT = datetime(2026, 8, 30, 3, 0, tzinfo=UTC)
FIXTURES = (
    ("ordinary", date(2024, 1, 15), "UTC", 24),
    ("leap_day", date(2024, 2, 29), "UTC", 24),
    ("dst_gap", date(2024, 3, 10), "America/New_York", 23),
    ("dst_fold", date(2024, 11, 3), "America/New_York", 25),
    ("historical_offset", date(2014, 10, 26), "Europe/Moscow", 25),
)


def _fixed_id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:024X}"


def _fixture(
    index: int,
    name: str,
    civil_date: date,
    timezone: str,
    expected_hours: int,
    *,
    repository_root: Path,
    repository_commit: str,
) -> tuple[dict[str, object], NatalTimeManifest, NatalTimeFreeze, object, object]:
    provider = SyntheticAnalyticEphemerisProvider()
    lineage = EvidenceLineage(
        lineage_id=_fixed_id("NTL", index),
        version=1,
        date_evidence=(
            DateEvidence(
                evidence_id=_fixed_id("NTE", index * 10 + 1),
                asserted_date=civil_date,
                source=EvidenceSource.MEMORY,
                documentary_verification=DocumentaryVerification.NOT_APPLICABLE,
                entered_at_utc=CREATED_AT,
                entered_how="conspicuously_synthetic_audit_fixture",
            ),
        ),
        weekday_evidence=WeekdayEvidence(
            evidence_id=_fixed_id("NTE", index * 10 + 2),
            answer_status=WeekdayAnswerStatus.REMEMBERED,
            asserted_weekday=Weekday.from_date(civil_date),
            entered_at_utc=CREATED_AT,
            entered_how="conspicuously_synthetic_audit_fixture",
            locked_at_utc=CREATED_AT,
            server_lock_sequence=index,
        ),
    )
    assessment = assess_evidence(lineage)
    provenance = build_engine_provenance(
        provider,
        repository_commit=repository_commit,
        dependency_lock_path=repository_root / "requirements-dev.lock",
        runtime_or_container_sha256=synthetic_runtime_digest("foundation-audit-v1"),
        iana_timezone=timezone,
    )
    identity = full_state_identity_specification()
    manifest = NatalTimeManifest(
        manifest_id=_fixed_id("NTM", index),
        created_at_utc=CREATED_AT,
        evidence_lineage_sha256=lineage.content_sha256,
        candidate_dates=assessment.operative_dates,
        timezone_resolution=TimezoneResolution(
            iana_timezone=timezone,
            resolution_method="conspicuously_synthetic_explicit_fixture",
            participant_confirmed=True,
            timezone_database_version=provenance.timezone_database_version,
            timezone_file_sha256=provenance.timezone_file_sha256,
        ),
        engine_provenance=provenance,
        state_identity_specification=identity,
        state_identity_sha256=identity.content_sha256,
        fixture_classification=FixtureClassification.SYNTHETIC,
    )
    freeze = NatalTimeFreeze(
        freeze_id=_fixed_id("NTF", index),
        created_at_utc=CREATED_AT,
        manifest_sha256=manifest.content_sha256,
        deterministic_computation_sha256=deterministic_computation_sha256(manifest),
        repository_commit=repository_commit,
        engine_provenance_sha256=provenance.content_sha256,
        state_identity_sha256=identity.content_sha256,
    )
    result = enumerate_manifest(provider, manifest, freeze)
    public = serialize_synthetic_public_artifact(
        manifest,
        result,
        independent_public_id=_fixed_id("NTP", index),
    )
    receipt = result.coverage_receipts[0]
    actual_hours = receipt.actual_duration_microseconds / 3_600_000_000
    if actual_hours != expected_hours:
        raise RuntimeError(f"{name} duration mismatch: {actual_hours} != {expected_hours}")
    summary: dict[str, object] = {
        "name": name,
        "synthetic": True,
        "civil_date": civil_date.isoformat(),
        "iana_timezone": timezone,
        "expected_hours": expected_hours,
        "manifest_sha256": manifest.content_sha256,
        "freeze_sha256": freeze.content_sha256,
        "result_sha256": result.content_sha256,
        "public_artifact_sha256": sha256_json(public.model_dump(mode="json")),
        "coverage_receipt": receipt.model_dump(mode="json"),
        "ranking_present": result.ranking_present,
        "weights_present": result.weights_present,
        "probability_present": result.probability_present,
        "relationship_evidence_included": result.relationship_evidence_included,
    }
    return summary, manifest, freeze, result, public


def build_audit(repository_root: Path, repository_commit: str) -> dict[str, object]:
    summaries: list[dict[str, object]] = []
    sample_objects: dict[str, object] | None = None
    for index, fixture in enumerate(FIXTURES, start=1):
        summary, manifest, freeze, result, public = _fixture(
            index,
            *fixture,
            repository_root=repository_root,
            repository_commit=repository_commit,
        )
        summaries.append(summary)
        if sample_objects is None:
            sample_objects = {
                "manifest": manifest.model_dump(mode="json"),
                "manifest_sha256": manifest.content_sha256,
                "freeze": freeze.model_dump(mode="json"),
                "freeze_sha256": freeze.content_sha256,
                "result": result.model_dump(mode="json"),
                "result_sha256": result.content_sha256,
                "public_allowlist_artifact": public.model_dump(mode="json"),
                "public_allowlist_artifact_sha256": sha256_json(public.model_dump(mode="json")),
            }
    identity = full_state_identity_specification()
    payload: dict[str, object] = {
        "schema_version": "natal-time-foundation-audit-v1",
        "synthetic_only": True,
        "claim_scope": (
            "deterministic evidence transitions, candidate-complete interval coverage, "
            "immutability, and public-boundary mechanics only; no human calibration"
        ),
        "repository_commit": repository_commit,
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "state_identity_specification": identity.model_dump(mode="json"),
        "state_identity_sha256": identity.content_sha256,
        "fixtures": summaries,
        "sample_objects": sample_objects or {},
        "forbidden_semantics": {
            "rank": False,
            "weight": False,
            "score": False,
            "probability": False,
            "duration_mass": False,
            "stopping_rule": False,
            "time_window_recommendation": False,
            "relationship_evidence": False,
        },
    }
    payload["audit_sha256"] = sha256_json(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-commit", required=True)
    args = parser.parse_args()
    sys.stdout.buffer.write(
        canonical_json_bytes(
            build_audit(args.repository_root.resolve(strict=True), args.repository_commit)
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
