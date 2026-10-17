from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_POST_XCVI_BOUNDARY_CORRECTION_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B04r_SOURCE_BOUNDARY_CORRECTION.json"
PREV=B/"recovery/CURRENT_BEFORE_B04r_SOURCE_BOUNDARY_CORRECTION.md"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(p.exists() for p in (OLD,PREV,REPORT))
j=json.loads(I.read_text())
assert j["records_count"]==5586 and j["batches"][-1]["id"]=="B04q"
assert j["next"]["chapter"]=="POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES"
assert j["read_numbered_chapters"]==list(range(1,98))
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert subprocess.run(["git","diff","--quiet","HEAD","--",str(I.relative_to(ROOT))],cwd=ROOT).returncode==0
originalblob=subprocess.check_output(["git","rev-parse","HEAD:"+str(I.relative_to(ROOT))],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(I.read_bytes());PREV.write_bytes(CURRENT.read_bytes())
names={507:"UNNUMBERED_ESSEX",508:"PLANETARY_HOUR_TABLE_START",515:"PLANETARY_HOUR_TABLE_END",516:"PRINTED_CHAP_XCVII_START",520:"BOOK_II_SIGNED_CONCLUSION",521:"BOOK_III_TITLE"}
w=[]
for n,name in names.items():
 p=B/"evidence"/f"pdf_1647-{n}.jpg"
 w.append({"original_pdf_page":n,"role":name,"bytes":p.stat().st_size,"sha256":H(p)})
assert w[3]["sha256"]=="90c7e9d1fb07bebf45045a3b0aedb5064d5e246234f4959175e5623e18ade064"
assert w[5]["sha256"]=="ace314d80394c1ab22b58e4525d24cf82aacbfd1b8909bdeff48afd267be1d17"
j["status"]="BOOK_II_THROUGH_PRINTED_XCVI_ACCEPTED_ESSEX_TABLES_PRINTED_XCVII_STILL_OPEN"
j["next"]["postchapter_source_order"]=[{"type":"UNNUMBERED_ESSEX","pdf_page":507},{"type":"PLANETARY_HOUR_TABLE","first_pdf":508,"last_pdf":515},{"type":"PRINTED_CHAPTER_XCVII","first_pdf":516,"last_pdf":520},{"type":"NEXT_BOOK_TITLE","pdf_page":521}]
j["postchapter_20261017_original_source_correction"]="Original scan PDF516 explicitly prints CHAP. XCVII on planetary hours after an eight-page table PDF508–515; prior assertion that XCVI was final numbered Book II chapter is superseded. No source annotations added."
j["current_state"]=str(REPORT.relative_to(ROOT))
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
body=(B/"SOURCE_BOUNDARY_CORRECTION_20261017.md").read_text()
REPORT.write_text("# Corrected Lilly original Book II source frontier\n\n"+body+"\n**Accepted historical counts remain unchanged:** 5,586 Lilly + 1,066 Ptolemy = 6,652 records; next R5587. The prior boundary claim is superseded, not deleted.\n")
CURRENT.write_text("# Corrected Lilly source frontier (2026-10-17)\n\nPrinted Chapter XCVI was **not** last numbered chapter. Source PDF507 has unnumbered Essex figure; PDF508-515 planetary-hour table; **printed Chapter XCVII PDF516-520**; Book III starts PDF521. Accepted source count remains Lilly **5,586** + Ptolemy **1,066** = **6,652**, next R5587. Continue separate source extraction and include all postchapter units. See state/ASTROLOGY_SOURCE_AUDIT_POST_XCVI_BOUNDARY_CORRECTION_20261017.md.\n\n---\n\n"+PREV.read_text())
rec={"batch":"B04r","kind":"SOURCE_COVERAGE_BOUNDARY_CORRECTION_NO_NEW_RECORDS",
 "old_index_git_blob_sha1":originalblob,"old_index_sha256":H(OLD),"new_index_sha256":H(I),
 "report_sha256":H(REPORT),"current_sha256":H(CURRENT),
 "original_pdf_sha256":j["source_sha256"],"page_witnesses":w,
 "lilly_records_unchanged":5586,"ptolemy_retained":1066,"combined_unchanged":6652,
 "next_global_record":5587,"new_documentary_records":0,
 "empirical_validations":0,"runtime_promotions":0}
(B/"SOURCE_ORDER_CORRECTION_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps({"status":"corrected","pages":[x["original_pdf_page"] for x in w],"lilly":5586,"next":"ESSEX, TABLE, XCVII, BOOK III"}))
