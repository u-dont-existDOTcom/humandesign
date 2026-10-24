"""C18 ordinal source comparison, no predictions."""
import json
from pathlib import Path
from paulus_bysign_papyrus_c04 import sign_monomoiria
from oxy4277_monomoiria_audit_c05 import P_OXY_4277

SOURCE=Path(__file__).with_name('P_OXY_C18_ORDINAL_PARITY_AND_CHRONOLOGY_V1.json')
TOLSA_METHODS=('Tolsa_Paulus32','Tolsa_Olymp34','Tolsa_ValensIV26','Tolsa_mixed')

def load_witness():
    return json.loads(SOURCE.read_text(encoding='utf-8'))

def audit_ordinal_and_source_methods():
    data=load_witness()
    records=[]
    for old,item in zip(P_OXY_4277,data['labels']):
        sign=item['sign']
        degree=item['degree']
        minute=item['minutes']
        correct=sign_monomoiria(sign,degree,minute)
        truncated=sign_monomoiria(sign,degree-1,minute)
        variants={'C05_correct_ordinal':correct,'C05_completed_degree_ordinal':truncated}
        variants.update({key:item[key] for key in TOLSA_METHODS})
        labels=dict(object=item['object'],reported=item['reported'])
        labels['variants']=variants
        labels['matches']={name:(value==item['reported']) for name,value in variants.items()}
        labels['Valens_equals_truncated']=(item['Tolsa_ValensIV26']==truncated)
        records.append(labels)
    names=records[0]['variants'].keys()
    counts={name:sum(r['matches'][name] for r in records) for name in names}
    equal_valens=sum(r['Valens_equals_truncated'] for r in records)
    return {'kind':'HISTORICAL_SOURCE_COMPARISON_ONLY','records':records,
            'agreements':counts,'Valens_truncated_equivalences':equal_valens,
            'pre_Paulus_document':True,'glyphs_redeciphered':0,
            'human_predictive_validations':0,'model_promoted':False}

if __name__=='__main__':
    print(json.dumps(audit_ordinal_and_source_methods(),indent=2))
