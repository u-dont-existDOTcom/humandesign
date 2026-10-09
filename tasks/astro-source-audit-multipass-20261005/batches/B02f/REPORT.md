# Lilly: presence, absent people, ships and the time of a question

9 October 2026 · HumanDesign source audit · Batch B02f

## Completed scope

**Book II, chapters XXIV–XXVI are now read and extracted**, including the unnumbered discussion of when a question is received. The scope runs from PDF181/printed147 through the top of PDF201/printed167, stopping before the XXVII heading. All 21 page images were inspected alongside the existing text. Text from later pages was retrieved for boundary discovery only, not counted as completed extraction.

This batch adds **107 records R668–R774**: 40 grouped under XXIV, 15 under XXV, and 52 under XXVI. Lilly cumulative **774** plus the retained **1,066** Ptolemy records gives **1,840** source records. They include conditional rules, tables, qualifications, contradictions and examples—not independent successful predictions. Earlier source datasets, fitted models and personal freezes remain unchanged. No current participant data was inspected.

The original 894-page Wellcome 1647 witness has SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Original scans and page images remain outside Git. No new OCR was performed.

## 1. The question determines who a house represents

For finding an unrelated familiar person at home, Lilly gives that person the **seventh house**; relatives require their appropriate houses. In a general enquiry about an absent person with no relation to the asker, however, he assigns the absent person the **first house**, its ruler and the Moon. These are different source-defined enquiries, not interchangeable ways to get a more convenient chart. (Printed147 and151, PDF181 and185.)

The new reference helper requires the query type and relationship. It rejects unspecified contexts rather than making seventh house a universal default. The at-home chapter also distinguishes meeting someone from merely hearing where that person is; those alternative outcomes should not become a claim of an inevitable face-to-face meeting.

## 2. The time used for a chart is also query-specific

For a sudden occurrence, Lilly says to use the event time, or else when it was first heard of. Later he rejects automatically using the first arrival or greeting of a visitor: a conversation can end without a question ever being asked. His selected time is when the desire is actually propounded. (Printed148 and166, PDF182 and200.)

For a letter delivered earlier but read hours later, he selects the moment it is opened and the querent's intention is perceived—not mere physical delivery. He also permits a genuinely troubling self-question if the astrologer can judge impartially. His proposed explanation of why Bonatus objected to self-questions is explicitly his own conjecture, not a verified quotation from Bonatus. (Printed166–167, PDF200–201.)

The software stores these **historical clock rules** but does not invent a modern ChatGPT receipt/restart convention or choose a timestamp for an actual personal question. That would require a separate declared implementation decision.

## 3. Ship, cargo, crew and commercial success are separate outcomes

The shipping chapter initially assigns the Ascendant sign and Moon to the vessel and its goods, and the Ascendant ruler to those sailing. It explicitly allows **the ship to be lost while people survive**. In another adverse branch, reception saves some sailors without necessarily saving the ship. Benefic mitigation can preserve most people and cargo despite substantial damage. (Printed157–159, PDF191–193.)

Lilly also allows **return without loss** when retrogradation is the sole impediment; additional affliction changes the interpretation to danger or repairs. Poor sale of goods is another distinct result, examined through Fortune and the second ruler. None of these may be scored merely as generic success or failure. (Printed160–161, PDF194–195.)

An implementation must also preserve overlapping roles: when the Ascendant is Cancer, the Moon is both Moon and Ascendant ruler. Those labels do not constitute two independent astronomical observations. The reference code records shared roles without assigning a statistical evidence count.

The complete twelve-sign ship correspondence is preserved as a historical table. It is not maritime engineering, safety or insurance advice.

## 4. A favourable-looking feature is not automatically favourable

In the ship's adverse Mars branch, **essential dignity can qualify destructive action**, rather than automatically rescue the situation. A later lost-ship example contains a lunar trine to Saturn but treats Saturn's role as eighth ruler as adverse. Conversely, retrograde motion can accompany a harmless return or a rapid conclusion. The subject, function and full conditions matter. (Printed159–165, PDF193–199.)

For a hypothetical news enquiry, a square between planets in long-ascension signs is described as equivalent to a trine. The source's interpretive comparison is retained while the geometry remains **90 degrees**, not 120. The same hypothetical gap is assigned about ten weeks, or ten days if the absent person is known nearby. No numerical near-distance cutoff is supplied. (Printed156–157, PDF190–191.)

The earlier local lunar-news table gives days/weeks/months for moveable/common/fixed signs. That symbolic conversion remains separate from the alternative instruction to consult an ephemeris for the actual future contact. The new code requires the named source profile and does not silently select whichever scale matches an outcome.

## 5. Worked calculations expose a difference between an exact claim and printed coordinates

Using the mother-and-son chart's selected printed fields, the earlier declared Lilly Fortune formula reproduces **Gemini15°03′** exactly. The historical clock inscription remains unresolved; this arithmetic does not require pretending to have reconstructed the actual UTC instant. (Chart PDF186/printed152.)

In the first ship example, Lilly says Mars's antiscion falls on the very Ascendant degree. The printed chart gives Mars **Gemini19°26′** and Ascendant **Cancer11°33′**. Exact reflection produces **Cancer10°34′**, a difference of **59 arcminutes**. Both the source assertion and the coordinates are retained. This does not by itself establish an unusable contact or an accepted orb; it establishes that the selected printed inputs do not give exact-minute coincidence. (Chart printed162/PDF196; explanation printed164/PDF198.)

Jupiter is printed at Taurus21° without a minute in the selected chart field, while the second cusp is Leo9°01′. An exact Jupiter-antiscion coincidence therefore remains **unresolved**; missing minutes are not silently replaced by zero.

The ship chart's Moon-to-Mercury and Moon-to-Sun trine residuals reproduce **21′ and65′** respectively. These are static angular separations, not physical contact times or independently confirmed news deadlines.

## 6. One illustration is not several independent cases

The mother-and-son diagram is reused for hypothetical neighbour, stranger, sudden-event and absent-person questions. Those teaching branches do not add four confirmed cases. We preserve three historical case records in this batch: the mother/son and the two ships. Even their stated confirmations are author reports, not independently observed validation outcomes.

The first ship's proposed location is more specific than the reported confirmation: the proposed southwest coast near Ireland/Wales is followed by confirmation of **west and a harbour**. The latter does not independently establish every proposed geographic detail. (Printed163, PDF197.)

## Remaining ambiguities and verification

**28 unresolved issues** accompany the records. They include mixed-query role assignment, unspecified strength comparisons, asymmetric mark-side criteria, unquantified body-region degree bands, contradictory wording in the fortunate ship-parts paragraph, question-clock notation, source house/diagram discrepancies, and the exact antiscion claims. Historical bodily and mortality descriptions remain source claims, not current medical findings or missing-person assessments.

The new **31-test** suite checks query-scoped roles, exact arithmetic, defensive reference-table copying, symbolic-unit provenance, incomplete inputs, record IDs and deterministic data regeneration. The actual focused run passed **95 distinct checks:31 new B02f,30 retained B02e,34 methodology/index checks**. Exact scope is recorded in `VERIFICATION.json`; repeated runs are not new evidence. No full application, independent semantic adjudication, ephemeris parity, or predictive validation is claimed.

## Next source

**Book II chapter XXVII**, *Whether the Querent shall be Rich, or have a competent Fortune? By what means attain it? The time when, and if it shall continue?*, begins **midway through PDF201 / printed167**, after the self-question paragraph. The chapter is not extracted in this batch. The wider source audit, reconciliation, rule implementation and later untouched evaluation remain open.
