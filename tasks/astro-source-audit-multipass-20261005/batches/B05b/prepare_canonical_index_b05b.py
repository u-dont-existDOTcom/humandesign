#!/usr/bin/env python3
"""Guarded append-only original first-edition Lilly printed lifespan chapter."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05b_LIFESPAN_SOURCE.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B05b.json"
OLDSTATE=B/"recovery/CURRENT_BEFORE_B05b.md"
OLDPROGRESS=B/"recovery/PROGRESS_BEFORE_B05b.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in (OLD,OLDSTATE,OLDPROGRESS,REPORT,REC))
I=json.loads(IDX.read_text(encoding="utf-8"));A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6244 and I["batches"][-1]["id"]=="B05a"
assert I["next"]["chapter"]=="CIV" and I["next"]["pdf_page"]==559
assert I["read_numbered_chapters"]==list(range(1,104))
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(b["id"]=="B05b" for b in I["batches"])
assert R["record_count"]==A["new_historical_documentary_records"]==65
assert A["lilly_if_published"]==6309 and A["combined_if_published"]==7375
assert [r["record_number"] for r in R["rules"]]==list(range(6245,6310))
assert all(r["chapter"]=="CV_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert R["author_warns_not_to_pronounce_death_rashly"]
assert Z["crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==19
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());OLDSTATE.write_bytes(CUR.read_bytes());OLDPROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B05b","path":"batches/B05b/RULES.json",
 "records_count":65,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly 1647 printed CHAP CIII/editorial CIV historical infant longevity claims first-edition original PDF559-561/printed525-527. 62 substantive source conditions and 3 following Hyleg chapter navigation, six mapped passage groups, 25 limitations; infant survival and childbirth claims are historical, unverified and not medical prognosis. Favorable vs unfavorable lunar-phase/benefic exception preserved alongside warning not to pronounce death rashly. Next printed CHAP CIV begins below divider on original PDF561."})
I["records_count"]=6309
I["read_numbered_chapters"].append(104)
I["status"]="BOOK_III_INFANT_LIFESPAN_HISTORICAL_SOURCE_ADMITTED_NEXT_HYLEG_PROCEDURE_OPEN"
I["next"]={"pdf_page":561,"printed_page":527,
 "chapter":"CV","printed_chapter_numeral":"CIV",
 "heading":"Of the Prorogator of Life, called Hylech, or Hyleg, or Apheta: and of the killing or interficient Planet",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF561 after horizontal divider, historical life-significator/killing-planet procedure continues PDF562 onward; do not treat as medical assessment.",
 "historical_numeric_parity_still_open":[
 {"kind":"BOOK_II_PLANETARY_HOURS","original_pdf_pages":list(range(508,516))},
 {"kind":"BOOK_III_RIGHT_AND_OBLIQUE_ASCENSIONS","original_pdf_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_AND_CALENDAR_TABLE","original_pdf_pages":[536]},
 {"kind":"BOOK_III_SPECULUM_GRID","original_pdf_pages":[543]}]}
I["chapter_CIV_source_acceptance_note"]="65 first-edition historical annotations R6245-R6309: 62 lifespan/infancy beliefs and 3 separate Hyleg navigation. Three original page scans PDF559-561, six source passage groups, 25 limits, old-humoral full/new moon claims and contrary beneficial exception, parental charts, multiple benefic/malefic conditions, author explicitly warns against rash death judgment. Zero independent infant survival outcomes or clinical validity."
I["current_state"]=str(REPORT.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6309
assert I["read_numbered_chapters"]==list(range(1,105))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT.write_text("# Lilly historical natal lifespan and infancy source — documentary acceptance\n\n2026-10-17 Africa/Dakar (UTC+0).\n\n"+audit+
"\n**Accepted source:** 65 historical annotations R6245–R6309, 62 original longevity source statements and three following Hyleg navigation, six first-edition passage groups and 25 limitations. The full images PDF559–561 were SHA256-verified and retained; source page561 contains the next-chapter divider and no duplicated cases. Archive CRC, complete extraction, SHA256 per member and 19 replayed tests passed. The author's unfavorable lunar-phase propositions, favorable exception and explicit caution not to pronounce death rashly are all retained. These are historical beliefs, NOT valid clinical survival forecasts.\n\n**After authenticated GitHub publication:** Lilly **6,309** + retained Ptolemy **1,066** = **7,375 historic documentary annotations**, zero independently verified human longevity predictive successes, zero runtime promotions. Next Hyleg printed CHAP CIV/editorial CV on same original PDF561, continued subsequent pages.\n",encoding="utf-8")
PROGRESS.write_text("# Original Lilly source progress after infancy/lifespan historical chapter — 2026-10-17\n\nAccepted source through original PDF561 of 894-page volume, approximately **62.8% by scan position**, not rule-table digitization or empirically validated astrological performance. **6,309 Lilly + 1,066 Ptolemy = 7,375** historical annotation records, not distinct human prediction successes. Last chapter covers only first-edition unverified infant-survival/longevity astrology claims and retains contrary lunar-phase branches and a caution against rash death pronouncements. Dense reference-table numeric cell digitization and blinded real-person validation remain OPEN. Next printed Hyleg/Apheta historical life-significator procedure begins PDF561.\n\n---\n\n"+OLDPROGRESS.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# First-edition infant lifespan historical chapter documented; Hyleg method next\n\n2026-10-17: 65 first-edition source-only historical annotations R6245–R6309 added locally, cumulative after publication **6,309 Lilly + 1,066 Ptolemy = 7,375**. Original PDF559–561 printed CIII/editorial CIV. Claims about infant survival, new/full Moon, obstetrical complications and parental charts remain historical/unvalidated; author explicitly warns against rash death judgment. Next printed CHAP CIV/editorial CV Hyleg starts original PDF561 bottom. No clinical predictive claims or runtime promotions. Original numeric parity and full blind empirical study OPEN.\n\n---\n\n"+OLDSTATE.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B05b","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "prior_git_blob_sha1":blob,"prior_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),
 "latest_report_sha256":H(REPORT),"progress_sha256":H(PROGRESS),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "new_historical_records":65,"lilly_if_published":6309,"ptolemy_retained":1066,
 "combined_if_published":7375,
 "original_medical_longevity_claims_unvalidated":True,
 "original_explicit_warning_preserved":True,
 "next_printed_chapter":"CIV","next_editorial_chapter":"CV",
 "next_original_pdf_page":561,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
