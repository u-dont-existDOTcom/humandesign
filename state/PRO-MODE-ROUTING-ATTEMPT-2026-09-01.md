# Pro-mode routing attempt — 2026-09-01

Incident ID: `MC-PRO-MODE-RECEIPT-MISMATCH-20260901-001`

Status: `REJECTED_AS_REQUIRED_PRO_MODE`

The first clean meta-review attempt ran in signed-in ChatGPT Chat on the
`u-dont-exist.com Pro` account, but the visible reasoning control was **Extra High**
(`GPT-5.6 Sol`), not **Pro**. The response itself correctly refused admission as the
required Pro-mode meta-review. Its substantive review is non-authoritative candidate
input only.

```json
{
  "conversationUrl": "https://chatgpt.com/c/6a9748cc-3c10-83ea-83dc-d3e3f3d1edad",
  "conversationSessionId": "6a9748cc-3c10-83ea-83dc-d3e3f3d1edad",
  "surface": "Chat",
  "accountUi": "u-dont-exist.com Pro",
  "visibleModePreSubmission": "Extra High / GPT-5.6 Sol",
  "inputPayloadSha256": "99e4e8fb5596e85ebe090a945089f4d408eb325eb86606a835b4591474f1dec0",
  "submittedVisiblePayloadSha256": "9749d79349f1c1b95b4ae466be520fdbced748c28debd3ab4392f2b69a613beb",
  "completedResponseSha256": "8d2b2e01403ba861e646dfad30ce6a033228bab83a742814c3a10496022aa49f",
  "completedResponseLength": 19138,
  "assistantTurnCount": 1,
  "stopButtonAbsent": true,
  "visibleModePostResponse": "Extra High",
  "proMetaReviewAdmission": "REASONING_SURFACE_MODE_MISMATCH",
  "proMetaReviewAuthoritative": false
}
```

The corrected transaction uses the same single Brave-connected ChatGPT tab after
moving the reasoning-power control from Extra High (4 of 5) to Pro (5 of 5). Its
verified pre-submission receipt is:

```json
{
  "conversationUrl": "https://chatgpt.com/c/6a974b8a-31dc-83ea-90b5-f653b825a631",
  "conversationSessionId": "6a974b8a-31dc-83ea-90b5-f653b825a631",
  "surface": "signed-in ChatGPT Chat via Brave connected extension",
  "accountUi": "u-dont-exist.com Pro",
  "chatSurfaceSelected": true,
  "visibleModePreSubmission": "Pro",
  "inputPayloadSha256": "fb677f21e4dbc31bf1e9b205b5f6858d15a6a8b58b2c20ef2adcd6dd15d2a462",
  "submittedVisiblePayloadSha256": "0b06b1b79b4a88863eb2ceec559905555800bab4f73f53314a6bc90630b1a93a",
  "submittedVisiblePayloadLength": 51980,
  "userTurnCount": 1,
  "stopVisibleAfterSubmit": true
}
```

The corrected Pro response completed with the same-session and post-mode receipts
verified. Its admitted verdict and complete response are in
`state/PRO-META-REVIEW-2026-09-01.md`. The admitted state is
`PRO_META_REVIEW_ADMITTED_REVISE`.
