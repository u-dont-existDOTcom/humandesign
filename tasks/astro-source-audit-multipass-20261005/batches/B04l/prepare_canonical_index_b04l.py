#!/usr/bin/env python3
"""Guarded immutable-parent canonical source index integration for B04l."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04l_CHAPTER_XCII_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04l.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04l.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(p.exists() for p in (OLD,OLDC,LATEST,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes(); j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert j["records_count"]==5307 and j["batches"][-1]["id"]=="B04k"
assert j["read_numbered_chapters"]==list(range(1,92))
assert j["next"]["chapter"]=="XCII" and j["next"]["pdf_page"]==497
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert not any(x["id"]=="B04l" for x in j["batches"])
assert A["prior_lilly_accepted"]==5307 and A["new_documentary_records"]==31
assert A["lilly_if_published"]==5338 and A["combined_if_published"]==6404
assert R["record_count"]==31 and R["independently_authenticated_captive_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(5308,5339))
assert all(r["chapter"]=="XCIII_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==17 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parent_blob=git("rev-parse","HEAD:"+rel)
assert parent_blob==git("hash-object",str(IDX))
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDC.write_bytes(CUR.read_bytes())
j["batches"].append({"id":"B04l","path":"batches/B04l/RULES.json",
 "records_count":31,"sha256":A["rules_sha256"],
 "scope":"William Lilly first edition 1647 printed Chapter XCI / editorial XCII, captive or enslaved person and planetary hour of capture, original PDF497–498 printed463–464. 29 historic source clauses and two following witchcraft chapter navigation markers, five original passage groups, nineteen limitations; zero independently authenticated release/outcomes."})
j["records_count"]=5338
j["read_numbered_chapters"].append(92)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCII_SOURCE_ONLY_NEXT_XCIII_OPEN"
j["next"]={"pdf_page":498,"printed_page":464,"chapter":"XCIII",
 "printed_chapter_numeral":"XCII","heading":"If one be Bewitched or not",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF498/printed464 below the Captive or Slave concluding paragraph and horizontal rule; witchcraft attribution and later remedies begin a different numbered chapter."}
j["chapter_XCII_source_acceptance_note"]="31 historical annotations R5308–R5338, 29 captive/planetary-hour clauses + 2 next-chapter navigation; original PDF497-498, five reverse source spans, 19 limitations. Moon timing conditional; Sun one month and Venus forty days author-attributed, no independently verified detainee, captivity event, actual release or harm."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5338
assert j["read_numbered_chapters"]==list(range(1,93))
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
report="""# William Lilly (1647) original printed Chapter XCI — Captive or Slave (editorial XCII)

2026-10-17 — Africa/Dakar UTC+0. Primary source: Lilly, Christian Astrology, first edition 1647, Wellcome b30338724, complete original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original source window:** Chapter printed XCI starts near the bottom of original PDF497/printed463 **below the previous imprisonment divider**. It continues to the top of original PDF498/printed464 and ends before the horizontal rule opening printed Chapter XCII, *If one be Bewitched or not*. The actual first-edition original page JPEGs 497 and 498 are individually frozen by bytes and SHA-256. The sentence about a person taken at a particular planetary hour crosses PDF497–498; no scan reordering or duplicate passage invented.

**Authorial claims, with conditional structure:** Lilly treats sixth- or twelfth-house planet presence as an indicator of a captive and, when empty, turns to a planet under the Sun's beams. He judges the hour of capture, claiming adverse planetary rulers imply long detention and favorable rulers short. Explicitly attributing rules to ancient authorities, he states an alleged escape **within one month** for the Sun hour and **in forty days** for Venus; a Mercury hour implies long confinement. The Moon hour depends on its applying contacts and cannot be scored as a single unconditional timing claim. The physical page seam resumes with the Saturn-hour long confinement, Jupiter-hour prompt exit and Mars-hour risk of fetters, beatings or trouble. This section contains stigmatizing period labels for several classes of prisoners; those are not validated present-day classifications.

**Admitted documentary inventory:** 31 original-source annotations **R5308–R5338**, 29 captive/slavery chapter clauses and two separate subsequent-chapter navigation markers; five source passages including the original physical page seam; nineteen unresolved interpretive/evidentiary limits. Source-first and admission tests plus independent ZIP extraction verify exact provenance, not prediction effectiveness. No complete second diplomatic transcription or independent astro-chart calculation.

**After verified research publication:** Lilly **5,338** + Ptolemy **1,066** = **6,404 historical documentary annotations**. Independently confirmed captive/prison release, harm or death events **zero**; new empirical astrological predictive validations **zero**; runtime scoring/model promotions **zero**.

Owner archive saved directly to the Linux Downloads directory as Astrology-Lilly-Chapter-XCII-Captive-Original-20261017.zip. ZIP CRC, individual member SHA-256, full independent extraction and seventeen test replays verified.

**NEXT:** Original printed Chapter XCII / editorial XCIII *If one be Bewitched or not*, beginning original PDF498 after the divider. Its original witchcraft and health claims are not independently established; keep entirely separate from factual medical diagnoses. Research OPEN.
"""
LATEST.write_text(report,encoding="utf-8")
prefix="""# Original Lilly research — captive or enslaved person (printed XCI / editorial XCII)

CURRENT 2026-10-17: 31 source-only historical annotations R5308–R5338 locally admitted; after verified research-branch publication cumulative Lilly 5,338 + Ptolemy 1,066 = **6,404**. Next editorial XCIII printed XCII, *If one be Bewitched or not* on original PDF498 after divider. All captivity and harm claims are historical only. No empirical predictive validations or runtime model changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04l_CHAPTER_XCII_COMPLETE.md.

---

"""
CUR.write_text(prefix+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B04l","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "parent_index_git_blob_sha1":parent_blob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"state_sha256":H(CUR),
 "report_sha256":H(LATEST),"rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],"new_documentary_records":31,
 "lilly_if_published":5338,"retained_ptolemy":1066,"combined_if_published":6404,
 "next_editorial_chapter":"XCIII","next_printed_chapter":"XCII",
 "next_original_pdf_page":498,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
