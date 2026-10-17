#!/usr/bin/env python3
"""Guarded append-only integration of Lilly's 1647 manners chapter as history only."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05f_MANNERS.md"
OLD=B/"recovery/INDEX_BEFORE_B05f.json";PRIOR=B/"recovery/CURRENT_BEFORE_B05f.md"
PPRIOR=B/"recovery/PROGRESS_BEFORE_B05f.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(f.exists() for f in (OLD,PRIOR,PPRIOR,LATEST,REC))
I=json.loads(IDX.read_text(encoding="utf-8"));A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==6474 and I["batches"][-1]["id"]=="B05e"
assert I["read_numbered_chapters"]==list(range(1,108))
assert I["next"]["chapter"]=="CVIII" and I["next"]["pdf_page"]==568
assert I["source_sha256"]==A["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(b["id"]=="B05f" for b in I["batches"])
assert R["record_count"]==A["new_documentary_records"]==86
assert A["lilly_if_published"]==6560 and A["combined_if_published"]==7626
assert [r["record_number"] for r in R["rules"]]==list(range(6475,6561))
assert all(r["chapter"]=="CIX_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert Z["crc_pass"] and Z["per_member_sha256_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==20 and H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert blob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(IDX.read_bytes());PRIOR.write_bytes(CUR.read_bytes());PPRIOR.write_bytes(PROGRESS.read_bytes())
I["batches"].append({"id":"B05f","path":"batches/B05f/RULES.json",
 "records_count":86,"sha256":A["rules_sha256"],
 "scope":"Original first edition William Lilly printed CHAP CVII/editorial CVIII Manners of Native/Child, original PDF568-573 body, following CVIII PDF573-575 navigation. 83 substantive historical source annotations and 3 separate next chapter navigation, 14 original passage groups, 30 cautions. Historical significator selection with Asc/Mercury/Moon/dispositor fallbacks and lunar-direction change, broad 12 sign and four-humour manner stereotypes, epoch-dependent fixed stars and severe historically unsupported moral/criminal accusations, rejection of Johannes Angelus degree-by-degree inflexibility. All human personality accuracy, actual violence predictions and runtime promotions zero."})
I["records_count"]=6560;I["read_numbered_chapters"].append(108)
I["status"]="BOOK_III_MANNERS_OF_NATIVE_COMPLETE_HISTORICAL_DOCUMENTARY_NEXT_PLANET_SPECIFIC_MANNERS"
I["next"]={"pdf_page":573,"printed_page":539,
 "chapter":"CIX","printed_chapter_numeral":"CVIII",
 "heading":"The quality of Manners, which may in kind be discerned from every Planet",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Separate chapter begins below original horizontal divider in lower PDF573/printed539; continues PDF574-575 and needs actual following chapter boundary verified.",
 "research_scope":"Preserve positive/negative traits and exact planetary placement conditions, but do not use source stereotypes as established human behavior or forensic predictions."}
I["chapter_CVIII_source_acceptance_note"]="86 historical source records R6475-R6560 (83 manners/fixed-star/sign/humour clauses, 3 next navigation), 14 original page groups, 30 cautionary notes. No independent actual person character/violent act/outcome validated; multiple source fallbacks, lunar direction change and conflicting trait descriptions preserved."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(q["records_count"] for q in I["batches"])==6560
assert I["read_numbered_chapters"]==list(range(1,109))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
LATEST.write_text("# Original Lilly first-edition manners and personality stereotypes — historical source accepted\n\n2026-10-17 Africa/Dakar UTC+0.\n\n"+audit+
"\n## Source admission and scientific limits\n\n**86 historical documentary annotations R6475–R6560**, 83 chapter clauses and 3 following chapter navigation, 14 first-edition source image groups and 30 qualifications. Source PDF568–575 SHA/byte preserved; full source-first reverse mapping, ZIP CRC, per-member hash, full extraction and 20 replayed tests passed.\n\nNo original independent human personality test, corroboration of accused violence or criminal conduct, psychiatric diagnosis, or validated astrological forecast. These are historical assertions only. No output from this source was promoted into human-scoring runtime. Following printed Chapter CVIII begins below horizontal divider on PDF573.\n\n**After authenticated publication** **6,560 Lilly + 1,066 Ptolemy = 7,626 historical documentary records**. New empirical validations **0**, runtime promotions **0**.\n",encoding="utf-8")
PROGRESS.write_text("# First-edition Lilly source progress after manners, 2026-10-17\n\n**7,626 historical documentary annotations** accepted after authenticated publication (6,560 Lilly + 1,066 retained Ptolemy). Lilly original scan frontier PDF573 of 894 scanned pages, **64.1% by page-position proxy only**. This is NOT percentage of numerically transcribed table cells, verified predictive human traits or the project's overall goal. Printed CHAP CVII manners historical source has 86 new annotations, no validated human personality, mental health, criminal dangerousness or predictive findings. Next original printed CHAP CVIII, quality of manners from planets PDF573 onwards. Numerical tables, hidden-label human trials and actual prospective controls remain unfinished.\n\n---\n\n"+PPRIOR.read_text(encoding="utf-8"),encoding="utf-8")
CUR.write_text("# Original Lilly manners chapter now historical-source complete, separate planetary manners next\n\n2026-10-17: Lilly source records R6475–R6560 accepted locally (86 new); after verified research publication **6,560 Lilly + 1,066 retained Ptolemy = 7,626** historical source annotations. All source-specific personality claims, severe fixed-star moral/criminal stereotypes and 12 zodiac descriptions are historical only and unvalidated. Next printed CHAP CVIII/editorial CIX begins original PDF573. Source frontier ~64.1% of 894 scanned pages by position only, not full model completion. No new empirical validations or runtime changes.\n\n---\n\n"+PRIOR.read_text(encoding="utf-8"),encoding="utf-8")
receipt={"batch":"B05f","status":"GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
 "old_index_git_blob_sha1":blob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"latest_report_sha256":H(LATEST),
 "progress_report_sha256":H(PROGRESS),"current_sha256":H(CUR),
 "accepted_rules_sha256":A["rules_sha256"],"owner_archive_sha256":Z["archive_sha256"],
 "historical_records_added":86,"lilly_if_published":6560,
 "ptolemy_retained":1066,"combined_if_published":7626,
 "next_original_pdf":573,"next_printed_chapter":"CVIII","next_editorial_chapter":"CIX",
 "independently_validated_personality":0,"empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
REC.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
