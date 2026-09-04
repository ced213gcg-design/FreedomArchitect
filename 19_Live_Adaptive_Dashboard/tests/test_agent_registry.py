import yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_registry_has_no_self_registration(): d=yaml.safe_load((ROOT/"23_CCC_Agent_Mesh"/"registry.yaml").read_text()); assert d["self_registration"] is False and len(d["agents"])>=8
