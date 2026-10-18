#!/usr/bin/env python3
"""Archive and independently replay 54+38 bounded Chinese source-mechanics tests."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
PROJECT = "tasks/astro-chinese-primary-sources-20261017"
BATCH = PROJECT + "/batches/ChineseAstro-02/"
ZIPNAME = "Astrology-Chinese-ZiWei-QuanShu-Volume2-Original-Source-20261018.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


v2 = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json")
v1 = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
notes = j(B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json")
assert v1["sum_source_annotations"] == 72
assert v2["sum_source_annotations"] == 97
assert notes["count"] == witness["accepted_quote_count"] == 25
assert v2["independently_validated_real_human_claims"] == 0
assert v2["runtime_promotions"] == 0
assert witness["unmatched"] == []
assert all(row["original_revision_quote_match_confirmed"] for row in notes["records"])

files = [
    PROJECT + "/CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    PROJECT + "/CHINESE_SOURCE_AUDIT_INDEX_V2.json",
    PROJECT + "/SOURCE_MANIFEST_V1.json",
    PROJECT + "/RESEARCH_PLAN_20261017.md",
    PROJECT + "/SOURCE_REVIEW_20261017.md",
    PROJECT + "/bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    PROJECT + "/bazi/bazi_source_mechanics.py",
    PROJECT + "/ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    PROJECT + "/ziwei/ziwei_source_mechanics.py",
    PROJECT + "/ziwei/quan_shu_vol2_placements.py",
    PROJECT + "/tests/test_chinese_source_mechanics.py",
    "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md",
] + [
    BATCH + f
    for f in (
        "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
        "SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
        "ORIGINAL_SOURCE_REVIEW_20261018.md",
        "PREVIOUS_CHINESE_STATE_20261018.md",
        "prepare_chinese_source_index_v2.py",
        "verify_pinned_ziwei_source.py",
        "restore_pinned_raw_glyph_anchors.py",
        "test_ziwei_volume2_source.py",
        "build_ziwei_volume2_release.py",
    )
]
assert all((ROOT / n).is_file() for n in files), [n for n in files if not (ROOT / n).is_file()]
manifest = {
    "batch": "ChineseAstro-02",
    "source": "Zi Wei Dou Shu Quan Shu Wikisource volume 2 revision 1963110",
    "short_chinese_original_anchor_matches": 25,
    "original_raw_sha256": notes["raw_source_sha256"],
    "source_only_accepted_ziwei": 51,
    "source_only_accepted_bazi": 46,
    "source_only_chinese_total": 97,
    "complete_chinese_birth_calendar_engine": False,
    "complete_ziwei_14_star_chart_engine": False,
    "independent_human_predictive_validations": 0,
    "runtime_promotions": 0,
    "full_wikisource_text_not_republished": True,
    "members": {
        name: {"sha256": sha(ROOT / name), "bytes": (ROOT / name).stat().st_size} for name in files
    },
}
out = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
home = Path(
    out.stdout.strip()
    if out.returncode == 0 and out.stdout.strip()
    else str(Path.home() / "Téléchargements")
)
home.mkdir(parents=True, exist_ok=True)
archive = home / ZIPNAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in files:
        z.write(ROOT / name, "ChineseAstro-02-root/" + name)
    z.writestr(
        "ChineseAstro-02-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

counts = []
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    extraction = Path(tmp) / "ChineseAstro-02-root"
    assert j(extraction / "RELEASE_MANIFEST.json") == manifest
    for name, details in manifest["members"].items():
        file = extraction / name
        assert sha(file) == details["sha256"] and file.stat().st_size == details["bytes"]
    patterns = [
        (BATCH, "test_ziwei_volume2_source.py", 54),
        (PROJECT + "/tests/", "test_chinese_source_mechanics.py", 38),
    ]
    for rel, pattern, expected in patterns:
        proc = subprocess.run(
            [
                "python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(extraction / rel),
                "-p",
                pattern,
                "-q",
            ],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        match = re.search(r"Ran (\d+) tests", proc.stderr)
        assert match and int(match.group(1)) == expected, proc.stderr
        assert "skipped" not in proc.stderr, proc.stderr
        counts.append(int(match.group(1)))

assert counts == [54, 38]
receipt = {
    "batch": "ChineseAstro-02",
    "status": "PINNED_ORIGINAL_CHINESE_25_ANCHORS_ARCHIVE_92_TESTS_PASS",
    "archive_path": str(archive),
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_members": len(files),
    "crc_passed": True,
    "member_sha256_bytes_verified": True,
    "extracted_archive_replay_passed": True,
    "new_chinese_original_anchor_tests": 54,
    "retained_previous_chinese_tests": 38,
    "total_tests_replayed": sum(counts),
    "witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "notes_sha256": sha(B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"),
    "index_v2_sha256": sha(P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json"),
    "western_lilly_records_untouched": 11325,
    "chinese_historical_records_total": 97,
    "real_human_validation": 0,
    "runtime_promotions": 0,
    "remote_publication_verified": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, ensure_ascii=False, indent=2))
