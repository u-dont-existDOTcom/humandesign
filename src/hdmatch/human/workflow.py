"""Bounded orchestration for canonical human-development and evaluation artifacts."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import sha256_file, write_new_canonical_json
from hdmatch.human.artifacts import (
    HumanRevealReceipt,
    HumanWorkflowReceipt,
    assert_final_test_reveal_unused,
    exact_file_hashes,
    final_test_cohort_lock_path,
    load_blind_cohort,
    load_evaluation_protocol,
    load_human_answer_key,
    load_human_dataset_artifact,
    load_human_prediction_freeze,
    load_human_predictions,
    load_model_bundle,
    load_split_manifest,
    load_symbolic_prevalence,
    release_receipt_path,
    verify_final_test_freeze_ledger_receipt,
    verify_final_test_release_receipt,
    write_final_test_freeze_ledger_receipt,
    write_final_test_release_receipt,
    write_final_test_reveal_ledger_receipt,
    write_workflow_receipt,
)
from hdmatch.human.dataset import HumanDataset, load_human_dataset
from hdmatch.human.protocol import (
    FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
    BoundSymbolicScorer,
    Cohort,
    FrozenHumanEvaluationProtocol,
    FrozenHumanModelBundle,
    HumanCohortAnswerKey,
    HumanComparisonReport,
    HumanPredictionFreeze,
    HumanPredictionSet,
    SymbolicModelReference,
    fit_development_model_bundle,
    freeze_final_test_protocol,
    freeze_human_evaluation_protocol,
    freeze_human_predictions,
    reveal_and_evaluate_human_cohort,
    score_blind_human_cohort,
    verify_human_prediction_freeze,
)
from hdmatch.human.splits import (
    PersonSplitManifest,
    create_person_splits,
    select_partition,
    validate_manifest_for_dataset,
)
from hdmatch.model import score_symbolic
from hdmatch.runtime import RuntimeSymbolicModel
from hdmatch.schemas import BehavioralResponse, ChartFeatures
from hdmatch.synthetic.sealing import (
    SealingMetadata,
    decrypt_answer_key_json,
    generate_key_file,
    require_external_path,
    seal_answer_key,
)
from hdmatch.util import sha256_json


def _path(path: str | Path) -> Path:
    return Path(path).expanduser()


def _ensure_new_directory(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)


def _human_partition(
    dataset: HumanDataset,
    manifest: PersonSplitManifest,
    cohort: Cohort,
) -> HumanDataset:
    return HumanDataset(
        questionnaire_version=dataset.questionnaire_version,
        cases=select_partition(dataset, manifest, cohort),
        source_sha256=dataset.source_sha256,
    )


def import_human_cases(
    source_path: str | Path,
    output_dir: str | Path,
    *,
    questionnaire_version: str,
    seed: int,
    validation_fraction: float,
    final_test_fraction: float,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> HumanWorkflowReceipt:
    """Validate and split private human records before any fitting process is started."""

    source = _path(source_path)
    directory = _path(output_dir)
    require_external_path(source, repository_root, label="private human source dataset")
    require_external_path(directory, repository_root, label="private human import directory")
    _ensure_new_directory(directory)
    dataset = load_human_dataset(source, questionnaire_version)
    manifest = create_person_splits(
        dataset,
        seed,
        validation_fraction=validation_fraction,
        final_test_fraction=final_test_fraction,
    )
    partitions = {
        "development.cases.json": _human_partition(dataset, manifest, "development"),
        "validation.private.cases.json": _human_partition(dataset, manifest, "validation"),
        "final_test.private.cases.json": _human_partition(dataset, manifest, "final_test"),
    }
    split_path = directory / "person.split.json"
    dataset_path = directory / "human.dataset.json"
    write_new_canonical_json(dataset_path, dataset)
    write_new_canonical_json(split_path, manifest)
    for filename, partition in partitions.items():
        write_new_canonical_json(directory / filename, partition)
    output_hashes = {
        "human.dataset.json": sha256_file(dataset_path),
        "person.split.json": sha256_file(split_path),
        **{
            filename: sha256_file(directory / filename)
            for filename in sorted(partitions)
        },
    }
    return write_workflow_receipt(
        directory / "human-import.receipt.json",
        stage="import",
        artifact_id=f"human-import:{manifest.dataset_hash[:16]}",
        input_sha256={"source_dataset": sha256_file(source)},
        output_sha256=output_hashes,
        repository_root=repository_root,
        answer_key_accessed=False,
        claim_boundary=(
            "private person-level partitioning only; no model fit or validation result"
        ),
        created_at_utc=created_at_utc,
    )


def fit_development_bundle_artifacts(
    dataset_path: str | Path,
    split_manifest_path: str | Path,
    output_dir: str | Path,
    *,
    bundle_id: str,
    symbolic_model: SymbolicModelReference,
    empirical_feature_names: Sequence[str],
    alpha: float,
    hybrid_symbolic_weight: float,
    permutation_count: int,
    permutation_seed: int,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> tuple[FrozenHumanModelBundle, HumanWorkflowReceipt]:
    """Validate the complete split, then pass only development people into fitting."""

    full_dataset_path = _path(dataset_path)
    split_path = _path(split_manifest_path)
    directory = _path(output_dir)
    require_external_path(full_dataset_path, repository_root, label="private full human dataset")
    require_external_path(split_path, repository_root, label="private human split manifest")
    _ensure_new_directory(directory)
    dataset = load_human_dataset_artifact(full_dataset_path)
    manifest = load_split_manifest(split_path)
    validate_manifest_for_dataset(dataset, manifest)
    development_cases = select_partition(dataset, manifest, "development")
    bundle = fit_development_model_bundle(
        development_cases,
        manifest=manifest,
        bundle_id=bundle_id,
        questionnaire_version=dataset.questionnaire_version,
        symbolic_model=symbolic_model,
        empirical_feature_names=empirical_feature_names,
        alpha=alpha,
        hybrid_symbolic_weight=hybrid_symbolic_weight,
        permutation_count=permutation_count,
        permutation_seed=permutation_seed,
        created_at_utc=created_at_utc,
    )
    bundle_path = directory / "human-model.bundle.json"
    write_new_canonical_json(bundle_path, bundle)
    receipt = write_workflow_receipt(
        directory / "human-fit.receipt.json",
        stage="fit-development",
        artifact_id=bundle.bundle_id,
        input_sha256=exact_file_hashes(
            full_human_dataset=full_dataset_path,
            person_split=split_path,
        ),
        output_sha256={"human-model.bundle.json": sha256_file(bundle_path)},
        repository_root=repository_root,
        answer_key_accessed=False,
        claim_boundary=(
            "complete dataset/split validated; only development people fitted; "
            "not predictive validation"
        ),
        created_at_utc=created_at_utc,
    )
    return bundle, receipt


def freeze_protocol_artifacts(
    bundle_path: str | Path,
    split_manifest_path: str | Path,
    output_dir: str | Path,
    *,
    protocol_id: str,
    cohort: Cohort,
    candidate_universe_rule: str,
    selected_primary_method: str,
    final_test_release_id: str | None,
    release_authorization: str | None,
    release_ledger_dir: str | Path | None,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> tuple[FrozenHumanEvaluationProtocol, HumanWorkflowReceipt]:
    """Freeze one cohort protocol; final-test releases require an external durable ledger."""

    model_path = _path(bundle_path)
    split_path = _path(split_manifest_path)
    directory = _path(output_dir)
    _ensure_new_directory(directory)
    bundle = load_model_bundle(model_path)
    manifest = load_split_manifest(split_path)
    if cohort == "final_test":
        if release_ledger_dir is None:
            raise ValueError("final-test protocol requires --release-ledger")
        ledger = _path(release_ledger_dir)
        require_external_path(ledger, repository_root, label="final-test release ledger")
        if final_test_release_id is None:
            raise ValueError("final-test protocol requires --final-test-release-id")
        protocol = freeze_final_test_protocol(
            bundle,
            manifest,
            protocol_id=protocol_id,
            candidate_universe_rule=candidate_universe_rule,
            selected_primary_method=selected_primary_method,
            final_test_release_id=final_test_release_id,
            release_authorization=release_authorization or "",
            created_at_utc=created_at_utc,
        )
        # Claim the ID before materializing the protocol. A failed/repeated claim burns no truth.
        release_path, _ = write_final_test_release_receipt(
            ledger,
            protocol,
            created_at_utc=created_at_utc,
        )
        release_output_hashes = {
            "final_test_release_receipt": sha256_file(release_path),
            "final_test_cohort_lock": sha256_file(
                final_test_cohort_lock_path(ledger, protocol)
            ),
        }
    else:
        if final_test_release_id is not None or release_authorization is not None:
            raise ValueError("final-test release arguments are forbidden for other cohorts")
        if release_ledger_dir is not None:
            raise ValueError("release ledger is only valid for final-test protocols")
        protocol = freeze_human_evaluation_protocol(
            bundle,
            manifest,
            protocol_id=protocol_id,
            cohort=cohort,
            candidate_universe_rule=candidate_universe_rule,
            selected_primary_method=selected_primary_method,
            created_at_utc=created_at_utc,
        )
        release_output_hashes = {}
    protocol_path = directory / "human-evaluation.protocol.json"
    write_new_canonical_json(protocol_path, protocol)
    receipt = write_workflow_receipt(
        directory / "human-protocol.receipt.json",
        stage="freeze-protocol",
        artifact_id=protocol.protocol_id,
        input_sha256=exact_file_hashes(model_bundle=model_path, person_split=split_path),
        output_sha256={
            "human-evaluation.protocol.json": sha256_file(protocol_path),
            **release_output_hashes,
        },
        repository_root=repository_root,
        answer_key_accessed=False,
        claim_boundary=(
            "frozen final-test release; no answers inspected"
            if cohort == "final_test"
            else "frozen development/validation protocol; no answers inspected"
        ),
        created_at_utc=created_at_utc,
    )
    return protocol, receipt


def symbolic_reference(runtime: RuntimeSymbolicModel) -> SymbolicModelReference:
    return SymbolicModelReference(
        model_id=runtime.model_id,
        model_sha256=runtime.model_sha256,
        mapping_sha256=runtime.mapping_sha256,
        question_bank_sha256=runtime.question_bank_sha256,
    )


def _symbolic_scorer(
    runtime: RuntimeSymbolicModel,
    prevalence_by_anchor: Mapping[str, float],
) -> BoundSymbolicScorer:
    reference = symbolic_reference(runtime)

    def score(
        responses: Mapping[str, str],
        chart_features: Mapping[str, Any],
        reliability: Mapping[str, float],
    ) -> float:
        chart = ChartFeatures.model_validate(chart_features)
        normalized = tuple(
            BehavioralResponse(
                question_id=question_id,
                cluster_id=question_id,
                answer=answer,
                behavioral_confidence=1.0,
                measurement_reliability=reliability.get(question_id, 1.0),
            )
            for question_id, answer in sorted(responses.items())
        )
        return score_symbolic(
            chart,
            normalized,
            runtime.library,
            prevalence_by_anchor,
        ).net_rubric_bits

    return BoundSymbolicScorer(reference=reference, score=score)


def _assert_no_human_answer_keys(repository_root: str | Path) -> None:
    """Fail blind scoring if a plaintext human key is readable under the decoder root."""

    root = Path(repository_root)
    offenders: list[str] = []
    for candidate in root.rglob("*.json"):
        if ".git" in candidate.parts or not candidate.is_file():
            continue
        try:
            payload = json.loads(candidate.read_bytes())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and payload.get("schema_version") == (
            "human-cohort-answer-key-v1"
        ):
            offenders.append(candidate.relative_to(root).as_posix())
    if offenders:
        raise RuntimeError(
            f"{len(offenders)} plaintext human answer key file(s) exist under decoder root"
        )


def score_blind_artifacts(
    blind_cohort_path: str | Path,
    bundle_path: str | Path,
    protocol_path: str | Path,
    symbolic_prevalence_path: str | Path,
    symbolic_prevalence_source_path: str | Path,
    output_dir: str | Path,
    *,
    runtime_symbolic_model: RuntimeSymbolicModel,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> tuple[HumanPredictionSet, HumanWorkflowReceipt]:
    """Blind-score without an answer-key argument or truth-bearing dataset mount."""

    _assert_no_human_answer_keys(repository_root)
    blind_path = _path(blind_cohort_path)
    model_path = _path(bundle_path)
    frozen_protocol_path = _path(protocol_path)
    prevalence_path = _path(symbolic_prevalence_path)
    prevalence_source_path = _path(symbolic_prevalence_source_path)
    directory = _path(output_dir)
    _ensure_new_directory(directory)
    bundle = load_model_bundle(model_path)
    protocol = load_evaluation_protocol(frozen_protocol_path)
    blind = load_blind_cohort(blind_path)
    prevalence = load_symbolic_prevalence(prevalence_path)
    if sha256_file(prevalence_source_path) != prevalence.source_artifact_sha256:
        raise ValueError("symbolic prevalence source artifact hash does not match")
    reference = symbolic_reference(runtime_symbolic_model)
    if reference != bundle.symbolic_model or prevalence.symbolic_model != bundle.symbolic_model:
        raise ValueError("runtime/prevalence symbolic model does not match the frozen bundle")
    if blind.protocol_id != protocol.protocol_id or blind.protocol_sha256 != protocol.sha256:
        raise ValueError("blind cohort is bound to a different protocol")
    if blind.cohort != protocol.cohort:
        raise ValueError("blind cohort does not match the protocol cohort")
    if prevalence.candidate_universe_sha256 != blind.candidate_universe_sha256:
        raise ValueError("symbolic prevalence is bound to a different candidate universe")
    predictions = score_blind_human_cohort(
        blind.cases,
        bundle=bundle,
        protocol=protocol,
        symbolic_scorer=_symbolic_scorer(
            runtime_symbolic_model,
            prevalence.prevalence_by_anchor,
        ),
        created_at_utc=created_at_utc,
    )
    prediction_path = directory / "human.predictions.json"
    write_new_canonical_json(prediction_path, predictions)
    receipt = write_workflow_receipt(
        directory / "human-score.receipt.json",
        stage="blind-score",
        artifact_id=protocol.protocol_id,
        input_sha256=exact_file_hashes(
            blind_cohort=blind_path,
            model_bundle=model_path,
            evaluation_protocol=frozen_protocol_path,
            symbolic_prevalence=prevalence_path,
            symbolic_prevalence_source=prevalence_source_path,
        ),
        output_sha256={"human.predictions.json": sha256_file(prediction_path)},
        repository_root=repository_root,
        answer_key_accessed=False,
        claim_boundary=(
            "blind person-level predictions only; no answer key accessed or validation claim"
        ),
        created_at_utc=created_at_utc,
    )
    return predictions, receipt


def freeze_prediction_artifacts(
    prediction_path: str | Path,
    bundle_path: str | Path,
    protocol_path: str | Path,
    output_dir: str | Path,
    *,
    release_ledger_dir: str | Path | None,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> tuple[HumanPredictionFreeze, HumanWorkflowReceipt]:
    predictions_path = _path(prediction_path)
    model_path = _path(bundle_path)
    frozen_protocol_path = _path(protocol_path)
    directory = _path(output_dir)
    _ensure_new_directory(directory)
    predictions = load_human_predictions(predictions_path)
    bundle = load_model_bundle(model_path)
    protocol = load_evaluation_protocol(frozen_protocol_path)
    freeze = freeze_human_predictions(
        predictions,
        bundle=bundle,
        protocol=protocol,
        created_at_utc=created_at_utc,
    )
    ledger_input_hashes: dict[str, str] = {}
    ledger_hashes: dict[str, str] = {}
    if protocol.cohort == "final_test":
        if release_ledger_dir is None:
            raise ValueError("final-test prediction freeze requires --release-ledger")
        ledger = _path(release_ledger_dir)
        require_external_path(ledger, repository_root, label="final-test release ledger")
        ledger_path, _ = write_final_test_freeze_ledger_receipt(ledger, protocol, freeze)
        assert protocol.final_test_release_id is not None
        ledger_input_hashes = {
            "final_test_release_receipt": sha256_file(
                release_receipt_path(ledger, protocol.final_test_release_id)
            ),
            "final_test_cohort_lock": sha256_file(
                final_test_cohort_lock_path(ledger, protocol)
            ),
        }
        ledger_hashes["final_test_freeze_ledger"] = sha256_file(ledger_path)
    elif release_ledger_dir is not None:
        raise ValueError("release ledger is only valid for final-test prediction freeze")
    freeze_path = directory / "human.prediction.freeze.json"
    write_new_canonical_json(freeze_path, freeze)
    receipt = write_workflow_receipt(
        directory / "human-freeze.receipt.json",
        stage="freeze-predictions",
        artifact_id=protocol.protocol_id,
        input_sha256={
            **exact_file_hashes(
                predictions=predictions_path,
                model_bundle=model_path,
                evaluation_protocol=frozen_protocol_path,
            ),
            **ledger_input_hashes,
        },
        output_sha256={
            "human.prediction.freeze.json": sha256_file(freeze_path),
            **ledger_hashes,
        },
        repository_root=repository_root,
        answer_key_accessed=False,
        claim_boundary="cryptographic prediction freeze; answer key remains unrevealed",
        created_at_utc=created_at_utc,
    )
    return freeze, receipt


def _human_key_sealing_metadata(
    protocol: FrozenHumanEvaluationProtocol,
    bundle: FrozenHumanModelBundle,
    blind_input_sha256: str,
) -> SealingMetadata:
    return SealingMetadata(
        experiment_id=protocol.protocol_id,
        blind_input_sha256=blind_input_sha256,
        model_sha256=bundle.sha256,
        question_bank_sha256=bundle.symbolic_model.question_bank_sha256,
        mapping_sha256=bundle.symbolic_model.mapping_sha256,
    )


def seal_human_answer_key_artifacts(
    plaintext_answer_key_path: str | Path,
    key_file_path: str | Path,
    bundle_path: str | Path,
    protocol_path: str | Path,
    blind_cohort_path: str | Path,
    output_dir: str | Path,
    *,
    repository_root: str | Path,
    created_at_utc: datetime | None = None,
) -> HumanWorkflowReceipt:
    """Seal a separately prepared human key; never copy plaintext into the project."""

    plaintext_path = _path(plaintext_answer_key_path)
    key_path = _path(key_file_path)
    model_path = _path(bundle_path)
    frozen_protocol_path = _path(protocol_path)
    blind_path = _path(blind_cohort_path)
    directory = _path(output_dir)
    require_external_path(plaintext_path, repository_root, label="plaintext human answer key")
    require_external_path(key_path, repository_root, label="human answer-key encryption key")
    _ensure_new_directory(directory)
    bundle = load_model_bundle(model_path)
    protocol = load_evaluation_protocol(frozen_protocol_path)
    blind = load_blind_cohort(blind_path)
    answer_key = load_human_answer_key(plaintext_path)
    if answer_key.protocol_sha256 != protocol.sha256 or answer_key.cohort != protocol.cohort:
        raise ValueError("human answer key is bound to a different frozen protocol")
    if blind.protocol_sha256 != protocol.sha256 or blind.cohort != protocol.cohort:
        raise ValueError("human blind cohort is bound to a different frozen protocol")
    if answer_key.blind_input_sha256 != blind.blind_input_sha256:
        raise ValueError("human answer key is bound to a different blind input")
    if (
        protocol.cohort == "final_test"
        and answer_key.final_test_release_id != protocol.final_test_release_id
    ):
        raise ValueError("final-test answer-key release ID does not match protocol")
    if not key_path.exists():
        generate_key_file(key_path, decoder_root=repository_root)
    encrypted_path = directory / "human.answer-key.json.enc"
    seal_answer_key(
        answer_key,
        encrypted_path=encrypted_path,
        key_path=key_path,
        metadata=_human_key_sealing_metadata(protocol, bundle, blind.blind_input_sha256),
        decoder_root=repository_root,
    )
    return write_workflow_receipt(
        directory / "human-key-seal.receipt.json",
        stage="seal-answer-key",
        artifact_id=protocol.protocol_id,
        input_sha256=exact_file_hashes(
            plaintext_answer_key=plaintext_path,
            model_bundle=model_path,
            evaluation_protocol=frozen_protocol_path,
            blind_cohort=blind_path,
        ),
        output_sha256={"human.answer-key.json.enc": sha256_file(encrypted_path)},
        repository_root=repository_root,
        answer_key_accessed=True,
        claim_boundary="evaluator-side key sealing only; no prediction or validation claim",
        created_at_utc=created_at_utc,
    )


def reveal_evaluate_artifacts(
    prediction_path: str | Path,
    prediction_freeze_path: str | Path,
    bundle_path: str | Path,
    protocol_path: str | Path,
    encrypted_answer_key_path: str | Path,
    key_file_path: str | Path,
    output_dir: str | Path,
    *,
    release_ledger_dir: str | Path | None,
    repository_root: str | Path,
    evaluated_at_utc: datetime | None = None,
) -> tuple[HumanComparisonReport, HumanRevealReceipt, HumanWorkflowReceipt]:
    """Verify freeze first, then load one external key in memory and retain all failures."""

    predictions_path = _path(prediction_path)
    freeze_path = _path(prediction_freeze_path)
    model_path = _path(bundle_path)
    frozen_protocol_path = _path(protocol_path)
    encrypted_key_path = _path(encrypted_answer_key_path)
    key_path = _path(key_file_path)
    directory = _path(output_dir)
    require_external_path(key_path, repository_root, label="human answer-key encryption key")
    _ensure_new_directory(directory)
    predictions = load_human_predictions(predictions_path)
    freeze = load_human_prediction_freeze(freeze_path)
    bundle = load_model_bundle(model_path)
    protocol = load_evaluation_protocol(frozen_protocol_path)
    # This verification happens before opening the external answer-key file.
    verify_human_prediction_freeze(
        predictions,
        freeze,
        bundle=bundle,
        protocol=protocol,
    )
    release_input_hashes: dict[str, str] = {}
    release_output_hashes: dict[str, str] = {}
    ledger: Path | None = None
    if protocol.cohort == "final_test":
        if release_ledger_dir is None:
            raise ValueError("final-test reveal requires --release-ledger")
        ledger = _path(release_ledger_dir)
        require_external_path(ledger, repository_root, label="final-test release ledger")
        receipt = verify_final_test_release_receipt(ledger, protocol)
        release_input_hashes["final_test_release_receipt"] = sha256_json(receipt)
        release_input_hashes["final_test_cohort_lock"] = sha256_file(
            final_test_cohort_lock_path(ledger, protocol)
        )
        freeze_receipt = verify_final_test_freeze_ledger_receipt(ledger, protocol, freeze)
        release_input_hashes["final_test_freeze_ledger"] = sha256_json(freeze_receipt)
        assert_final_test_reveal_unused(ledger, protocol)
    elif release_ledger_dir is not None:
        raise ValueError("release ledger is only valid for final-test reveal")
    raw_answer_key = decrypt_answer_key_json(
        encrypted_key_path,
        key_path=key_path,
        decoder_root=repository_root,
        expected_metadata=_human_key_sealing_metadata(
            protocol,
            bundle,
            predictions.blind_input_sha256,
        ),
    )
    answer_key = HumanCohortAnswerKey.model_validate(raw_answer_key)
    evaluation_time = evaluated_at_utc or datetime.now(UTC)
    report = reveal_and_evaluate_human_cohort(
        predictions,
        freeze,
        answer_key,
        bundle=bundle,
        protocol=protocol,
        evaluated_at_utc=evaluation_time,
    )
    if ledger is not None:
        report = report.model_copy(
            update={
                "claim_boundary": (
                    "untouched person-level final test under persistent single-use "
                    "protocol/freeze/reveal release-ledger receipts"
                )
            }
        )
        ledger_path, _ = write_final_test_reveal_ledger_receipt(
            ledger,
            protocol,
            freeze,
            encrypted_answer_key_sha256=sha256_file(encrypted_key_path),
            comparison_report_sha256=sha256_json(report),
            revealed_at_utc=evaluation_time,
        )
        release_output_hashes["final_test_reveal_ledger"] = sha256_file(ledger_path)
    report_path = directory / "human.comparison.report.json"
    write_new_canonical_json(report_path, report)
    reveal_receipt = HumanRevealReceipt(
        protocol_sha256=protocol.sha256,
        prediction_freeze_sha256=sha256_file(freeze_path),
        answer_key_sha256=sha256_file(encrypted_key_path),
        report_sha256=sha256_file(report_path),
        revealed_at_utc=evaluation_time,
    )
    reveal_path = directory / "human.answer-key.reveal.receipt.json"
    write_new_canonical_json(reveal_path, reveal_receipt)
    workflow_receipt = write_workflow_receipt(
        directory / "human-evaluation.receipt.json",
        stage="reveal-evaluate",
        artifact_id=protocol.protocol_id,
        input_sha256={
            **exact_file_hashes(
                predictions=predictions_path,
                prediction_freeze=freeze_path,
                model_bundle=model_path,
                evaluation_protocol=frozen_protocol_path,
                encrypted_answer_key=encrypted_key_path,
            ),
            **release_input_hashes,
        },
        output_sha256=exact_file_hashes(
            comparison_report=report_path,
            reveal_receipt=reveal_path,
        )
        | release_output_hashes,
        repository_root=repository_root,
        answer_key_accessed=True,
        claim_boundary=report.claim_boundary,
        created_at_utc=evaluation_time,
    )
    return report, reveal_receipt, workflow_receipt


def final_release_authorization() -> str:
    """Expose the exact opt-in token without duplicating it in CLI implementation."""

    return FINAL_TEST_RELEASE_ACKNOWLEDGEMENT
