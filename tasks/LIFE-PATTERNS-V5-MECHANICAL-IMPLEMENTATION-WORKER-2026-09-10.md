# Life Patterns v5 mechanical implementation worker — 2026-09-10

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Authority

The independent target-theory-blind v5 contract review at `ce04642146c41a7d5d94f85360572c78de887682` PASSED its implementation gate: all 45 original OA blockers plus `NR-001` and `NR2-001` are RESOLVED, no `NR3-*` finding exists, `semantic_change_required=false`, and `safe_for_implementation=true`.

This authorizes **mechanical implementation only**. It does NOT authorize human collection, automated participant coding, target-model scoring/reveal, merge/deploy, recruitment/contact, or spending.

## Required read order

1. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`
2. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-SUMMARY-v1-2026-09-10.json`
3. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
4. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
5. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
6. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
7. current v5 implementation files and their tests.

Do not use target-model information to make neutral-measurement implementation choices.

## Existing implementation work to continue, not restart

The branch already contains:

- `src/hdmatch/evaluation/facet_relation_v5.py`
- `tests/unit/test_facet_relation_v5.py`
- `src/hdmatch/evaluation/development_evidence_v5.py`
- a narrow Ruff compatibility entry in `pyproject.toml`.

At implementation head `0debbb5eeb81235b7dd3041fedcbc73e1b321c7a`, pytest and Ruff passed, while strict mypy failed on mechanical typing issues. **Do not discard the existing implementation.** Fix it and continue.

Known mypy fixes:

- `facet_relation_v5.py`: `json.loads` return should be explicitly cast to `dict[str, Any]`; make the nested ID resolver generic with a `TypeVar` so heterogeneous record maps return their concrete record type rather than `object | None`.
- `development_evidence_v5.py`: `Literal[V5_REVIEW_COMMIT]` is not a valid Literal parameter. Use the exact literal commit string `ce04642146c41a7d5d94f85360572c78de887682` in both response models (and remove an unused constant import if applicable).
- Do not weaken repository-wide strict mypy to hide implementation errors.

## Mechanical implementation requirements

### 1. V5 response graph

Keep historical V1/V2 artifacts immutable. New V5 development responses must mechanically enforce the accepted contract:

- response-level normative containment for facet groups, value assertions, component assertions, absence conditions, provenance records, windows, stages, temporal edges, and evidence units;
- exact-one typed ID resolution within one observable response;
- no dangling, duplicate/ambiguous, or cross-response references;
- every value assertion in exactly one facet group and one stage, with that stage's evidence unit;
- every component assertion in exactly one stage and that stage's evidence unit;
- hybrid components do not create independent occurrence support;
- claim-specific provenance;
- stage/window-local facet cardinality;
- no global `value_relation` field;
- source-supported acyclic temporal partial order only;
- same-act anti-double-counting;
- silence/non-report remains insufficient, never behavioral nonoccurrence.

Add/extend tests for valid and invalid record graphs, including the R05 hybrid example that originally exposed the defect.

### 2. Development response contracts

Finish `development_evidence_v5.py` and add unit tests. Episode and repeated-series responses must bind exactly to their selected task/corpus/source IDs and accepted v5 review. Preserve recurrence-v2 semantics:

- generalized self-report can establish reported recurrence;
- a confirming episode is never independent frequency evidence;
- actual opportunity-level frequency requires sampled/external/mixed evidence basis;
- exception status/frequency and recurrence strength remain separate.

### 3. Versioned V5 human calibration UI

Create a **new versioned V5 builder and tests**. Do not modify historical V2 UI builders or private frozen handoff bytes.

The human UI must be human-first, not schema-first:

- exact narrator source + one behavioral question;
- substantive choices visible immediately;
- group choices by plain-English facet when one observable has multiple facets, so overlapping dimensions are visibly separate;
- do not show `Rxx` IDs as the concept the human must understand;
- no generic `Partially` fit state;
- fallback only when no substantive fact can be selected: `Doesn't apply to this story` / `Not enough information`;
- one-source provenance automatic; where multiple exact sources are present, ask only which exact source supports a selected claim when genuinely needed;
- machine bookkeeping, record IDs, stage IDs, evidence-unit IDs and JSON remain hidden until export.

#### Hybrid affirmative + absence values

Never render a hybrid as generic “did not act”. In particular R05-O2 must distinguish:

1. affirmative fact: narrator accepted/selected an existing or designated default option;
2. separate absence proposition: narrator did not perform additional alternative search during an applicable preselection opportunity.

The four-part absence gate applies only to the absent proposition. If the affirmative component is clear but the absence component is not established, retain the affirmative component and **do not assert the hybrid parent value**. Do not convert silence into absence.

#### Stages / trajectories

- Default a simple source to one stage automatically.
- Different facets can co-occur on one stage without ordering.
- Ask for multiple stages only where the exact source clearly contains distinct events/stages/windows that matter for a same-facet trajectory or an explicit temporal relation.
- Same-facet `zero_or_one` alternatives may appear at different supported stages/windows when permitted by the contract.
- Ask/order stages only when chronology is directly supported by source; never infer order from UI layout or co-presence.

#### Series

Keep the recurrence-v2 repeated-series judgments because they are substantive calibration targets; do not turn anecdotes into independent frequency counts.

#### Export

Export V5 response graphs / V5 episode or series response envelopes plus the existing auditor attestation. Do not make the human enter machine bookkeeping manually.

### 4. Private artifact boundary

Do not commit participant narrative, the private handoff, generated private HTML, completed human responses, or any artifact that embeds private exact source text.

The public builder must accept the exact private handoff at runtime and preserve/verify its bytes or receipt identity before showing evidence. Generated HTML must remain offline/no-network.

## Verification

Before stopping:

- run full pytest;
- Ruff passes;
- strict mypy passes without broad new suppressions;
- add focused V5 graph/development/UI tests;
- if a private handoff is locally available, generate the private V5 HTML and run a headless-browser smoke including no-network checks; otherwise leave generation to the owner/exposed continuation and state this explicitly;
- do not run any automated participant coding or target-model code.

## Repo state update

After green CI, update the public-safe current state / active task / handoff so that the next gate is **owner usability review of the regenerated V5 human UI**. Human first-pass collection remains unauthorized until owner acceptance.

Commit and push all public implementation/test/state work to `codex/discover-life-patterns-mvp`.

Return:

- GitHub-visible implementation commit SHA;
- CI run and conclusion;
- pytest/Ruff/mypy result;
- files added/changed;
- whether a private V5 UI was generated and browser-smoked;
- if generated, only its local filename/hash/size (never commit private bytes);
- exact remaining blocker before independent human collection.
