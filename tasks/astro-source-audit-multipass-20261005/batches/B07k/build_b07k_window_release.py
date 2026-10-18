#!/usr/bin/env python3
"""Portable original 1647 CLVI+directions photographic source-boundary packet only."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


download = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
folder = (
    Path(download.stdout.strip())
    if download.returncode == 0 and download.stdout.strip()
    else Path.home() / "Téléchargements"
)
folder.mkdir(parents=True, exist_ok=True)
archive = folder / "Astrology-Lilly-CLVI-Death-Original-Window-and-Directions-20261018.zip"
names = [
    "ORIGINAL_CLVI_WINDOW_AND_LIMITS_20261018.json",
    "ORIGINAL_SOURCE_WINDOW_WITNESS.json",
    "ORIGINAL_DIRECTIONS_WINDOW_20261018.json",
    "ORIGINAL_CLVI_AND_DIRECTIONS_BOUNDARY_REVIEW_20261018.md",
    "test_b07k_source_window.py",
    "build_b07k_window_release.py",
] + [f"evidence/pdf_1647-{i}.jpg" for i in range(678, 691)]
assert all((B / n).exists() for n in names)
manifest = {
    "batch": "B07k",
    "source": "Original William Lilly 1647, Wellcome b30338724",
    "status": "PHOTO_SOURCE_WINDOW_PROVISIONAL_NOT_HISTORIC_RULE_ACCEPTANCE",
    "death_chapter": "CLVI",
    "death_body_original_frames": list(range(678, 685)),
    "following_directions_unnumbered_from_frame": 685,
    "following_numbered_CLVII_frame": 688,
    "following_numbered_CLVIII_frame": 690,
    "new_historical_rules_accepted": 0,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {n: {"sha256": sha(B / n), "bytes": (B / n).stat().st_size} for n in names},
}
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipout:
    for n in names:
        zipout.write(B / n, "B07k/" + n)
    zipout.writestr(
        "B07k/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as zin, tempfile.TemporaryDirectory() as tmp:
    assert zin.testzip() is None
    zin.extractall(tmp)
    directory = Path(tmp) / "B07k"
    assert json.loads((directory / "RELEASE_MANIFEST.json").read_text()) == manifest
    for name, info in manifest["members"].items():
        assert sha(directory / name) == info["sha256"]
        assert (directory / name).stat().st_size == info["bytes"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(directory),
            "-p",
            "test_b07k_source_window.py",
            "-q",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0 and "Ran 10 tests" in proc.stderr, proc.stderr
receipt = {
    "batch": "B07k",
    "status": "PROVISIONAL_ORIGINAL_SOURCE_IMAGES_SHA_CRC_ZIP_REPLAY_10_TESTS_PASS",
    "archive_path": str(archive),
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "members": len(names),
    "member_CRC_SHA_bytes_ok": True,
    "extracted_test_replay_count": 10,
    "source_records_admitted": 0,
    "canonical_index_not_modified": True,
    "empirical_human_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_WINDOW_RELEASE_RECEIPT_20261018.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
