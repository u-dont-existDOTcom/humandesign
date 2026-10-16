#!/usr/bin/env python3
"""Guarded append of original Lilly Reading siege/Lawsuit into source-only index."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03l_CHAPTER_LXVI_COMPLETE.md"
OLDI=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03l_CANONICAL.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03l.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(f.exists() for f in (LATEST,OLDI,OLDC,REC))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
original=IDX.read_bytes();j=json.loads(original)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==3670 and j["batches"][-1]["id"]=="B03k"
assert j["next"]["chapter"]=="LXVI" and j["next"]["pdf_page"]==435
assert j["read_numbered_chapters"]==list(range(1,66))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert j["source_sha256"]==A["original_full_pdf_sha256"]
assert not any(b["id"]=="B03l" for b in j["batches"])
assert A["documentary_accepted_locally"] and A["whole_chapter_lxvi_documentary_complete"]
assert A["previous_lilly_accepted"]==3670 and A["new_documentary_records"]==76
assert A["lilly_if_published"]==3746 and A["combined_if_published"]==4812
assert A["original_reverse_spans"]==19 and A["retained_source_issues"]==23
assert R["record_count"]==76 and R["independently_validated_predictive_cases"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(3671,3747))
assert all(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert A["original_literal_surrender_year"]=="1644"
assert A["historically_corrob_surrender_year"]=="1643"
assert A["surrender_three_days_late_as_author_says"]
assert Z["zip_crc_pass"] and Z["all_member_hashes_pass"] and Z["real_extraction_pass"]
assert Z["extracted_source_tests_passed"]==26 and Z["extracted_test_exit_code"]==0
assert sha(Z["download_path"])==Z["release_zip_sha256"]
assert sha(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({
 "id":"B03l","path":"batches/B03l/RULES.json",
 "records_count":76,"sha256":A["rules_sha256"],
 "scope":"Original Lilly 1647 Chapter LXVI Essex-Reading siege with unnumbered hypothetical lawsuit. Original PDF435 through top of PDF438 above eighth-house divider; 74 LXVI source units and two next-section navigation units; 19 original-to-record spans, 23 original uncertainty limits. Horoscope 17 April 1643 6:50 PM, surrender sentence literally prints 27 April 1644 whereas independent history is 27 April 1643, author admits three-day missed capture deadline; negotiations around forecast date separately preserved. Not empirical validation."
})
j["records_count"]=3746
j["read_numbered_chapters"].append(66)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXVI_DOCUMENTARY_SOURCE_ONLY_NEXT_LXVII_OPEN"
j["next"]={
 "pdf_page":438,"printed_page":404,
 "chapter":"LXVII","printed_chapter_numeral":"LXVII",
 "heading":"If the absent party be alive or dead?",
 "include_opening_paragraph":True,"extracted":False,
 "boundary_image_read":True,
 "position":"On original PDF438/printed404 after ornamental divider and eighth-house preface Of Death, Dowry, Substance of the Wife. LXVI's hypothetical lawsuit ends ABOVE the divider. LXVII begins a new original eighth-house subject; retain prefatory section heading separately."
}
j["chapter_LXVI_source_acceptance_note"]=(
 "76 documentary annotations including two LXVII/eighth-house navigational markers, "
 "19 original visual passages, 23 retained uncertainties. Original chart 17 Apr 1643; "
 "original surrender sentence literally 27 Apr 1644, external 1643; author says final "
 "surrender three days after predicted deadline, negotiations began near prediction date. "
 "Counterfactual lawsuit is same Chapter LXVI, not an observed lawsuit. "
 "Zero blind independent prediction validations or model changes."
)
j["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03l_CHAPTER_LXVI_COMPLETE.md"
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==3746
assert j["read_numbered_chapters"]==list(range(1,67))
report="""# Original Lilly 1647 Chapter LXVI — Reading siege and lawsuit comparison

2026-10-16 Africa/Dakar UTC+0. Parent original-multi-author astrology research remains OPEN. Witness: William Lilly Christian Astrology (1647), Wellcome b30338724 original complete PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LXVI begins original PDF435 / printed401 with a separate square siege horoscope printed **17 April 1643, 6:50 PM**. It continues PDF436 (siege outcome), PDF437 (Feilding narrative plus unnumbered hypothetical lawsuit) and top of PDF438, ending above the ornamental eighth-house divider. The printed Chapter LXVII and eighth-house introduction below the divider are NOT source body of LXVI.

**Consequential original-text anomaly:** The original printed surrender sentence literally says Reading was delivered **27 April 1644**. The original horoscope is 1643. Independent English Civil War primary and historical sources corroborate the town's surrender on **27 April 1643**. Keep printed date and independently supported historical date separately. Never rewrite the original witness as though it printed 1643.

**Consequence for evaluation:** Lilly explicitly says surrender was **three days AFTER the time he predicted**, whereas surrender negotiations commenced near the eighth day after the figure. The initiation of talks near the expected date does not constitute on-time surrender; none of the events is a blind prospective validation. Additional same-author narratives include King Charles's failed relief, Aston's injury, Feilding's surrender and contesting accusations against Feilding. These require independent provenance; personal guilt or loyalty allegations must not be asserted as fact.

The final unnumbered legal analogy gives querent/defendant/judge significators, financial conditions, possible mediation and numerous incompatible people/attorneys who could represent Saturn. It describes no real case, and its alternatives remain explicit; no source-derived numerical algorithm or verified legal outcome is created.

**B03l documentary source acceptance:** 76 original-source editorial annotations R3671–R3746 (74 Chapter LXVI source units plus two following-section navigation markers), 19 original-image passage groups, 23 retained interpretive/chronological limits. All four original-page scans are SHA-256 frozen. No complete independent blinded diplomatic transcription, verified horoscope geometry, or untouched forecast test.

**After authenticated source-branch publication:** Lilly **3,746** + retained Ptolemy **1,066** = **4,812 historical documentary units**. Zero new empirically validated predictions, law or siege forecast successes, or runtime model promotions. ZIP in owner Downloads: Astrology-Lilly-Chapter-LXVI-Reading-Siege-Documentary-20261016.zip, CRC, SHA-256 member integrity, extraction and 26 focused test replay verified.

**NEXT:** Chapter LXVII *If the absent party be alive or dead?* after original PDF438/printed404 ornamental eighth-house preface. Keep eighth-house introduction, Chapter LXVII content and date-of-death/missing-person allegations strictly source-only; avoid medical or actual missing-person conclusions. Parent study OPEN.
"""
prefix="""# Current astrology original-source study — Chapter LXVI Reading siege

CURRENT 2026-10-16: Lilly Book II Chapter LXVI (Reading siege plus hypothetical lawsuit) historically source-admitted. After authenticated research publication Lilly 3,746 plus Ptolemy 1,066 = 4,812 documentary records. Chart 17 April 1643; printed surrender 27 April 1644 vs independent 1643, with final surrender three days after author's predicted deadline. No independently verified predictive accuracy; runtime promotion zero. Next Chapter LXVII begins original PDF438/printed404 below eighth-house divider. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03l_CHAPTER_LXVI_COMPLETE.md and B03l acceptance, release, publication receipts. Overall research OPEN.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CURRENT.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CURRENT.write_text(prefix+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(report,encoding="utf-8")
receipt={"batch":"B03l",
 "kind":"GUARDED_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_GITHUB_PUBLISHED",
 "previous_index_git_blob_sha1":oldblob,
 "previous_index_sha256":sha(OLDI),
 "new_index_sha256":sha(IDX),
 "new_current_state_sha256":sha(CURRENT),
 "new_latest_state_sha256":sha(LATEST),
 "rules_sha256":A["rules_sha256"],
 "owner_download_archive_sha256":Z["release_zip_sha256"],
 "historical_source_units_added":76,
 "lilly_if_published":3746,"retained_ptolemy":1066,
 "combined_if_published":4812,"next_chapter":"LXVII","next_pdf_page":438,
 "original_surrender_year_as_printed":"1644",
 "historically_corrob_surrender_year":"1643",
 "surrender_date_three_days_later_than_author_forecast":True,
 "empirical_predictions_validated":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2,ensure_ascii=False))
