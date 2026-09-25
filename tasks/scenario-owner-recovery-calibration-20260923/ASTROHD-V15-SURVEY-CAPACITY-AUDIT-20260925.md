# V1.5 survey compression and recovery-capacity audit

Date: 2026-09-25. Scope: read-only code/bridge inspection plus algebraic enumeration. No participant data, astronomy, rule selection, deployment, or scoring semantics were changed.

## Owner question and corrected interpretation

The owner asks how a drastically shortened survey could still contain enough information to recover a birth date and time. The current implementation provides no evidence that the shortened instrument preserves the full survey's information or supports general date/time recovery. A runnable nine-prompt interface is not proof of measurement adequacy. A six-rule fit to one known target is not proof that five broad behavioral judgments are sufficient for a new person.

The original survey remains available. What narrowed was the active scoring representation: the new pilot maps nine prompts or an imported interview into only five categorical judgments. This is a limited six-hypothesis pilot, not an established replacement for the fuller measurement or a completed general birth-recovery system. Do not represent it as sufficient merely because input edits reach scores or because the original target attained a rare maximum.

## Source-bound mechanics

Inspected branch: `chat/v15-survey-decoder-20260925`.

- `reference/research/astrohd_v15_behavioral_bridge.json`, Git blob `f526c7e879fe597bd8d2cf91b2abd602be99d799`.
- `src/hdmatch/evaluation/astrohd_v15_decoder.py`, Git blob `8f5c8881500de86407b8da0d2d8c906f93c2874c`.

The scorer uses five domains: sharing understanding, seeking solitude/privacy, recurring romantic attraction or pair-bonding, trying to influence shared plans, and entering roles through recognition/invitation. Each has five nominal labels. Supported produces +1, contradicted produces -1, and mixed/unknown/not-applicable have the same zero scoring effect. One rule uses an OR of persuasion and romantic attachment; two additional rules use romantic attachment. Thus repeated clause votes are not independent behavioral measurements.

For a fixed birthplace, candidate universe and model, equal five-domain codes always produce identical scores/rankings even when the detailed answers or interview histories differ. Importing more answers does not expand the representation unless downstream scoring also retains additional meaningful distinctions.

## Algebraic enumeration performed in this turn

Enumerated all 3,125 nominal five-label profiles using a transcription of the retrieved `answer_signs` and `score_mask` logic and exact rule-domain lists. This is not a claim that the complete deployed application was executed or that live availability was checked.

Results:

- 5^5 = 3,125 nominal profiles.
- Collapsing three zero-effect labels gives a simple upper bound of 3^5 = 243 effective profile configurations.
- The actual repeated-domain/OR mapping yields exactly 162 distinct six-rule coefficient vectors, including the all-zero vector that the application rejects as insufficient evidence; 161 are non-abstaining.
- Across all 64 logical astronomical masks these produce 162 distinct score vectors and weak orderings. Some masks may not be physically attainable at a fixed birthplace, so this is an upper bound on actual ranking diversity, not a measured count of distinct geographic/astronomical rankings.
- Exactly five nominal profiles give all six votes +1: sharing, solitude, romance and recognition supported, with any of the five persuasion states. Under the current OR, supported romance makes the persuasion judgment irrelevant to the final coefficients.
- The six Boolean chart conditions produce at most 2^6 = 64 chart descriptions. All dates with an identical description tie under every profile in this fixed model.

These are algebraic capacity results, not measured entropy, mutual information, population prevalence, accuracy, or p-values. Holding birthplace fixed is essential; location is an additional input. The absence of demonstrated predictive information in a longer survey is not repaired by merely retaining more questions either.

## Why the rare original fit does not contradict this ceiling

A small collection of binary tests can have one extremely rare joint outcome. One of 64 cells can contain nine minutes while the other cells collectively contain nearly all remaining minute candidates. Therefore it would be incorrect to claim that six Boolean conditions cannot isolate any particular known case.

The prior century result establishes a rare all-six-positive astronomical pattern for the selected owner case at the fixed birthplace. The identities of those six rules were selected using the known birth target from a much larger library. The rule-selection step therefore used information beyond the five new-person answers. Other people with the same five codes and birthplace inherit the same score function and rankings; their true births do not become the new maximum automatically.

Under the hypothetical task of identifying an arbitrary uniformly distributed minute among 52,596,001 possibilities, the starting uncertainty is log2(52,596,001) = 25.64845 bits. The profile channel has at most log2(243) = 7.92481 bits, reduced by the actual score mapping to at most log2(162) = 7.33985 bits; these maxima are not measured birth-related information. This is a statement about general average identification, not a prohibition on a rare individual result. It also does not mean precisely 26 literal survey questions are required: questions may have many outcomes, correlated/redundant answers convey less information, and prior date knowledge changes the task.

## Causal correction and next authorized direction

Observed chain: a source-grounded sparse rule subset fitted to the known case -> only those rules' topics retained in the pilot -> five broad signed interpretations -> a technically functioning answer-to-score interface presented too close to completion of general decoding. The missing proof was that the shortened representation retained decision-relevant information and could distinguish diverse unknown cases. Software tests of update propagation do not establish that property.

Preserve the six-rule model, historical fit, and working pilot as explicit development/control artifacts. Do not erase the full survey or treat its unused responses as redundant. Do not require separate whole-tradition success or prohibit declared target-aware development. Do not send a new participant through a full interview and claim to use the full evidence if the scorer still discards everything beyond these five labels.

For the general recovery goal, return to fuller neutral behavioral evidence, preserve distinctions that could change different chart comparisons, and assess collisions/remaining date-time uncertainty directly. A small rule set can remain a useful selected component or baseline; six globally fixed Boolean clauses are not established as a sufficient universal decoder. Any proposed compression must earn its status by preserving the relevant recovery performance, not inherit it from a known-target fit.

The current small pilot can still test a narrow association on a new person. This audit does not prohibit that reversible experiment, disable the deployed site, alter answers, add arbitrary weights, or claim astrology is disproved. It corrects the scope and the expectation of general date/time recovery.

## Activation and delivery boundary

Live default-branch Universal AGENTS and the current operational owner-method preservation rule were retrieved for this turn. The actual diagnostic retains the owner's survey-to-birth recovery goal and separates supporting pilot completion from that broader open outcome. No new methods or mandatory independent-tradition gates were introduced. The answer should state the measured representation limit and the known-target selection distinction rather than merely repeat 'not yet validated'.
