import sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_bridge
from evidence_bridge import validate_sanitized_payload

def test_bridge_rejects_unknown_command_field():
    payload=valid_bridge(); payload['command_to_execute']='whoami'
    errors=validate_sanitized_payload(payload)
    assert any('command_to_execute' in e.lower() for e in errors)

def test_bridge_rejects_nested_shell_field():
    payload=valid_bridge(); payload['vm_health']=[{'name':'x','shell':'cmd.exe'}]
    errors=validate_sanitized_payload(payload)
    assert any('forbidden_field:shell' in e.lower() for e in errors)
