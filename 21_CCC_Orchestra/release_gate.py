def evaluate(checks: dict[str,bool]) -> dict:
    failed=sorted([k for k,v in checks.items() if v is not True])
    return {"pass":not failed,"state":"READY_FOR_HUMAN_REVIEW" if not failed else "HOLD_WITH_DEFECTS","failed":failed}
