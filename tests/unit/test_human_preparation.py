from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.cli import main
from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.human import (
    FrozenHumanEvaluationProtocol,
    HumanBlindCase,
    HumanBlindCohort,
    HumanCandidate,
    HumanCandidateSet,
    HumanCandidateUniverse,
    HumanCase,
    HumanCohortAnswerKey,
    HumanDataset,
    HumanWorkflowReceipt,
    VerifiedBirthRecord,
    human_dataset_sha256,
    prepare_blind_cohort_artifacts,
)
from hdmatch.schemas import BehavioralResponse
from hdmatch.synthetic.sealing import AnswerKeySealingError
from hdmatch.util import sha256_json

ROOT = Path(__file__).resolve().parents[2]
NOW = datetime(2026, 8, 21, tzinfo=UTC)


def _birth_record(**updates: object) -> VerifiedBirthRecord:
    payload: dict[str, object] = {
        "local_datetime": "2000-01-02T12:00:00",
        "birthplace": "Fixture City",
        "iana_timezone": "UTC",
        "resolved_utc": "2000-01-02T12:00:00Z",
        "precision_minutes": 15,
        "provenance": {
            "source_kind": "fixture documented record",
            "verification_method": "fixture two-person transcription check",
        },
    }
    payload.update(updates)
    return VerifiedBirthRecord.model_validate(payload)


def _response() -> BehavioralResponse:
    return BehavioralResponse(
        question_id="Q037",
        cluster_id="LEARNING_MOTIVE",
        answer="C",
        behavioral_confidence=0.75,
        measurement_reliability=0.8,
        example_text="A synthetic example only.",
        counterexample_text="A synthetic counterexample only.",
    )


def _private_case(
    *,
    participant_id: str = "P-001",
    cohort: str = "validation",
) -> HumanCase:
    response = _response()
    return HumanCase(
        participant_id=participant_id,
        cohort=cohort,
        responses={response.question_id: response.answer},
        response_reliability={response.question_id: response.measurement_reliability},
        response_records=(response,),
        chart_features={"type": "fixture"},
        verified_birth_record=_birth_record(),
        birth_year=2000,
        birth_month=1,
        birth_day=2,
        documented_time_precision_minutes=15,
    )


def _protocol(*, participant_ids: tuple[str, ...] = ("P-001",)) -> FrozenHumanEvaluationProtocol:
    return FrozenHumanEvaluationProtocol(
        protocol_id="HUMAN-PREP-FIXTURE",
        cohort="validation",
        participant_ids=participant_ids,
        questionnaire_version="Q-RICH-1",
        split_manifest_sha256="a" * 64,
        model_bundle_sha256="b" * 64,
        candidate_universe_rule="caller-supplied fixture intervals",
        selected_primary_method="hybrid_hd",
        created_at_utc=NOW,
    )


def _candidate_set(participant_id: str = "P-001") -> HumanCandidateSet:
    return HumanCandidateSet(
        participant_id=participant_id,
        candidates=(
            HumanCandidate(
                candidate_id="EARLY",
                chart_features={"type": "early"},
                local_year=2000,
                local_month=1,
                local_day=2,
                start_utc=datetime(2000, 1, 2, 10, tzinfo=UTC),
                end_utc=datetime(2000, 1, 2, 11, tzinfo=UTC),
            ),
            HumanCandidate(
                candidate_id="TRUE-STABLE-INTERVAL",
                chart_features={"type": "fixture"},
                local_year=2000,
                local_month=1,
                local_day=2,
                start_utc=datetime(2000, 1, 2, 11, 30, tzinfo=UTC),
                end_utc=datetime(2000, 1, 2, 12, 30, tzinfo=UTC),
            ),
        ),
    )


def _write_inputs(
    tmp_path: Path,
    *,
    case: HumanCase | None = None,
    protocol: FrozenHumanEvaluationProtocol | None = None,
    universe_protocol_sha256: str | None = None,
    partition_split_sha256: str | None = None,
    candidate_set: HumanCandidateSet | None = None,
) -> tuple[Path, Path, Path, FrozenHumanEvaluationProtocol, HumanCandidateUniverse]:
    selected_protocol = protocol or _protocol()
    selected_case = case or _private_case()
    assert selected_case.cohort != "unassigned"
    partition = HumanDataset(
        schema_version="human-dataset-v2",
        questionnaire_version="Q-RICH-1",
        cases=(selected_case,),
        partition=selected_case.cohort,
        split_manifest_sha256=(
            partition_split_sha256 or selected_protocol.split_manifest_sha256
        ),
        full_dataset_sha256="d" * 64,
    )
    universe = HumanCandidateUniverse(
        protocol_id=selected_protocol.protocol_id,
        protocol_sha256=universe_protocol_sha256 or selected_protocol.sha256,
        cohort=selected_protocol.cohort,
        cases=(candidate_set or _candidate_set(),),
    )
    partition_path = tmp_path / "private" / "validation.partition.json"
    universe_path = tmp_path / "public" / "candidate-universe.any-extension"
    protocol_path = tmp_path / "public" / "protocol.json"
    write_new_canonical_json(partition_path, partition)
    write_new_canonical_json(universe_path, universe)
    write_new_canonical_json(protocol_path, selected_protocol)
    return partition_path, universe_path, protocol_path, selected_protocol, universe


def test_rich_response_list_migrates_only_to_exact_flattened_views() -> None:
    response = _response()
    case = HumanCase.model_validate(
        {
            "participant_id": "P-001",
            "cohort": "validation",
            "responses": [response.model_dump(mode="json")],
            "chart_features": {},
            "verified_birth_record": _birth_record().model_dump(mode="json"),
        }
    )
    assert case.responses == {"Q037": "C"}
    assert case.response_reliability == {"Q037": 0.8}
    assert case.evidence_weights == {"Q037": pytest.approx(0.6)}
    assert case.response_records == (response,)
    assert (case.birth_year, case.birth_month, case.birth_day) == (2000, 1, 2)
    with pytest.raises(ValidationError, match="human-dataset-v2"):
        HumanDataset(questionnaire_version="Q-RICH-1", cases=(case,))


def test_legacy_minimal_dataset_and_blind_hash_shapes_remain_compatible() -> None:
    legacy_dataset_payload = {
        "schema_version": "human-dataset-v1",
        "questionnaire_version": "Q-LEGACY-1",
        "cases": [
            {
                "participant_id": "LEGACY-1",
                "cohort": "development",
                "responses": {"Q1": "yes"},
                "response_reliability": {},
                "chart_features": {"type": "fixture"},
                "birth_year": None,
                "birth_month": None,
                "birth_day": None,
                "documented_time_precision_minutes": None,
                "metadata": {},
            }
        ],
        "source_sha256": None,
    }
    legacy_dataset = HumanDataset.model_validate(legacy_dataset_payload)
    assert human_dataset_sha256(legacy_dataset) == sha256_json(legacy_dataset_payload)

    legacy_blind_case_payload = {
        "participant_id": "LEGACY-1",
        "cohort": "validation",
        "questionnaire_version": "Q-LEGACY-1",
        "responses": {"Q1": "yes"},
        "response_reliability": {},
        "candidates": [
            {
                "candidate_id": "C1",
                "chart_features": {"type": "fixture"},
                "local_year": None,
                "local_month": None,
                "local_day": None,
            }
        ],
    }
    legacy_blind_case = HumanBlindCase.model_validate(legacy_blind_case_payload)
    assert legacy_blind_case.hash_payload() == legacy_blind_case_payload


def test_human_import_preserves_rich_versioned_private_partitions(tmp_path: Path) -> None:
    source = tmp_path / "rich-source.json"
    write_new_canonical_json(
        source,
        HumanDataset(
            schema_version="human-dataset-v2",
            questionnaire_version="Q-RICH-1",
            cases=(
                _private_case(participant_id="DEV-001", cohort="development"),
                _private_case(participant_id="P-001", cohort="validation"),
            ),
        ),
    )
    output = tmp_path / "private-import"
    assert (
        main(
            [
                "human-import",
                "--dataset",
                str(source),
                "--questionnaire-version",
                "Q-RICH-1",
                "--output-dir",
                str(output),
                "--seed",
                "17",
            ]
        )
        == 0
    )
    validation = HumanDataset.model_validate(
        load_json_bytes(output / "validation.private.cases.json", require_canonical=True)
    )
    assert validation.schema_version == "human-dataset-v2"
    assert validation.cases[0].response_records == (_response(),)
    assert validation.cases[0].verified_birth_record == _birth_record()


@pytest.mark.parametrize(
    ("updates", "message"),
    (
        ({"iana_timezone": "CST"}, "IANA timezone"),
        ({"local_datetime": "2000-02-30T12:00:00"}, "day"),
        (
            {
                "provenance": {
                    "source_kind": "   ",
                    "verification_method": "fixture check",
                }
            },
            "provenance",
        ),
    ),
)
def test_verified_birth_record_rejects_invalid_timezone_date_and_provenance(
    updates: dict[str, object],
    message: str,
) -> None:
    with pytest.raises((ValidationError, ValueError), match=message):
        _birth_record(**updates)


def test_verified_birth_record_rejects_fold_for_unique_local_time() -> None:
    with pytest.raises(ValidationError, match="forbidden for an unambiguous"):
        _birth_record(timezone_fold=0)


def test_human_schemas_reject_blank_participant_ids() -> None:
    payload = _private_case().model_dump(mode="json")
    payload["participant_id"] = "   "
    with pytest.raises(ValidationError, match="participant_id cannot be blank"):
        HumanCase.model_validate(payload)
    with pytest.raises(ValidationError, match="participant_id cannot be blank"):
        HumanCandidateSet(participant_id="   ", candidates=_candidate_set().candidates)


def test_candidate_and_blind_schemas_reject_truth_fields() -> None:
    with pytest.raises(ValidationError, match="forbidden truth field"):
        HumanCandidate(
            candidate_id="LEAK",
            chart_features={"engine_metadata": {"true_candidate_id": "LEAK"}},
        )
    blind_payload = {
        "participant_id": "P-001",
        "cohort": "validation",
        "questionnaire_version": "Q-RICH-1",
        "responses": {},
        "candidates": [],
        "verified_birth_record": _birth_record().model_dump(mode="json"),
    }
    with pytest.raises(ValidationError, match="verified_birth_record"):
        HumanBlindCase.model_validate(blind_payload)
    with pytest.raises(ValidationError, match="true_candidate_id"):
        HumanCandidateSet.model_validate(
            {
                "participant_id": "P-001",
                "candidates": [_candidate_set().candidates[0].model_dump(mode="json")],
                "true_candidate_id": "EARLY",
            }
        )


def test_human_prepare_blind_cli_round_trips_bindings_and_external_truth(
    tmp_path: Path,
) -> None:
    partition, universe_path, protocol_path, protocol, universe = _write_inputs(tmp_path)
    output_dir = tmp_path / "decoder-run"
    answer_key_path = tmp_path / "owner-secrets" / "validation.answer-key.data"
    assert (
        main(
            [
                "human-prepare-blind",
                "--partition",
                str(partition),
                "--candidate-universe",
                str(universe_path),
                "--protocol",
                str(protocol_path),
                "--output-dir",
                str(output_dir),
                "--answer-key-out",
                str(answer_key_path),
            ]
        )
        == 0
    )

    blind_path = output_dir / "human.blind-cohort.json"
    blind = HumanBlindCohort.model_validate(
        load_json_bytes(blind_path, require_canonical=True)
    )
    key = HumanCohortAnswerKey.model_validate(
        load_json_bytes(answer_key_path, require_canonical=True)
    )
    receipt = HumanWorkflowReceipt.model_validate(
        load_json_bytes(output_dir / "human-prepare-blind.receipt.json")
    )
    assert blind.schema_version == "human-blind-cohort-v2"
    assert blind.protocol_id == protocol.protocol_id
    assert blind.protocol_sha256 == protocol.sha256
    assert blind.candidate_universe_sha256 == universe.candidate_universe_sha256
    assert blind.cases[0].response_records == (_response(),)
    assert blind.cases[0].response_records[0].cluster_id == "LEARNING_MOTIVE"
    assert blind.cases[0].evidence_weights == {"Q037": pytest.approx(0.6)}
    serialized_blind = blind.model_dump(mode="json")
    for forbidden_birth_field in (
        "verified_birth_record",
        "local_datetime",
        "birthplace",
        "iana_timezone",
        "resolved_utc",
        "timezone_fold",
        "precision_minutes",
        "provenance",
    ):
        assert forbidden_birth_field not in str(serialized_blind)
    assert "true_candidate_id" not in str(serialized_blind)
    assert key.true_candidate_ids == {"P-001": "TRUE-STABLE-INTERVAL"}
    assert key.blind_input_sha256 == blind.blind_input_sha256
    assert key.protocol_sha256 == blind.protocol_sha256
    assert stat.S_IMODE(answer_key_path.stat().st_mode) == 0o600
    assert receipt.answer_key_accessed is True
    assert receipt.output_sha256 == {"human.blind-cohort.json": sha256_file(blind_path)}
    assert sha256_json(blind) == sha256_file(blind_path)


@pytest.mark.parametrize("mismatch", ("person", "cohort", "protocol", "split"))
def test_human_prepare_blind_rejects_person_cohort_protocol_and_split_mismatch(
    tmp_path: Path,
    mismatch: str,
) -> None:
    case = _private_case(
        participant_id="OTHER" if mismatch == "person" else "P-001",
        cohort="development" if mismatch == "cohort" else "validation",
    )
    partition, universe, protocol, _, _ = _write_inputs(
        tmp_path,
        case=case,
        universe_protocol_sha256="c" * 64 if mismatch == "protocol" else None,
        partition_split_sha256="e" * 64 if mismatch == "split" else None,
    )
    expected_message = {
        "person": "participants",
        "cohort": "cohort",
        "protocol": "protocol",
        "split": "person split",
    }[mismatch]
    with pytest.raises(ValueError, match=expected_message):
        prepare_blind_cohort_artifacts(
            partition,
            universe,
            protocol,
            tmp_path / "decoder-run",
            answer_key_output_path=tmp_path / "owner-secrets" / "key.data",
            repository_root=ROOT,
            created_at_utc=NOW,
        )


def test_human_prepare_blind_refuses_truth_under_decoder_or_repository_root(
    tmp_path: Path,
) -> None:
    partition, universe, protocol, _, _ = _write_inputs(tmp_path)
    output_dir = tmp_path / "decoder-run"
    with pytest.raises(AnswerKeySealingError, match="outside the decoder project root"):
        prepare_blind_cohort_artifacts(
            partition,
            universe,
            protocol,
            output_dir,
            answer_key_output_path=output_dir / "renamed-key.data",
            repository_root=ROOT,
            created_at_utc=NOW,
        )
