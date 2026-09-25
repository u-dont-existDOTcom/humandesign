# V1.4d unchanged-model exact century result

Date: 2026-09-25. Status: COMPLETE. Scope: fixed-signature development audit, not completed survey decoding or independent validation.

## Direct result

The same six-rule model was evaluated over every minute from 1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC, inclusive: 52,596,001 candidate instants. The maximum score is six. Exactly nine instants reach it, all on 1985-01-29 at 10:18 through 10:26 UTC. The recorded 10:25 is jointly first; no candidate scores higher. January 29, 1985 is the sole maximum-scoring date on this entire minute grid. Raw and declared lineage-deduplicated scores coincide because their selected rules coincide.

The original Python scorer was replayed separately. Scores were 6 at 10:25, 1 at the 2013-01-28 08:30 comparator, 5 at 10:17, 6 at 10:18, 6 at 10:26, and 5 at 10:27. These numbers are points for satisfied astronomical clauses, not ranks, probabilities, or counts of correct questionnaire answers.

## What the exact pass changes

The previous century screen used interpolated coordinates with conservative guards. This pass uses direct Swiss-file coordinates with no project-side interpolation. Each minute is examined; evaluation can stop after the first failed clause because a failed clause makes the maximum of six impossible. It enumerates all maxima rather than storing all lower scores.

The native implementation matched all six bits of the frozen Python implementation on 1,989 checks, including all prior four-rule maxima, randomly distributed candidates, endpoints, and second-level local boundary probes. All 263 result chunks were read back and verified to partition the declared grid without gaps or duplicate offsets. Their rejection/max counts sum to 52,596,001. The process exited zero, ephemeris fallback count was zero, and every final winning minute was rechecked by the original Python scorer. Model and executed-source hashes were unchanged at final verification.

The read connection briefly dropped. The existing job completed; no duplicate full scan was launched. Final result and process exit were recovered after reconnection.

## Preserved limits and unfinished owner outcome

This resolves the earlier interpolation-screen qualification at one-minute resolution. It does not exclude sub-minute windows between grid samples and is not a mathematically exhaustive continuous-time result. The previously computed local plateau remains approximately 10:17:52 to 10:26:12 UTC; this pass does not identify uniquely 10:25.

The model was fitted on the known owner case. This is a full-search audit of that fitted signature, not independent evidence of personality-to-birth prediction. No source rules, behavioral meanings, answers, or rule combinations were changed for this run.

The owner's expectation of answer-responsive rankings is correct. The saved V1.4d scorer does not yet implement it: it reads fixed rule IDs and candidate chart coordinates, not edited survey answers. The missing answer-conditioned scoring and survey connection remain OPEN. See `ASTROHD-V14-SURVEY-DECODER-GAP-20260925.md`. Freezing rules does not require freezing answers; meaningful recoding can change rankings in the completed decoder, but identical chart-feature vectors remain tied. Do not substitute known-target refitting or rescoring only today's maxima for that decoder.

## Evidence

The adjacent `ASTROHD-V14-EXACT-CENTURY-RESULT-20260925.json` contains sanitized results, partition counts, and hashes. Frozen model SHA-256: `4bd0b02cc099142f932cc608e821d5db6539e1ec88a67c1d4f93f638d4cc0e83`. Private numerical result SHA-256: `57d110a55f3db9a6e458d5b1578291a59f55d5587dc4dc5b7fe31d1fd31ff45a`. Private direct-readback SHA-256: `59fd8cd0a851787de00feb038a2be8b916361e36f6c92a7ef534a791a23a5a54`. Private raw answers and participant coding were neither accessed nor published in this operation.
