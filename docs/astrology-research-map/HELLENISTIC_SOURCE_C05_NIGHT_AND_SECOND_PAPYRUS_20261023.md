# Hellenistic primary-source reader C05 — Paulus nocturnal variants, second papyrus, and Hephaistio “face”

23 October 2026 · **Research only, not human prediction** · All branches other than the Hellenistic source lane untouched

## Root objective, historical evidence layers and access limits

Continue the user's acquired Hellenistic astrology books and source comparison, map only historically explicit algorithms, and ensure contradictions remain visible for subsequent prospective empirical testing. C04 was the accepted start; **no natal-model scoring or real-human validation has been run**, and the purchased Kindle *Primary Directions* was not accessed.

Original ancient Greek author ≠ modern critical Greek edition ≠ Eulogikon normalized corpus ≠ Greek-to-English translation ≠ later commentator ≠ modern reconstruction ≠ a working human predictor. Preserve each separately. This source reader checks line/section and numerals; it does **not** claim to have inspected Pingree's Teubner critical apparatus or ancient manuscript images.

## 1. Paulus's actual nocturnal trigon rule located in Greek

**Direct Greek source:** [Paulus of Alexandria, *Eisagogika* (Introduction), ch.2 and ch.32, Eulogikon](https://eulogikon.org/works/paul-alexandria-astrology-sum-aa) / [markdown](https://eulogikon.org/works/paul-alexandria-astrology-sum-aa.md), HTTP 200 and complete source text personally read. Oct 23 UTF-8 snapshot **181,883 bytes**, SHA-256 `5403036ff14392f80025f9730f449d5b297ea4fee2c8e9e41f675385454d8c1c`. The independent [Eulogikon GitHub corpus export](https://github.com/eulogikon/ancient-greek-texts/blob/main/grc/paul-alexandria-astrology-sum-aa.grc.md) explicitly contains the same passage; observed GitHub blob SHA `d1f433537fa27fccecc2ffd38432d4a1edc4c556`. **Not independent ancient witnesses**, but useful archive/source identity parity. The repository does not provide a per-work apparatus naming a precise Greek base edition. Eulogikon's notice explicitly disclaims errors and source contamination.

Paulus ch.2 independently specifies **each triplicity's day and night rulers**; ch.32 prescribes one degree per planet while skipping previously used planets until the seven-star set is complete. It then states that for *night* the order is exchanged, illustrating the first trigon (Aries/Leo/Sagittarius) with **Jupiter followed by Sun**. This is an explicit ancient-text line **not available in the owner's acquired modern book's *missing Olympiodorus commentary*** but **already present in Paulus ch.32 itself**. The earlier C04 phrasing “no original nocturnal instruction available” is thereby superseded; a fully collated nighttime *manuscript table* is still unavailable.

### Greek author's pairs (ch.2)

| Triplicity / signs | First daytime ruler | First nighttime ruler |
|---|---|---|
| Fire / Aries, Leo, Sagittarius | Sun | Jupiter |
| Earth / Taurus, Virgo, Capricorn | Venus | Moon |
| Air / Gemini, Libra, Aquarius | Saturn | Mercury |
| Water / Cancer, Scorpio, Pisces | Venus | Mars |

With fixed trigon order fire → earth → air → water, rotate to the target trigon, use the relevant sect's order for each pair, and **skip any planet previously assigned in the seven-planet sequence**. This is a modern *explicit deterministic reconstruction* of Paulus's words, not evidence that every surviving edited table agrees with it. Complete reconstructed examples:
- Fire day: Sun → Jupiter → Venus → Moon → Saturn → Mercury → Mars.
- Fire night: Jupiter → Sun → Moon → Venus → Mercury → Saturn → Mars.
- Water day: Venus → Mars → Sun → Jupiter → Moon → Saturn → Mercury.
- Water night: **Mars → Venus → Jupiter → Sun → Moon → Mercury → Saturn**.

A valuable independent scholarly secondary check is **Cristian Tolsa**, “New Zodiacal Divisions in P.Oxy. LXI 4277,” *Zeitschrift für Papyrologie und Epigraphik* 203 (2017), **pp.192–198, esp. p197 note 10** (the accessible re-hosted text explicitly presents the exact nighttime water order). Tolsa also distinguishes a *later* Olympiodoran variant that reverses daytime assignments in adjacent pairs, described as a variation or possible corruption. **This later commentary variant is not identical to an independently verified entire night table.** The original article can be obtained from its scholarly publisher or library if necessary; the evidence examined here is a readable reposted scholarly text, not the papyrus facsimile.

### Material discrepancy with owned corrected Greenbaum daytime table

**Edition:** Dorian Greenbaum, *Late Classical Astrology: Paulus Alexandrinus and Olympiodorus*, **Paulus ch.32 printed pp66–69**, day `Canon of Monomoiria by Trigon` printed **p67**, photographed owner-acquired PDF **leaf83**. It has a corrected daytime allocation and explicitly warns about manuscript-table corruption in the translator's notes. The Greek *narrative algorithm* and this *edited day table* agree on first 30 rows of **fire** and **earth**, but differ in **16/30 air** and **18/30 water** degree entries: **34/120 cells**. The ancient *scholion* example **Cancer ordinal degree 8 = Venus** agrees with the Greek narrative reconstruction, while the Greenbaum printed table gives **Mars**. These must remain explicit competing historical/editorial witnesses; neither may win by checking a known person's chart.

[Executable separate C05 Greek narrative](paulus_trigon_narrative_c05.py), [six deterministic tests](test_hellenistic_c05_night.py). Strict input guards reject unsupported sects and noninteger degrees. **A reconstructed 120-cell nocturnal *variant*** can now be generated, but its status is `DERIVED_NOT_CRITICALLY_COLLATED`, and it must not be described as an authenticated direct ancient nighttime table. The older [C04 edited day canon](paulus_monomoiria_source_c04.py) remains unchanged.

## 2. New independent documentary horoscope: P.Oxy. LXI 4277

**Historical source:** a damaged Oxyrhynchus papyrus, late **2nd or early 3rd century CE** by handwriting, discussed in Tolsa 2017, **p.197**. Not the 319 CE P.Berl. 9825 from C04. Three readable papyrus attributions are available for direct numerical comparison (the original photograph was not fetched here):

| Recorded object and longitude | Preserved monomoiria | Paulus *by-sign* ruler, proper ordinal | Result |
|---|---|---|---|
| Mercury at Capricorn **6°22′** | Venus | Moon | **Mismatch** |
| Midheaven at Taurus **27°08′** | Mercury | Sun | **Mismatch** |
| Lower Midheaven at Scorpio **27°08′** | Jupiter | Jupiter | **Match** |

Paulus's simpler **by-sign** rule (not the trigonal system) assigns the first *ordinal* degree to that sign's domicile lord, then proceeds Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon in a seven-planet cycle. Therefore **6°22′ lies in ordinal degree 7** and **27°08′ in ordinal degree 28**. Simulating the common historically attested but mathematically wrong “completed-degrees as ordinal” convention gives Mercury/Mars/Saturn, **0/3** matching these same papyrus labels. Under correct ordinal counting only **1/3** match, and **2 mismatches remain**.

This is **not evidence that Paulus by-sign always wins or should be adjusted**. Tolsa's *mixed* alternative combines different systems, and the paper explicitly notes ancient computational inconsistency. Changing formula **after** examining the manuscript's labels would be an exploratory reconstruction, not an independent success. Likewise C04's P.Berl. 9825 yielded **6/7** including an explicit Mercury failure; two different ancient records must **not be combined into a retrospective human-prediction accuracy score**.

[Exact three-row documentary comparison code](oxy4277_monomoiria_audit_c05.py) and [three tests](test_hellenistic_c05_oxy4277.py). The entry `SOURCE_REPORTED_READING_NOT_FACSIMILE_VERIFIED` continues until original line image / critical apparatus confirmation. The author's own historical and interpretative conclusions are secondary to the papyrus' damaged primary text.

An additional paper, **Michael W. Zellmann-Rohrer (2024), “Three Deluxe Horoscopes,” *Archiv für Papyrusforschung* 70(2), pp283–316**, is bibliographically and abstract-verified via Freie Universität Berlin repository [record](https://refubium.fu-berlin.de/handle/fub188/49674). It supplies three further potentially relevant ancient documents. Its actual PDF is **access-restricted by an Anubis challenge** in this session, so it was **not read** and no exact outcomes or additional papyrus measurements from it were scored. Do not label it completed or bypass access control.

## 3. Hephaistio Book I “own face” is now lexically distinguished in Greek

**Owner English scan:** Hephaistio, *Apotelesmatics* I, Schmidt/Hand, ch.19, printed p36 / PDF p52 (checked C03). **Greek transcription** of Hephaistio Book I chapter 19 from Eulogikon (Hephaistio source hash retained C04, `2265293a6088920adbb487fe91ede7d275db21674da6b997fb98a9584a6c6d63`) has a chapter headed **`Περὶ ἰδιοπροσωπίας`** and describes preserving a planet's geometrical relation to Sun or Moon comparable to its domicile's configuration. Separately, the same work has explicit **`δεκαν-`** discussion for 10-degree decans elsewhere. These are demonstrably **distinct Greek technical terms**. Therefore do not translate Hephaistio's *own face* mechanically into Dorotheus's fifth `image [decan]` dignity; source synonymy has **not** been established.

### Strict research states

- `PAULUS_CH32_GREEK_NIGHT_RECONSTRUCTION`: source-backed opening **but derived full sequences**, not collation of all Greek manuscript diagrams.
- `GREENBAUM_CORRECTED_DAY_TABLE`: directly inspected 120-cell edited witness, **34 disputed cells** against narrative.
- `P_OXY_4277_BY_SIGN_DOCUMENT`: second independent ancient papyrus; **1/3** direct arithmetic matches, **2 preserved disagreements**, no clinical/personal forecast.
- `HEPHAISTIO_BOOK_I_OWN_FACE`: Greek terminology now distinguishes **prosopon-based geometry** from **decanos-based tens**, with absolute identity/etymology not extrapolated.
- Eulogikon Greek line transcription **may derive** from Pingree or other modern editorial text, but no exact collation trace was verified. It must not count as an independently collated manuscript.
- Scientific parent outcome **OPEN**; forward-blind consenting human validation **0**; neither chart model nor user-life labels changed.

## 4. Verification and next frontier

C05 source-specific [night reconstruction tests](test_hellenistic_c05_night.py): **6/6 passed** from GitHub branch files. New independent P.Oxy 4277 [documentary tests](test_hellenistic_c05_oxy4277.py): **3/3 passed**. Tests establish precise source arithmetic, preserve disagreements, and guard against unsupported data. This report is not a full canonical-release approval. Previous C01–C04 testing must be rerun together before claiming an aggregate count.

Next investigate an officially accessible full scholarly witness for *Three Deluxe Horoscopes*, an original P.Oxy. 4277 photograph or full critical edition, and Paulus's **transmission relationship** between corrected daytime table, Greek prose and later Olympiodoran nighttime inversion. Search/compare independent ancient documents without selecting records by matched outcomes. The unresolved Hephaistio 360/365 versus English 375 numerical table remains **OPEN** and is not solved by monomoiria work.

**Task recovery:** resume with [C04 checkpoint](HELLENISTIC_CONTINUATION_C04_20261023.md), this C05 source report, the two source-specific modules and tests, and the existing single research-map `README.md`. Never redo completed C04 papyrus extraction when testing newer manuscripts.
