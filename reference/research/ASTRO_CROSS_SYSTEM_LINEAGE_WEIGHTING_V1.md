# Cross-system convergent prediction audit V1: count *distinct lineages*, not books

**Status:** EXPERIMENTAL DIAGNOSTIC; **not a calibrated person-probability model**. Generic implementation: `scripts/audit_astrology_cross_system_consensus_v1.py`; synthetic tests: `tests/test_astrology_cross_system_consensus_v1.py`. No participant outcomes required or read. This is an additional development arm, not a replacement of any prior frozen project model or a validation result.

## Question and current project baseline

User suggestion: agreement between multiple astrological systems should support a stronger prediction. Current project `score_snapshot` in `astrohd_v13_traditions.py` ALREADY computes three **different** arms: (1) one domain vote after collapsing all rule testimonies; (2) sum of each source tradition's signed vote; (3) raw individual testimony sum. They are NOT calibrated probabilities. The existing protocol V2 also instructs collapsing repeated astronomy and preserving contradictions. Human Design V4.3's 15% corroborator cap is its own symbolic ranking rule, **not** a validated cross-astrology weight.

## Necessary distinction

A source tradition is not automatically an independent prediction generator. Two treatises may copy the same verse. Multiple historical traditions may use the same Mercury position and same idea about Mercury's intellect. BaZi and Zi Wei use different primary calendar mechanics but share birth date, time and calendar ancestry; they are not automatically statistically independent either. More agreement warrants attention as a candidate only when the systems imply the **same exclusive measured outcome** in the **same context**; otherwise it is verbal resemblance, not confirmatory evidence.

## Mechanical V1 source-lineage audit

The input JSON has `schema: astro-cross-system-consensus-input-v1`, a `study_id`, and a nonempty `claims` array. Each claim has `claim_id`, exhaustive mutually exclusive `outcomes`, and `testimonies`. Every testimony specifies:

- `testimony_id` (unique within claim), `system_id`, `source_locator`;
- `preferred_outcome` in the exclusive outcome set (or `null` when the source abstains);
- `signal_keys`: normalized underlying astronomical or calendar root(s) supporting it;
- `source_lineage_keys`: normalized textual/doctrinal origin root(s), including borrowing/republication.

Rules: one direction per system; if a system itself offers opposed outputs, it abstains. Collapse system outputs into connected dependency groups whenever they share any signal or source lineage. If a dependent group conflicts internally, flag it and prohibit an affirmative consensus winner. The result records raw testimonies, number of source systems, lineage-distinct groups, explicit oppositions, and one symbolic consensus option if unopposed/unique. A larger group count makes the statement **more worth pretesting**, not empirically likelier yet; `empirical_probability_or_validated_weight` remains null.

**Conservative boundary:** An actual pair of traditions may be correlated in ways not represented by supplied roots. The audit does not prove statistical independence or source correctness; the contract's lineage ids require human/original-source verification. Do not manipulate dependency keys to manufacture more apparent confirmations. Capturing all copied source relationships may decrease a previous convergence count.

## A higher-weight model may be promoted only if it adds held-out information

Experimental arms to freeze **before** new people's answers:

- **C0:** baseline frequency/control covariates without any astrology;
- **C1:** one domain vote collapsed across all astrology source traditions;
- **C2:** per-system signed votes with raw additive stacking (current exploratory arm);
- **C3:** V1 lineage-distinct groups, with contradiction/null handling;
- **C4:** learned, calibrated regularized stacking of genuinely out-of-sample system predictions, using person-split development and cross-fitting, and testing C4 against C0/C1/C2/C3 on an untouched cohort.

For calibration, use held-out probabilities per system only if already calibrated externally, or fit coefficients to training people by cross-validation with explicit regularization. Example (binary event, *not* preset values):

`logit P(Y|inputs) = logit P_base(Y|nuisances) + beta_W*x_W + beta_J*x_J + beta_B*x_B + beta_Z*x_Z + interaction_terms`

The beta coefficients and permitted interactions must be learned from independent development cases **without using the final test people**, not assigned because the astrologer finds the symbolism convincing. Shared data, source ancestry and correlated predictions require effective weighting/shrinkage; absence of empirical skill leads to zero/negative incremental value even if 10 traditions agree. The no-astrology model must be strong and use comparable season/birthplace/age controls to avoid attributing cultural or seasonal correlations to astrology.

Primary outcome: out-of-person multiclass log loss/Brier skill over no-chart baselines, with true versus nuisance-matched decoy charts, chart-label permutation and confidence intervals. Secondary: directional coverage, false positives, null/contradictory support, and interpretive dependence. Selection of the best weighting strategy is a training/validation decision; one untouched final test is used once without reranking to the best-looking arm.

**Do not call the V1 audit a 'newly weighted predictive model'.** It makes the user's independent-convergence hypothesis operational and tests the no-double-counting logic but it cannot decide actual cross-system coefficients. The applied production scorer remains unchanged until real held-out evidence justifies promotion.