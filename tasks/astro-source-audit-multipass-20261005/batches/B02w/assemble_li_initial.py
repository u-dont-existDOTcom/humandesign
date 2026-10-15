"""Assemble a PROVISIONAL original-1647 Lilly Chapter LI source inventory.

All input descriptions are source-first editorial normalizations, not
diplomatic transcriptions or empirically observed predictions.
The upper text of PDF400 is accepted Chapter L and is excluded from LI.
The Chapter LII heading at PDF403 is navigation only.
"""
from pathlib import Path
from collections import Counter
import hashlib,json

B=Path(__file__).resolve().parent
P=B.parent
def read(name):return json.loads((B/name).read_text(encoding="utf-8"))
def digest(content):return hashlib.sha256(content).hexdigest()
def sha_file(path):return digest(Path(path).read_bytes())

src=read("SOURCE_FIRST_CLAUSES_DRAFT.json")
before=read("RETAINED_LILLY_INDEX_BEFORE_B02w.json")
prior=read("SOURCE_IMAGE_MANIFEST_OPENING_20261015.json")
assert before["records_count"]==2974 and before["batches"][-1]["id"]=="B02v"
assert before["next"]["pdf_page"]==400 and before["next"]["chapter"]=="LI"
assert len(src["rows"])==42
assert [r["record_number"] for r in src["rows"]]==list(range(2975,3017))
assert src["rows"][0]["kind"]=="chapter_li_heading"
assert src["rows"][-1]["kind"]=="chapter_lii_boundary"
assert src["rows"][0]["original_pdf_pages"]==[400] and src["rows"][-1]["original_pdf_pages"]==[403]
assert all(not r["accepted"] and not r["case_evidence_countable"] for r in src["rows"])

# Original identical p400 image in accepted B02v, copied here for portable B02w evidence.
image_baseline={x["original_pdf_page"]:x for x in prior["original_images"]}
page_data=[]
for p in range(400,404):
    f=B/"evidence"/f"pdf-{p}.png"
    assert f.exists(),str(f)
    blob=f.read_bytes()
    image={"original_pdf_page":p,"printed_page":p-34,
        "path":f"evidence/pdf-{p}.png","bytes":len(blob),"sha256":digest(blob),
        "role":("CHAPTER_LI_START_BELOW_CHAPTER_L_DIVIDER" if p==400 else
                "CHAPTER_LII_HEADING_BOUNDARY_ONLY" if p==403 else
                "CHAPTER_LI_BODY")}
    if p==400:
        accepted_prev=P/"B02v"/"evidence/pdf-400.png"
        assert digest(blob)==sha_file(accepted_prev),"B02v boundary image differs"
        image["identical_to_accepted_B02v_pdf400"]=True
    else:
        prev=image_baseline[p]
        assert image["sha256"]==prev["sha256"] and image["bytes"]==prev["bytes"]
    page_data.append(image)

window={
  "batch":"B02w","status":"PROVISIONAL_CHAPTER_LI_SOURCE_WINDOW_BOUNDARY_VERIFIED",
  "original_source":"William Lilly, Christian Astrology (1647), original Wellcome b30338724",
  "original_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
  "original_source_baseline":before["records_count"],
  "opening":{"pdf_page":400,"printed_page":366,"position":"BELOW printed horizontal divider after Chapter L final capture clause"},
  "closing":{"last_chapter_LI_pdf_page":402,"last_chapter_LI_printed_page":368,
             "next_heading_pdf_page":403,"next_heading_printed_page":369,
             "next_heading":"CHAP. LII. Who shall doe best in a suit of Law."},
  "includes_any_chapter_L_above_divider":False,
  "includes_any_chapter_LII_body":False,
  "source_images":page_data,
  "image_count":len(page_data),
  "source_image_originals_preserved":True,
  "independently_reproduced_full_text_transcription":False
}
(B/"SOURCE_WINDOW_MANIFEST.json").write_text(json.dumps(window,ensure_ascii=False,indent=2)+"\n")

byimg={x["original_pdf_page"]:x for x in page_data}
records=[]
for r in src["rows"]:
    pgs=r["original_pdf_pages"]
    assert all(p in byimg for p in pgs)
    role=r["role"]
    if role=="boundary":assert r["record_number"]==3016 and pgs==[403]
    if 403 in pgs:assert role=="boundary"
    rec={
      "id":r["id"],"record_number":r["record_number"],"batch":"B02w",
      "book":"II","chapter":"LI","source_id":"LILLY1647_WELLCOME_B30338724",
      "source_full_pdf_sha256":window["original_full_pdf_sha256"],
      "source_locator":{
        "pdf_pages":pgs,"printed_pages":r["printed_pages"],
        "page_images":[byimg[p]["path"] for p in pgs],
        "original_image_is_authoritative":True,
        "source_statement_is_verbatim":False
      },
      "source_record_kind":r["kind"],"source_record_role":role,
      "source_statement":r["source_statement"],
      "original_source_anchor_editorial_normalization":r["source_anchor_editorial_normalization"],
      "source_statement_type":"EDITORIAL_PARAPHRASE_NOT_DIPLOMATIC_TRANSCRIPTION",
      "preconditions":r["preconditions"],
      "exceptions_and_evidence_limits":r["exceptions_and_uncertainty"],
      "draft_origin_file":"SOURCE_FIRST_CLAUSES_DRAFT.json",
      "draft_origin_local_id":r["local_id"],
      "source_witness_only":True,"case_evidence_countable":False,
      "independently_authenticated_outcome":False,
      "prospective_blinded_prediction":False,
      "clinical_or_criminal_efficacy_verified":False,
      "runtime_status":"REFERENCE_ONLY_NOT_PROMOTED",
    }
    records.append(rec)
assert len({x["source_record_kind"] for x in records})==42
assert [x["record_number"] for x in records]==list(range(2975,3017))
draft={
  "batch":"B02w","status":"SOURCE_FIRST_PROVISIONAL_LI_DRAFT_NOT_ACCEPTED",
  "accepted":False,
  "original_source_pdf_sha256":window["original_full_pdf_sha256"],
  "source_window_manifest_sha256":sha_file(B/"SOURCE_WINDOW_MANIFEST.json"),
  "previous_accepted_lilly":2974,
  "provisional_new_units":42,
  "lilly_if_accepted_not_current":3016,
  "ptolemy_retained":1066,
  "combined_if_accepted_not_current":4082,
  "original_chapter_LI_body_pages":[400,401,402],
  "next_chapter_LII_boundary_page":403,
  "independent_semantic_source_review_complete":False,
  "original_to_record_completeness_proven":False,
  "historical_predictive_accuracy_validated":False,
  "newly_accepted_documentary_records":0,
  "records":records
}
(B/"RULES_DRAFT.json").write_text(json.dumps(draft,ensure_ascii=False,indent=2)+"\n")

pages=[]
for p in range(400,404):
    units=[x for x in records if p in x["source_locator"]["pdf_pages"]]
    pages.append({
       "pdf_page":p,"printed_page":p-34,
       "source_image_sha256":byimg[p]["sha256"],
       "record_ids":[x["record_number"] for x in units],
       "role":byimg[p]["role"]
    })
cross=[{"record_number":r["record_number"],"pdf_pages":r["source_locator"]["pdf_pages"]}
       for r in records if len(r["source_locator"]["pdf_pages"])>1]
assert [x["record_number"] for x in cross]==[2978,2999]
order={
  "batch":"B02w","status":"SOURCE_FIRST_DRAFT_ORDER_NOT_ACCEPTED",
  "record_count":len(records),
  "ranges":{"first":2975,"last":3016},
  "original_printed_range":[366,368],
  "source_pages_including_boundary":[400,401,402,403],
  "pdf400_part_boundary_only_below_chapter_L_divider":True,
  "pdf403_only_next_chapter_heading":True,
  "cross_page_record_ids":[x["record_number"] for x in cross],
  "cross_page_records":cross,"pages":pages,
  "upstream_sha256":{
    "SOURCE_FIRST_CLAUSES_DRAFT.json":sha_file(B/"SOURCE_FIRST_CLAUSES_DRAFT.json"),
    "SOURCE_WINDOW_MANIFEST.json":sha_file(B/"SOURCE_WINDOW_MANIFEST.json"),
    "RULES_DRAFT.json":sha_file(B/"RULES_DRAFT.json")
  },
  "independent_full_fidelity_review":False
}
(B/"SOURCE_ORDER_DRAFT.json").write_text(json.dumps(order,ensure_ascii=False,indent=2)+"\n")

uncertainties=[
  ("LI-U01","First paragraph question/defendant assignment spans original PDF400→401; source direction Moon separation (querent) vs application (defendant) must not be reversed."),
  ("LI-U02","The opening adversary paragraph contains two literal 'e contra' clauses; the later war-outcome passage instead prints 'the contrary noteth the contrary'. All six converse-style units lack fully enumerated inverse conditions."),
  ("LI-U03","The war-voyage safe-return paragraph contains three further literal 'e contra' abbreviations (five literal instances in Chapter LI overall); do not infer a precise inverse algorithm."),
  ("LI-U04","Printed Saturn/Mars/Dragon's Tail injury symbolism is historical and the node glyph/branch grouping should not be promoted to medical causality."),
  ("LI-U05","Printed 'and so of the tenth and seventh' after Sun/eighth war-return warning is elliptical; no complete independent further predicate invented."),
  ("LI-U06","Printed marginal house partitions are original side-label instructions (10,11,12,1,2,3 vs 9,8,7,6,5,4), not an evidence-based war forecast."),
  ("LI-U07","The 'fortune of the Actors' clause has ambiguous referent beyond the immediate seventh-lord-in-first antecedent."),
  ("LI-U08","Compound both-house-lords-in-first with benefics to second cusp has alternatives of victory and reconciliation; preserve conjunctions and distinct outcomes."),
  ("LI-U09","Original wood/stone wound condition starts on PDF401 and ends on PDF402. Physical page seam must remain attached to one clause."),
  ("LI-U10","The included PDF403 Chapter LII heading is a boundary/navigation unit ONLY; it must not be counted as a Chapter LI prediction."),
  ("LI-U11","Source-first 42-unit draft was produced in the same context as original image reading; no blinded independent line-complete collation or empirical tests are established.")
]
issue={
  "batch":"B02w","status":"PROVISIONAL_UNRESOLVED_EDITORIAL_NOT_EMPIRICAL",
  "retained_count":len(uncertainties),
  "issues":[{"id":i,"status":"RETAINED_ORIGINAL_TEXT_AMBIGUITY_OR_METHOD_LIMIT","description":s}
             for i,s in uncertainties],
  "any_retroactive_chart_score_change":False
}
(B/"UNRESOLVED_DRAFT.json").write_text(json.dumps(issue,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({
 "source_window_original_pdfs":[400,401,402],
 "next_chapter_boundary_pdf":403,
 "verbatim_source_images_hashed":len(page_data),
 "draft_records":len(records),
 "first_record":records[0]["record_number"],
 "last_record":records[-1]["record_number"],
 "cross_page_records":cross,
 "uncertainties":len(uncertainties),
 "draft_sha256":sha_file(B/"RULES_DRAFT.json"),
 "accepted":False
},indent=2))
