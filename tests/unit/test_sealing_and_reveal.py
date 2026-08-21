from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import ArtifactBindings, freeze_predictions
from hdmatch.experiments.reveal import reveal_answer_key
from hdmatch.runtime.recovery import RecoverySettings, recover_blind_file
from hdmatch.search import AggregationMode
from hdmatch.synthetic.sealing import (
    AnswerKeySealingError,
    SealingMetadata,
    assert_no_plaintext_answer_keys,
    decrypt_answer_key_json,
    decrypt_answer_key_to_file,
    generate_key_file,
    seal_answer_key,
    seal_answer_key_file,
)


def _digest(label: str) -> str:
    return sha256_bytes(label.encode())


def _bindings() -> ArtifactBindings:
    return ArtifactBindings(
        blind_input_sha256=_digest("blind"),
        model_sha256=_digest("model"),
        question_bank_sha256=_digest("questions"),
        mapping_sha256=_digest("mapping"),
    )


def _metadata() -> SealingMetadata:
    return SealingMetadata(experiment_id="EXP-1", **_bindings().model_dump())


def _answer_key() -> dict[str, object]:
    return {
        "schema_version": "answer-key-v1",
        "experiment_id": "EXP-1",
        "blind_input_sha256": _digest("blind"),
        "cases": [{"case_id": "C1", "true_local_date": "2000-01-02"}],
    }


def test_aes_gcm_round_trip_authenticates_metadata_and_external_key(tmp_path: Path) -> None:
    project = tmp_path / "decoder"
    project.mkdir()
    key_path = tmp_path / "secret.key"
    encrypted = project / "answer-key.json.enc"
    generate_key_file(key_path, decoder_root=project)
    assert key_path.stat().st_mode & 0o077 == 0
    seal_answer_key(
        _answer_key(),
        encrypted_path=encrypted,
        key_path=key_path,
        metadata=_metadata(),
        decoder_root=project,
    )
    assert decrypt_answer_key_json(
        encrypted,
        key_path=key_path,
        decoder_root=project,
        expected_metadata=_metadata(),
    ) == _answer_key()

    envelope = json.loads(encrypted.read_bytes())
    envelope["authenticated_metadata"]["experiment_id"] = "OTHER"
    encrypted.write_bytes(json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode())
    with pytest.raises(AnswerKeySealingError, match="metadata"):
        decrypt_answer_key_json(
            encrypted,
            key_path=key_path,
            decoder_root=project,
            expected_metadata=_metadata(),
        )


def test_aes_gcm_rejects_tampered_ciphertext_wrong_key_and_open_permissions(
    tmp_path: Path,
) -> None:
    project = tmp_path / "decoder"
    project.mkdir()
    key_path = tmp_path / "secret.key"
    wrong_key = tmp_path / "wrong.key"
    generate_key_file(key_path, decoder_root=project)
    generate_key_file(wrong_key, decoder_root=project)
    encrypted = project / "answer-key.json.enc"
    seal_answer_key(
        _answer_key(),
        encrypted_path=encrypted,
        key_path=key_path,
        metadata=_metadata(),
        decoder_root=project,
    )
    with pytest.raises(AnswerKeySealingError, match="authentication"):
        decrypt_answer_key_json(
            encrypted,
            key_path=wrong_key,
            decoder_root=project,
            expected_metadata=_metadata(),
        )

    envelope = json.loads(encrypted.read_bytes())
    ciphertext = envelope["ciphertext_base64"]
    envelope["ciphertext_base64"] = ("A" if ciphertext[0] != "A" else "B") + ciphertext[1:]
    encrypted.write_bytes(json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode())
    with pytest.raises(AnswerKeySealingError, match="authentication"):
        decrypt_answer_key_json(
            encrypted,
            key_path=key_path,
            decoder_root=project,
            expected_metadata=_metadata(),
        )

    key_path.chmod(0o644)
    with pytest.raises(AnswerKeySealingError, match="owner-only"):
        decrypt_answer_key_json(
            encrypted,
            key_path=key_path,
            decoder_root=project,
            expected_metadata=_metadata(),
        )


def test_plaintext_and_key_paths_under_decoder_root_are_refused(tmp_path: Path) -> None:
    project = tmp_path / "decoder"
    project.mkdir()
    with pytest.raises(AnswerKeySealingError, match="outside"):
        generate_key_file(project / "secret.key", decoder_root=project)

    key_path = tmp_path / "secret.key"
    generate_key_file(key_path, decoder_root=project)
    encrypted = project / "answer-key.json.enc"
    seal_answer_key(
        _answer_key(),
        encrypted_path=encrypted,
        key_path=key_path,
        metadata=_metadata(),
        decoder_root=project,
    )
    linked_key = project / "linked.key"
    linked_key.symlink_to(key_path)
    with pytest.raises(AnswerKeySealingError, match="outside"):
        decrypt_answer_key_json(
            encrypted,
            key_path=linked_key,
            decoder_root=project,
        )
    plaintext = project / "answer-key.json"
    write_new_canonical_json(plaintext, _answer_key())
    with pytest.raises(AnswerKeySealingError, match="plaintext answer key"):
        seal_answer_key_file(
            plaintext,
            encrypted_path=project / "another-answer-key.json.enc",
            key_path=key_path,
            metadata=_metadata(),
            decoder_root=project,
        )
    with pytest.raises(AnswerKeySealingError, match="plaintext answer key file"):
        assert_no_plaintext_answer_keys(project)
    with pytest.raises(AnswerKeySealingError, match="output"):
        decrypt_answer_key_to_file(
            project / "missing.enc",
            output_path=project / "revealed.json",
            key_path=key_path,
            decoder_root=project,
        )


def test_recovery_plaintext_preflight_runs_before_blind_input_or_scoring(tmp_path: Path) -> None:
    project = tmp_path / "decoder"
    project.mkdir()
    write_new_canonical_json(project / "answer-key.json", _answer_key())

    with pytest.raises(AnswerKeySealingError, match="plaintext answer key file"):
        recover_blind_file(
            project / "missing-blind.json",
            decoder_root=project,
            model=None,  # type: ignore[arg-type]
            ephemeris_path=project / "missing-ephemeris",
            cache_dir=project / "cache",
            settings=RecoverySettings(
                aggregation=AggregationMode.DURATION_WEIGHTED_EVIDENCE,
                threshold_rubric_bits=0.0,
            ),
        )


def test_reveal_requires_valid_unchanged_freeze_and_matching_envelope(tmp_path: Path) -> None:
    project = tmp_path / "decoder"
    run_dir = project / "run"
    run_dir.mkdir(parents=True)
    key_path = tmp_path / "evaluator.key"
    encrypted = run_dir / "answer-key.json.enc"
    generate_key_file(key_path, decoder_root=project)
    seal_answer_key(
        _answer_key(),
        encrypted_path=encrypted,
        key_path=key_path,
        metadata=_metadata(),
        decoder_root=project,
    )
    (run_dir / "predictions.json").write_bytes(b"{}")

    with pytest.raises(Exception, match="freeze"):
        reveal_answer_key(
            run_dir,
            encrypted_answer_key_path=encrypted,
            key_path=key_path,
            decoder_root=project,
        )

    freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    result = reveal_answer_key(
        run_dir,
        encrypted_answer_key_path=encrypted,
        key_path=key_path,
        decoder_root=project,
        revealed_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    assert result.answer_key == _answer_key()
    assert "true_local_date" not in repr(result)
    assert "answer_key" not in result.model_dump()
    assert result.record.answer_key_revealed is True
    assert result.record.encrypted_answer_key_file == "answer-key.json.enc"
    assert result.record.encrypted_answer_key_sha256 == sha256_file(encrypted)
    assert result.record.answer_key_payload_sha256 == sha256_bytes(
        canonical_json_bytes(_answer_key())
    )
    assert not (run_dir / "answer-key.json").exists()


def test_reveal_refuses_changed_prediction_bytes(tmp_path: Path) -> None:
    project = tmp_path / "decoder"
    run_dir = project / "run"
    run_dir.mkdir(parents=True)
    key_path = tmp_path / "evaluator.key"
    encrypted = run_dir / "answer-key.json.enc"
    generate_key_file(key_path, decoder_root=project)
    seal_answer_key(
        _answer_key(),
        encrypted_path=encrypted,
        key_path=key_path,
        metadata=_metadata(),
        decoder_root=project,
    )
    predictions = run_dir / "predictions.json"
    predictions.write_bytes(b"{}")
    freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
    )
    predictions.write_bytes(b'{"changed":true}')
    with pytest.raises(Exception, match="frozen prediction"):
        reveal_answer_key(
            run_dir,
            encrypted_answer_key_path=encrypted,
            key_path=key_path,
            decoder_root=project,
        )
