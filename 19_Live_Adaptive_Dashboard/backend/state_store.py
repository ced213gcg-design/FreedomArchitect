from pathlib import Path
import json, os, yaml
ROOT=Path(__file__).resolve().parents[2]
def repo_path(*parts): return ROOT.joinpath(*parts)
def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def read_yaml(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
def manifest(): return read_json(repo_path("20_CCC_Living_Organism","ccc.manifest.json"))
def hosts(): return read_yaml(repo_path("20_CCC_Living_Organism","host-registry.yaml"))
def agents(): return read_yaml(repo_path("23_CCC_Agent_Mesh","registry.yaml"))
def ledger_path(): return Path(os.getenv("CCC_LEDGER_PATH", repo_path("runtime","ccc-ledger.jsonl")))
