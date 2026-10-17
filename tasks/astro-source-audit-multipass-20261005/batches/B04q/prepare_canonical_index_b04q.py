from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04q_CHAPTER_XCVII_COMPLETE.md"
OLD=B/"recovery/INDEX_BEFORE_B04q.json";PREV=B/"recovery/CURRENT_BEFORE_B04q.md"
assert not any(f.exists() for f in (OLD,PREV,LATEST))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads(IDX.read_text());a=json.loads((B/"ACCEPTANCE.json").read_text())
r=json.loads((B/"RULES.json").read_text());z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert j["records_count"]==5552 and j["batches"][-1]["id"]=="B04p"
assert j["next"]["chapter"]=="XCVII" and j["next"]["pdf_page"]==505
assert j["read_numbered_chapters"]==list(range(1,97))
assert j["source_sha256"]==a["source_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert a["lilly_if_published"]==5586 and a["combined_if_published"]==6652
assert r["record_count"]==34 and [x["record_number"] for x in r["rules"]]==list(range(5553,5587))
assert H(B/"RULES.json")==a["rules_sha256"]==z["rules_sha256"]
assert H(Path(z["owner_download_path"]))==z["archive_sha256"] and z["extracted_tests_passed"]==14
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldsha=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert oldsha==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PREV.write_bytes(CUR.read_bytes())
j["batches"].append({"id":"B04q","path":"batches/B04q/RULES.json",
 "records_count":34,"sha256":a["rules_sha256"],
 "scope":"First edition William Lilly printed XCVI/editorial XCVII wife asks if husband released, original PDF505-506. 30 source clauses and 4 postchapter navigation markers, 7 passage groups and 19 limitations. Lilly hedges already released OR within 3 days, then asserts release and garrison capture on day before question. No independent record or prospective success. Next unnumbered Essex chart and tables not completed."})
j["records_count"]=5586
j["read_numbered_chapters"].append(97)
j["status"]="BOOK_II_PRINTED_NUMBERED_THROUGH_XCVI_DOCUMENTARY_COMPLETE_POSTCHAPTER_UNNUMBERED_MATERIAL_OPEN"
j["next"]={"pdf_page":507,"printed_page":473,"chapter":"POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES",
 "printed_chapter_numeral":None,"heading":"The time of his Excellencies Robert Earle of Essex last setting forth into the west",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF507 has independent unnumbered 13 May 1644 chart. Original PDF508-510 are table pages; audit full remainder before treating Book II as complete."}
j["chapter_XCVII_source_acceptance_note"]="34 original documentary annotations R5553-R5586, 30 numbered case clauses and 4 unnumbered Essex/table navigation markers, 7 image spans, 19 uncertainties. Past-or-future release disjunction and self-reported prior-day garrison capture prevent clean prospective result."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5586
assert j["read_numbered_chapters"]==list(range(1,98))
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
aud=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text()
LATEST.write_text("# Original Lilly last printed numbered chapter — wife asks about husband release\n\n2026-10-17 Africa/Dakar (UTC+0).\n\n"+aud+"\n**Documentary admission:** 34 historical source annotations R5553–R5586, seven original passage groups and nineteen retained limits. The author explicitly says release either had occurred or would occur within three days, then reports release and the garrison's capture the day *before* the question. The source does not establish independent dates, a named wife/husband or prospective predictive success. No runtime changes.\n\n**After authenticated publication:** **5,586 Lilly + 1,066 Ptolemy = 6,652 historical source units**. All originally numbered chapter labels through printed XCVI have been indexed; the unnumbered Essex worked figure and table material are still OPEN, so this does not mean complete Book II coverage.\n\nOwner ZIP already placed in Linux Downloads: Astrology-Lilly-Chapter-XCVII-Release-Documentary-20261017.zip, CRC/SHA/full extraction and 14 replayed tests passed.\n")
CUR.write_text("# Original Lilly through printed XCVI, postchapter material OPEN\n\n2026-10-17: 34 historical source annotations R5553–R5586 accepted locally, Lilly **5,586** + Ptolemy **1,066** = **6,652** upon verified publication. Original chapter says husband either already released or will be within three days, then reports prior-day release and capture of garrison; no independent prospective validation. Next PDF507 unnumbered Earl of Essex figure; original PDF508 onward tables need source coverage.\n\n---\n\n"+PREV.read_text())
receipt={"batch":"B04q","status":"GUARDED_INDEX_PREPARED_NOT_REMOTE",
 "parent_blob_sha1":oldsha,"old_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_sha256":H(CUR),"latest_report_sha256":H(LATEST),
 "accepted_rules_sha256":a["rules_sha256"],"owner_archive_sha256":z["archive_sha256"],
 "added_historical_source_records":34,"lilly_if_published":5586,
 "retained_ptolemy":1066,"combined_if_published":6652,
 "next":"POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES",
 "independent_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
