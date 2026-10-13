"""Prepare B02u image-first source authority and errata witness, no records accepted."""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==2305 and idx["next"]["pdf_page"]==364 and idx["next"]["chapter"]=="L"
scan_hash="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
assert manifest["full_original_1647_sha256"]==scan_hash
assert len(manifest["original_images"])==20
for e in manifest["original_images"]:
    p=B/e["relative_path"]
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==e["sha256"]
with (B/"SOURCE_IDENTITY.json").open("w") as f:
    json.dump({"batch":"B02u","source":"William Lilly Christian Astrology, 1647, original Wellcome b30338724",
       "full_1647_pdf_sha256":scan_hash,"original_pdf_total_pages":894,
       "accepted_baseline":{"lilly":2305,"ptolemy":1066,"combined":3371,"last_record":"R2305"},
       "physical_source_pages":list(range(364,382)),
       "chapter":"Book II, L (incomplete until original PDF400 above Chapter LI)",
       "start":"PDF364/printed330 BELOW 'Of a Thief and Theft' heading",
       "stop":"PDF381/printed347 immediately BEFORE 'Of the house of the Thiefe, and the mark thereof'",
       "next_source_section":"PDF381 'Of the house of the Thiefe' then remainder through PDF400",
       "historical_not_empirical":True,"actual_thieves_or_crimes_verifiably_observed":0,
       "new_records_accepted":0},f,indent=2)
    f.write("\n")
scope={"batch":"B02u","status":"STAGED_SOURCE_IMAGES_NOT_DOCUMENTARY_ACCEPTED",
       "start_pdf":364,"stop_pdf":381,
       "start_boundary":"Printed p330 Of a Thief and Theft heading, below B02t accepted fugitive/woman rules",
       "stop_boundary":"Printed p347 below Which way the Thief is gone, before Of the house of the Thiefe",
       "next": "PDF381 Of the house of the Thiefe; include the physically overlapping image in next phase but not duplicate earlier lines",
       "windows":{"A":[364,369],"B":[369,373],"C":[373,377],"D":[377,381]},
       "window_duplicate_page_policy":"Original PDF369,373,377 included twice for page joins; deduplicate by printed clause anchor, NOT blindly by page identity",
       "whole_chapter_L_complete":False,
       "first_accepted_record_if_review_passes":"R2306",
       "images_count":20,"source_units_accepted":0,"one_hundred_percent_original_text_completion":False}
(B/"SECTION_COVERAGE.json").write_text(json.dumps(scope,indent=2)+"\n")
errata={"batch":"B02u","source_pdf_page":888,"source_image":"evidence/errata-888.png",
 "physical_printed_page_scope": [330,347],
 "original_printed_errata_entries":[
  {"printed_page":330,"line":"6","read":"or","body_context":"last previous B02t fugitive three-day news/return sentence ABOVE new thief heading","admission":"ALREADY_ACCEPTED_B02t_DO_NOT_RECOUNT"},
  {"printed_page":335,"line":"ult.","read":"Planes","body_context":"last line of printed335, original PDF369","body_target_matched":False,"admission":"DRAFT_COLLATION_PENDING"},
  {"printed_page":336,"line":"4","read":"vertue","body_context":"beginning printed336, original PDF370","body_target_matched":False,"admission":"DRAFT_COLLATION_PENDING"},
  {"printed_page":336,"line":"9","read":"vertues","body_context":"printed336, original PDF370","body_target_matched":False,"admission":"DRAFT_COLLATION_PENDING"}
 ],
 "same_volume_original_print_only":True,
 "handwritten_margins_not_assumed_authored":True,
 "never_silently_emend_original_images":True,
 "absence_of_other_entries_not_proof_of_absence_of_print_errors":True}
(B/"ERRATA_COLLATION.json").write_text(json.dumps(errata,indent=2)+"\n")
print(json.dumps({"original_image_hashes":len(manifest["original_images"]),"baseline_lilly":2305,"source_only":True,"errata_draft":3}))
