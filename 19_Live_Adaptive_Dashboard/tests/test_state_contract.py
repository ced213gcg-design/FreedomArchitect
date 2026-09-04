import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
def test_all_schemas_are_valid():
    for p in (ROOT/"20_CCC_Living_Organism"/"schemas").glob("*.json"): Draft202012Validator.check_schema(json.loads(p.read_text()))
def test_manifest_states_are_legal():
    m=json.loads((ROOT/"20_CCC_Living_Organism"/"ccc.manifest.json").read_text()); allowed=set(m["state_model"]["allowed"]); assert all(o["state"] in allowed for o in m["organs"])
