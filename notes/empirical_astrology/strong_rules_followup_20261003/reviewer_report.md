**Verdict: AGREES_WITH_EVIDENCE.** The evidence supports the bounded negative reading below. I found no material error that could plausibly hide strong separation.

**What the results support**
- **No family came near the benchmark on held-out data.** This includes the selected pipeline.
  - Original arm AUC was 0.45–0.55; year-matched arm AUC was 0.43–0.50.
  - Rough null SDs are about 0.045 (82 v 82) and 0.057 (51 v 51). Every value is compatible with chance, and AUC 0.80 is more than 5 SE away.
- **The strong-looking rules come from fitting, not signal.** The depth-4 fusion tree scores AUC 0.85 / BA 0.80 in-sample, which clears the benchmark. It is at chance held-out. Unrestricted trees fit shuffled labels perfectly.
- **The largest separations are non-astrological.** Both beat every astrology and numerology family:
  - the offender is younger within the pair: 0.87 pairwise accuracy;
  - name format: AUC about 0.69 in both arms, because initials appear only on controls.
- **Matching birth years removes what little there was.** Astro falls from 0.55 to 0.47. The calendar draws (0.48–0.60) show the noise spread.

**What they do not support**
- That no astrological model can work (see below).
- Anything about happiness, which was never measured. The Nobel-achievement proxy is confounded by era, name reporting, geography and selection.
- Any conclusion about an individual.
- A "reverse" signal. AUCs below 0.5 fit null noise plus cross-validation's small-sample negative bias.

**Code and design check**

The pipeline does respond to real signal:
- Year-only drops from 0.63 to exactly 0.50 once years are matched, as the construction requires.
- Name format stays at about 0.69.
- BA values are exact multiples of 1/492 and 1/306, which matches this code's pooled evaluation.

A label-alignment or grouping bug would not produce that pattern. Non-material issues:

1. **Pooled AUC.** Out-of-fold scores are pooled across folds with different scales. In the selected pipeline they also mix model types (tree probabilities and expit of SVM margins). Report fold-averaged AUC too. Near-chance BA makes this immaterial here.
2. **Shuffled-label control.** It uses an unrestricted tree, which always reaches 1.0. A depth-4 permutation distribution would calibrate the 0.85 apparent fit.
3. **No input-format checks.**
   - `dateutil.parse` silently fills partial birth dates from the run date and reads ambiguous day/month strings month-first.
   - Offender sex codes other than `M`/`F`/`U` would be silently excluded, not treated as eligible.
   - Nothing shows either happened.
4. **Provenance.** The aggregates are reshaped from the script's output (`fit` instead of `fitting_diagnostic`; no code or input hashes; no selection log). The packet alone can't prove this exact file produced them, though the arithmetic is consistent.

**A bounded search, not proof of impossibility**

This tested one pipeline:
- date-only planetary features (no Moon, houses, angles or birth time);
- listed names, not birth names;
- six fixed learners on up to 433 features;
- 102–164 previously exposed people;
- one confounded contrast.

It is reasonably informative against a strong, simple signal in these inputs for this cohort. It says little about modest or diffuse effects, time-dependent astrology, or other populations. It supports no claim that no model could work.

Sensitivity was never demonstrated, and one internal hint suggests it is limited. In the original arm, slow planets encode birth year, yet astro scored 0.55 against 0.63 for year alone.

**Do these results explain why individual readings seem accurate?**

No. The cohort test asks whether features predict a coarse label across people. A reading is judged by its subject against detailed self-knowledge, with nothing to compare it to. Fitting you well is not the same as fitting you better than someone else's reading would.

The null group result is compatible with:
- broadly applicable statements;
- real person-specific content that these labels cannot capture;
- selective recall.

None of these is established here. The owner's experience should not be called bias without testing it.

**Weakest step:** there is no quantified sensitivity or uncertainty. There is no planted-signal check and no intervals, and the three repeats only vary the fold split. So the null speaks to strong signals, not modest ones.

**Concrete material bug or counterexample:** none that changes the interpretation. The useful counterexample is a pure artifact: within-pair age reaches 0.87 pairwise accuracy, above the 75% bar under paired scoring. So crossing the bar would not, by itself, have validated astrology.

**Best discriminating next experiment:** a preregistered, blinded own-versus-decoy test. Use the owner's actual reading protocol, frozen in advance, not this reduced model.

1. Each consenting participant (the owner, ideally plus at least 20 others) gets readings from their true birth data and from four decoys matched on birth year and sex.
2. Remove dates, signs, names and jargon, then shuffle the order.
3. Participants rank fit before unblinding. The primary outcome is how often the own reading is ranked first, against 20% chance.
4. Add a Forer arm: an identical generic reading presented as each participant's own.

High fit ratings with chance-level ranking would mean the fit isn't specific to the person. Above-chance ranking would mean the readings carry person-specific information that outcome labels miss.
