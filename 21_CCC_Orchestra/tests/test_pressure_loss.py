import importlib.util
from pathlib import Path
M=Path(__file__).resolve().parents[1]/"pressure_loss.py"; s=importlib.util.spec_from_file_location("pressure_loss",M); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_minimum_is_pressure_loss():
    r=m.calculate({"Progress":80,"Evidence":55,"Compliance":90,"Resilience":70,"EconomicValue":75})
    assert r["PressureLoss"]==55 and r["weakest_dimension"]=="Evidence"
