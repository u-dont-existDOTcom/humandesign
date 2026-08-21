"""Authenticated answer-key encryption with an external 256-bit key file."""

from __future__ import annotations

import base64
import json
import os
import stat
from pathlib import Path
from typing import Any, Literal

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, ConfigDict, Field

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
    write_new_canonical_json,
)
from hdmatch.experiments.manifest import SHA256_PATTERN


class AnswerKeySealingError(RuntimeError):
    """The answer key could not be safely sealed or authenticated."""


class SealingMetadata(BaseModel):
    """Non-secret experiment bindings authenticated as AES-GCM associated data."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    experiment_id: str = Field(min_length=1)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)


class AnswerKeyEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["answer-key-envelope-v1"] = "answer-key-envelope-v1"
    algorithm: Literal["AES-256-GCM"] = "AES-256-GCM"
    nonce_base64: str
    ciphertext_base64: str
    authenticated_metadata: SealingMetadata
    associated_data_sha256: str = Field(pattern=SHA256_PATTERN)


def _is_within(path: str | Path, root: str | Path) -> bool:
    candidate_path = Path(path).expanduser()
    boundary_path = Path(root).expanduser()
    candidate_lexical = Path(os.path.abspath(candidate_path))
    boundary_lexical = Path(os.path.abspath(boundary_path))
    candidate_resolved = candidate_path.resolve(strict=False)
    boundary_resolved = boundary_path.resolve(strict=False)
    return (
        candidate_lexical == boundary_lexical
        or boundary_lexical in candidate_lexical.parents
        or candidate_resolved == boundary_resolved
        or boundary_resolved in candidate_resolved.parents
    )


def require_external_path(path: str | Path, decoder_root: str | Path, *, label: str) -> None:
    if _is_within(path, decoder_root):
        raise AnswerKeySealingError(f"{label} must remain outside the decoder project root")


def assert_no_plaintext_answer_keys(decoder_root: str | Path) -> None:
    """Refuse a blind run when an answer-key-v1 JSON is readable below its root."""

    root = Path(decoder_root)
    offending: list[str] = []
    for candidate in root.rglob("*.json"):
        if not candidate.is_file():
            continue
        try:
            value = json.loads(candidate.read_bytes())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and value.get("schema_version") == "answer-key-v1":
            try:
                name = candidate.relative_to(root).as_posix()
            except ValueError:
                name = candidate.name
            offending.append(name)
    if offending:
        raise AnswerKeySealingError(
            f"{len(offending)} plaintext answer key file(s) exist under decoder project root"
        )


def generate_key_file(path: str | Path, *, decoder_root: str | Path) -> Path:
    """Create a new base64-encoded AES-256 key with owner-only permissions."""

    destination = Path(path).expanduser()
    require_external_path(destination, decoder_root, label="encryption key file")
    destination.parent.mkdir(parents=True, exist_ok=True)
    encoded = base64.urlsafe_b64encode(AESGCM.generate_key(bit_length=256)) + b"\n"
    try:
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise FileExistsError("refusing to replace external encryption key") from None
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return destination


def _load_key(path: str | Path, *, decoder_root: str | Path) -> bytes:
    require_external_path(path, decoder_root, label="encryption key file")
    try:
        source = Path(path)
        if stat.S_IMODE(source.stat().st_mode) & 0o077:
            raise AnswerKeySealingError("external encryption key permissions must be owner-only")
        encoded = source.read_bytes().strip()
        key = base64.b64decode(encoded, altchars=b"-_", validate=True)
    except AnswerKeySealingError:
        raise
    except (OSError, ValueError) as exc:
        raise AnswerKeySealingError("cannot load valid external encryption key") from exc
    if len(key) != 32:
        raise AnswerKeySealingError("AES-256 key file must contain exactly 32 decoded bytes")
    return key


def _associated_data(metadata: SealingMetadata) -> bytes:
    return canonical_json_bytes(
        {
            "schema_version": "answer-key-envelope-v1",
            "algorithm": "AES-256-GCM",
            "authenticated_metadata": metadata,
        }
    )


def seal_answer_key(
    answer_key: Any,
    *,
    encrypted_path: str | Path,
    key_path: str | Path,
    metadata: SealingMetadata,
    decoder_root: str | Path,
) -> AnswerKeyEnvelope:
    """Seal an in-memory answer-key object without creating plaintext in the project."""

    key = _load_key(key_path, decoder_root=decoder_root)
    plaintext = answer_key if isinstance(answer_key, bytes) else canonical_json_bytes(answer_key)
    nonce = os.urandom(12)
    aad = _associated_data(metadata)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    envelope = AnswerKeyEnvelope(
        nonce_base64=base64.b64encode(nonce).decode("ascii"),
        ciphertext_base64=base64.b64encode(ciphertext).decode("ascii"),
        authenticated_metadata=metadata,
        associated_data_sha256=sha256_bytes(aad),
    )
    write_new_canonical_json(encrypted_path, envelope)
    return envelope


def seal_answer_key_file(
    plaintext_path: str | Path,
    *,
    encrypted_path: str | Path,
    key_path: str | Path,
    metadata: SealingMetadata,
    decoder_root: str | Path,
) -> AnswerKeyEnvelope:
    """Seal an existing key only when its plaintext path is outside decoder access."""

    require_external_path(plaintext_path, decoder_root, label="plaintext answer key")
    try:
        plaintext = Path(plaintext_path).read_bytes()
    except OSError as exc:
        raise AnswerKeySealingError("cannot read external plaintext answer key") from exc
    return seal_answer_key(
        plaintext,
        encrypted_path=encrypted_path,
        key_path=key_path,
        metadata=metadata,
        decoder_root=decoder_root,
    )


def load_envelope(path: str | Path) -> AnswerKeyEnvelope:
    try:
        value = load_json_bytes(path, require_canonical=True)
        return AnswerKeyEnvelope.model_validate(value)
    except (OSError, ValueError) as exc:
        raise AnswerKeySealingError("invalid encrypted answer-key envelope") from exc


def decrypt_answer_key_bytes(
    encrypted_path: str | Path,
    *,
    key_path: str | Path,
    decoder_root: str | Path,
    expected_metadata: SealingMetadata | None = None,
) -> bytes:
    """Authenticate and decrypt in memory; this function never writes plaintext."""

    envelope = load_envelope(encrypted_path)
    if expected_metadata is not None and envelope.authenticated_metadata != expected_metadata:
        raise AnswerKeySealingError("answer-key metadata does not match frozen run bindings")
    aad = _associated_data(envelope.authenticated_metadata)
    if sha256_bytes(aad) != envelope.associated_data_sha256:
        raise AnswerKeySealingError("answer-key associated-data digest is inconsistent")
    key = _load_key(key_path, decoder_root=decoder_root)
    try:
        nonce = base64.b64decode(envelope.nonce_base64, validate=True)
        ciphertext = base64.b64decode(envelope.ciphertext_base64, validate=True)
        if len(nonce) != 12:
            raise ValueError("AES-GCM nonce must be 12 bytes")
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except (InvalidTag, ValueError) as exc:
        raise AnswerKeySealingError("answer-key authentication failed") from exc


def decrypt_answer_key_json(
    encrypted_path: str | Path,
    *,
    key_path: str | Path,
    decoder_root: str | Path,
    expected_metadata: SealingMetadata | None = None,
) -> Any:
    plaintext = decrypt_answer_key_bytes(
        encrypted_path,
        key_path=key_path,
        decoder_root=decoder_root,
        expected_metadata=expected_metadata,
    )
    try:
        return json.loads(plaintext)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AnswerKeySealingError("decrypted answer key is not valid UTF-8 JSON") from exc


def decrypt_answer_key_to_file(
    encrypted_path: str | Path,
    *,
    output_path: str | Path,
    key_path: str | Path,
    decoder_root: str | Path,
    expected_metadata: SealingMetadata | None = None,
) -> Path:
    """Explicit export helper that forbids plaintext under the decoder root."""

    require_external_path(output_path, decoder_root, label="plaintext answer-key output")
    plaintext = decrypt_answer_key_bytes(
        encrypted_path,
        key_path=key_path,
        decoder_root=decoder_root,
        expected_metadata=expected_metadata,
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise FileExistsError("refusing to replace external plaintext answer key") from None
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(plaintext)
        handle.flush()
        os.fsync(handle.fileno())
    return destination
