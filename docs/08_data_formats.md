# 08 — Data Formats

## Behavioral response record

```json
{
  "participant_id": "P-001",
  "questionnaire_version": "Q1",
  "responses": [
    {
      "question_id": "Q037",
      "cluster_id": "LEARNING_MOTIVE",
      "answer": "C",
      "behavioral_confidence": 0.75,
      "measurement_reliability": 1.0,
      "example_text": "...",
      "counterexample_text": "..."
    }
  ]
}
```

## Known-month blind case

```json
{
  "case_id": "CASE-001",
  "known_birth_year": 1985,
  "known_birth_month": 1,
  "birthplace": "Istanbul, Türkiye",
  "iana_timezone": "Europe/Istanbul",
  "responses": [...]
}
```

For true blind local-date recovery, timezone may be provided because the purpose is to recover day/time, not infer timezone from behavior.

## Candidate state

```json
{
  "state_id": "STATE-...",
  "start_utc": "...",
  "end_utc": "...",
  "local_date_overlap": {
    "date": "1985-01-29",
    "seconds": 26787
  },
  "chart_features_hash": "...",
  "chart_features": {
    "type": "...",
    "authority": "...",
    "profile": "...",
    "definition": "...",
    "defined_centers": [],
    "channels": [],
    "activations": {}
  }
}
```

## Ranked date result

```json
{
  "local_date": "1985-01-29",
  "date_score": 12.34,
  "date_rank": 1,
  "best_state": {
    "start_utc": "...",
    "end_utc": "...",
    "score": 14.22
  },
  "duration_weighted_support": 0.81
}
```

## Human model artifact

```json
{
  "model_id": "EMP-003",
  "training_dataset_hash": "...",
  "questionnaire_version": "...",
  "feature_schema_version": "...",
  "split_manifest_hash": "...",
  "hyperparameters": {},
  "calibration": {},
  "created_at_utc": "..."
}
```

## Run manifest

Every run gets an immutable manifest containing:
- inputs and hashes;
- code commit;
- environment;
- seed;
- model;
- candidate universe;
- reveal status;
- output hashes.
