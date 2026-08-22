from __future__ import annotations

import importlib.util
from pathlib import Path
from state_store import repo_path


def _engine():
    path=repo_path('26_CCC_Game_Theory','engine.py')
    spec=importlib.util.spec_from_file_location('ccc_game_theory_engine',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyze(payload: dict) -> dict:
    return _engine().analyze(payload)


def recent() -> dict:
    return {
        'state':'NO_RUNTIME_STRATEGIC_ANALYSES_RECORDED',
        'authority':'ADVISORY_ONLY',
        'analyses':[],
        'note':'Game Theory results do not become Ledger truth without separate evidence validation.'
    }
