#!/usr/bin/env python3
"""Portable pinned Chinese original 65-note ZIP; replay 249 source/mechanics tests."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = "tasks/astro-chinese-primary-sources-20261017"
REL = P + "/batches/ChineseAstro-04/"
WEST = "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME = "Astrology-ZiWei-QuanShu-Volume2-LifeBody-65-Historical-Source-B04-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


notes = j(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
previous = B / "recovery" / "CHINESE_V3_BEFORE_04.json"
old = previous if previous.exists() else ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json"
idx = j(old)
assert idx["sum_source_annotations"] == 142
assert idx["systems"][0]["accepted_source_annotations"] == 46
assert idx["systems"][1]["accepted_source_annotations"] == 96
assert idx["systems"][1]["next_id"] == "ZWD-R0097"
assert notes["count"] == witness["original_quote_count"] == 65
assert notes["short_chinese_quote_direct_match_count"] == 65
assert notes["raw_source_sha256"] == witness["original_full_raw_source_sha256"]
assert all(r["original_revision_quote_match_confirmed"] for r in notes["records"])
assert all(not r["runtime_promoted"] for r in notes["records"])
assert j(ROOT / WEST)["records_count"] == 12472
assert witness["runtime_promotions"] == 0
assert witness["independent_actual_human_outcome_validations"] == 0

paths = [
    P + "/CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    P + "/CHINESE_SOURCE_AUDIT_INDEX_V2.json",
    P + "/SOURCE_MANIFEST_V1.json",
    P + "/ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P + "/ziwei/ziwei_source_mechanics.py",
    P + "/ziwei/quan_shu_vol2_placements.py",
    P + "/ziwei/quan_shu_vol2_aux_placements.py",
    P + "/ziwei/quan_shu_vol2_life_body_taxonomy.py",
    P + "/bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P + "/bazi/bazi_source_mechanics.py",
    P + "/batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
    P + "/batches/ChineseAstro-02/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P + "/batches/ChineseAstro-02/test_ziwei_volume2_source.py",
    P + "/batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json",
    P + "/batches/ChineseAstro-03/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P + "/batches/ChineseAstro-03/test_chinese_source_03.py",
    P + "/tests/test_chinese_source_mechanics.py",
] + [
    REL + n
    for n in (
        "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
        "SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
        "ORIGINAL_SOURCE_REVIEW_20261019.md",
        "CONTINUATION_HANDOFF_ACCEPTED_20261019.md",
        "verify_pinned_chinese_04_source.py",
        "test_chinese04_source_and_mechanics.py",
        "build_chinese_04_release.py",
        "prepare_chinese_04_index_v4.py",
    )
]
files = {p: ROOT / p for p in paths}
files[P + "/CHINESE_SOURCE_AUDIT_INDEX_V3.json"] = old
files[WEST] = ROOT / WEST
assert all(f.is_file() for f in files.values()), [
    name for name, f in files.items() if not f.is_file()
]
manifest = {
    "batch": "ChineseAstro-04",
    "source": "Zi Wei Dou Shu Quan Shu transmitted volume II Wikisource oldid1963110",
    "frozen_raw_chinese_source_sha256": notes["raw_source_sha256"],
    "frozen_source_exact_quote_matches": 65,
    "previous_chinese_historical_notes": 142,
    "new_ziwei_source_notes": 65,
    "Chinese_ZiWei_after_if_accepted": 161,
    "Chinese_BaZi_retained": 46,
    "Chinese_total_after_if_accepted": 207,
    "separate_Lilly_index_unmodified": 12472,
    "source_is_genuine_Ming_print_critically_verified": False,
    "modern_birth_calendar_and_full_fourteen_star_parity_verified": False,
    "independent_human_predictive_validations": 0,
    "runtime_model_promotions": 0,
    "members": {
        path: {"sha256": sha(file), "bytes": file.stat().st_size} for path, file in files.items()
    },
}
out = downloads()
out.mkdir(parents=True, exist_ok=True)
archive = out / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path, f in files.items():
        z.write(f, "ChineseAstro-04-root/" + path)
    z.writestr(
        "ChineseAstro-04-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
cases = [
    (REL, "test_chinese04_source_and_mechanics.py", 89),
    (P + "/batches/ChineseAstro-03/", "test_chinese_source_03.py", 68),
    (P + "/batches/ChineseAstro-02/", "test_ziwei_volume2_source.py", 54),
    (P + "/tests/", "test_chinese_source_mechanics.py", 38),
]
replayed = []
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "ChineseAstro-04-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for path, meta in manifest["members"].items():
        f = root / path
        assert f.stat().st_size == meta["bytes"]
        assert sha(f) == meta["sha256"]
    for directory, pattern, expected in cases:
        proc = subprocess.run(
            [
                "python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(root / directory),
                "-p",
                pattern,
                "-q",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        m = re.search(r"Ran (\d+) tests", proc.stderr)
        assert m and int(m.group(1)) == expected, proc.stderr
        assert "skipped" not in proc.stderr
        replayed.append(expected)
assert sum(replayed) == 249
receipt = {
    "batch": "ChineseAstro-04",
    "status": "ORIGINAL_PINNED_65_ZIWEI_QUOTES_249_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "crc_passed": True,
    "member_SHA256_and_bytes_passed": True,
    "independent_ZIP_extract_passed": True,
    "source_mechanics_new_tests": 89,
    "previous_ChineseAstro03_tests": 68,
    "previous_ChineseAstro02_tests": 54,
    "retained_prior_chinese_mechanics_tests": 38,
    "total_replayed_tests": 249,
    "new_65_source_notes_SHA256": sha(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"),
    "original_revision_source_witness_SHA256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "old_Chinese_V3_index_SHA256": sha(old),
    "unchanged_Western_Lilly_count": 12472,
    "independent_real_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
