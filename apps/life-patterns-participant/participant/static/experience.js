"use strict";
/* Optional, post-review lived-experience module. No network or chart scoring. */
(function () {
  let bank = null;
  const el = id => document.getElementById(id);
  const itemNodes = Object.create(null);
  const select = (parent, prompt, choices, suffix, itemId) => {
    const label = document.createElement("label");
    label.textContent = prompt;
    const control = document.createElement("select");
    control.name = itemId + "-" + suffix;
    const empty = document.createElement("option");
    empty.value = "";
    empty.textContent = "Optional — choose if you wish";
    control.appendChild(empty);
    choices.forEach(([value, text]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = text;
      control.appendChild(option);
    });
    label.appendChild(control);
    parent.appendChild(label);
    return control;
  };

  function displayItem(item, target) {
    const box = document.createElement("fieldset");
    box.className = "experience-item";
    const title = document.createElement("legend");
    title.textContent = item.label;
    box.appendChild(title);
    const prompt = document.createElement("p");
    prompt.textContent = item.question;
    box.appendChild(prompt);
    const controls = {item, box};
    if (item.mode === "dual_meaning") {
      controls.personal = select(box, "Life feels meaningful to me personally",
        bank.meaning_options, "personal", item.id);
      controls.contribution = select(box, "I feel I make a difference to others or the world",
        bank.meaning_options, "contribution", item.id);
    } else {
      controls.value = select(box, item.mode === "frequency"
        ? "How often (past year)?" : "How predictable?", item.mode === "frequency"
          ? bank.frequency_options : bank.predictability_options, "value", item.id);
      if (item.mode === "frequency") {
        const intensities = document.createElement("div");
        controls.typical = select(intensities, "Typical intensity, when it happens (optional)",
          bank.intensity_options, "typical", item.id);
        controls.peak = select(intensities, "Strongest intensity it reaches (optional)",
          bank.intensity_options, "peak", item.id);
        box.appendChild(intensities);
        const update = () => {
          const v = controls.value.value;
          const meaningful = v && !["never","unknown","skip"].includes(v);
          intensities.hidden = !meaningful;
          if (!meaningful) {
            controls.typical.value = "";
            controls.peak.value = "";
          }
        };
        controls.value.addEventListener("change", update);
        update();
      }
    }
    const noteLabel = document.createElement("label");
    noteLabel.textContent = "Context, interpretation or earlier-life difference (optional)";
    controls.note = document.createElement("textarea");
    controls.note.rows = 3;
    controls.note.maxLength = 4000;
    controls.note.placeholder = "An example is never required.";
    noteLabel.appendChild(controls.note);
    box.appendChild(noteLabel);
    target.appendChild(box);
    itemNodes[item.id] = controls;
  }

  function setup(instrument) {
    if (!instrument || !Array.isArray(instrument.items) || instrument.items.length !== 8) {
      el("experience-optional").hidden = true;
      bank = null;
      return;
    }
    if (instrument.version !== "experience-meaning-v2-20261017") {
      el("experience-optional").hidden = true;
      bank = null;
      return;
    }
    bank = instrument;
    el("experience-optional").hidden = false;
    el("experience-context").textContent = bank.context_note;
    el("experience-core-items").replaceChildren();
    el("experience-additional-options").replaceChildren();
    el("experience-additional-items").replaceChildren();
    bank.items.forEach(item => {
      const holder = bank.core_ids.includes(item.id)
        ? el("experience-core-items") : el("experience-additional-items");
      displayItem(item, holder);
      if (!bank.core_ids.includes(item.id)) {
        itemNodes[item.id].box.hidden = true;
        const label = document.createElement("label");
        label.className = "checkline";
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "experience-topic-" + item.id;
        checkbox.addEventListener("change", () => {
          itemNodes[item.id].box.hidden = !checkbox.checked;
        });
        label.appendChild(checkbox);
        const text = document.createElement("span");
        text.textContent = item.label;
        label.appendChild(text);
        el("experience-additional-options").appendChild(label);
        itemNodes[item.id].topicToggle = checkbox;
      }
    });
    el("experience-opt-in").checked = false;
    el("experience-questions").hidden = true;
    el("experience-opt-in").addEventListener("change", () => {
      el("experience-questions").hidden = !el("experience-opt-in").checked;
    });
  }

  function responseFor(item) {
    const c = itemNodes[item.id];
    if (c.topicToggle && !c.topicToggle.checked) {
      return {question_id:item.id,state:"NOT_ASKED"};
    }
    const note = c.note.value;
    const answer = {question_id:item.id,state:"NOT_ASKED"};
    if (item.mode === "dual_meaning") {
      const personal = c.personal.value || "not_answered";
      const contribution = c.contribution.value || "not_answered";
      if (personal !== "not_answered" || contribution !== "not_answered") {
        answer.state = "ANSWERED";
        answer.values = {personal_meaning:personal,perceived_contribution:contribution};
      }
    } else {
      const v = c.value.value;
      if (v === "never") {
        answer.state = "NEVER";
      } else if (v === "unknown") {
        answer.state = "UNKNOWN";
      } else if (v === "skip") {
        answer.state = "SKIPPED";
      } else if (v) {
        answer.state = "ANSWERED";
        answer.value = v;
        if (item.mode === "frequency") {
          if (c.typical.value) answer.typical_intensity = c.typical.value;
          if (c.peak.value) answer.peak_intensity = c.peak.value;
        }
      }
    }
    if (note.trim() && answer.state !== "NOT_ASKED") answer.note = note;
    return answer;
  }

  function collect() {
    if (!bank || !el("experience-opt-in").checked) return null;
    const selected = bank.optional_ids.filter(id => itemNodes[id].topicToggle.checked);
    const responses = bank.items.map(responseFor);
    for (const response of responses) {
      const controls = itemNodes[response.question_id];
      const chosen = !controls.topicToggle || controls.topicToggle.checked;
      if (chosen && response.state === "NOT_ASKED" && controls.note.value.trim()) {
        throw new Error("Choose a response for " + controls.item.label +
          " (including Not sure or Skip), or clear its note before finishing.");
      }
    }
    return {
      schema:"life-patterns-experience-meaning-addendum-v2",
      instrument:bank.version,
      research_use_consented:true,
      collection_mode:"railway_finish",
      status:"post_review_exploratory_not_scored",
      topics_selected:selected,
      responses
    };
  }
  function sourceCatalog() {
    if (!bank || !el("experience-opt-in").checked) return [];
    return bank.items.map(responseFor).flatMap((response, index) => {
      if (!["ANSWERED", "NEVER", "UNKNOWN"].includes(response.state) ||
          !response.note || !response.note.trim()) return [];
      const item = bank.items.find(item => item.id === response.question_id);
      return [{
        source_ref: "/experience/responses/" + index + "/note",
        question_text: item.question,
        answer_text: response.note,
      }];
    });
  }
  window.LifePatternsExperience = {setup,collect,sourceCatalog};
})();
