from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def _load_routing():
    path=ROOT/"25_CCC_Exception_Intelligence"/"routing.py"; spec=importlib.util.spec_from_file_location("ccc_exception_routing",path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
routing=_load_routing()
def evaluate(exception:dict)->dict:
    routed=routing.route_exception(exception)
    return {"exception_id":exception.get("exception_id"),"from":"exception-intelligence-agent",**routed,"ledger_required":True,"human_authority_preserved":True}
