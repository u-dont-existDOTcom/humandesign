#!/usr/bin/env python3
"""Opt-in modern edited-print NaYin reading, preserving original oldid errors.

DO NOT silently replace the original transmitted Wikisource evidence with
the edited print. A second published reproduction can help diagnose likely
textual corruption, but this is NOT a verified Ming original woodblock, full
traditional natal calculation, or person-level prediction evidence.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from ziwei_nayin_bureau_source import (
    STEMS_ROMAN, BRANCHES_ROMAN, PHASE_TO_BUREAU,
    conditional_source_bureau, read_source_poem,
)

HERE=Path(__file__).resolve().parent
SECONDARY=HERE/'SECONDARY_MODERN_EDITED_NAYIN_WITNESS_20261020.json'
PERMITTED_POLICIES=('strict_oldid1963110','explicit_later_edited_print_candidate')

def secondary_witness_checked():
    obj=json.loads(SECONDARY.read_text(encoding='utf-8'))
    if obj['schema']!='ZIWEI_NAYIN_EDITED_MODERN_PRINT_SECONDARY_VARIANT_WITNESS_V1':
        raise ValueError('Modern edited-print witness schema changed')
    if len(obj['readings'])!=2 or obj['PDF_viewer_page_1_based']!=80 or obj['secondary_modern_book_printed_folio']!=66:
        raise ValueError('Edited source page/reading index changed')
    primary=read_source_poem()
    for r in obj['readings']:
        a=primary[r['poem_pair_ordinal']-1]
        if a['original_written_stem_branch_pair']!=r['primary_oldid1963110_exact_pair']:
            raise ValueError('Original frozen oldid line now differs from witness manifest')
        if a['cycle_expected_stem_branch_pair_NOT_original']!=r['secondary_edited_print_visually_read_pair']:
            raise ValueError('Edited reading contradicts computed sexagenary cycle; do not auto-repair')
        if a['source_Chinese_element']!=r['nayin_element']:
            raise ValueError('Printed glyph fixes change element category')
        file=HERE/'evidence'/Path(r['bounded_secondary_excerpt_repo_relative']).name
        if not file.is_file() or file.stat().st_size!=r['excerpt_png_bytes'] or hashlib.sha256(file.read_bytes()).hexdigest()!=r['excerpt_png_sha256']:
            raise ValueError('Photographic excerpt missing or byte-mismatched')
    assert obj['independent_expert_manuscript_diplomatic_collation_complete'] is False
    return obj

def source_bureau_with_explicit_edition_policy(yearstem:str,life:str,*,edition_policy:str='strict_oldid1963110'):
    if edition_policy not in PERMITTED_POLICIES:
        raise ValueError('Explicit original-vs-later-edited edition policy required')
    src=conditional_source_bureau(yearstem,life)
    row={
      'yearstem_input':yearstem,
      'life_palace_branch_input':life,
      'edition_policy_requested':edition_policy,
      'primary_oldid_original_label':src.original_chinese_pair_as_printed,
      'derived_exact_sexagenary_name':src.derived_source_palace_sexagenary_name,
      'original_primary_source_strict_valid':src.original_source_glyph_permitted_for_queried_natal_pillar,
      'primary_original_non_emended_bureau':src.source_conditional_bureau_Chinese,
      'effective_bureau_candidate_under_requested_source_policy':src.source_conditional_bureau_Chinese,
      'evidence_status':src.original_literal_status,
      'correction_applied_from_secondary':False,
      'secondary_evidence_PDF_first_source_page':None,
      'secondary_source_photo_SHA256':None,
      'source_original_early_edition_authenticated':False,
      'individual_natal_chart_or_human_prediction_validated':False,
      'runtime_model_promoted':False
    }
    if src.source_conditional_bureau_Chinese is not None or edition_policy=='strict_oldid1963110':
        return row
    witness=secondary_witness_checked()
    matches=[r for r in witness['readings'] if r['poem_pair_ordinal']==src.original_nayin_source_poem_pair_ordinal]
    if len(matches)!=1:
        raise ValueError('No unique modern alternate witness for malformed old source glyph')
    entry=matches[0]
    assert src.derived_cycle_name_if_source_were_emended_not_adopted is not None
    assert src.derived_cycle_name_if_source_were_emended_not_adopted in entry['secondary_complete_four_char_pair']
    assert src.original_source_glyph_permitted_for_queried_natal_pillar is False
    elem=entry['nayin_element']
    row['effective_bureau_candidate_under_requested_source_policy']=PHASE_TO_BUREAU[elem]
    row['evidence_status']='MODERN_EDITED_SECONDARY_TEXT_SUPPORTS_EMENDATION_NOT_EARLY_ORIGINAL'
    row['correction_applied_from_secondary']=True
    row['secondary_evidence_PDF_first_source_page']=witness['PDF_viewer_page_1_based']
    row['secondary_source_photo_SHA256']=entry['excerpt_png_sha256']
    return row

def compare_120_modes():
    records=[]
    for year in STEMS_ROMAN:
        for branch in BRANCHES_ROMAN:
            strict=source_bureau_with_explicit_edition_policy(year,branch)
            edited=source_bureau_with_explicit_edition_policy(year,branch,edition_policy='explicit_later_edited_print_candidate')
            records.append({'yearstem':year,'life_branch':branch,'original_primary_strict':strict,'secondary_modern_edited_opt_in':edited})
    changed=[x for x in records if x['secondary_modern_edited_opt_in']['correction_applied_from_secondary']]
    return {'schema':'ZIWEI_ORIGINAL_NAYIN_STRICT_VS_SECONDARY_EDITED_OPTIONAL_RECONSTRUCTION_V1',
      'secondary_source_manifest_SHA256':hashlib.sha256(SECONDARY.read_bytes()).hexdigest(),
      'original_pinned_text_and_secondary_editing_kept_separate':True,
      'original_reading_stays_default':True,
      'result_scope':'Source arithmetic only for given life palace/year stem; source edition is an explicit gate, no future chart prediction allowed',
      'all_120_year_stem_life_branch_cases_evaluated':120,
      'primary_strict_source_bureau_valid_cases':116,
      'secondary_modern_edited_source_alternate_candidates':4,
      'secondary_changes_four_only':[{'yearstem':x['yearstem'],'life_branch':x['life_branch'],'secondary_bureau':x['secondary_modern_edited_opt_in']['effective_bureau_candidate_under_requested_source_policy']} for x in changed],
      'unresolved_early_Ming_text_authority_cases':4,
      'provisional_correction_does_not_upgrade_orig_authenticity':True,
      'independent_real_human_predictions_validated':0,
      'runtime_astrological_promotions':0,
      'per_candidate_original_vs_second_edition_results':records}

def main():
    obj=compare_120_modes()
    p=HERE/'ZIWEI_SOURCE_STRICT_VS_MODERN_EDITION_120_CANDIDATES_20261020.json'
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':120,'strict_primary_exact':obj['primary_strict_source_bureau_valid_cases'],
      'later_edited_opt_in':obj['secondary_modern_edited_source_alternate_candidates'],
      'changed_four':obj['secondary_changes_four_only'],
      'original_Ming_print_authenticated':False},ensure_ascii=False,indent=2))
if __name__=='__main__':
    main()
