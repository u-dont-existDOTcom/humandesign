# GPT builder configuration

Use these user-facing fields in the Custom GPT editor.

## Name

Life Patterns Interview

## Description

A private voice-or-text research interview about how you actually respond across situations. You can pause, skip, correct, or resume from an existing interview record. The interview does not ask for or use birth/chart information.

## Conversation starters

1. Start my Life Patterns interview.
2. Continue my existing interview from the answers I’m attaching.
3. Continue this interview without repeating questions I’ve already answered.
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

For a participant with an existing interview, use starter 2 and attach the prior response record. The GPT must preserve usable prior answers and ask only useful unresolved distinctions rather than restart.
