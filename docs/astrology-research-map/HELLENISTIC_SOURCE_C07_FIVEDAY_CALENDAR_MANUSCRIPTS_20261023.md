# Hellenistic source reading C07 — explicit five-day calendrical text and manuscript witnesses

**C08 correction to the C07 reading:** Direct high-resolution inspection of Epitome IV §37 printed p240 established that the Saturn→Mercury numeral is **μ = 40**, not 140. The same printed row has other corrupt numbers and its editor explicitly warns of them. **140 is obtained by executing its approximate sevenfold rule**, not by transcribing the printed list. Further, in Epitome IV §44, Venus is **22** in the 365-day headline but **23** in its finer heading and child totals; the editor proposes 22. See [the source-exact C08 report](HELLENISTIC_SOURCE_C08_CORRUPT_EPITOME_AND_RECONSTRUCTION_20261023.md) and [verified numeric witness](HEPHAISTIO_C08_LITERAL_VS_DERIVED_SUBPERIOD_WITNESS_V1.json). Older C07 green tests were testing derived numbers as though literally printed, and have been repaired. All human predictive validation remains zero.

23 October 2026 — research-only Hellenistic continuation in `humandesign`. Parent empirical astrology project: **OPEN**, human forward-blind validation: **zero**.

## Scope and authority

This follows [C06](HELLENISTIC_CONTINUATION_C06_20261023.md), not the older C04/C05 task descriptions. The user asked to continue reading and comparing actual traditional astrology sources already obtainable. This pass re-examined **Hephaistio, *Apotelesmatics*, Book II ch29 and ch36** directly in **David Pingree's 1973 Teubner critical Greek Volume I** (temporary authorized research copy, SHA-256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae`). It inspected Pingree's **Latin preface on manuscript descent** as well as body text and bottom apparatus at cited pages. No copyrighted full text, source PDF, or modern edition images are checked into the repository.

Bibliography and secondary cross-checks: Pingree, ed. 1973, *Hephaestionis Thebani apotelesmaticorum libri tres*, vol. I; Robert H. Schmidt, trans., *Apotelesmatics II* (1998), independently inspected owner copy; later fifth-century addition to Vettius Valens, English Mark T. Riley. Reader provenance and page alignment were established in C06. The **Greek critical text and Eulogikon normalization likely share an editorial source**, so they are not counted as independent ancient manuscript confirmations.

## Finding A. Actual five-day text in Book II.29, overlooked by earlier pass

**Greek primary critical text, printed p201 (physical PDF page 231), final line of ch29** explicitly says that the **five-day period** is taken along with the twelve months of each year. This is *not merely inferred* from totaling 365; it is a direct passage in the surviving transmitted Greek edited text. Its rare term for that five-day interval is `πενθήμερον`.

**Critical apparatus printed p201, line 31** separately attributes to **P²**, a later correction hand in manuscript P, a marginal instruction to always include the five days when distributing the period. The critical edition's preface (physical PDF pp11–15) identifies the main manuscript **P as Parisinus graecus 2417, copied in the 13th century**; **P²** is a **14th-century corrector**, and the original P text is itself an abbreviated/partly disordered transmission. Epitome IV (`Ep.⁴`) is a related abbreviated textual witness, *not* an intact independent authorial autograph.

**Evidence classification:**
- The transmitted *edited main text* mentions the five-day adjustment: **DIRECT_GREEK_SOURCE**.
- The later `P²` margin reinforces it: **LATE_MANUSCRIPT_CORRECTION**, lower chronological authority.
- Inferring precisely *how* this adjustment was deployed in every other chapter, sign and planetary subdivision: **OPEN_HISTORICAL_INTERPRETATION**.
- It would be wrong to continue writing “Hephaistio contains no explicit evidence of five days.” The correct narrower statement from C04/C06 was only that **the specific ch36 window** did not explicitly explain how to handle the mismatch.

## Finding B. Book II.36 also has a 365-day manuscript reference, but two contrary numeral readings survive

**Pingree printed p225 (physical PDF 255), ch36 apparatus at line 17** notes that manuscript **P adds a 365-day numeral** after a sentence about planets' natal positions. This makes a 365-day source convention more plausible in the transmitted material, but manuscript P is late, shortened and not the author's original; furthermore the inserted words' exact grammatical relation to the following timing procedure remains to be settled.

The distinct, already witnessed readings must **not** be conflated:

| Evidence layer | Saturn | Jupiter | Mars | Sun | Venus | Mercury | Moon | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Printed Greek ch36 primary allocation | 85 | 34 | 42 | 54 | 22 | **52** | 71 | **360** |
| Printed Greek secondary heading amounts | 85 | 34 | 42 | 54 | 22 | **57** | 71 | **365** |
| The seven detailed secondary lists *summed individually* | **86** | 34 | 42 | 54 | **21** | 57 | 71 | **365** |
| Schmidt's English printed secondary headings | 85 | 34 | 42 | 54 | 22 | 57 | **81** | **375** |

At p225 **line 27** Pingree's apparatus explicitly indicates `νβ desid.`, meaning he *desiderates* / expects the numeral **52** where his edited body prints **57**. This is an **editor's expectation**, not a second authentic manuscript shown to read 52. Changing only the heading to 52 would reconcile the **360 main/secondary headline sums**, but not all seven detailed secondary allocations, so **no corrected historical algorithm is admissible** from this alone.

Important source wording: Book II.29 **positively establishes that five days belong to at least one of the transmitted annual division procedures**. Book II.36, with another 365 numeral attributed to P, has further supporting context. **Neither fact proves whether the II.36 primary 360-day series versus its fine 365-day series represents an intentional epagomenal algorithm, manuscript error, or mixed procedures.** Preserve variants.

## Finding C. Recompute all seven II.29 subdivision rows under each calendar

Numbers were *not* changed or rounded to rescue a hypothesis; [the exact arithmetic register](HEPHAISTIO_C07_FIVEDAY_MANUSCRIPT_AND_CALENDAR_V1.json) records every previously checked child sum. Using 129 months (30+12+15+19+8+20+25) and the two plausible calendar denominators:

| Parent planet | Printed sum of seven subperiods | Expected using 30-day months | Expected using 365/12-day months |
|---|---:|---:|---:|
| Saturn (30 mo) | 913 | 900 | 912.5 |
| Jupiter (12 mo) | 365 | 360 | 365 |
| Mars (15 mo) | 450 | 450 | 456.25 |
| Sun (19 mo) | 569 | 570 | 577.9167 |
| Venus (8 mo) | 243 | 240 | 243.3333 |
| Mercury (20 mo) | 606 | 600 | 608.3333 |
| Moon (25 mo) | 764 | 750 | 760.4167 |
| **All rows summed** | **3,910** | **3,870** | **3,923.75** |

**Total absolute discrepancy over the seven parent-row sums:** **42 days** for the 360-day convention versus exactly **263/12 = 21 11/12 days** for the 365-day convention. The latter is a substantially better arithmetic fit *given these limited row totals*; it is not a prediction, demonstration of historical intent, or permission to auto-correct child-table entries. Mars and Sun remain especially inconsistent under 365. The closer fit of the later Valens Saturn→Mercury **140** than the printed Hephaistio **150** remains a distinct textual/algorithmic candidate, not a correction of the Greek source.

**The user-facing takeaway:** We now have both **primary Greek textual evidence** for a five-day adjustment and a quantified reason that a 365-day interpretation deserves investigation. The 360/365 implementation question is narrowed substantially but **not solved**.

## Finding D. Additional text leads and access outcomes

1. **Paulus/Olympiodorus night-table discrepancy**: Two *specific critical editions* are verified bibliographically: **Aemilia Boer, *Pauli Alexandrini Elementa apotelesmatica* (1958)**, and **Aemilia Boer, *Heliodori, ut dicitur, In Paulum Alexandrinum commentarium* (1962)** (astronomical explanations by O. Neugebauer and D. Pingree). Perseus explicitly reports **no online text** for the latter; the 1963 scholarly review discusses its manuscript base (Vindobonensis A with Byzantine reconstructions of a missing opening). The modern Greenbaum edition's **34/120** corrected daytime table disagreements with the Greek narrative **are still unresolved**: no new manuscript diagram was actually viewed in this pass. Do not falsely claim the original-night manuscript table was recovered.
2. **P.Oxy. LXI 4277 photographic check**: The official [Oxford Sustainable Digital Scholarship catalogue](https://www.sds.ox.ac.uk/oxyrhynchus-papyri) states that images up through vol. LXXIII and beyond are maintained by its portal (where items remain in the Oxford collection). The exact [portal search](https://portal.sds.ox.ac.uk/search?groups=35280) responded **HTTP 403** in this session; a reliable image of fragment 4277 was **not** recovered. Keep the Tolsa 2017 critical secondary description and the C05 **1/3** monomoiria mismatch separate from actual firsthand manuscript verification. The Oxford original or Jones's 1999 first edition is a future source lookup, not a reason to halt other reading.
3. These external searches were **bibliographic discovery and source access checks**, not source-text readings; **no additional historical computation match was asserted**. The owner need not purchase a new book for the work already completed.

## Follow-on recensional discovery, corrected by C08: Epitome IV's printed 40 versus derived 140, and its explicit 365-day year

After the initial C07 main-edition audit, I directly examined **David Pingree's Volume II, *Hephaestionis Thebani Apotelesmaticorum Epitomae Quattuor* (1974)**. Research copy SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`, **80,704,330 bytes, 524 physical PDF pages**. Only targeted Greek pages were inspected and no copyrighted book scan or complete text is committed. Volume I preface **printed pp XVIII–XXI** argues that Epitomes II and IV are related but form another textual class from the main manuscript P and its near relatives; different transmission does not make them statistically independent astrologers.

Three primary-source observations decisively upgrade the research:

**1. Epitome IV section 37 (printed pp240–241, physical PDF 270–271):** This corresponds to Hephaistio II.29. For Saturn's 30 months, the Epitome **literally prints 40 days for Mercury** in the visibly corrupted list, but the text's stated sevenfold approximation **would calculate 140**; the main Book II.29 prints **150**. Pingree explicitly aligns the section with Hephaistio II.29 in its critical reference. The **calculated 140** matches the separately checked later fifth-century addition to Valens, but **it is NOT printed as 140 in Epitome IV**. Such historically related witnesses may share older material. It is a source-critical alternative, not a prospective human-confirmed method.

In the same section the Greek text says to convert Saturn's 30 months into **900 days** and approximately divide by 129, giving **7** days as a convenient factor; then multiply each of the seven planetary periods by seven. Applied to [30,12,15,19,8,20,25] months this gives **[210,84,105,133,56,140,175]**, summing **903** versus the theoretical **900**. That **+3** is explicable by the *explicit rounding approximation*, whereas the main version's Mercury **150** creates an additional **+10** unexplained by that instruction. Pingree's **Epitome IV printed p240 apparatus** itself warns that some numerals in the nearby section are corrupt. Thus the *approximate algorithm* favors a derived **140**, while the transmitted Epitome copy prints corrupted **40** and the main Greek witness prints **150**; none may be silently overwritten.

**2. Epitome IV section 37 (printed p242, PDF 272):** Its Greek instructions **explicitly add the five-day interval** to the twelve months of each year. This is a second *recensional* attestation of the five-day clause, beyond main Hephaistio II.29 and P²'s marginal notation. It strengthens the inference that the five-day convention was present in the textual tradition, though **not** that every individual planetary subperiod was computed using 365/12-day months: the Saturn example immediately above uses the **900-day / 129-month** approximation and handles annual five days separately.

**3. Epitome IV section 44 (printed p264, PDF 294):** Its Greek text says **to reckon the year as 365 days**, not simply as a computable sum. It then explicitly assigns annual principal periods **85,34,42,54,22,57,71 days**, totaling **365**. Compare the main Hephaistio II.36 series **85,34,42,54,22,52,71 = 360**. Therefore a **365-day procedure is directly and unambiguously attested in this later recension**. Main II.36 continues to have competing 52/57 readings, and other detailed child-list ±1 problems remain.

[Machine-checked Epitome IV witness](HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json) and [focused tests](test_hellenistic_c07_epitome_iv.py) keep the families separate. **The prior conclusion that 365 was merely a hypothetical general explanation is superseded for Epitome IV specifically**. The higher-level question “what single formula best reconstructs the earliest authorial Hephaistio?” remains unresolved and may legitimately have no single answer where texts intentionally transmit variant computational approximations.

## Tests, preservation, and next safe reading

Five targeted tests in [C07](test_hellenistic_c07_fiveday.py) **passed from a fresh GitHub download**. They verify the exact fraction `263/12`, preserve the textual manuscript classes (P vs P²), refuse an unsupported human-validation claim, preserve 150 vs 140, and assert II.36 remains inconsistent. Previous 36 C02–C06 tests remain unchanged and require one final all-version fresh-run before a combined C07 total may be claimed.

All source distinctions, older C02–C06 correction notes and the project-level human-validation boundary must remain. The runtime scoring model stays untouched.

**Next source frontier:** collate Book II.29 and II.36 with the relevant *Epitoma IV* passage from Pingree vol II / a second authentic manuscript, focusing on whether annual epagomenal insertion is part of that recension; locate the actual Boer 1958/1962 manuscript-table readings that could resolve the 34 disputed Paulus cells. The P.Oxy photograph remains a specific optional open bibliographic source, not a blocker.

**Scientific status:** historical rule reconstruction only; untouched human predictive tests **0**.
