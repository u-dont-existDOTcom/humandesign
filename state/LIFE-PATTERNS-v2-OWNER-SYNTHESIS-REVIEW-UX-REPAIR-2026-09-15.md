# Life Patterns v2 synthesis-review UX repair — 2026-09-15

Status: **IMPLEMENTED / CI GREEN / LIVE — OWNER RETEST REQUIRED**.

## Owner finding

Direct owner use exposed a nonfinal-state UI defect in synthesis review. The `Close, but change it` path conflated two different participant intents:

1. explaining what the current synthesis gets right/wrong or what scope remains untested;
2. authoring the exact replacement proposition to be recorded.

The UI treated free-form explanatory feedback entered into the revision textarea as if it were exact replacement wording, then immediately asked grounding/final-status questions about that text. At the same time, the ordinary chat composer was hidden in a proposal state unless an explicit refinement mode had already been entered. This made the button/form choices act like a forced-response frontier even though the underlying interview remained nonfinal.

No private owner interview narrative is stored here.

## Causal mechanism

The product projection had a state-machine mismatch:

- authoritative state: active proposal remains open to refinement;
- UI projection: `Close, but change it` entered a participant-authored-final-wording form;
- free-form continuation capability: hidden during ordinary proposal adjudication;
- unsupported/other-situation revision grounding: auto-submitted as unresolved instead of exposing another executable conversational step.

Thus `feedback_on_synthesis` and `participant_authored_exact_revision` were collapsed into one UI path.

## Repair

The live recoverability UI now:

- keeps the chat composer visible whenever a synthesis proposal is still active;
- states that buttons are shortcuts and free-form chat is always available in this nonfinal state;
- splits the old revision action into:
  - `Close — I’ll explain what needs changing` → ordinary conversational feedback;
  - `Edit exact wording myself` → explicit participant-authored replacement wording;
- labels the exact-wording editor as exact recorded wording rather than an explanation box;
- adds `← Back to synthesis choices`;
- makes the final exact-wording status question explicit (`Accept`, `Reject`, or `Leave unresolved`);
- when exact wording depends on other situations or grounding is uncertain, returns to chat instead of auto-finalizing the thread as unresolved;
- collapses stale exact-wording controls when the participant resumes free-form chat.

The accepted Life Patterns v2 evidence semantics and target-theory-blind runtime boundary are unchanged.

## Verification

Application head: `d281ce7433c261585115c571384d099595b96cce`.

Regression/test head: `a601b4c10261c6afefe51bb149809e4e16e930f7`.

GitHub Actions run `35019754274`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

Railway deployment `eabec6ca-5622-4f91-a953-ece4f2bef088`: **SUCCESS** from application head `d281ce7433c261585115c571384d099595b96cce`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP `200`.

## Next owner check

Refresh/reopen the live interview and reproduce the synthesis-review point.

PASS requires:

1. the chat box remains available while the synthesis buttons are visible;
2. `Close — I’ll explain what needs changing` focuses the free-form chat path rather than asking the participant to manufacture exact wording;
3. `Edit exact wording myself` is clearly separate and reversible with Back;
4. grounding that depends on undiscussed situations leads back to conversation rather than silently terminating as unresolved.

The owner recoverability/DOB-time regression gate remains the larger active task after this UI seam is judged.
