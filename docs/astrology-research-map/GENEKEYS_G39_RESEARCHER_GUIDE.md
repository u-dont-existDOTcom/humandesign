# Gene Keys G39 — Researcher instructions and scientific limitations

The researcher materials and the reviewer materials are distributed
in distinct ZIPs. Only send the reviewer ZIP to voluntary independent
raters; never attach the answer key, line/category crosswalk, source code, or
research findings to the same invitation.

## Exactly what was executed

- Six offline HTML reviewer packets were generated, each with 24 coded
  fictional messages in a different order. The rater-visible HTML contains no
  intended source Line, original Gene Keys label number or chart.
- Each form asks which source-style descriptor best fits the message,
  confidence, whether the three facts were preserved, naturalness and felt
  pressure. None/unclear is admissible.
- The local standalone Brave/Chromium browser actually executed
  24 simulated clicks and exported parseable JSON for packets R01 and R04;
  both exported files passed the separate Python grader. No real rater.
- The grader checks completeness, respondent-packet ID, category map,
  invalid/duplicate replies and source-provenance file hashes, then emits
  descriptive confusion, per-style accuracy, unknowns, factual-error judgments,
  perceived pressure/naturalness, pairwise inter-rater agreement.
- Three artificial control sets were generated from the answer key itself:
  perfect (144/144), one-class (24/144), and all-unclear (0/144). These are
  programming tests; they are NOT people or communication-quality results.

## How to grade actual opt-in responses later — NOT undertaken now

Run on the owner's private computer with the accepted repo/source files:

  cd /home/joel/development-worktrees/humandesign/astro-genekeys-g39-20261025/docs/astrology-research-map
  python3 genekeys_g39_rate_blind_packets.py \
      --key GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json \
      --ratings /private/consented/G39_R01_optional_ratings.json \
                /private/consented/G39_R02_optional_ratings.json \
      --out /private/consented/G39_manipulation_rating_summary.json

These are schematic paths, NOT files that presently exist. Do not pass
--synthetic-fixtures for actual reviewer submissions. Never commit actual
responses, recruit people through the existing participant-session-v1 task,
or claim the local code verifies rater identity/independence.

## Interpretation and limits

The six style labels are visible to reviewers because this is a source-style
manipulation check, not a hidden natal prediction test. The researcher code and
key are also in humandesign: a determined reviewer could obtain those files.
This is not cryptographically adversarial double-blinding. For a real natal
study use independent response custody and externally sealed predictions.

Do not declare the six-message bank valid just because software regressions
pass or reviewers easily guess the categories. EIGHT messages repeat category
keywords (all four variants of source styles 3 and 5), while style 1 is
much longer than style 5. Styles 2 and 4 only partially capture the source
metaphors about high frequency and romance. Independently rate naturalness
and perceived pressure, and keep all unfavorable results. A response-driven
rewrite is development work, requiring another untouched group if the next
version is to be confirmatory.

Correctly identifying a message's intended style is not evidence that people
born under that Gene Keys Line prefer that style. Human Design and Gene Keys
share the same Rave Line coordinates, so numeric parity is not independent
birth-chart predictive evidence.

Main owner goal remains OPEN. Zero actual human predictive validations.
