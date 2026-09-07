#!/usr/bin/env python3
"""Regenerate the frozen Life Patterns human-calibration handoff from exact recovered sources.

This is a transport/recovery helper only. It does not run a model, create annotations,
change the frozen sampling, or authorize later coding. The input archive must contain both
exact v8/v8.1 source byte sequences previously verified by the public recovery receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

V8_BYTES = 54_488
V8_SHA256 = "3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637"
V8_1_BYTES = 25_844
V8_1_SHA256 = "93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7"
ORIGINAL_PREPARATION_SOURCE_COMMIT = "5a278d135af4de5190d9b74d8e55489dc92efaf1"
ORIGINAL_PREPARED_AT_UTC = "2026-09-06T22:10:58.534703Z"
EXPECTED_PACKAGE_ID = "LPKG-18170B8D3EEC8423A523"
EXPECTED_PACKAGE_SHA256 = "18170b8d3eec8423a523cc2151020a2e2dfead8abf3a9ea5b941fdc9194dd66f"
EXPECTED_CALIBRATION_ID = "LPCA-5B3E6CFCCE49807050DF"
EXPECTED_CALIBRATION_SHA256 = "5b3e6cfcce49807050df03f8ab27cbfbb610869dcb9cfa30064cd485d4646140"
EXPECTED_EPISODE_UNITS = 44
EXPECTED_SERIES_UNITS = 22
EXPECTED_HANDOFF_FILE_COUNT = 15
SAFE_HANDOFF_RECEIPT = Path(
    "state/life-patterns-development-preparation-2026-09-06/"
    "human_handoff_public_safe_receipt.json"
)


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _find_exact_sources(source_archive: Path, extraction_root: Path) -> tuple[Path, Path]:
    with zipfile.ZipFile(source_archive) as archive:
        members = [info for info in archive.infolist() if not info.is_dir()]
        if not members:
            raise ValueError("recovery archive contains no files")
        archive.extractall(extraction_root)

    by_digest: dict[str, Path] = {}
    for path in extraction_root.rglob("*"):
        if not path.is_file():
            continue
        raw = path.read_bytes()
        digest = _sha256(raw)
        if digest in {V8_SHA256, V8_1_SHA256}:
            if digest in by_digest:
                raise ValueError(f"recovery archive repeats exact source digest {digest}")
            by_digest[digest] = path

    if set(by_digest) != {V8_SHA256, V8_1_SHA256}:
        missing = sorted({V8_SHA256, V8_1_SHA256} - set(by_digest))
        raise ValueError("recovery archive is missing exact frozen source bytes: " + ", ".join(missing))
    if by_digest[V8_SHA256].stat().st_size != V8_BYTES:
        raise ValueError("v8 exact source byte count disagrees with recovery receipt")
    if by_digest[V8_1_SHA256].stat().st_size != V8_1_BYTES:
        raise ValueError("v8.1 exact source byte count disagrees with recovery receipt")
    return by_digest[V8_SHA256], by_digest[V8_1_SHA256]


def _run(command: list[str], *, cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}\n{detail}")


def _verify_prepared(prepared_dir: Path) -> None:
    package = _load_json(prepared_dir / "development_coding_package_public_safe.json")
    if package.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError("regenerated package ID does not match frozen package")
    if package.get("package_sha256") != EXPECTED_PACKAGE_SHA256:
        raise ValueError("regenerated package hash does not match frozen package")
    payload = package.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("regenerated package payload is invalid")
    expected = {
        "calibration_manifest_id": EXPECTED_CALIBRATION_ID,
        "calibration_manifest_sha256": EXPECTED_CALIBRATION_SHA256,
        "calibration_episode_unit_count": EXPECTED_EPISODE_UNITS,
        "calibration_series_unit_count": EXPECTED_SERIES_UNITS,
        "target_model_scoring_authorized": False,
        "development_only": True,
        "validation_use_forbidden": True,
    }
    mismatches = {key: (payload.get(key), value) for key, value in expected.items() if payload.get(key) != value}
    if mismatches:
        raise ValueError(f"regenerated package differs from frozen preparation: {mismatches}")


def _verify_handoff(handoff_dir: Path, repo_root: Path) -> dict[str, Any]:
    expected_receipt = _load_json(repo_root / SAFE_HANDOFF_RECEIPT)
    actual_receipt = _load_json(handoff_dir / "human_handoff_public_safe_receipt.json")
    if actual_receipt != expected_receipt:
        raise ValueError("regenerated human handoff receipt is not byte/content-equivalent to frozen receipt")

    payload = expected_receipt.get("payload")
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), dict):
        raise ValueError("committed human handoff receipt is malformed")
    expected_files = payload["files"]
    actual_files = sorted(path for path in handoff_dir.rglob("*") if path.is_file())
    relative_actual = {path.relative_to(handoff_dir).as_posix(): path for path in actual_files}
    if set(relative_actual) != set(expected_files):
        missing = sorted(set(expected_files) - set(relative_actual))
        extra = sorted(set(relative_actual) - set(expected_files))
        raise ValueError(f"regenerated handoff file set differs; missing={missing}; extra={extra}")
    if len(relative_actual) != EXPECTED_HANDOFF_FILE_COUNT:
        raise ValueError("regenerated human handoff does not contain exactly 15 frozen files")

    mismatched_hashes = {
        name: (_sha256(relative_actual[name].read_bytes()), expected_digest)
        for name, expected_digest in expected_files.items()
        if _sha256(relative_actual[name].read_bytes()) != expected_digest
    }
    if mismatched_hashes:
        raise ValueError(f"regenerated handoff contains changed frozen bytes: {mismatched_hashes}")
    if payload.get("episode_unit_count") != EXPECTED_EPISODE_UNITS:
        raise ValueError("human handoff episode unit count changed")
    if payload.get("series_unit_count") != EXPECTED_SERIES_UNITS:
        raise ValueError("human handoff series unit count changed")
    if payload.get("readiness") != "awaiting_human":
        raise ValueError("human handoff is not in the frozen awaiting-human state")
    if payload.get("response_templates_are_annotations") is not False:
        raise ValueError("blank response templates were incorrectly promoted to annotations")
    return expected_receipt


def _write_deterministic_zip(source_dir: Path, output_zip: Path) -> tuple[str, int, int]:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists() or output_zip.is_symlink():
        raise FileExistsError(f"output archive already exists: {output_zip}")
    paths = sorted(path for path in source_dir.rglob("*") if path.is_file())
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in paths:
            relative = path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100400 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    raw = output_zip.read_bytes()
    return _sha256(raw), len(raw), len(paths)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--output-zip", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    source_archive = args.source_archive.resolve()
    output_zip = args.output_zip.resolve()
    if not source_archive.is_file():
        parser.error(f"source archive does not exist: {source_archive}")
    if not (repo_root / SAFE_HANDOFF_RECEIPT).is_file():
        parser.error("repo root does not contain the frozen human-handoff receipt")

    with tempfile.TemporaryDirectory(prefix="life-patterns-recovery-") as temporary:
        temp = Path(temporary)
        v8, v8_1 = _find_exact_sources(source_archive, temp / "source")
        private_root = temp / "private"
        prepared = private_root / "prepared"
        handoff = private_root / "human-handoff"
        private_root.mkdir()

        _run(
            [
                sys.executable,
                str(repo_root / "scripts/prepare_life_patterns_development_package.py"),
                "--v8-record",
                str(v8),
                "--v8-1-supplement",
                str(v8_1),
                "--output-dir",
                str(prepared),
                "--repo-root",
                str(repo_root),
                "--source-commit",
                ORIGINAL_PREPARATION_SOURCE_COMMIT,
                "--created-at-utc",
                ORIGINAL_PREPARED_AT_UTC,
                "--render-blind-packets",
            ],
            cwd=repo_root,
        )
        _verify_prepared(prepared)
        _run(
            [
                sys.executable,
                str(repo_root / "scripts/export_life_patterns_human_calibration_bundle.py"),
                "--prepared-dir",
                str(prepared),
                "--output-dir",
                str(handoff),
            ],
            cwd=repo_root,
        )
        receipt = _verify_handoff(handoff, repo_root)
        archive_sha256, archive_bytes, archive_members = _write_deterministic_zip(handoff, output_zip)

    result = {
        "schema_version": "life-patterns-regenerated-human-handoff-transfer-v1",
        "status": "verified_frozen_handoff_regenerated",
        "source_archive_sha256": _sha256(source_archive.read_bytes()),
        "source_identities": {
            "v8_sha256": V8_SHA256,
            "v8_1_sha256": V8_1_SHA256,
        },
        "frozen_package_id": EXPECTED_PACKAGE_ID,
        "frozen_package_sha256": EXPECTED_PACKAGE_SHA256,
        "calibration_manifest_id": EXPECTED_CALIBRATION_ID,
        "calibration_manifest_sha256": EXPECTED_CALIBRATION_SHA256,
        "human_handoff_receipt_id": receipt.get("receipt_id"),
        "human_handoff_receipt_sha256": receipt.get("receipt_sha256"),
        "episode_units": EXPECTED_EPISODE_UNITS,
        "series_units": EXPECTED_SERIES_UNITS,
        "handoff_internal_files_match_committed_hashes": True,
        "blank_forms_are_annotations": False,
        "human_first_pass_received": False,
        "automated_coding_run": False,
        "development_only": True,
        "validation_use_forbidden": True,
        "output_zip": str(output_zip),
        "output_zip_sha256": archive_sha256,
        "output_zip_bytes": archive_bytes,
        "output_zip_members": archive_members,
        "outer_zip_is_new_transport_container": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
