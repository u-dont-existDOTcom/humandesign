"""Snapshot the accepted source baseline and bounded original-page source navigation.
No source record is assigned or integrated by this script.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(INDEX.read_text())
assert I["records_count"]==2572 and I["batches"][-1]["id"]=="B02u"
assert I["next"]["chapter"]=="L" and I["next"]["pdf_page"]==381
assert I["next"]["heading"].lower().startswith("of the house of the thiefe")
def save(name,data):(B/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
save("RETAINED_LILLY_INDEX_BEFORE.json",I)
manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
assert len(manifest["images"])==21
r=json.loads((B/"SOURCE_REPLAY_RECEIPT.json").read_text())
assert r["all_source_image_renders_replayed_rgb_identical"] and len(r["images"])==21
windows={"A":[381,385],"B":[385,389],"C":[389,393],"D":[393,397],"E":[397,400]}
for k,rg in windows.items():
 s=json.loads((B/f"SOURCE_READER_INPUT_{k}.json").read_text())
 assert s["source_window"]==rg
 ims=[x for x in s["files"] if x["path"].endswith(".png")]
 assert len(ims)==rg[1]-rg[0]+2
 expected={f"source_images/pdf-{x}.png" for x in range(rg[0],rg[1]+1)}|{"source_images/errata-888.png"}
 assert {x["path"] for x in ims}==expected
save("COUNTS.json",{
 "batch":"B02v","status":"INITIAL_SOURCE_STAGING_ONLY_NO_ACCEPTANCE",
 "lilly_previous_accepted":2572,"retained_ptolemy":1066,
 "combined_previous_accepted":3638,"new_source_units_accepted":0,
 "last_accepted_reference":"R2572","next_provisional":"R2573",
 "source_original_pages":20,"original_errata_pages":1,
 "chapter_l_complete":False,
 "independently_verified_crimes":0,"prospective_predictions":0,
 "clinical_or_legal_validation":False
})
save("SECTION_COVERAGE.json",{
 "batch":"B02v","status":"SOURCE_IMAGE_EVIDENCE_COMPLETE_RULE_EXTRACTION_PENDING",
 "printed_pages":list(range(347,367)), "source_original_pdf_pages":list(range(381,401)),
 "first_page_boundary":"PDF381 after thief-house-and-mark heading; exclude earlier 'Which way the thief is gone'",
 "last_page_boundary":"PDF400 before Chapter LI Battle/Warre divider",
 "five_reader_windows":windows,"overlap_pages":[385,389,393,397],
 "original_image_replay_passed":True,"whole_chapter_L_completeness_depends_on_source_review":True,
 "candidate_section_navigation":"SECTION_NAVIGATION_ONLY.json",
 "original_errata_scope":"printed p360 line4, source original PDF394; glyph body needs collation"
})
print(json.dumps({"source_original_pages":20,"image_replay":True,
 "review_windows":len(windows),"previous_accepted":2572,"new_source_records":0}))
