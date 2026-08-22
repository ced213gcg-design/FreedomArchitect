from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'19_Live_Adaptive_Dashboard'/'backend'))
from crayola_adapter import current,normalize


def test_crayola_has_seven_stages_and_valid_terminal_types():
    c=current()
    assert len(c['stages'])==7
    assert set(c['terminal_output_types'])=={'EVIDENCE','CAPABILITY','MEMORY','SEED','DOCUMENTED_REJECTION'}


def test_unvalidated_crayola_cannot_become_ledger_truth():
    result=normalize({
        'question':'Is this claim proven?',
        'terminal_output_type':'EVIDENCE',
        'sources':['source-a'],
        'yielded_evidence':['artifact-a'],
        'validated':False,
        'confidence':0.9,
    })
    assert result['authority']=='ADVISORY'
    assert result['ledger_truth_allowed'] is False


def test_validated_cycle_requires_sources_and_evidence():
    incomplete=normalize({'question':'q','terminal_output_type':'EVIDENCE','validated':True,'confidence':1})
    assert incomplete['ledger_truth_allowed'] is False
    complete=normalize({'question':'q','terminal_output_type':'EVIDENCE','validated':True,'sources':['s'],'yielded_evidence':['e'],'confidence':1})
    assert complete['ledger_truth_allowed'] is True
    assert complete['authority']=='VALIDATED_EVIDENCE'
