# Public-method cross-family review

Model: claude-opus-5-5, requested effort max. Scope: public policy and constructed examples only. No participant data or birth information supplied.

**Verdict: FINDS_ERROR.** The direction is right: don't restart, preserve the imported evidence, keep unknowns as unknown, and treat a mechanical pass as `needs_semantic_review`. But one load-bearing gap lets edited content be credited as if it were what the respondent was actually asked. Separately, the "attestation completeness" check is ambiguous. Read strictly, it either rejects honest unknowns or invites fabricated attestations.

**Weakest load-bearing step**

The policy treats the edited record's content as the elicitation context.

- It labels turns "edited" but never says what that label changes.
- "Preserved exactly as received" preserves the edit, not what the respondent saw or said.
- Quote containment is checked against the edited record, so it only certifies the edit.
- The policy's own rule against inferring a construct from context that wasn't elicited would catch this. But nothing says that edited question text doesn't count as elicited context.
- Participant confirmation may stand in for recovering the original, with no limit on what confirmation can establish.

**Counterexamples (all newly constructed)**

1. **Editor-added premise leads to false credit.**
   - Question actually shown: "What happens when you promise a friend something?"
   - Edited record: "You promised a friend a small task; you have a free evening and normal energy. Do you finish it?"
   - Answer: "Usually, yes."
   - The mapping sees an admissible follow-through scene, containment passes, and attestations are honestly unknown. Follow-through gets credited under conditions the respondent never saw.
2. **Stripped condition leads to over-general credit.** The respondent said "I'd probably speak up, unless my manager was there." The edit reads "I'd speak up." The missing hedge and condition now read as unconditional, and confirming the gist tends to accept the cleaner text.
3. **Dropped antecedent.** The record keeps "How dependable is that feeling? — Mostly" but drops the turn showing whether a bodily or felt reaction was reported. The protocol suppresses SIGNAL-DEPENDABILITY without that antecedent. So the item must stay unassessed: neither credited nor scored as "no signal."
4. **Editor text laundered through confirmation.** The answer field holds an editor's summary: "Plans trips in detail; dislikes improvising." The participant says "yeah, that's me." That is agreement with framing someone else supplied, which the protocol refuses to count as the respondent's own answer.
5. **Barrier.** The question has been reduced to a heading, "Deadlines." The answer is: "Bounded report, a week to do it: I start early; if two deadlines collide I say which slips." The answer states its own determining conditions. If mapping requires the question to match a bank route, this valid report goes uncredited.
6. **Barrier or fabrication.** Consent is unknown, so the completeness check fails. Either the import is rejected, or someone types "yes" to get it through.

Apart from 5 and 6, the policy doesn't discard valid evidence. Keeping unmapped off-bank content out of canonical credit is required by the protocol, not an artificial barrier.

**Continuation vs restart**

A continuation packet plus scoped mapping is sufficient, and better than a restart.

- A restart doesn't give a clean baseline. The respondent has already answered, so a retake is a second exposure shaped by the first. It would also discard evidence and add burden.
- The plan is reversible only on the data side. That requires an unchanged import plus versioned mapping notes that record the reviewer and their exposure.
- Anything the respondent sees can't be undone, so it comes last: recover the original, then map, then work out what's unresolved, then contact the participant.
- Where practical, have the participant review their prior text after the new questions, so re-reading doesn't prime the new answers.
- Work out "unresolved" from what the preserved respondent text says, not from what has been credited. Otherwise distinctions that were answered but not credited get asked again.

With only two people, the kind of source can be mistaken for a difference between the people. Condition-stripped edits look more trait-like than native answers. Carry the source kind into the shared-model feasibility check.

**Smallest necessary correction**

1. **Add one rule for edited records whose original can't be recovered.**
   - Question-side text is unverified and can't set an answer's scope. Answers that depend on it stay partial and go through the normal continuation gate.
   - Credit rests on the respondent's own words, including any conditions they state.
   - A missing hedge, condition, or correction is not evidence that it was absent.
   - Conditional routes need their antecedent to appear in preserved respondent text.
   - Editor-written text is never credited. That covers summaries, labels, headings, and third-person paraphrase.
   - Confirmation, done turn by turn, only attests the gist of the respondent's own text. It can't verify what the question said. It can't support wording-level credit for framing or negotiation constructs. Updates become new dated turns.
2. **Define completeness as "every field present, marked attested, unknown, or n.a., with its source."** An unknown value limits how the record can be used; it never blocks the import.
   - Consent unknown: private preservation and draft mapping only. No fitting or sharing until consent is confirmed, first thing in the continuation contact.
   - Blinding unknown: a flag carried into any fit.
3. **Disclosing birth exposure doesn't fix it.** The protocol bars birth data from selecting, admitting, or interpreting questions. Anyone who has seen birth data shouldn't make mapping or continuation-selection decisions. Use a reviewer working only from the birth-free packet.
4. **Remove "validated" as a status the pipeline can reach.** After semantic review, the highest status is "reviewed for development fitting."

*I reviewed only the supplied packet; no files, birth data, charts, or fits were consulted.*
