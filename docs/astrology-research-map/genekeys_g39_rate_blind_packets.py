"""Offline grader for anonymous Gene Keys G39 manipulation-only rating packets.

Only checks whether a human/fictional reviewer recognizes the intended
researcher-authored communication-style proxy. It cannot establish Gene
Keys behavior, natal predictions, genetics, or independent rater identity.
Do NOT commit any real voluntary rater response files or send to a server.

Usage:
 python genekeys_g39_rate_blind_packets.py --key <research_only.json> \
    --ratings <r01.json> [other separate packets] --out /private/report.json
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import math

from genekeys_g39_blind_rating_packets import (
    N_ITEMS,N_RATERS, ROOT, digest,
)

SCHEMA="G39_ANONYMOUS_OPTIONAL_BLIND_MESSAGE_RATER_V1"
KEY_SCHEMA="G39_RESEARCHER_ONLY_SOURCE_STIMULUS_KEY_V1"
REPORT_SCHEMA="G39_MANIPULATION_CHECK_ONLY_DESCRIPTIVE_V1"


def load(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf8"))


def validate_key(key:dict, *, check_html:bool=True)->dict:
    if key.get("schema") != KEY_SCHEMA or key.get("synthetic_stimuli_only") is not True:
        raise ValueError("incorrect researcher key")
    checksum=key.get("research_key_body_sha256")
    material={k:v for k,v in key.items() if k!="research_key_body_sha256"}
    if digest(material)!=checksum:
        raise ValueError("research key was modified")
    if key.get("no_genuine_independent_rater_answers_collected") is not True:
        raise ValueError("key does not describe an unfielded rater packet")
    if len(key.get("rater_packets",[]))!=N_RATERS:
        raise ValueError("expected 6 rater packets")
    items=key.get("items",[])
    if len(items)!=N_ITEMS or len({x["item_code"] for x in items})!=N_ITEMS:
        raise ValueError("expected 24 unique stimuli")
    seen=set()
    for p in key["rater_packets"]:
        rid=p["packet_id"]
        if rid in seen or rid not in {f"R{i:02d}" for i in range(1,7)}:
            raise ValueError("duplicate or unknown rater ID")
        seen.add(rid)
        if set(p["item_order"])!={x["item_code"] for x in items}:
            raise ValueError("rater packet has missing stimulus IDs")
        cats=p["public_category_code_to_original_source_line"]
        if len(cats)!=6 or set(cats.values())!=set(range(1,7)):
            raise ValueError("rater category map must be one-to-one")
        if check_html:
            html_path=ROOT/"GENEKEYS_G39_ANONYMOUS_RATER_HTML"/p["rater_html_basename"]
            if not html_path.is_file():
                raise ValueError("missing associated blinded HTML packet")
            from genekeys_g39_blind_rating_packets import sha_bytes
            if sha_bytes(html_path.read_bytes())!=p["rater_html_sha256"]:
                raise ValueError("HTML packet changed from the frozen research key")
            contents=html_path.read_text(encoding="utf8")
            for item in items:
                if item["item_code"] not in contents:
                    raise ValueError("blind packet item omitted")
            for leak in ("researcher_intended_style_original_line",
                         "source_line","Gene Keys","Human Design"):
                if leak in contents:
                    raise ValueError("rater-visible source answer key leaked")
    return key


def validate_submission(key:dict, rating:dict)->dict:
    if rating.get("schema")!=SCHEMA:
        raise ValueError("unsupported reviewer response format")
    if rating.get("synthetic_messages_only") is not True:
        raise ValueError("only ratings of synthetic fictional messages accepted")
    if rating.get("respondent_bio_data_collected") is not False:
        raise ValueError("field wrongly implies personal bio collection")
    if rating.get("independent_of_respondent_birth_chart") is not True:
        raise ValueError("cannot conflate style review with a chart study")
    rid=rating.get("packet_id")
    packet=next((p for p in key["rater_packets"] if p["packet_id"]==rid),None)
    if packet is None:
        raise ValueError("unexpected reviewer packet")
    rows=rating.get("ratings")
    if not isinstance(rows,list) or len(rows)!=N_ITEMS:
        raise ValueError("a complete response packet requires exactly 24 ratings")
    expected=set(packet["item_order"])
    supplied=set()
    selections={}
    categories=set(packet["public_category_code_to_original_source_line"])
    for record in rows:
        if not isinstance(record,dict) or set(record)!={
            "item_code","category_code","confidence","facts_check",
            "naturalness","perceived_pressure"
        }:
            raise ValueError("each response needs exact four fields")
        code=record["item_code"]
        if code not in expected or code in supplied:
            raise ValueError("duplicate or unexpected stimulus code")
        supplied.add(code)
        cat=record["category_code"]
        if cat not in categories|{"U"}:
            raise ValueError("choice not a rater-visible category")
        conf=record["confidence"]
        if type(conf) is not int or not 1<=conf<=5:
            raise ValueError("confidence must be integer 1..5")
        if record["facts_check"] not in ("yes","no","unsure"):
            raise ValueError("unknown factual-equivalence rating")
        for item in ("naturalness","perceived_pressure"):
            if type(record.get(item)) is not int or not 1<=record[item]<=5:
                raise ValueError("missing or invalid perceptual Likert rating: "+item)
        selections[code]=record
    if supplied!=expected:
        raise ValueError("rater omitted one or more stimuli")
    return selections


def agreement(categories_a:list, categories_b:list)->dict:
    """Descriptive ordinary category agreement/kappa, never natal accuracy."""
    if len(categories_a)!=len(categories_b) or not categories_a:
        raise ValueError("paired categories required")
    n=len(categories_a)
    observed=sum(x==y for x,y in zip(categories_a,categories_b))/n
    cats=set(categories_a)|set(categories_b)
    ca=Counter(categories_a);cb=Counter(categories_b)
    chance=sum((ca[c]/n)*(cb[c]/n) for c in cats)
    kappa=None if abs(1-chance)<1e-12 else (observed-chance)/(1-chance)
    return {"paired_items":n,"raw_agreement":observed,
            "chance_marginal_agreement":chance,
            "Cohen_kappa_descriptive":kappa}


def grade(key:dict, response_packets:list[dict],
          *, all_submissions_are_SYNTHETIC_FIXTURES:bool=False)->dict:
    key=validate_key(key)
    if not response_packets:
        raise ValueError("no reviewer responses provided")
    if type(all_submissions_are_SYNTHETIC_FIXTURES) is not bool:
        raise ValueError("fixture flag must be exact boolean")
    saved={}
    packets={p["packet_id"]:p for p in key["rater_packets"]}
    for response in response_packets:
        rid=response.get("packet_id")
        if rid in saved:
            raise ValueError("same reviewer packet submitted twice")
        records=validate_submission(key,response)
        p=packets[rid]
        decoder=p["public_category_code_to_original_source_line"]
        saved[rid]={code:{
            "original_category": (decoder[r["category_code"]]
                                  if r["category_code"]!="U" else None),
            "confidence":r["confidence"],"facts_check":r["facts_check"],
            "naturalness":r["naturalness"],
            "perceived_pressure":r["perceived_pressure"]
            } for code,r in records.items()}
    truths={r["item_code"]:r["researcher_intended_style_original_line"]
            for r in key["items"]}
    confusion={str(i):{str(j):0 for j in [1,2,3,4,5,6,"U"]}
               for i in range(1,7)}
    per_category={str(i):{"n":0,"correct":0,"unsure":0,"wrong":0}
                  for i in range(1,7)}
    total=0;correct=0;unsure=0;facts_no=0;facts_unsure=0;confidence_correct=[]
    naturalness_by_true={str(i):[] for i in range(1,7)}
    pressure_by_true={str(i):[] for i in range(1,7)}
    for rid,records in saved.items():
        for code,obj in records.items():
            label=truths[code]
            chosen=obj["original_category"]
            total+=1
            per_category[str(label)]["n"]+=1
            naturalness_by_true[str(label)].append(obj["naturalness"])
            pressure_by_true[str(label)].append(obj["perceived_pressure"])
            confusion[str(label)][str(chosen) if chosen is not None else "U"]+=1
            if chosen==label:
                correct+=1;per_category[str(label)]["correct"]+=1
                confidence_correct.append(obj["confidence"])
            elif chosen is None:
                unsure+=1;per_category[str(label)]["unsure"]+=1
            else:
                per_category[str(label)]["wrong"]+=1
            if obj["facts_check"]=="no":facts_no+=1
            if obj["facts_check"]=="unsure":facts_unsure+=1

    # All 24 items use 4 true messages per each category. Therefore
    # chance from marginal rater preferences is 1/6 under independence.
    pairs=[]
    for ra,rb in combinations(sorted(saved),2):
        codes=sorted(truths)
        ca=[saved[ra][code]["original_category"] or "U" for code in codes]
        cb=[saved[rb][code]["original_category"] or "U" for code in codes]
        pairs.append({"rater_packets":[ra,rb],**agreement(ca,cb)})
    result={
        "schema":REPORT_SCHEMA,
        "research_key_digest":key["research_key_body_sha256"],
        "protocol_is_manipulation_classification_NOT_natal_prediction":True,
        "human_GeneKeys_natal_validation":False,
        "real_person_births_or_relationship_data_used":False,
        "submissions_marked_synthetic_fixtures":all_submissions_are_SYNTHETIC_FIXTURES,
        "rater_independence_or_identity_NOT_verified_by_software":True,
        "number_of_distinct_stimulus_texts":N_ITEMS,
        "number_of_response_packets":len(saved),
        "ratings_total":total,
        "correct_style_classifications":correct,
        "nonmatching_style_classifications":total-correct-unsure,
        "unsure_classifications":unsure,
        "coverage_adjusted_accuracy_all_ratings":correct/total,
        "conditional_accuracy_if_classified":(
            correct/(total-unsure) if total>unsure else None),
        "balanced_six_style_independence_baseline":1/6,
        "fraction_factually_wrong_reported":facts_no/total,
        "fraction_factually_uncertain_reported":facts_unsure/total,
        "mean_confidence_correct_only":(
            sum(confidence_correct)/len(confidence_correct)
            if confidence_correct else None),
        "confusion_truth_rows_rater_category_columns":confusion,
        "per_researcher_intended_style":per_category,
        "per_intended_style_mean_naturalness":{
            k:sum(v)/len(v) for k,v in naturalness_by_true.items() if v},
        "per_intended_style_mean_perceived_pressure":{
            k:sum(v)/len(v) for k,v in pressure_by_true.items() if v},
        "mean_naturalness_all":sum(map(sum,naturalness_by_true.values()))/total,
        "mean_perceived_pressure_all":sum(map(sum,pressure_by_true.values()))/total,
        "these_are_perceived_style_and_credibility_not_natal_predictions":True,
        "inter_rater_pairwise_agreement_descriptive":pairs,
        "external_manipulation_review_status":(
            "SYNTHETIC_DEVELOPMENT_FIXTURES_NOT_INDEPENDENT_RATERS"
            if all_submissions_are_SYNTHETIC_FIXTURES
            else "ANONYMOUS_RATING_FILES_RECEIVED_INDEPENDENCE_NOT_ATTESTED"
        ),
        "not_predefined_binary_PASS_or_FAIL":True,
        "no_automatic_after_response_rewrite_or_model_promotion":True,
    }
    result["self_digest_sha256"]=digest(result)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--key",type=Path,required=True)
    parser.add_argument("--ratings",type=Path,nargs="+",required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--synthetic-fixtures",action="store_true")
    args=parser.parse_args()
    if args.out.exists():
        raise FileExistsError("never overwrite a source classification record")
    key=load(args.key)
    ratings=[load(x) for x in args.ratings]
    result=grade(key,ratings,
                 all_submissions_are_SYNTHETIC_FIXTURES=args.synthetic_fixtures)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,
                                  ensure_ascii=False)+"\n",encoding="utf8")
    print("G39_STYLE_MANIPULATION_REVIEW",result["ratings_total"],
          "correct",result["correct_style_classifications"],
          "accuracy",result["coverage_adjusted_accuracy_all_ratings"],
          "fixture",result["submissions_marked_synthetic_fixtures"])


if __name__=="__main__":
    main()
