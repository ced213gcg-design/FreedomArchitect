from datetime import datetime,timezone,timedelta
from importlib import import_module
m=import_module("25_CCC_Exception_Intelligence.freshness")
def test_stale_leaves_verified():
    now=datetime(2026,8,22,tzinfo=timezone.utc); e={"type":"EMPLOYMENT","last_verified":(now-timedelta(hours=80)).isoformat(),"freshness_state":"VERIFIED"}
    r=m.evaluate_freshness(e,{"default":{"verified_max_hours":24,"aging_max_hours":72,"stale_archive_after_hours":168},"types":{}},now); assert r["freshness_state"]=="STALE"
def test_security_ages_faster():
    now=datetime(2026,8,22,tzinfo=timezone.utc); p={"default":{"verified_max_hours":24,"aging_max_hours":72,"stale_archive_after_hours":168},"types":{"SECURITY":{"verified_max_hours":1,"aging_max_hours":6,"stale_archive_after_hours":24}}}
    assert m.evaluate_freshness({"type":"SECURITY","last_verified":(now-timedelta(hours=2)).isoformat()},p,now)["freshness_state"]=="AGING"
