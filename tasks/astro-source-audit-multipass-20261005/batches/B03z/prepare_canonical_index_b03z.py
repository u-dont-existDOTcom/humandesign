#!/usr/bin/env python3
"""Guarded historical source index integration for Chapter LXXX."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03z_CHAPTER_LXXX_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03z_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03z.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4549 and j["batches"][-1]["id"]=="B03y"
assert j["next"]["chapter"]=="LXXX" and j["next"]["pdf_page"]==473
assert j["read_numbered_chapters"]==list(range(1,80))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert not any(k["id"]=="B03z" for k in j["batches"])
assert A["documentary_accepted_locally"] and A["prior_lilly_accepted"]==4549
assert A["new_documentary_records"]==82 and A["lilly_if_published"]==4631
assert A["combined_if_published"]==5697
assert R["record_count"]==82 and R["independently_verified_political_events"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(4550,4632))
assert all(r["chapter"]=="LXXXI_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==19 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({
 "id":"B03z","path":"batches/B03z/RULES.json",
 "records_count":82,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly (1647) Book II LXXX Presbytery horary public-institution forecast on original PDF473-476, printed439-442, 80 substantive claims plus two LXXXI navigation markers, 13 source passages, 24 unresolved limits, one original 11 March 1646/7 chart, separate three-year alternatives and explicit statu quo/reform qualifier, zero independently authenticated political predictions."})
j["records_count"]=4631
j["read_numbered_chapters"].append(80)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXX_HISTORICAL_SOURCE_ONLY_NEXT_LXXXI_OPEN"
j["next"]={
 "pdf_page":476,"printed_page":442,"chapter":"LXXXI",
 "printed_chapter_numeral":"LXXXI","heading":"If attaine the Philosopher's Stone?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF476/printed442 below Presbytery conclusion and horizontal divider, separate square horary diagram 27 May 1647 at 10:45 AM."}
j["chapter_LXXX_source_acceptance_note"]="82 historical annotations R4550-R4631, 80 LXXX source clauses plus two navigation markers, 13 original page groups and 24 limits. Lilly's 11 March 1646/7 three-year forecast qualified by statu quo reforms and multiple alternatives; no independently verified English institutional prediction."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==4631
assert j["read_numbered_chapters"]==list(range(1,81))
REPORT="""# William Lilly first edition — Chapter LXXX, *If Presbytery shall stand?*

2026-10-16 — Africa/Dakar (UTC+0). Primary original: Lilly, Christian Astrology (1647), Wellcome b30338724; original full PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original boundary:** Chapter LXXX starts original PDF473/printed439 with circular horoscope dated **11 March 1646/7, 4:45 PM**, preserving the year displayed with 1646 above 7. It continues PDF474–475, closing on PDF476/printed442 **above** Chapter LXXXI. The latter has a distinct square chart dated **27 May 1647, 10:45 AM**.

**What Lilly actually asserts:** The question concerns the survival of Presbytery in contemporary England. Lilly contrasts mutable angles with fixed ninth-house Taurus; uses Saturn and Jupiter religious significations, Saturn's weak circumstances, Jupiter's directional station and changing zodiacal dignities, Venus's difficult ninth-house-lady circumstances, and the Moon's separating/void/applied squares. He expressly calls his conclusion **conjectural rather than positive or affirmative**.

**Distinct source-side proposed outcomes:** Internal clerical disputes, young-versus-old theological differences, discomfort among gentry and countrymen, resistance from soldiers, withheld contributions, popular opposition, and magistrate or governmental action. He gives **within three whole years** from the printed question date as a window, but his remedies and outcomes are multiple alternatives: revising discipline, pursuing earlier religious purity, broader national acceptance, or merely moderating current practices. His final conclusion is that the institution would not **continue statu quo without refinement or amendment**, not that Presbyterianism must universally or instantly disappear.

**Documentary admission:** 82 records **R4550–R4631**; 80 Chapter LXXX annotations, two separate following-chapter navigation units; 13 source passage spans with two page seams and **24** retained uncertainties. The original four page JPEGs each have frozen SHA-256. The source-first test suite, historical documentary admission tests, independently extracted owner archive, and integrated canonical index have passing receipts. No independent diplomatic second transcription or chart reconstruction is claimed.

**Scientific evidence status:** There is no independently verified contemporary forecast deposit, frozen unambiguous outcome test, external political timeline adjudication, blind matching evaluation or causal mechanism. **Independent empirical astrological validations added: zero. Runtime models/scoring weights changed: zero.**

**After independently verified research-branch publication:** cumulative **4,631 Lilly** plus **1,066 retained Ptolemy** = **5,697 historical documentary source units**.

Owner archive in laptop Downloads: Astrology-Lilly-Chapter-LXXX-Presbytery-Documentary-20261016.zip. ZIP CRC, all members' SHA-256s and full re-extraction with 19 replayed tests passed.

**NEXT:** Chapter LXXXI *If attaine the Philosopher's Stone?*, original PDF476/printed442 below the divider. Parent original-source study OPEN.
"""
PREFIX="""# Original Lilly research current — Chapter LXXX Presbytery

2026-10-16: Original Lilly LXXX source accepted locally. Following authenticated branch publication: Lilly **4,631**, Ptolemy **1,066**, combined **5,697 historical annotations**. Next LXXXI Philosopher's Stone original PDF476 below divider. Three-year institutional predictions must preserve explicit reform/status-quo scope and conjectural hedge; zero independently validated predictions and zero runtime model changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03z_CHAPTER_LXXX_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
receipt={"batch":"B03z","status":"GUARDED_CANONICAL_INDEX_PREPARED_NOT_REMOTE",
 "prior_index_git_blob_sha1":oldblob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_state_sha256":H(CUR),
 "latest_state_sha256":H(LATEST),
 "accepted_source_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "new_documentary_records":82,"lilly_if_published":4631,
 "ptolemy_retained":1066,"combined_if_published":5697,
 "next_chapter":"LXXXI","next_original_pdf_page":476,
 "independent_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2,ensure_ascii=False))
