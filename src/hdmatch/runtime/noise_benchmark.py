"""Post-reveal artifact loading for the synthetic noise-tier comparator.

The complete public provenance chain is verified without decrypting answer-key
material.  This module has no external key, recovery, or answer-key interface.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from hdmatch.evaluation.noise_benchmark import (
    DeclaredNoiseSettings,
    NoiseBenchmarkInputError,
    NoiseBenchmarkReport,
    NoiseRunMetadata,
    NoiseTier,
    RevealedNoiseTierEvaluation,
    compare_revealed_noise_tiers,
)
from hdmatch.evaluation.report import EvaluationReport
from hdmatch.experiments.canonical import (
    load_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import (
    ArtifactBindings,
    FreezeRecord,
    FreezeVerificationError,
    verify_frozen_predictions,
)
from hdmatch.experiments.manifest import RunManifest, load_run_manifest
from hdmatch.experiments.reveal import RevealRecord, verify_reveal_record
from hdmatch.synthetic.noise import (
    NoiseTier as GeneratorNoiseTier,
)
from hdmatch.synthetic.noise import (
    noise_parameters_payload,
)


def _load_evaluation(path: Path) -> EvaluationReport:
    try:
        raw = load_json_bytes(path, require_canonical=True)
        return EvaluationReport.model_validate(raw)
    except (OSError, ValueError, ValidationError) as exc:
        raise NoiseBenchmarkInputError(f"invalid canonical evaluation report: {path}") from exc


def _load_blind_document(path: Path) -> dict[str, Any]:
    try:
        raw = load_json_bytes(path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise NoiseBenchmarkInputError(f"invalid canonical public blind input: {path}") from exc
    if (
        not isinstance(raw, dict)
        or raw.get("schema_version") != "blind-synthetic-v1"
        or raw.get("generator") != "frozen-chart-to-response-model"
    ):
        raise NoiseBenchmarkInputError(f"unsupported public blind input: {path}")
    return raw


def _require_case_list(blind: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw_cases = blind.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise NoiseBenchmarkInputError("public blind input must contain cases")
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_cases:
        if not isinstance(raw, dict) or not isinstance(raw.get("case_id"), str):
            raise NoiseBenchmarkInputError("public blind input contains an invalid case")
        case_id = raw["case_id"]
        if case_id in seen:
            raise NoiseBenchmarkInputError(f"public blind input duplicates case {case_id}")
        seen.add(case_id)
        cases.append(raw)
    return cases


def _noise_settings_from_frozen_payload(
    tier: NoiseTier, raw: object
) -> DeclaredNoiseSettings:
    """Validate the generator payload and explicitly translate its field names."""

    expected = noise_parameters_payload(GeneratorNoiseTier(tier.value))
    if raw != expected:
        raise NoiseBenchmarkInputError(
            f"tier {tier} noise_parameters do not match the frozen generator values"
        )
    # Generator names describe compact simulator internals.  Evaluation names spell
    # out the questionnaire fields they alter; this translation is intentionally
    # explicit so confidence and measurement reliability cannot be interchanged.
    return DeclaredNoiseSettings(
        missing_rate=expected["missing_rate"],
        flip_rate=expected["flip_rate"],
        cluster_dropout_rate=expected["cluster_dropout_rate"],
        behavioral_confidence_values=tuple(expected["confidence_values"]),
        measurement_reliability_values=tuple(expected["reliability_values"]),
        conditioning=expected["conditioning"],
    )


def _candidate_universe_sha256(
    *, blind: Mapping[str, Any], cases: Sequence[Mapping[str, Any]], manifest: RunManifest
) -> str:
    universe = blind.get("candidate_universe")
    descriptors: list[dict[str, Any]] = []
    for case in cases:
        if case.get("candidate_universe") != universe:
            raise NoiseBenchmarkInputError(
                f"case {case['case_id']} candidate universe differs from its document"
            )
        descriptors.append(
            {
                "case_id": case["case_id"],
                "candidate_universe": case.get("candidate_universe"),
                "known_birth_year": case.get("known_birth_year"),
                "known_birth_month": case.get("known_birth_month"),
                "known_birth_day": case.get("known_birth_day"),
                "iana_timezone": case.get("iana_timezone"),
            }
        )
    ephemeris_hashes = {
        key: value
        for key, value in manifest.input_hashes.items()
        if key.startswith("ephemeris:")
    }
    if not ephemeris_hashes:
        raise NoiseBenchmarkInputError("run manifest has no exact ephemeris bindings")
    return sha256_json(
        {
            "schema_version": "candidate-universe-binding-v1",
            "candidate_universe": universe,
            "software_commit": manifest.software_commit,
            "software_environment": manifest.software_environment.model_dump(mode="json"),
            "ephemeris_input_hashes": dict(sorted(ephemeris_hashes.items())),
            "case_constraints": sorted(descriptors, key=lambda item: str(item["case_id"])),
        }
    )


def _validate_cross_artifact_bindings(
    *,
    expected_tier: NoiseTier,
    blind: Mapping[str, Any],
    blind_sha256: str,
    cases: Sequence[Mapping[str, Any]],
    manifest: RunManifest,
    evaluation: EvaluationReport,
) -> None:
    if blind.get("noise_tier") != expected_tier.value:
        raise NoiseBenchmarkInputError(
            f"expected {expected_tier} run but blind input declares {blind.get('noise_tier')!r}"
        )
    if manifest.software_dirty:
        raise NoiseBenchmarkInputError(
            "comparable noise benchmarks require a clean committed recovery manifest"
        )
    expected_recovery_seed = int(blind_sha256[:16], 16)
    if manifest.seed != expected_recovery_seed:
        raise NoiseBenchmarkInputError(
            "run manifest recovery seed is not deterministically derived from blind input"
        )
    config = manifest.config_payload
    if config is None:
        raise NoiseBenchmarkInputError(
            "run manifest lacks its exact recovery configuration payload"
        )
    required_config_fields = {
        "aggregation",
        "threshold_rubric_bits",
        "workers",
        "cache_policy",
    }
    if set(config) != required_config_fields:
        raise NoiseBenchmarkInputError(
            "run manifest recovery configuration has missing or unexpected fields"
        )
    threshold = config["threshold_rubric_bits"]
    workers = config["workers"]
    if config["aggregation"] != manifest.aggregation_rule:
        raise NoiseBenchmarkInputError(
            "run manifest recovery aggregation differs from its exact configuration"
        )
    if (
        not isinstance(threshold, (int, float))
        or isinstance(threshold, bool)
        or not math.isfinite(threshold)
    ):
        raise NoiseBenchmarkInputError("invalid recovery threshold in run manifest")
    if not isinstance(workers, int) or isinstance(workers, bool) or workers < 1:
        raise NoiseBenchmarkInputError("invalid recovery worker count in run manifest")
    if config["cache_policy"] != "hash-bound exact month universes":
        raise NoiseBenchmarkInputError("unsupported recovery cache policy in run manifest")
    if manifest.experiment_id != evaluation.experiment_id or blind.get(
        "experiment_id"
    ) != evaluation.experiment_id:
        raise NoiseBenchmarkInputError("experiment_id differs across public artifacts")
    if manifest.created_at_utc > evaluation.created_at_utc:
        raise NoiseBenchmarkInputError("evaluation timestamp predates its run manifest")
    if manifest.model_id != blind.get("model_id"):
        raise NoiseBenchmarkInputError("model_id differs between manifest and blind input")
    if blind.get("model_sha256") != evaluation.model_sha256:
        raise NoiseBenchmarkInputError("model hash differs between blind input and evaluation")
    for field in ("question_bank_sha256", "mapping_sha256"):
        if blind.get(field) != getattr(evaluation, field):
            raise NoiseBenchmarkInputError(
                f"{field} differs between blind input and evaluation"
            )
    if manifest.candidate_universe != blind.get("candidate_universe"):
        raise NoiseBenchmarkInputError("candidate universe differs across public artifacts")
    if manifest.input_hashes.get("blind_cases.json") != blind_sha256:
        raise NoiseBenchmarkInputError("run manifest does not bind the public blind input")
    if evaluation.blind_input_sha256 != blind_sha256:
        raise NoiseBenchmarkInputError("evaluation does not bind the public blind input")
    if len(cases) != evaluation.aggregate.case_count:
        raise NoiseBenchmarkInputError("public blind case count differs from evaluation")
    blind_case_ids = {str(case["case_id"]) for case in cases}
    report_case_ids = {case.case_id for case in evaluation.cases} | {
        failure.case_id for failure in evaluation.failures
    }
    if blind_case_ids != report_case_ids:
        raise NoiseBenchmarkInputError("evaluation case identities differ from blind input")


def _verify_public_provenance_chain(
    *,
    directory: Path,
    blind: Mapping[str, Any],
    blind_sha256: str,
    manifest: RunManifest,
    evaluation: EvaluationReport,
) -> tuple[FreezeRecord, RevealRecord]:
    freeze_path = directory / "prediction.freeze.json"
    reveal_path = directory / "answer-key.reveal.json"
    expected_bindings = ArtifactBindings(
        blind_input_sha256=blind_sha256,
        model_sha256=str(blind.get("model_sha256", "")),
        question_bank_sha256=str(blind.get("question_bank_sha256", "")),
        mapping_sha256=str(blind.get("mapping_sha256", "")),
    )
    try:
        freeze = verify_frozen_predictions(
            directory,
            freeze_path=freeze_path,
            expected_bindings=expected_bindings,
            expected_experiment_id=str(blind.get("experiment_id", "")),
            run_manifest_path=directory / "run.manifest.json",
            require_run_manifest=True,
        )
        reveal = verify_reveal_record(
            directory,
            freeze=freeze,
            freeze_path=freeze_path,
            reveal_record_path=reveal_path,
        )
    except (ValueError, FreezeVerificationError) as exc:
        raise NoiseBenchmarkInputError("invalid frozen prediction/reveal provenance chain") from exc

    prediction_path = directory / freeze.prediction_file
    try:
        predictions = load_json_bytes(prediction_path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise NoiseBenchmarkInputError("frozen predictions are not canonical JSON") from exc
    if not isinstance(predictions, dict) or predictions.get("schema_version") != "predictions-v1":
        raise NoiseBenchmarkInputError("frozen predictions use an unsupported schema")
    for field, expected in {
        "experiment_id": freeze.experiment_id,
        "model_id": manifest.model_id,
        "blind_input_sha256": freeze.blind_input_sha256,
        "model_sha256": freeze.model_sha256,
        "question_bank_sha256": freeze.question_bank_sha256,
        "mapping_sha256": freeze.mapping_sha256,
        "aggregation_rule": manifest.aggregation_rule,
    }.items():
        if predictions.get(field) != expected:
            raise NoiseBenchmarkInputError(f"frozen predictions {field} binding differs")

    manifest_sha256 = sha256_file(directory / "run.manifest.json")
    if freeze.run_manifest_sha256 is None:
        raise NoiseBenchmarkInputError("prediction freeze lacks a run-manifest binding")
    if freeze.run_manifest_sha256 != manifest_sha256:
        raise NoiseBenchmarkInputError("prediction freeze does not bind the run manifest")
    if freeze.software_commit != manifest.software_commit or freeze.software_dirty:
        raise NoiseBenchmarkInputError(
            "prediction freeze software state differs from clean manifest"
        )
    expected_freeze_versions = manifest.software_environment.packages | {
        "python": manifest.software_environment.python_version
    }
    if freeze.software_versions != expected_freeze_versions:
        raise NoiseBenchmarkInputError(
            "prediction freeze environment differs from the recovery manifest"
        )
    if manifest.created_at_utc > freeze.created_at_utc:
        raise NoiseBenchmarkInputError("prediction freeze predates its run manifest")
    if reveal.revealed_at_utc > evaluation.created_at_utc:
        raise NoiseBenchmarkInputError("evaluation timestamp predates answer-key reveal")

    expected_report_hashes: dict[str, str | None] = {
        "prediction_sha256": freeze.prediction_sha256,
        "freeze_sha256": sha256_file(freeze_path),
        "reveal_sha256": sha256_file(reveal_path),
        "run_manifest_sha256": manifest_sha256,
        "encrypted_answer_key_file": reveal.encrypted_answer_key_file,
        "encrypted_answer_key_sha256": reveal.encrypted_answer_key_sha256,
        "answer_key_payload_sha256": reveal.answer_key_payload_sha256,
    }
    for field, report_expected in expected_report_hashes.items():
        if getattr(evaluation, field) != report_expected:
            raise NoiseBenchmarkInputError(
                f"evaluation {field} does not match the verified provenance chain"
            )
    return freeze, reveal


def load_revealed_noise_tier_run(
    run_dir: str | Path, *, expected_tier: NoiseTier
) -> RevealedNoiseTierEvaluation:
    """Load one completed tier without opening answer-key or reveal-key material."""

    directory = Path(run_dir)
    evaluation_path = directory / "evaluation.json"
    manifest_path = directory / "run.manifest.json"
    blind_path = directory / "blind_cases.json"
    evaluation = _load_evaluation(evaluation_path)
    try:
        manifest = load_run_manifest(manifest_path)
    except (OSError, ValueError) as exc:
        raise NoiseBenchmarkInputError(f"invalid canonical run manifest: {manifest_path}") from exc
    blind = _load_blind_document(blind_path)
    cases = _require_case_list(blind)
    blind_sha256 = sha256_file(blind_path)
    _validate_cross_artifact_bindings(
        expected_tier=expected_tier,
        blind=blind,
        blind_sha256=blind_sha256,
        cases=cases,
        manifest=manifest,
        evaluation=evaluation,
    )
    _verify_public_provenance_chain(
        directory=directory,
        blind=blind,
        blind_sha256=blind_sha256,
        manifest=manifest,
        evaluation=evaluation,
    )
    noise = _noise_settings_from_frozen_payload(expected_tier, blind.get("noise_parameters"))
    revealed_target_set_sha256 = evaluation.revealed_target_set_sha256
    if revealed_target_set_sha256 is None:
        raise NoiseBenchmarkInputError(
            "noise comparison requires a post-reveal target-set hash; legacy evaluation "
            "reports must be regenerated from their frozen predictions and revealed key"
        )
    generation_seed_commitment_sha256 = evaluation.generation_seed_commitment_sha256
    if generation_seed_commitment_sha256 is None:
        raise NoiseBenchmarkInputError(
            "noise comparison requires a post-reveal synthetic generation-seed commitment"
        )
    metadata = NoiseRunMetadata(
        experiment_id=evaluation.experiment_id,
        tier=expected_tier,
        model_id=manifest.model_id,
        model_sha256=evaluation.model_sha256,
        candidate_universe=manifest.candidate_universe,
        candidate_universe_sha256=_candidate_universe_sha256(
            blind=blind,
            cases=cases,
            manifest=manifest,
        ),
        case_set_sha256=revealed_target_set_sha256,
        generation_seed_commitment_sha256=generation_seed_commitment_sha256,
        declared_case_count=evaluation.aggregate.case_count,
        aggregation_rule=manifest.aggregation_rule,
        recovery_config_sha256=manifest.config_sha256,
        run_manifest_sha256=sha256_file(manifest_path),
        evaluation_sha256=sha256_file(evaluation_path),
        noise=noise,
    )
    return RevealedNoiseTierEvaluation(metadata=metadata, evaluation=evaluation)


def build_noise_benchmark_from_run_dirs(
    run_dirs: Mapping[NoiseTier, str | Path],
) -> NoiseBenchmarkReport:
    """Load exactly four public post-reveal run directories and compare them."""

    provided = set(run_dirs)
    required = set(NoiseTier)
    if provided != required:
        missing = sorted(tier.value for tier in required.difference(provided))
        unexpected = sorted(str(tier) for tier in provided.difference(required))
        raise NoiseBenchmarkInputError(
            f"noise run directories must contain exactly four tiers; "
            f"missing={missing}, unexpected={unexpected}"
        )
    evaluations = tuple(
        load_revealed_noise_tier_run(run_dirs[tier], expected_tier=tier)
        for tier in NoiseTier
    )
    return compare_revealed_noise_tiers(evaluations)


def write_noise_benchmark_report(
    report: NoiseBenchmarkReport, output_path: str | Path
) -> Path:
    """Write a new canonical comparison artifact without replacing prior evidence."""

    return write_new_canonical_json(output_path, report)
