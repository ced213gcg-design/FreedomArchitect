from pathlib import Path
import sys,yaml

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'19_Live_Adaptive_Dashboard'/'backend'))
from economics_gate import evaluate_mechanism,DISTINCTIONS

MATRIX=ROOT/'22_CCC_Ledger'/'economics'/'technology-choice-matrix.yaml'


def test_fourteen_dimensions_and_candidate_set_A_to_I():
    result=evaluate_mechanism(MATRIX,{'question':'internal evidence'})
    assert len(result['dimensions'])==14
    assert set(result['candidate_technologies'])==set('ABCDEFGHI')
    assert result['authority']=='ADVISORY_ONLY'
    assert result['executed'] is False


def test_no_consensus_requirement_prefers_simpler_architecture():
    result=evaluate_mechanism(MATRIX,{
        'question':'Do we need blockchain for internal evidence?',
        'verified_requirements':['tamper-evident audit history'],
        'consensus_required':False,
        'settlement_required':False,
        'multi_party_untrusted_writers':False,
    })
    assert result['blockchain_required'] is False
    assert result['recommendation']==['B','C']
    assert result['documented_rejection']=='BLOCKCHAIN_NOT_REQUIRED'


def test_distinction_rules_prevent_conflation():
    required={
        'blockchain != cryptocurrency','blockchain != money','token != money',
        'ledger entry != settlement','database != distributed ledger',
        'opportunity != revenue','invoice != collected cash','collected cash != reconciled realized revenue'
    }
    assert required.issubset(DISTINCTIONS)
