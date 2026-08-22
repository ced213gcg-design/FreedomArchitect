from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=json.loads((ROOT/'20_CCC_Living_Organism'/'ccc.manifest.json').read_text(encoding='utf-8'))


def test_369_counts_and_historical_preservation():
    assert len(MANIFEST['governance']['decision_triad'])==3
    assert len(MANIFEST['governance']['evidence_sextet'])==6
    assert len(MANIFEST['completion_nonet'])==9
    assert MANIFEST['completion_nonet'][-1]=='OPERATIONALIZE / REINVEST'
    assert len(MANIFEST['governance']['completion_cycle'])==10
    assert any(x['field']=='governance.completion_cycle' for x in MANIFEST['supersession_history'])


def test_creator_alignment_and_gamma():
    assert len(MANIFEST['creator_alignment'])==9
    assert MANIFEST['creator_alignment'][0]=='TRUTH'
    lifecycle=MANIFEST['lifecycle_infinity']
    assert lifecycle['sequence']==['ALPHA','BETA','GAMMA','OMEGA','REINJECTION','NEXT_ALPHA']
    assert lifecycle['gamma']['is_pass'] is False
    assert 'PROMOTE_TO_OMEGA_CANDIDATE' in lifecycle['gamma']['outcomes']
    assert 'RETURN_TO_BETA' in lifecycle['gamma']['outcomes']


def test_symbolic_cadence_is_not_telemetry():
    cadence=MANIFEST['symbolic_cadence']
    assert cadence['ui_cadence_ms']==963
    assert cadence['telemetry_independent'] is True
    assert 'Operational telemetry uses evidence-grounded timing.' in cadence['operator_notice']
    assert MANIFEST['governance']['heartbeat']['critical_telemetry_independent'] is True
