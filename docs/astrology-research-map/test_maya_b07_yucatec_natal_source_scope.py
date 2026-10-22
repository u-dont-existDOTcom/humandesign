#!/usr/bin/env python3
"""Original Yucatec colonial natal-source evidence; NO predictive human validation."""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
import unittest
from maya_calendar_reference import YUCATEC_DAYS, KICHE_DAY_NAMES_BY_YUCATEC

ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/"MAYA_B07_YUCATEC_NATAL_SOURCE_PROVENANCE_V1.json").read_text(encoding="utf-8"))
STUDY=json.loads((ROOT/"MAYA_B07_ARTISAN_BLIND_STUDY_DRAFT_V1.json").read_text(encoding="utf-8"))
TABLE=ROOT/"MAYA_B07_YUCATEC_NATAL_20_SOURCE_DOMAIN_ROWS.txt"

def parsed_source_rows(text=None):
    if text is None:
        text=TABLE.read_text(encoding="utf-8")
    rows=[]
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts=line.split("|")
        if len(parts)!=6:
            raise ValueError("Source record needs 6 fields")
        num,historic,canonical,pdf_page,domain,status=parts
        rows.append((int(num),historic,canonical,int(pdf_page),domain,status))
    return rows

class YucatecOriginalNatalSourceScopeTests(unittest.TestCase):
    def test_exactly_twenty_canonical_Yucatec_labels(self):
        rows=parsed_source_rows()
        self.assertEqual(len(rows),20)
        self.assertEqual([r[0] for r in rows],list(range(1,21)))
        self.assertEqual(len({r[2] for r in rows}),20)
        self.assertEqual(set(r[2] for r in rows),set(YUCATEC_DAYS))
        self.assertEqual({r[2] for r in rows if r[5]=="CRAFT_CANDIDATE"},
                         {"CHUWEN","MEN","KAB’AN"})

    def test_historical_source_ordinal_Kan_is_not_highland_Kan(self):
        row=parsed_source_rows()[0]
        self.assertEqual(row[:3],(1,"Kan","K’AN"))
        mapping=dict(zip(YUCATEC_DAYS,KICHE_DAY_NAMES_BY_YUCATEC))
        self.assertEqual(mapping["K’AN"],"K’AT")
        self.assertEqual(mapping["CHIKCHAN"],"KAN")
        self.assertEqual(mapping["CHUWEN"],"B’ATZ’")
        self.assertEqual(mapping["KAB’AN"],"NO’J")

    def test_source_original_20_entries_are_separate_from_editor_interp(self):
        self.assertEqual(SOURCE["classification"]["day_count"],20)
        self.assertEqual(SOURCE["classification"]["prediction_class"],"natal_trait_attributed_to_birth_day")
        self.assertEqual(SOURCE["classification"]["original_bilingual_excerpt_pages"],[21,22,23,24])
        self.assertEqual(SOURCE["classification"]["parallel_manuscripts_pdf_pages"],[38,39,40,41])
        self.assertTrue(SOURCE["classification"]["no_verified_birth_hour_boundary"])
        self.assertIn("Editor",SOURCE["classification"]["directional_day_attributions"])

    def test_source_manuscript_lineage_is_not_5_independent_replications(self):
        a=SOURCE["separate_historic_manuscript_ancestors"]
        self.assertEqual(len(a),4)
        self.assertEqual({x["id"] for x in a},{"KAUA","CHAN_CAH","PEREZ","IXIL"})
        self.assertTrue([x for x in a if x["id"]=="KAUA"][0]["three_text_loci_not_three_independent_humans"])
        self.assertEqual(SOURCE["nonpromotion"]["historical_copy_variants_independent_phenotypic_replications"],0)

    def test_source_archival_hashes_present_but_not_public_PDFs(self):
        self.assertEqual([a["page_count"] for a in SOURCE["sources"][:2]],[325,376])
        for s in SOURCE["sources"][:2]:
            self.assertRegex(s["sha256"],r"^[a-f0-9]{64}$")
        self.assertFalse(SOURCE["provenance_security"]["source_pdfs_committed_public_repo"])
        self.assertFalse(SOURCE["provenance_security"]["source_pdfs_in_owner_zip"])

    def test_historically_moralized_attributions_quarantined(self):
        rows=parsed_source_rows()
        counts=Counter(r[5] for r in rows)
        self.assertEqual(counts,{"QUARANTINE":15,"CONTEXT_ONLY":2,"CRAFT_CANDIDATE":3})
        self.assertTrue({"IMIX’","IK’","AK’B’AL","KIMI","MULUK"}.issubset(
            {r[2] for r in rows if r[5]=="QUARANTINE"}))
        self.assertFalse({"IMIX’","KIMI"} & set(STUDY["exploratory_not_primary"]["modern_composite_day_names"]))

    def test_specific_source_variant_caban_craft_is_only_long_Kaua(self):
        x={v["modern_yucatec"]:v for v in SOURCE["source_fidelity_positive_candidates"]}
        self.assertIn("weaving",x["CHUWEN"]["artisanal_claim"])
        self.assertIn("longer Kaua",x["KAB’AN"]["evidence_strength"])
        self.assertEqual(x["MEN"]["test_eligibility"],"EXPLORATORY_ONLY")
        self.assertEqual(x["CHUWEN"]["test_eligibility"],"UNFROZEN_POTENTIAL_PRIMARY")

    def test_proposed_primary_is_single_sign_not_posthoc_best_of_three(self):
        self.assertEqual(STUDY["status"],"PRE_REGISTRATION_DRAFT_NOT_FROZEN_NOT_RUNNING")
        self.assertEqual(STUDY["primary"]["canonical_yucatec_day"],"CHUWEN")
        self.assertEqual(STUDY["exploratory_not_primary"]["modern_composite_day_names"],
                         ["CHUWEN","MEN","KAB’AN"])
        self.assertTrue(STUDY["exploratory_not_primary"]["is_investigator_generated_group_not_in_original_source"])
        self.assertTrue(STUDY["exploratory_not_primary"]["not_usable_to_rescue_failed_single_CHUWEN_result"])

    def test_group_prevalence_power_pilot_honestly_nonconfirmatory(self):
        self.assertEqual(STUDY["analysis_draft"]["mechanical_feasibility_only_minimal_pilot_n"],60)
        self.assertEqual(STUDY["analysis_draft"]["confirmatory_n_at_alpha05_80percent_power_for_standardized_d03_approx"],1836)
        self.assertEqual(STUDY["exploratory_not_primary"]["sample_size_for_d03_approx_two_sided_80power"],684)
        self.assertAlmostEqual(STUDY["exploratory_not_primary"]["estimated_prevalence_under_uniform_day_names"],.15)
        self.assertEqual(STUDY["analysis_draft"]["primary_group"].split()[0],"CHUWEN")

    def test_hidden_answers_and_birth_time_uncertainty_not_silently_resolved(self):
        self.assertFalse(STUDY["population"]["selection_status"]=="FROZEN")
        self.assertFalse(STUDY["population"]["historical_era_calendar_continuity_validated"])
        self.assertFalse(STUDY["chart_and_decoys"]["natal_chart_engine_verified_for_living_yucatec"])
        self.assertTrue(STUDY["chart_and_decoys"]["no_prediction_selected_post_outcome"])
        self.assertEqual(STUDY["primary"]["source_feature_eligible_for_scored_untouched_human"],False)

    def test_scoring_missing_and_opportunity_controls_present(self):
        q=STUDY["question_prototype"]
        self.assertEqual(len(q["response_options"]),8)
        self.assertEqual(q["predeclared_scored_bins"],list(range(6)))
        self.assertEqual(len(q["primary_nonresponse"]),2)
        self.assertIn("access",q["separate_opportunity_item"].lower())
        self.assertIn("occupation",q["separate_paid_trade_item"].lower())
        self.assertIn("nonastrology",STUDY["chart_and_decoys"]["null_models"][1])

    def test_mutated_canonical_day_name_is_rejected(self):
        rows=parsed_source_rows()
        raw=TABLE.read_text(encoding="utf-8")
        bad=raw.replace("8|Chuen|CHUWEN","8|Chuen|KAB’AN")
        mutant=parsed_source_rows(bad)
        self.assertEqual(len(mutant),20)
        self.assertNotEqual(len({r[2] for r in mutant}),20)
        self.assertNotEqual(set(r[2] for r in mutant),set(YUCATEC_DAYS))

    def test_counters_zero_despite_real_original_natal_source_read(self):
        self.assertEqual(SOURCE["nonpromotion"]["actual_untouched_human_natal_validations"],0)
        self.assertEqual(SOURCE["nonpromotion"]["rule_promotions_to_runtime"],0)
        self.assertEqual(STUDY["counters"]["frozen_questionnaire_versions"],0)
        self.assertEqual(STUDY["counters"]["scored_untouched_participants"],0)
        self.assertEqual(STUDY["counters"]["validated_human_effects"],0)

if __name__=="__main__":
    unittest.main()
