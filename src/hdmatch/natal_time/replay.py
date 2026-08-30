"""Fixture-granular, resumable replay receipts for the qualified real engine.

The immutable checkpoint-2 fixture audit is the expectation source.  A replay
receipt is one civil-day attestation, while execution is grouped by the source
fixture so the original multi-date result digest can be reproduced exactly.
Aggregate verification reads receipt hashes only; it never reruns astronomy.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal, Protocol, cast
from zoneinfo import ZoneInfo

from hdmatch.chart.ephemeris import CelestialBody, SwissEphemerisProvider
from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.conformance import independently_enumerate_line_transitions
from hdmatch.natal_time.enumerator import _validated_civil_date_domain, enumerate_manifest
from hdmatch.runtime.chart_adapter import declared_ephemeris_files
from hdmatch.util import canonical_json_bytes, sha256_file, sha256_json

QUALIFIED_FIXTURE_AUDIT_SHA256 = (
    "c81264cbc6a5cc2b6e702f55ed063e9eec0558f11124da4619ca76a8b8b7d1e1"
)
QUALIFIED_FIXTURE_FILE_SHA256 = (
    "77a60c9d880d9458c9571f6fbc0086d0622fc26ddbf0ea20da812f8fc5b7cb76"
)
QUALIFIED_IDENTITY_PACKET_SHA256 = (
    "7c2a4fede57da9cda3b35008c7433b6d6d63a6bcb313206bcac8804c344d98b6"
)
QUALIFIED_IDENTITY_FILE_SHA256 = (
    "05c80517099790b8213e86fb0b3d366c57a56a784577dfcf161c1fbb3ac6f27d"
)
PRODUCTION_RECEIPT_SCHEMA = "natal-time-real-engine-fixture-replay-receipt-v1"
PRODUCTION_INDEX_SCHEMA = "natal-time-real-engine-fixture-replay-index-v1"
SYNTHETIC_RECEIPT_SCHEMA = "natal-time-replay-synthetic-orchestration-receipt-v1"
SYNTHETIC_INDEX_SCHEMA = "natal-time-replay-synthetic-orchestration-index-v1"
SOURCE_VERIFICATION_SCHEMA = "natal-time-real-engine-replay-source-verification-v1"
PRODUCTION_OUTPUT_REPO_RELATIVE = "state/NATAL-TIME-REAL-ENGINE-REPLAY-V1"
_ROOT_TOLERANCE_SECONDS = 0.000001


class ReplayValidationError(ValueError):
    """Raised when replay state is incomplete, stale, duplicated, or mismatched."""


@dataclass(frozen=True, slots=True)
class ReplayExpectation:
    receipt_id: str
    source_fixture_name: str
    source_fixture_index: int | None
    civil_date: str
    iana_timezone: str
    status: Literal["success", "fail_closed"]
    fixture_input: dict[str, Any]
    civil_day_domain: dict[str, Any]
    committed_interval_count: int
    committed_ordered_full_state_vector_sha256: str
    committed_coverage_receipt_sha256: str
    committed_result_sha256: str

    @property
    def fixture_input_sha256(self) -> str:
        return sha256_json(self.fixture_input)

    @property
    def civil_day_domain_sha256(self) -> str:
        return sha256_json(self.civil_day_domain)


@dataclass(frozen=True, slots=True)
class ReplayContext:
    execution_mode: Literal["real_engine_production", "synthetic_orchestration_test"]
    repository_root: Path
    repository_commit: str
    commit_tree_oid: str
    source_verification: dict[str, Any]
    source_verification_sha256: str
    fixture_artifact_path: Path
    fixture_artifact_file_sha256: str
    fixture_artifact_audit_sha256: str
    fixture_artifact: dict[str, Any]
    engine_identity_path: Path
    engine_identity_file_sha256: str
    engine_identity_packet_sha256: str
    engine_identity: dict[str, Any]
    expectations: tuple[ReplayExpectation, ...]


class FixtureExecutor(Protocol):
    """An execution boundary that returns all receipts for one source fixture."""

    def __call__(
        self,
        context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]: ...


def current_repository_commit(repository_root: Path) -> str:
    """Return the exact checked-out commit without inspecting or changing Git state."""

    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def verify_production_source(
    repository_root: Path,
    repository_commit: str,
    output_root: Path,
) -> dict[str, Any]:
    """Verify exact HEAD and a clean source tree, excluding only the output root."""

    root = repository_root.resolve(strict=True)
    _require_current_head(root, repository_commit)
    output = output_root.resolve()
    if output == root or root not in output.parents:
        raise ReplayValidationError("production output root must be a strict repository child")
    relative_output = output.relative_to(root).as_posix()
    if relative_output != PRODUCTION_OUTPUT_REPO_RELATIVE:
        raise ReplayValidationError(
            f"production output root must be {PRODUCTION_OUTPUT_REPO_RELATIVE}"
        )
    tree_oid = _git_output(root, ["rev-parse", "HEAD^{tree}"])
    if not _is_git_oid(tree_oid):
        raise ReplayValidationError("current commit tree OID is invalid")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout
    dirty_outside = tuple(
        path
        for path in _porcelain_paths(status)
        if path != relative_output and not path.startswith(f"{relative_output}/")
    )
    if dirty_outside:
        rendered = ", ".join(dirty_outside[:5])
        raise ReplayValidationError(
            f"production replay source tree is dirty outside output root: {rendered}"
        )
    payload: dict[str, Any] = {
        "schema_version": SOURCE_VERIFICATION_SCHEMA,
        "verification_mode": "exact-head-clean-tree-excluding-declared-output-root",
        "repository_commit": repository_commit,
        "commit_tree_oid": tree_oid,
        "head_matches_declared_commit": True,
        "clean_worktree_excluding_output_root": True,
        "output_root_repo_relative": relative_output,
    }
    payload["source_verification_sha256"] = sha256_json(payload)
    return payload


def load_replay_context(
    repository_root: Path,
    repository_commit: str,
    *,
    fixture_artifact_path: Path | None = None,
    engine_identity_path: Path | None = None,
    source_verification: Mapping[str, Any] | None = None,
) -> ReplayContext:
    """Load and pin the qualified source artifacts and derive nine expectations."""

    root = repository_root.resolve(strict=True)
    _require_current_head(root, repository_commit)
    verification = (
        dict(source_verification)
        if source_verification is not None
        else _head_only_source_verification(root, repository_commit)
    )
    _validate_source_verification(root, repository_commit, verification)
    return _load_pinned_context(
        root,
        repository_commit,
        execution_mode="real_engine_production",
        source_verification=verification,
        fixture_artifact_path=fixture_artifact_path,
        engine_identity_path=engine_identity_path,
    )


def load_synthetic_test_context(
    repository_root: Path,
    *,
    fixture_artifact_path: Path | None = None,
    engine_identity_path: Path | None = None,
) -> ReplayContext:
    """Load pinned expectations for orchestration tests without real-engine claims."""

    root = repository_root.resolve(strict=True)
    verification: dict[str, Any] = {
        "schema_version": "natal-time-replay-synthetic-source-v1",
        "verification_mode": "synthetic-orchestration-test-no-git-claim",
        "repository_commit": "synthetic-orchestration-test",
        "commit_tree_oid": "0" * 40,
        "head_matches_declared_commit": False,
        "clean_worktree_excluding_output_root": False,
        "output_root_repo_relative": None,
    }
    verification["source_verification_sha256"] = sha256_json(verification)
    return _load_pinned_context(
        root,
        "synthetic-orchestration-test",
        execution_mode="synthetic_orchestration_test",
        source_verification=verification,
        fixture_artifact_path=fixture_artifact_path,
        engine_identity_path=engine_identity_path,
    )


def _load_pinned_context(
    root: Path,
    repository_commit: str,
    *,
    execution_mode: Literal["real_engine_production", "synthetic_orchestration_test"],
    source_verification: dict[str, Any],
    fixture_artifact_path: Path | None,
    engine_identity_path: Path | None,
) -> ReplayContext:
    fixture_path = (
        fixture_artifact_path or root / "state" / "NATAL-TIME-REAL-ENGINE-FIXTURES.json"
    ).resolve(strict=True)
    identity_path = (
        engine_identity_path or root / "state" / "NATAL-TIME-REAL-ENGINE-IDENTITY-V4.json"
    ).resolve(strict=True)
    fixture = _load_json_object(fixture_path)
    identity = _load_json_object(identity_path)
    fixture_file_sha = sha256_file(fixture_path)
    identity_file_sha = sha256_file(identity_path)
    if fixture_file_sha != QUALIFIED_FIXTURE_FILE_SHA256:
        raise ReplayValidationError("qualified fixture artifact exact bytes changed")
    if identity_file_sha != QUALIFIED_IDENTITY_FILE_SHA256:
        raise ReplayValidationError("qualified engine identity artifact exact bytes changed")
    _verify_embedded_hash(fixture, "audit_sha256", QUALIFIED_FIXTURE_AUDIT_SHA256)
    _verify_embedded_hash(identity, "packet_sha256", QUALIFIED_IDENTITY_PACKET_SHA256)
    if fixture.get("engine_identity_packet_sha256") != identity.get("packet_sha256"):
        raise ReplayValidationError("fixture artifact is bound to a different engine identity")
    expectations = _build_expectations(fixture)
    return ReplayContext(
        execution_mode=execution_mode,
        repository_root=root,
        repository_commit=repository_commit,
        commit_tree_oid=cast(str, source_verification["commit_tree_oid"]),
        source_verification=source_verification,
        source_verification_sha256=cast(
            str, source_verification["source_verification_sha256"]
        ),
        fixture_artifact_path=fixture_path,
        fixture_artifact_file_sha256=fixture_file_sha,
        fixture_artifact_audit_sha256=cast(str, fixture["audit_sha256"]),
        fixture_artifact=fixture,
        engine_identity_path=identity_path,
        engine_identity_file_sha256=identity_file_sha,
        engine_identity_packet_sha256=cast(str, identity["packet_sha256"]),
        engine_identity=identity,
        expectations=expectations,
    )


def make_receipt(
    context: ReplayContext,
    expectation: ReplayExpectation,
    *,
    interval_count: int,
    ordered_interval_list_sha256: str,
    ordered_full_state_vector_sha256: str,
    coverage_receipt_sha256: str,
    result_sha256: str,
    independent_verification: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct a self-hashing receipt and enforce every committed expectation."""

    actual = {
        "interval_count": interval_count,
        "ordered_full_state_vector_sha256": ordered_full_state_vector_sha256,
        "coverage_receipt_sha256": coverage_receipt_sha256,
        "result_sha256": result_sha256,
    }
    committed = {
        "interval_count": expectation.committed_interval_count,
        "ordered_full_state_vector_sha256": (
            expectation.committed_ordered_full_state_vector_sha256
        ),
        "coverage_receipt_sha256": expectation.committed_coverage_receipt_sha256,
        "result_sha256": expectation.committed_result_sha256,
    }
    if actual != committed:
        raise ReplayValidationError(
            f"{expectation.receipt_id} does not match committed result components"
        )
    if not _is_sha256(ordered_interval_list_sha256):
        raise ReplayValidationError(
            f"{expectation.receipt_id} ordered interval-list digest is invalid"
        )
    verification = dict(independent_verification)
    production = context.execution_mode == "real_engine_production"
    required_status = "synthetic_not_executed"
    if production:
        required_status = (
            "passed_exact_event_key_agreement"
            if expectation.status == "success"
            else "passed_expected_fail_closed"
        )
    if verification.get("status") != required_status:
        raise ReplayValidationError(
            f"{expectation.receipt_id} independent verification did not pass"
        )
    receipt_schema = PRODUCTION_RECEIPT_SCHEMA if production else SYNTHETIC_RECEIPT_SCHEMA
    payload: dict[str, Any] = {
        "schema_version": receipt_schema,
        "execution_mode": context.execution_mode,
        "real_engine_executor": production,
        "synthetic_orchestration_test_only": not production,
        "receipt_id": expectation.receipt_id,
        "status": expectation.status,
        "repository_commit": context.repository_commit,
        "commit_tree_oid": context.commit_tree_oid,
        "source_verification_sha256": context.source_verification_sha256,
        "fixture_artifact_file_sha256": context.fixture_artifact_file_sha256,
        "fixture_artifact_audit_sha256": context.fixture_artifact_audit_sha256,
        "engine_identity_file_sha256": context.engine_identity_file_sha256,
        "engine_identity_packet_sha256": context.engine_identity_packet_sha256,
        "fixture_input": expectation.fixture_input,
        "fixture_input_sha256": expectation.fixture_input_sha256,
        "civil_day_domain": expectation.civil_day_domain,
        "civil_day_domain_sha256": expectation.civil_day_domain_sha256,
        "ordered_interval_list_scope": (
            "canonical-model-dumps-of-every-complete-ordered-civil-day-interval"
        ),
        "ordered_interval_list_sha256": ordered_interval_list_sha256,
        "ordered_full_state_vector_scope": (
            "ordered-complete-full-state-sha256-vector-from-coverage-receipt"
        ),
        **actual,
        "committed_expectations": committed,
        "committed_components_match": True,
        "independent_verification": verification,
        "independent_verification_sha256": sha256_json(verification),
        "fixture_data_synthetic_only": True,
        "inference_semantics_present": False,
    }
    payload["receipt_sha256"] = sha256_json(payload)
    return payload


def real_engine_fixture_executor(
    context: ReplayContext,
    expectations: tuple[ReplayExpectation, ...],
) -> Sequence[Mapping[str, Any]]:
    """Recompute one original source fixture and independently verify each day."""

    if context.execution_mode != "real_engine_production":
        raise ReplayValidationError("real-engine executor rejects synthetic test contexts")
    if not expectations:
        raise ReplayValidationError("fixture execution requires at least one expectation")
    first = expectations[0]
    if any(item.source_fixture_name != first.source_fixture_name for item in expectations):
        raise ReplayValidationError("fixture execution group mixes source fixtures")
    if first.status == "fail_closed":
        return (_execute_fail_closed(context, first),)
    if first.source_fixture_index is None:
        raise ReplayValidationError("successful fixture is missing its source index")

    # Importing the frozen fixture constructor avoids a second subtly different
    # manifest recipe while leaving the qualified implementation untouched.
    from scripts.audit_natal_time_real_engine_fixtures import (  # noqa: PLC0415
        FIXTURES,
        _manifest_and_freeze,
    )

    source = FIXTURES[first.source_fixture_index - 1]
    name, candidate_dates, timezone, _expected_hours = source
    if name != first.source_fixture_name:
        raise ReplayValidationError("source fixture ordering changed")
    if tuple(item.civil_date for item in expectations) != tuple(
        value.isoformat() for value in candidate_dates
    ):
        raise ReplayValidationError("source fixture civil-day set changed")
    provider = SwissEphemerisProvider(
        declared_ephemeris_files(context.repository_root / "data" / "ephemeris")
    )
    manifest, freeze = _manifest_and_freeze(
        provider,
        context.repository_root,
        cast(str, context.fixture_artifact["repository_commit"]),
        cast(str, context.engine_identity["runtime"]["sha256"]),
        first.source_fixture_index,
        candidate_dates,
        timezone,
    )
    expected_input = first.fixture_input
    if manifest.content_sha256 != expected_input["source_manifest_sha256"]:
        raise ReplayValidationError("reconstructed fixture manifest digest changed")
    if freeze.content_sha256 != expected_input["source_freeze_sha256"]:
        raise ReplayValidationError("reconstructed fixture freeze digest changed")
    result = enumerate_manifest(provider, manifest, freeze)
    if result.content_sha256 != first.committed_result_sha256:
        raise ReplayValidationError("recomputed source fixture result digest changed")

    output: list[dict[str, Any]] = []
    for expectation in expectations:
        civil = date.fromisoformat(expectation.civil_date)
        intervals = tuple(item for item in result.intervals if item.civil_date == civil)
        coverage = next(
            (item for item in result.coverage_receipts if item.civil_date == civil), None
        )
        if coverage is None:
            raise ReplayValidationError(f"missing coverage receipt for {expectation.receipt_id}")
        ordered_interval_list_sha = sha256_json(
            [item.model_dump(mode="json") for item in intervals]
        )
        ordered_full_state_vector_sha = sha256_json(
            [item.full_state_sha256 for item in intervals]
        )
        verification = _independent_verification(provider, intervals, coverage)
        output.append(
            make_receipt(
                context,
                expectation,
                interval_count=len(intervals),
                ordered_interval_list_sha256=ordered_interval_list_sha,
                ordered_full_state_vector_sha256=ordered_full_state_vector_sha,
                coverage_receipt_sha256=sha256_json(coverage.model_dump(mode="json")),
                result_sha256=result.content_sha256,
                independent_verification=verification,
            )
        )
    return tuple(output)


def run_replay(
    context: ReplayContext,
    output_root: Path,
    *,
    aggregate_only: bool = False,
    progress: Callable[[str, str], None] | None = None,
) -> dict[str, Any]:
    """Run or verify production replay; the real executor cannot be substituted."""

    _validate_production_context(context, output_root)
    return _run_replay(
        context,
        output_root,
        executor=real_engine_fixture_executor,
        aggregate_only=aggregate_only,
        progress=progress,
    )


def run_synthetic_test_replay(
    context: ReplayContext,
    output_root: Path,
    *,
    executor: FixtureExecutor,
    aggregate_only: bool = False,
) -> dict[str, Any]:
    """Exercise resume/aggregation only, using unmistakably synthetic artifacts."""

    if context.execution_mode != "synthetic_orchestration_test":
        raise ReplayValidationError("synthetic test runner requires a synthetic context")
    return _run_replay(
        context,
        output_root,
        executor=executor,
        aggregate_only=aggregate_only,
        progress=None,
    )


def _run_replay(
    context: ReplayContext,
    output_root: Path,
    *,
    executor: FixtureExecutor,
    aggregate_only: bool,
    progress: Callable[[str, str], None] | None,
) -> dict[str, Any]:
    """Shared immutable receipt orchestration behind separated public modes."""

    root = output_root
    receipts_dir = root / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    _reject_unexpected_receipt_files(context, receipts_dir)
    existing = _load_valid_receipts(context, receipts_dir, allow_missing=True)
    if not aggregate_only:
        grouped = _group_expectations(context.expectations)
        for expectations in grouped:
            if all(item.receipt_id in existing for item in expectations):
                continue
            if context.execution_mode == "real_engine_production":
                _validate_production_context(context, output_root)
            if progress is not None:
                progress("start", expectations[0].source_fixture_name)
            generated = tuple(dict(item) for item in executor(context, expectations))
            if progress is not None:
                progress("done", expectations[0].source_fixture_name)
            if context.execution_mode == "real_engine_production":
                _validate_production_context(context, output_root)
            generated_by_id = {cast(str, item.get("receipt_id")): item for item in generated}
            expected_ids = {item.receipt_id for item in expectations}
            if len(generated_by_id) != len(generated) or set(generated_by_id) != expected_ids:
                raise ReplayValidationError(
                    "fixture executor returned missing or duplicate receipts"
                )
            for expectation in expectations:
                payload = generated_by_id[expectation.receipt_id]
                _validate_receipt(context, expectation, payload)
                path = receipts_dir / f"{expectation.receipt_id}.json"
                if path.exists():
                    existing_payload = _load_json_object(path)
                    if existing_payload != payload:
                        raise ReplayValidationError(
                            f"existing receipt changed during resume: {expectation.receipt_id}"
                        )
                else:
                    write_new_bytes(path, canonical_json_bytes(payload) + b"\n")
                existing[expectation.receipt_id] = payload
    receipts = _load_valid_receipts(context, receipts_dir, allow_missing=False)
    if context.execution_mode == "real_engine_production":
        _validate_production_context(context, output_root)
    index = build_aggregate_index(context, receipts)
    index_path = root / "index.json"
    if index_path.exists():
        if _load_json_object(index_path) != index:
            raise ReplayValidationError("existing replay index does not match verified receipts")
    elif aggregate_only:
        raise ReplayValidationError("aggregate-only verification requires an existing index")
    else:
        write_new_bytes(index_path, canonical_json_bytes(index) + b"\n")
    return index


def build_aggregate_index(
    context: ReplayContext,
    receipts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Aggregate verified receipt hashes without executing transition calculations."""

    ordered = [
        {
            "receipt_id": item.receipt_id,
            "receipt_sha256": cast(str, receipts[item.receipt_id]["receipt_sha256"]),
        }
        for item in context.expectations
    ]
    production = context.execution_mode == "real_engine_production"
    aggregate_input = {
        "execution_mode": context.execution_mode,
        "repository_commit": context.repository_commit,
        "commit_tree_oid": context.commit_tree_oid,
        "source_verification_sha256": context.source_verification_sha256,
        "fixture_artifact_file_sha256": context.fixture_artifact_file_sha256,
        "fixture_artifact_audit_sha256": context.fixture_artifact_audit_sha256,
        "engine_identity_file_sha256": context.engine_identity_file_sha256,
        "engine_identity_packet_sha256": context.engine_identity_packet_sha256,
        "receipt_hashes": ordered,
    }
    payload: dict[str, Any] = {
        "schema_version": PRODUCTION_INDEX_SCHEMA if production else SYNTHETIC_INDEX_SCHEMA,
        "real_engine_executor": production,
        "synthetic_orchestration_test_only": not production,
        "source_verification": context.source_verification,
        **aggregate_input,
        "receipt_count": len(ordered),
        "successful_civil_day_count": sum(
            item.status == "success" for item in context.expectations
        ),
        "fail_closed_civil_day_count": sum(
            item.status == "fail_closed" for item in context.expectations
        ),
        "all_committed_components_match": True,
        "all_independent_verifications_passed": production,
        "real_engine_executed": production,
        "aggregate_from_receipt_hashes_without_transition_recomputation": True,
        "aggregate_sha256": sha256_json(aggregate_input),
    }
    payload["index_sha256"] = sha256_json(payload)
    return payload


def _build_expectations(fixture: Mapping[str, Any]) -> tuple[ReplayExpectation, ...]:
    expectations: list[ReplayExpectation] = []
    fixtures = cast(list[dict[str, Any]], fixture.get("fixtures"))
    for fixture_index, source in enumerate(fixtures, start=1):
        candidate_dates = cast(list[str], source["candidate_dates"])
        coverage_items = cast(list[dict[str, Any]], source["coverage_receipts"])
        if [item["civil_date"] for item in coverage_items] != candidate_dates:
            raise ReplayValidationError("fixture candidate and coverage date order differs")
        for coverage in coverage_items:
            civil = cast(str, coverage["civil_date"])
            receipt_id = _receipt_id(cast(str, source["name"]), civil)
            fixture_input = {
                "source_fixture_name": source["name"],
                "source_fixture_index": fixture_index,
                "source_candidate_dates": candidate_dates,
                "civil_date": civil,
                "iana_timezone": source["iana_timezone"],
                "source_manifest_sha256": source["manifest_sha256"],
                "source_freeze_sha256": source["freeze_sha256"],
                "source_result_sha256": source["result_sha256"],
            }
            domain = {
                "civil_date": civil,
                "iana_timezone": source["iana_timezone"],
                "domain_start": coverage["domain_start"],
                "domain_end": coverage["domain_end"],
                "actual_duration_microseconds": coverage["actual_duration_microseconds"],
            }
            states = cast(list[str], coverage["interval_state_sha256"])
            expectations.append(
                ReplayExpectation(
                    receipt_id=receipt_id,
                    source_fixture_name=cast(str, source["name"]),
                    source_fixture_index=fixture_index,
                    civil_date=civil,
                    iana_timezone=cast(str, source["iana_timezone"]),
                    status="success",
                    fixture_input=fixture_input,
                    civil_day_domain=domain,
                    committed_interval_count=cast(int, coverage["interval_count"]),
                    committed_ordered_full_state_vector_sha256=sha256_json(states),
                    committed_coverage_receipt_sha256=sha256_json(coverage),
                    committed_result_sha256=cast(str, source["result_sha256"]),
                )
            )
    skipped = cast(dict[str, Any], fixture.get("skipped_date_fixture"))
    skip_input = deepcopy(skipped)
    skip_domain = {
        "civil_date": skipped["civil_date"],
        "iana_timezone": skipped["iana_timezone"],
        "positive_instant_domain": False,
    }
    expectations.append(
        ReplayExpectation(
            receipt_id=_receipt_id(cast(str, skipped["name"]), cast(str, skipped["civil_date"])),
            source_fixture_name=cast(str, skipped["name"]),
            source_fixture_index=None,
            civil_date=cast(str, skipped["civil_date"]),
            iana_timezone=cast(str, skipped["iana_timezone"]),
            status="fail_closed",
            fixture_input=skip_input,
            civil_day_domain=skip_domain,
            committed_interval_count=0,
            committed_ordered_full_state_vector_sha256=sha256_json([]),
            committed_coverage_receipt_sha256=sha256_json(skip_domain),
            committed_result_sha256=sha256_json(skip_input),
        )
    )
    ids = [item.receipt_id for item in expectations]
    if len(expectations) != 9 or len(ids) != len(set(ids)):
        raise ReplayValidationError("qualified replay requires nine unique civil-day receipts")
    return tuple(expectations)


def _execute_fail_closed(
    context: ReplayContext, expectation: ReplayExpectation
) -> dict[str, Any]:
    try:
        _validated_civil_date_domain(
            date.fromisoformat(expectation.civil_date), ZoneInfo(expectation.iana_timezone)
        )
    except ValueError as exc:
        actual = {
            "name": expectation.fixture_input["name"],
            "civil_date": expectation.civil_date,
            "iana_timezone": expectation.iana_timezone,
            "enumeration_allowed": False,
            "failure_type": type(exc).__name__,
            "failure_message": str(exc),
        }
    else:
        raise ReplayValidationError("expected nonexistent civil day acquired a positive domain")
    if actual != expectation.fixture_input:
        raise ReplayValidationError("fail-closed result changed from committed artifact")
    verification = {
        "status": "passed_expected_fail_closed",
        "enumeration_allowed": False,
        "failure_type": actual["failure_type"],
        "failure_message": actual["failure_message"],
    }
    return make_receipt(
        context,
        expectation,
        interval_count=0,
        ordered_interval_list_sha256=sha256_json([]),
        ordered_full_state_vector_sha256=sha256_json([]),
        coverage_receipt_sha256=sha256_json(expectation.civil_day_domain),
        result_sha256=sha256_json(actual),
        independent_verification=verification,
    )


def _independent_verification(
    provider: SwissEphemerisProvider,
    intervals: Sequence[Any],
    coverage: Any,
) -> dict[str, Any]:
    start = coverage.domain_start.utc.astimezone(UTC)
    end = coverage.domain_end.utc.astimezone(UTC)
    production = tuple(
        sorted(
            _event_key(encoded)
            for interval in intervals
            for encoded in interval.boundary_events
        )
    )
    independent = independently_enumerate_line_transitions(
        provider,
        start,
        end,
        initial_scan_step_seconds=3600.0,
        design_root_time_tolerance_seconds=_ROOT_TOLERANCE_SECONDS,
    )
    independent_keys = tuple(
        (
            item.at_utc,
            item.side,
            item.body.value,
            item.before_gate,
            item.before_line,
            item.after_gate,
            item.after_line,
        )
        for item in independent.transitions
    )
    if production != independent_keys:
        raise ReplayValidationError("independent transition enumeration disagrees with replay")
    return {
        "status": "passed_exact_event_key_agreement",
        "production_event_count": len(production),
        "independent_event_count": len(independent_keys),
        "independent_enumeration_sha256": independent.content_sha256,
        "independent_series_certificate_sha256": sha256_json(
            [item.model_dump(mode="json") for item in independent.series_certificates]
        ),
    }


def _event_key(encoded: str) -> tuple[datetime, str, str, int, int, int, int]:
    at, side, body, transition = encoded.split("|", 3)
    before, after = transition.split("->", 1)
    before_gate, before_line = (int(value) for value in before.split("."))
    after_gate, after_line = (int(value) for value in after.split("."))
    CelestialBody(body)  # fail closed if a non-canonical body appears
    return (
        datetime.fromisoformat(at),
        side,
        body,
        before_gate,
        before_line,
        after_gate,
        after_line,
    )


def _load_valid_receipts(
    context: ReplayContext,
    receipts_dir: Path,
    *,
    allow_missing: bool,
) -> dict[str, dict[str, Any]]:
    expected = {item.receipt_id: item for item in context.expectations}
    loaded: dict[str, dict[str, Any]] = {}
    for receipt_id, expectation in expected.items():
        path = receipts_dir / f"{receipt_id}.json"
        if not path.exists():
            if allow_missing:
                continue
            raise ReplayValidationError(f"missing replay receipt: {receipt_id}")
        payload = _load_json_object(path)
        _validate_receipt(context, expectation, payload)
        loaded[receipt_id] = payload
    return loaded


def _validate_receipt(
    context: ReplayContext,
    expectation: ReplayExpectation,
    payload: Mapping[str, Any],
) -> None:
    production = context.execution_mode == "real_engine_production"
    expected_schema = PRODUCTION_RECEIPT_SCHEMA if production else SYNTHETIC_RECEIPT_SCHEMA
    if payload.get("schema_version") != expected_schema:
        raise ReplayValidationError("replay receipt schema changed")
    if payload.get("execution_mode") != context.execution_mode:
        raise ReplayValidationError("replay receipt execution mode mismatch")
    if payload.get("real_engine_executor") is not production:
        raise ReplayValidationError("replay receipt executor mode mismatch")
    if payload.get("synthetic_orchestration_test_only") is not (not production):
        raise ReplayValidationError("replay receipt synthetic-mode flag mismatch")
    if payload.get("receipt_id") != expectation.receipt_id:
        raise ReplayValidationError("replay receipt ID mismatch")
    if payload.get("status") != expectation.status:
        raise ReplayValidationError("replay receipt status mismatch")
    exact_bindings = {
        "repository_commit": context.repository_commit,
        "commit_tree_oid": context.commit_tree_oid,
        "source_verification_sha256": context.source_verification_sha256,
        "fixture_artifact_file_sha256": context.fixture_artifact_file_sha256,
        "fixture_artifact_audit_sha256": context.fixture_artifact_audit_sha256,
        "engine_identity_file_sha256": context.engine_identity_file_sha256,
        "engine_identity_packet_sha256": context.engine_identity_packet_sha256,
        "fixture_input_sha256": expectation.fixture_input_sha256,
        "civil_day_domain_sha256": expectation.civil_day_domain_sha256,
        "interval_count": expectation.committed_interval_count,
        "ordered_full_state_vector_sha256": (
            expectation.committed_ordered_full_state_vector_sha256
        ),
        "coverage_receipt_sha256": expectation.committed_coverage_receipt_sha256,
        "result_sha256": expectation.committed_result_sha256,
    }
    for key, expected_value in exact_bindings.items():
        if payload.get(key) != expected_value:
            raise ReplayValidationError(
                f"{expectation.receipt_id} stale or mismatched binding: {key}"
            )
    if payload.get("fixture_input") != expectation.fixture_input:
        raise ReplayValidationError("replay receipt fixture input mismatch")
    if payload.get("civil_day_domain") != expectation.civil_day_domain:
        raise ReplayValidationError("replay receipt civil-day domain mismatch")
    if payload.get("committed_expectations") != {
        "interval_count": expectation.committed_interval_count,
        "ordered_full_state_vector_sha256": (
            expectation.committed_ordered_full_state_vector_sha256
        ),
        "coverage_receipt_sha256": expectation.committed_coverage_receipt_sha256,
        "result_sha256": expectation.committed_result_sha256,
    }:
        raise ReplayValidationError("replay receipt committed expectations mismatch")
    if not _is_sha256(payload.get("ordered_interval_list_sha256")):
        raise ReplayValidationError("replay receipt ordered interval-list digest is invalid")
    verification = payload.get("independent_verification")
    if not isinstance(verification, dict):
        raise ReplayValidationError("replay receipt lacks independent verification")
    required_status = "synthetic_not_executed"
    if production:
        required_status = (
            "passed_exact_event_key_agreement"
            if expectation.status == "success"
            else "passed_expected_fail_closed"
        )
    if verification.get("status") != required_status:
        raise ReplayValidationError("replay receipt independent verification failed")
    if production and expectation.status == "success":
        production_count = verification.get("production_event_count")
        independent_count = verification.get("independent_event_count")
        if (
            not isinstance(production_count, int)
            or production_count < 0
            or production_count != independent_count
        ):
            raise ReplayValidationError("production and independent event counts differ")
        if not _is_sha256(verification.get("independent_enumeration_sha256")):
            raise ReplayValidationError("independent enumeration digest is invalid")
        if not _is_sha256(verification.get("independent_series_certificate_sha256")):
            raise ReplayValidationError("independent series digest is invalid")
    if (
        production
        and expectation.status == "fail_closed"
        and verification
        != {
            "status": "passed_expected_fail_closed",
            "enumeration_allowed": False,
            "failure_type": expectation.fixture_input["failure_type"],
            "failure_message": expectation.fixture_input["failure_message"],
        }
    ):
        raise ReplayValidationError("fail-closed verification receipt mismatch")
    if not production and verification != {
        "status": "synthetic_not_executed",
        "real_engine_executed": False,
        "independent_verification_executed": False,
    }:
        raise ReplayValidationError("synthetic receipt falsely asserts real verification")
    if payload.get("independent_verification_sha256") != sha256_json(verification):
        raise ReplayValidationError("independent verification digest mismatch")
    unhashed = dict(payload)
    embedded = unhashed.pop("receipt_sha256", None)
    if embedded != sha256_json(unhashed):
        raise ReplayValidationError("replay receipt self-hash mismatch")


def _reject_unexpected_receipt_files(context: ReplayContext, receipts_dir: Path) -> None:
    expected = {f"{item.receipt_id}.json" for item in context.expectations}
    actual = {item.name for item in receipts_dir.glob("*.json")}
    unexpected = sorted(actual - expected)
    if unexpected:
        raise ReplayValidationError(f"duplicate or unexpected replay receipts: {unexpected}")


def _group_expectations(
    expectations: Sequence[ReplayExpectation],
) -> tuple[tuple[ReplayExpectation, ...], ...]:
    groups: list[list[ReplayExpectation]] = []
    for item in expectations:
        if not groups or groups[-1][0].source_fixture_name != item.source_fixture_name:
            groups.append([item])
        else:
            groups[-1].append(item)
    return tuple(tuple(group) for group in groups)


def _validate_production_context(context: ReplayContext, output_root: Path) -> None:
    if context.execution_mode != "real_engine_production":
        raise ReplayValidationError("production replay rejects synthetic test contexts")
    _require_current_head(context.repository_root, context.repository_commit)
    current_tree = _git_output(context.repository_root, ["rev-parse", "HEAD^{tree}"])
    if current_tree != context.commit_tree_oid:
        raise ReplayValidationError("production replay commit tree changed")
    verification = context.source_verification
    if verification.get("clean_worktree_excluding_output_root") is not True:
        raise ReplayValidationError("production replay requires a clean-tree source receipt")
    output = output_root.resolve()
    if output == context.repository_root or context.repository_root not in output.parents:
        raise ReplayValidationError("production output root must be a strict repository child")
    expected_output = output.relative_to(context.repository_root).as_posix()
    if verification.get("output_root_repo_relative") != expected_output:
        raise ReplayValidationError("production output root differs from source verification")
    fresh = verify_production_source(
        context.repository_root, context.repository_commit, output_root
    )
    if fresh != verification:
        raise ReplayValidationError("production source verification is stale or mismatched")


def _head_only_source_verification(root: Path, repository_commit: str) -> dict[str, Any]:
    tree_oid = _git_output(root, ["rev-parse", "HEAD^{tree}"])
    payload: dict[str, Any] = {
        "schema_version": SOURCE_VERIFICATION_SCHEMA,
        "verification_mode": "exact-head-only-context-load-no-execution-authorization",
        "repository_commit": repository_commit,
        "commit_tree_oid": tree_oid,
        "head_matches_declared_commit": True,
        "clean_worktree_excluding_output_root": None,
        "output_root_repo_relative": None,
    }
    payload["source_verification_sha256"] = sha256_json(payload)
    return payload


def _validate_source_verification(
    root: Path, repository_commit: str, verification: Mapping[str, Any]
) -> None:
    if verification.get("schema_version") != SOURCE_VERIFICATION_SCHEMA:
        raise ReplayValidationError("production source verification schema changed")
    if verification.get("repository_commit") != repository_commit:
        raise ReplayValidationError("source verification commit mismatch")
    if verification.get("head_matches_declared_commit") is not True:
        raise ReplayValidationError("source verification does not attest exact HEAD")
    tree_oid = _git_output(root, ["rev-parse", "HEAD^{tree}"])
    if verification.get("commit_tree_oid") != tree_oid or not _is_git_oid(tree_oid):
        raise ReplayValidationError("source verification commit tree mismatch")
    unhashed = dict(verification)
    embedded = unhashed.pop("source_verification_sha256", None)
    if embedded != sha256_json(unhashed):
        raise ReplayValidationError("source verification self-hash mismatch")


def _require_current_head(root: Path, repository_commit: str) -> None:
    if not _is_git_oid(repository_commit):
        raise ReplayValidationError("repository commit must be an exact 40-hex Git OID")
    actual = current_repository_commit(root)
    if actual != repository_commit:
        raise ReplayValidationError(
            f"declared repository commit does not match current HEAD: {repository_commit}"
        )


def _git_output(root: Path, arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _porcelain_paths(raw: bytes) -> tuple[str, ...]:
    tokens = raw.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(tokens):
        record = tokens[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise ReplayValidationError("could not parse Git porcelain status")
        status = record[:2]
        paths.append(record[3:].decode("utf-8", errors="surrogateescape"))
        if b"R" in status or b"C" in status:
            if index >= len(tokens) or not tokens[index]:
                raise ReplayValidationError("incomplete Git rename/copy status")
            paths.append(tokens[index].decode("utf-8", errors="surrogateescape"))
            index += 1
    return tuple(paths)


def _verify_embedded_hash(
    payload: Mapping[str, Any], hash_field: str, qualified_value: str
) -> None:
    unhashed = dict(payload)
    embedded = unhashed.pop(hash_field, None)
    if embedded != qualified_value or embedded != sha256_json(unhashed):
        raise ReplayValidationError(f"qualified artifact {hash_field} mismatch")


def _load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise ReplayValidationError(f"JSON artifact is not an object: {path}")
    return cast(dict[str, Any], value)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_git_oid(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _receipt_id(source_name: str, civil_date: str) -> str:
    safe = "".join(character if character.isalnum() else "-" for character in source_name)
    return f"{safe.strip('-')}-{civil_date}".lower()


def fake_receipt_executor() -> FixtureExecutor:
    """Return a no-astronomy executor that cannot claim independent verification."""

    def execute(
        context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        return tuple(
            make_receipt(
                context,
                item,
                interval_count=item.committed_interval_count,
                ordered_interval_list_sha256=sha256_json(
                    {
                        "synthetic_orchestration_test_only": True,
                        "receipt_id": item.receipt_id,
                    }
                ),
                ordered_full_state_vector_sha256=(
                    item.committed_ordered_full_state_vector_sha256
                ),
                coverage_receipt_sha256=item.committed_coverage_receipt_sha256,
                result_sha256=item.committed_result_sha256,
                independent_verification={
                    "status": "synthetic_not_executed",
                    "real_engine_executed": False,
                    "independent_verification_executed": False,
                },
            )
            for item in expectations
        )

    return execute
