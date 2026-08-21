# Blind and validation boundary audit

Integrated implementation head reviewed: `a75696ec0f4f86a6b6c0e5c8bdc1639095736e48`

Audit date: 2026-08-21

Claim boundary: synthetic results are engineering validation only; they do not validate Human Design in humans.

## Conclusion

Three original HIGH findings are `CLOSED`. Synthetic pre-recovery isolation is
`PROCESS-REQUIRED`: the integrated preflight and Bubblewrap wrapper enforce the
application and process contract, but claim-grade status belongs only to a particular
recovery that actually ran under that external contract and retained its isolation
receipt. Repository code cannot prove how a future operator mounted or executed a
different run.

Legacy V1 reveal receipts, manifests, or evaluations lacking the current bindings are
not silently upgraded. Claim-grade evidence must be regenerated through the current
chain. This audit does not authorize more security architecture and does not change
the scientific boundary: synthetic recovery is engineering validation, not evidence
that Human Design predicts human behavior.

## HIGH findings

### HIGH-1 — Synthetic pre-recovery isolation: PROCESS-REQUIRED

- Integrated preflight commits and files:
  - `389dd03ed37b9a620ccf22b17364e4d6dc11b0dc` —
    `src/hdmatch/synthetic/sealing.py`, `src/hdmatch/experiments/freeze.py`,
    `src/hdmatch/experiments/reveal.py`, `src/hdmatch/runtime/noise_benchmark.py`,
    and `src/hdmatch/evaluation/report.py`.
  - `5604cc0b2d8c09718a54874ba6c385ec3a9f9157` —
    `src/hdmatch/cli.py` and `src/hdmatch/runtime/recovery.py`, including ephemeris
    path coverage.
- Integrated Bubblewrap boundary commits and files:
  - `dbf28af4de7c5568cdf07b5b7069afdf2ab7ea76` —
    `src/hdmatch/runtime/keyless_boundary.py`,
    `src/hdmatch/runtime/isolation_probe.py`, `scripts/run_keyless_recovery.py`, and
    `docs/16_claim_grade_keyless_recovery.md`.
  - `ab4d4669a757ea56a5e7dd5dbf57433c0b1432bf` and
    `eb693427d8b6ed67c90bc12de02b2c31709413e2` — ordinary-manifest and exact child
    Python-runtime binding in `src/hdmatch/runtime/keyless_boundary.py`.
- Integrated application invariant: recovery accepts no key, truth, decrypt,
  envelope, or reveal capability. Content-based secret preflight runs before model
  loading, cache generation, or scoring; it covers the bounded decoder-visible
  source, run, blind, mapping, ephemeris, and cache paths without trusting file names
  or extensions. Failure output reports counts, not secret paths.
- Integrated process mechanism: the wrapper runs recovery as UID/GID 65534 in
  Bubblewrap with namespaces unshared, network absent, nested user namespaces
  disabled, capabilities dropped, environment cleared, exact public inputs mounted
  read-only, and one empty output directory mounted read-write. Secret and evaluator
  paths and their parents are not mounted. Its canonical isolation receipt binds the
  runtime identity, mount/control contract, source commit/tree, public input hashes,
  recovery configuration, manifest, predictions, and exit status without recording
  host secret paths.
- Exact preflight tests:
  - `tests/unit/test_keyless_boundary.py::test_recovery_interfaces_have_no_key_decrypt_or_reveal_parameter`
  - `tests/unit/test_keyless_boundary.py::test_cli_preflight_rejects_plaintext_key_in_run_dir_before_model_or_cache`
  - `tests/unit/test_keyless_boundary.py::test_cli_preflight_rejects_plaintext_key_disguised_as_ephemeris`
  - `tests/unit/test_sealing_and_reveal.py::test_plaintext_preflight_detects_answer_key_schema_regardless_of_name_or_extension`
  - `tests/unit/test_sealing_and_reveal.py::test_plaintext_preflight_scans_decoder_controlled_cache_and_build_trees`
  - `tests/unit/test_sealing_and_reveal.py::test_plaintext_preflight_detects_nested_human_key_and_tabular_truth_in_bin_file`
  - `tests/unit/test_sealing_and_reveal.py::test_recovery_preflight_scans_candidate_cache_before_blind_input`
  - `tests/unit/test_sealing_and_reveal.py::test_recovery_plaintext_preflight_runs_before_blind_input_or_scoring`
- Exact Bubblewrap tests:
  - `tests/unit/test_keyless_boundary.py::test_recovery_mount_plan_is_allowlisted_read_only_and_keyless`
  - `tests/unit/test_keyless_boundary.py::test_ordinary_manifest_git_revision_ignores_isolation_spoof_environment`
  - `tests/unit/test_keyless_boundary.py::test_wrapper_fails_closed_before_creating_output_without_isolation_runtime`
  - `tests/unit/test_keyless_boundary.py::test_wrapper_rejects_child_environment_that_differs_from_manifest_runtime`
  - `tests/unit/test_keyless_boundary.py::test_real_bubblewrap_boundary_reads_public_input_writes_output_and_denies_secret`
  - `tests/unit/test_keyless_boundary.py::test_optional_real_exact_recovery_completes_inside_keyless_boundary`
- Executed host evidence: both real Bubblewrap tests passed. One proved an existing
  unmounted evaluator-secret location was inaccessible while the public input and
  allowed output worked. The other completed a real one-case exact recovery with no
  key, envelope, reveal, or evaluation capability.
- Why the overall finding is `PROCESS-REQUIRED`: preflight is defense in depth and a
  wrapper test proves the mechanism, not the provenance of a future experiment.
  Claim-grade status additionally requires that the specific recovery actually run
  under the external isolation contract and retain its
  `keyless-isolation.receipt.json` plus operator/host evidence. Application code
  alone cannot prove the operator's mounts, host trust, or absence of privileged
  observation. The operational contract is documented in
  `docs/16_claim_grade_keyless_recovery.md`.

### HIGH-2 — Reveal, envelope, decrypted-key, and manifest binding: CLOSED

- Implementation commit: `41826afd2d45a54746adc26b603637d1c108bbd3`.
- Exact implementation files: `src/hdmatch/experiments/reveal.py`,
  `src/hdmatch/experiments/freeze.py`, `src/hdmatch/experiments/manifest.py`,
  `src/hdmatch/synthetic/sealing.py`, and `src/hdmatch/evaluation/report.py`.
- Enforced invariant: reveal first verifies current prediction bytes, freeze bytes,
  manifest bytes and semantics, then hashes and AES-GCM authenticates the exact same
  encrypted-envelope bytes. `answer-key-reveal-v2` directly binds experiment ID,
  blind-input, model, question-bank, mapping, run manifest, prediction, freeze,
  envelope, and canonical decrypted-payload hashes. Plaintext truth remains in
  memory. Claim-grade evaluation accepts only the in-memory `RevealResult` minted by
  authenticated reveal, not a caller-supplied dictionary, and re-verifies the
  current envelope, receipt, freeze, prediction, and manifest. Ordering is enforced
  as `manifest <= freeze <= reveal <= evaluation`.
- Exact tests:
  - `tests/unit/test_freeze_and_manifest.py::test_strict_freeze_verification_checks_exact_run_manifest_bytes`
  - `tests/unit/test_freeze_and_manifest.py::test_freeze_refuses_manifest_timestamp_after_prediction_freeze`
  - `tests/unit/test_freeze_and_manifest.py::test_manifest_rejects_config_payload_hash_mismatch`
  - `tests/unit/test_sealing_and_reveal.py::test_reveal_requires_valid_unchanged_freeze_and_matching_envelope`
  - `tests/unit/test_sealing_and_reveal.py::test_reveal_refuses_changed_prediction_bytes`
  - `tests/unit/test_metrics_and_report.py::test_claim_grade_evaluator_accepts_no_independent_plaintext_key`
  - `tests/unit/test_metrics_and_report.py::test_evaluator_refuses_mutated_in_memory_reveal_key`
  - `tests/unit/test_metrics_and_report.py::test_evaluator_refuses_envelope_tampered_after_reveal`
  - `tests/unit/test_metrics_and_report.py::test_evaluator_refuses_run_manifest_tampered_after_freeze`
  - `tests/unit/test_metrics_and_report.py::test_evaluator_refuses_reveal_receipt_direct_binding_mismatch`
  - `tests/unit/test_metrics_and_report.py::test_evaluator_refuses_timestamp_before_reveal`

The ordering checks are relative artifact-time checks, not external timestamp
notarization or trusted-clock evidence.

### HIGH-3 — Noise/robustness provenance: CLOSED

- Implementation commit: `41826afd2d45a54746adc26b603637d1c108bbd3`.
- Exact implementation files: `src/hdmatch/runtime/noise_benchmark.py`,
  `src/hdmatch/evaluation/noise_benchmark.py`,
  `src/hdmatch/evaluation/report.py`, `src/hdmatch/experiments/freeze.py`,
  `src/hdmatch/experiments/manifest.py`, `src/hdmatch/experiments/reveal.py`, and
  `src/hdmatch/synthetic/sealing.py`.
- Enforced invariant: every tier is independently loaded from canonical public
  artifacts and verifies the blind hash; direct model/question/mapping hashes;
  canonical run manifest and exact recovery configuration; blind-derived public
  recovery seed; prediction bytes; freeze, reveal, current encrypted envelope and
  evaluation hashes; target-set hash; timestamp order; exact frozen noise,
  missingness, flip, cluster-dropout and reliability parameters; and the same opaque
  post-reveal generation-seed commitment across tiers. The comparator imports no
  decrypt/reveal/key capability and does not decrypt answer keys.
- Exact tests:
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_builds_metadata_from_public_bound_artifacts`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_noise_payload_not_equal_to_frozen_generator`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_recovery_seed_not_derived_from_blind_input`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_manifest_without_exact_recovery_config_payload`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_run_manifest_bytes_changed_after_prediction_freeze`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_tampered_public_provenance_artifact`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_evaluation_hash_not_bound_to_public_chain`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_evaluation_timestamp_before_reveal`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_reveal_timestamp_before_prediction_freeze`
  - `tests/unit/test_noise_benchmark_runtime.py::test_runtime_rejects_prediction_freeze_before_run_manifest`
  - `tests/unit/test_noise_benchmark_runtime.py::test_comparison_binds_exact_recovery_configuration`
  - `tests/unit/test_noise_benchmark_runtime.py::test_comparison_binds_same_hidden_generation_seed_without_decrypting`

The public comparator verifies the evaluator-created seed commitment; by design it
cannot rederive the concealed seed or regenerate noise without entering the reveal
boundary.

### HIGH-4 — Human final-test single-use release: CLOSED

- Implementation commits: `5c6d9fe886d747d4d128ae58de343c8b306641ba` introduced
  the durable final-test workflow and
  `aef277c3d640a12fce31e5af2c83c0fc21d1915b` adversarially hardened its canonical
  cohort lock.
- Exact implementation files: `src/hdmatch/human/artifacts.py`,
  `src/hdmatch/human/workflow.py`, `src/hdmatch/human/protocol.py`, and
  `src/hdmatch/cli.py`.
- Enforced invariant: the external durable release/cohort/freeze/reveal ledgers are
  append-only and independent of ordinary run artifacts. Release binds the exact
  protocol, model, split, canonical participant set and release ID; a canonical
  sorted participant-set digest prevents release-ID or participant-order bypass.
  Freeze must follow release and bind exact prediction bytes. Reveal must follow
  freeze and bind the encrypted key and report. The same cohort cannot be released,
  revealed, or evaluated twice, and deleting or renaming normal run artifacts does
  not reset the external ledger.
- Exact tests:
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_same_release_id_twice`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_cohort_lock_survives_changed_release_id_and_participant_order`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_second_evaluation_of_same_cohort`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_reveal_before_freeze_receipt`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_freeze_before_release_receipt`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_changed_prediction_bytes`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_changed_protocol_model_split_or_participants`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_changed_encrypted_answer_key_after_reveal`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_rejects_timestamp_reversal`
  - `tests/unit/test_human_final_ledger_adversarial.py::test_final_ledger_survives_deleted_or_renamed_normal_run_artifacts`

## Remaining non-HIGH findings

| Severity | Status | Finding |
|---|---|---|
| Medium | OPEN | Human blind scoring still accepts a caller-provided callable whose claimed model reference is checked but whose implementation/capabilities are not. Construct it from exact frozen artifacts or use a restricted keyless worker before a claim relying on that path. |
| Medium | CLOSED | Recovery resume now verifies the canonical exact configuration payload and its digest, including aggregation, threshold, worker count, cache policy, inputs, model, universe, and public seed. Commit `41826afd2d45a54746adc26b603637d1c108bbd3`; tests `test_manifest_resume_requires_exact_recovery_configuration`, `test_manifest_rejects_config_payload_hash_mismatch`, and the noise config tests above. |
| Low | CLOSED | Generator output withholds the external reveal-key filesystem path. The encrypted public envelope path may be printed; the owner-only key location is not placed in decoder-visible logs. Commit `389dd03ed37b9a620ccf22b17364e4d6dc11b0dc`. |

## Verification evidence

- Local complete suite: `260 passed, 2 skipped`; focused integrated security suite:
  `90 passed, 2 skipped`. The two skipped cases are the real Bubblewrap tests that
  cannot run inside the inner Codex sandbox; both passed through the approved host
  boundary as documented under HIGH-1.
- Local Ruff: `All checks passed!`.
- Local strict mypy: `Success: no issues found in 80 source files`.
- Local task acceptance: `TASK_STATUS: INITIAL_ENGINEERING_MILESTONE_READY`, with
  `FULL_MODEL_OBJECTIVE: NOT_EVALUATED_BY_THIS_GATE`.
- GitHub Actions on audited implementation head `a75696e`:
  - push run `32525119352`: passed in 50 seconds;
  - pull-request run `32525122037`: passed in 51 seconds.

No benchmark, answer-key reveal, or human final-test release was performed while
closing these findings.
