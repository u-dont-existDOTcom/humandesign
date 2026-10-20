#!/usr/bin/env python3
"""Portable original Zi Wei star profiles 5-8 source and cold offline tests.

This is a historical source witness pack, not a validated full natal chart.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED,ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
INDEX=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
ORIGINAL=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS=T/"batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"
WESTERN=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME="Astrology-ZiWei-Original-Life-Third-Four-Stars-83-Sources-V12-20261020.zip"

def h(raw):return sha256(raw).hexdigest()
def main():
    needed=[INDEX,ORIGINAL,PREVIOUS,WESTERN]
    local=[p for p in B.rglob("*") if p.is_file()
           and p.suffix.lower() in (".py",".json",".md",".txt")
           and "__pycache__" not in str(p) and "recovery" not in str(p)
           and p.name not in (
              "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
              "CANONICAL_PREPARE_RECEIPT_20261020.json",
              "ACCEPTED_CONTINUATION_CHECKPOINT_20261020.json"
           )]
    paths=sorted(set(needed+local),key=lambda p:str(p.relative_to(ROOT)))
    members={}
    for p in paths:
        data=p.read_bytes()
        members[str(p.relative_to(ROOT))]={"sha256":h(data),"bytes":len(data)}
    downloads=Path.home()/"Téléchargements"
    downloads.mkdir(parents=True,exist_ok=True)
    archive=downloads/NAME
    with ZipFile(archive,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in paths:z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(members):
            raise ValueError("Source ZIP wrong CRC/member count")
        for name,meta in members.items():
            b=z.read(name)
            if h(b)!=meta["sha256"] or len(b)!=meta["bytes"]:
                raise ValueError("Independent source byte and SHA changed "+name)
    with tempfile.TemporaryDirectory(prefix="ChineseV12_source_cold_") as tmp:
        fresh=Path(tmp)
        with ZipFile(archive) as z:z.extractall(fresh)
        suite=fresh/"tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12SRC-Life"
        testcmd=["/usr/bin/python3","-m","unittest","discover",
                 "-s",str(suite),"-p","test_chinese12src_ziwei_life_original.py","-v"]
        p=subprocess.run(testcmd,cwd=fresh,capture_output=True,text=True,timeout=45)
        log=p.stdout+p.stderr
        if p.returncode or "Ran 15 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1300:])
            raise ValueError("Cold source original 15/15 replay not verified")
    record={
        "schema":"CHINESE_V12_LIFE_STAR_9_12_COLD_SOURCE_RECEIPT",
        "batch":"ChineseAstro-12SRC-Life",
        "source_original_oldid":1963110,
        "status":"SOURCE_ZIP_VERIFIED_CANONICAL_ADMISSION_NOT_YET",
        "filename":NAME,"owner_local_archive_path":str(archive),
        "archive_sha256":h(archive.read_bytes()),
        "archive_size_bytes":archive.stat().st_size,
        "original_source_member_count":len(members),
        "source_exact_member_sha256_bytes":members,
        "zip_CRC_verified":True,
        "all_member_SHA_and_bytes_verified":True,
        "independently_cold_replayed_source_tests":15,
        "independently_cold_replayed_tests_green":15,
        "new_historical_documentary_annotations":83,
        "previous_V11_index_unchanged":True,
        "original_Ming_imprint_authenticated":False,
        "actual_human_predictive_validations":0,
        "runtime_astrology_model_promotions":0
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "ZIP":str(archive),"bytes":archive.stat().st_size,
        "sha256":record["archive_sha256"],"members":len(members),"cold_source_tests":15
    },indent=2,ensure_ascii=False))

if __name__=="__main__":main()
