import sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_bridge
from evidence_bridge import validate_payload,MAX_PAYLOAD

def test_payload_over_one_mib_is_rejected_before_processing():
    payload=valid_bridge(); raw=b'x'*(MAX_PAYLOAD+1)
    assert validate_payload(payload,raw,'A'*48,'sha256='+'0'*64)==['PAYLOAD_TOO_LARGE']
