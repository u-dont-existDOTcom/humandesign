#!/usr/bin/env python3
"""Document original printed 1647 and independent typeset 1659 Marriage chapter.

Source-only historic assertions/interpretive rules, NOT predictive success.
Original four folios: first printed754 part, 755-756 full, 757 top before
physical divider to CLXXXII Children. Next source record R13045, no repeats.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
WESTERN = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE_V7 = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PARENT = TASK / "batches/B07bc"
PARENT_SHA = "6047f72d89e6b0a3b9198c244a8538c6abb1a076"
ORIGINAL_FULL_1647_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
CHINESE_V7_SHA = "bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"
START_R=13045

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()

def write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def photo_witnesses() -> dict[str, dict[str, object]]:
    """Allow exact reuse of accepted folio754 images; no repeated downloads."""
    parent=read(PARENT / "ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json")
    source=parent["original_photographic_witnesses"]["754"]
    original={}
    initial={}
    for ed in ("1647","1659"):
        obj=source[ed]
        filename=ROOT / obj["original_source_repo_relative_file"]
        if (not filename.is_file() or file_sha(filename)!=obj["sha256"]
                or filename.stat().st_size!=obj["bytes"]):
            raise ValueError(f"Previously accepted source folio754 changed: {ed}")
        initial[ed]={
            "repository_source_path":str(filename.relative_to(ROOT)),
            "source_edition":int(ed),
            "original_printed_folio":754,
            "scan_page_identifier":obj["scan_frame"],
            "photo_sha256":obj["sha256"],
            "photo_byte_length":obj["bytes"],
            "source_provenance":"accepted original source from B07bb/B07bc",
            "full_original_1659_DjVu_binary_sha_checked":False,
        }
    original["754"]=initial
    manifest=read(B/"ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json")
    for folio in (755,756,757):
        pair=manifest["folios"][str(folio)]
        if set(pair)!={"1647","1659"}:
            raise ValueError(f"Both independently printed folio {folio} witnesses required")
        original[str(folio)]={}
        for ed in ("1647","1659"):
            data=pair[ed]
            path=ROOT/data["path"]
            if not path.is_file() or file_sha(path)!=data["sha256"] or path.stat().st_size!=data["bytes"]:
                raise ValueError(f"Folio {folio} source photo {ed} SHA drift")
            if data["physical_printed_folio"]!=folio or data["source_scan_frame"]!=folio+(34 if ed=="1647" else 29):
                raise ValueError(f"Original {folio} scan sequence / printed label drift")
            original[str(folio)][ed]={
                "repository_source_path":str(path.relative_to(ROOT)),
                "source_edition":int(ed),
                "original_printed_folio":folio,
                "scan_page_identifier":data["source_scan_frame"],
                "photo_sha256":data["sha256"],
                "photo_byte_length":data["bytes"],
                "original_photo_url":data["exact_source_url"],
                "source_provenance":data["original_printing"],
                "full_original_1659_DjVu_binary_sha_checked":False,
            }
    return original

# (folio, source meaning identifier, historical layer, brief exact printed
# 1647 anchor, working inference only, potential measurable target).
# Short anchors are NOT a complete transcription or independent proof of
# the already-known merchant's real marital life.
SOURCE_CLAUSES = [
(754,"CHAP_CLXXXI_MARRIAGE_BOUNDARY","PHYSICAL_CHAPTER_BOUNDARY","Of Marriage.","Following separate physical 7th-house chapter opening below old CLXXX servant-case divider.","navigation"),
(754,"FIRST_ASK_IF_HE_WILL_MARRY","QUESTION_FRAMING","Whether the Native shall Marry","Chapter poses whether this already-known merchant will marry at all.","binary"),
(754,"CANCER_SEVENTH_FRUITFUL","SYMBOLIC_SOURCE_RULE","the Signe descending in the seventh","Cancer is read as a fruitful seventh-house sign supporting occurrence of marriage.","mechanical_predicate"),
(754,"MOON_FIFTH_PLEASURE","SYMBOLIC_SOURCE_RULE","is in the fift","The Moon is treated as fifth-house pleasure significator.","mechanical_predicate"),
(754,"MOON_SEXTILE_MARS_SEVENTH","SYMBOLIC_SOURCE_RULE","in the seventh","The source links a Moon aspect to Mars positioned in the seventh.","mechanical_predicate"),
(754,"SATURN_ASC_NOT_AFFLICT_MOON_VENUS","SYMBOLIC_SOURCE_RULE","neither afflict the","Saturn as ascendant lord is said not to afflict the Moon or Venus.","mechanical_predicate"),
(754,"MOON_TRINE_MERCURY_SUN_VENUS","SYMBOLIC_SOURCE_RULE","applies by","The Moon's application to Mercury/Sun/Venus is used in an affirmative marriage argument; glyphs remain historically source-specific.","mechanical_predicate"),
(754,"SUN_VENUS_SIGN_SQUARE_EQUATOR_TRINE","HISTORICAL_ASTRO_GEOMETRY","equivalent to a","The text equates a sign-based seventh-cusp square in signs of long ascension with a trine in the equator; not independently calculated here.","mechanical_predicate"),
(754,"VENUS_ALMUTEN_OWN_HOUSE","SYMBOLIC_SOURCE_RULE","Almuten of the Geniture","Venus is called almuten of geniture and in her own house, contributing to an affirmative reading.","mechanical_predicate"),
(754,"AFFIRMATIVE_MARRIAGE_CONCLUSION","HISTORICAL_UNVERIFIED_LIFE_FORECAST","I hold the Native shall marry","Original text explicitly predicts marriage; no independent merchant life-record verification.","binary"),
(754,"MARITAL_OBSTACLES_SMALL","HISTORICAL_UNVERIFIED_LIFE_FORECAST","no cause to judge the Native shall be impedited","Lilly expects no substantial obstacles in obtaining a wife, before specifying limited family resistance.","social_obstacle"),
(754,"LOVE_VERSUS_RELATIVES_DISTINCTION","QUALIFIED_SOCIAL_INFERENCE","in obtaining the love of the Woman","Source separates woman's feelings from possible family opposition; not a claim she personally resisted.","social_obstacle"),
(754,"WOMANS_FATHER_FRIENDS_HINDER","HISTORICAL_UNVERIFIED_LIFE_FORECAST","small hinderance by the Father","Predicts minor obstacles from the woman's father or her friends.","social_obstacle"),
(755,"FATHER_TENTH_DERIVED_FOURTH","DERIVED_HOUSE_RULE","Lord of the tenth","Mars as tenth-house lord, fourth derived from partner seventh, is used as wife's father significator.","mechanical_predicate"),
(755,"CHURCHMAN_BROTHER_IN_LAW","HISTORICAL_UNVERIFIED_LIFE_FORECAST","Church-man or Brother in law","Speculates a clergyman or brother-in-law may create some difficulties.","social_obstacle"),
(755,"SPOUSE_SISTER_HUSBAND_DERIVATION","DERIVED_HOUSE_RULE","Husband of one of the Wives Sisters","The old derivative-house interpretation alternatively identifies the wife's sister's husband.","mechanical_predicate"),
(755,"YOUTH_VS_AGE_SECTION","SUBSECTION_HEADER","Whether in age or youth.","New subsection on age/timing of marriage.","navigation"),
(755,"MOON_OCCIDENTAL_SUN","SYMBOLIC_SOURCE_RULE","Occidentall of the","Moon occidental to Sun is invoked as a later-marriage condition.","mechanical_predicate"),
(755,"VENUS_EIGHTH_DESCENDING","SYMBOLIC_SOURCE_RULE","descending from the Meridian angle","Venus is described as descending from meridian and in the eighth house.","mechanical_predicate"),
(755,"MARRIAGE_NOT_IN_YOUTH","HISTORICAL_UNVERIFIED_AGE_FORECAST","cannot be celebrated in youth","Forecast marriage not in youth.","age_threshold"),
(755,"MARRIAGE_AFTER_SATURN_RETURN_29","HISTORICAL_UNVERIFIED_AGE_FORECAST","after his twenty ninth yeer of age","Forecast marriage after Saturn has revolved and after age 29, not a demonstrated actual timing.","age_threshold"),
(755,"EXACT_MARRIAGE_YEAR_REQUIRES_DIRECTIONS","EXPLICIT_SOURCE_UNCERTAINTY","particular yeer is known onely by Direction","Text does not provide a specific marriage year, explicitly defers its selection to directions.","temporal_nonprediction"),
(755,"HOW_MANY_SECTION","SUBSECTION_HEADER","How many.","Marriage-number subsection heading.","navigation"),
(755,"MOON_GEMINI_MARS_LEO_MERCURY_COMBUST_ONE","CONTRARY_SYMBOLIC_SOURCE_RULE","doe promise but one","Earlier lunar/mars positions and Mercury combustion are said to imply only one marriage.","mechanical_countertestimony"),
(755,"VENUS_LIBRA_CAZIMI","SYMBOLIC_SOURCE_RULE_CRITICAL","and in Caximi","Original Venus in Libra and Cazimi counters one-marriage premise; exact modern ephemeris parity remains unverified.","mechanical_predicate"),
(755,"MOON_PARTILE_SEXTILE_MARS","SYMBOLIC_SOURCE_RULE","her partill","Moon's near-exact sextile with Mars is invoked to support multiplicity.","mechanical_predicate"),
(755,"MOON_REFLECTION_MERCURY_VENUS","SYMBOLIC_SOURCE_RULE","then to","The Moon's subsequent aspect to Mercury and Venus is invoked as additional evidence; exact glyph transcription remains qualified.","mechanical_predicate"),
(755,"SUN_EXCLUDED_FROM_COUNT","NEGATIVE_SOURCE_RULE","hath no signification herein","The Sun is explicitly excluded as a count significator despite earlier involvement.","mechanical_countertestimony"),
(755,"EXACT_TWO_MARRIAGES_FORECAST","HISTORICAL_UNVERIFIED_INTEGER_FORECAST","marry two times onely","Specific original forecast of exactly two marriages; merchant outcomes unverified.","integer"),
(755,"EXACT_TWO_EXTRA_SWEETHEARTS","HISTORICAL_UNVERIFIED_INTEGER_FORECAST","two Sweet-hearts","Separate forecast of two romances outside his wives; not independently verified.","integer"),
(755,"FIRST_WIFE_MOON_MARS_LEO","SYMBOLIC_SOURCE_RULE","description of the first Wife","First wife's expected characteristics are attributed to Moon/Mars/Leo.","mechanical_predicate"),
(755,"FIRST_WIFE_BODY","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","a lean Body erect","Forecast average or shorter stature, lean body, strong joints and broad shoulders.","physical"),
(755,"FIRST_WIFE_HAIR_COMPLEXION","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","bright flaxen","Forecast pale complexion and light flaxen hair.","physical"),
(755,"FIRST_WIFE_FACE_SCARS","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","some Scarre, blemish","Speculates marks, scars or pockholes in first wife's face; not a verified observation.","physical"),
(755,"FIRST_WIFE_MARTIAL_TEMPER","HISTORICAL_UNVERIFIED_SPOUSE_PERSONALITY","violent, furious, of great spirit","Forecast strong spirit, command-oriented and frugal personality; historically value-laden.","personality"),
(755,"MARS_EXALTED_ASC_SATURN_RELIEF","SYMBOLIC_SOURCE_RULE","exalted in the ascendant","Mars dignified in the ascendant and Saturn superiority are invoked to mitigate trouble.","mechanical_predicate"),
(756,"FIRST_WIFE_DISAGREEMENTS_SHORT","HISTORICAL_UNVERIFIED_RELATIONSHIP_OUTCOME","not any feare of their disagreement to be of long continuance","Foresees quarrels but not lasting disagreements with first wife.","relationship"),
(756,"SECOND_WIFE_VENUS","SYMBOLIC_SOURCE_RULE","The second Wife is signified by","Venus is used to signify the second wife.","mechanical_predicate"),
(756,"SECOND_WIFE_HEIGHT_BUILD","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","of middle stature, but inclining to talnesse","Second wife forecast medium to tall, slender build and rounded face.","physical"),
(756,"SECOND_WIFE_HAIR_EYES","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","a black lovely eye","Forecast ruddy complexion, dark eye and beauty; not verified facts.","physical"),
(756,"SECOND_WIFE_RELIGION_ROLE","HISTORICAL_UNVERIFIED_SPOUSE_PERSONALITY","modest, religious","Speculates a modest, religious, independent-minded householder with good disposition.","personality"),
(756,"SECOND_WIFE_LEFT_FOREHEAD_MOLE","HISTORICAL_UNVERIFIED_SPOUSE_APPEARANCE","little mole on her Forehead","Highly specific forecast: a mole on forehead near left eye.","physical"),
(756,"SECOND_WIFE_PREVIOUS_NEGOTIATION","HISTORICAL_UNVERIFIED_RELATIONSHIP_HISTORY","perhaps she was in some treaty","Uncertain conjecture of earlier relationship negotiations with a gentleman.","relationship"),
(756,"WIVES_WEALTH_SECTION","SUBSECTION_HEADER","Wealth of Wives.","New subsection on spouses' estates and complications.","navigation"),
(756,"COR_LEONIS_MARS_EIGHTH","SYMBOLIC_SOURCE_RULE","Cor Leonis in partill","Named fixed star and Mars near eighth-house cusp underpin fortune speculation.","mechanical_predicate"),
(756,"WIFE_INHERITS_ESTATE","HISTORICAL_UNVERIFIED_FINANCIAL_OUTCOME","a plentifull Estate left her","Forecast one wife may have fixed fortune/inherited property.","economic"),
(756,"WIVES_ESTATE_HINDERED_BY_OTHERS","HISTORICAL_UNVERIFIED_FINANCIAL_OUTCOME","shall endeavour either upon pretences to keep it back","Predicts interference or withholding of wife's money or inherited estate.","economic"),
(756,"ESTATE_ARRIVES_LATE","HISTORICAL_UNVERIFIED_FINANCIAL_OUTCOME","some trouble or vexation ere he obtaine it","Forecast eventual access to funds after obstacles.","economic"),
(756,"VENUS_FOURTH_AND_MERCURY_APPLIES","SYMBOLIC_SOURCE_RULE","Mercury Lord of","Uses fourth-house lord Venus and Mercury's application to Sun/Venus to argue estate transfer.","mechanical_predicate"),
(756,"ESTATE_APPROX_THREE_MONTHS_OR_TERMS","EXPLICIT_HISTORICAL_TIME_AMBIGUITY","after almost three moneths, or perhaps so many Termes","Gives explicit alternative time units for property transfer; not a precise calendar prediction.","temporal_ambiguous"),
(756,"FORTUNE_AND_TROUBLE_COMBINED","HISTORICAL_UNVERIFIED_FINANCIAL_OUTCOME","Fortune, but much trouble","Summary predicts wife/wives bring good fortune but difficulty obtaining part of it.","economic"),
(756,"WIVES_ORIGINS_SUBSECTION","SUBSECTION_HEADER","Which way they shall live","Subsection on wives' geographic origins / local residency.","navigation"),
(756,"FIRST_WIFE_EAST_SOUTH_FROM_BIRTH","HISTORICAL_UNVERIFIED_GEOGRAPHIC_OUTCOME","Eastward, inclining somewhat to the South","Forecast first wife's residence/origin east to southeast of merchant birthplace.","residence"),
(756,"FIRST_WIFE_NOT_SAME_SHIRE","HISTORICAL_UNVERIFIED_GEOGRAPHIC_OUTCOME","not Native of his owne Shire","Forecast first wife not born in merchant's shire.","residence"),
(757,"SECOND_WIFE_WEST_FAR","HISTORICAL_UNVERIFIED_GEOGRAPHIC_OUTCOME","west, farre from the place","Forecast second wife west of birthplace and far away.","residence"),
(757,"SECOND_WIFE_ENGLISH","HISTORICAL_UNVERIFIED_NATIONALITY_OUTCOME","but English","Qualified assertion second wife English, despite foreign-direction location.","nationality"),
(757,"PHYSICAL_CHILDREN_NEXT_CHAPTER","NEXT_CHAPTER_BOUNDARY","Of Children.","Physical divider then independent fifth-house Chapter CLXXXII begins; no children outcome recorded as marriage.","navigation"),
]

def build():
    west=read(WESTERN)
    china=read(CHINESE_V7)
    if (west["records_count"]!=13044 or west["batches"][-1]["id"]!="B07bc"
            or west["source_sha256"]!=ORIGINAL_FULL_1647_SHA
            or west["next"]["chapter"]!="CLXXXI" or west["next"]["pdf_page"]!=788):
        raise ValueError("Accepted original Lilly B07bc append frontier drift")
    if file_sha(CHINESE_V7)!=CHINESE_V7_SHA or china["sum_source_annotations"]!=355:
        raise ValueError("Separate accepted Chinese V7 frozen source changed")
    photos=photo_witnesses()
    if set(photos)!={"754","755","756","757"}:
        raise ValueError("Expected exactly four original printed folios")
    records=[]
    unique=set()
    for i,(folio,role,layer,original_anchor,gloss,target) in enumerate(SOURCE_CLAUSES):
        if role in unique or folio not in (754,755,756,757):
            raise ValueError("Repeated role or out-of-scope marriage original folio")
        if i>0 and folio<SOURCE_CLAUSES[i-1][0]:
            raise ValueError("Documentary source order must follow printed folios")
        unique.add(role)
        data=photos[str(folio)]
        records.append({
            "id":f"R{START_R+i}",
            "record_number":START_R+i,
            "batch":"B07bd",
            "printed_folio":folio,
            "1647_first_edition_pdf_frame":folio+34,
            "1659_separately_printed_DjVu_frame":folio+29,
            "source_span":f"B07bd-S{folio-753:03d}",
            "source_1647_original_photo_sha256":data["1647"]["photo_sha256"],
            "source_1659_original_print_photo_sha256":data["1659"]["photo_sha256"],
            "role":role,
            "historical_evidence_category":layer,
            "1647_short_original_anchor_not_diplomatic_transcription":original_anchor,
            "working_source_gloss_not_original_quote":gloss,
            "candidate_scored_target_type_NOT_pre_registered":target,
            "actual_merchant_life_and_spouse_outcomes_independently_verified":False,
            "original_astrological_glyphs_full_expert_collation_done":False,
            "real_human_behavioral_prediction_validation_count":0,
            "apply_historical_moral_gender_appearance_claims_to_person":False,
            "runtime_astrological_model_promoted":False,
        })
    if records[0]["id"]!="R13045" or records[-1]["role"]!="PHYSICAL_CHILDREN_NEXT_CHAPTER":
        raise ValueError("Marriage first source and final physical divider shifted")
    if len(records) < 45:
        raise ValueError("Incomplete clause-level source coverage")
    source={
        "schema":"LILLY_B07bd_ORIGINAL_1647_1659_CLXXXI_MARRIAGE_SOURCE_V1",
        "status":"ORIGINAL_SOURCE_DRAFT_PENDING_GUARDED_REGISTRY_ACCEPTANCE",
        "batch":"B07bd",
        "parent_accepted_original_source_commit":PARENT_SHA,
        "original_Wellcome_1647_whole_PDF_sha256":ORIGINAL_FULL_1647_SHA,
        "whole_1659_DjVu_binary_verified":False,
        "all_original_1647_1659_folio_photo_sha_and_bytes_verified":True,
        "four_original_folio_photographs":photos,
        "original_1647_printed_folios":[754,755,756,757],
        "original_1659_DjVu_frames":[783,784,785,786],
        "first_marriage_Chapter_CLXXXI_begins_after_CLXXX_sixth_house_divider":True,
        "last_marriage_Chapter_CLXXXI_ends_before_CLXXXII_children_divider":True,
        "distinct_merchant_already_known_to_author":True,
        "source_predicted_marriage_count":2,
        "source_predicted_extra_sweethearts":2,
        "source_maturity_threshold_after_age_years":29,
        "source_actual_merchant_marriage_count_independently_verified":False,
        "source_actual_spouse_appearance_or_money_geography_independently_verified":False,
        "interpretive_17th_century_sex_norms_validated":False,
        "original_1647_1659_exact_all_glyphs_expert_collated":False,
        "independent_prospective_human_predictive_tests":0,
        "astrology_production_promotions":0,
        "new_source_only_records":len(records),
        "first_R":records[0]["id"],
        "last_R":records[-1]["id"],
        "next_R":f"R{START_R+len(records)}",
        "next_original_folio":757,
        "next_original_pdf_frame":791,
        "next_chapter":"CLXXXII Of Children",
        "all_source_records":records,
    }
    write(B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json",source)
    write(B/"RULES.json",{
        "batch":"B07bd","status":"HISTORICAL_MARRIAGE_SOURCE_ONLY_NO_PERSON_PREDICTIONS",
        "original_folios":[754,755,756,757],
        "record_count":len(records),
        "first_R":records[0]["id"],"last_R":records[-1]["id"],
        "new_17th_century_gender_stereotypes_are_not_empirical_life_rules":True,
        "human_predictive_validation_count":0,
        "runtime_model_promotions":0,
        "rules":records,
    })
    write(B/"ACCEPTANCE.json",{
        "batch":"B07bd","parent":PARENT_SHA,
        "Lilly_before":13044,"Ptolemy_retained":1066,
        "Chinese_V7_historical_retained":355,
        "new_historical_source_only_notes":len(records),
        "Lilly_after_if_accepted":13044+len(records),
        "Western_after_if_accepted":13044+len(records)+1066,
        "first_R":records[0]["id"],"last_R":records[-1]["id"],
        "next_R":f"R{START_R+len(records)}",
        "next_original_pdf_frame":791,
        "next_printed_folio":757,
        "next_chapter":"CLXXXII Of Children",
        "original_1647_1659_CLXXXI_physically_covered":True,
        "critical_17th_century_astro_glyphs_fully_verified":False,
        "original_source_merchant_marriage_outcome_independently_verified":False,
        "retrospective_known_merchant_cannot_count_as_blind":True,
        "genuine_human_predictive_validations":0,
        "production_runtime_promotions":0,
        "original_photo_manifest_sha256":file_sha(B/"ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json"),
        "source_notes_sha256":file_sha(B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json"),
        "rules_sha256":file_sha(B/"RULES.json"),
        "Chinese_V7_index_sha256":file_sha(CHINESE_V7),
    })
    print("B07bd draft notes",len(records),"start",records[0]["id"],"end",records[-1]["id"],
          "next",f"R{START_R+len(records)}","after_if_accepted",13044+len(records))

if __name__=="__main__":
    build()
