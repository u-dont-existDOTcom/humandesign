#!/usr/bin/env python3
"""Guarded append-only original-source integration for Lilly printed XCV."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04p_CHAPTER_XCVI_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04p.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04p.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(p.exists() for p in (OLD,OLDC,LATEST,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();I=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5510 and I["batches"][-1]["id"]=="B04o"
assert I["read_numbered_chapters"]==list(range(1,96))
assert I["next"]["chapter"]=="XCVI" and I["next"]["pdf_page"]==504
assert I["source_sha256"]==A["original_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(x["id"]=="B04p" for x in I["batches"])
assert A["prior_lilly_accepted"]==5510 and A["new_documentary_records"]==42
assert A["lilly_if_published"]==5552 and A["combined_if_published"]==6618
assert R["record_count"]==42 and R["independently_authenticated_fugitive_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(5511,5553))
assert all(r["chapter"]=="XCVII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==18
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDC.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04p","path":"batches/B04p/RULES.json",
 "records_count":42,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly 1647 printed XCV/editorial XCVI escaped-prisoner direction and recapture worked horary dated June 6 1647 8PM, original PDF504-505 printed470-471. Thirty-nine substantive historical source annotations and three following-chapter navigation markers, seven page passage groups, 20 uncertainties. Author reports eastern route, one-night concealment, Friday letter and Sunday recapture without independent evidence."})
I["records_count"]=5552
I["read_numbered_chapters"].append(96)
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCVI_HISTORICAL_SOURCE_ONLY_NEXT_XCVII_OPEN"
I["next"]={"pdf_page":505,"printed_page":471,"chapter":"XCVII",
 "printed_chapter_numeral":"XCVI",
 "heading":"A Lady of her Husband imprisoned, when he should be delivered?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF505/printed471 below separate divider, with its own new square horoscope printed October 19, 1645, 7:20 PM; verify original year glyph and boundary before extraction."}
I["chapter_XCVI_source_acceptance_note"]="42 source-only historical records R5511-R5552; 39 escaped prisoner substantive claims and three subsequent chapter navigation markers. Author forecast East, near-town one-night concealment, letter/messenger by day six or seven, recapture by authority and retrospective Friday letter/Sunday arrest. No independently authenticated prisoner, letter or actual capture; seven source passages and 20 limits."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5552
assert I["read_numbered_chapters"]==list(range(1,97))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT="""# William Lilly first-edition printed XCV / editorial XCVI — Escaped prisoner

2026-10-17 — Africa/Dakar UTC+0.

""" + audit + """

## Historical source admission

42 original documentary annotations R5511–R5552: 39 substantive source details and three following separate chapter navigation markers. Seven mapped original image passage groups and 20 explicit unresolved qualifications. Original first-edition PDF504 and PDF505 are individually SHA-256 verified and the sentence that crosses the page seam is not duplicated. No independent full diplomatic second transcription, original prison/court/letter data or independently reconstructed horoscope is claimed.

**Reported episodes are not independent predictive evidence.** Direction East, one-night hiding, temporary nearness to town, letter or younger messenger, timing within six-seven days and Sunday recapture are separate source endpoints, only retrospectively asserted by Lilly. The exact timing and calendar convention are not externally verified. The next lady/husband imprisonment horoscope is a different person and figure.

**After authenticated research publication:** Lilly **5,552** + Ptolemy **1,066** = **6,618 historical source annotations**; new independent predictive validations **zero**, runtime promotion **zero**.

Owner ZIP saved to Linux Downloads: Astrology-Lilly-XCVI-Original-20261017.zip. Archive CRC, member hashes, full extraction and 18 replayed tests passed; integrated test suites and source-to-record mapping checked.

Next original printed XCVI/editorial XCVII, Lady asks about husband imprisoned, original PDF505 below line. Research OPEN.
"""
LATEST.write_text(REPORT,encoding="utf-8")
prefix="""# Original Lilly research — Escaped prisoner and recapture (printed XCV/editorial XCVI)

2026-10-17: 42 source-only records R5511–R5552 locally admitted. Upon verified publication, cumulative **5,552 Lilly + 1,066 Ptolemy = 6,618 historical source annotations**. Lilly's Eastward escape, short hiding and re-arrest are author-reported, not independently documented or scientifically validated. Next editorial XCVII printed XCVI lady asks about imprisoned husband, original PDF505/printed471. No runtime model changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04p_CHAPTER_XCVI_COMPLETE.md.

---

"""
CUR.write_text(prefix+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B04p","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "old_index_git_blob_sha1":oldblob,"old_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"new_report_sha256":H(LATEST),
 "new_current_state_sha256":H(CUR),
 "accepted_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "source_records_added":42,"lilly_if_published":5552,
 "ptolemy_retained":1066,"combined_if_published":6618,
 "next_chapter_editorial":"XCVII","next_chapter_printed":"XCVI",
 "next_original_pdf_page":505,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
