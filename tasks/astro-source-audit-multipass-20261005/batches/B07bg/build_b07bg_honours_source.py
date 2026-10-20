#!/usr/bin/env python3
"""1647/1659 original Lilly source CLXXXIIII tenth-house Honours and Calling.

The known merchant's social position is retrospective, not a blind human
forecast. Original Roman heading duplicates in later next-source vicinity.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
WEST=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
BASE=TASK/"batches"
START=13193
PARENT_COMMIT="11873f82b7afc3e77c98fee252673080038cf9d0"
SOURCE_1647_ROOT="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
CHINESE_V7_SHA="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def original_photos():
    prev=rd(BASE/"B07bf/ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json")
    out={}
    for folio in (760,761):
        out[str(folio)]={}
        for edition in ("1647","1659"):
            w=prev["four_source_page_first_second_photo_witnesses"][str(folio)][edition]
            fp=ROOT/w["source_photo_path"]
            if not fp.is_file() or sha(fp)!=w["sha256"] or fp.stat().st_size!=w["bytes"]:
                raise ValueError(f"Already accepted original photo {folio} {edition} changed")
            out[str(folio)][edition]={
                "printed_folio":folio,"original_edition":int(edition),
                "scan_page":folio+(34 if edition=="1647" else 29),
                "original_photo_SHA256":w["sha256"],"original_photo_bytes":w["bytes"],
                "source_photo_path":w["source_photo_path"],
                "source_url":w["original_source_url"],
                "reuse_previous_accepted_exact_bytes":True,
                "complete_1659_DjVu_original_binary_verified":False,
            }
    known={
        (762,"1647"):("2d5ff4cfa3bc6448a641e859cd1af7f51affc23cb84a86fcb7204fb06be1e5a0",762436),
        (762,"1659"):("80cdacc16eed3015177538ad25c65560fc7a94c07c41489cc49493162d864040",465115),
        (763,"1647"):("63fafb62cb82c36c34a92361402babf4f0515a8180f2dbc509a2a2fffbd8c991",771028),
        (763,"1659"):("6374f3f964c2ce97b7a28844baa3d25570576711824ff10657f93bf6cee19daa",388559),
    }
    for (folio,edition),(h,size) in known.items():
        fp=B/"evidence"/(f"{edition}-original-folio{folio}-"+
            ("IIIF.jpg" if edition=="1647" else "DjVu.jpg"))
        if not fp.is_file() or sha(fp)!=h or fp.stat().st_size!=size:
            raise ValueError(f"New independent original edition photo {folio} {edition} changed")
        url=(
          f"https://iiif.wellcomecollection.org/image/b30338724_{folio+34:04d}.jp2/full/1800,/0/default.jpg"
          if edition=="1647" else
          "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/"
          "Christian_Astrology_%28Lilly%2C_1659%29.djvu/"
          f"page{folio+29}-1280px-Christian_Astrology_%28Lilly%2C_1659%29.djvu.jpg"
        )
        out.setdefault(str(folio),{})[edition]={
            "printed_folio":folio,"original_edition":int(edition),
            "scan_page":folio+(34 if edition=="1647" else 29),
            "original_photo_SHA256":h,"original_photo_bytes":size,
            "source_photo_path":str(fp.relative_to(ROOT)),"source_url":url,
            "reuse_previous_accepted_exact_bytes":False,
            "complete_1659_DjVu_original_binary_verified":False,
        }
    if set(out)!={"760","761","762","763"}:
        raise ValueError("Four original folio boundaries expected")
    return out

def build():
    index=rd(WEST)
    if (index["records_count"],index["batches"][-1]["id"],
        index["next"]["chapter"],index["next"]["pdf_page"],index["next"]["printed_page"])!=(
        13192,"B07bf","CLXXXIIII",794,760
    ):
        raise ValueError("Accepted CLXXXIII prior source frontier changed")
    if index["source_sha256"]!=SOURCE_1647_ROOT or sha(CHINA)!=CHINESE_V7_SHA:
        raise ValueError("Original 1647 root or Chinese V7 SHA changed")
    clauses=rd(B/"HONOURS_CLAUSE_DRAFT_V1.json")
    photos=original_photos()
    out=[];seen=set()
    for i,row in enumerate(clauses):
        folio=row["folio"];role=row["role"]
        if role in seen or folio not in (760,761,762):
            raise ValueError("Repeated or wrong original chapter note")
        seen.add(role)
        witness=photos[str(folio)]
        out.append({
          "id":f"R{START+i}","record_number":START+i,"batch":"B07bg",
          "original_printed_folio":folio,
          "original_1647_photo_SHA256":witness["1647"]["original_photo_SHA256"],
          "independent_1659_photo_SHA256":witness["1659"]["original_photo_SHA256"],
          "original_1647_PDF_frame":folio+34,
          "independent_1659_DjVu_frame":folio+29,
          "role":role,"historical_evidence_type":row["kind"],
          "source_short_original_1647_verbatim_fragment_NOT_diplomatic_full_glyphs":row["anchor"],
          "research_gloss_separate_from_original_quote":row["gloss"],
          "candidate_future_observable_type_NOT_frozen":row["target"],
          "merchant_already_known_to_author":True,
          "historical_original_actual_career_verified":False,
          "historical_original_cazimi_astronomy_verified":False,
          "independent_human_blind_forecast_tested":False,
          "runtime_astrological_rule_promoted":False
        })
    if out[0]["role"]!="HONOURS_CLXXXIIII_SOURCE_BOUNDARY" or out[-1]["role"]!="NEXT_FRIENDS_CLXXXIII_PRINTED_HEADING":
        raise ValueError("Original honours source boundary not complete")
    if len(out)<35 or not all(x["original_printed_folio"]<=out[-1]["original_printed_folio"] for x in out):
        raise ValueError("Too little or out-of-bound original source evidence")
    source={
      "schema":"ORIGINAL_LILLY_1647_1659_CLXXXIIII_HONOURS_CALLING_SOURCE_V1",
      "status":"PROVISIONAL_NOT_YET_GUARDED_ACCEPTED",
      "parent_accepted_Lilly_original_commit":PARENT_COMMIT,
      "first_Wellcome_original_1647_full_PDF_root_SHA256":SOURCE_1647_ROOT,
      "second_1659_entire_DjVu_source_SHA_not_verified":True,
      "source_original_printed_Roman_literal_honours":"CLXXXIIII",
      "honours_editorial_numerical_ordinal":184,
      "source_honours_original_folios":[760,761,762],
      "distinct_next_friends_original_start_folio":762,
      "next_chapter_printed_literally_CLXXXIII_reused_from_Travels":True,
      "next_chapter_original_headed_section":"Of Friends",
      "source_folio_763_next_chapter_only_photo_extra":True,
      "source_photo_witnesses":photos,
      "author_known_merchant":True,
      "preknown_merchant_actual_job_reputation_verified":False,
      "venus_cazimi_repeated_as_professional_honours_premise":True,
      "previous_original_marriage_cazimi_premise_same_natal_data_not_independent_repeat_evidence":True,
      "original_1647_Sun_Venus_17arcminute_source_and_modern_75arcminute_disagreement_not_resolved":True,
      "no_occupational_honor_income_fame_outcome_verified":True,
      "new_historical_source_only_records":len(out),
      "first_R":out[0]["id"],"last_R":out[-1]["id"],
      "next_R":f"R{START+len(out)}",
      "next_original_printed_folio":762,
      "next_original_1647_pdf_frame":796,
      "next_original_chapter_source_label":"CLXXXIII of Friends (original repeats Travels Roman numeral)",
      "next_editorial_source_sequence_ordinal":185,
      "independent_real_human_predictive_validations":0,
      "runtime_astrological_promotions":0,
      "records":out
    }
    wr(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json",source)
    wr(B/"RULES.json",{
      "batch":"B07bg","source_only_not_career_truth":True,
      "record_count":len(out),"first_R":out[0]["id"],"last_R":out[-1]["id"],
      "actual_person_profession_or_occupational_status_verified":False,
      "genuine_human_blind_predictive_tests":0,
      "runtime_promotions":0,"rules":out
    })
    wr(B/"ACCEPTANCE.json",{
      "batch":"B07bg","Lilly_before":13192,"Ptolemy_retained":1066,
      "Chinese_V7_SHA256_unchanged":CHINESE_V7_SHA,
      "new_historical_source_only_annotations":len(out),
      "Lilly_after_if_accepted":13192+len(out),
      "Western_after_if_accepted":13192+len(out)+1066,
      "first_R":out[0]["id"],"last_R":out[-1]["id"],
      "next_R":f"R{START+len(out)}",
      "next_printed_chapter":"CLXXXIII","next_editorial_ordinal":185,
      "next_original_folio":762,"next_original_first_1647_pdf_frame":796,
      "source_folios":[760,761,762],
      "source_honours_1647_print_label":"CLXXXIIII",
      "original_next_friends_repeats_Travels_numeral_CLXXXIII":True,
      "eight_original_photos_verified":True,
      "actual_real_profession_honours_verified":False,
      "source_original_cazimi_repeated_not_additional_independent_evidence":True,
      "human_blind_predictions_validated":0,"runtime_astrological_promotions":0,
      "source_SHA256":sha(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json"),
      "rules_SHA256":sha(B/"RULES.json")
    })
    print("B07bg source DRAFT",len(out),out[0]["id"],out[-1]["id"],
          "next",f"R{START+len(out)}","Lilly if accepted",13192+len(out))

if __name__=="__main__":build()
