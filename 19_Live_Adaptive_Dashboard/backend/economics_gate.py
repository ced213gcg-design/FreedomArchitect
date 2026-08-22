from __future__ import annotations

from pathlib import Path
from uuid import uuid4
import yaml

DISTINCTIONS={
    'blockchain != cryptocurrency',
    'blockchain != money',
    'token != money',
    'ledger entry != settlement',
    'database != distributed ledger',
    'opportunity != revenue',
    'invoice != collected cash',
    'collected cash != reconciled realized revenue',
}


def load_matrix(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))


def internal_evidence_decision(path):
    data=load_matrix(path)
    case=data['example_decisions']['ccc_internal_evidence']
    return {**case,'distinctions':sorted(DISTINCTIONS),'authority':'ADVISORY_ONLY','executed':False}


def evaluate_mechanism(path, proposal: dict) -> dict:
    data=load_matrix(path)
    dimensions=list(data.get('dimensions') or [])
    choices=dict(data.get('choices') or {})
    supplied=dict(proposal.get('dimensions') or {})
    evaluated={name:supplied.get(name,'UNKNOWN') for name in dimensions}
    verified_requirements=list(proposal.get('verified_requirements') or [])
    consensus=bool(proposal.get('consensus_required', False)) or str(evaluated.get('consensus_requirement','')).upper() in {'TRUE','REQUIRED','YES'}
    settlement=bool(proposal.get('settlement_required', False)) or str(evaluated.get('settlement_finality','')).upper() in {'TRUE','REQUIRED','YES'}
    multi_party=bool(proposal.get('multi_party_untrusted_writers', False))

    if consensus and settlement and multi_party:
        recommendation=['E']
        if proposal.get('public_verifiability_required'):
            recommendation=['F']
        blockchain_required=True
        rejection='NONE'
        reason='Verified multi-party consensus and settlement requirements may justify a distributed-ledger option; further legal, privacy, governance, recovery and performance validation remains required.'
    else:
        recommendation=['B','C']
        blockchain_required=False
        rejection='BLOCKCHAIN_NOT_REQUIRED'
        reason='No verified requirement currently proves that blockchain or consensus is necessary beyond a signed/hash-linked append-only or event-sourced trusted-operator architecture.'

    return {
        'gate_id': proposal.get('gate_id') or f'mech-{uuid4()}',
        'question': proposal.get('question') or 'What is the simplest architecture that satisfies the verified requirement?',
        'dimensions': evaluated,
        'candidate_technologies': choices,
        'verified_requirements': verified_requirements,
        'distinctions': sorted(DISTINCTIONS),
        'recommendation': recommendation,
        'reason': reason,
        'blockchain_required': blockchain_required,
        'documented_rejection': rejection,
        'authority': 'ADVISORY_ONLY',
        'executed': False,
    }
