#!/usr/bin/env python3
"""Guard source-history integration for Lilly first-edition LXXXI."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04a_CHAPTER_LXXXI_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04a_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04a.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4631 and j["batches"][-1]["id"]=="B03z"
assert j["next"]["chapter"]=="LXXXI" and j["next"]["pdf_page"]==476
assert j["read_numbered_chapters"]==list(range(1,81))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert not any(b["id"]=="B04a" for b in j["batches"])
assert A["documentary_accepted_locally"] and A["prior_lilly_accepted"]==4631
assert A["new_documentary_records"]==57 and A["lilly_if_published"]==4688
assert A["combined_if_published"]==5754 and A["next_chapter"]=="LXXXII"
assert R["record_count"]==57 and R["independently_verified_alchemical_successes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(4632,4689))
assert all(r["chapter"]=="LXXXII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==17 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({"id":"B04a","path":"batches/B04a/RULES.json",
 "records_count":57,"sha256":A["rules_sha256"],
 "scope":"Original 1647 William Lilly Book II LXXXI Philosopher's Stone worked horary, original PDF476-478/printed442-444. 54 substantive authorial belief, source aspects, failure explanations and historical consumption warning plus three next Tenth House/LXXXII navigation markers; eleven original passages, twenty source uncertainties, no independently authenticated elixir, clinical diagnosis or predictive validation."})
j["records_count"]=4688
j["read_numbered_chapters"].append(81)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXI_HISTORICAL_SOURCE_ONLY_NEXT_LXXXII_OPEN"
j["next"]={"pdf_page":478,"printed_page":444,"chapter":"LXXXII",
 "printed_chapter_numeral":"LXXXII",
 "heading":"Of Government, Office, Dignity, Preferment, or any place of Command or Trust",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF478/printed444 below decorative Tenth House divider, after LXXXI final health paragraph. No new figure at LXXXII heading."}
j["chapter_LXXXI_source_acceptance_note"]="57 original source annotations R4632-R4688, 54 alchemy worked-question content and 3 next-section navigation; eleven image passage groups and twenty interpretive limits. Lilly believes in Stone but warns this querent to stop and makes separate consumption claim; none independently authenticated or medically validated."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==4688
assert j["read_numbered_chapters"]==list(range(1,82))
REPORT="""# William Lilly (1647) Chapter LXXXI — Philosopher's Stone, original source

2026-10-16 — Africa/Dakar (UTC+0). Lilly, Christian Astrology (1647 first edition), Wellcome b30338724, original full PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Boundaries:** Separate square horoscope dated **27 May 1647, 10:45 AM**, starting below the LXXX Presbytery divider on original PDF476/printed442. Chapter continues PDF477 and finishes near top of PDF478/printed444 before the decorative Tenth House separator. Chapter LXXXII's independent office/government topic begins **below** the separator on PDF478.

**Source interpretations:** Lilly personally believes that the Philosopher's Stone or elixir exists and can be attained, although he thinks it exceedingly rare and more likely given by angelic revelation than ordinary industry. He then narrows the question to the particular applicant's knowledge and capability. He uses Mercury as ascendant ruler and Mars as lord of ninth/science, repeated squares and changing Mercury direction to infer that the man had earlier failed, desired to resume, and was unsuitable for the work. He reports counseling the man to desist and speculates that his materials or composition were faulty.

**Health evidence separation:** Lilly next asserts the man needed care for **consumption**, supported in the source by Saturn as sixth ruler, a twelfth-house Mars affliction, and no intervening fortunate testimony. This alleged diagnosis has no independent medical record, patient outcome or clinician confirmation. No current clinical inference should be made from the horoscope.

**Documentary acceptance:** 57 original historical source annotations **R4632–R4688**: 54 LXXXI clauses and three following-section/LXXXII navigation markers; 11 source image passages, 20 retained uncertainties, PDF476–478 SHA-256 witness copies. No independent complete diplomatic transcription or ephemeris recast. Archive CRC, SHA-256 member identity and full re-extraction with 17 tests passed, along with source and guarded index tests.

**After authenticated source research publication:** Lilly **4,688** + retained Ptolemy **1,066** = **5,754 historical documentary records**. Independent proven Philosopher's Stone manufactures **zero**, authenticated medical diagnoses **zero**, new empirical astrology predictions validated **zero**, runtime model promotions **zero**.

Owner ZIP in laptop Downloads: Astrology-Lilly-Chapter-LXXXI-Philosophers-Stone-Documentary-20261016.zip.

**Next:** Original Chapter LXXXII, general Tenth House questions about office, preferment and command, begins original PDF478/printed444. Parent source study OPEN.
"""
PREFIX="""# Original historical Lilly research — Chapter LXXXI

CURRENT 2026-10-16: historical original Chapter LXXXI Philosopher's Stone source accepted; after authenticated publication Lilly **4,688** + Ptolemy **1,066** = **5,754** source annotations. Next Chapter LXXXII Government, Office and Preferment begins original PDF478 below the Tenth House divider. Authorial belief in Stone and alleged consumption are **unverified historical claims**; zero new empirical predictions or runtime changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04a_CHAPTER_LXXXI_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
rec={"batch":"B04a","status":"GUARDED_CANONICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE",
 "previous_index_git_blob_sha1":oldblob,
 "previous_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_state_sha256":H(CUR),"latest_state_sha256":H(LATEST),
 "accepted_source_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "source_records_added":57,"lilly_if_published":4688,
 "ptolemy_retained":1066,"combined_if_published":5754,
 "next_chapter":"LXXXII","next_original_pdf_page":478,
 "independent_alchemical_manufactures":0,
 "independent_medical_diagnoses":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(rec,indent=2,ensure_ascii=False))
