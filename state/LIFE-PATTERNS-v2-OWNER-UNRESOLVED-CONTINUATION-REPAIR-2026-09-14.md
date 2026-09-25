# Life Patterns v2 owner unresolved-thread continuation repair — 2026-09-14

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner product evidence

The owner tested a second fresh pattern thread on the deployed multi-pattern surface. The thread continued to produce new discriminating information after the first tentative synthesis, but the product converted uncertainty into a terminal `unresolved` result instead of offering an executable same-thread continuation.

This is a **workflow-liveness / adjudication-frontier defect**, not evidence that the pattern-first interview strategy itself failed. The strategy remains viable because the conversation was still generating useful distinctions when the UI stopped it.

No private interview narrative from the owner report is persisted in this receipt.

## Repair

The owner-only product layer now makes the choice explicit after a synthesis:

- `Keep trying to pin it down`;
- `Leave it unresolved for now`;
- the existing accept / revise / reject judgments remain available.

Choosing continuation keeps the same backend pattern session open and asks another discriminating question. Later participant answers can add post-proposal episode facts, but continuation does **not** silently write an `unresolved` adjudication and does **not** auto-create a replacement person-level proposal from evidence acquired after the first proposal.

This preserves the accepted v2 timing rule: post-proposal information remains post-proposal information. If the eventual participant-authoritative wording changes, the existing explicit revision/adjudication route remains the persistence boundary.

The unresolved consequence copy is intentionally target-neutral: leaving a thread unresolved means it contributes no settled person-level pattern to later analysis. The owner-proposed references to predictive power / astrological fit are not shown inside the pre-freeze interview because target-theory blindness remains binding and predictive performance has not been established.

## Implementation and verification

- owner refinement overlay: `src/hdmatch/api/life_patterns_v2_owner_refinement.py`;
- secured deployment wrapper routes the existing owner-only service through the refinement app;
- regressions: `tests/unit/test_life_patterns_v2_owner_refinement.py`.

Exact final verified code/test head: `21d6a4addfd5549ef2d81ce694e8e127bd3eecce`.

The first hosted run failed during test collection because FastAPI/Starlette `TestClient` required an uninstalled `httpx2` package. No product assertion had run. The unnecessary test dependency was removed; the composed app/session boundary is tested through the registered FastAPI endpoints directly instead of changing project dependencies.

GitHub Actions run `34872101510` on `21d6a4addfd5549ef2d81ce694e8e127bd3eecce`: **SUCCESS**.

- unit/integration tests: passed;
- Ruff: passed;
- strict mypy: passed.

Existing owner-only Railway service reused; no new service and no access broadening.

- service: `life-patterns-owner`;
- deployment: `a1aa5bdf-82f9-4e71-b7c9-9268eecea894`;
- application source head: `0d2aac5d65076f3ccc03e330c6696807ad5a7661`;
- status: **SUCCESS**;
- application startup complete;
- Railway runtime health request: `/healthz` -> HTTP `200`;
- the deployed code's health response contract includes `unresolved_thread_continuation=true`;
- later test/state-only commits are outside the Railway source watch surface.

Privacy boundary is unchanged: no automatic transcript persistence or request-body logging was added.

## Next decision-changing owner evidence

Use the deployed owner-only browser on a pattern that remains uncertain after a first synthesis. Choose `Keep trying to pin it down` and judge whether the interviewer actually continues the same thought with useful discriminating questions rather than forcing closure or starting over. Then explicitly settle, revise, reject, or leave the thread unresolved.

After that, use `Finish for now` and judge the session-level summary. Durable persistence / a real Life Patterns Map remains contingent on that owner product evidence.

**There was never a completion policy.**
