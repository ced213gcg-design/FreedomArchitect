from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
_path=ROOT/"23_CCC_Agent_Mesh"/"approvals.py"
_spec=importlib.util.spec_from_file_location("ccc_mesh_approvals",_path)
_mod=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
create_request=_mod.create_request
