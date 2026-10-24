#!/usr/bin/env python3
"""Independent-source check of constructed zero-latitude ecliptic rays.

Uses unchanged Morinus SE upstream toPlanet bodies, not its whole GUI.
Disagreements due to the previously verified under-the-pole signed AODO bug
are isolated; there is no code correction of the upstream algorithms here.
"""

import json
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

from hdmatch.astrology.aspect_points import (
    RayAspect,
    aspect_branches,
    zodiacal_promissor_ray,
)
from hdmatch.astrology.geometry import (
    EquatorialPoint,
    GeometryMethod,
    GeometryUnavailable,
    direction_arc,
)

ROOT = Path(os.environ.get("MORINUS_HARNESS_DIR", "/tmp/gansten_morinus_compare_20261023"))
if not (ROOT / "Morinus" / "placidianutppd.py").is_file():
    raise SystemExit("Requires checked-out Morinus source and unchanged AST harness (see README)")
sys.path.insert(0, str(ROOT))
import compare_morinus_source as mor  # noqa: E402 (source path is runtime-supplied)

rng = random.Random(20261024)
n = 600
count = defaultdict(int)
failures = []
max_delta = defaultdict(float)
known_sign_bug = 0
unexpected_differences = 0
for i in range(n):
    lat = rng.uniform(-58, 58)
    ramc = rng.uniform(0, 360)
    sigra = rng.uniform(0, 360)
    sigdec = rng.uniform(-20, 20)
    lonprom = rng.uniform(0, 360)
    eps = rng.uniform(23.2, 23.8)
    asp = rng.choice(tuple(RayAspect))
    branch = rng.choice(aspect_branches(asp))
    ray = zodiacal_promissor_ray(lonprom, aspect=asp, branch=branch, obliquity_deg=eps)
    fixed = EquatorialPoint(sigra, sigdec)
    object_, p, r = mor.synthetic(lat, ramc, sigra, sigdec)
    runner = mor.Runner(object_, lat, ramc)
    mpoint = ray.equatorial
    ad = mor.ai(mor.t(lat) * mor.t(mpoint.dec_deg))
    cases = [
        (
            "semi_arc",
            GeometryMethod.PROPORTIONAL_SEMI_ARC,
            mor.semi_method,
            (False, 99, -1, mpoint.ra_deg, ad, 3, 0, 0),
        ),
        (
            "under_pole",
            GeometryMethod.PLACIDEAN_UNDER_POLE,
            mor.utp_method,
            (False, 99, -1, mpoint.ra_deg, mpoint.dec_deg, 3, 0, 0),
        ),
        (
            "regiomontanus",
            GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
            mor.reg_method,
            (
                False,
                99,
                -1,
                ray.ecliptic_longitude_deg,
                0.0,
                mpoint.ra_deg,
                mpoint.dec_deg,
                3,
                0,
                0,
            ),
        ),
    ]
    for name, method, fn, args in cases:
        count[name + ":attempt"] += 1
        try:
            source = runner.call(fn, *args)
            reference = direction_arc(method, lat, ramc, fixed, mpoint)
        except (AssertionError, GeometryUnavailable, ValueError) as exc:
            count[name + ":rejected"] += 1
            if len(failures) < 9:
                failures.append({"case": i, "method": name, "error": str(exc)})
            continue
        delta = abs((source - reference + 180) % 360 - 180)
        physical_coord = p.speculum[13] if object_.eastern else -p.speculum[13]
        if delta > 1e-8:
            if (
                name == "under_pole"
                and physical_coord < 0
                and abs(delta - 2 * abs(physical_coord)) < 1e-8
            ):
                known_sign_bug += 1
            else:
                unexpected_differences += 1
        count[name + ":match" if delta < 1e-8 else name + ":mismatch"] += 1
        max_delta[name] = max(max_delta[name], delta)
        if delta > 1e-8 and len(failures) < 15:
            failures.append(
                {
                    "case": i,
                    "method": name,
                    "input": [lat, ramc, sigra, sigdec, lonprom, eps, asp.value, branch.value],
                    "source": source,
                    "reference": reference,
                    "delta": delta,
                    "stored_source_AODO": p.speculum[13],
                }
            )
result = {
    "source_commit": "020492d5fce1c7a3d6b81186cef6cf04d93fb694",
    "seed": 20261024,
    "generated_ray_inputs": n,
    "counts": dict(count),
    "max_abs_delta": dict(max_delta),
    "recognized_original_under_pole_AODO_sign_discrepancies": known_sign_bug,
    "unexplained_source_discrepancies": unexpected_differences,
    "first_issues": failures,
    "scope": (
        "unchanged Morinus toPlanet original AST only; zodiacal promissor ray "
        "λ±ψ, β_ray=0 and natal significator bodily; conjunction target; "
        "3 methods; not human predictions"
    ),
}
Path(__file__).with_name("MORINUS_ZODIACAL_RAY_SOURCE_PARITY.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "counts": result["counts"],
            "max_abs_delta": result["max_abs_delta"],
            "known_sign_bug": known_sign_bug,
            "unexplained_differences": unexpected_differences,
            "first_issues": failures[:6],
        },
        indent=2,
    )
)
assert count["semi_arc:match"] == n
assert count["regiomontanus:match"] == n
assert unexpected_differences == 0
assert count["under_pole:mismatch"] == known_sign_bug
