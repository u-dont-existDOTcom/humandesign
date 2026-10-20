#!/usr/bin/env python3
"""Independent cold-extracted Chinese Zi Wei first four life-star text source ZIP.

Source text, canonical prior index, all 89 full byte-offset original quotes,
UTF-8 SHA witnesses and source-focused tests; no unrelated binaries or
human-predictive outcomes. Source is transmitted online text, not Ming imprint.
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
TASK=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD_INDEX=TASK/"CHINESE_SOURCE_AUDIT_INDEX_V9.json"
SRC=TASK/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREV=TASK/"batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
FILENAME="Astrology-ZiWei-Original-Life-Palace-Four-Stars-89-Sources-V10-20261020.zip"


def hash_bytes(raw):
    return sha256(raw).hexdigest()


def main():
    required=[OLD_INDEX,SRC,PREV,WEST]
    local=[
        p for p in B.rglob("*")
        if p.is_file() and p.suffix.lower() in (".py",".json",".md",".txt")
        and "__pycache__" not in str(p)
        and "recovery" not in str(p)
        and p.name not in (
            "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json",
            "CANONICAL_PREPARE_RECEIPT_20261020.json",
            "ACCEPTED_CONTINUATION_CHECKPOINT_20261020.json"
        )
    ]
    paths=sorted(set(required+local),key=lambda p:str(p.relative_to(ROOT)))
    manifests={}
    for p in paths:
        raw=p.read_bytes()
        manifests[str(p.relative_to(ROOT))]={"sha256":hash_bytes(raw),"bytes":len(raw)}
    downloads=Path.home()/"Téléchargements"
    downloads.mkdir(parents=True,exist_ok=True)
    archive=downloads/FILENAME
    with ZipFile(archive,"w",ZIP_DEFLATED,compresslevel=3) as z:
        for p in paths:
            z.write(p,arcname=str(p.relative_to(ROOT)))
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist())!=sorted(manifests):
            raise ValueError("Source archive member names or ZIP CRC invalid")
        for name,ref in manifests.items():
            b=z.read(name)
            if hash_bytes(b)!=ref["sha256"] or len(b)!=ref["bytes"]:
                raise ValueError("Source ZIP member exact bytes/SHA mismatch "+name)
    with tempfile.TemporaryDirectory(prefix="chinese10_source_cold_") as d:
        fresh=Path(d)
        with ZipFile(archive) as z:z.extractall(fresh)
        testdir=fresh/"tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-10SRC-Life"
        cmd=["/usr/bin/python3","-m","unittest","discover","-s",str(testdir),
             "-p","test_chinese10src_ziwei_life_original.py","-v"]
        completed=subprocess.run(cmd,cwd=fresh,capture_output=True,text=True,timeout=45)
        log=completed.stdout+completed.stderr
        if completed.returncode!=0 or "Ran 17 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1600:])
            raise ValueError("Independent cold ZIP source 17/17 replays failed")
    meta={
        "schema":"CHINESEASTRO_10SRC_LIFE_COLD_SOURCE_ARCHIVE_RECEIPT",
        "batch":"ChineseAstro-10SRC-Life",
        "original_Chinese_witness_oldid":1963110,
        "status":"PORTABLE_VERIFIED_NOT_YET_INDEX_ADMITTED",
        "filename":FILENAME,
        "archive_path_on_owner_machine":str(archive),
        "archive_sha256":hash_bytes(archive.read_bytes()),
        "archive_size_bytes":archive.stat().st_size,
        "source_zip_member_count":len(manifests),
        "individual_member_sha256_and_bytes":manifests,
        "ZIP_CRC_validated":True,
        "ZIP_member_SHA_and_bytes_validated":True,
        "independently_extracted_test_count":17,
        "independently_extracted_tests_all_green":True,
        "historical_source_annotations_provisional":89,
        "earlier_V9_index_untouched":True,
        "early_Ming_original_imprint_authenticated":False,
        "human_personality_fate_predictive_validations":0,
        "runtime_astrological_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
        json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "ZIP":str(archive),"bytes":archive.stat().st_size,
        "sha256":meta["archive_sha256"],"members":len(manifests),
        "cold_tests_green":17
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
