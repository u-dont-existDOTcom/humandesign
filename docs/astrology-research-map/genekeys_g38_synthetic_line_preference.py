"""G38 finite SYNTHETIC ONLY Gene Keys Line-preference dry run.

Researcher-made behavioral proxy to six official 'responds best to' style
labels. NOT Richard Rudd's own statistical forecast, official profile
calculator, a new independent astronomical feature beyond Human Design, or
a consented human trial.

Phases (separate sealed files; independent mock outcome generation):
  freeze → mock-responses → score
All files are exclusive-create. This is NOT trusted external notarization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
from collections import Counter
from typing import Any

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json"
BANK=ROOT/"GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json"
CONTRACT=ROOT/"GENEKEYS_G38_LINE_STYLE_STUDY_CONTRACT_DRAFT_V1.json"
SOURCE_PIN="2e53d6013037aeb40884df1da96390a27b7fbeb15828bb0a84342ddabd660b82"
SOURCE_STYLES=("detailed_open_info","warm_open_invitation",
               "autonomy_no_pressure","honest_gentle_nonromantic",
               "concise_next_step","unhurried_pacing")
DEV_SEED=20261025
OUTCOME_SALT="G38-DELIBERATELY_NO_BIRTH_ASSOCIATION"
PERSON_COUNT=120
PERMUTATIONS=1999
MOCK_POPULATION_STYLE_WEIGHTS=(.08,.12,.24,.22,.26,.08)
SCHEMAS=("G38_SYNTHETIC_PREFERENCE_FREEZE_V1",
         "G38_SYNTHETIC_INDEPENDENT_MOCK_CHOICES_V1",
         "G38_SYNTHETIC_PREFERENCE_PERMUTATION_SCORE_V1")


def canonical(o:Any)->bytes:
    return json.dumps(o,ensure_ascii=False,sort_keys=True,
                      separators=(",",":"),allow_nan=False).encode("utf8")


def digest(o:Any)->str:
    return hashlib.sha256(canonical(o)).hexdigest()


def packet(o:dict)->dict:
    return {"body":o,"sha256":digest(o)}


def check_packet(o:dict,schema:str)->dict:
    if not isinstance(o,dict) or set(o)!={"body","sha256"}:
        raise ValueError("invalid two-part source packet")
    b=o["body"]
    if not isinstance(b,dict) or b.get("schema")!=schema:
        raise ValueError("wrong packet schema")
    if o["sha256"]!=digest(b):
        raise ValueError("packet SHA256 mismatch")
    if b.get("synthetic_only") is not True:
        raise ValueError("this code refuses real participant records")
    return b


def read_json(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf8"))


def write_once(path:Path,body:dict):
    with path.open("x",encoding="utf8") as f:
        f.write(json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+"\n")


def validate_sources()->tuple[dict,dict,dict]:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_PIN:
        raise ValueError("original G37 six-line source changed")
    s=read_json(SOURCE)
    b=read_json(BANK)
    c=read_json(CONTRACT)
    assert s["schema"]=="HUMANDESIGN_G37_GENEKEYS_PROFILE_SIX_LINE_BEHAVIOR_SCOPE_V1"
    if b["source_registry_sha256"]!=SOURCE_PIN:
        raise ValueError("bank not tied to exact original six-line register")
    if c["official_source"]["source_registry_sha256"]!=SOURCE_PIN:
        raise ValueError("study contract not tied to exact original")
    labels={str(x["line"]):x for x in s["verified_six_line_interpersonal_styles"]}
    if set(b["style_map"])!=set(labels) or len(b["scenarios"])!=4:
        raise ValueError("missing publisher's source styles or fictional tasks")
    for key,style in b["style_map"].items():
        if style["source_phrase"]!=labels[key]["brief_official_responds_best_to"]:
            raise ValueError("source heading/paraphrase accidentally changed")
        if style["construct"]!=SOURCE_STYLES[int(key)-1]:
            raise ValueError("experiment's six construct labels changed")
    if c["branch"]["natal_sphere_choice_is"]!="ASSISTANT_ANALYST_DESIGN_CHOICE_NOT_PUBLISHER_PRESCRIPTION":
        raise ValueError("researcher-added sphere must be disclosed")
    if not c["blinding"]["posthoc_line_or_sphere_changes_require_new_untouched_cohort"]:
        raise ValueError("source rule has no holdout protection")
    ids=set()
    for task in b["scenarios"]:
        if task["id"] in ids:
            raise ValueError("duplicate fictional task")
        ids.add(task["id"])
        if len(task["facts"])!=3 or len(set(task["facts"]))!=3:
            raise ValueError("need three distinct facts per scenario")
    return s,b,c


def messages_from_bank(bank:dict)->dict:
    output={}
    for task in bank["scenarios"]:
        facts=" ".join(task["facts"])
        messages={}
        for n,s in bank["style_map"].items():
            msg=s["intro"]+facts+s["outro"]
            if any(msg.count(f)!=1 for f in task["facts"]):
                raise ValueError("factual content not equal/complete for style")
            messages[int(n)]=msg
        output[task["id"]]={"facts":task["facts"],"messages":messages}
    return output


def fake_freeze()->dict:
    _src,bank,contract=validate_sources()
    rendered=messages_from_bank(bank)
    participants=[]
    for j in range(PERSON_COUNT):
        pid=f"ONLY-SYNTHETIC-G38-{j+1:03d}"
        group=f"MOCK-GROUP-{j//30+1}"
        fake_line=j%6+1
        trials=[]
        for task in bank["scenarios"]:
            tid=task["id"]
            pseudo=int.from_bytes(hashlib.sha256(
                f"ORDER:{DEV_SEED}:{pid}:{tid}".encode()).digest()[:8],"big")
            rng=random.Random(pseudo)
            order=list(range(1,7))
            rng.shuffle(order)
            trials.append({
                "task":tid,
                "displayed_styles_in_order":order,
                "messages_displayed_in_order":[rendered[tid]["messages"][line]
                                               for line in order],
            })
        participants.append({
            "synthetic_participant_id":pid,
            "synthetic_cohort_stratum":group,
            "SYNTHETIC_chart_line_not_actual_astro":fake_line,
            "trials":trials,
        })
    if len(participants)!=120 or len({p["synthetic_participant_id"]
                                       for p in participants})!=PERSON_COUNT:
        raise ValueError("incomplete synthetic cohort")
    # Groups balanced by line exactly 5 for each synthetic group of 30.
    for group in sorted(set(x["synthetic_cohort_stratum"] for x in participants)):
        counts=Counter(x["SYNTHETIC_chart_line_not_actual_astro"] for x in participants
                       if x["synthetic_cohort_stratum"]==group)
        if counts!={k:5 for k in range(1,7)}:
            raise ValueError("imbalanced synthetic natal-line assignment")
    return packet({
        "schema":SCHEMAS[0],"synthetic_only":True,
        "source_G37_SHA256":SOURCE_PIN,
        "stimulus_bank_file_SHA256":hashlib.sha256(BANK.read_bytes()).hexdigest(),
        "study_contract_file_SHA256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "original_G37_publisher_sphere_choice_undetermined":True,
        "natal_Sun_sphere_line_is_analyst_chosen":True,
        "Gene_Keys_Human_Design_numeric_line_identical":True,
        "same_chart_CANNOT_add_information_beyond_full_HD_natal_input":True,
        "stimuli_manipulation_peer_validated":False,
        "all_messages_six_source_style_PROXIES_not_original_gene_keys_scripts":True,
        "actual_birth_records_used":False,
        "real_predictions_before_responses":False,
        "real_consent_or_communication_administered":False,
        "rehearsal_is_NOT_externally_timestamped":True,
        "analysis_contract":{
            "primary_statistic":"mean_person_matched_choice_rate_4_scenarios",
            "one_sided_alternative":"source_matched_rate_greater_than_permuted_person_lines",
            "clustered_null":"whole-person synthetic chart-lines permuted within pre-existing 4 mock strata",
            "preserve_style_popularity":True,
            "preserve_within_person_repeated_response_correlation":True,
            "do_not_use_naive_one_sixth_as_primary_null":True,
            "perm_seed":DEV_SEED,"perm_count":PERMUTATIONS,
            "source_nonliteral":"natal Sun Line choice plus six message-style proxy operationalization",
            "no_real_significance_from_artificial_outcomes":True
        },
        "participant_count":len(participants),
        "trials_per_person":len(bank["scenarios"]),
        "question":"Which message would you most prefer to receive?",
        "synthetic_participants":participants,
    })


def verified_source_locked_freeze(f:dict)->dict:
    body=check_packet(f,SCHEMAS[0])
    if f!=fake_freeze():
        raise ValueError("even validly rehashed change from original source freeze rejected")
    return body


def synthetic_independent_style_choice(pid:str,task_id:str)->int:
    """Independent of synthetic Line and display position; popularity unequal."""
    h=hashlib.sha256(f"MOCK:{OUTCOME_SALT}:{pid}:{task_id}".encode()).digest()
    u=int.from_bytes(h[:8],"big")/2**64
    cumulative=0.
    for i,p in enumerate(MOCK_POPULATION_STYLE_WEIGHTS,1):
        cumulative+=p
        if u<cumulative:
            return i
    return 6


def fake_responses(f:dict)->dict:
    b=verified_source_locked_freeze(f)
    answers=[]
    for person in b["synthetic_participants"]:
        pid=person["synthetic_participant_id"]
        for t in person["trials"]:
            style=synthetic_independent_style_choice(pid,t["task"])
            index=t["displayed_styles_in_order"].index(style)+1
            answers.append({
                "synthetic_participant_id":pid,
                "task":t["task"],
                "selected_visible_position_1to6":index,
                "no_actual_person_answered":True
            })
    return packet({
        "schema":SCHEMAS[1],"synthetic_only":True,
        "pre_answer_frozen_packet_sha256":f["sha256"],
        "responses_generated_independently_of_fake_natal_line":True,
        "response_generator_has_unequal_general_style_popularity":True,
        "synthetic_mock_label_count":len(answers),
        "response_rows":answers
    })


def _map_responses(fbody:dict,rbody:dict)->tuple[list[dict],dict]:
    persons=fbody["synthetic_participants"]
    wanted={(p["synthetic_participant_id"],t["task"]) for p in persons
            for t in p["trials"]}
    received={}
    for answer in rbody["response_rows"]:
        key=(answer.get("synthetic_participant_id"),answer.get("task"))
        if key not in wanted or key in received:
            raise ValueError("missing/duplicate/unknown mock choice key")
        position=answer.get("selected_visible_position_1to6")
        if type(position) is not int or not 1<=position<=6:
            raise ValueError("mock selected position invalid")
        if answer.get("no_actual_person_answered") is not True:
            raise ValueError("real response not admitted in synthetic runner")
        received[key]=position
    if set(received)!=wanted:
        raise ValueError("not all synthetic task responses present")
    scored=[]
    for p in persons:
        styles=[]
        for t in p["trials"]:
            position=received[(p["synthetic_participant_id"],t["task"])]
            styles.append(t["displayed_styles_in_order"][position-1])
        scored.append({
            "id":p["synthetic_participant_id"],
            "stratum":p["synthetic_cohort_stratum"],
            "source_line":p["SYNTHETIC_chart_line_not_actual_astro"],
            "preferred_message_styles":styles,
        })
    return scored,received


def _matched_count(rows:list[dict],labels:dict[str,int])->int:
    return sum(style==labels[row["id"]]
               for row in rows for style in row["preferred_message_styles"])


def score_mock(f:dict,responses:dict)->dict:
    b=verified_source_locked_freeze(f)
    o=check_packet(responses,SCHEMAS[1])
    if o.get("pre_answer_frozen_packet_sha256")!=f["sha256"]:
        raise ValueError("mock response cohort has different pre-answer freeze")
    rows,_=_map_responses(b,o)
    assignments={p["id"]:p["source_line"] for p in rows}
    actual=_matched_count(rows,assignments)
    all_choices=sum(len(x["preferred_message_styles"]) for x in rows)
    if all_choices!=480:
        raise ValueError("unexpected mock observation denominator")
    cnt=Counter(k for r in rows for k in r["preferred_message_styles"])
    byline=Counter(assignments.values())
    popularity={str(style):cnt[style]/all_choices for style in range(1,7)}
    baseline=sum(popularity[str(assignments[p["id"]])] for p in rows)/len(rows)
    # Permute PERSON-LEVEL Line among 4 strata. Four within-person repeated
    # mock choices are NEVER shuffled independently.
    groups=sorted(set(x["stratum"] for x in rows))
    grouped={g:[x["id"] for x in rows if x["stratum"]==g] for g in groups}
    rng=random.Random(int(b["analysis_contract"]["perm_seed"]))
    stats=[]
    for _ in range(int(b["analysis_contract"]["perm_count"])):
        hypothetical=assignments.copy()
        for ids in grouped.values():
            labels=[assignments[i] for i in ids]
            rng.shuffle(labels)
            hypothetical.update(zip(ids,labels))
        stats.append(_matched_count(rows,hypothetical))
    p=(1+sum(value>=actual for value in stats))/(1+len(stats))
    return packet({
        "schema":SCHEMAS[2],
        "synthetic_only":True,
        "freezed_source_packet_sha256":f["sha256"],
        "synthetic_mock_responses_sha256":responses["sha256"],
        "truly_blinded_human_validation_count":0,
        "real_age_or_birth_location_records_used":False,
        "selected_preference_stimuli_original_source_not_manipulation_verified":True,
        "matched_line_hits_across_all_synthetic_tasks":actual,
        "synthetic_task_choices_total":all_choices,
        "matched_preference_fraction_mock":actual/all_choices,
        "population_style_preference_rates_mock":popularity,
        "nonastrology_popularity_baseline_fraction_mock":baseline,
        "mock_difference_over_population_popularity":actual/all_choices-baseline,
        "SOURCE_DEFINED_HYPOTHESIS_NOT_AUTHOR_QUANTIFIED":True,
        "mock_unadjusted_uniform_one_sixth_is_NOT_appropriate_null":True,
        "perm_group_strata":groups,
        "perm_whole_person_line_labels":True,
        "perm_count":len(stats),
        "person_level_null_one_sided_p_MOCK_ONLY":p,
        "not_a_human_GeneKeys_utility_or_predictivity_measure":True,
        "production_scorer_modified":False
    })


def main()->None:
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="action",required=True)
    for name in ("freeze","mock","score"):
        p=sub.add_parser(name)
        p.add_argument("--out",type=Path,required=True)
        if name!="freeze":p.add_argument("--freeze",type=Path,required=True)
        if name=="score":p.add_argument("--responses",type=Path,required=True)
    args=parser.parse_args()
    if args.action=="freeze":data=fake_freeze()
    elif args.action=="mock":data=fake_responses(read_json(args.freeze))
    else:data=score_mock(read_json(args.freeze),read_json(args.responses))
    write_once(args.out,data)
    print("G38_SYNTHETIC_ONLY",args.action,args.out,"sha",data["sha256"])


if __name__=="__main__":
    main()
