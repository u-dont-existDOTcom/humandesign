# B53 — Actual 1929 Sanskrit plate check: Sarvārtha Cintāmaṇi

**22 October 2026, source criticism only.** This pass resolves B52's specific missing-evidence problem: it visually inspects a printed Sanskrit witness, rather than inferring the glyphs from digital Devanāgarī. It does **not** authenticate a manuscript, establish a critical text, validate a birth-chart prediction, or justify any moral or economic prognosis.

## Physical witness and procedure

- **Source:** *Sarvarth Chintamani*, Mahīdhara Śarmā bhāṣā-ṭīkā printing, dated **1929**, Internet Archive ID `in.ernet.dli.2015.312429` (Digital Library of India). Public-domain historical edition, not the Bhasin translation.
- **Book URL:** `https://archive.org/details/in.ernet.dli.2015.312429`; downloaded 8,735,151-byte PDF `2015.312429.Sarvarth-Chintamani.pdf`; **SHA-256** `8fc0e8a5a212d1b3312363135347c47846671a3d184232eaf276ea0c96f57624`; **298 PDF pages**, with PDF page 1 indexing.
- **Evidence workflow:** obtained scanned PDF on an authorized research machine, extracted Internet Archive's OCR *for navigation only*, mapped original printed page numbers using the Archive scandata metadata, rendered PDF pp.166–173 at 165 dpi and the key pages at 320 dpi, then **visually read source images**. OCR was *not* accepted as a witness by itself. The text has no selectable PDF text layer; images were inspected directly.
- **Parallel modern edition:** user's originally uploaded J. N. Bhasin English *Sarvārtha Cintāmaṇi*, scanned PDF pp.204,206–208 and 212–213, as indexed in Library. This PDF has corrupted extracted Sanskrit fonts; its English prose is legible. Also checked Sanskrit e-text and editorial English at VedicPupil chapter 8, a digital proxy **not counted as a separate physical manuscript**.
- **Lineage limit:** Karma Sakha's edition audit reports 1929 Bombay and 2015 Gauḍ/1906 Mumbai/ Khemraj-related printings may share a printing family. Bhasin's Sanskrit underlying edition is unspecified. **One physically checked 1929 print is not multiple independent manuscript recensions**, regardless of website agreement.

## Five high-leverage visual checks

| Source locus | Original PDF leaf/printed page | Image-grounded Sanskrit evidence | Bhasin English layer | Disposition |
|---|---|---|---|---|
| Tenth-house vv2–3 | PDF166–167 / pp148–149 | v2 uses `यज्ञकरा` (sacrifice-acting); v3 adverse case names `शशांकात्मजजीवशुक्राः` = Mercury, Jupiter, **Venus**, not simply v2's three | v2–3 recast this as service to others and acts helping public causes; v3 says “these three” (tenth lord/Jupiter/Mercury) for negative case | **Two separate problems:** target-domain drift (ritual → generic public service), and conditional planet-list mismatch. No canonical forecast. |
| Tenth-house v16 | PDF168 / p150 | `आज्ञास्थानगते सूर्ये भूमिपुत्रेण वा युते` contains printed `वा` (“or”) | Sun in tenth **and** joined Mars and angular tenth lord | Material **AND-vs-OR** difference, but exact full syntax/priority remains uncollated; no personal ethics forecast. |
| Tenth-house v24 | PDF169 / p151 | adverse antecedent `पापग्रहाणां सम्बन्धे ... क्रूरषष्ट्यंशसंयुक्ते`, **favorable** ending `सत्कीर्तिसहितो भवेत्` | **Bad name** / unfavorable reputation under adverse antecedent | **Genuine printed Sanskrit–English polarity discrepancy**. The 1929 Hindi gloss refers to the preceding “same result”; a dittography/semantic correction is plausible but **not proven**. Preserve 1929 favorable and Bhasin unfavorable versions without silently emending either. |
| Eleventh-house v2 | PDF171 / p153 | `लाभे वा पापसंयुक्ते धनलाभमुदीरयेत्` gives **gain** with malefic joined to eleventh as one alternative | Gain when a malefic occupies eleventh, or lord in kendra/trine | Both source layers agree on the positive clause. |
| Eleventh-house v10 | PDF172 / p154 | `लाभे पापे तद्गृहे वा धनहानिं विनिर्दिशेत्` gives **loss** when malefic in eleventh | Loss when malefic occupies eleventh or afflicts the lord | Both source layers agree on the negative clause. The two clauses can coactivate; neither scanned pair nor nearby v9 supplies a global priority. |

**Key conclusion:** the prior B50/B51 “source-versus-translation” concerns are **confirmed as genuine statements of the 1929 physical printing**. This is a more robust documentary claim than “an online Sanskrit site says”. It still **does not** prove whether the 1929 printing preserves the author's earliest wording, whether one stanza has a scribal error, or how a traditional astrologer would resolve all competing yogas.

## Model and ethics boundary

The ritual/public-service distinction matters for a future questionnaire: a generic “I help the public” answer is not confirmation of an early Sanskrit condition that specifically describes Vedic ritual. Likewise, fame after malefic tenth-lord conditions and wealth gain/loss from a malefic in the eleventh are versioned, non-scoring historical statements. They cannot be retrospectively combined, “fixed,” or selected according to a person's reputation or finances.

The diagnostic file `original_witness_integrity_B53.py` encodes **alternative source-version predicates**, edition metadata, and collision status. `test_original_witness_integrity_B53.py` passed **19/19** checks. These verify that the alternatives are preserved and never scored; they are not astrology validation or independent OCR adjudication.

**Cumulative status:** the five-book reader still has **432 distinct source-only annotations**, **0** validated real-human prospective predictions, **0** production-rule promotions. B53 contributes five physically verified *existing* loci, not new de-duplicated source IDs.

**Next:** compare the Sanskrit readings with a genuinely separate manuscript/edition if accessible (1906/1925 alone may share the Bombay lineage); continue *Jātaka Pārijāta* profession and prosperity cases and isolate actually new conditional information from borrowed *Bṛhat Jātaka* core verses. Preserve known non-hits and null hypotheses. No other reader, survey, person or model is altered.
