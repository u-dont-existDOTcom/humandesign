# 21 — Forward-Blind Execution Checklist

This file turns the forward-blind design in `docs/20_forward_blind_prospective_validation.md` into a concrete implementation/operations checklist.

## A. Engineering implementation

Required commands/modules before recruiting untouched participants:

- `forward-prepare`: normalize DOB/time/place, resolve historical timezone, calculate concealed chart, freeze chart/model/question/decoy hashes before any scored answer;
- `forward-questionnaire`: render only neutral behavior-first wording with frozen randomized option order;
- `forward-freeze-responses`: persist raw/coded answers and a response hash before reveal;
- `forward-evaluate`: score true chart and declared controls/decoys without model edits;
- `forward-reveal`: reveal chart only after prediction + response + evaluation freezes;
- `forward-cohort-evaluate`: build response×chart matrix, true-chart ranks, permutation null, and layer-wise results.

Reuse existing chart, V4.3 scoring, questionnaire, sealing, permutation, and cache components. Do not fork a second scoring implementation.

## B. Minimum first pilot

Use DEVELOPMENT participants only.

Target: 5–10 people with documented birth times, preferably HD-naive.

Collect before testing:

- exact local DOB/time;
- birthplace;
- source of birth time;
- stated uncertainty;
- whether they know Human Design;
- whether they already know Type/Profile/Authority;
- consent to store a pseudonymous research record.

Pilot goals are UX, leakage detection, missing mappings, and runtime validation. Pilot accuracy is not evidence.

## C. First evidential cohort

After the complete questionnaire/mapping/scoring stack is frozen:

- recruit a VALIDATION cohort not used for wording/mapping changes;
- primary analysis should prefer HD-naive participants;
- freeze a primary group statistic before opening results;
- use participant-chart permutation and matched decoy panels;
- report every participant, including poor/negative matches;
- do not exclude participants post hoc because they are said to be `not-self`.

If the model changes after validation, obtain a new untouched cohort.

## D. Color/Tone/Base readiness

CTB remains off for primary testing until all engineering gates in `docs/19_base_level_substructure_validation.md` pass.

After CTB calculation parity passes:

1. freeze primary Ra/IHDS CTB→PHS/Rave Psychology/Variable mappings from source materials;
2. build behavior-first concealed questions/tasks;
3. use DEVELOPMENT only for question refinement;
4. compare nested `F4` vs `F3` on untouched participants;
5. promote CTB only if it adds prospective out-of-sample discrimination.

## E. Materials requested from the user

Highest-value contributions are:

1. original Ra/IHDS PHS, Rave Psychology, Variable, Color/Tone/Base transcripts or PDFs;
2. official/Jovian/IHDS chart screenshots/exports that visibly show Color/Tone/Base for exact known timestamps;
3. 5–10 willing DEVELOPMENT participants with documented birth times and preferably little/no prior HD knowledge;
4. later, a separate untouched cohort that has never supplied answers to model development.

See `reference/substructure/SOURCES_NEEDED.md` for exact source priorities.

## F. Do-not-cross boundary

Do not begin an evidential human cohort while any of these are still changing:

- question wording;
- answer-to-mechanic direction;
- dependency clusters;
- scoring weights/flexibility classes;
- reliability policy;
- decoy sampling policy;
- primary statistic;
- CTB mapping conventions for any CTB-enabled analysis.
