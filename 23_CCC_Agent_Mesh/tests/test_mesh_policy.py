import importlib.util
from pathlib import Path
M=Path(__file__).resolve().parents[1]/"agent_mesh.py"; s=importlib.util.spec_from_file_location("agent_mesh_policy",M); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_unknown_agent_rejected(): assert m.authorize("does-not-exist","read_code")["allowed"] is False
def test_registered_action_allowed(): assert m.authorize("github-agent","read_code")["allowed"] is True
def test_unregistered_action_denied(): assert m.authorize("dashboard-agent","direct_privileged_execution")["allowed"] is False
