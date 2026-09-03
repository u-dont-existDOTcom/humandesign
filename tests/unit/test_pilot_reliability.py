from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.pilot_reliability import (
    PilotAdjudicationPayload,
    PilotCoderOutputReference,
    PilotCorpusItem,
    PilotCorpusManifestPayload,
    PilotFirstPassPayload,
    build_pilot_adjudication,
    build_pilot_corpus_manifest,
    build_pilot_first_pass,
    load_pilot_corpus_manifest,
    pilot_adjudication_integrity_errors,
    pilot_corpus_manifest_integrity_errors,
    pilot_first_pass_integrity_errors,
    write_pilot_artifact,
)


def _item(
    item_id: str,
    *,
    role: str = "reliability",
    reason: str = "ordinary_development_episode",
) -> PilotCorpusItem:
    return PilotCorpusItem(
        pilot_item_id=item_id,
        role=role,  # type: ignore[arg-type]
        freeze_id="BPF-1234567890ABCDEF1234",
        freeze_sha256="a" * 64,
        episode_id=f"EP-{item_id}",
        episode_sha256="b" * 64,
        selection_reason=reason,  # type: ignore[arg-type]
        boundary_case_tags=("BOUNDARY_ALPHA",) if reason == "boundary_case" else (),
    )


def _manifest() -> object:
    payload = PilotCorpusManifestPayload(
        codebook_content_sha256="c" * 64,
        coding_procedure_sha256="d" * 64,
        training_protocol_sha256="e" * 64,
        items=(
            _item("TRAIN-1", role="training"),
            _item("REL-1"),
            _item("REL-2", reason="boundary_case"),
        ),
        created_at_utc=datetime(2026, 9, 3, 22, 0, tzinfo=UTC),
    )
    return build_pilot_corpus_manifest(payload)


def _coder_output(coder_id: str, start_minute: int, freeze_minute: int) -> PilotCoderOutputReference:
    return PilotCoderOutputReference(
        coder_id=coder_id,
        training_receipt_sha256=("1" if coder_id == "CODER-A" else "2") * 64,
        annotation_output_sha256=("3" if coder_id == "CODER-A" else "4") * 64,
        coding_started_at_utc=datetime(2026, 9, 3, 22, start_minute, tzinfo=UTC),
        coding_frozen_at_utc=datetime(2026, 9, 3, 22, freeze_minute, tzinfo=UTC),
    )


def test_boundary_case_requires_theory_neutral_tag() -> None:
    with pytest.raises(ValueError, match="boundary-case pilot items require"):
        PilotCorpusItem(
            pilot_item_id="REL-X",
            role="reliability",
            freeze_id="BPF-1234567890ABCDEF1234",
            freeze_sha256="a" * 64,
            episode_id="EP-X",
            episode_sha256="b" * 64,
            selection_reason="boundary_case",
        )


def test_manifest_is_content_addressed_and_immutable(tmp_path: Path) -> None:
    manifest = _manifest()
    assert hasattr(manifest, "manifest_id")
    assert pilot_corpus_manifest_integrity_errors(manifest) == ()  # type: ignore[arg-type]

    path = tmp_path / "pilot-manifest.json"
    write_pilot_artifact(path, manifest)  # type: ignore[arg-type]
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_pilot_corpus_manifest(path) == manifest
    with pytest.raises(FileExistsError):
        write_pilot_artifact(path, manifest)  # type: ignore[arg-type]


def test_first_pass_requires_distinct_independent_coders_and_ordered_freeze() -> None:
    with pytest.raises(ValueError, match="distinct coder identities"):
        PilotFirstPassPayload(
            corpus_manifest_id="LPPM-1234567890ABCDEF1234",
            corpus_manifest_sha256="a" * 64,
            codebook_content_sha256="b" * 64,
            coding_procedure_sha256="c" * 64,
            coder_outputs=(
                _coder_output("CODER-A", 1, 5),
                _coder_output("CODER-A", 6, 10),
            ),
            frozen_at_utc=datetime(2026, 9, 3, 22, 15, tzinfo=UTC),
        )

    with pytest.raises(ValueError, match="cannot precede a coder-output freeze"):
        PilotFirstPassPayload(
            corpus_manifest_id="LPPM-1234567890ABCDEF1234",
            corpus_manifest_sha256="a" * 64,
            codebook_content_sha256="b" * 64,
            coding_procedure_sha256="c" * 64,
            coder_outputs=(
                _coder_output("CODER-A", 1, 5),
                _coder_output("CODER-B", 6, 20),
            ),
            frozen_at_utc=datetime(2026, 9, 3, 22, 15, tzinfo=UTC),
        )


def test_adjudication_binds_frozen_first_pass_and_occurs_after_it() -> None:
    first_pass = build_pilot_first_pass(
        PilotFirstPassPayload(
            corpus_manifest_id="LPPM-1234567890ABCDEF1234",
            corpus_manifest_sha256="a" * 64,
            codebook_content_sha256="b" * 64,
            coding_procedure_sha256="c" * 64,
            coder_outputs=(
                _coder_output("CODER-A", 1, 5),
                _coder_output("CODER-B", 6, 10),
            ),
            frozen_at_utc=datetime(2026, 9, 3, 22, 15, tzinfo=UTC),
        )
    )
    adjudication = build_pilot_adjudication(
        PilotAdjudicationPayload(
            first_pass_id=first_pass.first_pass_id,
            first_pass_sha256=first_pass.first_pass_sha256,
            adjudication_output_sha256="d" * 64,
            adjudicator_ids=("CODER-A", "CODER-B"),
            adjudicated_at_utc=datetime(2026, 9, 3, 22, 30, tzinfo=UTC),
        )
    )
    assert pilot_first_pass_integrity_errors(first_pass) == ()
    assert pilot_adjudication_integrity_errors(adjudication, first_pass) == ()

    wrong_first_pass = first_pass.model_copy(
        update={"first_pass_sha256": "f" * 64},
    )
    errors = pilot_adjudication_integrity_errors(adjudication, wrong_first_pass)
    assert any("does not bind" in error for error in errors)
