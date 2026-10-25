"""Reproducible objective-wording audit for G38/G39 communication stimuli.

Mechanical checks can diagnose direct lexical cues and major length variation.
They cannot establish an independently perceived communication construct.
"""
from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re

from genekeys_g39_blind_rating_packets import ROOT,source_stimuli,digest

BANK=ROOT/"GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json"
SOURCE=ROOT/"GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json"
OUT=ROOT/"GENEKEYS_G39_STIMULUS_WORDING_CONFOUND_PREFLIGHT_V1.json"

def build()->dict:
    rows,terms=source_stimuli()
    bank=json.loads(BANK.read_text(encoding="utf8"))
    out=[]
    grouped=defaultdict(list)
    facts_by_scenario={i["id"]:i["facts"] for i in bank["scenarios"]}
    # Literal cue checks are NOT model-generated semantic evaluations.
    regexes={
       1:r"\b(?:full information|heartfelt directness)\b",
       2:r"\b(?:high frequency|no agenda)\b",
       3:r"\b(?:no pressure)\b",
       4:r"\b(?:integrity|honesty|softness|romance)\b",
       5:r"\b(?:practical)\b",
       6:r"\b(?:patience)\b",
    }
    for r in rows:
        line=r["source_line"];message=r["message"]
        facts=facts_by_scenario[r["scenario"]]
        all_present=all(message.count(f)==1 for f in facts)
        original_short_label=terms[line-1]
        source_exact_cue=bool(re.search(regexes[line],message,re.I))
        others=[i for i in range(1,7)
                if i!=line and bool(re.search(regexes[i],message,re.I))]
        if not all_present:
            raise ValueError("factual core missing in one source style")
        grouped[line].append(r["word_count"])
        out.append({
            "item_code":r["item_code"],
            "scenario":r["scenario"],
            "source_style":line,
            "word_count":r["word_count"],
            "contains_all_three_scenario_facts_exactly_once":all_present,
            "literal_source_keyword_or_phrase_cue_present":source_exact_cue,
            "other_category_keyword_cues_present":others,
            "researcher_wording_not_full_Rudd_text":True,
        })
    bystyle={}
    for line in range(1,7):
        selections=[x for x in out if x["source_style"]==line]
        lens=grouped[line]
        bystyle[str(line)]={
           "words_by_scenario":lens,
           "average_words":sum(lens)/len(lens),
           "min_words":min(lens),
           "max_words":max(lens),
           "direct_category_label_cue_instances":
               sum(x["literal_source_keyword_or_phrase_cue_present"] for x in selections),
           "contains_all_stated_facts":all(x["contains_all_three_scenario_facts_exactly_once"]
                                           for x in selections),
        }
    body={
        "schema":"HUMANDESIGN_G39_OBJECTIVE_STIMULUS_WORDING_PREFLIGHT_V1",
        "original_G38_source_bank_sha256":sha256(BANK.read_bytes()).hexdigest(),
        "source_six_line_short_headings_sha256":sha256(SOURCE.read_bytes()).hexdigest(),
        "preflight_is_mechanical_not_an_independent_human_rating":True,
        "new_rater_packet_count":6,
        "unique_messages":len(rows),
        "all_three_core_event_facts_in_every_message":all(
            x["contains_all_three_scenario_facts_exactly_once"] for x in out),
        "same_scenario_core_facts_across_style_variants":True,
        "style_3_no_pressure_directly_echoes_official_category":True,
        "style_5_practical_directly_echoes_official_category":True,
        "source_phrase_keyword_cue_can_inflate_easy_category_classification":True,
        "word_count_factual_realism_and_emotional_intent_still_need_independent_review":True,
        "per_style":bystyle,
        "item_checks":out,
        "zero_real_rater_responses_or_person_predictions":True,
    }
    body["canonical_preflight_sha256"]=digest(body)
    return body


if __name__=="__main__":
    x=build()
    if OUT.exists():raise FileExistsError("Do not overwrite accepted source preflight")
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print("G39_WORDING_CONFOUND_PREFLIGHT",len(x["item_checks"]),"items",
          [(k,v["average_words"],v["direct_category_label_cue_instances"])
           for k,v in x["per_style"].items()])
