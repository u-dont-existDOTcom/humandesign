#!/usr/bin/env python3
"""Portable original 1647/1659 Riches source with 41 independently replayed tests."""

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
REL = TASK + "/batches/B07az/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-Riches-1647-1659-29-Historical-Sources-B07az-20261020.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


source = j(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
old = j(ROOT / WEST)
chinese = j(ROOT / CHINA)
assert old["records_count"] == 12940 and old["batches"][-1]["id"] == "B07ay"
assert chinese["sum_source_annotations"] == 355
assert len(source["records"]) == rules["record_count"] == 29
assert accept["next_R"] == "R12970" and accept["next_chapter"] == "CLXXVIII"
assert source["independent_biographical_wealth_predicted_outcomes_validated"] == 0
assert not source["complete_independent_critical_edition_expert_review"]
assert sha(B / "RULES.json") == accept["rules_SHA256"]
assert (
    sha(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
    == (accept["source_photo_witness_SHA256"])
)
names = [
    "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "TASK_SCOPE.json",
    "RECOVERY_CHECKPOINT_20261020.md",
    "build_b07az_original_riches.py",
    "test_b07az_riches_original.py",
    "build_b07az_release.py",
    "prepare_b07az_canonical.py",
]
files = {REL + n: B / n for n in names}
photos = source["original_1647_and_1659_six_source_photo_witnesses"]
for entries in photos.values():
    for meta in entries.values():
        name = meta["relative_path"]
        p = ROOT / name
        assert p.is_file() and sha(p) == meta["sha256"]
        assert p.stat().st_size == meta["bytes"]
        files[name] = p
files[TASK + "/batches/B07ay/ORIGINAL_PHOTO_WITNESS_V1.json"] = (
    B.parent / "B07ay/ORIGINAL_PHOTO_WITNESS_V1.json"
)
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(x.is_file() for x in files.values()), [
    name for name, p in files.items() if not p.is_file()
]
manifest = {
    "batch": "B07az",
    "source": "Lilly Christian Astrology 1647 first and independently typeset 1659 printed749–751",
    "1647_original_Wellcome_full_pdf_SHA256": source["original_full_1647_PDF_sha256"],
    "source_physical_first_and_second_print_page_images": 6,
    "source_note_records": 29,
    "start_R": "R12941",
    "last_R": "R12969",
    "next_R": "R12970",
    "next_distinct_chapter": "CLXXVIII Of Brethren",
    "known_merchant_retrospective_not_heldout_sample": True,
    "individual_financial_familial_legal_outcomes_validated": 0,
    "Lilly_documentary_after_if_admitted": 12969,
    "Chinese_V7_documentary_retained": 355,
    "critical_edition_expert_review_complete": False,
    "historical_1616_natal_chart_engine_verified": False,
    "runtime_model_promotions": 0,
    "members": {name: {"sha256": sha(p), "bytes": p.stat().st_size} for name, p in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
tmp = folder / (NAME + ".building")
assert not tmp.exists(), tmp
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07az-root/" + name)
    z.writestr(
        "B07az-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07az-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        p = root / name
        assert sha(p) == meta["sha256"], name
        assert p.stat().st_size == meta["bytes"], name
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07az_riches_original.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    matched = re.search(r"Ran (\d+) tests", result.stderr)
    assert matched and int(matched.group(1)) == 41, result.stderr
    assert "skipped" not in result.stderr
os.replace(tmp, archive)
receipt = {
    "batch": "B07az",
    "status": "LILLY_1647_1659_RICHES_29_SOURCE_41_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "member_SHA256_exact_bytes_passed": True,
    "independent_archive_extracted_test_replay_passed": 41,
    "source_notes_sha256": sha(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"),
    "source_rules_sha256": sha(B / "RULES.json"),
    "prior_Lilly_index_sha256": sha(ROOT / WEST),
    "Chinese_V7_index_sha256": sha(ROOT / CHINA),
    "human_outcomes_validated": 0,
    "runtime_promotions": 0,
    "published_remotely": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
