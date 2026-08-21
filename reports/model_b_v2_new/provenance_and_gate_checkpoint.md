# MODEL-B-DETAILED-V2-NEW provenance and gate checkpoint

This checkpoint precedes any provenance-hardened V2 behavioral-difference result
or synthetic generation. It records implementation state, not model performance.

## Scientific identity

`MODEL-B-DETAILED-V2-NEW` is a new prospective symbolic hypothesis. It does not
reproduce the lost historical detailed scorer. The V2 provenance amendment does
not change the preregistered observations, pathways, question tokens, constants,
or discovery/holdout assignments from prospective V1.

The initial compiled/freeze V1 files committed at `250d64f` predate the owner's
retrieval-level provenance-hardening requirement. They are preserved for history
but are superseded and may not authorize a V2 generation or recovery run.

## Provenance artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| retrieval manifest V1 | `8ed6a6358ce8502946a604430f0d0a902980730ae9796c16fa05097c4ee0a808` |
| external source catalog V2 | `b79d5cc939fbd35d2de7d6f1ad932ea8f4b625a22c9781b2975e043c52fcd765` |
| prospective preregistration V2 | `a956620ad9094bfbc2e481c76ee62eb1b6087c69339d9e4c4d2035af6b2afe25` |

Eight Jovian URL records bind the exact captured HTTP response body by SHA-256
and byte count. Four Human.Design records preserve exact URL/timestamp/locator
but explicitly omit a snapshot/content hash under the recorded license/technical
constraint. No external page body is committed.

## Mandatory behavioral-difference gate

The enforced sequence is:

```text
preregistration
→ deterministic compile
→ clean committed-source model freeze
→ answer-key-free behavioral-difference audit
→ PASS
→ synthetic generation/recovery
```

The audit and verifier bind and recompute:

- exact Model A semantic and mapping hashes;
- exact V2 compiled bytes, freeze receipt bytes, semantic model hash, and question bank;
- exact chart-engine fingerprint and month request;
- exact retained candidate-cache bytes and the canonical full-state universe hash;
- response-difference groups, favorable/adverse tie splits, and witnesses;
- `freeze <= audit <= generation/recovery` ordering.

A pass requires at least one genuine non-unknown detailed response difference,
at least one source-favoring Model A tie split, zero adverse tie-split groups, and
no failure reason. Failed audits are preserved but cannot authorize generation
or recovery.

## Benchmark boundary

No V2 benchmark has run at this checkpoint. If the January 2000/UTC public-cache
audit passes, only a small paired oracle comparison is authorized. Model A and V2
must use the same owner-only generation seed and otherwise identical config. The
revealed target-set identity must match before paired metrics are computed. The
result is engineering discovery-only, not holdout or human validation.
