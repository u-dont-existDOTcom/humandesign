#!/usr/bin/env python3
"""Build research-only ranked Maya sources and missing-tradition triage.

These are source DISCOVERY records, not annotations, translated book excerpts,
verified ancient natal rules, person outcomes or software-engine validations.
"""
from __future__ import annotations
import json
from pathlib import Path

B=Path(__file__).resolve().parent

MAYA=[
("MAYA-01",1,"Dresden Maya Codex","original_codex","Maya scribal transmission; German SLUB manuscript facsimile",
"https://www.slub-dresden.de/en/explore/manuscripts/the-dresden-maya-codex","free_institutional_facsimile_portal",
"Original Postclassic calendar, rituals, eclipse/Venus and other astronomical tables; compare dated almanac passages to modern scholarly readings",
"Read digital original folio images with a separate keyed pagination/citation ledger; codex images not ingested by this register."),
("MAYA-02",1,"Living Maya Time: Calendar & contemporary daykeepers","contemporary_indigenous_source","Smithsonian National Museum of the American Indian / living Maya participants",
"https://maya.nmai.si.edu/calendar","museum_page_discovered_but_automation_received_HTTP_403",
"Distinguish actual contemporary K’iche’ Chol Q’ij divination and living traditional calendar practice from modern pseudo-Mayan systems",
"Educational museum page and calendar converter; does not stand in for a formal ethnographic source or a tested individual birth-fate rule."),
("MAYA-03",1,"Time and the Highland Maya (revised ed., 1992)","ethnography","Barbara Tedlock; University of New Mexico Press",
"https://www.unmpress.com/9780826313584/time-and-the-highland-maya/","publisher_book_purchase_or_library",
"Highest priority book for K’iche’ contemporary daykeeper interpretive methods, ethnographic social/ritual context and calendrical divination",
"Book not acquired/read in this track; contemporary K’iche’ is not identical to every ancient Classic Maya system."),
("MAYA-04",2,"Maya Calendar and Mesoamerican Astronomy","scholarly_review","Gerardo Aldana; Encyclopedia of the History of Science",
"https://ethos.lps.library.cmu.edu/article/id/520/","free_scholarly_article",
"Decipherment cautions, origins of calendar astronomy, 260-day count, reinterpretations of supposed astronomical text",
"Use historical context and source criticism, not blanket validation of natal fate claims."),
("MAYA-05",2,"The Madrid Codex: New Approaches to Understanding an Ancient Maya Manuscript","scholarly_book","Gabrielle Vail and Anthony F. Aveni (eds); University Press of Colorado, 2004 (updated paperback 2009)",
"https://upcolorado.com/university-press-of-colorado/the-madrid-codex","publisher_book_purchase_with_free_chapter_extract",
"Technical edition and interpretation of original Maya almanacs/ritual dates, Tzolk’in tables, context and links to broader Mesoamerican sources",
"Book not ingested. The edited interpretation is separate from the manuscript original; no individual personality rule assumed."),
("MAYA-06",2,"Astronomy in the Maya Codices","scholarly_book","Harvey M. Bricker and Victoria R. Bricker; American Philosophical Society (2011)",
"https://www.pennpress.org/9780871692658/astronomy-in-the-maya-codices/","publisher_book_purchase_or_library",
"Most important detailed academic codex astronomical and calendar-mechanics comparison, especially Venus, Mercury, eclipse/Mars and dates",
"Large specialist reference, not a pre-verified reading of every code page; astronomy precision does not equal natal behavioral predictive accuracy."),
("MAYA-07",2,"Skywatchers: A Revised and Updated Version of Skywatchers of Ancient Mexico","scholarly_book","Anthony F. Aveni; University of Texas Press (2001)",
"https://utpress.utexas.edu/9780292705029/","publisher_book_purchase_or_library",
"Broader independent Mesoamerican archaeoastronomy and sky/calendar measurement context for selecting testable calculation claims",
"Regional synthesis rather than a codex itself or a single Maya natal divination rulebook."),
("MAYA-08",3,"Maya Calendar Origins: Monuments, Mythistory, and the Materialization of Time","historical_hypothesis_book","Prudence M. Rice; University of Texas Press (2007)",
"https://utpress.utexas.edu/9780292716926/","publisher_book_purchase_or_library",
"History of the 260-day/365-day calendars and their political/cosmological origins",
"Rice's origin scenario is a research hypothesis, not an established earliest historical account or human astrology validation."),
("MAYA-09",2,"Other surviving original Maya codices (Madrid, Paris, Maya Codex of Mexico)","original_codex","Institutional owner/catalog summary: SLUB Dresden cross-codex inventory",
"https://www.slub-dresden.de/en/explore/manuscripts/the-dresden-maya-codex/other-maya-codices","free_institutional_original_codex_catalog",
"Separate original Maya Madrid almanacs, Paris K'atun calendar/zodiac, and Mexico Venus manuscript for comparison against Dresden",
"Catalog page, not an independent facsimile download. Read individual original manuscript reproductions before rule extraction."),
("MAYA-10",3,"The Maya Calendar System","museum_educational_reference","Smithsonian National Museum of the American Indian (Living Maya Time)",
"https://maya.nmai.si.edu/sites/default/files/resources/The%20Maya%20Calendar%20System.pdf","free_museum_pdf",
"Names 20 Tzolk’in/Chol Q’ij signs, 13 coefficients, 365-day Haab, regional K’iche’/Yucatec vocabulary",
"Educational handout rather than a primary source in which every day-name is a personality prognosis."),
("MAYA-11",4,"Popol Vuh: The Mayan Book of the Dawn of Life","indigenous_cosmology_translation","Dennis Tedlock (trans., revised ed. 1996); Smithsonian bibliographic record",
"https://www.si.edu/object/popol-vuh-mayan-book-dawn-life-translated-dennis-tedlock-commentary-based-ancient-knowledge-modern%3Asiris_sil_724998","publisher_or_library",
"K’iche’ cosmology, historical/ritual symbolism and texts about cosmic order",
"Important context, NOT a direct natal horoscopy manual; don't infer birth-sign meanings."),
("MAYA-12",3,"Cycles of Time and Meaning in the Mexican Books of Fate","neighboring_culture_comparator","Elizabeth Hill Boone (2007); University of Texas Press",
"https://utpress.utexas.edu/9780292712638/","publisher_book_purchase_or_library",
"Explicit contrasting Mexica/Nahua and allied Mesoamerican divinatory codices and birth-fate almanacs; related 260-day count but distinct culture",
"Cross-Mesoamerican comparator, NOT an ancient Maya daykeeper source; keep tradition IDs independent.")
]

MAYA.extend([
("MAYA-13",1,"Calendrical Calculations: The Ultimate Edition; Mayan calendar chapter and source algorithms","calendar_engine_reference","Edward M. Reingold and Nachum Dershowitz; Cambridge University Press (2018)",
"https://reingold.co/calendars.shtml","book_publisher_and_free_author_algorithm_papers",
"Established independent Gregorian/Julian/Long Count/Haab/Tzolk'in computational reference and code, as an alternative to building a new converter",
"Correlation, day epoch conventions and living K’iche’ daykeeping continuity still require source declarations; an accurate converter is not a personality predictor."),
("MAYA-14",1,"Maya Long Count conversion: configurable correlation constant","calendar_converter_control","FAMSI Research Mesoamerican Calendrics",
"https://research.famsi.org/date_mayaLC.php","free_public_converter",
"Independent reference lookup with explicitly configurable GMT 584283 versus other Long Count correlations; golden calculations for an eventual Maya calendar engine",
"Do not ingest dynamically displayed today's date as a timeless fixture; specific input/output pairs must be recorded and verified."),
("MAYA-15",2,"Maya/Mesoamerican original codices facsimile index","original_manuscript_facsimile_portal","Foundation for the Advancement of Mesoamerican Studies (FAMSI)",
"https://www.famsi.org/mayawriting/codices/","free_facsimiIes_and_codex_context",
"Additional facsimile access and manuscript/codex lineage cross-comparison rather than reliance on one edited online codex text",
"Facsimile images and scholarly interpretive commentary are distinct evidence records; no raw original folio was read during this discovery.")
])

OTHER=[
("ASTRO-HELLENISTIC",1,"Hellenistic practical natal techniques","high","Vettius Valens, Anthologies; Dorotheus of Sidon, Carmen Astrologicum","https://www.skyscript.co.uk/valens_riley.html",
"Source differences from Ptolemy/Lilly matter for timing, chronocrators, technique and independent original-rule maps. Riley translation is openly posted but incomplete; Dorotheus survives through Arabic mediation.",
"research_planned_no_complete_critical_sources_in_current_research"),
("ASTRO-ISLAMIC-PERSIAN",1,"Medieval Arabic/Persian astrological synthesis","high","Abu Ma'shar Great Introduction; al-Biruni Book of Instruction; al-Qabisi","https://old-digitalcollections.nypl.org/collections/the-book-of-instruction-in-the-elements-of-the-art-of-astrology?filters%5Btopic%5D%5B%5D=Science%2C+Medieval&filters%5Btype%5D=text&keywords=",
"Independent bridges between classical Greek/Indian/Arabic medieval methods and later Lilly; historical original Arabic/Persian and translation lineages, lots, profections, elections and annual revolutions.",
"research_planned_translation_critical_review_required"),
("ASTRO-MESOAMERICAN-NAHUA",2,"Mexica/Nahua tonalpohualli day-sign fate almanacs","medium_high","Florentine Codex Book IV; Codex Borgia; Elizabeth Hill Boone","https://www.getty.edu/projects/florentine-codex/",
"Related 260-day divination but separate from Maya, with direct historical birth-day prognostic material; cross-cultural comparison should avoid treating it as a second independent unrelated clock.",
"research_planned_day_count_related_to_maya"),
("ASTRO-MESOPOTAMIAN",2,"Babylonian horoscopy and omen astronomy","medium_high","Francesca Rochberg The Heavenly Writing; documented Babylonian horoscope tablets","https://www.cambridge.org/core/books/the-heavenly-writing/9A24735C23CA63EF8E1819B283B39F47",
"Historical precursor; separates personal horoscopes and royal/collective omen claims; important transmission but perhaps lower marginal behavioral signal than missing original Hellenistic natal texts.",
"research_planned_source_language_and_outcome_limits"),
("ASTRO-CHINESE-QIMEN",3,"Qi Men Dun Jia question-time/electional and other Chinese divination","medium","Early and later printed Chinese Qi Men Dun Jia methods, version/era critical editions required",None,
"Method/phenotype space distinct from Zi Wei and BaZi, but often question- or date-of-action divination rather than birth-derived stable personality.",
"discovery_only_do_not_falsely_call_another_natal_system"),
("ASTRO-SOUTHEAST-ASIA",4,"Burmese, Thai and related weekday natal astrology","exploratory","Documented Mahabote and weekday birth traditions, identify authoritative local-language sources first",None,
"Potential independent coarse weekday/pattern structures, but culture-specific source provenance and calendar alignment must be researched before scoring.",
"exploratory_no_pinned_source_or_engine"),
("ADJACENT-DIVINATION",4,"Ifa, geomancy and other ritual systems","outside_core_astrology","Traditional original cultural knowledge, not automatically an astronomical natal horoscope",None,
"Separate comparative divination practice only with legitimate source/cultural context; don't present as missing horoscopic astrology.",
"outside_core_or_optional")
]

def generate():
    maya=[]
    for iid,tier,title,kind,authors,url,access,use,caution in MAYA:
        maya.append({"source_id":iid,"priority_tier":tier,"title":title,
                     "source_kind":kind,"authors_or_holder":authors,"reference_url":url,
                     "access_status_at_discovery":access,"research_purpose":use,
                     "interpretation_limit":caution,
                     "original_content_ingested":False,"book_full_read_verified":False,
                     "source_to_human_observable_rules_promoted":0,
                     "empirical_human_predictive_validations":0})
    other=[]
    for iid,tier,title,importance,texts,url,purpose,state in OTHER:
        other.append({"tradition_id":iid,"priority_tier":tier,"tradition_class":title,
                      "expected_incremental_value":importance,
                      "first_reference_texts":texts,"starter_reference_url":url,
                      "reason_for_priority":purpose,"actual_state":state,
                      "source_pinned_original_rules":0,
                      "validated_real_human_prediction_results":0})
    parent={
      "schema_version":"MAYA_SOURCE_READING_PRIORITY_AND_PROVENANCE_V1",
      "as_of":"2026-10-22",
      "purpose":"Rank authoritative free primary and scholarly sources before rule extraction; not verified books already read",
      "source_prior_parent_status":"BOOK_AND_MAYAN_COVERAGE_STATUS_20261022.md",
      "not_a_uniform_historical_maya_personality_horoscope":True,
      "regional_practice_layers":[
        {"system":"MAYA-CLASSIC-POSTCLASSIC","calendar":["Tzolk'in","Haab","Calendar Round","Long Count","astronomical almanacs"],"source_basis":"Original Maya codices and securely interpreted glyph/date inscriptions","not_equivalent_to_birth_personality":True},
        {"system":"MAYA-CONTEMPORARY-KICHE","calendar":["Chol Q'ij, living 260-day daykeeper counting"],"source_basis":"Modern Indigenous K'iche' participants and independent ethnography","not_interchangeable_with_classic_maya_codex_asterisms":True},
        {"system":"MODERN-DREAMSPELL","calendar":["modern Dreamspell day/kin constructs"],"source_basis":"Twentieth-century esoteric construction, independently date/provenance required","cannot_label_ancient_maya_astrology":True}
      ],
      "original_Maya_calendar_correlation_policy":"GMT 584283 commonly used in historical reconstructions, but exact JDN convention and independently verified daykeeper continuity must be declared and tested; not selected in a chart engine by this registry.",
      "first_task":"Primary original Dresden page/facsimile and Smithsonian Indigenous education + Tedlock ethnography, then specialized Madrid and Bricker astronomy",
      "source_records":maya,
      "no_original_classic_personality_prediction_automatically_inferred":True,
      "no_emails_DOBs_or_personal_data":True,
      "real_human_blind_predictions_validated":0
    }
    nextset={"schema_version":"DISTINCT_ASTROLOGICAL_TRADITIONS_TRIAGE_V1",
             "goal":"Coverage-before-depth across independent natal, historical, electional, divinatory and cross-cultural traditions",
             "priority_not_proof_of_astrological_effect":True,
             "source_level_not_product_promotion":True,
             "traditions":other,
             "no_person_blind_predictions_in_these_new_lanes":True}
    for file,obj in (("MAYA_RANKED_SOURCE_REGISTER_V1.json",parent),
                     ("ADDITIONAL_TRADITIONS_PRIORITY_REGISTER_V1.json",nextset)):
        (B/file).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("MAYA_SOURCE_RECORDS",len(maya),"TRADITION_CLASSES",len(other))

if __name__=="__main__":
    generate()
