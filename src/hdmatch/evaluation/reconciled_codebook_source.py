"""Lossless structural parser for the frozen reconciled Life Patterns codebook.

The parser extracts already-authored text from the frozen Markdown. It does not invent,
paraphrase, merge, classify, or score behavioral constructs. In particular, it does not decide
which subcodes count as substantive non-action; that remains a separate frozen theory-blind
coding-procedure decision.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_OBSERVABLE_HEADING = re.compile(r"^## (NBM-R\d{2}) — (.+?)\s*$", re.MULTILINE)
_FIELD_HEADING = re.compile(r"^\*\*([^*\n]+?):\*\*\s*", re.MULTILINE)
_SUBCODE_BULLET = re.compile(r"^\* (R\d{2}-[A-Za-z0-9]+)\s+(.+?)\s*$")
_FACET_HEADING = re.compile(r"^\*\*([^*\n]+?)\*\*\s*$")


class ReconciledSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ReconciledSubcodeSource(ReconciledSourceModel):
    subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    description: str = Field(min_length=1)
    facet: str | None = None


class ReconciledObservableSource(ReconciledSourceModel):
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    heading: str = Field(min_length=1)
    short_behavioral_name: str = Field(min_length=1)
    operational_definition: str = Field(min_length=1)
    inclusion_criteria: tuple[str, ...] = Field(min_length=1)
    exclusion_criteria: tuple[str, ...] = Field(min_length=1)
    subcodes: tuple[ReconciledSubcodeSource, ...] = Field(min_length=1)
    minimum_evidence_requirements: str = Field(min_length=1)
    counterevidence: str = Field(min_length=1)
    relevant_context_modifiers: str = Field(min_length=1)
    fictional_boundary_examples: tuple[str, ...] = Field(min_length=1)
    common_coding_mistakes: str = Field(min_length=1)
    source_provenance: str = Field(min_length=1)
    raw_section_sha256: str = Field(pattern=_SHA256_PATTERN)
    raw_section_markdown: str = Field(min_length=1)

    @field_validator("subcodes")
    @classmethod
    def subcodes_are_unique(
        cls,
        value: tuple[ReconciledSubcodeSource, ...],
    ) -> tuple[ReconciledSubcodeSource, ...]:
        ids = [row.subcode_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("reconciled observable contains duplicate subcode IDs")
        return value


class ReconciledCodebookSourcePayload(ReconciledSourceModel):
    schema_version: Literal["life-patterns-reconciled-codebook-source-v1"] = (
        "life-patterns-reconciled-codebook-source-v1"
    )
    source_markdown_sha256: str = Field(pattern=_SHA256_PATTERN)
    source_title: str = Field(min_length=1)
    universal_insufficient_evidence_text: str = Field(min_length=1)
    universal_not_applicable_text: str = Field(min_length=1)
    universal_other_specified_id: Literal["OS"] = "OS"
    universal_other_specified_text: str = Field(min_length=1)
    observables: tuple[ReconciledObservableSource, ...] = Field(min_length=1)
    parser_does_not_classify_non_action: Literal[True] = True
    parser_does_not_rewrite_substantive_content: Literal[True] = True

    @model_validator(mode="after")
    def observable_set_is_unique_and_complete(self) -> ReconciledCodebookSourcePayload:
        ids = [row.observable_id for row in self.observables]
        if len(ids) != len(set(ids)):
            raise ValueError("reconciled codebook source repeats observable IDs")
        expected = [f"NBM-R{index:02d}" for index in range(1, 23)]
        if ids != expected:
            raise ValueError(f"reconciled codebook observable IDs are not exact R01-R22 sequence: {ids}")
        return self


class ReconciledCodebookSourceArtifact(ReconciledSourceModel):
    schema_version: Literal["life-patterns-reconciled-codebook-source-artifact-v1"] = (
        "life-patterns-reconciled-codebook-source-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPCB-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ReconciledCodebookSourcePayload


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _strip_terminal_semicolon(value: str) -> str:
    stripped = value.strip()
    return stripped[:-1].rstrip() if stripped.endswith(";") else stripped


def _field_value(section: str, label: str) -> str:
    match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.*)$", section, re.MULTILINE)
    if match is None:
        raise ValueError(f"reconciled observable is missing field: {label}")
    header_end = match.end() - len(match.group(1))
    following = _FIELD_HEADING.search(section, match.end())
    end = following.start() if following is not None else len(section)
    return section[header_end:end].strip()


def _bullet_items(block: str) -> tuple[str, ...]:
    items = tuple(
        line[2:].strip()
        for line in block.splitlines()
        if line.startswith("* ") and not line.startswith("* **")
    )
    if items:
        return items
    stripped = block.strip()
    if stripped:
        return (stripped,)
    raise ValueError("expected a non-empty criteria block")


def _numbered_items(block: str) -> tuple[str, ...]:
    items = tuple(
        match.group(1).strip()
        for line in block.splitlines()
        if (match := re.match(r"^\d+\.\s+(.+)$", line)) is not None
    )
    if not items:
        raise ValueError("expected at least one numbered Markdown item")
    return items


def _subcodes(block: str) -> tuple[ReconciledSubcodeSource, ...]:
    rows: list[ReconciledSubcodeSource] = []
    facet: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        facet_match = _FACET_HEADING.match(line)
        if facet_match is not None:
            facet = facet_match.group(1).strip()
            continue
        subcode_match = _SUBCODE_BULLET.match(line)
        if subcode_match is None:
            continue
        rows.append(
            ReconciledSubcodeSource(
                subcode_id=subcode_match.group(1),
                description=_strip_terminal_semicolon(subcode_match.group(2)),
                facet=facet,
            )
        )
    if not rows:
        raise ValueError("reconciled observable has no parseable substantive subcodes")
    return tuple(rows)


def _source_title(markdown: str) -> str:
    match = re.search(r"^# (.+)$", markdown, re.MULTILINE)
    if match is None:
        raise ValueError("reconciled codebook has no top-level title")
    return match.group(1).strip()


def _universal_evidence_state_text(markdown: str, state_heading: str) -> str:
    match = re.search(rf"^### {re.escape(state_heading)}\s*$", markdown, re.MULTILINE)
    if match is None:
        raise ValueError(f"reconciled codebook has no universal evidence state: {state_heading}")
    following = re.search(r"^### .+$", markdown[match.end() :], re.MULTILINE)
    end = match.end() + following.start() if following is not None else len(markdown)
    return markdown[match.end() : end].strip()


def _universal_other_specified(markdown: str) -> str:
    match = re.search(r"^\*\*OS — Other specified:\*\*\s*(.+)$", markdown, re.MULTILINE)
    if match is None:
        raise ValueError("reconciled codebook has no universal Other Specified rule")
    return match.group(1).strip()


def parse_reconciled_codebook_markdown(markdown: str) -> ReconciledCodebookSourceArtifact:
    headings = list(_OBSERVABLE_HEADING.finditer(markdown))
    if len(headings) != 22:
        raise ValueError(f"expected 22 reconciled primary observables, found {len(headings)}")

    source_stop_match = re.search(r"^# 3\. Source constructs not retained", markdown, re.MULTILINE)
    source_stop = source_stop_match.start() if source_stop_match is not None else len(markdown)
    observables: list[ReconciledObservableSource] = []

    for index, heading_match in enumerate(headings):
        start = heading_match.start()
        end = headings[index + 1].start() if index + 1 < len(headings) else source_stop
        raw_section = markdown[start:end].rstrip()
        values_block = _field_value(raw_section, "Possible substantive values/subcodes")
        observables.append(
            ReconciledObservableSource(
                observable_id=heading_match.group(1),
                heading=heading_match.group(2).strip(),
                short_behavioral_name=_field_value(raw_section, "Short behavioral name").strip(),
                operational_definition=_field_value(raw_section, "Operational definition").strip(),
                inclusion_criteria=_bullet_items(_field_value(raw_section, "Inclusion criteria")),
                exclusion_criteria=_bullet_items(_field_value(raw_section, "Exclusion criteria")),
                subcodes=_subcodes(values_block),
                minimum_evidence_requirements=_field_value(
                    raw_section,
                    "Minimum evidence requirements",
                ).strip(),
                counterevidence=_field_value(raw_section, "Counterevidence").strip(),
                relevant_context_modifiers=_field_value(
                    raw_section,
                    "Relevant context modifiers",
                ).strip(),
                fictional_boundary_examples=_numbered_items(
                    _field_value(raw_section, "Fictional boundary examples")
                ),
                common_coding_mistakes=_field_value(
                    raw_section,
                    "Common coding mistakes",
                ).strip(),
                source_provenance=_field_value(raw_section, "Source provenance").strip(),
                raw_section_sha256=_sha256_text(raw_section),
                raw_section_markdown=raw_section,
            )
        )

    payload = ReconciledCodebookSourcePayload(
        source_markdown_sha256=_sha256_text(markdown),
        source_title=_source_title(markdown),
        universal_insufficient_evidence_text=_universal_evidence_state_text(
            markdown,
            "IE — Insufficient evidence",
        ),
        universal_not_applicable_text=_universal_evidence_state_text(
            markdown,
            "NA — Not applicable",
        ),
        universal_other_specified_text=_universal_other_specified(markdown),
        observables=tuple(observables),
    )
    digest = sha256_json(payload)
    return ReconciledCodebookSourceArtifact(
        artifact_id=f"LPCB-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def parse_reconciled_codebook_file(path: str | Path) -> ReconciledCodebookSourceArtifact:
    markdown = Path(path).read_text(encoding="utf-8")
    return parse_reconciled_codebook_markdown(markdown)


def reconciled_codebook_source_integrity_errors(
    artifact: ReconciledCodebookSourceArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPCB-{digest[:20].upper()}":
        return ("reconciled codebook source failed content-address verification",)
    return ()


def write_reconciled_codebook_source(
    path: str | Path,
    artifact: ReconciledCodebookSourceArtifact,
) -> Path:
    errors = reconciled_codebook_source_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid reconciled codebook source: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_reconciled_codebook_source(path: str | Path) -> ReconciledCodebookSourceArtifact:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = ReconciledCodebookSourceArtifact.model_validate(raw)
    errors = reconciled_codebook_source_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid reconciled codebook source: " + "; ".join(errors))
    return artifact
