from __future__ import annotations

import asyncio
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest
from fastapi import FastAPI
from pydantic import ValidationError
from starlette.types import Message, Scope

from hdmatch.api.natal_time_app import create_natal_time_app
from hdmatch.natal_time.enumerator import (
    _validated_civil_date_domain,
    derive_mechanic_facts,
    enumerate_manifest,
)
from hdmatch.natal_time.evidence import assess_evidence
from hdmatch.natal_time.models import (
    CandidateDateSetEvidence,
    DateEvidence,
    DocumentaryVerification,
    EvidenceLineage,
    EvidenceSource,
    EvidenceState,
    Weekday,
    WeekdayAnswerStatus,
    WeekdayEvidence,
)
from hdmatch.natal_time.provenance import (
    build_engine_provenance,
    default_activation_field_count,
    full_state_identity_specification,
    synthetic_runtime_digest,
    timezone_file_sha256,
)
from hdmatch.natal_time.public import (
    SyntheticPublicNatalTimeArtifact,
    serialize_synthetic_public_artifact,
)
from hdmatch.natal_time.records import (
    FixtureClassification,
    MechanicStatus,
    NatalTimeManifest,
    TimezoneResolution,
)
from hdmatch.natal_time.service import NatalTimeIntakeService
from hdmatch.natal_time.store import NatalTimePrivateStore
from hdmatch.natal_time.synthetic import SyntheticAnalyticEphemerisProvider
from hdmatch.natal_time.workflow import create_freeze, create_manifest

PROJECT_ROOT = Path(__file__).parents[2]
NOW = datetime(2026, 8, 30, 2, 0, tzinfo=UTC)


def _id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:024X}"


def _lineage(
    *,
    asserted_date: date = date(2000, 1, 3),
    source: EvidenceSource = EvidenceSource.MEMORY,
    verification: DocumentaryVerification = DocumentaryVerification.NOT_APPLICABLE,
    weekday_status: WeekdayAnswerStatus = WeekdayAnswerStatus.REMEMBERED,
    weekday: Weekday | None = Weekday.MONDAY,
    extra_dates: tuple[DateEvidence, ...] = (),
    candidate_dates: tuple[date, ...] | None = None,
    version: int = 1,
    supersedes: str | None = None,
) -> EvidenceLineage:
    first = DateEvidence(
        evidence_id=_id("NTE", 1),
        asserted_date=asserted_date,
        source=source,
        documentary_verification=verification,
        entered_at_utc=NOW,
        entered_how="synthetic_unit_test",
    )
    all_dates = (first, *extra_dates)
    candidate = None
    if candidate_dates is not None:
        candidate = CandidateDateSetEvidence(
            evidence_id=_id("NTE", 90),
            candidate_dates=candidate_dates,
            declared_date_evidence_ids=tuple(item.evidence_id for item in all_dates),
            confirmed_at_utc=NOW + timedelta(minutes=1),
            confirmed_how="synthetic_unit_test",
        )
    return EvidenceLineage(
        lineage_id=_id("NTL", 1),
        version=version,
        date_evidence=all_dates,
        weekday_evidence=WeekdayEvidence(
            evidence_id=_id("NTE", 2),
            answer_status=weekday_status,
            asserted_weekday=weekday,
            entered_at_utc=NOW,
            entered_how="synthetic_unit_test",
            locked_at_utc=NOW,
            server_lock_sequence=1,
        ),
        candidate_date_set=candidate,
        supersedes_lineage_sha256=supersedes,
    )


@pytest.mark.parametrize(
    ("source", "verification", "status", "weekday", "expected_state", "allowed"),
    [
        (
            EvidenceSource.DOCUMENTARY,
            DocumentaryVerification.PARTICIPANT_REPORTED,
            WeekdayAnswerStatus.NOT_REMEMBERED,
            None,
            EvidenceState.DOCUMENTARY_WEEKDAY_UNAVAILABLE,
            True,
        ),
        (
            EvidenceSource.DOCUMENTARY,
            DocumentaryVerification.INDEPENDENTLY_VERIFIED,
            WeekdayAnswerStatus.REMEMBERED,
            Weekday.MONDAY,
            EvidenceState.DOCUMENTARY_CONCORDANT,
            True,
        ),
        (
            EvidenceSource.DOCUMENTARY,
            DocumentaryVerification.INDEPENDENTLY_VERIFIED,
            WeekdayAnswerStatus.REMEMBERED,
            Weekday.TUESDAY,
            EvidenceState.DOCUMENTARY_WEEKDAY_CONFLICT,
            True,
        ),
        (
            EvidenceSource.MEMORY,
            DocumentaryVerification.NOT_APPLICABLE,
            WeekdayAnswerStatus.UNKNOWN,
            None,
            EvidenceState.MEMORY_DATE_UNVERIFIED,
            True,
        ),
        (
            EvidenceSource.MEMORY,
            DocumentaryVerification.NOT_APPLICABLE,
            WeekdayAnswerStatus.REMEMBERED,
            Weekday.MONDAY,
            EvidenceState.MEMORY_CONCORDANT,
            True,
        ),
        (
            EvidenceSource.MEMORY,
            DocumentaryVerification.NOT_APPLICABLE,
            WeekdayAnswerStatus.REMEMBERED,
            Weekday.TUESDAY,
            EvidenceState.BIRTH_DATE_UNCERTAIN,
            False,
        ),
    ],
)
def test_transition_table_preserves_date_without_manufactured_precision(
    source: EvidenceSource,
    verification: DocumentaryVerification,
    status: WeekdayAnswerStatus,
    weekday: Weekday | None,
    expected_state: EvidenceState,
    allowed: bool,
) -> None:
    lineage = _lineage(
        source=source,
        verification=verification,
        weekday_status=status,
        weekday=weekday,
    )

    assessment = assess_evidence(lineage)

    assert assessment.state is expected_state
    assert assessment.enumeration_allowed is allowed
    assert assessment.operative_dates == (date(2000, 1, 3),)
    assert assessment.date_was_auto_corrected is False
    assert assessment.agreement_adds_precision is False


def test_conflicting_documentary_dates_fail_closed_until_full_set_is_confirmed() -> None:
    second = DateEvidence(
        evidence_id=_id("NTE", 3),
        asserted_date=date(2000, 1, 4),
        source=EvidenceSource.DOCUMENTARY,
        documentary_verification=DocumentaryVerification.PARTICIPANT_REPORTED,
        entered_at_utc=NOW,
        entered_how="synthetic_unit_test",
    )
    lineage = _lineage(
        source=EvidenceSource.DOCUMENTARY,
        verification=DocumentaryVerification.INDEPENDENTLY_VERIFIED,
        extra_dates=(second,),
    )

    assessment = assess_evidence(lineage)

    assert assessment.state is EvidenceState.UNRESOLVED_DOCUMENTARY_CONFLICT
    assert assessment.enumeration_allowed is False
    assert assessment.requires_candidate_date_set is True


def test_memory_conflict_requires_explicit_unordered_set_containing_original_date() -> None:
    conflicted = _lineage(weekday=Weekday.TUESDAY)
    with pytest.raises(ValueError, match="silently remove"):
        assess_evidence(
            _lineage(
                weekday=Weekday.TUESDAY,
                candidate_dates=(date(2000, 1, 4),),
                version=2,
                supersedes=conflicted.content_sha256,
            )
        )

    confirmed = _lineage(
        weekday=Weekday.TUESDAY,
        candidate_dates=(date(2000, 1, 4), date(2000, 1, 3)),
        version=2,
        supersedes=conflicted.content_sha256,
    )
    assessment = assess_evidence(confirmed)

    assert assessment.state is EvidenceState.CANDIDATE_DATE_SET_CONFIRMED
    assert assessment.enumeration_allowed is True
    assert assessment.operative_dates == (date(2000, 1, 3), date(2000, 1, 4))
    assert confirmed.candidate_date_set is not None
    assert confirmed.candidate_date_set.candidate_ordering == "none"


def test_server_correction_appends_lineage_and_never_overwrites_evidence(tmp_path: Path) -> None:
    ticks = iter((NOW, NOW + timedelta(minutes=1)))
    store = NatalTimePrivateStore(tmp_path)
    service = NatalTimeIntakeService(store, clock=lambda: next(ticks))
    receipt = service.capture_initial_evidence(
        asserted_date=date(2000, 1, 3),
        date_source=EvidenceSource.MEMORY,
        documentary_verification=DocumentaryVerification.NOT_APPLICABLE,
        weekday_answer_status=WeekdayAnswerStatus.REMEMBERED,
        asserted_weekday=Weekday.MONDAY,
        entered_how="synthetic_unit_test",
    )
    first = store.load_latest_lineage(receipt.lineage_id)

    second = service.supersede_declared_date(
        receipt.lineage_id,
        superseded_evidence_id=first.date_evidence[0].evidence_id,
        asserted_date=date(2000, 1, 4),
        source=EvidenceSource.DOCUMENTARY,
        documentary_verification=DocumentaryVerification.PARTICIPANT_REPORTED,
        entered_how="synthetic_correction",
    )

    assert second.version == 2
    assert second.supersedes_lineage_sha256 == first.content_sha256
    assert second.date_evidence[0] == first.date_evidence[0]
    assert second.date_evidence[-1].supersedes_evidence_id == first.date_evidence[0].evidence_id
    assert len(tuple((tmp_path / "natal-time" / "intakes" / receipt.lineage_id).glob("*"))) == 2


@pytest.mark.parametrize(
    ("civil_date", "timezone", "expected_hours"),
    [
        (date(2024, 1, 15), "UTC", 24),
        (date(2024, 2, 29), "UTC", 24),
        (date(2024, 3, 10), "America/New_York", 23),
        (date(2024, 11, 3), "America/New_York", 25),
        (date(2014, 10, 26), "Europe/Moscow", 25),
    ],
)
def test_civil_date_domain_handles_leap_dst_and_historical_offsets(
    civil_date: date,
    timezone: str,
    expected_hours: int,
) -> None:
    from zoneinfo import ZoneInfo

    start, end = _validated_civil_date_domain(civil_date, ZoneInfo(timezone))

    assert (end - start).total_seconds() == expected_hours * 3600
    assert start.astimezone(ZoneInfo(timezone)).date() == civil_date
    assert (end - timedelta(microseconds=1)).astimezone(ZoneInfo(timezone)).date() == civil_date


def test_skipped_civil_date_fails_closed() -> None:
    from zoneinfo import ZoneInfo

    with pytest.raises(ValueError, match="no positive instant domain"):
        _validated_civil_date_domain(date(2011, 12, 30), ZoneInfo("Pacific/Apia"))


def _frozen_synthetic_run(
    timezone: str = "UTC",
    candidate_date: date = date(2024, 1, 15),
) -> tuple[SyntheticAnalyticEphemerisProvider, NatalTimeManifest, Any]:
    provider = SyntheticAnalyticEphemerisProvider()
    lineage = _lineage(asserted_date=candidate_date, weekday=Weekday.from_date(candidate_date))
    assessment = assess_evidence(lineage)
    provenance = build_engine_provenance(
        provider,
        repository_commit="synthetic-test-commit",
        dependency_lock_path=PROJECT_ROOT / "requirements-dev.lock",
        runtime_or_container_sha256=synthetic_runtime_digest("natal-time-unit"),
        iana_timezone=timezone,
        boundary_root_tolerance_seconds=0.01,
    )
    identity = full_state_identity_specification()
    timezone_resolution = TimezoneResolution(
        iana_timezone=timezone,
        resolution_method="synthetic_explicit_fixture",
        participant_confirmed=True,
        timezone_database_version=provenance.timezone_database_version,
        timezone_file_sha256=provenance.timezone_file_sha256,
    )
    manifest = create_manifest(
        lineage,
        assessment,
        timezone_resolution=timezone_resolution,
        engine_provenance=provenance,
        state_identity=identity,
        fixture_classification=FixtureClassification.SYNTHETIC,
        created_at_utc=NOW,
    )
    return provider, manifest, create_freeze(manifest, created_at_utc=NOW)


def test_enumerator_produces_complete_maximal_unranked_receipt() -> None:
    provider, manifest, freeze = _frozen_synthetic_run()

    result = enumerate_manifest(provider, manifest, freeze)

    receipt = result.coverage_receipts[0]
    assert receipt.actual_duration_microseconds == 24 * 3600 * 1_000_000
    assert receipt.summed_interval_duration_microseconds == receipt.actual_duration_microseconds
    assert receipt.interval_count == len(result.intervals)
    assert receipt.coverage_complete is True
    assert receipt.boundary_sides_verified is True
    assert receipt.maximality_verified is True
    assert all(
        previous.end.utc == current.start.utc
        for previous, current in zip(result.intervals, result.intervals[1:], strict=False)
    )
    assert all(
        previous.full_state_sha256 != current.full_state_sha256
        for previous, current in zip(result.intervals, result.intervals[1:], strict=False)
    )
    assert result.ranking_present is False
    assert result.weights_present is False
    assert result.probability_present is False
    assert result.duration_used_as_evidence is False


def test_full_identity_includes_every_activation_and_documents_continuous_exclusions() -> None:
    identity = full_state_identity_specification()
    included = {field.path for field in identity.fields if field.included}
    excluded = {
        field.path: field.exclusion_reason for field in identity.fields if not field.included
    }

    assert default_activation_field_count() == 26
    assert {
        "activations.personality.sun.gate",
        "activations.personality.sun.line",
        "activations.design.pluto.gate",
        "activations.design.pluto.line",
        "bodygraph.definition_components",
        "bodygraph.channels",
    }.issubset(included)
    assert excluded["activations[*].longitude"]
    assert identity.reduced_signature_is_identity is False


def test_same_reduced_signature_does_not_collapse_different_full_states() -> None:
    first = {
        "visible": {"type": "generator", "authority": "sacral"},
        "activations": [{"body": "sun", "side": "personality", "gate": 1, "line": 1}],
    }
    second = {
        "visible": {"type": "generator", "authority": "sacral"},
        "activations": [{"body": "sun", "side": "personality", "gate": 1, "line": 2}],
    }

    facts = {fact.path: fact for fact in derive_mechanic_facts((first, second))}

    assert facts["visible.type"].status is MechanicStatus.STABLE
    assert facts["activations[0].line"].status is MechanicStatus.VARIABLE


def test_manifest_freeze_result_are_content_bound_and_extra_fields_are_rejected() -> None:
    provider, manifest, freeze = _frozen_synthetic_run()
    result = enumerate_manifest(provider, manifest, freeze)
    changed = manifest.model_copy(update={"candidate_dates": (date(2024, 1, 16),)})

    assert changed.content_sha256 != manifest.content_sha256
    assert result.manifest_sha256 == manifest.content_sha256
    assert result.freeze_sha256 == freeze.content_sha256
    with pytest.raises(ValidationError):
        NatalTimeManifest.model_validate({**manifest.model_dump(mode="json"), "rank": 1})
    with pytest.raises(ValidationError):
        type(result).model_validate({**result.model_dump(mode="json"), "probability": 0.9})
    with pytest.raises(ValidationError):
        type(freeze).model_validate({**freeze.model_dump(mode="json"), "relationship_evidence": {}})


def test_public_serializer_is_allowlisted_synthetic_only_and_contains_no_private_values() -> None:
    provider, manifest, freeze = _frozen_synthetic_run()
    result = enumerate_manifest(provider, manifest, freeze)
    artifact = serialize_synthetic_public_artifact(
        manifest,
        result,
        independent_public_id=_id("NTP", 7),
    )
    encoded = artifact.model_dump_json()

    assert "2024-01-15" not in encoded
    assert "UTC" not in encoded
    assert manifest.manifest_id not in encoded
    assert result.result_id not in encoded
    assert artifact.contains_exact_birth_data is False
    with pytest.raises(ValidationError):
        SyntheticPublicNatalTimeArtifact.model_validate(result.model_dump(mode="json"))

    real_manifest = manifest.model_copy(
        update={"fixture_classification": FixtureClassification.REAL_PRIVATE}
    )
    with pytest.raises(ValueError, match="real participant"):
        serialize_synthetic_public_artifact(
            real_manifest,
            result,
            independent_public_id=_id("NTP", 8),
        )


def test_runtime_provenance_mismatch_fails_closed() -> None:
    provider, manifest, freeze = _frozen_synthetic_run()
    bad_provenance = manifest.engine_provenance.model_copy(
        update={"timezone_file_sha256": "0" * 64}
    )
    with pytest.raises(ValidationError, match="timezone checksum"):
        NatalTimeManifest.model_validate(
            {
                **manifest.model_dump(mode="json"),
                "engine_provenance": bad_provenance.model_dump(mode="json"),
            }
        )

    assert timezone_file_sha256("UTC") == manifest.timezone_resolution.timezone_file_sha256


@pytest.mark.parametrize(
    ("civil_date", "timezone", "expected_hours"),
    [
        (date(2024, 2, 29), "UTC", 24),
        (date(2024, 3, 10), "America/New_York", 23),
        (date(2024, 11, 3), "America/New_York", 25),
        (date(2014, 10, 26), "Europe/Moscow", 25),
    ],
)
def test_enumerator_emits_complete_receipts_for_calendar_edge_cases(
    civil_date: date,
    timezone: str,
    expected_hours: int,
) -> None:
    provider, manifest, freeze = _frozen_synthetic_run(timezone, civil_date)

    result = enumerate_manifest(provider, manifest, freeze)

    receipt = result.coverage_receipts[0]
    assert receipt.actual_duration_microseconds == expected_hours * 3600 * 1_000_000
    assert receipt.coverage_complete is True
    assert receipt.boundary_sides_verified is True


def test_identical_frozen_inputs_produce_byte_identical_results() -> None:
    provider, manifest, freeze = _frozen_synthetic_run()

    first = enumerate_manifest(provider, manifest, freeze)
    second = enumerate_manifest(provider, manifest, freeze)

    assert first.model_dump_json() == second.model_dump_json()
    assert first.content_sha256 == second.content_sha256


def test_explicit_candidate_set_enumerates_every_date_without_order_or_prior() -> None:
    first_date = date(2024, 1, 15)
    second_date = date(2024, 1, 16)
    initial = _lineage(asserted_date=first_date, weekday=Weekday.TUESDAY)
    lineage = _lineage(
        asserted_date=first_date,
        weekday=Weekday.TUESDAY,
        candidate_dates=(second_date, first_date),
        version=2,
        supersedes=initial.content_sha256,
    )
    assessment = assess_evidence(lineage)
    provider = SyntheticAnalyticEphemerisProvider()
    provenance = build_engine_provenance(
        provider,
        repository_commit="synthetic-test-commit",
        dependency_lock_path=PROJECT_ROOT / "requirements-dev.lock",
        runtime_or_container_sha256=synthetic_runtime_digest("candidate-set-unit"),
        iana_timezone="UTC",
    )
    identity = full_state_identity_specification()
    manifest = create_manifest(
        lineage,
        assessment,
        timezone_resolution=TimezoneResolution(
            iana_timezone="UTC",
            resolution_method="synthetic_explicit_fixture",
            participant_confirmed=True,
            timezone_database_version=provenance.timezone_database_version,
            timezone_file_sha256=provenance.timezone_file_sha256,
        ),
        engine_provenance=provenance,
        state_identity=identity,
        fixture_classification=FixtureClassification.SYNTHETIC,
        created_at_utc=NOW,
    )
    freeze = create_freeze(manifest, created_at_utc=NOW)

    result = enumerate_manifest(provider, manifest, freeze)

    assert manifest.candidate_dates == (first_date, second_date)
    assert manifest.candidate_ordering == "none"
    assert [item.civil_date for item in result.coverage_receipts] == [first_date, second_date]
    assert result.ranking_present is False
    assert result.weights_present is False


def test_unresolved_or_unknown_timezone_cannot_create_a_manifest() -> None:
    provider, manifest, _freeze = _frozen_synthetic_run()
    payload = manifest.timezone_resolution.model_dump(mode="json")
    with pytest.raises(ValidationError):
        TimezoneResolution.model_validate({**payload, "resolution_status": "ambiguous"})
    with pytest.raises(ValueError, match="checksum"):
        timezone_file_sha256("Mars/Olympus_Mons")


class AsgiResponse:
    def __init__(self, status_code: int, body: dict[str, Any]) -> None:
        self.status_code = status_code
        self.body = body


def _request_json(
    app: FastAPI,
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
) -> AsgiResponse:
    parsed = urlsplit(url)
    encoded = b"" if body is None else json.dumps(body).encode()
    headers = [(b"accept", b"application/json")]
    if body is not None:
        headers.extend(
            (
                (b"content-type", b"application/json"),
                (b"content-length", str(len(encoded)).encode()),
            )
        )
    scope: Scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": parsed.path,
        "raw_path": parsed.path.encode(),
        "query_string": parsed.query.encode(),
        "root_path": "",
        "headers": headers,
        "client": ("test", 123),
        "server": ("testserver", 80),
        "state": {},
    }
    sent: list[Message] = []
    delivered = False

    async def receive() -> Message:
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": encoded, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    start = next(message for message in sent if message["type"] == "http.response.start")
    payload = b"".join(
        message.get("body", b"") for message in sent if message["type"] == "http.response.body"
    )
    return AsgiResponse(start["status"], json.loads(payload))


def test_api_locks_weekday_before_any_implied_weekday_reveal(tmp_path: Path) -> None:
    app = create_natal_time_app(tmp_path)
    intake = _request_json(
        app,
        "POST",
        "/v1/natal-time/intakes",
        {
            "asserted_date": "2000-01-03",
            "date_source": "memory",
            "documentary_verification": "not_applicable",
            "remembered_weekday_status": "remembered",
            "remembered_weekday": "tuesday",
        },
    )
    intake_text = json.dumps(intake.body, sort_keys=True)

    assert intake.status_code == 200
    assert intake.body["lock"]["weekday_locked"] is True
    assert intake.body["lock"]["implied_weekday_revealed"] is False
    assert "2000-01-03" not in intake_text
    assert "monday" not in intake_text
    lineage_id = intake.body["lock"]["lineage_id"]

    assessment = _request_json(
        app,
        "POST",
        f"/v1/natal-time/intakes/{lineage_id}/assessment",
    )
    assert assessment.status_code == 200
    assert assessment.body["assessment"]["state"] == "birth_date_uncertain"
    assert assessment.body["assessment"]["date_weekday_facts"][0]["implied_weekday"] == "monday"


def test_api_rejects_relationship_or_client_independence_fields(tmp_path: Path) -> None:
    app = create_natal_time_app(tmp_path)
    response = _request_json(
        app,
        "POST",
        "/v1/natal-time/intakes",
        {
            "asserted_date": "2000-01-03",
            "date_source": "memory",
            "documentary_verification": "not_applicable",
            "remembered_weekday_status": "unknown",
            "remembered_weekday": None,
            "relationship_id": "pair-private",
            "captured_independently": True,
        },
    )

    assert response.status_code == 422
    assert not tuple((tmp_path / "natal-time" / "intakes").glob("**/*.private.json"))


def test_store_refuses_in_place_scientific_overwrite(tmp_path: Path) -> None:
    _provider, manifest, freeze = _frozen_synthetic_run()
    store = NatalTimePrivateStore(tmp_path)
    store.append_manifest(manifest)
    store.append_freeze(manifest.manifest_id, freeze)

    with pytest.raises(FileExistsError):
        store.append_manifest(manifest)
    with pytest.raises(FileExistsError):
        store.append_freeze(manifest.manifest_id, freeze)
