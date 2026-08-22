from importlib import import_module
m=import_module("25_CCC_Exception_Intelligence.routing")
def test_high_priority_routes_to_mission_control():
    r=m.route_exception({"freshness_state":"VERIFIED","exception_score":{"score":88},"type":"EMPLOYMENT","risk":"MEDIUM","approval_required":True}); assert r["target"]=="mission-control-agent" and r["queue"]=="HIGH_PRIORITY"
def test_stale_routes_hold_even_with_high_score():
    assert m.route_exception({"freshness_state":"STALE","exception_score":{"score":99},"type":"MARKET","risk":"LOW","approval_required":False})["queue"]=="HOLD"
def test_critical_security_overrides_commercial_queue():
    r=m.route_exception({"freshness_state":"VERIFIED","exception_score":{"score":40},"type":"SECURITY","risk":"CRITICAL","approval_required":False}); assert r["queue"]=="SECURITY_PRIORITY" and r["approval_required"] is True
