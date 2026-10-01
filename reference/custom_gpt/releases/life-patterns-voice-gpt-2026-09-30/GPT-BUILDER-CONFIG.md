# GPT builder configuration

Use these user-facing fields in the Custom GPT editor.

## Name

Life Patterns Interview

## Description

A private voice-or-text research interview about how you actually respond across situations. You can pause, skip, correct, or resume from an existing interview record. The interview does not ask for or use birth/chart information.

## Conversation starters

1. Start my Life Patterns interview.
2. Find my Life Patterns record in my Library and continue.
3. Continue my interview from this chat or a record I attach.
4. I want to do the interview mainly by voice.

## Capabilities

Enable **Code Interpreter & Data Analysis** for downloadable backup JSON files.

## Action

Create one Action:
- Schema URL: `https://life-patterns-participant-production.up.railway.app/action-openapi.yaml`
- Authentication: **API key → Bearer**
- API key: use the private submission-only key supplied separately; never use the researcher/admin token.
- Privacy policy: `https://life-patterns-participant-production.up.railway.app/privacy`

The Action sends the two frozen research records to Joel's encrypted study store after recorded consent. It does not run model inference. ChatGPT may require the participant to approve this external write. Current OpenAI product behavior does not support Actions in Pro mode, so select an action-capable non-Pro model for this GPT.

## Expected opening behavior

A Custom GPT cannot send a message before the user sends or taps something. When the participant taps a starter or sends any first message, the GPT Instructions require it to immediately:
- explain the research purpose and that responses may be shared with Joel;
- say voice or text is fine and the participant may pause, skip, correct, or stop;
- say birth/chart information will not be requested or used;
- request research-use consent, expected voice/text/mixed mode, and permission for useful earlier-life comparison questions;
- then begin the interview without requiring another “ready” message.

For a participant with an existing interview, there are three safe resume paths:
- **Library fallback:** use starter 2. This explicitly authorizes a narrow Library search for canonical Life Patterns export/recovery schemas only. One exact candidate may be imported automatically; multiple candidates require participant selection. Never use a merely similar behavioral/interview file.
- **Same-chat automatic resume (web):** reopen the old interview, type `@`, select **Life Patterns Interview**, then say “Continue my interview.” The GPT uses only that conversation's visible interview context.
- **New-chat attachment:** explicitly attach/add the participant's interview record, then use starter 3.

A generic continue request must not search Library, Memory, chat history, connected apps, or other account-level sources.
