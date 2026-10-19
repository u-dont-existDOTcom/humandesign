"""Limited literal Di Tian Sui 04/05/07/08/11/12 source enumerations.

No natal chart inference or verified human-event prediction. The transmitted
Wikisource verses/commentaries have historically disputed author/edition
attribution and contain moralizing/fate claims requiring quarantine.
"""

from __future__ import annotations

from bazi_source_mechanics import BRANCHES

HISTORIC_WOOD_EAST_DIRECTION = ("Yin", "Mao", "Chen")
HISTORIC_WOOD_THREE_HARMONY = ("Hai", "Mao", "Wei")
OLD_TEXT_FORMATION_FAMILIES = {
    "wood_eastern_direction": HISTORIC_WOOD_EAST_DIRECTION,
    "wood_three_harmony": HISTORIC_WOOD_THREE_HARMONY,
}
SOURCE_STRENGTH_EXCEPTIONS = (
    "旺中有衰者存，不可損也。",
    "衰中有旺者存，不可益也。",
    "旺之極者不可損，以損在其中矣",
    "衰之極者不可益，以在其中矣",
    "至於所當損者而損之反凶，所當益者而益之反害",
)
SOURCE_FALSE_FOLLOWING_PARAGRAPH = "日主弱矣，財官強矣，不能不從，中有所助者，便假"
SOURCE_TRUE_FOLLOWING_CONTEXT = "日主孤弱無氣，天地人三元，絕無一毫生扶之意"


def _valid_branches(branches: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(branches, tuple):
        raise ValueError("Supply an explicit tuple of independently established branch names")
    if not all(isinstance(x, str) and x in BRANCHES for x in branches):
        raise ValueError("Unknown Earthly Branch: full Chinese calendar not implemented")
    if len(set(branches)) != len(branches):
        raise ValueError("Repeated branch is not a complete three-branch formation")
    return branches


def original_text_wood_branch_group(branches: tuple[str, ...]) -> dict[str, object]:
    """Recognize exactly named source triplets, with NO fortune-classification."""
    values = _valid_branches(branches)
    found = [
        name
        for name, group in OLD_TEXT_FORMATION_FAMILIES.items()
        if len(values) == 3 and set(values) == set(group)
    ]
    return {
        "matched_source_group": found[0] if found else None,
        "historical_source_membership_only": True,
        "full_natal_or_luck_structure_computed": False,
        "predicted_fortune_or_character": None,
    }


def original_text_formation_source_warnings() -> dict[str, object]:
    """Explicit exception clauses in the pinned text; not an inference engine."""
    return {
        "strength_exception_Chinese_quotes": SOURCE_STRENGTH_EXCEPTIONS,
        "no_universal_want_stronger_or_weaker_rule": True,
        "requires_month_calendar_and_all_four_pillars": True,
        "author_early_physical_edition_verified": False,
        "expert_original_to_English_translation_verified": False,
        "independently_blinded_real_person_accuracy_verified": False,
    }


def original_text_true_false_following_preconditions() -> dict[str, object]:
    return {
        "literal_original_true_following_condition": SOURCE_TRUE_FOLLOWING_CONTEXT,
        "literal_original_apparent_following_condition": SOURCE_FALSE_FOLLOWING_PARAGRAPH,
        "requires_total_daymaster_support_and_hidden_stems": True,
        "requires_wealth_official_source_strength": True,
        "requires_month_luck_calendar_context": True,
        "full_general_true_false_transformation_engine_verified": False,
        "no_actual_person_moral_character_deduction_permitted": True,
    }


def source_research_limits() -> dict[str, object]:
    return {
        "independent_authentic_original_early_print_verified": False,
        "pinned_online_text_edition_critically_reconciled": False,
        "source_glosses_expert_classical_chinese_translated": False,
        "birth_Gregorian_to_lunisolar_and_solar_terms_verified": False,
        "Four_Pillars_accurate_natal_engine_verified": False,
        "verified_human_character_gender_wealth_health_predictions": 0,
        "real_human_prospective_blind_predictions_validated": 0,
        "model_runtime_promotions": 0,
    }
