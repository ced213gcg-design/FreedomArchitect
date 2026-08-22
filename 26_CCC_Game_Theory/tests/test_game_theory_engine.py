from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gt',ROOT/'26_CCC_Game_Theory'/'engine.py')
gt=importlib.util.module_from_spec(spec); spec.loader.exec_module(gt)


def payload():
    return {
        'players':['CCC','environment'],
        'objectives':{'CCC':'verified progress','environment':'respond to CCC action'},
        'constraints':['human authority'],
        'information_by_player':{'CCC':['ledger evidence'],'environment':['external state']},
        'information_asymmetry':['external response uncertain'],
        'strategies':['act','hold'],
        'costs':{'act':1,'hold':0},
        'payoffs':{'act':'conditional upside','hold':'preserve optionality'},
        'likely_response':'environment adapts after CCC acts',
        'second_order_response':'CCC must observe the adaptation',
        'repeated_game_effects':'reputation and learning compound across rounds',
        'reputation_cooperation_effects':'predictable restraint improves cooperation',
        'hard_controls':[],
        'no_play_option':'hold until evidence improves',
        'evidence_change_trigger':['new verified runtime evidence'],
        'evidence_confidence':0.8,
    }


def test_engine_answers_both_required_questions():
    result=gt.analyze(payload())
    assert result['authority']=='ADVISORY_ONLY'
    assert result['can_execute'] is False
    assert result['can_write_verified_ledger_truth'] is False
    assert result['will_this_work']
    assert result['what_happens_after_we_act']
    assert result['likely_response']
    assert result['repeated_game_effects']
    assert result['reputation_cooperation_effects']
