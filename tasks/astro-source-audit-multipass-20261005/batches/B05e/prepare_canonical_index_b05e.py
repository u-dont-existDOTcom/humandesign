#!/usr/bin/env python3
"""Guarded first-edition four-humours chapter documentary index, no clinical inference."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05e_TEMPERAMENT.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B05e.json"
PRIOR=B/"recovery/CURRENT_BEFORE_B05e.md"
PRIOR_PROGRESS=B/"recovery/PROGRESS_BEFORE_B05e.md"
RECEIPT=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(q.exists() for q in (OLD,PRIOR,PRIOR_PROGRESS,LATEST,RECEIPT))
I=json.loads(IDX.read_text(encoding="utf-8"))
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6415 and I["batches"][-1]["id"]=="B05d"
assert I["next"]["chapter"]=="CVII" and I["next"]["pdf_page"]==566
assert I["read_numbered_chapters"]==list(range(1,107))
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert A["new_documentary_records"]==R["record_count"]==59
assert A["lilly_if_published"]==6474 and A["combined_if_published"]==7540
assert [r["record_number"] for r in R["rules"]]==list(range(6416,6475))
assert all(r["chapter"]=="CVIII_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert not any(q["id"]=="B05e" for q in I["batches"])
assert Z["crc_pass"] and Z["all_member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==19
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PRIOR.write_bytes(CUR.read_bytes());PRIOR_PROGRESS.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B05e","path":"batches/B05e/RULES.json",
 "records_count":59,"sha256":A["rules_sha256"],
 "scope":"Original first-edition William Lilly printed CHAP CVI/editorial CVII humoral complexion/temperament historical rules, PDF566-568; following CVII Manners navigation PDF568-569. 56 substantive historical annotations, three next navigation, nine source passages, 23 limits. Five natal significator categories; oriental/occidental planets, Moon quarters, seasonal Sun and sign triplicities; explicit Saturn/Mars adverse overlay, opposing equal quality cancellation, conditional triple count for lord-geniture plus Ascendant ruler and double Moon-in-Ascendant count. No biological/personality validation or runtime promotion."})
I["records_count"]=6474
I["read_numbered_chapters"].append(107)
I["status"]="BOOK_III_FOUR_HUMOURS_HISTORICAL_SOURCE_ADMITTED_NEXT_MANNERS_OF_NATIVE"
I["next"]={"pdf_page":568,"printed_page":534,"chapter":"CVIII",
 "printed_chapter_numeral":"CVII",
 "heading":"Of the Manners of the Native or Child",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF568 lower part after complexion divider, original PDF569 and following pages. Locate next original printed heading before source extraction.",
 "research_relevance":"Historical human personality claims only. Compare to blinded questionnaire targets only after complete rule and score freeze, not retrospective profiling."}
I["chapter_CVII_source_acceptance_note"]="59 source-only annotations R6416-R6474. Humoral quality testimony list, lunar phases, Sun seasons, zodiac triplicities, malefic overlay, equal opposing cancellation, 3x lord geniture plus Asc ruler and 2x Moon in first; all historical beliefs with zero independent biomedical or personality validation."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==6474
assert I["read_numbered_chapters"]==list(range(1,108))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
LATEST.write_text("# William Lilly original four-humour temperament chapter — historical source accepted\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n## Historical source admission and scientific disposition\n\n**59 original documentary annotations R6416–R6474** (56 substantive source clauses and 3 following manners-navigation), nine primary page groups, 23 explicit limitations. Original first-edition full pages PDF566–569 SHA256/bytes verified, forward and reverse mappings intact, ZIP CRC/hash/full extraction and 19 replayed tests.\n\n**After authenticated publication:** **6,474 Lilly + 1,066 Ptolemy = 7,540** historical annotations. These are not 7,540 independent successful behavior predictions. The original historical four-humour categories have no independently confirmed clinical validity or blinded personality predictive result in this source research lane; zero model/scorer runtime promotions.\n\n**NEXT:** original printed CHAP CVII / editorial CVIII on manners and mind begins original PDF568 below divider; its decision logic must be extracted and independently tested as historical documentary first.\n",encoding="utf-8")
PROGRESS.write_text("# Astrology original-source progress — 2026-10-17 through temperament\n\n**7,540 historical source annotations accepted** (6,474 Lilly + 1,066 retained Ptolemy). First-edition Lilly scan source frontier through original PDF568 of 894 pages, approximately 63.5% of scan position only, not proportion of machine-readable rule completion or empirical model science. Four-humour testimony weights are now historical-source preserved but not human validated. Last newly accepted source printed CVI, next is printed CVII *Manners of the Native*. Prior open dense numeric table reconstructions, independent birth-time / questionnaire validation and prospective outcome testing remain open. Empirical validations and promoted executable rules attributable to historical source batches zero.\n\n---\n\n"+PRIOR_PROGRESS.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# Lilly temperament first-edition historic source accepted, Manners next\n\n2026-10-17: B05e 59 historic source annotations R6416-R6474 locally admitted, after authenticated publication **6,474 Lilly + 1,066 Ptolemy = 7,540**. Four-humour hot/cold/moist/dry historical testimony tally, conditional 3x lord-geniture/Asc ruler and 2x Moon-in-Asc, equal adverse cancellation, Saturn/Mars overlay, no validated modern psychometric diagnosis. Next source original printed CVII editorial CVIII Manners PDF568 onward. PDF-position ~63.5% of first-edition scan, not predictive science completion. All historical numerical table tasks and empirical validation remain open.\n\n---\n\n"+PRIOR.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B05e","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "parent_index_blob_sha1":blob,"prior_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_sha256":H(CUR),
 "latest_report_sha256":H(LATEST),"progress_report_sha256":H(PROGRESS),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "new_records":59,"lilly_if_published":6474,"ptolemy_retained":1066,
 "combined_if_published":7540,"next_printed_chapter":"CVII","next_editorial_chapter":"CVIII",
 "next_original_pdf":568,"empirical_validations":0,"runtime_promotions":0,"remote_published":False}
RECEIPT.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
