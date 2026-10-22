"""B58 source-critical transfer/negative case diagnostics for BPHS29.

No natal data, inferred criminality, medical predictions, participants or scoring.
Always marks derived rules as dependent upon their source family, not a new hit.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Transfer:
    rule_id: str
    source_reference: str
    destination_reference: str
    source_house: int | None
    destination_house: int | None
    inherited_claim_family: str
    exclusions: tuple[str, ...]


SOURCE_TRANSFERS = {
    'BPHS29.22': Transfer('BPHS29.22', 'ARUDHA', 'ARUDHA', 12, 11,
                           'SAME_UPSTREAM_PLANETARY_CONFIGURATION_WITH_RELABELED_GAIN', ()),
    'BPHS29.27': Transfer('BPHS29.27', 'ARUDHA', 'ARUDHA', 7, 2,
                           'SAME_SEVENTH_HOUSE_CONDITION_IN_SECOND', ()),
    'BPHS29.29': Transfer('BPHS29.29', 'ARUDHA', 'KARAKAMSHA', None, None,
                           'ARUDHA_YOGA_APPLIED_TO_KARAKAMSHA', ('RELATIVES_OR_BANDHAVA',)),
    'BPHS29.35': Transfer('BPHS29.35', 'ARUDHA_A1_A7', 'ARUDHA_A1_A5_ETC', None, None,
                           'FRIENDSHIP_AND_GAIN_RELATION_EXTENDED_TO_OTHER_PADAS', ()),
}


def transferred_condition(*, parent_rule_id: str, original_house: int | None,
                           synthetic: bool = False) -> dict[str, object]:
    if not synthetic: raise ValueError('Synthetic rule placeholders only')
    if parent_rule_id not in SOURCE_TRANSFERS:raise ValueError('Only documented transfer instructions accepted')
    transfer=SOURCE_TRANSFERS[parent_rule_id]
    if transfer.source_house is not None and original_house!=transfer.source_house:
        raise ValueError('Source rule must use specified original relative house')
    if transfer.source_house is None and original_house is not None:
        raise ValueError('Sign-wide rule has no implied source house')
    return {
        'source_id':parent_rule_id, 'parent_claim_family':transfer.inherited_claim_family,
        'origin_frame':transfer.source_reference,
        'derived_frame':transfer.destination_reference,
        'origin_relative_house':transfer.source_house,
        'derived_relative_house':transfer.destination_house,
        'exclusions':transfer.exclusions,
        'independently_evidenced_prediction':False,
        'separate_score_credit':False,'canonical_target':None,'score_allowed':False
    }


def economic_source_kind(kind: str, *, synthetic: bool=False) -> dict[str, object]:
    if not synthetic:raise ValueError('Synthetic classification only')
    kinds={
      'PROFIT_VOLUME':('AMOUNT_OR_THRESHOLD',False),
      'EXPENDITURE_AMOUNT':('AMOUNT_OR_THRESHOLD',False),
      'PROFIT_METHOD_MORAL':('MORAL_HISTORICAL_EXCLUDED',True),
      'EXPENDITURE_CAUSE':('DATED_CAUSE_SOURCE',False),
      'STATUS_HONOR':('VERIFIED_ROLE_STATUS',False),
      'RELATIONSHIP_HARMONY':('SELF_REPORT_OR_BEHAVIOR',False),
    }
    if kind not in kinds:raise ValueError('Unrecognized original source claim family')
    observable,excluded=kinds[kind]
    return {'family':kind,'observational_domain':observable,'ethically_excluded':excluded,
            'calibrated':False,'score_allowed':False}


def relationship_a7_position(relative_house: int, *, synthetic: bool = False) -> dict[str,object]:
    if not synthetic or not isinstance(relative_house,int) or isinstance(relative_house,bool) or not 1<=relative_house<=12:
        raise ValueError('Require synthetic inclusive sign house 1..12')
    favored={1,4,5,7,9,10}
    adverse={6,8,12}
    if relative_house in favored:outcome='FRIENDSHIP_CLAIM_SOURCE_ONLY'
    elif relative_house in adverse:outcome='ENMITY_CLAIM_SOURCE_ONLY'
    else:outcome='NO_BINARY_29_34_CLAIM'
    return {'relative_house':relative_house,'claim':outcome,'observational_validation':False,
            'canonical_source_version':None,'score_allowed':False}


def social_king_claim(relative_house: int, *, synthetic: bool=False) -> dict[str,object]:
    if not synthetic or not isinstance(relative_house,int) or isinstance(relative_house,bool) or not 1<=relative_house<=12:
        raise ValueError('Require synthetic inclusive house 1..12')
    # BPHS29.36 names mutually angular, 3rd/11th, and trinal as rulership alternatives;
    # no strength or independent political status prediction is frozen.
    declared={1,3,4,5,7,9,10,11}
    return {'relative_house':relative_house,'29_36_rulership_antecedent':relative_house in declared,
            'independent_of_29_34_friendship_claim':False,
            'modern_rulership_translation_calibrated':False,'score_allowed':False}


def mixed_means_result(planet_classes: tuple[str, ...], *, synthetic: bool=False) -> dict[str,object]:
    if not synthetic:raise ValueError('Synthetic historical source classification only')
    if not planet_classes or set(planet_classes)-{'BENEFIC','MALEFIC'}:
        raise ValueError('Only documented benefic/malefic labels')
    unique=set(planet_classes)
    reading='MIXED' if len(unique)==2 else ('BENEFIC_ONLY' if 'BENEFIC' in unique else 'MALEFIC_ONLY')
    return {'source_moral_category':reading,'multiple_independent_outcome_counts':0,
            'person_specific_inference_allowed':False,'score_allowed':False}
