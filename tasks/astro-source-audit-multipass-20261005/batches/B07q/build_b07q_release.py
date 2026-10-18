#!/usr/bin/env python3
"""Preserve CLX, frozen parent index, photos and 71 tests in independently replayed ZIP."""

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
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
REL = TASK + "/batches/B07q/"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


accepted = load(B / "ACCEPTANCE.json")
rules = load(B / "RULES.json")
source_window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert accepted["new_historical_annotations"] == rules["record_count"] == 258
assert accepted["substantive"] == 256 and accepted["next_navigation"] == 2
assert accepted["rules_sha256"] == sha(B / "RULES.json")
assert not rules["empirical_validations"] and not rules["runtime_promotions"]
pre_index = B / "recovery" / "INDEX_BEFORE_B07q.json"
index_source = pre_index if pre_index.exists() else ROOT / INDEX
assert sha(index_source) == source_window["accepted_index_sha256"]
assert load(index_source)["records_count"] == 11067
assert load(ROOT / CHINA)["sum_source_annotations"] == 72

out = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
home = Path(
    out.stdout.strip()
    if out.returncode == 0 and out.stdout.strip()
    else str(Path.home() / "Téléchargements")
)
home.mkdir(parents=True, exist_ok=True)
archive = home / "Astrology-Lilly-Printed-CLX-Midheaven-Directions-1647-20261018.zip"
names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "PRELIMINARY_WINDOW_VERIFICATION_20261018.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_PART_01_SATURN_JUPITER_20261018.json",
    "SOURCE_PART_02_MARS_SUN_20261018.json",
    "SOURCE_PART_03_VENUS_MERCURY_20261018.json",
    "SOURCE_PART_04_MOON_HOUSE_CUSPS_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "CLX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "PLAN_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b07q_documentary.py",
    "repair_b07q_boundary.py",
    "test_b07q_documentary.py",
    "test_b07q_source_window.py",
    "prepare_original_b07q_source_window.py",
    "build_b07q_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(702, 721)]

files = {REL + name: B / name for name in names}
files[INDEX] = index_source
files[CHINA] = ROOT / CHINA
manifest = {
    "batch": "B07q",
    "source": "William Lilly 1647 first edition / Wellcome b30338724",
    "historical_source_annotations": 258,
    "substantive": 256,
    "next_navigation": 2,
    "original_clx_body": list(range(702, 712)),
    "following_original_context": list(range(712, 721)),
    "source_groups": 27,
    "independent_real_human_prediction_validations": 0,
    "runtime_promotions": 0,
    "complete_diplomatic_transcription": False,
    "original_direction_angle_to_date_engine_verified": False,
    "preserved_pre_acceptance_index": True,
    "members": {rel: {"sha256": sha(f), "bytes": f.stat().st_size} for rel, f in files.items()},
}
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for rel, file in files.items():
        z.write(file, "B07q-root/" + rel)
    z.writestr(
        "B07q-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    site = Path(tmp) / "B07q-root"
    extracted = site / REL
    assert load(site / "RELEASE_MANIFEST.json") == manifest
    for rel, w in manifest["members"].items():
        assert sha(site / rel) == w["sha256"]
        assert (site / rel).stat().st_size == w["bytes"]
    counts = []
    for pattern in ("test_b07q_documentary.py", "test_b07q_source_window.py"):
        proc = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", str(extracted), "-p", pattern, "-q"],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        match = re.search(r"Ran (\d+) tests", proc.stderr)
        assert match, proc.stderr
        counts.append(int(match.group(1)))
    assert counts == [62, 9], counts

receipt = {
    "batch": "B07q",
    "status": "DOCUMENTARY_ARCHIVE_EXTRACTED_CRC_SHA_71_TESTS_PASS",
    "archive_path": str(archive),
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "members": len(files),
    "crc_passed": True,
    "sha256_passed": True,
    "extraction_passed": True,
    "replayed_documentary_tests": 62,
    "replayed_source_window_tests": 9,
    "independent_archive_replay_total": 71,
    "rules_sha256": sha(B / "RULES.json"),
    "historical_records_if_accepted": 258,
    "pre_acceptance_index_sha256": sha(index_source),
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
