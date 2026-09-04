from pathlib import Path
import yaml
def load_matrix(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
def internal_evidence_decision(path):
    data=load_matrix(path); case=data["example_decisions"]["ccc_internal_evidence"]
    return case
