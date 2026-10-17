from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
C=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md";L=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04j_CHAPTER_XC_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04j.json";OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04j.md"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads(I.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert not L.exists() and not OLD.exists()
assert j["records_count"]==5193 and j["batches"][-1]["id"]=="B04i"
assert j["next"]["chapter"]=="XC" and j["next"]["pdf_page"]==494
assert j["read_numbered_chapters"]==list(range(1,90))
assert j["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert H(B/"RULES.json")==A["rules_sha256"]==Z["rules_sha256"]
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert subprocess.run(["git","diff","--quiet","HEAD","--",str(I.relative_to(ROOT))],cwd=ROOT).returncode==0
OLD.parent.mkdir(parents=True,exist_ok=True);OLD.write_bytes(I.read_bytes());OLDC.write_bytes(C.read_bytes())
j["batches"].append({"id":"B04j","path":"batches/B04j/RULES.json",
 "records_count":29,"sha256":A["rules_sha256"],
 "scope":"Original Lilly first edition printed LXXXIX editorial XC Twelfth House unnamed secret enemies and alleged illness on PDF494–495, 27 substantive source clauses, 2 navigation, four passages; no independent enemy or medical verification."})
j["records_count"]=5222;j["read_numbered_chapters"].append(90)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XC_SOURCE_ONLY_NEXT_XCI_OPEN"
j["next"]={"pdf_page":495,"printed_page":461,"chapter":"XCI","printed_chapter_numeral":"XC",
 "heading":"Any man committed to Prison, whether he shall be soone Delivered?",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF495/printed461 BELOW secret enemy chapter divider."}
j["current_state"]=str(L.relative_to(ROOT))
j["chapter_XC_source_acceptance_note"]="29 historical clauses R5194–R5222 about anonymous enemy vs named enemy, and unverified health/hostility hypotheses; following imprisonment separate."
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5222
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
L.write_text("# Lilly first edition — secret enemies, printed LXXXIX / editorial XC\n\nOriginal PDF494–495 / printed460–461, Wellcome b30338724, original full PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. Twenty-nine historical annotations **R5194–R5222** include twenty-seven conditions and two next-chapter navigation markers. The source distinguishes unnamed twelfth-house enemy from named seventh-house enemy, unsupported hostile intent from verified action, and speculates about enemy illness or near death without evidence. Four original page spans. No empirically verified enemy identity, actual medical diagnosis, predictive validation, or runtime promotion.\n\nAccepted upon remote readback: **5,222 Lilly + 1,066 Ptolemy = 6,288 historical source units**. Next original printed Chapter XC / editorial XCI *Any man committed to Prison, whether he shall be soone Delivered?*, starts PDF495.\n")
C.write_text("# Original Lilly source research — editorial XC\n\nHistorical original source accepted locally: Lilly 5,222 + retained Ptolemy 1,066 = 6,288 once remote verified. Next XCI original printed XC PDF495. No new empirical validations.\n\n---\n\n"+OLDC.read_text())
P={"batch":"B04j","prior_index_sha256":H(OLD),"new_index_sha256":H(I),"report_sha256":H(L),
 "current_sha256":H(C),"rules_sha256":A["rules_sha256"],"archive_sha256":Z["archive_sha256"],
 "new_documentary_records":29,"lilly_if_published":5222,"combined_if_published":6288,"empirical_validations":0}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261016.json").write_text(json.dumps(P,indent=2)+"\n")
print(json.dumps(P))
