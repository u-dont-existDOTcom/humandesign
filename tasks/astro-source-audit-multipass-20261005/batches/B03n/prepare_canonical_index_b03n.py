#!/usr/bin/env python3
"""Guarded historical source-index append of 1647 Chapter LXVIII wife's portion."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03n_CHAPTER_LXVIII_COMPLETE.md"
OLDI=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03n_CANONICAL.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03n.md"
PREP=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,PREP))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *xs:subprocess.check_output(["git",*xs],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==3932 and j["batches"][-1]["id"]=="B03m"
assert j["next"]["chapter"]=="LXVIII" and j["next"]["pdf_page"]==446
assert j["read_numbered_chapters"]==list(range(1,68))
assert j["source_sha256"]==A["original_full_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert all(x["id"]!="B03n" for x in j["batches"])
assert A["documentary_accepted_locally"] and A["new_documentary_records"]==44
assert A["previous_lilly_accepted"]==3932 and A["lilly_if_published"]==3976
assert A["original_reverse_spans"]==11 and A["unresolved_source_issues"]==15
assert R["record_count"]==44 and R["independent_dowry_receipts_verified"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(3933,3977))
assert R["rules"][-1]["chapter"]=="LXIX_NAVIGATION_ONLY"
assert Z["zip_crc_pass"] and Z["member_sha256_pass"] and Z["actual_extraction_pass"]
assert Z["replay_tests_passed"]==16 and Z["replay_test_exit_code"]==0
assert sha(Z["owner_download_path"])==Z["archive_sha256"]
assert sha(B/"RULES.json")==A["rules_sha256"]==Z["source_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({
 "id":"B03n","path":"batches/B03n/RULES.json",
 "records_count":44,"sha256":A["rules_sha256"],
 "scope":"Original 1647 Book II Chapter LXVIII wife's portion/dowry wealth: original PDF446 below LXVII divider through PDF447, next LXIX heading PDF448. 43 historical wealth/dowry source clauses plus one next-chapter heading, eleven reverse image source groups, fifteen retained uncertainty/negative clauses; no independent transactions or wealth predictions validated."})
j["records_count"]=3976
j["read_numbered_chapters"].append(68)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXVIII_DOCUMENTARY_SOURCE_ONLY_NEXT_LXIX_OPEN"
j["next"]={"pdf_page":448,"printed_page":414,"chapter":"LXIX",
 "heading":"If one be afraid of a thing, Whether he shall be in danger of the same or not.",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF448/printed414 top, distinct CHAP LXIX after complete LXVIII on PDF447. The next numbered LXIX concerns anticipated fear, not dowry."}
j["chapter_LXVIII_source_acceptance_note"]="44 historical documentary units (43 wealth clauses, one LXIX heading); 11 original-page spans, 15 uncertainties. Eighth vs second house, good versus delayed payment, square/opposition and reception conditions retained; original warns rules not universal. Zero verified property or fraud outcomes."
j["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03n_CHAPTER_LXVIII_COMPLETE.md"
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==3976
assert j["read_numbered_chapters"]==list(range(1,69))
REPORT="""# Lilly (1647) Chapter LXVIII — original wife-portion historical source

2026-10-16 Africa/Dakar UTC+0. William Lilly, Christian Astrology original 1647, Wellcome b30338724 original full-PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

The numbered **Chapter LXVIII** begins below the horizontal divider on original PDF446/printed412 and its original source body concludes at the bottom of PDF447/printed413. The next unrelated Chapter LXIX concerning fear/danger begins PDF448/printed414. The author asks whether a prospective wife's promised portion is substantial, easy to obtain or whether the woman is rich.

Source rules distinguish the querent's estate (second house) from the spouse's portion (eighth). Eighth-house cusp terms, ruler, occupiers, Jupiter/Venus, the Part of Fortune, its dispositor, dignity, retrogradation, combustion and reception are separate source conditions. Significant promised wealth is NOT the same as actual prompt payment. The author presents separate negative branches for little payment, delay, disputes, unfulfilled promise or suspected dishonesty. The chapter explicitly warns that general rules are not always certain and requires attention to the questioner's circumstances.

**Accepted source batch B03n:** 44 original documentary annotations R3933–R3976 (43 Chapter LXVIII historical rules plus one Chapter LXIX heading), 11 original-image passage groups including one cross-page passage, 15 text/glyph/interpretation uncertainties. No independent proof of dowry transfer, parental ability, inheritance, or alleged cheating; no fully blinded second diplomatic transcription. This is an original-text record set, not a calibrated financial prediction.

**After authenticated source-branch publication:** accepted Lilly 3,976 plus retained Ptolemy 1,066 = 5,042 historical documentary annotations. Zero independent predictive validations or model/runtime promotions.

Owner-local accepted ZIP Astrology-Lilly-Chapter-LXVIII-Wife-Portion-Documentary-20261016.zip under designated Downloads: all member SHA-256, ZIP CRC, extraction and sixteen source/admission tests replayed before integration. Historical source research OPEN.

**NEXT:** Chapter LXIX, If one be afraid of a thing, Whether he shall be in danger of the same or not, original PDF448/printed414. Identify following true chapter boundary and preserve conditions, not personal safety determinations.
"""
PREFIX="""# Current original astrology source research — Chapter LXVIII

CURRENT 2026-10-16: Lilly Chapter LXVIII original wife-portion/dowry source accepted. After authenticated research publication: 3,976 Lilly + 1,066 retained Ptolemy = 5,042 original historical documentary units. Next Chapter LXIX fear/danger begins original PDF448/printed414. No independent predictive case validations, no runtime model changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03n_CHAPTER_LXVIII_COMPLETE.md and B03n acceptance/publication receipts.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
receipt={"batch":"B03n","status":"GUARDED_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE",
 "previous_index_git_blob_sha1":oldblob,
 "old_index_sha256":sha(OLDI),"new_index_sha256":sha(IDX),
 "new_current_state_sha256":sha(CUR),"new_latest_state_sha256":sha(LATEST),
 "source_rules_sha256":A["rules_sha256"],
 "accepted_owner_archive_sha256":Z["archive_sha256"],
 "new_source_records":44,"lilly_if_published":3976,
 "ptolemy_retained":1066,"combined_if_published":5042,
 "next_chapter":"LXIX","next_pdf_page":448,
 "independent_predictive_validations":0,"runtime_promotions":0,
 "remote_published":False}
PREP.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
