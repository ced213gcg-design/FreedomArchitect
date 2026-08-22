from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gt',ROOT/'26_CCC_Game_Theory'/'engine.py')
gt=importlib.util.module_from_spec(spec); spec.loader.exec_module(gt)


def test_missing_material_fields_seeks_evidence_not_execution():
    result=gt.analyze({'players':['CCC']})
    assert result['status']=='HOLD'
    assert result['recommendation']=='SEEK_EVIDENCE'
    assert result['authority']=='ADVISORY_ONLY'
    assert result['can_execute'] is False
    assert result['can_write_verified_ledger_truth'] is False
