#!/usr/bin/env python3
"""Generate the mechanical AstroHD downstream rank-consumer audit."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import re
from collections.abc import Callable, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, NamedTuple

from hdmatch.participant.backend import AstroHDParticipantBackend, _percentile
from hdmatch.schemas import (
    CandidateState,
    LocalDateOverlap,
    ScoredState,
    StructuralChartFeatures,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path("src/hdmatch")
OUTPUT_PATH = Path("reference/audits/astrohd_rank_tiebreak_downstream_v1.json")
HISTORICAL_ARTIFACT_SHA256 = "c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103"

JsonObject = dict[str, Any]
SortKey = Callable[[CandidateState], tuple[Any, ...]]

SYMBOLS = (
    "_rank_states",
    "_evidence_tie_key",
    "_top_net_margin",
    "_RankedState",
)
CONNECTED_RANK_FIELDS = (
    "top_state_tie_count",
    "true_state_rank",
    "true_state_percentile",
)


class HistoricalAuditSourceMismatch(RuntimeError):
    """Raised when regeneration is attempted outside the audited pre-patch baseline."""


class ResearchRankedState(NamedTuple):
    state: CandidateState
    score: ScoredState
    rank: float


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_json(payload: JsonObject) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _assert_historical_source_baseline(repository_root: Path) -> None:
    artifact_path = repository_root / OUTPUT_PATH
    observed_artifact_sha256 = sha256_file(artifact_path)
    if observed_artifact_sha256 != HISTORICAL_ARTIFACT_SHA256:
        raise HistoricalAuditSourceMismatch(
            "historical audit describes pre-patch source and must not be regenerated "
            "against changed production semantics: historical artifact hash mismatch"
        )

    historical = json.loads(artifact_path.read_text(encoding="utf-8"))
    mismatches = []
    for row in historical["source_file_hashes"]:
        relative_path = Path(row["path"])
        observed_sha256 = sha256_file(repository_root / relative_path)
        if observed_sha256 != row["sha256"]:
            mismatches.append(
                f"{relative_path.as_posix()} expected {row['sha256']} observed {observed_sha256}"
            )
    if mismatches:
        details = "; ".join(mismatches)
        raise HistoricalAuditSourceMismatch(
            "historical audit describes pre-patch source and must not be regenerated "
            f"against changed production semantics: {details}"
        )


def _source_files(repository_root: Path) -> list[Path]:
    return sorted((repository_root / SOURCE_ROOT).rglob("*.py"))


def _source_hashes(repository_root: Path) -> list[JsonObject]:
    rows = [
        {
            "path": path.relative_to(repository_root).as_posix(),
            "sha256": sha256_file(path),
        }
        for path in _source_files(repository_root)
    ]
    return rows


def _enclosing_names(source: str, line_number: int) -> str:
    tree = ast.parse(source)
    classes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        and node.lineno <= line_number <= (node.end_lineno or node.lineno)
    ]
    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and node.lineno <= line_number <= (node.end_lineno or node.lineno)
    ]
    class_name = min(
        classes,
        key=lambda node: (node.end_lineno or node.lineno) - node.lineno,
        default=None,
    )
    function_name = min(
        functions,
        key=lambda node: (node.end_lineno or node.lineno) - node.lineno,
        default=None,
    )
    if function_name is not None and class_name is not None:
        return f"{class_name.name}.{function_name.name}"
    if function_name is not None:
        return function_name.name
    if class_name is not None:
        return class_name.name
    return "<module>"


def _source_use_category(line: str, token: str) -> str:
    stripped = line.strip()
    if stripped.startswith("def ") or stripped.startswith("async def "):
        return "function_definition"
    if stripped.startswith("class "):
        return "class_definition"
    if token == "_RankedState" and "_RankedState(" in stripped:
        return "constructor_call"
    if token == "_RankedState":
        return "type_reference"
    if token == "_rank_states" and "=" in stripped:
        return "rank_sequence_assignment"
    return "function_call_or_reference"


def _scan_locations(repository_root: Path) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for path in _source_files(repository_root):
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(repository_root).as_posix()
        for line_number, line in enumerate(source.splitlines(), start=1):
            detected: list[tuple[str, str]] = []
            for symbol in SYMBOLS:
                if symbol in line:
                    detected.append((symbol, _source_use_category(line, symbol)))
            if relative == "src/hdmatch/participant/backend.py" and re.search(r"\.rank\b", line):
                detected.append((".rank", "rank_attribute_read"))
            for field in CONNECTED_RANK_FIELDS:
                if field in line:
                    detected.append((field, "connected_rank_summary_field"))
            if (
                relative == "src/hdmatch/participant/backend.py"
                and "_percentile" in line
                and ("true_state_percentile" in line or line.strip().startswith("def _percentile"))
            ):
                detected.append(("percentile", _source_use_category(line, "_percentile")))
            for token, category in detected:
                rows.append(
                    {
                        "enclosing_function_or_method": _enclosing_names(source, line_number),
                        "line": line_number,
                        "path": relative,
                        "source_excerpt": line.strip(),
                        "syntactic_use_category": category,
                        "token": token,
                        "traceability": "traceable",
                    }
                )
    return sorted(
        rows,
        key=lambda row: (
            row["path"],
            row["line"],
            row["token"],
            row["syntactic_use_category"],
        ),
    )


def _ordered_sequence_consumers(repository_root: Path) -> list[JsonObject]:
    path = repository_root / "src/hdmatch/participant/backend.py"
    source = path.read_text(encoding="utf-8")
    patterns = (
        (
            re.compile(r"item\.rank, ranked_states\[0\]\.rank"),
            "iterate_ranked_states_and_index_first_rank",
        ),
        (re.compile(r"for item in ranked_states"), "iterate_ranked_states"),
        (
            re.compile(r"self\._top_net_margin\(ranked_states\)"),
            "pass_ranked_states_to_top_net_margin",
        ),
        (
            re.compile(r"item\.rank, ranked\[0\]\.rank"),
            "iterate_ranked_and_index_first_rank",
        ),
        (
            re.compile(r"self\._top_net_margin\(ranked\)"),
            "pass_ranked_to_top_net_margin",
        ),
        (re.compile(r"top = ranked\[0\]"), "index_first_ranked_state"),
        (re.compile(r"for item in ranked\[1:\]"), "iterate_ranked_tail_slice"),
    )
    rows: list[JsonObject] = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for pattern, operation in patterns:
            if pattern.search(line):
                rows.append(
                    {
                        "function": _enclosing_names(source, line_number),
                        "line": line_number,
                        "operation": operation,
                        "path": "src/hdmatch/participant/backend.py",
                    }
                )
                break
    return rows


def _candidate_state(state_id: str, start: datetime) -> CandidateState:
    end = start + timedelta(minutes=1)
    features = StructuralChartFeatures(
        type="Generator",
        strategy="Wait to Respond",
        authority="Sacral",
        profile="1/4",
        definition="Single",
        defined_centers=("Sacral",),
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=hashlib.sha256(state_id.encode()).hexdigest(),
        chart_features=features,
        local_date_overlaps=(
            LocalDateOverlap(date=start.date(), seconds=(end - start).total_seconds()),
        ),
    )


def _score(
    state_id: str,
    *,
    net: float = 1.0,
    contradictions: int = 0,
    detailed: float = 50.0,
    core_fit: float = 50.0,
) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=net,
        evidence_rubric_bits=max(net, 0.0),
        contradiction_rubric_bits=max(-net, 0.0),
        meaningful_contradictions=contradictions,
        detailed_support=detailed,
        core_fit=core_fit,
    )


def _rank_equivalence_key(score: ScoredState) -> tuple[float | int, ...]:
    return (
        round(score.net_rubric_bits, 12),
        score.meaningful_contradictions,
        round(score.detailed_support, 12),
    )


def _rank_research_order(
    states: Sequence[CandidateState],
    scores: dict[str, ScoredState],
    *,
    order_key: SortKey,
) -> tuple[ResearchRankedState, ...]:
    ordered = sorted(states, key=order_key)
    result: list[ResearchRankedState] = []
    position = 0
    while position < len(ordered):
        key = _rank_equivalence_key(scores[ordered[position].state_id])
        end = position + 1
        while end < len(ordered) and _rank_equivalence_key(scores[ordered[end].state_id]) == key:
            end += 1
        midrank = (position + 1 + end) / 2.0
        result.extend(
            ResearchRankedState(item, scores[item.state_id], midrank)
            for item in ordered[position:end]
        )
        position = end
    return tuple(result)


def rank_group_without_core_fit(
    states: Sequence[CandidateState],
    scores: dict[str, ScoredState],
) -> tuple[ResearchRankedState, ...]:
    """Keep current sequence order while grouping on three evidence fields only."""

    return _rank_research_order(
        states,
        scores,
        order_key=lambda state: (
            -scores[state.state_id].net_rubric_bits,
            scores[state.state_id].meaningful_contradictions,
            -scores[state.state_id].detailed_support,
            -scores[state.state_id].core_fit,
            -(state.end_utc - state.start_utc).total_seconds(),
            state.start_utc,
        ),
    )


def rank_order_without_core_fit(
    states: Sequence[CandidateState],
    scores: dict[str, ScoredState],
) -> tuple[ResearchRankedState, ...]:
    """Order and group on three evidence fields, then deterministic display fields."""

    return _rank_research_order(
        states,
        scores,
        order_key=lambda state: (
            -scores[state.state_id].net_rubric_bits,
            scores[state.state_id].meaningful_contradictions,
            -scores[state.state_id].detailed_support,
            -(state.end_utc - state.start_utc).total_seconds(),
            state.start_utc,
        ),
    )


def _rank_result(ranked: Sequence[Any]) -> JsonObject:
    return {
        "ordered_state_ids": [item.state.state_id for item in ranked],
        "scientific_rank_by_state_id": {item.state.state_id: item.rank for item in ranked},
    }


def _current_rank(
    states: Sequence[CandidateState], scores: dict[str, ScoredState]
) -> tuple[Any, ...]:
    backend = object.__new__(AstroHDParticipantBackend)
    return backend._rank_states(states, scores)


def _equal_evidence_case() -> JsonObject:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _candidate_state("LOW", start),
        _candidate_state("HIGH", start + timedelta(minutes=1)),
    )
    scores = {
        "LOW": _score("LOW", core_fit=66.66666666666667),
        "HIGH": _score("HIGH", core_fit=78.57142857142857),
    }
    current = _current_rank(states, scores)
    proposal_a = rank_group_without_core_fit(states, scores)
    proposal_b = rank_order_without_core_fit(states, scores)
    backend = object.__new__(AstroHDParticipantBackend)
    return {
        "current": _rank_result(current),
        "helper_outputs": {
            "current_top_net_margin": backend._top_net_margin(current),
            "percentile_by_comparator_and_state": {
                "current": {
                    item.state.state_id: _percentile(item.rank, len(current)) for item in current
                },
                "rank_group_without_core_fit": {
                    item.state.state_id: _percentile(item.rank, len(proposal_a))
                    for item in proposal_a
                },
                "rank_order_without_core_fit": {
                    item.state.state_id: _percentile(item.rank, len(proposal_b))
                    for item in proposal_b
                },
            },
            "top_state_tie_count_by_comparator": {
                "current": sum(math.isclose(item.rank, current[0].rank) for item in current),
                "rank_group_without_core_fit": sum(
                    math.isclose(item.rank, proposal_a[0].rank) for item in proposal_a
                ),
                "rank_order_without_core_fit": sum(
                    math.isclose(item.rank, proposal_b[0].rank) for item in proposal_b
                ),
            },
        },
        "rank_group_without_core_fit": _rank_result(proposal_a),
        "rank_order_without_core_fit": _rank_result(proposal_b),
        "scores": {state_id: score.model_dump(mode="json") for state_id, score in scores.items()},
        "state_start_order": [state.state_id for state in states],
    }


def _control_case(
    control_id: str,
    preferred_score: ScoredState,
    other_score: ScoredState,
) -> JsonObject:
    start = datetime(2001, 1, 1, tzinfo=UTC)
    states = (
        _candidate_state("OTHER", start),
        _candidate_state("PREFERRED", start + timedelta(minutes=1)),
    )
    scores = {"PREFERRED": preferred_score, "OTHER": other_score}
    return {
        "control_id": control_id,
        "current": _rank_result(_current_rank(states, scores)),
        "rank_group_without_core_fit": _rank_result(rank_group_without_core_fit(states, scores)),
        "rank_order_without_core_fit": _rank_result(rank_order_without_core_fit(states, scores)),
        "scores": {state_id: score.model_dump(mode="json") for state_id, score in scores.items()},
    }


def _non_tie_controls() -> list[JsonObject]:
    return [
        _control_case(
            "different_net_rubric_bits",
            _score("PREFERRED", net=2.0, core_fit=0.0),
            _score("OTHER", net=1.0, core_fit=100.0),
        ),
        _control_case(
            "different_meaningful_contradictions",
            _score("PREFERRED", contradictions=0, core_fit=0.0),
            _score("OTHER", contradictions=1, core_fit=100.0),
        ),
        _control_case(
            "different_detailed_support",
            _score("PREFERRED", detailed=60.0, core_fit=0.0),
            _score("OTHER", detailed=50.0, core_fit=100.0),
        ),
    ]


def build_audit(repository_root: Path = ROOT) -> JsonObject:
    return {
        "comparators": {
            "equal_evidence_core_fit_difference": _equal_evidence_case(),
            "non_tie_controls": _non_tie_controls(),
        },
        "input_scope": "synthetic_candidate_and_scored_state_records_only",
        "ordered_sequence_consumers": _ordered_sequence_consumers(repository_root),
        "schema_version": "astrohd-rank-tiebreak-downstream-audit-v1",
        "source_file_hashes": _source_hashes(repository_root),
        "source_locations": _scan_locations(repository_root),
        "status": "mechanical_downstream_audit_no_runtime_effect",
    }


def write_audit(
    repository_root: Path = ROOT,
    *,
    output: Path | None = None,
) -> Path:
    _assert_historical_source_baseline(repository_root)
    output_path = output or repository_root / OUTPUT_PATH
    output_path.write_bytes(render_json(build_audit(repository_root)))
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    repository_root = arguments.repository_root.resolve()
    output = arguments.output.resolve() if arguments.output else None
    output_path = write_audit(repository_root, output=output)
    audit = json.loads(output_path.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "ordered_sequence_consumer_count": len(audit["ordered_sequence_consumers"]),
                "output": output_path.as_posix(),
                "source_file_count": len(audit["source_file_hashes"]),
                "source_location_count": len(audit["source_locations"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
