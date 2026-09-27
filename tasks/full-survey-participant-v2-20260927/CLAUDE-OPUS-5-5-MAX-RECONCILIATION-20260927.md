# Claude Opus 5.5 max reconciliation — Full Life Patterns V2

Scope: public generic V2 package/worktree only. No private participant answers, birth data, charts, targets, ranks, secrets, or Downloads were supplied or read.

**VERDICT: PASS_WITH_MINOR_FIXES**

F1–F10, F12 and blocker B1 are all addressed. There is no new blocking issue. This round introduced one small regression in Mode B, and I found two small participant-facing problems (the closing line and the route card). All three are text-level fixes, listed below.

## Resolved vs remaining

| Item | Status | Where / what remains |
|---|---|---|
| **B1** recovery generator | Resolved | Details under F10 |
| **F1** precedence and "can't see the bank" rule | Resolved | Controller:5-13. It overrides protocol:128 for Mode B, and says not to improvise questions if the bank isn't visible |
| **F2** old chat: exact visible turns, no Memory rebuild, contamination | Resolved | Controller:35-42, including `not_visible_in_context` |
| **F3** edited-record conditions can't be laundered | Resolved, with one regression | All four rules are there (:54-65). **But** HEAD's Mode B said "preserve the attached record **exactly as received**", and line 52 now says only "preserve the record as its declared source type". The turns contract no longer says the answer must be exact either. |
| **F4** fixed consent wording; decline stops | Resolved | :15-27 (includes the later birth-comparison notice). Mode C opens with the bank's intro (:69) |
| **F5** Memory, custom instructions, chart features, fictional answers, clean-chat switch | Resolved | :83-93 |
| **F6** visible route tags, antecedents, exploratory limit | Resolved | :112-130. Matches the bank's exploratory admission and protocol:126 |
| **F7** stop and pause | Resolved | :161-165, consistent with protocol:13. Small gap: `stop_reason` isn't set on a stop |
| **F8** literal JSON template | Mostly resolved | The template parses and its hashes match the builder (tested). Small gaps under fix 4 |
| **F9** serialize once; route card | Resolved, with two defects | Closing line and route card label (fixes 1 and 3) |
| **F10** generator | Resolved | Data round-trips exactly. The fence is always longer than any backtick run. `.strip()` no longer touches the data. Answer-only turns are accepted. `--source-type` is required. Repo paths are refused except `experiments/private/`, which is git-ignored. The controller comes before the imported record. |
| **F12** participant instructions | Resolved | START-HERE covers all five cases, plus "normal chat, not Temporary Chat" and "you don't need to read the file" |
| **#8** file size | Not fixable by text | The packet is now 193,095 bytes. Live ChatGPT file handling is still unverified. |
| **Privacy** | Clean in the worktree | The name isn't anywhere in the worktree. It is still in commit `ddaf34b` on origin; rewriting that is your call. |

## Small fixes worth making before sending
1. **Closing line contradicts itself (controller:306 vs :291).** The one fixed message says "send Joel the … file I created" even when no file was made, which breaks "Never claim a file/link exists". The participant can't tell which case they're in. Use two variants:
   - **File created:** "I created your research record as `life-patterns-participant-export.json`. Download it now and send it to Joel."
   - **No file:** "This chat couldn't create a file, so your record is the JSON block above (or all numbered parts). Use the copy button on each block and send all of it to Joel."
2. **Put "exactly as received" back into Mode B (controller:52).** Also say that imported question and answer text goes into `turns` word for word, never summarized. This is the one regression, and it matters most for the recovery path. Add the phrase to the safeguards test; it slipped through because that test doesn't check for it.
3. **Route card label (builder:41).** This is my own spec's mistake. `context_sources` is not a list of prerequisites:
   - STATUS, OWNERSHIP and ROUTINE-CHANGE show `antecedents=G20`/`G21`, but the bank says they need no prior answer and those links are "advisory, not prerequisites".
   - For the 40 dependent routes, the bank means one matching answer from the list. For example, R09's `G15,R07,R08` means any one of them, not all three.
   - As labelled, the interviewer may wrongly skip the three self-contained routes or tag false antecedents. Instead, derive a flag from `context_requirement`: 39 routes start with "Self-contained", 40 need one prior answer. Assert those counts in the test.
4. **JSON consistency (optional, one line each):**
   - On stop, also set `stop_reason`.
   - Bring back V1's list of `interview_status` values and its coverage keys (`question_id`, `status`, `reason`).
   - Say the `blinding` booleans describe this V2 chat only. Blinding for older sources goes in that source's `source_records` entry as `unknown` unless recovered.
   - `contamination_notes` should record what kind of exposure happened and at which turn, never the birth or chart values. Otherwise the interim record carries them into the "clean" chat.
5. **Generator (optional):**
   - Reject duplicate keys. Today `json.loads` silently keeps only the last one; this is the one remaining silent data-loss path.
   - Allow `answer_text: null`. It's currently refused with a clear error.
   - Run the path check before `mkdir`. A refused run currently leaves an empty directory behind.

Then rebuild the packet. Commit the review file along with the fixes: the whitelist test fails on a clean checkout without it, and it contains no participant data. Keep `.review/` out of the commit, because it isn't git-ignored.

## Ready to send?
- **Generic V2:** yes, after fixes 1–3 and a rebuild. If it has to go out unchanged, it still works. Expect confusing wording at the end of sessions where no file is created, and STATUS, OWNERSHIP and ROUTINE-CHANGE may be skipped.
- **Recovery generator:** yes, it's safe with private input and output paths; I checked the mechanics. First apply fix 2, because the packet embeds the controller; regenerate any packet already made. Then either add the duplicate-key check or check the private JSON for duplicate keys yourself. If a `null` answer is refused, loosen the check rather than editing the record. Also give the participant a message to send with the packet; START-HERE's "Recover my existing interview…" line works.

## Tests
The 12 tests now cover my earlier gaps 1–5 and 7. Still untested: gap 6 (filenames in START-HERE and UPGRADE), the record order in the recovery packet, the command-line path guard, and what the route card's dependency labels mean.

## What I ran
- `python3 -m unittest tests.test_full_survey_participant_v2 -v`: 12/12 OK.
- `python3 -m unittest tests.test_full_survey_resume_packet -v`: 8/8 OK.
- `python3 tasks/scenario-survey-v7-redesign-20260922/verify_v7.py`: 497/497.
- Generator probes with made-up data:
  - A hostile answer containing an END marker, a 10-backtick run, a heading, CR and U+2028 round-tripped exactly (fence length 11).
  - The recovery packet order is controller → route card → record → authorities.
  - Duplicate keys collapse silently, `null` answers are refused, and a blank source type is refused.
  - The command-line checks ran on a copy in `/tmp`: repo input and output paths are refused, and a missing source type is refused.
- Bank analysis of `context_sources` against `context_requirement`.
- Read `git diff HEAD`.
- Searched for the participant name: no hits in the worktree, `.git` excluded. For `.review/` I listed matching filenames only (none) and didn't open it. The name appears only in `ddaf34b`'s history.
- I read no private data and changed no files.
