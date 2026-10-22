#!/usr/bin/env python3
"""Deliver source-pinned cross-tradition Maya map with cold-reproducible tests.

Research-only. Does not redistribute the owner's copyrighted PDF/EPUB books,
Maya facsimile page images, compiled vendor libraries, or personal survey data.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,subprocess,sys,tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
MAP=Path("docs/astrology-research-map")
PACKAGE=Path("tasks/astro-multitradition-integrator-20261022")
DEST=Path("/home/joel/Téléchargements/Astrology-Maya-Reconciled-Books-Source-To-Test-Map-20261022.zip")
FILENAMES=[
    Path("ARCHITECTURE.md"),
    Path("reference/core/MAPPING_V2_EVIDENCE_PROTOCOL.md"),
    Path("docs/20_forward_blind_prospective_validation.md"),
]
FILENAMES += [
    p.relative_to(ROOT) for p in sorted((ROOT/MAP).iterdir())
    if p.is_file() and p.suffix in (".md",".json",".py",".mmd")
]
FILENAMES += [
    PACKAGE/"WORKING_CHECKPOINT_20261022.md",
    PACKAGE/"CONTINUATION_HANDOFF_ACCEPTED_20261022.md",
    PACKAGE/"build_portable_integrated_maya_source_map.py",
]
FILENAMES += [
    Path("tasks/astro-maya-comparative-map-20261022")/x for x in (
        "MAYA_LOCAL_SOURCE_INVENTORY_V1.json",
        "MAYA_SOURCE_FIRST_READING_AND_PARALLEL_MAP_ALIGNMENT_20261022.md",
        "EXACT_BOOK_TITLES_TO_SEARCH_20261022.md",
    )
]
FILENAMES += [
    Path("tasks/astro-multitradition-source-coverage-20261022")/x for x in (
        "MAYA_RANKED_SOURCE_REGISTER_V1.json",
        "ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json",
        "TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json",
        "MAYA_BOOKS_OTHER_SYSTEMS_AND_METHOD_20261022.md",
    )
]
FILENAMES += [
    Path("tasks/astro-maya-dresden-facsimile-page24-20261022")/x for x in (
        "DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json",
        "DRESDEN_FOLIOS24_46_SOURCE_CRITICAL_REVIEW_20261022.md",
        "MAYA_SOURCE_TO_TEST_MAP_DELTA_V2.json",
        "SOURCE_ARCHIVE_RELEASE_RECEIPT_20261022.json",
    )
]
EXPECTED_RECONCILED_SHA="1a99626ac5af6de94cda71745b28b0cfe02014f2ec8bef477206102decb1b8a6"
EXPECTED_LEDGER_SHA="474fd7557be4973771fb70e7001cb8014d96d68f1f4e7dc80a11e2f15a1e8d3e"
ORIGINAL_FILE_CONTENT_NOT_COPIED=["original local full PDF/EPUB files",
 "FAMSI/SLUB codex facsimile rendered images and full PDF",
 "private birth dates, questionnaire responses and names",
 "unlicensed fonts or compiled external vendor libraries"]

def sha(content):return sha256(content).hexdigest()
def main():
    if DEST.exists():
        raise ValueError("Owner ZIP exists; inspect the existing receipt and do not overwrite.")
    if not DEST.parent.is_dir():
        raise ValueError("Owner Downloads directory not mounted.")
    if len(FILENAMES)!=len(set(FILENAMES)):
        raise ValueError("Archive input list repeats a source document.")
    if sha((ROOT/MAP/"TRADITION_COVERAGE_RECONCILED_V2.json").read_bytes())!=EXPECTED_RECONCILED_SHA:
        raise ValueError("Reconciled book/map coverage source diverged before ZIP.")
    if sha((ROOT/MAP/"RECONCILED_SOURCE_TO_TEST_EVIDENCE_V1.json").read_bytes())!=EXPECTED_LEDGER_SHA:
        raise ValueError("Versioned source evidence ledger changed unexpectedly.")
    witness={}
    for rel in FILENAMES:
        file=ROOT/rel
        if not file.is_file():
            raise ValueError("Missing immutable source/companion file: "+str(rel))
        if file.suffix not in (".json",".md",".py",".mmd"):
            raise ValueError("Disallowed media/large copyrighted-original type: "+str(rel))
        raw=file.read_bytes()
        witness[rel.as_posix()]={"sha256":sha(raw),"bytes":len(raw)}
    manifest={
        "schema":"MAYA_MULTITRADITION_SINGLE_RECONCILED_MAP_SOURCE_ARCHIVE_V1",
        "owner_root_scientific_goal":"OPEN_REAL_HUMAN_CHART_BLIND_TEST_NOT_YET_EXECUTED",
        "one_canonical_candidate_Mermaid_workflow":str(MAP/"WORKFLOW.mmd"),
        "source_companion_protocol":"reference/core/MAPPING_V2_EVIDENCE_PROTOCOL.md",
        "original_imported_tradition_families":16,
        "source_imported_owned_nonfiction_Maya_books":4,
        "source_original_Dresden_facsimile_visual_pages":2,
        "original_glossed_Maya_glyph_decipherments":0,
        "source_exploratory_living_Maya_natal_claims":7,
        "cross_system_chart_behaviour_predictions_promoted":0,
        "real_human_blind_predictive_validations":0,
        "nonredistributed_material":ORIGINAL_FILE_CONTENT_NOT_COPIED,
        "source_file_SHA256_and_byte_sizes":witness,
    }
    readme=(
        "# Maya astrology owner reading plan + one cross-tradition map\n\n"
        "Start with docs/astrology-research-map/OWNER_GUIDE_MAYA_BOOKS_SYSTEMS_AND_RESEARCH_MAP_20261022.md.\n"
        "Open docs/astrology-research-map/README.md for Mermaid maps and source-claim evidence gates.\n"
        "The owner's existing four nonfiction Maya books remain outside this ZIP; "
        "no copyrighted full original, manuscript PDF, customer birth data or compiled binaries redistributed.\n"
        "Reproduce source-only checks from the archive root:\n"
        "python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -v\n"
        "The 37 tests establish document/provenance/calendar reference consistency, not human astrology accuracy.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
        for rel in FILENAMES:
            z.write(ROOT/rel,arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(FILENAMES)+2:
            raise ValueError("Original source ZIP CRC/inventory mismatch.")
        for name,proof in witness.items():
            raw=z.read(name)
            if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Archived source content SHA/byte mismatch: "+name)
    with tempfile.TemporaryDirectory(prefix="maya-one-map-cold-") as scratch:
        target=Path(scratch)/"root";target.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(target)
        for name,proof in witness.items():
            raw=(target/name).read_bytes()
            if (sha(raw),len(raw))!=(proof["sha256"],proof["bytes"]):
                raise ValueError("Cold-extracted source bytes differ: "+name)
        proc=subprocess.run([sys.executable,"-m","unittest","discover",
            "-s",MAP.as_posix(),"-p","test_*.py","-v"],
            cwd=target,capture_output=True,text=True)
        log=proc.stdout+proc.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261022.txt").write_text(log,encoding="utf-8")
        if proc.returncode or "Ran 37 tests" not in proc.stderr or proc.stderr.count(" ... ok")!=37:
            raise ValueError("Source-only cold ZIP test suite failed: "+log[-2200:])
    receipt={
        "schema":"MAYA_OWNER_RECONCILED_SOURCE_TO_TEST_MAP_RELEASE_RECEIPT_V1",
        "status":"INTEGRATED_SOURCE_SHA_CRC_AND_37_FOCUSED_37_INDEPENDENT_COLD_TESTS_GREEN",
        "owner_local_archive_path":str(DEST),
        "archive_bytes":DEST.stat().st_size,
        "archive_sha256":sha(DEST.read_bytes()),
        "archive_members":len(FILENAMES)+2,
        "source_item_count":len(FILENAMES),
        "every_original_member_SHA256_and_size_verified":True,
        "ZIP_CRC_verified":True,
        "focused_reconciled_map_tests_passed":37,
        "cold_independent_source_tests_passed":37,
        "owner_has_four_relevant_existing_nonfiction_books":True,
        "original_full_copyrighted_PDF_EPUB_content_not_redistributed":True,
        "real_human_blind_predictions_validated":0,
        "astrology_runtime_rules_promoted":0,
    }
    (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261022.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
