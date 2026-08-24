# 16 — Claim-grade keyless recovery boundary

## Claim boundary

Application checks and same-user filesystem scans do not establish blindness. A
claim-grade synthetic recovery must run in an externally enforced process boundary
whose mount namespace contains no evaluator secret. The repository supplies a
fail-closed Bubblewrap wrapper and an auditable receipt, but an evaluator/operator
must still provision and attest the host boundary. This finding therefore remains
`PROCESS-REQUIRED` until an actual experiment is executed under that external process
contract.

The wrapper is for synthetic engineering validation. It does not turn synthetic
recovery into evidence that Human Design predicts human behavior.

## Required host preparation

Use Linux with working unprivileged user namespaces and `bwrap`. Build a dedicated
Python environment from `requirements-dev.lock` plus the editable package install.
That environment must contain dependencies only—no credentials, key files, shell
history, evaluator data, or general-purpose user material.

Prepare these public inputs:

- canonical `blind_cases.json`;
- frozen mapping artifact;
- the exact question-bank file whose SHA-256 is stored in that mapping;
- the frozen Model B artifact when selecting Model B;
- for `MODEL-B-DETAILED-V2-NEW`, the exact compiled artifact, freeze receipt,
  passing behavioral-difference audit, and audited retained month-cache file;
- declared Swiss Ephemeris `.se1` files;
- optionally, public `month-*.json` candidate-cache files;
- a new empty decoder output directory.

Encryption keys, plaintext answer keys, encrypted answer-key envelopes, reveal
receipts, and evaluator directories must not be below or symlinked into any supplied
path. In particular, do not reuse a generator run directory containing
`answer_key.json.enc` as the decoder output directory.

## Production invocation

From a clean checkout at the intended commit:

```bash
PYTHONPATH=src .venv/bin/python scripts/run_keyless_recovery.py \
  --blind-file /public/blind/EXP/blind_cases.json \
  --run-dir /public/decoder-output/EXP \
  --ephemeris /public/ephemeris \
  --mapping mappings/mapping_library_v1.json \
  --question-bank reference/core/question_bank_v1.json \
  --python-environment .venv \
  --model MODEL-A-CORE-V1 \
  --candidate-cache /public/candidate-cache
```

For Model B, select its exact frozen identity and artifact:

```text
--model MODEL-B-DETAILED-V1 \
--model-b-artifact mappings/model_b_mapping_library_v1.json
```

For prospective V2, the wrapper verifies the complete difference gate on the
host, mounts the exact retained audited cache only once under the read-only
candidate-cache directory, and the isolated child independently verifies the
same audit/model/cache binding before scoring:

```bash
PYTHONPATH=src .venv/bin/python scripts/run_keyless_recovery.py \
  --blind-file /public/blind/V2/blind_cases.json \
  --run-dir /public/decoder-output/V2 \
  --ephemeris /public/ephemeris \
  --mapping mappings/mapping_library_v1.json \
  --question-bank reference/core/question_bank_v1.json \
  --python-environment .venv \
  --model MODEL-B-DETAILED-V2-NEW \
  --model-b-v2-compiled mappings/model_b_detailed_v2_new_compiled_v2.json \
  --model-b-v2-freeze mappings/model_b_detailed_v2_new_freeze_v2.json \
  --model-b-v2-difference-audit reports/model_b_v2_new/behavioral_difference_2000_01_UTC.json \
  --model-b-v2-difference-cache run_artifacts/known_month_oracle_1000/candidate_cache/month-2000-01-UTC-09e811ca0fe51797.json \
  --candidate-cache run_artifacts/known_month_oracle_1000/candidate_cache
```

The audited cache must be the exact named `month-*.json` member used by recovery;
equal bytes copied to a different sandbox path do not satisfy the child path
binding. The isolation receipt records the verified audit SHA-256, compiled and
freeze hashes, V2 model and question-bank identities, cache and full candidate-
universe hashes, audited month request, and the read-only mount contract.

## Paired Model A/V2 invocation

For the paired oracle comparison, create the public paired plan before either
generation. Both generators must receive the same protected seed file, exact
public config, and their fixed arm ID. In addition to the ordinary public inputs,
each keyless recovery invocation must receive:

```text
--paired-plan /public/paired/experiment.plan.json
--paired-public-config configs/model_a_v2_new_paired_oracle_75.yaml
--paired-generation-receipt /public/generation/ARM/generation.receipt.json
--paired-generation-binding /public/generation/ARM/paired-generation.binding.json
--paired-arm-id MODEL-A|MODEL-B-V2
```

The wrapper mounts those four artifacts as individual read-only files. On a
successful isolated recovery it stages only `blind_cases.json`,
`generation.receipt.json`, and `paired-generation.binding.json` into that arm's
decoder output. It never stages or mounts the encrypted envelope or key.

Freeze each arm's prediction bytes normally. Before revealing either arm, create
one two-arm receipt with `hdmatch freeze-paired-model-a-v2-new`. This verifies the
plan, public config, both generation bindings, both manifests, both prediction
files and freezes, both Bubblewrap receipts, the single exact audited month cache,
generation/recovery source and environment identities, chart-engine identity, and
ephemeris bytes. Both prediction freezes must predate this receipt.

Every paired `reveal-evaluate` call then requires the same complete two-arm
artifact set plus `--paired-freeze`; a partial set fails closed. The authenticated
V3 reveal binds the common seed commitment, target-set hash, local-date-set hash,
paired plan, arm ID, and two-arm freeze. After both reveals,
`hdmatch compare-paired-model-a-v2-new` verifies the complete public chains and
recomputes Top-1/3/5, MRR, midrank, percentile, case-level rank changes, ties,
failures, restoration, and ablation differences without accepting a key or
decrypt capability. Supplied generation receipts must byte-match the public
copies staged by the keyless recoveries.

The wrapper deliberately has no key, encrypted-envelope, decrypt, truth, evaluation,
or reveal argument. If Bubblewrap is absent or cannot create every namespace, the
wrapper exits before creating the output directory. It also refuses a dirty checkout,
a nonempty output directory, a question-bank mismatch, missing public inputs, a child
Python environment different from the wrapper environment recorded in the manifest,
or recognizable plaintext key material in a decoder-visible public/run/cache path.

## Enforced Bubblewrap contract

The decoder is mapped to UID/GID 65534. Bubblewrap unshares user, mount, PID, IPC,
UTS, cgroup, and network namespaces; disables nested user namespaces; drops all
capabilities; starts a new session; clears the inherited environment; and mounts:

- individual tracked `src/hdmatch` files read-only;
- `/usr` and a dedicated Python environment read-only;
- each declared public artifact and ephemeris/cache file read-only;
- exactly one empty run-output directory read-write;
- private `/proc`, `/dev`, and tmpfs `/tmp` instances required by the runtime.

Host parent directories are not mounted. Evaluator key/plaintext/envelope paths are
not accepted by the wrapper and cannot enter the mount plan. Network access is absent
because the network namespace is unshared and no interface is supplied.

On success, `keyless-isolation.receipt.json` canonically records the runtime controls,
mount contract (without host filesystem paths), fixed recovery entrypoint and exit
status, clean source commit/tree, public artifact hashes, and the exact manifest and
prediction hashes. Freeze the prediction bytes immediately after the isolated process
exits; the isolation receipt is evidence about this wrapper invocation, not a
replacement for the prediction freeze/reveal chain.

Before entering Bubblewrap, the wrapper creates the ordinary public run manifest from
the verified clean checkout and exact public hashes. The isolated `recover` command
then follows its existing resume path and requires that manifest to match the complete
recovery configuration. No environment-variable shortcut can replace ordinary Git
revision verification or declare a dirty checkout clean.

## Verification

The always-on tests cover fail-closed runtime detection, command/mount allowlisting,
the absence of key/reveal parameters, broader plaintext-key preflight, and preflight
ordering. Where Bubblewrap namespaces are available, the OS harness additionally
executes as UID/GID 65534, reads a public mount, writes only the output mount, and
fails to read an existing but unmounted evaluator-secret path.

```bash
PYTHONPATH=src python -m pytest -q \
  tests/unit/test_keyless_boundary.py \
  tests/unit/test_sealing_and_reveal.py
```

The harness receipt explicitly says it performs no ephemeris, chart computation,
scoring, or scientific recovery. It must not be described as a successful recovery.

An optional one-case exact recovery exercises the real `hdmatch recover` entrypoint
only when the retained public ephemeris/cache fixtures are explicitly enabled:

```bash
HDMATCH_RUN_EXACT_KEYLESS_E2E=1 PYTHONPATH=src python -m pytest -q \
  tests/unit/test_keyless_boundary.py::test_optional_real_exact_recovery_completes_inside_keyless_boundary
```

This is an integration smoke, not a benchmark, and it never reads or mounts hidden
truth.

## Residual process requirement

Repository code cannot prove that a production operator used the audited wrapper,
that the kernel/runtime itself was trustworthy, that the dedicated dependency
environment contained no secrets, or that a different privileged host process did
not inspect data. A claim-grade report must retain the isolation receipt plus external
process evidence identifying the host/runtime policy and exact invocation. Missing
evidence leaves the run non-claim-grade.
