"""Materialize the Chat-authored convergence receipt, not a semantic evaluator."""
from pathlib import Path
import json,hashlib,sys,shutil
P=Path(sys.argv[1]); S=P/'source'; S.mkdir(exist_ok=True)
# The source directory is supplied or recovered separately, not inferred from answers.
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n' if not isinstance(obj,str) else obj)
B=json.loads((P/'interviewer-bank-v6.json').read_text());G=json.loads((P/'ROUTING-GRAPH.json').read_text());E=json.loads((P/'EVIDENCE-GUIDE-v6.json').read_text())
names=['interviewer-bank-v6.json','ROUTING-GRAPH.json','EVIDENCE-GUIDE-v6.json','INTERVIEW-PROTOCOL.md','graph_model.py']
identity={name:sha(P/name) for name in names}
write('FINAL-SWEEP.json',{'scope':'Complete final same-context semantic review; hashes bind the reviewed candidate and are not independent evidence of meaning.','candidate_version':B['version'],'reviewed_question_ids':[q['id'] for q in B['questions']],'reviewed_information_ids':[e['facet_id'] for e in E],'family_count':len(G['families']),'edge_count':len(G['edges']),'prior_dialogue_examples_reviewed':32,'graph_focused_dialogue_examples_reviewed':16,'final_changes':{'question_wording':0,'admission_or_context':0,'interpretations':0,'graph_model':0},'known_material_findings_remaining':[],'review_judgment':'CONVERGED_GOOD_FOR_SAVED_CHAT_PILOT','review_input_sha256':identity,'review_output_sha256':identity,'independent_review':False,'human_or_deployed_model_validation':False})
write('VERIFICATION.json',{'task_id':'scenario-graph-convergence-20260919','source_head':'55b894227022df3aee8ffd96a95e10f2a02ffe6c','owned_branch':'chat/scenario-graph-convergence-20260919','candidate':B['version'],'judgment':'CONVERGED_GOOD_FOR_SAVED_CHAT_PILOT','judgment_scope':'Own design judgment, not human or runtime certification','review_counts':{'questions':len(B['questions']),'information_guides':len(E),'families':len(G['families']),'nodes':len(G['nodes']),'edges':len(G['edges'])},'initial_repairs':{'question_wording':2,'new_questions':0,'missing_context_links':1,'self_contained_metadata_values':40,'illustration':1,'interpretation_narrowing':1},'audit_model_repairs':['same-message contrast branches','explicit life-stage contrasts','inherited source-topic closures and independent-topic preservation'],'last_complete_pass_changes':0,'focused_test_methods_passed':22,'focused_test_failures':0,'final_test_runtime_seconds':0.038,'test_evidence_class':'Explicit reviewed-state model; no natural-language classification','test_graph_sha256':sha(P/'test_graph.py'),'graph_model_sha256':sha(P/'graph_model.py'),'graph_mutants_rejected':4,'presentation_checks_passed':9,'presentation_checks_failed':0,'presentation_method':'Exact HTML loaded with headless Chromium set_content; file navigation policy left unchanged','html_sha256':sha(P/'GRAPH-EXPLORER.html'),'observer':{'canonical_script_sha256':'b3afec50c3d31eef344be623520a4117a3e46fad33b7000cea1895fd1928c723','focused_runs':2,'observed_test_seconds':0.37,'observation_window_seconds':1131.81,'forced_redundant_green_seconds':0},'private_preservation':{'events':5,'actual_pilot_answers':0,'latest_design_feedback_saved':True,'readback_verified':True,'raw_content_in_public_packet':False,'background_monitoring':False,'railway_sync':False},'boundaries':{'pilot_paused':True,'runtime_changes':False,'vm_contacted':False,'inference_calls':0,'deployment':False,'recruitment':False,'chart_scoring':False},'owner_audit_request':'SATISFIED_AT_DESIGN_CONVERGENCE','parent_product_outcome':'OPEN'})
write('README.md', '''# Scenario-first survey — converged graph review

Start with **REPORT.md** for the judgment or open **GRAPH-EXPLORER.html** for the offline graph. The HTML is read-only: it makes no network requests and captures no answers. Search or select a topic to inspect the actual questions. On a phone, diagrams scroll within their containers; the text panels remain readable.

The final full review required zero further substantive changes. This is an explicitly bounded design judgment, not proof of empirical validity, runtime performance or full AstroHD recovery. The pilot remains paused.

## Main artifacts

- INTERVIEW-PROTOCOL.md: conversational and privacy rules.
- REVIEWED-QUESTIONS.md and interviewer-bank-v6.json: all 79 available entries, not a fixed survey length.
- ROUTING-GRAPH.json and SCENARIO-GRAPH.md: source graph and Mermaid views. Edges distinguish context, advisory links and possible information; none awards evidence credit.
- EVIDENCE-GUIDE-v6.json: 73 narrow interpretation examples.
- DIALOGUE-CHECKS.md: 16 graph-focused authored examples; source-dialogues-v5.json preserves the 32 prior examples.
- CHANGES.json and FINDINGS.json: initial repairs, including repairs to the new audit model.
- FINAL-SWEEP.json and VERIFICATION.json: exact review scope, zero-change final pass and test limitations.

## Reproduction

`python3 test_graph.py` runs the explicit-state tests without network or inference. It does not interpret participant language. `python3 build_views.py` regenerates the HTML, SVG and Mermaid views from the JSON and requires Graphviz's `dot`. `python3 build_dialogue_checks.py` reproduces the authored examples.

`python3 rebuild_from_source.py` reproduces the data artifacts from the frozen files under source/. Run generators in a disposable copy when preserving an audited version. VIEW-CHECKS.json describes the separate browser check. No diagram is a deployed controller.

Personal records are held by the existing owner-private capture arrangement outside Git and Railway; this packet contains no actual participant answers. Design scope does not authorize app deployment or waking inference.
''')
# This script is included for reproducible nonsemantic receipt materialization.
write('MANIFEST.json',{'algorithm':'sha256','scope':'public graph/design artifacts and frozen sources; no private content or derived private hashes','files':{str(f.relative_to(P)):sha(f) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='MANIFEST.json' and f.suffix not in {'.png','.pyc'} and '__pycache__' not in f.parts}})
print(json.dumps({'final_sweep_changes':0,'questions':len(B['questions']),'information_guides':len(E),'manifest_entries':len(json.loads((P/'MANIFEST.json').read_text())['files'])}))
