#!/usr/bin/env python3
"""Cross-tradition source-map structural tests; do NOT infer predictive validity."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def load(name:str)->dict:
    return json.loads((HERE/name).read_text(encoding="utf-8"))


class SourceMapIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.family=load("TRADITION_COVERAGE_V1.json")
        cls.biblio=load("MAYA_SOURCE_CATALOG_V1.json")
        cls.first=load("MAYA_FIRST_SOURCE_WITNESS_V1.json")

    def test_all_three_mermaid_maps_exist_and_are_referenced(self):
        index=(HERE/"README.md").read_text(encoding="utf-8")
        for map_name in ("WORKFLOW.mmd","SOURCE_TO_TEST_GATES.mmd","TRADITION_DEPENDENCIES.mmd"):
            with self.subTest(map=map_name):
                self.assertTrue((HERE/map_name).is_file())
                self.assertIn(map_name,index)
        self.assertEqual(index.count("&#x200b;"),0)
        self.assertGreaterEqual(index.count("```mermaid"),2)

    def test_mermaid_graph_nodes_and_arrows_resolve(self):
        for map_name in ("WORKFLOW.mmd","SOURCE_TO_TEST_GATES.mmd","TRADITION_DEPENDENCIES.mmd"):
            with self.subTest(map=map_name):
                data=(HERE/map_name).read_text(encoding="utf-8")
                self.assertTrue(data.startswith("flowchart "))
                declared=set(re.findall(r"(?m)^\s*([A-Z][A-Z0-9_]*)\s*(?:\[|\{)",data))
                self.assertGreaterEqual(len(declared),7)
                self.assertIn(">",data)
                for line in data.splitlines()[1:]:
                    if "-->" not in line and ".->" not in line:
                        continue
                    no_labels=re.sub(r'\"[^\"]*\"',"",line)
                    ids=set(re.findall(r"\b[A-Z][A-Z0-9_]*\b",no_labels))
                    self.assertFalse(ids-declared,f"{map_name} undefined node {ids-declared} in {line}")

    def test_inventory_covers_16_distinct_classes(self):
        inventory=self.family["traditional_systems"]
        self.assertEqual(len(inventory),16)
        ids=[x["id"] for x in inventory]
        self.assertEqual(len(set(ids)),len(ids))
        for x in inventory:
            self.assertEqual(x["human_validation"],0)
            self.assertNotIn("real_human_prediction_count",x)
            self.assertIsInstance(x["state"],str)

    def test_lineage_edges_are_inside_declared_inventory(self):
        ids={s["id"] for s in self.family["traditional_systems"]}
        self.assertGreaterEqual(len(self.family["documented_cross_source_links_not_confirmation"]),9)
        for edge in self.family["documented_cross_source_links_not_confirmation"]:
            self.assertIn(edge["from"],ids)
            self.assertIn(edge["to"],ids)
            self.assertNotEqual(edge["from"],edge["to"])
        self.assertTrue(self.family["project_empirical_state"]["source_annotations_not_real_people"])

    def test_maya_bibliography_has_11_direct_institutional_or_labeled_links(self):
        docs=self.biblio["reading_queue"]
        self.assertEqual(len(docs),11)
        self.assertEqual(len({d["id"] for d in docs}),11)
        for doc in docs:
            self.assertTrue(doc["url"].startswith("https://"))
            self.assertIn(doc["priority"],(1,2,3))
            self.assertTrue(doc["source_quality"] if "source_quality" in doc else doc["cautions"])
        self.assertFalse(self.biblio["completed_full_books"])
        self.assertEqual(self.biblio["real_human_blind_prediction_validations"],0)

    def test_20_traditional_day_name_pairs_are_unique(self):
        items=self.first["day_name_crosswalk_only"]
        self.assertEqual(len(items),20)
        self.assertEqual(len({d["kiche"] for d in items}),20)
        self.assertEqual(len({d["yucatec"] for d in items}),20)
        self.assertEqual([x["index_within_published_table"] for x in items],list(range(20)))
        self.assertEqual(Counter(x["source_pdf_page_one_based"] for x in items),Counter({1:4,2:8,3:8}))
        self.assertFalse(self.first["actual_calculation_engine_verified"])

    def test_page_bound_and_quarantined_candidate_claims(self):
        claims=self.first["observed_primary_claims_development_only"]
        self.assertEqual(len(claims),7)
        self.assertEqual(len({x["id"] for x in claims}),7)
        pairs=set(x["kiche"].casefold() for x in self.first["day_name_crosswalk_only"])
        for c in claims:
            self.assertIn(c["page"],(1,2,3))
            self.assertNotEqual(c["status"],"VALIDATED")
            self.assertGreater(len(c["confounds"]),0)
            self.assertGreater(len(c["eligibility"]),5)
            self.assertIn(c["name"].split(" / ")[0].casefold(),pairs)
        self.assertEqual(self.first["real_human_blind_validations"],0)

    def test_only_date_not_private_birth_in_reference_converter(self):
        src=(HERE/"maya_calendar_reference.py").read_text(encoding="utf-8")
        self.assertIn("type(civil_day) is not date",src)
        self.assertIn("eligible_to_score_a_human",src)
        self.assertIn("personality_or_fate_prediction_validated",src)
        self.assertNotIn("submit_answers",src)

    def test_cross_tradition_pointer_from_existing_HD_architecture(self):
        arch=(ROOT/"ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("docs/astrology-research-map/README.md",arch)
        self.assertIn("Human Design-specific",arch)

    def test_source_coverage_status_is_not_human_prediction_success(self):
        for record in self.family["traditional_systems"]:
            self.assertEqual(record["human_validation"],0)
        self.assertEqual(self.biblio["original_source_annotation_records_admitted_to_merged_model"],0)
        self.assertFalse(self.first["actual_calculation_engine_verified"])

    def test_claim_trace_schema_requires_all_scientific_stages(self):
        schema=load("CLAIM_TRACE_SCHEMA_V1.json")
        self.assertEqual(schema["$schema"],"https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        required=set(schema["required"])
        self.assertEqual(required,{
            "claim_id","tradition_id","source_witness","prediction_class",
            "chart_feature","observable","dependencies","readiness","human_evidence",
        })
        for key in required:
            self.assertIn(key,schema["properties"])
        self.assertIn("unimplemented",
                      schema["properties"]["chart_feature"]["properties"]["uncertainty_state"]["enum"])
        self.assertIn("source_only",
                      schema["properties"]["readiness"]["properties"]["stage"]["enum"])
        self.assertIn("untouched_human_test",
                      schema["properties"]["readiness"]["properties"]["stage"]["enum"])

    def test_source_only_Maya_example_is_unfrozen_and_unscored(self):
        schema=load("CLAIM_TRACE_SCHEMA_V1.json")
        example=load("CLAIM_TRACE_EXAMPLE_MAYA_E_V1.json")
        self.assertEqual(set(example),set(schema["required"]))
        for key,prop in schema["properties"].items():
            if key in example and prop.get("type")=="object":
                self.assertTrue(set(prop["required"]).issubset(example[key]))
                self.assertTrue(set(example[key]).issubset(prop["properties"]))
        self.assertEqual(example["claim_id"],"MAYA-CAND-001")
        self.assertEqual(example["tradition_id"],"MAYA-LIVING")
        self.assertEqual(example["source_witness"]["source_id"],"MAYA-S01")
        self.assertEqual(example["readiness"]["stage"],"source_only")
        self.assertFalse(example["readiness"]["frozen_before_outcomes"])
        self.assertEqual(example["chart_feature"]["uncertainty_state"],"unimplemented")
        self.assertEqual(example["human_evidence"]["untouched_test_participants"],0)
        self.assertEqual(example["human_evidence"]["validated_predictive_successes"],0)
        self.assertEqual(example["human_evidence"]["effect_size_status"],"unmeasured")

if __name__=="__main__":
    unittest.main()
