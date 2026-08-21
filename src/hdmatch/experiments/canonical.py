"""Canonical serialization and exact-byte hashing primitives.

Canonical JSON is deliberately small and explicit: UTF-8, lexicographically sorted
object keys, no insignificant whitespace, finite numbers only, and no trailing newline.
File hashes always cover the bytes on disk rather than a parsed/re-serialized form.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
from dataclasses import asdict, is_dataclass
from datetime import UTC, date, datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def _json_default(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="python")
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("naive datetimes are not canonical")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


def _reject_non_finite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite floats are not canonical JSON")
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("canonical JSON object keys must be strings")
        for item in value.values():
            _reject_non_finite(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_non_finite(item)
    elif isinstance(value, (set, frozenset)):
        raise TypeError("unordered sets are not canonical JSON")


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize *value* to the project's deterministic JSON byte representation."""

    _reject_non_finite(value)
    rendered = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=_json_default,
    )
    return rendered.encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Hash the exact bytes stored at *path*."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def write_new_bytes(path: str | Path, data: bytes, *, mode: int = 0o644) -> Path:
    """Atomically create *path* and refuse to replace an existing artifact."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"immutable artifact already exists: {destination}")
    descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            raise FileExistsError(f"immutable artifact already exists: {destination}") from None
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def write_new_canonical_json(path: str | Path, value: Any, *, mode: int = 0o644) -> Path:
    return write_new_bytes(path, canonical_json_bytes(value), mode=mode)


def load_json_bytes(path: str | Path, *, require_canonical: bool = False) -> Any:
    raw = Path(path).read_bytes()
    value = json.loads(raw)
    if require_canonical and canonical_json_bytes(value) != raw:
        raise ValueError(f"JSON artifact is not canonically encoded: {path}")
    return value
