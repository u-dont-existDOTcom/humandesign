from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    EphemerisFilePin,
    EphemerisFileVerificationError,
    EphemerisManifestError,
    load_ephemeris_source_manifest,
    verify_ephemeris_directory,
)
from hdmatch.util import sha256_file
from scripts import fetch_swisseph_ephemeris

ROOT = Path(__file__).resolve().parents[2]


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_source_manifest(path: Path, files: dict[str, bytes]) -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": "ephemeris-file-manifest-v1",
                "provider": "Swiss Ephemeris",
                "upstream_repository": PINNED_UPSTREAM_REPOSITORY,
                "upstream_commit": PINNED_UPSTREAM_COMMIT,
                "files": [
                    {
                        "name": name,
                        "bytes": len(payload),
                        "sha256": _digest(payload),
                    }
                    for name, payload in files.items()
                ],
                "tested_range": "test-only",
                "license": "test-only",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_committed_source_manifest_is_strictly_pinned() -> None:
    manifest = load_ephemeris_source_manifest(ROOT / "data/ephemeris/manifest.json")

    assert manifest.upstream_repository == PINNED_UPSTREAM_REPOSITORY
    assert manifest.upstream_commit == PINNED_UPSTREAM_COMMIT
    assert {record.name: (record.bytes, record.sha256) for record in manifest.files} == {
        "sepl_18.se1": (
            484061,
            "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
        ),
        "semo_18.se1": (
            1304771,
            "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
        ),
    }


def test_source_manifest_rejects_a_changed_upstream_commit(tmp_path: Path) -> None:
    source = json.loads((ROOT / "data/ephemeris/manifest.json").read_text(encoding="utf-8"))
    source["upstream_commit"] = "0" * 40
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(EphemerisManifestError, match="invalid pinned"):
        load_ephemeris_source_manifest(path)


def test_verifier_returns_deterministic_path_free_binding(tmp_path: Path) -> None:
    files = {
        "sepl_18.se1": b"test planetary ephemeris",
        "semo_18.se1": b"test lunar ephemeris",
    }
    source_manifest = tmp_path / "source-manifest.json"
    ephemeris_dir = tmp_path / "ephemeris"
    ephemeris_dir.mkdir()
    _write_source_manifest(source_manifest, files)
    for name, payload in files.items():
        (ephemeris_dir / name).write_bytes(payload)

    first = verify_ephemeris_directory(
        source_manifest_path=source_manifest,
        ephemeris_directory=ephemeris_dir,
    )
    second = verify_ephemeris_directory(
        source_manifest_path=source_manifest,
        ephemeris_directory=ephemeris_dir,
    )

    assert first == second
    assert first.verification_status == "pass"
    assert first.source_manifest_sha256 == sha256_file(source_manifest)
    assert first.source_commit == PINNED_UPSTREAM_COMMIT
    binding = first.manifest_binding()
    assert "path" not in json.dumps(binding)
    assert binding["ephemeris_file_set_sha256"] == first.ephemeris_file_set_sha256


def test_verifier_rejects_hash_mismatch_and_unlisted_files(tmp_path: Path) -> None:
    files = {
        "sepl_18.se1": b"test planetary ephemeris",
        "semo_18.se1": b"test lunar ephemeris",
    }
    source_manifest = tmp_path / "source-manifest.json"
    ephemeris_dir = tmp_path / "ephemeris"
    ephemeris_dir.mkdir()
    _write_source_manifest(source_manifest, files)
    for name, payload in files.items():
        (ephemeris_dir / name).write_bytes(payload)

    (ephemeris_dir / "semo_18.se1").write_bytes(b"same byte count bad")
    with pytest.raises(EphemerisFileVerificationError, match="byte-size mismatch"):
        verify_ephemeris_directory(
            source_manifest_path=source_manifest,
            ephemeris_directory=ephemeris_dir,
        )

    (ephemeris_dir / "semo_18.se1").write_bytes(files["semo_18.se1"])
    (ephemeris_dir / "unexpected.se1").write_bytes(b"unexpected")
    with pytest.raises(EphemerisFileVerificationError, match="unlisted"):
        verify_ephemeris_directory(
            source_manifest_path=source_manifest,
            ephemeris_directory=ephemeris_dir,
        )


def test_fetch_payload_must_match_pin_before_install(tmp_path: Path) -> None:
    destination = tmp_path / "sepl_18.se1"
    destination.write_bytes(b"existing verified bytes")
    pin = EphemerisFilePin(
        name="sepl_18.se1",
        bytes=len(b"expected bytes"),
        sha256=_digest(b"expected bytes"),
    )

    with pytest.raises(EphemerisFileVerificationError, match="SHA-256 mismatch"):
        fetch_swisseph_ephemeris._verify_payload(
            "sepl_18.se1",
            b"tampered bytes",
            pin,
        )

    assert destination.read_bytes() == b"existing verified bytes"


def test_verify_only_writes_a_deterministic_local_receipt(tmp_path: Path) -> None:
    files = {
        "sepl_18.se1": b"test planetary ephemeris",
        "semo_18.se1": b"test lunar ephemeris",
    }
    source_manifest = tmp_path / "source-manifest.json"
    ephemeris_dir = tmp_path / "ephemeris"
    ephemeris_dir.mkdir()
    _write_source_manifest(source_manifest, files)
    for name, payload in files.items():
        (ephemeris_dir / name).write_bytes(payload)

    arguments = [
        "--output-dir",
        str(ephemeris_dir),
        "--source-manifest",
        str(source_manifest),
        "--verify-only",
    ]
    assert fetch_swisseph_ephemeris.main(arguments) == 0
    receipt = ephemeris_dir / "swisseph_ephemeris_manifest.json"
    first_bytes = receipt.read_bytes()
    assert fetch_swisseph_ephemeris.main(arguments) == 0

    assert receipt.read_bytes() == first_bytes
    payload = json.loads(first_bytes)
    assert payload["verification_status"] == "pass"
    assert payload["source_commit"] == PINNED_UPSTREAM_COMMIT
