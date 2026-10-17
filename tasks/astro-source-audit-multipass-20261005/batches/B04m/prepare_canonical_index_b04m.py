#!/usr/bin/env python3
"""Guarded source-only index integration, Lilly original printed XCII."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04m_CHAPTER_XCIII_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04m.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04m.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(p.exists() for p in (OLD,OLDC,LATEST,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();I=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5338 and I["batches"][-1]["id"]=="B04l"
assert I["read_numbered_chapters"]==list(range(1,93))
assert I["next"]["chapter"]=="XCIII" and I["next"]["pdf_page"]==498
assert I["source_sha256"]==A["original_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(x["id"]=="B04m" for x in I["batches"])
assert A["prior_lilly_accepted"]==5338 and A["new_documentary_records"]==75
assert A["lilly_if_published"]==5413 and A["combined_if_published"]==6479
assert R["record_count"]==75 and R["independent_verified_witchcraft_cases"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(5339,5414))
assert all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==21 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
old_blob=git("rev-parse","HEAD:"+rel)
assert old_blob==git("hash-object",str(IDX))
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDC.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04m","path":"batches/B04m/RULES.json",
 "records_count":75,"sha256":A["rules_sha256"],
 "scope":"Original first-edition Lilly printed XCII/editorial XCIII claims about supernatural witchcraft, 1647 PDF498-500, with an unnumbered domestic-ritual subsection, and distinct following horse case on PDF501; 72 substantive historical claims, three navigation markers, 11 source spans, 28 explicit limitations, zero independently authenticated outcomes."})
I["records_count"]=5413
I["read_numbered_chapters"].append(93)
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCIII_SOURCE_ONLY_NEXT_XCIV_OPEN"
I["next"]={"pdf_page":501,"printed_page":467,"chapter":"XCIV",
 "printed_chapter_numeral":"XCIII","heading":"A Horse lost or stolen neer Henley, if recoverable or not?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF501/printed467 begins distinct square horoscope 11 January 1646, 2:59 PM. Lilly later asserts return after three days, compared to forecast within one or two; distinct from witchcraft."}
I["chapter_XCIII_source_acceptance_note"]="75 documentary source units R5339-R5413: 72 historic witchcraft/remedy claims and three following horse-case navigation markers, 11 primary-source passage groups, 28 unresolved limitations; source does not verify supernatural causes, health conditions or treatments."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5413
assert I["read_numbered_chapters"]==list(range(1,94))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT="""# Original Lilly (1647) printed Chapter XCII / editorial XCIII — alleged Witchcraft and historical remedies

2026-10-17 — Africa/Dakar (UTC+0).

""" + audit + """

## Admitted historical source and evidence level

**75 documentary annotations R5339–R5413**, consisting of 72 claims within the printed chapter and three following-chapter navigation markers. Eleven original page groups including the PDF498-499 and PDF499-500 physical text seams, with 28 retained uncertainties. Source pages PDF498, PDF499, PDF500 and navigation-only PDF501 are hash-frozen. Archive CRC, individual-member SHA-256, complete extraction and 21 replayed tests pass. No complete second diplomatic transcription or chart parity is claimed.

**After authenticated GitHub research publication:** 5,413 Lilly + 1,066 Ptolemy = **6,479 historical source annotations**. Independently verified supernatural causes **0**, medical diagnoses **0**, treatment successes **0**, empirically validated astrological forecasts **0**, runtime/scoring promotions **0**.

Owner archive is already saved in the OS Downloads folder as Astrology-Lilly-Chapter-XCIII-Witchcraft-Historical-20261017.zip. Its checksums are in SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json.

**NEXT:** editorial XCIV / printed XCIII, the separate dated horse-lost-near-Henley case, begins original PDF501. Its one-to-two-day forecast and author-reported actual three-day return must be preserved as separate statements and not counted as a prospective independent success. Parent text research remains OPEN.
"""
LATEST.write_text(REPORT,encoding="utf-8")
prefix="""# Original Lilly first-edition source research — alleged Witchcraft and remedies

2026-10-17: printed XCII / editorial XCIII historical text locally accepted, R5339–R5413 (75 new); after verified branch publication Lilly 5,413 + Ptolemy 1,066 = **6,479 historical source units**. The unnumbered remedies subsection is included, but does NOT support occult medical causation or safe effective treatments. Next editorial XCIV / printed XCIII horse case original PDF501. No independent predictive validations or runtime changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04m_CHAPTER_XCIII_COMPLETE.md.

---

"""
CUR.write_text(prefix+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B04m","status":"GUARDED_CANONICAL_PREPARED_NOT_REMOTE",
 "previous_index_git_blob_sha1":old_blob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_state_sha256":H(CUR),
 "latest_report_sha256":H(LATEST),"accepted_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "new_documentary_records":75,"lilly_if_published":5413,
 "ptolemy_retained":1066,"combined_if_published":6479,
 "next_editorial_chapter":"XCIV","next_printed_chapter":"XCIII",
 "next_original_pdf_page":501,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
