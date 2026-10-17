"use strict";
(function () {
  const find = id => document.getElementById(id);
  const panels = ["progress", "review", "questions", "done"];
  let csrf = "";
  let cf003Questions = [];
  let savedBatch = "";
  let batchQuestions = [];
  let batchRequest = null;
  let busy = false;
  let confirmed = false;
  let lastState = null;
  let timer = null;

  function alertMessage(message) {
    find("alert").hidden = !message;
    find("alert").textContent = message || "";
  }
  function showPanel(name) {
    for (const pane of panels) {
      find(pane + "-panel").hidden = pane !== name;
      const step = find("step-" + pane);
      step.removeAttribute("aria-current");
      step.classList.toggle("complete", panels.indexOf(pane) < panels.indexOf(name));
      if (pane === name) step.setAttribute("aria-current", "step");
    }
    find("loading").hidden = true;
  }
  async function api(path, body, method = "POST") {
    const opts = {
      method, credentials: "same-origin", cache: "no-store",
      headers: {Accept: "application/json"}
    };
    if (method !== "GET") {
      opts.headers["Content-Type"] = "application/json";
      if (path !== "/api/finish/exchange") opts.headers["X-Finish-CSRF"] = csrf;
      opts.body = JSON.stringify(body);
    }
    const response = await fetch(path, opts);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(
      typeof data.detail === "string" ? data.detail : "The secure request could not be completed."
    );
    return data;
  }
  function add(parent, tag, message, className) {
    const node = document.createElement(tag);
    node.textContent = message == null ? "" : String(message);
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  }
  function showEvidence(items) {
    const host = find("review-items");
    host.replaceChildren();
    if (!items.length) add(host, "p",
      "No descriptive observation was admitted by the independent reviewer. Unknown traits remain unknown.");
    for (const item of items) {
      const card = add(host, "article", "", "evidence");
      const labels = Array.isArray(item.measurement_labels) ? item.measurement_labels : [];
      add(card, "h3", labels.join(" / ") || "Reported pattern");
      add(card, "p", item.observation || "No observation recorded.");
      const conditions = Array.isArray(item.conditions) ? item.conditions : [];
      if (conditions.length) add(card, "small", "Conditions: " + conditions.join("; "));
      if (item.time_frame) add(card, "small", "Time frame: " + item.time_frame);
      if (item.relationship_context) add(card, "small", "Context: " + item.relationship_context);
      for (const quote of (Array.isArray(item.source_quotes) ? item.source_quotes : [])) {
        add(card, "blockquote", quote.quote || "", "quote");
      }
    }
  }
  function showFinalQuestions(data) {
    if (!Array.isArray(data) || data.length !== 3) {
      throw new Error("The fixed three-question supplement is unavailable.");
    }
    cf003Questions = data;
    const host = find("cf003-items");
    host.replaceChildren();
    data.forEach((question, i) => {
      const label = add(host, "label", (i + 1) + ". " + question.question, "question");
      const area = document.createElement("textarea");
      area.required = true;
      area.maxLength = 20000;
      area.name = question.question_id;
      area.rows = 5;
      area.setAttribute("aria-label", question.question);
      label.appendChild(area);
      add(host, "small", "Answer in your own words; being unsure is valid.", "subtle");
    });
    const values = [
      ["", "Choose one"], ["yes", "Yes"], ["no", "No"],
      ["unsure", "Not sure"], ["prefer_not_to_say", "Prefer not to say"]
    ];
    find("finish-form").querySelectorAll("select").forEach(select => {
      select.replaceChildren();
      for (const pair of values) {
        const option = document.createElement("option");
        option.value = pair[0];
        option.textContent = pair[1];
        select.appendChild(option);
      }
    });
  }
  function showDone(receipt) {
    clearTimeout(timer);
    alertMessage("");
    showPanel("done");
    find("receipt-text").textContent = receipt.submission_id ?
      "Submission receipt: " + receipt.submission_id : "Your submission receipt was stored.";
  }
  function currentBatch(items, id) {
    const host = find("clarification-items");
    const key = id || "legacy:" + items[0].clarification_id;
    if (savedBatch === key && host.children.length) return; // keep typing during checks
    savedBatch = key;
    batchQuestions = items;
    batchRequest = null;
    host.replaceChildren();
    items.forEach((item, i) => {
      const part = add(host, "fieldset", "", "review-question");
      add(part, "legend", "Question " + (i + 1) + " of " + items.length +
        " in this batch (not the final interview total)");
      add(part, "p", item.question_text || "Question text unavailable.");
      if (item.participant_purpose) add(part, "p",
        "Why this is asked: " + item.participant_purpose, "subtle");
      const label = add(part, "label", "Your answer", "question");
      const area = document.createElement("textarea");
      area.name = item.clarification_id;
      area.maxLength = 20000;
      area.rows = 4;
      area.setAttribute("aria-label", item.question_text);
      label.appendChild(area);
      const skip = add(part, "label", "", "checkline");
      const input = document.createElement("input");
      input.type = "checkbox";
      input.name = "skip-" + item.clarification_id;
      input.addEventListener("change", () => {
        area.disabled = input.checked;
        if (input.checked) area.value = "";
      });
      skip.append(input);
      add(skip, "span", "Skip this question (keep this distinction unknown)");
    });
  }
  function schedule() {
    clearTimeout(timer);
    if (!lastState || lastState.status === "ready" ||
        lastState.status === "stored" || lastState.status === "stopped") return;
    if (["paused", "error", "resource_limited", "withdrawn"].includes(lastState.status)) return;
    const interval = document.hidden ? 60000 : 20000;
    timer = setTimeout(() => {
      if (busy) { schedule(); return; }
      refresh(false);
    }, interval);
  }
  function showProgress(data) {
    const stage = data.review_stage_label || String(data.status).replaceAll("_", " ");
    const closed = Boolean(data.clarification_intake_closed);
    find("review-stage-message").textContent = closed ?
      (["error", "resource_limited", "paused"].includes(data.status) ?
        "No more questions will be asked. Independent review is blocked or paused." :
        "No more questions will be asked. Railway is processing final evidence.") :
      "Current stage: " + stage;
    find("review-count").textContent =
      (data.original_turn_count || 0) + " earlier responses preserved. " +
      (data.clarification_count || 0) + " reviewer clarifications answered or skipped. " +
      "Overall questions that might be needed are unknown.";
    find("review-wait").textContent = ["error", "resource_limited", "paused"].includes(data.status) ?
      "Review is paused or blocked, not silently progressing. You can return to the original GPT to resolve it." :
      "This page automatically checks the saved review while open. You can leave and return in this browser; no repeated GPT status messages are necessary. Processing time is not guaranteed.";
    const pending = !closed && data.status === "clarification_needed" &&
      Array.isArray(data.clarifications) ? data.clarifications : [];
    const panel = find("clarification-panel");
    panel.hidden = !pending.length;
    if (pending.length) currentBatch(pending, data.batch_id);
    else if (!closed) {
      savedBatch = "";
      batchQuestions = [];
      batchRequest = null;
      find("clarification-items").replaceChildren();
    }
    find("close-questions").closest(".caution").hidden = closed;
    showPanel("progress");
  }
  function render(data) {
    lastState = data;
    csrf = data.csrf_token || "";
    if (data.submission && data.submission.submission_id) {
      showDone(data.submission);
      return;
    }
    if (data.status === "ready") {
      if (find("review-panel").hidden && find("questions-panel").hidden) {
        find("review-context").textContent = "Independent review complete. " +
          (data.original_turn_count || 0) + " original entries and " +
          (data.clarification_count || 0) + " saved reviewer clarifications.";
        showEvidence(Array.isArray(data.review_summary) ? data.review_summary : []);
        showFinalQuestions(data.cf003_questions);
        showPanel("review");
      }
      clearTimeout(timer);
      return;
    }
    if (data.status === "withdrawn" || data.status === "stopped") {
      throw new Error("This saved review has stopped. Return to your original interview.");
    }
    showProgress(data);
    schedule();
  }
  async function refresh(initial) {
    if (busy) return;
    try {
      render(await api("/api/finish/state", undefined, "GET"));
      if (initial) alertMessage("");
    } catch (err) {
      find("loading").hidden = true;
      alertMessage(err.message || "Review status unavailable.");
      if (lastState) schedule();
    }
  }
  async function open() {
    try {
      const match = /^#token=([A-Za-z0-9_-]{32,128})$/.exec(location.hash);
      if (location.hash) history.replaceState(null, "", "/finish");
      if (match) await api("/api/finish/exchange", {token: match[1]});
      await refresh(true);
    } catch (err) {
      find("loading").hidden = true;
      alertMessage(err.message || "Unable to open this private review.");
    }
  }
  find("clarification-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy || !batchQuestions.length) return;
    if (!batchRequest) {
      const form = new FormData(event.target);
      const answers = batchQuestions.map(question => {
        const skipped = form.get("skip-" + question.clarification_id) === "on";
        return {
          clarification_id: question.clarification_id,
          answer_text: skipped ? "" : String(form.get(question.clarification_id) || "").trim(),
          skipped
        };
      });
      if (answers.some(item => !item.skipped && !item.answer_text)) {
        alertMessage("Answer each current question or explicitly skip it.");
        return;
      }
      const operation_id = crypto.randomUUID();
      batchRequest = lastState.batch_id
        ? {batch_id: lastState.batch_id, operation_id, answers}
        : {...answers[0], operation_id};
    }
    busy = true;
    find("save-clarifications").disabled = true;
    try {
      const endpoint = "batch_id" in batchRequest
        ? "/api/finish/clarification-batches"
        : "/api/finish/clarifications";
      await api(endpoint, batchRequest);
      savedBatch = "";
      batchRequest = null;
      alertMessage("");
      render(await api("/api/finish/state", undefined, "GET"));
    } catch (err) {
      alertMessage(err.message + " The same saved batch can be retried without duplicating answers.");
    } finally {
      busy = false;
      find("save-clarifications").disabled = false;
      schedule();
    }
  });
  find("close-ack").addEventListener("change", event => {
    find("close-questions").disabled = !event.target.checked;
  });
  find("close-questions").addEventListener("click", async () => {
    if (busy || !find("close-ack").checked) return;
    busy = true;
    find("close-questions").disabled = true;
    try {
      await api("/api/finish/close-clarifications", {confirm_no_more_questions: true});
      savedBatch = "";
      alertMessage("");
      render(await api("/api/finish/state", undefined, "GET"));
    } catch (err) {
      alertMessage(err.message);
    } finally {
      busy = false;
      find("close-questions").disabled = !find("close-ack").checked;
      schedule();
    }
  });
  find("confirm-review").addEventListener("change", event => {
    confirmed = event.target.checked;
    find("next-button").disabled = !confirmed;
  });
  find("next-button").addEventListener("click", () => {
    if (confirmed) showPanel("questions");
  });
  find("back-button").addEventListener("click", () => showPanel("review"));
  find("finish-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy) return;
    if (!confirmed || !find("final-consent").checked) {
      alertMessage("Confirm both the reviewed evidence and storage permission first.");
      return;
    }
    const form = new FormData(event.target);
    const answers = cf003Questions.map(item => ({
      question_id: item.question_id,
      answer_text: String(form.get(item.question_id) || "").trim()
    }));
    if (answers.some(item => !item.answer_text)) {
      alertMessage("Answer all three questions; being unsure is a valid answer.");
      return;
    }
    const metadata = Object.fromEntries(
      ["rising_sign_previously_known", "previous_natal_chart_reading",
       "target_information_exposure"].map(key => [key, String(form.get(key) || "")])
    );
    busy = true;
    find("submit-button").disabled = true;
    try {
      showDone(await api("/api/finish/submit", {
        confirmed_review: true, submit_to_research: true, answers, metadata
      }));
    } catch (err) {
      alertMessage(err.message || "Final storage failed; your earlier answers remain saved.");
    } finally {
      busy = false;
      find("submit-button").disabled = false;
    }
  });
  document.addEventListener("visibilitychange", schedule);
  open();
})();
