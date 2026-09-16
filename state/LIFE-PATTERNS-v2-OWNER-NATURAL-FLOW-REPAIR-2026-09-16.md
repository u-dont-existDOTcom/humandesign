# Life Patterns v2 — owner natural-flow repair — 2026-09-16

## Owner finding

Direct owner testing exposed three coupled consumer-seam problems:

1. **Progress/liveness location:** `Continue interview` could scroll to a progress/status surface near the top of the page and then fail to return to the current interaction. Even when the second scroll worked, the up/down trip was unnecessary.
2. **Measurement completion versus synthesis:** a coverage area could be adequately measured and then surface a tentative synthesis that mainly repackaged the participant's immediately preceding statements. A section being complete is not by itself a reason to manufacture a participant-adjudicated Life Pattern.
3. **Decision liveness:** after a synthesis appeared, participant judgment could leave all synthesis buttons disabled under `Working on it…` because adjudication synchronously triggered another model-driven coverage pass.

No private interview narrative is stored here. The supplied owner audit snapshot was used only as direct development evidence for these abstract product findings.

## Causal mechanisms

### Status location / scrolling

The progress and request-liveness cards were placed near the page top and `showWorking()` scrolled to that card. The product therefore coupled *status visibility* to *navigation away from the current action*. Returning to the question/synthesis depended on a second asynchronous scroll.

### Measurement completion / synthesis

The planner had useful states for `ask another question` and `surface_hypothesis`, but no explicit successful state for:

> the current measurement area now has enough information, while any person-level synthesis would be little more than an obvious paraphrase.

That missing state made scientific coverage completion leak into participant-facing pattern adjudication.

### Participant decision / remote enrichment

Coverage had already been assessed when a synthesis was surfaced. Nevertheless, accepting/rejecting the synthesis called another LLM-backed coverage assessment before the HTTP response completed. An authoritative participant decision was therefore blocked on redundant remote enrichment.

## Repair

### Progress and liveness stay at the active end

The existing `operationStatus` and `interviewProgress` DOM nodes are moved to the end of the main interview container at runtime. The app no longer requires a top-of-page status excursion followed by a return scroll.

### Explicit `topic_complete` planner outcome

The target-blind interviewer may now close a local measurement area without creating a Life Pattern when:

- the current material is specific enough for the measurement need;
- another question has low expected information gain; and
- a proposed synthesis would mainly restate or enumerate what the participant just said.

`topic_complete` is an interview/workflow state only. It does **not** modify the accepted Life Patterns v2 semantic contract or automatically create a person-level pattern. The UI shows that the area is covered and exposes the finite `Continue interview` / finish frontier.

A participant-adjudicated synthesis is now reserved for cases where the model identifies a genuinely useful person-specific integration such as a conditional, contrast, boundary, recurring sequence, or other compression that is materially more informative than the immediately preceding statements. Explanatory surprise is not required; obvious paraphrase is insufficient reason to spend participant adjudication burden.

### Manual escape for a synthesis that slips through

Model classification is not assumed perfect. When a surfaced synthesis is true but obviously just restates what the participant said, the synthesis-review panel now includes:

**True, but too obvious — just move on**

That action closes the local measurement area using the already-computed coverage evidence, clears the ephemeral draft, and creates **no** v2 pattern proposal or participant adjudication. This also provides a correct exit for exact recovery checkpoints created by an earlier app version that already contain an over-obvious draft synthesis.

### Fast participant adjudication

When a real synthesis is surfaced, the in-thread coverage report is already cached. `Yes — keep that`, rejection, and the other terminal judgments now commit through the deterministic v2 adjudication core and reuse the cached coverage metadata. They do not launch a second LLM coverage pass.

This removes the redundant slow dependency that could leave buttons disabled under `Working on it…` after the synthesis had already arrived.

### Recovery

Exact audit/recovery snapshots now preserve whether the current workflow ended in `topic_complete`, so refresh/recovery returns to a continuation frontier rather than a blank composer.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_natural_flow.py`
- `src/hdmatch/api/life_patterns_v2_owner_natural_flow_ui.py`
- `tests/unit/test_life_patterns_v2_owner_natural_flow.py`
- deployment wrapper: `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`

Application source deployed: `78f674c471557d9b9ba8b567b080a75d29c45301`.

Regression checkpoint: `130d790326f4f88b393b1942da13d532ce816fd8`.

## Verification

GitHub Actions run `35154728412`: **SUCCESS**.

- unit/integration tests: PASS
- Ruff: PASS
- strict mypy: PASS

Railway deployment `350a756e-523f-4515-a26c-065166b9666d`: **SUCCESS** from application source `78f674c471557d9b9ba8b567b080a75d29c45301`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

The branch/PR remain development-only; no merge/release or external participant collection is authorized.

## Mission Control

The privacy-bounded logic lessons are durably captured on the existing UDA Mission Control correction branch as:

`feedback/mission-control/SDF-20260916-LIFE-PATTERNS-NATURAL-FLOW-017.json`

Truth state remains `CAPTURED_BRANCH_ONLY`.

## Next consumer-seam check

On refresh/recovery:

1. `Continue interview` should keep the working/status/progress surfaces at the active end rather than jumping to the page top;
2. a locally complete area whose only available synthesis is an obvious paraphrase should normally close as **area covered** rather than require synthesis approval;
3. if an obvious synthesis still slips through — including one restored from an older checkpoint — **True, but too obvious — just move on** should close the area without recording a Life Pattern;
4. a genuinely useful synthesis should still surface normally;
5. `Yes — keep that` / reject should return promptly and synthesis buttons must not remain frozen under `Working on it…`;
6. progress and exact audit/recovery must remain intact.

After these product seams pass, the next scientific boundary remains a fresh target-blind measurement freeze followed by the narrowly authorized owner DOB/time recovery regression against the frozen historical benchmark.
