from pathlib import Path
import json,hashlib
Q=Path('/workspace/scratch/43f75264c32e/b02l-workers/independent/repair_round01');I=Q.parent
P1=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-01');P2=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-02')
def bind(base,path):
 b=(base/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,o):(Q/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
m=json.loads((Q/'MECHANICAL_CARRY_FORWARD.json').read_text());l1=json.loads((P1/'CLAIM_LEDGER.json').read_text());l2=json.loads((P2/'CLAIM_LEDGER.json').read_text());old={x['id']:x for x in l1['items']};new={x['id']:x for x in l2['items']}
r1=json.loads((P1/'RULES.json').read_text());r2=json.loads((P2/'RULES.json').read_text());r1.pop('rules');r2.pop('rules');assert r1==r2
m['rules_top_level_metadata_unchanged']=True;save('MECHANICAL_CARRY_FORWARD.json',m)
checks=[
{'finding':'IF-01','target':'R1560/A011','status':'resolved','pdf_pages':[294],'printed_pages':[260],'source_anchor':'or from the principall Significators in the Figure','inspection':'Original PDF294 crop shows the plural. All seven affected leaf strings now use significators; title/proposition/conditions/uncertainties and canonical duplicates agree. Repeated-from uncertainty, alternatives, dependencies and non-executable status remain unchanged. No all-of-group requirement or vote count was added.','evidence':'original_pdf294_plural_exclusions_pagebreak.png'},
{'finding':'IF-02','target':'C10','status':'resolved','pdf_pages':[294],'printed_pages':[260],'source_anchor':'and neither of them be Lords of the sixt, or Dispositors of the Moon','inspection':'The repaired text explicitly applies the sixth-lord and Moon-dispositor exclusions to both Saturn and Mars. Strength, square/opposition, unwell versus perfectly sick, house inquiry, application/separation and local opposition qualification carry forward unchanged. R1562 is unchanged.','evidence':'original_pdf294_plural_exclusions_pagebreak.png'},
{'finding':'IF-03','target':'C35','status':'resolved','pdf_pages':[283,301],'printed_pages':[249,267],'source_anchor':'according to the nature and quality of the Signe; discretion and quality of the Disease; nature of the Disease','inspection':'Original PDF283 names the sign selector; original PDF301 supplies disease quality/nature and discretion. The repaired paragraph distinguishes them and preserves the no-combined-algorithm and future-figures evidence limits. Retained R1438 is unchanged.','evidence':['original_pdf283_earlier_sign_selector.png','original_pdf301_later_disease_selector.png']},
{'finding':'IF-04','target':'C09','status':'resolved','pdf_pages':[293,294],'printed_pages':[259,260],'source_anchor':'any Planet may in / this case be malignant, if he be Lord of the eighth, twelfth or sixt','inspection':'The new citation and ledger page list include PDF294/printed260. Original images confirm the list crosses that page break. The semantic paragraph and R1559 are unchanged.','evidence':['original_pdf293_no_sickness_and_cause.png','original_pdf294_plural_exclusions_pagebreak.png']},
{'finding':'IF-05','target':'C24','status':'resolved','pdf_pages':[300],'printed_pages':[266],'source_anchor':'the Signe of the eighth House of the yearly revolution of the World','inspection':'The repaired report now names the sign of the eighth house of the yearly world revolution. The natal-angle/ascendant emphasis and distinction from natal or horary eighth houses remain. Optional nativity, match/nearness uncertainty and first-sickness-or-demand alternative remain unchanged. R1629 is unchanged.','evidence':'original_pdf300_eighth_house_sign.png'},
{'finding':'IF-06','target':'C08','status':'resolved','pdf_pages':[293],'printed_pages':[259],'source_anchor':'they were not sick, or that no sicknesse would succeed upon this Quere, but that their mistrust ... was grounded upon some sudden distemper of Body','inspection':'The repaired paragraph connects the transient bodily distemper to the explanation of suspicion accompanying the alternative no-present/no-ensuing-sickness judgments. The opening negative-scope uncertainty and refusal to add an unprinted negative or executable polarity remain. R1557 is unchanged.','evidence':'original_pdf293_no_sickness_and_cause.png'},
{'finding':'MC-01','target':'C42','status':'original_text_binding_gap_resolved_with_separate_reference_issue','pdf_pages':[292,302],'printed_pages':[258,268],'source_anchor':'DARIOT Abridged; upper bridge before Hermes; provided task metadata','inspection':'C42 binds the existing title/byline exactly once and its text hash matches. The title/topic, Book II Chapter XLIV continuation, B02l label and 10 October2026 byline were already assessed in MC-01 against the source context and provided task-start metadata. No metadata text was changed. The new TASK_ENVELOPE.json evidence reference is unavailable in the frozen candidate; see RR1-01.','evidence':'Initial frozen MC-01 finding and current report/ledger text binding'}]
remaining=[{'id':'RR1-01','classification':'new_metadata_evidence_reference_not_resolvable_in_candidate','target':'CLAIM_LEDGER.json C42 evidence_files','referenced_file':'TASK_ENVELOPE.json','facts':'TASK_ENVELOPE.json does not exist at the stated candidate-relative location and is not among the45 manifest-listed files. SECTION_COVERAGE.json does exist. The declared modern byline date is supported by the provided task-start metadata; this is a packet reference defect, not a finding that the metadata facts are false.','bounded_correction':'Include and manifest the exact task envelope being cited, or replace the unavailable filename with a truthful, available provenance reference for the metadata. Keep the already-correct title/byline binding.','required_semantic_rework':'None to R1560 or C08/C09/C10/C24/C35. No further source sweep or new tests are requested.','why_in_scope':'The reference was newly introduced by C42, which this repair round explicitly required checking. This is the existing evidence-link obligation, not a new assurance gate.'}]
claimresults=[]
for cid in ['C08','C09','C10','C24','C35','C42']:
 relevant=[x for x in checks if x['target']==cid]
 claimresults.append({'id':cid,'before':old.get(cid),'after':new[cid],'assessment':relevant[0]['inspection'],'status':relevant[0]['status'],'finding':relevant[0]['finding'],'remaining_issue_ids':['RR1-01'] if cid=='C42' else []})
coverage={'source_first_units_retained':92,'final_canonical_records':101,'unchanged_record_objects_carried_forward':100,'changed_record_rechecked':1,'changed_record_id':'LI.1647.II.XLIV.R1560','initial_ledger_units':41,'unchanged_ledger_objects_carried_forward':36,'changed_existing_ledger_units_rechecked':5,'new_metadata_ledger_units_checked':1,'final_ledger_units':42,'all_final42_texts_uniquely_bound_and_hash_verified':True,'initial25_table_data_rows_unchanged_and_carried_forward':25,'report_outside_five_changed_units_identical':True,'canonical_distinct_tests':20,'new_test_identities_in_repair_round':0,'independent_test_rerun_this_round':False,'initial_source_window_pixel_checks_carried_forward':14,'source_window_file_hash_unchanged':True,'remaining_source_meaning_corrections':0,'remaining_metadata_reference_corrections':1,'assurance_note':'Counts measure review inventory and carry-forward identity, not independent predictions or an accuracy percentage.'}
result={'stage':'changed-item repair round1','candidate_manifest':bind(P2,'CANDIDATE_MANIFEST.json'),'initial_diagnosis_freeze':bind(I,'INITIAL_DIAGNOSIS_FREEZE.json'),'checks':checks,'claim_results':claimresults,'changed_record_field_differences':m['changed_record_leaf_differences'],'remaining_required_corrections':remaining,'final_coverage_accounting':coverage,'acceptance_recommendation':{'source_and_report_meaning':'Accept IF-01 through IF-06 as resolved. Accept MC-01 title/byline text binding as repaired.','packet_reference_completeness':'One narrow correction remains: resolve C42 TASK_ENVELOPE.json evidence reference (RR1-01).','final_adjudication':'Root retains final adjudication. This reviewer does not add an extra source, test or assurance gate.','further_review_scope_if_requested':'At most the one remaining changed-item repair round under the original two-round limit; inspect only the metadata-reference repair and resulting bindings.'},'preserved_initial_context':{'source_first_freeze_unchanged':True,'initial_diagnosis_and_all_bound_files_unchanged':True,'SC-01':'Candidate vitious remains correct; initial source-first viscous reading remains disclosed as reviewer error.','SC-02':'Candidate she longs after remains correct; initial source-first he anchor remains disclosed as reviewer error.','IC-01':'Nonunique fire-sign-context inheritance remains as previously diagnosed; unchanged R1601 was not reopened or newly adjudicated.'},'scope_and_exposure':{'original_source_images_rechecked_only_for_changed_assertions':[283,293,294,300,301],'unchanged_records_and_claims':'Mechanically compared by object identity and normalized hashes; original semantic conclusions carry forward.','root_narrative':'ROOT_SOURCE_CORRECTIONS.json was hash-verified only as a listed file; its narrative was not read. No other-worker/root narrative or status files were consulted.','test_evidence':'Inspected repaired actual20-test receipt and log, compared identical test IDs and helper/test/runner bytes, and verified every tested-file hash. Did not rerun unchanged test code in this repair round.','metadata_date_evidence':'Provided task-start metadata, as already recorded in frozen MC-01. No mid-task clock read or invented completion time.','writes':'Private repair_round01 directory only; no canonical/candidate modifications.','semantic_findings_released_before_freeze':False,'independence_limit':'Same-family contextual diagnostic separation; no clinical, cross-family, expert, IV&V or empirical validation claim.'}}
save('CHANGED_ITEM_RESULTS.json',result)
md='''# B02l changed-item repair round 1

## Recommendation

**Accept IF-01 through IF-06 as resolved.** R1560 and the five repaired report units now preserve the source readings identified in the frozen initial diagnosis. The new C42 correctly binds the existing title/byline, resolving MC-01’s omitted-text-binding issue.

**One metadata evidence-reference correction remains:** C42 cites `TASK_ENVELOPE.json`, but that file is absent from the frozen candidate and its 45-file manifest. This is RR1-01. The metadata facts themselves remain supported by the source context and provided task-start metadata. Include and manifest the exact cited task envelope, or replace that unavailable filename with a truthful, available provenance reference. No further change to R1560 or the five corrected source paragraphs is required.

This is a recommendation within the agreed diagnostic role. Root retains final adjudication. The remaining reference issue was introduced in the expressly reviewed C42; it is not an additional source-review, testing or assurance gate.

## Source-adjudicated repairs

| Finding | Target | Round-one result |
|---|---|---|
| IF-01 | R1560/A011 | Original PDF294/printed260 prints **principall Significators**. All seven affected canonical/duplicate strings now preserve the plural. The repeated-from uncertainty remains; no all-of-group rule is added. |
| IF-02 | C10 | Exclusions now apply to **both Saturn and Mars**, matching original **neither of them** on PDF294. Prior strength, square/opposition and other qualifications remain. R1562 is unchanged. |
| IF-03 | C35 | Earlier PDF283/printed249 **sign nature/quality** is separated from later PDF301/printed267 **disease quality/nature and discretion**. No combined algorithm or extra cases are inferred. R1438 is unchanged. |
| IF-04 | C09 | PDF294/printed260 is now included in the citation and ledger page list for the lordship clause crossing the page break. Meaning and R1559 are unchanged. |
| IF-05 | C24 | **Sign of the eighth house of the yearly revolution of the World** is restored, retaining the natal-angle reference frame and other qualifications. R1629 is unchanged. |
| IF-06 | C08 | The transient distemper is now the explanation of suspicion accompanying alternative no-present/no-ensuing-sickness judgments. Negative-scope uncertainty remains. R1557 is unchanged. |
| MC-01 | C42 | Existing title/byline is uniquely bound and correctly hashed. Its factual metadata is supported. A newly introduced unavailable evidence filename remains as RR1-01. |

I inspected direct original-PDF crops only for the changed assertions, on PDF283,293,294,300 and301. Unchanged sections were not reopened for another exhaustive source review. The exact before/after claim texts, changed record leaves and point-of-use evidence are retained in `CHANGED_ITEM_RESULTS.json`.

## Remaining correction: RR1-01

C42 lists `SECTION_COVERAGE.json` and `TASK_ENVELOPE.json` as evidence. The first exists and is manifest-bound. The second does not exist in `/workspace/scratch/43f75264c32e/review-candidate-b02l-02/` and is absent from `CANDIDATE_MANIFEST.json`.

The report title/byline was already present in candidate01 and was supported in frozen MC-01. This finding concerns the newly introduced evidence pointer, not an assertion that the date or batch label is false. The bounded repair is to package the actual cited envelope or use an available, truthful metadata-provenance reference. No new source research, helper change or test identity is requested.

## Exact carry-forward accounting

| Inventory | Final accounting |
|---|---:|
| Source-first units retained | 92 |
| Canonical records | 101 = 100 unchanged + 1 rechecked |
| Ledger units | 42 = 36 unchanged + 5 rechecked + 1 new metadata unit |
| Table data rows | 25, unchanged and carried forward |
| Candidate02 manifest files verified | 45 |
| Original source-window page comparisons carried forward | 14 |
| Canonical distinct focused tests | 20 |
| New test identities in this round | 0 |
| Remaining source-meaning corrections | 0 |
| Remaining metadata-reference corrections | 1 |

The 100 unchanged records are identical JSON objects, with matching normalized hashes. The 36 unchanged ledger items are identical complete objects, including text, citations and qualifiers. After substituting placeholders for the five changed report units, candidate01 and candidate02 report text is identical. C42 binds the existing title/byline; it does not add or modify report prose. All 42 ledger texts occur exactly once and match their text hashes. All substantive report text and the formerly unbound metadata remain accounted for; unchanged organizational headings carry forward from the original whole-report scan.

Only six existing manifest files changed: `RULES.json`, `AUDIT_REPORT.md`, `CLAIM_LEDGER.json`, the current Lilly index snapshot, the actual test summary, and the actual test log. The two added files are `ROOT_SOURCE_CORRECTIONS.json` and `REPAIR_ROUND01_CHANGESET.json`. The former was hash-verified as a file without reading its narrative. All 45 declared file hashes and byte counts match.

## Helper, tests and index

The helper, test module and runner are byte-identical to candidate01. The repaired actual test receipt and log report the same 20 tests, with no failure, error or skip. The exact test ID list is unchanged, and every receipt-bound tested-file hash matches candidate02. The current Lilly index differs only in the current B02l `RULES.json` hash, now:

`7f95bfd2e73d8c3c6f5ababdd12ee6e04b45fae314b35323ae50f905899c966c`

I did not run an additional independent suite in this repair round. The initial private execution and helper behavior review carry forward through unchanged code/test identities; the repaired actual receipt is checked against the changed data/index hashes. Repeated execution creates no new test identities. No claim of disease-prediction or treatment efficacy follows.

## Preserved freezes and limits

The original source-first outputs and all 30 files bound by the initial diagnosis freeze remain byte-for-byte unchanged. SC-01 (**vitious**, not the reviewer’s initial **viscous**) and SC-02 (**she longs after**, not the initial **he** anchor) remain disclosed. The candidate was correct on those readings. IC-01, the nonunique inheritance of the fiery-sign condition into the Venus/Mars continuation, remains as previously diagnosed; unchanged R1601 was not newly adjudicated.

No candidate or canonical file was changed. Work and new evidence remain in the private `repair_round01/` directory. No other-worker narrative, reconciliation or status summaries were read, no agent inventory was used, and no additional review scope was introduced. The modern byline date was assessed using the provided task metadata; no mid-task clock read or fabricated completion time was used.

This is same-family contextual diagnostic review. It is not cross-family, expert, clinical, IV&V or empirical validation. If a follow-up is requested, the existing policy allows at most one remaining changed-item repair check, limited to the metadata-reference correction and resulting bindings.

## Artifacts

- `CHANGED_ITEM_RESULTS.json`: per-finding decisions, exact changed claim objects, record-field differences, remaining correction and acceptance recommendation.
- `MECHANICAL_CARRY_FORWARD.json`: all file, record, ledger, code, test and index comparisons, plus prior-freeze integrity checks.
- `REPAIR_REPORT_RESIDUAL.txt`: report after masking all42 bound ledger units.
- `REPAIR_ROUND01_FREEZE.json`: hashes and byte counts for the completed result and direct original-source crops.
'''
(Q/'REPAIR_ROUND01_RESULT.md').write_text(md)
paths=['REPAIR_ROUND01_RESULT.md','CHANGED_ITEM_RESULTS.json','MECHANICAL_CARRY_FORWARD.json','REPAIR_REPORT_RESIDUAL.txt','check_repair_round01.py','finalize_repair_round01.py','original_pdf293_no_sickness_and_cause.png','original_pdf294_plural_exclusions_pagebreak.png','original_pdf283_earlier_sign_selector.png','original_pdf300_eighth_house_sign.png','original_pdf301_later_disease_selector.png']
freeze={'stage':'changed-item repair round1','candidate_manifest':bind(P2,'CANDIDATE_MANIFEST.json'),'initial_diagnosis_freeze':bind(I,'INITIAL_DIAGNOSIS_FREEZE.json'),'files':[bind(Q,n) for n in paths],'coverage':coverage,'acceptance_recommendation':'IF-01 through IF-06 resolved; MC-01 title/byline binding repaired; one C42 evidence-reference packaging correction RR1-01 remains. Root retains final adjudication.','remaining_corrections':['RR1-01'],'source_first_and_initial_diagnosis_unchanged':True,'semantic_findings_sent_before_this_freeze':False,'time_policy':'No completion timestamp claimed; no mid-task clock read.','review_policy':'First of at most two changed-item repair checks; no new exhaustive pass or added gates.'}
save('REPAIR_ROUND01_FREEZE.json',freeze)
for f in freeze['files']:assert bind(Q,f['path'])==f
print(json.dumps({'freeze':bind(Q,'REPAIR_ROUND01_FREEZE.json'),'artifacts':[bind(Q,n) for n in paths[:3]],'findings_resolved':[x['finding'] for x in checks if x['status']=='resolved'],'remaining_corrections':['RR1-01']},indent=2))
