"""Standalone CLI for whole-profile positive-evidence experiments.

Invoke with:

    python -m hdmatch.holistic_cli convert-human-cases ...
    python -m hdmatch.holistic_cli crossfit-opportunity ...
    python -m hdmatch.holistic_cli fit ...
    python -m hdmatch.holistic_cli evaluate ...
    python -m hdmatch.holistic_cli minimize ...

The separate module keeps holistic DEVELOPMENT experiments usable without
changing the frozen blind-recovery command surface.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from hdmatch.human.dataset import load_human_dataset
from hdmatch.human.holistic import (
    CandidateChart,
    HolisticModelArtifact,
    HolisticPositiveEvidenceModel,
    PositiveEvidenceRecord,
    evaluate_identification,
    greedy_minimize_feature_groups,
)
from hdmatch.human.holistic_humancase import human_cases_to_positive_evidence
from hdmatch.human.holistic_opportunity import (
    cross_fitted_opportunity_identification,
)
from hdmatch.util import sha256_file


def _read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_new_json(path: str | Path, payload: Any) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {target}")
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target


def _records(path: str | Path) -> tuple[PositiveEvidenceRecord, ...]:
    raw = _read_json(path)
    if isinstance(raw, Mapping):
        raw = raw.get("records")
    if not isinstance(raw, list):
        raise ValueError("positive-evidence input must be a JSON list or {'records': [...]}")
    return tuple(PositiveEvidenceRecord.model_validate(item) for item in raw)


def _charts(path: str | Path) -> tuple[CandidateChart, ...]:
    raw = _read_json(path)
    if isinstance(raw, Mapping):
        raw = raw.get("charts")
    if not isinstance(raw, list):
        raise ValueError("chart input must be a JSON list or {'charts': [...]}")
    return tuple(CandidateChart.model_validate(item) for item in raw)


def _model(path: str | Path) -> HolisticPositiveEvidenceModel:
    return HolisticPositiveEvidenceModel(HolisticModelArtifact.model_validate(_read_json(path)))


def _clusters(values: Sequence[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--cluster must use FEATURE=CLUSTER")
        feature, cluster = value.split("=", 1)
        feature = feature.strip()
        cluster = cluster.strip()
        if not feature or not cluster:
            raise ValueError("--cluster must use nonblank FEATURE=CLUSTER")
        if feature in result:
            raise ValueError(f"duplicate cluster assignment for {feature}")
        result[feature] = cluster
    return result


def _excluded_answers(values: Sequence[str]) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--exclude-answer must use QUESTION=ANSWER")
        question, answer = value.split("=", 1)
        question = question.strip()
        answer = answer.strip()
        if not question or not answer:
            raise ValueError("--exclude-answer must use nonblank QUESTION=ANSWER")
        grouped.setdefault(question, []).append(answer)
    return {
        question: tuple(dict.fromkeys(answers))
        for question, answers in grouped.items()
    }


def _convert_human_cases(args: argparse.Namespace) -> int:
    dataset = load_human_dataset(args.dataset, args.questionnaire_version)
    converted = human_cases_to_positive_evidence(
        dataset.cases,
        excluded_answers=_excluded_answers(args.exclude_answer),
        include_birth_year=not args.omit_birth_year,
        metadata_match_fields=tuple(args.metadata_match_field),
    )
    payload = {
        "schema_version": "holistic-human-case-packet-v1",
        "phase": "DEVELOPMENT",
        "source_dataset_sha256": sha256_file(args.dataset),
        "questionnaire_version": dataset.questionnaire_version,
        "records": [record.model_dump(mode="json") for record in converted.records],
        "charts": [chart.model_dump(mode="json") for chart in converted.true_charts],
        "label_opportunities": converted.label_opportunities,
        "label_dependency_clusters": converted.label_dependency_clusters,
        "skipped_no_scorable_evidence": converted.skipped_no_scorable_evidence,
        "claim_boundary": (
            "DEVELOPMENT packet contains true chart features; never use as blind "
            "VALIDATION input"
        ),
    }
    output = _write_new_json(args.output, payload)
    print(f"holistic HumanCase packet: {output}")
    print(f"packet sha256: {sha256_file(output)}")
    print(f"people converted: {len(converted.records)}")
    print(f"people skipped: {len(converted.skipped_no_scorable_evidence)}")
    return 0


def _crossfit_opportunity(args: argparse.Namespace) -> int:
    raw = _read_json(args.packet)
    if not isinstance(raw, Mapping):
        raise ValueError("opportunity packet must be a JSON object")
    opportunities = raw.get("label_opportunities")
    if not isinstance(opportunities, Mapping):
        raise ValueError("packet is missing label_opportunities")
    result = cross_fitted_opportunity_identification(
        _records(args.packet),
        _charts(args.packet),
        model_id=args.model_id,
        feature_names=tuple(args.feature),
        label_opportunities={str(key): str(value) for key, value in opportunities.items()},
        training_block_fields=tuple(args.training_block_field),
        candidate_match_fields=tuple(args.match_field),
        neighbor_count=args.neighbor_count,
        alpha=args.alpha,
        min_label_count=args.min_label_count,
        min_opportunity_count=args.min_opportunity_count,
        folds=args.folds,
        fold_seed=args.fold_seed,
        max_decoys=args.max_decoys,
        decoy_seed=args.decoy_seed,
        randomization_iterations=args.randomization_iterations,
    )
    payload = {
        "schema_version": "holistic-opportunity-run-v1",
        "phase": "DEVELOPMENT",
        "input_packet_sha256": sha256_file(args.packet),
        "evaluation": result.model_dump(mode="json"),
        "claim_boundary": "cross-fitting is DEVELOPMENT model selection, not confirmation",
    }
    output = _write_new_json(args.output, payload)
    print(f"opportunity-conditioned crossfit: {output}")
    print(f"crossfit sha256: {sha256_file(output)}")
    print(f"people evaluated: {result.people_evaluated}")
    print(f"mean true-chart percentile: {result.mean_percentile:.6f}")
    if result.randomization_p_value is not None:
        print(f"randomization p-value: {result.randomization_p_value:.6g}")
    return 0


def _fit(args: argparse.Namespace) -> int:
    records = _records(args.records)
    model = HolisticPositiveEvidenceModel.fit(
        records,
        model_id=args.model_id,
        feature_names=tuple(args.feature),
        feature_clusters=_clusters(args.cluster),
        alpha=args.alpha,
        min_label_count=args.min_label_count,
    )
    output = _write_new_json(args.output, model.artifact.model_dump(mode="json"))
    print(f"holistic model: {output}")
    print(f"holistic model sha256: {sha256_file(output)}")
    print(f"training people: {model.artifact.training_people}")
    print(f"retained labels: {len(model.retained_labels)}")
    return 0


def _evaluate(args: argparse.Namespace) -> int:
    model = _model(args.model)
    result = evaluate_identification(
        model,
        _records(args.people),
        _charts(args.charts),
        match_fields=tuple(args.match_field),
        max_decoys=args.max_decoys,
        seed=args.seed,
        enabled_features=tuple(args.feature) if args.feature else None,
        randomization_iterations=args.randomization_iterations,
    )
    output = _write_new_json(args.output, result.model_dump(mode="json"))
    print(f"holistic evaluation: {output}")
    print(f"holistic evaluation sha256: {sha256_file(output)}")
    print(f"people evaluated: {result.people_evaluated}")
    print(f"mean true-chart percentile: {result.mean_percentile:.6f}")
    if result.randomization_p_value is not None:
        print(f"randomization p-value: {result.randomization_p_value:.6g}")
    return 0


def _minimize(args: argparse.Namespace) -> int:
    raw_groups = _read_json(args.feature_groups)
    if not isinstance(raw_groups, Mapping):
        raise ValueError("feature-groups file must contain a JSON object")
    groups = {
        str(name): tuple(str(feature) for feature in features)
        for name, features in raw_groups.items()
        if isinstance(features, list)
    }
    if len(groups) != len(raw_groups):
        raise ValueError("every feature group value must be a JSON list")

    model = _model(args.model)
    result = greedy_minimize_feature_groups(
        model,
        _records(args.people),
        _charts(args.charts),
        feature_groups=groups,
        match_fields=tuple(args.match_field),
        max_decoys=args.max_decoys,
        seed=args.seed,
        max_absolute_percentile_loss=args.max_percentile_loss,
    )
    output = _write_new_json(args.output, result.model_dump(mode="json"))
    print(f"holistic minimization: {output}")
    print(f"holistic minimization sha256: {sha256_file(output)}")
    print(f"retained groups: {','.join(result.retained_groups)}")
    print(f"full mean percentile: {result.full_mean_percentile:.6f}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m hdmatch.holistic_cli",
        description=(
            "Positive-evidence whole-profile chart identification. "
            "Minimization is DEVELOPMENT-only."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser(
        "convert-human-cases",
        help="convert a rich DEVELOPMENT HumanDataset to positive-evidence records",
    )
    convert.add_argument("--dataset", required=True)
    convert.add_argument("--questionnaire-version", required=True)
    convert.add_argument("--output", required=True)
    convert.add_argument("--exclude-answer", action="append", default=[])
    convert.add_argument("--metadata-match-field", action="append", default=[])
    convert.add_argument("--omit-birth-year", action="store_true")
    convert.set_defaults(handler=_convert_human_cases)

    crossfit = subparsers.add_parser(
        "crossfit-opportunity",
        help="cross-fit a rich DEVELOPMENT packet with true missing-as-unknown semantics",
    )
    crossfit.add_argument("--packet", required=True)
    crossfit.add_argument("--output", required=True)
    crossfit.add_argument("--model-id", required=True)
    crossfit.add_argument("--feature", action="append", required=True)
    crossfit.add_argument("--training-block-field", action="append", default=[])
    crossfit.add_argument("--match-field", action="append", default=[])
    crossfit.add_argument("--neighbor-count", type=int, default=200)
    crossfit.add_argument("--alpha", type=float, default=4.0)
    crossfit.add_argument("--min-label-count", type=int, default=5)
    crossfit.add_argument("--min-opportunity-count", type=int, default=20)
    crossfit.add_argument("--folds", type=int, default=5)
    crossfit.add_argument("--fold-seed", type=int, default=0)
    crossfit.add_argument("--max-decoys", type=int, default=200)
    crossfit.add_argument("--decoy-seed", type=int, default=0)
    crossfit.add_argument("--randomization-iterations", type=int, default=5000)
    crossfit.set_defaults(handler=_crossfit_opportunity)

    fit = subparsers.add_parser("fit", help="fit a DEVELOPMENT positive-evidence model")
    fit.add_argument("--records", required=True)
    fit.add_argument("--output", required=True)
    fit.add_argument("--model-id", required=True)
    fit.add_argument("--feature", action="append", required=True)
    fit.add_argument("--cluster", action="append", default=[])
    fit.add_argument("--alpha", type=float, default=4.0)
    fit.add_argument("--min-label-count", type=int, default=10)
    fit.set_defaults(handler=_fit)

    evaluate = subparsers.add_parser(
        "evaluate",
        help="rank true charts against frozen matched decoys",
    )
    evaluate.add_argument("--model", required=True)
    evaluate.add_argument("--people", required=True)
    evaluate.add_argument("--charts", required=True)
    evaluate.add_argument("--output", required=True)
    evaluate.add_argument("--match-field", action="append", default=[])
    evaluate.add_argument("--max-decoys", type=int)
    evaluate.add_argument("--seed", type=int, default=0)
    evaluate.add_argument("--feature", action="append")
    evaluate.add_argument("--randomization-iterations", type=int, default=0)
    evaluate.set_defaults(handler=_evaluate)

    minimize = subparsers.add_parser(
        "minimize",
        help="greedily ablate feature groups on DEVELOPMENT people",
    )
    minimize.add_argument("--model", required=True)
    minimize.add_argument("--people", required=True)
    minimize.add_argument("--charts", required=True)
    minimize.add_argument("--feature-groups", required=True)
    minimize.add_argument("--output", required=True)
    minimize.add_argument("--match-field", action="append", default=[])
    minimize.add_argument("--max-decoys", type=int)
    minimize.add_argument("--seed", type=int, default=0)
    minimize.add_argument("--max-percentile-loss", type=float, default=0.01)
    minimize.set_defaults(handler=_minimize)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (FileNotFoundError, FileExistsError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"hdmatch holistic: error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
