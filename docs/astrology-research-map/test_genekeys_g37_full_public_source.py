"""G37 64 publicly accessible Gene Keys pages, exceptions, claim boundaries.

Offline tests verify *saved* direct publisher-page readings and wheel
consistency. Tests are NOT a live page crawl, proprietary text collation,
gene-function proof, real-person prediction or official profile parity.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib,json
from pathlib import Path
import unittest

from genekeys_g35_source_crosswalk import (
    wheel_programming_partner, RAVE_GATE_ORDER, digest
)
from genekeys_g37_public_source_catalog import (
    SOURCE_ANCHORS, OTHER_ILLUSTRATIVE_SOURCE_SCOPE, build
)

HERE=Path(__file__).resolve().parent
DATA=HERE/"GENEKEYS_G37_OFFICIAL_64_PUBLIC_CATALOG_V1.json"
PREVIOUS=HERE/"GENEKEYS_G36_PRIMARY_INTERPRETIVE_AND_PROFILE_ACCESS_AUDIT_V1.json"


class TestG37CompletePublicSourceLedger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(DATA.read_text(encoding="utf8"))
        cls.rows=cls.d["rows"]
        cls.by={r["key"]:r for r in cls.rows}
        cls.previous=json.loads(PREVIOUS.read_text(encoding="utf8"))

    def test_exact_64_unique_official_pages_and_three_short_labels_each(self):
        self.assertEqual(len(self.rows),64)
        self.assertEqual(list(self.by),list(range(1,65)))
        for i,r in self.by.items():
            self.assertEqual(r["official_url"],f"https://genekeys.com/gene-key-{i}/")
            self.assertTrue(all(r[x].strip()
                      for x in ("shadow","gift","siddhi")))
            self.assertEqual(len(r["page_html_sha256"]),64)
            self.assertEqual(len(r["page_quote_sha256"]),64)
            self.assertTrue(r["long_public_quote_NOT_stored"])
            self.assertGreater(r["short_public_preview_quote_length_chars"],65)

    def test_registry_hash_and_no_unexplained_source_mutations(self):
        b={k:v for k,v in self.d.items() if k!="canonical_registry_sha256"}
        self.assertEqual(self.d["canonical_registry_sha256"],digest(b))
        self.assertEqual(len(self.d["canonical_registry_sha256"]),64)
        self.assertTrue(self.d["raw_public_page_readings_private_temporary_not_committed"])
        self.assertTrue(self.d["each_quote_checked_against_original_publisher_public_page"])
        self.assertFalse(self.d["full_book_primary_chapters_read"])

    def test_official_links_all_64_and_explicit_two_nonreciprocal_exceptions(self):
        self.assertEqual(self.d["official_published_programming_partner_links_checked"],64)
        self.assertEqual(self.d["publisher_links_matching_opposite_wheel"],62)
        self.assertEqual(self.d["publisher_links_disagreeing"],2)
        self.assertEqual([x["key"] for x in self.d["site_partner_discrepancies"]],[6,8])
        self.assertEqual(
            {(x["key"],x["official_published_partner"],
              x["canonical_wheel_partner"]) for x in self.d["site_partner_discrepancies"]},
            {(6,2,36),(8,8,14)}
        )
        self.assertTrue(all(x["reciprocal_page_explicitly_names_original_key"]
                            for x in self.d["site_partner_discrepancies"]))

    def test_exact_recipient_pages_disprove_source_navigation_errors(self):
        self.assertEqual(self.by[36]["published_programming_partner"],6)
        self.assertEqual(self.by[14]["published_programming_partner"],8)
        self.assertEqual(self.by[2]["published_programming_partner"],1)
        self.assertEqual(self.by[1]["published_programming_partner"],2)
        self.assertEqual(self.by[6]["published_programming_partner"],2)
        self.assertEqual(self.by[8]["published_programming_partner"],8)
        self.assertNotEqual(self.by[6]["published_programming_partner"],
                            wheel_programming_partner(6))
        self.assertNotEqual(self.by[8]["published_programming_partner"],
                            wheel_programming_partner(8))

    def test_all_other_62_match_existing_opposition_without_rewriting_engine(self):
        self.assertEqual(len(RAVE_GATE_ORDER),64)
        mismatches=[]
        for r in self.rows:
            mate=wheel_programming_partner(r["key"])
            self.assertEqual(r["canonical_mandala_programming_partner"],mate)
            if r["published_programming_partner"]!=mate:
                mismatches.append(r["key"])
        self.assertEqual(mismatches,[6,8])
        self.assertEqual(
            len({tuple(sorted((n,wheel_programming_partner(n))))
                 for n in range(1,65)}),32)

    def test_source_matches_former_seven_independently_read_G36_pages(self):
        old=self.previous["source_sampled_7_keys"]
        self.assertEqual([x["number"] for x in old],[5,28,32,50,54,55,64])
        for item in old:
            key=item["number"];now=self.by[key]
            self.assertEqual(
                (now["shadow"],now["gift"],now["siddhi"]),
                (item["shadow"],item["gift"],item["siddhi"]))
            self.assertEqual(now["published_programming_partner"],
                             item["official_programming_partner"])

    def test_source_quote_claim_examples_are_exact_short_original_anchors(self):
        c=self.d["source_conditional_language_cases_selected_for_later_analysis"]
        self.assertEqual([x["key"] for x in c],[4,7,27,61])
        self.assertEqual([x["brief_exact_anchor"] for x in c],
                         [SOURCE_ANCHORS[x["key"]]["anchor"] for x in c])
        self.assertTrue(all(x["source_url"]==self.by[x["key"]]["official_url"]
                            for x in c))
        self.assertTrue(all(len(x["source_preview_quote_sha256"])==64 for x in c))
        self.assertTrue(all(x["frozen_behavioral_prediction_or_threshold"] is False
                            for x in c))

    def test_natal_conditions_and_ambiguous_qualifiers_not_overstated(self):
        c={x["key"]:x for x in self.d["source_conditional_language_cases_selected_for_later_analysis"]}
        self.assertEqual(c[4]["source_class"],"PROFILE_CONDITIONAL_FUTURE_DEVELOPMENT")
        self.assertIn("prominence threshold",c[4]["source_nonliteral_missing"])
        self.assertEqual(c[7]["source_class"],"GENE_KEY_ATTRIBUTE_WITHOUT_EXPLICIT_NATAL_PLACEMENT")
        self.assertIn("whether",c[7]["source_nonliteral_missing"])
        self.assertEqual(c[27]["source_class"],"HAVE_OR_FEEL_DRAWN_DISJUNCTION")
        self.assertIn("does not state natal condition is necessary",
                      c[27]["source_nonliteral_missing"])
        self.assertEqual(c[61]["source_class"],"HAVE_KEY_WITHOUT_SPHERE_OR_TIME_WINDOW")
        self.assertIn("which sphere",c[61]["source_nonliteral_missing"])

    def test_gift_or_contemplation_disjunctions_not_natal_claims(self):
        old=self.d["other_contemplation_or_Gift_conditional_examples"]
        self.assertEqual([x["key"] for x in old],[11,49])
        self.assertEqual({x["key"]:x["literal_short_source_anchor"] for x in old},
                         OTHER_ILLUSTRATIVE_SOURCE_SCOPE)
        for x in old:
            self.assertIn("not equivalent",x["scope"])

    def test_quote_keyword_counts_declared_as_heuristics_not_semantics(self):
        self.assertEqual(self.d["short_quote_heuristic_if_or_when_count"],20)
        self.assertEqual(self.d["short_quote_heuristic_mentions_profile_count"],1)
        self.assertTrue(self.d["heuristic_text_flags_are_NOT_a_complete_semantic_study"])
        self.assertEqual(sum(x["quote_mentions_profile_heuristic"] for x in self.rows),1)
        self.assertTrue(self.by[4]["quote_mentions_profile_heuristic"])

    def test_no_full_copyrighted_public_paragraph_or_paid_book_in_registry(self):
        self.assertFalse(self.d["full_book_primary_chapters_read"])
        self.assertIn("no full Richard Rudd",self.d["copyright_policy"])
        for r in self.rows:
            self.assertNotIn("public_rudd_quote",r)
            self.assertNotIn("full_chapter",r)
            self.assertEqual(set(("shadow","gift","siddhi"))-r.keys(),set())

    def test_exact_publisher_page_not_secret_profiler_or_live_person(self):
        self.assertFalse(self.d["official_completed_profile_calculator_parity_verified"])
        self.assertEqual(self.d["independent_natal_chart_evidence_beyond_Human_Design"],0)
        self.assertFalse(self.d["source_behavioral_trait_model_frozen"])
        self.assertEqual(self.d["human_predictive_validations"],0)
        self.assertFalse(self.d["production_chart_or_scoring_modified"])

    def test_pages_are_publicly_sourced_not_diagnostics_from_birth_answers(self):
        self.assertEqual(self.d["source"],"64 separate public pages on genekeys.com, n=1..64")
        self.assertEqual(self.d["as_of"],"2026-10-25")
        self.assertTrue(self.d["all_64_headings_checked"])
        for r in self.rows:
            self.assertTrue(r["no_behavioral_prediction_derived_automatically"])
            self.assertTrue(r["page_html_sha256"])

    def test_published_partner_error_cannot_be_repair_by_posthoc_claim(self):
        # Schematic synthetic mutation of the public registry cannot
        # mutate the canonical wheel or create statistical evidence.
        changed=deepcopy(self.d)
        changed["rows"][5]["published_programming_partner"]=36
        self.assertNotEqual(changed["rows"][5]["published_programming_partner"],
                            self.by[6]["published_programming_partner"])
        self.assertEqual(wheel_programming_partner(6),36)
        self.assertEqual(wheel_programming_partner(8),14)
        self.assertEqual(changed["human_predictive_validations"],0)


if __name__=="__main__":
    unittest.main()
