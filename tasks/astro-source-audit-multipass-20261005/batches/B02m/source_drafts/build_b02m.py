#!/usr/bin/env python3
"""Compile the source-read B02m notes without adding doctrinal rules."""
from pathlib import Path
from collections import Counter
import hashlib,json,shutil,subprocess
P=Path(__file__).resolve().parent
OUT=P/'B02m'; OUT.mkdir(exist_ok=True)
SRC=Path('/home/joel/Documents/astrology/source-audit-20261005/Lilly-1647-Christian-Astrology-I-III.pdf')
EXPECTED='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
def H(b):return hashlib.sha256(b).hexdigest()
def J(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def T(name,text):(OUT/name).write_text(text)
assert SRC.stat().st_size==141842963
with SRC.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
assert digest==EXPECTED
raw=sum((json.loads((P/f'CURATED_PART{i}.json').read_text()) for i in (1,2,3)),[])
assert len(raw)==52
records=[]
for num,entry in enumerate(raw,1651):
    loc={'source_id':'LILLY1647_WELLCOME_B30338724','source_sha256':EXPECTED,
         'book':'II','chapter':'XLIV','section':'Hermes Trismegistus upon the first Decumbiture of the Sick',
         'pdf_pages':entry['pages'],'printed_pages':[p-34 for p in entry['pages']],
         'passage_anchor':entry['anchor'],'authority':'Original page images, not OCR'}
    records.append({'id':f'LI.1647.II.XLIV.R{num}','kind':entry['kind'].lower(),
      'title':(entry['section']+' — '+entry.get('sign',entry['anchor'])),
      'source_locator':loc,'historical_genre':'medicine_and_horary',
      'source_attribution':entry.get('attribution','Hermes-headed material in Lilly 1647; authorial interpolations uncollated'),
      'source_statement':entry['statement'],'prerequisites':entry.get('conditions',[]),
      'exceptions_and_modifiers':entry.get('limits',[]),'sign':entry.get('sign'),
      'planetary_afflictor':entry.get('planetary_afflictor'),'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED',
      'independent_evidence_unit':False,'case_id':None,
      'case_evidence':{'dated_enquiry':False,'worked_chart':False,'verified_outcome':False,'count_as_prediction':False},
      'source_reader_note':entry})
J('RULES.json',{'batch':'B02m','status':'SOURCE_ONLY','records_count':len(records),'rules':records})
assert set(sum((x['source_locator']['pdf_pages'] for x in records),[]))==set(range(302,317))
sat=[x for x in records if x['planetary_afflictor']=='Saturn']
mar=[x for x in records if x['planetary_afflictor']=='Mars']
zod='Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
assert [x['sign'] for x in sat]==zod
assert [x['sign'] for x in mar]==zod
kinds=Counter(x['kind'] for x in records)
summary={'batch':'B02m','previous_lilly':1650,'new_records':len(records),'first_new_id':1651,
  'last_new_id':1650+len(records),'cumulative_lilly':1650+len(records),'retained_ptolemy':1066,
  'combined':2716+len(records),'saturn_sign_rows':len(sat),'mars_sign_rows':len(mar),
  'source_pdf_pages':15,'dated_cases':0,'worked_charts':0,'verified_patient_outcomes':0,
  'clinical_and_predictive_validity':False,'kind_counts':kinds}
J('COUNTS.json',summary)
groups=[('Hermes introduction, conception/natal correspondence',302,303),('Decumbiture, planets, illness and conditions',304,305),('Historical remedies and medicines, two lists',306,307),('Saturn/Moon twelve-sign catalogue',307,311),('Mars/Moon twelve-sign catalogue',311,316)]
J('SECTION_COVERAGE.json',{'start':'PDF302 below divider','end':'PDF316 before divider',
  'all_admitted_pages':list(range(302,317)),
  'sections':[{'title':a,'pages':list(range(b,c+1)),'related_ids':[r['id'] for r in records if any(b<=p<=c for p in r['source_locator']['pdf_pages'])]} for a,b,c in groups],
  'note':'Overlapping location groups do not increase canonical record counts.'})
materia=json.loads((P/'MATERIA_MEDICA_TABLES.json').read_text())
J('MATERIA_MEDICA_TABLES.json',materia)
J('REFERENCE_TABLES.json',{'genre':'historical_unvalidated','zodiac_keys':zod,
   'saturn':{r['sign']:r['id'] for r in sat},'mars':{r['sign']:r['id'] for r in mar},
   'printed_senses':{'right_eye':'Sun','left_eye':'Moon','hearing_ears':'Saturn','brain':'Jupiter','blood':'Mars','smell_taste':'Venus','tongue_throat_lung_pipe':'Mercury'},
   'materia_file':'MATERIA_MEDICA_TABLES.json',
   'qualifier':'Saturn list has catalogue-wide Moon waning/slow and Saturn-afflicted scope; Mars sign-specific conditions must also be retained. No medical validation.'})
unresolved=[
  'Hermes attribution comes from Lilly 1647; original ancient text and Lilly interpolations not independently collated.',
  'Historical herb names, glyphs and original unusual spellings require text-specific witnesses; no fabricated modern plant IDs.',
  'Conception/birth and first decumbiture are distinct chart contexts.',
  'Daily Moon light and speed are not interchangeable; exact computations and calendar conversions unspecified here.',
  'All exceptions and conjunctions preserved; no automatic universal boolean grouping where ambiguous.',
  'Claims of nine, ten, fourteen, twenty and thirty days lack individual verified outcomes.',
  'Historic medicine lists include white lead and other potentially toxic substances; efficacy and safety unproven.',
  'Bloodletting, emetics and purging are documented history only, not treatment advice.',
  'Mars/Scorpio source insinuates moral or sexual guilt without evidence; never use as factual inference.',
  'Some illness cause, affected planet and cure polarity statements are internally hard to reconcile.',
  'Several Mars sign rows have individual additional lunar light, motion or other restrictions.',
  'First-person experience reports have no patient counts, controls or independent follow-up.',
  'No complete source-independent replication or empirical predictive validation.',
  'Original source pages are retained externally; evidence rasters are locating images, not a diplomatic transcription.'
]
J('UNRESOLVED.json',{'limits':[{'id':f'U{i:02d}','status':'RETAINED','description':s} for i,s in enumerate(unresolved,1)],'retained_count':len(unresolved)})
(OUT/'evidence').mkdir(exist_ok=True)
images=[]
for pg in range(302,317):
    path=P/'visual'/f'pdf-{pg}.png'
    assert path.is_file(),pg
    rawimg=path.read_bytes()
    target=OUT/'evidence'/f'pdf-{pg}.png'
    if not target.exists() or H(target.read_bytes())!=H(rawimg):shutil.copyfile(path,target)
    images.append({'page':pg,'printed_page':pg-34,'path':'evidence/'+target.name,'bytes':len(rawimg),'sha256':H(rawimg)})
J('SOURCE_IMAGE_MANIFEST.json',{'source_pdf_sha256':EXPECTED,'rendering':'pdftoppm, PNG scaled to 1800px; original PDF is full visual authority','images':images})
J('SOURCE_IDENTITY.json',{'id':'LILLY1647_WELLCOME_B30338724','sha256':EXPECTED,'bytes':SRC.stat().st_size,'pages':894,'read_span_pdf_pages':list(range(302,317))})
T('SOURCES.md',f'# Primary witness\nWilliam Lilly, Christian Astrology (1647), Wellcome scan b30338724, 894 pages; SHA256 {EXPECTED}. Original page images PDF302–316 directly read; opening below first divider, ending above last divider. Included page renders are locating evidence; actual full-volume PDF remains external. There is no independent Hermes original-language collation, historical case validation or modern medical validation.\n')
T('CONTINUE_HANDOFF.md',f'# B02m continuation\nCompleted historical Hermes section, original PDF302/printed268 below divider through PDF316/printed282 above divider, including both 12-sign catalogues and historical remedies. New {len(records)} records R1651–R{1650+len(records)}; cumulative Lilly {1650+len(records)}, Ptolemy 1066, combined {2716+len(records)}. Chapter XLIV and wider audit OPEN.\n\nNext source PDF316/printed282 **below the horizontal divider**, heading **Astrologicall Aphorismes beneficiall for Physicians**, including the first complete numbered aphorism; then PDF317. Next record **R{1651+len(records)}**. Preserve earlier batches, models, personal inputs and prediction freezes. Read current UDA / HumanDesign AGENTS, this batch and unresolved register before further rules.\n')
report=f"""# Lilly Book II: Hermes-headed historical illness material
11 October 2026 — B02m source-only research.

## Completed source span
Original PDF302, printed268 below the divider and heading 'Hermes Trismegistus upon the first Decumbiture of the Sick', through original PDF316, printed282 above the divider and the next heading 'Astrologicall Aphorismes beneficiall for Physicians'. The fifteen original source pages have been read in their page-image form; all intervening material is accounted for.

This batch adds **{len(records)} documentary source records, R1651–R{1650+len(records)}**. Lilly cumulative {1650+len(records)}, retained Ptolemy 1,066, combined {2716+len(records)}. The inventory is not independent observations. There is no dated patient enquiry, worked chart or verified medical outcome in the admitted section.

## Findings
**1. Context is essential.** The opening moves from conception and nativity planetary assignments to first-decumbiture illness horary. The later physician inquiry is a fallback only when the original onset hour is unavailable. These are not one universal timing procedure.

**2. The sensory table gives distinct assignments.** Right eye Sun, left eye Moon, Saturn hearing/ears, Jupiter brain, Mars blood, Venus smell/taste, Mercury tongue and throat/lung pipe. It separately names the four principal parts head, breast, hands and feet. These are source assertions, not modern physiology.

**3. Lunar aspects have joint requirements.** Light, speed, conjunction/square/opposition and intervening benefics change the textual judgment. The immediate remission following Saturn opposition and a subsequent good aspect are important exceptions. A rule engine that counted every statement as a separate vote would duplicate dependencies.

**4. Two catalogues have different local conditions.** The first presents twelve signs with the Moon waning/slowing and afflicted by Saturn; the second uses Mars, with individual sign-specific additional conditions. Gemini/Saturn's ten-day danger also introduces Mars; Leo/Mars cites agreement of other configurations for its ninth-day death claim; Virgo/Mars requires no benefic aid for the thirty-day claim; Aquarius/Mars has a separate alleged twenty-day relief condition. A timing mention is not an independently verified outcome.

**5. Medicine material is documentary only.** Cooling and warming materia medica lists span printed pages272–273, with 3-column spellings preserved separately. White lead and other potentially hazardous substances appear, alongside historic bloodletting and purging. The source is NOT reliable clinical advice. No ingestion/treatment/dosing claims are endorsed.

**6. The first-person statements have no denominator.** The heading attributes material to Hermes in Lilly's 1647 presentation, but 'I find by experience' passages cannot be confidently assigned to the ancient author without another edition. The Mars/Scorpio sexual blame insinuation has no evidentiary validity about any person.

## Use and limitations
RULES.json holds the normalized source statements with precise page anchors, full declared local conditions and limits. REFERENCE_TABLES.json keeps 12 Saturn and 12 Mars rows separate. MATERIA_MEDICA_TABLES.json retains historical nomenclature. UNRESOLVED.json records 14 textual, implementation and evidence limitations. Fifteen original page-render PNGs have exact hashes in SOURCE_IMAGE_MANIFEST.json. This is historical preservation, not an executable natal horoscope or an evidence-based medical system.

## Continuation
PDF316, printed282 **below the divider**, *Astrologicall Aphorismes beneficiall for Physicians*; next R{1651+len(records)}. Chapter XLIV and the multipass astrology book audit remain OPEN.
"""
T('AUDIT_REPORT.md',report)
print(json.dumps({'source_verified':True,'records':len(records),'lilly':summary['cumulative_lilly'],'combined':summary['combined'],'images':len(images),'unresolved':len(unresolved),'output':str(OUT)}))
