# C34 — End-to-end synthetic pre-answer freeze, mock reveal and controlled score

**25 October 2026. PARENT HUMAN OUTCOME: OPEN.** The user’s objective remains a comparison of source-defined astrological systems against genuinely untouched, consenting people with concealed predictions, verified chart inputs, independent nonastrological controls, and explicit failures. This is a **research-only synthetic rehearsal** of one deliberately *partial* Hellenistic rule, not an astrological result or a live study. **No real respondent data collected; no new production scoring code; no root active-task lock changed.**

## 1. What the prior historical checkpoint actually provided

C33 recovered the following very narrow disjunct from **Ptolemy, `Tetrabiblos` IV.5**, original Greek read against the modern Perseus/Robbins texts and a hash-pinned Greek transcription: in the ancient **male-nativity** branch, Moon in one of Ptolemy’s four *bicorporeal signs* (**Gemini, Virgo, Sagittarius, Pisces**) is *one* condition associated with **multiple marriages**. The analogous historical female-nativity branch uses the Sun and is a different hypothesis. Other original alternatives include **multiform signs** and applications to several planets; those are not computed and may overlap with the sign-only clause. A non-bicorporeal sign is therefore **not** literally a source prediction of one marriage.

C33’s verified Swiss-ephemeris **2020 synthetic UTC-day** experiment had **366** discrete date windows: 55 positive-condition windows, 186 nonpositive windows, and 125 **unresolved** due to conservative input-time sign-boundary envelopes. This depends on an upstream *declared* Moon maximum speed of **16°/day**, not a fully independent historical-horizon proof. These are *artificial calendar-day exemplars, not 366 real birth records*, and the year 2020 is unsuitable for the actual marriage-by-age-50 outcome. We use it **only to test software phase transitions**.

C33 parent source snapshot SHA-256 is **`4e9f8a27fa1c284ab9b9b6a24cdc0834c5e3bacc757c8435c921fdc42c2c45d4`** (commit `ef8b143a`). It is consumed exactly, not silently re-rated after seeing outcomes.

## 2. The newly executed three-stage rehearsal, not just a proposed protocol

[Source-only synthetic runner](hellenistic_c34_synthetic_blind_freeze.py) implements three **distinct command-line phases**; each creates its output **exclusively** (existing file gives `FileExistsError`, never overwritten). All packets are canonical JSON with a SHA-256 content digest and the same frozen artificial cohort IDs, and changes invalidate readback.

| Stage, actually executed in order | Exact artifact | Committed-packet content digest |
|---|---|---|
| A. Birth-condition exposure / analysis policy **frozen without answers** | [Synthetic pre-answer freeze](HELLENISTIC_C34_SYNTHETIC_PREANSWER_FREEZE_V1.json) | `d6405eca803e5fdb6d990266e0290d1de9ba980cee996886654f9257c3c49216` |
| B. Independently seeded **mock responses** generated later | [Synthetic mock outcomes](HELLENISTIC_C34_SYNTHETIC_MOCK_OUTCOMES_V1.json) | `50c6e11d6548f997626ae4713fbf805fad62a4a8ed801eb0882264bdabee8ac1` |
| C. Readback-verified freeze and mock responses scored without model revision | [Synthetic month-stratified score](HELLENISTIC_C34_SYNTHETIC_STRATIFIED_SCORE_V1.json) | `5d161fd4f580f7f87ce01eedf3e9a0222af947828897b3945913953602b60e54` |

The artificial cohort includes a **pseudonymous `MOCK-C34-001` through `MOCK-C34-366`** identifier per day, declared synthetic date, fixed birth-month stratum, source-positive boolean or `null`, and permitted source-sign set. **No actual DOB, name, marital history, street, religion, sex/identity or contact field enters any packet.** The pre-answer packet binds the artificial cohort universe, C33 source digest and historical parent commit, narrowed source clause, source-uncertainty gates, no-opposite-claim constraint, modern endpoint draft, concealed question text, one-sided null, permutation count and seed.

The mock answer generator uses **only the fixed artificial ID, calendar month, and a separate deterministic mock seed**. It does **not use the bicorporeal status**; a mutation test inverts every source-positive label while preserving IDs and confirms that simulated answers remain **byte-identical**. The mock outcome is simply `two_plus` or `less_than_two` for a fictional respondent. It is neither a marriage record nor evidence of astrology. Outcomes are published here only because these are entirely artificial.

## 3. A fully specified descriptive association test — executed on mock data only

The freeze commits to a **one-sided, birth-month-stratified risk-difference estimator**, where an outcome is coded 1 for mock `two_plus` and 0 for `less_than_two`. Every birth month with both source-positive and source-comparator mock rows contributes its within-month exposed-minus-comparator risk difference, weighted by its fixed share of eligible scored rows. This controls the *synthetic month stratum* in the rehearsal rather than unconditionally assuming source-positive days are uniformly spread across months.

The conditional Monte Carlo null is **1999 permutations of outcome labels within each birth-month stratum**, seed **20261025**. The frozen rule is a one-sided greater-than comparison; `p=(1+number_null_stats>=observed)/(1999+1)`. This comparative enrichment test is a **modern analyst-inferred hypothesis**, *not* the literal negation of Ptolemy’s subclause; people outside the four signs remain a control group without being predicted to have exactly one marriage.

| Exact machine-readback from this fully artificial rehearsal | Result |
|---|---:|
| Artificial cohort | 366 |
| Source-positive condition (eligible) | 55 |
| Source-nonpositive comparison (eligible) | 186 |
| Source sign uncertain / excluded from primary score | 125 |
| Matched month strata | 12 |
| Fake outcome records missing/unknown | 0 |
| Month-stratified risk difference in **mock answers** | **−0.060107** |
| One-sided permutation `p` on **mock answers** | **0.862** |
| Empirical astrological performance or touched real persons | **none** |

The result *does not favor* the historical source clause on this simulated independent-null batch. It is a **quality check** that the scorer handles direction, full fixed enrollment, abstentions and explicit non-support, not an empirical null finding about astrology. In a real study, participants must be enrolled and their eligibility fixed *before* marriage answers, with birth-month **and** culture/era/region/observed age controls and a privacy-protecting adjudication scheme. This development script neither collects nor accepts actual participant records.

## 4. Actual executed integrity tests and limitations

[C34 focused regression suite](test_hellenistic_c34_synthetic_freeze.py) exercises **20** observable contracts:

- bitwise-equivalent replay of the original C33 synthetic source freeze, mock response generator and score;
- *even validly rehashed* post-outcome changes to source-positive sign labels or the frozen permutation seed are refused by an **independent re-derivation from the original C33 source digest**;
- accidental overwrite refusal for a sealed freeze;
- SHA failures for altered prediction and altered mock outcomes;
- invalid cross-cohort outcome binding (even when separately rehashed);
- missing/duplicate respondent IDs and illegal response labels;
- unknown/unspecified mock responses retained and excluded, not filled in as positives or negatives;
- invariance of answer generation under reversed chart labels, proving no seeded answer-key leakage from the predicted sign;
- all twelve predeclared month strata retain positive and control artificial labels;
- precise **55/186/125** source statuses, **241** scored records and **1999** predeclared permutations;
- preservation of the source one-way sign-clause and explicit **0** real human tests/production changes.

**Important limitation:** unlike a real externally preregistered trial, these three synthetic files are committed together during a development run. Local command order plus hashes is **not** a trusted timestamp, notarized consent, blinded external custodian, real immutable study record, or independent prospective human validation. The synthetic freeze pins C33 source bytes and their historical commit, but **not** a separately audited complete compiled scoring binary or future participant schema. No actual study should reuse this example’s publicly visible seed and model as its sole protection against outcome-guided retuning. For real participants, freeze versioned code hashes, ephemeris sources, exact birth-inputs and consented eligibility, audit trail, cohort and null, followed by a separately archived pre-answer timestamp outside the scorer’s editable environment.

## 5. Next owner-facing action

Source-specific Ptolemy IV.5 *sign-only* marriage-count methods now have a **read-only input model, conditional uncertainty path, source-level test, self-contained fake freeze, mock blind reveal, and explicitly non-positive mock score**. The real gap is not additional Greek manuscript collation or reproducing the fake 2020 null. It is **an approved, consented intake for participants sufficiently old to have observable outcome histories**, whose birth dates/timezones are reliable and who have not shared the answers with the score designer, plus a reasonable cohort size. Public U.S. Census number-of-marriages aggregates have no chart-linked birth times. The user’s separately active `participant-session-v1` work is a distinct trait interview and was not changed; actual recruitment, account-app contact or administering sensitive marriage-history questions were **not undertaken**.

**Status: research-only synthetic dry run complete; parent 16-tradition human predictive experiment OPEN; zero human validations.**

## Final C34 verification receipt and strict interpretation

After the original synthetic three-phase rehearsal, the verification code was **hardened without changing any of the three stored artificial freeze/outcome/score packets**: each accepted freeze must now not only have its own valid SHA but **equal an independent re-derivation from the exact C33 source byte digest and source-locked program**, so a copied freeze with changed source-positive classes or analysis-permutation seed cannot be accepted even if a developer recomputes its self-hash. The mock label generator is an isolated deterministic `synthetic_id + month + seed` function and stays invariant under deliberately inverted chart-source labels; two new tests verify this. This hardening does not establish unalterability against a malicious party who can edit the code and source simultaneously, nor substitute for external preregistration.

The research-only source admission and real-human consent boundaries are now recorded in [C34 readiness registry](HELLENISTIC_C34_REAL_STUDY_READINESS_GATES_V1.json); both live human admissions and production promotions are **0**. The complete `test_hellenistic_c34_*.py` focused suite passes **20/20**; with the inherited **347 C33** source/engineering cases, the full `test_hellenistic_*.py` suite passes **367/367**, exit zero, using the existing isolated optional ERFA and pinned IERS historical astronomical inputs. None are human outcome validations.

**Frozen artificial packet hashes remained identical after the integrity hardening**: `d6405eca...` (synthetic prediction), `50c6e11d...` (synthetic responses), `5d161fd4...` (synthetic score). A user-visible real prospective study must have its complete actual prediction/model/software hash and trusted outside timestamp frozen *before any real participant response*, and must remain separate from the root `participant-session-v1` worker.
