#!/usr/bin/env python3
"""Synthetic-only exact permutation null demo for a 20-day birth-sign class.

This module is NOT the project's production forward-blind scorer. Its only
purpose is to demonstrate why selecting the best of four post-outcome
calendar policies changes the null false-positive frequency.

The exact p for a single predeclared sign uses the standard subset-sum
permutation distribution over fixed-size label permutations. Real cohorts
with seasonal/cultural confounding need matched/stratified inference, not this
unstratified toy null. No person's data or astrology result is processed.
"""
from __future__ import annotations
from collections import Counter
from datetime import date, timedelta
from math import comb
from random import Random

from maya_yucatec_chuwen_policy_sensitivity import (
    diagnostic_chuwen_day_sensitivity, FIXED_VARIANTS
)

def exact_upper_tail_sum_p(values: tuple[int,...], indices: tuple[int,...]) -> float:
    """Probability selected sum >= observed under uniform k-subsets of n."""
    n=len(values);k=len(indices)
    if not (2<=n<=200 and 1<=k<n):
        raise ValueError("Small synthetic cohort with both groups is required")
    if any(type(v) is not int or not 0<=v<=5 for v in values):
        raise ValueError("Scores must be ordinal integers 0..5")
    if len(set(indices))!=k or any(type(j) is not int or not 0<=j<n for j in indices):
        raise ValueError("Indices must identify k distinct synthetic respondents")
    observed=sum(values[i] for i in indices)
    dp=[Counter() for _ in range(k+1)]
    dp[0][0]=1
    for seen,value in enumerate(values,1):
        for selected in range(min(k,seen),0,-1):
            for subtotal,count in list(dp[selected-1].items()):
                dp[selected][subtotal+value]+=count
    assignments=comb(n,k)
    if sum(dp[k].values())!=assignments:
        raise AssertionError("Exact uniform-subset combinatorics failed")
    return sum(count for total,count in dp[k].items() if total>=observed)/assignments

def source_declared_indices(start_date:date=date(2024,1,1),n:int=60):
    """Four FIXED source-policy classes; no search or best-fit selection."""
    if type(start_date) is not date or n!=60:
        raise ValueError("Only 60 synthetic consecutive dates implemented for demo")
    labels={p[0]:[] for p in FIXED_VARIANTS}
    for i in range(n):
        result=diagnostic_chuwen_day_sensitivity(start_date+timedelta(days=i))
        for alt in result["candidate_policies"]:
            if alt["chuwen_class"]:
                labels[alt["policy"]].append(i)
    return {k:tuple(v) for k,v in labels.items()}

def run_synthetic_null(repeats:int=384,seed:int=20261023) -> dict:
    if type(repeats) is not int or not 1<=repeats<=2048:
        raise ValueError("Synthetic repetition count 1..2048 only")
    if type(seed) is not int:
        raise ValueError("Integer deterministic synthetic seed required")
    rng=Random(seed)
    labels=source_declared_indices()
    assert len(labels)==4 and all(len(v)==3 for v in labels.values())
    assert len(set(i for ids in labels.values() for i in ids))==12
    hit_primary=0;hit_any=0
    primary=list(labels)[0]
    for _ in range(repeats):
        # Independent ordinal activity scores: no true birth-day effect.
        fake_scores=tuple(rng.randrange(6) for _ in range(60))
        ps={model:exact_upper_tail_sum_p(fake_scores,ids)
            for model,ids in labels.items()}
        hit_primary+=(ps[primary]<=.05)
        hit_any+=(min(ps.values())<=.05)
    return {
        "status":"SYNTHETIC_NULL_ONLY_NO_HUMAN_VALIDATION",
        "synthetic_people_per_replicate":60,
        "per_policy_positive_class_size":3,
        "four_policy_positive_classes_mutually_disjoint":True,
        "seed":seed,"replicates":repeats,
        "nominal_per_trial_alpha":.05,
        "single_locked_policy_positive_null_count":hit_primary,
        "posthoc_best_of_four_positive_null_count":hit_any,
        "locked_rate":hit_primary/repeats,
        "posthoc_selected_rate":hit_any/repeats,
        "no_actual_birthday_or_survey_data":True,
        "does_not_claim_randomized_human_birthdate_exchangeability":True,
        "no_chuen_prognosis_validated":True,
    }

if __name__=="__main__":
    import json
    print(json.dumps(run_synthetic_null(),indent=2))
