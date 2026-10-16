#!/usr/bin/env python3
"""Preserve 1647 printed heading repetitions without mutating accepted source records."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CORR=B/"ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json"
BEFORE=B/"recovery/LILLY_INDEX_BEFORE_ORIGINAL_PRINTED_HEADING_CORRECTION.json"
REC=B/"PRINTED_NUMBERING_CORRECTION_RECEIPT_20261016.json"
assert not BEFORE.exists() and not REC.exists()
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads(IDX.read_text());e=json.loads(CORR.read_text())
assert j["records_count"]==5080 and j["batches"][-1]["id"]=="B04f"
assert j["next"]["chapter"]=="LXXXVII" and j["next"]["pdf_page"]==490
assert j["read_numbered_chapters"]==list(range(1,87))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert [x["first_edition_heading"] for x in e["correspondence"]]==[
 "LXXXV","LXXXV","LXXXVI","LXXXVII","LXXXVIII"]
assert [x["editorial_sequence_id"] for x in e["correspondence"]]==[
 "LXXXV","LXXXVI","LXXXVII","LXXXVIII","LXXXIX"]
assert j["batches"][-1]["sha256"]=="42069ab80e3490645cffc385a62e726d902a8a1c43381d9294b78d2c521b59ae"
# Source images in accepted and navigation worktrees, not changed or duplicated.
sources={
 486:ROOT/"tasks/astro-source-audit-multipass-20261005/batches/B04d/evidence/pdf_1647-486.jpg",
 489:ROOT/"tasks/astro-source-audit-multipass-20261005/batches/B04f/evidence/pdf_1647-489.jpg",
 490:B/"evidence/pdf_1647-490.jpg",491:B/"evidence/pdf_1647-491.jpg",493:B/"evidence/pdf_1647-493.jpg"}
for c in e["correspondence"]:
 assert H(sources[c["original_pdf_page"]])==c["original_page_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
assert subprocess.check_output(["git","hash-object",str(IDX)],text=True).strip()==subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
BEFORE.parent.mkdir(parents=True,exist_ok=True);BEFORE.write_bytes(IDX.read_bytes())
j["read_numbered_chapters_basis"]="editorial_source_sequence_ordinals_not_literal_1647_headings"
j["original_printed_chapter_heading_crosswalk"]={
 "path":"batches/B04g/ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json",
 "sha256":H(CORR),"duplicate_printed_numeral":"LXXXV",
 "first_affected_editorial_sequence_id":"LXXXVI",
 "accepted_record_mapping":"R5027-R5080 retained as editorial LXXXVI despite original printed heading LXXXV",
 "next_editorial_alias":"LXXXVII","next_original_printed_numeral":"LXXXVI"}
j["next"]["printed_chapter_numeral"]="LXXXVI"
j["next"]["numbering_note"]="Editorial sequential LXXXVII but the original first-edition page says CHAP. LXXXVI after its repeated CHAP. LXXXV."
j["chapter_LXXXVI_source_acceptance_note"]+= " CORRECTION: this is a stable editorial SEQUENTIAL alias; original first edition printed CHAP. LXXXV again on PDF489/printed455. See original_printed_chapter_heading_crosswalk; source records and archive unchanged."
assert j["records_count"]==5080 and len(j["batches"])==len(json.loads(BEFORE.read_text())["batches"])
assert j["batches"][-1]==json.loads(BEFORE.read_text())["batches"][-1]
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
rec={"batch":"B04g","kind":"NONDESTRUCTIVE_ORIGINAL_PRINTED_NUMBERING_FIDELITY_CORRECTION",
 "prior_index_sha256":H(BEFORE),"corrected_index_sha256":H(IDX),
 "original_crosswalk_sha256":H(CORR),
 "duplicate_first_edition_heading":"LXXXV",
 "editorial_sequence_chapter_for_Irish_Queen":"LXXXVI",
 "original_printed_chapter_for_Irish_Queen":"LXXXV",
 "next_editorial_sequence_chapter":"LXXXVII",
 "next_original_printed_chapter":"LXXXVI",
 "accepted_R_records_rewritten":0,"existing_batch_hashes_changed":0,
 "historical_records_count":5080,"new_empirical_predictions":0}
REC.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(rec,indent=2))
