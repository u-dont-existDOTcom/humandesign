from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04d_CHAPTER_LXXXIV_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04d_CANONICAL.json"
OLDCUR=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04d.md"
REC=B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json"
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==4875 and j["batches"][-1]["id"]=="B04c"
assert j["next"]["chapter"]=="LXXXIV" and j["next"]["pdf_page"]==484
assert j["read_numbered_chapters"]==list(range(1,84))
assert j["source_sha256"]==A["original_pdf_sha256"]
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert A["new_documentary_records"]==R["record_count"]==79
assert R["vocational_glyphs_verified_mars_venus"]
assert A["lilly_if_published"]==4954 and A["combined_if_published"]==6020
assert [r["record_number"] for r in R["rules"]]==list(range(4876,4955))
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==15 and H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=git("rev-parse","HEAD:"+rel)
assert oldblob==git("hash-object",str(IDX))
j["batches"].append({"id":"B04d","path":"batches/B04d/RULES.json",
 "records_count":79,"sha256":A["rules_sha256"],
 "scope":"Original Lilly (1647) Book II LXXXIV profession, magistery and trade horary source. Original PDF484-485 printed450-451, following LXXXV figure navigation on PDF486. 77 historical substantive sign-to-vocation annotations plus two navigation, 15 original source groups, 24 interpretive limits. Mars and Venus vocational significator glyphs visually verified, no independent human vocational prediction."})
j["records_count"]=4954
j["read_numbered_chapters"].append(84)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXXIV_HISTORICAL_SOURCE_ONLY_NEXT_LXXXV_OPEN"
j["next"]={"pdf_page":486,"printed_page":452,"chapter":"LXXXV","printed_chapter_numeral":"LXXXV",
 "heading":"If Prince Rupert should get honour by our Warres, or worst the Earle of Essex?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF486/printed452 new polygonal horary 28 November 1642 9:23 AM; distinct Prince Rupert/Essex historical wartime case."}
j["chapter_LXXXIV_source_acceptance_note"]="79 historical source annotations R4876-R4954, 77 LXXXIV sign-based vocation claims and two LXXXV navigation markers; 15 original passages and 24 uncertainty statements. Query-time figure replaces unknown birth time; Mars and Venus transcribed; no independently verified career outcome."
j["current_state"]=str(LATEST.relative_to(ROOT))
assert j["records_count"]==sum(b["records_count"] for b in j["batches"])==4954
assert j["read_numbered_chapters"]==list(range(1,85))
REPORT="""# Original Lilly 1647 Chapter LXXXIV — Profession, Trade and Magistery

2026-10-16 Africa/Dakar UTC+0. William Lilly, Christian Astrology first edition, original Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Original Chapter LXXXIV begins on PDF484/printed450 below the LXXXIII divider, continues on PDF485/printed451, and finishes there before LXXXV begins on PDF486/printed452 with a separate **28 November 1642, 9:23 AM** Prince Rupert/Essex horoscope. All three original page-image witnesses have SHA-256 and byte sizes frozen.

The opening problem is that country families often lack the recorded time of a child's birth. Lilly therefore advises erecting a **horary figure at the moment the parents ask**, considering first and tenth houses and **Mars and Venus**, the two special trade significators. Enlarged examination of the actual PDF484 confirms the printed Mars and Venus glyphs. Their relative strength guides the subsequent sign branch, not a reconstructed birth chart.

His original lists map Aries and its fiery/animal associations to livestock and crafts; Taurus to husbandry, grain and household manufacture; Gemini to writing, arithmetic and surveying; Leo to hot crafts, hunting, horse work and cattle care; Virgo to secretarial, teaching, accountancy, printing and political/astrological tasks; Libra to speech, poetry, music, textiles and teaching; Scorpio to medicine, surgery, metal and beverage trades; Sagittarius to chemistry, cattle, clergy or cooking; Capricorn to farming and goods; Aquarius to ship work with additional watery aspect qualifications; and Pisces to performance, beverage/fish trades and a harsh, derogatory intelligence judgment. The opening also has overlapping animal, human and watery sign groups and conditional rulership, angularity and exaltation branches.

**Documentary acceptance:** 79 source records **R4876–R4954**: 77 LXXXIV clauses plus two following LXXXV navigation markers. Fifteen original-image passage groups; 24 preserved textual/interpretive limitations. The source uses 1647 social stereotypes and overlapping lists, not independently checked aptitude. No identified child, vocational follow-up, blind comparison, full independent diplomatic transcription or chart parity is supplied.

**After authenticated research-branch publication:** Lilly **4,954** + retained Ptolemy **1,066** = **6,020 historical documentary records**. New independent career prediction validations **zero**; runtime model promotions **zero**.

Owner archive in laptop Downloads: Astrology-Lilly-Chapter-LXXXIV-Professions-Documentary-20261016.zip, SHA/CRC and independent extracted tests replayed (15).

**NEXT:** LXXXV, the Prince Rupert versus Earl of Essex wartime question, original PDF486/printed452. Parent original-source study OPEN.
"""
PREFIX="""# Original Lilly source study — Chapter LXXXIV vocational rules

CURRENT 2026-10-16: locally accepted LXXXIV 79 documentary records. Upon authenticated research-branch publication, cumulative Lilly 4,954 + Ptolemy 1,066 = 6,020 historical original source units. Original Mars+Venus vocational significators visually confirmed on PDF484. No independent career validation; zero runtime model changes. Next LXXXV Prince Rupert/Essex begins PDF486. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04d_CHAPTER_LXXXIV_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
CUR.write_text(PREFIX+OLDCUR.read_text(),encoding="utf-8")
LATEST.write_text(REPORT,encoding="utf-8")
rec={"batch":"B04d","status":"GUARDED_CANONICAL_PREPARED_NOT_REMOTE",
 "previous_index_git_blob_sha1":oldblob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_state_sha256":H(CUR),
 "latest_state_sha256":H(LATEST),"accepted_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],"new_documentary_records":79,
 "lilly_if_published":4954,"ptolemy_retained":1066,"combined_if_published":6020,
 "next_chapter":"LXXXV","next_original_pdf_page":486,
 "independently_verified_vocational_outcomes":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
