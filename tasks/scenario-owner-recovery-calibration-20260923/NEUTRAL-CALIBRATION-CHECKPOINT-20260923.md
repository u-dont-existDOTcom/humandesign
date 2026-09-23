# Owner neutral calibration checkpoint — 2026-09-23

## Frozen input

Private measurement freeze SHA-256:
`7a6398de3c591e7dd8cc907b90c7312171452e6c13624a96e3f01826d6944863`

Participant-answer records: **68**

No birth/chart/model/candidate-ranking information was included in the neutral coding packet.

## Independent neutral coding

Two fresh GPT-5.6 Sol xhigh coding contexts independently reviewed the same frozen 68-answer packet against the neutral 73-facet contract.

Coder A:
- private output SHA-256: `538402a5d5f64ad4b75f08ba86943aab9d99d3011e14b040547032783966aa35`
- sufficient facets: 38
- partial facets: 11
- unknown facets: 3
- unassessed facets: 21
- fully covered neutral domains: 9 / 31
- partially covered neutral domains: 19 / 31
- uncovered neutral domains: 3 / 31

Coder B:
- private output SHA-256: `84be173203360e9d2370612ec492ae6dcec2bedd05540ced6f72ce7d4eec3e5c`
- sufficient facets: 42
- partial facets: 14
- unknown facets: 3
- unassessed facets: 14
- fully covered neutral domains: 9 / 31
- partially covered neutral domains: 19 / 31
- uncovered neutral domains: 3 / 31

The coders differ on 13 / 73 facet statuses but agree on the domain-level calibration shape.

## Decision

The completed owner pilot is **not yet a fully calibrated v7 neutral profile**. This does not mean the earlier pilot was unfinished. It means the pilot was completed, then its own evidence exposed several v6 questions as invalid, underspecified, tautological, or construct-mismatched; v7 subsequently replaced those routes. The old answers cannot simply be credited to the repaired constructs.

Do not open the participant to target-aware adaptive questioning. Additional questions must be selected from neutral evidence gaps only, with no birth/chart/model/rank information supplied to the selection context.

## Follow-up lane

The first target-blind repaired route selected for remeasurement is v7 `F0`, a matched audience-familiarity comparison. Its exact question was privately frozen before response. `F0` is a replacement measurement for a material repaired gap, not a generic decision to keep interviewing because some domain remains partial. Do not require exhaustive 73-facet completion; stop when remaining neutral gaps cannot materially change the declared recovery test.

F0 is now closed. The initial F0 replacement response was preserved without force-fitting; one narrow missing-piece clarification was collected privately. The working measurement now contains **70 answers**, and a fresh target-blind recoder marks `D05.audience_adaptation` **sufficient** under its narrow contract. Raw answers and participant-specific coding remain outside Git.

A fresh target-blind material-gap planner selected v7 `G17` next for `D16.challenge_threshold`, because prior evidence did not establish whether consequential and harmless errors change the participant's correction threshold. No birth/chart/model/rank information was supplied to the planner.

After sufficient additional neutral measurements are collected:
1. create a new immutable private measurement freeze;
2. rerun independent neutral coding;
3. freeze/adjudicate the final neutral profile;
4. only then apply the historical post-freeze owner-recovery crosswalk and birth search.

No birth-recovery result has been claimed from the incomplete profile.

## Incremental repaired-route progress

- `F0` / `D05.audience_adaptation`: **sufficient** after one narrow missing-piece clarification.
- `G17` / `D16.challenge_threshold`: **sufficient** from the matched consequence comparison; the optional reason probe is suppressed because the answer already supplied the reason.
- `WORKING-METHOD` / `D04.change_threshold`: **sufficient** from the recurring-friction scenario; the feasibility condition is preserved.
- `D0` / `D22.repetition_value`: **sufficient** for this specific pronunciation practice; repetition is valued while it is producing improvement and helping avoid habituating an inferior pronunciation.
- `G20` / `D19.resources_purpose`: **sufficient** for the normalized one-month extra-money amount; multiple intended functions are preserved without a fabricated rank order.
- `G01` / `D01.approach`: **closed unassessed**; the participant would seek explanation from another person or AI, which is useful behavior but does not establish personally organizing the messages by topic.
- `G03` / `D03.return_pattern`: **sufficient** after the narrow follow-up established that the unresolved question returns after full refocus.
- `G21` / `D21.ordinary_rhythm`: **sufficient** after the narrow follow-up established flexible state/need-dependent timing on a free day.
- `G02` / `D02.audience_use`: **sufficient** after the narrow follow-up established listener-contingent information selection.
- private working measurement: **78 answers**.
- next target-blind material route: narrow `G10` follow-up / `D10.stable_direction`.

Raw responses and participant-specific coding remain outside Git.

## G10 final-admission process repair

The first planner-generated G10 follow-up was **not asked for evidence credit** and is invalidated. Owner feedback exposed that it did not re-establish the nonadjacent group scene and asked a nearly universal broad join-decision question. Fresh target-blind audit confirmed failures in context binding, premise sufficiency, and discrimination.

The generating condition was repaired: planner output is now proposal-only, and the exact rendered question must pass context binding, premise sufficiency, discrimination, nonredundancy, construct alignment, and single-task admission before it may be shown. `verify_v7.py` now mechanically checks that this contract remains present.

Two attempted repairs were also rejected by the new gate. The third wording passed all six checks and is the only active G10 prompt. Private measurement remains **78 answers** because owner process feedback is not participant evidence for the invalid question.

## Final v2 natural stop and neutral-profile freeze

Target-blind questioning stopped naturally after the repaired G10 answer. G10 remained **partial**, and a fresh stop planner found no remaining neutral route with enough expected information gain to justify another owner turn.

Private immutable measurement v2:
- participant answers: **79**
- measurement freeze SHA-256: `6f49806cc086ba41d23d31882b6ccc218cef78f94d7599830f5a9a2b994737ba`
- minimal target-blind packet SHA-256: `411c9f8e24017fe412986f9ffeb35e396afc9b1213d86b38860329bb4a39d06b`

Fresh full-profile neutral coding on that exact packet:
- coder A SHA-256: `c3927ef06198a7208c2cdad7961b6c4690c0c6003d322a24dea18fb4dc158294`
- coder B SHA-256: `b02d36c0c123558cbf26b912c2f0b41ccb43a52f97a38ff8c2ed954d2a3517e0`
- stable disagreements: **14 / 73 facet statuses**, **6 / 31 domain statuses**
- fresh target-blind adjudication SHA-256: `cd8d69b43a0b6be0e208ada7304046ed596eec6a74af61700655a24b4560644d`

Frozen final neutral profile:
- SHA-256: `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`
- facets: **45 sufficient / 12 partial / 5 unknown / 8 inapplicable / 3 unassessed**
- domains: **14 full / 12 partial / 5 uncovered**

No participant-specific findings or raw answers are stored in Git. This closes Stage B and admits the post-freeze target-aware dual-translation stage.

The question-admission repair is also strengthened to seven checks: context binding, premise sufficiency, discrimination, nonredundancy, construct alignment, single response task, and expected information gain. Focused verifier: **497 / 497 PASS**.

## Post-freeze scorer translations

Both scorer-input translations were derived from the same frozen target-blind neutral profile and frozen before either new candidate ranking was opened.

- final neutral profile SHA-256: `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`;
- V1.1 merged translation SHA-256: `4211b1ee3941b1dabf5aba3677386cda1a68837a11ebbaa6ac618040f9ac5aa2` (19 rows);
- clean V4.3/NetInformation translation SHA-256: `310a0aea90400d1adf97b935ac370e58fb4c5f99ca5f4df56a8a8072fe42b0f3` (19 rows);
- translated profile contents remain private/outside Git; only hashes/counts/method are public.

The survey-instantiated V4.3 adapter excludes non-crosswalk historical behavioral clusters and post-selection carriers, treats historical CoreFit as constant/unavailable, and does not let historical core-field changes split score-identical intervals for the duration tie-break.

The original V1.1 one-off scanner has not been recovered from Git history, old local workspaces/sessions, dangling objects, or its August 24 workflow history. Any reconstruction must reproduce the frozen historical result before it may score the new translation.

## Scorer execution result

- survey-instantiated clean V4.3 result: **COMPLETED**; result SHA-256 `077a5ad94e9647855ac7c3f68b1ed706a9b6febbbc5a5d322c36a68dd7d806a3`; 2013 interval rank 1; best recorded-local-date interval rank 872; exact recorded-moment interval rank 1562; no post-result retuning permitted.
- historical V1.1 merged scorer: **TECHNICALLY UNRESOLVED**; exact old implementation/predicate semantics not recoverable; new frozen V1.1 translation remains unscored because the historical-reproduction gate was not satisfied.
- no additional participant questions are admitted from these results.
