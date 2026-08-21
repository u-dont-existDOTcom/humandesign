"""Post-reveal artifact loading for the synthetic noise-tier comparator.

Only canonical public blind inputs, public run manifests, and completed evaluation
reports are read.  This module has no answer-key, recovery, or reveal interface.
"""

from __future__ import annotations

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
from hdmatch.experiments.manifest import RunManifest, load_run_manifest
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
    if not isinstance(raw, dict) or raw.get("schema_version") != "blind-synthetic-v1":
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
    noise = _noise_settings_from_frozen_payload(expected_tier, blind.get("noise_parameters"))
    revealed_target_set_sha256 = evaluation.revealed_target_set_sha256
    if revealed_target_set_sha256 is None:
        raise NoiseBenchmarkInputError(
            "noise comparison requires a post-reveal target-set hash; legacy evaluation "
            "reports must be regenerated from their frozen predictions and revealed key"
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
        declared_case_count=evaluation.aggregate.case_count,
        aggregation_rule=manifest.aggregation_rule,
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
