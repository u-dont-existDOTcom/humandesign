from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
C=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
L=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04k_CHAPTER_XCI_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04k.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04k.md"
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads(I.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert not L.exists() and not OLD.exists()
assert j["records_count"]==5222 and j["batches"][-1]["id"]=="B04j"
assert j["next"]["chapter"]=="XCI" and j["next"]["pdf_page"]==495
assert j["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert j["read_numbered_chapters"]==list(range(1,91))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert h(B/"RULES.json")==A["rules_sha256"]==Z["rules_sha256"]
assert h(Z["owner_download_path"])==Z["archive_sha256"]
assert subprocess.run(["git","diff","--quiet","HEAD","--",str(I.relative_to(ROOT))],cwd=ROOT).returncode==0
OLD.parent.mkdir(parents=True,exist_ok=True);OLD.write_bytes(I.read_bytes());OLDC.write_bytes(C.read_bytes())
j["batches"].append({"id":"B04k","path":"batches/B04k/RULES.json","records_count":85,
 "sha256":A["rules_sha256"],
 "scope":"Lilly first edition printed XC/editorial XCI imprisonment and release, PDF495-497, 83 historical conditional source claims, two next-chapter markers; lunar speed, freedom, recapture, peril and prison break unverified."})
j["records_count"]=5307;j["read_numbered_chapters"].append(91)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCI_DOCUMENTARY_NEXT_XCII_OPEN"
j["next"]={"pdf_page":497,"printed_page":463,"chapter":"XCII","printed_chapter_numeral":"XCI",
 "heading":"Of a Captive or Slave","include_opening_paragraph":True,
 "extracted":False,"boundary_image_read":True,
 "position":"Original PDF497/printed463 below printed Chapter XC imprisonment conclusion and horizontal divider."}
j["current_state"]=str(L.relative_to(ROOT))
j["chapter_XCI_source_acceptance_note"]="85 historical text-only annotations R5223–R5307, 83 imprisonment and harm-related source clauses plus 2 next-chapter navigation; no independent prisoner outcome evidence."
assert j["records_count"]==sum(x["records_count"] for x in j["batches"])==5307
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
L.write_text("# Lilly first edition: printed XC / editorial XCI — imprisonment and release\n\nSource original PDF495–497, printed 461–463, original Wellcome 1647 full PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. First-edition printed XC is editorial sequential XCI. Distinct source conditions propose quick release, slow detention, repeat imprisonment, escape or breaking prison, no release and harms including unsupported medical/death allegations. Nothing verifies actual persons, imprisonment outcomes, medical harm, or successful forecasts.\n\nAccepted documentary historical records **R5223–R5307 (85)**, of which 83 are chapter source clauses and two next-chapter markers. Original page hashes frozen and reverse-mapped. ZIP CRC, exact per-member SHA256, full extract and 8 tests passed.\n\nAfter authenticated publication **5,307 Lilly + 1,066 Ptolemy = 6,373** historical documentary records; independent empirical predictions added zero, runtime promotions zero. Next printed XCI / editorial XCII *Of a Captive or Slave*, original PDF497 below divider.\n")
C.write_text("# Original Lilly research — editorial Chapter XCI\n\nLocally accepted prison/release historical source R5223-R5307; after remote publication 5,307 Lilly + 1,066 Ptolemy = 6,373 historical annotations. Next editorial XCII printed XCI original PDF497. Empirical predictive validations zero.\n\n---\n\n"+OLDC.read_text())
P={"batch":"B04k","prior_index_sha256":h(OLD),"new_index_sha256":h(I),"report_sha256":h(L),
 "current_sha256":h(C),"rules_sha256":A["rules_sha256"],"archive_sha256":Z["archive_sha256"],
 "source_records_added":85,"lilly_if_published":5307,"combined_if_published":6373,"empirical_validations":0}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261016.json").write_text(json.dumps(P,indent=2)+"\n")
print(json.dumps(P))
