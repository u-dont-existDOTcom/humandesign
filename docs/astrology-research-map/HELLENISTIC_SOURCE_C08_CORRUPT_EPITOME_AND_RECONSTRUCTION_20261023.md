# Hellenistic original-source C08 — separating Epitome IV's printed numbers from its reconstructable algorithm

23 October 2026 · Source-only mathematical/textual audit, **no human chart validation**. This report explicitly corrects a **material factual error** in C07.

## What was examined, without redoing earlier reading

Read the original printed Greek in David Pingree (ed.), *Hephaestionis Thebani apotelesmaticorum epitomae quattuor*, volume II (1974), **Epitome IV sections 37 and 44**. Verified PDF source SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`, temporary file in authorized research workstation, **not** committed or shared. Rendered / visually inspected printed **pp240–241 (PDF pp270–271)** and **pp264–265 (PDF pp294–295)**, with enlarged relevant numerical passages. The earlier Greek main Hephaistio witness is Pingree volume I (1973), printed pp200–201 and 225–226, SHA-256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae`.

The 1974 apparatus on printed **p240** explicitly warns that some numbers in the printed passage are corrupt, from the Saturn subdivision through printed p241 l14. **A coherent modern arithmetic reconstruction must be kept in a different field from what that edited source actually prints.**

## Critical correction of C07: 140 was inferred, not printed

In the previous C07 handoff and source register I claimed the Epitome IV printed **140** days for Saturn distributing to Mercury. A higher-resolution direct inspection shows this is **incorrect**: Epitome IV section 37 printed p240 shows Greek **`μ` = 40**, while main Hephaistio II.29 Greek (volume I, printed p200) shows **150**. The later appended material to Valens describes **140**; Epitome IV's *approximation instruction* yields **140**, but its literal list does **not print 140**.

**Three different evidence classes must stay separate:**

| Method/witness | Saturn→Mercury | Provenance |
|---|---:|---|
| Hephaistio main Greek II.29, Pingree Vol I p200 | **150** | Edited printed numerical list |
| Epitome IV §37, Pingree Vol II p240 | **40** | Edited **corrupt** printed numerical list |
| Epitome IV §37, approximate rule applied to Mercury's 20 months | **140** | **Calculated**, not source's printed numeral |
| Later fifth-century addition to Valens in Riley edition | **140** | Separate later textual witness, shared tradition possible |

Epitome IV's approximate source rule: use Saturn's **30 months × 30 = 900 days**, proportional to the complete **129-month** seven-planet cycle, approximate **900/129 ≈ 7** and multiply each of seven planetary month periods by 7. The resulting derived row is:

| Recipient | Saturn | Jupiter | Mars | Sun | Venus | Mercury | Moon | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Direct printed Epitome IV p240** | 210 | 84 | 105 | 133 | 57 | **40** | **105** | **734** |
| **Derived sevenfold shortcut** | 210 | 84 | 105 | 133 | 56 | **140** | **175** | **903** |

The literal-vs-derived discrepancy `[0,0,0,0,+1,−100,−70]` is much too large to call ordinary sevenfold rounding. **These printed data are corrupt**, just as Pingree's apparatus explicitly cautions. The derived 903 exceeds 900 by just 3 days because 900/129 was rounded to 7. This is a different statement than “Epitome IV prints 140” and is the only admissible source-grounded interpretation from these pages without an independently collated manuscript numerals list. The numerals are transcribed by visual reading; preservation of the corrupted printed row is intentional.

This correction required repairs to `HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json` and `test_hellenistic_c07_epitome_iv.py`: the original green tests had simply validated our *reconstructed* row while incorrectly labelling it a literal source reading. They are now forced to distinguish the values.

## Further C08 finding: Epitome IV 365-day primary series still has defective finer divisions

In **Epitome IV §44**, **printed p264**, the primary seven-planet annual allocation is explicitly **85,34,42,54,22,57,71 = 365**. This is **documented** in the Greek recension, not a modern guess, and the five-day annual addition is also explicitly stated in Epitome IV §37 p242.

But the original printed finer allocation on **p264–265** is internally inconsistent even within that 365-day tradition. Three clear directly read examples:

| Epitome IV parent | Headline days | Sum of the seven listed child allocations | Difference |
|---|---:|---:|---:|
| Saturn | 85 | 86 | +1 |
| Sun | 54 | 55 | +1 |
| Venus | 22 | 23 | +1 |

For Venus, **printed p265** starts its fine division with **κγ = 23**, while the higher allocation **p264** has **κβ = 22**. The p265 critical apparatus explicitly suggests **22** (*legendum κβ*) for the fine heading. As printed, the seven Venus child entries add to **23**, not 22. It would be improper to change the heading alone to 22 and leave the children summing 23 without noting the remaining discrepancy. Other source rows were not fully verified in this pass: **do not claim all seven recensional child rows were decoded or reconciled**.

This is substantively useful: **365-day annual reckoning is source attested**, but **a numerically exact 365-day subperiod implementation is NOT yet supplied by these witnesses**. Thus the method should preserve three layers: (1) literal transmitted corrupted numerals, (2) source-described approximate arithmetic, and (3) a proposed modern numerical correction requiring editorial analysis. None may silently substitute for the others when predicting a subject.

## Scientific and engineering consequences

- Explicit annual five-day clauses and the recensional 365-day year remain supported.
- The *claimed second explicit printed 140* in Epitome IV was erroneous and is now superseded. **140 is derived from the source's instructions** and also occurs in a later Valens appendix, but the Epitome printed Saturn→Mercury number is **40**.
- Exactly passing arithmetic tests on *internally assumed data* are not evidence the underlying Greek was transcribed correctly. This pass changed the test fixture to check the actual print against formula-derived output and explicitly include the negative corrupted values.
- These are source-reconstruction problems, not empirical evidence that astrology predicts human personality, occupation, life events, or death.
- No user or third-party birth data used, no source publication, no Kindle extraction, no production scoring changes.

### Reproduction and next step

[Machine-readable corrected witness](HEPHAISTIO_C08_LITERAL_VS_DERIVED_SUBPERIOD_WITNESS_V1.json), [new historical-source test](test_hellenistic_c08_source_literal.py), corrected [C07 Epitome register](HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json) and [C07 test](test_hellenistic_c07_epitome_iv.py). **Rerun all C02–C08 source tests** before claiming the total. Keep other traditions' branches untouched.

Next source tasks: (a) compare the remaining Epitome IV §37 and §44 numeric rows against Pingree's apparatus and a separately witnessed manuscript where possible, recording uncertain Greek glyphs; (b) investigate Paulus/Boer edited day/nocturnal diagrams for the **34/120** Greek-narrative-versus-Greenbaum daytime conflicts; (c) preserve P.Oxy 4277 uncertain original readings separately from modern reconstructions. Do not re-run already completed C01–C07 page discovery, or select a numerical correction to match a known biography.
