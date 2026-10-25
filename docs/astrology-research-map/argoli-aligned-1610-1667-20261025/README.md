# Argoli 1610–1667: first aligned historical worked examples

**25 October 2026. Root owner outcome: OPEN.** The eventual aim is to calculate and compare historically differentiated astrology traditions using predictions frozen before genuinely untouched human answers/events and matched controls. These source readings are evidence of textual/mathematical transmission, **not** evidence of astrological predictive success.

## Primary physical sources, separately identified

**1610 Rome, original:** Andrea Argoli, *Tabulae primi mobilis*, Bavarian State Library digitization `bsb11218073` (IIIF manifest preserved locally and versioned; **1760 digital canvases**, not 1760 modern pages of continuous prose; source rights `NoC-NC`). The original printed chapter and page numbers were read from the actual images. The Augsburg Staats- und Stadtbibliothek is listed as the holding institution. The three directly inspected images are:

| Original leaf | Printed page | Chapter | Primary image |
|---|---:|---|---|
| 0051 | 39 | XIII | `aligned_witness_pages/Argoli_1610_scan_0051.jpg` |
| 0052 | 40 | XIII | `aligned_witness_pages/Argoli_1610_scan_0052.jpg` |
| 0053 | 41 | XIII | `aligned_witness_pages/Argoli_1610_scan_0053.jpg` |

**1667 Padua, original prose/excerpt:** *Primi mobilis tabulae*, Internet Archive scan `primimobilistab00argogoog`, preserving original printed p.29 and p.30 within its **107-image excerpt**, which ends at printed page 95. Original scan leaves 42–43 align to chapter **XV** in the later edition. Original page images copied into `aligned_witness_pages/`. The older 107-image scan is emphatically **not the complete later edition**.

**Additional 1667 table collection:** The University of Turin source `bub_gb_065WxfytjWIC` is available separately as a 1036-image PDF with original position-circle and oblique-ascension **tables**, many photographed in reverse printed-page order. The full 59.36 MB original PDF is saved outside Git in the owner's local research artifacts, hash `2eacb5bb7f5b28f99dfea3d60c8728ddb467a33c53aebfbeb149606b8e4e87fc`. This table collection is a valuable distinct witness for table contents, but its sampled leaves do **not** include the same prose printed p.29–30. It is **not** a second physical copy of the printing error.

The complete bibliographic/source relations, unchanged original image SHA-256 values, canvas labels and numeric readings are stored in `ARGOLI_ALIGNED_EXAMPLES.json`.

## Verified alignment despite different chapter numbering

1610 original **chapter XIII** and 1667 original **chapter XV** share the heading on directing significators outside the angles in the **ascending** half of the sky. Both concern computing a significator's position circle/pole and subtracting its oblique ascension from that of the promissor under the appropriate pole. They are **homologous source passages**, unlike the previously contrasted unrelated printed p.3 passages in the two editions.

| Original worked example | 1610 reading | 1667 reading | Arithmetic |
|---|---|---|---|
| Part of Fortune to opposition of Sun, p.39 vs p.29 | 162°50′ − 125°11′ = **37°39′** | Same operands, **37°39′** | Agrees |
| Saturn position-circle pole interpolation, p.41 vs p.30 | 14°20′ − 0°05′30″ = **14°14′30″** | Same operands, **14°14′30″** | Agrees |
| Saturn to opposition of Sun, p.41 vs p.30 | 163°17′ − 119°55′ = **43°22′** | Same operands, printed **45°22′** | Later printed result is **2° higher** than arithmetic |

The different later reading is unambiguous in the inspected original Michigan 1667 image; the two operands are unchanged. The 1610 result and subtraction agree. Treat the 1667 printed **45°22′** as a source-level arithmetic inconsistency, not as an alternative calculation rule or an opportunity to change the primary-directions engine. The unmodified original reading is preserved **alongside** the mathematically correct 43°22′. Whether this discrepancy is a single-copy issue or shared among printings must await a **second original 1667 prose witness**.

The first two agreements demonstrate transmission of these **specific numerical procedures** despite changes in chapter labels/page order. They do **not** prove all position tables, time keys, promissor latitude rules, or the full historical astrology method remained identical.

## Source access and validation boundaries

BSB's 1610 IIIF was directly accessible and its rights/canvas counts verified. Attempts at original 1644 Google Books images returned HTTP 429; the Gallica record/IIIF access previously returned 403 from the Zorin execution route. No original 1644 calculation leaf was inspected. Do not invent a third-edition collation or repeatedly retry the blocked route unless new access exists.

`src/hdmatch/astrology/argoli_printed_arithmetic.py` contains small typed literal sexagesimal subtraction routines that reproduce all three results and explicitly preserve a printing error rather than overwriting witness evidence. `tests/unit/test_argoli_aligned_1610_1667.py` checks these source readings, 1610 canvas-to-printed-page mapping, SHA-256s, original parent source identity, no-human-data status, and invalid-input rejection.

**Prediction/human-validation status:** untested. The previous independent Regiomontanian engineering comparisons and a synthetic 96-chart inventory remain development/engineering evidence only. An empirical test still requires independently chosen, source-qualified rule interpretations, birth-time uncertainty handling, controls, and previously unseen human data. This historical comparison should not become a mandatory blocker for separately registered *modern diagnostic* pilot methods.

## Rebuild

On a source checkout containing both parent Argoli edition branches:

```sh
export PYTHONPATH="$PWD/src"
"$HOME/humandesign/.venv/bin/python" -m pytest -q tests/unit/test_argoli_aligned_1610_1667.py
"$HOME/humandesign/.venv/bin/python" docs/astrology-research-map/argoli-aligned-1610-1667-20261025/build_verification.py
```

Read `CONTINUATION_CHECKPOINT.md` before opening another chat. All original source images and integrity receipts are versioned; the large Turin tables PDF is retained directly on the Zorin laptop and may be included in the local handoff archive without bloating Git.
