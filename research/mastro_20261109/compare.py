#!/usr/bin/env python3
"""Frozen Mastro keyword comparison, using Python's standard library only.

Roles: custodian freezes charts; blind scorer freezes all response x chart scores;
custodian evaluates frozen scores with a separately held key. No model fitting.
Actual blindness requires an external custodian and access isolation, not filenames.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
from datetime import datetime, timezone
from typing import Any

VERSION = "mastro-literal-match-v1"
ARMS = ("standard", "inverted", "sham90", "sham270")


def canonical(obj: Any) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, allow_nan=False,
                       separators=(",", ":")) + "\n").encode()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_new(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(obj))


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def validate_charts(charts: Any) -> None:
    if not isinstance(charts, list) or not charts:
        raise ValueError("Nonempty chart package required")
    ids = set()
    for chart in charts:
        if set(chart) != {"chart_id", "keywords"} or not chart["chart_id"]:
            raise ValueError("Chart must contain opaque chart_id and keywords only")
        if chart["chart_id"] in ids:
            raise ValueError("Duplicate chart ID")
        ids.add(chart["chart_id"])
        if not chart["keywords"]:
            raise ValueError("Empty chart keywords")
        for row in chart["keywords"]:
            if (set(row) != {"word", "weight"} or not isinstance(row["word"], str)
                    or not row["word"] or isinstance(row["weight"], bool)
                    or not isinstance(row["weight"], (int, float))
                    or not math.isfinite(row["weight"])):
                raise ValueError("Expected nonempty literal word and finite numeric weight")


def literal_score(words: list[str], keywords: list[dict]) -> float:
    # Exactly the reproduced denominator: number of ASTRO rows. Duplicate BIO
    # words each contribute; duplicate ASTRO matches use the first row. Exact
    # duplicate-row source parity remains to be verified. No stemming or trim.
    first = {}
    for row in keywords:
        first.setdefault(row["word"].lower(), row["weight"])
    return math.fsum(first.get(word.lower(), 0.0) for word in words) / len(keywords)


def freeze(charts_path: Path, config_path: Path, out: Path) -> None:
    charts, config = load(charts_path), load(config_path)
    validate_charts(charts)
    required = {"seed", "permutations", "n_north", "n_south", "status",
                "engine_sha256", "settings_sha256", "birth_inputs_sha256",
                "measurement_protocol_sha256", "custody_attestation"}
    if not required <= set(config):
        raise ValueError("Missing preregistration/provenance fields")
    if config["status"] not in {"engineering_only", "preregistered_human"}:
        raise ValueError("Unknown evidence status")
    for name in ("seed", "permutations", "n_north", "n_south"):
        if type(config[name]) is not int or config[name] < (0 if name == "seed" else 1):
            raise ValueError("Invalid integer config: " + name)
    if len(charts) != 4 * (config["n_north"] + config["n_south"]):
        raise ValueError("Exactly four chart arms per enrolled person required")
    for name in ("engine_sha256", "settings_sha256", "birth_inputs_sha256",
                 "measurement_protocol_sha256"):
        value = config[name]
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("Invalid SHA-256: " + name)
    if config["status"] == "preregistered_human" and config["custody_attestation"] != "external_custodian_and_isolated_scorer":
        raise ValueError("Human run requires external custody and scorer isolation")
    record = {"schema": 1, "version": VERSION, "created_at_utc": stamp(),
              "software_base_commit": commit(), "scorer_sha256": sha(Path(__file__)),
              "charts_sha256": sha(charts_path), "config_sha256": sha(config_path),
              "config": config, "answer_key_revealed": False,
              "primary": "south_minus_north_inversion_win_rate",
              "tie_policy": "half_credit_at_exact_zero",
              "score": "case_insensitive_literal_first_lookup_sum_divided_by_astro_row_count"}
    save_new(out, record)


def verify(frozen_path: Path, charts_path: Path, config_path: Path) -> dict:
    frozen = load(frozen_path)
    for field, path in (("charts_sha256", charts_path), ("config_sha256", config_path),
                        ("scorer_sha256", Path(__file__))):
        if frozen[field] != sha(path):
            raise ValueError("Frozen artifact changed: " + field)
    if frozen["version"] != VERSION or frozen["config"] != load(config_path):
        raise ValueError("Frozen contract mismatch")
    return frozen


def score(frozen_path: Path, charts_path: Path, config_path: Path,
          responses_path: Path, out: Path) -> None:
    frozen = verify(frozen_path, charts_path, config_path)
    charts, responses = load(charts_path), load(responses_path)
    validate_charts(charts)
    if not isinstance(responses, list) or len(responses) != frozen["config"]["n_north"] + frozen["config"]["n_south"]:
        raise ValueError("Response count differs from frozen enrollment")
    ids = set()
    for response in responses:
        if set(response) != {"response_id", "words"} or not response["response_id"] or response["response_id"] in ids:
            raise ValueError("Response requires unique opaque ID and words only")
        ids.add(response["response_id"])
        if not response["words"] or not all(isinstance(w, str) and w for w in response["words"]):
            raise ValueError("Nonempty independent measurement words required")
    # No true-chart, orientation or hemisphere metadata enters this operation.
    matrix = [[literal_score(r["words"], c["keywords"]) for c in charts] for r in responses]
    save_new(out, {"schema": 1, "version": VERSION, "created_at_utc": stamp(),
                   "freeze_sha256": sha(frozen_path), "responses_sha256": sha(responses_path),
                   "charts_sha256": sha(charts_path), "scorer_sha256": sha(Path(__file__)),
                   "response_ids": [r["response_id"] for r in responses],
                   "chart_ids": [c["chart_id"] for c in charts], "scores": matrix,
                   "answer_key_revealed": False})


def evaluate(frozen_path: Path, matrix_path: Path, seal_path: Path,
             key_path: Path, repo_root: Path, out: Path) -> None:
    # Verify frozen matrix bytes BEFORE opening any key. Custodian must register
    # the matrix digest independently; a newly fabricated seal is not provenance.
    frozen, matrix, seal = load(frozen_path), load(matrix_path), load(seal_path)
    if seal != {"matrix_sha256": sha(matrix_path)}:
        raise ValueError("Matrix seal mismatch")
    if matrix["freeze_sha256"] != sha(frozen_path) or matrix["scorer_sha256"] != sha(Path(__file__)):
        raise ValueError("Frozen scoring package mismatch")
    if key_path.resolve().is_relative_to(repo_root.resolve()):
        raise ValueError("Answer key must be outside the decoder repository")
    keys = load(key_path)
    if not isinstance(keys, list) or len(keys) != len(matrix["response_ids"]):
        raise ValueError("Incomplete custodian key")
    key_by_id = {k["response_id"]: k for k in keys}
    if len(key_by_id) != len(keys) or set(key_by_id) != set(matrix["response_ids"]):
        raise ValueError("Key response IDs do not match matrix")
    columns = {cid: i for i, cid in enumerate(matrix["chart_ids"])}
    if len(columns) != len(matrix["chart_ids"]):
        raise ValueError("Duplicate matrix chart IDs")
    keys = [key_by_id[rid] for rid in matrix["response_ids"]]
    used = []
    for key in keys:
        if (set(key) != {"response_id", "hemisphere", "arms"}
                or key["hemisphere"] not in {"N", "S"}
                or set(key["arms"]) != set(ARMS)):
            raise ValueError("Invalid key row")
        used.extend(key["arms"].values())
    if len(set(used)) != len(used) or set(used) != set(columns):
        raise ValueError("Chart arms must partition the complete matrix")
    groups = {h: [i for i, k in enumerate(keys) if k["hemisphere"] == h] for h in ("N", "S")}
    if any(len(groups[h]) != frozen["config"]["n_north" if h == "N" else "n_south"] for h in groups):
        raise ValueError("Hemisphere counts differ from preregistration")
    scores = matrix["scores"]
    if len(scores) != len(keys) or any(len(row) != len(columns) or any(not math.isfinite(x) for x in row) for row in scores):
        raise ValueError("Invalid complete score matrix")

    def pair(response_i: int, chart_person_i: int) -> dict:
        k = keys[chart_person_i]
        return {a: scores[response_i][columns[k["arms"][a]]] for a in ARMS}

    def stats(assignment: list[int]) -> tuple[float, float, dict]:
        detail = {}
        for h, indices in groups.items():
            diffs = [pair(i, assignment[i])["inverted"] - pair(i, assignment[i])["standard"] for i in indices]
            detail[h] = {"n": len(indices), "inversion_wins": sum(d > 0 for d in diffs),
                         "standard_wins": sum(d < 0 for d in diffs), "ties": sum(d == 0 for d in diffs),
                         "win_rate_half_ties": sum(1 if d > 0 else .5 if d == 0 else 0 for d in diffs) / len(diffs),
                         "mean_inverted_minus_standard": math.fsum(diffs) / len(diffs)}
        return (detail["S"]["win_rate_half_ties"] - detail["N"]["win_rate_half_ties"],
                detail["S"]["mean_inverted_minus_standard"] - detail["N"]["mean_inverted_minus_standard"], detail)

    observed, continuous, by_group = stats(list(range(len(keys))))
    rng = random.Random(frozen["config"]["seed"])
    b = frozen["config"]["permutations"]
    extreme, extreme_continuous = 0, 0
    null_sum = 0.0
    for _ in range(b):
        assignment = list(range(len(keys)))
        for indices in groups.values():
            shuffled = indices.copy()
            rng.shuffle(shuffled)
            for i, j in zip(indices, shuffled):
                assignment[i] = j
        value, cont, _ = stats(assignment)
        null_sum += value
        extreme += value >= observed
        extreme_continuous += cont >= continuous
    ranks = []
    arm_means = {}
    for h, indices in groups.items():
        expected = "inverted" if h == "S" else "standard"
        for i in indices:
            true = pair(i, i)[expected]
            panel = [pair(i, j)[expected] for j in indices]
            better = sum(x > true for x in panel)
            tied = sum(x == true for x in panel)
            ranks.append({"response_id": keys[i]["response_id"], "hemisphere": h,
                          "rank_best": 1 + better, "rank_worst": better + tied,
                          "midrank": 1 + better + (tied - 1) / 2,
                          "panel_n": len(panel), "unique_top1": better == 0 and tied == 1})
        arm_means[h] = {a: math.fsum(pair(i, i)[a] for i in indices) / len(indices) for a in ARMS}
    save_new(out, {"status": frozen["config"]["status"], "created_at_utc": stamp(),
                   "version": VERSION, "freeze_sha256": sha(frozen_path),
                   "matrix_sha256": sha(matrix_path), "key_sha256": sha(key_path),
                   "answer_key_revealed": True, "primary_contrast": observed,
                   "primary_null_mean": null_sum / b,
                   "primary_upper_tail_p_plus_one": (extreme + 1) / (b + 1),
                   "primary_exceedances": extreme, "permutations": b,
                   "continuous_contrast_secondary": continuous,
                   "continuous_upper_tail_p_secondary": (extreme_continuous + 1) / (b + 1),
                   "by_hemisphere": by_group, "arm_means_secondary": arm_means,
                   "true_chart_ranks_secondary": ranks,
                   "limitations": ["Conditional exchangeability is an assumption", "No causal or human predictive validity from engineering cases", "Uncalibrated keyword scores are not probabilities"]})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    for name in ("freeze", "score", "evaluate"):
        p = sub.add_parser(name)
        p.add_argument("--freeze", type=Path, required=name != "freeze")
        p.add_argument("--out", type=Path, required=True)
        if name != "evaluate":
            p.add_argument("--charts", type=Path, required=True)
            p.add_argument("--config", type=Path, required=True)
        if name == "score":
            p.add_argument("--responses", type=Path, required=True)
        if name == "evaluate":
            p.add_argument("--matrix", type=Path, required=True)
            p.add_argument("--seal", type=Path, required=True)
            p.add_argument("--key", type=Path, required=True)
            p.add_argument("--repo-root", type=Path, required=True)
    a = parser.parse_args()
    if a.operation == "freeze":
        freeze(a.charts, a.config, a.out)
    elif a.operation == "score":
        score(a.freeze, a.charts, a.config, a.responses, a.out)
    else:
        evaluate(a.freeze, a.matrix, a.seal, a.key, a.repo_root, a.out)


if __name__ == "__main__":
    main()
