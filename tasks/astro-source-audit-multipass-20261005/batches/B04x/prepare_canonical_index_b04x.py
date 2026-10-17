#!/usr/bin/env python3
"""Append guarded Animodar original-source batch and separate progress assessment."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04x_ANIMODAR_COMPLETE.md"
PROGRESS=ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
OLD=B/"recovery/INDEX_BEFORE_B04x.json"
PRIOR=B/"recovery/CURRENT_BEFORE_B04x.md"
REC=B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(x.exists() for x in (OLD,PRIOR,LATEST,REC,PROGRESS))
I=json.loads(IDX.read_text());A=json.loads((B/"ACCEPTANCE.json").read_text())
R=json.loads((B/"RULES.json").read_text());Z=json.loads((B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").read_text())
assert I["records_count"]==5923 and I["batches"][-1]["id"]=="B04w"
assert I["next"]["chapter"]=="C" and I["next"]["pdf_page"]==539
assert I["read_numbered_chapters"]==list(range(1,100))
assert I["source_sha256"]==A["source_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert not any(b["id"]=="B04x" for b in I["batches"])
assert A["prior_lilly"]==5923 and A["new_documentary_records"]==R["record_count"]==34
assert A["lilly_if_published"]==5957 and A["combined_if_published"]==7023
assert [r["record_number"] for r in R["rules"]]==list(range(5924,5958))
assert all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in R["rules"][-3:])
assert A["source_says_Animodar_weaker_than_accidents"]
assert Z["zip_crc_pass"] and Z["member_hashes_pass"] and Z["full_extraction_pass"]
assert Z["extracted_tests_passed"]==19
assert H(Path(Z["owner_download_path"]))==Z["archive_sha256"]
assert H(B/"RULES.json")==A["rules_sha256"]==Z["accepted_rules_sha256"]
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(["git","diff","--quiet","HEAD","--",rel],cwd=ROOT).returncode==0
parentblob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
assert parentblob==subprocess.check_output(["git","hash-object",str(IDX)],cwd=ROOT,text=True).strip()
OLD.parent.mkdir(parents=True,exist_ok=True);OLD.write_bytes(IDX.read_bytes());PRIOR.write_bytes(CURRENT.read_bytes())
I["batches"].append({"id":"B04x","path":"batches/B04x/RULES.json",
 "records_count":34,"sha256":A["rules_sha256"],
 "scope":"Original Lilly 1647 printed CHAP XCIX/editorial C Animodar rectification; PDF539–540/printed505–506, following accidents CHAP C PDF541 navigation only. 31 source clauses plus three next-navigation, 5 passage spans and 22 limits. Ptolemaic preceding syzygy Sun/Moon above horizon, dignity winner/tie and Asc/MC proximity rules; example merchant 15 Sept 1616 full Moon, Sun 2d32 Libra, Saturn choice, estimated 9d02 Capricorn ascendant. Previously accident-adjusted chart cannot independently verify birth time. Lilly explicitly says Animodar and Trutine less sure than accidents."})
I["records_count"]=5957
I["read_numbered_chapters"].append(100)
I["status"]="BOOK_III_PRINTED_XCIX_ANIMODAR_SOURCE_ADMITTED_NEXT_ACCIDENTS_RECTIFICATION_OPEN"
I["next"]={"pdf_page":541,"printed_page":507,
 "chapter":"CI","printed_chapter_numeral":"C",
 "heading":"The Rectification of a Nativity by Accidents, and framing of an Astrologicall Speculum",
 "include_opening_paragraph":True,"extracted":False,"boundary_image_read":True,
 "position":"Original PDF541/printed507 starts new named chapter; primary text continues PDF542 onward. Source-first needed before rules formalization.",
 "outstanding_numeric_transcription":[
 {"kind":"BOOK_II_PLANETARY_HOUR_BOUNDARIES","pdf_first":508,"pdf_last":515},
 {"kind":"BOOK_III_RIGHT_AND_OBLIQUE_ASCENSIONS","pdf_pages":[523,526,527,528,529,530,531,532,533]},
 {"kind":"BOOK_III_GESTATION_TABLE","pdf_page":536}]}
I["book_iii_Animodar_acceptance_note"]="34 source-only records R5924–R5957 (31 Animodar clauses, 3 next Accidents chapter navigation), 5 spans, 22 limits. Historical practitioner compares against already accident-corrected natal figure, gives competing Venus possible dignity, and explicitly judges Animodar and Trutine less sure than accident rectification; no independent birth time verified."
I["current_state"]=str(LATEST.relative_to(ROOT))
assert I["records_count"]==sum(b["records_count"] for b in I["batches"])==5957
assert I["read_numbered_chapters"]==list(range(1,101))
IDX.write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n")
audit=(B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").read_text()
LATEST.write_text("# Original Lilly Book III Animodar — source-only documentary acceptance\n\n"+audit+
"\n**Historical acceptance:** 34 source records R5924–R5957, five passage groups and 22 preserved source limitations. Separate source-image hashes PDF539–541, complete reverse map, ZIP CRC, SHA256, extraction and 19 replayed tests.\n\n"+
"**After publication:** **5,957 Lilly + 1,066 Ptolemy = 7,023** historical documentary annotations. Zero independent validated natal birth-time matches, empirical astrological prediction successes or runtime promotions. Next printed CHAP C on accidents begins PDF541.\n")
PROGRESS.write_text("""# Astrology source study — outcome-focused progress and remaining work
2026-10-17 (Africa/Dakar UTC+0).

## Independent numerical progress estimates

- First-edition Lilly *Christian Astrology* (1647) has **894 scanned PDF pages** (Wellcome source b30338724; public bibliographic metadata also describes printed pages 25-832 and following leaves). Accepted original text frontier through original PDF540, with next distinct chapter beginning PDF541. By simple scan-position metric, **540/894 = 60.4%**. By nominal printed-text position, **506/832 = 60.8%**. These are only positional volume proxies, not verified percentage of transcribed or validated rules.
- Book I and Book II numbered historical prose/source units and Book II conclusion have been accepted. Book III title/introduction, house and ascension tables (image witnesses only for dense tables), Trutine and Animodar are accepted. Book III still has substantial material from printed 507 through 832 and supplemental leaves.
- Accepted after authenticated Animodar batch: **5,957 Lilly** source annotations plus **1,066 Ptolemy** retained historical annotations = **7,023 combined historical documentary records**. Most are clauses, caveats, procedures, examples, table images and navigation, NOT distinct empirically predictive rules, not people, and not independent success cases.
- Outstanding numerics: Book II eight-leaf planetary-hour table PDF508-515 (about 1,488 hour-boundary cells not fully digitized), Book III time-to-angle/right-ascensions/oblique ascensions PDF523/526-533 and historical gestation/month tables PDF536. Full source numeric reconstruction/calibration OPEN.
- Astrological empirical validity: **zero newly independently verified predictive successes** and **zero source-batch promotions into the executable runtime**. There are other ongoing independent astrology survey and backtest projects; these book-documentation counts must not be construed as their completion or success.
- Full parent goal: study traditional primary texts, code reproducible rule sets, run independent historical controls / calibration, then prospective blind birth-time/life-outcome comparisons against meaningful non-astrology baselines. Overall cross-book and empirical completion fraction **not responsibly estimable** from these source counts. Ptolemy 1,066 retained but no all-tradition corpus denominator certified here.

## Immediate priority

Next printed Book III CHAP. C, *Rectification by Accidents, and framing of an Astrological Speculum*, opens original PDF541/printed507. Prioritize source rules and admissions for event-based rectification (the author's preferred high-specificity technique), then natal directions/revolutions/profections/transits, while retaining 1647 date/house/astronomy caveats. Do NOT retrofit the current owner's already-known life events as prospective proof. Human outcome testing must use independently frozen targets, later untouched subjects and strong base-rate comparators.

## Provenance and scoping

894 scan pages: Wikimedia Commons source item corresponding to b30338724; Wellcome Collection's original volume pagination printed pp.25–832 with additional unnumbered preliminaries and leaves. Printed-page calculation deliberately uses 832 as a rough upper bound, not the total exact page count. Percentages are approximate progress in one volume; NOT completion of all historical astrology, horoscope inference, birth-time prediction, or scientific verification.
""")
CURRENT.write_text("# Lilly source frontier — Animodar documented; accidents next\n\n2026-10-17: 34 historical source annotations R5924–R5957 locally admitted. After verified publication **5,957 Lilly + 1,066 retained Ptolemy = 7,023** historic source records. Animodar select new/full-Moon degree and essential-dignity winner, then closest Asc/MC. Lilly expressly rates Animodar and Trutine below life-accident rectification; his worked merchant example compared with previously accident-adjusted chart and does not prove actual birth time. Next CHAP C/editorial CI begins original PDF541, accident-based natal correction. Lilly book physical source frontier **~60%** of 894-page scan, but numeric table transcription and independent human validation remain OPEN. Full progress details: state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md.\n\n---\n\n"+PRIOR.read_text())
rec={"batch":"B04x","status":"GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
 "parent_git_blob_sha1":parentblob,"old_index_sha256":H(OLD),
 "new_index_sha256":H(IDX),"report_sha256":H(LATEST),"progress_report_sha256":H(PROGRESS),
 "current_sha256":H(CURRENT),"rules_sha256":A["rules_sha256"],
 "owner_archive_sha256":Z["archive_sha256"],
 "historical_records_added":34,"lilly_if_published":5957,
 "retained_ptolemy":1066,"combined_if_published":7023,
 "next_editorial_chapter":"CI","next_printed_chapter":"C","next_original_pdf":541,
 "source_volume_position_pct_estimate":60.4,
 "new_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
REC.write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
