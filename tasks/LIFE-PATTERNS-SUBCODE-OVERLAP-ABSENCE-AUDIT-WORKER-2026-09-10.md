# Life Patterns subcode overlap / absence audit — fresh rerun worker

Use this as an **execution wrapper** around the already-frozen substantive audit prompt. The first worker attempt failed during output transport and is invalid. Do not inspect or reuse its partial findings.

## Fresh-context requirement

Run in a fresh target-theory-blind context. Do not inspect Human Design, astrology, target mappings, birth/chart data, participant-specific target results, model-fit results, or any theory-exposed interpretation of the subcodes.

For substantive reasoning, read **only**:

1. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt`
2. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`
3. `state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-COMPACT-v1-2026-09-04.json`
4. `state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-NORMALIZED-v1-2026-09-04.jsonl`
5. `state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-PROMPT-v1-2026-09-04.txt`

The wrapper itself is transport/validation guidance, not substantive evidence.

## Important: do not paste the large result into chat

The previous attempt failed while trying to emit a very large inline response. This rerun must write artifacts directly to repository files instead.

Create exactly:

- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`

The JSONL file contains **only** the finding objects required by the frozen audit prompt, one object per physical line, with no Markdown fences, headings, prose, comments, or escaped Markdown underscores.

The summary file contains **only** the final summary JSON object required by the frozen audit prompt.

Do not create a shortened, compressed, representative, or partial result merely to reduce response length. The repository files are the transport.

## Mechanical validation before committing

Run:

```bash
python scripts/validate_life_patterns_subcode_overlap_absence_audit.py \
  --findings state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl \
  --summary state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json
```

The validator checks JSON syntax, exact field sets, sequential `OA-001..OA-N` identities, allowed enums, internal summary counts, blocking-finding references, and 22-observable coverage. It does **not** judge substantive correctness.

If validation fails, correct only the transport/schema inconsistency necessary to make the already-reasoned audit artifact valid. Do not silently shorten or change substantive findings for convenience.

## Commit boundary

Once the two artifacts validate:

1. commit the exact JSONL and summary to `codex/discover-life-patterns-mvp`;
2. report the commit SHA;
3. report each file's SHA-256 and byte size;
4. report validator success and finding count;
5. stop.

Do **not** revise the codebook, response contract, UI, package, calibration selection, or human handoff in this fresh blind worker. The theory-exposed project chat will read the frozen blind audit only after it is safely committed and then decide the authorized disposition.

Do not run automated participant coding, consensus, target scoring/reveal, merge, deploy, recruitment/contact, or spending.

## Failure behavior

If you cannot finish the complete audit, do not commit a partial artifact under the authoritative output filenames. Instead return a concise failure report identifying the operational blocker. Partial findings must not be treated as the audit result.
