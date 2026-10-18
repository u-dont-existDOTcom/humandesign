#!/usr/bin/env python3
"""Portable source-only ChineseAstro-03 ZIP: 160 independent extracted tests."""

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
REL = P + "/batches/ChineseAstro-03/"
WESTERN = "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
FILENAME = "Astrology-Chinese-ZiWei-QuanShu-Volume2-Auxiliary-45-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


note = j(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
previous = B / "recovery" / "CHINESE_V2_BEFORE_03.json"
old_index = previous if previous.exists() else ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json"
old = j(old_index)
assert old["sum_source_annotations"] == 97
assert old["systems"][0]["accepted_source_annotations"] == 46
assert old["systems"][1]["accepted_source_annotations"] == 51
assert old["systems"][1]["next_id"] == "ZWD-R0052"
assert len(note["records"]) == note["count"] == 45
assert witness["short_exact_chinese_anchor_matches"] == 45
assert note["raw_source_sha256"] == witness["raw_source_sha256"]
assert j(ROOT / WESTERN)["records_count"] == 12472
assert all(r["original_revision_quote_match_confirmed"] for r in note["records"])
assert all(not r["runtime_promoted"] for r in note["records"])
assert witness["model_runtime_promotions"] == 0
assert witness["independent_real_person_predictive_validity"] is False

paths = [
    P + "/CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    P + "/SOURCE_MANIFEST_V1.json",
    P + "/RESEARCH_PLAN_20261017.md",
    P + "/SOURCE_REVIEW_20261017.md",
    P + "/bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P + "/bazi/bazi_source_mechanics.py",
    P + "/ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P + "/ziwei/ziwei_source_mechanics.py",
    P + "/ziwei/quan_shu_vol2_placements.py",
    P + "/ziwei/quan_shu_vol2_aux_placements.py",
    P + "/batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
    P + "/batches/ChineseAstro-02/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P + "/batches/ChineseAstro-02/test_ziwei_volume2_source.py",
    P + "/tests/test_chinese_source_mechanics.py",
] + [
    REL + name
    for name in (
        "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json",
        "SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
        "ORIGINAL_SOURCE_REVIEW_20261018.md",
        "verify_pinned_volume2_source.py",
        "test_chinese_source_03.py",
        "build_chinese_03_release.py",
    )
]
files = {name: ROOT / name for name in paths}
files[P + "/CHINESE_SOURCE_AUDIT_INDEX_V2.json"] = old_index
files[WESTERN] = ROOT / WESTERN
assert all(path.is_file() for path in files.values())
manifest = {
    "batch": "ChineseAstro-03",
    "source": "Zi Wei Dou Shu Quan Shu transmitted Volume 2, Wikisource oldid 1963110",
    "pinned_original_revision_sha256": note["raw_source_sha256"],
    "short_chinese_quote_matches": 45,
    "new_histories_ZWD": "ZWD-R0052 through ZWD-R0096",
    "original_ZiWei_history_notes_unchanged": 51,
    "original_BaZi_history_notes_unchanged": 46,
    "new_cumulative_ZiWei_histories_if_accepted": 96,
    "new_total_Chinese_histories_if_accepted": 142,
    "Western_Lilly_history_count_unchanged": 12472,
    "historic_text_not_legal_clinical_predictive_model": True,
    "Chinese_lunisolar_calculation_not_validated": True,
    "real_human_outcome_accuracy_validations": 0,
    "runtime_model_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "ChineseAstro-03-root/" + name)
    z.writestr(
        "ChineseAstro-03-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

tests = []
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "ChineseAstro-03-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, desc in manifest["members"].items():
        p = root / name
        assert p.stat().st_size == desc["bytes"]
        assert sha(p) == desc["sha256"]
    for directory, pattern, expected in (
        (REL, "test_chinese_source_03.py", 68),
        (P + "/batches/ChineseAstro-02/", "test_ziwei_volume2_source.py", 54),
        (P + "/tests/", "test_chinese_source_mechanics.py", 38),
    ):
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
            timeout=60,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        m = re.search(r"Ran (\d+) tests", proc.stderr)
        assert m and int(m.group(1)) == expected, proc.stderr
        assert "skipped" not in proc.stderr, proc.stderr
        tests.append(expected)
assert sum(tests) == 160
receipt = {
    "batch": "ChineseAstro-03",
    "status": "PINNED_RAW_VOLUME2_45_ANCHORS_160_ZIP_REPLAY_TESTS_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "member_sha256_bytes_verified": True,
    "independent_archive_extraction_passed": True,
    "new_original_quote_and_mechanics_tests": 68,
    "retained_prior_original_ziwei_tests": 54,
    "retained_chinese_engineering_tests": 38,
    "total_portable_test_replays": 160,
    "witness_sha256": sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "new_chinese_records_sha256": sha(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json"),
    "prior_chinese_index_sha256": sha(old_index),
    "western_lilly_records_unchanged": 12472,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
