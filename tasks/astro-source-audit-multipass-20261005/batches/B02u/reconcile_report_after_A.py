"""Final source report is a paraphrase with provenance, never human-case evidence."""
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/"AUDIT_REPORT.md"
s=p.read_text()
pairs=[
 ("**266 editorial documentary units R2306–R2571**","**267 editorial documentary units R2306–R2572**"),
 ("Lilly documentary inventory would be **2,571**, combined **3,637**","Lilly documentary inventory would be **2,572**, combined **3,638**"),
 ("A1/A2 first-review results must be reconciled before documentary acceptance.","Both split A1/A2 first-pass source reviews have been received and corrected; their page332 aspect-glyph disagreement remains open and no final blind rereview of the corrected reference packet has occurred.")
]
for a,z in pairs:
 assert s.count(a)==1,("missing report span",a)
 s=s.replace(a,z)
insert="""## First source-window readbacks: corrected source directions and open glyph (printed331–335)

The opening theft passage was independently re-read from original images in two separate smaller windows. Both first-pass reviews returned **FINDS_ERROR** and found several material changes of meaning. The printed p331 rule naming **LORD OF THE HOUR as ALSO LORD OF SEVENTH** only increases the supposed radicality of judgment; a **separate** later source claim says seventh lord in ascendant may point to querent only under a specific question of fidelity or when querent is the chief object of suspicion. The original source's subsequent complexion/sign rule does **not** require the hour/seventh identity. These are now separate R2319 and R2572 in \`SOURCE_ORDER.json\`, not one merged implied crime. A printed marginal word is **'consentanious'** (consonant with reason), not 'conscientious'; another sentence promises hope of **discovery** of goods, not actual guaranteed **recovery**. [PDF365; R2319,R2572,R2320,R2322,R2327; independent_review/OPUS_A1_INITIAL.json]

Multiple p332–333 worked conditional examples were repaired: the Sun as lord of second is in **TENTH**, not third, and no unprinted Sun/seventh sextile is added. In another example, Venus is in tenth **in sign of tenth**, while Moon **opposes** the seventh lord; a separate 'taken in jest' example also has Moon **opposing** seventh lord, not conjoining it. Another outcome says stolen-in-jest property will **'scant be had again'** (hard to recover), the opposite of a previous 'soon recovered' paraphrase. [PDF366–367; R2339,R2343,R2345,R2347; independent_review/OPUS_A1_INITIAL.json; OPUS_A2_INITIAL.json]

**Important unresolved original glyph:** A1 and A2 read the unusual aspect glyph in the p332 'taken away in jest' clause differently (**opposition vs conjunction** to the second HOUSE). The repaired R2338 preserves BOTH competing original-image readings as uncertainty, rather than making the attractive interpretation an executable rule. The destination is the printed **second HOUSE**, not an inferred second-house lord. More generally, source modalities 'in jest', 'scarcely recovered', 'possibly discovered', 'actually stolen' and 'suspected' are distinct authorial assertions, none empirically authenticated. [PDF366; R2338; A1_A2_RECONCILIATION.json]

Later source copies bear **handwritten** margin numbers 1–3, 5–8, possibly others, a large 7th-house annotation, the printed signature **Kk 3**, and a small letter/caret beside the printed last-line **Planet** on p335. These are catalogued as manuscript/bibliographic witnesses, **not additional numbered Lilly rules**; the owner of the annotations and their relation to the same-volume errata are unknown. [PDF365–369; ORIGINAL_MARGINALIA_REGISTER.json]

"""
marker="## Same-volume errata, evidentiary qualifications and final boundary"
assert s.count(marker)==1
s=s.replace(marker,insert+marker)
p.write_text(s)
print("REPORT_UPDATED_RECORDS",267,"BYTES",len(s.encode()))
