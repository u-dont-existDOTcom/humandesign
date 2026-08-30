# Natal-time checkpoint 7 acceptance packet — 2026-08-30

## Scope and supervision boundary

ChatGPT Pro checkpoint 6 returned `OWNER DECISION REQUIRED: NO` and
`CHECKPOINT-6 VERDICT: QUALIFIED`. Its exact ruling is
`docs/PRO_SUPERVISION_CHECKPOINT_6_20260830.md`. It authorized only:

1. final replay-source provenance closure; and
2. a test-only, structurally independent synthetic evaluator oracle.

This packet contains only those two phases. It introduces no estimator, procedure for constructing
or choosing `S_i`, questionnaire, baseline execution, candidate ranking or pruning, weight, prior,
score, probability, confidence, utility, threshold, recommendation, relationship evidence, live
record, participant workflow, public ledger, migration, deployment, or release.

The reference-custody qualification remains limited to synthetic, local, cooperative code. Before
any live documentary reference data, separate process identity, storage permissions, and
evaluator-only credentials remain mandatory.

## Exact source boundary

- Canonical comparison base: `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` on `main` and
  `origin/main`.
- Checkpoint-7 implementation-evidence head:
  `d2ee0a3b875f2e21c37534d5e338947a6e3ff098`.
- Implementation-evidence tree: `9535a05e4fffa5d8c2c3b7d04031238d2afc9c08`.
- Base-to-implementation diff: 226 files changed, 25,595 insertions, 54 deletions.
- Active local branch: `codex/astrohd-relationship-continuation`.

The commit adding this packet and the current-plan/state updates is a documentation-only child of
the implementation-evidence head. The Pro submission supplies the exact final head/tree and forced
verification results directly because a tracked document cannot contain its own eventual commit.

## Phase 0 — final replay-source closure

`state/NATAL-TIME-CHECKPOINT6-FINAL-REPLAY-SOURCE-CLOSURE.json` closes the exact gap identified at
checkpoint 6. It binds:

- receipt-generation source `1c59b8aae3c096c84a8116d49c0cb0525029837e`;
- checkpoint-5 acceptance source `2f707858425cb51f61c5d57e6a0364faf092b841`;
- checkpoint-6 implementation source `067ed6cdd504b368b88c203ca6d058c20b2fb913`; and
- checkpoint-6 documentation-only submission `a7a516fe7dc679909fba392a511570ae603e4fe3`.

The machine audit establishes the declared ancestor chain and the direct-parent relationship from
`067ed6c` to `a7a516f`. It inventories all 58 manifest-bound replay-affecting files and 28 semantic
functions spanning fixture inputs, engine invocation, event/interval construction, independent
verification, receipt fields, canonical serialization, digest/index construction, durable writes,
and resume behavior.

All 58 files and 28 functions are byte/AST identical at `2f707858`, `067ed6c`, and `a7a516f`.
Accordingly, final Route A source equivalence is established and Route B regeneration is not
required. The validator also proves:

- all nine committed receipts validate at `067ed6c`;
- rebuilt index bytes reproduce
  `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435`;
- aggregate SHA-256 reproduces
  `ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`;
- a semantic fixture-input mutation fails validation;
- mutating each of the 58 replay-affecting file byte streams requires Route B; and
- no prior receipt or attestation was overwritten.

Closure logical SHA-256:
`eb862ff17e3223a9a39af0a25c567dd24cecf67fb2c9524f44449214d80d5a88`.
Exact file SHA-256:
`be791a759af4e22a9ef1f429521112e098066d1b3c4327ececf6c88fd717554e`.

## Phase 1 — structurally independent synthetic evaluator oracle

### Independence and source binding

The test-only oracle is `tests/oracles/natal_time_v3_oracle.py`. It uses only the Python standard
library and imports neither `hdmatch` nor `scripts`. Its source contains no production evaluator or
builder call and no mechanism to generate, rank, optimize, or choose `S_i`.

- Exact oracle source commit: `01a60b28aac84a5b5ecbe66e64a489b8345e0d1b`.
- Exact oracle source tree: `de3762e0dc1905b9e3b3b4c8c6db784e9224b161`.
- Oracle source SHA-256:
  `4192061951696d28d9d2671c70e13bb69b38aeba95ee83dc9e53f40eadb234c3`.
- Oracle version SHA-256:
  `f3a3fc3b273da8a7d9a94d8e6b2e02bbbd9169093979aec42d084c272b78b623`.
- Operative v3 contract SHA-256:
  `75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe`.

The oracle independently implements exact UTC/half-open interval parsing, whole-interval
membership, duplicate/partial/foreign/manufactured rejection, canonical unordered-set
commitment, temporal width, canonical interval count, unique full-state count, date coverage,
documentary width, reference-domain classification, reference intersection, abstention/N/A
semantics, access ordering, `S_i`/`T_i` post-access integrity, connected-component contamination,
and recursive prohibited-field rejection.

### Adversarial corpus and comparison matrix

`state/NATAL-TIME-CHECKPOINT7-ORACLE-ADVERSARIAL-CORPUS.json` commits 41 deterministic cases:
all 35 separated synthetic evaluator fixtures plus six independently checked rehashed forbidden-
field receipt mutations. Its 29 observed coverage tags exactly equal all 29 required checkpoint-6
tags, including disconnected/reordered/repeated-state cases, every reference-domain edge,
precommit access, post-access mutation, cross-role contamination, and scalar/inferential-field
insertion.

`state/NATAL-TIME-CHECKPOINT7-ORACLE-COMPARISON-MATRIX.json` records exact production and oracle
summaries for every case:

- comparison count: 41;
- exact agreement count: 41;
- discrepancy count: 0;
- reference reads before exact `S_i` commitment: 0 for every case;
- changing only evaluator-side `T_i` leaves the inference-visible precommit bytes unchanged; and
- no comparison emits a scalar/inferential output or performs inference/selection.

Reordering an equivalent `S_i` preserves commitment and metrics; repeated full-state identities
produce the required interval-count/state-count divergence; partial/complete domain
incompatibility yields no valid reference-accuracy result; and abstention remains typed N/A rather
than zero, success, or failure.

| Artifact | Logical SHA-256 | Exact file SHA-256 |
| --- | --- | --- |
| Adversarial corpus | `acc7fcb9795f2fd07dabbfc3905d080aa29b3ab0d9f98a5339199de3c199df12` | `f791a7be473ed0af0e859a22da4fb8157a3b31f2785b6edef85094efd95b94bf` |
| Comparison matrix | `30cf1fbe145b4e2ed6ada066293b000e72c4e443dd61f716895942a9fdc3fc4e` | `07deeb95ffdf823dccf90a6b390ca6ec95ce7d09f0cba7553a08441febc84579` |

### Honest mutation audit

`state/NATAL-TIME-CHECKPOINT7-ORACLE-MUTATION-REPORT.json` applies 13 explicit mutations that
remove or corrupt the major membership, abstention, access-order, contamination, schema,
reference-domain, half-open-intersection, and fraction guards.

Each mutant runs in a fresh temporary project tree containing the complete `hdmatch` package, the
exact synthetic evaluator builder, and the evaluator contract tests. The exact-byte committed-
artifact identity test is deliberately deselected because a source mutation must change evaluator
identity; the remaining baseline contract suite passes in the isolated tree. A mutant counts as
killed only when pytest returns nonzero and reports a stable failing/error test node ID. The
report contains no raw timing, temporary path, or nondeterministic pytest-output digest.

- Mutation count: 13.
- Killed: 13.
- Survivors: 0.
- Logical report SHA-256:
  `0c16d226f631d27a5c30f14a01022f8e06b80f41d31c1fca98fee763727569b4`.
- Exact file SHA-256:
  `bddf2be59ace042fa28ae82961a7e7932bbd29c8d7139eeb897814880e9f89ff`.

The honest harness correction exposed one real missing assertion. A new committed contract test
now proves that endpoint-only contact is not a reference intersection; the half-open mutation is
killed by that exact test.

### Fail-closed discrepancy ledger

`state/NATAL-TIME-CHECKPOINT7-ORACLE-DISCREPANCY-LEDGER.json` records
`passed_no_discrepancies`, zero entries, and `checkpoint_completion_blocked: false`. A focused
test injects an oracle/verifier disagreement and proves that the builder returns a self-hashed
blocking ledger rather than allowing checkpoint completion.

- Logical ledger SHA-256:
  `aa87a1d7fe8dcab1211d9ad7b2686c29217ea101351bf4279eef66a98001cd64`.
- Exact file SHA-256:
  `7372aefd90876174ae7628f77145f695df4d099cab9048dc5badd968c2d608d6`.

## Verification evidence and corrected-command ledger

Before this documentation-only commit:

- the final replay-source closure validator passed;
- the checkpoint-7 oracle artifact validator reproduced all four artifacts exactly;
- 48 focused evaluator/oracle/artifact tests passed;
- the oracle and audit source passed Ruff and strict mypy; and
- the isolated mutation baseline passed and all 13 major-guard mutants were killed.

The exact final submission head receives a forced full-test run, complete strict-mypy source run,
exact Git-derived Ruff changed-file run, all required artifact validators, the privacy/history/
build gate, 48-file protected-core comparison, `git diff --check`, and clean worktree/index checks.
The final identifiers and outputs are supplied in the Pro submission.

Corrected execution ledger retained for supervision:

- direct execution of the oracle audit script did not put the repository root on the import path;
  module execution with `.venv/bin/python -m scripts.audit_natal_time_checkpoint7_oracle` was the
  correct generation command;
- the first mutation report hashed raw pytest output, making reproduction sensitive to timing and
  temporary paths; replacing raw output with stable test node IDs then exposed that the temporary
  tree lacked the builder, so the four uncommitted draft artifacts were deleted and never entered
  history;
- the final mutation harness uses a complete isolated synthetic project view and revealed the
  endpoint assertion gap described above;
- rerunning the immutable generator without `--validate-only` correctly returned
  `FileExistsError`; the validate-only command reproduced the committed artifacts; and
- a combined source-plus-test mypy invocation followed the repository's Python-3.11 target into a
  Python-3.12-only dependency stub error; the repository-standard strict complete source scope and
  focused source scopes are the authoritative checks.

## Fresh external read-only state

The checkpoint-7 work made no external changes. The last fresh read-only audit remains:

- public GitHub repository `u-dont-existDOTcom/humandesign`, default branch `main`, at
  `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`; main CI run `33283895301` passed;
- draft PR #1 remains the only open PR, at `3bab2c58f6972b4a66b7b68bb8cde6ba507d64db`,
  merge state `DIRTY`, with its old failing `verify` check; it was not touched; and
- Railway `relationship-web` remains online at successful deployment
  `60c360b2-6591-4e96-9d82-66e6808f82e5`, one EU West replica, with the persistent volume
  attached; it was not mutated.

No secret value, participant/live record, Railway setting/variable/data, GitHub setting, PR,
remote branch, deployment, or volume was changed.

## Requested checkpoint-7 ruling

Please answer first with exactly `OWNER DECISION REQUIRED: YES` or
`OWNER DECISION REQUIRED: NO`, then:

1. qualify or reject the final replay-source closure;
2. qualify or reject the structurally independent oracle, adversarial comparison matrix,
   mutation report, and discrepancy ledger;
3. identify any remaining blocking defect with an exact acceptance test;
4. state whether the deterministic/Phase-0 foundation remains qualified; and
5. authorize at most one bounded next slice while preserving every hard prohibition unless
   explicitly and safely superseded.

Successful checkpoint-7 evidence does not itself authorize inference, questionnaire content,
participant/live data, push, PR action, merge, migration, deployment, relationship evidence,
public release, or any scientific operating rule.
