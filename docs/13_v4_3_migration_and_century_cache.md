# 13 — V4.3 Migration and Precomputed Century Cache

## Purpose

Upgrade the research harness from the legacy V4.1/V3.2 symbolic implementation to the V4.3/V3.5 model without silently simplifying the scoring theory.

## Normative inputs

For new symbolic development runs, use:

1. `reference/core/v4_3_scoring_algorithm.md`
2. `reference/core/behavioral_target_combined_v3_5.md`
3. `reference/core/human_design_search_instructions_fixed_candidate_blind(6).md` for the original detailed V3 mechanics unless superseded by V4.3
4. `reference/core/human_design_reverse_matching_protocol_v4_1.md` only as historical background for sections not superseded by later protocol material

The current Python implementation still reflects V4.1/V3.2 assumptions and MUST NOT identify itself as V4.3 until the migration tests below pass.

## Required implementation changes

### Mapping schema

Add:

- `flexibility_class`
- `flexibility_factor`
- richer chart predicates for Gate, Line, Channel, planetary carrier, cardinal activation, Definition and conditional conjunctions
- prevalence parent metadata
- revision provenance metadata where human target observations are represented directly
- `required_feature_registry`

A frozen mapping with a feature predicate unsupported by the candidate feature vector is a hard error.

### Scoring

Implement `reference/core/v4_3_scoring_algorithm.md` exactly.

Do not replace it with architecture-only scoring. Do not omit the flexibility factor. Do not numerically add CoreFit to NetInformation.

### Full-universe reruns

After accepted target or mapping revisions, rescore the complete declared universe. A finalist-only re-score may be displayed for debugging but cannot be called a V4.3 ranking.

## Precomputed 100-year cache

### Why

The expensive part of global recovery is astronomical state generation, not target-specific scoring. Candidate chart states should therefore be built once, verified, versioned, and reused across profiles.

### Canonical horizon

Initial cache horizon:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

The end is exclusive.

### Storage format

Preferred:

```text
data/century_cache/v1/
    manifest.json
    states-1926-1935.parquet.zst
    states-1936-1945.parquet.zst
    ...
    states-2016-2026.parquet.zst
    prevalence-v4_3.json.zst
```

Use Zstandard compression. Shard by fixed UTC year ranges so updates and verification do not require replacing one giant binary.

If GitHub repository size becomes impractical, store the shards as versioned GitHub Release assets or Git LFS objects and keep `manifest.json` plus the generation/verification code in the repository. The repo must never silently download an unversioned mutable cache.

### Minimum state columns

Each exact interval row must include:

```text
state_id
utc_start
utc_end
duration_seconds
personality activations: body, gate, line [and substructure when available]
design activations: body, gate, line [and substructure when available]
design_timestamp
type
strategy
authority
profile
defined_centers
channels
definition
nodes
cardinal activations
feature_vector_schema_version
astronomy_engine_version
ephemeris_file_set_hash
node_convention
mandala_mapping_version
```

Prefer typed/list columns over JSON blobs where Parquet supports them.

### Manifest

`manifest.json` must include:

```text
cache_version
feature_vector_schema_version
utc_start
utc_end_exclusive
interval_count
uncompressed/canonical row hash strategy
per-shard sha256
combined universe hash
boundary policy version
design-root tolerance
ephemeris engine + version
ephemeris file hashes
node convention
mandala mapping hash
generation commit
created_at
verification status
```

### Runtime policy

Normal 100-year search MUST prefer the verified cache.

1. Verify manifest and shard hashes.
2. Verify requested UTC range is covered.
3. Verify required mapping features are present.
4. Verify astronomy/model metadata match the requested run.
5. Load prevalence table only if its universe hash and policy version match.
6. Score all matching exact intervals.
7. Fail closed on incompatibility unless the caller explicitly invokes rebuild mode.

### Build command

Add a CLI similar to:

```bash
hdmatch build-century-cache \
  --start 1926-08-22T00:00:00Z \
  --end-exclusive 2026-08-23T00:00:00Z \
  --output data/century_cache/v1

hdmatch verify-century-cache data/century_cache/v1

hdmatch recover-global \
  --cache data/century_cache/v1 \
  --target <target> \
  --mapping-library <mapping>
```

`recover-global` must not regenerate astronomy when a compatible verified cache exists.

## Anti-simplification compliance gate

Create one canonical compliance function/test that asserts:

```text
reported_model_version == V4.3
=> mapping schema supports flexibility
=> required_feature_registry coverage == 100%
=> exact interval source is verified
=> conditional prevalence policy is active
=> dependency control active
=> full-universe scoring active
=> ranking tuple exactly matches V4.3
```

A reduced model must identify itself honestly, e.g. `M0-architecture-only`, and its output must contain `v4_3_compliant: false`.

## Mutation tests

The suite must fail after deliberate mutations that:

- remove flexibility multiplication;
- ignore Gate/Line predicates;
- treat missing required candidate features as non-match;
- add CoreFit to NetInformation;
- sum alternative pathways;
- disable conditional prevalence;
- exceed corroboration cap;
- rescore only finalists after target updates;
- use coarse hourly sampling;
- accept cache hash mismatch.

These are not optional quality checks. They are the mechanism that prevents future threads/agents from implementing a superficially similar but materially simpler algorithm.
