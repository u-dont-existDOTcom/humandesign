#!/usr/bin/env python3
"""Generate a source-identity-only 20×community Maya registry for shared surveys.

No horoscope, predicted answer, participant or cultural-policy equivalence
is introduced. Preserve independent original source communities and all
negative/stigmatizing source exclusions as quarantined historical metadata.
"""
import json
from pathlib import Path
from maya_calendar_reference import YUCATEC_DAYS, KICHE_DAY_NAMES_BY_YUCATEC

ROOT=Path(__file__).resolve().parent
YUC=ROOT/"MAYA_B07_YUCATEC_NATAL_20_SOURCE_DOMAIN_ROWS.txt"
HIGHLAND=ROOT/"MAYA_MOMOSTENANGO_ZUNIL_NATAL_DOMAIN_CROSSWALK_V1.json"
OUTPUT=ROOT/"MAYA_COMBINED_SOURCE_DAYNAME_SURVEY_INDEX_V1.json"

def _yucatec():
    rows=[]
    for line in YUC.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):continue
        fields=line.split("|")
        if len(fields)!=6:raise ValueError("Historic source row changed shape")
        serial,name,canonical,pageno,domain,disposition=fields
        rows.append({
          "source_id":"BOLLES-PCML-COLONIAL-YUCATEC",
          "sequence_number":int(serial),
          "historical_Yucatec_spelling":name,
          "canonical_Yucatec_day_name":canonical,
          "Kiche_linguistic_crosswalk_not_same_natal_predicate":
            dict(zip(YUCATEC_DAYS,KICHE_DAY_NAMES_BY_YUCATEC))[canonical],
          "source_pdf_page_number":int(pageno),
          "source_semantic_domain_metadata_only":domain,
          "source_claim_disposition":disposition,
          "automatically_scored":False,
          "contemporary_birth_day_clock_verified":False,
          "unscored_historical_stigma":disposition=="QUARANTINE"
        })
    if len(rows)!=20 or [v["sequence_number"] for v in rows]!=list(range(1,21)):
        raise ValueError("Require all historical Yucatec 20 day names")
    if {r["canonical_Yucatec_day_name"] for r in rows}!=set(YUCATEC_DAYS):
        raise ValueError("Mismatch Yucatec source names and reference converter")
    return rows

def _highland():
    x=json.loads(HIGHLAND.read_text(encoding="utf-8"))
    rows=[{
      "source_id_pair":["TEDLOCK-MOMOSTENANGO-1992","KOMON-TOHIL-ZUNIL-NMAI"],
      "Kiche_day_name":r["kiche_reference_name"],
      "Yucatec_linguistic_crosswalk_not_same_natal_predicate":r["yucatec_crosswalk"],
      "Momostenango_source_pdf_or_printed_page":r["momostenango_page"],
      "Zunil_original_PDF_page":r["zunil_pdf_page"],
      "Momostenango_natal_source_domain_metadata_only":r["momostenango_natal_domain_labels"],
      "Zunil_natal_source_domain_metadata_only":r["zunil_natal_domain_labels"],
      "source_difference_not_resolved":r["comparison"],
      "stigma_quarantine":bool(r["stigma_or_safety_quarantine"]),
      "same_community_or_source":False,
      "automatically_scored":False,
      "independent_real_human_evidence":0
    } for r in x["records"]]
    if len(rows)!=20 or {r["Kiche_day_name"] for r in rows}!=set(KICHE_DAY_NAMES_BY_YUCATEC):
        raise ValueError("Require all 20 historical Highland names")
    return rows

def create():
    return {
      "schema":"MAYA_FULL_DAYNAME_SOURCE_IDENTITY_FOR_SHARED_SURVEY_V1",
      "status":"HISTORICAL_20_YUCATEC_PLUS_20_HIGHLAND_PAIRS_UNSCORED",
      "date":"2026-10-23",
      "source_files":[YUC.name,HIGHLAND.name],
      "reference_calendar_file":"maya_calendar_reference.py",
      "Yucatec_colonial_named_days":_yucatec(),
      "Highland_Kiche_two_community_named_day_pairs":_highland(),
      "historical_maya_codex_astronomy":"EXCLUDED_FROM_NATAL_SURVEY_CLAIMS",
      "modern_Dreamspell":"SEPARATE_MODERN_NON_CLASSICAL_SOURCE_NOT_MERGED",
      "original_natal_numerals_1_to_13":"NOT_AN_AUTOMATIC_PERSONALITY_RULE",
      "living_day_count_correlation_and_boundary":"UNRESOLVED_FOR_COMMUNITY_SPECIFIC_NATAL_USE",
      "identity_matching_is_not_source_prediction_equivalence":True,
      "actual_participants":0,"validated_natal_predictions":0,
      "new_surveys_or_scoring_rules_deployed":0
    }

if __name__=="__main__":
    obj=create()
    OUTPUT.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(OUTPUT,len(obj["Yucatec_colonial_named_days"]),
          len(obj["Highland_Kiche_two_community_named_day_pairs"]))
