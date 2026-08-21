from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.cli import main
from hdmatch.experiments.canonical import (
    load_json_bytes,
    sha256_file,
    write_new_canonical_json,
)
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
    HumanSymbolicPrevalenceArtifact,
    HumanWorkflowReceipt,
    candidate_universe_sha256,
    symbolic_reference,
)
from hdmatch.runtime import MODEL_A_ID, load_runtime_model
from hdmatch.schemas import Activation, ChartFeatures

ROOT = Path(__file__).resolve().parents[2]


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


def _runtime():  # type: ignore[no-untyped-def]
    return load_runtime_model(
        MODEL_A_ID,
        model_a_mapping_path=ROOT / "mappings" / "mapping_library_v1.json",
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


def _private_import(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "private-source.json"
    dataset = HumanDataset(
        questionnaire_version="Q-FIXTURE-1",
        cases=(
            _case("DEV-G", "development", "generator", 1),
            _case("DEV-P", "development", "projector", 2),
            _case("VAL-G", "validation", "generator", 3),
            _case("VAL-P", "validation", "projector", 4),
            _case("FINAL-G", "final_test", "generator", 5),
            _case("FINAL-P", "final_test", "projector", 6),
        ),
    )
    write_new_canonical_json(source, dataset)
    imported = tmp_path / "private-import"
    assert (
        main(
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
        )
        == 0
    )
    return imported / "human.dataset.json", imported / "person.split.json"


def _fit_bundle(tmp_path: Path, dataset: Path, split: Path) -> Path:
    fit_dir = tmp_path / "fit"
    assert (
        main(
            [
                "human-fit",
                "--dataset",
                str(dataset),
                "--split-manifest",
                str(split),
                "--output-dir",
                str(fit_dir),
                "--bundle-id",
                "HUMAN-FIXTURE-BUNDLE",
                "--feature",
                "type",
                "--permutation-count",
                "2",
            ]
        )
        == 0
    )
    return fit_dir / "human-model.bundle.json"


def _freeze_protocol(
    tmp_path: Path,
    bundle: Path,
    split: Path,
    cohort: str,
    *,
    release_id: str | None = None,
    ledger: Path | None = None,
) -> Path:
    protocol_dir = tmp_path / f"protocol-{cohort}"
    arguments = [
        "human-freeze-protocol",
        "--bundle",
        str(bundle),
        "--split-manifest",
        str(split),
        "--output-dir",
        str(protocol_dir),
        "--protocol-id",
        f"PROTOCOL-{cohort.upper()}",
        "--cohort",
        cohort,
        "--candidate-universe-rule",
        "two predeclared fixture candidates",
        "--selected-primary-method",
        "hybrid_hd",
    ]
    if release_id is not None and ledger is not None:
        arguments.extend(
            [
                "--final-test-release-id",
                release_id,
                "--final-test-release-acknowledgement",
                FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
                "--release-ledger",
                str(ledger),
            ]
        )
    assert main(arguments) == 0
    return protocol_dir / "human-evaluation.protocol.json"


def _blind_artifacts(
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
        cases.append(
            HumanBlindCase(
                participant_id=participant_id,
                cohort=protocol.cohort,
                questionnaire_version=bundle.questionnaire_version,
                responses={"D01": answer},
                response_reliability={"D01": 1.0},
                candidates=(
                    HumanCandidate(
                        candidate_id="GENERATOR-CANDIDATE",
                        chart_features=_chart("generator").model_dump(mode="json"),
                        local_year=2000,
                        local_month=1,
                        local_day=3,
                    ),
                    HumanCandidate(
                        candidate_id="PROJECTOR-CANDIDATE",
                        chart_features=_chart("projector").model_dump(mode="json"),
                        local_year=2000,
                        local_month=1,
                        local_day=4,
                    ),
                ),
            )
        )
        truths[participant_id] = (
            "GENERATOR-CANDIDATE" if generator else "PROJECTOR-CANDIDATE"
        )
    case_tuple = tuple(cases)
    blind = HumanBlindCohort(
        protocol_id=protocol.protocol_id,
        protocol_sha256=protocol.sha256,
        cohort=protocol.cohort,
        candidate_universe_sha256=candidate_universe_sha256(case_tuple),
        cases=case_tuple,
    )
    blind_path = tmp_path / f"{protocol.cohort}.blind.json"
    write_new_canonical_json(blind_path, blind)
    runtime = _runtime()
    prevalence_source_path = tmp_path / f"{protocol.cohort}.prevalence-source.json"
    write_new_canonical_json(
        prevalence_source_path,
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
        source_artifact_sha256=sha256_file(prevalence_source_path),
        prevalence_semantics="duration-weighted-frozen-candidate-universe",
        created_at_utc=datetime.now(UTC),
    )
    prevalence_path = tmp_path / f"{protocol.cohort}.prevalence.json"
    write_new_canonical_json(prevalence_path, prevalence)
    return blind_path, prevalence_path, prevalence_source_path, truths


def test_cli_runs_blind_validation_pipeline_with_exact_receipts(tmp_path: Path) -> None:
    dataset, split = _private_import(tmp_path)
    bundle = _fit_bundle(tmp_path, dataset, split)
    protocol = _freeze_protocol(tmp_path, bundle, split, "validation")
    blind, prevalence, prevalence_source, truths = _blind_artifacts(
        tmp_path,
        protocol,
        bundle,
    )
    run_dir = tmp_path / "validation-run"
    assert (
        main(
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
        )
        == 0
    )
    score_receipt = HumanWorkflowReceipt.model_validate(
        load_json_bytes(run_dir / "human-score.receipt.json")
    )
    assert score_receipt.answer_key_accessed is False
    assert (
        main(
            [
                "human-freeze",
                "--predictions",
                str(run_dir / "human.predictions.json"),
                "--bundle",
                str(bundle),
                "--protocol",
                str(protocol),
                "--output-dir",
                str(run_dir),
            ]
        )
        == 0
    )
    frozen_protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(protocol))
    frozen_blind = HumanBlindCohort.model_validate(load_json_bytes(blind))
    plaintext_key = tmp_path / "validation.answer-key.json"
    write_new_canonical_json(
        plaintext_key,
        HumanCohortAnswerKey(
            cohort="validation",
            protocol_sha256=frozen_protocol.sha256,
            blind_input_sha256=frozen_blind.blind_input_sha256,
            true_candidate_ids=truths,
        ),
    )
    encryption_key = tmp_path / "validation.aes256.key"
    assert (
        main(
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
        )
        == 0
    )
    assert (
        main(
            [
                "human-reveal-evaluate",
                "--predictions",
                str(run_dir / "human.predictions.json"),
                "--prediction-freeze",
                str(run_dir / "human.prediction.freeze.json"),
                "--bundle",
                str(bundle),
                "--protocol",
                str(protocol),
                "--encrypted-answer-key",
                str(run_dir / "human.answer-key.json.enc"),
                "--key-file",
                str(encryption_key),
                "--output-dir",
                str(run_dir),
            ]
        )
        == 0
    )
    evaluation_receipt = HumanWorkflowReceipt.model_validate(
        load_json_bytes(run_dir / "human-evaluation.receipt.json")
    )
    assert evaluation_receipt.answer_key_accessed is True
    assert "external_answer_key" not in evaluation_receipt.input_sha256
    assert (run_dir / "human.comparison.report.json").is_file()


def test_final_release_ledger_rejects_protocol_freeze_and_reveal_reuse(tmp_path: Path) -> None:
    dataset, split = _private_import(tmp_path)
    bundle = _fit_bundle(tmp_path, dataset, split)
    ledger = tmp_path / "release-ledger"
    protocol = _freeze_protocol(
        tmp_path,
        bundle,
        split,
        "final_test",
        release_id="FINAL-RELEASE-FIXTURE-1",
        ledger=ledger,
    )
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "human-freeze-protocol",
                "--bundle",
                str(bundle),
                "--split-manifest",
                str(split),
                "--output-dir",
                str(tmp_path / "second-final-protocol"),
                "--protocol-id",
                "SECOND-FINAL-PROTOCOL",
                "--cohort",
                "final_test",
                "--candidate-universe-rule",
                "two predeclared fixture candidates",
                "--selected-primary-method",
                "hybrid_hd",
                "--final-test-release-id",
                "FINAL-RELEASE-FIXTURE-1",
                "--final-test-release-acknowledgement",
                FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
                "--release-ledger",
                str(ledger),
            ]
        )
    assert exc_info.value.code == 2
    assert len(tuple(ledger.glob("*.final-test-release.json"))) == 1
    with pytest.raises(SystemExit) as renamed_release_error:
        main(
            [
                "human-freeze-protocol",
                "--bundle",
                str(bundle),
                "--split-manifest",
                str(split),
                "--output-dir",
                str(tmp_path / "renamed-final-release"),
                "--protocol-id",
                "RENAMED-FINAL-PROTOCOL",
                "--cohort",
                "final_test",
                "--candidate-universe-rule",
                "two predeclared fixture candidates",
                "--selected-primary-method",
                "hybrid_hd",
                "--final-test-release-id",
                "RENAMED-FINAL-RELEASE",
                "--final-test-release-acknowledgement",
                FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
                "--release-ledger",
                str(ledger),
            ]
        )
    assert renamed_release_error.value.code == 2
    assert len(tuple(ledger.glob("*.final-test-cohort-lock.json"))) == 1

    blind, prevalence, prevalence_source, truths = _blind_artifacts(
        tmp_path,
        protocol,
        bundle,
    )
    run_dir = tmp_path / "final-run"
    assert (
        main(
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
        )
        == 0
    )
    freeze_arguments = [
        "human-freeze",
        "--predictions",
        str(run_dir / "human.predictions.json"),
        "--bundle",
        str(bundle),
        "--protocol",
        str(protocol),
        "--output-dir",
        str(run_dir),
        "--release-ledger",
        str(ledger),
    ]
    assert main(freeze_arguments) == 0
    duplicate_freeze = freeze_arguments.copy()
    duplicate_freeze[duplicate_freeze.index(str(run_dir))] = str(tmp_path / "duplicate-freeze")
    with pytest.raises(SystemExit) as duplicate_freeze_error:
        main(duplicate_freeze)
    assert duplicate_freeze_error.value.code == 2
    assert len(tuple(ledger.glob("*.final-test-freeze.json"))) == 1

    frozen_protocol = FrozenHumanEvaluationProtocol.model_validate(load_json_bytes(protocol))
    frozen_blind = HumanBlindCohort.model_validate(load_json_bytes(blind))
    plaintext_key = tmp_path / "final.answer-key.json"
    write_new_canonical_json(
        plaintext_key,
        HumanCohortAnswerKey(
            cohort="final_test",
            protocol_sha256=frozen_protocol.sha256,
            blind_input_sha256=frozen_blind.blind_input_sha256,
            true_candidate_ids=truths,
            final_test_release_id="FINAL-RELEASE-FIXTURE-1",
        ),
    )
    encryption_key = tmp_path / "final.aes256.key"
    assert (
        main(
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
        )
        == 0
    )
    reveal_arguments = [
        "human-reveal-evaluate",
        "--predictions",
        str(run_dir / "human.predictions.json"),
        "--prediction-freeze",
        str(run_dir / "human.prediction.freeze.json"),
        "--bundle",
        str(bundle),
        "--protocol",
        str(protocol),
        "--encrypted-answer-key",
        str(run_dir / "human.answer-key.json.enc"),
        "--key-file",
        str(encryption_key),
        "--output-dir",
        str(run_dir),
        "--release-ledger",
        str(ledger),
    ]
    assert main(reveal_arguments) == 0
    final_report = load_json_bytes(run_dir / "human.comparison.report.json")
    assert final_report["claim_boundary"].startswith("untouched person-level final test")
    duplicate_reveal = reveal_arguments.copy()
    duplicate_reveal[duplicate_reveal.index(str(run_dir), 2)] = str(
        tmp_path / "duplicate-reveal"
    )
    with pytest.raises(SystemExit) as duplicate_reveal_error:
        main(duplicate_reveal)
    assert duplicate_reveal_error.value.code == 2
    assert len(tuple(ledger.glob("*.final-test-reveal.json"))) == 1


def test_human_fit_rejects_content_changed_outside_development(tmp_path: Path) -> None:
    dataset_path, split = _private_import(tmp_path)
    dataset = HumanDataset.model_validate(load_json_bytes(dataset_path))
    changed_cases = tuple(
        case.model_copy(update={"responses": {"D01": "changed"}})
        if case.cohort == "validation"
        else case
        for case in dataset.cases
    )
    tampered_path = tmp_path / "tampered-full-dataset.json"
    write_new_canonical_json(
        tampered_path,
        dataset.model_copy(update={"cases": changed_cases}),
    )
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "human-fit",
                "--dataset",
                str(tampered_path),
                "--split-manifest",
                str(split),
                "--output-dir",
                str(tmp_path / "tampered-fit"),
                "--bundle-id",
                "TAMPERED",
                "--feature",
                "type",
            ]
        )
    assert exc_info.value.code == 2
