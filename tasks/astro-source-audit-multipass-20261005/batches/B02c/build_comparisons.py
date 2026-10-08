"""Compare preserved source allocations; choose neither source as the winner."""
import hashlib
import json
from pathlib import Path
from lilly_sign_dignity_reference import DATA, PROFILE, SIGNS, compare_earlier_enumerations, ordinal_term
ROOT=Path(__file__).resolve().parent

def main():
    fixtures=json.loads((ROOT/'COMPARISON_INPUTS.json').read_text())
    old=compare_earlier_enumerations(fixtures['earlier_enumerations'])
    other=fixtures['robbins_terms']
    differences=[]; same=[]; row_comparisons=[]
    for s in SIGNS:
        a=DATA['terms'][s];b=other[s]
        if a==b:same.append(s)
        row_comparisons.append({'sign':s,'lilly_p104':a,'robbins_p107':b})
        for n in range(1,31):
            x=ordinal_term(s,n,profile=PROFILE)
            y=next(p for p,end in b if n<=end)
            if x!=y:differences.append({'sign':s,'numbered_cell':n,'lilly':x,'robbins':y})
    result={
      'schema_version':1,'scope':'source-allocation comparison, not prediction accuracy',
      'earlier_planets_sha256':fixtures['earlier_planets_sha256'],
      'lilly_p104_table_sha256':hashlib.sha256((ROOT/'DIGNITY_TABLE_P104.json').read_bytes()).hexdigest(),
      'earlier_vs_later_lilly':old,
      'robbins_vs_lilly':{'robbins_pdf_page':131,'robbins_printed_page':107,'lilly_pdf_page':138,'lilly_printed_page':104,
        'rows':row_comparisons,'compared_numbered_cells':360,'different_numbered_cells':len(differences),
        'different_arc_length_if_uniform_degree_segments':len(differences),'identical_sign_rows':same,'differences':differences,
        'interpretation':'The two tables labelled according to Ptolemy are not identical. This does not establish which better represents Ptolemy or which predicts better. Manuscript/translation history not independently adjudicated.',
        'coordinate_limit':fixtures['coordinate_note']},
      'earlier_source_mutated':False,'runtime_promotions':0,'empirical_validations':0,
    }
    (ROOT/'TABLE_COMPARISONS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Earlier/later Lilly:',old['comparison']['terms']['differences_count'],'term cells;',old['comparison']['faces']['differences_count'],'face cells')
    print('Lilly/Robbins:',len(differences),'of360 numbered cells; identical rows:',same)
if __name__=='__main__':main()
