"""Non-production symbolic diagnostics for Bhasin/Sanskrit career and income variants.

Requires synthetic-only inputs. No astrology predictions, participant profiles,
biography, profession or economic outcomes are inspected or scored.
"""
from __future__ import annotations
from typing import Literal

Modes = Literal["MOVABLE", "FIXED", "DUAL"]


def bhasin_11_malefic_collision(*, has_malefic_in_eleventh: bool,
                                eleventh_lord_kendra_trine: bool = False,
                                synthetic: bool = False) -> dict[str, object]:
    """Two source-literal *positive/negative* antecedents, no precedence."""
    if not synthetic:
        raise ValueError("Only invented chart-sign predicates allowed")
    if not isinstance(has_malefic_in_eleventh, bool) or not isinstance(eleventh_lord_kendra_trine, bool):
        raise TypeError("Symbolic antecedents must be booleans")
    gain_verse_2 = has_malefic_in_eleventh or eleventh_lord_kendra_trine
    loss_verse_10 = has_malefic_in_eleventh
    return {"v2_gain": gain_verse_2, "v10_loss": loss_verse_10,
            "outcome_collision": gain_verse_2 and loss_verse_10,
            "canonical_precedence": None, "score_allowed": False}


def movement_hunting_8_1_29(*, navamsa_mode: Modes, rasi_mode: Modes,
                              synthetic: bool = False) -> dict[str, object]:
    if not synthetic:
        raise ValueError("Only synthetic mode inputs")
    if navamsa_mode not in ("MOVABLE", "FIXED", "DUAL") or rasi_mode not in ("MOVABLE", "FIXED", "DUAL"):
        raise ValueError("Unrecognized mode")
    # The printed Bhasin English combines movable in both categories -> hunting;
    # online Sanskrit separates movable -> movement, fixed -> fixedness, dual -> hunting.
    printed_hunting = navamsa_mode == "MOVABLE" and rasi_mode == "MOVABLE"
    english_explicit_no_hunting = navamsa_mode in ("FIXED", "DUAL")
    sanskrit_movement = navamsa_mode == "MOVABLE"
    sanskrit_stability = navamsa_mode == "FIXED"
    sanskrit_hunting = navamsa_mode == "DUAL"
    return {"printed_hunting": printed_hunting,
            "printed_explicit_no_hunting": english_explicit_no_hunting,
            "sanskrit_movement": sanskrit_movement,
            "sanskrit_stability": sanskrit_stability,
            "sanskrit_hunting": sanskrit_hunting,
            "hunting_opposition": english_explicit_no_hunting and sanskrit_hunting,
            "source_only": True, "score_allowed": False}


def wealth_exchange_2_11(*, second_lord_house: int, eleventh_lord_house: int,
                           synthetic: bool = False) -> dict[str, object]:
    if not synthetic:
        raise ValueError("Only symbolic positions allowed")
    if not all(isinstance(x, int) and not isinstance(x, bool) and 1 <= x <= 12
               for x in (second_lord_house, eleventh_lord_house)):
        raise ValueError("House numbers must be integers 1..12")
    exchange = second_lord_house == 11 and eleventh_lord_house == 2
    return {"shared_antecedent": exchange,
            "bhasin_outcome": "GENERIC_WEALTH_GAIN" if exchange else None,
            "portuguese_bphs_outcome": "WEALTH_ACCUMULATES_AFTER_MARRIAGE" if exchange else None,
            "observational_targets_equal": False,
            "score_allowed": False}


def source_selection(strengths: dict[str, int], *, synthetic: bool = False) -> dict[str, object]:
    """Toy representation of disputed strongest-only versus all-contributor routing."""
    if not synthetic:
        raise ValueError("Only synthetic ordinal strengths allowed")
    if not strengths or any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in strengths.values()):
        raise ValueError("Nonempty ordinal strengths required")
    max_strength = max(strengths.values())
    return {"strongest_planets": sorted(k for k, v in strengths.items() if v == max_strength),
            "all_contributing_planets": sorted(strengths),
            "tiebreaker_frozen": False, "source_selection_canonical": None,
            "score_allowed": False}
