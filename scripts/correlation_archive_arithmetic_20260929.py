#!/usr/bin/env python3
"""Reproduce source-table arithmetic; NOT a calibrated test of astrology.

Python standard library only. Inputs were visually transcribed from Correlation
36(1), 2023, printed pp.51-52 and 38(1), 2026, printed pp.47-50.
Usage: python3 correlation_archive_arithmetic_20260929.py [--output FILE]
Never substitutes for person-level data, end-to-end nulls, or held-out validation.
"""
from __future__ import annotations
import argparse
from decimal import Decimal
import json
import math
from pathlib import Path

CELLS = [
    (1,1,13,.107,.00372), (1,2,24,.206,.000152), (1,3,29,.311,.00274),
    (2,1,23,.214,.000961), (2,2,39,.390,.0000317), (2,3,43,.546,.00624),
    (3,1,29,.319,.00432), (3,2,42,.548,.0135), (3,3,47,.718,.182),
]

def holm(values: list[float]) -> list[float]:
    """Holm adjusted p-values, retaining original order and all endpoints."""
    if not values or any(not math.isfinite(p) or not 0 <= p <= 1 for p in values):
        raise ValueError('Expected a nonempty list of finite probabilities.')
    order=sorted(range(len(values)),key=lambda i:(values[i],i))
    out=[0.0]*len(values); bound=0.0
    for rank,i in enumerate(order):
        bound=max(bound,(len(values)-rank)*values[i])
        out[i]=min(1.0,bound)
    return out

def binomial_upper(k: int, n: int, p: float) -> float:
    """Exact finite binomial sum, treating the supplied p as fixed."""
    if not isinstance(k,int) or not isinstance(n,int) or not 0<=k<=n or not 0<=p<=1:
        raise ValueError('Invalid binomial parameters.')
    return math.fsum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1))

def results() -> dict:
    published=[x[4] for x in CELLS]
    exact=[binomial_upper(x[2],61,x[3]) for x in CELLS]
    ha=holm(published); ea=holm(exact)
    cells=[]
    for idx,(rank,tries,k,p0,p) in enumerate(CELLS):
        cells.append(dict(rank_max=rank,tries=tries,n=61,successes=k,
            rounded_p0=p0,expected_from_rounded_p0=61*p0,
            published_p=p,published_p_holm=ha[idx],
            exact_binomial_sensitivity_p=exact[idx],
            exact_binomial_sensitivity_holm=ea[idx]))
    defects=[]
    for person,original,inverted,printed,page in [
        ('Allende','0.9989','0.9425','0.0456',47),
        ('Anitta','0.3616','0.9617','0.0201',47),
        ('Musk','0.3170','0.3329','0.1108',50),
    ]:
        actual=Decimal(inverted)-Decimal(original)
        defects.append(dict(person_as_published=person,printed_page=page,
            noninverted=original,inverted=inverted,printed_difference=printed,
            arithmetic_difference=str(actual),matches_printed=actual==Decimal(printed)))
    p_s=48/68; p_n=26/73; pooled=74/141
    z=(p_s-p_n)/math.sqrt(pooled*(1-pooled)*(1/68+1/73))
    # Pure mathematical counterexample, not a fitted model or a human dataset:
    # chart prediction f(C_i)=i mod 10; target g(C_i,B)=f(C_i) for ANY biography B.
    # Across 100 cyclic assignments, final target shuffling averages 10% hits,
    # while swapping biographies and regenerating g retains 100% hits.
    n=100; predicted=[i%10 for i in range(n)]
    shuffled_output_hits=[sum(predicted[i]==predicted[(i+shift)%n] for i in range(n))/n
                          for shift in range(n)]
    result={
        'schema_version':1,
        'scope':'Conditional arithmetic and a logical counterexample; not human validation.',
        'cf003':{
            'source':'Godbout and Coron, Correlation 36(1), 2023, pp.51-52, Tables 2-4',
            'source_issue_sha256':'a4c0da056639aa0833dd96229a4efc3817395729b26c361875f24322f5092f44',
            'cells':cells,'published_holm_below_0_05':sum(p<.05 for p in ha),
            'published_bonferroni_below_0_05':sum(9*p<.05 for p in published),
            'sensitivity_holm_below_0_05':sum(p<.05 for p in ea),
            'limitations':[
                'Holm requires valid individual p-values. This calculation does not establish them.',
                'The exact-binomial sensitivity treats rounded training-derived p0 values as known constants.',
                'No joint person-level null distribution, target-pipeline replay or new data are available here.',
                'Nine endpoint definitions on one sample are not nine replications.',
            ],
        },
        'cf004':{
            'source':'Godbout and Brun, Correlation 38(1), 2026, pp.47-50',
            'source_issue_sha256':'e3ad72ee69c213ebe79739c025c91357fd7c112eefc8468bbdb43911ee9e8e73',
            'printed_subtraction_checks':defects,
            'reported_counts_only':{
                'south_inversion_wins':48,'south_n':68,'north_inversion_wins':26,'north_n':73,
                'south_fraction':p_s,'north_fraction':p_n,'difference':p_s-p_n,
                'pooled_two_proportions_z':z,
                'one_sided_normal_p':.5*math.erfc(z/math.sqrt(2)),
                'cohen_h':2*math.asin(math.sqrt(p_s))-2*math.asin(math.sqrt(p_n)),
                'south_exact_binomial_p_given_half':binomial_upper(48,68,.5),
                'north_noninversion_exact_binomial_p_given_half':binomial_upper(47,73,.5),
            },
            'orientation_defect':'Printed p.49 Figure 6 calls the June-28 Sun Capricorn non-inverted and Cancer inverted; p.50 prose calls Capricorn inverted.',
            'limitations':[
                'Reported 48/68 and 26/73 counts have NOT been reconstructed from all141 individual score pairs.',
                'Arithmetic agreement at aggregate level cannot verify the labels or the scoring software.',
                'Two chart versions do not establish a 50/50 no-association baseline.',
                'No corrected headline count is inferred from the erroneous examples.',
            ],
        },
        'synthetic_target_coupling_counterexample':{
            'n_synthetic_indices':n,'human_people':0,'observed_agreement':1.0,
            'mean_agreement_after_final_target_label_shuffle':math.fsum(shuffled_output_hits)/n,
            'agreement_after_biography_swap_and_target_regeneration':1.0,
            'biography_information_used':0,
            'meaning':'Possible failure of output-only shuffling when both prediction and target depend on the same chart; not a claim that the published system equals this construction.',
        },
    }
    assert sum(p<.05 for p in ha)==8 and sum(p<.05 for p in ea)==8
    assert math.isclose(min(ha),.0002853,rel_tol=1e-12)
    assert math.isclose(min(ea),.00064361301926072,rel_tol=1e-10)
    assert [x['arithmetic_difference'] for x in defects]==['-0.0564','0.6001','0.0159']
    assert math.isclose(result['synthetic_target_coupling_counterexample']['mean_agreement_after_final_target_label_shuffle'],.1)
    assert holm([.03,.01,.02])==[.04,.03,.04]
    assert math.isclose(binomial_upper(1,1,.5),.5)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(results(),indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    else:
        print(text,end='')
