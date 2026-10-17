#!/usr/bin/env python3
"""Guarded append-only canonical Lilly geniture source integration."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05d_LORD_GENITURE.md"
OLD=B/"recovery/INDEX_BEFORE_B05d.json"
PRIOR=B/"recovery/CURRENT_BEFORE_B05d.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(f.exists() for f in (OLD,PRIOR,LATEST,REC))
I=json.loads(IDX.read_text(encoding="utf-8"));A=json.loads((B/"ACCEPTANCE.json").read_text());R=json.loads((B/"RULES.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6383 and I["batches"][-1]["id"]=="B05c"
assert I["read_numbered_chapters"]==list(range(1,106))
assert I["next"]["chapter"]=="CVI" and I["next"]["pdf_page"]==565
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(q["id"]=="B05d" for q in I["batches"])
assert A["new_historical_annotations"]==R["record_count"]==32
assert A["lilly_if_published"]==6415 and A["combined_if_published"]==7481
assert [r["record_number"] for r in R["rules"]]==list(range(6384,6416))
assert all(r["chapter"]=="CVII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert not Z["remote_published"] and Z["zip_crc_pass"] and Z["full_extraction_pass"] and Z["member_sha256_pass"]
assert Z["extracted_tests_passed"]==17
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
assert H(Z["owner_download_path"])==Z["archive_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
oldblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert oldblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PRIOR.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B05d","path":"batches/B05d/RULES.json",
 "records_count":32,"sha256":A["rules_sha256"],
 "scope":"First-edition William Lilly printed CHAP CV/editorial CVI Lord of Geniture original PDF565-566, with following complexion CHAP CVI navigation PDF566-567. 29 historical source details +3 following navigation, 6 source spans, 19 limitations. Rejected Firmicus next-Moon-sign scheme, competing all-point essential dignity aggregate and Greek Moon/Mercury dignity approach, Lilly preferred combined essential/accidental strength, elevation, nearequal runnerup mixture and aspects. No numeric weights fixed, no empirical personality evidence."})
I["records_count"]=6415
I["read_numbered_chapters"].append(106)
I["status"]="BOOK_III_LORD_GENITURE_SOURCE_ACCEPTED_NEXT_COMPLEXION_TEMPERAMENT"
I["next"]={"pdf_page":566,"printed_page":532,"chapter":"CVII",
 "printed_chapter_numeral":"CVI","heading":"Of the Complexion or Temperament of the Body; quality of the Planets and Signes",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF566 lower portion below separate CHAP CVI divider, continues PDF567 and the top of PDF568; next printed CHAP CVII begins below a divider on PDF568.",
 "source_safety":"Original medical/humoral terminology is historical only, no clinical diagnosis or validated personality scoring."}
I["lord_geniture_source_acceptance_note"]="32 source-only annotations R6384-R6415, three separately coded competing selection methods and rejected Firmicus sign successor; near equal planet blending without fixed weights. No independent human personality matches or runtime rules."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6415
assert I["read_numbered_chapters"]==list(range(1,107))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
LATEST.write_text("# Original first-edition Lilly Lord of the Geniture — historical source accepted\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n**Documentary acceptance:** 32 historical source annotations R6384–R6415 (29 chapter clauses, three next-chapter navigation), six source passage groups and 19 preserved limitations. Exact original JPEG witnesses PDF565–567, CRC/SHA/full extraction with 17 replayed tests and separate canonical integration checks.\n\n**After verified publication:** **6,415 Lilly** + **1,066 Ptolemy** = **7,481 historical source records**, not independent personality successes. No human data validated; no runtime scoring promoted. Next printed CHAP CVI / editorial CVII, humoral temperament, starts original PDF566 below divider, ends above next printed CHAP CVII divider on PDF568.\n",encoding="utf-8")
CUR.write_text("# Lilly original Lord-of-Geniture alternatives documented; temperament next\n\n2026-10-17: B05d historic source annotations R6384–R6415 locally accepted, to reach **6,415 Lilly +1,066 Ptolemy = 7,481** after remote publication. Source offers rejected next-sign approach, alternative aggregate dignity, preferred combined essential+accidental strength and near-equal blend, and Greek Moon/Mercury basis. None has independent behavioral validation or executable-scoring promotion. Next original printed CVI / editorial CVII temperament PDF566–568. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05d_LORD_GENITURE.md.\n\n---\n\n"+PRIOR.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B05d","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "prior_git_blob_sha1":oldblob,"prior_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),"report_sha256":H(LATEST),
 "rules_sha256":A["rules_sha256"],"archive_sha256":Z["archive_sha256"],
 "source_records_added":32,"lilly_if_published":6415,
 "ptolemy_retained":1066,"combined_if_published":7481,
 "next_printed_chapter":"CVI","next_editorial_chapter":"CVII",
 "next_original_pdf_page":566,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
