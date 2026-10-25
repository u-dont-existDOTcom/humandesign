# Modern Western primary-direction pilot — evidence-preserving research scaffold

**Checkpoint: 25 October 2026.** This is a **bounded engineering/design experiment**, not an enrolled study, not an authentic complete Lilly or Argoli method, and not proof of astrology. The overall owner objective remains **OPEN**: construct historically source-differentiated Western/Hellenistic/Jyotish/Chinese/Human Design models, freeze specific predictions and compare with genuinely untouched human records or prospective responses against proper decoys/controls.

## 1. Why this branch exists

After extensive 1647 Lilly and Argoli (1610, 1667) primary-source work, the principal remaining obstacle to **human predictive validation** is not just restoring older tables: the actual event targets, eligibility and opportunity denominators, uncertainty in recorded birth times, objective controls, and unseen participants are still required. Historical source work and modern validation can proceed **in parallel**, as separately named arms. Another 1644 scan is useful but cannot become an assistant-invented mandatory gate for an independently labeled modern test.

Previous primary-source meaning candidates are in `primary-direction-event-hypotheses-20261024` and `primary-direction-essential-dignity-20261025/NEXT_EMPIRICAL_GATE.md`. The research here **retains all eight** Lilly source-associated candidate rules from the original source inventory, without deleting six to improve apparent results. Only two occupational BODY contacts are provisionally concrete enough to **consider** as narrowly defined modern endpoints: Midheaven–Jupiter bodily contact → dated new formal appointment/promotion; Midheaven–Saturn bodily contact → dated involuntary removal/demotion. These are modern researcher interpretations with occupational-role context and possible alternatives in the historical prose, **not** unconditional Lilly promises or an authentic score-ready source model.

Six other candidates retain explicit *not ready* status: material patronage threshold unclear (Asc/Jupiter bodily and soft), formal complaint narrower than broad controversy (Asc/Mars bodily/hard), conditionally strong Jupiter unresolved (MC/Jupiter soft), and occupational-status conditions / nonindependence requiring separation (MC/Saturn hard). These can be studied later as explicit secondary models, never retrospectively rescued as confirmed hits.

## 2. New computational tool (not production astrology)

`src/hdmatch/astrology/western_forward_blind.py` supplies four testable bounded components:

- **Contact envelope:** requires every integer-minute birth-time offset around recorded time and forbids favorable-minute selection. A contact absent at any sampled minute, or belonging to one of the six unresolved source families, has `timing = null` so it **cannot be scored**; its potential age span remains separately visible in `possible_range_for_review`. The grid does **not** guarantee coverage of all continuous moments between ticks.
- **Exact exposure accounting:** clips and deduplicates overlapping half-open age intervals. Intersects forecast windows with independently established opportunity/eligibility AND outcome ascertainment periods; missing documentation is explicitly `UNASCERTAINED`, never equivalent to a true negative. Window fraction is exposure time, **not a calibrated event probability**.
- **Chart-label permutation method:** accepts an already-frozen participant × chart compatibility matrix, scores the true assignment against all permutations for N≤8, or a seeded Monte Carlo null for N≥9. It cannot independently guarantee matrix blinding or exchangeability, which must be fixed and audited by the actual human protocol. The model also needs an independently frozen scalar score to populate that matrix.
- **Privacy-safe prediction receipt:** creates a deterministic commitment for a pseudonymous participant with SHA-256 references to private birth inputs, ephemeris features, algorithm, rules and decoys, and all source-status/contact windows. It contains **no real birth date, birthplace, human event, questionnaire response, medical or legal predictions**. Creating a hash in memory does **not** itself prove human-model preregistration, time of sealing, or secure write-once storage; those require a separate authorized, auditable participant workflow.

No engine or external services are deployed. No person was recruited. Existing classical astrology program code remains unchanged. `PILOT_V0_METHOD_CONTRACT.json` spells out what is frozen **for engineering** versus still unspecified for an actual human trial.

## 3. Actual feasibility finding from the known 96-chart source panel

The only calculations using charts in this pass read the already-verified `SYNTHETIC_PANEL_EXPOSURES.json` and its checksum manifest, **without recomputing any astronomy**.

| Engineering quantity | Previously frozen 96-chart result |
| --- | ---: |
| All eight source-associated candidate contacts | 216 |
| Modern tentative Midheaven/Jupiter BODY contacts | 9 |
| Modern tentative Midheaven/Saturn BODY contacts | 11 |
| Total two-domain occupation contacts | **20** |
| Tentative windows' proportion of 96 × 47 unconditional adult years | **0.4233%** |

The fraction uses previous default **±0.5 symbolic-year** windows, no birth-time uncertainty, a fixed artificial age interval [18,65), and an unrealistically complete 47 years of observation/occupational eligibility per chart. It is **not** a demographic population incidence, a measured event rate, or a predictive hit rate. It is also far below the all-eight-candidate exposure occupancy calculated in the older source panel; broadening to poorly defined outcomes or widening windows *only because predictions are rare* would invite multiple-testing and coincidence artifacts.

In the earlier predeclared time-sensitivity audit, ±5 minutes of recorded birth-time uncertainty shifted matching direction ages by about **1.25 years** under a one-degree/year key. For the human cohort we must propagate actual uncertainty through the ephemeris/chart engine, report unresolved contacts, and match control opportunity years to the expanded window duration. A reported exact minute does **not** automatically equal certified ±0-minute birth precision. The discrete-minute-grid code alone is not a continuous-interval guarantee.

**Resulting feasibility assessment:** a prospective occupational-event timing study may require a large cohort or lengthy follow-up. Its sample size cannot be selected from synthetic occupancy without independently measured eligible professional-year and dated event rates. A separately designed forward-blind behavioral/questionnaire study remains a potentially faster companion test, and the official `humandesign` forward-blind protocol already describes its own guarded workflow.

## 4. First actual human trial: decisions still needed before launch

The six unresolved conditions and potential outcomes, including dependence between contacts and method families, remain in the source register. Before reading ANY untouched test outcome:

1. Fix the actual natal chart computation (ephemeris hashes + requested/returned SWIEPH mode, exact software direction and time key); declare **modern diagnostic**, not `authentic Argolus`.
2. Fix which occupational-role gains/losses qualify and who had an eligible position to gain/lose. A professional opportunity *timeline* and documentary-event availability must be independently coded without knowing predicted windows. Unknown completeness is not absence of an event.
3. Fix birth-time provenance, historical timezone/DST resolution, allowed minute/timing uncertainty domain, scoring/abstention and actual observable time horizon.
4. Freeze the cohort recruitment and independent controls, all N×N chart/response predictions, event evidence, chart matching strategy, primary scalar statistic and how multiple astrological traditions will be reported **separately**. Do not reuse owner/friends whose histories informed the original source selection for untouched final testing.
5. Seal raw birth inputs privately, model/code/rules/decoy hashes, the complete prediction package and timestamps in controlled storage **before** outcome records are accessed; then independently blind-code both positive and negative events, unanswered and unascertainable intervals, and predeclared null permutations.

**No human trial is registered or approved by merely executing this branch.** All code and synthetic tests are preparation. The user's higher-level historical reading work and existing Human Design scoring/forward-blind requirements are unaffected.

## 5. Build and recovery

From the isolated source-controlled branch:

```sh
export PYTHONPATH="$PWD/src"
$HOME/humandesign/.venv/bin/python -m pytest -q tests/unit/test_western_direction_forward_blind.py
$HOME/humandesign/.venv/bin/python docs/astrology-research-map/western-primary-direction-blind-pilot-20261025/build_synthetic_pilot_feasibility.py
```

The feasibility generator intentionally **refuses to overwrite** the already saved report. To reproduce its bytes, invoke its pure `build()` function and compare canonical serialization to the committed JSON. No network, participant birth inputs, PDF scans, or actual chart ephemerides are necessary to read the original saved synthetic contacts.

The live research branch and test results, exact evidence hashes, and source continuation are documented in `CONTINUATION_CHECKPOINT.md` and `VERIFICATION.json`. The owner-facing ZIP goes into `~/Téléchargements/gansten-astro/` as usual. **Empirical predictive accuracy: UNTESTED.**

**Validation as of this checkpoint:** 14 focused tests and **220 inherited + focused Western source/method tests** passed. No human event records were used or scored, and no sample-size or power claim was derived from the known synthetic panel.
