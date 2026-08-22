REQUIRED_END_FIELDS = ["shift_id", "worker", "ended_at", "starting_position", "completed_outcomes", "evidence", "unresolved_items", "final_state", "where_work_stopped", "next_owner", "exact_next_action", "expected_next_evidence", "lessons_reinjection", "cost_summary"]

def validate_end_shift(report: dict):
    missing = [k for k in REQUIRED_END_FIELDS if k not in report or report[k] in (None, "")]
    if report.get("report_type") != "END_SHIFT_HANDOFF":
        missing.append("report_type=END_SHIFT_HANDOFF")
    return {"valid": not missing, "missing": missing, "next_state_recorded": bool(report.get("next_owner") and report.get("exact_next_action"))}
