#!/usr/bin/env python3
"""Portable original 1647/1659 CLXXII final-source photo evidence ZIP."""

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
REL = TASK + "/batches/B07au/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXXII-Chart-Comparison-B07au-20261019.zip"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    folder = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if folder is not None and folder.is_dir() and folder.resolve() != Path.home().resolve():
        return folder
    fr = Path.home() / "Téléchargements"
    return fr if fr.is_dir() else Path.home()


data = j(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json")
prepped = j(B / "SOURCE_EVIDENCE_PREP_ONLY_V1.json")
rules = j(B / "RULES.json")
accepted = j(B / "ACCEPTANCE.json")
assert j(ROOT / WEST)["records_count"] == 12788
assert j(ROOT / CHINA)["sum_source_annotations"] == 355
assert len(data["records"]) == rules["record_count"] == 15
assert len(data["source_new_edition_photos"]) == 6
assert len(prepped["historical_first_edition_source_photographs"]) == 4
assert not data["critical_source_edition_expert_collation_complete"]
assert data["independent_real_human_prediction_validations"] == 0
assert (
    sha(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json")
    == (accepted["new_source_SHA256"])
)
assert sha(B / "RULES.json") == accepted["rules_SHA256"]

files = {
    REL + n: B / n
    for n in [
        "CONTINUATION_CHECKPOINT_PROVISIONAL_20261019.md",
        "SOURCE_EVIDENCE_PREP_ONLY_V1.json",
        "ORIGINAL_SOURCE_REVIEW_20261019.md",
        "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
        "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json",
        "RULES.json",
        "ACCEPTANCE.json",
        "build_b07au_original_revolution_comparison.py",
        "test_b07au_original_revolution.py",
        "build_b07au_release.py",
        "prepare_b07au_canonical.py",
    ]
}
for record in data["source_new_edition_photos"].values():
    p = ROOT / record["repository_path"]
    assert sha(p) == record["sha256"]
    files[record["repository_path"]] = p
for record in prepped["historical_first_edition_source_photographs"]:
    p = B / record["relative_evidence_file"]
    assert sha(p) == record["sha256"]
    files[REL + record["relative_evidence_file"]] = p
# Keep the separately printed p739 as a prepared-only future source.
for n in (765, 766, 767, 768):
    p = B / "evidence" / f"1659_original_djvu_{n}.jpg"
    assert p.is_file()
    files[REL + f"evidence/1659_original_djvu_{n}.jpg"] = p
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values())
manifest = {
    "batch": "B07au",
    "original_full_Wellcome_1647_PDF_sha256": data["original_full_first_edition_PDF_SHA256"],
    "original_source_reviewed_first_edition_frames": [770, 771, 772],
    "prepared_only_not_source_admitted_first_edition_frame": [773],
    "source_reviewed_actual_original_1647_and_separate_1659_photos": 6,
    "historical_documentary_source_records": 15,
    "Lilly_after_if_accepted": 12803,
    "Chinese_V7_retained": 355,
    "next_original_source": "R12804 CLXXIII p738/PDF772",
    "full_original_philological_expert_collation": False,
    "historical_natal_event_prediction_validated": False,
    "runtime_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
dest = downloads()
dest.mkdir(parents=True, exist_ok=True)
archive = dest / NAME
temporary = dest / (NAME + ".building")
assert not temporary.exists(), temporary
with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07au-root/" + name)
    z.writestr(
        "B07au-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temporary) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07au-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        p = root / name
        assert p.stat().st_size == meta["bytes"], name
        assert sha(p) == meta["sha256"], name
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07au_original_revolution.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    m = re.search(r"Ran (\d+) tests", result.stderr)
    assert m and int(m.group(1)) == 25, result.stderr
    assert "skipped" not in result.stderr
os.replace(temporary, archive)
receipt = {
    "batch": "B07au",
    "status": "CLXXII_ORIGINAL_SOURCE_SPAN_15_NOTES_25_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "CRC_passed": True,
    "all_members_SHA256_and_exact_bytes_passed": True,
    "independent_archive_extraction_replayed_tests": 25,
    "source_SHA256": sha(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "prior_Lilly_index_SHA256": sha(ROOT / WEST),
    "Chinese_V7_SHA256": sha(ROOT / CHINA),
    "new_documentary_notes_if_admitted": 15,
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
