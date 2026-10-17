#!/usr/bin/env python3
"""Guarded append-only original Hyleg source admission with no mortality model promotion."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05c_HYLEG_SOURCE.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B05c.json"
OLDSTATE=B/"recovery/CURRENT_BEFORE_B05c.md"
OLDPROGRESS=B/"recovery/PROGRESS_BEFORE_B05c.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in (OLD,OLDSTATE,OLDPROGRESS,REPORT,REC))
I=json.loads(IDX.read_text(encoding="utf-8"))
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6309 and I["batches"][-1]["id"]=="B05b"
assert I["next"]["chapter"]=="CV" and I["next"]["pdf_page"]==561
assert I["read_numbered_chapters"]==list(range(1,105))
assert I["source_sha256"]==A["original_source_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(x["id"]=="B05c" for x in I["batches"])
assert A["added_documentary_records"]==R["record_count"]==74
assert A["lilly_if_published"]==6383 and A["combined_if_published"]==7449
assert [x["record_number"] for x in R["rules"]]==list(range(6310,6384))
assert all(x["chapter"]=="CVI_NAVIGATION_ONLY" for x in R["rules"][-3:])
assert A["original_author_skepticism_explicit"] and not A["original_Alcochodon_years_independent_accuracy"]
assert Z["crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==19
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());OLDSTATE.write_bytes(CUR.read_bytes());OLDPROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B05c","path":"batches/B05c/RULES.json",
 "records_count":74,"sha256":A["rules_sha256"],
 "scope":"Original first edition Lilly 1647 printed CHAP CIV/editorial CV Hyleg Hylech Apheta Anareta Alcochodon historic lifespan source, PDF561–565 (following Chapter CV starts below divider on PDF565; PDF566 navigation context). 71 substantive original-source clauses plus 3 following Lord of Geniture navigation, 7 first-edition passage groups, 30 limits. Conditional sect, house eligibility 1/10/11/7/9, 25 degree Ascendant exception, multiple syzygy/dignity and Anareta contenders, 5 degrees before/25 after eighth cusp, competing Arabic and earlier sources, Alcochodon alleged planetary years. Lilly explicitly says he is unsatisfied selecting Hyleg, Anareta, Alcochodon, and has no independent human mortality validation."})
I["records_count"]=6383
I["read_numbered_chapters"].append(105)
I["status"]="BOOK_III_HYLEG_ANARETA_ALCOCHODON_HISTORICAL_SOURCE_ADMITTED_AUTHOR_UNCERTAINTY_RETAINED"
I["next"]={"pdf_page":565,"printed_page":531,
 "chapter":"CVI","printed_chapter_numeral":"CV",
 "heading":"Of the Lord of the Geniture",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF565/printed531 below divider contains distinct CHAP CV on Lord of Geniture; PDF566 continues. Historical retrospective source study only.",
 "outstanding_numeric_parity":[
 {"kind":"BOOK_II_PLANETARY_HOURS","source_original_pages":list(range(508,516))},
 {"kind":"BOOK_III_RIGHT_OBLIQUE_ASCENSIONS","source_original_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_MONTH_NUMERIC","source_original_pages":[536]},
 {"kind":"BOOK_III_ASTROLOGICAL_SPECULUM","source_original_pages":[543]},
 {"kind":"BOOK_III_PLANETARY_YEARS_REFERENCED_BY_ALCOCHODON","printed_source_pages":"57-83"}]}
I["chapter_CV_source_acceptance_note"]="74 original source R6310-R6383 annotations, seven mapped passage groups, 30 source limits. Historical potentially lethal directions are unvalidated; source branches include multiple candidate Hylegs/Anaretas/Alcochodons, including explicit degrees and fallback preferences. Lilly says not satisfied how to identify these or their claimed year values; no independent survival outcome."
I["current_state"]=str(REPORT.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6383
assert I["read_numbered_chapters"]==list(range(1,106))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT.write_text("# First edition Lilly Hyleg, Anareta and Alcochodon: historical source accepted\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n**Source acceptance:** 74 historical source clauses R6310–R6383, 71 substantive and three separate next-chapter navigation. Seven source-page groups and 30 explicit limitations. Source images PDF561–566 SHA256 and full ZIP CRC validated. Lilly's doubts about all three life-span selection methods are original authorial statements, not an assistant inference. They do not imply controlled empirical falsification; they do preclude treating the procedures as historically certain.\n\nArchive placed directly in Linux Downloads: Astrology-Lilly-Chapter-CV-Hyleg-Historical-Source-20261017.zip; full extraction, CRC, source member SHA256s and 19 tests replayed.\n\nAfter verified GitHub publication: **6,383 Lilly + 1,066 Ptolemy = 7,449 historical documentary annotations**. Zero independently authenticated predicted deaths, birth-times or clinical effects; no astrology runtime changes. Next printed CHAP CV on Lord of Geniture begins below divider PDF565.\n",encoding="utf-8")
PROGRESS.write_text("# Lilly first edition source progress — Hyleg historic uncertainty documented\n\n2026-10-17: historical original source frontier through PDF565 of 894 scanned pages, approximately **63.2% by physical scan position**. Accepted documentary annotations after verified publication: **6,383 Lilly + 1,066 Ptolemy = 7,449**. Not empirical successful predictions. Printed CHAP CIV's Hyleg, Anareta and Alcochodon selection methods retained with author Lilly's two explicit statements of being not satisfied he can identify them properly. Historic infant/death claims remain medically unsupported, no independent mortality or birth-time outcomes, no runtime promotion. Multiple original numeric tables and blind human model validation still OPEN. Next printed CHAP CV Lord of Geniture original PDF565.\n\n---\n\n"+OLDPROGRESS.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# Lilly Hyleg historical source documented with explicit author doubt; Lord of Geniture next\n\n2026-10-17: 74 historical first edition annotations R6310-R6383 locally admitted, after authenticated remote publication total **6,383 Lilly + 1,066 Ptolemy = 7,449**. Original PDF561-565 printed CIV/editorial CV, next printed CHAP CV starts PDF565 lower. Distinct Hyleg, Anareta and Alcochodon alternative selection branches and original explicit negative assessment are recorded. No individual clinical/natal predictive validation or runtime promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05c_HYLEG_SOURCE.md.\n\n---\n\n"+OLDSTATE.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B05c","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "original_git_blob_sha1":blob,"original_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),
 "latest_report_sha256":H(REPORT),"progress_report_sha256":H(PROGRESS),
 "rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "new_documentary_records":74,"lilly_if_published":6383,
 "ptolemy_retained":1066,"combined_if_published":7449,
 "original_author_uncertainty_preserved":True,
 "next_printed_chapter":"CV","next_editorial_chapter":"CVI",
 "next_original_pdf_page":565,
 "new_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
