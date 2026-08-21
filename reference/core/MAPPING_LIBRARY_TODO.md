# Mapping Library Formalization TODO

The current question bank is intentionally candidate-blind and does not contain server-side HD scoring keys.

Codex must formalize the existing V4/V3.2 rules into `mapping_library_v1.json`.

Rules:
- reuse existing mappings/rationales;
- mark unsupported mappings unresolved;
- do not invent mappings to improve synthetic recovery;
- version and hash the result;
- keep future empirically learned mappings in a separate artifact.
