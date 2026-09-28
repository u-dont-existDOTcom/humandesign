# Empirical Astrology Wave 1 — Coordinator Recovery Status

Date: 2026-09-28

## Published and merged

- W01 pp.197–272: source head `4e03f8f026e59d78cc9dd5ac773de28d3aa139b3`; merged via PR #33.
- W02 pp.273–329: source head `4ca1e93a1450bf49b38a867f29a1fdcf75256cba`; merged via PR #32.
- W03 pp.330–386: source head `2616a844bd9f3a8702b3dbc79491a37b116b7e92`; merged via PR #34.

These six worker files are now on `main`.

## Completed but local-only / not present on GitHub

The following worker commits were reported by their worker chats but GitHub does not know these SHAs, so the coordinator cannot merge them from this chat. Do NOT rerun extraction. Reopen each worker chat and explicitly authorize publishing its existing committed HEAD to the target branch below.

### W04
- scratch: `/workspace/scratch/348d11b9c976/humandesign`
- local commit: `52a7faace79a5678763603f24ba0bf8fb9817d0d`
- 191 sources; 219 feature records
- target branch: `worker/w04-empirical-astrology-wave1`

### W05
- scratch: `/workspace/scratch/4783d25ca790/humandesign`
- local commit: `6a0e7848b53a6bfefa772a40dfc49b4fc45ebe86`
- 76 summaries; 146 feature records
- target branch: `worker/w05-empirical-astrology-wave1`

### W06
- scratch: `/workspace/scratch/810649803af3/humandesign`
- local commit: `d30bf81b42dee9ebfd3d71bee4ed31eb7c3ea8e0`
- 70 study-level sources; 104 feature records
- target branch: `worker/w06-empirical-astrology-wave1`

### W07
- scratch: `/workspace/scratch/918ffd2c1591/humandesign`
- local commit abbreviated: `9db183e`
- 61 study-level sources; 130 feature records
- target branch: `worker/w07-empirical-astrology-wave1`

### W08
- scratch: `/workspace/scratch/910f80e4a736/humandesign`
- local commit: `e2eb021fa1194d0f9d0db05c5eb910de385ceb9b`
- 98 source/citation groups; 126 feature records
- target branch: `worker/w08-empirical-astrology-wave1`

### W09
- scratch: `/workspace/scratch/36d1d8caa8da/humandesign`
- local commit abbreviated: `a67a506`
- 64 sources / 50 empirical-data-bearing; 91 feature records
- target branch: `worker/w09-empirical-astrology-wave1`

### W10
- scratch: `/workspace/scratch/dab908b31973/humandesign`
- local commit: `08d25a1a963a2c46746f87411a6eaade7dbd6b9e`
- 128 sources/citations; 130 feature records
- target branch: `worker/w10-empirical-astrology-wave1`

## Universal recovery instruction for each worker chat

Replace WXX and TARGET_BRANCH as appropriate:

> Your Wave 1 extraction is already complete. Do not rerun or modify the extraction. The coordinator has explicitly authorized publication. From your existing scratch worktree, verify HEAD is your reported completed commit, then push that exact existing HEAD to `origin/TARGET_BRANCH`. Do not push to main and do not rebase onto current main. After pushing, verify the remote branch contains exactly your two worker-specific output files and report the full remote commit SHA.

Equivalent git action if needed:

```bash
git status --short
git rev-parse HEAD
git push -u origin HEAD:refs/heads/TARGET_BRANCH
```

## Coordinator next step after branches appear

For W04–W10:
1. compare each branch against the Wave 1 base / current main;
2. ensure only the two assigned worker files are added;
3. create/merge coordinator PRs;
4. validate all 10 JSONL files;
5. normalize citations and deduplicate source documents;
6. build the study-family/dataset reuse map;
7. generate the A/B/C/D original-full-text acquisition queue;
8. produce Wave 1 synthesis and then Wave 2 source-family assignments.
