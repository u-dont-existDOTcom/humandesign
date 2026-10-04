"""Source-audit arithmetic, not empirical prediction or a production chart engine.

Explicit source branches are arguments, never selected from outcomes. Caller supplies
verified ASCII name components, pronunciation masks and date/name roles. No implicit
transliteration, hyphen splitting, legal-name substitution or missing-data imputation.
See the four 20261004 author specifications for provenance and interpretive limits.
"""
from __future__ import annotations
from collections import Counter
from datetime import date
import calendar
from math import lcm
from typing import Iterable, Sequence

JORDAN = "JORDAN_ROMANCE_NAME_V1"
CAMPBELL = "CAMPBELL_YOUR_DAYS_V1"
JB = "JAVANE_BUNKER_DIVINE_TRIANGLE_V1"
CHEIRO = "CHEIRO_CHALDEAN_V2"
SYSTEMS = {JORDAN, CAMPBELL, JB, CHEIRO}
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COMPACT = {c: i % 9 + 1 for i, c in enumerate(ALPHABET)}
ORDINAL = {c: i + 1 for i, c in enumerate(ALPHABET)}
CHALDEAN = {c: i for i, group in enumerate(
    ["", "AIJQY", "BKR", "CGLS", "DMT", "EHNX", "UVW", "OZ", "FP"])
    for c in group}
MASTERS = {JORDAN: (), CAMPBELL: (11, 22), JB: (11, 22, 33, 44), CHEIRO: ()}


def digit_sum(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("Expected a nonnegative integer, not a missing input")
    return sum(map(int, str(n)))


def reduction(n: int, masters: Iterable[int] = ()) -> list[int]:
    digit_sum(n)
    stops = set(masters)
    out = [n]
    while n >= 10 and n not in stops:
        n = digit_sum(n)
        out.append(n)
    return out


def root(n: int) -> int:
    return reduction(n)[-1]


def result(n: int, system: str) -> dict:
    if system not in SYSTEMS:
        raise ValueError("Unknown author system")
    digit_sum(n)
    admitted = n
    admission_chain = [n]
    if system == JB:
        while admitted > 78:
            admitted = digit_sum(admitted)
            admission_chain.append(admitted)
    return {"raw": n, "admitted": admitted,
            "admission_chain": admission_chain,
            "chain": reduction(admitted, MASTERS[system]),
            "value": reduction(admitted, MASTERS[system])[-1],
            "root": root(admitted)}


def tokens(parts: Sequence[str]) -> list[str]:
    if isinstance(parts, str) or not parts:
        raise ValueError("Supply an explicit nonempty list of name components")
    out = []
    for part in parts:
        if not isinstance(part, str) or not part or any(c not in ALPHABET + ALPHABET.lower() for c in part):
            raise ValueError("Resolve punctuation, initials, scripts and name roles explicitly")
        out.append(part.upper())
    return out


def name_number(parts: Sequence[str], system: str, masks: Sequence[str] | None = None,
                selection: str = "all", campbell_letters: str | None = None,
                component_masters: str | None = None) -> dict:
    """masks contain V/C for every letter. Jordan rejects vowel Y/W masks.

    Campbell literal/compact K/V and retain/root intermediate-master branches are
    explicit. Empty selected sums remain zero markers, not interpreted personalities.
    """
    parts = tokens(parts)
    if system not in SYSTEMS or selection not in {"all", "vowels", "consonants"}:
        raise ValueError("Invalid system or selection")
    if system == CHEIRO and selection != "all":
        raise ValueError("Cheiro has no vowel/consonant core in the inherited specification")
    if system == CAMPBELL and campbell_letters is None and any(c in "KV" for p in parts for c in p):
        raise ValueError("Choose Campbell literal or compact K/V branch explicitly")
    campbell_letters = campbell_letters or "compact"
    if campbell_letters not in {"compact", "literal"} or component_masters not in {None, "retain", "root"}:
        raise ValueError("Unknown source branch")
    if masks is None:
        if selection != "all" and system != JORDAN:
            raise ValueError("Pronunciation-dependent author requires explicit vowel masks")
        masks = ["".join("V" if c in "AEIOU" else "C" for c in p) for p in parts]
    if len(masks) != len(parts) or any(len(p) != len(m) or set(m) - {"V", "C"} for p, m in zip(parts, masks)):
        raise ValueError("One V/C mask per component is required")
    if system == JORDAN and any(m != "".join("V" if c in "AEIOU" else "C" for c in p)
                               for p, m in zip(parts, masks)):
        raise ValueError("Jordan's only vowels are AEIOU; Y/W have no exception")
    table = CHALDEAN if system == CHEIRO else COMPACT.copy()
    if system == CAMPBELL and campbell_letters == "literal":
        table.update(K=11, V=22)
    choose = lambda kind: selection == "all" or (kind == "V") == (selection == "vowels")
    raw_parts = [sum(table[c] for c, k in zip(p, mask) if choose(k)) for p, mask in zip(parts, masks)]
    if system == CAMPBELL and component_masters is None and any(reduction(n, (11, 22))[-1] != root(n) for n in raw_parts):
        raise ValueError("Choose Campbell intermediate-master branch explicitly")
    component_masters = component_masters or "retain"
    if system == JB:
        n = sum(raw_parts)
        addends = raw_parts
    else:
        stops = MASTERS[system] if component_masters == "retain" else ()
        addends = [reduction(n, stops)[-1] for n in raw_parts]
        n = sum(addends)
    return {"system": system, "parts": parts, "masks": list(masks), "selection": selection,
            "component_raw": raw_parts, "component_addends": addends,
            "branch_choices": {"campbell_letters": campbell_letters, "component_masters": component_masters},
            "result": result(n, system), "interpretation_available": n != 0}


def date_number(born: date, system: str, component_masters: str | None = None) -> dict:
    if not isinstance(born, date):
        raise ValueError("A verified Gregorian date is required")
    if system == JB:
        return result(born.month + born.day + digit_sum(born.year), JB)
    if system == CHEIRO:
        return {"birth_day": result(born.day, CHEIRO), "year": result(born.year, CHEIRO),
                "period": cheiro_period(born.month, born.day)}
    if system == CAMPBELL and component_masters is None and any(reduction(n, (11, 22))[-1] != root(n) for n in (born.month, born.day, born.year)):
        raise ValueError("Choose Campbell date intermediate-master branch explicitly")
    component_masters = component_masters or "retain"
    if system not in {CAMPBELL, JORDAN} or component_masters not in {"retain", "root"}:
        raise ValueError("Specify the author's date-component branch")
    stops = MASTERS[system] if component_masters == "retain" else ()
    addends = [reduction(n, stops)[-1] for n in (born.month, born.day, born.year)]
    return {"addends": addends, "result": result(sum(addends), system)}


def calendar_number(month: int, day: int, year: int, system: str,
                    component_masters: str = "retain") -> dict:
    """Campbell/Jordan PY or Universal Day using explicit month/day/year inputs.
    Birth-year input is replaced with the target year for a Personal Year.
    February29 in a nonleap target year remains permissible as a birth component.
    """
    if not (1 <= month <= 12 and 1 <= day <= 31) or system not in {CAMPBELL, JORDAN}:
        raise ValueError("Invalid components or calendar-cycle system")
    stops = MASTERS[system] if component_masters == "retain" else ()
    return result(sum(reduction(n, stops)[-1] for n in (month, day, year)), system)


def pinnacles(month: int, day: int, year: int, system: str,
              component_masters: str = "retain") -> list[dict]:
    if system not in {CAMPBELL, JORDAN}:
        raise ValueError("This author does not use these Pinnacles")
    stops = MASTERS[system] if component_masters == "retain" else ()
    m, d, y = (reduction(n, stops)[-1] for n in (month, day, year))
    p1, p2 = result(m + d, system), result(d + y, system)
    a, b = (p1["value"], p2["value"]) if component_masters == "retain" else (p1["root"], p2["root"])
    return [p1, p2, result(a + b, system), result(m + y, system)]


def pinnacle_marks(life_number: int, system: str, master_duration: str | None = None) -> list[int]:
    if system not in {CAMPBELL, JORDAN}:
        raise ValueError("No conventional Pinnacle timing for this author")
    if system == CAMPBELL and life_number in (11, 22) and master_duration not in {"literal", "root"}:
        raise ValueError("Campbell master-Life-Path duration is unresolved; select a named branch")
    v = life_number if system == CAMPBELL and master_duration == "literal" else root(life_number)
    b = 36 - v
    return [b, b + 9, b + 18]


def challenges(month: int, day: int, year: int, system: str) -> list[int]:
    if system not in {CAMPBELL, JORDAN}:
        raise ValueError("No conventional subtraction Challenges for this author")
    m, d, y = map(root, (month, day, year))
    a, b = abs(m - d), abs(d - y)
    out = [a, b, abs(a - b)]
    return out + [abs(m - y)] if system == JORDAN else out


def jordan_day(month: int, day: int, year_or_personal_year: int) -> dict:
    return {"day": calendar_number(month, day, year_or_personal_year, JORDAN),
            "pinnacles": pinnacles(month, day, year_or_personal_year, JORDAN),
            "challenges": challenges(month, day, year_or_personal_year, JORDAN),
            "clock_blocks": [[0, 8], [8, 16], [16, 24]], "fourth_is_background": True}


def histogram(parts: Sequence[str]) -> dict[int, int]:
    counts = Counter(COMPACT[c] for p in tokens(parts) for c in p)
    return {n: counts[n] for n in range(1, 10)}


def campbell_ruling_passion(parts: Sequence[str]) -> dict:
    counts = histogram(parts)
    adjusted = dict(counts)
    adjusted[5] -= 2
    best = max(adjusted.values())
    return {"counts": counts, "adjusted": adjusted,
            "formula_winners": [n for n in adjusted if adjusted[n] == best]}


def planes(parts: Sequence[str], system: str) -> dict:
    letters = "".join(tokens(parts))
    if system == JORDAN:
        groups = {"physical": "DMVENW", "mental": "AJSHQZ", "emotional": "BKTCLUFOX", "intuitive": "GPYIR"}
        counts = {k: sum(c in group for c in letters) for k, group in groups.items()}
        return {"counts": counts, "totals": {k: root(v) for k, v in counts.items()}}
    if system != CAMPBELL:
        raise ValueError("No imported Planes model")
    cells = {"inspired": {"mental": "A", "physical": "E", "emotional": "ORIZ", "intuitive": "K"},
             "dual": {"mental": "HJNP", "physical": "W", "emotional": "BSTX", "intuitive": "FQUY"},
             "balanced": {"mental": "GL", "physical": "DM", "emotional": "", "intuitive": "CV"}}
    values = {k: {p: sum(c in group for c in letters) for p, group in row.items()} for k, row in cells.items()}
    return {"cells": values, "planes": {p: sum(row[p] for row in values.values()) for p in cells["inspired"]},
            "classes": {k: sum(row.values()) for k, row in values.items()}}


def tape(parts: Sequence[str], completed_age: int, system: str, indexing: str = "birth_start") -> dict:
    if system not in {CAMPBELL, JORDAN} or completed_age < 0:
        raise ValueError("Unsupported tape or age")
    if indexing not in {"birth_start", "display_age_minus_one"}:
        raise ValueError("Unknown indexing branch")
    t = completed_age - (indexing == "display_age_minus_one")
    parts = tokens(parts)
    if t < 0:
        return {"active": None, "reason": "Br_column_in_display_branch"}
    active, periods = [], []
    for p in parts:
        duration = sum(COMPACT[c] for c in p)
        periods.append(duration)
        u = t % duration
        for c in p:
            if u < COMPACT[c]:
                active.append(c)
                break
            u -= COMPACT[c]
    return {"active": active, "periods": periods, "joint_repeat": lcm(*periods),
            "essence": result(sum(COMPACT[c] for c in active), system), "indexing": indexing}


def jordan_race_consciousness(age: int) -> int:
    if age < 0:
        raise ValueError("Age cannot be negative")
    return root(root(age) + root(age + 1))


def campbell_cycle_candidates(born: date, target_age: int) -> dict:
    if target_age not in (28, 56):
        raise ValueError("Campbell's approximate target ages are 28 and 56")
    target = born.year + target_age
    years = [y for y in range(target - 9, target + 10)
             if calendar_number(born.month, born.day, y, CAMPBELL)["root"] == 1]
    return {"target_age": target_age, "preceding_or_same": max(y for y in years if y <= target),
            "following_or_same": min(y for y in years if y >= target),
            "nearest_calendar_year_branch": min(years, key=lambda y: (abs(y - target), y)),
            "exact_lunar_return": None, "exact_in_year_boundary": None}


PERIODS = [("Capricorn", (12, 21)), ("Aquarius", (1, 21)), ("Pisces", (2, 19)),
           ("Aries", (3, 21)), ("Taurus", (4, 20)), ("Gemini", (5, 21)),
           ("Cancer", (6, 21)), ("Leo", (7, 21)), ("Virgo", (8, 21)),
           ("Libra", (9, 21)), ("Scorpio", (10, 21)), ("Sagittarius", (11, 21))]
ELEMENT = {s: e for e, ss in {"Earth": ["Capricorn", "Taurus", "Virgo"],
          "Air": ["Aquarius", "Gemini", "Libra"], "Water": ["Pisces", "Cancer", "Scorpio"],
          "Fire": ["Aries", "Leo", "Sagittarius"]}.items() for s in ss}
OPPOSITE = {a: b for a, b in zip([s for s, _ in PERIODS], [s for s, _ in PERIODS][6:] + [s for s, _ in PERIODS][:6])}


def cheiro_period(month: int, day: int) -> str:
    date(2000, month, day)
    ordered = sorted(PERIODS, key=lambda x: x[1])
    return next((s for s, start in reversed(ordered) if (month, day) >= start), "Capricorn")


def cheiro_affinity(m1: int, d1: int, m2: int, d2: int) -> dict:
    s1, s2 = cheiro_period(m1, d1), cheiro_period(m2, d2)
    a, b = root(d1), root(d2)
    mental = a == b or (a in {1, 2, 4, 7} and b in {1, 2, 4, 7})
    same, central = ELEMENT[s1] == ELEMENT[s2], OPPOSITE[s1] == s2
    return {"periods": [s1, s2], "mental_WWYB": mental, "same_element": same,
            "central_opposite": central, "joint": mental and (same or central),
            "fire_water_conflict": {ELEMENT[s1], ELEMENT[s2]} == {"Fire", "Water"},
            "cusp_weights": None, "monthly_prose_exceptions_in_spec": True}


def periodicity(seed: int, steps: int) -> list[int]:
    if seed <= 0 or steps < 0:
        raise ValueError("Positive year seed and nonnegative steps required")
    out = [seed]
    for _ in range(steps):
        out.append(out[-1] + digit_sum(out[-1]))
    return out


def jb_year(born: date, last_birthday_year: int) -> dict:
    if last_birthday_year < born.year:
        raise ValueError("Target precedes birth")
    return result(born.month + born.day + digit_sum(last_birthday_year), JB)


def jb_periods(born: date, last_birthday_year: int, life_compound: int, soul_compound: int) -> list[dict]:
    age = last_birthday_year - born.year
    if age < 0:
        raise ValueError("Target precedes birth")
    return [result(digit_sum(last_birthday_year + n), JB) for n in (age, life_compound, soul_compound)]


def jb_month(personal_year_compound: int, month: int) -> dict:
    if not 1 <= month <= 12:
        raise ValueError("Month outside 1..12")
    return result(personal_year_compound + month, JB)


def jb_power(path_compound: int, life_compound: int) -> dict:
    return result(path_compound + life_compound, JB)


def jb_missing(parts: Sequence[str], personal_and_power: Sequence[int], actual_use_names: Sequence[int] = ()) -> dict:
    initial = [n for n, count in histogram(parts).items() if count == 0]
    supplied = {root(n) for n in list(personal_and_power) + list(actual_use_names)}
    return {"initial_missing": initial, "remaining_missing": [n for n in initial if n not in supplied]}


def jb_triangle(given_names: Sequence[str], born: date, continued_alert_youth: bool = False) -> dict:
    """Given names ONLY. Caller must exclude surname; no outcome-based role choice.
    Alert continuation after81 is the specifically illustrated 81..144 youth square.
    """
    parts = tokens(given_names)
    sequence = "".join(parts)
    offset, count, span, base_age = (9, 3, 21, 81) if continued_alert_youth else (0, 9, 9, 0)
    sides = [born.month, born.day, digit_sum(born.year)]
    ll = date_number(born, JB)
    letters = [sequence[(offset + i) % len(sequence)] for i in range(count)]
    sq = [sum(ORDINAL[c] for c in letters[j:j + 3]) + sides[j // 3] for j in range(0, count, 3)]
    lines = []
    for i, c in enumerate(letters):
        a, b, side, square = base_age + i * span, base_age + (i + 1) * span, sides[i // 3], sq[i // 3]
        major = []
        for label, n in [("square", square), ("birth_side", side), ("life_lesson", ll["admitted"])]:
            for age in (a + root(n), b - root(n)):
                major.append({"age": age, "layer": label, "number": result(n, JB)})
        young, old = sorted((a + root(ORDINAL[c]), b - root(ORDINAL[c])))
        minor = [{"age": young, "number": result(ORDINAL[c] + square, JB)},
                 {"age": old, "number": result(ORDINAL[c] + side, JB)}]
        pos = (offset + i + 1) % len(sequence)
        ends = {sum(len(p) for p in parts[:j]) % len(sequence) for j in range(1, len(parts) + 1)}
        lines.append({"line": ["AB", "BC", "CD", "DE", "EF", "FG", "GH", "HI", "IA"][i],
                      "interval": [a, b], "letter": c, "ordinal": ORDINAL[c], "name_end_X": pos in ends,
                      "major": major, "minor": minor})
    return {"life_lesson": ll, "sides": sides, "squares": [result(n, JB) for n in sq],
            "lines": lines, "entry_count": sum(len(x["major"]) + len(x["minor"]) for x in lines)}


def jordan_balance_intervals(values: dict[str, int]) -> list[dict]:
    if set(values) != {"heart", "destiny", "birth_force", "reality"}:
        raise ValueError("Four labelled Jordan major positions are required")
    items = list(values.items())
    out = []
    for i, (a, v) in enumerate(items):
        for b, w in items[i + 1:]:
            gap = abs(root(v) - root(w))
            category = "equality_qualified" if gap == 0 else "easy" if gap in (1, 2, 4) else "strain"
            out.append({"positions": [a, b], "difference": gap, "category": category})
    return out
