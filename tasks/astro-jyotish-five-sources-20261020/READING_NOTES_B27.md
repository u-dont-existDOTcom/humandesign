# JYOT B27 — Portuguese *Bṛhat Parāśara Horā Śāstra*: recoverable table of contents, omitted chapters and editorial imports (21 October 2026)

**Root task OPEN.** Twenty new source-only documentary annotations in `SOURCE_CANDIDATES_B27.json`; a reproducible topic map of the supplied 5,941-line CP1252 Portuguese text in `BPHS_PORTUGUESE_TOC_AND_OMISSIONS_B27.json`. This is **André Kerr's Portuguese adaptation from English, not an independently collated Parāśara Sanskrit critical edition**. No person chart or answer key was consulted. **Historical annotation total: 350+20 = 370; human predictive validations 0; production model promotions 0.**

## 1. The supplied Portuguese *translation's* table of contents is recoverable—but incomplete

The first 190 lines have alternate blank lines and 87 exact named entries at physical text lines **16,18,...,188**. The first 86 are astrological, medicalized or ritual topics; the last is **Conclusão**. Accent-insensitive casefolded equality matches **all 87** to the main body after line190. A monotonic physical-order rule resolves two earlier accidental matches: `Yogakarakas` is a section heading at **2816** (an earlier passing mention is at 2708), and `Combinações de Pobreza` belongs at **3327** (earlier mention 975). The index's `matched_body_heading_line_1based` and next-section exclusive boundary are source-navigation locators, **not verified ancient numbered chapter identities**.

Crucially, **at least nine additional *numbered* section headings appear in the body but not this table of contents**, among them:
- **9 Males de Nascença** line743 (pre-24 lifespan judgment limit);
- **28 Forças Isht e Kasht** line2528 (planet-benefic/malefic weights modifying period effects);
- **29 Padas das casas** line2562 (Arūḍha for all houses);
- **31 Argala e Intervenção Planetária** line2653;
- **37 Yogas da Lua** line3142;
- **74 Efeitos do Sudarshana Chakra** line5404 (also indexed in B20 already);
- **80 Horóscopo das Mulheres** line5533 and **81 Efeitos das Características dos Corpos Femininos** line5581;
- **84 Medidas Corretivas dos Planetas** line5743 (ritual remedy/propitiation).
A further **unnumbered** chapter-like heading `Remédio Para Nascimento Gandanta de Jyeshtha` appears at **line5892**, absent from the TOC. These are recorded as explicit body-only headings; the source could contain other nonmatching headings, and a number in a modern translated book is not a proof of the original Sanskrit manuscript's chapter structure. **The previous assertion that complete section navigation was unavailable is superseded by this *translator-edition navigation map*; original ancient chapter completeness remains unverified.**

## 2. Textual dependencies are even clearer in the omitted female-horoscope passage

**Line5533** begins `80. Horóscopo das Mulheres`, *between* TOC entries `Yogas de Vocação Espiritual` (line5509) and `Efeitos de Marcas no Corpo Para Homens e Mulheres` (line5682). The translated text distributes different targets across self, spouse and children, including harmful mortality, sexual and disability stereotypes. **Lines5539–5551** explicitly label **`Notas de Outros Livros`**, quoting respectively `Brihat Jatak`, `Phaldeepika de Mantreswara`, and `Jatakpari Jata`. The latter is the user's separately uploaded `Jātaka Pārijāta`, and overlaps gendered scope passages in other books. These are **editorically imported attributed paragraphs**, not automatically original Parāśara verses or three independent predictive witnesses.

The next body-only numbered section **81**, at line5581, switches from natal chart rules to **physiognomic body features** allegedly determining a woman's prosperity, family or virtue. A separate TOC section at **5682–5700** discusses **moles and asymmetrical hair whorls**, explicitly requiring physical observation unrelated to date/time/place. This is an extra-input method, not permitted to raise a birth-chart-only accuracy score.

## 3. Conflicting lifespan admission windows, and bounded sky inputs

The body-only chapter **9** line745 says a definitive lifespan judgment should wait until **age 24**. Previous B23 source-audit *Sarvārtha Cintāmaṇi* X.4 PDF240 and B25 *Jātaka Pārijāta* IV.1 PDF571 both warned astrologers against definitive judgment before **12**. These are **distinct age thresholds in different editions/schools**, with no verified clinical effect and no justification to choose one after a person's death history.

The headings include **84 planetary remedial measures** and **multiple distinct birth-omen time bases**. Line5782 explicitly says unfavorable alleged birth events can override an otherwise well-placed ascendant; its source categories include Amāvasyā, Kṛṣṇa Caturdaśī, Bhadra Karaṇa, matching a family member's nakṣatra, solar ingress, eclipses, Gandānta, and other tithi/yoga states. **Lines5849–5859** define three Gandānta categories (tithi, nakṣatra, Lagna) and the special Abhukta Mūla interval, with different ghatika boundary widths. A natal planetary chart alone does not contain all these family/visibility inputs, so a rigorous implementation must either explicitly collect and freeze them or declare a reduced **chart-only** subsystem.

## 4. Ritual, previous-life, fetal/sex discrimination and harmful source claims are not remedies

- **Lines5703–5739** explain supposed infertility or child loss through prior-birth curses and recommend ritual mitigation. These are religious causal assertions, **not explanations for reproductive conditions or evidence that rituals affect fertility**.
- **Line5743** marks a separate chapter of rituals/planetary symbols whose declared goal is better wealth, health and lifespan; source assertion, not established treatment efficacy.
- **Line5869** has an explicit `Nota:` statement about religious experts, an explanatory source layer distinct from surrounding verse claims.
- **Lines5872–5906** include accounts of avoiding or abandoning a child born in particular lunar positions, plus partner-family misfortune allegations. One narrow source exception says no adverse effect on a husband with no elder brother, but that does **not** establish the premise.
- **Line5913** presents a daughter after three sons (and a specified reversal) as a family curse. **Line5922** portrays congenital differences and unusual deliveries as communal bad omens with harsh exclusion of the mother/child. These are **harmful, discriminatory historical beliefs**, not true medical facts, ethical advice, or actionable personal forecasts.

The record preserves the author's/transmitted text's social claims **without endorsing** them. There is no medical, spiritual or psychosocial efficacy evidence in this upload to justify recommending ritual preparations, excluding babies, making family death predictions, or treating disability/child sex as a sign of misfortune.

## Counting and next frontier

The current independent reader stores **370 unique source-only documentation entries** after B27 (prior 350 + B27 20). `BPHS_PORTUGUESE_TOC_AND_OMISSIONS_B27.json` is a structural navigation artifact, and its 87 headings do **not** add 87 independent scientific results. The original Sanskrit chronological/manuscript recension and translation ancestry remain open. No existing birth-chart engine, questionnaire, participant response or other astrology reader’s source files were modified.

Next: provide a small reproducibility script to rederive exact headings and TOC/body matches from the CP1252 file; investigate any additional body-only nonnumbered headings; then return to deeply testable historical source rules, non-negative prediction/cancellation records, Sanskrit variants and independent blind matched-decoy evaluations. Maintain publisher-rights exclusion of full book bytes from public GitHub.