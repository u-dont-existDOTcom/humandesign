# B49 exact continuation — 2026-10-22 UTC

**Root task OPEN**, original scope: independently read the five owner-supplied Jyotish books. Canonical repository `u-dont-existDOTcom/humandesign`, task `astro-jyotish-five-source-reader-20261020`, isolated branch `research/astro-jyotish-five-sources-reader-20261020`, unmerged **draft research PR 136**. Preserve Western/Chinese/Tibetan work, private people, surveys, production code; never publicly publish the books.

**B48 carried over:** uploaded Portuguese *BPHS* indexed snippets matched and corrected Sanskrit house arithmetic and age-range broadening. Its 14 tests pass; its leading line in `B48_SHA256SUMS.txt` is an informational header and not a hash entry, so `sha256sum -c` emits one benign malformed-line warning after validating six files.

**B49 new substantive reading:** new edition-specific ambiguity in BPHS 18.33: published Santhanam English Rahu in either fifth/ninth, but modern English Sanskrit gloss requires Rahu conjunct *both fifth/ninth lords*; synthetic sky demonstrates predicates independent, no canonical scoring. Sanskrit 18.34 has new `तद्द्यूने` (proofread SanskritDocuments) versus `तद्द्वूने` (E-Bharatisampat) transcription variants, `dyūna` known seventh-house word in Varāhamihira, original manuscripts unverified. 18.38 12/21 years appears also in Santhanam English (not just Kerr PT) while Sanskrit e-text has 12/19; archive-only historical spouse-loss statement. One VedicPupil page EN assigns *duration* ten years, its HI assigns *marriage age* ten years (18.40); 18.41 next verse and printed English favor age, not canonical precedent for generic verses. Scoped search 18.22–42: no global precedence. See `SOURCE_WITNESS_COLLATION_B49.json`, `READING_NOTES_B49.md`.

**Verification:** `python3 -m unittest -v test_marriage_witness_variants_B49.py` passes 10 tests from clean local batch. Synthetic source variants only. **432** cumulative historical annotations; **0** genuine human forecasts validated; **0** production rules.

**Next executable source frontier:** inspect actual printed Sanskrit image/witness with apparatus for 18.33, 18.34, 18.38 (and confirm `dyūna` in context); seek further original five-book career/wealth/property rules and record positives and negatives without biographical lookup; preserve chapter-specific unindexed marriage age abstention. Do not promote predictive model, privately profile anybody, publish copyrighted binaries, or merge draft PR.

**Checkpoint:** `TASK_STATUS.json` must point at this B49 handoff once commit is verified. Other task notes remain unchanged.
