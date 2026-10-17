#!/usr/bin/env python3
"""Guarded historical source index integration for Lilly printed XCIV."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04o_CHAPTER_XCV_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04o.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04o.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(p.exists() for p in (OLD,OLDC,LATEST,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();I=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5457 and I["batches"][-1]["id"]=="B04n"
assert I["read_numbered_chapters"]==list(range(1,95))
assert I["next"]["chapter"]=="XCV" and I["next"]["pdf_page"]==502
assert I["source_sha256"]==A["original_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(x["id"]=="B04o" for x in I["batches"])
assert A["prior_lilly_accepted"]==5457 and A["new_documentary_records"]==53
assert A["lilly_if_published"]==5510 and A["combined_if_published"]==6576
assert R["record_count"]==53 and R["independent_verified_medical_outcomes"]==0
assert R["definitive_source_witchcraft_judgment_negative"] and R["author_does_not_confirm_syphilis"]
assert [r["record_number"] for r in R["rules"]]==list(range(5458,5511))
assert all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==21 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parentblob=git("rev-parse","HEAD:"+rel)
assert parentblob==git("hash-object",str(IDX))
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDC.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04o","path":"batches/B04o/RULES.json",
 "records_count":53,"sha256":A["rules_sha256"],
 "scope":"First-edition William Lilly (1647) printed XCIV/editorial XCV separate dated If Bewitched illness/medical worked case original PDF502-503, navigation-only separate prisoner escape case on PDF504. Fifty historical source assertions, three navigation, ten source spans, twenty-two limits; initially suspected bewitchment then negative author judgment, speculative venereal etiology explicitly not confirmed as syphilis, claimed three-week recovery without independent patient records."})
I["records_count"]=5510
I["read_numbered_chapters"].append(95)
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCV_HISTORICAL_SOURCE_ONLY_NEXT_XCVI_OPEN"
I["next"]={"pdf_page":504,"printed_page":470,"chapter":"XCVI",
 "printed_chapter_numeral":"XCV","heading":"A Prisoner escaped out of Prison, which way he went, If Recoverable?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF504/printed470 following the close of dated March 1646 illness case, with its own square figure dated 6 June 1647, 8 PM. Distinct prison escape/recapture question."}
I["chapter_XCV_source_acceptance_note"]="53 historical source annotations R5458–R5510, 50 dated illness/negative witchcraft narrative clauses and three prisoner-next-navigation; 10 source spans and 22 limits. Author reports negative witchcraft verdict, speculative renal/private parts illness without confirmed syphilis, and approximately three-week recovery after an unspecified regimen change, none independently authenticated."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5510
assert I["read_numbered_chapters"]==list(range(1,96))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT="""# Original Lilly (1647) printed XCIV / editorial XCV — Medical case initially suspected of witchcraft

2026-10-17 — Africa/Dakar UTC+0.

""" + audit + """

## Source inventory and scientific-evidence disposition

**53 first-edition documentary annotations R5458–R5510**, with 50 substantive historical claims and three following-chapter navigation markers, ten original passage groups across original PDF502-503 and navigation-only PDF504, twenty-two unresolved source/evidence limitations. Original source-page JPEG images, independent hash checks, documented chart timestamp ambiguity, exact source-first reverse mapping and original-to-canonical ID continuity are preserved. Focused and archive tests confirm source integrity, not occult, clinical or predictive efficacy.

Lilly explicitly rejects the occult suspicion, hypothesizes genital/renal illness, explicitly does not make a definitive lues venerea (syphilis) diagnosis, says physicians changed treatment, and asserts full recovery after approximately three weeks. No patient identity, physician notes, treatment or independent outcome verification; no fact of infection or causal effect can be concluded. No chart has been independently recast.

**After independent research-branch GitHub readback:** **5,510 Lilly** + **1,066 Ptolemy** = **6,576 historical source records**. New independent astrological prediction validations **0**, clinical diagnoses established **0**, independently verified treatment outcomes **0**, runtime model promotions **0**.

Owner archive already saved in the Linux Downloads directory: Astrology-Lilly-Chapter-XCV-Bewitched-Illness-Documentary-20261017.zip. ZIP CRC, per-member SHA-256, full independent extraction and 21 replayed tests passed.

**Next:** Original printed Chapter XCV / editorial XCVI, the separate prisoner-escape direction/recovery question, starts original PDF504/printed470 with new horoscope dated 6 June 1647 at 8 PM. Historical source project OPEN.
"""
LATEST.write_text(REPORT,encoding="utf-8")
prefix="""# Original Lilly source study — dated case rejecting bewitchment

2026-10-17: Printed XCIV / editorial XCV first-edition case locally accepted, R5458–R5510 (53 source units). Upon authenticated research publication cumulative Lilly **5,510** + retained Ptolemy **1,066** = **6,576 historical annotations**. The author refuses a witchcraft diagnosis; his conjectured venereal cause and ~three-week recovery remain unverified historical claims with no independent clinical efficacy. Next printed XCV/editorial XCVI prison escape begins original PDF504. No new empirical forecasts validated; runtime unchanged. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04o_CHAPTER_XCV_COMPLETE.md.

---

"""
CUR.write_text(prefix+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B04o","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "parent_index_git_blob_sha1":parentblob,
 "previous_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_state_sha256":H(CUR),"latest_report_sha256":H(LATEST),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "new_source_records":53,"lilly_if_published":5510,
 "ptolemy_retained":1066,"combined_if_published":6576,
 "next_editorial_chapter":"XCVI","next_printed_chapter":"XCV",
 "next_original_pdf_page":504,"independent_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
