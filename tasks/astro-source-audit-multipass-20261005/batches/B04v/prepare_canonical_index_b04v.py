from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04v_BOOK_III_INTRO_COMPLETE.md"
OLD=B/"recovery/INDEX_BEFORE_B04v.json"
PREV=B/"recovery/CURRENT_BEFORE_B04v.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(x.exists() for x in (OLD,PREV,LATEST,REC))
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=IDX.read_bytes();I=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5753 and I["batches"][-1]["id"]=="B04u"
assert I["read_numbered_chapters"]==list(range(1,99))
assert I["next"]["chapter"]=="BOOK_III_TITLE_AND_NATIVITY_PROCEDURE" and I["next"]["pdf_page"]==521
assert I["source_sha256"]==A["original_source_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(t["id"]=="B04v" for t in I["batches"])
assert R["record_count"]==A["new_documentary_records"]==71
assert A["lilly_if_published"]==5824 and A["combined_if_published"]==6890
assert [r["record_number"] for r in R["rules"]]==list(range(5754,5825))
assert all(r["section"]=="NEXT_RECTIFICATION_CHAPTER_NAVIGATION" for r in R["rules"][-3:])
assert A["original_arithmetic_discrepancy_arcminutes"]==120
assert not A["full_numeric_table_transcription_complete"]
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==20
assert h(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert h(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
old_blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert old_blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);PREV.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04v","path":"batches/B04v/RULES.json",
 "records_count":71,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly (1647) Book III nativity title/unprinted verso, time-to-equatorial-degree table PDF523, Regiomontanus use & worked 12 June 1647 house cusp example PDF524-525, right ascensions PDF526-527, oblique ascensions for latitudes 34,49,53 PDF528-533, navigation to first printed rectification CHAP XCVIII PDF534. 68 substantive introductory/table-image annotations + 3 navigation, 14 source spans and 24 limits. Printed 142d20m +90d ->230d20m inconsistent mathematically (232d20m). Numeric tables not fully digitized."})
I["records_count"]=5824
I["status"]="BOOK_III_INTRO_TIME_AND_ASCENSION_TABLE_IMAGE_WITNESSES_ADMITTED_NEXT_PRINTED_XCVIII_RECTIFICATION_OPEN"
I["next"]={"pdf_page":534,"printed_page":500,
 "chapter":"XCIX","printed_chapter_numeral":"XCVIII",
 "heading":"Divers wayes of rectifying Nativities",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF534/printed500, first numbered Book III chapter includes a merchant nativity chart. Need full historical next-chapter boundary and rectification procedure extraction.",
 "outstanding_prior_numeric_reference_tables":[
 {"source_pdf_pages":list(range(508,516)),"table":"BOOK_II_PLANETARY_HOUR_NUMERIC_CELLS","status":"NOT_FULLY_DIGITIZED"},
 {"source_pdf_pages":[523,526,527,528,529,530,531,532,533],"table":"BOOK_III_TIME_RA_OBLIQUE_ASCENSION_NUMERIC_CELLS","status":"NOT_FULLY_DIGITIZED"}]}
I["book_iii_intro_source_note"]="71 original-source annotations R5754-R5824 across PDF521-534, 14 source passage groups, 24 limits; printed arithmetic contradiction 142d20m+90d as 230d20m instead of 232d20m and resulting ascendant source discrepancy preserved; all numeric grids not fully machine-transcribed. No empirically validated natal rectification."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5824
assert I["read_numbered_chapters"]==list(range(1,99))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT="""# First edition Lilly Book III — natal introduction, time and ascension references

2026-10-17 — Africa/Dakar UTC+0.

""" + audit + """

## Historical source acceptance and arithmetic issue

**71 original documentary annotations R5754–R5824**: 68 Book III title/time/house-calculation and reference-table image annotations, three navigation for the separate first printed natal rectification chapter, across 14 source groups and 24 limitations. All original consecutive PDF521–534 1600-pixel source witnesses individually SHA-256 and byte frozen. The 24h↔360°, 3h=45°, 25 time minutes=6°15′, Sun RA91°05′+time51°15′=142°20′ relationships are testable elementary conversions.

**Historically printed error intentionally preserved:** 142°20′ plus 90° was printed as **230°20′** rather than mathematically **232°20′**, and Lilly follows his printed value in the nearby 5° Scorpio, 230°52′ oblique-ascension lookup. This is a reproduction-relevant defect and cannot be hidden by repairing the source or used to support retrospective birth-time matching.

The 9 dense table leaves remain available as their exact image witnesses but do NOT constitute complete verified numeric datasets. No original example birth time has been independently reconstructed/validated.

Owner original-source ZIP saved in Linux Downloads: Astrology-Lilly-BookIII-Introduction-Ascensions-Original-20261017.zip. CRC, all member SHA-256, full extraction and 20 replayed tests passed.

**After authenticated research-branch publication:** 5,824 Lilly + 1,066 Ptolemy = **6,890 historical documentary records**. Independent human birth-time rectification results **zero**, empirical forecast validations **zero**, runtime promotions **zero**.

Next original printed Chapter **XCVIII** / editorial **XCIX**, *Divers wayes of rectifying Nativities*, begins PDF534/printed500 with a distinct merchant nativity chart. Additional earlier numeric digitization tasks remain OPEN.
"""
LATEST.write_text(REPORT,encoding="utf-8")
CUR.write_text("# Original Lilly Book III introduction and numeric table witnesses\n\n2026-10-17: 71 new source records R5754–R5824 locally accepted. After verified publication Lilly **5,824** + Ptolemy **1,066** = **6,890** historical annotations. Original PDF521-534 title, time conversion and RA/oblique tables; large grids not fully digitized. Confirmed source arithmetic discrepancy: author prints **142°20′ + 90° = 230°20′** whereas correct result is **232°20′**. Next printed CHAP XCVIII (editorial XCIX) rectification PDF534. Book II numeric tables remain open; zero empirical forecasts or runtime changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04v_BOOK_III_INTRO_COMPLETE.md.\n\n---\n\n"+PREV.read_text(encoding="utf-8"))
rec={"batch":"B04v","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "prior_git_blob_sha1":old_blob,"prior_index_sha256":h(OLD),
 "new_index_sha256":h(IDX),"current_state_sha256":h(CUR),
 "report_sha256":h(LATEST),"rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "source_records_added":71,"lilly_if_published":5824,"ptolemy_retained":1066,
 "combined_if_published":6890,"source_images":14,"numeric_tables_full_digitization":False,
 "printed_arithmetic_discrepancy_arcminutes":120,
 "next_editorial_chapter":"XCIX","next_printed_chapter":"XCVIII",
 "next_original_pdf_page":534,"independent_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
