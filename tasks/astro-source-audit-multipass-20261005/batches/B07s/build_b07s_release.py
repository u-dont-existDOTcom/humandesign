#!/usr/bin/env python3
"""Archive, CRC/member-SHA verify and replay the original 1647 CLXII source packet."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = "tasks/astro-source-audit-multipass-20261005"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
INDEX = P + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
REL = P + "/batches/B07s/"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


w = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
prior = B / "recovery" / "INDEX_BEFORE_B07s.json"
prior_index = prior if prior.exists() else ROOT / INDEX
assert sha(prior_index) == w["prior_index_sha256"]
assert j(prior_index)["records_count"] == 11415
assert rules["record_count"] == accept["new_historical_annotations"] == 306
assert rules["substantive"] == 304 and rules["following_navigation"] == 2
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert rules["empirical_human_validations"] == 0
assert rules["runtime_promotions"] == 0
assert j(ROOT / CHINA)["sum_source_annotations"] == 97

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "PLAN_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "SOURCE_PART_01_SATURN_JUPITER_20261018.json",
    "SOURCE_PART_02_JUPITER_MARS_20261018.json",
    "SOURCE_PART_03_VENUS_MERCURY_20261018.json",
    "SOURCE_PART_04_MOON_NODES_20261018.json",
    "SOURCE_PART_05_HOUSES_SEAM_20261018.json",
    "PRE_FREEZE_ROLE_REPAIR_RECEIPT_V1.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SUN_DIRECTION_HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b07s_documentary.py",
    "repair_b07s_roles_before_freeze.py",
    "prepare_original_b07s_source_window.py",
    "prepare_canonical_b07s.py",
    "build_b07s_release.py",
    "test_b07s_source_window.py",
    "test_b07s_documentary.py",
] + [f"evidence/pdf_1647-{i}.jpg" for i in range(713, 726)]
files = {REL + name: B / name for name in names}
files[INDEX] = prior_index
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values())
manifest = {
    "batch": "B07s",
    "source": "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724",
    "original_pdf_sha256": w["original_pdf_sha256"],
    "original_pdf_bytes": w["original_pdf_bytes"],
    "historical_documentary_source_annotations": 306,
    "substantive_source_annotations": 304,
    "next_chapter_navigation_annotations": 2,
    "source_groups": 40,
    "source_image_frames": 13,
    "body_pdf_frames": list(range(713, 724)),
    "original_public_domain_pdf_not_embedded": True,
    "prior_lilly_index_snapshot_embedded": True,
    "chinese_source_index_unchanged": 97,
    "hyleg_anareta_primary_directions_math_parity_verified": False,
    "independent_human_forecasts_validated": 0,
    "runtime_models_promoted": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
out = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
downloads = Path(
    out.stdout.strip()
    if out.returncode == 0 and out.stdout.strip()
    else str(Path.home() / "Téléchargements")
)
downloads.mkdir(parents=True, exist_ok=True)
archive = downloads / "Astrology-Lilly-Printed-CLXII-Sun-Directions-1647-20261018.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path, file in files.items():
        z.write(file, "B07s-root/" + path)
    z.writestr(
        "B07s-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
replayed = []
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    restored = Path(tmp) / "B07s-root"
    assert j(restored / "RELEASE_MANIFEST.json") == manifest
    for path, spec in manifest["members"].items():
        file = restored / path
        assert sha(file) == spec["sha256"]
        assert file.stat().st_size == spec["bytes"]
    for test_name, count in (
        ("test_b07s_documentary.py", 81),
        ("test_b07s_source_window.py", 24),
    ):
        proc = subprocess.run(
            [
                "python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(restored / REL),
                "-p",
                test_name,
                "-q",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        result = re.search(r"Ran (\d+) tests", proc.stderr)
        assert result and int(result.group(1)) == count, proc.stderr
        assert "skipped" not in proc.stderr, proc.stderr
        replayed.append(count)
assert replayed == [81, 24]
receipt = {
    "batch": "B07s",
    "status": "ORIGINAL_CLXII_SOURCE_ZIP_SHA_CRC_105_TESTS_REPLAYED",
    "archive_path": str(archive),
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "member_hashes_verified": True,
    "independent_extract_replay": True,
    "replayed_documentary_tests": 81,
    "replayed_source_window_tests": 24,
    "portable_test_replay": 105,
    "rules_sha256": sha(B / "RULES.json"),
    "prior_canonical_index_sha256": sha(prior_index),
    "new_source_records_if_accepted": 306,
    "empirical_human_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
