# HumanDesign astrology research — accepted continuation handoff (20 October 2026)

**Root task: OPEN.** Continue the original Western Lilly/Ptolemy and Chinese BaZi/Zi Wei source study, independently calculate traditional natal charts and timing, then freeze a model and run preregistered, blinded real-human forward and reverse tests against decoys and non-astrology baselines. Keep misses and negative results. Historical annotation counts are **not predictive success**.

## Last independently verified durable checkpoint

Repository: `u-dont-existDOTcom/humandesign`. Accepted branch: `research/astro-b07bb-clxxix-parents-source-20261020`. Exact local **and remote** accepted commit: `964d08bb4c61f6fc410052cb996b121180f5f855`. Earlier draft-only checkpoint `4009fda34aa3494d6b411c7960961916efe35e8f` is superseded by the accepted commit. Working tree was clean on remote readback.

Historical Lilly registry: **13,017 accepted source annotations** (latest batch **B07bb**, R12992–R13017) plus independent Ptolemy **1,066** = **14,083 Western historical documentary annotations**. Separately, Chinese historical index **V7** has **154 BaZi + 201 Zi Wei = 355**. No entries were deleted or re-numbered and Chinese V7 remains byte-identical. Last accepted physical Lilly chapter: original **CLXXIX, Of Parents**, printed folios752–753/PDF786–787. Next original historical source: **R13018**, original first edition PDF787/printed753 **CLXXX, Sicknesse, Servants**.

Verified original 1647 full book/source SHA256: `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. CLXXIX uses two original first-edition photographs and two separately typeset 1659 photographs, with four individual image SHA/byte witnesses in `B07bb/ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json`. The printed752 photos were **reused** from B07az/B07ba rather than re-extracted. The printed753 originals and a first-edition printed754 preview were saved in B07bb/evidence.

**What was learned:** Lilly's already-known merchant case attributes Sun/Venus and Saturn aspects to a father's temperament, estate, marital harmony, maternal affection and possible relative longevity. These have **zero independent real-family outcome confirmations**. Lilly also gives a Ptolemy-attributed procedure for deriving a *hypothetical parent chart from the firstborn child's chart*; it specifies a 40° circle-of-position pole, adding 30° to oblique solar ascension when constructing houses, and example father ascendant **6°37′ Libra**. This is **not** a verified real parent's independently timed birth chart, validated Regiomontanus calculation, or demonstration of predictive accuracy. Source authorship of the underlying Ptolemy passage is not independently verified.

**Verified QA:** **42 source-provenance/record tests** passed, including an independent ZIP extract with CRC/member SHA256/exact bytes. **12 post-index append-only tests** passed. The original Parents chapter is marked *physically covered*, NOT independent expert diplomatic collation or experimentally accurate astrology. Actual-human predictive validations **0**; runtime astrology promotions **0**.

Owner portable evidence archive on the authorized laptop:
`~/Téléchargements/Astrology-Lilly-Parents-1647-1659-26-Historical-Sources-B07bb-20261020.zip`
- bytes: **4,588,283**
- SHA-256: `8ab8165c1e7d82e2c16c902fed196151583d5d3a1b6f5fbff543b6724abb4187`.
The archive includes the source, four original-image witnesses, checks, source notes and a provisional source-stage handoff. The definitive **accepted** handoff is this file; the earlier `CONTINUATION_HANDOFF_PROVISIONAL_20261020.md` and `TASK_SCOPE.json` record their former pre-acceptance snapshot, not current pending work.

## Exact next autonomous work — do not repeat B07bb

1. Bootstrap current root `AGENTS.md` in UDA, its `LESSON-INDEX.md` and task patterns, plus humandesign `AGENTS.md`. Read live Git/index before any mutation. Preserve the accepted `964d08bb...` baseline and all historical source files. Open a **new task branch/worktree** for B07bc rather than rewriting B07bb.
2. Begin **Lilly R13018** on original 1647 printed753/PDF787 **below the CLXXIX divider**. Continue into printed754/PDF788. That page already shows CLXXX's remaining sickness and servants discussion, then a clear physical divider leading to **CHAP CLXXXI, Of Marriage** on the same printed754/PDF788. Do not merge two chapters or add observations from the previous Parents case twice. The first edition p787 and p788 source photos are preserved in B07bb/evidence; a corresponding 1659 independently typeset printed753/DjVu782 is preserved, and original 1659 printed754/DjVu783 should be verified if needed.
3. Capture only historical medical and servant/social claims *as source claims*. Do not infer personal diagnosis, health treatment, prejudice, morality, predictive accuracy or harm from them. Preserve exact original wording versus working paraphrase; separate unverified predictions from mathematical/source conventions. Admit contiguous historical IDs from **R13018** only after photo-source witnesses, exact bytes/hashes, relevant portable tests, guarded canonical append, and exact remote Git SHA readback.
4. Resume Chinese source branches from **BaZi BZI-R0155** and **Zi Wei ZWD-R0202** without repeating Chinese V7. The five Zi Wei original palace/day diagrams are preserved but not verified birth-calendar/chart calculations.
5. Remain explicit about the major unfinished outcome: **original natal and timing-engine parity plus genuinely preregistered blinded human evaluation**. Current documentary records establish neither. The earlier Lilly annual-rate table still has **seven unresolved first-edition glyphs**, and historical Naibod/Maginus discrepancies remain separately recorded.

Suggested repeatable recovery checks from the current worktree:

```bash
git status --short --branch
git ls-remote origin refs/heads/research/astro-b07bb-clxxix-parents-source-20261020
python3 -m unittest discover -s tasks/astro-source-audit-multipass-20261005/batches/B07bb -p test_b07bb_post_index.py -q
```

**No owner decision is required** for the next source-only batch. Stop for a real missing authorization/access or a genuine owner tradeoff, not because a single archival increment is complete. This handoff is the requested deliberate stop after a fully published checkpoint; on “continue,” pick up at R13018 without repeating accepted work.
