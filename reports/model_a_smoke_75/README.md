# Model A known-month blind smoke

This is the completed 75-case engineering smoke for `MODEL-A-CORE-V1`. It is not
evidence that Human Design predicts human behavior. The prediction file was hashed
and frozen before the encrypted synthetic answer key was revealed; the frozen
prediction SHA-256 remained
`a191159ae0c6a09b919349763f0514b2bdfbb5e0f67eefa4bcb4e9f315f42516`.

## Result

- Top-1: `0.4533333333333333`
- Top-3: `0.7466666666666667`
- Top-5: `0.8266666666666667`
- MRR: `0.6256797385620916`
- Mean midrank: `3.3466666666666667`
- Median midrank: `2.0`
- Tie rate: `0.0`
- Unevaluable cases: `0`

The active restoration curve improved from chance-like zero-cluster Top-1
`0.03289581015943641` / mean midrank `15.706666666666667` to the final Top-1
`0.4533333333333333` / mean midrank `3.3466666666666667` after seven independent
response clusters. The random restoration endpoint was identical. Leave-one-cluster-out
mean rank worsening was largest for `PROFILE_ARCHITECTURE` (`1.0733333333333333`),
followed by `AUTHORITY_DECISION` (`0.56`) and `CENTER_G_STATE`
(`0.49333333333333335`). All seven ablations and all sixteen restoration points are
preserved in the ignored run artifact whose hashes are recorded in `summary.json`.

## Every non-Top-1 case

No case was discarded. The post-reveal evaluator assigned the residual category
`scoring_bug` when it could establish no search failure, missing mapping, structural
tie, or aggregation explanation. That label means “scoring behavior still requires
investigation”; it is not proof of an implementation defect. The 41 cases and exact
true-date midranks were:

```text
CASE-0001 6   CASE-0005 2   CASE-0006 3   CASE-0007 2
CASE-0010 5   CASE-0012 2   CASE-0013 2   CASE-0014 17
CASE-0017 3   CASE-0020 2   CASE-0023 5   CASE-0024 7
CASE-0026 3   CASE-0028 2   CASE-0030 14  CASE-0032 4
CASE-0035 2   CASE-0037 8   CASE-0041 4   CASE-0042 2
CASE-0043 3   CASE-0044 2   CASE-0047 16  CASE-0049 2
CASE-0050 2   CASE-0052 3   CASE-0054 12  CASE-0055 7
CASE-0056 16  CASE-0058 6   CASE-0059 7   CASE-0061 2
CASE-0062 8   CASE-0063 2   CASE-0066 5   CASE-0068 2
CASE-0070 2   CASE-0071 2   CASE-0073 17  CASE-0074 4
CASE-0075 2
```

The dominant scientific explanation is coarse model discrimination: Model A contains
only architecture-level behavior mappings, so many dates receive similar aggregate
support. The source-bounded Model B audit confirms that richer mechanics can partition
the same candidate universe more finely, but the repository does not supply frozen
detailed behavior-to-structure mappings. Therefore the misses cannot honestly be
“fixed” by adding favorable gate/channel meanings after reveal.

## Provenance

The 12 exact cached month universes contain 13,777 stable intervals and share chart
engine fingerprint
`09e811ca0fe517975f9718ea7e12b72f66bf3d2509e049bc29f47169adef5397`.
Canonical artifact hashes, including blind input, encrypted-key receipt, leakage
audit, run manifest, freeze, reveal record, and evaluation, are in `summary.json`.
The encrypted key and answer key are not committed.
