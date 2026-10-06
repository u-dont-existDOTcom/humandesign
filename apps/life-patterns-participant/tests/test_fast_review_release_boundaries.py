"""Release checks at the saved-source and participant guidance boundaries."""
from participant.review_timing import review_guidance
from participant.shadow_triage import make_gap_spec_triage_context
from test_fast_review_integration import answer_batch, setup_fast, start_fast, view
from test_participant import authority


def test_explicit_batch_skip_stays_visible_and_is_not_a_reopened_gap(tmp_path, monkeypatch):
    settings, fake, app, client, worker, box, _ = setup_fast(tmp_path, monkeypatch)
    review_id = start_fast(client, settings)["review_id"]
    worker.process_one("https://testserver", settings.review_worker_token, outbox=box)
    batch = view(client, settings, review_id)
    skipped_route = batch["clarifications"][0]["route_id"]
    response, _ = answer_batch(client, settings, batch, count=1, skip=True)
    assert response.status_code == 200
    worker.process_one("https://testserver", settings.review_worker_token, outbox=box)
    source = fake.seen_sources[-1][-1]
    assert source["answer_text"] is None
    assert source.get("answer_status") == "skipped"
    saved = app.state.store.gpt_review_read(review_id)["worker_state"]
    context = make_gap_spec_triage_context(saved, authority())
    assert skipped_route not in {row["id"] for row in context["candidate_routes"]}


def test_unmeasured_integrated_stage_estimates_are_labelled_provisional():
    for stage in ("reconciliation", "omission_audit", "final_synthesis", "final_admission"):
        info = review_guidance({
            "status": "processing", "review_protocol": "fast-batch-v1",
            "review_stage": stage, "stage_started_at_unix": 1000,
            "worker_heartbeat_at_unix": 1020,
        }, now=1020)
        assert "provisional" in info["estimate_basis"].lower()
        assert "provisional" in info["wait_guidance"].lower()
        assert info["recommended_check_after_seconds"] > 0
