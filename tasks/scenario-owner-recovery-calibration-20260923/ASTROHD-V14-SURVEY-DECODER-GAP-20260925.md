# V1.4d: fitted signature versus answer-conditioned decoder

Date: 2026-09-25. This is a code-grounded clarification, not a scoring revision.

## What the current code actually does

The staged fitter consumed the existing behavioral translation, admitted source-linked rule instances for supported domains, and used the known development birth moment to select a small subset. The saved V1.4d replay then loads those six fixed rule IDs, the generic source map and candidate chart coordinates. It does not load current survey answers or a current behavioral profile.

Thus its runtime function is `score(candidate_chart; six_saved_rules)`. An edit to the survey does not propagate into this function. The earlier explanation that this was merely a fixed model could be misleading: freezing a general model does not normally freeze its inputs. A fully implemented questionnaire decoder would freeze `F` while allowing `answers` to vary in `F(answers, candidate_chart)`.

The current result is a person-specific development signature fitted using behavior and the known target, not a completed survey-responsive decoder. This distinction must remain in parent outcome and completion state. A successful century audit does not finish the missing input path.

## What needs completing

The missing V1.4 path is: changed raw answer -> neutral recoding with source provenance -> updated versioned behavioral profile -> explicit fixed behavior-to-rule comparison -> recomputation of candidate scores -> ranking over the declared candidate universe. The old answer/profile snapshots remain historical evidence rather than being overwritten.

Use actual support, contradiction and unknown semantics from the adopted measurement/mapping. Do not invent an opposite prediction from mere absence of support. Do not silently introduce arbitrary numerical astrology weights. Routine inference must not rerun target-aware subset optimization against the known birth date on every answer edit and call that decoding. Target-aware fitting remains permitted in separately declared development revisions.

A meaningful recoded answer change can alter ranks; changing wording while preserving its coded meaning need not. Changing an answer irrelevant to the active model need not. Identical candidate feature vectors remain tied for every answer-dependent scoring function that uses only those identical vectors.

## Acceptance examples for the future input connection

- A changed relevant coded assertion actually reaches the scorer and changes the appropriate candidate score comparison, with the exact causal input trace retained.
- An irrelevant or semantically unchanged edit does not create artificial rank movement.
- Unknown is not silently treated as a contradictory response.
- The same fixed scoring function is applied across candidates; the recorded target is used to assess recovery, not to favor itself at inference time.
- Equal feature vectors retain equal scores regardless of answer edits.
- A UI/save action cannot leave a stale prior profile or ranking while displaying the new answer as current.

These are endpoint requirements, not implemented behavior claimed by this note. No survey response, behavioral code, source meaning, selected rule or numerical weight was changed in this task.

## Score is not rank

The recorded instant's score 6 means six selected conditions hold. The 2013 comparator's score 1 means one holds. Neither number is a position in the ranking, a probability, or a likelihood ratio. The earlier tied rank is a separate result: no candidate scored higher than the target, but neighboring minutes tied at six.

## Current execution

The authorized full-century audit keeps the six-rule signature unchanged. It directly checks every minute in the existing century interval rather than reusing approximate interpolation screening. Completing that audit is useful numerical specificity evidence for this signature, not evidence that survey-answer updates have been wired into a decoder.
