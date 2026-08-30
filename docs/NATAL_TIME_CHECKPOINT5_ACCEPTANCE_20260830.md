# Natal-time checkpoint-5 acceptance packet — 2026-08-30

## Decision boundary

This packet closes only the checkpoint-4 Phase-0 corrections and the authorized synthetic
evaluation-contract verifier. It does not authorize or implement questionnaire content,
candidate selection/ranking/elimination, baselines, fitting, calibration, inference, thresholds,
probabilities, participant-facing output, relationship evidence, live records, recruitment,
public release, migration, deployment, push, or merge.

The requested supervisor response must begin with exactly one of:

- `OWNER DECISION REQUIRED: YES`
- `OWNER DECISION REQUIRED: NO`

If `YES`, work stops for the owner. If `NO`, only the next scope explicitly authorized by the
supervisor may proceed.

## Exact Git anchors

- Fresh audited `main` / `origin/main`: `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`.
- Checkpoint-3 reviewed head: `8cc97025f1e30c52a156e3c7bb5068baf5aea39b`.
- Checkpoint-4 evaluated head: `90220a3d67e847d883b2060fa3578fe5026cc414`.
- Phase-0 closure through operational evidence: `b3e5314f8f0cc611ea1b3784bc55c798323ae1d3`.
- Phase-1 implementation: `3c12801a8ec44e97579f869a96643aebc24a37f9`.
- Acceptance source head: `2f707858425cb51f61c5d57e6a0364faf092b841`.
- Acceptance source tree: `a9b9ad7dd259bb52e08add603de061853f408548`.
- From baseline through the acceptance source head: 56 direct first-parent commits, zero merge
  commits, 133 changed paths, 16,668 insertions, and 54 deletions.

The two commits after `f07dc44486ddc68dfa516cc3632de916dcadb9d4` changed and then restored only
the import order in `tests/unit/test_audit_natal_time_foundation_runner.py`. The final tree OID is
exactly the same as `f07dc44486ddc68dfa516cc3632de916dcadb9d4`; no qualified byte changed.

## Phase-0 closure

- `state/NATAL-TIME-CHECKPOINT4-LINEAGE-ATTESTATION.json` logical SHA-256:
  `934fdd1c6d4dce01c16d0baaef89a2744d9ca057a1f466c1f8a0e75f605f693d`.
- `state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json` logical SHA-256:
  `133ff5f38866b4641c804c9744b6a1a30626b81ac49df995c0a5ffab9aceb3ff`.
- `state/NATAL-TIME-CHECKPOINT4-OPERATIONAL-EVIDENCE.json` logical SHA-256:
  `3aace230c0711d579b965e3d0e811e79fd5249e60578868084fcd0414f686677`.
- `state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json` logical SHA-256:
  `067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`.
- Preserved v1 logical SHA-256:
  `c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9`.
- Unresolved-decision register logical SHA-256:
  `5d33ba6d5021bc693f2ff362737dabcdc5bdf6740f007f5f11270d9d22483df8`.

The deliberate interruption test starts with an empty output directory, writes two of nine exact
committed local real-engine receipts, interrupts, proves an incomplete aggregate fails closed,
and resumes without rewriting valid receipt bytes or mtimes. It then proves exact clean-run and
committed-index equivalence. Missing, duplicate, corrupt, wrong-head, wrong-engine, stale,
truncated/partial JSON, incomplete, and omitted-Pacific/Apia states all fail closed.

The operational evidence describes a **local real-engine replay**, not a production replay. Its
1,126.942930551-second conservative durable-write lower bound is filesystem metadata evidence,
not end-to-end timing and not an operational guarantee. The release-disabled schema remains only
a threat-model artifact and is not anonymity or disclosure-safety evidence.

## Phase-1 synthetic verifier

Implementation and rationale are in
`docs/NATAL_TIME_SYNTHETIC_EVALUATION_CONTRACT_VERIFIER_20260830.md`. The committed bundle under
`state/NATAL-TIME-SYNTHETIC-EVALUATION-V1/` contains 46 files: one schema, one manifest, 22 fixed
synthetic 2099-only fixtures, and 22 receipts.

- Manifest logical SHA-256:
  `f021a2773328c8f68966023fa025dce68774b135b9eead1c19704cf663d0fd0c`.
- Manifest exact-file SHA-256:
  `0f52c2f8d3d32d775465790383025920254e169c16b83ddfd1b00660349e780a`.
- Schema logical SHA-256:
  `a720000cc9af0c401aac1a98870099d52ae17deb87911113904303e4eccf4509`.
- Schema exact-file SHA-256:
  `297072905ee4a12b1215ab72a32efe3c44130cf136d3711f9547803690f84619`.
- Evaluator-version SHA-256:
  `fcd2db6768f6263b928a3fdcf7905978e4e1b4ee9c5c817cbd7b02ea7d4a0b5c`.
- Receipt kinds: 12 `descriptive_metric_receipt`; 10 `fail_closed_rejection`.

The state machine enforces `C_i` freeze, method/preregistration freeze, exact preconstructed `S_i`
commitment, evaluator-only `T_i` access, then receipt. It never chooses `S_i`. The pre-commit
public-fixture digest excludes hidden `T_i`; the manifest binds complete fixture bytes and a valid
receipt binds the canonical hidden reference after authorized access. Tests prove zero reference
parser calls and no hidden-reference semantic digest dependency before `S_i` commitment.

Schemas are recursively closed. Exact full-record membership includes both provenance digests,
ID, endpoints, full-state digest, and civil date. Duplicate detection precedes canonical sorting.
Partial intervals, foreign/manufactured intervals, post-reference mutation, early access,
cross-role components, contamination, personal/relationship/free-text fields, inferential fields,
and rehashed unknown receipt fields fail closed. Half-open endpoint touching is non-overlap;
positive-width partial reference overlap is compatible and unclipped; distinct surviving source
intervals conflict even when they overlap; identical intervals remain usable. Abstention and all
reference failures use typed component-specific nulls. Documentary width, temporal width,
canonical interval count, unique state count, date coverage, intersection, and abstention remain
separate with no scalar summary.

The preregistration structural checker requires exact controlled IDs for all 15 baselines, all 11
measurement requirements, roles, actors, source rules/classes/precision, connected-component
edges, leakage/contamination, metrics, disclosure threats/controls, prohibited public fields, and
release declarations. It accepts no item content, prose substitute, duplicate, unknown, or
heading-only placeholder.

## Acceptance verification

The source tree `a9b9ad7dd259bb52e08add603de061853f408548` passed:

- `.venv/bin/python -m pytest`: **345 passed** in 29.16 seconds.
- `.venv/bin/mypy --strict src/hdmatch`: **132 source files**, no issues.
- `scripts/audit_natal_time_checkpoint4_phase0.py --validate-only`:
  `CHECKPOINT4_PHASE0_ATTESTATIONS_OK`.
- `scripts/audit_natal_time_checkpoint4_operational_evidence.py --validate-only`:
  `CHECKPOINT4_OPERATIONAL_EVIDENCE_OK`.
- `scripts/check_private_artifacts.py --diff-base b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`:
  `private-artifact gate: pass`.
- Phase-1 focused verifier: **20 passed**.
- Phase-0/Phase-1 affected gate: **47 passed**.
- `git diff --check`: pass.
- All 48 checkpoint-3 protected paths have the exact reviewed Git blob OID at the acceptance
  source head.
- Worktree and index: clean at acceptance capture.

The exact post-checkpoint-4 Ruff manifest is the 12 Python paths changed from `90220a3` through
the acceptance source head:

1. `scripts/audit_natal_time_checkpoint4_operational_evidence.py`
2. `scripts/audit_natal_time_checkpoint4_phase0.py`
3. `scripts/audit_natal_time_preinference_feasibility.py`
4. `scripts/build_natal_time_synthetic_evaluation_verifier.py`
5. `src/hdmatch/natal_time/evaluation_contract.py`
6. `src/hdmatch/natal_time/replay.py`
7. `tests/integration/test_natal_time_replay_interruption.py`
8. `tests/unit/test_natal_time_checkpoint4_operational_evidence.py`
9. `tests/unit/test_natal_time_checkpoint4_phase0.py`
10. `tests/unit/test_natal_time_metric_semantics_contract_v2.py`
11. `tests/unit/test_natal_time_preinference_feasibility_and_disclosure.py`
12. `tests/unit/test_natal_time_synthetic_evaluation_contract.py`

The exact command
`git diff --name-only -z 90220a3d67e847d883b2060fa3578fe5026cc414..HEAD -- '*.py' | xargs -0 .venv/bin/ruff check`
passed. The 43-Python-path whole task-branch manifest has one pre-existing Ruff import-order
finding in the byte-protected `tests/unit/test_audit_natal_time_foundation_runner.py`; it was not
silently changed. The operational artifact separately records the 1,812 legacy repo-wide Ruff
findings and the two earlier seven-path Git-derived scopes that passed.

Operational corrections are explicit: one affected-test command named a nonexistent privacy-test
path and ran zero tests before the corrected 47-test command passed; one full-test command
mistakenly invoked npm in this Python-only repository and failed before collection, after which the
repository-standard full pytest command passed; combined-file mypy invocations produced duplicate
module-name/tooling errors, after which the executable modules and complete source package passed
using repository-compatible module/package scopes. None of those invocation errors changed files
or weakened a gate.

## Fresh external-state audit

The read-only refresh on 2026-08-30 found GitHub still public with default branch `main` at
`b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`. Only old draft PR #1 remains open and dirty. Railway
project `humandesign-relationship`, production service `relationship-web`, still reports latest
deployment `60c360b2-6591-4e96-9d82-66e6808f82e5` successful for commit `450d806`, one Amsterdam
replica, the existing service domain, and the `/data` volume. Only variable names were inspected;
the expected direct-OpenAI and OpenRouter names remain present. No GitHub, Railway, deployment,
configuration, variable, volume, participant, or public state was mutated.
