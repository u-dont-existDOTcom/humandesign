#!/usr/bin/env python3
"""1647 and independently typeset 1659 Lilly CLXXXIII Travels, source only.

Printed pages758-760; distinct original tenth-house chapter starts p760.
Preserves author's preknown 3-trip marginal fact as DISCLOSED PRIOR
information rather than astrological accuracy. All forecasts unverified.
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
BASE=T/"batches"
START=13132
PREV_ACCEPTED_SHA="fe84cb135a3aa976de34140ea39d99e0138aa862"
WELLCOME_ORIGINAL_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
CHINA_SHA="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"

def read(p):return json.loads(p.read_text(encoding="utf-8"))
def digest(p):return sha256(p.read_bytes()).hexdigest()
def write(p,what):p.write_text(json.dumps(what,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def original_witnesses():
    b07be=read(BASE/"B07be/ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json")
    prior=b07be["source_photo_witnesses"]["758"]
    witnesses={"758":{edition:{
        **{
          "source_edition":int(edition),
          "printed_folio":758,
          "source_frame":758+(34 if edition=="1647" else 29),
          "source_photo_path":prior[edition]["source_photo_path"],
          "original_source_url":prior[edition]["source_photo_url"],
          "sha256":prior[edition]["photo_SHA256"],
          "bytes":prior[edition]["photo_bytes"],
          "reused_from_previously_accepted_source":True
        },
    } for edition in ("1647","1659")}}
    historic_folio759_first=BASE/"B07bd/next_children_1647_photo_prefetch/1647-original-folio759-iiif.jpg"
    local={
        (759,"1647"):historic_folio759_first,
        (759,"1659"):B/"evidence/1659-original-folio759-DjVu.jpg",
        (760,"1647"):B/"evidence/1647-original-folio760-IIIF.jpg",
        (760,"1659"):B/"evidence/1659-original-folio760-DjVu.jpg",
        (761,"1647"):B/"evidence/1647-original-folio761-IIIF.jpg",
        (761,"1659"):B/"evidence/1659-original-folio761-DjVu.jpg",
    }
    known={
        (759,"1647"):("c2a761067fca9491082c4c3d31dedea0702b5d480bda6c22255b6e363610e2e2",856378),
        (759,"1659"):("8cc8da53ddd25f0c84bb1fef98cada8dcd894ae76521a0a985503cffa2ce3a24",546168),
        (760,"1647"):("d396901ee82ffc702aa42783195603333a8eef4a5b53ea53b9c1b13c7b2e842d",756066),
        (760,"1659"):("886dedb21b77f36b8eead74b2b888e7625699d71a74dcdcd151625274c808dd5",549832),
        (761,"1647"):("db6d432f7ab1549f1480560bd16d8edc4c710f3c28c4984c7fced64ae69b64ff",858238),
        (761,"1659"):("2628bf8e9ec26ceb7d7ae9bb9efa79d6fb6cfec8b0ab03f85b76733a0ae1cf60",568713),
    }
    for (folio,edition),photo in local.items():
        pinned,nbytes=known[(folio,edition)]
        if not photo.is_file() or photo.stat().st_size!=nbytes or digest(photo)!=pinned:
            raise ValueError(f"Original first/second edition {folio} {edition} image mismatch")
        url=(
            f"https://iiif.wellcomecollection.org/image/b30338724_{folio+34:04d}.jp2/full/1800,/0/default.jpg"
            if edition=="1647" else
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/"
            "Christian_Astrology_%28Lilly%2C_1659%29.djvu/"
            f"page{folio+29}-1280px-Christian_Astrology_%28Lilly%2C_1659%29.djvu.jpg"
        )
        witnesses.setdefault(str(folio),{})[edition]={
            "source_edition":int(edition),"printed_folio":folio,
            "source_frame":folio+(34 if edition=="1647" else 29),
            "source_photo_path":str(photo.relative_to(ROOT)),
            "original_source_url":url,
            "sha256":pinned,"bytes":nbytes,
            "reused_from_previously_accepted_source":folio==759 and edition=="1647",
        }
    for folio,pair in witnesses.items():
        if set(pair)!={"1647","1659"}:
            raise ValueError("Original separately printed source editions missing")
        for edition,obj in pair.items():
            photo=ROOT/obj["source_photo_path"]
            if (not photo.is_file() or photo.stat().st_size!=obj["bytes"]
                or digest(photo)!=obj["sha256"]):
                raise ValueError(f"Accepted original {folio} {edition} bytes changed")
    return witnesses

# 1647 original short exact wording fragment and separate interpretive working
# summary. Source note purpose: distinct rules, examples, claims and negatives.
CLAUSES=[
(758,"CLXXXIII_TRAVELS_HEADING","SOURCE_CHAPTER_BOUNDARY","Of Travels.","New ninth-house original chapter after CLXXXII Children physical divider.","navigation"),
(758,"TRAVEL_NATURAL_INCLINATION_QUESTION","ORIGINAL_QUESTION","Whether naturally this Native was designed to Travell","The author raises prospective inclination rather than observing the biography here.","question"),
(758,"MERCURY_MOON_TRAVEL_SIGNIFICATORS","SOURCE_ASTRO_RULE","who signifie Travels","Swift Mercury and Moon are chosen as natural travel significators.","mechanical"),
(758,"TRINE_SEXTILE_THIRD_NINTH_RULE","SOURCE_ASTRO_RULE","out of the ninth or third houses","Trines or sextiles from third and ninth houses supply a general travel trigger.","mechanical"),
(758,"MOBILE_SIGNS_NEVER_REST","HISTORICAL_UNVERIFIED_GENERALIZATION","will never rest at home","Movable signs in the travel rule are said to promote constant foreign journeys.","conditional_forecast"),
(758,"THIRD_NEAR_NINTH_FAR","SOURCE_DERIVED_HOUSE_RULE","the ninth farther off","Third denotes shorter/near travel, ninth denotes distant travel.","mechanical"),
(758,"REPORTED_THREE_PREVIOUS_SEA_VOYAGES","DISCLOSED_PREEXISTING_OBSERVATION_NOT_CHART_INFERENCE","He hath thrice been beyond Sea","Page marginal note discloses three previous sea voyages as known information.","already_known_unverified"),
(758,"REPORTED_TWO_BARBARY_VOYAGES","DISCLOSED_PREEXISTING_OBSERVATION_NOT_CHART_INFERENCE","twice in Barbary","Past narrative reports two Barbary journeys; no corroborating travel logs.","already_known_unverified"),
(758,"REPORTED_ONE_HOLLAND_VOYAGE","DISCLOSED_PREEXISTING_OBSERVATION_NOT_CHART_INFERENCE","once in Holland.","Past narrative reports one Holland journey; no corroborating travel logs.","already_known_unverified"),
(758,"MERCURY_MOON_TRINE","SOURCE_ASTRO_PREDICATE","in our Scheme","Author's example attributes travel tendency to a Mercury-Moon trine.","mechanical"),
(758,"MUTUAL_RECEPTION_SMALL","SOURCE_ASTRO_PREDICATE","reception besides","Moon-Mercury small mutual reception is cited as additional travel support.","mechanical"),
(758,"AFFIRM_TRAVEL_FROM_CHART","HISTORICAL_UNVERIFIED_JUDGMENT","this Native should travell","Claims a chart-based travel judgment, though the past voyages were disclosed.","binary"),
(758,"INTERVALS_BETWEEN_JOURNEYS","HISTORICAL_UNVERIFIED_FREQUENCY_FORECAST","space of time betwixt Journey and Journey","Mixed movable/common signs cause intermittent rather than uninterrupted travel.","frequency"),
(758,"PART_OF_WORLD_HEADING","SOURCE_SUBSECTION","Part of the World.","Separate travel geography section.","navigation"),
(758,"MARS_THIRD_VENUS_NINTH","DERIVED_HOUSE_PREDICATE","Lord of the third","Mars rules third travel; Venus controls ninth distant travel, Moon and Mercury additional.","mechanical"),
(758,"TRAVEL_SIGN_ARIES_LIBRA_GEMINI","SOURCE_ASTRO_GEOGRAPHY","the Signes","Specific natal travel significator signs are cited without independent chart data.","mechanical"),
(758,"MARS_WEST_ANGLE","SOURCE_ASTRO_GEOGRAPHY","Mars is in the West angle","Mars is located at a western chart angle.","mechanical"),
(758,"MOON_WEST_QUARTER_NORTH","SOURCE_ASTRO_GEOGRAPHY","in West quarter","Moon situated in western quarter inclining north.","mechanical"),
(758,"VENUS_SOUTHWEST_QUARTER","SOURCE_ASTRO_GEOGRAPHY","in Southwest quarter","Venus assigned southwest geographical quarter.","mechanical"),
(758,"MARS_MOON_NATURAL_WEST","SOURCE_ASTRO_GEOGRAPHY","naturally signifie the West","Mars and Moon considered to signify west in this symbolic tradition.","mechanical"),
(758,"VENUS_NATURAL_SOUTH","SOURCE_ASTRO_GEOGRAPHY","the South","Venus described as naturally southerly.","mechanical"),
(758,"MERCURY_PEREGRINE_SUN_WEAK","SOURCE_ASTRO_PREDICATE","being Peregrine","Travel compass weighting based on Mercury's debility and Sun weakness.","mechanical"),
(758,"SOUTH_BY_WEST_DESTINATIONS","HISTORICAL_UNVERIFIED_DIRECTION_FORECAST","South and by West","Main predicted journey direction is southern tending west/southwest.","direction"),
(758,"SOUTHEAST_UNLIKELY_JOURNEY","NEGATIVE_HISTORICAL_DIRECTION_FORECAST","Native denied travelling towards the South-east","South-east journeys are described as less indicated, a qualified negative forecast.","direction_negative"),
(759,"MARS_LEO_SATURN_TAURUS_SOUTHEAST","SOURCE_ASTRO_GEOGRAPHY","Mars is entring Leo","Southeast alternative considered from Mars entering Leo and Saturn in Taurus.","mechanical"),
(759,"DISCOURAGE_SOUTHEAST_UNLESS_SATURN","EXPLICIT_SOURCE_CONDITION","cannot encourage much that wayes","Southeast route not encouraged unless Saturn strong in easterly sign.","conditional_direction"),
(759,"TRAVEL_CAUSE_SUBSECTION","SOURCE_SUBSECTION","The cause moving to Travell.","Travel motivation section independent of geographical inference.","navigation"),
(759,"TRAVEL_CAUSE_HOUSE_LORDS","SOURCE_METHOD_PREFERENCE","houses of which the Significators are Lords","Lilly prefers houses ruled by significators to their mere positions for motives.","mechanical"),
(759,"VENUS_MERCURY_SUN_IN_EIGHTH","SOURCE_ASTRO_PREDICATE","are in the eighth","Venus, Mercury and Sun said to be in eighth and linked to resources.","mechanical"),
(759,"VENUS_FOURTH_MERCURY_MOON_DISPOSITOR","SOURCE_ASTRO_PREDICATE","being Lady of the fourth","Venus as fourth ruler and Mercury dispositor of Moon used in motive inference.","mechanical"),
(759,"MOON_SEVENTH_MARS_PRESENT","SOURCE_ASTRO_PREDICATE","Lady of the seventh","Moon rules seventh and Mars placed there; source sees occupational link.","mechanical"),
(759,"TRAVEL_FOR_WEALTH_MERCURY_MOON","HISTORICAL_UNVERIFIED_MOTIVE_INFERENCE","desire to encrease his Fortune","Trine and relevant rulers used to infer wealth-motivated travel.","motivation"),
(759,"FOREIGN_TRAVEL_AS_PERSONAL_DESIRE","HISTORICAL_UNVERIFIED_MOTIVE_INFERENCE","propensity to visit forreign parts","Source conjectures natural desire for foreign travel.","motivation"),
(759,"PROFESSION_MARS_TENTH","SOURCE_ASTRO_PREDICATE","Mars also being Lord of the tenth","Tenth lord Mars brings trade or profession into travel question.","mechanical"),
(759,"TRAVEL_BY_OFFICIAL_COMMISSION","HISTORICAL_UNVERIFIED_MOTIVE_INFERENCE","by commission or authority","Suggests travel might begin by a patron's commission or government/official task.","motivation"),
(759,"TRAVEL_SUCCESS_SUBSECTION","SOURCE_SUBSECTION","Successe in Travels.","Separate outcome/reputation section.","navigation"),
(759,"SPICA_VIRGO_NEAR_NINTH","SOURCE_FIXED_STAR_PREDICATE","Spica Virgo with the cusp","Spica Virgo cited as near ninth cusp supporting safe journey.","mechanical"),
(759,"VENUS_FORTIFIED_NINTH_FREE","SOURCE_ASTRO_PREDICATE","essentially fortified","Venus strong and ninth house free of hostile Saturn/Mars aspect.","mechanical"),
(759,"TRAVEL_WEALTH_REPUTATION_SUCCESS","HISTORICAL_UNVERIFIED_SUCCESS_FORECAST","attained Wealth and Reputation","Predicts favourable travel with prosperity and enhanced reputation.","financial_status"),
(759,"MOON_MARS_AND_MARS_VENUS_SEXTILES","SOURCE_ASTRO_PREDICATE","Signs of long ascensions","The Moon/Mars and Mars/Venus sextiles also underpin safety concern.","mechanical"),
(759,"DIRECTIONS_CONDITION_RISKS","EXPLICIT_TIMING_UNCERTAINTY","upon some malevolent direction","Serious dangers are tied to adverse astrological directions, not a definite dated outcome.","conditional_risk"),
(759,"FUTURE_FIRE_THREAT","HISTORICAL_UNVERIFIED_HARM_FORECAST","danger by a sudden fire","Conditional danger forecast involving sudden fire.","harm_risk"),
(759,"FUTURE_SHIPWRECK_THREAT","HISTORICAL_UNVERIFIED_HARM_FORECAST","or by shipwrack","Conditional shipwreck risk without date/location or actual record.","harm_risk"),
(759,"FUTURE_ROBBERY_RISK","HISTORICAL_UNVERIFIED_HARM_FORECAST","robbery and depredation","Conditional robbery or predation by thieves during travel.","harm_risk"),
(759,"FUTURE_THIEVES_SAILORS","HISTORICAL_UNVERIFIED_HARM_FORECAST","Thieves and Saylors","The text names thieves and sailors as possible sources of robbery.","harm_risk"),
(759,"WAIT_FOR_BENEVOLENT_DIRECTION","HISTORICAL_PRACTICE_NOT_PROVEN","rest quiet, unlesse he find a stronger benevolent","Ancient advice to pause travel during adverse directions is not modern safety advice.","historic_recommendation"),
(760,"BENEVOLENT_CAN_CONTRADICT_MARS","EXPLICIT_MITIGATION_OR_OVERRIDE","that of Mars may be contradicted","A supposedly benevolent direction can override earlier Mars danger, making forecast conditional.","override_rule"),
(760,"KINGDOMS_COUNTRIES_SECTION","SOURCE_SUBSECTION","Kingdomes and Countries","Section on regions supposedly fortunate for travel.","navigation"),
(760,"CAPRICORN_COUNTRIES_HEALTH_SECURITY","HISTORICAL_UNVERIFIED_COUNTRY_FORECAST","promise the Native health and security","Capricorn-governed countries described as safe/protective, not empirical safety data.","geography_safety"),
(760,"PISCES_COUNTRIES_FORTUNE_GAIN","HISTORICAL_UNVERIFIED_COUNTRY_FORECAST","encrease his Fortune exceedingly","Pisces-governed countries purportedly highly profitable.","geography_finance"),
(760,"JUPITER_ESSENTIAL_SAG","SOURCE_ASTRO_RULER_PREDICATE","essentially strong in Sagittarius","Ruler Jupiter strong in Sagittarius cited for Pisces country fortune.","mechanical"),
(760,"LIBRA_COUNTRIES_TRADE_REPUTATION","HISTORICAL_UNVERIFIED_COUNTRY_FORECAST","advance his Estate and Reputation","Libra-governed regions forecast trade, estate and reputation growth.","geography_finance"),
(760,"VENUS_SAFE_RETURN_SUN_HONOUR","HISTORICAL_UNVERIFIED_TRAVEL_SUCCESS","portends a safe returne","Venus supposedly promises safe return, Sun honours in Libra-linked areas.","geography_safety"),
(760,"SAGITTARIUS_COUNTRIES_STOCK","HISTORICAL_UNVERIFIED_INVESTMENT_COUNTRY_FORECAST","safely adventure either his person or stock","Sagittarius-ruled places deemed safe to invest person or commercial stock.","financial_risk"),
(760,"CAPRICORN_SOUTHWEST_SIDE","HISTORICAL_UNVERIFIED_DIRECTIONAL_CONDITION","Southern parts thereof, verging a little to the West","Within supposed Capricorn regions advises southern/western portions.","direction"),
(760,"PISCES_NORTH_CITIES","HISTORICAL_UNVERIFIED_DIRECTIONAL_CONDITION","Cities in the North","Within supposed Pisces regions specifies northern cities.","direction"),
(760,"LIBRA_WEST_SOUTH_TRADE","HISTORICAL_UNVERIFIED_DIRECTIONAL_CONDITION","West part thereof, verging a little South","Within Libra-associated lands specifies west/south trading regions.","direction"),
(760,"SAGITTARIUS_EAST_NORTHEAST","HISTORICAL_UNVERIFIED_DIRECTIONAL_CONDITION","East and North-east parts thereof","Within Sagittarius-associated regions specifies east/northeast.","direction"),
(760,"RELIGIOUS_DREAMS_EXPLICIT_DEFERENCE","SOURCE_DISCLOSURE_OF_SUBJECTIVE_JUDGMENT","Dreams and Religion I leave to the Natives owne judgment","Explicitly avoids divination about dreams and religion before next separate claim.","explicit_nonprediction"),
(760,"RELIGION_SAME_AS_UPBRINGING","HISTORICAL_UNVERIFIED_RELIGION_FORECAST","Religion he was trained up in","Historical forecast that merchant will remain in childhood religion, no independent follow-up.","belief"),
(760,"NEXT_HONOURS_CHAPTER_CLXXXIIII","NEXT_SEPARATE_CHAPTER_BOUNDARY","Honours, Preferment","Physical tenth-house separate chapter follows horizontal divider, as printed first edition CLXXXIIII.","navigation"),
]

def build():
    index=read(WEST)
    china=read(CHINA)
    if (index["records_count"],index["batches"][-1]["id"],
        index["next"]["chapter"],index["next"]["pdf_page"],
        index["next"]["printed_page"])!=(13131,"B07be","CLXXXIII",792,758):
        raise ValueError("Exact accepted source children frontier not found")
    if index["source_sha256"]!=WELLCOME_ORIGINAL_SHA or digest(CHINA)!=CHINA_SHA or china["sum_source_annotations"]!=355:
        raise ValueError("Accepted old primary source root or separate Chinese source changed")
    photos=original_witnesses()
    out=[]; roles=set()
    for i,(folio,role,kind,exact,gloss,target) in enumerate(CLAUSES):
        if role in roles or folio not in (758,759,760):
            raise ValueError("Duplicate or wrong original source role/folio")
        roles.add(role)
        w=photos[str(folio)]
        out.append({
            "id":f"R{START+i}","record_number":START+i,
            "source_batch":"B07bf",
            "printed_original_folio":folio,
            "original_first_1647_pdf_frame":folio+34,
            "original_independent_1659_DjVu_frame":folio+29,
            "original_1647_source_photo_SHA256":w["1647"]["sha256"],
            "original_1659_typeset_source_photo_SHA256":w["1659"]["sha256"],
            "source_role":role,"historical_evidence_type":kind,
            "1647_original_short_verbatim_anchor_NOT_diplomatic_full_transcription":exact,
            "working_source_interpretation_NOT_original_quote":gloss,
            "possible_future_blind_target_NOT_frozen":target,
            "author_already_knows_merchant":True,
            "already_known_prior_travel_information":kind=="DISCLOSED_PREEXISTING_OBSERVATION_NOT_CHART_INFERENCE",
            "independently_verified_merchant_historical_voyages":False,
            "independently_validated_conditional_harm_forecast":False,
            "independently_blind_real_human_prediction":False,
            "historic_recommendation_allowed_as_current_person_advice":False,
            "astrological_runtime_rule_promoted":False,
        })
    if (out[0]["id"],out[-1]["source_role"],len(out))!=(
        "R13132","NEXT_HONOURS_CHAPTER_CLXXXIIII",len(CLAUSES)
    ) or len(out)<55:
        raise ValueError("Source chapter open/close and case coverage drift")
    record={
        "schema":"ORIGINAL_1647_1659_LILLY_CLXXXIII_TRAVELS_DOCUMENTARY_SOURCE_V1",
        "status":"HISTORICAL_SOURCE_DRAFT_ONLY_PENDING_CANONICAL_ACCEPTANCE",
        "parent_accepted_source_commit":PREV_ACCEPTED_SHA,
        "original_1647_Wellcome_full_book_SHA256":WELLCOME_ORIGINAL_SHA,
        "separate_full_1659_DjVu_binary_SHA256_not_independently_verified":True,
        "original_first_and_second_print_photo_SHA_and_bytes_enforced":True,
        "source_original_printed_folios":[758,759,760,761],
        "source_travels_substantive_folios":[758,759,760],
        "physical_next_chapter": "CLXXXIIII (original literal, editorial184) Honours Preferment",
        "next_honours_first_substantive_new_chapter_p761":True,
        "four_source_page_first_second_photo_witnesses":photos,
        "source_retrospective_marginal_voyages":{
            "known_reported_voyages_beyond_sea":3,
            "known_reported_voyages_to_Barbary":2,
            "known_reported_voyages_to_Holland":1,
            "author_disclosed_them_before_astrological_interpretation":True,
            "external_ship_passenger_log_birth_history_verified":False,
            "cannot_count_as_out_of_sample_chart_prediction":True,
        },
        "source_future_disaster_hazards_are_conditional_to_unspecified_directions":True,
        "source_travel_fortune_success_not_independently_verified":True,
        "source_contradictory_mars_benevolent_override_documented":True,
        "source_religion_asked_about_dreams_explicitly_deferred":True,
        "original_astrological_glyphs_expert_blind_diplomatic_collation":False,
        "new_documentary_source_notes":len(out),
        "first_R":out[0]["id"],
        "last_R":out[-1]["id"],
        "next_R":f"R{START+len(out)}",
        "next_original_printed_folio":760,
        "next_original_1647_pdf_frame":794,
        "next_chapter_editorial":"CLXXXIV Honours, Preferment, Magistery",
        "human_retro_blinded_outcomes_verified":0,
        "human_prospective_blinded_outcomes_verified":0,
        "production_astrology_runtime_promotions":0,
        "records":out
    }
    write(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json",record)
    write(B/"RULES.json",{
        "batch":"B07bf",
        "status":"HISTORICAL_TRAVELS_SOURCE_ONLY_PREVIOUS_KNOWN_VOYAGES_NOT_PREDICTIONS",
        "record_count":len(out),
        "first_record":out[0]["id"],"last_record":out[-1]["id"],
        "all_actual_forecasts_real_outcomes_independently_verified":False,
        "astrological_runtime_rule_promotions":0,
        "rules":out
    })
    write(B/"ACCEPTANCE.json",{
        "batch":"B07bf",
        "parent_accepted_source_commit":PREV_ACCEPTED_SHA,
        "Lilly_before":13131,
        "Ptolemy_retained":1066,
        "Chinese_V7_sha256_unchanged":CHINA_SHA,
        "new_source_only_historical_notes":len(out),
        "Lilly_after_if_accepted":13131+len(out),
        "Western_after_if_accepted":13131+len(out)+1066,
        "first_R":out[0]["id"],"last_R":out[-1]["id"],
        "next_R":f"R{START+len(out)}",
        "next_printed_chapter":"CLXXXIIII","next_chapter_editorial_ordinal":184,
        "next_original_first_1647_pdf_frame":794,
        "next_original_printed_folio":760,
        "original_travels_text_only_folios":[758,759,760],
        "source_historical_past_known_travels_must_not_be_counted_as_astrological_prediction":True,
        "original_all_4_folio_2_edition_images_sha_verified":True,
        "source_all_original_1647_1659_astrological_glyphs_expert_verified":False,
        "independent_retrospective_merchant_voyages_and_forecasts_verified":False,
        "human_predictive_successes_validated":0,
        "runtime_astrological_promotions":0,
        "source_sha256":digest(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json"),
        "rules_sha256":digest(B/"RULES.json"),
    })
    print("B07bf PROVISIONAL",len(out),out[0]["id"],out[-1]["id"],
          "NEXT",record["next_R"],"WESTERN_AFTER_IF_ACCEPTED",13131+len(out)+1066)

if __name__=="__main__":
    build()
