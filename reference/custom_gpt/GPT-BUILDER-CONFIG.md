# GPT builder configuration

Use these user-facing fields in the Custom GPT editor.

## Name

Life Patterns Interview

## Description

A private voice-or-text research interview with an independent quality-review step before the final record is frozen. You can pause, skip, correct, or resume. The interview does not ask for or use birth/chart information.

## Conversation starters

1. Start my Life Patterns interview.
2. Find my Life Patterns record in my Library and continue.
3. Continue my interview from this chat or a record I attach.
4. Check my independent Life Patterns review.

## Capabilities

Enable **Code Interpreter & Data Analysis** for downloadable backup JSON files.

## Action

Create one Action:
- Schema URL: `https://life-patterns-participant-production.up.railway.app/action-openapi.yaml`
- Authentication: **API key → Bearer**
- API key: use the private submission-only key supplied separately; never use the researcher/admin token.
- Privacy policy: `https://life-patterns-participant-production.up.railway.app/privacy`

The Action first queues the unfrozen, chart-blind primary record for independent study review, lets the GPT check status and submit any admitted clarification answer, and later sends the reviewed frozen primary plus CF-003 records to Joel's encrypted study store. During this development pilot the queued review may be processed through Joel's ChatGPT-authenticated Codex CLI. ChatGPT may require approval for external writes. Use an action-capable non-Pro model.

## Expected opening behavior

A Custom GPT cannot send a message before the user sends or taps something. When the participant taps a starter or sends any first message, the GPT Instructions require it to immediately:
- explain the research purpose, that responses may be shared with Joel, and that the chart-blind interview will receive an independent study-AI review before final freeze;
- say voice or text is fine and the participant may pause, skip, correct, or stop;
- say birth/chart information will not be requested or used;
- request research-use consent covering independent review/final submission, expected voice/text/mixed mode, and permission for useful earlier-life comparison questions;
- then begin without requiring another “ready” message.

For a participant with an existing interview, there are three safe resume paths:
- **Library fallback:** use starter 2. This explicitly authorizes a narrow Library search for canonical Life Patterns export/recovery schemas only. One exact candidate may be imported automatically; multiple candidates require participant selection. Never use a merely similar behavioral/interview file.
- **Same-chat automatic resume (web):** reopen the old interview, type `@`, select **Life Patterns Interview**, then say “Continue my interview.” The GPT uses only that conversation's visible interview context.
- **New-chat attachment:** explicitly attach/add the participant's interview record, then use starter 3.

A generic continue request must not search Library, Memory, chat history, connected apps, or other account-level sources.

Schema 1.2 adds review start, status, clarification, pause/stop/withdraw controls and strict reviewed submission. Import the existing schema URL again; JSON OpenAPI is valid at that YAML endpoint. The same Bearer key remains valid. Treat review IDs as private.

## Delivery hotfix 2026-10-01.5

Add `ACTION-HANDOFF-GUIDE-v1.md` as the sixth Knowledge file. Replace Instructions and reimport the existing Action schema (1.2.1); keep the same Bearer credential. This adds exact backup before the first review call, actionable error paths, the explicit approval sentence, honest stage/count progress, and a bottom status footer. Existing five Knowledge files and frozen v7 measurement wording are unchanged. A separate hybrid question candidate is under development; this delivery fix does not silently activate it.

## Owner testing / GPT updates

Use Builder Preview only for short smoke tests. For any interview whose answers matter, open the GPT as a normal saved conversation.

**Before clicking Update while an interview is in progress:** in that interview chat, ask: `Create my Life Patterns recovery checkpoint before I update the GPT.` Wait for the actual `life-patterns-live-recovery-checkpoint.json` file link and verify the GPT reports the correct answer count. Only then edit/update the GPT. After an update, reopen the same saved conversation if available; otherwise attach the checkpoint or explicitly use the canonical Library fallback. Never interpret a new chat with zero visible turns as proof that the old answers never existed.
