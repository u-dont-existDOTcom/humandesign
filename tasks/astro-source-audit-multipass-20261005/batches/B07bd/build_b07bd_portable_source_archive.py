#!/usr/bin/env python3
"""Portable exact SHA/CRC source evidence archive for B07bd CLXXXI Marriage.

Archive contains all material required for the standalone 17 offline source
unittests from a fresh extracted directory. Original 1647/1659 page images
are public-domain scans, tracked via exact bytes and SHA and not new outcomes.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
CHINESE=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
WEST=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PORTABLE_NAME="Astrology-Lilly-Original-Marriage-1647-1659-B07bd-20261020.zip"

SOURCE_LOCALS = [
    WEST, CHINESE,
    TASK/"batches/B07bb/evidence/1647_original-788.jpg",
    TASK/"batches/B07bc/evidence/1659_original_djvu_783.jpg",
    TASK/"batches/B07bc/ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json",
    TASK/"batches/B07ax/MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json",
]
INCLUDE_B07BD_EXTS={".py",".json",".md",".jpg"}
SKIP_NAMES={
    "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
    "CANONICAL_PREPARE_RECEIPT_20261020.json",
    "ACCEPTED_CONTINUATION_CHECKPOINT_20261020.json",
}
def h(data):return sha256(data).hexdigest()

def main():
    local=[p for p in SOURCE_LOCALS]
    local += [
        p for p in B.rglob("*") if p.is_file()
        and p.suffix in INCLUDE_B07BD_EXTS
        and p.name not in SKIP_NAMES
        and "__pycache__" not in str(p)
        and "recovery" not in str(p)
    ]
    local=sorted(set(local),key=lambda p:str(p.relative_to(ROOT)))
    if any(not p.is_file() for p in local):
        raise FileNotFoundError("Unresolved independent source input missing")
    expected={}
    for path in local:
        name=str(path.relative_to(ROOT))
        data=path.read_bytes()
        expected[name]={"sha256":h(data),"bytes":len(data)}
    # Use French-localized Downloads only when actual directory exists.
    download=Path.home()/"Téléchargements"
    if not download.is_dir():
        download=Path.home()/"Downloads"
    download.mkdir(parents=True,exist_ok=True)
    outfile=download/PORTABLE_NAME
    with ZipFile(outfile,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for path in local:
            z.write(path,arcname=str(path.relative_to(ROOT)))

    with ZipFile(outfile,"r") as z:
        if z.testzip() is not None:
            raise ValueError("Corrupt ZIP CRC")
        names=z.namelist()
        if sorted(names)!=sorted(expected):
            raise ValueError("Missing/extra ZIP member")
        for name,origin in expected.items():
            data=z.read(name)
            if h(data)!=origin["sha256"] or len(data)!=origin["bytes"]:
                raise ValueError("ZIP original member SHA/bytes changed")

    with tempfile.TemporaryDirectory(prefix="lilly_b07bd_independent_source_") as tm:
        output=Path(tm)
        with ZipFile(outfile) as z:
            z.extractall(output)
        # Execute independent fresh process with NO project site-packages:
        # optional genuine Swiss ephemeris tests are expected to skip.
        testdir=output/"tasks/astro-source-audit-multipass-20261005/batches/B07bd"
        script=[
            "/usr/bin/python3","-m","unittest","discover",
            "-s",str(testdir),
            "-p","test_b07bd_original_marriage.py",
            "-v",
        ]
        r=subprocess.run(script,cwd=output,capture_output=True,text=True,timeout=50)
        if r.returncode!=0 or "Ran 19 tests" not in (r.stderr+r.stdout):
            print((r.stderr+r.stdout)[-1600:])
            raise ValueError("Independently extracted full source test suite failed")
        if not "OK (skipped=2)" in r.stderr:
            print(r.stderr[-700:])
            raise ValueError("Expected 17/19 unittests active and 2 SWIEPH optional skips")
        verified_actual=17

    receipt={
        "batch":"B07bd",
        "source_archive":"1647/1659 photographed primary Marriage chapter and dependencies",
        "filename":PORTABLE_NAME,
        "archive_path_on_owner_machine":str(outfile),
        "archive_sha256":h(outfile.read_bytes()),
        "archive_bytes":outfile.stat().st_size,
        "ZIP_member_count":len(expected),
        "source_member_manifest":expected,
        "ZIP_CRC_verified":True,
        "member_SHA256_and_bytes_verified":True,
        "independently_extracted_standalone_original_tests_executed":19,
        "independently_extracted_actual_offline_tests_passed":verified_actual,
        "independently_extracted_optional_SWE_tests_skipped":2,
        "original_1647_Wellcome_whole_PDF_binary_copied":False,
        "original_1659_whole_DjVu_binary_copied":False,
        "Lilly_before_append":13044,
        "Lilly_after_if_accepted":13101,
        "accepted_chinese_other_lane_unchanged":True,
        "real_human_predictive_tests_verified":0,
        "runtime_astrological_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "ZIP":str(outfile),"bytes":outfile.stat().st_size,
        "SHA":receipt["archive_sha256"],"members":len(expected),
        "independent_tests":19,"passed":17,"skipped_optional_swe":2,
    },indent=2))

if __name__=="__main__":
    main()
