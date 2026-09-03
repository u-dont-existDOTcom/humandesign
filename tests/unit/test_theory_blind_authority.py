from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.theory_blind_authority import (
    BlindHumanReliabilityReceipt,
    TheoryBlindContentAuthorityPayload,
    TheoryBlindContentReviewReceipt,
    TheoryBlindDevelopmentProvenance,
    build_theory_blind_content_authority,
    compact_theory_blind_content_authority_receipt,
    load_theory_blind_content_authority,
    theory_blind_content_authority_integrity_errors,
    write_theory_blind_content_authority,
)


def _development_provenance(
    *,
    content_sha: str = "a" * 64,
    detailed_seed: bool = True,
    with_replication: bool = False,
) -> TheoryBlindDevelopmentProvenance:
    return TheoryBlindDevelopmentProvenance(
        content_sha256=content_sha,
        author_kind="ai",
        authorship_context_sha256="b" * 64,
        exact_prompt_sha256="c" * 64,
        exact_first_output_sha256="d" * 64,
        source_artifact_sha256=("e" * 64, "f" * 64),
        author_or_model_identity="STRUCTURAL_TEST_MODEL",
        author_or_model_version="STRUCTURAL_TEST_VERSION",
        fresh_session_or_workspace=True,
        prompt_author_theory_exposed=detailed_seed,
        prompt_seed_level="detailed_domain_seeded" if detailed_seed else "minimally_seeded",
        independent_replication_artifact_sha256=("1" * 64 if with_replication else None),
        reconciliation_artifact_sha256=("2" * 64 if with_replication else None),
        generated_at_utc=datetime(2026, 9, 3, 20, 0, tzinfo=UTC),
    )


def _review(
    *,
    content_sha: str = "a" * 64,
    validation: bool = False,
    changed: bool = False,
) -> TheoryBlindContentReviewReceipt:
    return TheoryBlindContentReviewReceipt(
        content_sha256=content_sha,
        reviewer_kind="human",
        review_protocol_sha256="3" * 64,
        review_notes_sha256="4" * 64,
        review_outcome=(
            "approved_validation_candidate" if validation else "approved_development_only"
        ),
        content_changed_during_review=changed,
        reviewed_at_utc=datetime(2026, 9, 3, 20, 30, tzinfo=UTC),
    )


def _reliability(*, content_sha: str = "a" * 64) -> BlindHumanReliabilityReceipt:
    return BlindHumanReliabilityReceipt(
        content_sha256=content_sha,
        ontology_artifact_sha256="5" * 64,
        coding_procedure_sha256="6" * 64,
        development_corpus_sha256="7" * 64,
        reliability_report_sha256="8" * 64,
        created_at_utc=datetime(2026, 9, 3, 21, 0, tzinfo=UTC),
    )


def test_ai_authorship_requires_exact_prompt_and_first_output_hashes() -> None:
    with pytest.raises(ValueError, match="exact prompt and first-output hashes"):
        TheoryBlindDevelopmentProvenance(
            content_sha256="a" * 64,
            author_kind="ai",
            authorship_context_sha256="b" * 64,
            prompt_author_theory_exposed=False,
            prompt_seed_level="minimally_seeded",
            generated_at_utc=datetime(2026, 9, 3, 20, 0, tzinfo=UTC),
        )


def test_detailed_theory_exposed_seed_is_allowed_for_development_only() -> None:
    payload = TheoryBlindContentAuthorityPayload(
        content_sha256="a" * 64,
        authority_stage="development_candidate",
        development_provenance=_development_provenance(with_replication=False),
        content_review=_review(),
        authorized_at_utc=datetime(2026, 9, 3, 20, 45, tzinfo=UTC),
    )
    artifact = build_theory_blind_content_authority(payload)
    assert artifact.payload.authority_stage == "development_candidate"
    assert compact_theory_blind_content_authority_receipt(artifact).authority_stage == (
        "development_candidate"
    )


def test_validation_requires_replication_reconciliation_and_human_reliability() -> None:
    with pytest.raises(ValueError, match="independent replication and reconciliation"):
        TheoryBlindContentAuthorityPayload(
            content_sha256="a" * 64,
            authority_stage="validation_candidate",
            development_provenance=_development_provenance(with_replication=False),
            human_reliability=_reliability(),
            content_review=_review(validation=True),
            authorized_at_utc=datetime(2026, 9, 3, 21, 15, tzinfo=UTC),
        )

    with pytest.raises(ValueError, match="human-human reliability evidence"):
        TheoryBlindContentAuthorityPayload(
            content_sha256="a" * 64,
            authority_stage="validation_candidate",
            development_provenance=_development_provenance(with_replication=True),
            content_review=_review(validation=True),
            authorized_at_utc=datetime(2026, 9, 3, 21, 15, tzinfo=UTC),
        )


def test_validation_path_binds_exact_content_and_chronology() -> None:
    payload = TheoryBlindContentAuthorityPayload(
        content_sha256="a" * 64,
        authority_stage="validation_candidate",
        development_provenance=_development_provenance(with_replication=True),
        human_reliability=_reliability(),
        content_review=_review(validation=True),
        authorized_at_utc=datetime(2026, 9, 3, 21, 15, tzinfo=UTC),
    )
    artifact = build_theory_blind_content_authority(payload)
    assert theory_blind_content_authority_integrity_errors(artifact) == ()
    receipt = compact_theory_blind_content_authority_receipt(artifact)
    assert receipt.content_sha256 == "a" * 64
    assert receipt.authority_stage == "validation_candidate"

    with pytest.raises(ValueError, match="human reliability receipt does not bind"):
        TheoryBlindContentAuthorityPayload(
            content_sha256="a" * 64,
            authority_stage="validation_candidate",
            development_provenance=_development_provenance(with_replication=True),
            human_reliability=_reliability(content_sha="9" * 64),
            content_review=_review(validation=True),
            authorized_at_utc=datetime(2026, 9, 3, 21, 15, tzinfo=UTC),
        )

    with pytest.raises(ValueError, match="cannot precede its latest dependency"):
        TheoryBlindContentAuthorityPayload(
            content_sha256="a" * 64,
            authority_stage="validation_candidate",
            development_provenance=_development_provenance(with_replication=True),
            human_reliability=_reliability(),
            content_review=_review(validation=True),
            authorized_at_utc=datetime(2026, 9, 3, 20, 45, tzinfo=UTC),
        )


def test_validation_review_cannot_silently_change_content() -> None:
    with pytest.raises(ValueError, match="new content hash"):
        _review(validation=True, changed=True)


def test_authority_artifact_is_content_addressed_and_immutable(tmp_path: Path) -> None:
    payload = TheoryBlindContentAuthorityPayload(
        content_sha256="a" * 64,
        authority_stage="development_candidate",
        development_provenance=_development_provenance(with_replication=False),
        content_review=_review(),
        authorized_at_utc=datetime(2026, 9, 3, 20, 45, tzinfo=UTC),
    )
    artifact = build_theory_blind_content_authority(payload)
    assert artifact.authority_id == f"LPTB-{artifact.authority_sha256[:20].upper()}"

    path = tmp_path / "authority.json"
    write_theory_blind_content_authority(path, artifact)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_theory_blind_content_authority(path) == artifact
    with pytest.raises(FileExistsError):
        write_theory_blind_content_authority(path, artifact)
