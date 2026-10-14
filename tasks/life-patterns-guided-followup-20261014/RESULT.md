# Automatic eight-question context review — 2026-10-14

**Owner outcome:** After the prior V3-to-historical comparison identified eight specific questions needing conditional clarification, the respondent should be ASKED those questions directly, one at a time, without knowing or selecting route IDs.

**Implemented:** The offline V3 experiment now automatically starts a guided eight-route sequence after a previous JSON is imported, while a separately generated owner-private HTML preloads the exact previous V3 export and begins the first question immediately on open. It shows the original choices and Other text as context, asks the missing decision rule and/or recent real example, accepts No stable default or Skip, and supports Previous, Save & next, resume partially answered exports, Review all, and an explicit JSON download.

Pinned routes: TF1-G01, TF1-G02, TF1-G16, TF1-G23, TF1-M05, TF1-G20, TF1-M01, TF1-M03. Completion is based on an actual source field or an explicit skip; respondent text already saved in context fields is not asked again. New fields do not replace `selected`, `other`, or `unique_behaviors`.

**Delivered locally:**
- `~/Téléchargements/Life-Patterns-8-Guided-Followups-PRIVATE-2026-10-14.html` — owner-prefilled with existing private JSON. File mode 0600; do not share. Opens at first unfinished question, no import step.
- `~/Téléchargements/Life-Patterns-Idiographic-Pilot-2026-10-10/LIFE_PATTERNS_GUIDED_EIGHT_FOLLOWUPS_2026-10-14.html` — generic unfilled offline version that starts after import.
- `~/Téléchargements/Life-Patterns-Researcher-Guide.html` now has an entry titled **Answer my eight context follow-ups** pointing to the owner-private file.

**Privacy and scientific limits:** All private answers remain on the authorized local computer; no exact answers are in Git or tests, and no network is required to use the pilot. Data are **not** submitted to Railway or to the previously completed independent review. The live GPT question bank, frozen V7/V1, natal scoring and previous 84+3 submission remain unchanged. Optional context is a source-improvement exercise, not new independent birth-chart validation.

**Verified:** A synthetic file-based browser test imports 25 original answers and three unique behaviors, completes/backs/skips/reviews all eight prompts, resumes partial progress on re-import, preserves untouched answers on export, and checks mobile width and zero external calls. An additional browser test opens the real private prefilled file and verifies that it starts the first route with all 25 saved answers and three behaviors loaded (no private wording printed). The previous edit/re-import and contextual-input regression browser tests also pass. Focused Python tests cover bank identity, no-network boundaries, private HTML escaping and file mode, malformed source, and idempotent guide link installation.

**Remaining owner step:** open the private file from the Life Patterns researcher guide, answer or skip the eight guided questions and select Export updated JSON; the participant's replies cannot be supplied by automation. No manual route selection, new interview, or GPT editor change is required.
