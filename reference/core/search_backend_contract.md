# Deterministic Search Backend Contract

## Purpose

A Custom GPT should conduct the interview and maintain the audit trail. It should not improvise astronomical calculations. This backend performs chart generation, exact boundary segmentation, scoring, and candidate-difference analysis.

## Non-negotiable properties

- deterministic results for identical inputs;
- versioned chart engine, ephemeris, timezone database, mapping library, and scoring model;
- no access to the sealed true-candidate answer key;
- opaque candidate IDs until reveal;
- complete input/output hashes;
- exact historical local-to-UTC handling;
- exact 88-degree Design-time root;
- event-based boundary segmentation;
- no silent Moshier or other fallback;
- independent-engine validation status;
- full-universe rerun after every frozen answer batch.

## Recommended endpoints

### `POST /v1/runs`

Create an auditable run.

Input:

```json
{
  "search_mode": "bounded",
  "candidate_universe_sha256": "...",
  "profile_sha256": "...",
  "question_bank_version": "1.0.0",
  "mapping_library_version": "...",
  "scoring_model_version": "v4-symbolic",
  "holdout_seed": 42
}
```

Output:

```json
{
  "run_id": "run_...",
  "status": "created",
  "engine_manifest": {
    "chart_engine": "...",
    "ephemeris": "...",
    "tzdb": "...",
    "commit": "..."
  }
}
```

### `POST /v1/runs/{run_id}/profile`

Upload a frozen profile conforming to `profile_schema_v1.json`.

The backend must verify the profile hash and reject mutable or incomplete records.

### `POST /v1/runs/{run_id}/candidates`

Upload a bounded candidate CSV or JSON array. Preserve supplied candidate IDs and tuples exactly. Resolve UTC independently and compare with any supplied UTC field.

Return errors for:

- impossible civil times;
- unresolved ambiguous folds;
- invalid IANA zones;
- mismatched supplied and independently resolved UTC;
- duplicate row IDs.

Do not discard duplicate chart states. Report both row rank and distinct-state rank.

### `POST /v1/runs/{run_id}/search/bounded`

Score all candidate rows on discovery evidence.

### `POST /v1/runs/{run_id}/search/global`

Search a declared UTC range using exact state segmentation.

Input includes:

```json
{
  "range_start_utc": "1926-08-21T00:00:00Z",
  "range_end_utc": "2026-08-21T00:00:00Z",
  "feature_layers": ["architecture", "gate_line"],
  "boundary_tolerance_seconds": 0.1
}
```

### `GET /v1/runs/{run_id}/opaque-results`

Return rankings without birth data or chart labels. This endpoint is used during blind discrimination.

Required fields:

```json
{
  "candidate_id": "C-...",
  "discovery_rank": 1,
  "core_fit": 100.0,
  "detailed_support": 71.2,
  "evidence_bits": 19.4,
  "contradiction_bits": 0.5,
  "net_bits": 18.9,
  "stable_interval_id": "SI-...",
  "boundary_status": "wider_stable_interval"
}
```

### `GET /v1/runs/{run_id}/differences`

Return predeclared behavioral distinctions among opaque finalists without date, time, gate, channel, profile, or chart labels.

Each difference should contain:

```json
{
  "difference_id": "DIFF-...",
  "eligible_question_ids": ["T01", "T02"],
  "candidate_partition": [["C-A", "C-C"], ["C-B"]],
  "mapping_directness": "direct",
  "dependency_cluster": "CL-...",
  "expected_answerability": 0.75,
  "body_access_sensitive": false
}
```

The GPT selects a neutral question. It must never receive a natural-language statement such as “answer A favors the 1985 chart.”

### `POST /v1/runs/{run_id}/answers`

Append a frozen answer batch with observation IDs, evidence, confidence, reliability, and hash. The backend creates a new profile version and reruns the full declared universe.

### `POST /v1/runs/{run_id}/freeze-finalists`

Freeze the discovery finalist set and stopping rule before holdout release.

### `POST /v1/runs/{run_id}/reveal-holdout`

Score held-out clusters only after finalist freeze.

### `POST /v1/runs/{run_id}/robustness`

Run confidence/reliability perturbation, cluster ablation, mapping variants, body-sensitive removal, and time sensitivity.

### `GET /v1/runs/{run_id}/final-report`

Return complete results. Birth tuples remain concealed until `reveal=true` is explicitly authorized after ranking is locked.

## Exact chart-state record

Each unique interval should store:

```json
{
  "state_id": "STATE-...",
  "start_utc": "...",
  "end_utc": "...",
  "representative_utc": "...",
  "complete_feature_hash": "...",
  "personality_activations": {},
  "design_utc": "...",
  "design_activations": {},
  "type": "...",
  "strategy": "...",
  "authority": "...",
  "profile": "...",
  "definition": "...",
  "defined_centers": [],
  "channels": [],
  "boundary_events": [],
  "cross_engine_status": "verified"
}
```

## Boundary algorithm acceptance tests

The backend must pass tests in which:

- a relevant transition occurs inside a minute;
- two interior transitions occur while coarse bracket endpoints match;
- a local time is nonexistent;
- a local time has two folds;
- a Design-side activation crosses a boundary while the Personality chart remains unchanged;
- a candidate minute straddles a boundary;
- two local tuples resolve to the same UTC and tie;
- adjacent intervals merge only when the complete frozen feature vector is identical.

## Information security and blinding

The backend must not receive the answer key in a blinded challenge. The user reveals the answer key only after the final report hash is committed.
