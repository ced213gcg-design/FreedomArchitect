from importlib import import_module
m=import_module("25_CCC_Exception_Intelligence.exception_engine")
def test_exception_score_visible_and_weighted():
    r=m.exception_score({"strategic_value":100,"time_sensitivity":80,"probability":80,"economic_upside":60,"capability_alignment":90,"confidence":80,"reinjection_value":70})
    assert r["score"]==85.5 and r["classification"]=="HIGH PRIORITY" and "formula" in r and len(r["components"])==7
