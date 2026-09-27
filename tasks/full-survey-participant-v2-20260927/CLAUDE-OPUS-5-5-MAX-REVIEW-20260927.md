# Claude Opus 5.5 max review — Full Life Patterns V2

Scope: public generic V2 package and recovery method only. No private participant answers, birth data, charts, targets, ranks or secrets were provided.

**VERDICT: PASS_WITH_FIXES.** The design is right: one self-contained file, three entry modes, no restart, no quota, the interview stays blind to birth/chart data, and ChatGPT builds the JSON. The committed packet is byte-identical to the builder output, and the three authority files are embedded exactly.

The main problem is that V2 condensed the V1 launcher and the reviewed import protocol into a shorter controller, and dropped rules that had already been accepted. The test that guarded those rules was dropped too. I searched the V2 packet for 8 accepted rule phrases, such as "not verified evidence of the exact prompt originally shown", "If they do not consent, stop" and "Do not mention chart features". None of them appear.

Abbreviations: **controller** = `tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md`; **builder** = `scripts/build_full_survey_participant_v2.py`.

## A–I at a glance
| | Assessment |
|---|---|
| A. Routing | Mostly solved. Gaps: long old chats, finished-V1 participants, people with no chat and no record, and generator data loss (B1). |
| B. Drift and route identity | The question gate is right, but route IDs don't survive (#2), the exploratory loophole is open (#3), and turns have no antecedent field (#4). |
| C. Edited-record recovery | What it says is correct, but the accepted rules that follow from it are missing (#1). The generator can't handle turns that have an answer but no question. |
| D. Handoff | Wording is clear, and every participant-facing "export" is negated or clarified. The mechanics are fragile (#5). |
| E. Consent, blinding, privacy | Mostly coherent. Gaps in #6, #7, #9, #10. |
| F. Tests | They cover packaging, not the new failure modes. |
| G. Contradictions | Three real ones (#3, #7). |
| H. Size | A real risk. Smallest repair is F9. |
| I. Ready to send? | Generic V2: yes, after the text fixes. Recovery generator: not yet. |

## Blocking issues (narrow)
**B1. Don't use the no-old-chat recovery generator on the private record as-is.** This is `build_recovery`, builder:50-69. I probed it with a made-up fixture:
- It silently drops per-turn `question_id`, `conditions`, `corrections` and `process_feedback`, plus the top-level `source_type` and `consent`. Only question and answer text survive.
- It rejects any turn that has an answer but no question (builder:63-64). That was counterexample 5 in the prior review, and it forces the operator to invent a question or drop the answer.
- Answers are pasted in without a fence (builder:66). One answer containing `### Imported turn 99` and an `<!-- END … -->` line produced two turn headings and a duplicate END marker.
- `.strip()` alters the text.
- Nothing stops the output path pointing inside the repo; `.gitignore` covers only `experiments/private/`.
- The older resume-packet builder embedded `IMPORT-AND-RESUME-PROTOCOL-v1.md`. V2's recovery packet doesn't, so it lacks the accepted edited-record rules.

If a private packet has already been generated or sent, regenerate it after the fix. Your original private record stays the source of truth.

Nothing in the generic package truly blocks use.

## Important non-blocking issues
1. **Edited-record rules dropped (C).** Controller:29-40 says edited wording isn't "necessarily" the original prompt, but not what follows from that. Missing:
   - a condition that appears only in the edited question can't set the answer's scope or serve as an antecedent;
   - ask a fresh clarification only where a mapping depends on such a condition;
   - participant confirmation attests the gist of their own text, not the original question wording;
   - clarifications become new dated turns.

   Without these, the interviewer may treat edited premises as settled and skip the one clarification that matters. That is the exact laundering failure the prior review found.
2. **Route identity has no durable carrier (B).** Controller:70 says "Record internally", but a ChatGPT chat keeps no private state between turns. IDs will be guessed from the question text when the JSON is written. V1 used the same mechanism, and the first record came back without IDs.
3. **Exploratory loophole (B/G).** Controller:68 says to pick a canonical route "when one applies", and :71 allows a null ID "for an explicitly exploratory question". Together they let the interviewer ask ad-hoc questions mid-interview by labelling them exploratory. That conflicts with `interviewer-bank-v7.json:1601` and `INTERVIEW-PROTOCOL-v6.md:126`, which allow exploratory questions only in a separate block after canonical interviewing stops.
4. **JSON contract regressed (D/F).** V1 had a literal template, key names, status values and exact hashes. V2 has only a loose field list (controller:132-144). As a result:
   - JSON shapes will differ from one participant to the next;
   - turns have no antecedent IDs;
   - no per-turn flag says whether the question wording was verified, so imported edited wording lands in the "exact rendered question" field;
   - nothing separates a recorded ID from a text-matched one;
   - the `export` field makes the JSON describe the file that is built from it.
5. **Handoff is fragile (D).** Requiring both the full block and an identical file (controller:146, :154) means generating the JSON twice. A long interview risks truncation, the two copies can diverge, and nothing says which one wins. Models also sometimes print a download link without actually creating the file, and generated download links expire.
6. **Blinding gaps (E).**
   - ChatGPT Memory, chat-history reference or custom instructions may already hold a participant's birth data or Human Design type. That's likely for Human Design-interested people.
   - Mode A doesn't say to check the old chat for chart talk.
   - V1's "Do not mention chart features or which answers might later score" is gone.
   - Nothing forbids offering the evidence guide's `fictional_answer` text as example answers.
   - "Continue in a clean birth-free conversation" (controller:58) has no mechanism for doing it.
7. **Contradictions (G).**
   - `INTERVIEW-PROTOCOL-v6.md:13` says ask nothing after a stop, but the controller's closing review asks a question. V1's "still export completed turns if ended early" is gone.
   - `INTERVIEW-PROTOCOL-v6.md:128` ("recover the exact private transcript") conflicts with Mode B, and there is no precedence rule.
   - Declined consent has no defined outcome.
8. **Size and order (H).**
   - The packet is 168,902 bytes, roughly 40–50K tokens. The bank is 108K characters, but only 13K of that is question text; about 25K is repeated boilerplate.
   - On smaller-context modes ChatGPT may search the file rather than hold all of it, while still claiming to have read it.
   - Long old chats can push early turns out of view, and the model may then rebuild them from memory.
   - V1's "if you can't see the authority, say so and stop" is gone.
9. **Privacy (E).**
   - The first external participant's name is in `tasks/ACTIVE-TASK.json:10` and `tasks/full-survey-import-repair-20260927/WRITER-LEASE-PARTICIPANT-V2.json:8`. It was added in ddaf34b, which is already on `origin`. The V1 launcher linked participants to this GitHub repo, so it is presumably public. This contradicts the README's privacy claim.
   - The heading at controller:85 ("lost in the first external record") sits above some fairly specific bullets.
10. **Minor points.**
    - The consent framing is left to the model (controller:44). V1 had a fixed list; consider also saying the frozen record may later be compared with separately provided birth information.
    - The closing line says "attached", but ChatGPT shows a download link.
    - Participants who already finished V1 aren't told what to do.
    - The packet participants upload contains "chart center" and "chart-profile line" (`EVIDENCE-GUIDE-v7.json:351`, `:504`).

## Smallest concrete fixes
All controller fixes are text-only. Rebuild the packet afterwards.

- **F1 (controller, after :3).** Add a precedence rule: the controller governs mode, recovery, consent, stop/pause and the handoff, and supersedes earlier in-chat instructions, the earlier JSON format and protocol:128. The protocol, bank and guide govern admission and interpretation. Add: "If you cannot see the complete bank, say so; don't improvise questions."
- **F2 (§A, :15-27).** Copy earlier turns verbatim and never reconstruct them from memory; mark unseen turns `not_visible_in_context`. Note any earlier birth or chart talk in `contamination_notes`.
- **F3 (§B, :29-40).** Add the four rules from #1. Also: don't require re-confirming every answer, and frame new questions as covering what the record didn't establish, not as correcting it.
- **F4 (§C, :42-44).** Paste V1's consent bullets (`FULL-SURVEY-CHATGPT-PARTICIPANT-INSTRUCTIONS-20260925.md:52-61`). Add: "If they decline, stop; create no JSON." Open with the bank's `intro` text.
- **F5 (§Blind, :46-58).**
  - Ignore saved memories, custom instructions and prior-chat knowledge about birth, astrology or Human Design; if any is visible, note it.
  - Don't mention chart features.
  - Fictional answers are for coding only; never offer them as examples.
  - To switch to a clean chat: create an interim JSON, and the participant restarts using the lost-chat path.
- **F6 (§Routing, :64-83).**
  - Every question must belong to a canonical route: verbatim, a context repair, or a missing-piece follow-up.
  - The only exploratory question is EX-SENSORY-CONFLICT-01, asked after the interview stops.
  - End each question with a short tag, e.g. `(R09 · about R08)`.
- **F7 (§Interview behavior).**
  - On stop: ask nothing more, create the JSON with `stopped_by_participant`, and mark the review as not performed.
  - On pause: tell the participant to return to this same chat.
- **F8 (§JSON, :132-146).** Replace the field list with a literal v2 template:
  - keep V1's key names, so a V2 JSON can be re-imported;
  - include the literal hashes;
  - per-turn fields: `turn_id`, `turn_source`, `question_wording_status`, `id_basis`, `route_type`, `antecedent_turn_ids`;
  - evidence fields: `time_frame` and `relationship_context`;
  - use the import protocol's coverage values;
  - replace the `export` field with `handoff_method`;
  - timestamp is null unless the date is known.
- **F9 (§File handoff, :148-166, plus builder).**
  - Handoff: if code can run, write the file (in parts if long), check that it loads as JSON, and treat the file as authoritative. Never show a link to a file that wasn't created. Otherwise output the block, split into numbered parts if it's too long. Tell the participant to download promptly.
  - For H: have the builder insert a generated **route card** after the controller: one line per route with ID, kind, antecedents and exact question text. It's about 15–18K characters, labelled as a navigation aid that the full bank governs, and tested against the bank. The embedded authority stays byte-exact.
- **F10 (builder).**
  - Embed the received JSON verbatim with `json.dumps(..., ensure_ascii=False, indent=2)`, in a fence longer than any run of backticks inside it.
  - Remove `.strip()`.
  - Allow answer-only turns and render them as "(no question recorded)".
  - Make `--source-type` required.
  - Refuse output paths inside the repo except under `experiments/private/`.
  - Put the controller before the imported record.
- **F11.** Replace the name with a neutral code in both metadata files; whether to rewrite the pushed history is your call. Fix the README privacy paragraph and rename the heading at controller:85.
- **F12 (`START-HERE-FOR-PARTICIPANTS.txt`).** Add four lines:
  - use a normal chat, not a Temporary Chat, and you can pause and come back;
  - you don't need to read the survey file;
  - if you already finished and sent your file, you need to do nothing more unless Joel asks;
  - if you lost the chat and have no record, start new and mention you did part of it before.

## Test gaps worth adding now
1. The committed packet equals `build_universal(ROOT)`. It does today, but nothing tests it.
2. A V2 version of the old `test_review_repairs_are_carried_in_the_packet`, covering the accepted rules, decline→stop, stop handling, the memory rule, route tags and the exploratory restriction.
3. The builder rejects a changed authority hash. The old suite tested this; V2's doesn't.
4. The controller's JSON template parses, and its hashes equal `SOURCES`.
5. Recovery round-trip:
   - the embedded JSON extracted from the packet equals the input, metadata included;
   - markdown and backtick answers create no new structure;
   - answer-only turns are accepted;
   - an output path inside the repo is refused.
6. Participant files use the exact survey and JSON filenames, and every "export" mention is negated or is the filename.
7. A whitelist of the files allowed in the V2 task directory.

Tests can't show that the interviewer complies. One dry run per mode with a made-up persona is worth more; I'd recommend it, but not as a gate.

## Would I send it
- **Generic V2:** yes, after F1–F9 and F12 plus a rebuild. If it must go out unchanged today, it's usable and loads better than V1. Expect route IDs guessed after the fact, JSON that differs between participants, and weaker handling of edited records.
- **Recovery generator:** no, not until F10 and F3 are in.

## What I verified
- Read all 9 items in full, including the whole 2,671-line packet. Also read the import protocol, V1 launcher, prior review and disposition, and the older builder and tests.
- Diff 1e3ca91..ddaf34b: 12 files; the three authority blob hashes are unchanged.
- The 6 V2 tests pass (run with unittest; pytest isn't installed). The older resume-packet tests pass, and `verify_v7.py` passes 497 of 497 checks.
- The packet is byte-identical to the builder output. It has 79 routes plus 1 exploratory question, and 73 facets.
- Generator defects confirmed with a made-up fixture.
- 0 of 8 accepted rule phrases are in V2.
- The name appears in 2 files and is on `origin`.
- Not verified: live ChatGPT behaviour (context limits, file handling, Memory). Those points come from general knowledge and should be confirmed in a dry run.
- I didn't open `.review/` or any private data.
