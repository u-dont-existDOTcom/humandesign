#!/usr/bin/env python3
"""Guarded append-only Lilly original single-page natal conditions acceptance."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05a_NATAL_CONDITIONS.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B05a.json"
OLDSTATE=B/"recovery/CURRENT_BEFORE_B05a.md"
OLDPROGRESS=B/"recovery/PROGRESS_BEFORE_B05a.md"
RCPT=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in [OLD,OLDSTATE,OLDPROGRESS,REPORT,RCPT])
I=json.loads(IDX.read_text(encoding="utf-8"))
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6215 and I["batches"][-1]["id"]=="B04z"
assert I["next"]["chapter"]=="CIII" and I["next"]["pdf_page"]==558
assert I["read_numbered_chapters"]==list(range(1,103))
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(b["id"]=="B05a" for b in I["batches"])
assert A["prior_lilly"]==6215 and A["new_documentary_records"]==R["record_count"]==29
assert A["lilly_if_published"]==6244 and A["combined_if_published"]==7310
assert [r["record_number"] for r in R["rules"]]==list(range(6216,6245))
assert all(r["chapter"]=="CIV_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert not Z["independent_predictive_validations"] and Z["archive_replayed_tests"]==17
assert Z["crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert oldblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());OLDSTATE.write_bytes(CUR.read_bytes());OLDPROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B05a","path":"batches/B05a/RULES.json",
 "records_count":29,"sha256":A["rules_sha256"],
 "scope":"William Lilly (1647) first edition printed CHAP CII/editorial CIII, single-page natal prejudgment conditions original PDF558/printed524, 26 substantive source clauses and 3 following mortality/lifespan navigation from PDF559. Four source passage groups, 17 qualifications. Accidents birth-time rectification author favored; planetary strengths/Part of Fortune, aspects, antiscia and contra-antiscia, unquantified closeness to houses/planets, first/second magnitude fixed stars with unquantified small ecliptic latitude. No independent medical, natal or empirical outcome."})
I["records_count"]=6244
I["read_numbered_chapters"].append(103)
I["status"]="BOOK_III_NATAL_PREJUDGMENT_CONDITIONS_SOURCE_ACCEPTED_NEXT_PRINTED_CIII_LIFESPAN_OPEN"
I["next"]={"pdf_page":559,"printed_page":525,
 "chapter":"CIV","printed_chapter_numeral":"CIII",
 "heading":"Of the space of Life, or whether the Native is like to live long, or not",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF559/printed525 begins the next printed and medically sensitive longevity/lifespan chapter. Extract its source boundaries and retain historical-only status; do not turn statements into health advice.",
 "prior_unresolved_reference_data":[
 {"kind":"BOOK_II_PLANETARY_HOUR_NUMERIC_TABLE","pdf_first":508,"pdf_last":515},
 {"kind":"BOOK_III_RIGHT_OBLIQUE_ASCENSION_TABLES","pdf_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_MONTH_TABLE","pdf_page":536},
 {"kind":"BOOK_III_ASTROLOGICAL_SPECULUM_CELL_TRANSCRIPTION","pdf_page":543}]}
I["chapter_CIII_source_acceptance_note"]="29 historical first-edition annotations R6216-R6244: prerequisite planetary/Part of Fortune placement, strength, aspects, antiscia/contra-antiscia and fixed-star proximity before natal judgments; does not supply numeric thresholds for proximity to planets/cusps or 'small' fixed-star latitude. Separate longevity printed CIII PDF559 only navigation."
I["current_state"]=str(REPORT.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6244
assert I["read_numbered_chapters"]==list(range(1,104))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT.write_text("# First-edition Lilly Natal pre-judgment conditions — historical source acceptance\n\n2026-10-17 Africa/Dakar (UTC+0).\n\n"+audit+
"\n**Historical documentary admission:** 29 annotations R6216–R6244 (26 source conditions and three following longevity navigation), four first-edition passage groups, 17 source limitations. Original PDF558–559 hashed and replayed from archive. Source does not specify numerical orbs for antiscia proximity or a fixed star latitude cutoff.\n\n**After authenticated GitHub publication:** **6,244 Lilly + 1,066 Ptolemy = 7,310 historical documentary annotations**, no independently verified person forecasts or runtime model promotions. Owner ZIP: Astrology-Lilly-Chapter-CIII-Natal-Prejudgment-1647-20261017.zip; CRC, per-member SHA256, full extraction and 17 replayed tests passed.\n\nNEXT: separate printed CHAP CIII/editorial CIV, *space of Life*, original PDF559 onward. This is historic astrology, not prognostic clinical guidance.\n",encoding="utf-8")
PROGRESS.write_text("# Lilly original-source frontier — 2026-10-17 natal prerequisites\n\nHistorical source records after authenticated admission **6,244 Lilly + 1,066 Ptolemy = 7,310**. Original first-edition study source frontier through PDF558/894 (~62.4% scan-position only); not a percentage of completed numeric tables or empirical astrology validity. Printed CHAP CII source has 29 accepted documentation clauses, unquantified antiscia/fixed-star proximity thresholds retained. Next printed CHAP CIII on historical infant/lifespan judgments; isolate clinical claims and avoid treating as medical predictions. No new human outcome or runtime promotion; numeric table and blind empirical lanes remain OPEN.\n\n---\n\n"+OLDPROGRESS.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# First-edition Lilly natal pre-judgment conditions source complete, lifespan chapter next\n\n2026-10-17: first-edition PDF558 printed CII/editorial CIII, 29 historical source-only R6216-R6244 locally accepted, proposed cumulative **6,244 Lilly + 1,066 Ptolemy = 7,310**. Full source image/record archive tests passed, but antiscia/fixed star candidate-orb thresholds unspecified, no empirical predictive outcomes. Next printed CIII/editorial CIV longevity beginning PDF559. Remaining numerical table digitization and blind outcome validation OPEN.\n\n---\n\n"+OLDSTATE.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B05a","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "parent_git_blob_sha1":oldblob,"old_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),
 "latest_report_sha256":H(REPORT),"progress_sha256":H(PROGRESS),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "records_added":29,"lilly_if_published":6244,"retained_ptolemy":1066,
 "combined_if_published":7310,"next_printed_chapter":"CIII",
 "next_editorial_chapter":"CIV","next_original_pdf_page":559,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
RCPT.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
