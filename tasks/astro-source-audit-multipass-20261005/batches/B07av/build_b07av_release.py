#!/usr/bin/env python3
"""Portable Lilly CLXXIII original two-edition historical source snapshot.

Carries all eight primary printed photographs, two authentic heading crop
evidence images and exact source-only 42-clause mapping. Independently extract,
CRC-check, verify every binary SHA256/size, and replay 106 tests OFF the worktree.
"""

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
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07av/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXXIII-42-Radix-Returns-B07av-20261019.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    folder = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if folder is not None and folder.is_dir() and folder.resolve() != Path.home().resolve():
        return folder
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


rules = j(B / "RULES.json")
source = j(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json")
photo = j(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json")
roman = j(B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json")
accept = j(B / "ACCEPTANCE.json")
west = j(ROOT / INDEX)
china = j(ROOT / CHINESE)
assert west["records_count"] == accept["Lilly_before"] == 12803
assert west["batches"][-1]["id"] == "B07au"
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert rules["record_count"] == 42
assert len(source["rows"]) == len(rules["rules"]) == 42
assert len(photo["photo_witnesses"]) == 8
assert rules["physical_CLXXIII_text_covered"]
assert not source["complete_expert_critical_edition_collation"]
assert source["actual_real_human_prediction_validations"] == 0
assert source["runtime_promotions"] == 0
assert accept["next_R"] == "R12846"
assert roman["source_original_first_1647_literal_printed_heading"] == "CHAP. CLXXIIII."
assert roman["source_second_1659_literal_printed_heading"] == "CHAP. CLXXIV."
assert sha(B / "RULES.json") == accept["rules_sha256"]
assert (
    sha(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json")
    == (accept["source_full_doc_sha256"])
)

names = [
    "TASK_SCOPE.json",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "MATRIX_SOURCE_CHECKPOINT_20261019.md",
    "CONTINUATION_HANDOFF_SOURCE_READY_20261019.md",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json",
    "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json",
    "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json",
    "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "build_b07av_42_source_rules.py",
    "test_b07av_source_preflight.py",
    "test_b07av_original_rules.py",
    "build_b07av_release.py",
    "prepare_b07av_canonical.py",
]
files = {REL + name: B / name for name in names}
for _key, meta in photo["photo_witnesses"].items():
    file = ROOT / meta["relative_repo_path"]
    assert file.is_file()
    assert file.stat().st_size == meta["bytes"]
    assert sha(file) == meta["sha256"]
    files[meta["relative_repo_path"]] = file
for edition in ("1647", "1659"):
    relative = roman[f"{edition}_heading_crop"]
    file = B / relative
    assert sha(file) == roman[f"{edition}_heading_crop_sha256"]
    files[REL + relative] = file
files[INDEX] = ROOT / INDEX
files[CHINESE] = ROOT / CHINESE
assert all(file.is_file() for file in files.values()), [
    key for key, file in files.items() if not file.is_file()
]
assert len(files) == len(set(files))
manifest = {
    "batch": "B07av",
    "source_original_Wellcome_1647_book_full_pdf_SHA256": source[
        "original_full_1647_source_pdf_sha256"
    ],
    "source_original_print_folios": [738, 739, 740, 741],
    "source_two_edition_witnesses_count": 8,
    "source_historical_clause_rows": 42,
    "one_reader_documentary_photo_mapping_only": True,
    "1647_next_distinct_chapter_literal": "CLXXIIII",
    "1659_next_distinct_chapter_literal": "CLXXIV",
    "expert_independent_original_edition_collation_complete": False,
    "next_historical_R": "R12846",
    "Lilly_count_before": 12803,
    "Lilly_count_if_accepted": 12845,
    "Chinese_V7_history_unchanged": 355,
    "real_person_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "members": {
        key: {"sha256": sha(file), "bytes": file.stat().st_size} for key, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
building = folder / (NAME + ".building")
assert not building.exists()
with zipfile.ZipFile(building, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07av-root/" + name)
    z.writestr(
        "B07av-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
results = []
with zipfile.ZipFile(building) as z, tempfile.TemporaryDirectory() as d:
    assert z.testzip() is None
    z.extractall(d)
    home = Path(d) / "B07av-root"
    assert j(home / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        file = home / name
        assert file.stat().st_size == meta["bytes"], name
        assert sha(file) == meta["sha256"], name
    for pattern, expected in (
        ("test_b07av_source_preflight.py", 52),
        ("test_b07av_original_rules.py", 54),
    ):
        proc = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", str(home / REL), "-p", pattern, "-q"],
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        m = re.search(r"Ran (\d+) tests", proc.stderr)
        assert m and int(m.group(1)) == expected, proc.stderr
        assert "skipped" not in proc.stderr
        results.append(expected)
assert results == [52, 54]
os.replace(building, archive)
receipt = {
    "batch": "B07av",
    "status": "ORIGINAL_1647_1659_CLXXIII_42_SOURCE_CLAUSES_106_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "member_SHA256_bytes_verified": True,
    "independent_extracted_archive_tests_passed": True,
    "preflight_tests_replayed": 52,
    "source_tests_replayed": 54,
    "archive_test_replays_total": sum(results),
    "original_source_photo_manifest_sha256": sha(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "source_witness_sha256": sha(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json"),
    "source_original_next_chapter_roman_variant_sha256": sha(
        B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json"
    ),
    "previous_Western_index_sha256": sha(ROOT / INDEX),
    "Chinese_V7_sha256": sha(ROOT / CHINESE),
    "historical_source_records_if_admitted": 42,
    "human_predictive_validations": 0,
    "astrological_runtime_model_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
