# V15 gap-spec admission repair - 2026-10-04

V15 was invalidated by two observed scored failures with the same architecture pattern. W4 proposed PREFER-EXCHANGE correctly but admission rejected it. W7 proposed M05 plus G20 correctly but admission kept only M05. V14 had independently exposed the same general coupling: route-level gap existence and exact question wording were judged as one verdict.

The repair keeps one semantic admission call but returns two independent verdicts. approved now means route-level gap-spec admission and depends only on source reference, answeredness, premise, antecedent/context, material information gain, and batch independence. question_approved means current rendered-question quality and depends only on construct discrimination, one-response-task form, and unsupported extension. Wording-only failures can no longer erase a valid gap.

Fresh validation also fails when an admitted route still has question_approved false, so the split cannot hide unusable participant-facing wording.

The route-level rubric now explicitly says that an unrecoverable placeholder answer does not satisfy a route merely by filling the grammatical slot, and that a preference/intensity/persistence route remains unresolved when source explicitly leaves materially opposed possibilities open without a usual tendency, selection condition, or settled inclination.

Focused evidence: Ruff passed; 29/29 shadow-triage tests passed. Contaminated W4 then admitted PREFER-EXCHANGE in about 31 seconds semantic time. Contaminated W7 admitted G20 plus M05 in about 43 seconds. Neither tuning case had wording rejection codes. These runs are tuning evidence only. The remaining decision gate is one fresh untouched packet, one unchanged stability repeat if it passes, then owner-scale latency measurement.
