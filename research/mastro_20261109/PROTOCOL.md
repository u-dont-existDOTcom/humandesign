# Mastro comparative replication: execution protocol v1

Status: **engineering implementation; new-human protocol is a draft, not a completed preregistration or human experiment**. This lane concerns Mastro's tropical-sign keyword pipeline. It changes no Human Design mappings or accepted checkpoints.

## What the correspondence commits to

The 2026-11-08 sent reply commits to installing the current Mastro version, notifying Vincent when running, obtaining the exact older study executable and original birth files, and discussing a preregistered blinded follow-up. The 2026-11-06/07 exchange distinguishes the already reproduced historical arithmetic from that new test. The original two-proportion test was, according to Vincent's clarification, selected at the outset. Do not describe test shopping as established fact. No email is sent by this task.

The public predecessor note is preserved in `PRIOR-STUDY.md`; canonical predecessor source commit is `111f7943ac8a73abe9273cff8c08f8b7cff1d080`, branch `research/godbout-hemisphere-inversion-20261106`. The original 141 identities, descriptions, outcomes and all their reanalyses are development evidence. They cannot become an untouched cohort by renaming or shuffling them.

## Two separate operations

1. **Original-engine reproduction:** custodian obtains original build and input files, hashes them, records complete settings, reproduces the standard/inverted keyword exports and compares them against retained source exports. Verify numerical positions independently, including historical timezone and birth-source uncertainty. Current v7.8.0 does not establish parity with the original build. This is an engineering reproduction of known outcomes.
2. **New-human replication:** freeze the following contract before collecting any scored measurements from new people. Register recruitment, stopping/sample-size rationale, exclusion rules, matching strata, lexical extraction and all nuisance/baseline models. An external custodian must preserve identity/chart/orientation keys outside the blind scorer's account or inaccessible storage. A worktree or different directory under the same user is not an access boundary.

## Proposed fixed comparison

For each independently documented birth input produce standard, 180-degree inverted, 90-degree sham and 270-degree sham chart keyword vectors. The inversion must reproduce the author's sign-label procedure: do not simulate it by moving the birth date six months, and do not rotate houses/aspects without explicit source verification. The exact Mastro operation remains a required parity check. Keep one person's four charts together throughout permutation.

Primary endpoint: South-minus-North difference in inversion win rates, where an exact score tie contributes 0.5 and remains separately reported. This is an explicit prospective tie rule, not a claim about ties in the original study. Primary null: assign each response to a random person's complete four-chart package **within the same hemisphere**. Use a predeclared seed and permutation count, include self-assignments, report the plus-one upper-tail p-value `(extreme+1)/(B+1)`. Do not tune the endpoint or permutation scheme after seeing results. Conditional exchangeability within hemisphere is an assumption, not proof of absence of confounding. North/South strata alone do not control demographics or sampling differences.

Secondary outputs: continuous inverted-minus-standard contrasts, all four arm mean scores, and within-hemisphere N x N true-person chart ranks with best/worst tied ranks and unique top-one counts. All secondaries are exploratory without multiplicity correction. Report each hemisphere separately. The code does not yet implement a demographic/occupation/season predictive baseline or equatorial causal experiment; these require independently frozen data/design before the full proposed follow-up can be called operational.

The scorer uses case-insensitive literal terms, first matching ASTRO row, summed per BIO occurrence and divided by ASTRO row count. It does not trim, stem, infer synonyms or turn keyword scores into probabilities. Duplicate-row/lexical conventions must pass original-export parity before claiming exact original-engine reproduction. No post-outcome editing of descriptions, words, weights, settings, denominators, exclusions, comparisons or cohort is permitted. A later redesign is a new version with new untouched people.

## Blinding and freeze sequence

1. Trusted birth custodian verifies birth dates, local times, IANA zones and offsets at birth, latitude/longitude, source quality and uncertainty; keeps identifying data private. Do not infer residence or birth place from the operator's system timezone.
2. Chart operator records Mastro executable/rule DB/ephemeris hashes and complete settings: zodiac, inversion/rotation procedure, houses, points, aspects/orbs, corpus language, scoring, included factors, normalization and output format. Produce all chart arms and random opaque IDs. Shuffle chart order; give the scorer a flat list containing only `chart_id` and `keywords`. Keep person/orientation/hemisphere mapping away from scorer.
3. Freeze chart package, settings/input/measurement-protocol hashes, recruitment counts and stopping rule, software hash/commit, primary endpoint, tie policy, permutation seed/count. Save the freeze digest with an independent timestamp/registration **before responses**. A locally writable hash file alone is not an externally verifiable preregistration.
4. Independent assessors collect descriptions without identities, birthdays, hemisphere, astrology or predicted terms. Freeze raw descriptions, extraction pipeline and final lexical lists. Named-celebrity LLM biographies are not this measurement. Use consent and private storage appropriate to the data. Split by person before any fitting or selection.
5. Isolated scorer sees only response IDs/word lists and flat opaque chart vectors, calculates **every** response x chart score, and freezes the complete matrix. Custodian independently registers its digest before any key access. The scorer never selects a favorite orientation or participant subset.
6. Custodian runs `evaluate` with the registered matrix digest and separately held key. Reveal once, retain failures/ties and negative results. Human outputs remain private unless sharing is explicitly authorized. Publish only sanitized aggregates and reproducibility code.

The CLI checks content drift, unique IDs, completeness, finite scores, group counts, all four arms, key placement outside the supplied decoder root, and no overwrite of existing result files. These are file-integrity checks. They do **not** prove event chronology, independent custody, external registration, assessor blindness or ethical recruitment. Those receipts must exist before a human run. Self-declared custody/config fields are not independently verified controls.

## Data schemas and commands

Charts: `[{"chart_id":"opaque-random-id","keywords":[{"word":"example","weight":1.2}]}]`.
Responses: `[{"response_id":"opaque-random-id","words":["example"]}]`.
Custodian key, outside decoder access: `[{"response_id":"...","hemisphere":"N","arms":{"standard":"...","inverted":"...","sham90":"...","sham270":"..."}}]`.

Config requires `seed`, `permutations`, `n_north`, `n_south`, `status`, `engine_sha256`, `settings_sha256`, `birth_inputs_sha256`, `measurement_protocol_sha256` and `custody_attestation`. `preregistered_human` status additionally requires `external_custodian_and_isolated_scorer`; this declaration must be supported externally. The public engineering fixture uses artificial terms and placeholder provenance explicitly labeled `engineering_only`.

```bash
python3 research/mastro_20261109/compare.py freeze --charts CHARTS --config CONFIG --out FREEZE
python3 research/mastro_20261109/compare.py score --freeze FREEZE --charts CHARTS --config CONFIG --responses RESPONSES --out MATRIX
# Custodian independently records {"matrix_sha256":"<registered digest>"} in SEAL.
python3 research/mastro_20261109/compare.py evaluate --freeze FREEZE --matrix MATRIX --seal SEAL --key EXTERNAL_KEY --repo-root DECODER_ROOT --out EVALUATION
python3 -m unittest discover -s research/mastro_20261109/tests -v
python3 research/mastro_20261109/engineering_smoke.py --out FRESH_OUTPUT_DIRECTORY
```

The synthetic smoke is a known-answer software test. Its operator/source knows the constructed answers. It is **not** an actual blinded experiment, Mastro accuracy test, or behavioral replication.

## Inputs still required

- Vincent's exact original executable, study birth files and source-quality ratings, full settings and retained original exports for parity. Do not request these from memory or infer the historical build from current v7.8.0.
- New participants not used for design, with independently documented birth data and uncertainty, and independent measurements not yet inspected by developers.
- External custodian/access isolation and registration receipts; finalized cohort/power/stopping/exclusion/matching/measurement/baseline design before recruitment.
- For any actual sending to Vincent, explicit owner instruction to send. Read/search access and research execution do not authorize outward mail.

## Noninterfering Wine execution

Owner correction during this task: GUI menus/dialogs must not cover the owner's work, and the owner must not be relied on to notice helper errors. Consequently `wine_controls.py` refuses mutations on the normal display. All further GUI execution uses a private, authenticated Xvfb display with no TCP listener and a **separate Wine-prefix snapshot**, with Desktop/Documents links redirected inside that snapshot. Original Mastro remains on its original prefix. This is GUI isolation, not scientific blinding or a security sandbox.

`background_desktop.py` starts the display and background Mastro using explicit source/runtime paths. Keep its session file, authentication file, registry, activation state and copied vendor databases private. Do not commit or distribute a Wine prefix or licensed Mastro binaries. An activation prompt is a stop boundary, never a reason to bypass licensing. The portable Xvfb used here was extracted locally from the official Ubuntu package `xvfb_21.1.12-1ubuntu1.9_amd64.deb`, SHA-256 `2011271eabcc2eb460e99995c5ef26e46633e87d04f570e305b62f178f7b452c`; no system installation is required.

After every mutation the helper drains output and checks for application-error dialogs. It reports exceptions in text with a nonzero exit code. Use checked sequential calls so a failure prevents dependent actions. Capture screenshots from the background display; PrintWindow/X11 capture on the normal Wayland desktop was unavailable. Do not request repeated owner screenshots to drive automation.

## Live export receipt

The current v7.8.0 instance completed a real Animation batch on the private desktop: three consecutive test charts at 2026-11-10/11/12 13:29:28, 190/193/202 scored keyword rows. `import_mastro.py` parsed its actual Trees.csv and removed identifying labels/signatures from the vector schema. This was a current-sky engineering fixture, with no human outcomes. The private raw export stays private; `results/live-export-receipt.json` binds its hash/counts/conditions.

Separately, Tools > Ephemeris generated three tropical/geocentric midnight-UTC position rows for the same dates. The table can be inspected, but clipboard copying returned no text and no raw batch numerical export or CLI/API has been established. Do not mistake rounded table values or screenshots for a precision ephemeris audit.
