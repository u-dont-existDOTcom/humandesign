# Scenario-first survey v7 redesign rationale — 2026-09-22

## Why v7 exists

The v6 graph-converged bank survived synthetic/design review but still produced repeated failures in a real saved Chat pilot. The redesign treats those live failures as product evidence about question construction and interviewer routing, while keeping raw participant answers private.

This is a behavior-only survey redesign. It does not use chart/birth cues, does not score the pilot participant, and does not claim AstroHD or population validity.

## Main redesign mechanisms

1. **Premise sufficiency gate** — do not ask a question when the respondent must invent the main motive, baseline, cause, workload, environment, or trade-off.
2. **Construct-discrimination gate** — suppress tautological or near-universal questions whose ordinary answer carries little useful information.
3. **Redundancy gate** — do not ask paraphrases, mirrored opposites, or causes/limits already supplied in earlier answers.
4. **Missing-piece follow-up rule** — acknowledge answered clauses and ask only the one missing target instead of replaying the scene.
5. **Context-dependence rule** — “it depends” plus named conditions is evidence, not a failure to produce a global trait.
6. **Natural-stop rule** — empty coverage fields never justify filler questions.

## Canonical bank changes

v7 has 79 canonical nodes, down from 79. `C0` was retired because it had no planning target and the live pilot showed no reason to ask it merely as an extra scene.

Known live-failure repairs are incorporated directly into the candidate:

- `G23`: shared-meal people/setting and “no assigned job” are explicit.
- `VERIFY`: suppressed when the respondent already resolves conflict by returning it to the group/source or has another checking method.
- `WORKING-METHOD`: replaced the trivial “working method” contrast with recurring friction in a method that otherwise works.
- `D0` / `PRACTICE-REASON`: repetition value is tied to one exact pronunciation practice instead of a generic boring-practice question.
- `M05` / `M06`: the cue is familiarity-dependent by construction; direct constraints/hazards do not enter the transfer probe.
- `M09`: old/new planning systems now have concrete properties and switching costs.
- `M11`: the reason for the proposed exchange is explicit rather than hidden.
- `R07` / `R08`: workload, duration, temperature, sleep/food, and recovery conditions are concrete.
- `R10`: slow progress is replaced with persistent internal disagreement after attempted repair.
- `STATUS`: asks intrinsic reward of genuine admiration directly instead of defining away all useful consequences.
- `ROMANCE-FADE`: asks only for additional weakening pathways beyond already-named closeness dimensions.

## Exploratory item

The cross-person sensory-conflict/mold question is retained separately as `EX-SENSORY-CONFLICT-01`. It is explicitly unmapped and receives no automatic AstroHD evidence credit. This preserves a potentially useful behavioral dimension without contaminating canonical scoring or pretending its mapping is known.

## What v7 is not

v7 is not a runtime implementation, shortened validated interview, psychometric instrument, population norm, chart decoder, or proof that the target theory is recoverable from behavior. It is the next text-only survey candidate after a live usability/semantic pilot.
