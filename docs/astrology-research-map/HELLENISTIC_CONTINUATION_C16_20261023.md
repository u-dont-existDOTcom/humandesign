# Hellenistic source continuation C16 — durable editor/stemma checkpoint

**Date 2026-10-23. Research outcome OPEN. Human predictive validations 0.** Source-critical computation and transmission only; no change to natal/relationship production scoring, other traditions, or existing cross-tradition research map.

## Mandatory recovery

Re-read live default-branch `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` and `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md` and this checkpoint. Previous C01–C15 is preserved; **do not rerun the three manuscript acquisitions**.

- **C15 accepted exact source base:** `d2ad5b3ad7022b6f66c57471ed0bb92decad5693`, `research/astro-hellenistic-c15-third-witness-20261023`.
- **C16 isolated child branch:** `research/astro-hellenistic-c16-boer-preface-20261023`. Parent research-integration branch `research/astro-missing-book-audit-20261022` stays integrator-owned. Do not merge any scoring rule.
- Canonical new source artifacts: [C16 editorial finding report](HELLENISTIC_SOURCE_C16_BOER_EDITORIAL_ARCHETYPE_20261023.md), [Boer 1958 source-provenance registry](PAULUS_C16_BOER_1958_PREFACE_GENEALOGY_V1.json), [source-interpretation comparison](paulus_boer_preface_lineage_c16.py), [source-only tests](test_hellenistic_c16_boer_preface.py).
- A C16 README pointer has been added; C15/C14 and other research lanes remain untouched.

## New fact genuinely advanced

For the **first time in this lane**, examined a publicly searchable **OCR preview of Emilie Boer's own 1958 Teubner critical edition preface** (pp VII–XI), rather than only summaries citing the edition. Source `https://dokumen.pub/paulus-alexandrinus-elementa-apotelesmatica.html`. **This was OCR, not a verified original edition page image or the ch32 apparatus**.

The editor's preface explicitly names the **Florence Laur. gr. 28.7, Vatican gr.1444, and Munich gr.170** manuscripts already physically photographed in C13–C15. More importantly, **Boer conjectures probable derivation of surviving subarchetypes from *one already mutilated archetype***, using `verisimile`. This is an **editor's conjecture, not a proven genealogical stemma**. It **undercuts treating three photographed documents as three independent ancient source families**. The original 120/119 glyph agreements are still fully true as *observations*.

Boer indicates two potentially more valuable textual targets: **`Z` = Parisinus gr.2506** (editor's relatively preferred early-14th-century recension) and **`Y` = Parisinus gr.2425** (15th-century witness with arguably older graphic/number forms and recapitulation). Do not assume their ch32 tables exist or differ; neither has been opened this batch. Previous C15 used a **13th-century** dating for Paris 2506; preserve dating disagreement until independent codicology/source review.

An OCR inventory near chapter **λβ trigonal monomoiria** includes **`Pauli est, non Heliodori`** for a particular excerpt. **Witness siglum unreadable** in OCR; global Heliodorus/Paulus attribution not adjudicated.

## Prior exact source negative results unchanged

- Three physical original manuscripts: Vatican vs Florence **120/120** matching, Vatican vs readable Munich **119/119** matching; Munich **earth d28 still null**.
- Naïve eight-slot repetition contradicts **25** source cells: earth d28–30 + water d9–30.
- Pre-existing 34 C04/C05 Greenbaum-vs-narrative source differences compared with manuscripts: **11 narrative-only / 1 corrected-only / 22 neither**.
- Boer **1958 actual printed Greek ch32 apparatus** not read; **1962 attributed Heliodorus/Olympiodorus** apparatus not read. Exact P.Oxy. LXI **4277 full authentic papyrus photograph** not read (only prior published-source comparison **1/3**, two negatives). No verified manuscript day/night rubric.
- Zero untouched real-human predictive tests. Do not use a known biography to prefer source variants. Purchased Amazon Gansten *Primary Directions* Kindle ebook remains outside extracted corpus: **never use Work to extract**.

## Exact tests / next steps

Focused:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c16_*.py' -v
```
C16 focused **11/11 PASSED after repairing a test expectation**. **Verified C16 full historical-source suite: 133/133 PASSED (exit 0)** from the isolated C16 worktree; 122 prior tests plus 11 C16. Zero real-human predictive validations.

1. Actually inspect legible **Boer 1958 ch32 printed source and variant apparatus**; preserve source reading, explicit editor correction, later reconstruction separately. Find lawful institutional scan or use allowed small critical-page view; no scan copying into Git.
2. Pursue **Z Paris gr2506** and **Y Paris gr2425** original images to test alternative text lineage (not by assuming these contain tables). Old Gallica route HTTP403 was a transport-specific failure; do not invent absence.
3. Inspect actual **Boer 1962** commentator edition where possible and independently identify **P.Oxy. 4277 original photo** through EES/Oxford holding record; retain failures and unread sources.

**Resume one-liner:** C16 clarified editorial genealogy from Boer 1958 preface; probable shared damaged archetype means 3 photographed equal codices ≠ 3 independent ancient authorities. Locate variant `Z`/`Y` and actual Greek ch32 apparatus next; no production rule, no human prediction.
