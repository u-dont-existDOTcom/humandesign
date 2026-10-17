#!/usr/bin/env python3
"""Freeze first-edition source boundary for retrospective accident rectification."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(IDX.read_text())
assert I["records_count"]==5957 and I["batches"][-1]["id"]=="B04x"
assert I["read_numbered_chapters"]==list(range(1,101))
assert I["next"]["chapter"]=="CI" and I["next"]["pdf_page"]==541
assert I["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert I["empirical_validations"]==I["runtime_promotions"]==0
images=[]
for n in range(541,555):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
 "path":p.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
j={"batch":"B04y","status":"ORIGINAL_BOUNDARY_AND_PAGE_IMAGES_VERIFIED_NOT_EXTRACTED",
 "source_sha256":I["source_sha256"],"original_images":images,
 "accepted_parent_batch":"B04x","accepted_parent_lilly":5957,
 "retained_ptolemy":1066,"accepted_parent_combined":7023,
 "next_global_record_number":5958,
 "source_printed_chapter":"C","source_editorial_chapter":"CI",
 "source_chapter_heading":"The Rectification of a Nativity by Accidents, and framing of an Astrologicall Speculum",
 "source_body_page_start":541,"source_body_page_end":553,
 "source_body_ends_before_next_heading":True,
 "following_heading_starts_on_shared_pdf_page":553,
 "following_printed_chapter":"CI","following_editorial_chapter":"CII",
 "following_chapter_heading":"To erect a Scheame of heaven by the Tables of Regiomontanus",
 "following_next_chapter_page":554,
 "source_speculum_table_page":543,
 "source_direction_period_rule":"1 degree per year, 5 arcminutes per month, original PDF553",
 "original_author_prior_event_target_fitting":True,
 "blind_out_of_sample_prediction_not_established":True,
 "all_table_cell_transcription_complete":False,
 "new_documentary_records_accepted":0,"new_empirical_validations":0,
 "runtime_model_promotions":0}
(B/"SOURCE_WINDOW_PROVISIONAL_20261017.json").write_text(json.dumps(j,indent=2)+"\n")
print(json.dumps({"batch":"B04y","status":"BOUNDARY_IMAGES_FROZEN",
 "witness_pages":len(images),"body":[541,553],"next_heading":553,
 "new_records":0}))
