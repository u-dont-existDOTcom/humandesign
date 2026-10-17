#!/usr/bin/env python3
"""Guarded append-only first-edition Regiomontanus house chart source index."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04z_REGIOMONTANUS_METHOD.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B04z.json"
OLDSTATE=B/"recovery/CURRENT_BEFORE_B04z.md"
OLDPROGRESS=B/"recovery/PROGRESS_BEFORE_B04z.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in [OLD,OLDSTATE,OLDPROGRESS,LATEST,REC])
I=json.loads(IDX.read_text(encoding="utf-8"))
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6145 and I["batches"][-1]["id"]=="B04y"
assert I["next"]["chapter"]=="CII" and I["next"]["pdf_page"]==553
assert I["read_numbered_chapters"]==list(range(1,102))
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert A["previous_lilly"]==6145 and R["record_count"]==70
assert A["lilly_if_published"]==6215 and A["combined_if_published"]==7281
assert [r["record_number"] for r in R["rules"]]==list(range(6146,6216))
assert all(r["chapter"]=="CIII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==20
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert oldblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());OLDSTATE.write_bytes(CUR.read_bytes());OLDPROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B04z","path":"batches/B04z/RULES.json",
 "records_count":70,"sha256":A["rules_sha256"],
 "scope":"First-edition original Lilly printed CHAP CI/editorial CII Regiomontanus natal house erection, original PDF553-557, following printed CII heading PDF558. 67 original worked source annotations and 3 following navigation, 6 source groups, 24 uncertainties. Merchant Sep19 1616 2:24:25PM at latitude53; original source MC RA222deg10 from rounded solar RA/time and six house cusps, exact intermediates give222deg10min10sec. Original Capricorn Asc6deg37 vs printed OA interpolation near6deg40 discrepancy and 25s versus30s time conversion. No independent natal accuracy or fully verified table data."})
I["records_count"]=6215
I["read_numbered_chapters"].append(102)
I["status"]="BOOK_III_REGIOMONTANUS_CALCULATION_SOURCE_ADMITTED_NEXT_NATAL_JUDGMENT_CII"
I["next"]={"pdf_page":558,"printed_page":524,"chapter":"CIII",
 "printed_chapter_numeral":"CII",
 "heading":"Of things considerable before judgement be given upon a Nativity",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"New printed CHAP CII starts original PDF558/printed524 following completed CHAP CI on PDF557; preliminary natal condition and significator judgments.",
 "outstanding_numeric_parity":[
 {"kind":"BOOK_II_PLANETARY_HOUR_TABLE","original_pages":list(range(508,516))},
 {"kind":"BOOK_III_RIGHT_OBLIQUE_ASCENSION_TABLES","original_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_MONTH_TABLES","original_pages":[536]},
 {"kind":"BOOK_III_SOURCE_SPECULUM","original_pages":[543]}]}
I["chapter_CII_source_acceptance_note"]="70 first-edition historical source records R6146-R6215. Merchant source chart MC222deg10 RA, six printed Regiomontanus house cusps, 34/49 degree approximated intermediate house pole values from latitude53 and natal ephemeris London correction. Original intermediate 30 seconds vs stated25, Asc Capricorn6deg37 versus table interpolation about6deg40. No independent natal time validation."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==6215
assert I["read_numbered_chapters"]==list(range(1,103))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
LATEST.write_text("# First-edition Regiomontanus natal chart calculations — documentary acceptance\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n**Historical source admission:** 70 first-edition documentary annotations R6146–R6215 (67 substantive, 3 following navigation), 6 primary page groups, 24 preserved mathematical/source qualifications. All original PDF553–558 scans and their SHA256s frozen, original-to-record mapping verified. Source calculation can be replayed internally, but Sun/planet ephemerides, original birth time, table-grid parity and geographic longitude remain externally unverified.\n\nOwner ZIP placed in Linux Downloads: Astrology-Lilly-Chapter-CII-Regiomontanus-Original-20261017.zip; CRC/member SHA/full extraction and 20 replayed tests passed. After authenticated GitHub publication: Lilly **6,215** + Ptolemy **1,066** = **7,281** historical documentary annotations; **zero** independent birth-time/predictive validations and **zero** runtime promotions. Next printed CHAP CII, editorial CIII begins original PDF558.\n",encoding="utf-8")
PROGRESS.write_text("# Historical astrology original-source progress — latest accepted Regiomontanus chapter\n\n2026-10-17: original Lilly documentary frontier through PDF557 of 894 scans, approximately 62.3% by physical scan position; this is NOT total scientific project progress or numeric table-cell completion. Cumulative **6,215 Lilly + 1,066 Ptolemy = 7,281** source records, consisting of historic instructions, examples, caveats and image-documentary units, not independently successful predictions. Last admission reconstructed period 1647 Regiomontanus source with precise time and ascension arithmetic, retains Asc interpolation ≈3 arcminutes discrepancy. Unverified merchant birth clock and longitudes, all dense source tables digitization still OPEN. Independent astro-validity tests and runtime promotions new in source lane zero. NEXT printed CII natal judgment original PDF558.\n\n---\n\n"+OLDPROGRESS.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# First edition Regiomontanus house construction documented; natal judgment next\n\n2026-10-17: 70 historical source annotations R6146-R6215 accepted locally, total after verified branch publication **6,215 Lilly + 1,066 Ptolemy = 7,281**. Source arithmetic near MC222deg10, six house cusps, and source year/time rounding preserved; Asc printed Capricorn6deg37 versus direct source OA 39/59 interpolation near6deg40 unresolved. Frontiers next original PDF558 printed CHAP CII natal considerations. No empirical human birth-time outcomes, predictive validations or runtime promotions.\n\n---\n\n"+OLDSTATE.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B04z","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "prior_git_blob_sha1":oldblob,"prior_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_sha256":H(CUR),"latest_report_sha256":H(LATEST),"progress_sha256":H(PROGRESS),
 "rules_sha256":A["rules_sha256"],"archive_sha256":Z["archive_sha256"],
 "added_documentary_records":70,"lilly_if_published":6215,"ptolemy_retained":1066,
 "combined_if_published":7281,"next_original_pdf_page":558,
 "no_independent_natal_time_confirmation":True,"empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
