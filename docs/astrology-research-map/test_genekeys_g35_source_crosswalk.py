"""G35 official 11-sphere correlation and duplicate-evidence safeguards."""
from __future__ import annotations

import copy
from datetime import UTC,datetime
from math import isclose
from pathlib import Path
import importlib.util
import json
import unittest

from genekeys_g35_source_crosswalk import (
    CORE_11, SUPPLEMENTARY_3, CORE_SEQUENCE_ORDER,
    crosswalk_from_activations_for_synthetic_only,
    crosswalk_from_incumbent_verified_chart,
    digest, wheel_programming_partner,
)
from genekeys_g35_synthetic_profiles import SYNTHETIC_UTC
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.bodygraph import GateActivation
from hdmatch.chart.rave_mandala import RAVE_GATE_ORDER,longitude_to_gate_line

HERE=Path(__file__).resolve().parent
DATA=HERE/"GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json"
HAS_SWISS=importlib.util.find_spec("swisseph") is not None


def fake_activations(*,include_supplementary:bool=True)->list[GateActivation]:
    """Fabricated LONGITUDES, not actual DOB; exact mandala label parity."""
    specs=CORE_11+(SUPPLEMENTARY_3 if include_supplementary else ())
    lon={
      ("personality",CelestialBody.SUN):10.0,
      ("personality",CelestialBody.EARTH):190.0,
      ("design",CelestialBody.SUN):280.0,
      ("design",CelestialBody.EARTH):100.0,
      ("design",CelestialBody.MOON):93.5,
      ("personality",CelestialBody.VENUS):42.0,
      ("personality",CelestialBody.MARS):69.0,
      ("design",CelestialBody.VENUS):121.0,
      ("design",CelestialBody.MARS):245.0,
      ("design",CelestialBody.JUPITER):313.3,
      ("personality",CelestialBody.JUPITER):357.7,
      ("design",CelestialBody.URANUS):15.0,
      ("personality",CelestialBody.MERCURY):130.0,
      ("design",CelestialBody.SATURN):175.0,
    }
    keys={(s.birth_layer,s.body) for s in specs}
    out=[]
    for side,body in sorted(keys,key=lambda x:(x[0],x[1].value)):
        x=lon[(side,body)]
        gx=longitude_to_gate_line(x)
        out.append(GateActivation(body=body,side=side,longitude=x,
                                  gate=gx.gate,line=gx.line))
    return out


class TestG35GeneKeysCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot=json.loads(DATA.read_text(encoding="utf8"))

    def test_official_core_11_unique_and_three_supplementary_distinct(self):
        self.assertEqual(len(CORE_11),11)
        self.assertEqual(len(SUPPLEMENTARY_3),3)
        self.assertEqual(len({s.slug for s in CORE_11+SUPPLEMENTARY_3}),14)
        self.assertTrue(all(s.source_status=="core" for s in CORE_11))
        self.assertTrue(all(s.source_status=="extended" for s in SUPPLEMENTARY_3))

    def test_official_sphere_to_planet_map_exact(self):
        expected={
          "lifes_work":("personality","sun"),
          "evolution":("personality","earth"),
          "radiance":("design","sun"),
          "purpose":("design","earth"),
          "attraction":("design","moon"),
          "iq":("personality","venus"),
          "eq":("personality","mars"),
          "sq":("design","venus"),
          "core_vocation":("design","mars"),
          "culture":("design","jupiter"),
          "pearl":("personality","jupiter")
        }
        got={s.slug:(s.birth_layer,s.body.value) for s in CORE_11}
        self.assertEqual(got,expected)
        extras={s.slug:(s.birth_layer,s.body.value) for s in SUPPLEMENTARY_3}
        self.assertEqual(extras,{
            "creativity":("design","uranus"),
            "relating":("personality","mercury"),
            "stability":("design","saturn")
        })

    def test_sequences_reuse_spheres_not_14_independent_natal_positions(self):
        self.assertEqual(CORE_SEQUENCE_ORDER["activation"],
            ("lifes_work","evolution","radiance","purpose"))
        self.assertEqual(CORE_SEQUENCE_ORDER["venus"],
            ("purpose","attraction","iq","eq","sq","core_vocation"))
        self.assertEqual(CORE_SEQUENCE_ORDER["pearl"],
            ("core_vocation","culture","lifes_work","pearl"))
        self.assertEqual(len(set(sum(CORE_SEQUENCE_ORDER.values(),()))),11)

    def test_four_independent_solar_earth_spheres_really_two_oppositions(self):
        a=crosswalk_from_activations_for_synthetic_only(fake_activations())
        x={s["slug"]:s for s in a["spheres"]}
        self.assertEqual(a["core_sphere_count"],11)
        self.assertEqual(a["supplementary_sphere_count"],0)
        for lhs,rhs in (("lifes_work","evolution"),("radiance","purpose")):
            self.assertEqual(x[lhs]["line"],x[rhs]["line"])
            self.assertEqual(wheel_programming_partner(
                x[lhs]["gate_gene_key_number"]),x[rhs]["gate_gene_key_number"])
        self.assertTrue(a["two_sun_earth_oppositions_not_four_independent_factors"])

    def test_all_wheel_32_programming_partner_pairs_symmetric(self):
        for key in range(1,65):
            partner=wheel_programming_partner(key)
            self.assertNotEqual(key,partner)
            self.assertEqual(wheel_programming_partner(partner),key)
            i=RAVE_GATE_ORDER.index(key)
            self.assertEqual(RAVE_GATE_ORDER[(i+32)%64],partner)
        self.assertEqual(wheel_programming_partner(7),13)

    def test_boolean_and_out_of_range_not_accepted_as_gene_keys(self):
        for invalid in (True,False,0,65,-1,1.0,"1"):
            with self.subTest(gate=repr(invalid)),self.assertRaises(ValueError):
                wheel_programming_partner(invalid)

    def test_sphere_output_equals_existing_human_design_gates(self):
        rows=fake_activations()
        cross=crosswalk_from_activations_for_synthetic_only(rows,
                                                     include_supplementary=True)
        existing={(row.side,row.body.value):(row.gate,row.line)
                  for row in rows}
        self.assertEqual(len(cross["spheres"]),14)
        for x in cross["spheres"]:
            self.assertEqual((x["gate_gene_key_number"],x["line"]),
                             existing[(x["planetary_layer"],x["body"])])
        self.assertTrue(cross["same_64_wheel_and_longitudes_as_existing_Human_Design"])
        self.assertEqual(cross["independent_astrological_evidence_count"],0)

    def test_no_shadow_gift_siddhi_strings_extracted_as_predictions(self):
        data=crosswalk_from_activations_for_synthetic_only(fake_activations())
        self.assertTrue(data["shadow_gift_siddhi_labels_are_contemplative_not_measured_frequencies"])
        self.assertFalse(data["gk_copyrighted_full_key_descriptions_copied"])
        self.assertEqual(data["human_predictions_made"],0)
        self.assertEqual(data["human_validation_results"],0)
        for sphere in data["spheres"]:
            self.assertNotIn("shadow_description",sphere)
            self.assertNotIn("gift_description",sphere)
            self.assertNotIn("siddhi_description",sphere)

    def test_missing_activation_and_duplicate_fail_closed(self):
        rows=fake_activations()
        with self.assertRaises(ValueError):
            crosswalk_from_activations_for_synthetic_only(rows[:-1],
                                                         include_supplementary=True)
        with self.assertRaises(ValueError):
            crosswalk_from_activations_for_synthetic_only(rows+[rows[0]])

    def test_mismatched_gene_key_gate_or_line_rejected(self):
        rows=fake_activations()
        idx=0;r=rows[idx]
        rows[idx]=GateActivation(body=r.body,side=r.side,
                                 longitude=r.longitude,gate=(
                                     (r.gate %64)+1),line=r.line)
        with self.assertRaises(ValueError):
            crosswalk_from_activations_for_synthetic_only(rows)

    def test_sun_earth_wrong_opposition_or_line_rejected(self):
        rows=fake_activations()
        idx=next(i for i,r in enumerate(rows)
                 if (r.side,r.body)==("design",CelestialBody.EARTH))
        actual=rows[idx]
        displaced=longitude_to_gate_line(actual.longitude+1)
        rows[idx]=GateActivation(body=actual.body,side=actual.side,
               longitude=actual.longitude+1,
               gate=displaced.gate,line=displaced.line)
        with self.assertRaises(ValueError):
            crosswalk_from_activations_for_synthetic_only(rows)

    def test_untyped_activation_input_and_untyped_chart_rejected(self):
        rows=fake_activations()
        with self.assertRaises(ValueError):
            crosswalk_from_activations_for_synthetic_only([{}]+rows)
        with self.assertRaises(ValueError):
            crosswalk_from_incumbent_verified_chart(object())

    def test_synthetic_six_profile_research_hash(self):
        obj=self.snapshot
        self.assertEqual(obj["synthetic_sample_count"],6)
        self.assertEqual(len(obj["samples"]),6)
        self.assertTrue(obj["source_only_not_a_personality_prediction"])
        self.assertFalse(obj["owner_private_birth_data_used"])
        self.assertEqual(obj["human_predictions_tested"],0)
        self.assertEqual([x["synthetic_UTC_time"] for x in obj["samples"]],
                         [x.isoformat() for x in SYNTHETIC_UTC])
        b={k:v for k,v in obj.items() if k!="research_snapshot_sha256"}
        self.assertEqual(obj["research_snapshot_sha256"],digest(b))

    def test_official_public_January_6_2020_sun_pulse(self):
        obj=self.snapshot["samples"][0]
        lifes_work=next(x for x in obj["profile_11"]["spheres"]
                       if x["slug"]=="lifes_work")
        self.assertEqual(lifes_work["gate_gene_key_number"],54)
        self.assertEqual(lifes_work["line"],1)
        self.assertFalse(obj["official_web_profile_calculated"])

    @unittest.skipUnless(HAS_SWISS, "pyswisseph needed for actual official Pulse calendar comparison")
    def test_four_source_published_sun_pulses_match_swisseph_wheel(self):
        """Gene Keys official Pulse webpage is a real-world WHEEL check, not full profile parity."""
        from hdmatch.chart.ephemeris import SwissEphemerisProvider
        provider=SwissEphemerisProvider((
          Path("/home/joel/humandesign/data/ephemeris/sepl_18.se1"),
          Path("/home/joel/humandesign/data/ephemeris/semo_18.se1")))
        public_pulse=[
          (datetime(2020,1,6,12,tzinfo=UTC),54),
          (datetime(2026,10,15,12,tzinfo=UTC),32),
          (datetime(2026,10,20,12,tzinfo=UTC),50),
          (datetime(2026,10,26,12,tzinfo=UTC),28),
        ]
        for instant,official_gate in public_pulse:
            with self.subTest(instant=instant):
                lon=provider.position(CelestialBody.SUN,instant).longitude
                actual=longitude_to_gate_line(lon)
                self.assertEqual(actual.gate,official_gate)
        self.assertFalse(self.snapshot["production_chart_or_scorer_modified"])

    def test_core_vs_optional_no_unadvertised_additional_spheres(self):
        for s in self.snapshot["samples"]:
            a=s["profile_11"]
            b=s["profile_14_with_supplementary"]
            self.assertEqual(len(a["spheres"]),11)
            self.assertEqual(len(b["spheres"]),14)
            self.assertEqual(a["spheres"],b["spheres"][:11])
            self.assertTrue(all(x["source_status"]=="extended"
                                for x in b["spheres"][11:]))
            self.assertFalse(a["official_gene_keys_profile_website_comparison_performed"])

    def test_calendar_88_days_not_same_as_HD_88_degree(self):
        differences=[s["difference_88degree_minus_88calendar_days_days"]
                     for s in self.snapshot["samples"]]
        self.assertGreater(max(abs(x) for x in differences),3)
        self.assertEqual(
            [s["number_different_gene_keys_at_design"]
             for s in self.snapshot["samples"]],[1,1,4,4,1,1])
        self.assertEqual(
            [s["number_different_design_lines"]
             for s in self.snapshot["samples"]],[4,5,7,4,3,5])
        self.assertEqual(self.snapshot["official_free_profile_parity_status"],
                         "UNVERIFIED")
        self.assertTrue(self.snapshot["source_only_not_a_personality_prediction"])

    def test_no_duplication_as_separate_astrological_ensemble_evidence(self):
        for s in self.snapshot["samples"]:
            a=s["profile_11"]
            self.assertEqual(a["independent_astrological_evidence_count"],0)
            self.assertEqual(a["human_validation_results"],0)
            self.assertFalse(a["production_scorer_modified"])
        self.assertFalse(self.snapshot["production_chart_or_scorer_modified"])


class TestG35ResearchAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((HERE/"GENEKEYS_G35_SOURCE_STATUS_AND_TEST_PLAN_V1.json").read_text(encoding="utf8"))

    def test_GeneKeys_contemplation_distinct_HD_geom_not_independent_vote(self):
        x=self.r["classification"]
        self.assertFalse(x["is_GeneKeys_equivalent_to_HumanDesign"])
        self.assertTrue(x["has_broadly_same_geometric_birth_chart_inputs"])
        self.assertEqual(x["independent_ephemeris_natal_variables_added_to_full_HD_chart"],0)
        self.assertFalse(x["should_be_separate_predictive_evidence_vote_in_an_astrological_ensemble"])
        self.assertTrue(x["not_a_verified_genetic_or_neurobiological_mechanism"])

    def test_two_scientific_questions_not_conflated(self):
        a,b=self.r["two_distinct_research_questions"]
        self.assertEqual(a["scientific_role"],"ASTROLOGY_PROFILE_INCREMENTAL_CLAIM")
        self.assertEqual(b["scientific_role"],"INTERVENTION_EFFICACY_NOT_NATAL_CHART_PREDICTION")
        self.assertFalse(a["operationally_frozen_GeneKeys_feature_to_human_outcome_mapping"])
        self.assertFalse(b["actual_intervention_or_randomization_started"])
        self.assertTrue(b["finding_cannot_validate_birth_chart_calculation"])

    def test_11_and_three_supplementary_official_sources(self):
        x=self.r["astronomical_research_status"]
        self.assertEqual(x["first_core_spheres"],11)
        self.assertEqual(x["optional_additional_spheres"],3)
        self.assertEqual((x["core_activation_sequence_spheres"],
                          x["venus_sequence_sphere_references"],
                          x["pearl_sequence_sphere_references"]),(4,6,4))
        self.assertEqual(x["wheel_programming_partner_pairs"],32)
        self.assertEqual(x["unique_core_spheres_after_sequence_overlap"],11)
        self.assertEqual(x["source_wheel_gate_equal_degrees"],5.625)
        self.assertEqual(x["source_wheel_line_equal_degrees"],.9375)

    def test_88degree_and_calendar_day_warning_kept_unresolved(self):
        x=self.r["astronomical_research_status"]
        self.assertTrue(x["official_88_day_vs_88_degree_wording_ambiguity_exposed"])
        self.assertFalse(x["HD_88_degree_official_gene_keys_parity_verified"])
        self.assertEqual(x["synthetic_8_design_planet_gene_key_differences"],[1,1,4,4,1,1])
        self.assertFalse(x["exact_official_hologenetic_profile_goldenset_for_given_birth_utc"])
        self.assertTrue(x["missing_goldenset_not_substituted_by_code_replay"])

    def test_no_owner_private_chart_reused_or_production_promoted(self):
        x=self.r["administrative_boundary"]
        self.assertFalse(x["personal_user_or_absent_third_party_charts_computed"])
        self.assertFalse(x["active_task_modified"])
        self.assertFalse(x["production_chart_or_scorer_modified"])
        self.assertEqual(x["real_participant_predictions_or_answers_collected"],0)
        self.assertFalse(x["systematic_GeneKeys_outcome_accuracy_estimated"])
        self.assertEqual(x["root_scientific_goal_status"],"OPEN")

if __name__=="__main__":
    unittest.main()
