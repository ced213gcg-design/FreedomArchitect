from __future__ import annotations

import importlib.util
from state_store import repo_path

_RECENT=[]
_MAX_RECENT=25


def _engine():
    path=repo_path('26_CCC_Game_Theory','engine.py')
    spec=importlib.util.spec_from_file_location('ccc_game_theory_engine',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyze(payload: dict) -> dict:
    result=_engine().analyze(payload)
    if result.get('analysis_id'):
        _RECENT.append(result)
        if len(_RECENT)>_MAX_RECENT:
            del _RECENT[:-_MAX_RECENT]
    return result


def recent() -> dict:
    return {
        'state':'ADVISORY_RUNTIME_MEMORY' if _RECENT else 'NO_RUNTIME_STRATEGIC_ANALYSES_RECORDED',
        'authority':'ADVISORY_ONLY',
        'persistence':'PROCESS_LOCAL_NON_AUTHORITATIVE',
        'analyses':list(reversed(_RECENT)),
        'note':'Game Theory results do not become Ledger truth without separate evidence validation.'
    }
