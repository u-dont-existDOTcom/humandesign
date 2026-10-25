# Western primary directions: outcome-blind, event-only scoring research

**25 October 2026. The owner's actual research goal is still OPEN.** The combined project aims to calculate historically distinct Western/Hellenistic/Jyotish/Chinese/Human Design methods, preregister specific predictions, and compare genuinely untouched human outcomes with independent controls. This single Western modern-diagnostic engineering experiment does not create a human validation result.

## Scientific reason for this stage

The preceding research proved historically attributed arc/dignity calculations and built private, hash-bound Swiss natal chart prediction receipts. It **did not** connect those receipts to real, independently coded outcomes, so the more than 235 passing numerical/privacy tests are not a measurement of whether astrology works.

The two tentative modern occupational endpoints are deliberately narrow: (1) a **documented formal role gain** associated with a bodily Jupiter–Midheaven contact, and (2) **documented involuntary role loss** associated with a bodily Saturn–Midheaven contact. They are modern operational restrictions of broader historical source language; their validity is itself an experimental hypothesis, not a statement that 1647 Lilly unconditionally predicted a particular career event. The six additional source-associated aspect/bodily families retain their source status **UNRESOLVED**, never selected post hoc to rescue failures.

`src/hdmatch/astrology/western_event_only_scoring.py` computes the coverage of each independently dated **positive** occupational event (as an age interval) by each candidate chart's deduplicated source-qualified timing windows. For an event known only to a calendar year, it measures the *fraction of that year interval* covered by the chart's windows instead of promoting the event to a fictional exact day. This uses a **uniform-within-reported-interval exploratory convention**, not a measured event-date probability. Overlapping contact windows for the same domain count once. An empty event list is **unknown event ascertainment**, not proof of no event. Repeated citations of the same dated event cannot multiply the hit score.

For N outcome cases and N independently produced candidate charts, the code builds the complete **N×N event-case by chart timing-alignment matrix** without consulting true chart assignments. The separate permutation helper evaluates the assigned diagonal against chart-label permutations, preserving equal N-by-N opportunity for decoy comparisons. It *does not* by itself establish that chart labels are exchangeable across sex, birth cohort, occupation, age, fame, source completeness or historical era. The permutation statistic is only an exploratory null until matching/stratification, model freeze, independent outcome collection, and external validity are proved.

**This is not an ordinary accuracy percentage, probability forecast, population incidence, event sensitivity/specificity or a proper scoring rule.** Broad windows can raise all raw event overlap scores, but should also raise scores under shuffled charts; direct comparisons of uncalibrated raw scores across astrology traditions are invalid.


## Candidate human evidence source: free Astro-Databank C sample

Publisher: <https://www.astro.com/adbexport/>. Astrodienst's **7 October 2026** readme describes an openly downloadable `c_sample.zip` (5,866 records starting with C, including 3,692 AA-rated); the freely provided sample is intended to help researchers develop techniques before seeking fuller data. This is **not** a population-random cohort: all surnames start with one letter and records are largely notable public figures. Its event lists are incomplete and often year-only; the database's documentation says only ~40% have any coded events and around 40% of those event records specify only a year. Those historical aggregate percentages are *documentation*, not a freshly verified proportion in the current C file.

The archive was **NOT acquired in this turn**. The connected Zorin browser-independent HTTP client received status 200 and announced 2,752,783 bytes but reading the body timed out after 60 seconds, saving zero bytes. A second bounded command-line route could not connect to the server. The public directory and file list were verified, but their existence is **not evidence that the actual source records were downloaded**. Do not fill the missing source gap by fabricating event records, or claim any human outcome comparison occurred.

Astrodienst's September 2026 licensing page now also requires paid subscriptions for broader ADB research data exports; only the free developmental sample is under consideration here. No subscription has been purchased or requested. Even for free material, do **not** mirror the original human records, names or event notes to the public `humandesign` repository. Preserve source identifiers/terms and later hash a securely saved external copy.

If an authorized connection can obtain the free sample, the next operation is a **birth-only, outcome-inaccessible extraction**. The preauthored `src/hdmatch/astrology/western_birth_only_cohort.py` accepts only AA-rated public birth-source metadata with valid UTC and documented birth-time fields in the supported interval. It uses a fixed hash-based 20% development / 80% *candidate* holdout split by stable source ID; high-entropy HMAC pseudonyms hide identifying IDs. The labels are merely a **partition plan** until event files are actually sequestered and timestamps/permissions independently audited. The selector has no event or profession fields. Keep the full source outside Git and never use event existence to choose which charts to compute.

The next source-data action must distinguish the following: **retrospective, outcome-blind evaluation of already-recorded events** is still not equivalent to a **prospective real-world prediction study**. It may supply controlled evidence if chart predictions/selection are frozen before decoding the event nodes and outcome ascertainment is independently conducted. Incomplete biographies cannot justify treating missing promotion/demotion entries as genuine non-events. Formal appointment/removal and career eligibility must be independently verified; an astrology database label alone is insufficient.

## Build and execute without real participants

```sh
export PYTHONPATH="$PWD/src"
$HOME/humandesign/.venv/bin/python -m pytest -q \
  tests/unit/test_western_event_only_scoring.py \
  tests/unit/test_western_birth_only_cohort.py
```

All test people, events and chart windows are *fictional*. The score matrix, chart-label null, source status guards, date precision, event-evidence dedup, no-event abstention and source-only cohort selection are under test. No calibrated probabilities, claims about personal destinies, exact historic method certification, or genuine human predictive validity result are produced.

The current exact source, test and checkpoint are in `BLIND_EVENT_SCORING_CONTRACT.json`, `CONTINUATION_CHECKPOINT.md`, `VERIFICATION.json`, the two new Python modules and their tests. Further development should prioritize truly blinded human evidence, with source-accurate multi-tradition arms frozen separately. **Root outcome OPEN. Human predictive accuracy UNTESTED.**


## Verification completed

**15/15 focused tests passed; 250/250 inherited and new Western source/math/blinding tests passed** with pinned Swiss files. Ruff formatting/lint and mypy type checks passed for the new source scoring, birth-only cohort and verification modules. Source/algorithm SHA-256 manifest output and private HMAC safeguards are preserved. This is strong engineering reproducibility for a **nonempirical test fixture**, not support for astrological validity.

**Source access remains the only external acquisition blocker in this subtask.** An open publisher directory is not a successful download: the official `c_sample.zip` body timed out and the local restricted folder has no raw source. The 2026 publisher readme offers the sample for research-tool development, while broader research data subscriptions are paid. No paid access, use-right expansion or claim about actual recorded event incidence is implied by this project.
