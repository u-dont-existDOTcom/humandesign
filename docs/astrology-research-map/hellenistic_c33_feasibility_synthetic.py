"""C33: zero-human, no-biography source-feasibility and scenario calculations.

2020 UTC calendar days and pure assumed event-prevalence scenarios.
None is a real participant, empirical prevalence estimate, validation,
recruitment requirement, study power guarantee or experiment outcome.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from math import ceil,sqrt
from statistics import NormalDist
from pathlib import Path
import json

from hellenistic_c33_ptolemy_marriage_count import (
    synthetic_body_from_verified_provider,
)

SCENARIOS=(
    {
      "id":"WAR_LOW_HYPOTHETICAL",
      "candidate":"C30_DOROTHEUS_CAMPAIGN",
      "assumed_unexposed_event_risk":0.01,
      "assumed_exposed_event_risk":0.02,
      "exposed_fraction_assumed":1/3,
    },
    {
      "id":"WAR_MODERATE_HYPOTHETICAL",
      "candidate":"C30_DOROTHEUS_CAMPAIGN",
      "assumed_unexposed_event_risk":0.03,
      "assumed_exposed_event_risk":0.045,
      "exposed_fraction_assumed":1/3,
    },
    {
      "id":"MARRIAGE_LARGE_HYPOTHETICAL",
      "candidate":"C33_PTOLEMY_MORE_THAN_ONE",
      "assumed_unexposed_event_risk":0.15,
      "assumed_exposed_event_risk":0.25,
      "exposed_fraction_assumed":1/3,
    },
    {
      "id":"MARRIAGE_SMALL_HYPOTHETICAL",
      "candidate":"C33_PTOLEMY_MORE_THAN_ONE",
      "assumed_unexposed_event_risk":0.20,
      "assumed_exposed_event_risk":0.25,
      "exposed_fraction_assumed":1/3,
    },
)


def required_n_two_group_unadjusted(
    *, p0:float,p1:float,exposed_fraction:float=1/3,
    alpha:float=0.05,power:float=0.8
)->int:
    """Normal approximation for a two-sided unequal-size two-proportion test.

    This is for rough feasibility ONLY; source outcomes are historical,
    context-dependent and not independent identical Bernoulli draws.
    Cohort/clusters, stratification, ascertainment and enrollment losses
    can inflate sample size and must be handled separately.
    """
    if not (0<p0<p1<1 and 0<exposed_fraction<1
            and 0<alpha<1 and 0<power<1):
        raise ValueError("strict illustrative alternative rates required")
    q=exposed_fraction
    pb=q*p1+(1-q)*p0
    vn=pb*(1-pb)*(1/q+1/(1-q))
    va=p1*(1-p1)/q+p0*(1-p0)/(1-q)
    nd=NormalDist()
    zcrit=nd.inv_cdf(1-alpha/2)
    zpow=nd.inv_cdf(power)
    n=(zcrit*sqrt(vn)+zpow*sqrt(va))**2/(p1-p0)**2
    return ceil(n)


def synthetic_utc_2020_moon_days(provider:object)->dict:
    """Every UTC civil-day window across leap year; not a participant cohort."""
    current=datetime(2020,1,1,tzinfo=UTC)
    end=datetime(2021,1,1,tzinfo=UTC)
    rows=[]
    while current<end:
        nextday=current+timedelta(days=1)
        source=synthetic_body_from_verified_provider(
            provider,time_start=current,time_end=nextday,
            historical_branch="men_moon")
        envelope=source["conditional_interval_enclosure"]
        values=envelope["possible_bicorporeal_values"]
        cls=("MANY_INDICATED_CONDITIONALLY" if values==[True]
             else "NO_INDICATION_CONDITIONALLY" if values==[False]
             else "TIME_INDETERMINATE")
        rows.append({
            "utc_civil_date":current.date().isoformat(),
            "moon_midpoint_tropical_longitude":source["source_body_midpoint"],
            "possible_signs":envelope["possible_signs"],
            "source_class":cls,
            "ephemeris_file_hashes":source["source_files_sha256"],
        })
        current=nextday
    return {
      "schema":"HUMANDESIGN_C33_SYNTHETIC_UTC_DAY_CLASSIFIER_V1",
      "all_dates_are_SYNTHETIC_not_people":True,
      "epoch":"2020-01-01_to_2020-12-31_UTC",
      "sampled_days":len(rows),
      "no_real_births_or_outcomes":True,
      "no_legal_marriage_predictions_frozen":True,
      "conditional_on_incumbent_declared_Moon_max_speed_16_deg_per_day":True,
      "actual_speed_enclosure_for_full_historical_range_independently_proved":False,
      "UTC_day_is_not_an_IANA_birth_civil_day":True,
      "source_bicorporeal_positive_windows":sum(
          x["source_class"]=="MANY_INDICATED_CONDITIONALLY" for x in rows),
      "source_bicorporeal_negative_windows":sum(
          x["source_class"]=="NO_INDICATION_CONDITIONALLY" for x in rows),
      "unresolved_sign_boundary_windows":sum(
          x["source_class"]=="TIME_INDETERMINATE" for x in rows),
      "production_scorer_modified":False,
      "real_human_predictive_validations":0,
      "rows":rows,
    }


def feasibility_scenarios()->dict:
    cases=[]
    for scenario in SCENARIOS:
        n=required_n_two_group_unadjusted(
            p0=scenario["assumed_unexposed_event_risk"],
            p1=scenario["assumed_exposed_event_risk"],
            exposed_fraction=scenario["exposed_fraction_assumed"])
        cases.append({**scenario,"estimated_total_N_unadjusted":n})
    return {
       "schema":"HUMANDESIGN_C33_HYPOTHETICAL_POWER_SCENARIOS_V1",
       "status":"SCENARIO_ASSUMPTIONS_NOT_MEASURED_BASE_RATES",
       "two_sided_alpha":0.05,
       "nominal_power":0.8,
       "method":"normal-approximation unequal-allocation difference-in-proportions",
       "ignores_ascertainment_bias_clustering_and_birth_data_exclusion":True,
       "not_a_real_study_sample_size_commitment":True,
       "human_predictions_tested":0,
       "scenario_rows":cases,
    }


if __name__=="__main__":
    import argparse
    cli=argparse.ArgumentParser()
    cli.add_argument("--ephemeris-dir",type=Path,required=True)
    cli.add_argument("--out",type=Path,default=Path(__file__).with_name(
      "HELLENISTIC_C33_UTC_2020_SYNTHETIC_CLASSIFIER_V1.json"))
    args=cli.parse_args()
    from hdmatch.chart.ephemeris import SwissEphemerisProvider
    root=args.ephemeris_dir.expanduser().resolve()
    provider=SwissEphemerisProvider(
        (root/"sepl_18.se1",root/"semo_18.se1"))
    result=synthetic_utc_2020_moon_days(provider)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    scenario_path=args.out.with_name("HELLENISTIC_C33_HYPOTHETICAL_POWER_V1.json")
    scenario_path.write_text(json.dumps(
        feasibility_scenarios(),indent=2,sort_keys=True)+"\n")
    print("SYNTHETIC_UTC_DAYS",result["sampled_days"],
          "POSITIVE",result["source_bicorporeal_positive_windows"],
          "NEGATIVE",result["source_bicorporeal_negative_windows"],
          "UNRESOLVED",result["unresolved_sign_boundary_windows"])
    print("POWER_SCENARIOS",[(x["id"],x["estimated_total_N_unadjusted"])
         for x in feasibility_scenarios()["scenario_rows"]])
