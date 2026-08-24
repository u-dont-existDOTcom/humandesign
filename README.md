# HD Reverse-Matching Research Harness

This repository contains a typed Python harness for blinded Human Design birth-moment reverse-matching research. Human Design is treated as an experimental symbolic hypothesis. Synthetic recovery validates engineering coherence only; it does not validate Human Design in humans.

## Current model status

The normative development model is now **V4.3 / behavioral target V3.5**.

Start with:

- `AGENTS.md`
- `reference/core/v4_3_scoring_algorithm.md`
- `reference/core/behavioral_target_combined_v3_5.md`
- `docs/13_v4_3_migration_and_century_cache.md`
- `CODEX_V4_3_MIGRATION_PROMPT.md`

The existing Python implementation was originally built around V4.1/V3.2 and must not call itself V4.3 until the migration/compliance tests pass. Reduced architecture-only runs must be labeled reduced and emit `v4_3_compliant=false`.

## Environment

Required: Python 3.11 or newer. The tested development runtime is Python 3.12.

```bash
bash scripts/bootstrap.sh
source .venv/bin/activate
```

Swiss Ephemeris is an optional engine dependency with AGPL/professional dual licensing. Exact production runs must point to declared local ephemeris files and will fail rather than silently use Moshier. See `docs/PRIOR_WORK_SCAN.md`.

## Verification

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check src tests scripts
.venv/bin/mypy src/hdmatch
```

The task-specific milestone gate is:

```bash
.venv/bin/python scripts/task_acceptance.py
```

Ordinary green legacy tests do not by themselves prove V4.3 compliance. The migration must add anti-simplification/mutation tests described in `docs/13_v4_3_migration_and_century_cache.md`.

## Blind workflow

The CLI exposes separate commands for generation, recovery, prediction freeze, and reveal/evaluation. Keep the answer-key encryption key outside this repository and outside the decoder workspace. The default known-month configuration is the bounded 75-case Model A engineering smoke; the deferred 1,000-case configuration is not an acceptance default.

```bash
hdmatch generate-blind \
  --config configs/synth_month.yaml \
  --run-dir run_artifacts/model_a_smoke \
  --ephemeris /path/to/declared-swiss-files

hdmatch recover \
  --run-dir run_artifacts/model_a_smoke \
  --ephemeris /path/to/declared-swiss-files \
  --cache-dir run_artifacts/candidate_cache

hdmatch freeze --run-dir run_artifacts/model_a_smoke

hdmatch reveal-evaluate --run-dir run_artifacts/model_a_smoke
```

Generation creates or uses an owner-only AES key under `/tmp/hdmatch-secrets` by default, but ordinary command output does not disclose its path. Recovery accepts no key or answer-key path and performs a plaintext-answer-key preflight before scoring. That scan is defense in depth, not a substitute for running the decoder in a separate keyless operating-system user, container, or equivalent access boundary. Reveal binds the exact encrypted envelope and canonical decrypted payload; evaluation refuses a different in-memory key. Exact ephemeris files and their hashes must be supplied for every chart run.

Claim-grade synthetic recovery uses the fail-closed Bubblewrap wrapper and a separate
empty decoder output directory; see `docs/16_claim_grade_keyless_recovery.md`. The
wrapper mounts only tracked decoder code and declared public artifacts, disables the
network namespace, accepts no reveal/key capability, and writes a canonical isolation
receipt. External operator/runtime evidence remains required because application code
cannot prove its own host isolation.

The completed smoke report is in `reports/model_a_smoke_75/`. It retains all 41 non-Top-1 cases and explains the residual failure classification.

## Synthetic noise-tier comparison

The bounded noise smoke uses four 25-case configs:
`synth_month_oracle_noise_smoke.yaml`, `synth_month_low_smoke.yaml`,
`synth_month_medium_smoke.yaml`, and `synth_month_adversarial_smoke.yaml`.
Generate the four runs with the same external secret seed so they conceal the same
birth moments, then run the normal recover → freeze → reveal/evaluate sequence for
each directory. Do not compare an interrupted or unrevealed run.

After all four canonical `evaluation.json` files exist, aggregate them without
opening an answer key:

```bash
hdmatch compare-noise-tiers \
  --oracle-run-dir run_artifacts/noise_oracle \
  --low-run-dir run_artifacts/noise_low \
  --medium-run-dir run_artifacts/noise_medium \
  --adversarial-run-dir run_artifacts/noise_adversarial \
  --output run_artifacts/noise_comparison.json
```

This command reads the complete public provenance chain: blind input, recovery
manifest, predictions, prediction freeze, reveal record, encrypted envelope, and
post-reveal evaluation. It decrypts nothing. It verifies exact bytes, recovery-config
hash, frozen model and noise settings, envelope path/hash, freeze/reveal bindings,
timestamp ordering, candidate-universe binding, case denominator, aggregation rule,
and revealed target consistency. The report preserves every tier, failure, and
unevaluable case and shows Top-1/3/5 and MRR degradation from oracle. It is an
engineering robustness result, not human validation.

## Model A and Model B

`MODEL-A-CORE-V1` is the unchanged coarse architecture model. `MODEL-B-DETAILED-V1` is a structural-only intermediate containing all source-supported detailed mechanics: 36 complete channels, separate Personality/Design Sun–Earth gate and line representations, Definition, mechanics-only repeated gates and Nodes, a deliberately empty unresolved prominent-activation allowlist, hanging-gate candidates, dependency controls, and the conditional-prevalence framework. It is not completion of the detailed behavioral-model objective.

Rebuild either frozen artifact with:

```bash
hdmatch compile-model --model MODEL-A-CORE-V1
hdmatch compile-model --model MODEL-B-DETAILED-V1
```

Select Model B for generation and recovery by passing the same explicit model identity to both commands:

```bash
hdmatch generate-blind --config configs/synth_month.yaml --run-dir run_artifacts/model_b_smoke --ephemeris /path/to/declared-swiss-files --model MODEL-B-DETAILED-V1
hdmatch recover --run-dir run_artifacts/model_b_smoke --ephemeris /path/to/declared-swiss-files --cache-dir run_artifacts/candidate_cache --model MODEL-B-DETAILED-V1
```

The legacy result proves that an earlier D1–D10/A1–A6 detailed scorer existed. A source-recovery audit found the exact frozen target and generic rubric, but not the pre-search per-observation definitions, selectors, roles, directness assignments, dependency clusters, or contradictions. The eight V1 behavioral-family placeholders remain `unresolved`; that status is an intermediate limitation, not an acceptance condition or a completed Model B. Model B V1 currently generates and scores only its unchanged Model A behavioral base, so no behavioral A/B benchmark may run until a provenance-reviewed Model B actually produces different behavioral predictions. See `reports/model_b_source_recovery_audit.md` and the machine-readable audit under `mappings/`.

The detailed mechanics can still be audited as a clearly labeled structural-resolution upper bound, using no responses or answer keys:

```bash
hdmatch compare-models \
  --cache-dir run_artifacts/candidate_cache \
  --ephemeris /path/to/declared-swiss-files \
  --year 2000 \
  --timezone UTC \
  --output run_artifacts/structural_comparison.json
```

Over the retained 13,777 exact 2000/UTC intervals, Model A produced 950 structural signatures and Model B 2,963. This shows additional mechanical partitioning only—not behavioral observability, recovery, or human validity. The transparent summary is in `reports/model_b_structural_audit_2000/`.

### Prospective MODEL-B-DETAILED-V2-NEW

`MODEL-B-DETAILED-V2-NEW` is a prospective detailed symbolic hypothesis. It is
not a reconstruction of the lost historical D1–D10/A1–A6 scorer. Its
questionnaire mappings were preregistered before candidate scoring. The V2
provenance amendment adds retrieval-level records without changing any frozen
observation, pathway, token, constant, or discovery/holdout assignment.

The normative source chain is:

- `reference/prospective/model_b_detailed_v2_new_source_retrieval_manifest_v1.json`;
- `reference/prospective/model_b_detailed_v2_new_sources_v2.json`;
- `reference/prospective/model_b_detailed_v2_new_preregistration_v2.json`.

Every external record contains its exact URL, access timestamp, locator, and
either the SHA-256 of the exact retrieved response body or an explicit
legal/technical reason why no body/hash was retained. Check the deterministic
provenance build with:

```bash
.venv/bin/python scripts/build_model_b_v2_new_provenance.py --check
```

The required experiment order is enforced, not advisory:

```text
preregistration → deterministic compile → clean-tree model freeze
→ answer-key-free behavioral-difference audit → PASS
→ synthetic generation → blind recovery
```

Compile and freeze from a clean committed source tree:

```bash
hdmatch compile-model-b-v2-new \
  --preregistration reference/prospective/model_b_detailed_v2_new_preregistration_v2.json \
  --output mappings/model_b_detailed_v2_new_compiled_v2.json

hdmatch freeze-model-b-v2-new \
  --preregistration reference/prospective/model_b_detailed_v2_new_preregistration_v2.json \
  --compiled mappings/model_b_detailed_v2_new_compiled_v2.json \
  --output mappings/model_b_detailed_v2_new_freeze_v2.json \
  --source-software-commit COMMITTED_SHA \
  --source-software-tree COMMITTED_TREE_SHA
```

Then audit one retained exact public month cache. The audit is preserved whether
it passes or fails:

```bash
hdmatch audit-model-b-v2-new-difference \
  --cache-dir run_artifacts/known_month_oracle_1000/candidate_cache \
  --ephemeris data/ephemeris \
  --year 2000 --month 1 --timezone UTC \
  --mapping mappings/mapping_library_v1.json \
  --model-b-v2-compiled mappings/model_b_detailed_v2_new_compiled_v2.json \
  --model-b-v2-freeze mappings/model_b_detailed_v2_new_freeze_v2.json \
  --output reports/model_b_v2_new/behavioral_difference_2000_01_UTC.json
```

V2 generation and recovery both require the exact passing audit and exact cache
file. Verification re-runs the public difference computation and rejects a
missing, failed, fabricated, stale, or mismatched artifact before generation or
recovery scoring:

```bash
hdmatch generate-blind \
  --config configs/model_a_v2_new_paired_oracle_75.yaml \
  --run-dir /protected/model-b-v2-generation \
  --ephemeris data/ephemeris \
  --model MODEL-B-DETAILED-V2-NEW \
  --model-b-v2-compiled mappings/model_b_detailed_v2_new_compiled_v2.json \
  --model-b-v2-freeze mappings/model_b_detailed_v2_new_freeze_v2.json \
  --model-b-v2-difference-audit reports/model_b_v2_new/behavioral_difference_2000_01_UTC.json \
  --model-b-v2-difference-cache run_artifacts/known_month_oracle_1000/candidate_cache/month-2000-01-UTC-09e811ca0fe51797.json

hdmatch recover \
  --run-dir /public/model-b-v2-decoder-output \
  --blind-file /public/model-b-v2-generation/blind_cases.json \
  --ephemeris data/ephemeris \
  --cache-dir run_artifacts/known_month_oracle_1000/candidate_cache \
  --model MODEL-B-DETAILED-V2-NEW \
  --model-b-v2-compiled mappings/model_b_detailed_v2_new_compiled_v2.json \
  --model-b-v2-freeze mappings/model_b_detailed_v2_new_freeze_v2.json \
  --model-b-v2-difference-audit reports/model_b_v2_new/behavioral_difference_2000_01_UTC.json \
  --model-b-v2-difference-cache run_artifacts/known_month_oracle_1000/candidate_cache/month-2000-01-UTC-09e811ca0fe51797.json
```

Only a PASS with at least one genuine non-unknown response difference and zero
adverse tie-split groups authorizes the small paired Model A/V2 oracle experiment.
Both arms must use the same external secret seed and otherwise identical config;
revealed target-set identity must match before metrics are compared. V2 remains
engineering discovery-only, its holdout pathways remain frozen and withheld, and
no result is human validation. The previously committed V1 compile/freeze is a
superseded pre-provenance-hardening artifact and must not authorize generation.

The paired workflow is fail-closed at four additional boundaries. First,
`plan-paired-model-a-v2-new` binds the public configuration, common secret-seed
commitment, exact Model A/V2 identities, and verified PASS audit before either arm
is generated. Each generation and keyless recovery then binds that plan and its
arm. After both ordinary prediction freezes exist,
`freeze-paired-model-a-v2-new` binds both complete public chains before either
answer key may be revealed. Finally, `compare-paired-model-a-v2-new` recomputes
the metrics from frozen predictions and reveal-authenticated public dates; it
rejects different target sets, seeds, caches, ephemeris bytes, source trees,
software environments, settings, timestamps, or incomplete isolation receipts.
The comparator accepts no key or decrypt interface. See
`docs/16_claim_grade_keyless_recovery.md` for the paired invocation and mount
contract.

## Precomputed 100-year universe

The expensive astronomical candidate universe should be generated once, verified, versioned, and reused across behavioral targets.

Initial canonical range:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

The migration target uses Zstandard-compressed Parquet shards plus a cryptographic manifest and cached duration-weighted prevalence tables. Normal broad searches should load the verified cache instead of rebuilding a century of exact states for every person.

If binary shards are too large for ordinary Git history, store them in Git LFS or versioned GitHub Release assets. Keep the manifest, schema, generation code, and verification code in the repository.

## Research claim boundary

The project explicitly allows **post-hoc fitting on human development data**.

That is not a methodological error. It is the training stage.

The error would be fitting a model to people and then citing its performance on those same people as evidence that it predicts new people.

The intended cycle is:

```text
development humans
    ↓
fit / revise / learn
    ↓
freeze model version
    ↓
untouched humans
    ↓
prospective evaluation
    ↓
new version if needed
    ↓
new untouched test
```

Synthetic tests come first to validate the machinery.

## Reference material

`reference/core/` contains the scoring/search/questionnaire specifications and current target material.

`reference/verified_cases/` contains externally checked chart fingerprints useful for calculation parity/golden tests. These are references, not behavioral training targets unless a study explicitly declares them as such.

`reference/legacy_runs/` contains previous search outputs for regression/debugging only. Legacy/simplified result files must never be mined as a mapping source.

`reference/custom_gpt/` contains the Custom GPT/transit materials, which are secondary to the research harness.

`reference/research/` contains methodological context.

## Security

For a real blind run, keep the answer key outside this project/workspace or encrypted with a passphrase unavailable to the decoder until predictions are frozen.
