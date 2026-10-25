"""G36 independent official interpretive source vs pre-natal geometry caution.

Reconstruct source-faithful public *seven* archetype triads, verify official
programming partners against the incumbent 64-wheel, and show the material
difference exact HD 88° solar arc vs naive 88-CALENDAR-day prenatal placements
at the ACTUAL official sphere granularity for six synthetic dates.

Does NOT fetch protected profile results or infer private human experiences.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from genekeys_g35_source_crosswalk import (
    CORE_11, SUPPLEMENTARY_3, digest, wheel_programming_partner,
)

ROOT=Path(__file__).resolve().parent
PARENT=ROOT/"GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json"
REGISTRY=ROOT/"GENEKEYS_G36_PRIMARY_INTERPRETIVE_AND_PROFILE_ACCESS_AUDIT_V1.json"
OUT=ROOT/"GENEKEYS_G36_PRENATAL_SPHERE_SENSITIVITY_V1.json"
PARENT_RESEARCH_HASH="e5f47a5debd6101219a33929cbdace2fc7ddf17788ef08bb387c9a13f839a303"

def load_json(path:Path)->dict:
    return json.loads(path.read_text(encoding="utf8"))

def build() -> dict:
    earlier=load_json(PARENT)
    source=load_json(REGISTRY)
    pb={k:v for k,v in earlier.items() if k!="research_snapshot_sha256"}
    if earlier["research_snapshot_sha256"]!=PARENT_RESEARCH_HASH:
        raise ValueError("Expected original G35 parent research digest")
    if digest(pb)!=PARENT_RESEARCH_HASH:
        raise ValueError("G35 source snapshot altered")
    if len(earlier["samples"])!=6:
        raise ValueError("Six complete official-source-independent synthetic samples required")

    official_short_sources=[]
    for key in source["source_sampled_7_keys"]:
        number=key["number"]
        partner=wheel_programming_partner(number)
        if partner!=key["official_programming_partner"]:
            raise ValueError(f"public official programming partner mismatches wheel: {number}")
        official_short_sources.append({
            "key":number,
            "official_partner":partner,
            "public_source_url":key["official_url"],
            "shadow":key["shadow"],
            "gift":key["gift"],
            "siddhi":key["siddhi"],
            "source_style":key["source_style"],
            "not_source_specified_natal_behavioral_probability":
                not key["natal_person_trait_proportional_claim"],
        })
    if {x["key"] for x in official_short_sources}!={5,28,32,50,54,55,64}:
        raise ValueError("Unexpected or missing predeclared original-key sample")

    specs=CORE_11+SUPPLEMENTARY_3
    prenatal=[x for x in specs if x.birth_layer=="design"]
    if len(prenatal)!=8:
        raise AssertionError("expected six core design spheres plus two extras")
    keyed={(x.slug,x.body.value):x for x in prenatal}
    aggregate={}
    samples=[]
    for sample in earlier["samples"]:
        official_crosswalk=sample["profile_14_with_supplementary"]
        if official_crosswalk["human_predictions_made"]!=0:
            raise AssertionError("No participant prediction admissible")
        mapped={x["slug"]:x for x in official_crosswalk["spheres"]}
        planet_comparison={x["body"]:x
                           for x in sample["two_candidate_design_time_planet_mismatches"]}
        if len(planet_comparison)!=8:
            raise ValueError("Complete eight prenatal source-geometry comparisons required")
        rows=[]
        for (sphere,body_name),spec in keyed.items():
            current=mapped[sphere]
            d=planet_comparison[body_name]
            if current["gate_gene_key_number"]!=d["88_degree_exact_gene_key"]:
                raise ValueError("sphere label differs from exact-88-degree parent chart")
            if current["line"]!=d["88_degree_exact_line"]:
                raise ValueError("sphere line differs from exact-88-degree parent chart")
            changed_key=d["gene_key_mismatch"]
            changed_line=d["line_mismatch"]
            if (current["gate_gene_key_number"]!=d["naive_88_calendar_days_gene_key"])!=changed_key:
                raise ValueError("pre-natal planet mismatch source contradicts itself")
            if (current["line"]!=d["naive_88_calendar_days_line"])!=changed_line:
                raise ValueError("prenatal line comparison contradiction")
            rows.append({
                "sphere":sphere,"body":body_name,
                "core_Golden_Path":spec.source_status=="core",
                "HD_exact_88_degrees_gate":current["gate_gene_key_number"],
                "HD_exact_88_degrees_line":current["line"],
                "naive_88_calendar_days_gate":d["naive_88_calendar_days_gene_key"],
                "naive_88_calendar_days_line":d["naive_88_calendar_days_line"],
                "change_key":changed_key,"change_line":changed_line
            })
            x=aggregate.setdefault(sphere,{"body":body_name,
                                          "core":spec.source_status=="core",
                                          "changed_key_cases":0,
                                          "changed_line_cases":0})
            x["changed_key_cases"]+=int(changed_key)
            x["changed_line_cases"]+=int(changed_line)
        if sum(x["change_key"] for x in rows)!=sample["number_different_gene_keys_at_design"]:
            raise ValueError("per-sphere and C35 body count mismatch")
        if sum(x["change_line"] for x in rows)!=sample["number_different_design_lines"]:
            raise ValueError("per-sphere line count mismatch")
        samples.append({
            "synthetic_utc_date":sample["synthetic_UTC_time"],
            "HD_exact_88_degree_minus_naive_88_day_design_offset_days":
                sample["difference_88degree_minus_88calendar_days_days"],
            "reconstructed_spheres":rows,
            "changed_prenatal_gate_sphere_count":sum(x["change_key"] for x in rows),
            "changed_prenatal_line_sphere_count":sum(x["change_line"] for x in rows)
        })

    bysphere=[{"sphere":slug,**v} for slug,v in sorted(aggregate.items())]
    body={
        "schema":"HUMANDESIGN_G36_PRIMARILY_GENEKEYS_SOURCE_G36_PRENATAL_SPHERE_SENSITIVITY_V1",
        "source_parent_G35_research_sha256":PARENT_RESEARCH_HASH,
        "source_parent_G35_file_sha256":sha256(PARENT.read_bytes()).hexdigest(),
        "source_G36_interpretive_register_sha256":sha256(REGISTRY.read_bytes()).hexdigest(),
        "synthetic_chart_count":len(samples),
        "pre_natal_core_sphere_count":sum(x["core"] for x in bysphere),
        "prenatal_supplementary_spheres":sum(not x["core"] for x in bysphere),
        "official_7_public_partner_and_triads":official_short_sources,
        "core_prenatal_sphere_total_gate_changes":sum(x["change_key"]
            for y in samples for x in y["reconstructed_spheres"] if x["core_Golden_Path"]),
        "core_prenatal_sphere_total_line_changes":sum(x["change_line"]
            for y in samples for x in y["reconstructed_spheres"] if x["core_Golden_Path"]),
        "all_prenatal_sphere_total_gate_changes":sum(x["change_key"]
            for y in samples for x in y["reconstructed_spheres"]),
        "all_prenatal_sphere_total_line_changes":sum(x["change_line"]
            for y in samples for x in y["reconstructed_spheres"]),
        "by_prenatal_sphere":bysphere,
        "synthetic_sphere_comparisons":samples,
        "official_real_profile_88_day_vs_88_degree_method_certified":False,
        "this_is_two_candidate_methods_not_two_real_GeneKeys_profiles":True,
        "six_source_times_are_synthetic_not_personal_births":True,
        "actual_real_human_behavioral_predictions_or_outcomes":0,
        "all_public_triads_from_primary_official_pages_not_full_proprietary_text":True,
        "source_pages_do_not_state_natal_specific_numeric_trait_predictions":True,
        "cannot_count_Human_Design_as_independent_confirmation":True,
        "no_owner_chart_or_participant_responses_used":True,
        "production_changed":False,
    }
    return {**body,"replay_source_digest_sha256":digest(body)}

if __name__=="__main__":
    result=build()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("G36_OFFICIAL_SOURCE_ONLY_7KEYS",len(result["official_7_public_partner_and_triads"]))
    print("G36_SYNTHETIC_PROFILE_N",result["synthetic_chart_count"])
    print("G36_CORE_DESIGN_GATE_CHANGES",
          result["core_prenatal_sphere_total_gate_changes"])
    print("G36_CORE_DESIGN_LINE_CHANGES",
          result["core_prenatal_sphere_total_line_changes"])
    print("G36_BY_SPHERE",
          [(x["sphere"],x["changed_key_cases"],x["changed_line_cases"])
           for x in result["by_prenatal_sphere"]])
    print("SHA",result["replay_source_digest_sha256"])
