#!/usr/bin/env python3
"""Guarded append-only source admission, original accident based natal rectification."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04y_ACCIDENT_RECTIFICATION.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B04y_CANONICAL.json"
OLDSTATE=B/"recovery/CURRENT_BEFORE_B04y_CANONICAL.md"
OLDPROGRESS=B/"recovery/PROGRESS_BEFORE_B04y_CANONICAL.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in [OLD,OLDSTATE,OLDPROGRESS,LATEST,REC])
I=json.loads(IDX.read_text(encoding="utf-8"))
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5957 and I["batches"][-1]["id"]=="B04x"
assert I["read_numbered_chapters"]==list(range(1,101))
assert I["next"]["chapter"]=="CI" and I["next"]["pdf_page"]==541
assert I["source_sha256"]==A["original_source_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(q["id"]=="B04y" for q in I["batches"])
assert A["prior_lilly_accepted"]==5957 and A["new_documentary_records"]==R["record_count"]==188
assert A["lilly_if_published"]==6145 and A["combined_if_published"]==7211
assert [r["record_number"] for r in R["rules"]]==list(range(5958,6146))
assert all(r["chapter"]=="CII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert A["source_fever_timing_mismatch_unresolved"] and not A["source_speculum_full_numeric_data_complete"]
assert Z["zip_crc_pass"] and Z["per_member_sha256_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==28
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());OLDSTATE.write_bytes(CUR.read_bytes());OLDPROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B04y","path":"batches/B04y/RULES.json",
 "records_count":188,"sha256":A["rules_sha256"],
 "scope":"Original 1647 Lilly printed CHAP C/editorial CI accident-based rectification and graphical speculum, PDF541-553; 185 substantive historical source clauses and 3 following Regiomontanus navigation markers, 13 original page spans and 25 outstanding limits. Prior merchant known accidents and alternative promissors, original biquintile 105/205 discrepancy, term off-by-one warning, 16y7m in-sample career fit, 20y10m fever target versus fitted 19y10m10d. No independent true birth time or unseen event verified."})
I["records_count"]=6145
I["read_numbered_chapters"].append(101)
I["status"]="BOOK_III_ACCIDENT_RECTIFICATION_ORIGINAL_SOURCE_ACCEPTED_NEXT_REGIOMONTANUS"
I["next"]={"pdf_page":553,"printed_page":519,"chapter":"CII",
 "printed_chapter_numeral":"CI",
 "heading":"To erect a Scheame of heaven by the Tables of Regiomontanus",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF553 bottom after the accident-rectification horizontal divider; printed Regiomontanus demonstration continues PDF554 onward.",
 "outstanding_historical_numeric_data":[
 {"kind":"BOOK_II_PLANETARY_HOUR_FULL_DIGITIZATION","original_pdf_pages":list(range(508,516))},
 {"kind":"BOOK_III_ASCENSION_NUMERIC_TABLES","original_pdf_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_NUMERIC_TABLE","original_pdf_pages":[536]},
 {"kind":"MERCHANT_SPECULUM_GRAPHIC_GRID","original_pdf_pages":[543]}]}
I["chapter_CI_source_acceptance_note"]="188 original source annotations R5958-R6145, 13 passage groups, 25 limits. Historical retrospective fit to four known merchant events; fever 20y10m reported initially vs 19y10m10d selected direction remains mismatched; original 105deg44 biquintile print versus 205deg44 correction source. Multiple free candidate aspects and directions, accepts year-only event ages and birth-time adjustment backward/forward. No out-of-sample success."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6145
assert I["read_numbered_chapters"]==list(range(1,102))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
LATEST.write_text("# First-edition Lilly accident-based birth-time rectification: source accepted\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n## Acceptance and continuation\n\n188 original historical annotations R5958-R6145, 185 substantive source details and three next-chapter navigation records, 13 page groups, 25 source limitations. Four original reported merchant accidents retained; the fever-age discrepancy and biquintile printing discrepancy prevent false perfect agreement. In-sample event fitting is NOT independent birth-time recovery. CRC, original member SHA256, complete archive extraction and 28 test replays passed.\n\nAfter authenticated publication: Lilly 6,145 + Ptolemy 1,066 = 7,211 historical documentary annotations; zero independent predictive validations and runtime promotions. Original PDF553 bottom starts distinct Regiomontanus house chart chapter, next source unit. Numerical table parity incomplete.\n",encoding="utf-8")
previous=OLDPROGRESS.read_text(encoding="utf-8")
PROGRESS.write_text("# Astrology original-source study — updated 2026-10-17 after accident rectification\n\n"+
"Accepted first-edition Lilly original PDF body now through page 553 of a scanned 894-page volume: **61.9% by scan position**, not full digitization or predictive model completion. Historical source annotations: **6,145 Lilly + 1,066 Ptolemy = 7,211**. This count comprises conditions, qualifications, historical anecdotes, examples and source-image witness records, not 7,211 independent predictions. Remaining numeric work: Book II planetary hours PDF508-515; Book III ascension/time tables PDF523 and PDF526-533; gestation PDF536 and the merchant speculum graphic PDF543. All partially image-preserved but not fully cell transcribed.\n\nThe rectification by known accidents chapter PDF541-553 is now documented with 188 source annotations; a prior known apprenticeship event at 16y7m is matched to MC/Mars trine, but the fever target initially at 20y10m conflicts with chosen Asc/Mars direction around 19y10m10d, alongside a 105 vs 205 degree source misprint. Lilly allows retrospective moving of Asc/MC to make known events agree. Independent true-time matching, out-of-sample forecast testing, blinded comparisons against flexible controls, and promotion into the executable runtime remain open and unverified in this source lane.\n\nNext original chapter: printed CI/editorial CII, Regiomontanus chart erection begins original PDF553. Cross-text empirical overall completion percentage cannot responsibly be assigned.\n\n---\n\n"+previous,encoding="utf-8")
CUR.write_text("# Original Lilly accident-based rectification completed as historical source; Regiomontanus next\n\n2026-10-17: accepted locally R5958-R6145 (188 new), cumulative if verified **6,145 Lilly + 1,066 Ptolemy = 7,211** historical source records. Four known merchant life accidents fitted retrospectively; main first-edition fever-age mismatch 20y10m versus chosen 19y10m10d and biquintile 105/205 discrepancy are unresolved. All original source scans PDF541-554 frozen. No empirically validated predictions or runtime promotions. Next original printed CHAP CI/editorial CII Regiomontanus starts PDF553. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04y_ACCIDENT_RECTIFICATION.md.\n\n---\n\n"+OLDSTATE.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B04y","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "old_index_git_blob_sha1":blob,"prior_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),
 "latest_report_sha256":H(LATEST),"progress_report_sha256":H(PROGRESS),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "new_historical_records":188,"lilly_if_published":6145,"ptolemy_retained":1066,
 "combined_if_published":7211,
 "source_fever_age_mismatch_preserved":True,"source_biquintile_misprint_preserved":True,
 "next_editorial_chapter":"CII","next_printed_chapter":"CI","next_original_pdf":553,
 "empirical_validations":0,"runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
