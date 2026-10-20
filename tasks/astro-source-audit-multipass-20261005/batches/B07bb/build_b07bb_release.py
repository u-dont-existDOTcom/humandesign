#!/usr/bin/env python3
"""Portable Lilly 1647/1659 parents-source archival packet, 42 extracted tests."""

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
T = "tasks/astro-source-audit-multipass-20261005"
REL = T + "/batches/B07bb/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-Parents-1647-1659-26-Historical-Sources-B07bb-20261020.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def owner_downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


source = load(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
old = load(ROOT / WEST)
china = load(ROOT / CHINESE)
assert old["records_count"] == accept["Lilly_before"] == 12991
assert old["batches"][-1]["id"] == "B07ba"
assert old["next"]["chapter"] == "CLXXIX" and old["next"]["pdf_page"] == 786
assert china["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert len(source["records"]) == len(rules["rules"]) == 26
assert source["next_record"] == "R13018"
assert all(not x["runtime_model_promoted"] for x in rules["rules"])
assert accept["source_notes_sha256"] == sha(
    B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json"
)
assert accept["rules_sha256"] == sha(B / "RULES.json")

names = [
    "build_b07bb_parents_source.py",
    "test_b07bb_original_parents.py",
    "prepare_b07bb_canonical.py",
    "build_b07bb_release.py",
    "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "TASK_SCOPE.json",
    "ORIGINAL_SOURCE_REVIEW_20261020.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261020.md",
]
files = {REL + n: B / n for n in names}
files[T + "/batches/B07ba/ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"] = (
    B.parent / "B07ba/ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"
)
for folio, editions in source["two_original_printings_four_page_photo_witnesses"].items():
    for ed, entry in editions.items():
        name = entry["original_source_repo_relative_file"]
        file = ROOT / name
        assert int(folio) == entry["original_folio"]
        assert int(ed) == entry["source_ed"]
        assert sha(file) == entry["sha256"]
        assert file.stat().st_size == entry["bytes"]
        files[name] = file
extra = B / "evidence/1647_original-788.jpg"
if extra.is_file():
    files[REL + "evidence/1647_original-788.jpg"] = extra
files[WEST] = ROOT / WEST
files[CHINESE] = ROOT / CHINESE
assert all(path.is_file() for path in files.values())
manifest = {
    "batch": "B07bb",
    "source": "Original William Lilly Christian Astrology 1647 first and separately typeset 1659",
    "original_1647_full_PDF_sha256": source["source_full_original_Wellcome_1647_PDF_sha256"],
    "original_printed_chapter": "CLXXIX Of Parents",
    "original_photographic_printed_folios": [752, 753],
    "original_first_second_edition_source_photos": 4,
    "prior_Lilly_source_records": 12991,
    "new_historical_parent_source_notes": 26,
    "Lilly_total_if_admitted": 13017,
    "Ptolemy_retained": 1066,
    "Western_total_if_admitted": 14083,
    "Chinese_V7_retained": 355,
    "Ptolemy_attribution_externally_verified": False,
    "real_parent_independent_birth_chart_verified": False,
    "real_parent_mortality_and_love_predictions_verified": False,
    "source_procedure_not_validated_as_astronomical_engine": True,
    "next_R": "R13018",
    "next_chapter": "CLXXX Sicknesse, Servants",
    "empirical_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in files.items()},
}
out = owner_downloads()
out.mkdir(parents=True, exist_ok=True)
archive = out / NAME
temp = out / (NAME + ".building")
assert not temp.exists(), temp
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, f in files.items():
        z.write(f, "B07bb-root/" + name)
    z.writestr(
        "B07bb-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    restored = Path(td) / "B07bb-root"
    assert load(restored / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        file = restored / name
        assert file.stat().st_size == meta["bytes"], name
        assert sha(file) == meta["sha256"], name
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(restored / REL),
            "-p",
            "test_b07bb_original_parents.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 42, proc.stderr
    assert "skipped" not in proc.stderr
os.replace(temp, archive)
receipt = {
    "batch": "B07bb",
    "status": "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_42_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "members": len(files),
    "CRC_passed": True,
    "member_SHA256_and_exact_bytes_passed": True,
    "independent_archive_extraction_tests_passed": True,
    "portable_test_replays": 42,
    "source_notes_sha256": sha(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "old_Lilly_index_sha256": sha(ROOT / WEST),
    "Chinese_V7_index_sha256": sha(ROOT / CHINESE),
    "new_historical_notes_if_admitted": 26,
    "human_parental_outcomes_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
