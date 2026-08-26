#!/usr/bin/env python3
"""Audit the public Astro-Databank C-sample for pair-specific quality labels.

This is Track-Q data sufficiency work, not a compatibility model. The script
uses only pair-specific relationship notes and person-level relationship
categories whose catnotes explicitly name the linked partner. It writes only
aggregate counts; no identities or raw research_data notes are committed.
"""
from __future__ import annotations

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "adb_csample_pair_quality_audit_v1.json"
URL = "https://www.astro.com/adbexport/c_sample.xml"

ROMANTIC_REL_IDS = {843: "spouse", 858: "lover", 859: "spousal_equivalent"}
HIGH_RR = {"AA", "A"}
DOB_RE = re.compile(r"born:\s*([+-]?\d{1,4})/(\d{1,2})/(\d{1,2})([jg]?)", re.I)
PARTNER_RE = re.compile(r"\bwith\s+(.+?)(?:,\s*born:|$)", re.I)

# Public ADB relationship-quality category IDs already declared in the project.
# We use the IDs as data labels, but only when catnotes explicitly name the
# linked partner. No unlabeled category is assigned to a pair by inference.
QUALITY_CATEGORIES = {
    183: ("positive_quality",),          # Marriage - Compatible
    186: ("positive_quality",),          # Marriage - Very happy
    986: ("negative_burden", "bitter_divorce"),
    987: ("friendly_divorce",),
    193: ("long_duration",),
    194: ("short_duration",),
    192: ("negative_burden",),          # chronic misery
    973: ("negative_burden",),          # distant
    185: ("negative_burden", "severe_negative_burden"),
    972: ("negative_burden",),          # extramarital affairs
    975: ("sexual_chemistry",),
}

# Relationship relnotes are pair-specific by construction. To avoid inventing
# a broad sentiment model after seeing the data, only these predeclared ADB
# vocabulary phrases are recognized.
RELNOTE_PATTERNS = {
    "positive_quality": ("compatible", "very happy"),
    "bitter_divorce": ("bitter",),
    "friendly_divorce": ("friendly",),
    "negative_burden": (
        "bitter", "chronic misery", "distant", "domestic violence",
        "extramarital affair", "extramarital affairs",
    ),
    "severe_negative_burden": ("domestic violence",),
    "sexual_chemistry": ("sexual chemistry",),
}


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").casefold()).strip()


def name_tokens(name: str) -> set[str]:
    stop = {
        "relationship", "spouse", "lover", "with", "born", "family",
        "associates", "equivalent",
    }
    return {t for t in norm(name).split() if len(t) >= 4 and t not in stop}


def parse_partner_stub(text: str) -> dict | None:
    md = DOB_RE.search(text or "")
    if not md:
        return None
    mn = PARTNER_RE.search(text or "")
    name = mn.group(1).strip() if mn else ""
    return {
        "name": name,
        "tokens": name_tokens(name),
        "year": int(md.group(1)),
        "month": int(md.group(2)),
        "day": int(md.group(3)),
        "calendar": "julian" if md.group(4).lower() == "j" else "gregorian",
    }


def note_labels(text: str | None) -> set[str]:
    n = norm(text)
    labels: set[str] = set()
    for label, phrases in RELNOTE_PATTERNS.items():
        for phrase in phrases:
            if norm(phrase) in n:
                labels.add(label)
                break
    return labels


def note_mentions_tokens(text: str | None, tokens: set[str]) -> bool:
    words = set(norm(text).split())
    return bool(tokens and any(t in words for t in tokens))


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "humandesign-pair-quality-audit/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        raw = response.read()
    root = ET.fromstring(raw)

    entries: dict[int, dict] = {}
    observed_quality_cat_counts = Counter()
    for e in root.findall("adb_entry"):
        aid = int(e.attrib["adb_id"])
        pub = e.find("public_data")
        if pub is None:
            continue
        name = (pub.findtext("name") or "").strip()
        rr = (pub.findtext("roddenrating") or "").strip()
        bt = pub.find("./bdata/sbtime")
        timed = bool(bt is not None and bt.attrib.get("jd_ut") and (bt.text or "").strip())

        rels = []
        cats = []
        research = e.find("research_data")
        if research is not None:
            rp = research.find("relationships")
            if rp is not None:
                for rel in rp.findall("relationship"):
                    try:
                        rid = int(rel.attrib.get("rel_id", "0"))
                        other = int(rel.attrib.get("rel_adb_id", "0"))
                    except ValueError:
                        continue
                    if rid not in ROMANTIC_REL_IDS:
                        continue
                    text = (rel.text or "").strip()
                    rels.append({
                        "rel_id": rid,
                        "other": other,
                        "text": text,
                        "relnotes": rel.attrib.get("relnotes", ""),
                        "stub": parse_partner_stub(text),
                    })
            cp = research.find("categories")
            if cp is not None:
                for cat in cp.findall("category"):
                    try:
                        cid = int(cat.attrib.get("cat_id", "0"))
                    except ValueError:
                        continue
                    if cid in QUALITY_CATEGORIES:
                        observed_quality_cat_counts[cid] += 1
                        cats.append({
                            "cat_id": cid,
                            "catnotes": cat.attrib.get("catnotes", ""),
                        })
        entries[aid] = {
            "id": aid,
            "name": name,
            "tokens": name_tokens(name),
            "rr": rr,
            "timed": timed,
            "rels": rels,
            "cats": cats,
        }

    # Aggregate directional evidence onto unordered ADB pair keys. External
    # partner IDs are still stable rel_adb_id values even though their records
    # are absent from the C-sample.
    pairs: dict[tuple[int, int], dict] = {}
    directed_romantic = 0
    directed_with_nonempty_relnote = 0
    directed_with_recognized_relnote = 0
    strict_category_attributions = 0
    strict_category_attributions_by_id = Counter()
    relnote_label_attributions = Counter()

    for aid, source in entries.items():
        for rel in source["rels"]:
            directed_romantic += 1
            other = rel["other"]
            key = tuple(sorted((aid, other)))
            target = entries.get(other)
            if target is not None:
                ptokens = target["tokens"]
                internal = True
                both_timed = source["timed"] and target["timed"]
                both_high_rr_timed = (
                    source["rr"] in HIGH_RR and target["rr"] in HIGH_RR and both_timed
                )
                partner_dob_known = True
            else:
                stub = rel.get("stub")
                ptokens = stub["tokens"] if stub else set()
                internal = False
                both_timed = False
                both_high_rr_timed = False
                partner_dob_known = bool(stub and stub["calendar"] == "gregorian")

            rec = pairs.setdefault(key, {
                "internal": internal,
                "both_timed": both_timed,
                "both_high_rr_timed": both_high_rr_timed,
                "high_rr_timed_focal_with_partner_dob": False,
                "labels": set(),
                "sources": set(),
            })
            # A pair might first be created from one direction; update invariant
            # properties when the reciprocal internal edge arrives.
            rec["internal"] = rec["internal"] or internal
            rec["both_timed"] = rec["both_timed"] or both_timed
            rec["both_high_rr_timed"] = rec["both_high_rr_timed"] or both_high_rr_timed
            if source["rr"] in HIGH_RR and source["timed"] and partner_dob_known:
                rec["high_rr_timed_focal_with_partner_dob"] = True

            relnotes = rel.get("relnotes", "")
            if norm(relnotes):
                directed_with_nonempty_relnote += 1
                labs = note_labels(relnotes)
                if labs:
                    directed_with_recognized_relnote += 1
                    rec["labels"].update(labs)
                    rec["sources"].add("relationship_relnote")
                    for lab in labs:
                        relnote_label_attributions[lab] += 1

            # Person-level category only becomes pair-specific if its catnotes
            # explicitly mention this relationship's partner by >=4-char token.
            for cat in source["cats"]:
                if not note_mentions_tokens(cat["catnotes"], ptokens):
                    continue
                strict_category_attributions += 1
                strict_category_attributions_by_id[cat["cat_id"]] += 1
                rec["labels"].update(QUALITY_CATEGORIES[cat["cat_id"]])
                rec["sources"].add("strict_partner_named_category")

    usable = {k: r for k, r in pairs.items() if r["labels"]}

    def count_pairs(predicate) -> int:
        return sum(1 for r in usable.values() if predicate(r))

    label_pair_counts = Counter()
    exact_label_pair_counts = Counter()
    external_dateonly_label_pair_counts = Counter()
    for rec in usable.values():
        for lab in rec["labels"]:
            label_pair_counts[lab] += 1
            if rec["both_high_rr_timed"]:
                exact_label_pair_counts[lab] += 1
            if (not rec["internal"]) and rec["high_rr_timed_focal_with_partner_dob"]:
                external_dateonly_label_pair_counts[lab] += 1

    positive = {k for k, r in usable.items() if "positive_quality" in r["labels"]}
    adverse = {k for k, r in usable.items() if "negative_burden" in r["labels"]}
    mixed = positive & adverse
    exact_positive = {
        k for k in positive if usable[k]["both_high_rr_timed"]
    }
    exact_adverse = {
        k for k in adverse if usable[k]["both_high_rr_timed"]
    }
    ext_positive = {
        k for k in positive
        if (not usable[k]["internal"]) and usable[k]["high_rr_timed_focal_with_partner_dob"]
    }
    ext_adverse = {
        k for k in adverse
        if (not usable[k]["internal"]) and usable[k]["high_rr_timed_focal_with_partner_dob"]
    }

    summary = {
        "status": "data_sufficiency_audit_only",
        "source": URL,
        "raw_bytes": len(raw),
        "entry_count": len(entries),
        "linkage_rules": {
            "relationship_relnote": "pair-specific edge; only predeclared exact ADB quality vocabulary recognized",
            "person_category": "accepted only when catnotes explicitly contain >=4-char token from linked partner name",
            "forbidden_inference": "no unique-spouse or biography-based assignment of an unlabeled category to a pair",
        },
        "quality_category_ids": {str(k): list(v) for k, v in QUALITY_CATEGORIES.items()},
        "observed_quality_category_occurrences_person_level": {
            str(k): observed_quality_cat_counts[k] for k in sorted(QUALITY_CATEGORIES)
        },
        "relationship_edges": {
            "directed_romantic": directed_romantic,
            "directed_with_nonempty_relnote": directed_with_nonempty_relnote,
            "directed_with_recognized_quality_relnote": directed_with_recognized_relnote,
            "recognized_relnote_label_attributions": dict(sorted(relnote_label_attributions.items())),
        },
        "strict_partner_named_categories": {
            "attribution_count": strict_category_attributions,
            "by_category_id": {str(k): v for k, v in sorted(strict_category_attributions_by_id.items())},
        },
        "pair_counts": {
            "all_unique_romantic_pairs_seen": len(pairs),
            "pairs_with_any_usable_quality_label": len(usable),
            "exact_A_AA_both_timed_pairs_with_any_quality_label": count_pairs(lambda r: r["both_high_rr_timed"]),
            "external_highRR_timed_focal_dateonly_partner_pairs_with_any_quality_label": count_pairs(
                lambda r: (not r["internal"]) and r["high_rr_timed_focal_with_partner_dob"]
            ),
            "positive_quality_pairs": len(positive),
            "negative_burden_pairs": len(adverse),
            "positive_and_negative_mixed_pairs": len(mixed),
            "exact_A_AA_positive_quality_pairs": len(exact_positive),
            "exact_A_AA_negative_burden_pairs": len(exact_adverse),
            "external_dateonly_positive_quality_pairs": len(ext_positive),
            "external_dateonly_negative_burden_pairs": len(ext_adverse),
        },
        "pair_label_counts_all": dict(sorted(label_pair_counts.items())),
        "pair_label_counts_exact_A_AA": dict(sorted(exact_label_pair_counts.items())),
        "pair_label_counts_external_dateonly": dict(sorted(external_dateonly_label_pair_counts.items())),
        "model_readiness": {
            "exploratory_binary_quality_minimum_per_class": 25,
            "exact_binary_quality_ready": len(exact_positive) >= 25 and len(exact_adverse) >= 25,
            "dateonly_binary_quality_ready": len(ext_positive) >= 25 and len(ext_adverse) >= 25,
            "note": "threshold is an engineering minimum, not a power calculation",
        },
        "limitations": [
            "ADB editorial quality labels are observational and heterogeneous, not standardized partner self-report scales.",
            "Positive and negative dimensions are not forced into one compatibility scalar.",
            "A pair may legitimately carry both positive and adverse labels across time.",
            "No raw research_data notes, identities, or relationship records are written to this result.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
