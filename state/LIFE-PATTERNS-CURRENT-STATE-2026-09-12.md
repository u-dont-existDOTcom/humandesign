# Life Patterns current state — 2026-09-16

V2 independent semantic review remains **PASS**. Semantic change required: `false`.

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER RECOVERY/PROGRESS/LIVENESS RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, participant authority over person-level patterns, and the episode-fact/person-pattern firewall.

No private owner interview narrative is stored in Git. Only abstract product/logic findings and mechanical regression evidence are durable.

## Current architecture

`participant-led characteristic material -> dynamic target-blind interviewing against fixed 23-dimension recoverability surface -> periodic in-thread coverage estimate -> ephemeral working synthesis -> participant judgment -> v2 proposal/adjudication materialization -> exact browser-local working-ledger audit/recovery -> local SHA-256 measurement freeze -> owner-only post-freeze DOB/time recovery regression`

The runtime receives no chart, birth target, expected answer direction, target mapping, candidate score/rank, or historical AstroHD crosswalk.

## Working-ledger recovery boundary

Browser recovery preserves the exact current *working* hidden ledger for crash recovery and audit. Exactness does not imply correctness: a restored checkpoint remains unvalidated and does not become canonical/scientific data merely because it can be resumed.

Participant controls include **Download audit/recovery snapshot** and **Import audit/recovery snapshot**. Older visible-transcript-only files can be used for development continuity; their hidden ledger was never saved, so any reconstructed ledger remains explicitly non-scientific.

Private narrative is not persisted to Git or a Railway volume.

## Latest consumer-seam repair: progress hydration + request liveness

The owner supplied a private recovery checkpoint after accepting a reconstructed synthesis. That checkpoint showed materially incomplete scientific coverage, while the UI had remained at `Preparing…` and then claimed **Interview coverage is complete** after `Continue interview`.

The generating condition was exact and mechanical: recovery restored coverage rows but bypassed the fresh-session bootstrap that loads the fixed 23-dimension coverage blueprint. With an empty blueprint, the progress renderer looked uninitialized and the missing-dimension predicate saw an empty universe as zero missing.

This is repaired in:

- `src/hdmatch/api/life_patterns_v2_owner_liveness_ui.py`;
- `src/hdmatch/api/life_patterns_v2_owner_liveness.py`;
- the deployment wrapper now serves the liveness-aware surface.

Every restore/import path now loads the real coverage blueprint before restored progress or completion is evaluated. `Continue interview` also ensures the blueprint is present before testing whether anything remains open.

Long-running user actions now expose a separate request-liveness surface with an indeterminate progress bar and explicit status. Current messages include:

- **Rebuilding the recovered interview and preparing a synthesis…**;
- **Saving that and updating interview progress…**;
- **Choosing the next useful question…**.

Scientific interview progress and request-liveness progress are separate concepts.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-RECOVERY-PROGRESS-LIVENESS-REPAIR-2026-09-16.md`.

## Existing participant-facing rules retained

- simple is fine; generic is not;
- fixed scientific constructs do not imply fixed question order;
- one natural answer may cover several dimensions;
- completed material is skipped and partial material asks only for the missing discriminator;
- broad labels preserve cross-domain scope;
- self/observer, inner/outer, automatic/deliberate and other discriminators are used selectively;
- free-form chat remains available in every nonfinal synthesis state;
- `Keep investigating` is the single visible generic refinement action;
- `Continue interview` is the finite default after a settled pattern;
- `Explore another pattern` is not visible;
- progress reports **measurement areas still open**, not remaining questions;
- action-oriented scrolling keeps the next answer/judgment surface visible;
- long-thread planning treats semantic rewording of already answered questions as repetition;
- participant finalization remains transactional;
- working syntheses remain ephemeral until participant judgment.

## Recoverability criterion

The active `life-patterns-recoverability-coverage-v2` blueprint has 23 required neutral dimensions with explicit `unassessed`, `partial`, `sufficient`, `unknown`, `inapplicable`, and `declined` states.

Coverage alone cannot pass the owner's hard development criterion. After a fresh target-blind interview is frozen locally, the historical owner AstroHD procedure must still achieve:

- exact recorded moment hourly rank no worse than **#2**;
- correct date as the **#1 distinct refined neighborhood**;
- refined peak within **11 minutes** of recorded time.

## Verification / deployment

Exact liveness-aware application head: `625ec596fd4098096357f5cb3c7bee522ce4d5ea`.

Regression checkpoint: `a71ab72d39dd46c0793ac5ec207640bf62186e21`.

GitHub Actions run `35115906379`: **SUCCESS** — unit/integration tests PASS, Ruff PASS, strict mypy PASS.

Railway deployment `54e829be-6fe5-4570-9321-609468b414ff`: **SUCCESS** from the exact application head; application startup completed and `/healthz` returned HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. This does not authorize external participant collection/recruitment.

## Mission Control capture

Owner-explicit reasoning/product-logic corrections remain durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127, truth state **`CAPTURED_BRANCH_ONLY`**.

Newest privacy-bounded record: `feedback/mission-control/SDF-20260916-LIFE-PATTERNS-LIVENESS-AND-BLUEPRINT-HYDRATION-015.json`.

## Current gate

Owner consumer-seam retest should now verify:

1. recovered progress resolves from `Preparing…` to an actual approximate percentage/open-area count;
2. reconstruction, acceptance, and continue-interview operations visibly show an in-flight working state;
3. `Continue interview` advances into remaining dimensions rather than falsely reporting completion;
4. long threads still avoid semantic duplicate questions and can end in an actual current synthesis;
5. after these product seams pass, run a fresh target-blind interview and freeze it before DOB/time scoring.

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware questioning, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
