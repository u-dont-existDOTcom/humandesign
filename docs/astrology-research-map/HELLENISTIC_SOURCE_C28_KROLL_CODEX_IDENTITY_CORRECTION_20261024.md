# C28 — A cross-codex attribution error corrected

The C27 research mistakenly assigned Kroll 1903, volume VI, printed page 2 (folio 159–159v) to Vienna Cod. phil. gr. 115. The catalogue's original printed page 1 identifies its first manuscript as Cod. phil. gr. 108; printed page 16 begins the second manuscript Cod. phil. gr. 115. Thus the folio-159v table belongs to **108**, not **115**. The previously examined images of 115 folios 159r–160r are not evidence about 108's table. Preserve C27 as historical error and supersede this claim here; do not infer glyphs or night rules.

## Direct primary-source collation

The actual printed 1903 Kroll *Catalogus Codicum Astrologorum Graecorum* VI, examined photographically rather than trusting OCR, distinguishes two numbered manuscript descriptions:

- **Printed p. 1 / PDF p. 19:** No. 1 is **Cod. phil. gr. 108**, a paper manuscript catalogued as sixteenth century with 371 folios.
- **Printed p. 2 / PDF p. 20:** Under No. 1, its folio 159 has the triplicity monomoiria incipit `Ἡ κατὰ τρίγωνον μονομοιρία λαμβάνεται οὕτως` and the cataloguer's note `Des. in tabula f. 159v`.
- **Printed p. 16 / PDF p. 34:** A separate numbered entry No. 2 begins: **Cod. phil. gr. 115**, a paper manuscript described as thirteenth-century, 226 folios.
- **Printed p. 27 / PDF p. 45:** Under No. 2, chapter 34 concerns triplicity monomoiriai ending at **folio 205v**, followed by the distinct Ascendant-degree chapter 35.

All these passages come from the same physically inspected PDF with SHA-256 `282b09d68335979dce9daf41fdbb5b845c75fb0a1f7864bcd5d73ebf38d4c4e7`. Their page-number and item-number boundaries are decisive. A Pinakes record independently assigns Kroll pages 1–16 to codex 108.

## Why the C27 photographic comparison was invalid

C27 examined original-library IIIF photographs of **Cod. phil. gr. 115**, canvas indices **324–326**, at that codex's own folios 159r–160r. Those pages show prose and no obvious monomoiria table. That observation remains true **for codex 115**, but cannot be evidence of what **codex 108** contains at its independently numbered folio 159v.

The C27 register incorrectly stored Kroll's printed-p2 `earlier_catalogued_passage` inside its `catalogue_witnesses.vienna` object whose shelfmark was **115**. Its `independent_manuscript=false` and missing-table investigation therefore reflected a **cross-codex identity error**. C28 supersedes only those inferences, not the preserved photographic data or C27 historical file.

## What the newly identified witness adds—and does not

Kroll now supports **three distinct physical witnesses/locations** for related triplicity-monomoiria material: Vienna **108** f159v (catalogue testimony only), Vienna **115** f205v (original photo examined), and Florence **Plut. 28.14** f204v (original photo examined). The 108 passage could become a useful independent manuscript collation if the actual folio image becomes accessible. It is **not a third independently proven computational rule**. The Kroll text is editorial testimony that does not provide 108's complete ruler sequence.

Date discrepancy: Kroll labels 108 sixteenth-century; the modern ARCA catalogue labels it fifteenth-century. We record both without silently preferring the older estimate. ARCA reports a microfilm of the codex but its photographs are restricted; a freely usable folio-159v original image has not been established. The acquired Boer's 1962 critical apparatus remains **unread**; Google Books offers snippet view and Perseus catalogues the edition without an online full text.

**No model promotion or human result:** C22 has 96/120 older Paulus source positions matching neither candidate daytime algorithm; Florence C24 still matches C05 day at 104/120 and Greenbaum C04 day at 102/120, second-slot pair exchange 120/120 but C05 reconstructed night only 48/120; P.Oxy.4277 remains 1/3; Epitome IV.37 literal 40, derived 140, main 150 remain distinct. These are manuscript diagnostics, not prediction rates. **Zero human prospective predictive validations.**

## Bounded source-intake disposition and provenance

- Original CCAG VI catalogue URL: https://archive.org/download/CatalogusCodicumAstrologorumGraec6/Catalogus_codicum_astrologorum_graec_6.pdf — original printed pages **1, 2, 16, 27**, PDF page numbers **19, 20, 34, 45**.
- Specialist 108 manuscript record: https://pinakes.irht.cnrs.fr/notices/cote/71222/ ; photographic access status: https://arca.irht.cnrs.fr/ark:/63955/md20ft84c99g . Do **not** confuse this with Österreichische Nationalbibliothek's accessible codex **115** IIIF manifest: https://api.onb.ac.at/iiif/presentation/v3/manifest/1182CE33 .
- C28 corrected source register: `HELIODORUS_C28_KROLL_CODEX_IDENTITY_V1.json`; source-only code safeguards: `test_hellenistic_c28_codex_identity.py`.
- Previously published C27 documents stay unchanged and are labelled superseded **only on the original cross-codex identification**.

**Next useful action:** preserve the 108 f159v table as *catalogued but not photographed*; no need to obtain restricted microfilm to finish the testable cross-tradition work. If lawful original access appears, read its ruler glyphs independently before comparing models; otherwise freeze the already available C04/C05 computations with textual uncertainty and move toward blinded testing. Do not infer day/night slot identities, ancient authorship, relative historical authority, or empirical predictive success from this correction.

## Verification receipt

Eight new C28 codex-identity tests passed. The complete Hellenistic documentary regression also passed: **262/262** (254 inherited, 8 new). Unit tests only check recorded provenance and source-boundary constraints, not Greek paleographic accuracy or human predictive validity. No production model changed.
