# G38 — Source-bounded Gene Keys Line-preference pilot, synthetic freeze and natal-time eligibility

**25 October 2026. Parent owner outcome OPEN:** reproducibly reconstruct source-specific chart interpretations (Gene Keys, Human Design, Hellenistic and other traditions), then test genuinely **frozen, independently measured** predictions about untouched consenting humans with transparent negatives, decoys and strong nonastrology controls. No G38 participant enrolled, no official completed Gene Keys profile verified, no real outcome observed or natal production scorer changed.

## 1. The important new source qualification

G37 covered all 64 public short Gene Keys pages and identified Rudd's [six Line response styles](https://genekeys.com/how-to-read-your-profile/). Reading the companion [official source on changing Line keynotes by Sequence](https://genekeys.com/docs/why-do-i-have-different-line-keynotes-in-my-venus-or-pearl-sequence/) established an often-overlooked limitation: **a Line number can remain the same while its narrative keynote changes with the Sphere and sequence**. For example, Purpose Line 1 is described differently in Activation versus Venus. Thus the general "responds best to" page is a genuine author/publisher source, but it does **not prescribe a specific natal Sphere, communication scenario, response variable, success cutoff or statistical model**.

The deliberately narrow **G38 Life's Work / natal Sun Line** choice is therefore recorded as an **analyst-derived exploratory research hypothesis**, NOT a source-stated guaranteed behavior or complete Gene Keys scientific model. The official interpretations of Line 2 ("high frequency") and Line 4 ("romance") cannot be instantiated literally in a safe neutral unsolicited-message setting. G38 marks the warm and gently connected replacements as **researcher-created partial proxies**, not full fidelity to Rudd's terms. Because many people prefer practical information or patience regardless of chart Line, **simple above-one-sixth response matching is not an adequate confirmatory test**.

**Critical shared-input consequence:** The Gene Keys numerical Line for natal Sun is the *same source astronomical Line* as the existing Human Design Rave Mandala natal Sun. A preference association cannot provide incremental **natal feature information** beyond the full HD input. It could at most support a source-specific interpretive assertion when compared against **a separately frozen Human Design interpretation**, identical chart inputs, neutral-message popularity, birth-season, culture, and matched chart decoys. Re-labelling a true HD Line as a Gene Keys Line is not two independent corroborations.

## 2. Concrete source-constrained, falsifiable pilot proposal — NOT yet enrolled

The [original short phrases from G37](GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json) were paired with the new [G38 *researcher-authored* message bank](GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json):

| Original Gene Keys Line category | G38 **analyst-designed** neutral communication contrast |
|---|---|
| 1: Full information / heartfelt directness | Clear, detailed direct explanation |
| 2: High frequency / no agenda | Friendly invitation, with no hidden agenda; literal physical "frequency" not operationalized |
| 3: No pressure | Explicit respect for declining without coercion |
| 4: Honesty/softness/romance | Sincere, gentle nonromantic invitation; not literal romance |
| 5: Practical solutions | Concrete actionable information |
| 6: Patience | Unhurried explanation with time to consider |

Four **fictional, non-medical** situations are included: a mapmaking workshop, drawing session, gardening meeting and local history talk. Within each scenario, the six message versions contain the **exact same three factual sentences once each** (time/place, registration deadline, optional participation). The source-related pragmatic frames differ; word count, implied warmth, pressure, redundancy and style contrast have **not** yet been independently validated by human raters. A strict machine test proves fact inclusion, not equal pragmatics or social expectancy. No one was actually invited to a real event.

A future blinded, consented pilot could ask respondents to choose which of six otherwise fact-preserving messages they'd prefer to receive, four times across neutral scenarios with randomized style positions. The primary *modern analyst* rule would be **the subject's certified Life's Work/natal Sun Line predicts the corresponding chosen style more frequently than person-level-permuted Line assignments**. This does not claim that Rudd tested such a task; the real cutoff and stimuli must be accepted independently **before** respondents answer, with manipulation checks and a nonastrology/HD interpretation baseline.

## 3. Actually executed, source-locked 120-person synthetic pipeline

[Research-only G38 runner](genekeys_g38_synthetic_line_preference.py) implements three distinct, **exclusive-create** local phases, in this order:

- **A. Freeze (before simulated responses):** 120 obviously fictitious synthetic IDs balanced across the 6 fake Line values (20 per Line), 4 equal-size artificial strata, 4 scenarios per ID, all six available styles in deterministically pseudorandomized order; exact source registry and message-bank bytes, scenario/question, experiment's *analyst-supplied* sphere and model assumptions, 1,999 person-level permutations and seed, all in a canonical SHA256-checked freeze. Fake natal Line is assigned **synthetically round-robin**, not from real or pretend birth certificates.
- **B. Mock response:** 480 response positions generated separately from **only** each artificial ID + scenario with a different fixed seed, not source Line or chart. The mock generator deliberately makes generic practical/no-pressure styles more popular (so a uniform six-choice preference model would be misleading). Replies represent **fictional style choices, not human data**.
- **C. Score:** validate the freeze against **exact re-derivation from the original G37 six-Line source digest, the committed bank and the analyst study contract**, then validate response packet SHA and frozen-cohort binding. The predeclared test permutes *whole artificial-person natal Line labels* **within each synthetic stratum**, preserving all four correlated responses per participant and the population style distribution. The one-sided null has **1,999 exact predetermined Monte Carlo shuffles**.

The saved, accepted **synthetic-only** artifacts are:

| Object | Packet SHA256 |
|---|---|
| [Pre-answer freeze](GENEKEYS_G38_SYNTHETIC_PREANSWER_V1.json) | `8ad17bee6a67df5be0130ea06357ca9dfd4c84cbb97562b88b03de7e72de7ba2` |
| [Independent mock choices](GENEKEYS_G38_SYNTHETIC_MOCK_CHOICES_V1.json) | `42b483904cdfe2745eb3ddf769a32428d28903f2e3d09fef4e207b777032b071` |
| [Mock-only permutation score](GENEKEYS_G38_SYNTHETIC_SCORE_V1.json) | `2a2d4f816cfee75dbe1bee885378ef5b7d8dd70b29a131838768d62d853a7d7a` |

Artificial mock outcome: **76/480 = 15.83%** source-style choices versus an overall 16.67% style-popularity baseline in this balanced simulated cohort; one-sided person-level mock permutation **p=0.7115**. Style 5 was chosen in **26.875%** of simulated choices, showing a universal preference skew; the permutation preserves it. **These numbers are entirely simulated and neither support nor refute Gene Keys.** A local **prepublication development correction** renamed two confusingly negative-named protocol status fields and then corrected the Line-1/Line-5 length manipulation before accepting the final development checkpoint; earlier synthetic scratch files are retained only under `/tmp/g38-superseded-prepublication-synthetic/`, never committed. The final packets were regenerated in correct freeze→mock→score order after the correction.

The same synthetic tests reject model tampering, validly rehashed changes to an originally source-locked fake Line, wrong cohort/freeze digest, missing/duplicate/unknown subject responses, invalid choice positions, and accidental overwrite of saved packet paths. The source bank and study contract are **development files**, not an externally timestamped preregistration; these safeguards do not protect against a malicious operator changing both code and trusted source simultaneously.

## 4. A decision-relevant constraint from actual Swiss positions: Line requires birth-time precision

G38 independently used the incumbent **fail-closed Swiss Ephemeris** Sun and exact 64-Gene-Key/6-Line Mandala wheel to estimate the **conditional** Sun Line ambiguity across five possible birth-time widths, using all **366 synthetic UTC noon instants in leap-year 2020**. The Sun’s existing declared conservative upper speed bound is **1.1°/day**; each complete Gene Key occupies **5.625°**, but an individual **Line only 0.9375°**. The code propagates a **full closed angular range over the *entire* possible time interval**, analytically enumerating all gate/line boundaries, rather than treating selected sample times as proof. This tests *potential* input resolvability, not a person's actual recorded birth window. The 1.1° bound is **not independently certified for all centuries**.

| Hypothetical complete UTC birth-time window | Conditionally stable **Sun Gene Key** across 366 synthetic dates | Conditionally stable **Sun Line** across 366 |
|---|---:|---:|
| **1 hour** | 364 | **350** |
| **2 hours** | 362 | **329** |
| **6 hours** | 350 | **261** |
| **12 hours** | 329 | **153** |
| **24 hours** | 293 | **0** |

This distinction is decisive for study planning: under the chosen **full 24-hour conservative bound**, no 2020 synthetic date establishes a unique **Line**, although **293/366** still establish a unique **Key**. A future **Line-specific** study cannot use unspecified date-only natal input as though the Line were known. More precise independently sourced clock times—and birth timezone/DST conversion—may make the Line stable, without requiring prenatal 88°/88-day resolution because the Life's Work *natal Sun* branch is unrelated to the Design root.

The complete [strict-Swiss synthetic 366-date time window receipt](GENEKEYS_G38_SYNTHETIC_NATAL_SUN_LINE_UNCERTAINTY_V1.json), [analytic width engine](genekeys_g38_sun_line_uncertainty.py), and exact reproducibility tests are saved. These stability counts are **conditional conservatism**, not a claim about actual Sun speed on every possible day, the number of eligible real participants, or the psychological meaning of a Line.

## 5. Honest acceptance, limitations and next external gate

**Achieved G38:** a fixed source-to-analyst mapping, an inspectable four-scenario/six-style bank, an executable mock freeze/outcome/score with independent control for general response-style popularity and person-level correlation, a 366-date verified strict-Swiss **Line-versus-Key input precision** audit, no actual user/participant data. The original Gene Keys and Hellenistic source registries, including their disagreements, remain unchanged.

**Not achieved:** independent human verification that the messages actually evoke the intended six distinct states, full literal Rudd Line-2/4 coverage, official Gene Keys Profile parity, 88°/day Design method adjudication, independently certified speed bounds for actual birth eras, real birth timestamp consent/custody, participant blinding, a trusted pre-answer external timestamp, power plan, actual held-out outcomes, or increment over a real frozen HD behavioral interpreter. As a result, this remains **`ANALYST_DERIVED_EXPLORATORY_NOT_HUMAN_READY`**, not a demonstrated source prediction or finalized real study. **0 human predictive validations, 0 production model changes.**

**Next useful step:** a separate neutral **message manipulation/credibility check** by independent reviewers (without exposing any chart or source Line), followed—only if the source/analyst distinction and exact Line birth-input eligibility make sense—by an authorized new consenting cohort, truly frozen scripts/predictions, chart decoys and independent response custody. If these six communication constructs cannot be distinguished reliably, record the negative source-feasibility finding and choose a more explicit source-anchored behavior rule instead of retuning descriptions after outcomes are observed.

The root exclusive `participant-session-v1` study and the accepted Hellenistic C34 synthetic freeze have **not been changed**. Broader user scientific objective remains **OPEN**, independent of this completed source/engineering subtask.


## Final source/engineering verification and accepted artifact hashes

- **29/29** G38 focused source-lock, synthetic mock, stimulus-factual-equivalence and full Sun Line interval tests passed with the existing project venv and verified Swiss local `.se1` files.
- **88/88** complete Gene Keys G35–G38 tests passed, including all **59** accepted prior source checks and **29** G38 tests.
- **367/367** Hellenistic inherited source/engineering tests passed with optional pinned ERFA/IERS sources enabled; **455 distinct source/engineering tests across two research lanes**. These are **not** 455 human predictions or validators.
- The final accepted mock `freeze → mock → score` was rerun in an isolated temporary directory by three different CLI invocations, and **all three JSON files were byte-identical to the accepted packets** (source hashes exactly as in the above table). Saved tests additionally detect even validly rehashed synthetic model/participant deviations and refuse overwriting the accepted freeze.
- **Prepublication stimulus refinement:** direct automated word count found the initially drafted "practical" Line 5 message was not shorter than all others. Before accepting G38 and while there were **no real human responses**, the Line-1 message was lengthened to **56–57 words** and Line-5 shortened to **29–30 words**, preserving all three exact factual sentences in each of the six versions per fictional scenario. The three simulated packet files were then generated anew in freeze-before-mock order; superseded artificial dry-run files are preserved *outside* Git under `/tmp/g38-superseded-prepublication-synthetic/`. This is not after-the-fact retuning of human outcomes. It DOES create a new message-length manipulation confound that must be transparently checked by independent people before any actual human trial.
- The 366-date source-only Sun Line uncertainty receipt was regenerated from the actual strict Swiss provider as part of the focused suite. All status labels retain **conditional-on-speed-bound**, no individual birth/clock use and **0 actual human participant outcomes**.
