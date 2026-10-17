from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04i_CHAPTER_LXXXIX_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04i.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04i.md"
assert not OLD.exists() and not LATEST.exists()
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads(I.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text())
z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").read_text())
assert j["records_count"]==5161 and j["batches"][-1]["id"]=="B04h"
assert j["next"]["chapter"]=="LXXXIX" and j["next"]["pdf_page"]==493
assert j["empirical_validations"]==j["runtime_promotions"]==0
assert j["read_numbered_chapters"]==list(range(1,89))
assert H(z["owner_download_path"])==z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==z["accepted_rules_sha256"]
assert j["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert subprocess.run(["git","diff","--quiet","HEAD","--",str(I.relative_to(ROOT))],cwd=ROOT).returncode==0
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(I.read_bytes());OLDC.write_bytes(CUR.read_bytes())
j["batches"].append({"id":"B04i","path":"batches/B04i/RULES.json",
 "records_count":32,"sha256":A["rules_sha256"],
 "scope":"Lilly first edition original printed LXXXVIII, stable editorial LXXXIX, friendship, secret wishes and mutual love on PDF493/printed459; 30 clauses, 2 next-chapter navigation records, 4 source spans, 14 limitations; no independent relationship outcomes."})
j["records_count"]=5193
j["read_numbered_chapters"].append(89)
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_LXXXIX_HISTORICAL_SOURCE_ONLY_NEXT_XC_OPEN"
j["next"]={"pdf_page":494,"printed_page":460,"chapter":"XC","printed_chapter_numeral":"LXXXIX",
 "heading":"Of secret Enemies, not named","include_opening_paragraph":True,
 "extracted":False,"boundary_image_read":True,
 "position":"Original PDF494/printed460 after Twelfth House divider; printed LXXXIX editorial XC."}
j["current_state"]=str(LATEST.relative_to(ROOT))
j["chapter_LXXXIX_source_acceptance_note"]="Printed LXXXVIII friendship, secrecy of wishes and mutual love; 32 documentary records R5162-R5193, four source passages, no empirical validation."
assert sum(x["records_count"] for x in j["batches"])==5193
assert j["read_numbered_chapters"]==list(range(1,90))
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
report="# Original Lilly Friendship and Mutual Love — printed LXXXVIII / editorial LXXXIX\n\nOriginal first-edition 1647 William Lilly, Wellcome b30338724, full original PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. Chapter is wholly on PDF493/printed459; next Twelfth House and printed chapter LXXXIX begin PDF494/printed460.\n\nLilly distinguishes friendship agreement through first/Moon to eleventh applications (trine or sextile favorable, square or opposition conflict; opposition worse) from a separately framed hidden wish and another subsection asking whether two people love one another. Secret wishes depend on Fortunes angular/succedent but named wishes transfer to topical houses. Mutual love branches compare 11th, 7th, 3rd and twelfth-house interferences, fixed sign modifiers, and outward displays versus inner feelings. None is an independently verified relationship outcome.\n\nHistorical source batch: **32 annotations R5162–R5193**, 30 substantive and two following-section navigation; four mapped primary page passage groups and fourteen unresolved limitations. ZIP CRC, per-member SHA256 and fully extracted 7 tests passed.\n\nAfter publication **5,193 Lilly + 1,066 Ptolemy = 6,259 historical records**. New independent empirical astrology validations **zero**; runtime promotions **zero**. Next editorial XC, printed LXXXIX: secret unnamed enemies on original PDF494.\n"
LATEST.write_text(report)
CUR.write_text("# Original Lilly source research — friendship\n\n2026-10-16: LXXXIX editorial (printed LXXXVIII), 32 historical records locally accepted. Once published 5,193 Lilly + 1,066 Ptolemy = 6,259 historical records; next editorial XC printed LXXXIX original PDF494. No empirical forecast validation. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04i_CHAPTER_LXXXIX_COMPLETE.md.\n\n---\n\n"+OLDC.read_text())
rec={"batch":"B04i","state":"GUARDED_INDEX_PREPARED","old_index_sha256":H(OLD),
 "new_index_sha256":H(I),"current_sha256":H(CUR),"report_sha256":H(LATEST),
 "rules_sha256":A["rules_sha256"],"archive_sha256":z["archive_sha256"],
 "records_count":5193,"next_chapter":"XC","empirical_validations":0}
(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec))
