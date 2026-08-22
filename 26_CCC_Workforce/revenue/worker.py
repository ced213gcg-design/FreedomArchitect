from pathlib import Path
import yaml
WORKER_ID = "revenue"
def describe():
    root = Path(__file__).resolve().parents[1]
    workforce = yaml.safe_load((root / "workforce.yaml").read_text(encoding="utf-8"))
    policy = yaml.safe_load((Path(__file__).with_name("policy.yaml")).read_text(encoding="utf-8"))
    worker = next(w for w in workforce["workers"] if w["id"] == WORKER_ID)
    return {**worker, "policy": policy}
