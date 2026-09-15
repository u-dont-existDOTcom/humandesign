# Current state

## Life Patterns — 2026-09-15

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Only abstract product findings, neutral measurement definitions, historical development metrics, and synthetic/mechanical regressions are preserved.

## Product strategy

The participant-facing strategy is now:

**target-aware instrument design / target-blind runtime execution / local pre-scoring freeze / post-freeze owner recoverability regression**.

Development may intentionally require neutral behavioral dimensions that are useful for later astrology / Human Design analysis and InnerSignal, but the runtime interviewer receives no participant chart, birth target, expected answer direction, target-model mapping, candidate score/rank, or historical recovery crosswalk.

The interviewer retains:

- person-specificity admission: generic high-base-rate regularities are not promoted to Life Patterns;
- adaptive burden control: no arbitrary episode or counterexample quota;
- familiar-observer / self and inner / outer triangulation when informative;
- dedicated non-repetitive refinement after an imperfect synthesis;
- participant authority over person-level synthesis;
- explicit preproposal versus postproposal evidence timing;
- explicit standardized coverage and missingness states.

## Owner hard criterion: the new instrument must preserve birth-recovery information

The owner established a stronger development acceptance criterion: if the new standardized interview cannot preserve enough behavioral information for the historical owner AstroHD procedure to recover the owner's known DOB/time at least as well as before, **the instrument fails**.

This is an owner development regression criterion, not untouched human validation of astrology or Human Design.

Historical benchmark:

- century hourly candidates: 876,601;
- exact recorded moment historical merged rank: **#2**;
- leading hourly state: same recorded date, 17 minutes later;
- recorded date: **#1 distinct local refined neighborhood**;
- best refined minute: **11 minutes** from the recorded time.

Frozen baseline:

`reference/research/life_patterns_astrohd_owner_recovery_baseline_v1.json`

Executable gate:

`src/hdmatch/evaluation/life_patterns_owner_recovery_gate.py`

The gate requires the same declared historical search procedure, correct date as the top distinct refined neighborhood, exact recorded hourly rank no worse than #2, and absolute refined-peak offset no worse than 11 minutes. **Coverage completion alone cannot pass.**

## Why the 10-domain blueprint was superseded

The prior `life-patterns-required-coverage-v1` candidate correctly introduced standardized coverage mechanics, but its 10 broad domains were too coarse for the new recoverability criterion. A domain such as cognition, communication, values, or environment could become `sufficient` after only one narrow facet was learned, while historically score-bearing distinctions inside the same broad bucket remained unmeasured.

The broad 10-domain partition is therefore superseded as the active recoverability candidate. Its useful mechanics remain: version/hash, explicit coverage states, evidence-citation requirements, adaptive neutral screeners, and the `Continue required coverage` flow.

## Recoverability coverage v2

Active blueprint version:

`life-patterns-recoverability-coverage-v2`

Runtime files:

- `src/hdmatch/api/life_patterns_recoverability_domains.py`
- `src/hdmatch/api/life_patterns_v2_owner_recoverability.py`
- `src/hdmatch/api/life_patterns_v2_owner_recoverability_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`

The v2 blueprint contains 23 neutral required dimensions:

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

Natural participant-led evidence can satisfy multiple dimensions; fixed wording is not required when existing evidence already establishes the dimension. Coverage states remain `unassessed`, `partial`, `sufficient`, `unknown`, `inapplicable`, and `declined`; silence is never absence.

## AstroHD behavior-profile crosswalk

Frozen development-only crosswalk:

`reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json`

It verifies coverage against two evidence classes:

1. all **19 historical score-bearing behavior clusters** in the successful merged owner recovery;
2. all **19 clean V3.6 information-bearing observables** from the holistic-profile information audit.

Important distinction: score-bearing/information-bearing does **not** mean each individual feature has been proven necessary by leave-one-out ablation. No such necessity claim is made. The two explicitly post-selection V3.6 carrier refinements are excluded from required survey design.

The crosswalk is not imported by or exposed to the interviewer runtime. It is post-freeze-only.

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-ASTROHD-RECOVERABILITY-GATE-2026-09-15.md`
- `state/LIFE-PATTERNS-v2-OWNER-CLIENT-SIDE-MEASUREMENT-FREEZE-2026-09-15.md`
- `state/LIFE-PATTERNS-v2-OWNER-SYNTHESIS-REVIEW-UX-REPAIR-2026-09-15.md`

## Owner correction: synthesis review must remain conversational

Direct owner use exposed a nonfinal-state UI defect. The prior `Close, but change it` path collapsed two different participant intents:

1. explaining what the current synthesis gets right, gets wrong, or has not yet established;
2. authoring the exact replacement proposition to be recorded.

The revision textarea was actually wired as participant-authored final wording, but its presentation made explanatory feedback a natural response. The UI then asked evidence-grounding and final-status questions about that explanatory text. At the same time, ordinary chat could be hidden while a synthesis proposal was active. This made a nonfinal inquiry look like a forced-response form.

The live repair now enforces a coherent executable frontier:

- free-form chat remains available whenever the synthesis is still open;
- synthesis buttons are shortcuts rather than exclusive response channels;
- `Close — I’ll explain what needs changing` routes to ordinary chat;
- `Edit exact wording myself` is a separate explicit authoring path;
- the exact-wording editor has `← Back to synthesis choices`;
- its copy explicitly says that the textarea is the exact wording that would be recorded;
- if exact wording depends on undiscussed situations or the participant is unsure of its grounding, the UI returns to chat rather than auto-finalizing the pattern as unresolved;
- starting free-form chat collapses stale exact-wording controls while keeping the active synthesis inquiry open.

This is a participant-facing workflow repair only. The accepted v2 semantic substrate and target-theory-blind runtime boundary are unchanged.

## Pre-scoring measurement freeze

The live development browser exposes **Freeze/export measurement**. It creates a local JSON bundle from the completed participant-adjudicated pattern results and aggregate standardized coverage, retains per-pattern freeze hashes, computes a client-side SHA-256 `measurement_bundle_sha256`, and downloads the bundle locally.

The freeze/export action does not send the bundle to an AstroHD endpoint, Git, or Railway persistence. Its purpose is to make the measurement fixed before target-aware owner recovery scoring begins. The live interview model calls remain ordinary interview processing; the new freeze specifically prevents the later scoring step from feeding back into elicitation.

## Blinding and authority boundary

During interview execution the runtime must not receive:

- chart or known birth answer;
- historical target-model mapping;
- expected answer direction;
- candidate score/rank;
- post-freeze AstroHD crosswalk.

The owner has narrowly authorized **owner-self post-freeze recovery regression** after a fresh measurement is frozen. General target-model activity remains unauthorized, especially external-participant scoring.

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware questioning, external-participant target scoring, publication/validation claims, merge/release, production expansion, and unapproved spending.

## Verification and live development deployment

Current recoverability/synthesis-review application head: `d281ce7433c261585115c571384d099595b96cce`.

Current synthesis-review regression test head: `a601b4c10261c6afefe51bb149809e4e16e930f7`.

GitHub Actions run `35019754274`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `eabec6ca-5622-4f91-a953-ece4f2bef088`: **SUCCESS** from exact application head `d281ce7433c261585115c571384d099595b96cce`.

Runtime evidence:

- application startup completed;
- `GET /healthz` returned **200 OK**.

The development surface remains passwordless under the owner's prior explicit instruction. This does not authorize recruitment or external data collection.

## Current gate

**The synthesis-review defect is repaired in the live candidate, but owner consumer-seam judgment and the larger recoverability criterion remain open.**

Next:

1. owner refreshes/reopens and reproduces the synthesis-review point;
2. verify the chat box remains available while synthesis buttons are visible;
3. verify `Close — I’ll explain what needs changing` returns to free-form conversation rather than treating explanation as exact final wording;
4. verify `Edit exact wording myself` is explicit and reversible with Back;
5. verify undiscussed-situation or uncertain grounding returns to chat rather than silently terminating as unresolved;
6. if that seam passes, continue the target-blind recoverability interview;
7. click **Freeze/export measurement** and keep the downloaded JSON unchanged;
8. only after that local freeze, apply the historical owner AstroHD crosswalk/recovery procedure and evaluate the produced date/time signature with the executable regression gate;
9. if recovery is worse, revise the measurement design rather than weakening the historical benchmark.

PR #24 remains draft/open/unmerged.

**There was never a completion policy.**
