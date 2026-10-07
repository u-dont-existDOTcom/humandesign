# Stripped imported-route provenance repair — 2026-10-07

Parent outcome remains OPEN. First repair correctly invalidated legacy G15 and fast triage returned review-ready, but the live existing review later emitted TF1-G15 during legacy final synthesis.

New exact diagnosis: the candidate actually persisted in Railway has only turn_id/question_text/answer_text for historical turns. It has historical_interview_status at record level, but its per-turn source.historical_question_id/canonical_question_id metadata was stripped before the review was started. Sequence 37 still has upstream turn_id e00000094-G15-answer; sequence 58 e00000154-R07-answer; sequence 67 e00000174-WORK-RECOVERY-answer; sequence 68 e00000176-R08-answer. Recovered sequence 80 has a generic ID but its exact question text matches current R07. Fast triage reached review_ready; legacy final synthesis then considered TF1-G15 unpresented because this provenance was unresolved.

Repair:
- canonical ID -> explicit top-level/nested historical ID -> verified known-route suffix in original upstream turn_id -> exact frozen question text;
- normalize old saved states with the same chain;
- final-synthesis route eligibility sees historical + TF1 lineage as presented;
- add a stripped-candidate regression covering the exact live format and legacy make_context/route_cards, not only fast triage;
- after deploy, invalidate the currently pending TF1-G15 on the same existing review and requeue it without adding an answer or skip;
- no participant source text in Git.

Acceptance:
- stripped 81-style synthetic record resolves G15/R07/R08/WORK-RECOVERY from upstream turn IDs and exact text;
- TF1-G15 is not eligible as a fresh canonical route in fast or legacy contexts;
- existing real review keeps clarification_history count=1, clears pending TF1-G15, and resumes same review ID;
- next state cannot return G15 or canonical TF1-G15 merely for the already-answered baseline/version gap;
- focused + participant tests, current-head deploy/readback, live same-review status check.
