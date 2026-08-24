# Paired Model A/V2 pre-recovery checkpoint

Status: implementation and local verification complete; no paired synthetic cases
have been generated and no answer key has been revealed.

The frozen `MODEL-B-DETAILED-V2-NEW` preregistration, compiled artifact, model
freeze, and canonical January 2000/UTC behavioral-difference PASS audit are
unchanged. The audit remains answer-key free and records 22 genuine non-unknown
response-difference groups and zero adverse tie-split groups.

The paired experiment implementation now enforces this sequence:

```text
paired public plan and common seed commitment
→ separate sealed generation for Model A and Model B V2
→ claim-grade keyless recovery for both arms
→ individual prediction freezes
→ one two-arm prediction-freeze receipt
→ authenticated reveal/evaluation for each arm
→ public paired comparison
```

The two-arm freeze and comparator bind the exact public config, PASS audit,
compiled/frozen V2 identities, Model A identity, seed commitment, target set,
question bank, one audited month cache, ephemeris, clean source tree and commit,
software environment, recovery settings, prediction bytes, isolation receipts,
and timestamp order. The comparison recomputes metrics from frozen predictions
and reveal-authenticated public local dates rather than trusting mutable summary
statistics. It has no key or decrypt input.

No result in this checkpoint is a Human Design validation claim. A claim-grade
paired run still requires two actual successful Bubblewrap recoveries and retained
isolation receipts under the external process contract.
