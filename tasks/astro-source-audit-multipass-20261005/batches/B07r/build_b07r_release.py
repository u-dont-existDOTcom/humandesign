#!/usr/bin/env python3
"""Independently CRC/SHA and unit-replay original CLXI source ZIP release."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX_PATH = (
    ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


win = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = j(B / "RULES.json")
acc = j(B / "ACCEPTANCE.json")
pre = B / "recovery" / "INDEX_BEFORE_B07r.json"
pre_index = pre if pre.exists() else INDEX_PATH
assert sha(pre_index) == win["prior_index_sha256"]
assert j(pre_index)["records_count"] == 11325
assert j(CHINA)["sum_source_annotations"] == 97
assert rules["record_count"] == acc["new_historical_annotations"] == 90
assert acc["rules_sha256"] == sha(B / "RULES.json")
assert acc["table_sha256"] == sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json")
assert rules["runtime_promotions"] == rules["empirical_human_validations"] == 0
names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "SOURCE_PART_01_FIRST_STARS_20261018.json",
    "SOURCE_PART_02_LAST_STARS_SEAM_20261018.json",
    "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "HIGH_STAKES_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "prepare_original_b07r_source_window.py",
    "freeze_b07r_documentary.py",
    "test_b07r_documentary.py",
    "prepare_canonical_b07r.py",
    "build_b07r_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(711, 715)]
members = {"B07r/" + name: B / name for name in names}
members["prior/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"] = pre_index
members["prior/CHINESE_SOURCE_AUDIT_INDEX_V2.json"] = CHINA
assert all(p.is_file() for p in members.values())
manifest = {
    "batch": "B07r",
    "original": "William Lilly Christian Astrology 1647 Wellcome b30338724",
    "printed_chapter": "CLXI",
    "new_historical_documentary_notes": 90,
    "substantive_notes": 88,
    "next_chapter_navigation_notes": 2,
    "source_groups": 12,
    "period_star_designations": 14,
    "accepted_lilly_before_this_archive": 11325,
    "ptolemy_unchanged": 1066,
    "chinese_v2_unchanged": 97,
    "original_1647_source_pdf_sha256": win["original_full_pdf_sha256"],
    "source_epochs_modern_star_parity_verified": False,
    "independent_human_predictive_validations": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in members.items()},
}
out = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
home = Path(
    out.stdout.strip()
    if out.returncode == 0 and out.stdout.strip()
    else str(Path.home() / "Téléchargements")
)
home.mkdir(parents=True, exist_ok=True)
archive = home / "Astrology-Lilly-Printed-CLXI-Midheaven-Fixed-Stars-1647-20261018.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in members.items():
        z.write(file, "B07r-root/" + name)
    z.writestr(
        "B07r-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07r-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, details in manifest["members"].items():
        f = root / name
        assert sha(f) == details["sha256"] and f.stat().st_size == details["bytes"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / "B07r"),
            "-p",
            "test_b07r_documentary.py",
            "-q",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    match = re.search(r"Ran (\d+) tests", proc.stderr)
    assert match and int(match.group(1)) == 50, proc.stderr
    assert "skipped" not in proc.stderr, proc.stderr
receipt = {
    "batch": "B07r",
    "status": "ORIGINAL_CLXI_DOCUMENTARY_ZIP_CRC_SHA_50_TESTS_PASS",
    "archive_path": str(archive),
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "members": len(members),
    "crc_passed": True,
    "member_hashes_verified": True,
    "independent_extract_replay": True,
    "portable_test_replay": 50,
    "rules_sha256": sha(B / "RULES.json"),
    "table_sha256": sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json"),
    "prior_canonical_index_sha256": sha(pre_index),
    "new_historical_source_notes_if_accepted": 90,
    "empirical_human_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
