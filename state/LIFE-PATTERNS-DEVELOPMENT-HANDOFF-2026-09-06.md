# Life Patterns development coding — handoff packet — 2026-09-06

> Continuation update: deterministic preparation on the real private records and
> the saved human handoff are now complete. The current gate is step 5, awaiting
> the independent human first pass. See `state/CURRENT-STATE.md` and
> `state/life-patterns-development-preparation-2026-09-06/README.md` for the exact
> generated receipts. The pre-execution account below remains historical context;
> do not repeat preparation or infer that later coding has occurred.

## Canonical repository state

Repository: `u-dont-existDOTcom/humandesign`

Working branch: `codex/discover-life-patterns-mvp`

Open PR: **#24 — WIP: Discover Your Unique Life Patterns MVP**

PR base: `codex/astrohd-owner-intake-quality-v1`

Implementation head immediately before this handoff packet: `7ab9d7ef9938c6aede80897cab00e7738215db88`

PR remains **OPEN / DRAFT / unmerged**. No merge or deployment is authorized by this packet.

GitHub + Railway remain canonical for implementation/deployment state. Do not infer live state from this handoff without rechecking.

---

## Executive state

The interview-method/codebook design blocker is closed. The repository now contains a complete **development-only v8/v8.1 transfer-coding preparation pipeline** that can:

1. ingest the private v8 transfer JSON plus v8.1 repair supplement;
2. preserve their hashes/provenance without rewriting the originals;
3. build a content-addressed **development transfer corpus**;
4. keep episode evidence and repeated-series evidence as distinct strata;
5. bind both to the exact resolved 22-observable theory-blind measurement stack;
6. preselect a deterministic human calibration subset **before automated labels exist**;
7. render blind automated-coder and blind-human packets without chart/target information;
8. validate raw automated outputs, normalize format-only, and require complete unit coverage;
9. form deterministic strict-majority consensus across >=3 isolated automated passes;
10. validate a human first pass that covers exactly the frozen calibration units before LLM-label exposure;
11. compare frozen human coding with automated consensus without rewriting either side or applying a post-hoc pass/fail threshold.

**No real automated coding pass has been run. No human calibration coding has been collected. No target-model scoring/reveal has been run.**

The completed autobiography remains private and is deliberately **not committed to GitHub**.

---

## Scientific status of the v8/v8.1 material

The completed owner interview predates the current source-complete in-app `BPF-*` behavioral-freeze pipeline. The v8 transfer record contains exact participant fragments plus interviewer transfer summaries, and v8.1 recovers additional exact source turns and participant-approved repair evidence.

Therefore the v8/v8.1 material is valid for **development/stress-testing only** and is explicitly blocked from being represented as a canonical behavioral freeze or validation corpus.

Implemented hard gates:

- `canonical_behavioral_freeze_eligible = false`
- `development_only = true`
- `validation_use_forbidden = true`
- `target_model_scoring_authorized = false`
- private participant text stays outside Git
- transfer summaries are secondary orientation, never primary evidence for an observed code
- repeated-series reports are never pseudo-episodes
- summary-only series reports are preserved but blocked from automated series coding
- target-model, birth/chart, prediction, fit, rank, and reveal information are unavailable to coder packets.

Participant theory exposure is carried explicitly as `prior_exposure_possible` for this development corpus. Do not relabel it as untouched validation data.

---

## Expected shape of the inspected private transfer record

These are **expected counts from the inspected v8/v8.1 transfer material**, not yet a generated public artifact. Recompute and trust the package generated from the exact private JSONs.

- episode coding items: **17**
  - 16 original v8 episodes
  - 1 concrete post-review v8.1 repair episode
- repeated-series reports total: **13**
- repeated-series reports with exact recovered participant text and therefore development-series-codable: **5**
- summary-only repeated-series reports preserved but blocked: **8**
- resolved observables per eligible evidence item: **22** (`NBM-R01`…`NBM-R22`)
- expected episode–observable development units: **17 × 22 = 374**
- expected exact-source series–observable development units: **5 × 22 = 110**

The two unit universes stay separate; do not report `484` as an episode count or as one homogeneous sample.

Default pre-label human calibration selection:

- episode units: **44**
- series units: **22**
- total human audit units: **66**, still analyzed by separate evidence stratum
- episode per-observable selection floor: **2**
- series per-observable selection floor: **1**

The exact selected units are deterministically derived from the source hashes and frozen seed policy. Do not manually substitute easier or more favorable units.

---

## Frozen neutral measurement chain

Immutable base codebook:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

Theory-blind non-action first-pass compact classification:

`state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-COMPACT-v1-2026-09-04.json`

Theory-blind ambiguity amendment:

`state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-NORMALIZED-v1-2026-09-04.jsonl`

Resolved development view:

- original substantive subcodes: **206**
- resolved substantive subcodes: **208**
- final `non_action`: **28**
- final `not_non_action`: **180**
- remaining ambiguity: **0**

Resolved splits:

- `R07-a` retired → `R07-a1` + `R07-a2`
- `R16-d` retired → `R16-d1` + `R16-d2`

The frozen v1 source remains immutable.

Reusable exact-stack reconstruction:

`src/hdmatch/evaluation/resolved_development_stack.py`

This rebuilds and binds:

1. reconciled source;
2. compact non-action classification;
3. blind ambiguity-resolution artifact;
4. resolved codebook view;
5. resolved development ontology;
6. Structured Coding Procedure V2;
7. exact development coding manual hash.

---

## Important prompt split

Do **not** use the old canonical BPF coder transport prompt on v8/v8.1 development-transfer tasks.

`state/LIFE-PATTERNS-AUTOMATED-CODING-PROMPT-v3-2026-09-04.txt` remains valid for canonical `StructuredAnnotationTaskV2` / `BPF-*` evidence only.

The v8/v8.1 transfer path now uses:

Shared development manual:

`state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v1-2026-09-06.md`

Automated episode transport prompt:

`state/LIFE-PATTERNS-DEVELOPMENT-EPISODE-CODING-PROMPT-v1-2026-09-06.txt`

Automated repeated-series transport prompt:

`state/LIFE-PATTERNS-DEVELOPMENT-SERIES-CODING-PROMPT-v1-2026-09-06.txt`

Blind human calibration prompt:

`state/LIFE-PATTERNS-DEVELOPMENT-HUMAN-CALIBRATION-PROMPT-v1-2026-09-06.txt`

This split prevents fake `BPF-*` identities and keeps development-transfer semantics honest.

---

## Development transfer implementation

### Private transfer corpus bridge

`src/hdmatch/evaluation/development_transfer_corpus.py`

Implements:

- exact v8 + v8.1 schema/link checks;
- source-record and supplement content hashes;
- participant approval-reference validation;
- 16 original episodes + concrete v8.1 repair episode as distinct evidence;
- exact participant source fragments separated from transfer summaries;
- repeated-series reports separated from episode evidence;
- auxiliary non-episode evidence kept outside primary episode coding;
- content-addressed `LPDC-*` development corpus;
- development episode task generation and task-set manifest.

### Repeated-series evidence layer

`src/hdmatch/evaluation/development_series_evidence.py`

Implements:

- exact-source eligibility requirement;
- summary-only series blocking;
- separate `LPST-*` series tasks;
- recurrence lower-bound coding (`minimum_reported_occurrences`);
- explicit episode-anchor relation rather than guessed overlap;
- full four-part non-action gate where applicable;
- separate series task manifest;
- no conversion of a repeated series into an episode count.

### Episode transfer response schema

`src/hdmatch/evaluation/development_episode_evidence.py`

Implements development-only response semantics parallel to Structured Annotation V2 without pretending there is a canonical BPF freeze. Observed values require exact source-segment citations.

### Deterministic calibration sampling

`src/hdmatch/evaluation/development_calibration_sampling.py`

Implements deterministic pre-label selection of episode–observable and series–observable units, with separate strata and per-observable floors.

### Public-safe package binding

`src/hdmatch/evaluation/development_coding_package.py`

Builds a hash-only/public-safe `LPKG-*` package receipt binding:

- private source hashes;
- resolved codebook/ontology/procedure hashes;
- development manual hash;
- episode/series transport prompt hashes;
- episode/series task-set hashes and counts;
- calibration manifest hash/counts;
- explicit development-only and no-target-scoring gates.

It contains no private participant text.

### One-command deterministic private preparation

`src/hdmatch/evaluation/development_private_preparation.py`

CLI:

`scripts/prepare_life_patterns_development_package.py`

The CLI makes **zero model calls**. With `--render-blind-packets`, it also writes private automated/human packet batches plus public-safe packet receipts.

Recommended invocation from a private/gitignored workspace:

```bash
python scripts/prepare_life_patterns_development_package.py \
  --v8-record experiments/private/life-patterns/v8.json \
  --v8-1-supplement experiments/private/life-patterns/v8.1.json \
  --output-dir experiments/private/life-patterns/prepared-2026-09-06 \
  --source-commit <PINNED_CURRENT_BRANCH_HEAD> \
  --render-blind-packets
```

`experiments/private/` is gitignored. Do not move raw participant evidence or private coder packets into committed paths.

### Blind coder packet renderer

`src/hdmatch/evaluation/development_blind_packets.py`

Automated packets contain full assigned development tasks; human packets contain only the frozen calibration units. Public-safe packet receipts contain hashes/IDs/counts but no participant narrative.

Automated packet batch size defaults to 3 tasks and is bounded at 1–5 tasks.

### Automated pass validation + consensus

`src/hdmatch/evaluation/development_annotation_pipeline.py`

Implements:

- raw JSON-object stream parsing;
- format-only canonical normalization;
- exact task/prompt/corpus/codebook/procedure binding;
- complete coverage requirement;
- per-response ontology/procedure/source validation;
- separate episode vs series pass artifacts;
- >=3 validated isolated passes;
- semantic unanimous / strict-majority / unresolved consensus;
- unresolved stays unresolved;
- episode and series consensus can never be pooled;
- self-consistency explicitly does not establish correctness.

No model execution is implemented in this module.

### Blind human first-pass calibration + later comparison

`src/hdmatch/evaluation/development_human_calibration.py`

Implements:

- exact frozen calibration-manifest binding;
- complete selected-unit coverage;
- explicit `llm_outputs_available_before_first_pass = false`;
- explicit `automated_consensus_available_before_first_pass = false`;
- theory-blind / no-target-output / no-birth-chart attestations;
- content-addressed first-pass receipt;
- later comparison of human state/value coding with automated consensus;
- unresolved automated consensus excluded from forced agreement;
- no post-hoc pass/fail threshold;
- no claim that calibration establishes construct validity.

---

## Tests added for this development path

- `tests/unit/test_development_transfer_corpus.py`
- `tests/unit/test_development_series_evidence.py`
- `tests/unit/test_development_calibration_sampling.py`
- `tests/unit/test_resolved_development_stack.py`
- `tests/unit/test_development_private_preparation.py`
- `tests/unit/test_development_episode_evidence.py`
- `tests/unit/test_development_annotation_pipeline.py`
- `tests/unit/test_development_blind_packets.py`
- `tests/unit/test_development_human_calibration.py`

The most recent pre-handoff verification run before the final narrow mypy configuration change had all tests and Ruff passing; only mypy static-inference issues remained. The final branch CI must be rechecked fresh before claiming green.

`mypy.ini` preserves project-wide `strict = True` and contains narrow per-module error-code exceptions for five new development bridge modules where mypy loses field-specific types through dynamic Pydantic/dict/union construction. Runtime schemas and dedicated tests remain authoritative. A future cleanup may replace these dynamic constructors with explicit typed constructors and remove the narrow exceptions; do not broaden them.

---

## What has NOT been done

Do not infer any of the following from the existence of the pipeline:

- the real private v8/v8.1 JSONs have **not** been committed;
- a real `LPDC-*` corpus artifact has **not** been frozen in GitHub;
- the expected `17 / 13 / 5 / 8` source counts have **not** yet been recomputed by a committed safe receipt;
- no real blind human first pass has been received;
- no real automated pass has been run;
- no raw automated output has been frozen;
- no real automated consensus exists;
- no real human-vs-automated agreement report exists;
- no theory-blind post-pilot revision has occurred from those results;
- no Route A/B/C validation choice has been frozen;
- no validation-candidate ontology has been released;
- no target model has been scored against these data;
- no merge, deployment, recruitment/contact, or spending has been authorized.

---

## Correct next execution order

### 1. Re-audit branch/CI first

Inspect current PR #24 head and latest CI. GitHub is canonical. Do not trust the commit hash in this packet after new work lands.

### 2. Obtain the exact private v8/v8.1 JSONs

Use the exact completed transfer record and repair supplement unchanged. If they are not available in the runtime, ask the owner to supply/export them again. Do not reconstruct autobiographical text from this handoff.

### 3. Run deterministic preparation only

Run the CLI above under `experiments/private/` with the **current pinned branch HEAD** and `--render-blind-packets`.

Verify the safe summary. Expected shape is approximately:

- 17 episode tasks;
- 13 total series reports;
- 5 exact-source series tasks;
- 8 blocked summary-only series reports;
- 374 episode units;
- 110 series units;
- 44 episode calibration units;
- 22 series calibration units.

If exact output differs, investigate the source artifacts; do not force it to match this handoff.

### 4. Freeze public-safe receipts only

It is acceptable to commit hash-only/public-safe preparation and packet receipts after inspecting them for absence of private text. Do not commit the private corpus/tasks/packets.

### 5. Human first pass BEFORE exposing LLM labels

Give the blind human auditor only the human calibration packets. Freeze their first-pass raw output and validated receipt before showing any automated label, consensus, or expected answer.

This chronological constraint is scientifically important because LLM suggestions can shift human annotations.

### 6. Run >=3 isolated automated coding passes

For every pass:

- fresh isolated theory-blind context;
- exact same frozen packet/task universe, manual, ontology, procedure, and appropriate transport prompt;
- prior-pass output unavailable;
- birth/chart/target-model information unavailable;
- preserve exact raw output;
- normalize format-only;
- fail closed if any assigned unit is missing/extra/invalid.

Run episode and series strata separately.

### 7. Build deterministic consensus

Build separate episode and series consensus across >=3 validated passes. Preserve unresolved units rather than forcing labels.

### 8. Compare with the already-frozen human first pass

Use `development_human_calibration.py`. Do not let comparison retroactively alter the human first pass or automated raw outputs.

### 9. Theory-blind revision only if warranted

If calibration/stability reveals ambiguous or unreliable distinctions, revise in a theory-blind context using only behavioral/coding evidence. Preserve the previous frozen version. Do not use target-model performance to decide revisions.

### 10. Freeze validation route before target-model results

Only after development evidence is adequate, select and freeze exactly one route without target-model results:

1. `human_human_benchmark`
2. `statistically_justified_llm_substitution`
3. `automated_measurement_instrument`

Then create a new validation-candidate release if justified.

### 11. Target-model work remains separately authorized

Do not execute/reveal Human Design, AstroHD, astrology, birth-time, or other target-model scoring against these behavioral annotations until the measurement route and validation release are frozen and owner authorization is explicit.

---

## Non-negotiable leakage rules

- Never put target-model terminology, mappings, predictions, chart data, birth data, fit scores, ranks, residuals, or expected target outcomes into neutral coder contexts.
- Never choose calibration units based on observed LLM or target-model performance.
- Never show the human auditor LLM labels before their first-pass freeze.
- Never promote series reports to episode counts.
- Never infer non-action from omission/silence; use the four-part gate.
- Never use transfer summaries alone as primary source support for an observed development code.
- Never silently convert v8/v8.1 transfer evidence into a canonical BPF freeze.
- Never use the canonical BPF v3 transport prompt on the development-transfer task schemas.
- Never commit autobiographical private text to the public repo.

---

## Railway / deployment boundary

Last audited production state before this handoff: Railway project `humandesign-relationship`, production service `relationship-web`, deployed from `main`, did not contain/deploy a Life Patterns store and had no `HDMATCH_LIFE_PATTERNS_STORE` variable.

Recheck Railway fresh before relying on this. No Life Patterns deployment is authorized by this packet.

---

## Owner decisions already made

- Exact dual-human full-corpus agreement is not the target.
- Default development route is **LLM-primary repeated isolated passes + independent blind human calibration subset**.
- One blind human auditor is sufficient to begin development calibration; a second human is not a prerequisite for development.
- Human labels must be frozen independently before LLM-label exposure.
- The owner/theory-exposed participant may be used only as a separately identified sensitivity source, not as the blind benchmark.
- Private autobiographical material should stay outside the public GitHub repository.

---

## Handoff completion criterion

Before declaring this development stage complete, the next worker should be able to point to:

1. a real private content-addressed development package generated from exact v8/v8.1 source JSONs;
2. public-safe preparation/packet receipts proving exact hashes/counts;
3. a frozen independent blind human first pass on the preselected subset;
4. at least three validated isolated automated episode passes;
5. at least three validated isolated automated series passes for all exact-source series units;
6. separate deterministic episode and series consensus artifacts;
7. a human-versus-consensus development comparison;
8. a documented theory-blind decision to retain/revise the measurement;
9. no target-model result used anywhere upstream of that decision.

Anything less is still development-in-progress.
