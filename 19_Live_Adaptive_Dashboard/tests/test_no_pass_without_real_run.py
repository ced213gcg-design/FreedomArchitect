import json,sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_run,valid_bridge
from soc_scenario_adapter import scenario_summary

def test_three_nominal_pass_rows_without_evidence_do_not_create_pass(monkeypatch,tmp_path):
    runs=[valid_run('DET-01',f'run-{i}',state='PASS',evidence=False) for i in range(3)]
    path=tmp_path/'bridge.json'; path.write_text(json.dumps(valid_bridge(runs)))
    monkeypatch.setenv('CCC_BRIDGE_PAYLOAD_PATH',str(path))
    row=next(x for x in scenario_summary()['scenarios'] if x['id']=='DET-01')
    assert row['state']=='UNKNOWN'
    assert row['runs_real']==0

def test_no_bridge_means_all_scenarios_unknown(monkeypatch,tmp_path):
    monkeypatch.setenv('CCC_BRIDGE_PAYLOAD_PATH',str(tmp_path/'missing.json'))
    summary=scenario_summary()
    assert summary['real_scenario_count']==0
    assert all(x['state']=='UNKNOWN' for x in summary['scenarios'])
