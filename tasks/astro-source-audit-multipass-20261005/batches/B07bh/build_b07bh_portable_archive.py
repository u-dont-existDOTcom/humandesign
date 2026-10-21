#!/usr/bin/env python3
"""Cold-replay portable archival evidence for Lilly's 1647/1659 merchant Friends."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


accept = json.loads((B / "ACCEPTANCE.json").read_text(encoding="utf-8"))
assert accept["new_historical_source_only_annotations"] == 35
assert accept["real_human_blind_validations"] == accept["runtime_promotions"] == 0
dl_result = subprocess.run(
    ["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True, check=False
)
reported = Path(dl_result.stdout.strip()) if dl_result.stdout.strip() else None
french_downloads = Path.home() / "Téléchargements"
destination = (
    reported
    if dl_result.returncode == 0 and reported is not None and reported != Path.home()
    else french_downloads
)
destination.mkdir(parents=True, exist_ok=True)
archive = destination / "Astrology-Lilly-Original-Friends-1647-1659-B07bh-20261021.zip"
sources = [
    "SOURCE_FIRST_AUTHORING_20261021.json",
    "ORIGINAL_SOURCE_WITNESS_20261021.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "PLAN_20261021.md",
    "freeze_b07bh_documentary.py",
    "test_b07bh_original_friends.py",
    "build_b07bh_portable_archive.py",
]
photos = sorted(str(p.relative_to(B)) for p in (B / "evidence").glob("*.jpg"))
assert len(photos) == 5
names = sources + photos
assert all((B / filename).is_file() for filename in names)
manifest = {
    "schema": "LILLY_B07BH_ORIGINAL_FRIENDS_PORTABLE_V1",
    "batch": "B07bh",
    "original_first_1647_and_independent_second_1659_printed_page_photos": True,
    "historical_source_annotations": 35,
    "substantive": 32,
    "next_source_navigation": 3,
    "editorial_ordinal": 185,
    "literal_source_printed_CLXXXIII": True,
    "source_R_range": ["R13237", "R13271"],
    "real_human_blind_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "member_meta": {
        filename: {"sha256": sha(B / filename), "bytes": (B / filename).stat().st_size}
        for filename in names
    },
}
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        z.write(B / name, "B07bh/" + name)
    z.writestr(
        "B07bh/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive, "r") as z, tempfile.TemporaryDirectory() as work:
    assert z.testzip() is None
    z.extractall(work)
    cold = Path(work) / "B07bh"
    assert json.loads((cold / "RELEASE_MANIFEST.json").read_text()) == manifest
    for filename, expected in manifest["member_meta"].items():
        assert sha(cold / filename) == expected["sha256"]
        assert (cold / filename).stat().st_size == expected["bytes"]
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(cold),
            "-p",
            "test_b07bh_original_friends.py",
            "-v",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Ran 18 tests" in result.stderr, result.stderr
receipt = {
    "batch": "B07bh",
    "status": "FIRST_EDITION_1647_AND_1659_PHOTOS_ZIP_CRC_SHA_EXTRACTED_18_TESTS_PASS",
    "archive_path_on_owner_machine": str(archive),
    "archive_filename": archive.name,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(names),
    "zip_CRC_check_passed": True,
    "all_members_exact_SHA_and_bytes_check_passed": True,
    "independent_cold_source_tests_executed": True,
    "independent_cold_source_tests_green": 18,
    "original_1647_or_1659_whole_binary_republished": False,
    "real_human_blind_predictive_validations": 0,
    "runtime_astrological_rule_promotions": 0,
}
(B / "SOURCE_RELEASE_RECEIPT_20261021.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
