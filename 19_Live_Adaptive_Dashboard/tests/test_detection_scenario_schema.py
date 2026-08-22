import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
TESTS=Path(__file__).resolve().parent; ROOT=TESTS.parents[1]; sys.path.insert(0,str(TESTS))
from physical_test_helpers import valid_run

def test_detection_run_schema_accepts_real_bounded_record():
    schema=json.loads((ROOT/'20_CCC_Living_Organism'/'schemas'/'soc-detection-run.schema.json').read_text())
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(valid_run()))
    assert errors==[]

def test_detection_run_schema_rejects_synthetic_true():
    schema=json.loads((ROOT/'20_CCC_Living_Organism'/'schemas'/'soc-detection-run.schema.json').read_text())
    row=valid_run(); row['synthetic']=True
    assert list(Draft202012Validator(schema).iter_errors(row))
