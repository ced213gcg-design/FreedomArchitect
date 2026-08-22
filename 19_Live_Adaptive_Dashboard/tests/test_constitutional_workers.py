from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]
CFG=yaml.safe_load((ROOT/'config'/'ccc-constitutional-workers.yaml').read_text(encoding='utf-8'))


def test_exactly_five_constitutional_workers_no_sixth_worker():
    workers=[w['id'] for w in CFG['workers']]
    assert workers==['COMMAND','INTELLIGENCE','SECURITY','REVENUE','COMMS']
    assert CFG['exact_worker_count']==5
    assert len(workers)==5
    assert len(set(workers))==5


def test_shift_contracts_and_truth_boundary():
    assert set(CFG['mid_shift_required'])=={'starting_position','work_completed_so_far','evidence','current_position','blockers','immediate_next_action'}
    assert set(CFG['end_shift_required'])=={'starting_position','work_completed','evidence','current_position','blockers','where_work_stopped','next_owner','exact_next_action','expected_next_evidence'}
    assert CFG['truth_authority']=='LEDGER'
    assert CFG['consensus_creates_truth'] is False
    assert CFG['security_hold_can_override_commercial_enthusiasm'] is True
