#!/usr/bin/env python3
"""Build hash/CRC-verified cold-replay archive of pinned Di Tian Sui 19 Wikitext."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = Path("tasks/astro-chinese-primary-sources-20261017")
REL = T/"batches/ChineseAstro-25SRC-BaZi-SourceFlow"
DEST = Path("/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-SourceFlow-6-Original-Notes-V25-20261021.zip")
FILES = [
    T/"CHINESE_SOURCE_AUDIT_INDEX_V24.json",
    T/"batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json",
    Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
] + [REL/name for name in (
    "WRITER_LEASE.json",
    "WORKING_CHECKPOINT_20261021.md",
    "PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json",
    "evidence/DiTianSui_19_oldid844368.wikitext",
    "BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json",
    "SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_bazi19_source.py",
    "test_bazi25_original_source.py",
    "build_bazi25_portable_archive.py",
)]
def sha(b:bytes)->str:
    return sha256(b).hexdigest()

def main()->None:
    if DEST.exists():
        raise ValueError("Owner archive already exists; inspect receipt before overwriting")
    if not DEST.parent.is_dir():
        raise ValueError("Expected owner Downloads folder unavailable")
    files={}
    for rel in FILES:
        p=ROOT/rel
        if not p.is_file():
            raise ValueError("Source fixture absent: "+str(rel))
        blob=p.read_bytes()
        files[rel.as_posix()]={"sha256":sha(blob),"UTF8_or_raw_bytes":len(blob)}
    man={"schema":"BAZI_DTS19_SOURCE_FLOW_COLD_REPRODUCIBLE_ARCHIVE_V1",
         "source_oldid":844368,
         "source_raw_SHA256":"032a772c550dedb35aa130b835bb12d09dd3f3e89652aea382d7b00587ccf28d",
         "source_components":{"verse":1,"commentary":3,"four_pillar_chart_tables":2},
         "two_historical_case_outcomes_not_independently_verified":True,
         "ancient_print_origin_authentication":False,
         "real_human_blind_predictions_validated":0,
         "runtime_astrology_promotions":0,
         "original_file_SHA256_and_byte_sizes":files}
    readme=(
        "# Di Tian Sui section 19 Source and Flow source evidence\n\n"
        "Read batch ORIGINAL_SOURCE_REVIEW_20261021.md first. "
        "Original Wikitext is revision oldid844368, not an authenticated ancient printing.\n"
        "After extracting ZIP run:\n"
        "python3 -m unittest discover -s tasks/astro-chinese-primary-sources-20261017/"
        "batches/ChineseAstro-25SRC-BaZi-SourceFlow -p test_bazi25_original_source.py -v\n\n"
        "Two historical case examples have no independent birth or outcome verification.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILES:
            z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(man,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
            raise ValueError("ZIP CRC or member inventory failed")
        for name,proof in files.items():
            raw=z.read(name)
            if (sha(raw),len(raw))!=(proof["sha256"],proof["UTF8_or_raw_bytes"]):
                raise ValueError("Source archive SHA/size mismatch "+name)
    with tempfile.TemporaryDirectory(prefix="bazi-dts19-cold-") as temp:
        out=Path(temp)/"extracted"
        out.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(out)
        for name,proof in files.items():
            blob=(out/name).read_bytes()
            if (sha(blob),len(blob))!=(proof["sha256"],proof["UTF8_or_raw_bytes"]):
                raise ValueError("Cold source component SHA/size mismatch "+name)
        replay=subprocess.run([sys.executable,"-m","unittest","discover",
            "-s",REL.as_posix(),"-p","test_bazi25_original_source.py","-v"],
            cwd=out,capture_output=True,text=True)
        log=replay.stdout+replay.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if replay.returncode or replay.stderr.count(" ... ok")!=11 or "Ran 11 tests" not in replay.stderr:
            raise ValueError("Cold extracted source tests failed: "+log[-1600:])
    receipt={
        "batch":"ChineseAstro-25SRC-BaZi-SourceFlow",
        "status":"PINNED_SOURCE_ARCHIVE_CRC_SHA_COLD_11_TESTS_GREEN",
        "local_archive_path":str(DEST),"filename":DEST.name,
        "archive_SHA256":sha(DEST.read_bytes()),
        "archive_bytes":DEST.stat().st_size,
        "archive_members":len(FILES)+2,
        "ZIP_CRC_verified":True,
        "member_SHA256_byte_sizes_verified":True,
        "cold_extracted_source_test_green":11,
        "ancient_original_print_authenticity_verified":False,
        "real_human_blind_forecast_validations":0,
        "runtime_astrological_promotions":0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
