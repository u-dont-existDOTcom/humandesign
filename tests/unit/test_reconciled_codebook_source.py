from __future__ import annotations

import stat
from pathlib import Path

import pytest

from hdmatch.evaluation.reconciled_codebook_source import (
    load_reconciled_codebook_source,
    parse_reconciled_codebook_file,
    parse_reconciled_codebook_markdown,
    reconciled_codebook_source_integrity_errors,
    write_reconciled_codebook_source,
)

CODEBOOK_PATH = Path(
    "state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md"
)


def _observable(artifact, observable_id: str):
    return next(row for row in artifact.payload.observables if row.observable_id == observable_id)


def test_frozen_reconciled_markdown_parses_exactly_22_primary_observables() -> None:
    artifact = parse_reconciled_codebook_file(CODEBOOK_PATH)
    assert artifact.payload.source_title == (
        "Neutral Behavioral Measurement Codebook — Theory-Blind Reconciled Candidate v1"
    )
    assert [row.observable_id for row in artifact.payload.observables] == [
        f"NBM-R{index:02d}" for index in range(1, 23)
    ]
    assert artifact.payload.universal_other_specified_id == "OS"
    assert "qualifying behavior" in artifact.payload.universal_other_specified_text
    assert artifact.payload.parser_does_not_classify_non_action is True
    assert reconciled_codebook_source_integrity_errors(artifact) == ()


def test_parser_preserves_simple_and_faceted_subcode_structures() -> None:
    artifact = parse_reconciled_codebook_file(CODEBOOK_PATH)

    r01 = _observable(artifact, "NBM-R01")
    assert [row.subcode_id for row in r01.subcodes] == [
        "R01-a",
        "R01-b",
        "R01-c",
        "R01-d",
        "R01-e",
        "R01-f",
        "R01-g",
        "R01-h",
    ]
    assert all(row.facet is None for row in r01.subcodes)

    r05 = _observable(artifact, "NBM-R05")
    assert [row.subcode_id for row in r05.subcodes] == [
        "R05-O1",
        "R05-O2",
        "R05-O3",
        "R05-O4",
        "R05-O5",
        "R05-O6",
        "R05-R1",
        "R05-R2",
        "R05-R3",
        "R05-R4",
        "R05-R5",
        "R05-R6",
        "R05-R7",
        "R05-R8",
        "R05-R9",
    ]
    assert {row.facet for row in r05.subcodes} == {"Option-set facet", "Resolution facet"}

    r11 = _observable(artifact, "NBM-R11")
    assert {row.facet for row in r11.subcodes} == {
        "Immediate-response facet",
        "Later goal-status facet",
    }
    assert r11.subcodes[0].subcode_id == "R11-I1"
    assert r11.subcodes[-1].subcode_id == "R11-G7"

    r22 = _observable(artifact, "NBM-R22")
    assert r22.subcodes[-1].subcode_id == "R22-g"


def test_parser_copies_operational_fields_without_substantive_rewriting() -> None:
    markdown = CODEBOOK_PATH.read_text(encoding="utf-8")
    artifact = parse_reconciled_codebook_markdown(markdown)
    r02 = _observable(artifact, "NBM-R02")
    assert r02.short_behavioral_name == "Information seeking."
    assert r02.operational_definition.startswith("Deliberate action to obtain")
    assert "recognized information gap" in r02.inclusion_criteria[0]
    assert "Recognized information gap" in r02.minimum_evidence_requirements
    assert r02.raw_section_markdown in markdown


def test_parser_artifact_is_content_addressed_and_immutable(tmp_path: Path) -> None:
    artifact = parse_reconciled_codebook_file(CODEBOOK_PATH)
    path = tmp_path / "reconciled-source.json"
    write_reconciled_codebook_source(path, artifact)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_reconciled_codebook_source(path) == artifact
    with pytest.raises(FileExistsError):
        write_reconciled_codebook_source(path, artifact)


def test_parser_fails_closed_if_primary_observable_is_removed() -> None:
    markdown = CODEBOOK_PATH.read_text(encoding="utf-8")
    start = markdown.index("## NBM-R22 —")
    end = markdown.index("# 3. Source constructs not retained")
    damaged = markdown[:start] + markdown[end:]
    with pytest.raises(ValueError, match="expected 22"):
        parse_reconciled_codebook_markdown(damaged)
