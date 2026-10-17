#!/usr/bin/env python3
"""Guarded original-source canonical admission: lost horse near Henley."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04n_CHAPTER_XCIV_COMPLETE.md"
OLD=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04n.json"
OLDC=B/"recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04n.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
assert not any(x.exists() for x in (OLD,OLDC,LATEST,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();I=json.loads(raw)
A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text())
Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5413 and I["batches"][-1]["id"]=="B04m"
assert I["read_numbered_chapters"]==list(range(1,94))
assert I["next"]["chapter"]=="XCIV" and I["next"]["pdf_page"]==501
assert I["source_sha256"]==A["original_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(q["id"]=="B04n" for q in I["batches"])
assert A["prior_lilly_accepted"]==5413 and A["new_documentary_records"]==44
assert A["lilly_if_published"]==5457 and A["combined_if_published"]==6523
assert A["source_author_timing_shortfall_preserved"] and A["absolute_reported_actual_day_ambiguous"]
assert R["record_count"]==44 and R["independently_authenticated_horse_outcomes"]==0
assert [r["record_number"] for r in R["rules"]]==list(range(5414,5458))
assert all(r["chapter"]=="XCV_NAVIGATION_ONLY" for r in R["rules"][-2:])
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==18 and Z["extracted_exit_code"]==0
assert H(Z["owner_download_path"])==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
blob=git("rev-parse","HEAD:"+rel)
assert blob==git("hash-object",str(IDX))
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDC.write_bytes(CUR.read_bytes())
I["batches"].append({"id":"B04n","path":"batches/B04n/RULES.json",
 "records_count":44,"sha256":A["rules_sha256"],
 "scope":"Original Lilly first-edition printed XCIII/editorial XCIV lost or stolen horse near Henley dated horary 11 Jan 1646 at 2:59 PM on original PDF501–502/printed467–468; 42 substantive source annotations and two next-chapter navigation markers, seven original passage groups, 20 limitations. Lilly predicts within one-to-two days, says horse returned after three, alternatively dates Jan13 or Jan14; timing discrepancy and independent-outcome absence preserved."})
I["records_count"]=5457
I["read_numbered_chapters"].append(94)
I["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_XCIV_HISTORICAL_SOURCE_ONLY_NEXT_XCV_OPEN"
I["next"]={"pdf_page":502,"printed_page":468,"chapter":"XCV",
 "printed_chapter_numeral":"XCIV","heading":"If Bewitched",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF502/printed468 below Henley horse case closing and horizontal divider, separate square horoscope dated Anno 1646 March 13 (exact hour requires visual source audit)."}
I["chapter_XCIV_source_acceptance_note"]="44 historical source annotations R5414-R5457 (42 horse horary and two following separate witchcraft case navigation); predicted return within 1-2 days, self-reported actual three days and date Jan13/14 ambiguity; self-reported westward direction and rider interpretation lack independent corroboration. Seven source passages, 20 unresolved limits, no empirical prediction credit."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(x["records_count"] for x in I["batches"])==5457
assert I["read_numbered_chapters"]==list(range(1,95))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text(encoding="utf-8")
REPORT="""# First-edition Lilly printed XCIII / editorial XCIV — horse lost near Henley

2026-10-17 — Africa/Dakar (UTC+0).

""" + audit + """

## Documentary acceptance and scoring limitations

**44 historically sourced annotations R5414–R5457:** 42 horse-recovery worked-example source units and two next-chapter navigation annotations, seven original-source passage groups, and twenty preserved source/timing limitations. Primary first-edition PDF501–502 page witnesses are hash frozen, and the source-first→record reverse map is complete. ZIP CRC, member hashes, full extraction with 18 replayed tests, plus canonical integration checks pass.

**Predictive-scoring disposition:** The author reports both returning the horse and an earlier-than-actual prediction. The stated one-to-two-day forecast is *not* the same as his own three-day-return account; the alternative January 13/14 date makes exact event timing uncertain. His claimed rider identities and compass direction have no external evidence. Code separately as (a) purported return, (b) self-reported timing discrepancy, and (c) unresolved event timing, with no independently authenticated forecast success. No horoscope has been independently recast.

**After authenticated source publication:** **5,457 Lilly** + **1,066 Ptolemy** = **6,523 historical source records**. New independent predictive validations **zero**, runtime model promotions **zero**.

Owner archive saved in laptop Downloads: Astrology-Lilly-Chapter-XCIV-Henley-Horse-Documentary-20261017.zip, with exact SHA256 in the documentary release receipt.

**Next:** original printed XCIV / editorial XCV, *If Bewitched*, begins below the separate divider on original PDF502. Preserve separate chart and any unverified medical/occult claims. Parent text study OPEN.
"""
LATEST.write_text(REPORT,encoding="utf-8")
PREFIX="""# Original Lilly source research — printed XCIII / editorial XCIV horse case

2026-10-17: 44 historical documentary records R5414-R5457 accepted locally, cumulative Lilly 5,457 + Ptolemy 1,066 = **6,523** after verified publication. Crucial negative: prediction within a day or two versus Lilly's reported return three days later, with 13th/14th January alternative actual dates. No independent horse outcome or empirical astrology validation. Next editorial XCV printed XCIV *If Bewitched* begins original PDF502/printed468. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04n_CHAPTER_XCIV_COMPLETE.md.

---

"""
CUR.write_text(PREFIX+OLDC.read_text(encoding="utf-8"),encoding="utf-8")
rec={"batch":"B04n","status":"GUARDED_CANONICAL_INDEX_PREPARED_PENDING_REMOTE",
 "parent_index_git_blob_sha1":blob,"previous_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"current_state_sha256":H(CUR),
 "latest_report_sha256":H(LATEST),
 "accepted_rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "new_documentary_records":44,"lilly_if_published":5457,
 "ptolemy_retained":1066,"combined_if_published":6523,
 "author_timing_discrepancy_preserved":True,
 "return_date_jan_13_or_14_ambiguous":True,
 "next_editorial_chapter":"XCV","next_printed_chapter":"XCIV",
 "next_original_pdf_page":502,
 "independent_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
