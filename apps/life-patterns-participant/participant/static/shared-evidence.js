"use strict";
/* Optional source collection. No chart rules, network calls or scoring. */
(function () {
  const el = id => document.getElementById(id);
  const choices = [
    ["ANSWERED", "Answer in my own words"],
    ["CONTEXT_DEPENDENT", "It depends on the context"],
    ["NO_OPPORTUNITIES", "I have not had the relevant opportunities"],
    ["NEVER", "This has never happened in the period asked about"],
    ["NOT_APPLICABLE", "This does not apply to me"],
    ["UNCERTAIN", "I am unsure"],
    ["SKIPPED", "I prefer to skip this question"],
    ["ALREADY_COVERED", "An earlier answer already covers this"],
  ];
  const substantive = new Set(["ANSWERED", "CONTEXT_DEPENDENT", "UNCERTAIN"]);
  let bank = null, prior = [], getAdditionalSources = () => [];
  let sittings = [], current = null, active = null, nextIndex = 0, stored = false;
  const nodes = new Map();

  function add(parent, tag, text, className) {
    const node = document.createElement(tag);
    node.textContent = text || "";
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  }
  function message(text) {
    el("shared-message").textContent = text || "";
    el("shared-message").hidden = !text;
  }
  function optedIn() { return Boolean(bank && el("shared-opt-in").checked); }
  function itemFor(id) {
    return [...bank.questions, ...bank.optional_microprobes].find(item => item.id === id);
  }
  function priorResponses() { return sittings.flatMap(sitting => sitting.responses); }
  function askedIds() {
    return new Set(priorResponses().filter(row => row.state !== "NOT_ASKED")
      .map(row => row.question_id));
  }
  function updateSelection() {
    const selected = [...nodes.values()].filter(node => node.checked);
    el("shared-selection-count").textContent = selected.length + " of up to 5 topics selected. You may decline the entire section.";
    const previous = askedIds();
    for (const [id, node] of nodes) {
      node.disabled = previous.has(id) || (!node.checked && selected.length >= 5);
    }
    el("shared-start").disabled = !selected.length;
  }
  function showSelection() {
    active = null;
    current = null;
    el("shared-selection").hidden = false;
    el("shared-question").hidden = true;
    el("shared-complete").hidden = true;
    for (const node of nodes.values()) node.checked = false;
    updateSelection();
  }
  function sources() {
    const collected = [];
    sittings.forEach((sitting, si) => sitting.responses.forEach((row, ri) => {
      if (active && active.editing &&
          (si > active.sittingIndex || (si === active.sittingIndex && ri >= active.responseIndex))) return;
      if (!["ANSWERED", "CONTEXT_DEPENDENT", "NO_OPPORTUNITIES", "NEVER", "NOT_APPLICABLE", "UNCERTAIN"].includes(row.state) ||
          typeof row.answer_text !== "string" || !row.answer_text.trim()) return;
      collected.push({
        source_ref: "/shared/sittings/" + si + "/responses/" + ri + "/answer_text",
        question_text: row.question_text, answer_text: row.answer_text,
      });
    }));
    return [...prior, ...getAdditionalSources(), ...collected];
  }
  function showSource() {
    const source = sources().find(item => item.source_ref === el("shared-source").value);
    el("shared-source-quote").textContent = source ? source.answer_text : "";
    el("shared-source-excerpt").value = source && source.answer_text.length <= 20000 ? source.answer_text : "";
    if (source && source.answer_text.length > 20000) {
      message("This earlier answer is long. Copy an exact relevant excerpt into the box below; the original stays intact.");
    }
  }
  function refreshSources() {
    const select = el("shared-source");
    select.replaceChildren();
    const blank = add(select, "option", "Choose the earlier answer that covers this");
    blank.value = "";
    sources().forEach((source, i) => {
      const option = add(select, "option", (i + 1) + ". " + source.question_text);
      option.value = source.source_ref;
    });
    el("shared-source-quote").textContent = "";
    el("shared-source-excerpt").value = "";
  }
  function stateChanged() {
    const state = el("shared-state").value;
    el("shared-answer-label").hidden = ["SKIPPED", "ALREADY_COVERED"].includes(state);
    el("shared-source-label").hidden = state !== "ALREADY_COVERED";
  }
  function showQuestion(id, kind = "main", distinction = null) {
    const item = itemFor(id);
    active = {id, kind, distinction};
    el("shared-state").disabled = false;
    el("shared-stop").hidden = false;
    el("shared-cancel-edit").hidden = true;
    el("shared-selection").hidden = true;
    el("shared-complete").hidden = true;
    el("shared-question").hidden = false;
    el("shared-question-title").textContent = item.label || "Optional clarification";
    el("shared-question-text").textContent = kind === "main"
      ? item.question : (item.optional_followup || item.followup);
    el("shared-answer").value = "";
    el("shared-feedback").value = "";
    el("shared-state").value = "ANSWERED";
    refreshSources();
    stateChanged();
    const left = current.topics_selected.length - nextIndex;
    el("shared-progress").textContent = kind === "main" && bank.questions.some(q => q.id === id)
      ? (nextIndex + 1) + " of " + current.topics_selected.length + " chosen topics in this sitting; " +
        left + " topic(s) to answer or skip. Roughly " + left + "–" + (left * 3) + " answering minutes, depending on your answers."
      : "One optional detail you requested. You may skip it; no further detail is required.";
    message("");
  }
  function responseFromControls(forceSkip = false) {
    const state = forceSkip ? "SKIPPED" : el("shared-state").value;
    const row = {question_id: active.id, prompt_kind: active.kind, state};
    if (active.kind === "followup") row.unresolved_distinction = active.distinction;
    const feedback = el("shared-feedback").value;
    if (feedback.trim()) row.process_feedback = [feedback];
    if (state === "ALREADY_COVERED") {
      const source = sources().find(item => item.source_ref === el("shared-source").value);
      if (!source) throw new Error("Choose an actual earlier answer, or use another response option.");
      const quote = el("shared-source-excerpt").value;
      if (!quote.trim() || quote.length > 20000 || !source.answer_text.includes(quote)) {
        throw new Error("Use an exact contiguous excerpt of the selected earlier answer, up to 20,000 characters.");
      }
      row.source_ref = source.source_ref;
      row.source_quote = quote;
    } else {
      row.question_text = el("shared-question-text").textContent;
      if (state === "SKIPPED") row.answer_text = null;
      else {
        const answer = el("shared-answer").value;
        if (!answer.trim() && ["ANSWERED", "CONTEXT_DEPENDENT"].includes(state)) {
          throw new Error("Write your answer, choose another response, or skip this question.");
        }
        // A deliberately chosen response label is itself source, never a default negative.
        row.answer_text = answer.trim() ? answer : choices.find(pair => pair[0] === state)[1];
      }
    }
    return row;
  }
  function showComplete() {
    active = null;
    el("shared-question").hidden = true;
    el("shared-selection").hidden = true;
    el("shared-complete").hidden = false;
    el("shared-progress").textContent = "This optional sitting is complete. No more questions are required. You can submit the whole interview now.";
    const detail = el("shared-detail-options");
    detail.replaceChildren();
    const blank = add(detail, "option", "Only if a distinction in your answer remains unresolved");
    blank.value = "";
    const admitted = new Set(current.probe_admissions.map(p => p.probe_id));
    const previouslyAsked = askedIds();
    const skipped = new Set(current.responses.filter(row => row.state === "SKIPPED").map(row => row.question_id));
    for (const response of current.responses) {
      if (response.prompt_kind !== "main" || !substantive.has(response.state) || skipped.has(response.question_id)) continue;
      const item = itemFor(response.question_id);
      if ((item.optional_followup || item.followup) &&
          !current.responses.some(r => r.question_id === item.id && r.prompt_kind === "followup")) {
        const option = add(detail, "option", "More detail: " + (item.label || "your clarification"));
        option.value = "followup|" + item.id;
      }
      if (current.probe_admissions.length >= 2) continue;
      for (const probe of bank.optional_microprobes) {
        if (!probe.related_topics.includes(item.id) || !(item.conditional_new_probe_ids || []).includes(probe.id) ||
            admitted.has(probe.id) || previouslyAsked.has(probe.id)) continue;
        const option = add(detail, "option", "Related clarification: " + probe.question);
        option.value = "probe|" + probe.id + "|" + item.id;
      }
    }
    el("shared-detail-reason").value = "";
    el("shared-details").hidden = detail.options.length <= 1;
    el("shared-download").disabled = false;
    renderDrafts();
    message("");
  }
  function renderDrafts() {
    const host = el("shared-draft-answers");
    host.replaceChildren();
    sittings.forEach((sitting, si) => sitting.responses.forEach((row, ri) => {
      if (["NOT_ASKED", "FUTURE_PENDING"].includes(row.state)) return;
      const box = add(host, "article", "", "evidence");
      add(box, "h4", itemFor(row.question_id).label || "Optional clarification");
      add(box, "p", row.answer_text || row.source_quote || "Skipped");
      const button = add(box, "button", "Edit this draft", "secondary");
      button.type = "button";
      button.addEventListener("click", () => editDraft(si, ri));
    }));
  }
  function editDraft(si, ri) {
    const row = sittings[si].responses[ri];
    current = sittings[si];
    showQuestion(row.question_id, row.prompt_kind, row.unresolved_distinction);
    active.editing = true;
    active.sittingIndex = si;
    active.responseIndex = ri;
    // Preserve the response state and its dependency meaning; repair text/source only.
    el("shared-state").value = row.state;
    el("shared-state").disabled = true;
    el("shared-answer").value = row.answer_text || "";
    el("shared-feedback").value = (row.process_feedback || []).join("\n");
    refreshSources();
    if (row.state === "ALREADY_COVERED") {
      el("shared-source").value = row.source_ref;
      const source = sources().find(item => item.source_ref === row.source_ref);
      el("shared-source-quote").textContent = source ? source.answer_text : "";
      el("shared-source-excerpt").value = row.source_quote;
    }
    stateChanged();
    el("shared-stop").hidden = true;
    el("shared-cancel-edit").hidden = false;
    el("shared-progress").textContent = "Editing an optional draft before final submission. Check any later answer that reuses this source.";
  }
  function returnFromEdit() {
    current = sittings[sittings.length - 1];
    nextIndex = current.topics_selected.length;
    showComplete();
  }
  function saveCurrent(endSitting = false) {
    try {
      if (!active || !current) return;
      const row = responseFromControls(endSitting);
      if (active.editing) {
        current.responses[active.responseIndex] = row;
        returnFromEdit();
        return;
      }
      current.responses.push(row);
      const isTopic = bank.questions.some(item => item.id === active.id);
      if (active.kind === "main" && isTopic) nextIndex++;
      if (endSitting) {
        for (const id of current.topics_selected.slice(nextIndex)) {
          current.responses.push({question_id: id, prompt_kind: "main", state: "NOT_ASKED"});
        }
        nextIndex = current.topics_selected.length;
      }
      if (nextIndex < current.topics_selected.length) showQuestion(current.topics_selected[nextIndex]);
      else showComplete();
    } catch (err) { message(err.message); }
  }
  function collect() {
    if (!optedIn()) return null;
    if (active) throw new Error("Save or skip the current optional question before submitting. Your text is still here.");
    if (!sittings.length) return null;
    return {
      schema: "life-patterns-shared-evidence-addendum-v1",
      instrument: bank.version,
      research_use_consented: true,
      collection_mode: "railway_finish",
      status: "post_review_development_not_scored",
      sittings: JSON.parse(JSON.stringify(sittings)),
    };
  }
  function setup(instrument, earlierSources, additionalSources) {
    if (!instrument || instrument.version !== "shared-life-topics-v3-20261026" ||
        !Array.isArray(instrument.questions) || instrument.questions.length !== 23 ||
        !Array.isArray(instrument.optional_microprobes) || instrument.optional_microprobes.length !== 7) {
      el("shared-optional").hidden = true;
      return;
    }
    bank = instrument;
    prior = Array.isArray(earlierSources) ? earlierSources : [];
    getAdditionalSources = additionalSources || (() => []);
    el("shared-optional").hidden = false;
    el("shared-controls").hidden = true;
    el("shared-opt-in").checked = false;
    const host = el("shared-topic-options");
    host.replaceChildren();
    nodes.clear();
    for (const item of bank.questions) {
      const label = add(host, "label", "", "checkline");
      const input = document.createElement("input");
      input.type = "checkbox";
      input.name = "shared-topic-" + item.id;
      input.addEventListener("change", updateSelection);
      label.appendChild(input);
      add(label, "span", item.label);
      nodes.set(item.id, input);
    }
    const states = el("shared-state");
    states.replaceChildren();
    for (const [value, label] of choices) add(states, "option", label).value = value;
    showSelection();
  }
  el("shared-opt-in").addEventListener("change", () => {
    el("shared-controls").hidden = !optedIn();
    message("");
  });
  el("shared-start").addEventListener("click", () => {
    try {
      // This callback also verifies that CF003 is answered before the addendum.
      getAdditionalSources();
      const ids = [...nodes].filter(([, node]) => node.checked).map(([id]) => id);
      if (!ids.length || ids.length > 5) throw new Error("Choose between one and five optional topics, or decline the section.");
      current = {sitting_id: crypto.randomUUID(), topics_selected: ids, probe_admissions: [], responses: []};
      sittings.push(current);
      nextIndex = 0;
      el("shared-download").disabled = true;
      showQuestion(ids[0]);
    } catch (err) { message(err.message); }
  });
  el("shared-state").addEventListener("change", stateChanged);
  el("shared-source").addEventListener("change", showSource);
  el("shared-cancel-edit").addEventListener("click", returnFromEdit);
  el("shared-next").addEventListener("click", () => saveCurrent(false));
  el("shared-stop").addEventListener("click", () => saveCurrent(true));
  el("shared-more").addEventListener("click", showSelection);
  el("shared-detail-start").addEventListener("click", () => {
    const parts = el("shared-detail-options").value.split("|");
    const reason = el("shared-detail-reason").value;
    if (!parts[0] || !reason.trim()) {
      message("Choose the detail and say which distinction remains unresolved. You can also finish without it.");
      return;
    }
    if (parts[0] === "probe") {
      current.probe_admissions.push({probe_id: parts[1], parent_topic_id: parts[2], unresolved_distinction: reason});
    }
    el("shared-download").disabled = true;
    showQuestion(parts[1], parts[0] === "followup" ? "followup" : "main", reason);
  });
  el("shared-download").addEventListener("click", () => {
    try {
      const record = collect();
      if (!record) return;
      const url = URL.createObjectURL(new Blob([JSON.stringify(record, null, 2) + "\n"], {type: "application/json"}));
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "life-patterns-shared-evidence-addendum-v1.json";
      anchor.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (err) { message(err.message); }
  });
  window.addEventListener("beforeunload", event => {
    if (!stored && optedIn() && sittings.length) {
      event.preventDefault();
      event.returnValue = "";
    }
  });
  window.LifePatternsSharedEvidence = {setup, collect, markStored: () => { stored = true; }};
})();
