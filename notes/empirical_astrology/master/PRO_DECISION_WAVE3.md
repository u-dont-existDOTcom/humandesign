# Wave 3 Pro decision — frozen development architecture

2026-09-28. Version `literature_model_v1.0.0-wave3-20260928`. Machine-readable decision: `reference/empirical_astrology/literature_model_v1_decision.json`. Starting evidence commit: `7e18f6b84fb923d7d99ba85a3f9ed23cfdc78013`.

## Decision

The only executable v1 birth-derived hypothesis is whether personality distance increases with elapsed birth-time distance among births recorded at the same hospital. It is theory-neutral. Include site/date/cohort, clock-time and recruitment controls; account for repeated people in matched pairs. This is a test specification, not a positive result. Prior time-twin analyses are negative development evidence, including the NCDS mean serial r=-.003 and the Roberts–Greengrass reanalysis r=-.001; neither validates the narrower design (`evidence_map.md`, Programme 5).

No candidate astrology feature earns an evidence-derived, equal-initialized or production coefficient. The v1 astrology coefficient vector is empty. Later coefficients must start at zero and be learned with shrinkage inside development data only. The Wave 4 worker may evaluate controls and theory-neutral time distance, but cannot invent an aspect mapping or interpret an unevaluated ablation as a negative result. If exact secondary mappings are later justified, they require a separately frozen version before any outcomes from that prospective cohort are opened.

| Candidate | Disposition | Adjudication |
| --- | --- | --- |
| CF-001, karaka kendra | Exploratory prominence study only | D1-or-D9 is one binary rule. D1 and D9 are ablations, not independent confirmations. The 60/84 result, permutation comparison and follower regressions use one selected N=84 cohort. Broader Vedic null is not an exact-rule replication. Exclude exact ties unless the original tie rule is recovered; no transport to personality. |
| CF-002, applying orb allowance | Exploratory only; no v1 term | The 1–2° statement is abstract-only, with unknown outcomes and multiplicity. Treat 1° and 2° as two corrected alternatives in future research, never a choice optimized on validation. Startup's null aspect study constrains broad personality claims but does not directly refute the asymmetry. |
| CF-003, adjusted dominance | Excluded | A claimed N=61 independent match cannot supply a model column without the actual scoring dictionary, cohort identities and semantic-label audit. Random-keyword simulation requires a complete-pipeline negative control. Discovery and replication cannot be equated from abstracts. |
| CF-004, hemisphere inversion | Excluded | The abstract's 180° sign transform is not a specification for houses, aspects, or trait coding. North/south, latitude, culture and celebrity selection are confounded. Lu's large ordinary Sun-sign null is contextual, not a direct inversion test. |
| CF-005, Mars and violence | Excluded | Abstract-only eight tests, uncertain cohort independence and control construction; adjacent criminality studies are not exact replications. No person-level violence scoring even if full text becomes available. |
| CF-006, Gauquelin sectors | Exploratory replication programme only | No sector geometry, planet/profession pair, eminence threshold or selection rule can be chosen from favorable historical subsets. Positive and negative reanalyses conflict. Gauquelin, CSICOP and CFEPP reuses count by distinct civil records; Ertel–Irving is not a new cohort. |
| CF-007, aspect tightness and angularity | Secondary template only; no executable v1 mapping | Startup's one N=911 cohort supplies four analyses, broad null overall (3/32 nominal, family p=.21). Heterogeneous medical, vocational and mundane outcomes do not establish personality mappings. No exact trait mapping in the packet clears the freeze gate. |
| CF-008, Vedic clinical judgments | Excluded | The apparent 77–82% case/control classification is vulnerable to reader-by-subset and recruitment confounding. Shared-chart current illness agreement κ=-.111 on ten charts and no deterministic rule bar algorithmic translation. No clinical person-level output. |

Generic Sun-sign traits/compatibility, human reader confidence, whole-chart similarity, hard/soft aspect weights, harmonics and high-stakes predictions are also excluded.

## Exact secondary interaction policy

Once an exact **body pair × aspect angle × measured trait** mapping is frozen in a new outcome-blind version, the only allowed secondary template terms are its indicator times (1) continuous distance to aspect exactness, (2) applying status, and (3) minimum angular distance to ASC, MC, DSC or IC. Their exact directions, frame, orb, uncertainty threshold and calculation version must be frozen with the mapping. There is no three-way term or general aspect effect in v1. These three terms form one corrected secondary family and cannot rescue failure of the primary time-distance test. A 1° versus 2° applying-orb comparison is only a separate exploratory family after full-text audit. No body pairs or trait directions are inferred from owner cases.

## Dependency, constraints and remaining evidence

Count unique nonoverlapping cohorts, not source documents, outcomes, regressions or pairs. Unknown cohort lineage supplies no additional independent corroboration. Use person- and site/date-aware inference and controls preserving hospital, calendar/cohort, local clock time, geography, birth-time quality and astronomical base rates. Keep rectified times outside confirmatory calculations and propagate uncertainty. Freeze/hide outcomes before selecting any map or weight.

The fifteen constraints in `negative_constraint_registry.jsonl` are binding: NC-001–005, 012 and 014 block specified features or uses; NC-006–011, 013 and 015 govern design, evidence counting and validation. In particular synthetic examples are engineering checks, and historical literature and owner-known cases remain development evidence. Evidence needed to reopen each candidate is recorded in the decision JSON; obtaining full texts alone does not turn a favorable retrospective result into held-out replication.

The packet has 49 extracted feature rows from 14 read originals and hundreds of missing originals. The Gauquelin and aspect ledgers contain mixed source tags and incomplete lineage. These limitations favor a small v1; they do not imply a general proof of absence. The next genuine test is a preregistered, untouched same-hospital cohort with a held-out replication cohort, conventional date/time/location baselines and complete reporting of failures.
