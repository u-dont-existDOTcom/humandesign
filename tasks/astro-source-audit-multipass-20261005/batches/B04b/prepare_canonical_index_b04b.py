#!/usr/bin/env python3
"""Guarded historical-source-only canonical index update: Lilly LXXXII."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04b_CHAPTER_LXXXII_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04b_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04b.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4688 and j["batches"][-1]["id"]=="B04a"
assert j["next"]["chapter"]=="LXXXII" and j["next"]["pdf_page"]==478
assert j["read_numbered_chapters"]==list(range(1,82))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert not any(b["id"]=="B04b" for b in j["batches"])
assert A["documentary_accepted_locally"] and A["prior_lilly_accepted"]==4688
assert A["new_documentary_records"]==141 and A["lilly_if_published"]==4829
assert A["combined_if_published"]==5895
assert R["record_count"]==141 and R["independently_verified_office_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(4689,4830))
assert all(r["chapter"]=="LXXXIII_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==18 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(I.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(I))
j["batches"].append({"id":"B04b","path":"batches/B04b/RULES.json",
 "records_count":141,"sha256":A["rules_sha256"],
 "scope":"Original William Lilly (1647) Book II LXXXII Government Office Dignity Preferment source-only rules, original PDF478–482 (printed444–448). 139 substantive clauses for obtaining, holding, transferring or losing an office plus two following LXXXIII navigation markers; 21 passage groups, 26 source limitations; no independent appointment or prediction evidence."})
j["records_count"]=4829
j["read_numbered_chapters"].append(82)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXII_HISTORICAL_SOURCE_ONLY_NEXT_LXXXIII_OPEN"
j["next"]={"pdf_page":482,"printed_page":448,"chapter":"LXXXIII",
 "printed_chapter_numeral":"LXXXIII",
 "heading":"Whether a King expelled his Kingdom, or an Officer removed from his government shall return",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF482/printed448 below office-retention conclusion and chapter divider."}
j["chapter_LXXXII_source_acceptance_note"]="141 original documentary records R4689–R4829 (139 substantive office/tenure clauses, two LXXXIII navigation). Separate office attainment from retention, transfer, removal and reinstatement; 21 source passages and 26 limitations; no independent verified outcome, no runtime change."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==4829
assert j["read_numbered_chapters"]==list(range(1,83))
REPORT="""# Lilly Book II Chapter LXXXII — government, office and preferment

2026-10-16 — Africa/Dakar (UTC+0). Original witness: William Lilly, Christian Astrology (first edition, 1647), Wellcome b30338724, original full PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original boundaries:** Chapter LXXXII starts on PDF478/printed444 after the decorative Tenth House heading. Its source covers PDF479, 480, 481 and the upper portion of PDF482/printed448. The next separate Chapter LXXXIII begins below a divider on PDF482 with the return-to-government question. Original page JPEGs PDF478–482 preserved and SHA-256 hashed.

**First outcome family — obtaining an office:** Lilly assigns first house/lord to applicant and tenth house/lord to desired position. Historical conditional routes involve contacts of the Sun, Moon, tenth and first rulers; application/reception, an unimpeded significator in tenth, benefics and qualified malefics, translation of light by brokers, a complex chain of intermediaries, and long delays before apparent success. The source sometimes predicts office but only with great efforts and expense. Angular, succedent and cadent positions are used for relative timing, without validated durations. His mitigation of adverse intermediary contacts can predict no quarrel even if the office is lost. Different source conditions and exceptions are not treated as independent observed successes.

**Second outcome family — retaining an existing office:** A new subheading on PDF481 concerns remaining in command. It contains separate branches for serving out a term, temporary loss followed by reinstatement, permanent separation, removal around a receiver's retrogradation/combustion/sign exit, and reassignment to a different office as distinct from removal. Source passages also speculate about public criticism, adverse administration and rank-conditioned consequences. The fourth-house/cardinal-sign and various Moon-sign combinations are additional, not automatically cumulative, endings.

**Source-admission scope:** 141 historical documentary annotations **R4689–R4829**: 139 LXXXII source units and two LXXXIII navigation markers; 21 original-image passage groups, 26 explicit unresolved uncertainties, two physical PDF page seams. Tests and archive re-extraction verify corpus/byte integrity, not astrological predictive validity. No independent diplomatic complete transcription or ephemeris parity calculation is claimed.

**After verified research publication:** Lilly **4,829** plus retained Ptolemy **1,066** = **5,895 combined historical source annotations**. New independent verified office cases **zero**, new empirical astrological predictions validated **zero**, runtime model changes **zero**.

Owner ZIP in Downloads: Astrology-Lilly-Chapter-LXXXII-Office-Preferment-Documentary-20261016.zip. CRC, individual member SHA-256 hashes and complete re-extraction with 18 focused tests passed.

**Next:** Chapter LXXXIII concerning restoration of a removed king or officeholder, original PDF482/printed448 below the divider. Parent research OPEN.
"""
PREFIX="""# Original Lilly source research — Chapter LXXXII

CURRENT 2026-10-16: Original Chapter LXXXII historical office/preferment source locally admitted and queued for remote research publication: Lilly **4,829** + retained Ptolemy **1,066** = **5,895** documentary records once remote readback passes. Next LXXXIII starts original PDF482. Office acquisition, loss, transfer and retention are distinct branches; no verified predictive successes or runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04b_CHAPTER_LXXXII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(encoding="utf-8"),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
rec={"batch":"B04b","status":"GUARDED_CANONICAL_PREPARED_NOT_REMOTE",
 "previous_index_git_blob_sha1":oldblob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(I),"current_state_sha256":H(CUR),
 "latest_state_sha256":H(LATEST),"accepted_source_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "source_records_added":141,"lilly_if_published":4829,"ptolemy_retained":1066,
 "combined_if_published":5895,"next_chapter":"LXXXIII","next_original_pdf_page":482,
 "independent_office_outcomes_verified":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
