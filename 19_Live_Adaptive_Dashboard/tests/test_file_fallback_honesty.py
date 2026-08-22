import json,sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent
ROOT=TESTS.parents[1]
BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'
sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_bridge
from soc_adapter import SocAdapter

def test_sanitized_file_import_keeps_fallback_label(monkeypatch,tmp_path):
    bridge=tmp_path/'ccc-soc-bridge-payload.json'
    bridge.write_text(json.dumps(valid_bridge()),encoding='utf-8')
    monkeypatch.setenv('CCC_BRIDGE_PAYLOAD_PATH',str(bridge))
    state=SocAdapter(path=tmp_path/'missing-live-state.json').get_state()
    assert state['connected'] is True
    assert state['bridge_mode']=='FILE_FALLBACK'
    assert state['validation'].startswith('VALID_FILE_FALLBACK')
