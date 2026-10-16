#!/usr/bin/env python3
"""Guarded historical documentary canonical admission: Lilly LXXXV Rupert and Essex."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04e_CHAPTER_LXXXV_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04e_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04e.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4954 and j["batches"][-1]["id"]=="B04d"
assert j["next"]["chapter"]=="LXXXV" and j["next"]["pdf_page"]==486
assert j["read_numbered_chapters"]==list(range(1,85))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert R["record_count"]==72 and R["author_acknowledged_partial_error"] and R["pre_question_battle_not_prospective"]
assert A["lilly_if_published"]==5026 and A["combined_if_published"]==6092
assert [r["record_number"] for r in R["rules"]]==list(range(4955,5027))
assert all(r["chapter"]=="LXXXVI_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==17 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(I.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(I))
j["batches"].append({"id":"B04e","path":"batches/B04e/RULES.json",
 "records_count":72,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly first-edition (1647) Chapter LXXXV Prince Rupert vs Earl of Essex and later fate, original PDF486–488 / printed452–454. 70 substantive source annotations and 2 following LXXXVI navigation, 11 primary-image passages, 25 source uncertainties. Includes prior Edgehill event (not forecast), later 1646 Oxford Rupert fate and Lilly's explicit partial error, 0 empirical prediction validations."})
j["records_count"]=5026
j["read_numbered_chapters"].append(85)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXV_HISTORICAL_SOURCE_ONLY_NEXT_LXXXVI_OPEN"
j["next"]={"pdf_page":489,"printed_page":455,"chapter":"LXXXVI",
 "printed_chapter_numeral":"LXXXVI",
 "heading":"If his Majesty should procure Forces out of Ireland; and if the Queen should advance with her Army",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF489/printed455 separate Irish forces/Queen Northern army questions; distinct square horary figure after Prince Rupert case closed on PDF488."}
j["chapter_LXXXV_source_acceptance_note"]="72 original source annotations R4955-R5026: 70 Rupert/Essex/honor/fate source claims plus two navigation; 11 original passage groups and 25 limitations; includes author's Edgehill retrospective and admitted partial failure on Rupert custody in 1646; zero independently validated forecasts."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5026
assert j["read_numbered_chapters"]==list(range(1,86))
REPORT="""# William Lilly original first edition — Chapter LXXXV Prince Rupert and Earl of Essex

2026-10-16 Africa/Dakar UTC+0. Primary witness: William Lilly, *Christian Astrology* (1647 first edition), Wellcome b30338724, whole original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original window:** Chapter LXXXV begins original PDF486/printed452 with polygonal horoscope dated **28 November 1642, 9:23 AM**. It continues original PDF487/printed453 and PDF488/printed454 through the final Rupert narrative. The next separate Chapter LXXXVI begins original PDF489/printed455 with new questions about royal Irish reinforcements and the Queen in the north. Four original JPEG witnesses preserve the boundary.

**Separate authorial predictions:** The chapter simultaneously asks whether Prince Rupert gains war honor, whether he beats the Earl of Essex, and what eventually becomes of him. Lilly assigns Rupert to tenth-house Scorpio/Mars and Essex to the opposed Taurus/Venus. Initial Moon sinister/Jupiter dexter trine readings suggest personal survival and possible public respect. He reports studying the question **twenty-four hours**, ultimately judging Rupert would gain **no war honor**, would attract hostility and depart without friendship but **would not be killed**. Initial favorable and later adverse judgment phases remain separate.

**Prior event and retrospective outcome:** In Essex comparison the Moon transfers Jupiter to Saturn and Venus is separated from a Mars square. Lilly interprets this as prior fighting at **Edgehill**, an event already more than a month before the dated question. Its supposed advantage to Essex and claimed officer testimony are author assertions, not independent battle verification. He says he forecast Rupert would not prevail over Essex and subsequently says he did not; neither claim constitutes a contemporaneously deposited verified prediction in this archive.

**Explicitly failed strong forecast:** Lilly's later Mars-in-third interpretation expected Rupert to be at Parliament's disposal and in custody after conflict. He calls his own forecast **'an errour in part'**. He invokes the Oxford siege in **1646**, surrender and Oatlands, but also says Parliament let Rupert depart and he escaped. His retrospective 'very near truth' cannot turn the literal custody forecast into success. The author's confession is preserved in a separate record and all positive and negative outcome variants remain distinct.

**Documentary acceptance:** 72 historical records **R4955–R5026**: 70 chapter source units plus 2 following LXXXVI navigation. Eleven source-image passage groups, 25 unresolved source/historical uncertainties. No full independent diplomatic transcription or modern horoscope ephemeris parity claimed. Original image SHA-256, exact source corpus/record bijection, ZIP full extraction and focused tests passed.

**After authenticated branch publication:** cumulative Lilly **5,026** + retained Ptolemy **1,066** = **6,092 historical source annotations**. Independently verified military prediction outcomes **zero**; runtime model rule promotions **zero**.

Owner ZIP in laptop Downloads: Astrology-Lilly-Chapter-LXXXV-Rupert-Essex-Documentary-20261016.zip; CRC, member SHA-256, independent complete extraction with 17 focused tests passed.

**NEXT:** Chapter LXXXVI, royal Irish forces and Queen's army questions, original PDF489/printed455, research OPEN.
"""
PREFIX="""# Original Lilly source research — Chapter LXXXV Prince Rupert

CURRENT 2026-10-16: locally accepted 72 original-source-only records. Upon authenticated remote publication Lilly **5,026** + Ptolemy **1,066** = **6,092** historical annotations; next Chapter LXXXVI starts original PDF489/printed455. Prince Rupert personal safety vs war glory vs Essex victory vs custody are separate endpoints; historical author's admitted partial custody error retained. Independent prediction validations and runtime promotions remain zero. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04e_CHAPTER_LXXXV_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
rec={"batch":"B04e","status":"GUARDED_CANONICAL_INDEX_PREPARED_PENDING_GITHUB",
 "prior_index_git_blob_sha1":oldblob,
 "previous_index_sha256":H(OLD),"new_index_sha256":H(I),
 "current_state_sha256":H(CUR),"latest_state_sha256":H(LATEST),
 "accepted_source_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "new_documentary_records":72,"lilly_if_published":5026,"ptolemy_retained":1066,
 "combined_if_published":6092,"next_chapter":"LXXXVI","next_original_pdf_page":489,
 "authorial_partial_error_retained":True,"pre_question_Edgehill_not_predictive":True,
 "independently_verified_wartime_outcomes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2,ensure_ascii=False))
