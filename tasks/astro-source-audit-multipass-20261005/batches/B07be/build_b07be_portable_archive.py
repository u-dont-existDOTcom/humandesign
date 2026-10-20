#!/usr/bin/env python3
"""Independently replay original 1647/1659 single-folio Children source from ZIP.

No empirical offspring validation. Original binary photo hashes, exact source
records and index snapshots are checked in a cold extracted directory.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
WEST=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PAR=TASK/"batches/B07bd"
NAME="Astrology-Lilly-Original-Children-B07be-1647-1659-20261020.zip"

def digest(b):return sha256(b).hexdigest()

def main():
    old_parent=[
        WEST,CHINA,
        PAR/"ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json",
        PAR/"evidence/1647-original-folio757-iiif.jpg",
        PAR/"evidence/1659-original-folio757-thumb.jpg",
        PAR/"next_children_1647_photo_prefetch/1647-original-folio758-iiif.jpg",
    ]
    local=[p for p in B.rglob("*") if p.is_file() and p.suffix in (".json",".py",".md",".jpg")
           and p.name not in (
               "CANONICAL_PREPARE_RECEIPT_20261020.json",
               "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
           ) and "__pycache__" not in str(p) and "recovery" not in str(p)]
    local=sorted(set(old_parent+local),key=lambda p:str(p.relative_to(ROOT)))
    entries={}
    for p in local:
        b=p.read_bytes()
        entries[str(p.relative_to(ROOT))]={"sha256":digest(b),"bytes":len(b)}
    location=Path.home()/"Téléchargements"
    location.mkdir(parents=True,exist_ok=True)
    zipf=location/NAME
    with ZipFile(zipf,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in local:z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(zipf) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(entries):
            raise ValueError("Original independent ZIP member CRC/count mismatch")
        for name,original in entries.items():
            b=z.read(name)
            if len(b)!=original["bytes"] or digest(b)!=original["sha256"]:
                raise ValueError("Portable original source bytes/hash modified: "+name)
    with tempfile.TemporaryDirectory(prefix="source_b07be_cold_") as temp:
        path=Path(temp)
        with ZipFile(zipf) as z:z.extractall(path)
        tests=path/"tasks/astro-source-audit-multipass-20261005/batches/B07be"
        cmd=["/usr/bin/python3","-m","unittest","discover","-s",str(tests),
             "-p","test_b07be_original_children.py","-v"]
        process=subprocess.run(cmd,cwd=path,capture_output=True,text=True,timeout=35)
        log=process.stdout+process.stderr
        if process.returncode or "Ran 14 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1400:])
            raise ValueError("Cold independently extracted Children original source tests failed")
    receipt={
        "batch":"B07be","original_1647_and_1659_source_one_folio":757,
        "source_heading_next_Travel_folio":758,
        "filename":NAME,"full_archive_path_on_owner_computer":str(zipf),
        "archive_SHA256":digest(zipf.read_bytes()),"archive_bytes":zipf.stat().st_size,
        "source_member_count":len(entries),"exact_members":entries,
        "ZIP_CRC_verified":True,"exact_member_SHA256_and_bytes_verified":True,
        "independent_cold_extracted_tests":14,
        "independent_cold_extracted_green":14,
        "Lilly_current_before_acceptance":13101,
        "Lilly_after_if_original_source_accepted":13131,
        "original_entire_Wellcome_pdf_binary_copied":False,
        "original_entire_1659_DjVu_binary_copied":False,
        "actual_human_offspring_count_sex_and_mortality_verified":False,
        "genuine_blind_human_forecasts_validated":0,
        "runtime_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({
        "ARCHIVE":str(zipf),"SHA":receipt["archive_SHA256"],"bytes":zipf.stat().st_size,
        "members":len(entries),"independent_cold_tests":14
    },indent=2))
if __name__=="__main__":
    main()
