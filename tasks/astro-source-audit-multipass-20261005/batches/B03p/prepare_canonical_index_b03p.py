#!/usr/bin/env python3
"""Guarded indexed publication of original historical Lilly Chapter LXX."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03p_CHAPTER_LXX_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03p_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03p.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLDI,OLDC,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=I.read_bytes();idx=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert idx['records_count']==4007 and idx['batches'][-1]['id']=='B03o'
assert idx['next']['chapter']=='LXX' and idx['next']['pdf_page']==449
assert idx['read_numbered_chapters']==list(range(1,70))
assert idx['empirical_validations']==idx['runtime_promotions']==0
assert idx['source_sha256']==A['original_pdf_sha256']
assert A['new_documentary_records']==45 and A['lilly_if_published']==4052
assert R['record_count']==45 and [r['record_number'] for r in R['rules']]==list(range(4008,4053))
assert R['independently_validated_historical_cases']==0
assert Z['crc_pass'] and Z['member_hash_pass'] and Z['extracted_pass'] and Z['replayed_tests']==12
assert H(Z['local_owner_zip_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
path=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',path],cwd=ROOT).returncode==0
before=git('rev-parse','HEAD:'+path)
assert before==git('hash-object',str(I))
assert not any(x['id']=='B03p' for x in idx['batches'])
idx['batches'].append({'id':'B03p','path':'batches/B03p/RULES.json',
 'records_count':45,'sha256':A['rules_sha256'],
 'scope':'Original 1647 Lilly Book II Chapter LXX, separate 6 Feb 1644 9:10 PM spouse death-order case; original PDF449-450 plus next LXXI heading PDF451. 44 historical case source assertions and one next navigation, 14 source passages, 18 uncertainties. Author reports grave pre-existing illness and a later 8 Oct outcome after a forecast late Sep/early Oct of death OR grave danger; no independent case validation.'})
idx['records_count']=4052
idx['read_numbered_chapters'].append(70)
idx['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXX_DOCUMENTARY_SOURCE_ONLY_NEXT_LXXI_OPEN'
idx['next']={'pdf_page':451,'printed_page':417,'chapter':'LXXI',
 'heading':'A Woman of her Husband at Sea, if alive, where, when return?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'New Chapter LXXI begins original PDF451/printed417 with distinct square figure dated 15 April 1645.'}
idx['chapter_LXX_source_acceptance_note']='45 original historical documentary records R4008-R4052, 14 visual passage groups, 18 textual limits. Original 6 Feb 1644 case, severe illness known, missing natal data and source-reported 8 Oct later outcome. Forecast was late September/beginning October death OR great danger, not an exact preannounced 8 Oct death. Zero independent prediction validations.'
idx['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03p_CHAPTER_LXX_COMPLETE.md'
assert idx['records_count']==sum(x['records_count'] for x in idx['batches'])==4052
assert idx['read_numbered_chapters']==list(range(1,71))
report="""# Lilly Chapter LXX — original historical spouse case

Original William Lilly, Christian Astrology 1647, Wellcome b30338724. Separate square figure dated 6 February 1644 9:10 PM on original PDF449/printed415; body concludes PDF450/printed416. Chapter LXXI begins original PDF451/printed417.

Lilly reports that an unnamed man's wife was already seriously ill. He could not obtain her exact natal chart and was told her age was 42. He reports a forecast she would die OR face serious danger around late September or beginning October; then says she died on 8 October. October 8 was not the exact prospectively announced date, and no external contemporaneous prediction or independent mortality record was established. Astrological details matching the alleged event are offered retrospectively.

B03p admits 45 historical documentary clauses R4008-R4052, mapped to 14 source passages with 18 uncertainties. No independent predictive validation or model-runtime change. After authenticated publication Lilly 4,052 + Ptolemy 1,066 = 5,118 documentary annotations. Next LXXI starts PDF451.

Owner archive Astrology-Lilly-Chapter-LXX-Spouse-Case-Documentary-20261016.zip, CRC, full extraction and 12 source tests replayed.
"""
prefix="""# Current original astrology source research

Current 2026-10-16: Chapter LXX admitted as historical source only. Lilly 4,052 plus Ptolemy 1,066 after research publication. Next LXXI PDF451. No empirical prediction or runtime promotion.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(idx,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prefix+OLDC.read_text())
LATEST.write_text(report)
rec={'batch':'B03p','status':'LOCAL_GUARDED_SOURCE_INDEX_PREPARED_PENDING_REMOTE',
 'previous_git_index_blob':before,'old_index_sha256':H(OLDI),
 'new_index_sha256':H(I),'current_state_sha256':H(CUR),
 'latest_state_sha256':H(LATEST),'rules_sha256':A['rules_sha256'],
 'archive_sha256':Z['archive_sha256'],
 'new_documentary_units':45,'lilly_if_published':4052,'ptolemy':1066,
 'combined_if_published':5118,'next':'LXXI','next_pdf':451,
 'empirical_predictions':0,'runtime_promotions':0,'remote_published':False}
PREP.write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
