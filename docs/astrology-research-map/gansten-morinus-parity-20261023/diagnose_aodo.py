#!/usr/bin/env python3
"""Independent diagnosis of Morinus 8 SE oblique-ascension boundary error.

Runs unchanged pinned Morinus source methods (see compare_morinus_source.py).
This script does NOT modify upstream software or certify whole application.
"""
import json, random, sys, types, zipfile, hashlib
from pathlib import Path
import compare_morinus_source as m

BASE=Path(__file__).resolve().parent
PKG=Path("/mnt/hdd/home/joel/Téléchargements/gansten-astro/Gansten_Primary_Directions_Reconciliation_20261023.zip")
if (BASE/"geometry_reference.py").exists():
    raw=(BASE/"geometry_reference.py").read_bytes()
else:
    with zipfile.ZipFile(PKG) as z: raw=z.read("geometry_reference.py")
refmod=types.ModuleType("prior_independent_geometry")
sys.modules[refmod.__name__]=refmod
exec(compile(raw,"prior_geometry_reference.py","exec"),refmod.__dict__)
R=refmod

summaries=[]
for seed,n in ((20261023,1200),(19870502,2400)):
    rng=random.Random(seed)
    counts={"cases":n,"three_methods_exact":0,"semi_exact":0,
            "regio_exact":0,"under_pole_exact":0,
            "under_pole_mismatch":0,"under_pole_negative_AODO":0,
            "negative_AODO_with_no_mismatch":0,
            "errors_not_explained_by_negative_AODO":0,
            "diagnostic_corrected_exact":0}
    examples=[]
    maxres=0.0
    for i in range(n):
        lat=rng.uniform(10,65)
        ramc=rng.uniform(0,360)
        decs=rng.uniform(-25,25)
        ad=m.ai(m.t(lat)*m.t(decs))
        ras=(ramc+rng.uniform(4,90+ad-4))%360
        decm=rng.uniform(-20,20)
        ram=(ramc+rng.uniform(4,165))%360
        observed=m.compute(lat,ramc,ras,decs,ram,decm)
        fixed=R.EquatorialPoint(ras,decs)
        moving=R.EquatorialPoint(ram,decm)
        expected={
            "semi_arc":R.proportional_semi_arc_direction(lat,ramc,fixed,moving),
            "under_pole":R.placidean_under_pole_east_upper_north(lat,ramc,fixed,moving),
            "regiomontanus":R.regiomontanus_position_circle_direction(lat,ramc,fixed,moving)
        }
        checks={k:abs(m.angular_diff(observed[k], expected[k]))<1e-7 for k in expected}
        for k,c in [("semi_exact","semi_arc"),("regio_exact","regiomontanus"),("under_pole_exact","under_pole")]:
            counts[k]+=checks[c]
        counts["three_methods_exact"]+=all(checks.values())
        neg=observed["source_speculum"]["AODO"]<0
        if neg:counts["under_pole_negative_AODO"]+=1
        if not checks["under_pole"]:
            counts["under_pole_mismatch"]+=1
            if not neg:counts["errors_not_explained_by_negative_AODO"]+=1
            raw=observed["source_speculum"]["AODO"]
            predicted_delta=2*abs(raw)
            actual_delta=abs(m.angular_diff(observed["under_pole"],expected["under_pole"]))
            maxres=max(maxres,abs(predicted_delta-actual_delta))
            if len(examples)<6:
                examples.append({"case":i,"input":[lat,ramc,ras,decs,ram,decm],
                    "source_under_pole":observed["under_pole"],
                    "reference_under_pole":expected["under_pole"],
                    "raw_AODO":raw,
                    "actual_abs_delta_degrees":actual_delta,
                    "predicted_abs_delta_degrees":predicted_delta})
        elif neg:counts["negative_AODO_with_no_mismatch"]+=1
        # Diagnostic counterfactual only: use the signed coordinate rather than
        # its absolute value. This is NOT a patched Morinus source function.
        raw=observed["source_speculum"]["AODO"]
        diagnostic=(observed["under_pole"]-2*raw) % 360 if raw<0 else observed["under_pole"]
        counts["diagnostic_corrected_exact"]+=abs(m.angular_diff(diagnostic,expected["under_pole"]))<1e-7
    summaries.append({"seed":seed,"counts":counts,
                      "max_error_magnitude_identity_residual":maxres,
                      "mismatch_examples":examples})
assert all(s["counts"]["semi_exact"]==s["counts"]["cases"] for s in summaries)
assert all(s["counts"]["regio_exact"]==s["counts"]["cases"] for s in summaries)
assert all(s["counts"]["under_pole_mismatch"]==s["counts"]["under_pole_negative_AODO"] for s in summaries)
assert all(s["counts"]["diagnostic_corrected_exact"]==s["counts"]["cases"] for s in summaries)
assert all(s["counts"]["errors_not_explained_by_negative_AODO"]==0 for s in summaries)
assert all(s["max_error_magnitude_identity_residual"]<1e-8 for s in summaries)
payload={
    "status":"CONFIRMED_SOURCE_LEVEL_EDGE_BUG_WITH_STATED_SCOPE",
    "tested_commit":"020492d5fce1c7a3d6b81186cef6cf04d93fb694",
    "source_location":"placidianutppd.py:1669 (verify pinned source line)",
    "mechanism":"fabs(negative eastern oblique ascension) wrongly reverses sign; under-pole angular arc shifted by 2*abs(AODO)",
    "reproduction":"synthetic equatorial fixed/moving points, northern latitude, fixed in east/above quadrant, original Morinus toPlanet methods and speculum classes",
    "coverage_limits":"not a full wxPython app run, not all hemispheres/quadrants, no actual historical chart or empirical forecasts",
    "samples":summaries,
    "source_sha256":hashlib.sha256((BASE/"Morinus"/"placidianutppd.py").read_bytes()).hexdigest(),
}
f=BASE/"MORINUS_AODO_DIAGNOSIS.json"
f.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"samples":[{"seed":x["seed"], **x["counts"], "maxres":x["max_error_magnitude_identity_residual"]} for x in summaries],"result":str(f)},indent=2))
