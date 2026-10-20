#!/usr/bin/env python3
"""Portable original Lilly Travels page snapshots and offline source tests.

Source-only public-domain folios, no actual merchant outcome evidence.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
WEST=T/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
TITLE="Astrology-Lilly-Original-Travels-1647-1659-B07bf-20261020.zip"

def digest(blob):return sha256(blob).hexdigest()

def archive():
    parent=[
        WEST,CHINA,
        T/"batches/B07be/ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json",
        T/"batches/B07bd/next_children_1647_photo_prefetch/1647-original-folio758-iiif.jpg",
        T/"batches/B07bd/next_children_1647_photo_prefetch/1647-original-folio759-iiif.jpg",
        T/"batches/B07be/evidence/1659-original-folio758-next-travel-thumbnail.jpg",
    ]
    local=[p for p in B.rglob("*") if p.is_file() and p.suffix.lower() in
           (".py",".md",".json",".jpg") and p.name not in
           ("SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
            "CANONICAL_PREPARE_RECEIPT_20261020.json")
           and "recovery" not in str(p) and "__pycache__" not in str(p)]
    files=sorted(set(parent+local),key=lambda p:str(p.relative_to(ROOT)))
    manifest={}
    for p in files:
        if not p.is_file():raise FileNotFoundError(p)
        data=p.read_bytes()
        manifest[str(p.relative_to(ROOT))]={"sha256":digest(data),"bytes":len(data)}
    download=Path.home()/"Téléchargements"
    download.mkdir(parents=True,exist_ok=True)
    zip_path=download/TITLE
    with ZipFile(zip_path,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in files:z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(zip_path) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(manifest):
            raise ValueError("Source archive CRC or exact member list invalid")
        for name,item in manifest.items():
            data=z.read(name)
            if len(data)!=item["bytes"] or digest(data)!=item["sha256"]:
                raise ValueError("Source archive SHA/bytes mismatch "+name)
    with tempfile.TemporaryDirectory(prefix="lilly_B07bf_source_") as tmp:
        extracted=Path(tmp)
        with ZipFile(zip_path) as z:z.extractall(extracted)
        testdir=extracted/"tasks/astro-source-audit-multipass-20261005/batches/B07bf"
        subprocess_call=["/usr/bin/python3","-m","unittest","discover",
                         "-s",str(testdir),"-p","test_b07bf_original_travels.py","-v"]
        p=subprocess.run(subprocess_call,cwd=extracted,capture_output=True,text=True,
                         timeout=45)
        logs=p.stdout+p.stderr
        if p.returncode or "Ran 11 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-1200:])
            raise ValueError("Independent cold extracted source-only tests did not pass 11/11")
    receipt={
        "batch":"B07bf",
        "filename":TITLE,"owner_local_portable_path":str(zip_path),
        "archive_sha256":digest(zip_path.read_bytes()),
        "archive_bytes":zip_path.stat().st_size,
        "source_member_count":len(manifest),
        "source_member_sha256_and_bytes":manifest,
        "zip_CRC_verified":True,
        "all_portable_members_independently_SHA_checked":True,
        "fresh_cold_extraction_source_tests_executed":11,
        "fresh_cold_extraction_source_tests_green":11,
        "original_1647_entire_Wellcome_PDF_redistributed":False,
        "original_1659_full_DjVu_binary_redistributed":False,
        "actual_known_merchant_trip_log_confirmed":False,
        "actual_human_predictive_accuracy_validated":0,
        "runtime_forecast_rules_promoted":0
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "ARCHIVE":str(zip_path),"SIZE":zip_path.stat().st_size,
        "SHA256":receipt["archive_sha256"],"MEMBERS":len(manifest),
        "COLD_UNITTTESTS_GREEN":11
    },indent=2))

if __name__=="__main__":archive()
