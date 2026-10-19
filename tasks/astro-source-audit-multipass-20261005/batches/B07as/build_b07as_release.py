#!/usr/bin/env python3
"""Original Lilly 1647/1659 CLXXI source-only portable evidence ZIP."""

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
REL = TASK + "/batches/B07as/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXXI-Fortune-Alfridary-B07as-20261019.zip"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    path = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if path and path.is_dir() and path.resolve() != Path.home().resolve():
        return path
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


a = j(B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
west = j(ROOT / WEST)
china = j(ROOT / CHINA)
assert west["records_count"] == accept["Lilly_before"] == 12742
assert west["batches"][-1]["id"] == "B07ar"
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert len(a["records"]) == rules["record_count"] == 22
assert a["source_full_life_cycle_sequence_in_this_chapter"] is False
assert a["independent_actual_human_forecasts_validated"] == 0
assert rules["real_person_predicted_life_events_validated"] == 0
assert (
    sha(B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json")
    == accept["source_records_SHA256"]
)
assert sha(B / "RULES.json") == accept["rules_SHA256"]

members = [
    "CONTINUATION_CHECKPOINT_20261019.md",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "ACCEPTANCE.json",
    "RULES.json",
    "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json",
    "SECONDARY_CLXXI_NAVIGATOR.txt",
    "build_b07as_original_CLXXI_source.py",
    "test_b07as_original_CLXXI.py",
    "build_b07as_release.py",
    "prepare_b07as_canonical.py",
]
files = {REL + n: B / n for n in members}
for n in (
    "evidence/1647_original-767.jpg",
    "evidence/1647_original-768.jpg",
    "evidence/original_1659_djvu_762.jpg",
    "evidence/original_1659_djvu_763.jpg",
):
    files[REL + n] = B / n
for name, entry in a["source_first_and_separate_second_original_printings"].items():
    file = ROOT / entry["relative_original_photo"]
    files[entry["relative_original_photo"]] = file
    assert sha(file) == entry["source_image_sha256"], name
    assert file.stat().st_size == entry["file_bytes"], name
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(v.is_file() for v in files.values()), [k for k, v in files.items() if not v.is_file()]
manifest = {
    "batch": "B07as",
    "source": "William Lilly original 1647 and independent typeset 1659 printed732–734",
    "primary_full_1647_PDF_sha256": a["source_original_book_Wellcome_1647_full_pdf_SHA256"],
    "original_six_first_second_edition_page_images": 6,
    "literal_original_full_expert_philological_verification": False,
    "historical_source_notes": 22,
    "first": "R12743",
    "last": "R12764",
    "Lilly_if_accepted": 12764,
    "Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "next_original_source": "R12765 / CLXXII Of Revolutions at original PDF768",
    "full_Alfridary_life_cycle_verified": False,
    "independent_actual_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "source_members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
dest = downloads()
dest.mkdir(parents=True, exist_ok=True)
archive = dest / NAME
building = dest / (NAME + ".building")
assert not building.exists(), building
with zipfile.ZipFile(building, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07as-root/" + name)
    z.writestr(
        "B07as-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(building) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07as-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["source_members"].items():
        f = root / name
        assert f.stat().st_size == meta["bytes"], name
        assert sha(f) == meta["sha256"], name
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07as_original_CLXXI.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 34, proc.stderr
    assert "skipped" not in proc.stderr
os.replace(building, archive)
receipt = {
    "batch": "B07as",
    "status": "ORIGINAL_1647_1659_CLXXI_22_HISTORICAL_NOTES_34_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "members": len(files),
    "CRC_passed": True,
    "every_member_SHA256_and_bytes_passed": True,
    "independent_archive_extraction_34_tests_passed": True,
    "portable_test_count": 34,
    "source_note_SHA256": sha(
        B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json"
    ),
    "rules_SHA256": sha(B / "RULES.json"),
    "prior_Lilly_index_sha256": sha(ROOT / WEST),
    "Chinese_V7_index_sha256": sha(ROOT / CHINA),
    "human_prediction_validations": 0,
    "runtime_model_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
