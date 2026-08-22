from __future__ import annotations

from uuid import uuid4

TERMINAL_TYPES = {'EVIDENCE','CAPABILITY','MEMORY','SEED','DOCUMENTED_REJECTION'}


def current() -> dict:
    return {
        'state': 'IDLE',
        'authority': 'ADVISORY',
        'stages': ['CORRECT_CROSS_EXAMINE','RESEARCH','ANALYZE','YIELD_EVIDENCE','OBSERVE','LEARN','AMEND_RECYCLE'],
        'terminal_output_types': sorted(TERMINAL_TYPES),
        'ledger_truth_allowed_without_validation': False,
        'active_cycle': None,
    }


def normalize(payload: dict) -> dict:
    terminal = str(payload.get('terminal_output_type','')).upper()
    validated = bool(payload.get('validated', False))
    sources = list(payload.get('sources') or [])
    evidence = list(payload.get('yielded_evidence') or [])
    accepted = terminal in TERMINAL_TYPES and bool(payload.get('question'))
    ledger_allowed = accepted and validated and bool(sources) and bool(evidence)
    return {
        'cycle_id': payload.get('cycle_id') or f'crayola-{uuid4()}',
        'question': payload.get('question',''),
        'current_assumption': payload.get('current_assumption',''),
        'cross_examination': list(payload.get('cross_examination') or []),
        'sources': sources,
        'analysis': payload.get('analysis',''),
        'yielded_evidence': evidence,
        'observation': payload.get('observation',''),
        'lesson': payload.get('lesson',''),
        'amendment': payload.get('amendment',''),
        'terminal_output_type': terminal if terminal in TERMINAL_TYPES else 'DOCUMENTED_REJECTION',
        'confidence': max(0.0,min(1.0,float(payload.get('confidence',0.0)))),
        'authority': 'VALIDATED_EVIDENCE' if ledger_allowed else 'ADVISORY',
        'validated': ledger_allowed,
        'ledger_truth_allowed': ledger_allowed,
        'accepted': accepted,
    }
