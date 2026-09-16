# Current state

## Life Patterns — 2026-09-16

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER NATURAL-FLOW RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Repository state contains abstract product findings, neutral measurement definitions, mechanical regressions, and privacy-bounded owner-authorized logic-correction receipts only.

## Current participant-facing architecture

**Target-aware instrument design / target-blind runtime / fixed 23-dimension recoverability surface / dynamic information-gain questioning / explicit local topic completion / selective person-level synthesis / in-thread progress at the active end / ephemeral working synthesis until participant judgment / low-latency deterministic adjudication using cached coverage / exact browser-local hidden-ledger audit/recovery / importable recovery snapshots / local pre-scoring freeze / owner-only post-freeze DOB-time recovery regression.**

Current behavior includes:

- person-specificity: recurrence alone is not useful if it is merely a high-base-rate human regularity;
- no arbitrary episode/counterexample quota;
- observer/self, inner/outer, context, scope, developmental, timing, and other neutral discriminators only when decision-changing;
- global-label scope preservation;
- fixed scientific coverage with adaptive order and wording;
- prior answers may satisfy multiple dimensions and should prevent duplicate later questions;
- long-thread planning keeps the practical conversation in view and treats semantic rewording as repetition;
- free-form chat in every nonfinal synthesis-review state;
- `Continue interview` as the finite default after a settled pattern or completed measurement area;
- progress during the active thread, expressed as approximate percent plus **measurement areas still open**, not a question count;
- progress and request-liveness surfaces are kept at the active end of the page rather than forcing scroll trips to the top;
- a measurement area may finish as **area covered** without manufacturing a participant-facing synthesis;
- participant adjudication is reserved for syntheses that add useful person-specific integration rather than obvious paraphrase;
- when a real synthesis is surfaced, participant judgment reuses the already-computed coverage report instead of blocking on another LLM coverage call;
- working syntheses remain ephemeral until participant judgment;
- exact hidden-ledger working state is automatically checkpointed browser-side and can be downloaded/imported for audit/recovery;
- audit/recovery exactness is explicitly not scientific validity;
- participant authority over durable person-level patterns.

Runtime elicitation receives no participant chart, birth target, expected answer direction, target-model mapping, candidate score/rank, or historical AstroHD crosswalk.

## Latest owner consumer-seam findings: natural flow

Direct owner testing plus an exact private audit/recovery checkpoint exposed three remaining defects.

### 1. Progress/liveness navigation

`Continue interview` could scroll to a status/progress card near the top and then fail to return to the live question. Even when the return scroll worked, the two-scroll round trip was unnecessary.

**Repair:** the existing progress and request-liveness DOM nodes are moved to the active end of the interview at runtime. Status visibility no longer requires navigating away from the current interaction.

### 2. Measurement completion versus person-level synthesis

The latest private checkpoint showed an adequately measured sensory/recovery area whose tentative synthesis mostly reorganized the immediately preceding answer. The scientific measurement had useful information, but participant adjudication of an obvious restatement added little value.

**Repair:** the target-blind planner now has an explicit `topic_complete` workflow outcome. It may use this when the local measurement need is adequately met and further questioning has low expected information gain, but a person-level synthesis would mainly paraphrase or enumerate what the participant just said.

`topic_complete` does **not** alter the accepted v2 semantic contract and does not create a durable Life Pattern. It simply closes the local measurement area and exposes the finite continuation frontier.

A synthesis is reserved for a genuinely useful person-specific integration such as a conditional, contrast, boundary, recurring sequence, or other compression that is materially more informative than the immediately preceding statements. It need not be surprising; obvious paraphrase is insufficient reason to spend participant adjudication burden.

### 3. Participant judgment waiting on redundant remote work

The earlier acceptance path could disable all synthesis buttons and remain under `Working on it…` because accepting/rejecting a synthesis synchronously launched another LLM-backed coverage assessment, even though coverage had already been assessed when the synthesis was surfaced.

**Repair:** synthesis adjudication now commits through the deterministic v2 core and reuses the cached in-thread coverage report. It does not launch a second coverage-model call merely to return the participant's decision.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-NATURAL-FLOW-REPAIR-2026-09-16.md`.

## Recovery architecture

The browser preserves a checksum-bound snapshot of the exact current *working* hidden ledger for crash recovery/audit. A working snapshot may contain a defect; exact restoration proves state preservation, not correctness. It is not canonical measurement data and is not the scientific freeze.

Recovery preserves:

- conversation and turn IDs;
- current episode/boundary/pattern-focus state;
- full v2 record including fact revision lineage and source-provenance hashes;
- proposal support / active proposal state;
- current ephemeral synthesis draft;
- latest in-thread progress report;
- the explicit workflow phase, including `topic_complete`.

Private narrative remains browser-local unless the participant explicitly downloads/uploads a checkpoint. It is not persisted to Git or a Railway volume.

Older files that never contained the hidden ledger can restore visible conversation for development continuity but cannot become the clean scientific freeze.

## Verification / live deployment

Natural-flow application source: `5405e4f5398d5fa5902474ddb3a3163d7807ae1e`.

Regression checkpoint: `559113ee6184c21f9ed2abeb45dbf620317311d2`.

GitHub Actions run `35154236382`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `1606fb4a-5812-4da2-976a-ff1d7a342f05`: **SUCCESS** from application source `5405e4f5398d5fa5902474ddb3a3163d7807ae1e`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. This does not authorize external participant collection/recruitment.

## Recoverability measurement and hard owner criterion

Active blueprint: `life-patterns-recoverability-coverage-v2`, with 23 required neutral dimensions and explicit missingness states.

A fresh completed interview still fails if it does not preserve enough behavioral information for the historical owner AstroHD recovery:

- exact recorded moment hourly rank no worse than **#2**;
- correct date remains the **#1 distinct refined neighborhood**;
- refined peak remains within **11 minutes** of recorded time.

Coverage completion alone cannot pass. The fresh interview must be frozen/exported locally before the narrowly authorized owner-self AstroHD recovery is run.

## Mission Control correction capture

Owner-explicit logic corrections remain durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127. Current truth remains **`CAPTURED_BRANCH_ONLY`**.

Latest privacy-bounded artifact: `feedback/mission-control/SDF-20260916-LIFE-PATTERNS-NATURAL-FLOW-017.json`.

## Current gate

Owner consumer-seam retest is next. Immediate checks:

1. refresh/reopen the exact-backed development checkpoint;
2. `Continue interview` should keep the active interaction/status/progress near the bottom rather than bounce to the page top;
3. an adequately measured area whose only available synthesis would be an obvious paraphrase should close as **area covered** and expose `Continue interview` rather than require synthesis approval;
4. a genuinely integrative person-specific synthesis should still surface normally;
5. `Yes — keep that` / reject should return promptly, and synthesis buttons must not remain disabled under `Working on it…`;
6. progress, exact recovery, non-repetition, and workflow-phase restoration must remain intact;
7. once the product seam passes, complete a fresh target-blind interview, Freeze/export measurement, then run the owner-self historical AstroHD recovery regression.

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware elicitation, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
