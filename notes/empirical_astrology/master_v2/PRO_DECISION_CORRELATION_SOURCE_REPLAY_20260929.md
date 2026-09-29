# Pro adjudication of the Correlation source-replay follow-up

Date: 2026-09-29

Decision version: `empirical-astrology-source-replay-pro-gate-v1-20260929`

Prior paid-archive science decision: `ede8f5a102127d4dfe215868ab1fafe9fff4afe1`

New evidence reviewed: `5cc1e5a9028358868570bffc963b95db1833fe37`

## Decision and scope

**Reaffirm the existing scientific model and prospective protocol. CF-003, CF-004 and CF-005 remain excluded from the personality model. No astrology feature, mapping, weight or executable moderator is activated.** The source replay improves documentation of conditional arithmetic, identifies additional reporting discrepancies, and raises the verified lower bound on southern participant reuse. It does not reproduce the missing source-level measurements or execute the null needed to test biography specificity.

This is an append-only evidence adjudication. It updates the meanings of *reproduced*, *independent* and *source-blocked* in the preceding decision; it does not overwrite that decision, its cohort graph, the reproduction specification, the Work evidence, or the frozen scientific files. The machine-readable companion is `reference/empirical_astrology/literature_model_v1b_source_replay_gate_20260929.json`.

The retained scientific model is **`literature_model_v1.0.0-wave3b-reaffirmed-20260928`**. The retained prospective protocol is **`same-hospital-personality-protocol-v1b-20260928`**. Its sole primary remains the theory-neutral, conditional association between within-hospital/same-date birth-time separation and the specified IPIP-50 personality distance. Astrology feature, trait-mapping and executable moderator lists remain empty; astrology weights remain `{}`. The implementation-acceptance and prospective-launch holds are preserved, not independently readjudicated here. Other candidate-family dispositions are inherited without a new literature assessment. [P1–P2]

### Evidence boundary

This review read the handoff, all three candidate replay reports, both numerical JSON outputs, the overlap JSON and all three replay scripts: the complete ten-file source-replay commit. It also read the prior decision, machine-readable gate, partial cohort graph and unchanged reproduction specification. The scripts were inspected **without executing them**. Neither the literature review nor the mechanical arithmetic was rerun. Findings about source pages and roster matches below are accepted from the committed, source-located Work evidence; this review does not claim a fresh visual recertification of the originals. [R0–R4]

Unavailability refers to the inspected source package and documented archive/publisher routes, not a finding that the authors never retained the materials.

No owner-known outcomes or prospective outcomes were used. No new human cohort, source-dependent permutation, fitted coefficient, person-level effect estimate or cluster-adjusted confidence interval was produced. Inaccessibility of a required source input is **not** evidence that its underlying effect is zero.

## 1. CF-003: arithmetic reproduced, claimed effect not independently reproduced

**Disposition: unchanged exclusion; conditional arithmetic is more thoroughly documented, but the scientific activation gap is unchanged.**

The replay covers all nine N=61 replication cells and all three N=189 training cells. It starts from the printed successes and rounded chance proportions. Its numerical agreement is within the declared rounding tolerances, not exact recovery of the authors' unrounded null probabilities or original random stream. The previously adjudicated result—eight of nine published replication p-values survive Holm across the nine endpoints—remains conditional on those p-values. The rank-three/three-try result remains a reported failure at p=.182. The training calculations remain fitted/discovery results. Reproducing their calculations does not convert training into validation. [R1; P1 §4]

The replay also preserves the training prose/table conflict (expected 151.6 in prose versus 135.8 in the table) and the replication prose/table conflict (43.8 successes versus 33.3 expected in prose, versus 47 and 43.8 in the table). The table-based reconstruction is explicit; it is not a reconciliation of the absent original subject records. [R1]

The scientific issue remains the target's construction. The predictor is a function of a chart, `f(C)`, while the alleged biographical target is a function of that same chart and a biography, `g(C,B)`. The ten candidate targets are obtained by tripling each planet's interpretive presence in the person's chart and matching the resulting portraits to biography words. A calculation of agreement between `f(C)` and `g(C,B)` does not determine whether the genuine biography contributes person-specific information beyond the shared chart. Shuffling completed targets breaks that shared-chart structure. Reproducing the p-values produced using such an expectation cannot establish that the expectation tests the intended hypothesis. [P1 §§1,3; R1]

The correct fixed-model comparison retains each chart and its frozen predictor, reassigns appropriately comparable complete biographies, and recomputes the biography-dependent target scores and ranks. The complete inputs for this comparison remain missing. The public 250-name appendix supplies a first biographical dominant per person, not all target ranks, predictor rankings, ten portrait word-score vectors, denominators or nine individual success vectors. It cannot generate the required off-diagonal chart–biography comparisons. [R1; P2 §A]

Use the following current wording:

> **Published new-person N=61 test of an inherited pipeline; its aggregate arithmetic is reproducible conditional on printed inputs. Individual agreement counts and biography-specific significance have not been independently reconstructed from source inputs. No additional empirical replication was supplied by this arithmetic replay.**

The 61-versus-189 person-disjointness remains source-reported; a complete stable-ID/alias audit has not been established by the replay. Later reuse of six people in the inversion study does not itself prove that the original 61 overlapped the original 189. Common software and authors do not, by themselves, invalidate a properly frozen new-person test. Equally, new people do not remove the need for a null that preserves the target's shared-chart input. [R1, R4; P1]

## 2. CF-004: unchanged exclusion, stronger documentary grounds for it

**Disposition: excluded as before. The new findings strengthen the documented reproducibility and external-independence reasons for exclusion; they do not supply a quantified adverse effect estimate or prove the reported aggregate false.**

The 48/68 versus 26/73 contrast and the separate binomial calculations reproduce **from the asserted counts and assumed nulls**. This establishes what those counts imply under those calculations. It does not establish which of the 141 people actually received which score or whether a 50/50 baseline is appropriate. [R2]

Only three paired global scores are printed; the other 138 remain unavailable. All three displayed differences disagree with their component scores. The Allende pair implies the direction opposite to its accompanying prose. The replay additionally documents the Figure 6 orientation conflict across pp.49–51, the inverted word score for “authority” appearing as 7.9 in one table and 7.0 in another, and an inconsistent displayed ratio expression. The inconsistent ratio expression is a display-level problem: the replay reports that the unrounded count ratio agrees with the headline ratio. It does not independently challenge the asserted aggregate. The score and orientation problems concern the unreconstructed measurement chain; none is a newly estimated human effect. The three printed examples are not a random error-audit sample from which to estimate an error rate for the other 138. Neither a one-person correction nor a global column swap is justified. Both failed latitude-distance analyses remain part of the evidence. [R2]

### Updated participant-reuse statement

The source-replay overlap record now supports **at least six exact-name witnesses** among the 68 southern participants:

| Earlier group | Southern participants documented in the replay | Basis and limit |
|---|---|---|
| N=189 training pool | Raymond Barre, Che Guevara, Xaviera Hollander, Luc Jouret | Present in the published pooled N=250 roster and absent from the printed N=61 roster; training membership follows the sources' stated disjoint 189+61 composition. |
| N=61 replication pool | Salvador Allende, Claudio Arrau | Present in the published N=61 and southern N=68 rosters; these are the two witnesses already in the prior Pro graph. |
| Earlier Le Monde training subset | All 73 northern participants | Documentary whole-cohort reuse reported by the papers; the replay does not claim an independently completed stable-ID match for every northern person. |

Source locations and original-PDF hashes are preserved in R4. Six is a verified documentary **lower bound**, not a full all-alias intersection count. The other 62 southern participants must not be labeled proved-new or independently held out. Regenerating their biographical word lists changes the measurement, not their person identities. The 2024 pooled 250 remain the old 189+61, not a third cohort. [R1, R4]

This supersedes the prior graph's *current lower-bound summary* of two southern reused people and the wholly unresolved southern-versus-training edge. The earlier two-person finding remains correct historical evidence; the original graph is not edited. The CF-004 report's narrower two-person passage must now be read with R4 and this adjudication, rather than as the complete current overlap statement.

Cross-study reuse weakens a claim of an independent external replication of the earlier programme. It does **not** establish that the 141-person inversion sample contains internal duplicate rows, that the inversion settings were fitted to these six people, or that a particular fraction of its contrast is bias. The outcomes needed to assess their contribution are absent. No leave-six-out estimate, revised success count, numerical independence weight or effective sample size is imputed. The newly documented four training intersections and the earlier two replication intersections remain distinct provenance categories.

Use the following current wording:

> **A reported north–south contrast with conditionally reproducible aggregate arithmetic, unreproduced individual classifications, unresolved score/orientation discrepancies, and documented reuse of all 73 northern people plus at least six southern people from the earlier dominance programme. No independently reconstructed or independent-cohort inversion effect is established by this replay.**

The exclusion is therefore better supported as a present evidence-admission decision. This is not the same as stronger measured evidence that the true inversion association is absent. The valid assignment-respecting null and the separate identity/world-knowledge measurement controls remain unperformed. [P2 §B; R2, R4]

## 3. CF-005: conditional event-table checks do not repair person-level inference

**Disposition: unchanged. Retain as aggregate methodological evidence only; no personality-model, clinical, forensic or individual-risk use.**

The executable replay covers 16 full-cohort aspect/event rows, two pooled full-cohort calculations and six pooled temporal calculations. It retains the Mercury–Mars conjunction result in both sources, the serial-source Venus–Mars conjunction result under the authors' within-table threshold, and the French final-third pooled failure near p=.210. [R3]

One scope qualification is essential: the **individual Mercury-conjunction-by-period** p-values in the C.3/D.3 figures were carried forward as reported values, not recalculated from transcribed cell counts. Those cell counts were not included in the executable dataset. “All temporal arithmetic reproduced” must not be expanded to include those cells. This review neither reruns their extraction nor turns the replay's untranscribed data into an assertion that the original figures cannot be read. [R3]

Recomputing an event/opportunity test does not reconstruct each person's repeated events, establish matched human controls, verify the historical source roster or calibrate person-clustered uncertainty. Calendar-day controls remain calendar-day controls. The full cohort and temporal summaries reuse observations; arithmetic checks add no people. Positive and unsuccessful source comparisons remain visible, but no new scientific activation threshold is crossed. Unavailable cluster-aware inference is unestimated, not negative. [R3; P2 §C]

### Availability wording corrections within the replay

The new pooled N=250 appendix and the printed N=61 roster permit a documentary reconstruction of the N=189 name list by set difference, conditional on the authors' stated composition. The CF-004 report's reference to a missing list of the additional 116 training names is therefore superseded by the newer pooled-roster finding. Similarly, the northern N=73 **printed name roster is available** in Figure 1; what remains missing is a completed stable-ID/alias cross-study linkage and the full underlying source exports, not the printed names. These qualifications do not supply biography profiles, birth-record verification, target vectors or a corrected null. [R1, R2, R4]

## 4. Exact materials sufficient to reopen CF-003 or CF-004

The following operationalizes **P2 §§A–B without replacing or relaxing them**. There are three separate boundaries: obtaining sufficient materials to execute a source replay; obtaining interpretable results from a frozen, assignment-respecting reanalysis; and satisfying any later independent measurement/held-out validation requirement for activation. Possession of a complete package satisfies only the first boundary's input requirement. None of these packages is itself a positive scientific result.

### Common intake and freeze

Provide lawful, immutable originals or an independently reproducible equivalent, with stable IDs, filenames, versions and content hashes. Preserve the historical export separately from every corrected or reimplemented version. Record the original collection/processing/model-selection chronology; a hash made today cannot demonstrate that a choice was fixed before the earlier test outcomes. A correction must identify the original discrepancy, changed input/rule, explanation and effect on reproduced outputs. A modern website scrape, new Mastro default or newly generated GPT profile must not silently stand in for its historical counterpart.

Before running a **new** permutation or dependent source repair, freeze the received package, executable implementation, discrepancy-handling plan, endpoint family, admissible assignments and exchangeability covariates/strata, applicable person/family dependence, tie/missingness rules, sparse-stratum handling, seeds, draw count and failure reporting. These settings have **not** been selected or declared frozen by the present decision. If defensible assignments cannot be supported by the available metadata, additional complete score files alone do not solve the null's identification problem. Keep licensed biographies and personal source records on an authorized protected surface; public Git need contain only lawful manifests, derived results and provenance. [P2 §§A–B,D]

### CF-003 complete source package

| Required material | Minimum usable content and acceptance purpose |
|---|---|
| People, charts and cohort lineage | Stable IDs/aliases for all 189 training, 61 replication and recombined 250 records; exact dated birth-source inputs, uncertainty/quality, locations and civil-time resolution; selection/exclusion and full-hour-rounding decisions; membership and processing dates. Explain the endnote's 22 acquaintances and whether/how their questionnaire-derived words entered the claimed biography sample. Do not invent their relation to N=189. |
| Actual biography inputs and preprocessing | The dated source texts or lawful reproducible access to the exact versions, language/source metadata, raw extracted word lists, final cleaned word lists and frequencies, extractor and complete thesaurus/cleaning rules, manual interventions and ordering. These establish what was measured and which stages can legitimately be held fixed under reassignment. |
| Complete chart-conditioned target generator | The Mastro build or a disclosed and parity-tested reproducible equivalent; the full keyword/scoring corpus and settings; ten planet-tripled portraits for every person, each with its complete word-score vector and denominator. Supply the resulting ten own-biography scores, all ranks and tie handling. Ten **already matched scalar scores** alone are insufficient: the export must permit scoring every admissible wrong biography against the fixed chart portraits. |
| Fixed predictor and comparison exports | Exact seven factors/weights and all aspect, orb, house, rulership, angle, rounding and tie conventions; per-person factor values, full planetary predictor scores/ranks and all nine individual success vectors; original target/predictor ordering. Include a contemporaneous checkpoint and decision log showing what was fixed before processing N=61, including any later modifications. |
| Original null provenance and new-null metadata | Original ordered target/predictor arrays, complete 30,000-shuffle algorithm, seed/random generator/software, candidate/rank/tie geometry and unrounded chance rates; archived draw outputs where available, or inputs sufficient to regenerate them. Also provide era, source/language, profession/fame/profile-length and relevant dependence/selection metadata needed to justify new biography assignments. Replaying the original output-shuffle does not validate its substantive null. |

These materials are sufficient to attempt the first-stage reconstruction of the original 189/61 measurements and all nine replication endpoints without inferred or fitted repairs, and to prepare the next-stage null under a frozen justified assignment plan. For that next stage, hold each chart and fixed predictor constant, reuse unaffected chart portraits, reassign whole biographies and recompute every affected cleaning/coding/target-score/ranking stage. Preserve the joint endpoint and within-person structure and account for the nine-test family; do not shuffle only finished target labels. [P2 §A; R1]

To reopen the **separate adaptive training-search question**, additionally supply the full 42-factor inputs, 42→18 screening rules/results, Solver objective/configuration and all selection/tuning logs. That search is rerun inside a development-search null, not inside a genuinely frozen-model N=61 validation test merely because training occurred. Unknown pre-test freezing must be reported, not retrospectively granted. The new endnote/roster clarification does not justify changing the frozen model. [P1 §3; P2 §A; R1]

### CF-004 complete source package

| Required material | Minimum usable content and acceptance purpose |
|---|---|
| All 141 people and sampling provenance | Stable IDs/aliases, northern/southern membership, original birth-source inputs/quality, latitude, exclusions, selection chronology and exact intersections with the prior 189/61/250 and Le Monde groups. Include the demographic, era, language, fame/source and dependence metadata needed to distinguish the paper's differently ascertained groups. |
| Both chart versions for every person | Original and transformed longitudes and displayed labels, the exact 180° operation/settings, all aspect/midpoint/angle conventions, executable build/corpus and reproducible configuration. Verify which quantities are invariant and which interpretations change; do not silently repair Figure 6 by relabeling an entire unseen dataset. |
| The actual biographical profiles | Complete original French word lists, actual lengths, frequencies/duplicates and any normalization; exact prompts and identity inputs, model/version/date, available generation settings/seeds, all retries/discards/edits and their timing relative to scoring. Preserve actual variable lengths, including the reported 151-word example, rather than enforcing an invented exactly-150-clean-traits rule. |
| Full scoring inputs and outputs | Both complete chart keyword-score vectors and denominators per person; matched-word contributions, unrounded paired global scores, differences, binary decisions and zero/tie/missingness rules for **all 141**, not just the missing 138. Export enough to recompute scores for admissibly reassigned biographies. A final 141-row win/loss sheet or two already-matched scalar scores per person alone cannot execute that null. |
| Discrepancy and analysis provenance | Original export/table-generation record and versioned author or independent-reproducer explanations reconciling the three subtractions, Allende direction, orientation conflict, 7.9/7.0 word value and inconsistent ratio expression. Include the full latitude/score series, exact two latitude-test definitions and analysis/selection chronology so both reported failures and all original endpoints can be retained. |

After source reconstruction resolves the score/classification discrepancies, a separately frozen conditional analysis must recompute the same paired transformation and hemisphere statistic using comparable wrong biographies while preserving the documented ascertainment, vocabulary/profile structure and applicable dependence. A nominal 50/50 baseline or shuffling already-finished wins does not substitute for this test. Additional metadata or a narrower honest estimand is needed if exchangeability cannot be justified; this decision does not silently authorize that scientific redesign. [P2 §B; R2, R4]

The package must also make identity/world-knowledge exposure auditable. A successful profile-assignment null would not establish that named-person GPT output is independent of known birth facts or chart stereotypes. The prior requirement for a **separate masked-biography or independently measured-trait sensitivity/validation design remains**. Unaffected profiles genuinely frozen independently of the reassigned chart need not be stochastically regenerated for every permutation; stages influenced by assignment or adaptive selection do. Historical generation provenance and measurement-independence testing answer different questions. [P1 §3; P2 §B]

### Reopening is not activation

A successful reconstruction plus a suitable new null could change the assessment of the **source-specific** association. Its result is not predetermined. Such a reanalysis still uses the existing people; it supplies no new untouched replication. Before either candidate could enter a personality model, the previously required independent, name-/birth-fact-blind measurement, exact chart-to-trait mapping, outcome-blind protocol and genuinely untouched held-out replication would still be needed. No available replay result reaches those boundaries. For CF-005, improved aggregate methods would still not authorize high-stakes individual use. [P2 §§C–E]

## Authority, completion and source references

This decision authorizes no new purchase, author contact, participant recruitment, outcome collection, owner-specific fitting, production prediction or launch. Existing separately authorized mechanical work is not revoked or certified by it. The present work package closes at publication and verification of this append-only Pro adjudication. The next **scientific evidence boundary** is receipt of the unpublished source packages, not another journal download or another calculation on the same printed aggregates.

Cross-family interpretation review and its limitations are recorded in `CORRELATION_SOURCE_REPLAY_CROSS_FAMILY_20260929.md`. Artifact/protected-file verification is recorded in `CORRELATION_SOURCE_REPLAY_PRO_VALIDATION_20260929.json`. Neither constitutes independent participant evidence.

References below are repository-relative and bound to the stated commits; the machine-readable gate records their hashes.

- **P1** — prior science commit: `notes/empirical_astrology/master_v2/PRO_DECISION_POST_CORRELATION_20260929.md`; companion `reference/empirical_astrology/literature_model_v1b_post_correlation_gate.json`; `reference/empirical_astrology/correlation_cohort_graph_20260929.json`.
- **P2** — same prior science commit: `notes/empirical_astrology/master_v2/CORRELATION_REPRODUCTION_SPEC_20260929.md`, especially §§A–B and D–E.
- **R0** — replay commit: `notes/empirical_astrology/master_v2/PRO_HANDOFF_CORRELATION_SOURCE_REPLAY_20260929.md`.
- **R1** — replay commit: `notes/empirical_astrology/master_v2/CF003_SOURCE_REPLAY_20260929.md`; `reference/empirical_astrology/cf003_source_replay_20260929.json`; `scripts/empirical_astrology/reproduce_cf003_20260929.py`.
- **R2** — replay commit: `notes/empirical_astrology/master_v2/CF004_SOURCE_REPLAY_20260929.md`; `scripts/empirical_astrology/reproduce_cf004_20260929.py`. Its arithmetic output is reported in the Markdown file; no separate CF-004 result JSON is present in this commit.
- **R3** — replay commit: `notes/empirical_astrology/master_v2/CF005_SOURCE_TABLE_REPLAY_20260929.md`; `reference/empirical_astrology/cf005_source_replay_20260929.json`; `scripts/empirical_astrology/reproduce_cf005_tables_20260929.py`.
- **R4** — replay commit: `reference/empirical_astrology/correlation_overlap_source_replay_20260929.json`, supplemented by R1's roster/lineage discussion.
