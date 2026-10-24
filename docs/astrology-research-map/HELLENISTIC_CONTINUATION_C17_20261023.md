# Hellenistic primary-source continuation C17 — original P.Oxy. 4277 image recovered

**Research began:** 2026-10-23. **Owner outcome:** OPEN, source-faithful historical astrology and eventual independently frozen/blinded human testing; currently **0 human predictive validations**. This handoff supersedes C16's *next-step list for the papyrus only*, not its source evidence. Production/cross-tradition scoring remains untouched.

## Rebootstrap and authority

Read LIVE `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md`, then THIS checkpoint and the C17 source report. Do not redo the C01–C16 source corpus or existing Hephaistio/Paulus diagram scans. No biography-based source selection and **do not use Work to extract the owner's purchased Gansten Kindle ebook**.

- **C16 exact accepted base commit** `65181da26f7b77edd9612dd3845388322bd8419b`, branch `research/astro-hellenistic-c16-boer-preface-20261023`.
- **C17 isolated child branch** `research/astro-hellenistic-c17-greek-witness-20261023`. Integrator-owned parent research branch `research/astro-missing-book-audit-20261022`; no direct production merge, no new scoring rules.

## Major C17 primary-source advance

**OFFICIAL authenticated original object photo now located and inspected**: University of Oxford Sustainable Digital Scholarship, Oxford Papyrology group **35280**, article **21178150**, exact named `P.Oxy. LXI 4277. Deluxe Horoscope`, DOI `10.25446/oxford.21178150.v1`, 2022 digital source record `https://api.figshare.com/v2/articles/21178150` (a different date than ancient manuscript creation).

Two original Oxford images directly downloaded from authorized publisher-provided Figshare URLs, viewed, and source integrity checked on owner-controlled workstation:

1. `https://ndownloader.figshare.com/files/37552438` (publisher file `POxy.v0061.n4277.a.01.hires.jpg`) — **3660×2632**, 9,361,845 bytes, SHA-256 **`aefec1af94416903fc25863bc7f8f74d9278fd9d4b3cc8f18056b01f2b06a084`**, publisher MD5 **`b62daf036de9d026b8e986f7c74c5bb3`**.
2. `https://ndownloader.figshare.com/files/37552441` (file `POxy.v0061.n4277.a.02.hires.jpg`) — **567×343**, 192,831 bytes, SHA-256 **`60e243177a325b26c53be96f17db439a2e176729ac64dd4f884a2708a69c9abe`**, publisher MD5 **`fbfc8184bec0bc05f8f61b5d3c4ff506`**.

Both fetched HTTP200 and passed exact publisher-MD5 and local-SHA256/size verification. Main photo and several image-specific high-resolution crops were viewed directly; second image smaller fragment seen. **No images redistributed in Git**; Oxford/EES record is **In Copyright**. Local ephemeral source study path on prior authorized machine: `/tmp/hellenistic-c17-original-poxy-4277/`; this path is not portable or guaranteed persistent. Full reproducible identity/provenance in machine record.

**This clears the previously open “original P.Oxy. 4277 image inaccessible/uninspected” gate at the original-object/photo level.**

### Preserve the crucial distinction: official photo ≠ fully deciphered Greek

The THREE extant numeric monomoiria *labels* from C05, taken from Jones (1999) / Tolsa (2017) as scholarly edited text, were **not independently re-deciphered glyph-by-glyph** from the original photographs in C17. The papyrus has missing/fragmentary Greek, and line-by-line published apparatus is still required.

Preexisting C05 comparative Paulus-by-sign calculation remains:
- Mercury Capricorn **6°22′**: reported **Venus**, predicted **Moon**, **mismatch**.
- Midheaven Taurus **27°08′**: reported **Mercury**, predicted **Sun**, **mismatch**.
- Lower Midheaven Scorpio **27°08′**: reported **Jupiter**, predicted **Jupiter**, **match**.
- **1/3 matches, 2 negatives**, zero new success claims. Do not tune to improve this. C06's Leo22→Virgo Valens *zodiacal place* is a distinct doctrine and not counted in these three.

C05 previous `MANUSCRIPT_IMAGE_NOT_RECHECKED` status remains truthful **historical at C05**, but it must now be accompanied by the C17 image-authentication status. Do not falsely mark the three edited monomoiria labels as individually photo-collated.

## C17 durable new artifacts

- [C17 original Oxford photograph authentication report](HELLENISTIC_SOURCE_C17_P_OXY_4277_ORIGINAL_PHOTO_AUTHENTICATION_20261023.md).
- [C17 publisher item, source file hashes and status registry](P_OXY_C17_OXFORD_ORIGINAL_IMAGE_EVIDENCE_V1.json).
- [C17 primary photo optional local integrity verifier + C05-source comparison](poxy4277_original_image_c17.py).
- [C17 source-state arithmetic regression](test_hellenistic_c17_poxy_4277_primary_image.py) — 12 new exact tests, including missing-source fail-closed, no copyright redistribution, no mythic prediction claims.
- Legacy C05 source report and C16 handoff only have appended C17 supersession notes, and research map `README.md` points to C17. Earlier witness logic remains intact.

### Test

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Verified C17 historical-source suite: 145/145 PASSED (exit 0)** on the isolated C17 worktree; 133 retained C16 tests plus 12 new C17. All relate to textual/provenance arithmetic, not human predictive validity. Optional source integrity check for the actual Oxford files has ALREADY returned two successful publisher MD5 and locally recorded SHA-256+size matches; not included as a hermetic repository test because copyrighted original images must not be added to Git.

## Next OPEN research actions

1. **Independently collate exact three P.Oxy. 4277 monomoiria words** and nearby calculations from Oxford photographic Greek + A. Jones *Astronomical Papyri from Oxyrhynchus* (1999), **vol II pp421–427**, comparing Tolsa 2017 p196–197. Record column/line, damaged letters, editor restorations and direct reading separately. No OCR-only declaration of palaeographic certainty. This is now a **source-reading**, not an image-access problem.
2. Obtain the actual **Boer 1958 Greek printed chapter-32 apparatus/diagram** and Boer 1962 scholia; C16 source hypothesis of probable one damaged archetype is **editorial, not proven**. Paris Z (gr2506), Y (gr2425) are still uncollated independent candidates.
3. Preserve unresolved Hephaistio Epitome IV.37/44 numerical corruption and source variants. Compare historical source methods before freezing an astrology feature for future blind human tests. No transition to production scoring or biographical optimization.

**One-line resume:** C17 official Oxford exact P.Oxy. 4277 two images retrieved and visually verified with 4 matching published/local checksum hashes; old 1/3 documentary numerics unchanged; **next is direct line-by-line Greek palaeography**, not hunting papyrus image again.

## Further access check after original Oxford image recovery

I also checked the original **Alexander Jones (1999), *Astronomical Papyri from Oxyrhynchus* (vols I–II)** edition route. The **Open Library record** for `OL18730540M` explicitly offers *preview/search only*, not authenticated full text of vol. II pp. 421–427; the original **Penn Press** ebook ISBN **9780871690173** is a paid $115 edition at the publisher. No purchase or access-control bypass was attempted. This leaves **Jones's exact Greek line edition and critical restorations uncollated**, even though the source papyrus photographs themselves are now authenticated, downloaded for temporary study, and publisher-checksum verified. Do not conflate the 2017 Tolsa discussion, Open Library bibliographic preview and the unseen 1999 printed critical apparatus. Publication/source handles: `https://openlibrary.org/books/OL18730540M/Astronomical_papyri_from_Oxyrhynchus`, `https://www.pennpress.org/9780871690173/astronomical-papyri-from-oxyrhynchus-vol-i-and-ii/` (verified through live bibliographic search; not proposed as purchase).

## C18 supersession — later numerical-method clarification

C17's **official Oxford photograph identity and hashes remain verified**; the C05 paper-derived source-label math remains **1/3**. A new C18 comparison of Tolsa 2017 p196–197 finds that the paper's Valens IV.26 column (Mercury/Mars/Saturn) equals the C05 **completed-degree-index** diagnostic 3/3, not the physically correct ordinal outputs (Moon/Sun/Jupiter). The three Tolsa p196 published trigonal models do not reproduce any of the three reported monomoiria labels. These are source-comparison differences, not human success rates. The papyrus is palaeographically dated late 2nd/early 3rd century, well before composition of Paulus's Eisagogika in 378 CE, so must not be described as a scribe copying Paulus's later authored book. Refer to [C18 report](HELLENISTIC_SOURCE_C18_ORDINAL_PARITY_AND_CHRONOLOGY_20261024.md) and [C18 handoff](HELLENISTIC_CONTINUATION_C18_20261024.md).
