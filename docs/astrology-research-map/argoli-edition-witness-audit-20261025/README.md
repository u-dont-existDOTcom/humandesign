# Argoli editions: page-witness recovery and correction of the 1667 scan extent

**Research continuation — 25 October 2026.** Owner's original goal remains **OPEN**: reconstruct source-grounded distinctions between Western, Hellenistic, Jyotish, Chinese and other astrology rule systems, then freeze explicit falsifiable chart predictions and test on genuinely untouched human evidence and controls. This work is a historical-document audit; no natal charts or human outcomes were used.

## Material correction to the prior Argoli research packet

The source identified as **Andrea Argoli, Primi mobilis tabulae (1667)**, Internet Archive/Google Books identifier `primimobilistab00argogoog`, was accurately described in several source files as *partial*, but a handoff called the 107-page file the **full public-domain 1667 source PDF**, and the accompanying owner summary called it a **complete original 107-page scanned volume**. Both expressions overstate the scope of the underlying original edition.

I personally inspected the terminal scanned leaves and documented them under `1667_terminal_pages/`: physical PDF leaf **105 is original printed p.94**, leaf **106 is original printed p.95**, and PDF leaf **107 is the binding back cover**, with no continuation of the printed source. The parent original PDF has only **107 image leaves**, verified with `pdfinfo`, SHA-256 `b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d`. A contemporaneous *Primi mobilis tabulae* first volume is reported by bibliographic listings as much longer, around **757 numbered pages** (not a 95-page printed pamphlet). In particular, the 1644 first-volume antiquarian description gives introductory 95 pages followed by 757 pages of tables; another 1667 first-volume description also lists 757 numbered pages. **The archived copy is only the introduction/preliminary section and should never stand in for complete edition-wide table coverage.**

The prior mathematical parity result remains valid within the verified source-specific domain, because original 1667 printed pp.3,7,23 remain inside this excerpt and the independent Regiomontanian reconstruction was separately checked. What **does not** follow is that later physical printed pp.96–757, the 1610 original, or the 1644 printing are covered by this PDF. This new branch corrects the old checkpoint and supporting provenance wording instead of silently replacing the historical evidence.

## Newly obtained original 1610 witnesses

Using authorized public-domain Google Books page-image URLs, three separate physical digitizations of Argoli's **1610 Rome first edition** were retrieved, and the original printed page **3** was checked visually in each, not by OCR. Their exact image files and SHA-256 values are indexed in `ARGOLI_EDITION_AUDIT.json`, and the original returned images are retained in `1610_witness_printed_p3/`.

- `R92lDeOw8X0C`: catalogued by Google Books as scanned from Rome's Alessandrina Library.
- `7utl-3EFz1UC`: catalogued by Google Books as scanned from the National Central Library of Florence.
- `-zhmAAAAcAAJ`: separate full-view digitized witness; holding institution not independently established in this turn.

These are three **different scanned-image files** but their text on original printed p.3 visibly agrees at the opening and end. The 1610 printed p.3 is part of a discourse about influences and changes in the natural world. By comparison, **original printed p.3 of the 1667 excerpt** discusses methods of primary directions and Regiomontanus, as the already published source plate demonstrates. This is an observed *nonaligned printed-page difference*. The two editions have different pagination/introductions, so **it does not establish addition, deletion or doctrinal disagreement** until homologous chapter passages are found and collated.

## Recovery limits and next source comparison

The 1610 Google Books full-page images were initially accessible for p.3, but after that, requests for printed pp.12,20,28,36,45,55 were met with **HTTP 429**. The downloadable original 1610 PDF endpoints also returned 429/Google's anti-automation page. They were not circumvented. The alternate 1644 Gallica manifests `bpt6k511622` and `bpt6k51163d` returned HTTP 403 through the tested authorized remote route. Those are *access limitations*, not evidence that any edition or passage is absent.

The best remaining textual objective is to secure accessible **aligned sections** in 1610 and 1644 (introduction to Regiomontanian position circles, right/oblique ascension definitions, pole elevation tables, then numeric table entries), identify corresponding text rather than same printed page numbers, and check them directly against the 1667 pages with image hashes. Alternative public library viewers/IIIF or human browser-based visual reading remain possible. Do **not** assert a complete 1610 vs 1644 vs 1667 collation from the evidence currently recovered.

**Research phase status:** 1610 p.3 visually cross-witness-verified; 1667 excerpt length and endpoint verified; 1644 originals located but not collated; historical exactness across editions remains OPEN; empirical astrology predictive accuracy remains **UNTESTED**. The owner-facing file path and checkout are recorded in the completion packet.

## Deterministic manifest reconciliation

The corrected inherited README, primary-source scope and continuation checkpoint necessarily changed three file hashes. The inherited regression-test name was also corrected from “full volume” to “partial excerpt.” On this **new branch only**, the inherited mathematical packet’s `VERIFICATION.json` has been regenerated against those four exact changed files. Its numeric parity-report bytes and mathematical replay record remain unchanged. The original published commit and receipt remain preserved in Git history. This is a source-scope correction, not new mathematical evidence.
