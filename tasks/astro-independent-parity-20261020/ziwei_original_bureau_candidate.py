#!/usr/bin/env python3
"""Strict source-only Zi Wei/Tian Fu candidate GIVEN bureau and lunar day.

Five transmitted bureau diagrams (Wikisource oldid1963110) are partially
internally inconsistent. A successful lookup means only that ONE visible day
numeral maps to ONE printed palace in this frozen text; it does not validate
birth-year NaYin->bureau, original ancient woodblock edition, natal 14-star
calculation, human outcomes, or a celestial mechanism. Failure is preserved.
"""
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass,asdict
from pathlib import Path
from ziwei_bureau_day_grid_decode import build_result
from ziwei_tianfu_relative import tianfu_from_ziwei,source_witness

BUREAUS={'水二局':2,'木三局':3,'金四局':4,'土五局':5,'火六局':6}

@dataclass(frozen=True)
class LiteralPlacement:
    source_transmitted_bureau: str
    supplied_lunar_day: int
    source_literal_status: str
    literal_ziwei_branch_if_single_source_label: str | None
    derived_tianfu_branch_if_single_ziwei_label: str | None
    printed_duplicate_ziwei_candidate_branches: tuple[str,...]
    source_original_full_document_revision: int
    excerpt_SHA256: str
    first_original_Ming_print_verified: bool
    independent_natal_calendar_or_bureau_calculation_verified: bool
    independently_confirmed_ziwei_14_star_birthday_chart: bool
    actual_person_predictions_validated: int


def candidate_given_bureau_day(bureau: str, lunar_day: int) -> LiteralPlacement:
    if bureau not in BUREAUS:
        raise ValueError('Unknown source elemental bureau, input one of exact names '+', '.join(BUREAUS))
    if isinstance(lunar_day,bool) or not isinstance(lunar_day,int) or not 1<=lunar_day<=30:
        raise ValueError('Lunar day must be integer 1..30 without coercion')
    source=build_result();w=source_witness()
    row=next(x for x in source['source_original_diagrams_decoded_with_explicit_anomalies'] if x['original_source_bureau']==bureau)
    dup=tuple(row['duplicate_original_day_assignments'].get(str(lunar_day),[]))
    if dup:
        status='AMBIGUOUS_SOURCE_DUPLICATE'
        ziwei=None;tianfu=None
    elif str(lunar_day) not in row['day_to_palace_only_when_single_original_label']:
        status='UNRESOLVED_SOURCE_MISSING_DAY'
        ziwei=None;tianfu=None
    else:
        status='SINGLE_TRANSMITTED_SOURCE_LABEL_NOT_VALIDATED_BIRTH_CHART'
        ziwei=row['day_to_palace_only_when_single_original_label'][str(lunar_day)]
        tianfu=tianfu_from_ziwei(ziwei)
    return LiteralPlacement(bureau,lunar_day,status,ziwei,tianfu,dup,
      source['source_Chinese_Wikisource_oldid'],w['original_Chinese_excerpt_sha256'],False,False,False,0)


def sample_source_decisions()->dict:
    rows=[]
    for bureau in BUREAUS:
        for lunar_day in range(1,31):
            rows.append(asdict(candidate_given_bureau_day(bureau,lunar_day)))
    from collections import Counter
    counter=Counter(row['source_literal_status'] for row in rows)
    return {'schema':'ZIWEI_FIVE_BUREAUS_150_DAY_SOURCE_CONDITIONAL_CANDIDATES_V1',
      'original_full_text_oldid':1963110,
      'source_limited_to':'Chinese Wikisource transmitted five bureau-day grids, NOT independently authenticated Ming woodblock and no complete birth calendar or star engine',
      'possible_bureau_count':5,'lunar_days_per_bureau_checked':30,
      'source_lookup_decisions':150,
      'status_counts':dict(sorted(counter.items())),
      'original_source_reading_errors_not_auto_corrected':True,
      'original_Ming_print_verified':False,
      'birth_year_and_life_palace_to_elemental_bureau_verified':False,
      'independent_14_star_chart_parity_verified':False,
      'actual_person_predictions_validated':0,'runtime_promotions':0,
      'all_150_source_conditional_lookup_records':rows}


def main():
    p=Path(__file__).resolve().parent/'ZIWEI_SOURCE_CONDITIONAL_150_DAY_PLACEMENTS_20261020.json'
    obj=sample_source_decisions();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'total':obj['source_lookup_decisions'],'status_counts':obj['status_counts'],'model_promoted':False},indent=2))
if __name__=='__main__':main()
