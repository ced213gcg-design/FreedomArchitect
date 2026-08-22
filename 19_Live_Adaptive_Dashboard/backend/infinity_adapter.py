from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import yaml

from state_store import manifest, repo_path


def _workers() -> dict:
    path = repo_path('config', 'ccc-constitutional-workers.yaml')
    return yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}


def state() -> dict:
    m = manifest()
    gamma = (m.get('lifecycle_infinity') or {}).get('gamma') or {}
    frozen = (m.get('release') or {}).get('frozen_physical_candidate') or {}
    return {
        'composition': m.get('composition', {}),
        'creator_alignment': m.get('creator_alignment', []),
        'decision_triad': (m.get('governance') or {}).get('decision_triad', []),
        'evidence_sextet': (m.get('governance') or {}).get('evidence_sextet', []),
        'completion_nonet': m.get('completion_nonet', []),
        'historical_completion_cycle': (m.get('governance') or {}).get('completion_cycle', []),
        'lifecycle': (m.get('lifecycle_infinity') or {}).get('sequence', []),
        'gamma': gamma,
        'symbolic_cadence': m.get('symbolic_cadence', {}),
        'five_workers': (m.get('five_worker_constitution') or {}).get('workers', []),
        'ledger_authority': (m.get('authority') or {}).get('ledger'),
        'game_theory_authority': (m.get('game_theory_contract') or {}).get('authority'),
        'physical_candidate': frozen,
        'pressure_loss': {
            'principle': 'WEAKEST_VERIFIED_MATERIAL_DIMENSION',
            'hard_control_override': True,
        },
        'state': 'BUILD',
        'validation': 'DECLARED_INFINITY_CONSTITUTION_NOT_RUNTIME_OMEGA',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def lifecycle() -> dict:
    m = manifest()
    return {
        'historical': (m.get('governance') or {}).get('lifecycle', []),
        'infinity': (m.get('lifecycle_infinity') or {}).get('sequence', []),
        'gamma': (m.get('lifecycle_infinity') or {}).get('gamma', {}),
        'omega_rule': (m.get('reinjection_contract') or {}).get('omega_requires', []),
        'reconciliation_rule': 'MACRO_STATE_MUST_RECONCILE_WITH_MICRO_STATE',
    }


def workers() -> dict:
    cfg = _workers()
    return {
        'exact_worker_count': cfg.get('exact_worker_count'),
        'workers': cfg.get('workers', []),
        'truth_authority': cfg.get('truth_authority'),
        'consensus_creates_truth': cfg.get('consensus_creates_truth'),
        'conflict_precedence': cfg.get('conflict_precedence', []),
    }


def handoffs() -> dict:
    cfg = _workers()
    return {
        'mid_shift_required': cfg.get('mid_shift_required', []),
        'end_shift_required': cfg.get('end_shift_required', []),
        'authority': 'ADVISORY_TO_LEDGER_AUTHORITY',
        'records': [],
        'state': 'NO_RUNTIME_HANDOFFS_RECORDED',
    }
