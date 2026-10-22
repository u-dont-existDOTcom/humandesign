#!/usr/bin/env python3
"""Source-locked SWIEPH file-backed fourth backend evidence ZIP + cold tests.

Vendor .se1 and compiled .so remain in owner's authorized existing folders,
not redistributed in this evidence archive. 21 tests replay from extraction.
"""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,os,subprocess,sys,tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
T=Path("tasks/astro-bazi-swieph-fourth-oracle-20261021")
PRIOR=Path("tasks/astro-bazi-third-solar-oracle-20261021")
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-Fourth-SWIEPH-36-JieQi-Source-20261021.zip")
INPUTS=[
    Path("tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"),
    PRIOR/"BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json",
    PRIOR/"THIRD_EPHEMERIS_PIN_MANIFEST_V1.json",
]+[T/name for name in (
    "WRITER_LEASE.json","WORKING_CHECKPOINT_20261021.md",
    "FOURTH_SWIEPH_SOURCE_PIN_MANIFEST.json",
    "calculate_swieph_fourth_oracle.py",
    "BAZI_FOURTH_SWIEPH_6_TERMS_36_FICTIONAL_CLOCKS_V1.json",
    "test_fourth_swieph_source.py",
    "SWIEPH_FOURTH_SOLAR_ORACLE_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_AND_HUMAN_LIMITS_V1.json",
    "build_portable_swieph_fourth_archive.py",
)]
PARENT_SHA="48d9b068797c4ef2209761c4d94532d035e26205b48c8f3cfb250c61722d06b1"
REPORT_SHA="7826f65e9dbff6142064a356c55c61a0ba659d423490bb59775dd0f563dd7e0d"

def sha(b:bytes)->str:return sha256(b).hexdigest()

def main():
    if DEST.exists():raise ValueError("Owner archived source already exists: do not overwrite/re-run")
    witness={}
    for rel in INPUTS:
        path=ROOT/rel
        if not path.is_file():raise ValueError("Missing original fourth witness artifact: "+str(rel))
        blob=path.read_bytes()
        witness[rel.as_posix()]={"sha256":sha(blob),"bytes":len(blob)}
    if witness[(PRIOR/"BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json").as_posix()]["sha256"]!=PARENT_SHA:
        raise ValueError("Original Moshier 36 clocks fixture missing or changed")
    if witness[(T/"BAZI_FOURTH_SWIEPH_6_TERMS_36_FICTIONAL_CLOCKS_V1.json").as_posix()]["sha256"]!=REPORT_SHA:
        raise ValueError("Original new SWIEPH fourth report source SHA changed")
    manifest={
        "schema":"SWIEPH_FOURTH_JIEQI_36_SYNTHETIC_EVIDENCE_ARCHIVE_V1",
        "historical_Chinese_source_index_annotations":1289,
        "old_third_Moshier_original_source_SHA256":PARENT_SHA,
        "new_SWIEPH_original_36_comparison_SHA256":REPORT_SHA,
        "source_SWIEPH_returned_flag":258,
        "Moshier_original_returned_flag":260,
        "fictional_precise_term_dates":6,
        "fictional_challenge_clocks":36,
        "SWIEPH_four_source_nonunanimous_samples":5,
        "two_calendar_consensus_2057_crossing_before_SWIEPH":True,
        "third_party_vendor_ephemeris_binary_files_included":False,
        "external_pinned_Swiss_planetary_se1_and_pysweph_needed":True,
        "ancient_Chinese_original_historical_calendar_authenticated":False,
        "real_blinded_human_predictive_validations":0,
        "runtime_astrology_model_promotions":0,
        "file_SHA256_and_byte_witnesses":witness
    }
    readme=(
        "# BaZi SWIEPH fourth software backend exact solar-term comparisons\n\n"
        "All dates are fictional fixed UTC+8 reference clocks, not people. "
        "Source critical review: SWIEPH_FOURTH_SOLAR_ORACLE_SOURCE_REVIEW_20261021.md.\n"
        "Archive omits third-party binary ephemeris data under owner existing "
        "/home/joel/humandesign/data/ephemeris and external source-pinned "
        "pysweph binary under /tmp/hd-bazi-third-ephemeris-20261021; "
        "full source hashes/versions are in FOURTH_SWIEPH_SOURCE_PIN_MANIFEST.json.\n"
        "To replay from archive root on owner's configured computer:\n"
        "PYTHONPATH=/tmp/hd-bazi-third-ephemeris-20261021:"
        "./tasks/astro-bazi-swieph-fourth-oracle-20261021 "
        "python3 -m unittest discover -s tasks/astro-bazi-swieph-fourth-oracle-20261021 "
        "-p test_fourth_swieph_source.py -v\n"
        "No original printed Chinese astrology or human predictions validated.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in INPUTS:z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(INPUTS)+2:
            raise ValueError("Fourth source ZIP CRC/inventory invalid")
        for path,proof in witness.items():
            b=z.read(path)
            if (sha(b),len(b))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Archived original file modified: "+path)
    with tempfile.TemporaryDirectory(prefix="bazi-swieph-fourth-cold-") as tmp:
        dest=Path(tmp)/"extracted";dest.mkdir()
        with ZipFile(DEST) as z:z.extractall(dest)
        for path,proof in witness.items():
            raw=(dest/path).read_bytes()
            if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Cold original source member differs: "+path)
        env={**os.environ}
        old_vendor=Path("/tmp/hd-bazi-third-ephemeris-20261021")
        if not old_vendor.is_dir():
            raise ValueError("Pinned external Swiss wrapper absent; cannot claim cold replay")
        env["PYTHONPATH"]=str(old_vendor)+":"+str(dest/T)
        proc=subprocess.run([
            sys.executable,"-m","unittest","discover","-s",T.as_posix(),
            "-p","test_fourth_swieph_source.py","-v"
        ],cwd=dest,capture_output=True,text=True,env=env)
        log=proc.stdout+proc.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if proc.returncode!=0 or proc.stderr.count(" ... ok")!=21 or "Ran 21 tests" not in proc.stderr:
            raise ValueError("Fourth source independent cold replay failed 21/21: "+log[-2100:])
    receipt={
        "schema":"BAZI_SWIEPH_FOURTH_SOURCE_ARCHIVE_RECEIPT_V1",
        "status":"SOURCE_BYTES_CRC_SHA_AND_21_COLD_TESTS_PASSED",
        "owner_archive_path":str(DEST),"archive_filename":DEST.name,
        "archive_sha256":sha(DEST.read_bytes()),
        "archive_bytes":DEST.stat().st_size,"archive_members":len(INPUTS)+2,
        "ZIP_CRC_verified":True,"source_members_sha256_and_bytes_verified":True,
        "independent_cold_source_tests_green":21,
        "SWIEPH_file_returnflags":258,
        "third_party_compiled_or_ephemeris_files_distributed":False,
        "SWIEPH_vs_Moshier_2057_disagreement_consistent":True,
        "real_human_blind_predictive_validations":0,
        "runtime_astrology_promotions":0,
    }
    (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
