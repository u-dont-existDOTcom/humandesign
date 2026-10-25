"""G35 source-only six synthetic Gene Keys planet-sphere crosswalks.

Uses actual fail-closed Swiss .se1 source files through existing Human
Design calculate_chart. 88-degree solar-arc root belongs to HD chart.
Compares that root to a separate naive minus-88-CALENDAR-day interpretation
because Gene Keys official FAQ phrases the source loosely. Neither is
certified as the actual genekeys.com Free Profile implementation.
No personal birth data, copyrighted interpretation texts or human outcomes.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path

from genekeys_g35_source_crosswalk import (
    crosswalk_from_incumbent_verified_chart, digest
)

SOURCE_DIR = Path(__file__).resolve().parent
SYNTHETIC_UTC = (
    datetime(2020,1,6,12,tzinfo=UTC),
    datetime(2020,3,20,12,tzinfo=UTC),
    datetime(2020,6,21,12,tzinfo=UTC),
    datetime(2020,9,22,12,tzinfo=UTC),
    datetime(2020,12,21,12,tzinfo=UTC),
    datetime(2021,5,15,12,tzinfo=UTC),
)
DESIGN_BODIES=("sun","earth","moon","venus","mars","jupiter","uranus","saturn")


def synthetic_demo(*, ephemeris_dir:Path)->dict:
    from hdmatch.chart.calculator import calculate_chart
    from hdmatch.chart.ephemeris import SwissEphemerisProvider,CelestialBody
    from hdmatch.chart.rave_mandala import longitude_to_gate_line
    root=ephemeris_dir.expanduser().resolve()
    provider=SwissEphemerisProvider((root/"sepl_18.se1",root/"semo_18.se1"))
    bodies=tuple(
        getattr(CelestialBody, value.upper())
        for value in ("sun","earth","moon","mercury","venus","mars","jupiter",
                      "saturn","uranus")
    )
    samples=[]
    for synthetic in SYNTHETIC_UTC:
        chart=calculate_chart(provider,synthetic,bodies=bodies)
        main=crosswalk_from_incumbent_verified_chart(
            chart,include_supplementary=False)
        extra=crosswalk_from_incumbent_verified_chart(
            chart,include_supplementary=True)
        naive_time=synthetic-timedelta(days=88)
        exactly_pre=chart.design_utc
        delta=(exactly_pre-naive_time).total_seconds()/86400.
        differences=[]
        for body_name in DESIGN_BODIES:
            body=getattr(CelestialBody,body_name.upper())
            exact=next(x for x in chart.activations
                       if x.side=="design" and x.body==body)
            naive=provider.position(body,naive_time)
            gp=longitude_to_gate_line(naive.longitude)
            differences.append({
                "body":body_name,
                "88_degree_exact_gene_key":exact.gate,
                "88_degree_exact_line":exact.line,
                "naive_88_calendar_days_gene_key":gp.gate,
                "naive_88_calendar_days_line":gp.line,
                "gene_key_mismatch":gp.gate != exact.gate,
                "line_mismatch":gp.line != exact.line,
            })
        samples.append({
            "synthetic_UTC_time":synthetic.isoformat(),
            "real_subject_id":None,
            "official_web_profile_calculated":False,
            "official_gene_keys_text_reading_performed":False,
            "profile_11":main,
            "profile_14_with_supplementary":extra,
            "prenatal_design_exact_88degree_utc":exactly_pre.isoformat(),
            "prenatal_naive_exact_88calendar_days_utc":naive_time.isoformat(),
            "difference_88degree_minus_88calendar_days_days":delta,
            "two_candidate_design_time_planet_mismatches":differences,
            "number_different_gene_keys_at_design":
                sum(x["gene_key_mismatch"] for x in differences),
            "number_different_design_lines":
                sum(x["line_mismatch"] for x in differences),
        })
    if samples[0]["profile_11"]["spheres"][0]["gate_gene_key_number"]!=54:
        raise AssertionError("official Jan 6 2020 Gene Key 54 pulse crosscheck failed")
    if samples[0]["profile_11"]["spheres"][0]["line"]!=1:
        raise AssertionError("official Jan 6 2020 GK54.1 daytime crosscheck failed")
    result={
        "schema":"HUMANDESIGN_G35_SIX_SYNTHETIC_GENEKEYS_CROSSWALK_REPLAY_V1",
        "objective_status":"OPEN",
        "source_only_not_a_personality_prediction":True,
        "owner_private_birth_data_used":False,
        "any_real_participant_births_used":False,
        "human_predictions_tested":0,
        "source_planet_mappings":"official 11 plus distinct additional 3, not 14 independent Golden Path spheres",
        "source_mapping_URL":"https://genekeys.com/docs/what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/",
        "incumbent_HD_swiss_ephemeris_binary_version":provider.metadata.library_version,
        "incumbent_swisseph_sources_sha256":sorted(
            {f.sha256 for f in provider.metadata.files}),
        "HD_Design_method":"Sun solar longitude 88 degrees before natal Sun",
        "Gene_Keys_official_prose_ambiguity":"FAQ heading refers to 88 degrees while prose calls it 88 days",
        "official_free_profile_parity_status":"UNVERIFIED",
        "Gene_Keys_solar_reference":"Jan 6 2020 GK54.1 on official Gene Keys Pulse page",
        "synthetic_sample_count":len(samples),
        "samples":samples,
        "production_chart_or_scorer_modified":False,
    }
    return {**result,"research_snapshot_sha256":digest(result)}


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--ephemeris-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,
        default=SOURCE_DIR/"GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json")
    args=p.parse_args()
    data=synthetic_demo(ephemeris_dir=args.ephemeris_dir)
    args.out.write_text(json.dumps(
        data,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("G35_SYNTHETIC",data["synthetic_sample_count"],
          "source_sha",data["research_snapshot_sha256"])
    for x in data["samples"]:
        print(x["synthetic_UTC_time"],
              "88_deg_minus_88_day",round(x["difference_88degree_minus_88calendar_days_days"],4),
              "changed_key",x["number_different_gene_keys_at_design"],
              "changed_line",x["number_different_design_lines"])
