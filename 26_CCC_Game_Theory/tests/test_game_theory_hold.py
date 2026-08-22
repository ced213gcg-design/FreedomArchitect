from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gt',ROOT/'26_CCC_Game_Theory'/'engine.py')
gt=importlib.util.module_from_spec(spec); spec.loader.exec_module(gt)


def test_security_hold_overrides_payoff():
    payload={
        'players':['CCC','counterparty'],
        'objectives':{'CCC':'value','counterparty':'response'},
        'constraints':['security'],
        'information_by_player':{'CCC':['verified evidence'],'counterparty':['unknown']},
        'information_asymmetry':['unknown counterparty intent'],
        'strategies':['act','hold'],
        'costs':{'act':1},
        'payoffs':{'act':999999},
        'likely_response':'counterparty reacts',
        'second_order_response':'system must reassess',
        'repeated_game_effects':'future trust changes',
        'reputation_cooperation_effects':'restraint protects reputation',
        'hard_controls':['SECURITY_HOLD'],
        'no_play_option':'do nothing',
        'evidence_change_trigger':['security hold cleared by evidence'],
        'evidence_confidence':1.0,
        'proposed_recommendation':'ACT'
    }
    result=gt.analyze(payload)
    assert result['recommendation']=='HOLD'
    assert result['reason']=='hard_control_precedence'
    assert result['executed'] is False
