"""Authenticated answer-key encryption with an external 256-bit key file."""

from __future__ import annotations

import base64
import csv
import json
import os
import re
import stat
from collections.abc import Iterable
from contextlib import suppress
from pathlib import Path
from typing import Any, Literal

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, ConfigDict, Field

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
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


_PREFLIGHT_SKIPPED_DIRECTORIES = {
    ".eggs",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}
_OBVIOUS_ANSWER_KEY_NAME = re.compile(
    r"(?:answer[_. -]?key|ground[_. -]?truth|truth[_. -]?key)"
    r"(?:[ _-](?:backup|copy|export|plain|plaintext))?",
    re.IGNORECASE,
)
_MAX_PREFLIGHT_TEXT_BYTES = 16 * 1024 * 1024
_PLAINTEXT_ANSWER_KEY_SCHEMAS = {
    "answer-key-v1",
    "human-cohort-answer-key-v1",
}
_SAFE_ANSWER_KEY_ARTIFACT_SCHEMAS = {
    "answer-key-envelope-v1",
    "answer-key-reveal-v1",
    "answer-key-reveal-v2",
    "human-answer-key-reveal-receipt-v1",
    "human-final-test-reveal-ledger-v1",
}
_SYNTHETIC_TRUTH_FIELDS = {
    "true_chart_features_hash",
    "true_local_date",
    "true_state_id",
    "true_utc",
}


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


def _has_obvious_answer_key_name(filename: str) -> bool:
    candidate = filename
    while candidate:
        if _OBVIOUS_ANSWER_KEY_NAME.fullmatch(candidate) is not None:
            return True
        candidate, separator, _suffix = candidate.rpartition(".")
        if not separator:
            return False
    return False


def _contains_plaintext_answer_key(value: object) -> bool:
    if isinstance(value, dict):
        schema = value.get("schema_version")
        if schema in _PLAINTEXT_ANSWER_KEY_SCHEMAS:
            return True
        synthetic_bindings = {"experiment_id", "blind_input_sha256", "cases"}
        cases = value.get("cases")
        if (
            synthetic_bindings <= value.keys()
            and isinstance(cases, list)
            and any(
                isinstance(case, dict) and bool(_SYNTHETIC_TRUTH_FIELDS & case.keys())
                for case in cases
            )
        ):
            return True
        human_bindings = {
            "cohort",
            "protocol_sha256",
            "blind_input_sha256",
            "true_candidate_ids",
        }
        if human_bindings <= value.keys() and isinstance(value.get("true_candidate_ids"), dict):
            return True
        return any(_contains_plaintext_answer_key(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_plaintext_answer_key(item) for item in value)
    return False


def _is_safe_answer_key_artifact(value: object) -> bool:
    return (
        isinstance(value, dict)
        and value.get("schema_version") in _SAFE_ANSWER_KEY_ARTIFACT_SCHEMAS
    )


def _looks_like_tabular_answer_key(text: str) -> bool:
    """Recognize standalone CSV/TSV truth tables without trusting their suffix."""

    sample = text[:8192]
    for delimiter in (",", "\t", ";"):
        try:
            rows = csv.reader(sample.splitlines(), delimiter=delimiter)
            header = next(rows)
        except (csv.Error, StopIteration):
            continue
        normalized = {re.sub(r"[^a-z0-9]", "", item.casefold()) for item in header}
        synthetic_truth = {
            re.sub(r"[^a-z0-9]", "", field.casefold()) for field in _SYNTHETIC_TRUTH_FIELDS
        }
        if "caseid" in normalized and bool(normalized & synthetic_truth):
            return True
        if "participantid" in normalized and bool(
            normalized & {"truecandidateid", "truecandidateids"}
        ):
            return True
    return False


def _candidate_files(path: Path) -> tuple[Path, ...]:
    if path.is_file():
        return (path,)
    if not path.is_dir():
        return ()
    candidates: list[Path] = []
    for current, directories, filenames in os.walk(path, followlinks=False):
        directories[:] = [
            name
            for name in directories
            if name.casefold() not in _PREFLIGHT_SKIPPED_DIRECTORIES
            and not name.casefold().endswith(".egg-info")
        ]
        candidates.extend(Path(current) / filename for filename in filenames)
    return tuple(candidates)


def _minimal_scan_paths(paths: Iterable[str | Path]) -> tuple[Path, ...]:
    """Deduplicate existing file/tree inputs without broadening to their parents."""

    resolved = sorted(
        {Path(path).expanduser().resolve(strict=False) for path in paths if Path(path).exists()},
        key=lambda item: (len(item.parts), item.as_posix()),
    )
    selected: list[Path] = []
    for candidate in resolved:
        if any(parent == candidate or parent in candidate.parents for parent in selected):
            continue
        selected.append(candidate)
    return tuple(selected)


def assert_no_plaintext_answer_keys_in_paths(paths: Iterable[str | Path]) -> None:
    """Refuse readable plaintext keys in bounded decoder-visible files and trees."""

    offending: list[str] = []
    for root in _minimal_scan_paths(paths):
        for candidate in _candidate_files(root):
            try:
                if (
                    not candidate.is_file()
                    or candidate.stat().st_size > _MAX_PREFLIGHT_TEXT_BYTES
                ):
                    continue
                raw = candidate.read_bytes()
            except OSError:
                continue
            if b"\x00" in raw[:8192]:
                continue
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            parsed: object = None
            with suppress(json.JSONDecodeError):
                parsed = json.loads(text)
            answer_key_schema = _contains_plaintext_answer_key(parsed)
            obvious_plaintext_name = (
                not _is_safe_answer_key_artifact(parsed)
                and _has_obvious_answer_key_name(candidate.name)
                and bool(text.strip())
            )
            tabular_answer_key = _looks_like_tabular_answer_key(text)
            if not answer_key_schema and not obvious_plaintext_name and not tabular_answer_key:
                continue
            try:
                name = candidate.relative_to(root).as_posix() if root.is_dir() else candidate.name
            except ValueError:
                name = candidate.name
            offending.append(name)
    if offending:
        raise AnswerKeySealingError(
            f"{len(offending)} plaintext answer key file(s) exist under decoder project root"
        )


def assert_no_plaintext_answer_keys(decoder_root: str | Path) -> None:
    """Backward-compatible one-root preflight used by freeze and human workflows."""

    assert_no_plaintext_answer_keys_in_paths((decoder_root,))


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
        raw = Path(path).read_bytes()
        return load_envelope_bytes(raw)
    except (OSError, ValueError) as exc:
        raise AnswerKeySealingError("invalid encrypted answer-key envelope") from exc


def load_envelope_bytes(raw: bytes) -> AnswerKeyEnvelope:
    """Parse one exact canonical envelope byte string."""

    try:
        value = json.loads(raw)
        if canonical_json_bytes(value) != raw:
            raise ValueError("encrypted answer-key envelope is not canonical JSON")
        return AnswerKeyEnvelope.model_validate(value)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise AnswerKeySealingError("invalid encrypted answer-key envelope") from exc


def verify_envelope_bindings(
    path: str | Path,
    *,
    expected_metadata: SealingMetadata | None = None,
) -> AnswerKeyEnvelope:
    """Validate canonical envelope structure and its public authenticated bindings."""

    envelope = load_envelope(path)
    if expected_metadata is not None and envelope.authenticated_metadata != expected_metadata:
        raise AnswerKeySealingError("answer-key metadata does not match frozen run bindings")
    aad = _associated_data(envelope.authenticated_metadata)
    if sha256_bytes(aad) != envelope.associated_data_sha256:
        raise AnswerKeySealingError("answer-key associated-data digest is inconsistent")
    return envelope


def verify_envelope_byte_bindings(
    raw: bytes,
    *,
    expected_metadata: SealingMetadata | None = None,
) -> AnswerKeyEnvelope:
    """Validate exact in-memory envelope bytes and public authenticated bindings."""

    envelope = load_envelope_bytes(raw)
    if expected_metadata is not None and envelope.authenticated_metadata != expected_metadata:
        raise AnswerKeySealingError("answer-key metadata does not match frozen run bindings")
    aad = _associated_data(envelope.authenticated_metadata)
    if sha256_bytes(aad) != envelope.associated_data_sha256:
        raise AnswerKeySealingError("answer-key associated-data digest is inconsistent")
    return envelope


def decrypt_answer_key_envelope_bytes(
    encrypted_bytes: bytes,
    *,
    key_path: str | Path,
    decoder_root: str | Path,
    expected_metadata: SealingMetadata | None = None,
) -> bytes:
    """Authenticate/decrypt the same exact envelope bytes later recorded by hash."""

    envelope = verify_envelope_byte_bindings(
        encrypted_bytes,
        expected_metadata=expected_metadata,
    )
    aad = _associated_data(envelope.authenticated_metadata)
    key = _load_key(key_path, decoder_root=decoder_root)
    try:
        nonce = base64.b64decode(envelope.nonce_base64, validate=True)
        ciphertext = base64.b64decode(envelope.ciphertext_base64, validate=True)
        if len(nonce) != 12:
            raise ValueError("AES-GCM nonce must be 12 bytes")
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except (InvalidTag, ValueError) as exc:
        raise AnswerKeySealingError("answer-key authentication failed") from exc


def decrypt_answer_key_bytes(
    encrypted_path: str | Path,
    *,
    key_path: str | Path,
    decoder_root: str | Path,
    expected_metadata: SealingMetadata | None = None,
) -> bytes:
    """Authenticate and decrypt in memory; this function never writes plaintext."""

    try:
        encrypted_bytes = Path(encrypted_path).read_bytes()
    except OSError as exc:
        raise AnswerKeySealingError("invalid encrypted answer-key envelope") from exc
    return decrypt_answer_key_envelope_bytes(
        encrypted_bytes,
        key_path=key_path,
        decoder_root=decoder_root,
        expected_metadata=expected_metadata,
    )


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
