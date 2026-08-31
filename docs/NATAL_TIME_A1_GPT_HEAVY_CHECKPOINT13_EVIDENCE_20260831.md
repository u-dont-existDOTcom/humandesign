# Checkpoint 13 — A1/GPT-heavy architecture evidence

Status: local, reversible, content-free, synthetic-test-only implementation

## Outcome

Checkpoint 13 implements the metadata and fail-closed control plane that lets GPT perform most
procedural work without becoming the silent source of the human meanings. Joel remains the sole
prospective human semantic source and final fidelity authority; no eligibility verdict has been
made. The architecture does not contain a question, construct, instrument, real-person record,
selected GPT configuration, or later mapping content.

The implementation separates:

- AstroHD-aware governance GPT;
- two future isolated GPT initial-adjudication runs;
- a separate GPT reconciliation context;
- an isolated chart-blind content-support GPT;
- Joel-author semantic events; and
- Joel-owner governance events.

The two initial adjudication slots are independent runs only. The architecture explicitly refuses
to call them independent models and leaves model, provider, version, prompt, evidence standard,
threshold, and reconciliation rule unselected.

## Human origin and GPT-heavy processing

The raw human-origin freeze must occur before every semantic GPT derivative. Original bytes remain
preserved beside any transcript. Exact quotation requires offsets. Mechanical formatting cannot
change meaning, hierarchy, or grouping. Exact and possible near duplicates are flags and cannot
delete source records or establish semantic equivalence.

GPT paraphrase, grouping, label, and synthesis candidates remain non-authoritative unless an exact
human-source lineage and a Joel-author decision are bound. Synthesis can use only accepted units
and must preserve conflict and unresolved material. The clean freeze requires a final Joel-author
fidelity attestation before protected mapping access. A later revision cannot overwrite the clean
freeze; it becomes a separate non-clean branch.

## Synthetic hostile coverage

Twenty-four conspicuously synthetic probes cover all required hostile families, including aware
pre-freeze access, cross-run leakage, reconciliation overwrite, owner override, unsourced GPT
semantics, unattested paraphrase, duplicate deletion, autonomous grouping or labeling, conflict
omission, meaning-changing formatting, transcript replacement, missing clean-unit source,
post-freeze overwrite, human-facing fields, real-person or eligibility records, protected
pre-freeze exposure, owner-as-author substitution, same-run identity, false independent-model and
cross-author claims, missing quote offsets, and unaccepted synthesis units.

The validator exists only under `tests/a1_gpt_heavy`; production code has no import of it. The
production-source diff from corrected checkpoint baseline
`497bfed7c554c52dc3b22b2548b41fef844c84a9` is empty.

## Verification

The checkpoint-13 suite passes 34/34 and the focused checkpoint-11/12/13 suite passes 168/168.
Strict mypy passes all 132 source files, Ruff passes the changed Python files, every tracked JSON
artifact parses, the privacy/history/build gate passes, `git diff --check` passes, protected bytes
match their frozen hashes, and the production-source diff is empty. The pre-commit full suite
produced 755 passes, 21 expected errors from the checkpoint-7 fixture that deliberately refuses a
dirty worktree, and one deselected manifest test. This expected dirty-tree failure is retained in
the execution ledger rather than concealed. The clean exact-head full-suite result and exact commit
and tree are reported in the Pro return receipt after the content-addressed commit, avoiding a
self-referential commit identifier inside its own tree.

The verification ledger is
`state/NATAL-TIME-A1-GPT-HEAVY-EXECUTION-LEDGER-V1.json`; the content-addressed artifact set is
`state/NATAL-TIME-A1-GPT-HEAVY-ARTIFACT-MANIFEST-V1.json`; and the exact 48-row trace is
`state/NATAL-TIME-A1-GPT-HEAVY-ACCEPTANCE-MATRIX-V1.json`.

## Boundaries and assurance

- Worker-to-contract alignment: `GREEN`.
- Bounded A1/GPT-heavy decision-to-owner alignment: `MATCH`.
- Root contract-to-owner alignment: `PARTIAL_ROOT_OPEN`.
- Typed completion claim: `WORKING`.
- Parent outcome: `OPEN`.
- Operational alignment: `PASS` for the bounded architecture and synthetic checks.
- Scientific adequacy: `WARN`; no task-specific adjudication, facilitation, fidelity, or
  cross-author validation exists.
- Release adequacy: `NOT_APPLICABLE`; release permission is false.

No GitHub or Railway mutation, push, merge, deployment, secret access, human activity, real
eligibility decision, construct work, reliability execution, mapping, publication, or release was
performed.
