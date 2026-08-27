# Survey v2: structural recoverability and empirical accuracy

Survey v2 has two deliberately separate success criteria.

## Structural perfect-match recoverability

This is an engineering test of the frozen prediction and search architecture. For every state in
the verified 1926–2026 century cache, an oracle supplies exactly the answer labels predicted by that
state. The candidate-blind adaptive policy starts with the clean V3.6 plus Moon, Mercury, Venus, and
channel fingerprint, asks Profile, and then asks only the predeclared planetary gate domains needed
to split the current anonymous tie set. A passing audit requires every state to end in a singleton
leaf and therefore achieve unique rank #1.

The selector may inspect only the current candidate partition, the frozen predicted answer matrix,
and unanswered feature ids. It may not inspect birth metadata, the identity of the true candidate,
candidate rank, participant prose, or whether a question would help a known target. Selection rules,
domain prompts, archetype vocabularies, classifier versions, thresholds, and partial-credit rules are
frozen before a validation cohort is opened.

This test detects structural collisions, incomplete question coverage, ranking bugs, and accidental
tie-breaking. It does **not** establish that Human Design descriptions are true or that a human or
classifier can reliably produce the oracle labels.

## Empirical human accuracy

Empirical accuracy must be measured prospectively on unseen participants after all freezes. Report
at least exact-state top-1, date-level top-1/top-k, rank percentile, abstention/Other rate, classifier
reliability, test-retest stability, calibration, and performance against preregistered null and
non-Human-Design baselines. Results must include every enrolled participant under the frozen
exclusion policy, not only confident or successful cases.

Accordingly, a green perfect-match audit permits only this statement:

> The frozen architecture can uniquely recover every cached century state if all behavioral labels
> match its own predictions perfectly.

It does not permit claims such as “the survey identifies anyone's date of birth,” “90% accurate,” or
“scientific breakthrough.” Those require independent prospective human results with uncertainty,
failure cases, and replication.
