#!/usr/bin/env python3
"""Guarded original historical-source index integration, Lilly Chapter LXVII."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03m_CHAPTER_LXVII_COMPLETE.md"
PREVI= B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03m_CANONICAL.json"
PREVC= B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03m.md"
PREP= B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(x.exists() for x in (LATEST,PREVI,PREVC,PREP))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
original=I.read_bytes()
j=json.loads(original)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==3746 and j["batches"][-1]["id"]=="B03l"
assert j["next"]["chapter"]=="LXVII" and j["next"]["pdf_page"]==438
assert j["read_numbered_chapters"]==list(range(1,67))
assert j["empirical_validations"]==0 and j["runtime_promotions"]==0
assert j["source_sha256"]==A["original_full_pdf_sha256"]
assert all(x["id"]!="B03m" for x in j["batches"])
assert A["documentary_accepted_locally"] and A["whole_chapter_lxvii_source_coverage_complete"]
assert A["prior_accepted_lilly"]==3746 and A["new_documentary_source_records"]==186
assert A["lilly_if_published"]==3932 and A["combined_if_published"]==4998
assert A["original_reverse_passages"]==38 and A["unresolved_source_issues"]==31
assert R["record_count"]==186 and R["independent_absent_person_return_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(3747,3933))
assert all(r["chapter"]=="LXVIII_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_sha256_and_size_match"] and Z["actual_extraction_pass"]
assert Z["extracted_source_tests_passed"]==25 and Z["extracted_test_exit_code"]==0
assert sha(Z["owner_os_download_path"])==Z["accepted_archive_sha256"]
assert sha(B/"RULES.json")==A["rules_sha256"]==Z["rules_sha256"]
rel=str(I.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(I))
j["batches"].append({
  "id":"B03m","path":"batches/B03m/RULES.json",
  "records_count":186,"sha256":A["rules_sha256"],
  "scope":"Original William Lilly Christian Astrology 1647 Book II Chapter LXVII (If absent party be alive or dead?) plus six unnumbered subsections about return/news, timing, querent lifespan, spouse death order and supposed manner of death. Body original PDF438 below eighth-house preface through PDF446 above LXVIII divider. 184 historical chapter source assertions and two LXVIII navigation headings, 38 visual source spans and 31 retained textual limits; no independent human/clinical predictions validated."
})
j["records_count"]=3932
j["read_numbered_chapters"].append(67)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXVII_DOCUMENTARY_SOURCE_ONLY_NEXT_LXVIII_OPEN"
j["next"]={
 "pdf_page":446,"printed_page":412,"chapter":"LXVIII",
 "printed_chapter_numeral":"LXVIII",
 "heading":"Whether the Portion of the Wife will be great, or easily obtained; or whether is the Woman enquired after rich or not?",
 "include_opening_paragraph":True,"extracted":False,
 "boundary_image_read":True,
 "position":"Original PDF446/printed412 BELOW horizontal divider following final LXVII manner-of-death paragraph; separate wife-portion wealth chapter starts there and continues on subsequent original pages."
}
j["chapter_LXVII_source_acceptance_note"]=(
 "186 original-source documentary annotations R3747–R3932, including 184 Chapter LXVII source claims and two LXVIII next-heading navigation markers. "
 "Thirty-eight original passage groups map to all annotations, with eight consecutive two-page seams and 31 retained uncertainties. "
 "No independently observed missing-person returns, deaths, spouse ordering or clinical causes; "
 "flexible death/return-time units and derived-house/reception exceptions are historical text, not validated predictive rules."
)
j["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03m_CHAPTER_LXVII_COMPLETE.md"
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==3932
assert j["read_numbered_chapters"]==list(range(1,68))
REPORT="""# Original Lilly (1647) Chapter LXVII — complete source-documentary edition

2026-10-16 Africa/Dakar UTC+0. Parent historical astrology source study OPEN.

**Original witness:** William Lilly, *Christian Astrology* (1647), Wellcome b30338724 complete original PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. Nine exact original scans PDF438–446 (printed pp404–412), with nine independent per-image SHA256 hashes in B03m.

**True physical scope:** Previous Chapter LXVI ends above an ornamental divider on PDF438, then the eighth-house general preface starts, followed by numbered LXVII *If the absent party be alive or dead?* The numbered chapter body runs through original PDF446 above its horizontal divider. Following Chapter LXVIII, about a wife's wealth/dowry, starts below that divider and is excluded except two navigation-only clauses.

**Original unnumbered subsections retained:** (1) whether an absent person will return, (2) when an absent person returns and the difference between receiving a letter and actual reunion, (3) querent lifespan, (4) open-ended timing of the querent's alleged death, (5) which spouse dies first, and (6) the alleged manner/cause of death. The author prioritizes natal astrology over horary in spouse comparison and uses relation-dependent derived houses for missing people.

**Important limitations and contradictory-looking branches:** Sixth-house affliction versus placement without affliction; applying future illness versus separating past danger; bare eighth-house occupation with eventual return versus afflicted occupation with permanent nonreturn; aspect date for news versus conjunction for reunion; flexible distance/house/sign-based weeks/months/years; first-house lord often prioritized over Moon in mortality questions; ambiguous one-way versus mutual reception and eclipses/anareta/degree-to-time formulas. Original astrological propositions are NOT valid clinical, missing-person, lifespan, or cause-of-death evidence.

**Source batch B03m:** 186 historical documentary units R3747–R3932 (184 Chapter LXVII assertions plus two LXVIII heading-navigation markers), 38 visually ordered original-source groups, 31 retained uncertainties, eight original cross-page passages. Original archive includes image scans, source clause draft, bidirectional mapping, accepted record layer, unresolved issues, original statement fidelity tests and SHA-256 checks. No complete independent blind diplomatic second transcription or modern ephemeris verification claimed.

**After authenticated research-branch publication:** 3,932 Lilly + 1,066 retained Ptolemy = 4,998 historical documentary annotations. No independent real human case outcome authenticated, no empirically validated prediction, and zero model/runtime promotions.

**Owner-local archive:** Astrology-Lilly-Chapter-LXVII-Documentary-20261016.zip under OS-designated Downloads; accepted ZIP CRC, all-member SHA256, actual extraction and source/admission test replay verified before canonical integration.

**Next:** Chapter LXVIII wife’s portion/dowry, begins original PDF446/printed412 BELOW divider. Identify its true next-chapter boundary from scanned original pages; include all unnumbered intervening subsections. Study remains OPEN.
"""
PREFIX="""# Current astrology historical source study — Lilly Chapter LXVII complete

CURRENT 2026-10-16: Original Lilly Chapter LXVII (absent status, return, lifespan, spouse and manner-of-death historical source statements) accepted for DOCUMENTARY research. After authenticated research publication, accepted Lilly 3,932 plus retained Ptolemy 1,066 = 4,998 historical source annotations. Original PDF438–446; next chapter LXVIII wife portion begins PDF446 below divider. No independent empirical prediction success and zero runtime scoring changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03m_CHAPTER_LXVII_COMPLETE.md and B03m acceptance, archive and publication receipts.

---

"""
PREVI.parent.mkdir(parents=True,exist_ok=True)
PREVI.write_bytes(original)
PREVC.write_bytes(CURRENT.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CURRENT.write_text(PREFIX+PREVC.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
receipt={"batch":"B03m","kind":"GUARDED_LOCAL_ORIGINAL_HISTORICAL_INDEX_PREPARATION",
 "original_predecessor_index_git_blob_sha1":oldblob,
 "previous_index_sha256":sha(PREVI),
 "new_index_sha256":sha(I),
 "new_current_state_sha256":sha(CURRENT),
 "new_latest_source_state_sha256":sha(LATEST),
 "accepted_rules_sha256":A["rules_sha256"],
 "accepted_owner_archive_zip_sha256":Z["accepted_archive_sha256"],
 "new_original_documentary_units":186,
 "lilly_if_published":3932,"retained_ptolemy":1066,
 "combined_if_published":4998,
 "next_numbered_chapter":"LXVIII","next_original_pdf_page":446,
 "new_independently_validated_predictions":0,
 "new_runtime_promotions":0,"remotely_published":False}
PREP.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(receipt,indent=2,ensure_ascii=False))
