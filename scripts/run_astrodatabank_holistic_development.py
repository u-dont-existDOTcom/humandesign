#!/usr/bin/env python3
"""Run source-aware holistic DEVELOPMENT analysis on Astro-Databank."""

from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from hdmatch.chart.bodygraph import CHANNELS, Center
from hdmatch.chart.ephemeris import EphemerisFallbackError
from hdmatch.human.astrodatabank_export import (
    AstroDatabankRecord,
    iter_astrodatabank_export,
)
from hdmatch.human.holistic import CandidateChart, PositiveEvidenceRecord
from hdmatch.human.holistic_labels import cluster_normalized_evidence_weights
from hdmatch.human.holistic_opportunity import (
    cross_fitted_opportunity_identification,
    taxonomy_opportunity,
)
from hdmatch.provenance import verify_ephemeris_directory
from hdmatch.runtime import ExactChartAdapter
from hdmatch.util import sha256_file

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPHEMERIS = ROOT / "data" / "ephemeris"
DEFAULT_EPHEMERIS_MANIFEST = DEFAULT_EPHEMERIS / "manifest.json"
FAST_BODIES = ("sun", "moon", "mercury", "venus", "mars")
ALL_BODIES = (
    "sun",
    "earth",
    "moon",
    "north_node",
    "south_node",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
)
SIDES = ("personality", "design")

SCOPE_PREFIXES: dict[str, tuple[str, ...]] = {
    "personality_lifestyle": (
        "Traits : Personality",
        "Traits : Mind",
        "Lifestyle : Work",
        "Lifestyle : Social Life",
        "Personal : Religion/Spirituality",
        "Notable : Extraordinary Talents",
    ),
    "behavior_vocation": (
        "Traits : Personality",
        "Traits : Mind",
        "Lifestyle : Work",
        "Lifestyle : Social Life",
        "Personal : Religion/Spirituality",
        "Notable : Extraordinary Talents",
        "Vocation",
    ),
    "life_patterns": (
        "Traits : Personality",
        "Traits : Mind",
        "Lifestyle : Work",
        "Lifestyle : Social Life",
        "Lifestyle : Home",
        "Lifestyle : Financial",
        "Personal : Religion/Spirituality",
        "Notable : Extraordinary Talents",
        "Family : Childhood",
        "Family : Relationship",
        "Family : Parenting",
        "Vocation",
    ),
}


def _channel_ids() -> tuple[str, ...]:
    return tuple(sorted(channel.identifier for channel in CHANNELS))


def _carrier_names(bodies: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        f"carrier:{side}:{body}:gate_line"
        for side in SIDES
        for body in bodies
    )


def _feature_names(representation: str) -> tuple[str, ...]:
    core = ("type", "authority", "profile", "definition")
    centers = tuple(f"center:{center.value}" for center in Center)
    channels = tuple(f"channel:{identifier}" for identifier in _channel_ids())
    gates = tuple(f"gate:{gate}" for gate in range(1, 65))
    choices = {
        "fast_carrier_gate_line": _carrier_names(FAST_BODIES),
        "all_carrier_gate_line": _carrier_names(ALL_BODIES),
        "gates": gates,
        "channels": channels,
        "gates_channels": gates + channels,
        "core_channels": core + centers + channels,
        "full_symbolic": (
            core + centers + channels + gates + _carrier_names(ALL_BODIES)
        ),
    }
    try:
        return choices[representation]
    except KeyError as exc:
        raise ValueError(f"unknown representation: {representation}") from exc


def _chart_feature_map(chart: object) -> dict[str, str | int]:
    features: dict[str, str | int] = {
        "type": str(chart.type),
        "authority": str(chart.authority),
        "profile": str(chart.profile),
        "definition": str(chart.definition),
    }
    defined = set(chart.defined_centers)
    for center in Center:
        features[f"center:{center.value}"] = int(center.value in defined)
    channels = set(chart.channels)
    for identifier in _channel_ids():
        features[f"channel:{identifier}"] = int(identifier in channels)
    active_gates = {activation.gate for activation in chart.activations.values()}
    for gate in range(1, 65):
        features[f"gate:{gate}"] = int(gate in active_gates)
    for key, activation in chart.activations.items():
        features[f"carrier:{key}:gate_line"] = (
            f"{activation.gate}.{activation.line}"
        )
    return features


def _normalize_source(value: str) -> str:
    return " ".join(value.split()).casefold() or "__unknown__"


def _nation_code(value: str) -> str:
    """Collapse ADB region codes such as ``CA (US)`` to their nation code."""

    normalized = " ".join(value.split()).upper()
    if normalized.endswith(")") and "(" in normalized:
        suffix = normalized.rsplit("(", 1)[1][:-1].strip()
        if suffix:
            return suffix
    return normalized or "__unknown__"


def _strata(record: AstroDatabankRecord) -> dict[str, str]:
    if record.birth_year is None:
        raise ValueError(f"record {record.adb_id} lacks recorded birth year")
    return {
        "sex": record.gender.strip().upper() or "__unknown__",
        "birth_year": str(record.birth_year),
        "country": _nation_code(record.country_code),
        "collector": _normalize_source(record.collector),
        "editor": _normalize_source(record.editor),
        "biographer": _normalize_source(record.biographer),
    }


def _labels(record: AstroDatabankRecord, scope: str) -> tuple[str, ...]:
    prefixes = SCOPE_PREFIXES[scope]
    selected = set()
    for category in record.categories:
        text = category.text.strip()
        if text and any(
            text == prefix or text.startswith(prefix + " :")
            for prefix in prefixes
        ):
            selected.add(text)
    return tuple(sorted(selected))


@contextmanager
def _xml_input(path: Path) -> Iterator[Path]:
    if path.suffix.lower() != ".zip":
        yield path
        return
    with zipfile.ZipFile(path) as archive:
        members = [
            item
            for item in archive.infolist()
            if not item.is_dir() and item.filename.lower().endswith(".xml")
        ]
        if len(members) != 1:
            raise ValueError("ADB ZIP must contain exactly one XML export")
        member = members[0]
        if Path(member.filename).name != member.filename:
            raise ValueError("ADB ZIP XML member must not contain directories")
        with tempfile.TemporaryDirectory(prefix="hdmatch-adb-") as temp:
            destination = Path(temp) / member.filename
            destination.write_bytes(archive.read(member))
            yield destination


def _eligible(path: Path) -> tuple[AstroDatabankRecord, ...]:
    return tuple(
        record
        for record in iter_astrodatabank_export(path)
        if record.is_primary_timed_public_record and record.birth_year is not None
    )


def _build_cases(
    records: tuple[AstroDatabankRecord, ...],
    *,
    adapter: ExactChartAdapter,
    scope: str,
) -> tuple[
    tuple[PositiveEvidenceRecord, ...],
    tuple[CandidateChart, ...],
    int,
]:
    people: list[PositiveEvidenceRecord] = []
    charts: list[CandidateChart] = []
    engine_coverage_exclusions = 0
    for record in records:
        labels = _labels(record, scope)
        if not labels or record.birth_utc is None:
            continue
        try:
            public_chart = adapter.calculate(record.birth_utc)
        except EphemerisFallbackError:
            engine_coverage_exclusions += 1
            continue
        feature_map = _chart_feature_map(public_chart)
        strata = _strata(record)
        clusters = {label: taxonomy_opportunity(label) for label in labels}
        weights = cluster_normalized_evidence_weights(
            labels,
            label_clusters=clusters,
        )
        participant_id = f"ADB-{record.adb_id}"
        people.append(
            PositiveEvidenceRecord(
                participant_id=participant_id,
                cohort="development",
                observed_labels=labels,
                chart_features=feature_map,
                match_strata=strata,
                evidence_weights=weights,
            )
        )
        charts.append(
            CandidateChart(
                chart_id=f"CHART-{record.adb_id}",
                owner_participant_id=participant_id,
                chart_features=feature_map,
                match_strata=strata,
            )
        )
    return tuple(people), tuple(charts), engine_coverage_exclusions


def _summary(result: object) -> dict[str, object]:
    payload = result.model_dump(mode="json", exclude={"results"})
    payload["claim_boundary"] = "DEVELOPMENT-only; not independent validation"
    return payload


def _country_transport(
    people: tuple[PositiveEvidenceRecord, ...],
    charts: tuple[CandidateChart, ...],
    *,
    feature_names: tuple[str, ...],
    args: argparse.Namespace,
) -> dict[str, object]:
    counts = Counter(person.match_strata.get("country", "") for person in people)
    by_owner = {chart.owner_participant_id: chart for chart in charts}
    output: dict[str, object] = {}
    for country, count in sorted(counts.items()):
        if count < args.min_country_people or not country:
            continue
        subset_people = tuple(
            person
            for person in people
            if person.match_strata.get("country") == country
        )
        subset_charts = tuple(
            by_owner[person.participant_id]
            for person in subset_people
            if person.participant_id in by_owner
        )
        try:
            result = cross_fitted_opportunity_identification(
                subset_people,
                subset_charts,
                model_id=f"adb-transport-{country}",
                feature_names=feature_names,
                candidate_match_fields=("sex", "birth_year"),
                neighbor_count=args.neighbor_count,
                folds=args.folds,
                max_decoys=args.max_decoys,
                randomization_iterations=args.randomization_iterations,
            )
        except ValueError as exc:
            output[country] = {
                "status": "unevaluable",
                "reason": str(exc),
                "n": count,
            }
        else:
            output[country] = _summary(result)
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Source-aware Astro-Databank holistic DEVELOPMENT analysis"
    )
    parser.add_argument("--input", required=True, help="official XML or ZIP")
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--scope",
        choices=tuple(SCOPE_PREFIXES),
        default="behavior_vocation",
    )
    parser.add_argument(
        "--representation",
        choices=(
            "fast_carrier_gate_line",
            "all_carrier_gate_line",
            "gates",
            "channels",
            "gates_channels",
            "core_channels",
            "full_symbolic",
        ),
        default="fast_carrier_gate_line",
    )
    parser.add_argument("--neighbor-count", type=int, default=200)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--max-decoys", type=int, default=200)
    parser.add_argument("--randomization-iterations", type=int, default=5000)
    parser.add_argument("--min-country-people", type=int, default=150)
    parser.add_argument(
        "--source-block",
        choices=("none", "collector"),
        default="none",
    )
    parser.add_argument("--ephemeris-path", default=str(DEFAULT_EPHEMERIS))
    parser.add_argument(
        "--source-manifest",
        default=str(DEFAULT_EPHEMERIS_MANIFEST),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    source = Path(args.input)
    verified = verify_ephemeris_directory(
        source_manifest_path=args.source_manifest,
        ephemeris_directory=args.ephemeris_path,
    )
    adapter = ExactChartAdapter(args.ephemeris_path)
    feature_names = _feature_names(args.representation)
    with _xml_input(source) as xml_path:
        records = _eligible(xml_path)
        people, charts, engine_exclusions = _build_cases(
            records,
            adapter=adapter,
            scope=args.scope,
        )

    training_blocks: tuple[str, ...] = ()
    candidate_fields = ("sex", "birth_year", "country")
    if args.source_block == "collector":
        training_blocks = ("collector",)
        candidate_fields += ("collector",)

    pooled = cross_fitted_opportunity_identification(
        people,
        charts,
        model_id=f"adb-{args.scope}-{args.representation}-{args.source_block}",
        feature_names=feature_names,
        training_block_fields=training_blocks,
        candidate_match_fields=candidate_fields,
        neighbor_count=args.neighbor_count,
        folds=args.folds,
        max_decoys=args.max_decoys,
        randomization_iterations=args.randomization_iterations,
    )
    collector_counts = Counter(
        record.collector.strip() or "__unknown__" for record in records
    )
    country_counts = Counter(
        person.match_strata.get("country", "__unknown__") for person in people
    )
    gauquelin_notes = sum(
        "gauquelin" in record.source_notes.casefold() for record in records
    )
    payload = {
        "schema_version": "adb-holistic-development-report-v1",
        "phase": "DEVELOPMENT",
        "input_sha256": sha256_file(source),
        "eligible_timed_public_records": len(records),
        "engine_coverage_exclusions_after_scope_filter": engine_exclusions,
        "people_with_scope_labels_and_verified_swieph_chart": len(people),
        "scope": args.scope,
        "representation": args.representation,
        "feature_count": len(feature_names),
        "neighbor_count": args.neighbor_count,
        "candidate_match_fields": candidate_fields,
        "training_block_fields": training_blocks,
        "ephemeris": verified.manifest_binding(),
        "engine_fingerprint": adapter.fingerprint,
        "pooled_crossfit": _summary(pooled),
        "country_transport_unblocked": _country_transport(
            people,
            charts,
            feature_names=feature_names,
            args=args,
        ),
        "provenance_summary": {
            "analysis_nation_counts": dict(country_counts.most_common()),
            "collector_counts_top20_before_engine_coverage_filter": dict(
                collector_counts.most_common(20)
            ),
            "source_notes_mention_gauquelin": gauquelin_notes,
        },
        "interpretation_rule": (
            "Do not call a pooled archive result generalizable unless its direction "
            "transports across material source/geography strata and survives training-"
            "source blocking or an independent external cohort."
        ),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote DEVELOPMENT report: {output}")
    print(f"report sha256: {sha256_file(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
