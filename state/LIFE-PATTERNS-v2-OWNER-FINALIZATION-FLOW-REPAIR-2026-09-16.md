# Life Patterns v2 — synthesis finalization and finite continuation repair — 2026-09-16

## Owner findings

Direct owner use exposed three related participant-facing defects:

1. a red `multiple adjudications` validation error could appear around final synthesis acceptance;
2. the two visible actions `Keep trying to pin it down` and `No — keep investigating` did not communicate a useful participant-level distinction;
3. after accepting a pattern, offering both `Continue interview` and `Explore another pattern` made the otherwise finite scientific instrument feel capable of branching indefinitely.

No private interview narrative is persisted here.

## Causal mechanism for duplicate adjudication

`RecoverabilityCoverageSession.adjudicate()` performed two dependent operations in sequence:

1. mutate the participant-adjudicated pattern record;
2. call the coverage assessor and attach the updated coverage report.

Those operations were not enclosed in one outer transaction. If step 2 failed, the browser received an error even though step 1 could already be committed in the in-memory session. A participant retry could then attempt to adjudicate the same proposal again, and the v2 contract correctly rejected the resulting second adjudication as `proposal ... has multiple adjudications`.

The UI also lacked an in-flight decision guard, leaving a second duplicate-request path through rapid/repeated clicks.

## Repair

### Transactional finalization

`TransactionalRecoverabilityCoverageSession` now snapshots the complete conversational/core state before adjudication. The participant decision plus post-decision coverage assessment either return successfully together or the complete snapshot is restored. A successful finalization clears the active proposal pointer so the settled proposal cannot be adjudicated again through the same session frontier.

The browser additionally blocks repeated in-flight synthesis decisions and temporarily disables synthesis controls until the request resolves.

### One clear continuation meaning

The visible nonterminal synthesis action is now simply **Keep investigating**. It means: do not settle the current synthesis yet; ask one more discriminating question.

The former separate visible `No — keep investigating` action is removed from the participant surface. If the participant already knows what the synthesis gets wrong or misses, the always-visible chat box is the direct correction path. `Close — I’ll explain what needs changing`, exact-wording editing, `Reject and stop this thread`, and `Leave it unresolved for now` retain their distinct purposes.

### Finite post-acceptance path

After a settled pattern, **Continue interview** is the primary continuation. The visible `Explore another pattern` branch is removed. The adaptive coverage selector already has authority to ask about a new pattern or domain when that is the highest-information next move, so a separate unlimited participant-created branch was redundant and undermined the finite completion horizon.

The persistent progress indicator remains the burden/completion reference.

## Verification

Application code head: `cef6ad16546448355a3e624016b46333b2730573`.

Regression tests include rollback after simulated post-decision failure, successful active-proposal closure, transactional session construction, single visible investigation path, duplicate-click protection, and finite post-acceptance continuation.

GitHub Actions run `35044113034`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `6126c7b7-d207-4552-a12f-65304be89ea5`: **SUCCESS** from application head `cef6ad16546448355a3e624016b46333b2730573`.

Runtime evidence:

- application startup completed;
- `GET /healthz` returned HTTP `200 OK`.

## Mission Control

The exact non-sensitive owner correction and the three logic mechanisms were captured on the existing isolated Universal Development Architecture feedback branch as:

`feedback/mission-control/SDF-20260916-LIFE-PATTERNS-FINALIZATION-CHOICE-FLOW-010.json`

Capture truth remains `CAPTURED_BRANCH_ONLY`; the Mission Control PR remains draft/open/unmerged.

## Next evidence boundary

Owner consumer-seam retest on a fresh browser session:

1. accept one surfaced synthesis once; no duplicate-adjudication error should appear;
2. verify there is only one visible `Keep investigating` continuation choice and that specific objections can be typed directly;
3. after acceptance, verify `Continue interview` is the primary finite path and `Explore another pattern` is not visible;
4. continue the target-blind interview, freeze/export the final measurement, then run the already-authorized owner-self DOB/time recovery regression.
