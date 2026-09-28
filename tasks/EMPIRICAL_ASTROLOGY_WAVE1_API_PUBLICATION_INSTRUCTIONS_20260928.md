# Empirical Astrology Wave 1 — Worker Publication Recovery Instructions

Date: 2026-09-28

Use this for W04-W10 when the extraction is complete locally but shell `git push` fails because the scratch worktree lacks GitHub credentials.

## Universal worker instruction

Your Wave 1 extraction is already complete. Do not rerun, modify, rebase, regenerate, or reinterpret any extraction output.

The coordinator explicitly authorizes publication of your already-completed worker output.

First verify the existing local state only:
1. `git status --short` — worktree should be clean.
2. `git rev-parse HEAD` — confirm it is the previously reported completed local commit.
3. Do not run `git push`; shell Git authentication is known to fail in these scratch worktrees.

Publish using the connected GitHub connector/API instead of shell Git:

1. Read the exact local contents of your two worker-specific files from the existing scratch worktree:
   - `data/empirical_astrology/wave1/worker_XX_studies.jsonl`
   - `notes/empirical_astrology/wave1/worker_XX_report.md`

2. Create the assigned remote worker branch from current `main`.
   - If the branch already exists, do not create a duplicate; inspect it first.

3. Using the GitHub API, create those exact two files on that worker branch.
   - If a file already exists on the branch, fetch it and compare it with the local file.
   - Only update it if necessary to make the remote content exactly match the completed local content.
   - Do not add or modify any other files.

4. Fetch both remote files back from GitHub and verify they match the local completed files exactly.
   - Prefer SHA-256 comparison if you can compute it on both sides.
   - Otherwise verify byte-for-byte / exact text equality.

5. Verify the remote branch differs from `main` only by your two assigned worker-specific files.

6. Do not merge to `main`, do not rebase, and do not modify the local completed extraction.

7. Report:
   - worker ID
   - scratch worktree path
   - original local completed HEAD
   - remote branch name
   - final remote commit SHA
   - confirmation that both remote files exactly match the local files
   - confirmation that the branch contains no unrelated changes

Important: the remote commit SHA will differ from the original local commit when the files are recreated through the GitHub contents API. That is expected. Content identity is the requirement.

## Worker-specific targets

- W04
  - scratch: `/workspace/scratch/348d11b9c976/humandesign`
  - expected local HEAD: `52a7faace79a5678763603f24ba0bf8fb9817d0d`
  - remote branch: `worker/w04-empirical-astrology-wave1`

- W05
  - scratch: `/workspace/scratch/4783d25ca790/humandesign`
  - expected local HEAD: `6a0e7848b53a6bfefa772a40dfc49b4fc45ebe86`
  - remote branch: `worker/w05-empirical-astrology-wave1`

- W06
  - scratch: `/workspace/scratch/810649803af3/humandesign`
  - expected local HEAD: `d30bf81b42dee9ebfd3d71bee4ed31eb7c3ea8e0`
  - remote branch: `worker/w06-empirical-astrology-wave1`

- W07
  - scratch: `/workspace/scratch/918ffd2c1591/humandesign`
  - previously reported local HEAD prefix: `9db183e`
  - remote branch: `worker/w07-empirical-astrology-wave1`
  - verify and report the full local HEAD before publication

- W08
  - scratch: `/workspace/scratch/910f80e4a736/humandesign`
  - expected local HEAD: `e2eb021fa1194d0f9d0db05c5eb910de385ceb9b`
  - remote branch: `worker/w08-empirical-astrology-wave1`

- W09
  - scratch: `/workspace/scratch/36d1d8caa8da/humandesign`
  - previously reported local HEAD prefix: `a67a506`
  - remote branch: `worker/w09-empirical-astrology-wave1`
  - verify and report the full local HEAD before publication

- W10
  - scratch: `/workspace/scratch/dab908b31973/humandesign`
  - expected local HEAD: `08d25a1a963a2c46746f87411a6eaade7dbd6b9e`
  - remote branch: `worker/w10-empirical-astrology-wave1`

## Success criterion

Publication is complete only when:
- the remote worker branch exists;
- both worker output files are present;
- both files match the completed local files exactly;
- no unrelated changes are present;
- the final remote commit SHA is reported.
