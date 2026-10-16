"use strict";
(function () {
  const find = id => document.getElementById(id);
  const alertBox = find("alert");
  const loading = find("loading");
  const panels = ["review", "questions", "done"];
  let csrf = "";
  let questions = [];
  let confirmed = false;
  let busy = false;

  function alertMessage(message) {
    alertBox.hidden = !message;
    alertBox.textContent = message || "";
  }
  function showPanel(name) {
    for (const pane of panels) {
      find(pane + "-panel").hidden = pane !== name;
      const step = find("step-" + pane);
      step.removeAttribute("aria-current");
      step.classList.toggle("complete", panels.indexOf(pane) < panels.indexOf(name));
      if (pane === name) step.setAttribute("aria-current", "step");
    }
    loading.hidden = true;
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
    if (!response.ok) {
      throw new Error(typeof data.detail === "string" ?
        data.detail : "The secure finishing request was not accepted.");
    }
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
    if (!items.length) {
      add(host, "p", "No descriptive observation was admitted by the independent reviewer. Do not infer missing traits.");
    }
    for (const e of items) {
      const card = add(host, "article", "", "evidence");
      const labels = Array.isArray(e.measurement_labels) ? e.measurement_labels : [];
      add(card, "h3", labels.join(" / ") || "Reported pattern");
      add(card, "p", e.observation || "No observation recorded.");
      const conditions = Array.isArray(e.conditions) ? e.conditions : [];
      if (conditions.length) add(card, "small", "Conditions: " + conditions.join("; "));
      if (e.time_frame) add(card, "small", "Time frame: " + e.time_frame);
      if (e.relationship_context) add(card, "small", "Context: " + e.relationship_context);
      for (const q of (Array.isArray(e.source_quotes) ? e.source_quotes : [])) {
        add(card, "blockquote", q.quote || "", "quote");
      }
    }
  }
  function showQuestions(data) {
    if (!Array.isArray(data) || data.length !== 3) {
      throw new Error("The fixed three-question supplement is unavailable.");
    }
    questions = data;
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
      add(host, "small", "Answer in your own words. Being unsure is a valid answer.", "subtle");
    });
    const values = [
      ["", "Choose one"], ["yes", "Yes"], ["no", "No"],
      ["unsure", "Not sure"], ["prefer_not_to_say", "Prefer not to say"]
    ];
    find("finish-form").querySelectorAll("select").forEach(select => {
      select.replaceChildren();
      for (const pair of values) {
        const opt = document.createElement("option");
        opt.value = pair[0]; opt.textContent = pair[1]; select.append(opt);
      }
    });
  }
  function showDone(receipt) {
    alertMessage("");
    showPanel("done");
    find("receipt-text").textContent = receipt.submission_id ?
      "Submission receipt: " + receipt.submission_id : "Your submission receipt is stored.";
  }
  function render(data) {
    csrf = data.csrf_token || "";
    if (data.submission && data.submission.submission_id) {
      showDone(data.submission);
      return;
    }
    if (data.status !== "ready") {
      throw new Error("This review is not ready to finish; return to the original saved GPT chat.");
    }
    find("review-context").textContent =
      "Independent review complete. " + (data.original_turn_count ?? 0) +
      " original entries and " + (data.clarification_count ?? 0) +
      " saved reviewer clarifications. Check the evidence below.";
    showEvidence(Array.isArray(data.review_summary) ? data.review_summary : []);
    showQuestions(data.cf003_questions);
    showPanel("review");
  }
  async function open() {
    try {
      const match = /^#token=([A-Za-z0-9_-]{32,128})$/.exec(location.hash);
      if (location.hash) history.replaceState(null, "", "/finish");
      if (match) await api("/api/finish/exchange", {token: match[1]});
      render(await api("/api/finish/state", undefined, "GET"));
    } catch (err) {
      loading.hidden = true;
      alertMessage(err.message || "Unable to open the private finishing session.");
    }
  }
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
      alertMessage("Confirm both the evidence and final storage permission first.");
      return;
    }
    const form = new FormData(event.target);
    const answers = questions.map(item => ({
      question_id: item.question_id,
      answer_text: String(form.get(item.question_id) ?? "").trim()
    }));
    if (answers.some(item => !item.answer_text)) {
      alertMessage("Answer all three questions; 'unsure' is a valid answer.");
      return;
    }
    const metadata = Object.fromEntries(
      ["rising_sign_previously_known", "previous_natal_chart_reading",
       "target_information_exposure"].map(key => [key, String(form.get(key) ?? "")])
    );
    busy = true;
    find("submit-button").disabled = true;
    alertMessage("");
    try {
      showDone(await api("/api/finish/submit", {
        confirmed_review: true, submit_to_research: true, answers, metadata
      }));
    } catch (err) {
      alertMessage(err.message || "Final storage failed; your original source remains unchanged.");
    } finally {
      busy = false;
      find("submit-button").disabled = false;
    }
  });
  open();
})();
