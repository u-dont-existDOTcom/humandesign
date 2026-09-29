#!/usr/bin/env python3
"""Reviewer probes for the CF-003 secondary module. Read-only: writes only to temp dirs."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from statistics import fmean

ROOT = Path("/mnt/hdd/var/tmp/humandesign-cf003-module-20260929")
sys.path.insert(0, str(ROOT / "src"))

from hdmatch.empirical_astrology import cf003_target as T  # noqa: E402
from hdmatch.empirical_astrology.cf003 import (  # noqa: E402
    CF003_CANDIDATE_BODIES,
    CF003_PUBLISHED_WEIGHTS,
    CF003FactorFlags,
    score_cf003_planet,
)

REF = ROOT / "reference" / "empirical_astrology"
CONTRACT = REF / "cf003_behavioral_classifier_contract_v0.json"
PROMPT = REF / "cf003_behavioral_classifier_prompt_v0.md"


def section(name: str) -> None:
    print("\n=== " + name + " ===")


# 1 ---------------------------------------------------------------------------
section("1. predictor spec parses as JSON?")
raw = (REF / "cf003_published_predictor_spec_v0.json").read_bytes()
print("last 8 bytes:", raw[-8:])
try:
    json.loads(raw)
    print("parses: yes")
except json.JSONDecodeError as exc:
    print("parses: NO ->", exc)

# 2 ---------------------------------------------------------------------------
section("2. flag subsets with equal real (tenths) sums but unequal float totals")
names = list(CF003_PUBLISHED_WEIGHTS)
tenths = {n: round(CF003_PUBLISHED_WEIGHTS[n] * 10) for n in names}
by_sum: dict[int, list[tuple[str, ...]]] = {}
for r in range(len(names) + 1):
    for combo in itertools.combinations(names, r):
        by_sum.setdefault(sum(tenths[n] for n in combo), []).append(combo)



def feasible(combo) -> bool:
    # No body rules both Asc and Desc (opposite signs); no body is both in house 12 and
    # within 5 degrees of the house-9 centre.
    s = set(combo)
    return not (
        {"modern_ascendant_ruler", "modern_descendant_ruler"} <= s
        or {"placidus_house_12", "within_5deg_placidus_house_9_center"} <= s
    )


def ascending_total(combo) -> float:
    total = 0.0
    for n in sorted(combo, key=lambda n: CF003_PUBLISHED_WEIGHTS[n]):
        total += CF003_PUBLISHED_WEIGHTS[n]
    return total


drift = []
groups = 0
for s, combos in sorted(by_sum.items()):
    combos = [c for c in combos if feasible(c)]
    if len(combos) < 2:
        continue
    groups += 1
    scaffold = {
        combo: score_cf003_planet("mars", CF003FactorFlags(**{n: n in combo for n in names})).total
        for combo in combos
    }
    ascending = {combo: ascending_total(combo) for combo in combos}
    print(
        f"  real sum {s / 10}: scaffold-order distinct floats={len(set(scaffold.values()))}, "
        f"ascending-order distinct floats={len(set(ascending.values()))}"
    )
    if len(set(scaffold.values())) > 1:
        drift.append((s, scaffold))
    if len(set(ascending.values())) > 1:
        for combo, total in ascending.items():
            print(f"    ascending {total!r:<22} {combo}")
print("feasible equal-real-sum subset groups:", groups)
print("feasible groups whose SCAFFOLD-order float totals differ:", len(drift))
if drift:
    _, totals = drift[0]
    (c1, t1), (c2, t2) = list(totals.items())[:2]
    pred = {b: 0.0 for b in CF003_CANDIDATE_BODIES}
    pred["venus"], pred["mars"] = t1, t2
    print("  rank_score_groups top groups for a real tie:", T.rank_score_groups(pred)[:2])
    beh = {b: float(v) for b, v in zip(CF003_CANDIDATE_BODIES, [0, 0, 0, 4, 0, 0, 0, 0, 0, 0])}
    cmp = T.compare_cf003_rankings(pred, beh)
    print(
        "  predictor_top_set:",
        cmp.predictor_top_set,
        "primary:",
        cmp.primary_top_set_mean_behavioral_midrank,
        "(a true venus/mars tie would give the mean of both midranks)",
    )

# 3 ---------------------------------------------------------------------------
section("3. float '<=' vs exact rational comparison in the global-permutation count")
print("fmean([10/3, 2.0]) =", repr(fmean([10 / 3, 2.0])), " fmean([13/3, 1.0]) =", repr(fmean([13 / 3, 1.0])))


def exact_count(pairs, perms) -> int:
    mids = [T.midranks_descending(p.behavioral_scores) for p in pairs]
    tops = [T.rank_score_groups(p.predictor_scores)[0] for p in pairs]

    def stat(perm) -> Fraction:
        src_of = dict(zip(CF003_CANDIDATE_BODIES, perm))
        total = Fraction(0)
        for m, top in zip(mids, tops):
            total += Fraction(sum(Fraction(m[src_of[label]]) for label in top)) / len(top)
        return total / len(pairs)

    obs = stat(tuple(CF003_CANDIDATE_BODIES))
    return sum(1 for perm in perms if stat(perm) <= obs)


rng = random.Random(20260929)
found = None
checked = 0
for trial in range(1500):
    n = rng.randint(2, 3)
    pairs = []
    for i in range(n):
        k = rng.choice([3, 6, 7, 9])
        top = set(rng.sample(CF003_CANDIDATE_BODIES, k))
        pred = {b: (2.0 if b in top else float(rng.randint(0, 1))) for b in CF003_CANDIDATE_BODIES}
        beh = {b: float(rng.randint(0, 4)) for b in CF003_CANDIDATE_BODIES}
        pairs.append(T.CF003CohortPair(f"p{i}", pred, beh))
    perms = [tuple(rng.sample(CF003_CANDIDATE_BODIES, 10)) for _ in range(120)]
    repo = T.permutation_test_from_global_label_maps(pairs, perms).equal_or_better_count
    exact = exact_count(pairs, perms)
    checked += 1
    if repo != exact:
        found = {"trial": trial, "repo_count": repo, "exact_count": exact, "n": n}
        break
print("cohorts checked:", checked, "| first float/exact discrepancy:", found)

# 4 ---------------------------------------------------------------------------
section("4. inclusive top-3 when the predictor has < 3 non-zero scores")
pred = {b: 0.0 for b in CF003_CANDIDATE_BODIES}
pred["sun"], pred["moon"] = 8.3, 7.6
values = [4, 4, 3, 3, 3, 2, 2, 1, 1, 0]
results = set()
for shift in range(10):
    rotated = values[shift:] + values[:shift]
    beh = {b: float(v) for b, v in zip(CF003_CANDIDATE_BODIES, rotated)}
    cmp = T.compare_cf003_rankings(pred, beh)
    results.add((len(cmp.predictor_top3_inclusive), cmp.top3_overlap_count, round(cmp.top3_jaccard, 4)))
print("(|predictor top3|, overlap, jaccard) over 10 different behavioral alignments:", sorted(results))

# 5 ---------------------------------------------------------------------------
section("5. packet-builder leakage probes")
spec = importlib.util.spec_from_file_location("cf003_builder", ROOT / "scripts" / "build_cf003_behavioral_packet_v0.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def one_turn(answer: str, **extra) -> dict:
    turn = {"turn_id": "t1", "turn_role": "behavioral", "question_text": "What recurs?", "answer_text": answer}
    turn.update(extra)
    return {"turns": [turn]}


probes = {
    "sun_sign_identity": one_turn("I'm a typical Scorpio, so I go deep on everything."),
    "saturn_return": one_turn("My Saturn return at 29 is when I finally learned discipline."),
    "leo_rising": one_turn("Leo rising here, I like being seen."),
    "planet_in_sign": one_turn("My Mars is in Aries which explains my temper."),
    "my_chart": one_turn("My chart says I am meant to teach."),
    "astrologer": one_turn("My astrologer told me I would change careers."),
    "horoscope": one_turn("My horoscope said this would be a year of growth."),
    "hd_type": one_turn("As a Projector I wait for the invitation before I start."),
    "hd_profile": one_turn("Being a 4/6 profile, my network brings me opportunities."),
    "control_natal_chart": one_turn("My natal chart says this is important."),
    "conditions_field_only": one_turn("I keep checking details.", conditions=["only because my natal chart says so"]),
    "forbidden_keys": {
        "birth_date": "1990-01-01",
        "chart": {"sun": "capricorn"},
        "planet_scores": {"sun": 8.3},
        "turns": [
            {
                "turn_id": "t1",
                "turn_role": "behavioral",
                "birth_time": "12:00",
                "question_text": "What recurs?",
                "answer_text": "I keep checking details.",
            }
        ],
    },
    "missing_turn_role": {"turns": [{"turn_id": "m1", "question_text": "Can you name your zodiac sign?", "answer_text": "Capricorn."}]},
    "record_exposure_flag": {
        "blinding": {"target_check_result": "exposure_detected", "contamination_notes": [{"kind": "x"}]},
        **one_turn("I keep checking details."),
    },
}
with tempfile.TemporaryDirectory() as d:
    for name, record in probes.items():
        src = Path(d) / f"{name}.json"
        src.write_text(json.dumps(record))
        try:
            pkt = B.build_packet(src, CONTRACT, prompt_path=PROMPT)
            blob = json.dumps(pkt)
            note = ""
            if name == "conditions_field_only":
                note = f" conditions={pkt['turns'][0].get('conditions')}"
            if name == "forbidden_keys":
                note = f" turn keys={sorted(pkt['turns'][0])}"
            if name == "record_exposure_flag":
                note = f" exposure carried into packet={'exposure' in blob}"
            if name == "missing_turn_role":
                note = f" included answers={[t['answer_text'] for t in pkt['turns']]}"
            print(f"  {name:24s} ACCEPTED{note}")
        except ValueError as exc:
            print(f"  {name:24s} rejected: {exc}")
    prim = Path(d) / "p.json"
    sec = Path(d) / "s.json"
    prim.write_text(json.dumps({"session_id": "A", **one_turn("participant A answer")}))
    sec_record = {"session_id": "B", "turns": [{"turn_id": "b1", "turn_role": "behavioral", "question_text": "Q", "answer_text": "participant B answer"}]}
    sec.write_text(json.dumps(sec_record))
    pkt = B.build_packet(prim, CONTRACT, prompt_path=PROMPT, secondary_path=sec)
    print("  cross_session_secondary  merged turn answers:", [t["answer_text"] for t in pkt["turns"]])

# 6 ---------------------------------------------------------------------------
section("6. classifier-output validator probes")
answers = {"t1": "I always come back to fairness at work and at home. a"}


def item(cid, rating, support=(), counter=(), suff=None):
    return {
        "construct_id": cid,
        "dominance_rating": rating,
        "evidence_sufficient": (rating is not None) if suff is None else suff,
        "support_quotes": [{"turn_id": "t1", "quote": q} for q in support],
        "counterevidence_quotes": [{"turn_id": "t1", "quote": q} for q in counter],
        "conditions": [],
        "time_frame": "unknown",
        "confidence": "low",
        "reason": "",
    }


def run(name, items):
    try:
        T.validate_behavioral_classifier_result({"construct_scores": items}, answer_text_by_turn_id=answers)
        print(f"  {name:52s} ACCEPTED")
    except ValueError as exc:
        print(f"  {name:52s} rejected: {exc}")


base = [item(c, 2, support=["fairness"]) for c in T.CF003_CONSTRUCT_IDS]
p = list(base)
p[0] = item("T01", 4, support=["a"])
run("rating 4 supported only by one-character quote 'a'", p)
run("same single quote supports rating 4 for all ten", [item(c, 4, support=["I always come back to fairness"]) for c in T.CF003_CONSTRUCT_IDS])
p = list(base)
p[0] = item("T01", 3, support=["fairness"], suff="false")
run("evidence_sufficient supplied as the string 'false'", p)
p = list(base)
p[0] = item("T01", 0, support=["fairness"])
run("rating 0 justified only by a SUPPORT quote", p)

# 7 ---------------------------------------------------------------------------
section("7. manifest flags")
man = json.loads((REF / "cf003_independent_behavioral_target_manifest_v0.json").read_text())
print("  behavioral_target.participant_visible_hidden_labels =", man["behavioral_target"]["participant_visible_hidden_labels"])
