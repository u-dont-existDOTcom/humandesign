# 05 — Blinding and Secrets

## Threat model

Prompt instructions such as “do not look at the key” are not enough if the decoder agent can read the key file.

Blindness should be enforced by data access.

## Secret-handling rule

During a blind recovery run:

- answer keys MUST NOT exist under the decoder project root;
- answer keys MUST NOT be mounted into decoder containers/worktrees;
- answer keys MUST NOT be in git history accessible to decoder agents;
- decoder logs MUST NOT contain secret paths or plaintext keys.

## Recommended synthetic workflow

1. Generator produces public blind file.
2. Generator serializes answer key.
3. Answer key is encrypted with a passphrase held by the human evaluator, or placed in a separate inaccessible workspace.
4. Decoder receives blind file only.
5. Decoder writes `predictions.json`.
6. Freeze command writes SHA-256 hash plus environment metadata.
7. Only after freeze does evaluator decrypt/reveal key.
8. Evaluation compares frozen predictions with key.

## Freeze record

At minimum:

```json
{
  "experiment_id": "...",
  "blind_input_sha256": "...",
  "model_sha256": "...",
  "question_bank_sha256": "...",
  "mapping_sha256": "...",
  "prediction_sha256": "...",
  "software_commit": "...",
  "created_at_utc": "...",
  "answer_key_revealed": false
}
```

## Human experiments

Researchers/developers may know birth data during development fitting.

Prospective evaluation differs:
- questionnaire collector should not provide chart interpretation before responses freeze;
- decoder sees participant responses and declared candidate universe;
- answer/reveal process is logged;
- if the true date is known to an operator, the adaptive question policy must still be automated/frozen so operator knowledge cannot steer it.

## Codex worktrees

Use worktrees/agents for parallel code tasks, but do not assume worktrees create data secrecy.
A worktree under a parent directory containing the secret may still be accessible depending on environment configuration.

For actual blind evaluation, use separate workspace/container/repository boundaries or encryption.
