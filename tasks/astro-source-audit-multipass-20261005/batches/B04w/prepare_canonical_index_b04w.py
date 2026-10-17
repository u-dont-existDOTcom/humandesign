from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04w_TRUTINE_RECTIFICATION.md"
OLD=B/"recovery/INDEX_BEFORE_B04w.json";PRIOR=B/"recovery/CURRENT_BEFORE_B04w.md"
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(q.exists() for q in (OLD,PRIOR,REPORT))
j=json.loads(IDX.read_text());a=json.loads((B/"ACCEPTANCE.json").read_text())
r=json.loads((B/"RULES.json").read_text());z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert j["records_count"]==5824 and j["batches"][-1]["id"]=="B04v"
assert j["next"]["chapter"]=="XCIX" and j["next"]["pdf_page"]==534
assert j["read_numbered_chapters"]==list(range(1,99))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert j["source_sha256"]==a["original_pdf_sha256"]
assert a["new_documentary_records"]==r["record_count"]==99
assert a["lilly_if_published"]==5923 and a["combined_if_published"]==6989
assert [x["record_number"] for x in r["rules"]]==list(range(5825,5924))
assert all(x["section"]=="NEXT_ANIMODAR_NAV_ONLY" for x in r["rules"][-3:])
assert a["Trutine_exact_degree_failure_admitted"] and a["source_conception_hour_method_not_credited"]
assert h(B/"RULES.json")==a["rules_sha256"]==z["accepted_rules_sha256"]
assert h(Path(z["owner_download_path"]))==z["archive_sha256"] and z["extracted_tests_passed"]==20
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parentblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert parentblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PRIOR.write_bytes(CURRENT.read_bytes())
j["batches"].append({"id":"B04w","path":"batches/B04w/RULES.json",
 "records_count":99,"sha256":a["rules_sha256"],
 "scope":"Lilly original printed Book III CHAP XCVIII / editorial XCIX birth-time rectification and Hermes Trutine, original PDF534–539 printed500–505, unidentified merchant 19 Sep 1616, historic pregnancy duration/moon-angle and calendar tables. 96 substantive claims and 3 following Animodar navigation records; 13 original source groups, 27 caveats. Lilly admits exact-degree Trutine imprecision, finds sign sometimes, claims accident/directions-based precision without independent verification, explicitly discredits different conception-hour formula. 1616 leap/conception 10Dec1615 calendar arithmetic checked, actual conception unverified."})
j["records_count"]=5923
j["read_numbered_chapters"].append(99)
j["status"]="BOOK_III_TRUTINE_HERMES_AND_ACCIDENT_RECTIFICATION_SOURCE_ADMITTED_NEXT_ANIMODAR"
j["next"]={"pdf_page":539,"printed_page":505,
 "chapter":"C","printed_chapter_numeral":"XCIX",
 "heading":"Of the Rectification of a Nativity by Animodar",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF539/printed505 following preceding Trutine chapter divider, continues PDF540 and must be bounded at following CHAP C original PDF541.",
 "unfinished_numeric_reference_tables":[
 {"kind":"BOOK_II_PLANETARY_HOUR_TABLE_FULL_DIGITIZATION","original_pdf_pages":list(range(508,516))},
 {"kind":"BOOK_III_TIME_AND_ASCENSION_TABLE_FULL_DIGITIZATION","original_pdf_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_AND_CALENDAR_TABLE_FULL_DIGITIZATION","original_pdf_pages":[536]}]}
j["book_iii_trutine_source_note"]="99 historic source annotations R5825-R5923. Sign-level use sometimes, degree within 1–3° often fails, 13° Moon/conception acceptance band and 1616/1615 calendar example, life-accident rectification preferred, exact conception-hour alternative explicitly not credited; none independently human-validated."
j["current_state"]=str(REPORT.relative_to(ROOT))
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5923
assert j["read_numbered_chapters"]==list(range(1,100))
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text()
REPORT.write_text("# Lilly first Book III numbered chapter — Trutine of Hermes original source\n\n"+audit+"\n**Documentary acceptance:** 99 historic annotations R5825–R5923, 96 substantive Trutine/rectification clauses and 3 next Animodar navigation, 13 original page groups and 27 limitations. Original first-edition PDF534–539 individually image SHA256 verified. Source pregnancy/moon table remains image-preserved, numeric digitization not exhaustive. Source arithmetic example 244+19=263, +366-285=344 and Dec10 1615 putative conception is internally valid, not an independent actual conception record.\n\n**After GitHub readback publication:** **5,923 Lilly + 1,066 Ptolemy = 6,989 historical documentary annotations**. Zero empirical predictive validations or runtime models promoted. Next printed CHAP XCIX / editorial C *Animodar*, PDF539-540; following printed CHAP C begins PDF541.\n\nOwner ZIP already placed in laptop Downloads: Astrology-Lilly-Chapter-XCIX-Trutine-Hermes-Rectification-20261017.zip. CRC, per-member SHA256, full extraction and 20 replay tests passed.\n")
CURRENT.write_text("# Lilly Book III Trutine rectification sources: sign not precise degree\n\n2026-10-17: 99 historical source records R5825–R5923 accepted locally; after publication **5,923 Lilly + 1,066 Ptolemy = 6,989** annotations. Lilly says Hermes Trutine seldom finds exact degree (sometimes rising sign), favors accident-based rectification but does not independently validate it; rejects a separate conception-hour method. 1616 merchant putative conception date 10 Dec 1615 arithmetically derives from source 285-day assumption. Next original printed XCIX/editorial C Animodar on PDF539. All original dense numerical table transcription and empirical time verification OPEN.\n\n---\n\n"+PRIOR.read_text())
rec={"batch":"B04w","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "parent_blob_sha1":parentblob,"prior_index_sha256":h(OLD),"new_index_sha256":h(IDX),
 "current_sha256":h(CURRENT),"report_sha256":h(REPORT),
 "rules_sha256":a["rules_sha256"],"owner_archive_sha256":z["archive_sha256"],
 "new_source_records":99,"lilly_if_published":5923,
 "ptolemy_retained":1066,"combined_if_published":6989,
 "original_source_trutine_degree_precision_unreliable":True,
 "independent_verified_birth_times":0,"new_empirical_validations":0,"runtime_promotions":0,
 "next_editorial_chapter":"C","next_printed_chapter":"XCIX","next_original_pdf_page":539,
 "remote_published":False}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
