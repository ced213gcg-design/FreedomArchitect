from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]/"coordinator"
def load(name):
    p=ROOT/f"{name}.py"; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_missing_runtime_metrics_stay_unknown():
    out=load("pressure").workforce_pressure([{"id":"command","Progress":None,"Evidence":None,"Compliance":None,"Resilience":None,"EconomicValue":None}])
    assert out["workers"][0]["PressureLoss"] is None
    assert out["system_weakest"] is None

def test_security_offline_holds_consequential_placement():
    online={"command":True,"intelligence":True,"security":False,"revenue":True,"communications":True}
    out=load("placement").place("CUSTOMER_OPPORTUNITY",online,consequential=True)
    assert out["status"]=="HOLD"
