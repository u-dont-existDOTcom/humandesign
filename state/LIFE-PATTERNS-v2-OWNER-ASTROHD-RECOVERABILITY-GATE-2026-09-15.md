# Life Patterns v2 — owner AstroHD recoverability gate — 2026-09-15

## Owner correction / hard product criterion

The owner established a stronger acceptance criterion for the standardized Life Patterns instrument: broad domain coverage is not enough. A replacement instrument that cannot preserve enough target-blind behavioral information for the historical owner AstroHD procedure to recover the owner's known birth date/time has failed the owner development case.

This is a **development regression criterion**, not untouched human validation of astrology or Human Design.

## Historical owner benchmark

The existing historical AstroHD artifacts establish the comparison signature:

- century hourly scan: 876,601 candidates;
- exact recorded moment: merged hourly rank **#2**;
- leading hourly candidate: same recorded date, 17 minutes later;
- local minute refinement: the recorded date is the **#1 distinct refined neighborhood**;
- leading refined minute: **11 minutes** from the recorded time.

Canonical sources:

- `experiments/astrohd/exact_actual_v1_1_user_v3_6.json`
- `experiments/astrohd/scan_summary_v1_1_user_v3_6.md`
- `experiments/astrohd/minute_refinement_v1_1_user_v3_6.md`
- `experiments/astrohd/merged_model_v1_1_user_v3_6.json`

The new frozen regression baseline is:

- `reference/research/life_patterns_astrohd_owner_recovery_baseline_v1.json`

The raw birth date/time is not duplicated in that baseline.

## Why the 10-domain candidate failed this criterion

The prior `life-patterns-required-coverage-v1` checklist standardized broad domains, but a broad domain could become `sufficient` after measuring only one narrow aspect. That means the instrument could report complete coverage while omitting historically score-bearing/discriminating distinctions such as:

- original contribution versus inherited method;
- insight-to-structure;
- recurring consequential mystery;
- persuasion capacity versus preferred use;
- recognition-sensitive entry;
- social-network opportunity pathways;
- role projection/misrecognition;
- immediate somatic/felt signals and override;
- resource sovereignty/motive;
- sanctuary/sensory baseline;
- emotional permeability;
- correction threshold;
- retreat/privacy;
- concentrated focus versus repetition/mastery;
- developmental phases.

Therefore the old 10-domain partition is no longer an acceptable recovery-capability candidate even though its measurement mechanics remain useful.

## Historical information crosswalk

A post-freeze-only crosswalk is frozen at:

- `reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json`

It covers two distinct evidence classes:

1. all 19 behavior clusters that carried nonzero contribution in the historical merged owner recovery;
2. all 19 observables that added information in the clean V3.6 holistic-profile audit.

Important non-claim: no artifact currently establishes that each individual historical cluster is **leave-one-out necessary** for the successful birth recovery. The correct labels are score-bearing / information-bearing unless and until an ablation run establishes necessity.

The two explicitly post-selection V3.6 carrier refinements are not used to define required questionnaire coverage.

## New target-blind recoverability coverage candidate

Runtime implementation:

- `src/hdmatch/api/life_patterns_recoverability_domains.py`
- `src/hdmatch/api/life_patterns_v2_owner_recoverability.py`

Blueprint version:

- `life-patterns-recoverability-coverage-v2`

It contains 23 neutral behavioral dimensions:

1. complexity/detail/structure;
2. insight translation;
3. unresolved-question return;
4. original contribution versus inherited method;
5. persuasion capacity versus preferred use;
6. entry/recognition/role acceptance;
7. network opportunity pathways;
8. role projection/misrecognition;
9. immediate bodily/felt signals;
10. autonomy/direction under external roles;
11. home/sensory/sanctuary conditions;
12. romantic/attachment dynamics;
13. emotional baseline/permeability;
14. work energy across intensity/duration;
15. consequential effort/struggle/purpose;
16. correction threshold;
17. retreat/privacy/re-entry;
18. competing-value tension;
19. resources/status/security/sovereignty motive;
20. developmental phases/learned change;
21. rhythm/routine/continuity;
22. concentrated focus/repetition/mastery;
23. needs sensitivity/responsibility.

These are measurement dimensions, not encoded HD/astrology answers. Natural participant-led evidence may satisfy multiple dimensions; the interviewer still has no fixed episode quota and no mandatory counterexample quota.

## Blinding firewall

During participant/owner interview execution the runtime receives **none** of:

- the participant chart;
- birth date/time target;
- expected answer direction;
- historical AstroHD crosswalk;
- target-model mapping;
- candidate scores/ranks.

The historical crosswalk/recovery procedure may be applied only **after a fresh owner measurement is frozen**. This prevents the interviewer from steering questions toward the known chart while still permitting the owner development regression requested here.

## Executable outcome gate

Implementation:

- `src/hdmatch/evaluation/life_patterns_owner_recovery_gate.py`
- `tests/unit/test_life_patterns_owner_recovery_gate.py`

A fresh candidate passes only if, under the same declared historical search procedure:

1. the recorded date remains the top distinct refined neighborhood;
2. the exact recorded moment's hourly rank is no worse than #2;
3. the absolute refined-peak offset is no worse than 11 minutes.

Changing the search procedure cannot claim equivalence. Coverage completion alone cannot pass.

## Verification

Focused/new regressions cover:

- exact 23-dimension registry;
- absence of astrology/HD/chart terminology from runtime dimensions;
- complete historical merged-cluster and clean-information crosswalks;
- crosswalk exclusion from runtime;
- neutral somatic screener wording;
- evidence citation requirements;
- health-contract recoverability-candidate marker;
- pass/fail behavior of the outcome-level recovery gate.

GitHub Actions run `34991018614`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

The immediately preceding run also showed all tests passing (`751 passed, 7 skipped`) and failed only on one unused import, which was removed by the subsequent refactor.

## Current gate

**NOT YET PASSED.**

The code now defines and deploys a measurement candidate capable of preserving the historical behavioral distinctions and defines the exact regression criterion, but no fresh owner interview generated by this v2 instrument has yet been frozen and run through the historical recovery procedure.

The next irreducible evidence is therefore:

1. owner completes the refreshed target-blind v2 interview;
2. freeze that measurement before target mapping/scoring;
3. apply the post-freeze historical crosswalk/recovery procedure;
4. evaluate the resulting signature with the executable regression gate;
5. if it fails, treat the instrument as failed and revise measurement coverage rather than weakening the historical criterion.

External participant target scoring remains unauthorized. This owner-self post-freeze recovery regression is the narrow target-model activity explicitly requested by the owner.
