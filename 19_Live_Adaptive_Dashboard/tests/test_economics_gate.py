import yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_internal_evidence_does_not_require_blockchain(): d=yaml.safe_load((ROOT/"22_CCC_Ledger"/"economics"/"technology-choice-matrix.yaml").read_text()); assert d["example_decisions"]["ccc_internal_evidence"]["blockchain_required"] is False
