from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'19_Live_Adaptive_Dashboard'/'backend'))
import app


def test_no_operational_timeout_or_sleep_depends_on_963():
    backend='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'19_Live_Adaptive_Dashboard'/'backend').glob('*.py'))
    forbidden=['sleep(0.963','timeout=0.963','retry_ms=963','poll_ms=963','interval_ms=963']
    assert not any(x in backend for x in forbidden)


def test_pressure_loss_exposes_causal_operator_fields():
    status,headers,payload=app.route_request('GET','/api/pressure-loss')
    data=json.loads(payload.decode())
    assert status==200
    assert data['principle']=='WEAKEST_VERIFIED_MATERIAL_DIMENSION'
    assert data['hard_control_override'] is True
    assert data['system_weakest'] is not None
    for key in ['constraint','owner','state_change_evidence','evidence_basis']:
        assert key in data['system_weakest']
