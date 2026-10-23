"""C16 source/interpretation boundary: Boer's 1958 editorial preface.

Three distinct photographed physical manuscripts are NOT proven three
genealogically independent sources. Boer's probable common archetype is an
EDITORIAL HYPOTHESIS, not an observed 4th-century text or a prediction test.
The edition's complete Greek diagram was not visually inspected here.
"""
from pathlib import Path
import json

from paulus_c15_three_manuscript_comparison import three_manuscript_comparison

HERE=Path(__file__).resolve().parent
REGISTRY=HERE/"PAULUS_C16_BOER_1958_PREFACE_GENEALOGY_V1.json"


def preface_record():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def source_lineage_assessment():
    r=preface_record()
    older=three_manuscript_comparison()
    counts=older["counts"]
    claims={item["id"]:item for item in r["observations"]}
    mss=claims["B1958-02"]["witnesses"]
    return {
        "analysis_class":"SOURCE_EDITING_GENEALOGY_NOT_PREDICTIVE_VALIDATION",
        "named_editor_preface_witnesses":[(x["repository"],x["shelfmark"]) for x in mss],
        "three_physical_codices_observed":counts["three_physical_manuscripts_consulted"],
        "vatican_florence_source_positions_equal":counts["vatican_florence_agree"],
        "vatican_munich_readable_positions_equal":counts["vatican_munich_agree"],
        "editorial_one_mutilated_archetype_is_hypothesis":claims["B1958-01"]["kind"]=="EDITORIAL_HYPOTHESIS",
        "editorial_conjecture_is_authenticated_textual_stemma":False,
        "independent_genealogical_manuscript_families_proven":0,
        "early_preferred_variant_by_editor":claims["B1958-03"]["siglum"],
        "another_valuable_variant_by_editor":claims["B1958-04"]["siglum"],
        "textual_witness_date_discrepancy_preserved":claims["B1958-03"]["dates_noted_in_previous_research"],
        "original_edition_table_apparatus_read":False,
        "ancient_paulus_algorithm_identified":False,
        "genuine_human_predictive_validations":0,
        "production_scorer_modified":False,
        "controls_unresolved":r["source_gaps"],
    }


if __name__=="__main__":
    print(json.dumps(source_lineage_assessment(),indent=2))
