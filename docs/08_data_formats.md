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

`human-dataset-v2` embeds these typed records and a verified birth record for each private
participant. The retained `responses`, `response_reliability`, date, and precision fields are
exact compatibility projections only; the importer does not invent clusters, confidence, or
provenance for a legacy `human-dataset-v1` record. Imported cohort partitions also retain the
full-dataset hash and exact person-split-manifest hash; preparation requires that split hash to
match the frozen protocol.

## Verified birth record

```json
{
  "schema_version": "verified-birth-record-v1",
  "local_datetime": "1985-01-29T07:26:00",
  "birthplace": "Istanbul, Türkiye",
  "iana_timezone": "Europe/Istanbul",
  "resolved_utc": "1985-01-29T05:26:00Z",
  "timezone_fold": null,
  "precision_minutes": 5,
  "provenance": {
    "source_kind": "caller-declared documented source",
    "verification_method": "caller-declared verification procedure",
    "notes": null
  }
}
```

`local_datetime` is a naive civil tuple; `resolved_utc` must exactly match historical IANA
resolution. Ambiguous civil times require `timezone_fold`. `precision_minutes` is a symmetric
uncertainty radius, so blind preparation emits a truth label only when the whole interval fits
exactly one caller-supplied candidate.

## Human blind preparation

`human-candidate-universe-v1` contains one public candidate set per frozen-protocol participant.
Every candidate used for truth resolution declares a half-open UTC interval and chart features;
truth flags and answer-key fields are forbidden. The owner-side command is:

```text
hdmatch human-prepare-blind \
  --partition /external/private/validation.partition.json \
  --candidate-universe candidate-universe.json \
  --protocol human-evaluation.protocol.json \
  --output-dir blind-run \
  --answer-key-out /external/owner-secrets/validation.answer-key.json
```

The response-only `human-blind-cohort-v2` is bound to the protocol and exact candidate-universe
hash. The plaintext `human-cohort-answer-key-v1` is bound to that blind-input hash and must stay
outside both the repository and decoder directory; it is not hashed into the public preparation
receipt.

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
