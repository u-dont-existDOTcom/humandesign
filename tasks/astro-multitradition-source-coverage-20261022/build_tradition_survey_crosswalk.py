#!/usr/bin/env python3
"""Generate a scope-typed crosswalk; do not fabricate historical source claims.

This is research design metadata, not a questionnaire edit or a scored model.
"""
from __future__ import annotations
import json
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
BASE=ROOT/"reference/core/survey_v2_behavioral_domains.json"

DECLARED_OTHER=[
 ("WESTERN-LILLY-HORARY","Western Lilly","event_or_horary",None,"lost-object, property, physician, imprisonment and other question-specific event outcomes","traditional_source_notes_exist_original_claim_to_question_not_converted",
  "A horary question needs a question time and independently defined outcome, not a birth-personality survey."),
 ("WESTERN-PTOLEMY-NATAL","Ptolemaic/Western","natal_trait_or_event",None,"temperament/conditions and subsequent natal life chapters","source_counts_exist_specific_behavioral_mapping_unverified",
  "Do not transfer generic planetary nouns into Human Design gate-specific meanings."),
 ("HELLENISTIC-VALENS","Hellenistic practical","natal_event_timing",None,"chronocrators, lots, planetary combinations and outcomes","source_acquisition_and_critical_translation_unverified",
  "May share Babylonian/Greek/Ptolemaic lineage; apparent replication is not independent corroboration."),
 ("ARABIC-PERSIAN","Medieval Arabic/Persian","natal_and_electional",None,"profections, revolutions, firdaria, Lots, mundane/electional claims","source_discovery_only",
  "Source transmission from Hellenistic and Persian traditions means lineage dependencies must be declared."),
 ("JYOTISH-NA","Classical Jyotish","natal_trait_event_timing",None,"natural abilities, family, timing, yogas, dashas","five_source_reader_sampled_but_no_approved_mapping",
  "Different ayanamsha, dasha system and source conditionals; cannot reuse HD questionnaire trait labels without exact supporting passage."),
 ("CHINESE-ZIWEI","Zi Wei Dou Shu","natal_palace_family_career_events",None,"career, parental relationship, siblings, property, illness narratives","online_volume_II_house_source_text_documented_not_human_pred",
  "Specific historical conditional sayings have multiple modifiers, and health/death/class claims are not medical or ethical advice."),
 ("CHINESE-BAZI","BaZi / Four Pillars","natal_trait_event_timing",None,"useful factor, strength, future luck-cycle events and occupation claims","online_Di_Tian_Sui_through_ch24_plus_synthetic_calendar_parity",
  "Real birth place/time boundary policies not closed; synthetic solar-term disagreements require explicit abstention."),
 ("TIBETAN-KALACAKRA","Tibetan calendar and astrology","birth_year_elemental_time",None,"elemental astrology, calendar, lifecycle and divination claims","scholarly_and_translation_sources_sampled_in_separate_reader",
  "Tibetan calendar rules and Mo divination may be different input questions; don't reframe as one personality type."),
 ("MAYA-CODEX","Ancient Maya codices","calendar_astronomical_and_electional",None,"Venus/eclipse/almanac/ritual dates","original_facsimiles_identified_but_no_passage_level_ingest",
  "No ancient stable natal-personality hypothesis may be inferred solely from astronomy or a 260-day count."),
 ("MAYA-CONTEMPORARY-KICHE","Contemporary K'iche' Chol Q'ij","living_daykeeper_interpretation",None,"nawal/day-sign and life/ritual advice, if explicitly documented by living tradition","institutional_and_Tedlock_ethnography_identified_not_read",
  "Must preserve language, community, 13 coefficient, 20 sign and daykeeper context; avoid inventing generic birth personalities."),
 ("MODERN-DREAMSPELL","Modern Dreamspell","modern_esoteric_day_code",None,"modernized Kin label and claimed personal attributes, if declared","modern_separate_lineage_not_ingested",
  "Never label a 20th-century system as an ancient Maya source, nor mix its traits into old codices."),
 ("MESOAMERICAN-NAHUA","Mexica/Nahua tonalpohualli","ritual_day_birth_fate",None,"birth-day augury and auspicious dates","authentic_Florentine_codex_book4_discovery_only",
  "Similar 260-day astronomical frequency to Maya; different source/culture, not independent uncorrelated replication."),
 ("MESOPOTAMIAN","Babylonian horoscopy","natal_omen_or_mundane",None,"ancient personal charts and separate royal/celestial omens","secondary_research_book_discovery_only",
  "Collective royal omens differ from natal behavioral prediction; historic causal and biographical claims need independent evidence."),
 ("HD-RELATIONSHIP","Human Design partnership","partner_joint_outcomes",None,"affection/safety/chemistry vs transition, dynamic concordance","existing_separate_relationship_questionnaire_but_no_human_validation",
  "Separate relationship outcomes from natal profile score; not a new source for unrelated birth-chart systems.")
]

def main():
    src=json.loads(BASE.read_text(encoding="utf-8"))
    existing={r["id"]:r for r in src["domains"]}
    if len(existing)!=6:
        raise ValueError("Survey-v2 normative domains changed: refresh crosswalk")
    rows=[]
    for domain_id,dom in existing.items():
        rows.append({
          "id":"HD-EXISTING-"+domain_id,
          "tradition":"Human Design",
          "input_kind":"natal_chart",
          "claimed_output_kind":"recurring_observable_behavior",
          "existing_Human_Design_survey_v2_domain_id":domain_id,
          "existing_chart_feature_key":dom["chart_feature"],
          "survey_status":"EXISTING_HD_CANDIDATE_PREVALIDATION_NOT_EMPIRICALLY_CONFIRMED",
          "source_claim_verification_state":"HD_source_evidence_protocol_normative; primary author original citation must be tracked per mapping",
          "calendar_engine_status":"existing HD astronomy implementation with versioned policy, full compliance run not attested here",
          "cross_tradition_claim_equivalence":False,
          "ready_for_new_cross_tradition_blind_pred":False,
          "real_human_predictive_validations":0,
          "source_evidence_reference":"reference/core/survey_v2_behavioral_domains.json"
        })
    for ident,trad,kind,current,construct,source_state,caution in DECLARED_OTHER:
        rows.append({
          "id":ident,"tradition":trad,"input_kind":kind,
          "claimed_output_kind":construct,
          "existing_Human_Design_survey_v2_domain_id":current,
          "survey_status":"NO_SOURCE_BOUNDED_CROSS_TRADITION_OBSERVABLE_FROZEN",
          "source_claim_verification_state":source_state,
          "calendar_engine_status":"NOT_CERTIFIED_FOR_THIS_TRADITION_INPUT",
          "cross_tradition_claim_equivalence":False,
          "proposed_next_rule":"Find an exact versioned source claim and qualify input/time/output, then design candidate-blind item under existing measurement/evidence protections",
          "critical_source_limit":caution,
          "ready_for_new_cross_tradition_blind_pred":False,
          "real_human_predictive_validations":0
        })
    dependencies=[
      {"family":["Hellenistic practical","Ptolemaic/Western","Medieval Arabic/Persian","Western Lilly"],
       "reason":"Transmission and development among Greek, Persian/Arabic and early modern Western texts; claims may share ancestry rather than independently corroborate."},
      {"family":["Ancient Maya codices","Contemporary K'iche' Chol Q'ij","Mexica/Nahua tonalpohualli"],
       "reason":"Related 260-day structures but region, authorship, continuous daykeeper practice and zodiac/ritual meanings must not be merged."},
      {"family":["Classical Jyotish","Tibetan calendar and astrology"],
       "reason":"Historical Buddhist and Indian calendrical/astrological transmissions, possibly shared source mathematics and interpretation."},
      {"family":["Human Design","Ptolemaic/Western","Classical Jyotish"],
       "reason":"Human Design reuses zodiac/planetary and other symbolic terms; overlapping input or vocabulary is not distinct empirical evidence."},
      {"family":["Zi Wei Dou Shu","BaZi / Four Pillars"],
       "reason":"Separate Chinese methods may share historical time/calendar inputs and seasonal conventions; exact agreement can share the same birth-calendar mistake."}
    ]
    doc={
      "schema":"ASTRO_MULTITRADITION_CLAIM_TO_OBSERVABLE_CROSSWALK_V1",
      "as_of":"2026-10-22",
      "authority":"research_mapping_discovery_only_not_scoring_or_human_seal",
      "existing_Human_Design_Survey_v2_status":src["status"],
      "existing_Human_Design_domain_ids":list(existing),
      "mapping_rule":"Only source-original narrow claim with exactly specified chart predicate, calculation/uncertainty, named observable and frozen scoring may become a later test candidate.",
      "group_legend":"Do not merge old document annotations, synthetic chart mechanics, previous known human development, untouched natal forward/reverse results, partner relationship and electional/ritual divination.",
      "dependency_and_shared_provenance_families":dependencies,
      "crosswalk":rows,
      "cross_tradition_hypotheses_active_in_runtime":0,
      "validated_human_blind_predictions":0
    }
    (B/"TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("HD norm domains",len(existing),"new candidate/unresolved domains",len(DECLARED_OTHER),"crosswalk rows",len(rows))

if __name__=="__main__":
    main()
