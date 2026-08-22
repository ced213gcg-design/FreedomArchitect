import json,sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_bridge
from soc_scenario_adapter import sensor_inventory

def test_sensor_inventory_comes_only_from_sanitized_physical_payload(monkeypatch,tmp_path):
    payload=valid_bridge(); payload['sensor_health']=[{'sensor':'Sysmon','host':'ccc-dell-compute-01','installed':True,'running':True,'source_path_channel':'Microsoft-Windows-Sysmon/Operational','freshness':'OBSERVED_NOW','scenario_support':['DET-05'],'state':'AVAILABLE'}]
    path=tmp_path/'bridge.json'; path.write_text(json.dumps(payload))
    monkeypatch.setenv('CCC_BRIDGE_PAYLOAD_PATH',str(path))
    inv=sensor_inventory()
    assert inv['state']=='AVAILABLE' and inv['count']==1
    assert inv['source']=='SANITIZED_BRIDGE_PAYLOAD'
