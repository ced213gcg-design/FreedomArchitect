REQUIRED=("SOURCE","TIME","OWNER","CHANGE","VALIDATION","PROVENANCE")
def evaluate(evidence: dict) -> dict:
    missing=[k for k in REQUIRED if not evidence.get(k)]
    return {"pass":not missing,"missing":missing,"state":"PASS" if not missing else "HOLD"}
