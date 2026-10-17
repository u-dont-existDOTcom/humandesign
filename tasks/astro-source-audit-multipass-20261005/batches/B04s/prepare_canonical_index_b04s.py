from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04s_ESSEX_ACCEPTED.md"
OLD=B/"recovery/INDEX_BEFORE_B04s.json";PREV=B/"recovery/CURRENT_BEFORE_B04s.md"
assert not any(p.exists() for p in (OLD,PREV,REPORT))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=json.loads(IDX.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text());R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5586 and I["batches"][-1]["id"]=="B04q"
assert I["next"]["chapter"]=="POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES"
assert I["next"]["postchapter_source_order"][0]["type"]=="UNNUMBERED_ESSEX"
assert I["read_numbered_chapters"]==list(range(1,98))
assert I["source_sha256"]==A["source_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert A["new_documentary_records"]==R["record_count"]==43
assert A["combined_if_published"]==6695
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert Z["replayed_tests"]==14 and Z["full_extract_pass"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parentblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert parentblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PREV.write_bytes(CURRENT.read_bytes())
I["batches"].append({"id":"B04s","path":"batches/B04s/RULES.json","records_count":43,
 "sha256":A["rules_sha256"],
 "scope":"Original Lilly first-edition unnumbered Robert Earl of Essex western march May13 1644 12:29PM on PDF507, 41 substantive historical annotations and two next table navigation; source-based forecasts and self-reported September defeat, independently corroborated army ammunition surrender Sep2, Essex himself escaped by sea Sep1; NOT independent verification of prior astrology forecast."})
I["records_count"]=5629
I["status"]="BOOK_II_UNNUMBERED_ESSEX_ADMITTED_TABLE_508_515_AND_PRINTED_XCVII_516_520_OPEN"
I["next"]={"pdf_page":508,"printed_page":None,"chapter":"PLANETARY_HOUR_TABLE",
 "printed_chapter_numeral":None,"heading":"A Table whereby to find the Planetary hour",
 "extracted":False,"boundary_image_read":True,
 "position":"Original 8 page numeric table PDF508-515 between unnumbered Essex PDF507 and printed Chapter XCVII PDF516. Need exact table schema/numeric fidelity before completion.",
 "remaining_original_source_order":[{"type":"PLANETARY_HOUR_TABLE","first_pdf":508,"last_pdf":515},
 {"type":"PRINTED_CHAPTER_XCVII","first_pdf":516,"last_pdf":520},
 {"type":"NEXT_BOOK_TITLE","pdf_page":521}]}
I["essex_unumbered_1644_historical_acceptance_note"]="43 source-only annotations R5587–R5629, 7 original passage groups, 20 caveats. Historic England verifies parliamentary arms surrender Sep2 1644 but Essex himself departed by sea Sep1. Not a contemporaneously authenticated astrology prediction."
I["current_state"]=str(REPORT.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5629
assert I["read_numbered_chapters"]==list(range(1,98))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n")
evidence=(B/"ORIGINAL_TO_INDEPENDENT_EVENT_AUDIT_20261017.md").read_text()
REPORT.write_text("# Original unnumbered Essex May 1644 horoscope — historical admission\n\n"+evidence+"\n**Historical source acceptance:** R5587–R5629, 43 original-source records, 7 mapped passages and 20 explicit limits. External military event verification is independent of, and does not establish, May 1644 horoscope foreknowledge. Source archival CRC/SHA/extraction and 14 replayed tests passed. Accepted source total after remote readback: 5,629 Lilly + 1,066 Ptolemy = **6,695 historical annotations**.\n\nNext source is the eight-page numeric planetary-hour lookup table original PDF508–515, then genuine printed Chapter XCVII original PDF516–520 before next book begins PDF521. All uncompleted. No empirical prediction validation, scoring or runtime changes.\n")
CURRENT.write_text("# Original Lilly Essex unnumbered chart admitted, numeric tables OPEN\n\n2026-10-17: 43 source annotations R5587–R5629 locally accepted; after publication **5,629 Lilly + 1,066 Ptolemy = 6,695**. Historic England confirms military arms surrender Sep2 1644 but Essex escaped by sea Sep1; prior chart prediction not independently authenticated. **NEXT** eight-page numerical planetary hour table original PDF508–515, then printed XCVII PDF516–520; Book III title PDF521. Retain source-only status, no model changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04s_ESSEX_ACCEPTED.md.\n\n---\n\n"+PREV.read_text())
rec={"batch":"B04s","status":"GUARDED_INDEX_PREPARED_PENDING_REMOTE","parent_git_blob_sha1":parentblob,
 "old_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_sha256":H(CURRENT),"report_sha256":H(REPORT),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "source_records_added":43,"lilly_if_published":5629,"ptolemy_retained":1066,
 "combined_if_published":6695,"next":"PLANETARY_HOUR_TABLE_PDF508_515",
 "historic_defeat_independently_corroborated":True,
 "independent_original_astrology_forecast":False,
 "empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
