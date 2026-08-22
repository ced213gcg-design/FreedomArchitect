from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'19_Live_Adaptive_Dashboard'/'backend'))
from reinjection_adapter import evaluate_capsule,current


def test_incomplete_capsule_is_not_omega_candidate():
    r=evaluate_capsule({'terminal_value':'SEED','next_alpha':'A2','omega_proof':['PROVED']})
    assert r['omega_candidate'] is False
    assert r['executed'] is False


def test_complete_capsule_can_become_candidate_but_not_execute():
    proof=['PROVED','USEFUL','SAFE','DOCUMENTED','REPEATABLE','MEASURED','EVIDENCE_BOUND']
    r=evaluate_capsule({
      'final_evidence':['artifact:sha256:x'],
      'replication_recipe':['repeat verified procedure'],
      'terminal_value':'CAPABILITY',
      'reinjection_destination':'NEXT_ALPHA',
      'next_alpha':'A2',
      'omega_proof':proof
    })
    assert r['omega_candidate'] is True
    assert r['authority']=='ADVISORY_UNTIL_LEDGER_VALIDATED'
    assert r['executed'] is False


def test_reinjection_terminal_values_are_bounded():
    assert set(current()['terminal_values'])=={'EVIDENCE','CAPABILITY','MEMORY','SEED','DOCUMENTED_REJECTION'}
