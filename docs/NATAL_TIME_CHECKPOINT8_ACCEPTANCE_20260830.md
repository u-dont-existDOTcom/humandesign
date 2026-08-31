# Natal-time checkpoint 8 acceptance packet — 2026-08-30

## Scope and mandatory decision boundary

ChatGPT Pro checkpoint 7 returned `OWNER DECISION REQUIRED: NO` for its bounded remediation and
`CHECKPOINT-7 STATUS: QUALIFIED, WITH ONE NARROW CURRENT-HEAD PROVENANCE CLOSURE REQUIRED`. Its
exact ruling is `docs/PRO_SUPERVISION_CHECKPOINT_7_20260830.md`.

Checkpoint 7 authorized only:

1. the 21-test checkpoint-7 current-head provenance closure; and
2. a documentation-only owner dossier presenting, without resolving:
   - **A — Stop and archive the deterministic foundation;**
   - **B — Measurement reliability before rectification;** or
   - **C — Blinded falsification study design.**

Both phases are complete. This packet asks Pro to confirm the closure, audit the dossier's
neutrality, and present A/B/C as the now-mandatory owner choice. No substantive scientific work may
continue after this packet without Joel's ruling.

This slice introduces no questionnaire content, response choice, scoring key, estimator,
procedure for generating or choosing `S_i`, candidate ranking or pruning, baseline execution,
operating point, cohort size, recruitment plan, probability, confidence, participant objective,
relationship evidence, public disclosure regime, live record, migration, deployment, or release.

## Exact source boundary

- Canonical comparison base: `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` on public GitHub
  `main` and `origin/main`.
- Checkpoint-7 Pro submission head: `b581ab3b7397abf5aed5e6da7f7e04deb22e2a06`.
- Current-head closure validator source commit:
  `8aa6aecb57832ae88537f30ce7125e2533a03cce`.
- Immutable current-head closure artifact commit:
  `f31a692f1b327078b18702072cff4330188cd5a2`.
- Dossier evidence head: `cdf1b0dac4e56cbefaaa387eb48cf38701d78660`.
- Dossier evidence tree: `a256c4c1ac2262b43a3f186566279b466e2bd6fd`.
- Base-to-dossier-evidence diff: 232 files changed, 27,644 insertions, 54 deletions.
- Exact `f31a692..cdf1b0d` documentation delta:
  - `CURRENT_PLAN.md`;
  - `docs/NATAL_TIME_OWNER_DECISION_DOSSIER_20260830.md`; and
  - `state/CURRENT-STATE.md`.
- Active local branch: `codex/astrohd-relationship-continuation`.

The commit adding this packet is a documentation-only child of the dossier evidence head. The Pro
submission supplies the exact final head/tree and forced exact-head verification results directly
because a tracked document cannot contain its own eventual commit.

## Phase 0 — checkpoint-7 current-head closure

`state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json` is the immutable machine-readable artifact
required by checkpoint 7.

### Commit topology and classified scope

The closure binds:

- checkpoint-6 final head `a7a516fe7dc679909fba392a511570ae603e4fe3`;
- oracle source head `01a60b28aac84a5b5ecbe66e64a489b8345e0d1b`;
- checkpoint-7 implementation head `d2ee0a3b875f2e21c37534d5e338947a6e3ff098`;
- checkpoint-7 documentation submission `b581ab3b7397abf5aed5e6da7f7e04deb22e2a06`; and
- required submission tree `a4a8dfc1947df513cf2fbeac82000992b74bce9d`.

The required ancestor/direct-parent topology passes with no merge or alternate-parent path. The
`a7a516f..d2ee0a3` delta contains exactly 14 classified paths: supervision documentation,
fail-closed provenance/oracle validators, synthetic test evidence, test-only oracle code, and
tests. Thirteen paths were added; the only modified path is the test-only endpoint assertion in
`tests/unit/test_natal_time_synthetic_evaluation_contract.py`. The
`d2ee0a3..b581ab3` delta contains exactly the three required documentation/state paths.

### Replay-current-head binding

- All 58 replay-affecting paths are byte-identical at `a7a516f` and `d2ee0a3`.
- All 28 replay-semantic functions are AST-identical across the same range.
- Fixture inputs, engine invocation, interval/event construction, independent verification,
  receipt fields, canonical serialization, digests, index construction, durable writes, and
  resume behavior are covered.
- Every controlled mutation to any of the 58 paths or 28 function bodies requires Route B.
- All nine receipts validate at `d2ee0a3`.
- The exact index self-hash reproduces as
  `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435`.
- The exact aggregate SHA-256 reproduces as
  `ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`.

No replay-semantic change was found. Route B receipt regeneration is not required, and no receipt
or earlier attestation was relabeled.

### Oracle-current-head binding

- The exact oracle source at `01a60b28`, `d2ee0a3`, and `b581ab3` hashes to
  `4192061951696d28d9d2671c70e13bb69b38aeba95ee83dc9e53f40eadb234c3`.
- The oracle version recomputes to
  `f3a3fc3b273da8a7d9a94d8e6b2e02bbbd9169093979aec42d084c272b78b623`.
- The strengthened exact-source AST audit finds no production/repository import, dynamic import,
  evaluation/compilation path, subprocess/shell invocation, or `S_i` generation/optimization
  definition.
- The exact adversarial corpus, comparison matrix, targeted mutation report, and discrepancy
  ledger reproduce from `d2ee0a3`.
- A controlled source mutation invalidates both oracle version and current-head closure.

The oracle remains described only as a **structurally independent synthetic contract oracle**.
The result remains **zero discrepancies across the committed 41-case adversarial corpus** and a
**targeted 13-guard mutation audit**, not external validation, universal equivalence, or a complete
mutation score.

### Protected/scope/acceptance result

- All 48 checkpoint-3 protected paths remain byte-identical.
- No participant/live data, documentary reference data, relationship evidence, questionnaire
  content, candidate choice, or inferential semantics entered the delta.
- The immutable closure reproduces byte-for-byte.
- Closure logical SHA-256:
  `5780b3285bc212e4a1830bca518fef617a06e538a08a4cdbe9e6bcc969f9751b`.
- Closure exact file SHA-256:
  `2d2f1b3655b810fd830cb2ef0b8bb8ed9b4f0419deae35f6f7d9a4ec70bc763a`.
- All 21 checkpoint-7 current-head acceptance tests pass.

The closure is a provenance extension, not a new scientific result.

## Phase 1 — neutral owner-decision dossier

`docs/NATAL_TIME_OWNER_DECISION_DOSSIER_20260830.md` has exact file SHA-256
`69e8fc1964c478a81db065983ce943bb0f293e468c14c01693cf646ff67d7650` at the dossier evidence head.

The dossier first preserves the common qualified foundation and nonclaims, then compares all three
options on the same dimensions:

- immediate scientific question;
- evidence required;
- primary failure modes;
- minimum governance prerequisites;
- approximate resource class, without approved expenditure;
- reusable methods-contract components;
- scientific advantage and limitation; and
- predeclared falsification or termination principle.

It also maps every immutable unresolved entry `UDR-001` through `UDR-012` across A/B/C without
resolving any entry. The owner ruling block contains three unchecked choices and an explicit stop.

### A — Stop and archive

No human study. Preserve the deterministic, replay, synthetic-oracle, and supervision evidence as
an auditable neutral or negative result with explicit nonclaims. This is the lowest and finite
resource class. It terminates after a replayable archive and claim ledger are frozen. Publication,
push, merge, or deployment remains a separate owner decision.

### B — Measurement reliability before rectification

Study whether proposed self-report constructs can be repeatedly elicited and consistently coded
without charts, `T_i`, candidate selection, or birth-time recovery. This is a moderate resource
class. Future evidence would need test-retest, inter-rater, missingness, response-style,
invariance, burden, privacy, and blinding controls. If no construct satisfies future predeclared
requirements, the measurement route stops before rectification; that would not by itself falsify
every formulation of HD.

### C — Blinded falsification study design

Design, but do not execute, a test of whether a future frozen HD method adds untouched
out-of-sample value over complete/no-pruning output, the strongest admissible ordinary non-HD
model, and participant/component-level permutation or mismatched-chart controls. This is a high
and materially uncertain resource class. A valid future null result under a predeclared rule could
terminate the tested method; custody, leakage, or preregistration failure would invalidate the
study rather than falsify it.

### Neutrality and temporal register note

The dossier selects no direction, construct, estimator, operating point, cohort size, recruitment
plan, probability interpretation, participant objective, disclosure regime, or external action.
Selecting B or C would authorize only a later bounded design/supervision step, not live execution.

The earlier `owner_decision_required_now: false` field in immutable
`state/NATAL-TIME-UNRESOLVED-DECISIONS.json` was correct for its earlier pre-inference slice.
Checkpoint 7's later ruling supersedes that temporal flag after this dossier; the earlier artifact
was not rewritten or relabeled.

## Verification evidence and corrected-command ledger

Before this documentation-only packet commit:

- the current-head closure generator completed from clean source and emitted logical digest
  `5780b328...`;
- validate-only mode reproduced the immutable closure;
- all 21 focused current-head acceptance tests passed in 60.46 seconds;
- the new source and test passed Ruff and strict mypy; and
- `git diff --check` and clean index/worktree checks passed before dossier authoring and after its
  local commit.

The exact final submission head receives a forced full-test run, strict-mypy complete source run,
exact Git-derived Ruff changed-Python-file run, all required artifact validators including the new
current-head closure, privacy/history/build gate, 48-file protected-core comparison,
`git diff --check`, exact documentation-child diff, and clean worktree/index checks. Final
identifiers and outputs are supplied directly in the Pro submission.

Corrected execution ledger retained for supervision:

- one telemetry query used unsupported `status`; the supported read-only subcommand is `summary`,
  and no test result or artifact was affected;
- a focused pytest process completed after its earlier caller session was no longer available, so
  the identical 21-test scope was rerun once to obtain an attributable terminal result; the forced
  redundant-green counter remains zero because the earlier result was not observed; and
- no visible/headed browser interaction was needed for the final external audit: the purpose-built
  read-only Railway connector supplied deployment/configuration state without secret values, in
  accordance with the owner's headless-by-default browser rule.

All earlier checkpoint-7 corrected-command history remains preserved in
`docs/NATAL_TIME_CHECKPOINT7_ACCEPTANCE_20260830.md` and
`docs/PRO_SUPERVISION_CHECKPOINT_7_20260830.md`.

## Fresh external read-only state

The checkpoint-8 work made no external change. The fresh read-only audit reconfirmed:

- public GitHub repository `u-dont-existDOTcom/humandesign`, default branch `main`, at
  `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` with successful main CI run `33283895301`;
- draft PR #1 remains the only open PR, unchanged at
  `3bab2c58f6972b4a66b7b68bb8cde6ba507d64db`, merge state `dirty`, with its old failed `verify`
  check; it was not touched;
- Railway project `humandesign-relationship`, production service `relationship-web`, remains on
  successful deployment `60c360b2-6591-4e96-9d82-66e6808f82e5` for commit `450d806`, with one
  `ams` replica and the `/data` persistent volume mount;
- the Railway-generated service domain is unchanged; `/healthz` returns `{"status":"ok"}`;
  `/api/llm-status` reports configured direct OpenAI `gpt-5.6-sol`; and recovery status reports
  configured magic-link and six-digit-OTP methods; and
- the service configuration lists both `OPENAI_API_KEY` and `OPENROUTER_API_KEY` by name. No value
  was requested, returned, or exposed.

No GitHub setting, PR, remote branch, Railway service, variable, deployment, replica, volume, data,
secret, participant/live record, or public runtime was changed.

## Requested checkpoint-8 ruling and owner choice

Please answer first with exactly `OWNER DECISION REQUIRED: YES` or
`OWNER DECISION REQUIRED: NO`, then:

1. qualify or reject the checkpoint-7 current-head closure against all 21 required tests;
2. confirm whether the deterministic/Phase-0 foundation remains qualified with its existing
   engine-relative and synthetic claim limits;
3. audit whether the owner dossier presents A/B/C neutrally and completely without selecting or
   implementing a prohibited choice;
4. identify any defect in the dossier that prevents an informed owner ruling; and
5. if no such defect remains, state that substantive scientific implementation must stop and
   present the explicit owner choice:
   - **A — Stop and archive the deterministic foundation;**
   - **B — Measurement reliability before rectification;** or
   - **C — Blinded falsification study design.**

Do not authorize a substantive next slice without Joel's explicit A/B/C ruling. Successful
checkpoint-8 evidence does not authorize inference, questionnaire content, estimator or baseline
implementation, participant/live data, recruitment, push, PR action, merge, migration,
deployment, relationship evidence, public release, or any scientific operating rule.
