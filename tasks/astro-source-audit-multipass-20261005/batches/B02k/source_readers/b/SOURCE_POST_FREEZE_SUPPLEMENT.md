# Reader B: post-freeze source supplement

## Independence and frozen baseline

The original `SOURCE_FIRST_NOTES.md` and `SOURCE_FIRST_FREEZE.json` remain unchanged. Their hashes are respectively `d69efe9e1e3a69590b9e6cc54a209d7a26db38d511e58e8b367dd6c30263d018` and `978bbe0f2fde8384072fe5f0edb8f7bae1b90e106ad711dd211b09f7df0d6916`.

Candidate creation began only after that freeze. No B02j schema, previous extraction, or other reader's substantive candidate set was consulted. After the freeze, the parent identified three relevant entries on the source's own errata page, PDF888. Reader B independently rendered and viewed that full page and an enlarged crop of its admitted-span entries. The parent had described one word provisionally as `scare`; reader B's direct reading is `feare`. The parent's provisional word was not copied into candidates.

The supplemental page is part of the same SHA256-verified PDF. It is consulted only as errata for admitted printed pages 254, 256, and 257. It does not extend the extracted rule scope into Dariot or other chapters.

## Source-authored corrections, separately layered

| Candidate | Original admitted page | Original/annotation observation | Errata at PDF888 | Treatment in current candidate |
|---|---|---|---|---|
| B069 | PDF288, printed 254, lines 18–19 | The word is broken after `pla-`; line 19 begins an overmarked character followed by `ed`, with the underlying print appearing to read `ted`. The annotation's author is not known. | `p 254 l 18 & 19 r placed` | The condition uses placement in the listed houses. The source-authored correction to `placed` is explicitly recorded in `source_layers`. |
| B085 | PDF290, printed 256, line 8 | The phrase after `after` is struck/overwritten. It is not wholly legible to this reader. A marginal annotation appears to contain `ear of danger`; neither that hand nor the strike-through is treated as authorial authority. | `p 256 l 8 dele all hopes of escape, r. feare of danger` | The erratum supplies the corrected reading: with the specified reception and fortunate Moon, after fear of danger a little hope remains. The deleted text is identified by the errata, not falsely claimed as a fully legible direct reading beneath the handwriting. |
| B105 | PDF291, printed 257, line 23 | The antiscion phrase visibly has `the Lord of the eight` followed by an overmarked terminal character. | `p 257 l 23 r eight` | The eighth-lord relation is retained and the correction is separately recorded. It does not resolve the rule's other condition-scope questions. |

The errata correction is read as **feare of danger**. The short form in the candidate assertion is a modern-spelling paraphrase; the `source_layers.authorial_errata.instruction` field preserves the source spelling. An assembled corrected reading is labeled as such rather than passed off as an uncorrected printed quotation.

## Further point-of-use visual checks

Reader B directly re-rendered and inspected full PDF290–292 at larger size from the same PDF, in addition to the supplied original full PNGs used before freeze. These checks confirmed:

- The PDF292 square/opposition clause pairs Saturn with **Mercury**, whose glyph is visible. It is not normalized to Mars. The full sign/aspect/star clause remains unresolved as to AND/OR grouping in B118.
- The PDF291 `some say` clause visibly uses **Saturn or Jupiter**, and its exception specifies Saturn retrograde **and** Jupiter direct. B104 retains attribution and both connectives even though another source rule gives a favorable Moon–Jupiter conjunction.
- The fixed-star list continues across PDF291–292. The listed values are Antares at fourth Sagittarius, the Lans/Lanx Australis name about ninth Scorpio, Palilicium in four Gemini, and Caput Medusae in twenty Taurus. B108 preserves the unresolved name spelling and does not infer present-day positions or an orb for `neer`.
- PDF292's last complete paragraph ends `shew death` immediately before `DARIOT Abridged.` B117–B119 include that complete paragraph. The Dariot heading and everything below are excluded.

Anchor phrases use ordinary `s` for long-s and join typographic line/page breaks. Where a first draft anchor verbalized a planet or aspect glyph as if it were printed words, the final anchor was changed to a short adjoining verbal phrase. Planet/aspect names in the candidate conditions remain explicit paraphrase of visible glyphs. The coverage file labels its start/end locators as navigation aids rather than exact quotations.

## Candidate and issue scope

The current reader-B set contains 119 candidates, B001–B119: 57 in the continuing long/short-sickness section, 23 in the survival-testimonies section, and 39 under Arguments of Death. These are reader-B extraction counts, not a claim of independent root acceptance, historical truth, clinical validity, or executable readiness.

The 18 typed issue records distinguish `source_defined_content` from `assistant_identified_gap`. Seventeen retain an open issue or evidence boundary; the final record marks the placement/eighth-word errata resolved with their separate layers retained. An issue's presence does not silently delete its source rule. All candidate condition logic has `executable: false`; ambiguous source grammar, undefined numeric thresholds, and comparative source modalities remain visible.

The parent refined the shared page boundary before freeze: reader A owns the complete common-sign/Pisces sentence across PDF282–283. Reader B begins with the following Moon ill-aspect rule, B001. That carried sentence is in reader B's notes only as context and has no duplicate substantive candidate here.

## Evidence files and local inspection images

Primary deliverables are `SOURCE_FIRST_NOTES.md`, `SOURCE_FIRST_FREEZE.json`, `CANDIDATE_RULES.json`, `SECTION_COVERAGE.json`, `UNRESOLVED.json`, and this supplement. `CANDIDATE_ALIAS_MAP.json` and `build_candidates.py` are reproducibility aids. `ARTIFACT_MANIFEST.json` records primary deliverable hashes and bounded mechanical checks.

Local visual evidence, all created in reader B's assigned workspace, includes `errata-888.png`, `errata-admitted-lines.png`, `p254-placement-crop.png`, `p257-antiscion-crop.png`, and the larger full-page `verification-290.png` through `verification-292.png`. These are inspection derivatives of the same source and are not substitutes for the verified PDF. The parent can preserve the relevant crops without copying every larger derivative.
