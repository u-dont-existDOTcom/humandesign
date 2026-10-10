"""Rebuild canonical B02j from frozen source-reader inputs and root transcription."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
SOURCE='LILLY1647_WELLCOME_B30338724'
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
SCOPE='Complete fifth-house heading and XXXIX–XLIII with every intervening unnumbered section, PDF256 below divider through276; before sixth-house heading/XLIV on PDF277.'


def read(path): return json.loads((HERE/path).read_text())
def write(path,data): (HERE/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


raw=[]
for reader,file in [('A','source_readers/a/CANDIDATE_RULES.json'),('B','source_readers/b/CANDIDATE_RULES.json'),('root','ROOT_CANDIDATE_RULES.json')]:
    data=read(file)
    rows=data if isinstance(data,list) else data['records']
    raw.extend((reader,row) for row in rows)
ids={row['id']:f"LI.1647.II.{row['chapter']}.R{1157+i}" for i,(_,row) in enumerate(raw)}
issues=[]
for reader,file,key in [('A','source_readers/a/UNRESOLVED.json','issues'),('B','source_readers/b/UNRESOLVED.json','items'),('root','ROOT_UNRESOLVED.json','issues')]:
    for row in read(file)[key]:
        new=dict(row)
        new['id']='U-C'+row['id'][1:] if reader=='root' else row['id']
        new['source_reader']=reader
        new['status']=row.get('status','PRESERVED_UNRESOLVED')
        new['record_ids']=[ids[x] for x in row.get('candidate_ids',[]) if x in ids]
        issues.append(new)
issue_ids={x['id'] for x in issues}
canon=[]
for reader,row in raw:
    unresolved=[]
    for detail in row.get('uncertainty',[]):
        for token in re.findall(r'U-A\d{2}|UB\d{3}|\bC\d{2}\b',detail):
            token='U-'+token if token.startswith('C') else token
            if token in issue_ids and token not in unresolved: unresolved.append(token)
    for issue in issues:
        if row['id'] in issue.get('candidate_ids',[]) and issue['id'] not in unresolved: unresolved.append(issue['id'])
    attribution='Lilly'
    if row['id']=='A008': attribution='Lilly reporting unnamed some say'
    if row['id']=='A027': attribution='Lilly reporting unnamed Others observe'
    if row['id'] in [f'B{i:03d}' for i in range(34,43)]: attribution='Lilly reporting Some say; endpoint of anonymous voice unresolved'
    new={
      'id':ids[row['id']], 'local_id':row['id'],
      'title':row.get('title',row['section']+' — '+row['id']),
      'kind':row['kind'],
      'source_locator':{'source_id':SOURCE,'source_sha256':SHA,'book':'II','section_key':'II.'+row['chapter'],
        'pdf_pages':row['pdf_pages'],'printed_sequence_expected':row['printed_pages'],
        'visible_printed_labels':[str(p) for p in row['printed_pages']],
        'passage_anchor':row['anchor'],
        'anchor_note':row.get('anchor_type','Short locating phrase checked against original image; long-s, glyph names and spacing normalized where stated in reader provenance; not a full diplomatic transcription.')},
      'genre':'historical_horary_source', 'statement_type':'editor_normalized_paraphrase',
      'source_attribution':attribution, 'source_statement':row['assertion'],
      'prerequisites':[{'source_clauses':row.get('conditions',[]),'condition_logic':row['condition_logic'],'executable':False}],
      'qualifications_and_limits':row.get('exceptions',[])+row.get('uncertainty',[]),
      'source_fields':row, 'source_reader':reader,
      'unresolved_ids':unresolved,
      'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED',
      'independent_evidence_unit':False,
      'case_id':row.get('case_id'),
      'related_record_ids':[ids[x] for x in row.get('dependencies',[]) if x in ids],
    }
    canon.append(new)
    for issue in issues:
        if issue['id'] in unresolved and new['id'] not in issue['record_ids']: issue['record_ids'].append(new['id'])
worked=sum(bool(x['case_id']) for x in canon)
write('RECORD_ID_MAP.json',{'batch':'B02j','map':ids})
write('RULES.json',{'schema_version':1,'batch':'B02j','source_id':SOURCE,'source_sha256':SHA,'status':'SOURCE_ONLY_NOT_RUNTIME_OR_VALIDATION','scope':SCOPE,'records_count':len(canon),'general_records_count':len(canon)-worked,'worked_example_records_count':worked,'rules':canon})
write('UNRESOLVED.json',{'batch':'B02j','issues_count':len(issues),'count_semantics':'Typed register entries for unresolved source grammar, local implementation dependencies, variants and evidence limits. Entries can group related gaps; inline qualifications remain in records. This is not a count of source errors.','issues':issues})
sections=[]
for reader in ('a','b'):
    for i,s in enumerate(read(f'source_readers/{reader}/SECTION_COVERAGE.json')['sections'],1):
        candidate_ids=s['candidate_ids']
        sections.append({'id':reader.upper()+f'-S{i:02d}',
          'title':s.get('title',' / '.join(s.get('headings_and_unheaded_units',[]))),
          'pdf_pages':s['pdf_pages'],'printed_pages':s['printed_pages'],
          'record_ids':[ids[x] for x in candidate_ids],
          'headings_and_unheaded_units':s.get('headings_and_unheaded_units',s.get('internal_subheadings',[])),
          'source_reader_details':s,'status':'ORIGINAL_IMAGES_READ_AND_EXTRACTED'})
for i,(title,selected) in enumerate([
 ('XLII: first figure, judgment, counterfactuals, symptoms and marks',[row for _,row in raw if row['id'].startswith('C') and row.get('case_id')=='LILLY_II_XLII_1635_CHILDREN']),
 ('XLII continuation: nativity comparison and first-question resemblance',[row for _,row in raw if row['id'].startswith('C') and row['chapter']=='XLII' and not row.get('case_id')]),
 ('XLIII: second figure and child-sex testimony table',[row for _,row in raw if row['id'].startswith('C') and row['chapter']=='XLIII' and max(row['pdf_pages'])<=275]),
 ('XLIII continuation: delivery arithmetic and reported outcome/transits',[row for _,row in raw if row['id'].startswith('C') and row['chapter']=='XLIII' and max(row['pdf_pages'])==276]),
],1):
    pages=sorted({p for x in selected for p in x['pdf_pages']})
    sections.append({'id':f'C-S{i:02d}','title':title,'pdf_pages':pages,'printed_pages':[p-34 for p in pages],'record_ids':[ids[x['id']] for x in selected],'status':'ORIGINAL_IMAGES_READ_AND_EXTRACTED'})
next_passage={'pdf_page':277,'printed_page':243,'heading':'Of the sixt House, and its Questions. Viz. Sicknesse, Servants, small Cattle.','chapter':'XLIV','chapter_heading':'Judgment of Sicknesse by ASTROLOGY.','position':'At top of page; include sixth-house heading, topic list, XLIV heading and full opening paragraph.','extracted':False,'boundary_image_read':True}
assigned=[x for s in sections for x in s['record_ids']]
assert Counter(assigned)==Counter(x['id'] for x in canon)
write('SECTION_COVERAGE.json',{'batch':'B02j','scope':SCOPE,'admitted_pdf_pages':list(range(256,277)),'numbered_chapters':['XXXIX','XL','XLI','XLII','XLIII'],'fifth_house_heading':{'pdf_page':256,'printed_page':222,'position':'below divider; bare heading is covered with XXXIX opening, no separate doctrine fabricated'},'section_unit_count':len(sections),'sections':sections,'next':next_passage,'book_complete':False})
cases=read('HISTORICAL_CASES.json')
for case in cases['cases']:
    # Keep temporary provenance and canonical references separately; repeatable.
    local=case.get('local_record_ids',case['dependent_record_ids'])
    case['local_record_ids']=local
    case['dependent_record_ids']=[ids[x] for x in local]
write('HISTORICAL_CASES.json',cases)
print(json.dumps({'records':len(canon),'first':canon[0]['id'],'last':canon[-1]['id'],'general':len(canon)-worked,'worked':worked,'issues':len(issues),'section_units':len(sections)}))
