# Astrology source audit — staged intake and pass plan

## Current result
All **13 supplied Drive files** were retrieved and inspected at intake level. There are **nine book-length files covering eight works**, one severely incomplete preview, and three auxiliary files. This is not a claim that every page, formula or argument has been audited. No new predictive rule has been promoted.

## The work is divided into five passes

| Pass | Work | Current status |
|---|---|---|
| 1. Intake | Identity, edition, hashes, readability, missing material | Complete, with explicit source gaps |
| 2. Section map | Every chapter/section, exact locators, genre and unread status | Ptolemy contents indexed: 61 sections; B01 exact English spans verified |
| 3. Rule extraction | Prerequisites, conditions, exceptions, contrary testimony, examples | B01 I.1-I.8: 24 source records completed |
| 4. Reconciliation | Compare authors without flattening disagreements; reproduce calculations | 18 isolated definition tests passed; cross-author work pending |
| 5. Implementation and testing | Source-linked rules, boundary tests, frozen comparisons, candidate retention | Not started |

Passes 2–4 proceed in source-sized batches, not as one enormous all-books turn. A checkpoint records the last verified unit and first unfinished one. Missing books do not stop independent available batches. Raw books and full extracted text remain outside Git.

## What the supplied files actually contain

| Source | Intake finding |
|---|---|
| Ptolemy / Robbins | 490-page Greek–English facsimile, **1964 reprint of the 1940 translation**. All four books are present structurally. Existing OCR needs checking against the page image. |
| Dorotheus / Dykes | 412 pages; **updated second edition, 2019**, matching the requested edition. |
| Persian Nativities IV | 728-page image scan of the complete Arabic-based translation. Content reaches index p. 714. Front run goes from covers to contents; title/copyright leaf is not supplied there. No text layer; chapter mapping and continuous page audit pending. |
| Introductions to Traditional Astrology | Dykes 2010, 220 scan pages, mostly **two printed pages per PDF page**, through print p. 425. Readable visually; no text layer. |
| Brihat Parasara Hora Sastra I–II | **Girish Chand Sharma, Sagar**, not Santhanam. Readable EPUBs. Chapters **1–47** and **48–100**, including an explicit editorial note about added chapters 5, 10 and 99. Registered as a separate source witness, not mislabeled as the requested Santhanam edition. |
| The Jewel of Annual Astrology | Gansten 2020 Sanskrit–English critical edition, text/searchable. Keep Tajika separate from Parashari. |
| Annual Predictive Techniques | Gansten/Wessex 2020, 213-page searchable PDF. |
| Planets in Transit | 540-page searchable scan; internal imprint **Whitford/Schiffer**, copyright 1976, ISBN 0-914918-24-9. Filename's 1983 Para metadata is not reliable edition evidence. |
| Rhetorius | **Partial preview:** 151 of 203 PDF pages are identical unavailable-page placeholders. Only 52 pages are non-placeholder. OCR cannot recover pages that were never included. |
| PrimaryDirectionsChapter | Authorized **ten-page chapter extract**, not the complete Gansten book. |
| Gansten DOCX | Interview transcript, not the book; preserve transcription uncertainty. |
| “Manetho” ZIP | 808 numbered OCR text files from a combined volume, containing **Tetrabiblos as well as Manetho**. Useful search witness after alignment, not an image-verified replacement. |

## Remaining access gaps
A full Rhetorius, full Gansten *Primary Directions*, Greenbaum's Paulus/Olympiodorus, and Bonatti *On Nativities* remain open. Santhanam remains a separately requested comparison edition; the owner-supplied Sharma pair can be audited now without silently merging their rules. No purchase or source replacement is required to begin the available foundation batches.

## Batch order and next pass
Start with **Ptolemy Book I** definitions and conditions, then his natal Books III–IV, with Book II separately classified as mundane. Continue through Lilly; Valens and Dorotheus; medieval introductions and Abu Mashar; the Jyotish witnesses; and separately attributed Tajika/modern companions.

The contents map now accounts for **61 Ptolemy sections** (I:24, II:13, III:14, IV:10), with **eight English sections read/extracted and 53 indexed, not read**. Readable EPUB/PDF navigation counts are also saved as discovery metadata; scan bookmarks that merely list image filenames are not counted as semantic chapters.

**Completed B01:** English Ptolemy I.1-I.8 has 24 source-linked records and 18 passing isolated definition tests. **Next executable batch B01b:** verify and read I.9-I.16 beginning English PDF p.71 / printed p.47, then stop before I.17. Preserve source claims separately from modern interpretation and do not consult participant histories to choose rules. See the batch reading receipt, RULES.json and CURRENT_PASS.json.

## Evidence and limits
The intake combined file-byte digests, PDF parsing, EPUB/ZIP integrity and navigation checks, existing-text extraction, selected front/end pages and visual inspection of the Rhetorius unavailable-page template. Exact decoded image hashes found the 151 matching placeholders. The original books were not modified. A structurally long document is not thereby a complete witness; continuous page/verse coverage is part of later passes.
