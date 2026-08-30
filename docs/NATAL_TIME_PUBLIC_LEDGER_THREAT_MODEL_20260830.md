# Natal-time cohort-aggregate public-ledger threat model — 2026-08-30

## Status and scope

This is a design review for a possible future public-safe outcome ledger. It does not deploy, publish, or authorize a ledger. The default and only schema considered here is cohort-aggregate. The companion machine-readable artifact, `state/NATAL-TIME-PUBLIC-LEDGER-SYNTHETIC-SCHEMA.json`, is conspicuously synthetic, requires `release_authorized: false`, and is not a release policy.

The release-disabled aggregate schema is only a threat-model artifact. Its existence, structural validation, and synthetic example are **not evidence of anonymity, de-identification, acceptable disclosure risk, or release safety** for any real cohort.

Participant-level natal rows, chart intervals, exact birth dates or times, places, timezones, source documents, relationship identifiers, free text, and deterministic personal-data hashes are prohibited from the public surface. They remain private even if names are removed.

No small-cell suppression threshold, privacy budget, release cadence, subgroup policy, withdrawal policy, or correction policy is selected in this slice.

## Protected information and adversaries

The protected facts include participation itself; birth facts; the existence, precision, and source of a documentary record; candidate-set rarity; chart-state sequences; answers and narratives; relationship or household links; and outcomes attributable to a person or connected component. Plausible adversaries include acquaintances with approximate birth knowledge, community members familiar with a rare story, data brokers, someone holding a source record, and observers able to compare several ledger versions or combine the ledger with other public releases.

An aggregate is unsafe when an adversary can isolate, link, infer membership, or estimate a protected contribution with materially greater confidence. Removing direct identifiers is therefore insufficient.

## Threats and required pre-release controls

| Threat | Failure mode | Required control or review before any release | Status |
| --- | --- | --- | --- |
| Exact birth linkage | Date, time, place, timezone history, or record precision links a row to a known person. | Prohibit participant rows and all birth-location/time fields from the public schema; review all derived dimensions for equivalence to those facts. | Structural prohibition present; live review not performed. |
| Sparse state fingerprints | A rare candidate-set size, interval sequence, state combination, or width pattern identifies someone even without birth facts. | Publish no chart interval or participant distribution; test whether proposed cohort summaries or subgroup combinations isolate rare contributors. | Participant detail prohibited; aggregation test unresolved. |
| Membership inference | A before/after count or recognizable cohort description reveals whether someone participated or had an eligible reference record. | Use coarse cohort descriptions, assess auxiliary knowledge, release cadence, cohort overlap, and minimum safe aggregation before release. | Threshold and cadence unresolved. |
| Rare candidate sets | A unique multi-date or timezone-history case makes aggregate changes attributable. | Do not publish candidate-set strata or rare-case narratives; test uniqueness and leave unsafe dimensions private. | Strata absent from candidate schema. |
| Repeated-release differencing | Subtracting versions, subgroup totals, corrections, or withdrawals reconstructs one contribution. | Review the complete release sequence, not each file alone; constrain cadence and overlapping cuts; treat corrections and deletions as disclosure events. | Policy unresolved. |
| Relationship-network linkage | Partner, household, or shared-record-source aggregates reveal identities through a social graph. | Do not publish relationship identifiers, pair rows, network components, or pair-level outcomes; assess connected components before aggregation. | Structurally prohibited. |
| Deterministic personal-data hashes | Hashes of low-entropy birth facts or identifiers can be enumerated and linked. | Never publish participant, birth-input, chart-feature, record, relationship, or response hashes. Only hashes of public nonpersonal protocol/software artifacts may appear. | Structural prohibition present. |
| Small cells | Low counts, narrow denominators, or complementary totals isolate participants. | Select and validate a suppression/combination mechanism against actual proposed tables and auxiliary data. Suppress complementary disclosures as well as direct cells. | No threshold selected. |
| Free text | Narratives contain names, places, dates, relationship facts, or distinctive phrases. | No public free text, excerpts, generated summaries of participant text, or row-level error notes. Every permitted string-valued candidate field must be a constant, controlled-code enumeration, or tightly structured nonpersonal version/commit identifier. | Structural prohibition and controlled-value schema present. |
| Withdrawal and deletion | Removing a participant from a later version exposes membership and their approximate contribution. | Define private deletion obligations separately from public correction behavior; threat-model tombstones, replacement releases, and frozen historic copies. | Policy unresolved. |
| Versioned corrections | A corrected count or outcome creates a public link between versions or makes one contribution solvable. | Version nonpersonal protocol provenance while preventing public personal linkage; evaluate differencing across every retained release. | Policy unresolved. |

## Candidate cohort-aggregate surface

The synthetic schema permits only overall eligible/included counts; an explicit non-abstaining/evaluable denominator; aggregate intersection and abstention counts; separate date-coverage eligible/evaluable/intersection counts; separate cohort summaries of temporal-width and full-state-count retained ratios; tightly patterned nonpersonal protocol/method/software provenance; and a disclosure-review block whose unresolved-control values come from a closed enumeration. It does not permit arbitrary properties or arbitrary public strings.

Structural JSON Schema validation is necessary but not sufficient because ordinary JSON Schema cannot express every arithmetic relationship among aggregate fields. Any candidate record must also pass the fail-closed `validate_public_aggregate_semantics` check. The check requires included count not to exceed eligible count; included count to equal abstentions plus the non-abstaining/evaluable denominator; intersection counts not to exceed their applicable evaluable denominators; date-coverage denominators to remain nested within included/non-abstaining counts; both retained-ratio summary counts to equal the non-abstaining/evaluable count; and summary values to be null exactly when that denominator is zero. The synthetic example passes these invariants with 180 included records, 45 abstentions, and 135 non-abstaining/evaluable outputs.

Those fields are a candidate vocabulary, not a determination that the fields are safe in a real cohort. Counts and precise ratio summaries can still leak information through small cells or repeated releases. A real proposed record must undergo a release-specific review using its cohort size, overlap, auxiliary-data environment, prior releases, correction history, and planned cadence. Subgroup/source-quality aggregates are intentionally absent until their utility and disclosure risk are reviewed.

## Release workflow boundary

Before any future publication, a separate approved process must:

1. freeze the public purpose and exact proposed fields;
2. construct the connected-component and shared-source disclosure view privately;
3. test exact linkage, uniqueness, membership, complementary cells, and differencing over all planned and historic releases;
4. select—not merely inherit—a suppression or other disclosure-control mechanism and justify its parameters;
5. decide whether a formal privacy budget is applicable and, if so, govern composition across versions;
6. define withdrawal, deletion, correction, retention, and incident-response behavior;
7. document human disclosure review and owner authorization; and
8. create a new release artifact rather than changing the synthetic example into a live record.

Until those choices are made, `release_authorized` remains false. There is no claim that aggregate-only data is automatically anonymous, that hashing de-identifies personal data, or that a particular privacy mechanism will preserve useful evidence at a small cohort size.
