# C17 — official Oxford original photographs of P.Oxy. LXI 4277 recovered and authenticated

**Research began:** 2026-10-23. **Scope:** primary-document authentication / history-of-computation research. **Human predictive validations = 0; no natal model promoted.** Continue from C16, preserving all C01–C16 historical source results. The user's purchased Gansten *Primary Directions* Kindle ebook is not involved.

## Result: the previously missing *exact original* papyrus image was located

The official **Oxford Sustainable Digital Scholarship / Oxford Papyrology** repository, via its public scholarly data API, positively identifies an item titled **`P.Oxy. LXI 4277. Deluxe Horoscope`**. This is the exact object discussed by A. Jones (1999) and Cristian Tolsa (2017), **not** an unrelated P.Oxy. 4276, 4278 or 4477 horoscope.

| Publisher-verified metadata | Exact value |
|---|---|
| Official record | `https://portal.sds.ox.ac.uk/articles/online_resource/P_Oxy_LXI_4277_Deluxe_Horoscope/21178150` |
| Public metadata API | `https://api.figshare.com/v2/articles/21178150` |
| DOI | `10.25446/oxford.21178150.v1` |
| Oxford record ID / group | `21178150` / `35280` |
| Digital deposit publication | 2022-09-21 (not the ancient papyrus date) |
| Original document date | late 2nd / early 3rd century CE *by handwriting*, Jones/Tolsa scholarly dating |
| Image use | **In Copyright** — reproduction permission handled by the Egypt Exploration Society |

**The two Oxford-supplied high-resolution source photographs were actually fetched and visually inspected on an authorized study machine.** The HTTP download matched both publisher-provided MD5 hashes, plus locally recorded SHA-256 hashes and exact file byte counts:

| Oxford file | Original image dimensions | Size | SHA-256 |
|---|---|---:|---|
| `POxy.v0061.n4277.a.01.hires.jpg` (file ID 37552438) | **3660 × 2632** | 9,361,845 bytes | `aefec1af94416903fc25863bc7f8f74d9278fd9d4b3cc8f18056b01f2b06a084` |
| `POxy.v0061.n4277.a.02.hires.jpg` (file ID 37552441) | **567 × 343** | 192,831 bytes | `60e243177a325b26c53be96f17db439a2e176729ac64dd4f884a2708a69c9abe` |

The first image is a large direct full-view original papyrus photograph with a physical measurement ruler, showing extensive holes and fragments of multiple writing columns. The second shows a small additional papyrus piece and measurement scale. **Do not assert a recto/verso or fragment alignment** beyond the limited Oxford file metadata. The first image was also inspected through full-resolution separately cropped / contrast-normalized local study regions in the left, center, right, upper and lower portions. Contrast processing can help visibility but **cannot restore torn-off Greek ink**. These are locally temporary study copies, **not redistributed into Git**, because the EES retains reproduction rights.

**Source-authentication conclusion:** the owner’s request to find and personally inspect an authenticated Oxford photograph of P.Oxy. 4277 is **now satisfied at the image-identity level**. The former open “no original photograph” limitation is superseded by a publisher-authenticated source item, two complete downloaded images and matching byte hashes.

## Still distinguish publisher-authenticated object from independently read papyrus *values*

Earlier C05’s separate *calculation* comparison from Tolsa/Jones reported exactly three surviving monomoiria labels. These are **scholarly text-edition readings**, not newly independently established from our photographs:

| Papyrus object | Reported longitude | Scholar-reported monomoiria | Paulus *by-sign* correct ordinal | Agreement |
|---|---|---|---|---|
| Mercury | Capricorn 6°22′ | Venus | Moon | **No** |
| Midheaven | Taurus 27°08′ | Mercury | Sun | **No** |
| Lower midheaven | Scorpio 27°08′ | Jupiter | Jupiter | **Yes** |

**Historical source arithmetic: 1 match / 3, two negatives unchanged.** These values were not individually and reliably re-deciphered from Greek letter forms during C17; the full image contains illegible/damaged writing. The next palaeographic task is to align **i/ii manuscript line numbering, three exact monomoiria Greek words, and Jones’s 1999 editorial apparatus**, preserving every uncertain letter. Do not mark them as three independently source-image-certified readings simply because their photograph now exists. The original C05 historical state `MANUSCRIPT_IMAGE_NOT_RECHECKED` remains a truthful statement *about C05*; C17 adds a **new later source-image authentication layer** without overwriting what previous investigators did or did not see.

The papyrus also contains separate **zodiacal places**, **terms**, **trigons**, **lots**, **steps/winds**, **decan** and **dodekatēmoria**. C06’s Valens VIII.7 Leo 22°→Virgo *zodiacal-place* agreement is **not** one of these three monomoiria calculations. No pooling or double counting is allowed, and an ancient horoscope is not a human behavioral prediction experiment.

## Reproducibility and reliability

- [Publisher identity, two file hashes, source scopes](P_OXY_C17_OXFORD_ORIGINAL_IMAGE_EVIDENCE_V1.json): official item, images, visual observation scope, copyright, separate C05 historical readings, unresolved palaeography.
- [C17 source-status and exact local image verifier](poxy4277_original_image_c17.py): pure historical comparison reads **unaltered C05** arithmetic and checks that source authentication is not upgraded into glyph certainty. An optional off-repo integrity-check function reproducibly validates both original image file hashes on a machine that has acquired legal study copies. This exact two-file check was performed and **both MD5/SHA-256/size checks passed**.
- [C17 source-status regression tests](test_hellenistic_c17_poxy_4277_primary_image.py): 12 controls, covering Oxford DOI, file IDs and hashes, no Oxford images in Git, no false independent paleographic source status, fail-closed missing files, the historical **1/3** with two preserved failures, and zero human predictions.

Test command:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
**C17 verified full suite: 145/145 historical-source tests passed, exit 0** (133 retained, 12 new) on the isolated C17 worktree. Source arithmetic and photograph integrity do not validate any algorithm on people. No production code or cross-tradition scoring changed.

## Remaining work (unadjudicated)

The biggest new source obstacle is **not image access any more**, but paleographic/source-genealogical interpretation: recheck Greek monomoiria labels against Jones original edition, investigate Boer's actual 1958 Greek ch.32 variant apparatus and 1962 commentary, plus the distinct Parisian manuscript witnesses `Z`/`Y`. No variant should be chosen for matching a previously known biography, and the papyrus's negative outcomes are not to be erased. No purchased Gansten ebook extraction via Work.
