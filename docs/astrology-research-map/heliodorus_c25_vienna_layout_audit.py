"""C25 official Austrian National Library Greek commentary layout audit.

Compare observed numbering, *not* planetary rulers, across Vienna A and
Florence commentary. A 15+15 model is an explicit tentative layout
interpretation and not a source transcription of unobserved planets,
nor evidence of human behavioral prediction.
"""
import json
from pathlib import Path

from paulus_c24_complete_240_source_comparison import complete_provisional_240

WITNESS=Path(__file__).with_name("HELIODORUS_C25_VIENNA_A_F205V_SOURCE_LAYOUT_V1.json")


def vienna_source():
    return json.loads(WITNESS.read_text(encoding="utf-8"))


def inspected_degree_number_pairs():
    """Exactly observed candidate numeral examples; do not extrapolate glyphs."""
    return vienna_source()["table_literal_visual_observations"]["observed_degree_pair_examples_provisional"]


def bounded_layout_reconciliation():
    a=vienna_source()
    rows=inspected_degree_number_pairs()
    pairs=[(r["row"],r["left_number"],r["right_number"]) for r in rows]
    C24=complete_provisional_240()
    observed_num_correct=sum(1 for x,y,z in pairs if x==y and z==x+15)
    return {
        "source_type":"VIENNA_MANUSCRIPT_DIRECT_PHOTOGRAPH_LAYOUT_ONLY",
        "Vienna_folio":a["primary_original_manuscript"]["located_folio"],
        "vienna_source_photo_size_px":a["primary_original_manuscript"]["actual_study_image_dimensions"],
        "observed_degree_pairs":pairs,
        "degree_pair_examples_passing_15_offset_diagnostic":observed_num_correct,
        "numbered_row_layout_hypothesis":"15_NUMBERED_ROWS_WITH_TWO_DEGREE_NUMBER_COLUMNS",
        "source_complete_30x4_planetary_cells_transcribed":False,
        "physical_num_pair_observations_used":len(pairs),
        "Vienna_num_pair_semantics_proved":False,
        "Vienna_has_day_night_pairs_proved":False,
        "later_Florence_24h_double_planet_slots":C24["provisional_first_slot_glyphs"]+C24["provisional_second_slot_glyphs"],
        "later_Florence_paired_photo_transcriptions_blinded":False,
        "older_Florence_and_Vienna_are_same_day_night_scheme_proved":False,
        "C24_source_numbers_overwritten":False,
        "C05_P_Oxy_matches_retained":a["comparison_controls"]["earlier_C05_P_Oxy4277_comparisons_unchanged"]["matches"],
        "human_predictive_validations":0,
        "scoring_rule_promoted":False
    }


if __name__=="__main__":
    print(json.dumps(bounded_layout_reconciliation(),ensure_ascii=False,indent=2))
