from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04c_CHAPTER_LXXXIII_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04c_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04c.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4829 and j["batches"][-1]["id"]=="B04b"
assert j["next"]["chapter"]=="LXXXIII" and j["next"]["pdf_page"]==482
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["read_numbered_chapters"]==list(range(1,83))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert R["record_count"]==46 and [r["record_number"] for r in R["rules"]]==list(range(4830,4876))
assert A["lilly_if_published"]==4875 and A["combined_if_published"]==5941
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==16 and Z["owner_download_path"]
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({"id":"B04c","path":"batches/B04c/RULES.json",
 "records_count":46,"sha256":A["rules_sha256"],
 "scope":"First-edition William Lilly Book II LXXXIII restoration to former office/kingdom, original PDF482-484. 44 historical clauses and two separate following-chapter navigation units, eight passages and 17 unresolved conditions, with restoration elsewhere distinct from return, zero independent empirical outcomes."})
j["records_count"]=4875
j["read_numbered_chapters"].append(83)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXIII_HISTORICAL_ONLY_NEXT_LXXXIV_OPEN"
j["next"]={"pdf_page":484,"printed_page":450,"chapter":"LXXXIV",
 "printed_chapter_numeral":"LXXXIV","heading":"Of the Profession, Magistery or Trade any one is capable of",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF484/printed450 BELOW separate LXXXIII horizontal divider, begins profession guidance."}
j["chapter_LXXXIII_source_acceptance_note"]="46 historical records R4830-R4875; 44 restoration/alternative-land/negative clauses and two LXXXIV navigation markers; 8 passages, 17 unresolved limits, zero independent authenticated restorations."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(z["records_count"] for z in j["batches"])==4875
assert j["read_numbered_chapters"]==list(range(1,84))
report="""# Original Lilly (1647) Chapter LXXXIII — Restoration after Expulsion

2026-10-16 Africa/Dakar UTC+0. Original William Lilly *Christian Astrology* first edition, Wellcome b30338724; whole original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

LXXXIII starts below Chapter LXXXII's divider on original PDF482/printed448, crosses PDF483/printed449 and closes near the top of PDF484/printed450 before a new horizontal rule. Following LXXXIV concerns vocational aptitude and is not part of restoration.

The historical question: can a king, prince, gentry member or officer expelled or displaced from power regain their old rule, office, dignity or estates? Lilly uses first and tenth rulers, heavier/lighter dispositor, Moon contacts and reception as proposed conditions. Cardinal Moon signs allegedly accelerate reinstatement but without a fixed interval. An under-earth peregrine planet and absent reception can negate positive indications.

A critical **alternative-place distinction**: with a benefic Moon contact Lilly names eight signs associated with return to former power, but Gemini, Virgo, Sagittarius or Pisces allegedly imply sovereignty **somewhere else** or an office **in another country**. That is not a success at restoration of the original place. A separate negative rule rejects return when the tenth ruler and Moon are angularly impeded by malefic conjunction.

**Documentary accepted:** 46 original historical annotations R4830–R4875, 44 chapter clauses and two following LXXXIV navigation markers; 8 source passages; 17 unresolved limitations. Three original PDF482–484 JPEG witnesses hashed; no full blind diplomatic transcription or modern chart recast claimed. Source, archive extraction and index tests passed.

**After authenticated research publication:** Lilly **4,875** plus retained Ptolemy **1,066** = **5,941 historical documentary records**. No individually named, prospectively frozen case or independently authenticated restoration outcome, no new empirical astrology validations or runtime model changes.

Owner ZIP: Astrology-Lilly-Chapter-LXXXIII-Restoration-Documentary-20261016.zip in Downloads, with CRC and individual SHA-256 verification and 16 extracted test replays passed.

**NEXT:** LXXXIV occupational/profession aptitude, original PDF484 below divider; parent research OPEN.
"""
prefix="""# Original Lilly source research — Chapter LXXXIII restoration

Current 2026-10-16: LXXXIII original historical source locally admitted, subject to authenticated research-branch publication. Lilly 4,875 + Ptolemy 1,066 = 5,941 documentary annotations after remote proof. Next LXXXIV profession aptitude begins original PDF484 below divider. New independent empirical validations zero; runtime promotions zero. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04c_CHAPTER_LXXXIII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(prefix+OLDCUR.read_text(),encoding="utf-8")
LATEST.write_text(report,encoding="utf-8")
rec={"batch":"B04c","status":"GUARDED_CANONICAL_PREPARED_NOT_REMOTE","previous_index_git_blob_sha1":oldblob,
 "previous_index_sha256":H(OLD),"new_index_sha256":H(IDX),
 "current_state_sha256":H(CUR),"latest_state_sha256":H(LATEST),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "documentary_records_added":46,"lilly_if_published":4875,"ptolemy_retained":1066,
 "combined_if_published":5941,"next_chapter":"LXXXIV","next_original_pdf_page":484,
 "independently_verified_restorations":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
