#!/usr/bin/env python3
"""Portable original Zi Wei six source structures with 58 independent ZIP test replays."""

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = "tasks/astro-chinese-primary-sources-20261017"
REL = P + "/batches/ChineseAstro-07/"
WEST = "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME = "Astrology-ZiWei-Volume2-Auxiliary-Five-Bureaus-40-Sources-B07-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    result = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    path = Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    if path is not None and path.is_dir() and path.resolve() != Path.home().resolve():
        return path
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


notes = j(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json")
witness = j(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json")
prior = j(ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json")
western = j(ROOT / WEST)
assert prior["sum_source_annotations"] == 315
assert prior["systems"][0]["accepted_source_annotations"] == 154
assert prior["systems"][1]["next_id"] == "ZWD-R0162"
assert western["records_count"] == 12611
assert notes["source_historical_annotation_count"] == 40
assert witness["original_anchor_count"] == 40
assert notes["first_id"] == "ZWD-R0162" and notes["last_id"] == "ZWD-R0201"
assert notes["pinned_original_volume2_full_raw_SHA256"] == witness["whole_raw_original_SHA256"]
assert notes["full_original_excerpt_SHA256"] == witness["excerpt_SHA256"]
assert (
    sha(B / "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt")
    == (notes["pinned_original_volume2_full_raw_SHA256"])
)
assert notes["independent_real_person_predictions_validated"] == notes["runtime_promotions"] == 0

names = [
    "TASK_SCOPE.json",
    "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    "SOURCE_1963110_AUXILIARY_AND_BUREAU_EXCERPT.txt",
    "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json",
    "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json",
    "ORIGINAL_ZIWEI_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "freeze_ziwei_vol2_aux_star_bureaus.py",
    "test_chinese07_source_aux_bureaus.py",
    "test_chinese07_full_original_provenance.py",
    "build_chinese_07_release.py",
    "prepare_chinese_07_index_v7.py",
]
files = {REL + name: B / name for name in names}
files[P + "/CHINESE_SOURCE_AUDIT_INDEX_V6.json"] = ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
files[P + "/batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"] = (
    ROOT / P / "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"
)
files[WEST] = ROOT / WEST
assert all(p.is_file() for p in files.values()), [
    name for name, p in files.items() if not p.is_file()
]
manifest = {
    "batch": "ChineseAstro-07",
    "source": (
        "Zi Wei Dou Shu Quan Shu Volume II transmitted source, pinned Wikisource oldid1963110"
    ),
    "source_full_raw_sha256": notes["pinned_original_volume2_full_raw_SHA256"],
    "source_full_raw_bytes": notes["pinned_original_volume2_full_raw_bytes"],
    "verbatim_quote_sha_and_offset_witnesses": 40,
    "five_diagrams_exact_raw_text_preserved": True,
    "original_stars_29_verse_5_bureaus_5": True,
    "ZiWei_source_notes_if_accepted": 201,
    "BaZi_history_retained": 154,
    "Chinese_total_if_accepted": 355,
    "Western_Lilly_branch_pinned_at": 12611,
    "full_Chinese_birth_lunar_day_palace_engine_verified": False,
    "source_original_early_Ming_print_authenticated": False,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
target = folder / NAME
temp = folder / (NAME + ".building")
assert not temp.exists(), temp
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "ChineseAstro-07-root/" + name)
    z.writestr(
        "ChineseAstro-07-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
test_suites = [
    ("test_chinese07_source_aux_bureaus.py", 55),
    ("test_chinese07_full_original_provenance.py", 3),
]
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    base = Path(td) / "ChineseAstro-07-root"
    assert j(base / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = base / name
        assert f.stat().st_size == meta["bytes"], name
        assert sha(f) == meta["sha256"], name
    for name, count in test_suites:
        result = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", str(base / REL), "-p", name, "-q"],
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert result.returncode == 0, result.stdout + "\n" + result.stderr
        n = re.search(r"Ran (\d+) tests", result.stderr)
        assert n and int(n.group(1)) == count, result.stderr
        assert "skipped" not in result.stderr
os.replace(temp, target)
receipt = {
    "batch": "ChineseAstro-07",
    "status": "ZIWEI_ORIGINAL_FIVE_BUREAU_DIAGRAMS_40_QUOTES_58_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(target),
    "archive_bytes": target.stat().st_size,
    "members": len(files),
    "CRC_passed": True,
    "all_member_SHA256_exact_bytes_passed": True,
    "extracted_original_source_tests_passed": 58,
    "earlier_unmodified_chinese_suites_rerun": False,
    "source_notes_SHA256": sha(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json"),
    "source_witness_SHA256": sha(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json"),
    "prior_Chinese_V6_SHA256": sha(ROOT / P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"),
    "parallel_Western_index_B07al_SHA256": sha(ROOT / WEST),
    "source_raw_volume_full_SHA256": sha(B / "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"),
    "new_historical_ZiWei_notes": 40,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
