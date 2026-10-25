"""G39 synthetic rater-score controls: not actual independent respondents."""
from __future__ import annotations

import json
from pathlib import Path

from genekeys_g39_rate_blind_packets import grade,validate_key
from genekeys_g39_blind_rating_packets import ROOT

KEY=ROOT/"GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json"
OUT=ROOT/"GENEKEYS_G39_SYNTHETIC_RATER_GRADER_RECEIPT_V1.json"

def make_mock(key:dict, *,mode:str)->list[dict]:
    """Build clearly synthetic fixtures from researcher answer key."""
    if mode not in {"perfect","all_line_1","all_unclear"}:
        raise ValueError("unknown mock fixture")
    packets=[]
    for packet in key["rater_packets"]:
        byline={line:code for code,line in
                packet["public_category_code_to_original_source_line"].items()}
        truth={x["item_code"]:x["researcher_intended_style_original_line"]
               for x in key["items"]}
        records=[]
        for code in packet["item_order"]:
            src=truth[code]
            selected=(
                byline[src] if mode=="perfect" else
                byline[1] if mode=="all_line_1" else "U"
            )
            records.append({"item_code":code,"category_code":selected,
                            "confidence":5 if mode=="perfect" else 2,
                            "facts_check":"yes",
                            "naturalness":3,
                            "perceived_pressure":2})
        packets.append({
            "schema":"G39_ANONYMOUS_OPTIONAL_BLIND_MESSAGE_RATER_V1",
            "packet_id":packet["packet_id"],
            "synthetic_messages_only":True,
            "respondent_bio_data_collected":False,
            "independent_of_respondent_birth_chart":True,
            "ratings":records
        })
    return packets


def build()->dict:
    k=validate_key(json.loads(KEY.read_text(encoding="utf8")))
    receipt={
        "schema":"G39_FULLY_SYNTHETIC_GRADER_CONTROLS_V1",
        "all_cases_constructed_from_researcher_answer_key_not_real_raters":True,
        "independent_raters_tested":0,
        "human_astrology_predicted_outcomes":0,
        "researcher_key_sha256":k["research_key_body_sha256"],
        "cases":{}
    }
    for mode in ("perfect","all_line_1","all_unclear"):
        r=grade(k,make_mock(k,mode=mode),
                all_submissions_are_SYNTHETIC_FIXTURES=True)
        receipt["cases"][mode]={
            "reviewer_packets":r["number_of_response_packets"],
            "responses":r["ratings_total"],
            "correct":r["correct_style_classifications"],
            "unknown":r["unsure_classifications"],
            "coverage_adjusted_accuracy":r["coverage_adjusted_accuracy_all_ratings"],
            "conditional_accuracy":r["conditional_accuracy_if_classified"],
            "per_source_line":r["per_researcher_intended_style"],
            "inter_rater_pairs":len(r["inter_rater_pairwise_agreement_descriptive"]),
        }
    p=receipt["cases"]["perfect"]
    a=receipt["cases"]["all_line_1"]
    u=receipt["cases"]["all_unclear"]
    if (p["correct"],p["responses"])!=(144,144):
        raise AssertionError("perfect source classifier fixture should be exactly 100%")
    if (a["correct"],a["responses"])!=(24,144):
        raise AssertionError("single-class rater should be exactly 1/6 on balanced stimuli")
    if (u["correct"],u["unknown"],u["conditional_accuracy"])!=(0,144,None):
        raise AssertionError("all unsure must not get artificial predicted matches")
    return receipt


if __name__=="__main__":
    if OUT.exists():
        raise FileExistsError("Do not overwrite original mock source fixture receipt")
    o=build()
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True,
                              ensure_ascii=False)+"\n",encoding="utf8")
    print("G39_GRADER_SYNTHETIC_CONTROLS",
          [(key,data["correct"],data["responses"])
           for key,data in o["cases"].items()])
