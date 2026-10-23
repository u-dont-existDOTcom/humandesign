# Hellenistic source reader C06: Pingree's apparatus, Paulus table fidelity, and Valens's zodiacal places

23 October 2026 · bounded source-critical research · Scientific outcome **OPEN** · Human predictive validations **0**

## Objective and source authority

Continue from `HELLENISTIC_CONTINUATION_C05_20261023.md` without redoing C01–C05, without reading the purchased Amazon *Primary Directions* via Work, without using biographies to fit variants, and without changing any live astrology model or scoring rule. This is a **historical textual/computational comparison**, not a claim astrology works.

Avoid collapsing:
- actual ancient manuscript readings;
- a modern scholarly critical edition and its conjectural emendations;
- a modern English translation;
- derivative Unicode transcription hosted elsewhere;
- historical papyrus records of scribal computations;
- genuinely prospective outcomes of humans (none tested).

## 1. Key recovery: Pingree's actual 1973 Greek critical edition inspected

The first public host for the modern 1973 critical edition returned **HTTP 403**, so no content was taken from that host. The same public bibliographic landing page also supplied an independently accessible [Internet Archive file-set](https://archive.org/details/BSGERT), and its 1973 Volume I PDF responded with **HTTP 200**. A copy was temporarily examined on the authorized owner workstation; **it has not been distributed, copied to GitHub, attached to the conversation, or modified**.

**Bibliography:** Hephaestionis Thebani *Apotelesmaticorum Libri Tres*, Volume I, ed. David Pingree, Teubner/De Gruyter, 1973; ISBN 9783598713668. The exact downloaded PDF is **78,200,132 bytes**, 496 physical pages, SHA-256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae`. It contains extractable Greek body text and a bottom critical apparatus. Only targeted passages were rendered and visually inspected.

| Book II passage | Original **printed** pages / physical PDF | Observed documentary consequence |
|---|---|---|
| Ch29, ten-year/nine-month subdivisions | **200–201 / PDF 230–231** | Saturn→Mercury is **150**, consistent with Schmidt's translation and the Eulogikon Greek transcription. A much later Valens appendix's **140** remains a distinct chronological reading, not corrected here. |
| Ch36, 360-day principal year | **225 / PDF 255** | Saturn 85, Jupiter 34, Mars 42, Sun 54, Venus 22, Mercury **52**, Moon 71 = **360**. |
| Ch36, finer divisions | **225 / PDF 255** | Printed Greek secondary headings shift Mercury to **57** but retain Moon **71**: these headings total **365**. The subsidiary individual items total **365**, with Saturn's 86 (+1) and Venus's 21 (−1) offsetting. |
| Ch36 alternate year-sign division | **226 / PDF 256** | Additional sign-lord distribution summing a stated **184** days and an explicit authorial note that the available divisions do not agree well. This is another *procedure*, not evidence of 360/365 validation. |

**New critical-apparatus finding**: the small type at bottom of original printed **p225**, keyed to **line 27**, reads **`νβ desid.`**. The Greek numeral `νβ` is **52**; editorial Latin `desid.` is a conventional notation that a reading is desiderated/expected. It stands adjacent to the prose's finer **Mercury 57** (`νζ`) and is consistent with the earlier primary **Mercury 52**. This is **an editorial apparatus judgment**, not proof that a separate ancient witness explicitly has 52 in that place. But it **directly weakens** an unqualified claim that the rise from 360 to 365 was *intended five epagomenal days assigned to Mercury*. The conjecture remains unresolved until the manuscript apparatus and calendar context are fully assessed.

At printed p225 the critical Greek **Moon fine heading is 71**, not the **81** printed in Schmidt English p106. Thus the **375** total belongs to the observed modern English heading, while the critical Greek finer header gives **365**. Correct modern-English printing has not been verified against the translator's later errata; do not imply a particular person committed the error without evidence.

**Provenance upgrade:** We have now **actually inspected pages of a named 1973 critical edition**. Eulogikon's Book II Unicode text aligns in chapter order, pagination and major Greek readings; it may use Pingree/TLG lineage. That is still **not two independent ancient manuscripts** or a collation of every variant in the apparatus. The exact preserved readings are in [source register](HEPHAISTIO_C06_PINGREE_CRITICAL_WITNESS_V1.json). The earlier C04 claim “Pingree not read” is superseded specifically for these inspected pages; the **complete Greek manuscript apparatus remains unread**.

## 2. Independent historical table *other than* monomoiria — P.Oxy. 4277 and Valens

A different ancient planetary-degree mapping called **“zodiacal place”** (`topos zodiakos`) is explicitly recorded in P.Oxy. LXI 4277; this must **not** be scored as the same `monomoiria` whose three manuscript allocations were audited in C05.

**Documentary source:** Cristian Tolsa, “'New' Zodiacal Divisions in POxy LXI 4277,” *Zeitschrift für Papyrologie und Epigraphik* **203 (2017), pp192–198**, especially **pp192–193**. Accessible scholarly text reproduces the relevant Greek fragments and discusses the older Alexander Jones first edition, *Astronomical Papyri from Oxyrhynchus* 1999 vol II pp421–427. The published *facsimile* is still not independently verified in this session.

- P.Oxy. 4277 records **Ascendant Leo 22°11′ → zodiacal place Virgo**.
- **Valens, *Anthologies* Book VIII.7** (English Riley translation in owner source PDF physical **p145**) has a separate example: **Leo 22° → Virgo** in the zodiacal-place table. This passage was *directly located and checked in the owned searchable Valens translation*. The historical cross-author *place label* agrees. Tolsa specifically notes this parallel.
- **P.Oxy. 4277** separately records **Mercury Capricorn 6°22′ → Sagittarius** as a zodiacal place. **No matching Valens entry** for the latter was individually located, so it is an **isolated papyrus attestation, not an independently reproduced match**.

**Critical caution:** The Leo fractional degree and the integer label in Valens can have different ancient ordinal conventions, and the zodiacal-place table has segments commonly **two to four degrees**, not one-degree monomoiriai. The agreement is **one shared place assignment, not a solved boundary rule**. No full 12×30 table can be recovered from one pair of examples.

[Exact attestations and non-generalizing lookup](valens_zodiacal_place_c06.py) are in the repo. Unknown input explicitly raises an error. No birth outcome was evaluated.

**Additional research lead but not a mandatory purchase:** [Oxford's Oxyrhynchus digital images catalogue](https://oxyrhynchus.web.ox.ac.uk/images) advertises digital images up to at least Volume LXXIII and links to its SDS portal. The known P.Oxy. 4277 image may be there; no exact authenticated fragment-image URL could be retrieved with the available ordinary public page access in this pass. [Jones, *Astronomical Papyri from Oxyrhynchus*](https://www.pennpress.org/9780871690173/astronomical-papyri-from-oxyrhynchus-vol-i-and-ii/) is available as a publisher edition, but the relevant original printed passage was not read in this pass. The latest C05 **1/3** monomoiria result remains unchanged and unvalidated at papyrus-image level.

## 3. Paulus's triplicity printed-table problem: avoid weaker “confirmations”

The previously read Greek Paulus ch2/ch32 says use the day/night rulers sequentially, proceeding through the four trigons and not repeating a planet before a complete seven-planet set; his nocturnal fire opening explicitly gives Jupiter then Sun. The C05 mathematical reconstruction differs from Greenbaum's corrected printed *daytime* chart in **34/120** cells. This difference remains an **editorial/transmission question**, not a signal that one yields a better chart fit.

A freely visible **2011 Italian secondary table** (“Monomoirie e rettifica dell’ora”, Mario Costantino, [online page](https://www.astrologiaclassica.it/wordpress/monomoirie-e-rettifica-dellora-di-mario-costantino/)) does **not** resolve the problem:
- It prints a daytime **fire** column beginning **Mars**, inconsistent with the independently inspected Greek Paulus chapter's **Sun**.
- Its first seven daytime fire entries repeat Mars in the seventh position **without allocating Sun**, conflicting with the Greek instruction to avoid a repeat before using all seven.
- Its other columns exhibit repeated entries that cannot independently validate a faithful 7-cycle reconstruction without critical apparatus and edition provenance.

Therefore an online derived table should **not** be granted manuscript authority or used to erase C05's 34-cell discrepancy. This is a negative **source integrity result**, not another rulebook counted.

### Ancillary full-source availability

Eulogikon's open [Greek Paulus *Eisagogika*](https://eulogikon.org/works/paul-alexandria-astrology-sum-aa) preserves the chapters but the crucial formatted ch32 canon is flattened in the accessible Markdown into header-like text and cannot supply a directly inspectable complete authoritative diagram. Greenbaum's scanned 120-cell day canon remains the audited **edited print witness**; C05's derived full nocturnal sequences remain **reconstructions**, not copied ancient nighttime tables.

## 4. Status and next source read

**Done C06:** read only the relevant pages of Pingree 1973 in actual scanned critical print, recorded p225 editorial expected 52, preserved primary 360/finer 365 and English 375 as distinct; located separate shared Valens–papyrus zodiacal place, and identified an invalid Italian monomoiria table corroboration. This work corrects source availability and confidence, but **does not prove which calendar is historically right**.

**Still open:**
1. Inspect a fuller section of Pingree apparatus, ideally manuscript sigla and the Greek base of the 52/57 issue; distinguish editorial emendation from actual manuscript variants.
2. Establish Greek Paulus table provenance from independently collated diagrams, e.g. ancient Greek Olympiodorus commentary. Do not resolve 34 cells by retrospective owner/chart data.
3. Access P.Oxy. 4277 original photographs/first edition, validate its uncertain signs and ordinal conventions, and test **separate** zodiacal-place versus monomoiria constructions on untouched *historical calculations*, not human traits.
4. For actual prediction, freeze historical features and nonleading observables *before* asking untouched, consenting participants. Keep the original Saturn→Mars contradictory forecasts and all other candidates separately source-gated.

**Scientific status:** human validation 0; source arithmetic reproducibility only; **no changes to production mapping, model, or other astrology lanes**.
