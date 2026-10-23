# C16 — Boer 1958 editorial preface: manuscript genealogy and the limits of three unanimous Paulus diagrams

**Research date:** 2026-10-23. **Scope:** Greek textual history, not proof that astrology predicts anything about humans. **0 untouched human validations, 0 changes to production scoring.** Continue from C15; no repetition of Munich/Florence/Vatican image acquisition.

## New directly consulted edition-level evidence

The 1958 Teubner critical edition **Emilie Boer, *Pauli Alexandrini Elementa apotelesmatica* (Eisagogika)** has a publicly searchable bibliographic/OCR preview of its Latin **Praefatio**, pp. VII–XI, at:

`https://dokumen.pub/paulus-alexandrinus-elementa-apotelesmatica.html`

**Access boundary:** C16 inspected the **edition's OCR preview of the editor's own Latin preface** and its visible bibliography; it did **not** successfully retrieve/visually inspect the original 1958 printed plates or the specific Greek chapter-32 table apparatus. The preview is machine-corrupted (Greek sigla, line breaks, accents, typography). Only legible editor-level propositions are admitted; ambiguous witness sigla beyond expressly readable `Z` and `Y` stay unresolved. Do not call this an autograph or a manuscript folio.

### 1. Boer explicitly lists the three independently photographed physical codices

In **Praefatio p. VII** Boer enumerates **Laurentianus gr. 28.7**, **Vaticanus gr. 1444**, and **Monacensis gr. 170** among source witnesses. These are exactly the three *physical* manuscript volumes C13–C15 observed independently at official libraries:

| Modern photo evidence | Edition-preface manuscript | Nature of the witness |
|---|---|---|
| Florence Plut. 28.7 folio 168v (C14) | Laur. gr. 28.7, **L** | Fourteenth-century physical manuscript |
| Vatican Vat. gr. 1444 digital opening 0202 (C15) | Vat. gr. 1444 | Sixteenth-century physical manuscript |
| Munich Cod. graec. 170 handwritten p65 (C13) | Mon. gr. 170 | Sixteenth-century physical manuscript |

This establishes the **bibliographic bridge** from the modern photographed objects to Boer's editorial manuscript inventory. It does not show that their **120 numbers are independently derived from 4th-century Paulus**.

### 2. The editor already warned about a common damaged source

In **Praefatio p. X** Boer writes the short Latin phrase **`Ex uno eodemque archetypo iam mutilo`**, completing the sentence with `verisimile`: Boer's assessment is that the surviving subarchetypes **probably descend from one already mutilated exemplar**. The hedge matters. This is **a textual-historical hypothesis advanced by the editor**, not proof of an exact stemma for the individual monomoiria chart.

In the surrounding preface Boer describes lacunae, altered chapter headings and sequences, transpositions and later scholia; the surviving work is not presented as a pristine original. This directly qualifies C13–C15's extremely strong **three physically distinct manuscripts, 120/120 Florence–Vatican and 119/119 legible Munich matching**: their perfect agreement can plausibly be inheritance from shared copied text, not three separate votes about the original intended formula.

**Never replace the observation** "three photographically checked physical manuscripts match" with the stronger, unjustified "three independent manuscript families confirm the ancient algorithm." Both documentary photo evidence and the editor's probable common archetype can be true simultaneously.

### 3. Editorially preferred manuscript targets: `Z` and `Y`

In **Praefatio pp. X–XI**, Boer states **`Recensioni ceteris utilior Z`**: in his judgment the **`Z` recension** preserves relatively useful readings, despite transmission corruption. The source inventory identifies `Z` with **Parisinus graecus 2506**. A separate `Y`, **Parisinus graecus 2425** (fifteenth century), is also valued by Boer as transmitting older-looking signs, numerical forms and an *Anakephalaiosis* (recapitulation), despite scribal spelling difficulties.

These are **editorial source-ranking leads**, not proof either witness holds a valid chapter-32 trigon table or that its figures supersede the three photographed copies. They are more discriminating next targets than simply downloading another late copy in the same chain.

**Dating discrepancy preserved:** the C15 research description previously used a *thirteenth-century* catalogue attribution for Paris gr. 2506; Boer's OCR preface labels `Z` **`s. XIV ineunt.` = early fourteenth century**. C16 records both descriptions and does not select one without consulting the object/codicological catalogue.

In **Praefatio p. IX** the OCR inventory also associates chapter `λβ` (trigonal monomoiria) with the short note **`Pauli est, non Heliodori`** for one excerpt. The **manuscript siglum is unreadable in the OCR**, so do not identify the physical codex or settle the attributed-Heliodorus commentary. This remains a source-directed *apparatus target*, not a final attribution.

### 4. What did *not* change: concrete negatives and unverified sources

Frozen source-only data from C15:

- Vatican vs Florence: **120/120** observed glyph agreements.
- Vatican vs readable Munich: **119/119**, with **Munich earth degree 28 unknown** (Vatican/Florence each show Mars).
- Against a naïve repeated first-octet system: **25 anomalies** (earth 28–30, water 9–30).
- Among **34 C04/C05 narrative vs printed diurnal-canon differences**: **11 narrative-only, 1 Greenbaum-only, 22 neither**.
- **Unverified:** exact 1958 edition printed *ch.32* diagram and line-by-line apparatus, Boer 1962 original Greek diagrams, whether `Z`/`Y` preserve this specific table, the full authentic **P.Oxy. LXI 4277** photograph, and a source-verified day/night rubric.
- **Access attempts:** Earlier Gallica/P.2506 requests returned HTTP403/404. This is an access-route limit, not proof the manuscript does not exist. Oxford SDS portal likewise did not yield an authenticated 4277 image. Do not substitute a paper's nearby closeup or another papyrus image.

**Research implication:** the key next step is no longer to count concordant late copies; it is to **test the source-lineage question against editor manuscript-family apparatus**, especially `Z` and `Y`, and compare any divergent *literal* ch.32 glyphs separately from a modern reconstructed algorithm. Choosing a "better" astrology reading based on known birth biographies is forbidden.

## Reproducible C16 records

- [C16 editor-premise and sigla uncertainty registry](PAULUS_C16_BOER_1958_PREFACE_GENEALOGY_V1.json) — primary editor *preface OCR* source, page span, short Latin excerpts, hypotheses vs verified facts, clear uninspected source controls.
- [C16 physical-vs-genealogical comparer](paulus_boer_preface_lineage_c16.py) — keeps C15 120/119 source agreements, adds editor's hypothetical common damaged archetype, promotes zero source rules.
- [C16 historical-source regression](test_hellenistic_c16_boer_preface.py) — tests editor/preface provenance, probable (not verified) archetype, priority of Z/Y, dating disagreement and gaps.

Command:

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Previous verified C15:** 122 source-only tests. C16 adds **11** new tests. **Full C16 regression verified: 133/133 historical-source tests PASSED (exit 0)** from the isolated worktree, after 122 retained and 11 C16 tests. A green fixture is not an independent visual authentication of noisy OCR, nor is any human predictive claim supported (**0 prospective human validations**).

**Next exact work:** Acquire/inspect a verifiable legal copy of Boer's **printed Greek chapter-32 apparatus/diagram**, distinguish the `Z` and `Y` object/date witnesses, and compare one materially different genealogy. Keep 1962 commentary and P.Oxy 4277 original photograph as separate, open research frontiers. Purchased Gansten Kindle ebook remains outside the extracted corpus; no Work-mode extraction.
