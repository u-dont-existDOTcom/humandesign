"""Source fidelity and bounded optional capture, without any human-data claim."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from participant.shared_evidence import (
    BANK_PATH,
    INSTRUMENT,
    RECORD_SCHEMA,
    experience_source_catalog,
    public_instrument,
    source_catalog,
    validate_shared_evidence_record,
)

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / "tasks/life-patterns-shared-runtime-20261026"
BANK = public_instrument()
ITEMS = {row["id"]: row for row in BANK["questions"] + BANK["optional_microprobes"]}


def answer(qid="TIMELINE", text="  The concert began on 2020-07-14 at 19:30.\n"):
    return {
        "question_id": qid,
        "prompt_kind": "main",
        "state": "ANSWERED",
        "question_text": ITEMS[qid]["question"],
        "answer_text": text,
    }


def empty(qid, state="NOT_ASKED"):
    return {"question_id": qid, "prompt_kind": "main", "state": state, "answer_text": None}


def sitting(topics=None, responses=None, sid="sitting-0000000001"):
    topics = topics or ["TIMELINE"]
    return {
        "sitting_id": sid,
        "topics_selected": topics,
        "probe_admissions": [],
        "responses": responses if responses is not None else [answer(topics[0])],
    }


def example():
    return {
        "schema": RECORD_SCHEMA,
        "instrument": INSTRUMENT,
        "research_use_consented": True,
        "collection_mode": "gpt_optional",
        "status": "post_review_development_not_scored",
        "sittings": [sitting()],
    }


def source():
    return {
        "turns": [
            {
                "turn_id": "original-1",
                "turn_role": "behavioral",
                "question_text": "What happened?",
                "answer_text": "We moved in about 2018, I think.",
            }
        ]
    }


def followup(qid, state="ANSWERED"):
    value = {
        "question_id": qid,
        "prompt_kind": "followup",
        "state": state,
        "question_text": ITEMS[qid].get("optional_followup", ITEMS[qid].get("followup")),
        "unresolved_distinction": "The participant wants to explain the context.",
        "answer_text": "I can only recall some of the occasions.",
    }
    if state == "SKIPPED":
        value["answer_text"] = None
    return value


def with_probe(parent="VOCATION", probe="EP-LEADERSHIP-HISTORY"):
    record = example()
    record["sittings"] = [sitting([parent], [answer(parent), answer(probe)])]
    record["sittings"][0]["probe_admissions"] = [
        {
            "probe_id": probe,
            "parent_topic_id": parent,
            "unresolved_distinction": "Which responsibilities were actually held is still unclear.",
        }
    ]
    return record


def test_projection_is_reproducible_and_all_original_wording_is_exact():
    spec = importlib.util.spec_from_file_location(
        "shared_projection", TASK / "build_shared_evidence_projection.py"
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    projected, manifest = builder.contents()
    assert BANK_PATH.read_bytes() == builder.encoded(projected)
    assert (TASK / "SHARED-EVIDENCE-PROJECTION.json").read_bytes() == builder.encoded(manifest)
    original = json.loads(builder.SOURCE.read_text())
    assert len(original["questions"]) == len(projected["questions"]) == 23
    assert len(original["optional_microprobes"]) == len(projected["optional_microprobes"]) == 7
    assert len(manifest["objects"]) == 30
    for key, whitelist, followup_key in (
        ("questions", builder.TOPIC_KEYS, "optional_followup"),
        ("optional_microprobes", builder.PROBE_KEYS, "followup"),
    ):
        for before, after in zip(original[key], projected[key], strict=True):
            assert after == {field: before[field] for field in whitelist}
            assert before["question"] == after["question"]
            assert before[followup_key] == after[followup_key]
            entry = next(row for row in manifest["objects"] if row["id"] == before["id"])
            assert entry["source_object_sha256"] == builder.object_hash(before)
    assert hashlib.sha256(builder.SOURCE.read_bytes()).hexdigest() == builder.SOURCE_SHA256
    serialized = json.dumps(projected)
    for forbidden in (
        "source_claim_ids",
        "source_domains",
        "external_source_reference_ids",
        "source_ids",
        "time_window",
        "V-I-VENUS",
        "V-I-MERCURY",
        "BJ-",
        "source_object_sha256",
    ):
        assert forbidden not in serialized


def test_event_date_clock_whitespace_and_original_object_are_preserved():
    value = example()
    before = copy.deepcopy(value)
    assert validate_shared_evidence_record(value) is value
    assert value == before
    assert value["sittings"][0]["responses"][0]["answer_text"].endswith("19:30.\n")


@pytest.mark.parametrize(
    "change",
    [
        "no_consent",
        "fake_truth",
        "wrong_version",
        "wrong_status",
        "wrong_channel",
        "extra",
        "empty_sittings",
        "missing_topic_state",
        "duplicate_response",
        "wording",
        "unselected",
        "explicit_birth",
        "explicit_chart",
        "state_object",
        "kind_object",
        "oversized",
    ],
)
def test_invalid_records_fail_without_mutating_source(change):
    value = example()
    response = value["sittings"][0]["responses"][0]
    if change == "no_consent":
        value["research_use_consented"] = False
    elif change == "fake_truth":
        value["research_use_consented"] = 1
    elif change == "wrong_version":
        value["instrument"] = "next"
    elif change == "wrong_status":
        value["status"] = "validated"
    elif change == "wrong_channel":
        value["collection_mode"] = {"railway_finish": True}
    elif change == "extra":
        value["score"] = 5
    elif change == "empty_sittings":
        value["sittings"] = []
    elif change == "missing_topic_state":
        value["sittings"][0]["responses"] = []
    elif change == "duplicate_response":
        value["sittings"][0]["responses"].append(copy.deepcopy(response))
    elif change == "wording":
        response["question_text"] += " A new scene?"
    elif change == "unselected":
        response.update(answer("DREAM"))
    elif change == "explicit_birth":
        response["answer_text"] = "My date of birth is private."
    elif change == "explicit_chart":
        response["answer_text"] = "My natal chart explains my work."
    elif change == "state_object":
        response["state"] = {}
    elif change == "kind_object":
        response["prompt_kind"] = []
    elif change == "oversized":
        response["answer_text"] = "a" * 250001
    before = copy.deepcopy(value)
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    assert value == before


def test_states_remain_distinct_and_skips_preserve_process_feedback_only():
    value = example()
    ids = ["DREAM", "BELIEF", "TIMELINE", "HOME", "ART"]
    responses = [
        empty(ids[0]),
        empty(ids[1], "SKIPPED"),
        answer(ids[2]),
        answer(ids[3]),
        answer(ids[4]),
    ]
    responses[1]["process_feedback"] = ["This seems repetitive to me."]
    responses[2]["state"] = "NEVER"
    responses[2]["answer_text"] = "That has never happened to me."
    responses[3]["state"] = "UNCERTAIN"
    responses[3]["answer_text"] = "I cannot tell."
    responses[4]["state"] = "NO_OPPORTUNITIES"
    responses[4]["answer_text"] = "I have not had the opportunity."
    value["sittings"] = [sitting(ids, responses)]
    assert validate_shared_evidence_record(value) == value
    for nonanswer in ("NOT_ASKED", "SKIPPED", "FUTURE_PENDING"):
        value["sittings"] = [sitting(["DREAM"], [empty("DREAM", nonanswer)])]
        assert validate_shared_evidence_record(value) == value
        value["sittings"][0]["responses"][0]["answer_text"] = "A made-up negative"
        with pytest.raises(ValueError):
            validate_shared_evidence_record(value)


def test_actual_earlier_source_is_required_for_reuse_and_metadata_is_excluded():
    primary = source()
    primary["turns"].append(
        {
            "turn_role": "collection_metadata",
            "question_text": "Prior familiarity?",
            "answer_text": "yes",
        }
    )
    secondary = {"turns": [{"question_text": "Continuity?", "answer_text": "Still learning."}]}
    catalog = source_catalog(primary, secondary)
    assert [row["source_ref"] for row in catalog] == [
        "/primary/turns/0/answer_text",
        "/cf003/turns/0/answer_text",
    ]
    value = example()
    reused = empty("TIMELINE", "ALREADY_COVERED")
    reused.update(source_ref=catalog[0]["source_ref"], source_quote="about 2018, I think.")
    value["sittings"][0]["responses"] = [reused]
    assert validate_shared_evidence_record(value, primary_record=primary) == value
    reused["source_quote"] = "about 2018"
    assert validate_shared_evidence_record(value, primary_record=primary) == value
    for bad_quote in ("about 2017", "We moved I think", ""):
        reused["source_quote"] = bad_quote
        with pytest.raises(ValueError):
            validate_shared_evidence_record(value, primary_record=primary)
    reused["source_quote"] = "about 2018"
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    reused["question_text"] = ITEMS["TIMELINE"]["question"]
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value, primary_record=primary)


def test_catalog_does_not_reuse_superseded_quarantined_or_skipped_source():
    primary = source()
    primary["turns"] += [
        {
            "turn_id": "fix",
            "correction_of": "original-1",
            "answer_text": "Correction: around 2019.",
        },
        {"answer_status": "skipped", "answer_text": "Please skip."},
        {"quarantined": True, "answer_text": "Quarantined words."},
        {"answer_text": "A birth chart was shown."},
    ]
    assert source_catalog(primary) == [
        {
            "source_ref": "/primary/turns/1/answer_text",
            "question_text": "",
            "answer_text": "Correction: around 2019.",
        }
    ]


def shared_reuse_record(*, separate_sittings=False):
    original = answer("VOCATION", "  I coordinated the volunteers at the festival.\n")
    reuse = empty("STATUS", "ALREADY_COVERED")
    reuse.update(
        source_ref="/shared/sittings/0/responses/0/answer_text",
        source_quote="I coordinated the volunteers at the festival.",
    )
    value = example()
    value["sittings"] = (
        [
            sitting(["VOCATION"], [original]),
            sitting(["STATUS"], [reuse], sid="sitting-0000000002"),
        ]
        if separate_sittings
        else [sitting(["VOCATION", "STATUS"], [original, reuse])]
    )
    return value


@pytest.mark.parametrize("separate_sittings", [False, True])
def test_earlier_shared_answers_can_be_reused_without_reasking(separate_sittings):
    value = shared_reuse_record(separate_sittings=separate_sittings)
    before = copy.deepcopy(value)
    assert validate_shared_evidence_record(value) is value
    assert value == before
    assert value["sittings"][0]["responses"][0]["answer_text"].startswith("  ")


def test_earlier_shared_followup_can_be_reused_directly():
    value = shared_reuse_record()
    responses = value["sittings"][0]["responses"]
    extra = followup("VOCATION")
    extra["answer_text"] = "The responsibilities were informal and unpaid."
    responses.insert(1, extra)
    responses[-1].update(
        source_ref="/shared/sittings/0/responses/1/answer_text",
        source_quote="informal and unpaid",
    )
    assert validate_shared_evidence_record(value) == value


@pytest.mark.parametrize("change", ["self", "forward", "absent", "reuse_chain", "bad_quote"])
def test_shared_reuse_requires_an_actual_preceding_substantive_answer(change):
    value = shared_reuse_record()
    current = value["sittings"][0]
    reuse = current["responses"][1]
    if change == "self":
        reuse["source_ref"] = "/shared/sittings/0/responses/1/answer_text"
    elif change == "forward":
        reuse["source_ref"] = "/shared/sittings/0/responses/1/answer_text"
        current["responses"].reverse()
    elif change == "absent":
        reuse["source_ref"] = "/shared/sittings/2/responses/0/answer_text"
    elif change == "reuse_chain":
        current["topics_selected"].append("LEARNING_HISTORY")
        chained = empty("LEARNING_HISTORY", "ALREADY_COVERED")
        chained.update(
            source_ref="/shared/sittings/0/responses/1/answer_text",
            source_quote=reuse["source_quote"],
        )
        current["responses"].append(chained)
    elif change == "bad_quote":
        reuse["source_quote"] = "I supervised all the volunteers."
    before = copy.deepcopy(value)
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    assert value == before


@pytest.mark.parametrize("state", ["NOT_ASKED", "SKIPPED", "FUTURE_PENDING"])
def test_unanswered_shared_states_and_process_feedback_cannot_be_reuse_sources(state):
    value = shared_reuse_record()
    current = value["sittings"][0]
    missing = empty("VOCATION", state)
    missing["process_feedback"] = ["I coordinated the volunteers at the festival."]
    current["responses"][0] = missing
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    current["responses"][1]["source_ref"] = "/shared/sittings/0/responses/0/process_feedback/0"
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)


def test_editing_earlier_shared_draft_requires_dependent_quote_revalidation():
    value = shared_reuse_record(separate_sittings=True)
    assert validate_shared_evidence_record(value) == value
    value["sittings"][0]["responses"][0]["answer_text"] = "I helped, but did not coordinate."
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    value["sittings"][1]["responses"][0]["source_quote"] = "I helped, but did not coordinate."
    assert validate_shared_evidence_record(value) == value


def experience_notes(state="ANSWERED"):
    from participant.experience import INSTRUMENT as EXPERIENCE_INSTRUMENT
    from participant.experience import RECORD_SCHEMA as EXPERIENCE_SCHEMA

    responses = [{"question_id": f"EM{number:02d}", "state": "NOT_ASKED"} for number in range(1, 9)]
    responses[0] = {
        "question_id": "EM01",
        "state": state,
        "note": "  Making wood sculptures is a regular source of wonder for me.\n",
    }
    if state == "ANSWERED":
        responses[0]["value"] = "weekly"
    return {
        "schema": EXPERIENCE_SCHEMA,
        "instrument": EXPERIENCE_INSTRUMENT,
        "research_use_consented": True,
        "collection_mode": "gpt_optional",
        "status": "post_review_exploratory_not_scored",
        "topics_selected": [],
        "responses": responses,
    }


def experience_reuse():
    reuse = empty("ART", "ALREADY_COVERED")
    reuse.update(
        source_ref="/experience/responses/0/note",
        source_quote="Making wood sculptures is a regular source of wonder for me.",
    )
    value = example()
    value["sittings"] = [sitting(["ART"], [reuse])]
    return value


@pytest.mark.parametrize("state", ["ANSWERED", "NEVER", "UNKNOWN"])
def test_exact_consented_experience_notes_can_cover_shared_topics(state):
    from participant.experience import public_instrument as experience_instrument

    record = experience_notes(state)
    before = copy.deepcopy(record)
    catalog = experience_source_catalog(record)
    assert catalog == [
        {
            "source_ref": "/experience/responses/0/note",
            "question_text": experience_instrument()["items"][0]["question"],
            "answer_text": record["responses"][0]["note"],
        }
    ]
    assert source_catalog(None, experience_record=record) == catalog
    value = experience_reuse()
    assert validate_shared_evidence_record(value, experience_record=record) is value
    assert record == before


@pytest.mark.parametrize("change", ["no_consent", "invalid_version", "missing_id", "bad_state"])
def test_invalid_experience_record_cannot_supply_reuse_notes(change):
    record = experience_notes()
    if change == "no_consent":
        record["research_use_consented"] = False
    elif change == "invalid_version":
        record["instrument"] = "other"
    elif change == "missing_id":
        record["responses"].pop()
    elif change == "bad_state":
        record["responses"][0]["state"] = {}
    with pytest.raises(ValueError):
        experience_source_catalog(record)
    with pytest.raises(ValueError):
        validate_shared_evidence_record(experience_reuse(), experience_record=record)


@pytest.mark.parametrize("state", ["SKIPPED", "NOT_ASKED", "ALREADY_COVERED"])
def test_skipped_unasked_or_reused_experience_sources_are_not_new_evidence(state):
    record = experience_notes("SKIPPED")
    record["responses"][0]["state"] = state
    if state != "SKIPPED":
        record["responses"][0].pop("note")
    if state == "ALREADY_COVERED":
        record["responses"][0]["source_ref"] = "An earlier experience record"
    assert experience_source_catalog(record) == []
    with pytest.raises(ValueError):
        validate_shared_evidence_record(experience_reuse(), experience_record=record)


@pytest.mark.parametrize(
    "path",
    [
        "/experience/responses/8/note",
        "/experience/responses/0/value",
        "/experience/responses/0/process_feedback",
        "/experience/responses/1/note",
    ],
)
def test_experience_reuse_rejects_unregistered_paths(path):
    value = experience_reuse()
    value["sittings"][0]["responses"][0]["source_ref"] = path
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value, experience_record=experience_notes())


def test_experience_optout_absent_notes_and_stale_quotes_invalidate_reuse():
    value = experience_reuse()
    assert experience_source_catalog(None) == []
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    record = experience_notes()
    record["responses"][0].pop("note")
    assert experience_source_catalog(record) == []
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value, experience_record=record)
    record = experience_notes()
    record["responses"][0]["note"] = "I appreciate sculptures but do not make them."
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value, experience_record=record)


def test_five_topics_is_per_sitting_and_not_a_lifetime_quota():
    value = example()
    ids = [row["id"] for row in BANK["questions"]]
    value["sittings"] = [
        sitting(ids[:5], [answer(qid) for qid in ids[:5]]),
        sitting(ids[5:10], [answer(qid) for qid in ids[5:10]], "sitting-0000000002"),
    ]
    assert validate_shared_evidence_record(value) == value
    value["sittings"][0]["topics_selected"].append(ids[10])
    value["sittings"][0]["responses"].append(answer(ids[10]))
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)


@pytest.mark.parametrize("state", ["ANSWERED", "SKIPPED", "UNCERTAIN", "NEVER"])
def test_another_sitting_cannot_reopen_answered_or_skipped_topics(state):
    value = example()
    first = empty("TIMELINE", state) if state == "SKIPPED" else answer()
    first["state"] = state
    value["sittings"] = [sitting(responses=[first]), sitting(sid="sitting-0000000002")]
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    value["sittings"][0]["responses"] = [empty("TIMELINE")]
    assert validate_shared_evidence_record(value) == value


def test_probe_and_followup_require_material_admission_and_eligible_parent():
    value = with_probe()
    value["sittings"][0]["responses"].append(followup("EP-LEADERSHIP-HISTORY"))
    assert validate_shared_evidence_record(value) == value
    for state in (
        "SKIPPED",
        "NOT_ASKED",
        "NO_OPPORTUNITIES",
        "NOT_APPLICABLE",
        "NEVER",
        "FUTURE_PENDING",
    ):
        broken = copy.deepcopy(value)
        parent = broken["sittings"][0]["responses"][0]
        parent["state"] = state
        if state in {"SKIPPED", "NOT_ASKED", "FUTURE_PENDING"}:
            parent.pop("question_text")
            parent["answer_text"] = None
        with pytest.raises(ValueError):
            validate_shared_evidence_record(broken)
    value["sittings"][0]["responses"][-1].pop("unresolved_distinction")
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    value = with_probe()
    value["sittings"][0]["responses"].reverse()
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)


def test_two_probe_limit_and_skip_covers_followup_variants():
    value = with_probe()
    sitting_value = value["sittings"][0]
    sitting_value["probe_admissions"] += [
        {
            "probe_id": pid,
            "parent_topic_id": "VOCATION",
            "unresolved_distinction": "Context remains unclear.",
        }
        for pid in ("EP-INDEPENDENT-FEEDBACK", "EP-PROJECT-FOLLOWTHROUGH")
    ]
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    value = with_probe()
    value["sittings"][0]["responses"].insert(1, followup("VOCATION", "SKIPPED"))
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
    value = example()
    value["sittings"][0]["responses"] = [empty("TIMELINE", "SKIPPED"), followup("TIMELINE")]
    with pytest.raises(ValueError):
        validate_shared_evidence_record(value)
