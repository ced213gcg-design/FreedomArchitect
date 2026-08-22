from pathlib import Path
import json, yaml
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]

def test_five_workers_registered_and_unique():
    data = yaml.safe_load((ROOT / "workforce.yaml").read_text(encoding="utf-8"))
    workers = data["workers"]
    assert len(workers) == 5
    assert {w["id"] for w in workers} == {"command", "intelligence", "security", "revenue", "communications"}
    assert len({w["identity_ref"] for w in workers}) == 5

def test_worker_schema_validates_all_workers():
    schema = json.loads((ROOT / "schemas" / "worker.schema.json").read_text(encoding="utf-8"))
    data = yaml.safe_load((ROOT / "workforce.yaml").read_text(encoding="utf-8"))
    for worker in data["workers"]:
        validate(worker, schema)
