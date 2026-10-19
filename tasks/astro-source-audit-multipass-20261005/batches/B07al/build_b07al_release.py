#!/usr/bin/env python3
"""Archive four original 1647 folios and source-only annual profections notes.

Verify CRC, per-file SHA256/size, and 43 hermetic replayed unit tests.
This explicitly does NOT attest every merchant table cell, date conversion
or empirical natal chart prediction.
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
REL = TASK + "/batches/B07al/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-Annual-Profections-30-Sources-B07al-20261019.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


source = read(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json")
rules = read(B / "RULES.json")
accept = read(B / "ACCEPTANCE.json")
prior = read(ROOT / INDEX)
chinese = read(ROOT / CHINA)
assert prior["records_count"] == 12581 and prior["batches"][-1]["id"] == "B07ak"
assert chinese["sum_source_annotations"] == 262
assert len(source["records"]) == len(rules["rules"]) == 30
assert source["original_merchant_table_physical_source_rows"] == 72
assert not source["all_merchant_table_zodiac_cells_expert_collated"]
assert accept["next_source_R"] == "R12612" and accept["Lilly_if_accepted"] == 12611
assert (
    sha(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json") == accept["source_SHA256"]
)
assert sha(B / "RULES.json") == accept["rules_SHA256"]
assert (
    rules["empirical_real_human_predictions_validated"]
    == source["real_person_outcome_predictions_validated"]
    == 0
)
assert source["runtime_model_promotions"] == rules["runtime_promotions"] == 0

names = [
    "ACCEPTANCE.json",
    "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json",
    "RULES.json",
    "source_annual_profections.py",
    "build_annual_profections_source.py",
    "test_b07al_original_profections.py",
    "prepare_b07al_canonical.py",
    "build_b07al_release.py",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "evidence/1647_original_pdf-751.jpg",
    "evidence/1647_original_pdf-752.jpg",
]
files = {REL + n: B / n for n in names}
for frame in (749, 750):
    name = f"{TASK}/batches/B07x/evidence/pdf_1647-{frame}.jpg"
    files[name] = B.parent / "B07x/evidence" / f"pdf_1647-{frame}.jpg"
files[TASK + "/batches/B07ak/ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json"] = (
    B.parent / "B07ak/ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values()), [
    key for key, file in files.items() if not file.is_file()
]
for entry in source["original_first_edition_photo_witnesses"].values():
    photo = ROOT / entry["file"]
    assert photo in files.values()
    assert sha(photo) == entry["sha256"]
    assert photo.stat().st_size == entry["bytes"]

manifest = {
    "batch": "B07al",
    "historical_textual_source_only": True,
    "physical_source": (
        "William Lilly Christian Astrology 1647 first edition, printed folios 715–718"
    ),
    "original_full_pdf_sha256": source["original_Wellcome_first_edition_full_PDF_SHA256"],
    "original_1647_photo_frames": [749, 750, 751, 752],
    "second_original_printed_CLXVI_physically_distinct": True,
    "next_original_printed_CLXVII_on_same_p718": True,
    "historical_notes": 30,
    "merchant_72_year_full_zodiac_table_critically_read": False,
    "prior_Lilly_source_count": 12581,
    "new_Lilly_source_count_if_accepted": 12611,
    "Chinese_V5_source_count_retained": 262,
    "full_birth_date_calendar_and_solar_return_engine_verified": False,
    "human_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {
        path: {"sha256": sha(file), "bytes": file.stat().st_size} for path, file in files.items()
    },
}
output = downloads()
output.mkdir(parents=True, exist_ok=True)
archive = output / NAME
building = output / (NAME + ".building")
assert not building.exists()
with zipfile.ZipFile(building, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path, file in files.items():
        z.write(file, "B07al-root/" + path)
    z.writestr(
        "B07al-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(building) as z, tempfile.TemporaryDirectory() as folder:
    assert z.testzip() is None
    z.extractall(folder)
    extracted = Path(folder) / "B07al-root"
    assert read(extracted / "RELEASE_MANIFEST.json") == manifest
    for name, spec in manifest["members"].items():
        file = extracted / name
        assert file.stat().st_size == spec["bytes"]
        assert sha(file) == spec["sha256"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(extracted / REL),
            "-p",
            "test_b07al_original_profections.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 43, proc.stderr
    assert "skipped" not in proc.stderr
os.replace(building, archive)
receipt = {
    "batch": "B07al",
    "status": "1647_ORIGINAL_SECOND_CLXVI_ANNUAL_PROFECTIONS_43_ZIP_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "members_sha256_bytes_passed": True,
    "independent_extracted_test_replay_passed": True,
    "test_count": 43,
    "source_SHA256": sha(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "prior_Western_index_SHA256": sha(ROOT / INDEX),
    "Chinese_V5_SHA256": sha(ROOT / CHINA),
    "new_historical_source_notes_if_accepted": 30,
    "no_independent_human_predictive_successes": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
