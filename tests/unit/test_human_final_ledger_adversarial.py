from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.cli import main
from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.human import (
    FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
    FrozenHumanEvaluationProtocol,
    FrozenHumanModelBundle,
    HumanBlindCase,
    HumanBlindCohort,
    HumanCandidate,
    HumanCase,
    HumanCohortAnswerKey,
    HumanDataset,
    HumanPredictionFreeze,
    HumanPredictionSet,
    HumanSymbolicPrevalenceArtifact,
    candidate_universe_sha256,
    symbolic_reference,
)
from hdmatch.human.artifacts import (
    FinalTestReleaseReceipt,
    FinalTestRevealLedgerReceipt,
    final_test_cohort_lock_path,
    final_test_reveal_ledger_path,
    release_receipt_path,
    verify_final_test_release_receipt,
    write_final_test_freeze_ledger_receipt,
    write_final_test_release_receipt,
    write_final_test_reveal_ledger_receipt,
)
from hdmatch.runtime import MODEL_A_ID, load_runtime_model
from hdmatch.schemas import Activation, ChartFeatures
from hdmatch.util import sha256_json

ROOT = Path(__file__).resolve().parents[2]


def _runtime():  # type: ignore[no-untyped-def]
    return load_runtime_model(
        MODEL_A_ID,
        model_a_mapping_path=ROOT / "mappings" / "mapping_library_v1.json",
    )


def _chart(chart_type: str) -> ChartFeatures:
    generator = chart_type == "generator"
    return ChartFeatures(
        personality_utc=datetime(2000, 1, 1, tzinfo=UTC),
        design_utc=datetime(1999, 10, 1, tzinfo=UTC),
        type=chart_type,
        strategy="wait_to_respond" if generator else "wait_for_invitation",
        authority="sacral" if generator else "splenic",
        profile="1/3" if generator else "2/4",
        definition="single_definition",
        defined_centers=("sacral",) if generator else ("spleen",),
        activations={
            "personality:sun": Activation(
                body="sun",
                side="personality",
                longitude=0.0,
                gate=41,
                line=1,
            )
        },
    )


def _case(participant_id: str, cohort: str, chart_type: str, day: int) -> HumanCase:
    chart = _chart(chart_type)
    answer = _runtime().library.canonical_answers(chart)["D01"]
    return HumanCase(
        participant_id=participant_id,
        cohort=cohort,
        responses={"D01": answer},
        response_reliability={"D01": 1.0},
        chart_features=chart.model_dump(mode="json"),
        birth_year=2000,
        birth_month=1,
        birth_day=day,
    )


@dataclass(frozen=True)
class _FinalLedgerRun:
    split: Path
    bundle: Path
    protocol: Path
    blind: Path
    ledger: Path
    run_dir: Path
    encryption_key: Path | None
    truths: dict[str, str]

    @property
    def predictions(self) -> Path:
        return self.run_dir / "human.predictions.json"

    @property
    def prediction_freeze(self) -> Path:
        return self.run_dir / "human.prediction.freeze.json"

    @property
    def encrypted_answer_key(self) -> Path:
        return self.run_dir / "human.answer-key.json.enc"


def _import_and_fit(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "private-source.json"
    write_new_canonical_json(
        source,
        HumanDataset(
            questionnaire_version="Q-FIXTURE-1",
            cases=(
                _case("DEV-G", "development", "generator", 1),
                _case("DEV-P", "development", "projector", 2),
                _case("FINAL-G", "final_test", "generator", 5),
                _case("FINAL-P", "final_test", "projector", 6),
            ),
        ),
    )
    imported = tmp_path / "private-import"
    assert main(
        [
            "human-import",
            "--dataset",
            str(source),
            "--questionnaire-version",
            "Q-FIXTURE-1",
            "--output-dir",
            str(imported),
            "--seed",
            "7",
        ]
    ) == 0
    bundle_dir = tmp_path / "fit"
    dataset = imported / "human.dataset.json"
    split = imported / "person.split.json"
    assert main(
        [
            "human-fit",
            "--dataset",
            str(dataset),
            "--split-manifest",
            str(split),
            "--output-dir",
            str(bundle_dir),
            "--bundle-id",
            "FINAL-LEDGER-ADVERSARIAL",
            "--feature",
            "type",
            "--permutation-count",
            "2",
        ]
    ) == 0
    return split, bundle_dir / "human-model.bundle.json"


def _freeze_final_protocol(
    tmp_path: Path,
    split: Path,
    bundle: Path,
    ledger: Path,
    *,
    release_id: str = "FINAL-LEDGER-RELEASE-1",
    output_name: str = "protocol-final",
) -> Path:
    output = tmp_path / output_name
    assert main(
        [
            "human-freeze-protocol",
            "--bundle",
            str(bundle),
            "--split-manifest",
            str(split),
            "--output-dir",
            str(output),
            "--protocol-id",
            f"PROTOCOL-{release_id}",
            "--cohort",
            "final_test",
            "--candidate-universe-rule",
            "two predeclared fixture candidates",
            "--selected-primary-method",
            "hybrid_hd",
            "--final-test-release-id",
            release_id,
            "--final-test-release-acknowledgement",
            FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
            "--release-ledger",
            str(ledger),
        ]
    ) == 0
    return output / "human-evaluation.protocol.json"


def _write_blind_artifacts(
    tmp_path: Path,
    protocol_path: Path,
    bundle_path: Path,
) -> tuple[Path, Path, Path, dict[str, str]]:
    protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(protocol_path))
    bundle = FrozenHumanModelBundle.model_validate(load_json_bytes(bundle_path))
    cases: list[HumanBlindCase] = []
    truths: dict[str, str] = {}
    for participant_id in protocol.participant_ids:
        generator = participant_id.endswith("G")
        answer = _runtime().library.canonical_answers(
            _chart("generator" if generator else "projector")
        )["D01"]
        candidates = (
            HumanCandidate(
                candidate_id="GENERATOR-CANDIDATE",
                chart_features=_chart("generator").model_dump(mode="json"),
                local_year=2000,
                local_month=1,
                local_day=5,
            ),
            HumanCandidate(
                candidate_id="PROJECTOR-CANDIDATE",
                chart_features=_chart("projector").model_dump(mode="json"),
                local_year=2000,
                local_month=1,
                local_day=6,
            ),
        )
        cases.append(
            HumanBlindCase(
                participant_id=participant_id,
                cohort="final_test",
                questionnaire_version=bundle.questionnaire_version,
                responses={"D01": answer},
                response_reliability={"D01": 1.0},
                candidates=candidates,
            )
        )
        truths[participant_id] = (
            "GENERATOR-CANDIDATE" if generator else "PROJECTOR-CANDIDATE"
        )
    case_tuple = tuple(cases)
    blind = HumanBlindCohort(
        protocol_id=protocol.protocol_id,
        protocol_sha256=protocol.sha256,
        cohort="final_test",
        candidate_universe_sha256=candidate_universe_sha256(case_tuple),
        cases=case_tuple,
    )
    blind_path = tmp_path / "final.blind.json"
    write_new_canonical_json(blind_path, blind)
    runtime = _runtime()
    prevalence_source = tmp_path / "final.prevalence-source.json"
    write_new_canonical_json(
        prevalence_source,
        {
            "schema_version": "fixture-candidate-universe-duration-v1",
            "candidate_universe_sha256": blind.candidate_universe_sha256,
        },
    )
    prevalence = HumanSymbolicPrevalenceArtifact(
        symbolic_model=symbolic_reference(runtime),
        candidate_universe_sha256=blind.candidate_universe_sha256,
        prevalence_by_anchor={
            mapping.anchor_id: 0.5 for mapping in runtime.library.frozen_mappings
        },
        source_artifact_sha256=sha256_file(prevalence_source),
        prevalence_semantics="duration-weighted-frozen-candidate-universe",
        created_at_utc=datetime.now(UTC),
    )
    prevalence_path = tmp_path / "final.prevalence.json"
    write_new_canonical_json(prevalence_path, prevalence)
    return blind_path, prevalence_path, prevalence_source, truths


def _setup_final_run(
    tmp_path: Path,
    *,
    freeze: bool = True,
    seal: bool = True,
    reveal: bool = False,
) -> _FinalLedgerRun:
    split, bundle = _import_and_fit(tmp_path)
    ledger = tmp_path / "external-release-ledger"
    protocol = _freeze_final_protocol(tmp_path, split, bundle, ledger)
    blind, prevalence, prevalence_source, truths = _write_blind_artifacts(
        tmp_path,
        protocol,
        bundle,
    )
    run_dir = tmp_path / "final-run"
    assert main(
        [
            "human-score",
            "--blind-cohort",
            str(blind),
            "--bundle",
            str(bundle),
            "--protocol",
            str(protocol),
            "--symbolic-prevalence",
            str(prevalence),
            "--symbolic-prevalence-source",
            str(prevalence_source),
            "--output-dir",
            str(run_dir),
        ]
    ) == 0
    if freeze:
        assert main(_freeze_arguments(bundle, protocol, run_dir, ledger)) == 0
    encryption_key: Path | None = None
    if seal:
        frozen_protocol = FrozenHumanEvaluationProtocol.model_validate(
            load_json_bytes(protocol)
        )
        frozen_blind = HumanBlindCohort.model_validate(load_json_bytes(blind))
        plaintext_key = tmp_path / "external-final.answer-key.json"
        write_new_canonical_json(
            plaintext_key,
            HumanCohortAnswerKey(
                cohort="final_test",
                protocol_sha256=frozen_protocol.sha256,
                blind_input_sha256=frozen_blind.blind_input_sha256,
                true_candidate_ids=truths,
                final_test_release_id=frozen_protocol.final_test_release_id,
            ),
        )
        encryption_key = tmp_path / "external-final.aes256.key"
        assert main(
            [
                "human-seal-key",
                "--plaintext-answer-key",
                str(plaintext_key),
                "--key-file",
                str(encryption_key),
                "--bundle",
                str(bundle),
                "--protocol",
                str(protocol),
                "--blind-cohort",
                str(blind),
                "--output-dir",
                str(run_dir),
            ]
        ) == 0
    result = _FinalLedgerRun(
        split=split,
        bundle=bundle,
        protocol=protocol,
        blind=blind,
        ledger=ledger,
        run_dir=run_dir,
        encryption_key=encryption_key,
        truths=truths,
    )
    if reveal:
        assert main(_reveal_arguments(result)) == 0
    return result


def _freeze_arguments(
    bundle: Path,
    protocol: Path,
    run_dir: Path,
    ledger: Path,
    *,
    output_dir: Path | None = None,
) -> list[str]:
    return [
        "human-freeze",
        "--predictions",
        str(run_dir / "human.predictions.json"),
        "--bundle",
        str(bundle),
        "--protocol",
        str(protocol),
        "--output-dir",
        str(output_dir or run_dir),
        "--release-ledger",
        str(ledger),
    ]


def _reveal_arguments(
    run: _FinalLedgerRun,
    *,
    predictions: Path | None = None,
    protocol: Path | None = None,
    bundle: Path | None = None,
    encrypted_answer_key: Path | None = None,
    output_dir: Path | None = None,
) -> list[str]:
    assert run.encryption_key is not None
    return [
        "human-reveal-evaluate",
        "--predictions",
        str(predictions or run.predictions),
        "--prediction-freeze",
        str(run.prediction_freeze),
        "--bundle",
        str(bundle or run.bundle),
        "--protocol",
        str(protocol or run.protocol),
        "--encrypted-answer-key",
        str(encrypted_answer_key or run.encrypted_answer_key),
        "--key-file",
        str(run.encryption_key),
        "--output-dir",
        str(output_dir or run.run_dir),
        "--release-ledger",
        str(run.ledger),
    ]


def test_final_ledger_rejects_same_release_id_twice(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path, freeze=False, seal=False)
    with pytest.raises(SystemExit) as error:
        _freeze_final_protocol(
            tmp_path,
            run.split,
            run.bundle,
            run.ledger,
            release_id="FINAL-LEDGER-RELEASE-1",
            output_name="same-release-again",
        )
    assert error.value.code == 2
    assert len(tuple(run.ledger.glob("*.final-test-release.json"))) == 1


def test_final_ledger_cohort_lock_survives_changed_release_id_and_participant_order(
    tmp_path: Path,
) -> None:
    run = _setup_final_run(tmp_path, freeze=False, seal=False)
    with pytest.raises(SystemExit) as changed_id_error:
        _freeze_final_protocol(
            tmp_path,
            run.split,
            run.bundle,
            run.ledger,
            release_id="CHANGED-RELEASE-ID",
            output_name="changed-release",
        )
    assert changed_id_error.value.code == 2

    protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol))
    reordered = protocol.model_copy(
        update={
            "protocol_id": "REORDERED-SAME-COHORT",
            "participant_ids": tuple(reversed(protocol.participant_ids)),
            "final_test_release_id": "REORDERED-RELEASE-ID",
        }
    )
    with pytest.raises(FileExistsError):
        write_final_test_release_receipt(run.ledger, reordered)
    assert len(tuple(run.ledger.glob("*.final-test-cohort-lock.json"))) == 1


def test_final_ledger_rejects_second_evaluation_of_same_cohort(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path, reveal=True)
    with pytest.raises(SystemExit) as error:
        main(_reveal_arguments(run, output_dir=tmp_path / "second-evaluation"))
    assert error.value.code == 2
    assert len(tuple(run.ledger.glob("*.final-test-reveal.json"))) == 1


def test_final_ledger_rejects_reveal_before_freeze_receipt(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path, freeze=False, seal=True)
    predictions = HumanPredictionSet.model_validate(load_json_bytes(run.predictions))
    bundle = FrozenHumanModelBundle.model_validate(load_json_bytes(run.bundle))
    protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol))
    synthetic_freeze = HumanPredictionFreeze(
        protocol_sha256=protocol.sha256,
        model_bundle_sha256=bundle.sha256,
        blind_input_sha256=predictions.blind_input_sha256,
        prediction_sha256=sha256_file(run.predictions),
        created_at_utc=max(predictions.created_at_utc, protocol.created_at_utc),
    )
    write_new_canonical_json(run.prediction_freeze, synthetic_freeze)
    with pytest.raises(SystemExit) as error:
        main(_reveal_arguments(run, output_dir=tmp_path / "premature-reveal"))
    assert error.value.code == 2
    assert not tuple(run.ledger.glob("*.final-test-reveal.json"))


def test_final_ledger_rejects_freeze_before_release_receipt(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path, freeze=False, seal=False)
    unreleased_ledger = tmp_path / "empty-unreleased-ledger"
    with pytest.raises(SystemExit) as error:
        main(
            _freeze_arguments(
                run.bundle,
                run.protocol,
                run.run_dir,
                unreleased_ledger,
                output_dir=tmp_path / "premature-freeze",
            )
        )
    assert error.value.code == 2
    assert not tuple(unreleased_ledger.glob("*.final-test-freeze.json"))


def test_final_ledger_rejects_changed_prediction_bytes(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path)
    predictions = HumanPredictionSet.model_validate(load_json_bytes(run.predictions))
    changed_path = tmp_path / "changed.predictions.json"
    write_new_canonical_json(
        changed_path,
        predictions.model_copy(
            update={"created_at_utc": predictions.created_at_utc + timedelta(seconds=1)}
        ),
    )
    with pytest.raises(SystemExit) as error:
        main(
            _reveal_arguments(
                run,
                predictions=changed_path,
                output_dir=tmp_path / "changed-prediction-reveal",
            )
        )
    assert error.value.code == 2
    assert not tuple(run.ledger.glob("*.final-test-reveal.json"))


@pytest.mark.parametrize("binding", ("protocol", "model", "split", "participants"))
def test_final_ledger_rejects_changed_protocol_model_split_or_participants(
    tmp_path: Path,
    binding: str,
) -> None:
    run = _setup_final_run(tmp_path, freeze=False, seal=False)
    protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol))
    updates: dict[str, object] = {
        "protocol": {"protocol_id": "CHANGED-PROTOCOL"},
        "model": {"model_bundle_sha256": "c" * 64},
        "split": {"split_manifest_sha256": "d" * 64},
        "participants": {"participant_ids": protocol.participant_ids + ("EXTRA-PERSON",)},
    }[binding]
    changed = protocol.model_copy(update=updates)
    with pytest.raises((FileNotFoundError, ValueError)):
        verify_final_test_release_receipt(run.ledger, changed)


def test_final_ledger_rejects_changed_encrypted_answer_key_after_reveal(
    tmp_path: Path,
) -> None:
    run = _setup_final_run(tmp_path, reveal=True)
    changed_key = tmp_path / "changed.answer-key.enc"
    changed_key.write_bytes(run.encrypted_answer_key.read_bytes() + b"tamper")
    assert sha256_file(changed_key) != sha256_file(run.encrypted_answer_key)
    ledger_receipt = FinalTestRevealLedgerReceipt.model_validate(
        load_json_bytes(next(run.ledger.glob("*.final-test-reveal.json")))
    )
    assert ledger_receipt.encrypted_answer_key_sha256 == sha256_file(
        run.encrypted_answer_key
    )
    with pytest.raises(SystemExit) as error:
        main(
            _reveal_arguments(
                run,
                encrypted_answer_key=changed_key,
                output_dir=tmp_path / "changed-key-reveal",
            )
        )
    assert error.value.code == 2


def test_final_ledger_rejects_timestamp_reversal(tmp_path: Path) -> None:
    run = _setup_final_run(tmp_path)
    protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol))
    with pytest.raises(ValueError, match="cannot predate protocol"):
        write_final_test_release_receipt(
            tmp_path / "backdated-release-ledger",
            protocol,
            created_at_utc=protocol.created_at_utc - timedelta(seconds=1),
        )

    release = FinalTestReleaseReceipt.model_validate(
        load_json_bytes(release_receipt_path(run.ledger, "FINAL-LEDGER-RELEASE-1"))
    )
    freeze = HumanPredictionFreeze.model_validate(load_json_bytes(run.prediction_freeze))
    backdated_freeze = freeze.model_copy(
        update={"created_at_utc": release.created_at_utc - timedelta(microseconds=1)}
    )
    with pytest.raises(ValueError, match="cannot predate release receipt"):
        write_final_test_freeze_ledger_receipt(run.ledger, protocol, backdated_freeze)

    with pytest.raises(ValueError, match="reveal cannot predate freeze"):
        write_final_test_reveal_ledger_receipt(
            run.ledger,
            protocol,
            freeze,
            encrypted_answer_key_sha256=sha256_file(run.encrypted_answer_key),
            comparison_report_sha256="e" * 64,
            revealed_at_utc=freeze.created_at_utc - timedelta(microseconds=1),
        )


def test_final_ledger_survives_deleted_or_renamed_normal_run_artifacts(
    tmp_path: Path,
) -> None:
    run = _setup_final_run(tmp_path, reveal=True)
    ledger_path = final_test_reveal_ledger_path(run.ledger, "FINAL-LEDGER-RELEASE-1")
    ledger_hash = sha256_file(ledger_path)
    (run.run_dir / "human.comparison.report.json").rename(
        run.run_dir / "renamed.comparison.report.json"
    )
    (run.run_dir / "human.answer-key.reveal.receipt.json").unlink()
    (run.run_dir / "human-evaluation.receipt.json").unlink()
    with pytest.raises(SystemExit) as error:
        main(_reveal_arguments(run))
    assert error.value.code == 2
    assert sha256_file(ledger_path) == ledger_hash
    assert final_test_cohort_lock_path(
        run.ledger,
        FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol)),
    ).is_file()
    assert sha256_json(
        FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol)).participant_ids
    ) in final_test_cohort_lock_path(
        run.ledger,
        FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(run.protocol)),
    ).name
