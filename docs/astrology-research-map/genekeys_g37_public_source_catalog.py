"""G37 copyright-minimal registry of Gene Keys Publishing 64 public preview pages.

Input is a PRIVATELY retained investigator-read HTML/excerpt cache; this
script never sends requests, bypasses accounts, copies full quote/body, or
assigns traits to actual people. Registry stores exact three-word headings,
the publisher's published partner links and short source-conditional anchors.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from genekeys_g35_source_crosswalk import (
    wheel_programming_partner, RAVE_GATE_ORDER, digest,
)

SOURCE_ANCHORS = {
    4: {
        "anchor": "If we have this Gene Key prominently in our profile",
        "source_class":"PROFILE_CONDITIONAL_FUTURE_DEVELOPMENT",
        "literal_scope":"if Gene Key 4 is prominent in profile; future relaxing need for answers",
        "source_nonliteral_missing":"undefined prominence threshold, time horizon, behavioral instrument",
        "analyst_measure_idea_not_a_source_rule":"need for cognitive closure measured in an untouched prospective cohort",
        "needs_actual_birth_placement_and_untouched_humans":True,
    },
    7: {
        "anchor": "The 7th Gene Key definitely has potent leadership potential",
        "source_class":"GENE_KEY_ATTRIBUTE_WITHOUT_EXPLICIT_NATAL_PLACEMENT",
        "literal_scope":"7th Gene Key influence when speaking in a group, leadership potential not necessarily holding a leader title",
        "source_nonliteral_missing":"whether any natal sphere qualifies, strength threshold, group and rater protocol",
        "analyst_measure_idea_not_a_source_rule":"blinded peer-rating of influence in a group interaction",
        "needs_actual_birth_placement_and_untouched_humans":True,
    },
    27: {
        "anchor": "If we have the 27th Gene Key, or feel mysteriously drawn to it",
        "source_class":"HAVE_OR_FEEL_DRAWN_DISJUNCTION",
        "literal_scope":"has Gene Key 27 OR feels drawn to it; links to caring/planetary healing",
        "source_nonliteral_missing":"does not state natal condition is necessary, operational caregiver metric or followup",
        "analyst_measure_idea_not_a_source_rule":"prospective caring acts, separate prior affinity to key",
        "needs_actual_birth_placement_and_untouched_humans":True,
    },
    61: {
        "anchor": "If we have this Gene Key, our life is a contemplation of death",
        "source_class":"HAVE_KEY_WITHOUT_SPHERE_OR_TIME_WINDOW",
        "literal_scope":"if having Gene Key 61, associated with contemplation of death",
        "source_nonliteral_missing":"which sphere counts, duration, age, frequency and comparison group",
        "analyst_measure_idea_not_a_source_rule":"past-month voluntary mortality reflection, independently corroborated self-report",
        "needs_actual_birth_placement_and_untouched_humans":True,
    },
}
OTHER_ILLUSTRATIVE_SOURCE_SCOPE = {
    11: "If we have the 11th Gift, or are contemplating it",
    49: "If we have the 49th Gift or are contemplating it",
}


def build(inv:dict)->dict:
    data=inv.get("results")
    if not isinstance(data,list) or len(data)!=64:
        raise ValueError("complete set of 64 official public key-page readings required")
    keys=[x["key"] for x in data]
    if keys!=list(range(1,65)):
        raise ValueError("pages are missing, duplicated or out of sequence")
    seen={}
    for x in data:
        k=x["key"]
        if x.get("status")!="OK" or x.get("url") != f"https://genekeys.com/gene-key-{k}/":
            raise ValueError("unretrieved or substituted publisher page")
        if len(x["heading"])!=3 or not all(isinstance(t,str) and t.strip()
                                               for t in x["heading"]):
            raise ValueError("incomplete three-component public key heading")
        literal=x["public_rudd_quote"]
        if "Richard Rudd" not in literal:
            raise ValueError("required short public attributed preview")
        if x["quote_sha256"]!=sha256(literal.encode()).hexdigest():
            raise ValueError("local reading cache quote-digest mismatch")
        if x["html_bytes"]<15000 or len(x["public_html_sha256"])!=64:
            raise ValueError("source HTML provenance not plausible")
        seen[k]=x
    candidates=[]
    for number,d in SOURCE_ANCHORS.items():
        if d["anchor"] not in seen[number]["public_rudd_quote"]:
            raise ValueError(f"source not containing the exact required claim anchor for {number}")
        candidates.append({
            "key":number,
            "source_url":seen[number]["url"],
            "brief_exact_anchor":d["anchor"],
            "source_page_html_sha256":seen[number]["public_html_sha256"],
            "source_preview_quote_sha256":seen[number]["quote_sha256"],
            **{k:v for k,v in d.items() if k!="anchor"},
            "frozen_behavioral_prediction_or_threshold":False,
            "publisher_did_not_state_a_predeclared_probability":True,
        })
    for number,anchor in OTHER_ILLUSTRATIVE_SOURCE_SCOPE.items():
        if anchor not in seen[number]["public_rudd_quote"]:
            raise ValueError("important contemplation-vs-Gift qualifier not present")

    rows=[]
    mismatches=[]
    for r in data:
        n=r["key"]
        expected=wheel_programming_partner(n)
        pub=r["programming_partner"]
        disagree=pub!=expected
        item={
            "key":n,
            "official_url":r["url"],
            "shadow":r["heading"][0],
            "gift":r["heading"][1],
            "siddhi":r["heading"][2],
            "page_html_sha256":r["public_html_sha256"],
            "page_quote_sha256":r["quote_sha256"],
            "published_programming_partner":pub,
            "canonical_mandala_programming_partner":expected,
            "official_link_disagrees_with_canonical_opposition":disagree,
            "short_public_preview_quote_length_chars":r["quote_length_chars"],
            "quote_has_if_or_when_heuristic":
                bool(__import__("re").search(r"\b(?:if|when|whoever)\b",
                         r["public_rudd_quote"],__import__("re").I)),
            "quote_mentions_profile_heuristic":"profile" in r["public_rudd_quote"].lower(),
            "long_public_quote_NOT_stored":True,
            "no_behavioral_prediction_derived_automatically":True,
        }
        rows.append(item)
        if disagree:
            mismatches.append({
                "key":n,"official_page":r["url"],
                "official_published_partner":pub,
                "canonical_wheel_partner":expected,
                "canonical_partner_official_page":seen[expected]["url"],
                "reciprocal_page_explicitly_names_original_key":
                    seen[expected]["programming_partner"]==n,
                "disposition":"PUBLISHER_PAGE_NAVIGATION_DISCREPANCY_NOT_AN_ALGORITHM_CORRECTION"
            })
    if {x["key"] for x in mismatches}!={6,8}:
        raise ValueError("unexpected mismatch set from independently retrieved 64 pages")
    if len(rows)!=64:
        raise ValueError("catalogue coverage incomplete")
    if not (seen[36]["programming_partner"]==6 and seen[14]["programming_partner"]==8):
        raise ValueError("independent official reciprocity check failed")
    assert len({tuple(sorted([i,wheel_programming_partner(i)]))
               for i in range(1,65)})==32
    result={
        "schema":"HUMANDESIGN_G37_OFFICIAL_64_PUBLIC_KEY_HEADINGS_PARTNERS_V1",
        "source":"64 separate public pages on genekeys.com, n=1..64",
        "as_of":"2026-10-25",
        "copyright_policy":"Only original short three-word public headings and four brief source claim anchors; no full Richard Rudd public preview paragraphs or copyrighted key essays stored in Git",
        "raw_public_page_readings_private_temporary_not_committed":True,
        "full_book_primary_chapters_read":False,
        "official_completed_profile_calculator_parity_verified":False,
        "each_quote_checked_against_original_publisher_public_page":True,
        "all_64_headings_checked":True,
        "official_published_programming_partner_links_checked":64,
        "canonical_wheel_geometry_programming_partner_pairs":32,
        "publisher_links_matching_opposite_wheel":64-len(mismatches),
        "publisher_links_disagreeing":len(mismatches),
        "site_partner_discrepancies":mismatches,
        "source_conditional_language_cases_selected_for_later_analysis":candidates,
        "other_contemplation_or_Gift_conditional_examples":[
           {"key":k,"literal_short_source_anchor":v,
            "scope":"already possessing Gift OR contemplating it; not equivalent to possessing natal key"}
           for k,v in OTHER_ILLUSTRATIVE_SOURCE_SCOPE.items()],
        "short_quote_heuristic_if_or_when_count":sum(x["quote_has_if_or_when_heuristic"]
                                                   for x in rows),
        "short_quote_heuristic_mentions_profile_count":sum(x["quote_mentions_profile_heuristic"]
                                                           for x in rows),
        "heuristic_text_flags_are_NOT_a_complete_semantic_study":True,
        "independent_natal_chart_evidence_beyond_Human_Design":0,
        "source_behavioral_trait_model_frozen":False,
        "human_predictive_validations":0,
        "production_chart_or_scoring_modified":False,
        "rows":rows
    }
    result["canonical_registry_sha256"]=digest(result)
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--private-scrape",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    raw=json.loads(args.private_scrape.read_text(encoding="utf8"))
    data=build(raw)
    args.output.write_text(json.dumps(data,indent=2,sort_keys=True,
                                      ensure_ascii=False)+"\n")
    print("G37_OFFICIAL_PAGES",data["official_published_programming_partner_links_checked"])
    print("G37_MATCHED",data["publisher_links_matching_opposite_wheel"])
    print("G37_ANOMALIES",data["site_partner_discrepancies"])
    print("G37_SOURCE_CONDITIONALS",[x["key"] for x in
          data["source_conditional_language_cases_selected_for_later_analysis"]])
    print("G37_SHA",data["canonical_registry_sha256"])
