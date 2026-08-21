# Prior-work scan

Date: 2026-08-21  
Applicability: `required`  
Disposition: `compose`

## Independent conception snapshot

The supplied architecture calls for a Python system that composes deterministic astronomy, historical civil-time conversion, exact state segmentation, a frozen symbolic rubric, authenticated prediction commitments, rank evaluation, and person-level empirical validation. The project-specific remainder is the auditable composition and the explicit separation between synthetic engineering validation and out-of-sample human validation.

## Existing-work map

| Surface | Existing work | Decision |
|---|---|---|
| Historical civil time | Python `zoneinfo`, PEP 495 folds, and first-party `tzdata` | Reuse; round-trip both folds to reject nonexistent local times and retain ambiguous resolutions. |
| Astronomical positions | Swiss Ephemeris / `pyswisseph` | Adapt behind a strict provider that requires declared local ephemeris data and rejects silent Moshier fallback. |
| Scalar roots | Bracketing plus a convergent bracketed root solver (Brent/bisection family) | Implement a small deterministic bisection boundary because the provider abstraction supplies the function and tolerances; benchmark against SciPy Brent where available. |
| Authenticated sealing | `cryptography` AEAD primitives | Reuse AES-GCM with unique nonces, associated metadata, and an external key file; never implement a cipher. |
| Person-level validation | Grouped/nested split methods and permutation tests in scikit-learn | Reuse grouped splits when the optional empirical dependency is installed; enforce participant exclusivity in core schemas independently. |
| API | FastAPI and the supplied OpenAPI/backend contract | Adapt; keep API optional and route it to the same pure services as the CLI. |
| HD symbolic semantics | Supplied V4/V3.2 protocols and question bank | Adapt only source-supported constructs; unresolved response encodings and mappings remain explicit. |

## Novel remainder and baselines

The novel remainder is the end-to-end blind experiment state machine, stable-state date aggregation, frozen generator/decoder rule identity, and failure classification under the repository's scientific constraints. External baselines are authoritative timezone round trips, independent ephemeris/HD chart comparison, candidate-date priors, calendar/season models, grouped empirical models, and chart-assignment permutations.

## Sources and limits

- Python `zoneinfo` documentation: https://docs.python.org/3/library/zoneinfo.html
- Swiss Ephemeris overview and licensing: https://www.astro.com/swisseph/swephinfo_e.htm
- Swiss Ephemeris programming interface: https://www.astro.com/swisseph/swephprg.htm
- Cryptography authenticated encryption documentation: https://cryptography.io/en/latest/hazmat/primitives/aead/
- SciPy bracketed root reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html
- scikit-learn grouped split reference: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html

Swiss Ephemeris is dual-licensed (AGPL or professional); redistribution or a public service requires an explicit compatible license decision. This repository may implement the adapter and local research workflow, but must not claim bundled production ephemeris data or independent HD-engine validation until those artifacts are actually supplied and hashed.
