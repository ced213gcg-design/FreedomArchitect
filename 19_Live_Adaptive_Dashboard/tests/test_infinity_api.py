from pathlib import Path
import sys,json

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'19_Live_Adaptive_Dashboard'/'backend'))
import app


def decode(result):
    status,headers,payload=result
    return status,json.loads(payload.decode())


def test_infinity_read_endpoints_are_available():
    for path in [
        '/api/infinity/state','/api/infinity/lifecycle','/api/infinity/reinjection',
        '/api/crayola/current','/api/game-theory/recent','/api/workers/constitutional',
        '/api/workers/handoffs'
    ]:
        status,data=decode(app.route_request('GET',path))
        assert status==200, (path,data)


def test_game_theory_post_is_advisory_only():
    payload={
      'players':['CCC','environment'],
      'objectives':{'CCC':'progress','environment':'response'},
      'constraints':['human authority'],
      'information_by_player':{'CCC':['ledger'],'environment':['unknown']},
      'information_asymmetry':['external intent'],
      'strategies':['act','hold'],
      'costs':{'act':1},
      'payoffs':{'act':'conditional'},
      'likely_response':'environment adapts',
      'second_order_response':'CCC reassesses',
      'repeated_game_effects':'learning compounds',
      'reputation_cooperation_effects':'restraint affects trust',
      'hard_controls':[],
      'no_play_option':'hold',
      'evidence_change_trigger':['new verified evidence'],
      'evidence_confidence':0.8
    }
    status,data=decode(app.route_request('POST','/api/game-theory/analyze',payload))
    assert status==200
    assert data['authority']=='ADVISORY_ONLY'
    assert data['can_execute'] is False
    assert data['can_write_verified_ledger_truth'] is False


def test_mechanism_gate_post_does_not_execute():
    status,data=decode(app.route_request('POST','/api/economics/mechanism-gate',{'question':'internal evidence'}))
    assert status==200
    assert data['executed'] is False
    assert data['authority']=='ADVISORY_ONLY'
