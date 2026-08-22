from __future__ import annotations

TERMINAL_VALUES={'EVIDENCE','CAPABILITY','MEMORY','SEED','DOCUMENTED_REJECTION'}
OMEGA_REQUIRES={'PROVED','USEFUL','SAFE','DOCUMENTED','REPEATABLE','MEASURED','EVIDENCE_BOUND'}


def current() -> dict:
    return {
        'state':'NO_RUNTIME_OMEGA_CAPSULE_RECORDED',
        'omega_requires':sorted(OMEGA_REQUIRES),
        'terminal_values':sorted(TERMINAL_VALUES),
        'next_alpha_required':True,
        'capsules':[],
        'authority':'LEDGER_VALIDATION_REQUIRED'
    }


def evaluate_capsule(payload: dict) -> dict:
    evidence=list(payload.get('final_evidence') or [])
    recipe=list(payload.get('replication_recipe') or [])
    terminal=str(payload.get('terminal_value','')).upper()
    next_alpha=str(payload.get('next_alpha','')).strip()
    requirements=set(str(x).upper() for x in payload.get('omega_proof',[]))
    omega_ready=OMEGA_REQUIRES.issubset(requirements) and bool(evidence) and bool(recipe) and terminal in TERMINAL_VALUES and bool(next_alpha)
    return {
        'omega_candidate':omega_ready,
        'missing_omega_proof':sorted(OMEGA_REQUIRES-requirements),
        'terminal_value':terminal if terminal in TERMINAL_VALUES else None,
        'reinjection_destination':payload.get('reinjection_destination'),
        'next_alpha':next_alpha or None,
        'authority':'ADVISORY_UNTIL_LEDGER_VALIDATED',
        'executed':False,
    }
