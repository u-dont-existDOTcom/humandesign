#!/usr/bin/env python3
"""Portable Maya codex visual facsimile packet, not original glyph decipherment.
Includes TWO FAMSI page PNGs + source hashes/notes, but excludes 36MB PDFs.
"""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile,ZIP_DEFLATED
import json,os,subprocess,sys,tempfile

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
TASK=Path("tasks/astro-maya-dresden-facsimile-page24-20261022")
OLD=Path("tasks/astro-maya-dresden-original-folio-20261022")
MAP=Path("tasks/astro-multitradition-source-coverage-20261022")
HOME=Path("/home/joel/Téléchargements")
DEST=HOME/"Astrology-Maya-Dresden-Venus-Folios24-46-Facsimile-20261022.zip"
SOURCE=TASK/"DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json"
FILES=[
    OLD/"DRESDEN_FOLIO_SOURCE_WINDOWS_V1.json",
    OLD/"FIRST_FOLIO_PROVENANCE_HANDOFF_20261022.md",
    MAP/"MULTITRADITION_SOURCE_TO_TEST_MAP.md",
]+[TASK/f for f in (
    "WRITER_LEASE.json","WORKING_CHECKPOINT_20261022.md",
    "DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json",
    "DRESDEN_FOLIOS24_46_SOURCE_CRITICAL_REVIEW_20261022.md",
    "pin_dresden_venus_folio_images.py",
    "test_dresden_venus_folio_visual_source.py",
    "build_portable_dresden_folio_visual_archive.py",
)]
def sha(raw:bytes)->str:return sha256(raw).hexdigest()
def main():
    if DEST.exists():raise ValueError("Existing owner Maya packet; inspect, do not overwrite")
    doc=json.loads((ROOT/SOURCE).read_text(encoding="utf-8"))
    entries={}
    for rel in FILES:
        f=ROOT/rel
        if not f.is_file():raise ValueError("Required source artifact missing: "+str(rel))
        blob=f.read_bytes()
        entries[rel.as_posix()]={"sha256":sha(blob),"bytes":len(blob)}
    if doc["independently_transcribed_Maya_hieroglyph_signs"]!=0 or len(doc["source_witnesses"])!=2:
        raise ValueError("Original source evidence class changed")
    image_map={}
    for x in doc["source_witnesses"]:
        original=HOME/x["page_png"]
        if not original.is_file() or sha(original.read_bytes())!=x["render_sha256"]:
            raise ValueError("Pinned original facsimile page image unavailable or changed")
        member=(TASK/"evidence"/x["page_png"]).as_posix()
        blob=original.read_bytes()
        if member in entries:raise ValueError("Duplicate PDF page source ID")
        image_map[member]=original
        entries[member]={"sha256":sha(blob),"bytes":len(blob)}
    manifest={
        "schema":"MAYA_DRESDEN_FOERSTEMANN_1892_P24_P46_VISUAL_REFERENCE_ZIP_V1",
        "status":"TWO_FACSIMILE_VISUAL_IMAGES_HASHED_NO_ORIGINAL_MAYA_GLYPH_DECIPHERMENT",
        "original_facsimile_pdf_sources_not_embedded":True,
        "original_pdf_sha256_and_open_URLs_preserved_in_visual_witness_manifest":True,
        "original_Foerstemann_1892_visual_folio_count":2,
        "source_rendered_images_in_archive":len(image_map),
        "source_required_for_full_cold_test":"Two original FAMSI PDF inputs on the owner's Downloads folder, external; source images included",
        "codex_p24_46_source_excerpt_glyph_decipherment_promotions":0,
        "Maya_calendar_to_human_natal_trait_model_promotions":0,
        "genuine_human_blind_predictions":0,
        "file_sha256_and_bytes":entries,
    }
    readme=(
        "# Maya Dresden Codex p24/p46 facsimile evidence packet\n\n"
        "Original visual facsimile page images are inside this ZIP, along with "
        "Maya original-source windows, code, institutional bibliography and "
        "the pre-existing multi-tradition evidence map. Each image is a rendered "
        "1892 Förstemann facsimile, NOT the original handwritten codex photo.\n"
        "The two original FAMSI scan PDF sections (16.3 MB and 20.4 MB) are NOT "
        "duplicated here, but the source SHA and exact URLs plus owner-local "
        "PDF filenames are in DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json.\n"
        "Full tests need those two PDF originals still in ~/Téléchargements. "
        "From archive root: python3 -m unittest discover -s "
        "tasks/astro-maya-dresden-facsimile-page24-20261022 "
        "-p test_dresden_venus_folio_visual_source.py -v\n"
        "Do not interpret calendrical source windows as natal personality traits "
        "or scored human astrology without independently attested text & a blind study.\n"
    )
    with ZipFile(DEST,"w",compression=ZIP_DEFLATED,compresslevel=8) as z:
        for rel in FILES:z.write(ROOT/rel,arcname=rel.as_posix())
        for member,src in image_map.items():z.write(src,arcname=member)
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md",readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(entries)+2:
            raise ValueError("Maya original reference archive CRC/members failed")
        for member,w in entries.items():
            b=z.read(member)
            if (sha(b),len(b))!=(w["sha256"],w["bytes"]):
                raise ValueError("Archive member changed: "+member)
    with tempfile.TemporaryDirectory(prefix="maya-venus-firstfolios-cold-") as tmp:
        root=Path(tmp)/"unpacked";root.mkdir()
        with ZipFile(DEST) as z:z.extractall(root)
        for member,w in entries.items():
            data=(root/member).read_bytes()
            if (sha(data),len(data))!=(w["sha256"],w["bytes"]):
                raise ValueError("Independent cold extracted original source changed: "+member)
        proc=subprocess.run([sys.executable,"-m","unittest","discover",
          "-s",TASK.as_posix(),"-p","test_dresden_venus_folio_visual_source.py","-v"],
          cwd=root,capture_output=True,text=True,env=os.environ.copy())
        log=proc.stdout+proc.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261022.txt").write_text(log,encoding="utf-8")
        if proc.returncode!=0 or proc.stderr.count(" ... ok")!=11 or "Ran 11 tests" not in proc.stderr:
            raise ValueError("Cold visual + source tests failed: "+log[-2100:])
    receipt={
        "schema":"MAYA_DRESDEN_VENUS_P24_P46_VISUAL_ARCHIVE_RECEIPT_V1",
        "status":"FOLIO24_AND_46_FACSIMILE_HASH_CRC_COLD11_GREEN",
        "owner_archive_path":str(DEST),"archive_filename":DEST.name,
        "archive_sha256":sha(DEST.read_bytes()),"archive_bytes":DEST.stat().st_size,
        "archive_members":len(entries)+2,
        "source_facsimile_PNG_members":len(image_map),
        "original_PDFs_in_archive":False,
        "external_original_PDFs_verified_on_owner_machine":True,
        "ZIP_CRC_verified":True,"all_members_SHA256_and_bytes_verified":True,
        "cold_extracted_source_and_visual_tests_green":11,
        "independently_deciphered_Maya_original_glosses":0,
        "genuine_real_human_predictive_validations":0,
        "runtime_astrology_rule_promotions":0
    }
    (B/"SOURCE_ARCHIVE_RELEASE_RECEIPT_20261022.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
