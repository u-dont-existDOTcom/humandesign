#!/usr/bin/env python3
"""Guarded historical LIX worked-chart source admission, not empirical validation."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03e_CHAPTER_LIX_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03e_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03e.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(p.exists() for p in (LATEST,OLDI,OLDC,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
G=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
a=json.loads((B/'ACCEPTANCE.json').read_text())
rules=json.loads((B/'RULES.json').read_text())
ziprec=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3360 and j['batches'][-1]['id']=='B03d'
assert j['next']['chapter']=='LIX' and j['next']['pdf_page']==419
assert j['read_numbered_chapters']==list(range(1,59))
assert j['runtime_promotions']==j['empirical_validations']==0
assert all(k['id']!='B03e' for k in j['batches'])
assert a['documentary_accepted_locally'] and a['whole_chapter_lix_documentary_accepted']
assert a['prior_accepted_lilly']==3360 and a['added_documentary_units']==58
assert a['source_reverse_passages']==25 and a['retained_ambiguities']==18
assert rules['record_count']==58
assert rules['rules'][-1]['chapter']=='LX_HEADING_ONLY'
assert [r['record_number'] for r in rules['rules']]==list(range(3361,3419))
assert all(r['chapter']=='LIX' for r in rules['rules'][:-1])
assert rules['independent_historical_outcome_confirmation']==0
assert rules['empirically_validated_predictive_results']==rules['runtime_promotions']==0
assert ziprec['zip_crc_pass'] and ziprec['file_sha256_and_bytes_pass'] and ziprec['actual_extraction_pass']
assert ziprec['extracted_source_test_count']==13 and ziprec['extracted_source_tests_exit_code']==0
assert H(ziprec['archive_on_laptop'])==ziprec['archive_sha256']
assert H(B/'RULES.json')==a['rules_sha256']==ziprec['accepted_rules_sha256']
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
prev=G('rev-parse','HEAD:'+rel)
assert prev==G('hash-object',str(I))
j['batches'].append({
 'id':'B03e','path':'batches/B03e/RULES.json','records_count':58,
 'sha256':a['rules_sha256'],
 'scope':'Original 1647 Book II Chapter LIX reported marriage horoscope, original PDF419 lower–PDF422 and next chapter LX heading PDF423: 57 historical case/diagram/editorial annotations and one LX boundary, 25 original-image reverse source passages, 18 unresolved chart/case issues. Claimed marriage outcome source-internal and partly affected by explicit advice, not independent empirical prediction.'})
j['records_count']=3418
j['read_numbered_chapters'].append(59)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LIX_DOCUMENTARY_SOURCE_ONLY_NEXT_LX_OPEN'
j['next']={
 'pdf_page':423,'printed_page':389,'chapter':'LX',
 'heading':'If she should marry the man desired?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF423/printed389 Chapter LX has an entirely separate worked marriage horoscope dated 11 June 1646, contrasted with LIX chart dated 16 June 1646. Preserve full original diagram and interpretation, do not conflate charts.'}
j['chapter_LIX_source_acceptance_note']='58 original-image historical documentary annotations incl LX header, 25 original passages, 18 uncertainty issues. Original 16 June 1646 square chart preserved with unresolved time and symbols, reported outcome not independently authenticated or blinding-frozen, social intermediary advice directly affected case. ZIP extraction replay 13 source tests, zero empirical or runtime promotion.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03e_CHAPTER_LIX_COMPLETE.md'
assert j['read_numbered_chapters']==list(range(1,60))
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3418
body="""# Lilly Book II Chapter LIX — 1647 worked horoscope original-source acceptance

2026-10-15 Africa/Dakar UTC+0. Original William Lilly Christian Astrology Wellcome b30338724, full original 894-page PDF verified SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LIX, *A Lady, if marry the Gentleman desired?*, begins original PDF419 printed385 BELOW the LVIII divider. The original square horoscope has a central date 16 June 1646 and apparently evening time; exact minute convention/rotated degree glyphs are NOT independently adjudicated into modern ephemeris coordinates. Its narrative occupies printed385–388/PDF419–422. Separate Chapter LX begins PDF423 printed389 with ANOTHER graphic dated 11 June 1646. Its heading is navigation-only within LIX and its astrological claims are excluded.

**Accepted B03e: 58 original historical source editorial units R3361–R3418**, 57 substantive LIX chart-and-case annotations and one LX header marker; 25 reverse original-image source passages, 18 retained chart/context/unverified-report limitations. The source reports that a social intermediary, approached after the astrologer's advice, helped arrange a marriage within twenty days. This is a single retrospective author account with feedback and active social intervention, NOT a frozen prospective astrological prediction or independently authenticated registry. The source also contains counterfactual lifespan, wealth, agreement and honesty claims; these are NOT observed outcomes.

**After authenticated remote publication: 3,418 Lilly + 1,066 retained Ptolemy = 4,484 historical documentary source units.** Zero independently confirmed prospective horary forecasts, clinical/couple/person character predictions or runtime rule promotion. The source archive Astrology-Lilly-Chapter-LIX-Documentary-20261015.zip in owner's French Telechargements passed ZIP integrity, individual file SHA-256, actual extraction and 13 original-source tests replayed. The original five scanned pages including both LIX and navigation-only LX diagram are included for image fidelity. This is not a complete blind diplomatic transcription.

**NEXT:** Original Chapter LX, *If she should marry the man desired?*, beginning original PDF423/printed389. Its June 11, 1646 chart must be independently mapped and chronologically separated from LIX June 16 chart. Continue overall historical book study; empirical performance study remains an independent future task.
"""
prefix="""# Current astrology source audit — newest accepted original historical checkpoint

2026-10-15 Africa/Dakar UTC+0. Book II Chapter LIX original worked marriage horary source-only accepted, 3,418 Lilly + 1,066 Ptolemy = 4,484 historical documentary units after authenticated research publication. Next Chapter LX has distinct chart dated 11 June 1646 on original PDF423 printed389, not same as Chapter LIX original 16 June chart. No independent empirical forecast confirmations or live model promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03e_CHAPTER_LIX_COMPLETE.md and B03e acceptance/source/receipt.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(prefix+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(body,encoding='utf-8')
r={'batch':'B03e','kind':'CANONICAL_SOURCE_INDEX_PREPARED_NOT_YET_REMOTE_PUBLISHED',
 'prior_index_git_blob_sha1':prev,'prior_index_sha256':H(OLDI),
 'new_index_sha256':H(I),'new_current_sha256':H(CUR),'new_latest_sha256':H(LATEST),
 'accepted_rules_sha256':a['rules_sha256'],'zip_release_sha256':ziprec['archive_sha256'],
 'new_historical_documentary_units':58,'lilly_if_published':3418,
 'retained_ptolemy':1066,'combined_if_published':4484,
 'next_chapter':'LX','next_original_pdf':423,'new_validated_predictions':0,
 'new_runtime_rule_promotions':0,'remote_publication_verified':False}
PREP.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(r,indent=2,ensure_ascii=False))
