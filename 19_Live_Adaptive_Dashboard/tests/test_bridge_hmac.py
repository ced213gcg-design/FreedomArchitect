import hashlib,hmac,json,sys
from pathlib import Path
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path[:0]=[str(TESTS),str(BACK)]
from physical_test_helpers import valid_bridge
from evidence_bridge import validate_payload

def test_valid_hmac_is_accepted():
    payload=valid_bridge(); raw=json.dumps(payload,separators=(',',':')).encode(); token='A'*48
    sig='sha256='+hmac.new(token.encode(),raw,hashlib.sha256).hexdigest()
    assert validate_payload(payload,raw,token,sig)==[]

def test_wrong_hmac_is_rejected():
    payload=valid_bridge(); raw=json.dumps(payload,separators=(',',':')).encode(); token='B'*48
    errors=validate_payload(payload,raw,token,'sha256='+'0'*64)
    assert 'INVALID_HMAC' in errors
