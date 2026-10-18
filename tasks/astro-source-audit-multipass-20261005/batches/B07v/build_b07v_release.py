#!/usr/bin/env python3
"""Portable first-edition unnumbered Moon-star source ZIP and independent CRC/hash replay."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07v/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
FILENAME = "Astrology-Lilly-Unnumbered-Moon-Fixed-Stars-1647-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
acc = load(B / "ACCEPTANCE.json")
previous = B / "recovery" / "INDEX_BEFORE_B07v.json"
old_index = previous if previous.exists() else ROOT / INDEX
assert sha(old_index) == window["prior_canonical_index_sha256"]
assert load(old_index)["records_count"] == 12168
assert rules["record_count"] == acc["new_historical_annotations"] == 100
assert acc["numbered_chapters_added"] == 0
assert rules["substantive"] == 98 and rules["following_navigation"] == 2
assert load(ROOT / CHINA)["sum_source_annotations"] == 97
assert rules["empirical_human_validations"] == rules["runtime_promotions"] == 0
assert sha(B / "RULES.json") == acc["rules_sha256"]

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "SOURCE_PART_01_MOON_STARS_RIGEL_ORION_20261018.json",
    "SOURCE_PART_02_MOON_STARS_SERPENT_HERCULES_20261018.json",
    "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "prepare_original_b07v_window.py",
    "freeze_b07v_documentary.py",
    "test_b07v_documentary.py",
    "prepare_canonical_b07v.py",
    "build_b07v_release.py",
] + [f"evidence/pdf_1647-{i}.jpg" for i in range(735, 739)]
files = {REL + name: B / name for name in names}
files[INDEX] = old_index
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values())
manifest = {
    "batch": "B07v",
    "source": "William Lilly 1647 first-edition Christian Astrology Wellcome b30338724",
    "original_full_pdf_sha256": window["original_full_pdf_sha256"],
    "printed_chapter_number": None,
    "source_is_unnumbered": True,
    "historical_records": 100,
    "substantive": 98,
    "following_navigation": 2,
    "original_photo_source_groups": 15,
    "historic_lunar_star_positions": 13,
    "source_photo_frames": [735, 736, 737, 738],
    "next_numbered_chapter": "CLXV",
    "next_heading_original_pdf": 737,
    "parent_index_records": 12168,
    "separate_chinese_source_count": 97,
    "independent_human_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "full_original_pdf_not_reproduced": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path, file in files.items():
        z.write(file, "B07v-root/" + path)
    z.writestr(
        "B07v-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07v-root"
    assert load(root / "RELEASE_MANIFEST.json") == manifest
    for path, info in manifest["members"].items():
        file = root / path
        assert file.stat().st_size == info["bytes"] and sha(file) == info["sha256"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07v_documentary.py",
            "-q",
        ],
        text=True,
        capture_output=True,
        timeout=50,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 53, p.stderr
    assert "skipped" not in p.stderr
receipt = {
    "batch": "B07v",
    "status": "UNNUMBERED_MOON_STAR_ORIGINAL_SOURCE_53_ZIP_REPLAYS_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "total_replayed_tests": 53,
    "rules_sha256": sha(B / "RULES.json"),
    "star_table_sha256": sha(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json"),
    "prior_index_sha256": sha(old_index),
    "historical_records_if_accepted": 100,
    "numbered_chapters_delta": 0,
    "independent_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
