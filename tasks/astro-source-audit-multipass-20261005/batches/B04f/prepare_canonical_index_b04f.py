#!/usr/bin/env python3
"""Guarded canonical historical source index update for Lilly LXXXVI."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04f_CHAPTER_LXXXVI_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04f_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04f.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(x.exists() for x in (LATEST,OLD,OLDCUR,REC))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==5026 and j["batches"][-1]["id"]=="B04e"
assert j["next"]["chapter"]=="LXXXVI" and j["next"]["pdf_page"]==489
assert j["read_numbered_chapters"]==list(range(1,86))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert A["prior_lilly_accepted"]==5026 and A["new_documentary_records"]==54
assert A["lilly_if_published"]==5080 and A["combined_if_published"]==6146
assert R["record_count"]==54 and R["independently_verified_royal_military_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(5027,5081))
assert all(r["chapter"]=="LXXXVII_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==15 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
old_blob=git("rev-parse","HEAD:"+rel)
assert old_blob==git("hash-object",str(IDX))
j["batches"].append({"id":"B04f","path":"batches/B04f/RULES.json",
 "records_count":54,"sha256":A["rules_sha256"],
 "scope":"Original Lilly 1647 Book II LXXXVI separate King/Irish forces and Queen northern army case, original PDF489–490 printed455–456, 52 substantive historical clauses and two LXXXVII navigation markers, ten source passages, twenty-four caveats. Source figure's absolute date unresolved; source retrospectively reports 14 July 1643 reunion and limited Queen army losses versus more categorical destruction forecast. No independently validated prediction."})
j["records_count"]=5080
j["read_numbered_chapters"].append(86)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXVI_HISTORICAL_SOURCE_ONLY_NEXT_LXXXVII_OPEN"
j["next"]={"pdf_page":490,"printed_page":456,
 "chapter":"LXXXVII","printed_chapter_numeral":"LXXXVII",
 "heading":"If attaine the Preferment desired?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF490/printed456 below LXXXVI closing and divider; next gentleman asks within 4–5 minutes of prior question. No new printed figure at this divider."}
j["chapter_LXXXVI_source_acceptance_note"]="54 historical records R5027–R5080, 52 substantive and two LXXXVII navigation; 10 source passage groups and 24 open limits. Distinguish Irish aid, temporary utility, Queen march, reunion date, losses; absolute horary figure date unresolved, full destruction not found in author's reported outcome."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==5080
assert j["read_numbered_chapters"]==list(range(1,87))
REPORT="""# Original Lilly Chapter LXXXVI — Irish Reinforcements and the Queen's Northern Army

2026-10-16 — Africa/Dakar (UTC+0). Original William Lilly, Christian Astrology first ed. 1647, Wellcome b30338724. Full first-edition PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original boundaries:** A square horoscope begins Chapter LXXXVI on original PDF489/printed455. The chapter continues to the upper portion of PDF490/printed456, then LXXXVII starts below its own divider. **No unambiguous absolute date is legible in LXXXVI's horoscope**; the following LXXXVII question says it was asked four or five minutes later but does not supply a calendar date.

**Four distinct targets:** (1) whether the King gains Irish troops; (2) whether they hurt Parliament or last as useful support; (3) whether the Queen advances with her northern army and prospers; (4) when she and the King reunite. Lilly uses the Moon in Cancer/tenth for the King, Sun as eleventh ruler for auxiliaries, and Saturn fourth/derived seventh for the Queen. The Moon/Sun strengthen current capability and reinforcements, but the Sun's adverse testimony signals scandal and limited duration. Lilly later reports Irish forces arrived but were cut off at Nantwich by Fairfax. These are the author's subsequent historical statements, not independently adjudicated war outcomes.

**Queen timing:** Saturn changing signs motivates an advance forecast, and an approaching Moon-to-Saturn trine three or four degrees away prompts a forecast of reunion **three or four months after the undated horary**. Lilly reports they met **about 14 July 1643 in Warwickshire**. Without the absolute question date we cannot judge timing accuracy.

**Critical partial failure:** Lilly says Saturn entering Aries, benefic Jupiter separating, and approaching Mars square indicate a failing royal army. He predicts Parliament's soldiers would essentially **destroy** it. His narrative instead says the Queen lost **some troops** near Nottingham on **11 April** and criticizes the Parliament soldiers for not inflicting more. A reported partial loss is not proof of the total destruction forecast; the author's counterfactual excuse is not a substitute for observed evidence.

**Documentary acceptance:** 54 source-only historical annotations **R5027–R5080** (52 Chapter LXXXVI, two following LXXXVII navigation markers), 10 passage groups and 24 unresolved limitations. Original scanned PDF489–490 images have exact individual SHA-256s. Archive extraction/CRC, tests and guarded index verified. No independent chart recast, precommitted forecast, source-independent military outcome or empirical prediction result.

**After authenticated publication:** Lilly **5,080** + retained Ptolemy **1,066** = **6,146 historical documentary records**. Independent predictive validations **zero**, runtime model promotions **zero**.

Owner archive: Astrology-Lilly-Chapter-LXXXVI-Irish-Queen-Documentary-20261016.zip in laptop Downloads. Full extracted package replayed 15 tests and every member SHA-256 verified.

**Next:** Chapter LXXXVII, attainment of desired preferment, starts on original PDF490/printed456 below the divider. Parent original-source research remains OPEN.
"""
PREFIX="""# Original Lilly research current — Chapter LXXXVI

CURRENT 2026-10-16: Original Chapter LXXXVI historical King/Irish reinforcements/Queen source accepted locally, pending remote authenticated research publication. On publication, Lilly **5,080** + retained Ptolemy **1,066** = **6,146 historical source annotations**. Next LXXXVII opens PDF490 below divider. No explicit absolute LXXXVI figure date; the reported July 1643 reunion is author-retrospective and destruction forecast differs from only partial losses. No empirical predictive validation or runtime rule change. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04f_CHAPTER_LXXXVI_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
rec={"batch":"B04f","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "previous_index_git_blob_sha1":old_blob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_state_sha256":H(CUR),
 "latest_state_sha256":H(LATEST),"accepted_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "documentary_records_added":54,"lilly_if_published":5080,
 "ptolemy_retained":1066,"combined_if_published":6146,
 "next_chapter":"LXXXVII","next_original_pdf_page":490,
 "independent_outcome_validations":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
