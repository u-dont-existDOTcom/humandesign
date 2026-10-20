#!/usr/bin/env python3
"""Document CLXXX in original 1647 and separate 1659 printing; NOT health advice."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / 'tasks/astro-source-audit-multipass-20261005'
WEST = T / 'LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CHINA = ROOT / 'tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json'
PREV = T / 'batches/B07bb'
SOURCE_SHA = '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path, obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
west=read(WEST); china=read(CHINA); scope=read(B/'TASK_SCOPE.json'); retrieval=read(B/'SOURCE_IMAGE_1659_754_RETRIEVAL.json')
assert west['records_count']==13017 and west['batches'][-1]['id']=='B07bb'
assert west['next']['chapter']=='CLXXX' and west['next']['pdf_page']==787
assert west['source_sha256']==SOURCE_SHA and china['sum_source_annotations']==355
assert sha(CHINA)==scope['chinese_v7_sha256']
assert scope['new_first_R']=='R13018' and scope['new_accepted_records']==0
prior=read(PREV/'ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json')
folio753=prior['two_original_printings_four_page_photo_witnesses']['753']
photos={}
for edition in ('1647','1659'):
 prior_meta=folio753[edition]
 fp=ROOT/prior_meta['original_source_repo_relative_file']
 assert fp.is_file() and sha(fp)==prior_meta['sha256'] and fp.stat().st_size==prior_meta['bytes']
 photos.setdefault('753',{})[edition]={'original_source_repo_relative_file':str(fp.relative_to(ROOT)),'source_edition':int(edition),'printed_folio':753,'scan_frame':787 if edition=='1647' else 782,'sha256':sha(fp),'bytes':fp.stat().st_size,'reused_from_accepted_batch':'B07bb'}
first754=PREV/'evidence/1647_original-788.jpg'
second754=B/'evidence/1659_original_djvu_783.jpg'
assert first754.is_file() and second754.is_file()
assert sha(second754)==retrieval['thumbnail_sha256'] and second754.stat().st_size==retrieval['thumbnail_exact_bytes']
for ed,fp in [('1647',first754),('1659',second754)]:
 photos.setdefault('754',{})[ed]={'original_source_repo_relative_file':str(fp.relative_to(ROOT)),'source_edition':int(ed),'printed_folio':754,'scan_frame':788 if ed=='1647' else 783,'sha256':sha(fp),'bytes':fp.stat().st_size,'reused_from_accepted_batch':'B07bb' if ed=='1647' else None,'hosted_page_image_not_original_whole_book':ed=='1659'}
# (printed page, local semantic locator, evidential classification, SHORT 1647 literal wording, scholarly working gloss)
# The short anchors are not complete diplomatic transcriptions of sentences.
C=[
(753,'CLXXX_SIXTH_HOUSE_OPEN','CHAPTER_BOUNDARY','Sicknesse, Servants.','CLXXX begins below separate Parents divider; this is the Sixth-house merchant-case chapter, not CLXXIX.'),
(753,'SIXTH_CUSP_LIMITED_AFFLICTION','SOURCE_ASTRO_PREDICATE','the cusp of the sixt house is not afflicted','The sixth-house cusp is described as mostly unafflicted, with an exception involving ambiguous printed planetary/aspect symbols.'),
(753,'MOON_OCULUS_TAURUS_MARS','SOURCE_ASTRO_PREDICATE','with Oculus','The Moon is placed with a named Taurus eye-star and an aspect to Mars; the source symbols have not been independently computed or astronomically verified.'),
(753,'MERCURY_SIXTH_LORD_COMBUST','SOURCE_ASTRO_PREDICATE','Lord of the sixt is combust','The text treats Mercury as sixth-house lord and combust in this merchant horoscope.'),
(753,'SATURN_ASC_LORD_RETRO_FIXED','SOURCE_ASTRO_PREDICATE','Lord of the ascendant is retrograde','Saturn is taken as first-house ruler and called retrograde in a fixed sign.'),
(753,'HUMORAL_CORRUPTION_OF_BLOOD','UNVERIFIED_HISTORICAL_MEDICAL_CAUSATION','corruption of Blood','An obsolete theory of blood corruption is invoked as a cause of disease, not accepted as modern medicine.'),
(753,'VIOLENT_FEVERS_PREDICTION','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','produce violent Feavers','Lilly speculates about serious fevers in an already-known individual; no independent illness history verified.'),
(753,'MERCURY_DISEASES_P247','SOURCE_CROSS_REFERENCE','vide pag.','For further Mercury-signified illness lore the source points back to printed page 247.'),
(753,'SIXTH_SIGN_BODY_PART_PROCEDURE','SOURCE_HISTORICAL_BODY_PART_RULE','consider the Signe of the sixt','The reader is instructed to infer an afflicted member or body part from the sixth sign and its ruler; untested historical procedure.'),
(753,'SIXTH_SIGN_BODY_PART_P119','SOURCE_CROSS_REFERENCE','vide pag. 119','Further reference for the sixth-sign body-part judgment is printed page 119.'),
(753,'ASCENDANT_MOVABLE_SIXTH_COMMON','SOURCE_ASTRO_PREDICATE','the Signe also movable','The historical interpretation compares the ascendant aspects and movable sign with the sixth-house common sign; the planetary glyphs require separate symbolic collation.'),
(753,'DISEASES_VARY_OVER_TIME','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','shall vary many times','The merchant is conjectured to experience changing disease types over time, not an observed longitudinal record.'),
(753,'ONE_DISEASE_INTO_ANOTHER','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','one Disease into another','The text elaborates the unverified forecast that one illness may yield to another.'),
(753,'SATURN_QUARTAN_COUNTERFACTUAL','UNVERIFIED_COUNTERFACTUAL_MEDICAL_CLAIM','quartan','The author states a conditional concerning Saturn as ascendant lord and the frequency of quartan agues, not a confirmed clinical prevention.'),
(753,'SQUINANCIES_SORE_THROATS','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','Squinancies or sore Throats','Squinancies and throat illnesses appear in the old prognosis; no actual medical diagnosis or outcome is corroborated.'),
(753,'MOON_TRINE_MITIGATION','SOURCE_ASTRO_PREDICATE','because the','The Moon is described as trine Sun, Venus, and Mercury and applied as a mitigating chart condition; no astronomical parity yet.'),
(753,'MERCURIAL_DISEASES_EASIER_CURE','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','be more easily evaded or cured','The text claims some Mercury-associated illnesses would be less serious or more curable; this is not clinical advice.'),
(754,'MARS_WOMEN_DANGER','UNVERIFIED_GENDERED_HISTORICAL_HEALTH_CLAIM','by Women may prove dangerous','The author speculates gender-associated danger in a Mars-connected illness condition; do not endorse or medicalize this social framing.'),
(754,'MOST_LIFE_HEALTH_FORECAST','UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS','greater part of this Native\'s life shall be in Health','The already-known merchant is expected to be healthy for much of life, with no validated observed health-course record.'),
(754,'UNFORTUNATE_DIRECTIONS_MEDICINE','HISTORICAL_PRACTICE_NOT_TREATMENT_ADVICE','unfortunate Directions carefully','The old author suggests unfavorable directions may be heeded or prevented with medicine; this is merely historical rhetoric, not evidence of efficacy or a treatment recommendation.'),
(754,'MERCURY_SERVANTS_SIGNIFICATOR','SOURCE_ASTRO_SOCIAL_PREDICATE','Servants are especially signified','Mercury is designated servant-significator in the context of the sixth house; social order and inference remain historical conventions.'),
(754,'MERCURY_LORD_OF_SIXTH','SOURCE_ASTRO_PREDICATE','generall Significator, and Lord of the sixt','The merchant example gives Mercury a second servants connection as lord of the sixth.'),
(754,'MERCURY_SATURN_NO_ASPECT','SOURCE_ASTRO_PREDICATE','hath no aspect to','The text says Mercury has no aspect to Saturn; not independently verified by a 1616 historical natal engine.'),
(754,'TRIPLICITY_SUGGESTS_SERVANT_GOOD','UNVERIFIED_SERVANT_CHARACTER_PREDICTION','being of one Triplicity','Shared triplicity is used to support a limited conjecture of beneficial behavior by servants.'),
(754,'MERCURIAN_SERVANTS_NOT_TRUSTED','UNVERIFIED_SERVANT_CHARACTER_PREDICTION','scarce find the Mercurians to be trusty','The author then predicts low reliability in Mercurian servants; no independent servants-person observations verified.'),
(754,'RED_HAIRED_SERVANTS_AVOIDANCE','HISTORICAL_PREJUDICIAL_SOCIAL_RULE_NOT_ENDORSED',"avoid red hair'd",'The old text says to avoid red-haired servants associated with Mars; this prejudicial stereotype is preserved as source history, never adopted as advice.'),
(754,'CLXXXI_MARRIAGE_NEXT_BOUNDARY','NEXT_CHAPTER_BOUNDARY','Of Marriage.','CLXXX ends above printed-page divider; the distinct seventh-house CLXXXI Of Marriage begins on printed754/PDF788 and is NOT extracted here.'),
]
start=13018
records=[]
for i,(folio,role,layer,exact,gloss) in enumerate(C):
 row=photos[str(folio)]
 records.append({'id':f'R{start+i}','record_number':start+i,'batch':'B07bc','source_span':f'B07bc-S{folio-752:03d}','original_printed_folio':folio,'original_first_edition_pdf_frame':folio+34,'original_second_edition_djvu_frame':folio+29,'original_paper_1647_sha256':row['1647']['sha256'],'independently_typeset_paper_1659_sha256':row['1659']['sha256'],'role':role,'evidence_layer':layer,'original_1647_short_verbatim_anchor_NOT_full_sentence':exact,'historical_gloss_NOT_author_quotation':gloss,'original_astrological_glyphs_full_critical_collation_complete':False,'previously_known_merchant_case':True,'actual_human_medical_or_servant_observation_independently_verified':False,'medical_diagnosis_treatment_or_social_prejudice_adopted':False,'independent_actual_person_prediction_result_validated':False,'runtime_model_promoted':False})
assert len(records)==27 and records[0]['id']=='R13018' and records[-1]['role']=='CLXXXI_MARRIAGE_NEXT_BOUNDARY'
notes={'schema':'LILLY_ORIGINAL_1647_1659_CLXXX_SICKNESSE_SERVANTS_SOURCE_V1','batch':'B07bc','source_full_original_Wellcome_1647_PDF_sha256':SOURCE_SHA,'original_photographic_witnesses':photos,'printed_original_folios':[753,754],'original_first_1647_pdf_frames':[787,788],'independently_typeset_original_1659_djvu_frames':[782,783],'source_known_merchant_historical_case':True,'historical_original_symbolic_glyph_collation_not_complete':True,'full_1659_DjVu_binary_sha256_unverified':True,'all_historical_health_and_servant_claims_unverified_by_independent_person_outcomes':True,'source_editable_gloss_separate_from_1647_exact_anchor':True,'no_1647_1659_independent_blind_prospective_test':True,'actual_human_predictive_validations':0,'runtime_promotions':0,'new_documentary_source_annotations':len(records),'first_R':records[0]['id'],'last_R':records[-1]['id'],'next_R':f'R{start+len(records)}','next_original_printed_folio':754,'next_first_1647_pdf_frame':788,'next_chapter':'CLXXXI','records':records}
save(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json',notes)
save(B/'RULES.json',{'batch':'B07bc','status':'CLXXX_HISTORICAL_SOURCE_NOT_MEDICAL_TRUTH_OR_SERVANT_VALIDATION','record_count':len(records),'first_record':records[0]['id'],'last_record':records[-1]['id'],'source_printed_folios':[753,754],'physical_CLXXX_source_covered':True,'actual_human_predictive_validations':0,'runtime_model_promotions':0,'rules':records})
accept={'batch':'B07bc','Lilly_before':13017,'Ptolemy_retained':1066,'Chinese_V7_retained':355,'new_historical_source_only_notes':len(records),'Lilly_after_if_accepted':13017+len(records),'Western_after_if_accepted':13017+len(records)+1066,'first_R':records[0]['id'],'last_R':records[-1]['id'],'next_R':notes['next_R'],'next_original_pdf_frame':788,'next_printed_folio':754,'next_chapter':'CLXXXI','new_original_1647_CLXXX_physical_source_covered':True,'critical_original_astrological_glyph_collation_complete':False,'clinical_truth_or_independent_merchant_illnesses_verified':False,'human_servant_observations_validated':False,'independent_real_person_predictions_validated':0,'runtime_promotions':0,'source_notes_sha256':sha(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json'),'rules_sha256':sha(B/'RULES.json'),'Chinese_V7_index_sha256':sha(CHINA)}
save(B/'ACCEPTANCE.json',accept)
print(json.dumps({'status':'SOURCE_DRAFT_ONLY','notes':len(records),'first':records[0]['id'],'last':records[-1]['id'],'next':notes['next_R'],'western_if_accepted':accept['Western_after_if_accepted'],'original_pages_with_separate_edition_photos':len(photos),'source_notes_sha256':accept['source_notes_sha256']},indent=2))
