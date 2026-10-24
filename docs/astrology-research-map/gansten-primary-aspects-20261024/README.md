# Primary Directions — zodiacal rays and mundane phase aspects

Checkpoint: 2026-10-24. Research-only implementation, NOT a verified complete historical technique and NOT a claim that astrology predicts events.

## What this adds

The earlier first-generation Swiss-verified engine calculated body-to-body conjunctions and directions to the natal Ascendant/Midheaven separately under proportional semi-arcs, Placidean under-the-pole, and Regiomontanian position circles. This update keeps its legacy default/JSON unchanged while adding TWO distinct selectable geometric contact profiles:

1. Zodiacal promissor rays — for each classical body promissor, construct an ecliptic ray point at natal tropical longitude ±60° sextile, ±90° square, ±120° trine, or +180° opposition. Exactly one opposition branch is generated. The point has latitude β_ray=0. Convert that constructed point to true-of-date RA and declination using the actual true obliquity; DO NOT add aspect degrees directly to right ascension. Direct it to the natal significator with each of three separately labeled geometry families. Use either its actual bodily coordinates by default or project its ecliptic longitude to β_significator=0 as a separately selectable alternative. Exact natal Asc/MC remain the actual angle circles for either policy.

2. Proportional semi-arc mundane aspects — use the independently documented normalized positional phase of the significator, offset it by ±60°, ±90°, ±120°, or 180°, and find the rotation of the moving body's own semi-arcs needed to reach that phase. This is NOT the same as an aspect in ecliptic longitude. This profile is restricted to the proportional semi-arc method and bodily significators. It is an explicit GEOMETRIC RECONSTRUCTION of the method described by the Gansten audit, not a universal primary-source formula attributed without qualification to all historical writers.

These are independent geometric CONTACT CANDIDATES with exact aspect/orientation/latitude labels, not forecasts or evidence of statistical usefulness. More candidates can create more incidental date hits. No scoring or outcome-based filtering is performed.

The program accepts only seven classical planets as promissors. The significators are other classical planets and the natal Ascendant and Midheaven. Self-to-self planetary directions are excluded in this initial profile. Rays of significators, other house cusps, lots, fixed stars, antiscia, dignities, lunar secondary motion, all-quadrant historical traditional converse, and entire historically distinct directed-ray models remain outside the implemented scope.

## Historical source trace (not copied from the book)

The owner-paid Martin Gansten Primary Directions audit records:
- Chapter 5 pp.65–70 and Chapter 8 pp.88–90: zero-latitude zodiacal rays are computed from ecliptic longitude ± aspect, NOT equatorial RA ± aspect.
- Chapter 8 pp.89–92 and the audited Appendix I §4a pp.152–154: mundane aspects instead involve semi-arc positional geometry.
- Chapter 5 pp.67–70: Bianchini's inclined-circle latitude prescriptions and Morin's latitude-change/orbital-maximum prescriptions are distinct, with some exact relations not fully established.
- Appendix I §4b: keeping the significator's bodily latitude while projecting the promissor to the ecliptic is documented as a hybrid; do NOT automatically assign it universally to a named practitioner.
- Chapter 1 pp.5–7, Chapter 5 p.71, Chapter 8 pp.88–101: interpretive role of promissor/significator and traditional versus reverse-rotation converse are different issues.

These locations come from the pre-existing, purchased-book Work audit, not from a new verbatim extraction this turn. The reference files in the prior research branch preserve uncertainty, cross-edition questions and witness disagreement. Where exact ancient/medieval attribution is not confirmed, this code is labeled an analytic implementation rather than attributed as a known complete historical engine.

## Latitude and historical-method control

The new CLI supports:
- profile body_conjunctions — unchanged prior default and unchanged JSON schema/contacts
- profile zodiacal_promissor_rays — ray always β=0
- profile mundane_proportional_semi_arc — normalized phase offsets only, one geometry

For zodiacal rays, significator-projection choices:
- retain_bodily (default) — fixed natal planet's physical RA/declination
- project_to_ecliptic — fixed planet longitude at β=0, source longitude frozen; actual ASC/MC circles not projected

Bianchini, Morin, and promissor-ray latitude retaining are NOT implemented. The CLI gives an error rather than pretending that the two supported fixed-planet policies reproduce these historically different orbital or inclined-circle models.

Aspect offset branch labels positive_offset / negative_offset deliberately describe the MATHEMATICAL offset. They are not silently labeled sinister/dexter when traditional naming/roles need additional source verification. Under-the-pole uses the previously audited signed AO/DO correction; the upstream Morinus bug report remains independent from this project's code.

The earlier one-equinoctial-degree-per-symbolic-year Ptolemy-style model and explicitly modern mean-solar diagnostic are still separately named. The original literal Lilly Naibod table has NOT been implemented; it must be checked against the printed source, with its anomalous cells retained. All projected model dates are modern mean-year arithmetic, not historical calendar assertions.

## Astronomy and execution

Reuses the existing strict SwissEphemerisProvider and SwissAstronomyReferenceProvider. Every one of the seven classical bodies has retained physical RA, declination, tropical ecliptic longitude and ecliptic latitude; true obliquity is frozen for the natal instant. The coordinate rotation is a newly tested spherical trig implementation independently compared with Swiss Ephemeris cotrans at 300 nonzero-latitude/ecliptic-longitude combinations. SWIEPH returned flags and file hashes are retained.

The official Swiss Ephemeris files remain OUTSIDE the Git repository:

    /home/joel/.local/share/hdmatch/ephemeris/1800-2399/

SHA-256:
- sepl_18.se1 = ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66
- semo_18.se1 = 1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7

Natal domain is 1800–2399 CE, latitude −66°..+66°. Do not silently extrapolate to other ephemeris periods or near-polar Placidus angles.

Runnable local research checkout (once installed, code remains isolated from production):

    cd /home/joel/Documents/astrology/gansten-primary-directions-aspects-engine
    export PYTHONPATH="$PWD/src"
    PY=/home/joel/humandesign/.venv/bin/python
    EPHE=/home/joel/.local/share/hdmatch/ephemeris/1800-2399
    "$PY" -m hdmatch.astrology.cli --utc 2000-01-01T12:00:00Z \
      --latitude 45 --longitude-east 0 --ephemeris-dir "$EPHE" \
      --profile zodiacal_promissor_rays --output /tmp/zodiacal_rays_example.json

For a projected fixed significator, add:

    --significator-projection project_to_ecliptic

For proportional mundane aspects replace the profile and do not request an unsupported position-circle/under-pole mundane ray:

    --profile mundane_proportional_semi_arc

The CLI still defaults to body_conjunctions and refuses to overwrite an existing output file. The JSON explicitly declares profile, aspect name, offset branch, sign convention, latitude policy, method, model age/date conversion, provenance and unavailable-count handling. No personal natal data or human event histories were used for these synthetic examples.

## Verification

- Four deterministic Swiss-file output examples from TWO synthetic charts (2000-01-01 12:00 UTC, 45N 0E; and 2026-03-19 06:00 UTC, 45N 24E) are in examples/ with full per-file Swiss input SHA-256 metadata. The 2000 case has 683 zodiacal bodily, 690 zodiacal projected, 222 mundane-phase contacts in a 100-symbolic-year window, and the 2026 zodiacal bodily case has 740. Different counts reflect the declared geometry/projection and time-window cut, NOT different numbers of verified predictions.
- Generated candidates per method/target/offset before age cuts: zodiacal = 1,176 (7 promissors × 8 other bodies/angles × 7 distinct aspect branches × 3 method geometries); mundane = 392 (same candidate labels but one method). No duplicate opposition branch.
- Existing original conjunction-only JSON is directly compared for full exact equality to the frozen previous file; no v1 regression.
- 300 independent Swiss cotrans comparisons on random ecliptic longitude/latitude/obliquity; 400 deterministic mathematical phase-residual tests; explicit positive/negative offset, wrap-around, latitude, duplicate-opposition and unsupported-method checks. Test commands/results captured in VERIFICATION.json.
- 600 extra aspect-ray inputs fed into the unchanged original Morinus toPlanet source bodies (all four sky quadrants and both hemispheres represented). Proportional semi-arcs and Regiomontanus agree 600/600 each. Under-the-pole matches 596/600, with all four disagreements equal to 2×|negative physical AO/DO| and thus fully explained by the previously submitted and tested Morinus 8 sign bug. No novel unexplained disagreement in the tested profile. This is source-method parity, NOT an end-to-end GUI run or guarantee on other aspect schemes.
- Run tests/unit/test_primary_direction_aspects.py, tests/unit/test_primary_directions.py, tests/unit/test_astronomy_reference.py, and tests/unit/test_relationship_western_rrf.py. Check VERIFICATION.json for final pass count, lint and type-check results.

## Next research tasks

1. Verify/implement aspects OF significators and traditional role-reversed converse using direct primary witnesses, separately from the current Morinus-like shortest signed arc convention.
2. Implement additional historically sourced mundane-aspect systems and Bianchini's latitude formulas only after exact mathematical and textual source requirements are recovered.
3. Literal Naibod/other time-key witness parity, lunar secondary motion, bounds/terms and Lot of Fortune constructions, then exhaustive branch/ephemeris and birth-time uncertainty coverage.
4. Freeze historically testable candidate variants before any prospective combined astrology experiment; report complexity penalties and multiple-testing burden. Never choose one method based on the actual participant's known life.

**Status:** engineering math reproducible in an isolated research branch; the complete historical predictive system remains OPEN. No production HD model or human survey was changed.
