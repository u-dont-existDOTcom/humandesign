from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04u_CHAPTER_XCVIII_COMPLETE.md"
OLD=B/"recovery/INDEX_BEFORE_B04u.json";PREV=B/"recovery/CURRENT_BEFORE_B04u.md"
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in (OLD,PREV,LATEST))
I=json.loads(IDX.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5639 and I["batches"][-1]["id"]=="B04t"
assert I["next"]["chapter"]=="XCVIII" and I["next"]["pdf_page"]==516
assert I["read_numbered_chapters"]==list(range(1,98))
assert I["source_sha256"]==A["original_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert R["record_count"]==A["new_documentary_records"]==114
assert [r["record_number"] for r in R["rules"]]==list(range(5640,5754))
assert all(r["printed_pages"]==[None] for r in R["rules"][-5:])
assert A["lilly_if_published"]==5753 and A["combined_if_published"]==6819
assert not A["planetary_table_complete_numeric_transcription"] and not Z["numeric_table_fully_machine_verified"]
assert h(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
assert h(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert Z["archive_tests_replayed"]==20 and Z["member_hashes_pass"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PREV.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04u","path":"batches/B04u/RULES.json",
 "records_count":114,"sha256":A["rules_sha256"],
 "scope":"William Lilly (1647) original printed Book II CHAP XCVII/editorial XCVIII method for variable planetary hours and examples, original PDF516-519, signed conclusion 11 June 1647 PDF520, separate Book III title PDF521; 109 historical method and conclusion annotations plus five next-book navigation, 13 source passage groups, 30 caveats, 3 internal clock calculations passing tests. Previous planetary-hour table numeric cells still incompletely digitized; no empirical claims or runtime change."})
I["records_count"]=5753
I["read_numbered_chapters"].append(98)
I["status"]="BOOK_II_PRINTED_PROSE_THROUGH_XCVII_AND_SIGNED_CONCLUSION_ADMITTED_TABLE_NUMERIC_PARITY_OPEN_NEXT_BOOK_III"
I["next"]={"pdf_page":521,"printed_page":None,
 "chapter":"BOOK_III_TITLE_AND_NATIVITY_PROCEDURE",
 "printed_chapter_numeral":None,
 "heading":"An Easie and plaine Method Teaching How to judge upon Nativities",
 "include_opening_paragraph":False,
 "extracted":False,"boundary_image_read":True,
 "position":"Separate first-edition Book III title original PDF521; following natality principles must begin original PDF522 onward. Do not include natal rules as Book II.",
 "outstanding_previous_book_data":[{"type":"PLANETARY_HOUR_TABLE_FULL_NUMERIC_TRANSCRIPTION",
 "original_pdf_pages":list(range(508,516)),"status":"OPEN","original_image_pages_complete":True}]}
I["chapter_XCVIII_source_acceptance_note"]="114 original historical annotations R5640–R5753: 109 printed method and signed conclusion clauses plus 5 Book III title navigation. Three printed examples arithmetic verified for Monday at 9:30 AM Mars, 5:20 PM Sun, 11:10 PM Mars; no independent human outcome or ephemeris. Table 508–515 cell digitization remains open."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5753
assert I["read_numbered_chapters"]==list(range(1,99))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text()
LATEST.write_text("# First-edition Lilly Book II printed Chapter XCVII and signed conclusion — source accepted\n\n"+audit+"\n**Documentary records:** R5640–R5753, 114 historical annotations (109 method and author conclusion; five separate next-book title navigation), 13 first-edition source groups, 30 retained limitations. Six original page image hashes for PDF516–521 with unnumbered Book III title page. Printed date **June 11, 1647** in the conclusion.\n\n**Mechanical checks:** The three example planetary-hour intervals are arithmetically internally consistent, not independently proven astrological influences. Source month/year dual notation, actual historical sunrise/sunset and natal calculation are unverified. ZIP CRC, full extraction, per-member SHA-256 and 20 replayed tests pass.\n\n**After authenticated publication:** **5,753 Lilly + 1,066 retained Ptolemy = 6,819 historical documentary records**. Printed prose through the final numbered Book II chapter is represented, but numeric-cell transcription for the previous 8-page table remains **OPEN**, so full computational source parity is not claimed. No human empirical forecast validations and no runtime astrology model updates.\n\nNext: original PDF521 separate Book III title; PDF522 onward requires primary-source natal rule extraction and source-window finding.\n")
CUR.write_text("# Lilly Book II method and conclusion accepted, numeric table parity open; Book III begins\n\n2026-10-17: 114 first-edition historical source records R5640–R5753 locally admitted (printed XCVII/editorial XCVIII, method PDF516–519, author signed 11 June 1647 PDF520, Book III title navigation PDF521). Once published: **5,753 Lilly + 1,066 Ptolemy = 6,819** historical records. Three printed planetary-hour examples arithmetically pass; no human validations. Prior planetary-hour table PDF508–515 images preserved, ~1,488 numeric cells not fully transcribed. Next original Book III starts PDF521; source research OPEN.\n\n---\n\n"+PREV.read_text())
rec={"batch":"B04u","status":"GUARDED_INDEX_PREPARED_PENDING_REMOTE",
 "prior_parent_git_blob_sha1":blob,"prior_index_sha256":h(OLD),
 "new_index_sha256":h(IDX),"current_sha256":h(CUR),"report_sha256":h(LATEST),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "documentary_records_added":114,"lilly_if_published":5753,
 "retained_ptolemy":1066,"combined_if_published":6819,
 "next_source":"BOOK_III_TITLE","next_original_pdf_page":521,
 "original_book_ii_prose_complete":True,"previous_table_numeric_cell_parity_complete":False,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
