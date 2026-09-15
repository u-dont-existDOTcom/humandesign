# Current state

## Life Patterns — 2026-09-15

Active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

V2 independent semantic review remains **PASS** with zero blockers and `semantic_change_required=false`.

The accepted hidden substrate is unchanged: open-world episode facts plus participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

The participant-facing interview is deliberately simpler and more selective than the internal evidence machinery.

## Product evidence so far

The surfaced fact-review/paraphrase workflow is **FAILED / REPLACED**.

The hidden-ledger pattern-first replacement produced useful non-parroting information gain in one bounded owner session and was judged **GOOD / PASS / PRELIMINARY POSITIVE**. Multi-pattern continuation was added. Later owner testing exposed and repaired:

- uncertainty being terminalized;
- `No` terminating the whole pattern inquiry;
- unsupported comparative/cross-context synthesis;
- severe over-interrogation caused by assistant-added multi-episode/counterexample/audit requirements;
- recurrence being mistaken for person-specific signal;
- most recently, `Keep trying to pin it down` repeating the existing synthesis and broad self-evaluations lacking self/observer triangulation.

No private owner interview narrative is committed. Only abstract product findings are preserved.

## Current product principle: target-aware instrument, target-blind runtime

The owner explicitly clarified that Life Patterns is intended to produce evidence useful for later astrology / Human Design analysis **and** for InnerSignal.

The controlling distinction is now:

- **instrument design may be target-aware**: development may intentionally prioritize neutral behavioral dimensions because they are likely to discriminate person models useful downstream;
- **runtime interviewing remains target-blind**: the interviewer does not receive the participant's chart, target-model mapping, expected answer direction, score, or hidden theory label, and participant-facing questions remain behavior-first.

Scientific blindness therefore prohibits chart-aware routing and target leakage. It does **not** require an instrument that is indifferent to which behavioral information is useful.

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-OBSERVER-TRIANGULATION-AND-REFINEMENT-REPAIR-2026-09-15.md`

## Current participant-facing method

The live owner candidate now combines:

1. **person-specificity admission** — recurrence alone is not enough; clearly generic/high-base-rate regularities are redirected before evidence collection;
2. **adaptive burden control** — another question is admitted only when plausible answers could materially change the person-level formulation;
3. **neutral discriminating elicitation** — the interviewer selects the one unresolved dimension most likely to change the formulation rather than mechanically asking for another episode;
4. **participant authority** — person-level synthesis remains tentative and adjudicated by the participant.

### Familiar-observer triangulation

For broad evaluative self-labels, an early high-value discriminator may be whether people who know the participant well tend to describe them similarly or differently, and whether outward presentation differs from inner experience.

Evidence sources remain distinct:

- participant self-description;
- direct behavioral/event report;
- participant-reported observer impression.

A familiar-observer report is useful evidence about externally visible reputation or self/observer convergence/divergence, but remains attributed secondhand evidence rather than verified objective truth.

### Neutral high-value discriminator menu

The model may select from these **only when the answer can materially change the formulation**; this is not a checklist or completion quota:

- self-view vs familiar observer-view;
- inner experience vs outward presentation;
- baseline vs triggered state and recovery;
- automatic first response vs deliberate/learned management or compensation;
- context/domain stability;
- timing, threshold, intensity, duration, escalation, stopping, recovery;
- developmental continuity/change and learned adaptation;
- decision phenomenology and immediate vs delayed clarity;
- social entry/role: self-initiation vs response/recognition, one-to-one vs group, role acceptance/resistance;
- energy, sustainable engagement, overload, stopping, retreat/restoration;
- capacity vs preferred use, especially communication/persuasion/leadership/care/confrontation;
- relating, reciprocity, sensitivity, conflict, repair/withdrawal, trust and boundaries;
- attention, cognition, focus, interruption, learning, novelty/continuity, persistence/stopping;
- values, purpose and salience—what reliably mobilizes effort or is easy to ignore;
- sensory/environmental conditions that materially change functioning;
- coexisting modes that differ by context, role, intensity, or timescale rather than forcing one trait pole.

The same neutral person-model distinctions are useful to InnerSignal without requiring external-theory language in participant-facing interviewing.

## `Keep trying to pin it down` repair

The previous path reused the ordinary synthesis planner. If that planner returned another `surface_hypothesis`, the refinement wrapper converted its move type to `follow_up` while preserving the same reply, which allowed the product to repeat the existing synthesis verbatim or nearly verbatim.

The live path now uses a dedicated refinement planner:

- `surface_hypothesis` is not allowed on the initial refinement call;
- the prompt explicitly forbids repeating, restating, lightly rephrasing, or re-presenting the current synthesis;
- the button action is recorded as a conversational user turn;
- the model must ask at most one genuinely decision-changing new question or say no high-value unresolved discriminator remains;
- a defensive fallback turns any attempted repeated synthesis into a new observer-triangulation question.

Answers during refinement continue through the same dedicated reasoning path.

Current limitation: post-proposal refinement evidence does **not yet automatically generate a revised formal proposal**. Participant manual revision/adjudication remains available. Any later automatic proposal revision must preserve post-proposal provenance rather than laundering later evidence into pre-proposal support.

## Verification / deployment

Current application/code checkpoint: `b46d480acf2209b5416f6ef158fd64de32a5358a`.

Focused regression/test checkpoint: `17ef230d51c2298ac6ca0a69c5cc4c3922b4a46d`.

GitHub Actions run `34915009454`: **SUCCESS**. The preceding behavior/test run established **736 passed / 7 skipped**, Ruff passed, with only a static typing issue at the dynamic refinement boundary; the final checkpoint passes tests, Ruff, and strict mypy.

Existing authenticated owner-only Railway service reused:

- deployment: `f4a49e7d-b0b1-4929-a3ad-9bbb11092ef6`;
- source: `b46d480acf2209b5416f6ef158fd64de32a5358a`;
- status: **SUCCESS**;
- application startup complete;
- `/healthz` -> HTTP `200`;
- health contract includes `person_specificity_gate=true`, `observer_triangulation=true`, `neutral_person_model_discriminators=true`, `refinement_repetition_guard=true`, `adaptive_information_gain_gate=true`, `fixed_episode_quota=false`, `mandatory_counterexample_gate=false`.

No new service, broadened access, automatic transcript persistence, target scoring, chart-aware runtime routing, Railway volume, or request-body logging was introduced.

## Next gate

Strategy efficacy: **TARGET-AWARE NEUTRAL INSTRUMENT / TARGET-BLIND RUNTIME CANDIDATE — OWNER RETEST REQUIRED**.

Next owner evidence:

1. Start with a broad self-description. When informative, the first clarification should prefer familiar-observer convergence/divergence or inner-vs-outer presentation rather than demanding an arbitrary episode.
2. After a synthesis, click `Keep trying to pin it down`. The next interviewer turn must contain genuinely new inquiry, never the same synthesis again.
3. Answer that question and judge whether the interviewer uses the new evidence without reopening settled material or marching through the discriminator menu.
4. Test another high-value domain such as decision timing, relationships/conflict, attention/work, energy/recovery, or values/purpose.
5. If within-pattern behavior is good, the next architecture decision is whether to add a **light adaptive cross-pattern coverage sweep** so important under-observed domains are not missed simply because the participant did not spontaneously volunteer them.
6. `Finish for now` summary utility still requires direct owner judgment before durable persistence / a real Life Patterns Map is authorized.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**