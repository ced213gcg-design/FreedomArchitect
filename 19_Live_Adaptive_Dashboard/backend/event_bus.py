from pathlib import Path
import json
from jsonschema import Draft202012Validator, FormatChecker
def validate(event,schema_path):
    schema=json.loads(Path(schema_path).read_text(encoding="utf-8")); v=Draft202012Validator(schema,format_checker=FormatChecker()); errors=sorted(v.iter_errors(event),key=lambda e:list(e.path)); return {"valid":not errors,"errors":[e.message for e in errors]}
