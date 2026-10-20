#!/usr/bin/env python3
"""Original 1647 and independent 1659 Lilly CLXXXII Children source, ONE page.

First printed folio757 after end of CLXXXI Marriage, before distinct
CLXXXIII Travels heading at start of folio758. Preserves contradictory
barren/fruitful, number/sex/mortality statements as period hypotheses only.
No modern medicine, pregnancy advice or validated person outcomes.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
WEST=T/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PARENT=T/"batches/B07bd"
SOURCE_FULL_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
CHINESE_SHA="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"
START=13102

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sh(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def photo_proof():
    prev=rd(PARENT/"ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json")
    out={}
    for ed in ("1647","1659"):
        record=prev["folios"]["757"][ed]
        photo=ROOT/record["path"]
        if (record["physical_printed_folio"]!=757
                or record["source_scan_frame"]!=757+(34 if ed=="1647" else 29)
                or not photo.is_file() or photo.stat().st_size!=record["bytes"]
                or sh(photo)!=record["sha256"]):
            raise ValueError(f"Prior immutable original Children open folio757 {ed} source drift")
        out.setdefault("757",{})[ed]={
            "source_edition":int(ed),"printed_folio":757,
            "source_frame":record["source_scan_frame"],
            "source_photo_path":record["path"],
            "source_photo_url":record["exact_source_url"],
            "photo_SHA256":record["sha256"],"photo_bytes":record["bytes"],
            "reused_exact_accepted_parent":True,
            "old_whole_edition_DjVu_verified":False,
        }
    first=PARENT/"next_children_1647_photo_prefetch/1647-original-folio758-iiif.jpg"
    second=B/"evidence/1659-original-folio758-next-travel-thumbnail.jpg"
    witness={
        "1647":("aaed642fce12ca6fffaed28aef50d1b2d28c60af3fec32d9af65ab538da44846",758192,first,
                "https://iiif.wellcomecollection.org/image/b30338724_0792.jp2/full/1800,/0/default.jpg"),
        "1659":("c2ac068cb38b04b2a38b394fc6bc005ac35bb4c4b8b0757dbaae9375703a02f4",524445,second,
                "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Christian_Astrology_%28Lilly%2C_1659%29.djvu/page787-1280px-Christian_Astrology_%28Lilly%2C_1659%29.djvu.jpg"),
    }
    for ed,(digest,size,photo,url) in witness.items():
        if not photo.is_file() or sh(photo)!=digest or photo.stat().st_size!=size:
            raise ValueError(f"Next independent original Travel folio758 {ed} source drift")
        out.setdefault("758",{})[ed]={
            "source_edition":int(ed),"printed_folio":758,
            "source_frame":758+(34 if ed=="1647" else 29),
            "source_photo_path":str(photo.relative_to(ROOT)),
            "source_photo_url":url,
            "photo_SHA256":digest,"photo_bytes":size,
            "reused_exact_accepted_parent":ed=="1647",
            "old_whole_edition_DjVu_verified":False,
        }
    return out

# (folio, short role, source evidence class, short printed 1647 witness,
#  distinct working historical gloss, future blind-target candidate)
CLAUSES=[
(757,"CHILDREN_FIFTH_HOUSE_HEADING","SOURCE_CHAPTER_BOUNDARY","Of Children.","Distinct CLXXXII fifth-house original after Marriage separator on printed757, not a continuation of marriage.","navigation"),
(757,"MERCURY_EXCLUDED_FIRST","EXPLICIT_SOURCE_DISCOUNT","totally excluded from judgment","Mercury is initially discounted as a children significator.","mechanical_countertestimony"),
(757,"MOON_TWO_DEGREES_FIFTH_CUSP","SOURCE_ASTRO_GEOMETRY","within two degrees of the cusp","Moon's proximity within two degrees of fifth cusp is used for fertility testimony.","mechanical_predicate"),
(757,"GEMINI_FIFTH_DESCENDING","SOURCE_ASTRO_GEOMETRY","a barren Sign, descends.","Fifth cusp Gemini classified barren in historical astrological sign taxonomy.","mechanical_predicate"),
(757,"MERCURY_COMBUST_NO_ISSUE","UNVERIFIED_REPRODUCTIVE_COUNTERTESTIMONY","an argument of no issue","Fifth lord Mercury combustion initially suggests no children, not a clinical infertility test.","negative_reproductive_countertestimony"),
(757,"GEMINI_BARREN_REPEATED","SOURCE_ASTRO_REITERATION","a testimony of barrennesse.","Gemini's historical barren label is cited a second time as adverse testimony.","negative_reproductive_countertestimony"),
(757,"SAGITTARIUS_ELEVENTH","SOURCE_ASTRO_GEOMETRY","ascending in the eleventh","Sagittarius at the eleventh house is introduced as an additional potential testimony.","mechanical_predicate"),
(757,"JUPITER_TWELFTH_IMPEDED","SOURCE_ASTRO_NEGATIVE","impedited from assistance","Jupiter in the twelfth is considered obstructed from aiding fifth-house matters.","negative_reproductive_countertestimony"),
(757,"MOON_FIFTH_POSITIVE","SOURCE_ASTRO_POSITIVE","The presence of the Moon","The Moon's fifth-house proximity is used to overcome the earlier negative arguments.","mechanical_predicate"),
(757,"MOON_MARS_SEXTILE_POSITIVE","SOURCE_ASTRO_GEOMETRY","benevolent aspect to Mars","Moon sextile Mars cited as positive for children, later partly used to diminish an initial numerical tally.","mechanical_predicate"),
(757,"MOON_MERCURY_SUN_VENUS_POSITIVE","SOURCE_ASTRO_GEOMETRY","to Mercury, Sun and Venus","Moon's friendly aspects to Mercury Sun and Venus help overcome barrenness countertestimonies.","mechanical_predicate"),
(757,"FRIENDLY_RAYS_FIFTH_CUSP","SOURCE_ASTRO_GEOMETRY","friendly radiation to the cusp","General benefic rays to fifth cusp claimed to support children.","mechanical_predicate"),
(757,"YES_CHILDREN_FORECAST","HISTORICAL_UNVERIFIED_CHILDREN_FORECAST","he shall have Issue","Despite barren-sign/combustion conditions, Lilly positively predicts eventual children.","binary_birth"),
(757,"EXPLICIT_CHILD_COUNT_PROCEDURE","HISTORICAL_SYMBOLIC_COUNT_RULE","number is derived from the Signe","Proposed count from fifth sign, Moon therein, and friendly aspecting planets.","mechanical_rule"),
(757,"BICORPOREAL_SIGN_COUNTS_TWO","HISTORICAL_SYMBOLIC_INTEGER_TALLY","A Bycorporeall Signe giveth","Historic fifth-sign contribution stated as 2.","numeric_contribution"),
(757,"MOON_CONTRIBUTES_ONE","HISTORICAL_SYMBOLIC_INTEGER_TALLY","The Moon cannot but adde","Historic Moon contribution 1 to the child-count reasoning.","numeric_contribution"),
(757,"FOUR_PLANETS_ASPECTS_COUNT_FOUR","HISTORICAL_SYMBOLIC_INTEGER_TALLY","In aspect with four Planets","Four beneficially aspecting bodies considered a numeric count ingredient, not necessarily arithmetic addend.","numeric_contribution"),
(757,"PROBABILITY_OF_FOUR_CHILDREN","HISTORICAL_UNVERIFIED_TENTATIVE_COUNT","a probability of four.","Explicitly tentative text suggests four children at this interim stage; not an independent actual birth count.","tentative_integer"),
(757,"MERCURY_COMBUSTION_KILLS_ONE","HISTORICAL_UNVERIFIED_INFANT_MORTALITY_CLAIM","Combustion of Mercury killeth one","Old astrological claim that Mercury combustion might prevent survival of one child; not biomedical evidence.","negative_life_event"),
(757,"MOON_MARS_SEXTILE_KILLS_ANOTHER","HISTORICAL_UNVERIFIED_INFANT_MORTALITY_CLAIM","to Mars another","A later claim counts a Moon–Mars sextile as removing another potential child; notably reuses earlier benefic testimony in adverse manner.","negative_life_event"),
(757,"SEX_ASSIGNMENT_SYMBOLIC_RULE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","Sex or kinds being required","An obsolete astrological method speculates offspring sex based on gendered classical sign assignments.","sex_prediction"),
(757,"MARS_MALE_SIGN_MALE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","Mars in a masculine Signe","Mars in historical masculine sign used to infer a male child.","sex_prediction"),
(757,"SUN_MALE_SIGN_MALE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","Sun in a masculine Signe","Sun in masculine sign used to infer male child.","sex_prediction"),
(757,"MOON_GEMINI_MARS_MALE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","Moon in Gemini","Moon in Gemini near aspect to Mars used as extra male testimony.","sex_prediction"),
(757,"MERCURY_POWER_TO_SUN_MALE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","power being given to Sun","Mercury's dispositor Sun used in a further speculative male count.","sex_prediction"),
(757,"VENUS_MOON_FEMININE_TWO_OR_THREE","HISTORICAL_UNVERIFIED_SEX_CATEGORIZATION","two Females, if not three","Two or possibly three female children are proposed, not a unique count.","tentative_integer"),
(757,"FEMALES_MAY_LIVE_MALES_NOT_ALL","HISTORICAL_UNVERIFIED_CHILD_MORTALITY","may live, but not all the Males","Conjectures females may survive and some male offspring may not; unverified life-and-death forecast.","negative_life_event"),
(757,"SIBLING_AGREEMENT_BENIGN_ASPECT","HISTORICAL_UNVERIFIED_SIBLING_RELATIONSHIP","concordancy amongst them","Forecast harmony among children from benign aspects, not a verified family observation.","relationship"),
(757,"VENUS_CHILD_PREFERMENT","HISTORICAL_UNVERIFIED_CHILD_STATUS","great preferment.","Forecast at least one child associated with Venus could advance in station, not observed career.","status"),
(758,"TRAVELS_CLXXXIII_NEXT_BOUNDARY","SOURCE_NEXT_CHAPTER_BOUNDARY","Of Travels.","Separate physically headed CLXXXIII of Travels begins first lines printed758; neither its factual travel example nor prophecy belongs to Children records.","navigation")
]

def build():
    index=rd(WEST)
    china=rd(CHINA)
    if (index["records_count"],index["batches"][-1]["id"],
        index["next"]["chapter"],index["next"]["pdf_page"])!=(13101,"B07bd","CLXXXII",791):
        raise ValueError("Exact latest accepted CLXXXI Lilly source frontier not present")
    if index["source_sha256"]!=SOURCE_FULL_SHA or sh(CHINA)!=CHINESE_SHA:
        raise ValueError("Original 1647 source root or independent Chinese V7 source changed")
    photos=photo_proof()
    rs=[]
    roles=set()
    for i,(folio,role,source_type,anchor,gloss,target) in enumerate(CLAUSES):
        if role in roles or (folio not in (757,758)):
            raise ValueError("Duplicate/off-boundary historical source annotation")
        roles.add(role)
        w=photos[str(folio)]
        rs.append({
            "id":f"R{START+i}",
            "record_number":START+i,
            "batch":"B07be",
            "original_printed_folio":folio,
            "original_1647_source_pdf_frame":folio+34,
            "separately_typeset_1659_source_DjVu_frame":folio+29,
            "original_1647_page_source_photo_sha256":w["1647"]["photo_SHA256"],
            "original_1659_page_source_photo_sha256":w["1659"]["photo_SHA256"],
            "role":role,"source_evidential_role":source_type,
            "original_1647_short_anchor_NOT_full_diplomatic_transcription":anchor,
            "historical_interpretation_NOT_original_verbatim":gloss,
            "candidate_future_blind_target_type_NOT_frozen":target,
            "historical_statement_about_known_merchant_only":True,
            "actual_child_counts_or_sexes_independently_confirmed":False,
            "original_sex_gender_and_mortality_theories_medically_true":False,
            "independently_validated_real_person_future_outcome":False,
            "allowed_for_medicine_parenting_reproductive_advice":False,
            "runtime_astrological_rule_promoted":False,
        })
    if (rs[0]["id"],rs[-1]["role"],len(rs)) != (
        "R13102","TRAVELS_CLXXXIII_NEXT_BOUNDARY",30
    ):
        raise ValueError("Original one-folio Children source frontier changed")
    source={
        "schema":"B07be_ORIGINAL_LILLY_1647_1659_CLXXXII_CHILDREN_DOCUMENTARY_SOURCE_V1",
        "status":"PENDING_GUARDED_CANONICAL_INDEX",
        "parent_source_original_accepted_branch_commit":"df9f700e0171a09da2e31b3793692a3d32339734",
        "original_Wellcome_1647_entire_original_pdf_sha256":SOURCE_FULL_SHA,
        "separate_1659_entire_DjVu_binary_sha256_not_verified":True,
        "source_first_and_second_print_folio_757_children":True,
        "next_first_and_second_print_folio_758_CLXXXIII_travels":True,
        "reused_immutable_parent_original_p757_photos":True,
        "original_printed_folios_read":[757,758],
        "original_1647_PDF_frames":[791,792],
        "separately_original_1659_DjVu_frames":[786,787],
        "source_photo_witnesses":photos,
        "source_no_children_countertestimonies_explicit":True,
        "source_positive_children_prediction_explicit":True,
        "source_conditional_tentative_four_children_not_actual_proven_count":True,
        "source_male_female_and_death_claims_historical_only":True,
        "source_first_suggests_no_issue_then_overrides_with_yes_children":True,
        "author_already_knows_the_native":True,
        "independently_verified_merchant_actual_children_count":False,
        "historical_reproductive_anatomy_medical_truth_verified":False,
        "historical_exact_astrological_glyphs_expert_collation_complete":False,
        "new_source_documentary_annotations":len(rs),
        "first_R":rs[0]["id"],
        "last_R":rs[-1]["id"],
        "next_R":f"R{START+len(rs)}",
        "next_chapter":"CLXXXIII Of Travels",
        "next_source_pdf":792,
        "next_source_printed_folio":758,
        "genuine_actual_person_predictive_accuracy_validated":0,
        "runtime_astrological_promotions":0,
        "records":rs,
    }
    wr(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json",source)
    wr(B/"RULES.json",{
        "batch":"B07be","source_historical_only":True,
        "record_count":len(rs),"first_R":rs[0]["id"],"last_R":rs[-1]["id"],
        "actual_merchant_children_observed_and_verified":False,
        "genuine_predictive_human_validations":0,
        "runtime_astrological_promotions":0,"rules":rs
    })
    wr(B/"ACCEPTANCE.json",{
        "batch":"B07be","Lilly_before":13101,"Ptolemy_retained":1066,
        "Chinese_V7_sha256_unchanged":CHINESE_SHA,
        "new_source_only_documentary_records":len(rs),
        "Lilly_after_if_accepted":13101+len(rs),
        "Western_after_if_accepted":13101+len(rs)+1066,
        "first_R":rs[0]["id"],"last_R":rs[-1]["id"],
        "next_R":f"R{START+len(rs)}",
        "next_chapter":"CLXXXIII","next_pdf":792,"next_folio":758,
        "original_source_page_count":2,
        "original_children_section_exactly_one_folio":True,
        "independent_actual_child_count_sex_or_mortality_confirmations":0,
        "genuine_human_prospective_blind_predictions":0,
        "runtime_astrological_promotions":0,
        "source_sha256":sh(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json"),
        "rules_sha256":sh(B/"RULES.json")
    })
    print("B07be provisional originals",len(rs),"records",rs[0]["id"],rs[-1]["id"],"next",f"R{START+len(rs)}")
if __name__=="__main__":
    build()
