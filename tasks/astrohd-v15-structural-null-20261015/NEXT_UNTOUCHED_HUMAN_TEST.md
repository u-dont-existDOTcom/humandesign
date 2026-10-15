# Ready next experiment: untouched AstroHD V1.5 participant

**Goal:** Determine whether neutral behavioral responses distinguish a birth chart that was **not** used to select the six astrological clauses. This is the owner's open human-recovery goal, not a new mandatory theory requirement.

## Ready receiving interface

The existing V1.5 participant-facing page is [Life Patterns birth-date research test](https://life-patterns-owner-production.up.railway.app/birth-test). On October 15 a fresh read-only GET returned HTTP 200 with the expected Life Patterns birth-test title; its contract returned nine source-faithful V7 questions, five neutral behavioral domains and the original frozen bridge SHA-256 (matching the repository). This is a read-only verification, not an assertion that a new participant has successfully completed a live submission today.

**No new questionnaire construction is required.** The respondent may answer only the already-supported short scenarios or import a prior interview, and then manually review the five neutral descriptions. Optional AI auto-interpretation previously had exhausted credits; direct manual self-review is the planned no-payment path.

## Minimal participant procedure

1. A consenting person who was **not used** in the six-rule development provides their own independently documented birth time, birthplace and any uncertainty. Prefer low prior knowledge of astrology/Human Design; record prior familiarity.
2. **Before revealing actual birth-time/chart identity to the evaluator**, collect their ordinary behavioral responses and review the five neutral codes. Mixed, unknown, skipped and contradictory cases are admissible without further forced questions.
3. Freeze/hash the first participant-reviewed profile and the fixed V1.5 model, bridge, scorer, candidate panels and seed. Use the existing V1.5 browser's built-in snapshot/reveal order. If the freeze cannot be independently reconstructed, report a **provenance limitation**, not a validation success.
4. Evaluate actual chart against the frozen primary 999-decoy panel and separately 9,999-decoy panel. Report exact `rank_best`, `rank_worst`, number of ties, highest other score and percentiles. **Flag structurally guaranteed first place** when the target has all six clauses and the sign vector is nonnegative. Do not treat that flag as predictive evidence.
5. Include the all-positive chart-only baseline and changed/contradictory-profile sensitivity. Do not fit new rules or recode any participant after seeing birth rank. Keep the first unedited outcome even if it fails.
6. With a consenting group, compute a person-by-chart N×N identification matrix using the new `cohort_rank_audit.py` and an exact participant-to-chart permutation null (N≤8) or transparently seeded simulation. Keep all participant rows and nonresponse.
7. Keep personal birth information, response exports, original evidence and pseudonymous cohort mappings **outside Git**; public research artifacts may contain only de-identified aggregate counts, frozen hashes safe for publication, and transparent limitations.

## Machine-facing handoff

The `cohort_rank_audit.py` tool accepts **only a privately stored, consenting, pseudonymous list of already verified six-bit chart masks and frozen five-domain response profiles**, not raw DOBs. It does not calculate chart masks, attest to birth certificates, or prove that the response freeze preceded chart reveal. Those provenance controls remain in the existing live study workflow. It rejects absent consent, leaked chart labels, invalid masks, repeated IDs and all-unknown profile claims. A synthetic three-person fixture demonstrated the exact group permutation calculation (p=1/6 for perfect synthetic identity, p=1 for the all-positive chart-only baseline). This is an **engineering check**, not a human validation result.

**Currently missing:** a consenting independent respondent's first frozen profile paired with an independently sourced birth time. No prior owner-provided data can serve as the first untouched case. No unsolicited invitation was sent, no new provider costs incurred, and no extra owner questionnaire requested.
