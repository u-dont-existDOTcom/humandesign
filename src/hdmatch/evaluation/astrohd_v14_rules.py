"""Source-grounded atomic-strength ensemble, development version 1.4.

Traditional strength clauses and the modern behavioral bridge are deliberately
separate. Debility is weaker predicted support, not observed contradiction.
No owner birth instant or continuous fitted astrology weight appears here.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Any
import numpy as np
from hdmatch.evaluation.astrohd_v13_traditions import (
    PLANETS, RULERS, EXALTATIONS, FALLS, DIURNAL, NOCTURNAL,
    sign_name, whole_sign_house_sign,
)
from hdmatch.evaluation.astrohd_v13b_native import lilly_planet_native_strength

SOURCES = {
    "lilly": {"title": "Christian Astrology", "location": "p.115 strength/debility table; planet and house significators from frozen V1.3 catalog", "url": "https://www.skyscript.co.uk/dig5.html"},
    "ptolemy": {"title": "Tetrabiblos", "location": "I.7 sect; I.17 domiciles; I.19 exaltations/depressions; I.23 proper places", "url": "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1B*.html"},
    "valens": {"title": "Anthology, Riley translation", "location": "I.1 planetary significations; II.1 sect/favorable placement (previously admitted V1.3 catalog)", "url": "https://www.skyscript.co.uk/pdf/pubs/texts/valens/riley/docs/Vettius_Valens_Riley.pdf"},
    "phaladeepika": {"title": "Phaladeepika, Subrahmanya Sastri translation", "location": "IV.1-5 strength; meanings from frozen BPHS/Phaladeepika V1.3 semantic bridge", "url": "https://www.wisdomlib.org/hinduism/book/phaladeepika-by-mantreswara-text-and-translation/d/doc1621576.html"},
}
LILLY_RULES = ("own_sign", "exaltation", "triplicity", "term", "face", "detriment", "fall", "peregrine", "house_1_10", "house_4_7_11", "house_2_5", "house_9", "house_3", "house_6_8", "house_12", "motion", "solar_visibility", "moon_phase", "benefic_conjunction", "benefic_trine", "benefic_sextile", "malefic_conjunction", "malefic_square", "malefic_opposition")
CONDITIONS = {
    "lilly": LILLY_RULES,
    "ptolemy": ("own_sign", "exaltation", "fall", "sect"),
    "valens": ("own_sign", "exaltation", "sect"),
    "phaladeepika": ("own_sign", "exaltation", "retrograde", "temporal", "directional", "kendra"),
}


def registry(consensus: dict[str, Any], supported: set[str]) -> list[dict[str, Any]]:
    bundles: dict[tuple[str, str], set[str]] = defaultdict(set)
    bridge_sources: dict[tuple[str, str], set[str]] = defaultdict(set)
    source_for = {"hellenistic_western": "valens", "lilly_traditional_western": "lilly", "parashari_jyotish": "phaladeepika"}
    for domain in consensus["domains"]:
        if domain["domain_id"] not in supported:
            continue
        for tradition in domain["traditions"]:
            source = source_for[tradition["tradition"]]
            for field, prefix in (("planets", "planet:"), ("houses", "lord:")):
                for item in tradition[field]:
                    subject = prefix + str(item["id"])
                    bundles[source, subject].add(domain["domain_id"])
                    bridge_sources[source, subject].update(item["source_ids"])
                    # Intentional cross-book composition: Ptolemy's strength
                    # clauses use already mapped western PLANET significators.
                    # This is not attributed to Ptolemy as a behavioral claim.
                    if field == "planets" and source in {"lilly", "valens"}:
                        bundles["ptolemy", subject].add(domain["domain_id"])
                        bridge_sources["ptolemy", subject].update(item["source_ids"])
    rows = []
    for (source, subject), domains in sorted(bundles.items()):
        frame = "sidereal_lahiri" if source == "phaladeepika" else "tropical"
        if subject.startswith("lord:"):
            frame += ":regiomontanus" if source == "lilly" else ":whole_sign"
        for condition in CONDITIONS[source]:
            if subject.startswith("planet:"):
                planet = subject.split(":")[1]
                if condition == "moon_phase" and planet != "moon":
                    continue
                if condition in {"motion", "retrograde"} and planet in {"sun", "moon"}:
                    continue
                if condition == "solar_visibility" and planet == "sun":
                    continue
                if condition == "sect" and planet == "mercury":
                    continue  # Mercury's phase-conditioned sect not implemented.
            rows.append({
                "rule_id": f"{source}/{subject}/{condition}",
                "source_id": source,
                "source": SOURCES[source],
                "subject": subject,
                "condition": condition,
                "lineage_key": f"{frame}/{subject}/{condition}",
                "supported_domain_ids": sorted(domains),
                "behavioral_bridge_source_ids": sorted(bridge_sources[source, subject]),
                "behavioral_bridge_id": "frozen-v13-source-only-consensus",
                "behavioral_bridge_status": "modern_crosswalk_not_verbatim_historical_prediction",
                "rule_meaning": "source strength condition for the mapped significator",
                "score_semantics": "equal signed vote: stronger +1, weaker -1, condition absent 0",
            })
    return rows


def deduplicate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = row["lineage_key"]
        if key not in result:
            result[key] = dict(row, contributing_rule_ids=[row["rule_id"]])
        else:
            result[key]["contributing_rule_ids"].append(row["rule_id"])
            result[key]["supported_domain_ids"] = sorted(set(result[key]["supported_domain_ids"]) | set(row["supported_domain_ids"]))
    return sorted(result.values(), key=lambda row: row["rule_id"])


def planet_for(snapshot: Any, source: str, subject: str) -> str:
    kind, value = subject.split(":")
    if kind == "planet":
        return value
    house = int(value)
    if source == "lilly":
        return RULERS[sign_name(snapshot.regio_cusps[house - 1])]
    asc = snapshot.sidereal_ascendant if source == "phaladeepika" else snapshot.tropical_ascendant
    return RULERS[whole_sign_house_sign(asc, house)]


def _sep(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def _sect(snapshot: Any, planet: str) -> int:
    return int((snapshot.day_chart and planet in DIURNAL) or (not snapshot.day_chart and planet in NOCTURNAL))


def conditions(snapshot: Any, source: str, planet: str) -> dict[str, int]:
    if source == "lilly":
        native = lilly_planet_native_strength(snapshot, planet)
        components = native["components"]
        values = {k: int(np.sign(components.get(k, 0))) for k in ("own_sign", "exaltation", "triplicity", "term", "face", "detriment", "fall", "peregrine", "motion")}
        house = native["house"]
        for name, houses, value in (("house_1_10", {1, 10}, 1), ("house_4_7_11", {4, 7, 11}, 1), ("house_2_5", {2, 5}, 1), ("house_9", {9}, 1), ("house_3", {3}, 1), ("house_6_8", {6, 8}, -1), ("house_12", {12}, -1)):
            values[name] = value if house in houses else 0
        lon = snapshot.tropical_longitudes
        if planet == "sun":
            values["solar_visibility"] = 0
        else:
            distance = _sep(lon[planet], lon["sun"])
            # Mutually exclusive states avoid counting combustion twice.
            values["solar_visibility"] = 1 if distance <= 17.0 / 60.0 or distance > 17.0 else -1
        values["moon_phase"] = (1 if (lon["moon"] - lon["sun"]) % 360.0 < 180.0 else -1) if planet == "moon" else 0
        for adjective, others, angles, sign in (("benefic", ("jupiter", "venus"), {"conjunction": 0, "trine": 120, "sextile": 60}, 1), ("malefic", ("saturn", "mars"), {"conjunction": 0, "square": 90, "opposition": 180}, -1)):
            for label, angle in angles.items():
                values[f"{adjective}_{label}"] = sign if any(other != planet and abs(_sep(lon[planet], lon[other]) - angle) <= 1.0 for other in others) else 0
        return values
    if source in {"ptolemy", "valens"}:
        sign = sign_name(snapshot.tropical_longitudes[planet])
        return {"own_sign": int(RULERS[sign] == planet), "exaltation": int(EXALTATIONS[planet] == sign), "fall": -int(FALLS[planet] == sign), "sect": _sect(snapshot, planet)}
    sign = sign_name(snapshot.sidereal_longitudes[planet])
    house = snapshot.sidereal_whole_houses[planet]
    directional = {"sun": 10, "mars": 10, "moon": 4, "venus": 4, "mercury": 1, "jupiter": 1, "saturn": 7}
    return {"own_sign": int(RULERS[sign] == planet), "exaltation": int(EXALTATIONS[planet] == sign), "retrograde": int(planet not in {"sun", "moon"} and snapshot.sidereal_speeds[planet] < 0), "temporal": 1 if planet == "mercury" else _sect(snapshot, planet), "directional": int(house == directional[planet]), "kendra": int(house in {1, 4, 7, 10})}


def feature_row(snapshot: Any, rows: list[dict[str, Any]]) -> np.ndarray:
    cache: dict[tuple[str, str], dict[str, int]] = {}
    result = []
    for rule in rows:
        source = rule["source_id"]
        planet = planet_for(snapshot, source, rule["subject"])
        key = (source, planet)
        if key not in cache:
            cache[key] = conditions(snapshot, source, planet)
        result.append(cache[key][rule["condition"]])
    return np.array(result, dtype=np.int8)
