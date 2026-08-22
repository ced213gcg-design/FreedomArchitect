import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path.insert(0,str(BACK))
from soc_mission_adapter import five_missions
from soc_scenario_adapter import scenario_summary

def test_control_gates_and_detection_scenarios_are_distinct(monkeypatch,tmp_path):
    monkeypatch.setenv('CCC_SOC_STATE_PATH',str(tmp_path/'missing-state.json'))
    monkeypatch.setenv('CCC_BRIDGE_PAYLOAD_PATH',str(tmp_path/'missing-bridge.json'))
    gates=five_missions(); scenarios=scenario_summary()
    gate_ids={x['id'] for x in gates['missions']}; scenario_ids={x['id'] for x in scenarios['scenarios']}
    assert gates['group']=='SOC_CONTROL_GATES'
    assert scenarios['group']=='SOC_DETECTION_SCENARIOS'
    assert gate_ids=={'SOC-01','SOC-02','SOC-03','SOC-04','SOC-05'}
    assert scenario_ids=={'DET-01','DET-02','DET-03','DET-04','DET-05'}
    assert gate_ids.isdisjoint(scenario_ids)
