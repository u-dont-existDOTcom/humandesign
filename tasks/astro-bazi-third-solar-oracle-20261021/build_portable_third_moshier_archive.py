#!/usr/bin/env python3
"""ZIP of synthetic source-evidence + cold replay; external Moshier binary NOT shipped."""
from __future__ import annotations
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
TASK=Path("tasks/astro-bazi-third-solar-oracle-20261021")
PARENT=Path("tasks/astro-bazi-fourpillars-jieqi-20261021")
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-Third-Moshier-Jieqi-36-Source-Compare-20261021.zip")
FILES=[
    Path("tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"),
    PARENT/"BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json",
]+[TASK/name for name in (
    "WRITER_LEASE.json",
    "WORKING_CHECKPOINT_20261021.md",
    "THIRD_EPHEMERIS_PIN_MANIFEST_V1.json",
    "BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json",
    "solve_third_moshier_solar_term.py",
    "test_third_moshier_solar_term.py",
    "THREE_SOFTWARE_SOLAR_TERM_SOURCE_CRITICAL_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_AND_HUMAN_LIMITS_V1.json",
    "build_portable_third_moshier_archive.py",
)]
PARENT_REPORT_SHA="bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e"
THIRD_REPORT_SHA="48d9b068797c4ef2209761c4d94532d035e26205b48c8f3cfb250c61722d06b1"

def sha(blob:bytes)->str:
    return sha256(blob).hexdigest()

def main()->None:
    if DEST.exists():
        raise ValueError("Owner source evidence ZIP already exists; inspect receipt, do not overwrite")
    witnesses={}
    for rel in FILES:
        source=ROOT/rel
        if not source.is_file():
            raise ValueError("Expected original source/reproducibility fixture missing "+str(rel))
        raw=source.read_bytes()
        witnesses[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
    if witnesses[(PARENT/"BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json").as_posix()]["sha256"]!=PARENT_REPORT_SHA:
        raise ValueError("Previous accepted 516-case fixture changed")
    if witnesses[(TASK/"BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json").as_posix()]["sha256"]!=THIRD_REPORT_SHA:
        raise ValueError("Third software comparison no longer source-locked")
    manifest={
        "schema":"THIRD_MOSHIER_JIEQI_36_PRESELECTED_SYNTHETIC_SOURCE_ARCHIVE_V1",
        "status":"ENGINEERING_ONLY_NOT_REAL_PEOPLE_OR_ASTROLOGICAL_ACCURACY",
        "original_parent_two_witness_report_sha256":PARENT_REPORT_SHA,
        "third_ephemeris_result_sha256":THIRD_REPORT_SHA,
        "original_source_Chinese_V30_historical_notes":1289,
        "original_6_JieQi_solar_term_days":6,
        "original_36_fictional_two_library_comparison_clocks":36,
        "two_library_older_nonunanimity_samples":4,
        "three_library_nonunanimity_samples":5,
        "two_calendar_libraries_consensus_against_Moshier_samples":1,
        "pysweph_version":"2.10.3.6",
        "Swiss_Ephemeris_Moshier_returned_flag_numeric":260,
        "vendor_compiled_binaries_included":False,
        "external_vendor_pinned_source_required_for_cold_execution":True,
        "real_human_blind_predictive_successes":0,
        "production_astrology_promotions":0,
        "source_file_witnesses":witnesses,
    }
    readme=(
        "# BaZi JieQi six dates, third solar longitude numerical witness\n\n"
        "Read THREE_SOFTWARE_SOLAR_TERM_SOURCE_CRITICAL_REVIEW_20261021.md first. "
        "These are 36 fictional UTC+08 clock readings, not real individual natal charts.\n"
        "This ZIP intentionally does NOT redistribute third-party compiled .so modules. "
        "For cold replay the same pinned pysweph==2.10.3.6 binary is expected on "
        "the owner's authorized machine under /tmp/hd-bazi-third-ephemeris-20261021; "
        "its exact SHA/bytes are specified in THIRD_EPHEMERIS_PIN_MANIFEST_V1.json.\n"
        "At archive root with that external dependency:\n"
        "PYTHONPATH=/tmp/hd-bazi-third-ephemeris-20261021:"
        "./tasks/astro-bazi-third-solar-oracle-20261021 "
        "python3 -m unittest discover -s tasks/astro-bazi-third-solar-oracle-20261021 "
        "-p test_third_moshier_solar_term.py -v\n"
        "No original Chinese printed book authentication or human predictive validation.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILES:
            z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
            raise ValueError("Third-witness source ZIP member CRC/inventory failed")
        for rel,proof in witnesses.items():
            raw=z.read(rel)
            if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Source archive member SHA/size differs: "+rel)
    with tempfile.TemporaryDirectory(prefix="bazi-jieqi-third-cold-") as t:
        output=Path(t)/"unpacked";output.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(output)
        for rel,proof in witnesses.items():
            raw=(output/rel).read_bytes()
            if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Cold extracted original source SHA differs: "+rel)
        env={**os.environ}
        local_vendor="/tmp/hd-bazi-third-ephemeris-20261021"
        if not Path(local_vendor).is_dir():
            raise ValueError("Owner external Moshier pin unavailable; no cold replay success claim")
        env["PYTHONPATH"]=local_vendor+":"+str(output/TASK)
        proc=subprocess.run([
            sys.executable,"-m","unittest","discover","-s",TASK.as_posix(),
            "-p","test_third_moshier_solar_term.py","-v"
        ],cwd=output,capture_output=True,text=True,env=env)
        log=proc.stdout+proc.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if proc.returncode!=0 or proc.stderr.count(" ... ok")!=22 or "Ran 22 tests" not in proc.stderr:
            raise ValueError("Independent third source cold replay did not pass 22/22: "+log[-2600:])
    receipt={
        "schema":"BAZI_THIRD_MOSHIER_JIEQI_INDEPENDENT_ARCHIVE_RECEIPT_V1",
        "status":"CRC_SHA_AND_22_INDEPENDENT_COLD_TESTS_GREEN",
        "owner_archive_path":str(DEST),
        "archive_filename":DEST.name,
        "archive_sha256":sha(DEST.read_bytes()),
        "archive_bytes":DEST.stat().st_size,
        "archive_members":len(FILES)+2,
        "ZIP_CRC_verified":True,
        "each_archive_member_SHA256_and_bytes_verified":True,
        "cold_replay_source_tests_green":22,
        "external_vendor_pinned_binary_not_redistributed":True,
        "pysweph_version":"2.10.3.6",
        "third_comparison_exact_5_nonunanimous_clock_records":True,
        "independent_printed_Chinese_original_authenticated":False,
        "actual_real_human_blind_predictions_validated":0,
        "production_astrology_rules_promoted":0,
    }
    (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
