#!/usr/bin/env python3
"""Provisional original source window for printed XCV, editorial XCVI."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert I["records_count"]==5510 and I["batches"][-1]["id"]=="B04o"
assert I["next"]["chapter"]=="XCVI" and I["next"]["pdf_page"]==504
assert I["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (504,505):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
m={"batch":"B04p","status":"PROVISIONAL_SOURCE_WINDOW_ONLY_NO_RECORDS_ADMITTED",
 "original_full_pdf_sha256":I["source_sha256"],
 "original_images":images,"parent_accepted_batch":"B04o",
 "parent_accepted_lilly":5510,"ptolemy_retained":1066,"combined_parent_total":6576,
 "next_global_record_number":5511,"chapter_editorial":"XCVI",
 "chapter_printed":"XCV","original_body_pdf_pages":[504,505],
 "printed_body_pages":[470,471],"following_heading_pdf":505,"following_heading_printed":"XCVI",
 "following_heading_editorial":"XCVII",
 "question_date_printed":"6 June 1647","question_clock_printed":"8 PM",
 "next_question_printed_date":"October 19, mid-1640s; original year glyph requires closer confirmation",
 "next_question_printed_clock":"7:20 PM",
 "source_end":"Original PDF505 above horizontal divider for new Lady/husband case",
 "source_forecast_direction":"Eastwards","source_forecast_hide":"About one night",
 "source_forecast_apprehension_window":"Six or seven days (as the source recounts)",
 "author_reported_direction_confirmation":True,
 "author_reported_news_friday":True,
 "author_reported_recapture_sunday":True,
 "next_chapter_has_distinct_horary_figure":True,
 "independent_actual_arrest_records_authenticated":0,
 "original_diplomatic_second_transcription_complete":False,
 "new_accepted_documentary_records":0,"new_empirical_validations":0,
 "runtime_promotions":0}
(B/"SOURCE_WINDOW_PROVISIONAL_20261017.json").write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"batch":"B04p","witness_pages":[504,505],
 "original_first_edition_hashes":[z["sha256"] for z in images],
 "accepted_documentary_added":0,"next_heading":"Printed XCVI / editorial XCVII"}))
