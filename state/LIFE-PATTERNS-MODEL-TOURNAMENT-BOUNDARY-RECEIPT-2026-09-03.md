# Life Patterns Model Tournament Boundary — Implementation Receipt

Date: 2026-09-03
Status: authorization/manifest boundary implemented and CI-verified on PR #24 development branch. Model execution remains intentionally unavailable. No birth intake, participant analysis, reveal, merge, or deployment authorized.

## Canonical branch

- repository: `u-dont-existDOTcom/humandesign`
- branch: `codex/discover-life-patterns-mvp`
- PR: #24, `WIP: Discover Your Unique Life Patterns MVP`
- exact verification head: `ed57d97628187255fa7458376c77d4b458cc092f`

## Design provenance

Independent conception was preserved before external-method scan:

- `state/LIFE-PATTERNS-MODEL-TOURNAMENT-INDEPENDENT-CONCEPTION-2026-09-03.md`

Existing-work scan and resulting boundary are frozen in:

- `docs/research/LIFE_PATTERNS_MODEL_TOURNAMENT_BOUNDARY_SPEC.md`

The design reuses/adapts:

- preregistration / Registered Reports for confirmatory-vs-exploratory status;
- model-selection-bias and nested-validation literature for development/evaluation separation;
- reusable-holdout/adaptive-analysis principles for untouched final validation;
- strictly proper scoring rules for probabilistic outputs;
- Model-Card-style explicit model identities/limitations;
- dynamic-consent principles for separate secondary-analysis authorization;
- repository-native immutable record, canonical hash, candidate-universe, tie-aware rank, and reveal-phase primitives.

## Implemented contract

`src/hdmatch/evaluation/tournament_manifest.py` implements strict immutable records for:

- participant analysis authorization;
- model manifest entries;
- metric policy;
- tournament manifest payload and artifact.

The core scientific identity is:

`behavioral freeze SHA-256 + tournament manifest SHA-256 + model implementation SHA-256 -> immutable result`

No result type or execution endpoint has been implemented yet.

## Separate analysis authorization

A behavioral freeze continues to mean `model_comparison_authorized=false`.

A separately content-addressed authorization can bind:

- exact session and behavioral freeze identity;
- permitted model-family scope;
- exact-birth-data-use permission;
- result-storage permission;
- research-only vs research+participant-reveal purpose;
- authorization timestamp.

A content-valid authorization may deliberately deny storage, birth-data use, or reveal. Those limits make a proposed execution non-ready; they do not make the authorization artifact itself invalid.

## Immutable tournament manifest

The manifest binds:

- exact behavioral freeze and authorization hashes;
- optional exact birth-input and civil-time-resolution hashes;
- cohort role;
- preregistration status;
- reveal policy;
- exact model roster;
- metric/tie/missing/rejected/uncertain/exclusion policy;
- runtime code identity;
- explicit declaration that target results were not supplied to the builder.

Each model entry binds:

- model/family/scientific status;
- implementation status/version/hash;
- adapter identity/hash;
- **measurement-bridge identity/hash**;
- scoring-contract identity/hash;
- birth-data requirement;
- baseline status;
- output type;
- candidate-universe identity for ranked outputs;
- tuning/search-budget description;
- limitations.

## Executability is distinct from artifact validity

This distinction was explicitly corrected during implementation.

A manifest may be:

- content-valid, immutable, and auditable; yet
- `execution_ready=false` with deterministic blockers.

This lets the project preregister or preserve a comparison contract before all adapters are implemented without pretending the tournament is runnable.

Integrity validation separately rejects tampered content hashes, IDs, or stale stored execution-ready/blocker fields.

## Fail-closed execution blockers

The validator blocks execution for, among other things:

- authorization integrity failure;
- result storage not authorized;
- session/freeze/authorization mismatch;
- model family outside participant authorization;
- no declared non-birth/context baseline;
- too few genuinely distinct non-baseline model families;
- confirmatory manifest without a confirmatory non-baseline model;
- development cohort mislabeled as confirmatory validation;
- birth-dependent roster without participant birth-data permission;
- missing birth/civil-time artifacts;
- participant reveal beyond authorization purpose;
- probabilistic/hybrid output without a predeclared proper scoring rule;
- planned-only model;
- missing implementation, adapter, **measurement-bridge**, or scoring-contract hashes;
- ranked output without a pinned candidate universe.

## Why execution remains blocked

The repository has mature AstroHD symbolic scoring, candidate-universe, leakage/permutation, discrimination, and ranking infrastructure. It does **not** yet have a defensible shared neutral Life-Patterns-to-model measurement layer or a genuinely multi-family executable adapter roster.

Therefore no birth intake, execution endpoint, result artifact, or reveal endpoint was added.

The next scientific blocker is the neutral measurement bridge, whose independent conception is already preserved at:

- `state/LIFE-PATTERNS-MEASUREMENT-BRIDGE-INDEPENDENT-CONCEPTION-2026-09-03.md`

## Verification

Exact GitHub Actions run: `33785114505`
Exact PR merge ref tested the branch head `ed57d97628187255fa7458376c77d4b458cc092f`.

Results:

- `388 passed, 6 skipped`
- tournament-manifest suite: `9 passed`
- behavioral-freeze suite: `10 passed`
- Ruff production/tests: passed
- strict mypy: passed across 134 source files

The six skips are pre-existing shallow-checkout / unavailable-official-Swiss-Ephemeris conditions. No Life Patterns freeze or tournament test was skipped.

## Key implementation commits

- independent tournament conception: `014a6116935c2f1823e910b483f9d748fc1e90ce`
- tournament boundary specification: `7e294c18962342c06149815721c560d9179796c2`
- initial immutable tournament contract: `409ee185e926bae5027fd3802e8bca68761c658d`
- separate artifact integrity from execution readiness: `568922682c954291a7be0f2d56c044e37274a2f5`
- tournament boundary tests: `0dbe780c328d75c439fcee8a6801c3f34e6828e2`
- lint-only test fix: `cded29982f482f0bf1fde6370df9070226167669`
- measurement-bridge independent conception / exact verified head: `ed57d97628187255fa7458376c77d4b458cc092f`
