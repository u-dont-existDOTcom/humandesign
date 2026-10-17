from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04t_PLANETARY_TABLE_IMAGES.md"
OLD=B/"recovery/INDEX_BEFORE_B04t.json";BEFORE=B/"recovery/CURRENT_BEFORE_B04t.md"
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in (OLD,BEFORE,LATEST))
j=json.loads(IDX.read_text());a=json.loads((B/"ACCEPTANCE.json").read_text())
r=json.loads((B/"RULES.json").read_text());z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert j["records_count"]==5629 and j["batches"][-1]["id"]=="B04s"
assert j["next"]["chapter"]=="PLANETARY_HOUR_TABLE" and j["next"]["pdf_page"]==508
assert j["read_numbered_chapters"]==list(range(1,98))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert j["source_sha256"]==a["original_pdf_sha256"]
assert a["new_documentary_records"]==r["record_count"]==10 and a["lilly_if_published"]==5639
assert not a["numeric_cell_transcription_complete"] and not z["numeric_cells_fully_digitized"]
assert h(B/"RULES.json")==a["rules_sha256"]==z["rules_sha256"]
assert h(Path(z["owner_download_path"]))==z["archive_sha256"]
assert z["archive_tests_replayed"]==15 and z["member_sha256_pass"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parentblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert parentblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());BEFORE.write_bytes(CUR.read_bytes())
j["batches"].append({"id":"B04t","path":"batches/B04t/RULES.json","records_count":10,"sha256":a["rules_sha256"],
 "scope":"First-edition original Lilly printed planetary-hour table leaves 1-8 (original PDF508–515), preserved by eight exact original page-image hashes, 8 page-witness annotations and 2 following chapter navigation records; printed numeric cells NOT fully machine-transcribed/independently validated. Next printed XCVII PDF516."})
j["records_count"]=5639
j["status"]="BOOK_II_TABLE_IMAGE_WITNESSES_ADMITTED_NUMERIC_CELL_DIGITIZATION_OPEN_PRINTED_XCVII_NEXT"
j["next"]={"pdf_page":516,"printed_page":482,"chapter":"XCVIII",
 "printed_chapter_numeral":"XCVII",
 "heading":"To find out what Planet ruleth every hour of the Day or Night, by the preceding Table",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF516–520 explanatory final printed numbered chapter and Lilly's signed conclusion June 11, 1647; next book title PDF521.",
 "remaining_source_tasks":[{"type":"PRINTED_XCVII_METHOD_AND_CONCLUSION","start_pdf":516,"end_pdf":520},
 {"type":"ORIGINAL_TABLE_ALL_NUMERIC_CELLS_VERIFICATION","start_pdf":508,"end_pdf":515,"status":"OPEN"},
 {"type":"NEXT_BOOK_TITLE","pdf_page":521}]}
j["planetary_hour_table_source_acceptance_note"]="10 historical documentary annotations R5630–R5639: eight original table-page image witnesses + two next-chapter navigation markers; eight table pages PDF508–515 preserved by exact hashes; ~1,488 numeric hour boundaries NOT transcribed or independently checked. No empirical prediction or runtime promotion."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5639
assert j["read_numbered_chapters"]==list(range(1,98))
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
audit=(B/"TABLE_SOURCE_FIRST_AUDIT_20261017.md").read_text()
LATEST.write_text("# Lilly original 1647 planetary-hours table: full source images, incomplete numeric data\n\n"+audit+"\n**Documentary acceptance:** ten source records R5630–R5639 for eight original table leaves and two following chapter navigation markers, nine mapped primary image groups. All eight original scans plus next Chapter XCVII PDF516 SHA-frozen. There are approximately **1,488 numeric hour-boundary cells not all digitized**, so this is not a verified machine-readable table and cannot be promoted into the astrology runtime. Eighteen historical source/data limitations retained. Archive CRC, full extraction, member SHA-256s and fifteen tests replayed.\n\nAfter verified publication: **5,639 Lilly + 1,066 Ptolemy = 6,705 historical documentary annotations**; zero independent predictive validations and runtime promotions.\n\nNEXT printed Chapter XCVII/editorial XCVIII original PDF516–520 plus conclusion; further separate numeric table cell transcription remains OPEN. Book III starts PDF521.\n")
CUR.write_text("# Lilly Book II planetary-hour original scans preserved, numeric cells open\n\n2026-10-17: original table PDF508–515, 8 original leaves, 10 image/documentary records R5630-R5639 accepted locally (not numeric transcription); following printed Chapter XCVII begins PDF516, ends PDF520, Book III starts PDF521. After branch publication Lilly **5,639** + Ptolemy **1,066** = **6,705** historical records. Numeric table cells undigitized/unverified; no runtime or empirical results.\n\n---\n\n"+BEFORE.read_text())
rec={"batch":"B04t","status":"GUARDED_INDEX_PREPARED_PENDING_REMOTE",
 "parent_git_blob_sha1":parentblob,"previous_index_sha256":h(OLD),
 "new_index_sha256":h(IDX),"current_sha256":h(CUR),"report_sha256":h(LATEST),
 "rules_sha256":a["rules_sha256"],"owner_archive_sha256":z["archive_sha256"],
 "documentary_records_added":10,"lilly_if_published":5639,
 "retained_ptolemy":1066,"combined_if_published":6705,
 "source_original_scan_pages_complete":True,"numeric_cell_transcription_complete":False,
 "next_editorial_chapter":"XCVIII","next_printed_chapter":"XCVII","next_original_pdf_page":516,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
