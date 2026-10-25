"""G39 source-blind offline rater packet and grader tests.

No volunteer source is opened. Perfect/default/unclear rating responses
are explicitly generated from the researcher key and are not empirical.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from genekeys_g39_blind_rating_packets import (
    ROOT,SHA_BANK,SHA_SOURCE,SHA_CONTRACT,
    N_RATERS,N_ITEMS,source_stimuli,generate,html_render,
    sha_bytes,digest,
)
from genekeys_g39_rate_blind_packets import (
    grade,validate_key,validate_submission,agreement,
)
from genekeys_g39_mock_rater_controls import make_mock,build

KEY=ROOT/"GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json"
MOCKS=ROOT/"GENEKEYS_G39_SYNTHETIC_RATER_GRADER_RECEIPT_V1.json"
BROWSER=ROOT/"GENEKEYS_G39_ACTUAL_BRAVE_OFFLINE_BROWSER_SMOKE_V1.json"
HTML_ROOT=ROOT/"GENEKEYS_G39_ANONYMOUS_RATER_HTML"


class TestG39BlindRaterPackets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key=validate_key(json.loads(KEY.read_text(encoding="utf8")))
        cls.mock=json.loads(MOCKS.read_text(encoding="utf8"))
        cls.browser=json.loads(BROWSER.read_text(encoding="utf8"))

    def test_parent_source_files_are_actual_accepted_exact_inputs(self):
        self.assertEqual(sha_bytes(
            (ROOT/"GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json").read_bytes()),SHA_BANK)
        self.assertEqual(sha_bytes(
            (ROOT/"GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json").read_bytes()),SHA_SOURCE)
        self.assertEqual(sha_bytes(
            (ROOT/"GENEKEYS_G38_LINE_STYLE_STUDY_CONTRACT_DRAFT_V1.json").read_bytes()),SHA_CONTRACT)
        self.assertEqual(self.key["input_source_sha256"],SHA_SOURCE)
        self.assertEqual(self.key["input_bank_sha256"],SHA_BANK)
        self.assertEqual(self.key["input_contract_sha256"],SHA_CONTRACT)

    def test_exact_24_distinct_messages_four_per_each_style(self):
        items=self.key["items"]
        self.assertEqual(len(items),24)
        self.assertEqual(len({x["item_code"] for x in items}),24)
        self.assertEqual({i:sum(x["researcher_intended_style_original_line"]==i
                                for x in items) for i in range(1,7)},
                         {i:4 for i in range(1,7)})
        self.assertEqual(len({x["source_scenario"] for x in items}),4)
        self.assertTrue(all(x["item_code"].startswith("M-") for x in items))

    def test_six_source_rater_packets_are_complete_and_different_order(self):
        self.assertEqual(self.key["n_rater_packets"],N_RATERS)
        self.assertEqual(self.key["n_items_per_rater"],N_ITEMS)
        self.assertEqual([x["packet_id"] for x in self.key["rater_packets"]],
                         ["R01","R02","R03","R04","R05","R06"])
        orders=[tuple(x["item_order"]) for x in self.key["rater_packets"]]
        self.assertEqual(len(set(orders)),6)
        for r in self.key["rater_packets"]:
            self.assertEqual(len(r["item_order"]),24)
            self.assertEqual(len(set(r["item_order"])),24)
            self.assertEqual(set(r["public_category_code_to_original_source_line"].values()),
                             set(range(1,7)))
            self.assertEqual(len(set(r["category_label_order"])),6)

    def test_all_raters_have_rotated_item_positions_not_same_position_confounds(self):
        r=self.key["rater_packets"]
        first=r[0]["item_order"]
        for i,p in enumerate(r):
            expected=first[4*i:]+first[:4*i]
            self.assertEqual(p["item_order"],expected)
        for key in first:
            positions=[x["item_order"].index(key) for x in r]
            self.assertEqual(len(set(positions)),6)

    def test_rater_html_contains_no_key_or_expected_answers(self):
        dangerous=("source_line","researcher_intended_style_original_line",
                   "Gene Keys","Human Design","target_line",
                   "target_category","@@","<script src=",
                   "https://","http://")
        for info in self.key["rater_packets"]:
            html=(HTML_ROOT/info["rater_html_basename"]).read_text(encoding="utf8")
            self.assertEqual(sha_bytes(html.encode()),info["rater_html_sha256"])
            for term in dangerous:
                with self.subTest(rater=info["packet_id"],term=term):
                    self.assertNotIn(term,html)
            self.assertIn("This page runs locally",html)
            self.assertIn("None / unclear",html)
            self.assertIn("Export anonymous ratings",html)
            self.assertIn('name="naturalness"',html)
            self.assertIn('name="perceived_pressure"',html)
            self.assertNotIn("birth date",html.lower())

    def test_browser_source_has_real_interactive_submission_and_export(self):
        h=(HTML_ROOT/"G39_Anonymous_Message_Reviewer_R01.html").read_text()
        self.assertIn('form.addEventListener("submit"',h)
        self.assertIn('URL.createObjectURL(blob)',h)
        self.assertIn('document.getElementById("export").addEventListener',h)
        self.assertIn('form.reportValidity()',h)
        self.assertNotIn("localStorage",h)
        self.assertNotIn("fetch(",h)
        self.assertNotIn("navigator.sendBeacon",h)

    def test_generator_regenerates_identical_bytes_and_key(self):
        with tempfile.TemporaryDirectory() as t:
            key,files=generate(out_dir=Path(t))
            self.assertEqual(key,self.key)
            self.assertEqual(len(files),6)
            for p in files:
                original=HTML_ROOT/p.name
                self.assertEqual(p.read_bytes(),original.read_bytes())

    @unittest.skipUnless(shutil.which("node") is not None,"Node syntax checker optional")
    def test_inline_browser_javascript_parses_as_real_source_code(self):
        html=(HTML_ROOT/"G39_Anonymous_Message_Reviewer_R01.html").read_text()
        script=html.split("<script>")[-1].split("</script>")[0]
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"packet.js"
            p.write_text(script,encoding="utf8")
            result=subprocess.run(["node","--check",str(p)],
                                   capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_researcher_key_tamper_rejected_even_if_label_is_changed(self):
        x=deepcopy(self.key)
        x["items"][0]["researcher_intended_style_original_line"]=6
        with self.assertRaises(ValueError):
            validate_key(x,check_html=False)

    def test_browser_html_hash_tamper_rejected_via_key_immutable_source(self):
        x=deepcopy(self.key)
        x["rater_packets"][0]["rater_html_sha256"]="0"*64
        x["research_key_body_sha256"]=digest({
            k:v for k,v in x.items() if k!="research_key_body_sha256"
        })
        with self.assertRaises(ValueError):
            validate_key(x)

    def test_perfect_synthetic_answers_produce_144_of_144_by_construction(self):
        responses=make_mock(self.key,mode="perfect")
        result=grade(self.key,responses,
                     all_submissions_are_SYNTHETIC_FIXTURES=True)
        self.assertEqual(result["number_of_response_packets"],6)
        self.assertEqual(result["ratings_total"],144)
        self.assertEqual(result["correct_style_classifications"],144)
        self.assertEqual(result["coverage_adjusted_accuracy_all_ratings"],1)
        self.assertEqual(result["unsure_classifications"],0)
        self.assertEqual(result["mean_naturalness_all"],3)
        self.assertEqual(result["mean_perceived_pressure_all"],2)
        self.assertTrue(result["submissions_marked_synthetic_fixtures"])
        self.assertEqual(len(result["inter_rater_pairwise_agreement_descriptive"]),15)
        self.assertTrue(all(x["Cohen_kappa_descriptive"]==1
                            for x in result["inter_rater_pairwise_agreement_descriptive"]))

    def test_uniform_one_category_synthetic_baseline_exact_sixth(self):
        r=grade(self.key,make_mock(self.key,mode="all_line_1"),
                all_submissions_are_SYNTHETIC_FIXTURES=True)
        self.assertEqual(r["correct_style_classifications"],24)
        self.assertEqual(r["ratings_total"],144)
        self.assertEqual(r["coverage_adjusted_accuracy_all_ratings"],1/6)
        self.assertEqual(r["balanced_six_style_independence_baseline"],1/6)
        self.assertTrue(all(x["Cohen_kappa_descriptive"] is None
                            for x in r["inter_rater_pairwise_agreement_descriptive"]))

    def test_all_uncertain_synthetic_fixture_preserves_abstentions(self):
        r=grade(self.key,make_mock(self.key,mode="all_unclear"),
                all_submissions_are_SYNTHETIC_FIXTURES=True)
        self.assertEqual((r["correct_style_classifications"],
                          r["unsure_classifications"]),(0,144))
        self.assertEqual(r["coverage_adjusted_accuracy_all_ratings"],0)
        self.assertIsNone(r["conditional_accuracy_if_classified"])

    def test_three_synthetic_control_results_saved_and_rebuild(self):
        self.assertEqual(build(),self.mock)
        self.assertEqual(
            [(x,self.mock["cases"][x]["correct"]) for x in ("perfect","all_line_1","all_unclear")],
            [("perfect",144),("all_line_1",24),("all_unclear",0)]
        )
        self.assertEqual(self.mock["independent_raters_tested"],0)
        self.assertTrue(self.mock["all_cases_constructed_from_researcher_answer_key_not_real_raters"])

    def test_missing_or_duplicate_rating_not_accepted(self):
        p=make_mock(self.key,mode="perfect")[0]
        a=deepcopy(p);a["ratings"].pop()
        with self.assertRaises(ValueError):
            validate_submission(self.key,a)
        b=deepcopy(p);b["ratings"][-1]=b["ratings"][0]
        with self.assertRaises(ValueError):
            validate_submission(self.key,b)

    def test_invalid_category_confidence_and_fact_values_rejected(self):
        orig=make_mock(self.key,mode="perfect")[0]
        for field,val in [
            ("category_code","NOT_A_CATEGORY"),
            ("confidence",True),
            ("confidence",0),
            ("confidence","1"),
            ("facts_check","maybe")]:
            p=deepcopy(orig)
            p["ratings"][0][field]=val
            with self.subTest(field=field,val=val),self.assertRaises(ValueError):
                validate_submission(self.key,p)

    def test_unknown_rater_packet_or_duplicate_rater_bundle_rejected(self):
        responses=make_mock(self.key,mode="perfect")
        bad=deepcopy(responses[0]);bad["packet_id"]="R11"
        with self.assertRaises(ValueError):
            validate_submission(self.key,bad)
        with self.assertRaises(ValueError):
            grade(self.key,[responses[0],responses[0]],
                  all_submissions_are_SYNTHETIC_FIXTURES=True)

    def test_fake_personal_biography_or_nonfiction_claim_rejected(self):
        responses=make_mock(self.key,mode="perfect")
        bad=deepcopy(responses[0]);bad["respondent_bio_data_collected"]=True
        with self.assertRaises(ValueError):
            grade(self.key,[bad])
        bad=deepcopy(responses[0]);bad["synthetic_messages_only"]=False
        with self.assertRaises(ValueError):
            grade(self.key,[bad])

    def test_distribution_bundle_separates_qualifying_reviewers_from_research_key(self):
        from genekeys_g39_deliver_separated_packages import (
            rater_members,researcher_members)
        rater=rater_members();research=researcher_members()
        self.assertEqual(len(rater),7)
        self.assertEqual(len(research),25)
        self.assertIn("README_FOR_RATERS.txt",rater)
        self.assertFalse(any("RESEARCHER_ONLY_ITEM_KEY" in name for name in rater))
        self.assertTrue(any("RESEARCHER_ONLY_ITEM_KEY" in name for name in research))
        self.assertTrue(all(b"Gene Keys" not in data for data in rater.values()))

    def test_owner_zip_delivery_receipt_does_not_embed_private_home_path(self):
        from genekeys_g39_deliver_separated_packages import (
            MANIFEST,DOWNLOAD_DIR)
        m=json.loads(MANIFEST.read_text(encoding="utf8"))
        self.assertTrue(m["reviewer_packet_contains_no_source_key"])
        self.assertTrue(m["no_rater_forms_sent_to_people"])
        self.assertTrue(m["absolute_private_owner_home_directory_not_recorded"])
        self.assertEqual(m["rater_archive"]["member_count"],7)
        self.assertEqual(m["researcher_archive"]["member_count"],25)
        for a in (m["rater_archive"],m["researcher_archive"]):
            self.assertEqual(len(a["sha256"]),64)
            destination=DOWNLOAD_DIR/a["zip_basename"]
            if destination.is_file():
                self.assertEqual(sha_bytes(destination.read_bytes()),a["sha256"])

    def test_not_any_consent_or_independent_human_result(self):
        self.assertTrue(self.key["no_genuine_independent_rater_answers_collected"])
        self.assertTrue(self.key["no_human_natal_predictions"])
        self.assertEqual(self.mock["human_astrology_predicted_outcomes"],0)
        self.assertEqual(self.browser["independent_user_raters_recruited"],0)

    def test_two_actual_Brave_offline_SMOKES_not_raters(self):
        b=self.browser
        self.assertTrue(b["local_anonymous_browser_export_actually_clicked"])
        self.assertEqual([x["rater_packet"] for x in b["two_browser_tested_packets"]],["R01","R04"])
        self.assertEqual([x["completed_items"] for x in b["two_browser_tested_packets"]],[24,24])
        self.assertTrue(all(x["exported_JSON_valid"] and x["initial_incomplete_form_blocked"]
                            and x["simulated_clicks_only"] for x in b["two_browser_tested_packets"]))
        self.assertEqual(b["actual_brave_exported_synthetic_ratings_total"],48)
        self.assertEqual(b["actual_browser_fake_correct_source_style_classifications"],8)
        self.assertEqual(b["fake_browser_mean_naturalness"],3)
        self.assertEqual(b["fake_browser_mean_perceived_pressure"],2)

    def test_objective_wording_audit_preserves_all_eight_literal_category_cues(self):
        from genekeys_g39_stimulus_preflight import build
        o=json.loads((ROOT/"GENEKEYS_G39_STIMULUS_WORDING_CONFOUND_PREFLIGHT_V1.json").read_text())
        self.assertEqual(build(),o)
        self.assertEqual(len(o["item_checks"]),24)
        self.assertTrue(o["all_three_core_event_facts_in_every_message"])
        self.assertEqual(o["per_style"]["3"]["direct_category_label_cue_instances"],4)
        self.assertEqual(o["per_style"]["5"]["direct_category_label_cue_instances"],4)
        for i in (1,2,4,6):
            self.assertEqual(o["per_style"][str(i)]["direct_category_label_cue_instances"],0)
        self.assertTrue(o["source_phrase_keyword_cue_can_inflate_easy_category_classification"])
        self.assertTrue(o["word_count_factual_realism_and_emotional_intent_still_need_independent_review"])

    def test_public_instructions_do_not_disclose_source_mapping_or_ask_private_births(self):
        public=(ROOT/"GENEKEYS_G39_PUBLIC_RATER_INSTRUCTIONS.txt").read_text().lower()
        researcher=(ROOT/"GENEKEYS_G39_RESEARCHER_GUIDE.md").read_text().lower()
        self.assertIn("do not distribute any",public)
        self.assertIn("birth date",public)
        self.assertIn("offline",public)
        self.assertNotIn("gene keys",public)
        self.assertNotIn("human design",public)
        self.assertNotIn("rudd",public)
        self.assertIn("distinct zips",researcher)
        self.assertIn("zero actual human predictive validations",researcher)
        self.assertIn("manipulation",researcher)

    def test_rater_data_need_be_graded_separately_no_real_user_DOB(self):
        b=self.browser
        self.assertTrue(b["fully_offline_no_web_upload"] is True)
        self.assertTrue(b["source_truth_not_embedded_in_packet_HTML"])
        self.assertTrue(b["real_style_perception_unmeasured"])


if __name__=="__main__":
    unittest.main()
