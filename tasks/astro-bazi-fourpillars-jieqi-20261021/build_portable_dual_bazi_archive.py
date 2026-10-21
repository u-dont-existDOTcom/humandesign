#!/usr/bin/env python3
"""Portable source-parity analysis evidence, not redistributable third-party binaries."""
from __future__ import annotations
from hashlib import sha256
import json,os
from pathlib import Path
import subprocess,sys,tempfile
from zipfile import ZipFile,ZIP_DEFLATED

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
T=Path("tasks/astro-bazi-fourpillars-jieqi-20261021")
DEST=Path("/home/joel/Téléchargements/Astrology-BaZi-FourPillars-Jieqi-516-Synthetic-Parity-20261021.zip")
FILES=[
    Path("tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"),
]+[T/name for name in (
    "WORKING_CHECKPOINT_20261021.md",
    "BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json",
    "dual_witness_bazi_fourpillars.py",
    "run_fictional_fourpillars_parity.py",
    "test_bazi_fourpillars_jieqi.py",
    "SCIENCE_VS_ENGINEERING_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_AND_HUMAN_LIMITS.json",
    "build_portable_dual_bazi_archive.py",
)]

def sha(b:bytes)->str:return sha256(b).hexdigest()

def main():
    if DEST.exists():
        raise ValueError("Owner ZIP already exists; inspect receipt before overwrite")
    witnesses={}
    for rel in FILES:
        p=ROOT/rel
        if not p.is_file():
            raise ValueError("Missing source/package member "+str(rel))
        b=p.read_bytes()
        witnesses[rel.as_posix()]={"sha256":sha(b),"bytes":len(b)}
    manifest={
        "schema":"BAZI_516_SYNTHETIC_FIXED_UTC8_FOURPILLARS_PARITY_COLD_ARCHIVE_V1",
        "owner_scope":"DEVELOPMENT_ONLY_NOT_HUMAN_ASTROLOGY_PREDICTION",
        "original_accepted_Chinese_V30_index_SHA256":"6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de",
        "fixture_SHA256":"bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e",
        "480_random_fictional_samples":480,
        "36_precise_Jie_term_fictional_boundaries":36,
        "naive_date_only_ordinary_misses":8,
        "corrected_ordinary_misses":0,
        "precise_solar_term_crossings_with_source_software_disagreement":4,
        "optional_external_dependencies":{"lunar-python":"1.4.8","sxtwl":"2.0.7"},
        "external_libraries_or_binaries_included":False,
        "ancient_original_calendar_text_authenticated":False,
        "real_human_blind_validations":0,"runtime_promotions":0,
        "files":witnesses,
    }
    readme=(
        "# BaZi exact JieQi 516 fictional synthetic four-pillar comparisons\n\n"
        "See SCIENCE_VS_ENGINEERING_REVIEW_20261021.md for meaning and critical limits. "
        "This archive NEVER includes or validates a real person's birth chart.\n"
        "The exact versions of two independently used calendar libraries must be "
        "installed by the archive reader externally. Their SHA/byte witnesses "
        "are stored in the output fixture, but no third-party binaries are redistributed.\n"
        "From extracted root (set PYTHONPATH with externally pinned libraries "
        "and the extracted task folder), run:\n"
        "PYTHONPATH=/path/to/pinned_calendar_packages:"
        "./tasks/astro-bazi-fourpillars-jieqi-20261021 "
        "python3 -m unittest discover -s tasks/astro-bazi-fourpillars-jieqi-20261021 "
        "-p test_bazi_fourpillars_jieqi.py -v\n"
        "Only synthetic UTC+8 reference-clock inputs. Never claim traditional "
        "original historical source or real human prediction is verified.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILES)+2:
            raise ValueError("ZIP CRC/member count check failed")
        for rel,w in witnesses.items():
            data=z.read(rel)
            if (sha(data),len(data))!=(w["sha256"],w["bytes"]):
                raise ValueError("Original source member mutated inside archive "+rel)
    with tempfile.TemporaryDirectory(prefix="bazi-jieqi-516-cold-") as t:
        root=Path(t)/"extract";root.mkdir()
        with ZipFile(DEST) as z:z.extractall(root)
        for rel,w in witnesses.items():
            data=(root/rel).read_bytes()
            if (sha(data),len(data))!=(w["sha256"],w["bytes"]):
                raise ValueError("Extracted evidence changed "+rel)
        env={**os.environ}
        external="/tmp/hd-calendar-parity-20261020"
        if not Path(external).is_dir():
            raise ValueError("Pinned local dependency set not available for independent cold replay")
        env["PYTHONPATH"]=external+":"+str(root/T)
        command=[sys.executable,"-m","unittest","discover",
                 "-s",T.as_posix(),"-p","test_bazi_fourpillars_jieqi.py","-v"]
        proc=subprocess.run(command,cwd=root,capture_output=True,text=True,env=env)
        log=proc.stdout+proc.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if proc.returncode!=0 or proc.stderr.count(" ... ok")!=18 or "Ran 18 tests" not in proc.stderr:
            raise ValueError("Independent extracted source+mutant tests failed: "+log[-2500:])
    receipt={
        "schema":"BAZI_516_SYNTHETIC_FOURPILLARS_COLD_ARCHIVE_RECEIPT_V1",
        "status":"EXTRACTED_CRC_ALL_MEMBER_SHA_18_INDEPENDENT_TESTS_GREEN",
        "owner_local_archive_path":str(DEST),
        "archive_sha256":sha(DEST.read_bytes()),"archive_bytes":DEST.stat().st_size,
        "archive_members":len(FILES)+2,
        "all_archive_members_sha256_bytes_verified":True,
        "archive_CRC_verified":True,
        "independent_cold_original_source_parity_tests_green":18,
        "external_pin_versions_pinned_but_not_redistributed":True,
        "historical_original_printing_authenticated":False,
        "independent_real_human_blind_predictive_validations":0,
        "runtime_astrological_promotions":0,
    }
    (B/"COLD_ARCHIVE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
