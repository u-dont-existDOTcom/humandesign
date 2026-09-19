# Private Chat-answer capture protocol

## Data boundary

The humandesign repository is public. Never commit raw participant answers, private exports, host/device identifiers or hashes derived from private response content. The owner has authorized durable preservation of this Chat pilot outside Railway. That authorization does not publish their personal answers or permit mining unrelated conversations.

Default private location used by the helper is below the current user's home: `.local/share/humandesign/private/chat-pilot-20260919/`. This is a local project data store, not a Git checkout. Require an owner-private directory (0700) and event files (0600). Permission restriction is not encryption. Do not claim protection from a compromised account or device.

## Per-turn workflow

1. Recover the latest private event records through the authorized owner-device connection. Do not copy their text to Git or public diagnostics.
2. Distinguish an actual participant answer from design feedback, a quoted test response, an instruction, a correction or a pause. The current “if I respond yes” example is design feedback only.
3. Before replying with a claim that the answer is saved, append a `participant_answer` event bound to the exact saved `presented_question`. Store the raw answer without replacing it with a paraphrase. Use increasing eight-digit event prefixes (`e00000001-...`) to preserve capture order.
4. Include `captured_at` from the current clock, `source_surface`, `question_event_id`, `source_kind` and `is_design_example=false`. Keep provider sent time null unless actually known. Mixed answers may include source-labelled segments; do not silently relabel the whole answer as a remembered episode.
5. The question record includes the exact text, scene ID, revision, changed assumptions and chosen relationship/time frame where applicable. Save a new question event when the wording or premise changes.
6. Save proposed interpretations separately with their source event IDs and adjudication state. Never present an assistant inference as the original answer. The inference/adjudication record classes preserve a later recovery route; they are not scoring authority.
7. Append corrections using `revises_event_id`; preserve original text. Do not apply the old interpretation to the corrected active answer.
8. Use the same event ID and exact payload on an ambiguous retry. A reused ID with different bytes is rejected; do not invent a new ID merely to conceal an unresolved write.
9. Read back the saved event. Maintain a downloadable private JSON export at useful checkpoints and on request. If the owner device cannot be reached, preserve a local downloadable checkpoint and state the durable-write failure; do not falsely say it reached the owner device.
10. No automatic background monitoring and no silent upload to Railway. A later app transfer requires an explicit evidence-mode-preserving adapter and its own verification.

## Operations

The helper accepts JSON through standard input and prints only a bounded save/count receipt for `append`. Do not put response text in command-line arguments, logs or Git. `export` deliberately returns private content and must be handled as private data.

```
python3 private_capture.py append < private-event.json
python3 private_capture.py status
(umask 077; python3 private_capture.py export > private-export.json)
```

A fresh Chat can retrieve the same local records and resume from the last real answer without waking the inference VM. It must also recover the current public question-bank version. Capture alone does not make the material independently validated, chart-compatible or a live-app answer.
